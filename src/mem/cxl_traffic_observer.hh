/*
 * Copyright (c) 2026 CXL-NMP
 * SPDX-License-Identifier: BSD-3-Clause
 */

#ifndef __MEM_CXL_TRAFFIC_OBSERVER_HH__
#define __MEM_CXL_TRAFFIC_OBSERVER_HH__

#include <vector>

#include "base/addr_range.hh"
#include "base/statistics.hh"
#include "mem/port.hh"
#include "params/CxlTrafficObserver.hh"
#include "sim/clocked_object.hh"
#include "sim/system.hh"

namespace gem5
{

/**
 * Passive inline observer for the CXL controller's memory-side port
 * (S1). It forwards EVERY packet verbatim, in every access mode, with
 * no added latency and no reordering; under TIMING it additionally
 * classifies each request into stats. Its only effect on a run is the
 * stats it produces.
 *
 * WHAT THIS OBJECT IS NOT -- read this before extending it.
 *
 * It does NOT hold, derive, store, or represent an encryption counter,
 * and it must not be made to. The integrity engine in this tree holds
 * no node values at all: both live trees are mocks, the value-carrying
 * tree is never instantiated, the tree's processWrite() is an empty
 * body with no callers, the verifier never reads a packet payload,
 * there is no comparison anywhere, and the metadata update on a data
 * write is a commented-out TODO behind a fatal(). A counter derived
 * here would therefore have nowhere to live and nothing to be checked
 * against. This object supports a claim about OBSERVABILITY and COST --
 * which traffic crosses this point, and what watching it costs -- and
 * deliberately supports no claim about correctness.
 *
 * Three properties keep that honest, and each is load-bearing:
 *
 *   1. The coverage structure is a BITMAP: exactly one SATURATING bit
 *      per line, recording "at least one data write-back to this line
 *      was seen". A bit cannot represent a magnitude, so it cannot be
 *      read as "how many times" anything happened -- which is what a
 *      counter would have to be. It is deliberately not an array of
 *      integers for that reason.
 *   2. Nothing here is reachable by another SimObject. There are no
 *      cxx_exports, no accessors, no SimObject-valued params pointing
 *      at it, and the bitmap is private. Its aggregate population is
 *      published only as a stat.
 *   3. It acts on no packet. Every request and response is forwarded
 *      unchanged; there is no address at which behaviour differs.
 *
 * If a future change adds per-line magnitude, an accessor, or an
 * action, this object has stopped being an observer and the comment
 * above has become false.
 */
class CxlTrafficObserver : public ClockedObject
{
  public:
    PARAMS(CxlTrafficObserver);

    CxlTrafficObserver(const Params &p);

    void init() override;

    Port &getPort(const std::string &if_name,
                  PortID idx=InvalidPortID) override;

  protected:
    /** Controller-facing port. */
    class ObserverResponsePort : public ResponsePort
    {
      public:
        ObserverResponsePort(const std::string &_name,
                             CxlTrafficObserver &_parent);

      protected:
        bool recvTimingReq(PacketPtr pkt) override;
        void recvRespRetry() override;
        Tick recvAtomic(PacketPtr pkt) override;
        Tick recvAtomicBackdoor(PacketPtr pkt,
                                MemBackdoorPtr &backdoor) override;
        void recvFunctional(PacketPtr pkt) override;
        AddrRangeList getAddrRanges() const override;

      private:
        CxlTrafficObserver &parent;
    };

    /** Bus-facing port. */
    class ObserverRequestPort : public RequestPort
    {
      public:
        ObserverRequestPort(const std::string &_name,
                            CxlTrafficObserver &_parent);

      protected:
        bool recvTimingResp(PacketPtr pkt) override;
        void recvReqRetry() override;
        void recvRangeChange() override;
        bool isSnooping() const override { return false; }

      private:
        CxlTrafficObserver &parent;
    };

    ObserverRequestPort memSidePort;
    ObserverResponsePort cpuSidePort;

    System *system;

    /** The range whose traffic counts as "protected". */
    const AddrRange observeRange;

    const unsigned int lineSize;

    /** Total lines in the observed range (a constant, published so the
     * coverage fraction is self-describing in stats.txt). */
    const uint64_t observedLineCount;

    /**
     * Distinct-line coverage. ONE SATURATING BIT per line of the
     * observed range: set when a data write-back carrying a payload is
     * seen for that line. Set membership, never a magnitude -- see the
     * class comment. Bounded and allocated once at construction:
     * observeRange.size() / lineSize bits.
     */
    std::vector<bool> lineSeen;

    /** Running population of lineSeen, maintained incrementally so the
     * stat does not require an O(lines) sweep at every dump. */
    uint64_t lineSeenCount;

    /** Classify and count one request. Timing path only. */
    void observe(PacketPtr pkt);

    struct CxlTrafficObserverStats : public statistics::Group
    {
        CxlTrafficObserverStats(CxlTrafficObserver *parent);

        void preDumpStats() override;

        CxlTrafficObserver *parent;

        /* Verifier metadata traffic, identified by the request TAG and
         * counted before any address classification, so metadata is
         * never conflated with data. */
        statistics::Scalar metadataReads;
        statistics::Scalar metadataWrites;
        statistics::Scalar metadataOther;

        /* Data traffic inside the observed range. */
        statistics::Scalar inReads;
        statistics::Scalar inWritebackDirty;
        statistics::Scalar inWritebackClean;
        statistics::Scalar inWriteClean;
        statistics::Scalar inWritesOtherWithData;
        statistics::Scalar inCleanEvicts;
        statistics::Scalar inOther;
        statistics::Scalar inPrefetches;
        statistics::Scalar inDemand;

        /* Data traffic outside it. */
        statistics::Scalar outReads;
        statistics::Scalar outWritesWithData;
        statistics::Scalar outCleanEvicts;
        statistics::Scalar outOther;
        statistics::Scalar outPrefetches;
        statistics::Scalar outDemand;

        /* Coverage. linesObserved is CUMULATIVE for the run: it is
         * recomputed from the bitmap at every dump, so unlike the event
         * counters above it does not reset. */
        statistics::Scalar linesObserved;
        statistics::Scalar linesInRange;
        statistics::Formula lineCoverage;

        /* Everything the observer saw, for the did-it-see-anything
         * check. */
        statistics::Scalar packetsObserved;
    } stats;
};

} // namespace gem5

#endif // __MEM_CXL_TRAFFIC_OBSERVER_HH__
