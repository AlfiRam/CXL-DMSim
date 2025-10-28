#include "dev/storage/cxl_memory.hh"

#include "arch/x86/regs/int.hh"
#include "base/trace.hh"
#include "cpu/thread_context.hh"
#include "debug/CXLMemory.hh"

namespace gem5
{

CXLMemory::CXLResponsePort::CXLResponsePort(const std::string& _name,
                                        CXLMemory& _cxlMemory,
                                        CXLRequestPort& _memReqPort,
                                        Cycles _protoProcLat, int _resp_limit,
                                        AddrRange _cxlMemRange)
    : ResponsePort(_name), cxlMemory(_cxlMemory),
    memReqPort(_memReqPort), protoProcLat(_protoProcLat),
    cxlMemRange(_cxlMemRange), outstandingResponses(0),
    retryReq(false), respQueueLimit(_resp_limit),
    sendEvent([this]{ trySendTiming(); }, _name)
{
}

CXLMemory::CXLRequestPort::CXLRequestPort(const std::string& _name,
                                    CXLMemory& _cxlMemory,
                                    CXLResponsePort& _cxlRspPort,
                                    Cycles _protoProcLat, int _req_limit)
    : RequestPort(_name), cxlMemory(_cxlMemory),
    cxlRspPort(_cxlRspPort),
    protoProcLat(_protoProcLat), reqQueueLimit(_req_limit),
    sendEvent([this]{ trySendTiming(); }, _name)
{
}

CXLMemory::CXLMemory(const Params &p)
    : PciDevice(p),
    cxlRspPort(p.name + ".cxl_rsp_port", *this, memReqPort,
            ticksToCycles(p.proto_proc_lat), p.rsp_size, p.cxl_mem_range),
    memReqPort(p.name + ".mem_req_port", *this, cxlRspPort,
            ticksToCycles(p.proto_proc_lat), p.req_size),
    nmpMemPort(p.name + ".nmp_mem_port", *this),
    preRspTick(0),
    enableNMP(p.enable_nmp),
    nmpCPU(nullptr),
    nmpTC(nullptr),
    nmpStartAddr(p.nmp_start_addr),
    nmpBinaryPath(p.nmp_binary),
    stats(*this),
    nmpStats(*this)
    {
        DPRINTF(CXLMemory, "BAR0_addr:0x%lx, BAR0_size:0x%lx\n",
            p.BAR0->addr(), p.BAR0->size());

        if (enableNMP) {
            DPRINTF(CXLMemory, "NMP enabled: binary=%s, start_addr=0x%x\n",
                    nmpBinaryPath.c_str(), nmpStartAddr);
        } else {
            DPRINTF(CXLMemory, "NMP disabled\n");
        }
    }

CXLMemory::CXLCtrlStats::CXLCtrlStats(CXLMemory &_cxlMemory)
    : statistics::Group(&_cxlMemory),

