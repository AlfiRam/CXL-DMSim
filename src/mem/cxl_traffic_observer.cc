/*
 * Copyright (c) 2026 CXL-NMP
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "mem/cxl_traffic_observer.hh"

#include <algorithm>

#include "base/logging.hh"
#include "base/trace.hh"
#include "debug/CxlTrafficObserver.hh"

namespace gem5
{

CxlTrafficObserver::CxlTrafficObserver(const Params &p)
    : ClockedObject(p),
      memSidePort(name() + ".mem_side_port", *this),
      cpuSidePort(name() + ".cpu_side_port", *this),
      system(p.system),
      observeRange(p.observe_addr, p.observe_addr + p.observe_size),
      lineSize(p.line_size),
      observedLineCount(p.line_size ? p.observe_size / p.line_size : 0),
      lineSeen(observedLineCount, false),
      lineSeenCount(0),
      stats(this)
{
}

void
CxlTrafficObserver::init()
{
    if (!cpuSidePort.isConnected() || !memSidePort.isConnected())
        fatal("CxlTrafficObserver %s is not connected on both sides.\n",
              name());

    if (lineSize == 0 || (lineSize & (lineSize - 1)) != 0)
        fatal("CxlTrafficObserver %s: line_size must be a power of two "
              "(got %u).\n", name(), lineSize);

    if (observeRange.size() == 0)
        fatal("CxlTrafficObserver %s: observed range is empty; an unset "
              "range would classify all traffic as out-of-range and the "
              "coverage figure would be silently meaningless.\n", name());

    if ((observeRange.size() % lineSize) != 0)
        fatal("CxlTrafficObserver %s: observed range %s is not a multiple "
              "of the %u-byte line.\n",
              name(), observeRange.to_string(), lineSize);

    // The observer counts only on the TIMING path, because that is the
    // only path a request takes as a discrete packet. Under KVM the CXL
    // ranges are mapped as a KVM memslot and guest accesses never become
    // packets at all, so a KVM-only flow would observe nothing. That is
    // reported rather than tolerated: the config refuses flag
    // combinations that can never reach TIMING, and the zero-traffic
    // warn in preDumpStats catches whatever slips past.
    const auto mode = system->getMemoryMode();
    if (mode != enums::timing) {
        inform("CxlTrafficObserver %s: memory mode is not 'timing' at "
               "init (atomic or atomic_noncaching); the observer counts "
               "only on the TIMING path and is dormant until (and "
               "unless) the run switches.\n", name());
    }

    inform("CxlTrafficObserver %s: observing %s (%llu lines of %u B); "
           "forwards every packet, acts on none, holds no counter.\n",
           name(), observeRange.to_string(),
           (unsigned long long)observedLineCount, lineSize);
}

Port &
CxlTrafficObserver::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "mem_side_port") {
        return memSidePort;
    } else if (if_name == "cpu_side_port") {
        return cpuSidePort;
    } else {
        return ClockedObject::getPort(if_name, idx);
    }
}

CxlTrafficObserver::ObserverResponsePort::ObserverResponsePort(
    const std::string &_name, CxlTrafficObserver &_parent)
    : ResponsePort(_name), parent(_parent)
{
}

CxlTrafficObserver::ObserverRequestPort::ObserverRequestPort(
    const std::string &_name, CxlTrafficObserver &_parent)
    : RequestPort(_name), parent(_parent)
{
}

bool
CxlTrafficObserver::ObserverResponsePort::recvTimingReq(PacketPtr pkt)
{
    // Classify BEFORE forwarding: on an accepted timing send the
    // receiver owns the packet. Observation reads nothing but the
    // command, the address range and the request flags -- never the
    // payload.
    parent.observe(pkt);
    return parent.memSidePort.sendTimingReq(pkt);
}

void
CxlTrafficObserver::ObserverResponsePort::recvRespRetry()
{
    parent.memSidePort.sendRetryResp();
}

Tick
CxlTrafficObserver::ObserverResponsePort::recvAtomic(PacketPtr pkt)
{
    // Forward only. Atomic accesses are not counted: they are not the
    // discrete-packet path the observability claim is about, and
    // counting them would mix two traffic models in one stat.
    return parent.memSidePort.sendAtomic(pkt);
}

Tick
CxlTrafficObserver::ObserverResponsePort::recvAtomicBackdoor(
    PacketPtr pkt, MemBackdoorPtr &backdoor)
{
    // Forward the access AND the backdoor request unchanged. Declining
    // it here would change what the requester downstream of the CXL
    // controller is offered, which is a behaviour change; this object
    // changes nothing.
    return parent.memSidePort.sendAtomicBackdoor(pkt, backdoor);
}

void
CxlTrafficObserver::ObserverResponsePort::recvFunctional(PacketPtr pkt)
{
    // Pure forward: the observer holds no packet and no data, so it can
    // satisfy nothing and must hide nothing.
    parent.memSidePort.sendFunctional(pkt);
}

AddrRangeList
CxlTrafficObserver::ObserverResponsePort::getAddrRanges() const
{
    return parent.memSidePort.getAddrRanges();
}

bool
CxlTrafficObserver::ObserverRequestPort::recvTimingResp(PacketPtr pkt)
{
    return parent.cpuSidePort.sendTimingResp(pkt);
}

void
CxlTrafficObserver::ObserverRequestPort::recvReqRetry()
{
    parent.cpuSidePort.sendRetryReq();
}

void
CxlTrafficObserver::ObserverRequestPort::recvRangeChange()
{
    parent.cpuSidePort.sendRangeChange();
}

void
CxlTrafficObserver::observe(PacketPtr pkt)
{
    stats.packetsObserved++;

    // Metadata FIRST, by the request tag rather than by address, so
    // verifier metadata traffic is never conflated with data. The tag
    // lives on the Request and survives every hop; exactly one site in
    // the tree sets it.
    if (pkt->req && pkt->req->getMetadataRequest()) {
        if (pkt->isRead()) {
            stats.metadataReads++;
        } else if (pkt->isWrite()) {
            stats.metadataWrites++;
        } else {
            stats.metadataOther++;
        }
        return;
    }

    const bool prefetch = pkt->req && pkt->req->isPrefetch();
    const AddrRange pktRange = pkt->getAddrRange();
    const bool inRange = observeRange.intersects(pktRange);

    DPRINTF(CxlTrafficObserver,
            "%s: %s %s%s (forwarded unchanged)\n",
            inRange ? "in-range" : "out-of-range", pkt->print(),
            prefetch ? "prefetch " : "demand ",
            pkt->hasData() ? "with-data" : "no-data");

    if (inRange) {
        if (prefetch) {
            stats.inPrefetches++;
        } else {
            stats.inDemand++;
        }
    } else {
        if (prefetch) {
            stats.outPrefetches++;
        } else {
            stats.outDemand++;
        }
    }

    // CleanEvict is called out on its own: it crosses this point with
    // neither IsWrite nor HasData, so an observer keyed on writes would
    // miss it entirely. Whether it is missed is itself a finding, which
    // is why it gets a stat rather than falling into "other".
    if (pkt->cmd == MemCmd::CleanEvict) {
        if (inRange) {
            stats.inCleanEvicts++;
        } else {
            stats.outCleanEvicts++;
        }
        return;
    }

    if (pkt->isRead() && !pkt->isWrite()) {
        if (inRange) {
            stats.inReads++;
        } else {
            stats.outReads++;
        }
        return;
    }

    if (pkt->isWrite()) {
        if (!inRange) {
            stats.outWritesWithData++;
            return;
        }
        if (pkt->cmd == MemCmd::WritebackDirty) {
            stats.inWritebackDirty++;
        } else if (pkt->cmd == MemCmd::WritebackClean) {
            stats.inWritebackClean++;
        } else if (pkt->cmd == MemCmd::WriteClean) {
            stats.inWriteClean++;
        } else {
            stats.inWritesOtherWithData++;
        }

        // Distinct-line coverage. One SATURATING bit per line -- set
        // membership, not a magnitude (see the class comment). Only
        // writes that actually carry data mark a line: a payload-less
        // command tells us nothing about the line's contents.
        if (!pkt->hasData()) {
            return;
        }
        const Addr lo = std::max(pktRange.start(), observeRange.start());
        const Addr hi = std::min(pktRange.end(), observeRange.end());
        for (Addr a = lo & ~((Addr)lineSize - 1); a < hi; a += lineSize) {
            if (a < observeRange.start()) {
                continue;
            }
            const uint64_t idx = (a - observeRange.start()) / lineSize;
            if (idx < lineSeen.size() && !lineSeen[idx]) {
                lineSeen[idx] = true;
                lineSeenCount++;
            }
        }
        return;
    }

    if (inRange) {
        stats.inOther++;
    } else {
        stats.outOther++;
    }
}

CxlTrafficObserver::CxlTrafficObserverStats::CxlTrafficObserverStats(
    CxlTrafficObserver *parent)
    : statistics::Group(parent, "cxl_traffic_observer"),
      parent(parent),
      ADD_STAT(metadataReads, statistics::units::Count::get(),
               "Verifier metadata reads (identified by request tag)"),
      ADD_STAT(metadataWrites, statistics::units::Count::get(),
               "Tagged metadata writes (none are generated today)"),
      ADD_STAT(metadataOther, statistics::units::Count::get(),
               "Tagged metadata packets that are neither read nor write"),
      ADD_STAT(inReads, statistics::units::Count::get(),
               "Reads inside the observed range"),
      ADD_STAT(inWritebackDirty, statistics::units::Count::get(),
               "WritebackDirty inside the observed range"),
      ADD_STAT(inWritebackClean, statistics::units::Count::get(),
               "WritebackClean inside the observed range"),
      ADD_STAT(inWriteClean, statistics::units::Count::get(),
               "WriteClean inside the observed range"),
      ADD_STAT(inWritesOtherWithData, statistics::units::Count::get(),
               "Other write commands inside the observed range"),
      ADD_STAT(inCleanEvicts, statistics::units::Count::get(),
               "CleanEvict inside the observed range (no payload, not a "
               "write: invisible to a write-keyed observer)"),
      ADD_STAT(inOther, statistics::units::Count::get(),
               "Other packets inside the observed range"),
      ADD_STAT(inPrefetches, statistics::units::Count::get(),
               "Prefetch-flagged requests inside the observed range"),
      ADD_STAT(inDemand, statistics::units::Count::get(),
               "Non-prefetch requests inside the observed range"),
      ADD_STAT(outReads, statistics::units::Count::get(),
               "Reads outside the observed range"),
      ADD_STAT(outWritesWithData, statistics::units::Count::get(),
               "Writes outside the observed range"),
      ADD_STAT(outCleanEvicts, statistics::units::Count::get(),
               "CleanEvict outside the observed range"),
      ADD_STAT(outOther, statistics::units::Count::get(),
               "Other packets outside the observed range"),
      ADD_STAT(outPrefetches, statistics::units::Count::get(),
               "Prefetch-flagged requests outside the observed range"),
      ADD_STAT(outDemand, statistics::units::Count::get(),
               "Non-prefetch requests outside the observed range"),
      ADD_STAT(linesObserved, statistics::units::Count::get(),
               "Distinct lines in the observed range for which a "
               "data-carrying write-back was seen (CUMULATIVE for the "
               "run; recomputed at every dump, so it does not reset)"),
      ADD_STAT(linesInRange, statistics::units::Count::get(),
               "Total lines in the observed range"),
      ADD_STAT(lineCoverage, statistics::units::Ratio::get(),
               "linesObserved / linesInRange"),
      ADD_STAT(packetsObserved, statistics::units::Count::get(),
               "All requests seen on the timing path")
{
    lineCoverage = linesObserved / linesInRange;
}

void
CxlTrafficObserver::CxlTrafficObserverStats::preDumpStats()
{
    statistics::Group::preDumpStats();

    linesObserved = parent->lineSeenCount;
    linesInRange = parent->observedLineCount;

    // Silently reporting zero is the outcome this object most needs to
    // avoid: it is indistinguishable from "the mechanism observed
    // nothing interesting". Say so at the moment it happens.
    if (packetsObserved.value() == 0) {
        warn("CxlTrafficObserver %s: dumped with ZERO packets observed. "
             "The timing path never carried traffic here -- a KVM-only "
             "or atomic-only phase, or a splice that is not on the "
             "host's CXL path. This is not a measurement of zero.",
             parent->name());
    }
}

} // namespace gem5
