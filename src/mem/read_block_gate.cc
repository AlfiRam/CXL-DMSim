/*
 * Copyright (c) 2026 CXL-NMP
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "mem/read_block_gate.hh"

#include <cstring>

#include "debug/ReadBlockGate.hh"

namespace gem5
{

ReadBlockGate::ReadBlockGate(const Params &p)
    : ClockedObject(p),
      memSidePort(name() + ".mem_side_port", *this),
      cpuSidePort(name() + ".cpu_side_port", *this),
      system(p.system),
      slotRange(p.slot_addr, p.slot_addr + p.slot_size),
      releaseLatency(p.release_latency),
      heldReadPkt(nullptr),
      heldSince(0),
      pendingStore(false),
      storeAddr(0),
      storeSize(0),
      releasePkt(nullptr),
      memRespRetryOwed(false),
      releaseEvent([this]{ processRelease(); }, name()),
      slotLabel(p.slot_label),
      holdTimeout(p.hold_timeout),
      deadlineEvent([this]{ holdDeadlineExpired(); }, name()),
      stats(this),
      maxHeldSeen(0)
{
}

void
ReadBlockGate::init()
{
    if (!cpuSidePort.isConnected() || !memSidePort.isConnected())
        fatal("ReadBlockGate %s is not connected on both sides.\n", name());

    if (slotRange.size() == 0)
        fatal("ReadBlockGate %s has a zero-sized slot.\n", name());

    if (slotRange.size() > sizeof(storeData))
        fatal("ReadBlockGate %s slot is larger than one cache line "
              "(%d > %d bytes).\n",
              name(), slotRange.size(), sizeof(storeData));

    // The ATOMIC interlock. A held read cannot exist outside timing
    // mode (recvAtomic must return synchronously), so running with the
    // gate in plain atomic mode would silently measure nothing --
    // fatal instead. atomic_noncaching is the KVM BOOT mode of the
    // --kvm-boot --kvm-dest timing flow: the gate is dormant there (no
    // port traffic reaches CXL under KVM) and arms when the barrier
    // switches the System to timing, so it is tolerated with a notice.
    // The backstop for anything that slips through is the fatal on an
    // atomic slot read in recvAtomic().
    const auto mode = system->getMemoryMode();
    if (mode == enums::atomic) {
        fatal("ReadBlockGate %s: memory mode is 'atomic'; a held read "
              "cannot exist outside timing mode, so this run would "
              "silently measure nothing. Use a timing flow.\n", name());
    } else if (mode == enums::atomic_noncaching) {
        inform("ReadBlockGate %s: memory mode is 'atomic_noncaching' "
               "(KVM boot); gate is dormant until the switch to "
               "timing.\n", name());
    }

    inform("ReadBlockGate %s: gating the %s slot %s (release latency "
           "%d cycles, hold timeout %llu ticks).\n",
           name(), slotLabel, slotRange.to_string(),
           (int)releaseLatency, (unsigned long long)holdTimeout);
}

Port &
ReadBlockGate::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "mem_side_port") {
        return memSidePort;
    } else if (if_name == "cpu_side_port") {
        return cpuSidePort;
    } else {
        return ClockedObject::getPort(if_name, idx);
    }
}

ReadBlockGate::GateResponsePort::GateResponsePort(
    const std::string &_name, ReadBlockGate &_parent)
    : ResponsePort(_name), parent(_parent)
{
}

ReadBlockGate::GateRequestPort::GateRequestPort(
    const std::string &_name, ReadBlockGate &_parent)
    : RequestPort(_name), parent(_parent)
{
}

bool
ReadBlockGate::GateResponsePort::recvTimingReq(PacketPtr pkt)
{
    return parent.handleTimingReq(pkt);
}

void
ReadBlockGate::GateResponsePort::recvRespRetry()
{
    parent.handleRespRetry();
}

Tick
ReadBlockGate::GateResponsePort::recvAtomic(PacketPtr pkt)
{
    // Backstop of the ATOMIC interlock: an atomic read of the gated
    // slot means a workload is exercising the slot in a mode where the
    // gate cannot hold -- the run is not measuring read-blocking, and
    // believing otherwise is the worst outcome. Everything else
    // forwards (boot-time atomic traffic under the tolerated
    // atomic_noncaching phase).
    if (pkt->isRead() && !pkt->isWrite() &&
        pkt->getAddrRange().isSubset(parent.slotRange)) {
        fatal("ReadBlockGate %s: atomic read of the gated slot %s; the "
              "gate cannot hold under atomic mode, so this run is NOT "
              "measuring read-blocking.\n",
              parent.name(), parent.slotRange.to_string());
    }
    return parent.memSidePort.sendAtomic(pkt);
}

Tick
ReadBlockGate::GateResponsePort::recvAtomicBackdoor(
    PacketPtr pkt, MemBackdoorPtr &backdoor)
{
    // Forward the access; leave `backdoor` untouched (decline).
    return recvAtomic(pkt);
}

void
ReadBlockGate::GateResponsePort::recvFunctional(PacketPtr pkt)
{
    // Pure forward is correct here (primer trap 19 considered): the
    // held read carries no data, and a pending release response holds
    // a copy of a store that was ALREADY forwarded downstream, so DRAM
    // always has bytes at least as new as anything the gate holds. A
    // functional write to the slot while a release is in flight
    // updates DRAM but not the crafted response -- the release
    // deliberately carries the triggering store's value.
    parent.memSidePort.sendFunctional(pkt);
}

AddrRangeList
ReadBlockGate::GateResponsePort::getAddrRanges() const
{
    // Ranges forwarded verbatim: splicing the gate is invisible to the
    // bus's routing (integrity verifier precedent).
    return parent.memSidePort.getAddrRanges();
}

bool
ReadBlockGate::GateRequestPort::recvTimingResp(PacketPtr pkt)
{
    return parent.handleTimingResp(pkt);
}

void
ReadBlockGate::GateRequestPort::recvReqRetry()
{
    // Combinational retry chain: the refusal we propagated upstream is
    // retried by the bus once the memory controller frees up.
    parent.cpuSidePort.sendRetryReq();
}

void
ReadBlockGate::GateRequestPort::recvRangeChange()
{
    parent.cpuSidePort.sendRangeChange();
}

bool
ReadBlockGate::handleTimingReq(PacketPtr pkt)
{
    const AddrRange pktRange = pkt->getAddrRange();
    const bool slotRead = pkt->isRead() && !pkt->isWrite() &&
        pktRange.isSubset(slotRange);
    const bool slotWrite = pkt->isWrite() && slotRange.intersects(pktRange);

    if (slotRead) {
        if (heldReadPkt) {
            // Ordering case 5: cannot occur with one blocked host core;
            // if it does, the N = 1 invariant is broken -- be loud.
            panic("ReadBlockGate %s: second slot read %s while one is "
                  "already held (N = 1).\n", name(), pkt->print());
        }
        if (pendingStore) {
            // Ordering case 4: a store already passed unconsumed; the
            // value is in DRAM and nothing further will arrive to
            // release a hold. Forward; consume the token only if the
            // forward is accepted (a refused packet is retried by the
            // sender and must see the same state).
            bool ok = memSidePort.sendTimingReq(pkt);
            if (ok) {
                pendingStore = false;
                stats.loadsPassedUnheld++;
                DPRINTF(ReadBlockGate,
                        "Slot read %s passed unheld (consumed pending "
                        "store)\n", pkt->print());
            }
            return ok;
        }
        // Ordering case 1: hold. Accept the packet, forward nothing.
        heldReadPkt = pkt;
        heldSince = curTick();
        stats.loadsHeld++;
        // Arm the hold deadline: the waiting guest's own budget cannot
        // bound this wait (it never reaches a loop boundary), so an
        // unreleased hold would hang the run silently without it.
        if (holdTimeout > 0 && !deadlineEvent.scheduled()) {
            schedule(deadlineEvent, curTick() + holdTimeout);
        }
        DPRINTF(ReadBlockGate, "HOLDING slot read %s at tick %llu\n",
                pkt->print(), (unsigned long long)curTick());
        return true;
    }

    if (slotWrite) {
        // Copy the payload BEFORE forwarding: on an accepted timing
        // send the receiver owns the packet (primer trap 18/3.2).
        const Addr sAddr = pkt->getAddr();
        const Addr sSize = pkt->getSize();
        panic_if(sSize > sizeof(storeData),
                 "ReadBlockGate %s: slot store %s larger than a cache "
                 "line.\n", name(), pkt->print());
        uint8_t buf[sizeof(storeData)];
        std::memcpy(buf, pkt->getConstPtr<uint8_t>(), sSize);

        bool ok = memSidePort.sendTimingReq(pkt);
        if (ok) {
            if (heldReadPkt && !releaseEvent.scheduled()) {
                // Ordering case 2: forward (done above) AND release.
                // The store must cover the held read or the gate
                // cannot supply its bytes -- engine invariant, loud.
                panic_if(!heldReadPkt->getAddrRange().isSubset(
                             RangeSize(sAddr, sSize)),
                         "ReadBlockGate %s: releasing store %s does not "
                         "cover held read %s.\n",
                         name(), pkt->print(), heldReadPkt->print());
                std::memcpy(storeData, buf, sSize);
                storeAddr = sAddr;
                storeSize = sSize;
                stats.storesReleasing++;
                schedule(releaseEvent, clockEdge(releaseLatency));
                DPRINTF(ReadBlockGate,
                        "Slot store [%#llx,+%llu) accepted; releasing "
                        "held read\n",
                        (unsigned long long)sAddr,
                        (unsigned long long)sSize);
            } else {
                // Ordering case 3 (no read held), or a further store
                // while a release is already in flight: record the
                // unconsumed-store token (saturates at one).
                pendingStore = true;
                stats.storesPassed++;
                DPRINTF(ReadBlockGate,
                        "Slot store [%#llx,+%llu) passed, no read "
                        "held; pendingStore set\n",
                        (unsigned long long)sAddr,
                        (unsigned long long)sSize);
            }
        }
        return ok;
    }

    // Ordering case 6: everything else forwards untouched, refusals
    // propagate to the sender which retains the packet.
    return memSidePort.sendTimingReq(pkt);
}

bool
ReadBlockGate::handleTimingResp(PacketPtr pkt)
{
    // Pure forward. On refusal we return false; the memory controller
    // retains the response and we owe it a retry once the bus frees.
    bool ok = cpuSidePort.sendTimingResp(pkt);
    if (!ok)
        memRespRetryOwed = true;
    return ok;
}

void
ReadBlockGate::handleRespRetry()
{
    // Our own pending release resends first (deterministic priority);
    // if the bus refuses again it owes us another retry, so the owed
    // downstream retry is not lost.
    if (releasePkt) {
        trySendRelease();
        if (releasePkt)
            return;
    }
    if (memRespRetryOwed) {
        memRespRetryOwed = false;
        memSidePort.sendRetryResp();
    }
}

void
ReadBlockGate::holdDeadlineExpired()
{
    // Loud, never silent. The alternative -- releasing with invented
    // data -- would corrupt the handshake and look like success, which
    // is strictly worse than stopping.
    panic("ReadBlockGate %s (%s): held read %s has been unreleased for "
          "%llu ticks (hold_timeout). The releasing store never "
          "arrived; the waiting guest cannot time out on its own "
          "because a held read consumes no poll iterations.\n",
          name(), slotLabel,
          heldReadPkt ? heldReadPkt->print() : "(none)",
          (unsigned long long)holdTimeout);
}

void
ReadBlockGate::processRelease()
{
    assert(heldReadPkt);
    assert(!releasePkt);

    // The hold is ending; disarm its deadline.
    if (deadlineEvent.scheduled()) {
        deschedule(deadlineEvent);
    }

    PacketPtr pkt = heldReadPkt;

    const Tick heldFor = curTick() - heldSince;
    stats.totalHeldTicks += heldFor;
    if (heldFor > maxHeldSeen)
        maxHeldSeen = heldFor;

    // Complete the held read in place with the stored bytes. Coverage
    // was checked at store-accept time. Read request packets on this
    // segment carry a data buffer (AbstractMemory's setData contract),
    // and the delays were the request's; the gate's own cost is the
    // releaseLatency already elapsed.
    pkt->makeResponse();
    pkt->setData(storeData + (pkt->getAddr() - storeAddr));
    pkt->headerDelay = 0;
    pkt->payloadDelay = 0;

    DPRINTF(ReadBlockGate,
            "RELEASING held read %s after %llu ticks\n",
            pkt->print(), (unsigned long long)heldFor);

    // Unblock the hold state BEFORE sending (primer trap 16): the send
    // can re-enter this object in the same call stack.
    heldReadPkt = nullptr;
    releasePkt = pkt;
    trySendRelease();
}

void
ReadBlockGate::trySendRelease()
{
    assert(releasePkt);
    PacketPtr pkt = releasePkt;
    // Mark ready before sending (primer trap 16).
    releasePkt = nullptr;
    if (!cpuSidePort.sendTimingResp(pkt)) {
        // Refused: we keep the packet (primer trap 13) and resend on
        // the bus's recvRespRetry.
        releasePkt = pkt;
    }
}

ReadBlockGate::ReadBlockGateStats::ReadBlockGateStats(ReadBlockGate *parent)
    : statistics::Group(parent, "read_block_gate"),
      parent(parent),
      ADD_STAT(loadsHeld, statistics::units::Count::get(),
               "Slot reads held awaiting a releasing store"),
      ADD_STAT(loadsPassedUnheld, statistics::units::Count::get(),
               "Slot reads forwarded unheld (a store had already "
               "passed)"),
      ADD_STAT(storesReleasing, statistics::units::Count::get(),
               "Slot stores that released a held read"),
      ADD_STAT(storesPassed, statistics::units::Count::get(),
               "Slot stores forwarded with no read held"),
      ADD_STAT(totalHeldTicks, statistics::units::Tick::get(),
               "Total ticks reads spent held"),
      ADD_STAT(maxHeldTicks, statistics::units::Tick::get(),
               "Longest single hold in ticks"),
      ADD_STAT(avgHeldTicks, statistics::units::Tick::get(),
               "Average hold. With loadsPassedUnheld == 0 and "
               "loadsHeld == 1 this is the waiting side's entire "
               "pickup delay, exactly -- the figure that replaces "
               "poll-period quantisation")
{
    avgHeldTicks = totalHeldTicks / loadsHeld;
}

void
ReadBlockGate::ReadBlockGateStats::preDumpStats()
{
    statistics::Group::preDumpStats();
    maxHeldTicks = parent->maxHeldSeen;

    // Armed but never consulted is indistinguishable, in stats alone,
    // from "the mechanism was exercised and found nothing to do". Say
    // which it was. loadsHeld + loadsPassedUnheld is every slot read
    // the gate saw.
    if (loadsHeld.value() == 0 && loadsPassedUnheld.value() == 0) {
        warn("ReadBlockGate %s (%s): dumped with ZERO reads of the "
             "gated slot. The mechanism did nothing -- no reader ever "
             "reached this slot on the timing path (an atomic or "
             "KVM-only phase, or the wrong slot address). This is not "
             "a measurement of an instant pickup.",
             parent->name(), parent->slotLabel);
    }
}

} // namespace gem5