      ADD_STAT(reqQueFullEvents, statistics::units::Count::get(),
               "Number of times the request queue has become full"),
      ADD_STAT(reqRetryCounts, statistics::units::Count::get(),
               "Number of times the request was sent for retry"),
      ADD_STAT(rspQueFullEvents, statistics::units::Count::get(),
               "Number of times the response queue has become full"),
      ADD_STAT(reqSendFaild, statistics::units::Count::get(),
               "Number of times the request send failed"),
      ADD_STAT(rspSendFaild, statistics::units::Count::get(),
               "Number of times the response send failed"),
      ADD_STAT(reqSendSucceed, statistics::units::Count::get(),
               "Number of times the request send succeeded"),
      ADD_STAT(rspSendSucceed, statistics::units::Count::get(),
               "Number of times the response send succeeded"),
      ADD_STAT(reqQueueLenDist, "Request queue length distribution (Count)"),
      ADD_STAT(rspQueueLenDist, "Response queue length distribution (Count)"),
      ADD_STAT(rspOutStandDist, "outstandingResponses distribution (Count)"),
      ADD_STAT(reqQueueLatDist, "Response queue latency distribution (Tick)"),
      ADD_STAT(rspQueueLatDist, "Response queue latency distribution (Tick)"),
      ADD_STAT(memToCXLCtrlRsp, "Distribution of the time intervals between "
               "consecutive mem responses from the memory media to the CXLCtrl (Cycle)")
{
    reqQueueLenDist
        .init(0, 49, 10)
        .flags(statistics::nozero);
    rspQueueLenDist
        .init(0, 49, 10)
        .flags(statistics::nozero);
    rspOutStandDist
        .init(0, 49, 10)
        .flags(statistics::nozero);
    reqQueueLatDist
        .init(12000, 41999, 1000)
        .flags(statistics::nozero);
    rspQueueLatDist
        .init(12000, 41999, 1000)
        .flags(statistics::nozero);
    memToCXLCtrlRsp
        .init(0, 299, 10)
        .flags(statistics::nozero);
}

CXLMemory::NMPStats::NMPStats(CXLMemory &_cxlMemory)
    : statistics::Group(&_cxlMemory),
      ADD_STAT(nmpMemReads, statistics::units::Count::get(),
               "Number of memory reads from NMP CPU"),
      ADD_STAT(nmpMemWrites, statistics::units::Count::get(),
               "Number of memory writes from NMP CPU"),
      ADD_STAT(nmpAccessLatency, statistics::units::Tick::get(),
               "NMP memory access latency distribution (ns)"),
      ADD_STAT(nmpActiveCycles, statistics::units::Cycle::get(),
               "Total cycles NMP CPU has been active"),
      ADD_STAT(nmpExecutions, statistics::units::Count::get(),
               "Number of times NMP CPU execution was started")
{
    nmpAccessLatency
        .init(0, 500, 10)  // 0-500ns in 10ns buckets
        .flags(statistics::nozero);
}

CXLMemory::NMPMemPort::NMPMemPort(const std::string& _name,
                                    CXLMemory& _device)
    : RequestPort(_name), cxlMemory(_device), portName(_name)
{
    DPRINTF(CXLMemory, "NMPMemPort created: %s\n", _name.c_str());
}

bool
CXLMemory::NMPMemPort::recvTimingResp(PacketPtr pkt)
{
    // Receive memory response from backend and forward to NMP CPU
    // This bypasses CXL protocol - direct local access!

    DPRINTF(CXLMemory, "NMP received memory response addr=0x%x, size=%d\n",
            pkt->getAddr(), pkt->getSize());

    // Calculate and record access latency
    Tick latency = curTick() - pkt->req->time();
    cxlMemory.nmpStats.nmpAccessLatency.sample(latency);

    // Update read/write statistics
    if (pkt->isRead()) {
        cxlMemory.nmpStats.nmpMemReads++;
        DPRINTF(CXLMemory, "NMP read complete: addr=0x%x\n", pkt->getAddr());
    } else if (pkt->isWrite()) {
        cxlMemory.nmpStats.nmpMemWrites++;
        DPRINTF(CXLMemory, "NMP write complete: addr=0x%x\n", pkt->getAddr());
    }

    // Forward response to NMP CPU if it exists
    if (cxlMemory.nmpCPU != nullptr) {
        // In a real implementation, would forward to CPU's data port
        // For now, just acknowledge the response
        delete pkt;
        return true;
    }

    delete pkt;
    return true;
}

void
CXLMemory::NMPMemPort::recvReqRetry()
{
    DPRINTF(CXLMemory, "NMP received retry from backend memory\n");
    // Handle retry - would retry pending requests
    // For now, just log it
}

Port &
CXLMemory::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "cxl_rsp_port")
        return cxlRspPort;
    else if (if_name == "mem_req_port")
        return memReqPort;
    else if (if_name == "nmp_mem_port") {
        if (enableNMP) {
            DPRINTF(CXLMemory, "Returning NMP memory port\n");
            return nmpMemPort;
        } else {
            panic("NMP memory port requested but NMP is disabled!");
        }
    }
    else if (if_name == "dma")
        return dmaPort;
    else
        return PioDevice::getPort(if_name, idx);
}

void
CXLMemory::init()
{
    if (!cxlRspPort.isConnected() || !memReqPort.isConnected())
        panic("CXL port of %s not connected to anything!", name());

    cxlRspPort.sendRangeChange();
}

AddrRangeList
CXLMemory::getAddrRanges() const
{
    return PciDevice::getAddrRanges();
}

bool
CXLMemory::CXLResponsePort::respQueueFull() const
{
    if (outstandingResponses == respQueueLimit) {
        cxlMemory.stats.rspQueFullEvents++;
        return true;
    } else {
        return false;
    }
}

bool
CXLMemory::CXLRequestPort::reqQueueFull() const
{
    if (transmitList.size() == reqQueueLimit) {
        cxlMemory.stats.reqQueFullEvents++;
        return true;
    } else {
        return false;
    }
}

