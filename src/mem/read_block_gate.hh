/*
 * Copyright (c) 2026 CXL-NMP
 * SPDX-License-Identifier: BSD-3-Clause
 */

#ifndef __MEM_READ_BLOCK_GATE_HH__
#define __MEM_READ_BLOCK_GATE_HH__

#include "base/addr_range.hh"
#include "base/statistics.hh"
#include "mem/port.hh"
#include "params/ReadBlockGate.hh"
#include "sim/clocked_object.hh"
#include "sim/system.hh"

namespace gem5
{

/**
 * Read-blocking completion gate.
 *
 * Inline on the cxl_mem_bus -> MemCtrl segment: a TIMING read whose
 * byte range lies inside the configured slot is HELD (accepted,
 * unanswered, not forwarded) until a store covering it arrives from
 * either System; the store is forwarded downstream (DRAM stays
 * authoritative -- the gate owns no functional/checkpoint state) and
 * the held read is completed with the store's data. Everything else is
 * forwarded verbatim, combinationally: refusals and retries propagate
 * through in both directions, and address ranges pass through
 * unchanged (the integrity verifier's splice precedent).
 *
 * N = 1 by design: one held read, one unconsumed-store token, no
 * containers. The token (`pendingStore`) is what separates "hold this
 * read" from "the value is already downstream": a store passing with
 * no read held sets it; the next slot read consumes it and is
 * forwarded instead of held (otherwise nothing would ever release it).
 *
 * The mechanism is value-blind and carries no mailbox semantics.
 */
class ReadBlockGate : public ClockedObject
{
  public:
    PARAMS(ReadBlockGate);

    ReadBlockGate(const Params &p);

    void init() override;

    Port &getPort(const std::string &if_name,
                  PortID idx=InvalidPortID) override;

  protected:
    /** Bus-facing port. */
    class GateResponsePort : public ResponsePort
    {
      public:
        GateResponsePort(const std::string &_name, ReadBlockGate &_parent);

      protected:
        bool recvTimingReq(PacketPtr pkt) override;
        void recvRespRetry() override;
        Tick recvAtomic(PacketPtr pkt) override;

        /**
         * Forward atomically but DECLINE the backdoor (leave it
         * untouched): granting one would let atomic/KVM accesses
         * bypass the gate entirely. CXLMemory's precedent
         * (cxl_memory.hh recvMemBackdoorReq comment).
         */
        Tick recvAtomicBackdoor(PacketPtr pkt,
                                MemBackdoorPtr &backdoor) override;
        void recvMemBackdoorReq(const MemBackdoorReq &req,
                                MemBackdoorPtr &backdoor) override {}

        void recvFunctional(PacketPtr pkt) override;

        AddrRangeList getAddrRanges() const override;

      private:
        ReadBlockGate &parent;
    };

    /** Memory-controller-facing port. */
    class GateRequestPort : public RequestPort
    {
      public:
        GateRequestPort(const std::string &_name, ReadBlockGate &_parent);

      protected:
        bool recvTimingResp(PacketPtr pkt) override;
        void recvReqRetry() override;

        void recvRangeChange() override;

        bool isSnooping() const override { return false; }

      private:
        ReadBlockGate &parent;
    };

    GateRequestPort memSidePort;
    GateResponsePort cpuSidePort;

    /** Pointer to the owning System, for the memory-mode interlock. */
    System *system;

    /** The gated slot. Reads inside it are held; stores covering the
     * held read release it. */
    const AddrRange slotRange;

    /** Cycles from accepting a releasing store to completing the held
     * read. */
    const Cycles releaseLatency;

    /**
     * N = 1 hold state.
     *
     * heldReadPkt: the one held read (ordering case 1); nullptr when
     * none. pendingStore: the one unconsumed-store token (case 3); a
     * slot store that passed with no read held sets it (it saturates
     * at one -- value-blind, latest value is downstream), and the next
     * slot read consumes it and is forwarded (case 4) because the
     * value is already in DRAM and nothing further will arrive to
     * release a hold.
     */
    PacketPtr heldReadPkt;
    Tick heldSince;
    bool pendingStore;

    /**
     * Release-in-flight state: the releasing store's payload is copied
     * out BEFORE the store is forwarded (the receiver owns the packet
     * afterwards), then releaseEvent builds the response and sends it.
     * releasePkt is non-null only while a built response awaits a
     * (re)send after an upstream refusal.
     */
    uint8_t storeData[64];
    Addr storeAddr;
    Addr storeSize;
    PacketPtr releasePkt;

    /** We refused a downstream response while the bus was busy and owe
     * the memory controller a retry. */
    bool memRespRetryOwed;

    EventFunctionWrapper releaseEvent;

    /** Which side's wait this instance gates; messages only. */
    const std::string slotLabel;

    /**
     * Hold deadline. A held read consumes no iterations of the waiting
     * guest's poll loop, so neither the loop's iteration budget nor its
     * time-equivalent deadline can bound the wait -- both are checked
     * at loop boundaries a held reader never reaches. Without this, an
     * unreleased hold hangs the run in silence, which is the worst
     * outcome available here. Scheduled on hold, descheduled on
     * release; firing is a loud abort.
     *
     * What it does NOT guarantee: it bounds the hold, not the
     * correctness of the release. A hold released with the wrong
     * store's value would still be wrong, and this says nothing about
     * that. Nor can it distinguish "the other side is slow" from "the
     * other side is never coming" -- it only puts a ceiling on how long
     * the run will wait to find out.
     */
    const Tick holdTimeout;
    EventFunctionWrapper deadlineEvent;

    bool handleTimingReq(PacketPtr pkt);
    bool handleTimingResp(PacketPtr pkt);
    void handleRespRetry();
    void processRelease();
    void trySendRelease();
    void holdDeadlineExpired();

    struct ReadBlockGateStats : public statistics::Group
    {
        ReadBlockGateStats(ReadBlockGate *parent);

        void preDumpStats() override;

        ReadBlockGate *parent;

        statistics::Scalar loadsHeld;
        statistics::Scalar loadsPassedUnheld;
        statistics::Scalar storesReleasing;
        statistics::Scalar storesPassed;
        statistics::Scalar totalHeldTicks;
        statistics::Scalar maxHeldTicks;

        /* Average hold. With loadsPassedUnheld == 0 and loadsHeld == 1
         * this IS the waiting side's whole pickup delay, exactly --
         * which is the number that replaces poll-period quantisation
         * (the two counters sum to every poll read the gate saw, so
         * their sum being 1 means the reader polled exactly once). */
        statistics::Formula avgHeldTicks;
    } stats;

    /** Longest single hold seen, mirrored into maxHeldTicks at dump. */
    Tick maxHeldSeen;
};

} // namespace gem5

#endif // __MEM_READ_BLOCK_GATE_HH__