bool
CXLMemory::CXLRequestPort::recvTimingResp(PacketPtr pkt)
{
    // all checks are done when the request is accepted on the response
    // side, so we are guaranteed to have space for the response
    DPRINTF(CXLMemory, "recvTimingResp: %s addr 0x%x\n",
            pkt->cmdString(), pkt->getAddr());

    DPRINTF(CXLMemory, "Request queue size: %d\n", transmitList.size());

    if (cxlMemory.preRspTick == -1) {
        cxlMemory.preRspTick = cxlMemory.clockEdge();
    } else {
        cxlMemory.stats.memToCXLCtrlRsp.sample(
            cxlMemory.ticksToCycles(cxlMemory.clockEdge() - cxlMemory.preRspTick));
        cxlMemory.preRspTick = cxlMemory.clockEdge();
    }

    // technically the packet only reaches us after the header delay,
    // and typically we also need to deserialise any payload
    Tick receive_delay = pkt->headerDelay + pkt->payloadDelay;
    pkt->headerDelay = pkt->payloadDelay = 0;

    cxlRspPort.schedTimingResp(pkt, cxlMemory.clockEdge(protoProcLat) +
                              receive_delay);

    return true;
}

bool
CXLMemory::CXLResponsePort::recvTimingReq(PacketPtr pkt)
{
    DPRINTF(CXLMemory, "recvTimingReq: %s addr 0x%x\n",
            pkt->cmdString(), pkt->getAddr());

    panic_if(pkt->cacheResponding(), "Should not see packets where cache "
             "is responding");

    if (retryReq)
        return false;

    DPRINTF(CXLMemory, "Response queue size: %d outresp: %d\n",
            transmitList.size(), outstandingResponses);

    // if the request queue is full then there is no hope
    if (memReqPort.reqQueueFull()) {
        DPRINTF(CXLMemory, "Request queue full\n");
        retryReq = true;
    } else {
        // look at the response queue if we expect to see a response
        bool expects_response = pkt->needsResponse();
        if (expects_response) {
            if (respQueueFull()) {
                DPRINTF(CXLMemory, "Response queue full\n");
                retryReq = true;
            } else {
                // ok to send the request with space for the response
                DPRINTF(CXLMemory, "Reserving space for response\n");
                assert(outstandingResponses != respQueueLimit);
                ++outstandingResponses;

                // no need to set retryReq to false as this is already the
                // case
                cxlMemory.stats.rspOutStandDist.sample(outstandingResponses);
            }
        }

        if (!retryReq) {
            Tick receive_delay = pkt->headerDelay + pkt->payloadDelay;
            pkt->headerDelay = pkt->payloadDelay = 0;

            memReqPort.schedTimingReq(pkt, cxlMemory.clockEdge(protoProcLat) +
                                      receive_delay);
        }
    }

    // remember that we are now stalling a packet and that we have to
    // tell the sending requestor to retry once space becomes available,
    // we make no distinction whether the stalling is due to the
    // request queue or response queue being full
    return !retryReq;
}

void
CXLMemory::CXLResponsePort::retryStalledReq()
{
    if (retryReq) {
        DPRINTF(CXLMemory, "Request waiting for retry, now retrying\n");
        retryReq = false;
        sendRetryReq();
        cxlMemory.stats.reqRetryCounts++;
    }
}

void
CXLMemory::CXLRequestPort::schedTimingReq(PacketPtr pkt, Tick when)
{
    // If we're about to put this packet at the head of the queue, we
    // need to schedule an event to do the transmit.  Otherwise there
    // should already be an event scheduled for sending the head
    // packet.
    if (transmitList.empty()) {
        cxlMemory.schedule(sendEvent, when);
    }

    assert(transmitList.size() != reqQueueLimit);

    transmitList.emplace_back(pkt, when);

    cxlMemory.stats.reqQueueLenDist.sample(transmitList.size());
}

void
CXLMemory::CXLResponsePort::schedTimingResp(PacketPtr pkt, Tick when)
{
    if (transmitList.empty()) {
        cxlMemory.schedule(sendEvent, when);
    }

    transmitList.emplace_back(pkt, when);

    cxlMemory.stats.rspQueueLenDist.sample(transmitList.size());
}

void
CXLMemory::CXLRequestPort::trySendTiming()
{
    assert(!transmitList.empty());

    DeferredPacket req = transmitList.front();

    assert(req.tick <= curTick());

    PacketPtr pkt = req.pkt;

    DPRINTF(CXLMemory, "trySend request addr 0x%x, queue size %d\n",
            pkt->getAddr(), transmitList.size());

    if (sendTimingReq(pkt)) {
        // send successful
        cxlMemory.stats.reqSendSucceed++;
        cxlMemory.stats.reqQueueLatDist.sample(curTick() - req.entryTime);

        transmitList.pop_front();

        cxlMemory.stats.reqQueueLenDist.sample(transmitList.size());
        DPRINTF(CXLMemory, "trySend request successful\n");

        // If there are more packets to send, schedule event to try again.
        if (!transmitList.empty()) {
            DeferredPacket next_req = transmitList.front();
            DPRINTF(CXLMemory, "Scheduling next send\n");
            cxlMemory.schedule(sendEvent, std::max(next_req.tick,
                                                cxlMemory.clockEdge()));
        }

        // if we have stalled a request due to a full request queue,
        // then send a retry at this point, also note that if the
        // request we stalled was waiting for the response queue
        // rather than the request queue we might stall it again
        cxlRspPort.retryStalledReq();
    } else {
        cxlMemory.stats.reqSendFaild++;
    }

    // if the send failed, then we try again once we receive a retry,
    // and therefore there is no need to take any action
}

void
CXLMemory::CXLResponsePort::trySendTiming()
{
    assert(!transmitList.empty());

    DeferredPacket resp = transmitList.front();

    assert(resp.tick <= curTick());

    PacketPtr pkt = resp.pkt;

    DPRINTF(CXLMemory, "trySend response addr 0x%x, outstanding %d\n",
            pkt->getAddr(), outstandingResponses);

    if (sendTimingResp(pkt)) {
        // send successful
        cxlMemory.stats.rspSendSucceed++;
        cxlMemory.stats.rspQueueLatDist.sample(curTick() - resp.entryTime);

        transmitList.pop_front();

        cxlMemory.stats.rspQueueLenDist.sample(transmitList.size());
        DPRINTF(CXLMemory, "trySend response successful\n");

        assert(outstandingResponses != 0);
        --outstandingResponses;

        cxlMemory.stats.rspOutStandDist.sample(outstandingResponses);

        // If there are more packets to send, schedule event to try again.
        if (!transmitList.empty()) {
            DeferredPacket next_resp = transmitList.front();
            DPRINTF(CXLMemory, "Scheduling next send\n");
            cxlMemory.schedule(sendEvent, std::max(next_resp.tick,
                                                cxlMemory.clockEdge()));
        }

        // if there is space in the request queue and we were stalling
        // a request, it will definitely be possible to accept it now
        // since there is guaranteed space in the response queue
        if (!memReqPort.reqQueueFull() && retryReq) {
            DPRINTF(CXLMemory, "Request waiting for retry, now retrying\n");
            retryReq = false;
            sendRetryReq();
            cxlMemory.stats.reqRetryCounts++;
        }
    } else {
        cxlMemory.stats.rspSendFaild++;
    }

    // if the send failed, then we try again once we receive a retry,
    // and therefore there is no need to take any action
}

void
CXLMemory::CXLRequestPort::recvReqRetry()
{
    trySendTiming();
}

void
CXLMemory::CXLResponsePort::recvRespRetry()
{
    trySendTiming();
}

Tick
CXLMemory::CXLResponsePort::recvAtomic(PacketPtr pkt)
{
    DPRINTF(CXLMemory, "CXLMemory recvAtomic: %s AddrRange: %s\n",
            pkt->cmdString(), pkt->getAddrRange().to_string());
    panic_if(pkt->cacheResponding(), "Should not see packets where cache "
             "is responding");

    Cycles delay = processCXLMem(pkt);

    Tick access_delay = memReqPort.sendAtomic(pkt);

    DPRINTF(CXLMemory, "access_delay=%ld, proto_proc_lat=%ld, total=%ld\n",
            access_delay, delay, delay * cxlMemory.clockPeriod() + access_delay);
    return delay * cxlMemory.clockPeriod() + access_delay;
}

Tick
CXLMemory::CXLResponsePort::recvAtomicBackdoor(
    PacketPtr pkt, MemBackdoorPtr &backdoor)
{
    Cycles delay = processCXLMem(pkt);

    return delay * cxlMemory.clockPeriod() + memReqPort.sendAtomicBackdoor(
        pkt, backdoor);
}

Cycles
CXLMemory::CXLResponsePort::processCXLMem(PacketPtr pkt) {
    if (pkt->cxl_cmd == MemCmd::M2SReq) {
        assert(pkt->isRead());
    } else if (pkt->cxl_cmd == MemCmd::M2SRwD) {
        assert(pkt->isWrite());
    }
    return protoProcLat + protoProcLat;
}

AddrRangeList
CXLMemory::CXLResponsePort::getAddrRanges() const {
    AddrRangeList ranges = cxlMemory.getAddrRanges();
    ranges.push_back(cxlMemRange);
    return ranges;
}

// ============================================================================
// NMP CPU Implementation
// ============================================================================

void
CXLMemory::initNMPCPU()
{
    if (!enableNMP) {
        DPRINTF(CXLMemory, "NMP CPU disabled, skipping initialization\n");
        return;
    }

    inform("Initializing NMP CPU at CXL memory device %s\n", name().c_str());

    // Validate NMP port is connected to backend memory
    if (!nmpMemPort.isConnected()) {
        warn("NMP memory port not connected to backend memory!\n");
        warn("Please connect nmpMemPort to backend memory in "
             "configuration.\n");
        return;
    }

    // Check if CPU was provided via Python configuration
    if (nmpCPU == nullptr) {
        inform("NMP CPU not yet created. It should be instantiated "
               "in Python config.\n");
        inform("The CPU will be connected when created via "
               "setNMPCPU() method.\n");
        return;
    }

    // CPU exists - set up thread context
    if (nmpCPU->numThreads > 0) {
        nmpTC = nmpCPU->getContext(0);
        inform("NMP CPU thread context acquired: %s\n",
               nmpTC->getCpuPtr()->name());
    } else {
        warn("NMP CPU has no thread contexts!\n");
        nmpCPU = nullptr;
        return;
    }

    DPRINTF(CXLMemory, "NMP CPU initialization complete\n");
    DPRINTF(CXLMemory, "  CPU Type: %s\n", nmpCPU->name());
    DPRINTF(CXLMemory, "  Binary: %s\n", nmpBinaryPath.c_str());
    DPRINTF(CXLMemory, "  Start address: 0x%x\n", nmpStartAddr);
    DPRINTF(CXLMemory, "  Memory port connected: %s\n",
            nmpMemPort.isConnected() ? "yes" : "no");
}

void
CXLMemory::startNMPExecution(Addr startPC, Addr stackPtr)
{
    if (!enableNMP) {
        warn("Attempt to start NMP execution but NMP is disabled\n");
        return;
    }

    if (nmpCPU == nullptr) {
        warn("NMP CPU not initialized, cannot start execution\n");
        return;
    }

    if (nmpTC == nullptr) {
        warn("NMP thread context not available\n");
        return;
    }

    inform("Starting NMP CPU execution at PC=0x%x, SP=0x%x\n",
           startPC, stackPtr);

    // Increment execution counter
    nmpStats.nmpExecutions++;

    // Set up CPU registers for execution
    // PC (Program Counter) - where to start execution
    nmpTC->pcState(startPC);

    // For simplified implementation, we'll rely on the workload/process
    // to set up registers properly. Manual register setup requires
    // more detailed ISA-specific knowledge.
    //
    // In a full implementation, registers would be set up through:
    // - Process object (for SE mode)
    // - Workload initialization
    // - ISA-specific initialization routines

    // Activate the thread context to begin execution
    if (nmpTC->status() != ThreadContext::Active) {
        nmpTC->activate();
        inform("NMP CPU thread context activated\n");
    }

    // Record start time for tracking active cycles
    nmpStats.nmpActiveCycles = nmpCPU->curCycle();

    DPRINTF(CXLMemory, "NMP CPU execution started successfully\n");
    DPRINTF(CXLMemory, "  PC: 0x%x\n", startPC);
    DPRINTF(CXLMemory, "  SP: 0x%x\n", stackPtr);
    DPRINTF(CXLMemory, "  Thread status: %s\n",
            nmpTC->status() == ThreadContext::Active ? "Active" : "Other");

    inform("NMP CPU now executing benchmark independently from host\n");
}

bool
CXLMemory::handleNMPMemoryAccess(PacketPtr pkt)
{
    if (!enableNMP) {
        warn("NMP memory access received but NMP is disabled\n");
        return false;
    }

    DPRINTF(CXLMemory, "NMP memory access: addr=0x%x, cmd=%s, size=%d\n",
            pkt->getAddr(), pkt->cmdString(), pkt->getSize());

    // Forward request to backend memory via nmpMemPort
    // This bypasses the CXL controller for direct local access
    // Note: Latency will be measured in recvTimingResp using pkt->req->time()
    bool success = nmpMemPort.sendTimingReq(pkt);

    if (success) {
        DPRINTF(CXLMemory, "NMP memory request sent successfully\n");
    } else {
        DPRINTF(CXLMemory, "NMP memory request blocked, will retry\n");
    }

    return success;
}

} // namespace gem5
