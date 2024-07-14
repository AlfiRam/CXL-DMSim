#include "base/trace.hh"
#include "dev/storage/cxl_memory.hh"
#include "debug/CXLMemory.hh"

namespace gem5
{

CXLMemory::CXLMemory(const Param &p)
    : PciDevice(p),
    mem_(RangeSize(p.BAR0->addr(), p.BAR0->size()), *this),
    latency_(ticksToCycles(p.latency)),
    cxl_mem_latency_(ticksToCycles(p.cxl_mem_latency)),
    cxl_mem_range_(p.cxl_mem_range), numa_flag_(p.numa_flag)
    {
        DPRINTF(CXLMemory, "BAR0_addr:0x%lx, BAR0_size:0x%lx\n", p.BAR0->addr(),
            p.BAR0->size());
    }

Tick CXLMemory::read(PacketPtr pkt) {
    DPRINTF(CXLMemory, "read address : (%lx, %lx)\n", pkt->getAddr(),
            pkt->getSize());
    Tick cxl_latency = resolve_cxl_mem(pkt);
    mem_.access(pkt);
    Tick read_latency = (latency_ + cxl_latency) * this->clockPeriod();
    DPRINTF(CXLMemory, "read latency = %llu\n", read_latency);
    return read_latency;
}

Tick CXLMemory::write(PacketPtr pkt) {
    DPRINTF(CXLMemory, "write address : (%lx, %lx)\n", pkt->getAddr(),
            pkt->getSize());
    Tick cxl_latency = resolve_cxl_mem(pkt);
    mem_.access(pkt);
    Tick write_latency = (latency_ + cxl_latency) * this->clockPeriod();
    DPRINTF(CXLMemory, "write latency = %llu\n", write_latency);
    return write_latency;
}

AddrRangeList CXLMemory::getAddrRanges() const {
    AddrRangeList ranges = PciDevice::getAddrRanges();
    if (numa_flag_)
        ranges.push_back(cxl_mem_range_);
    return ranges;
}

Tick CXLMemory::resolve_cxl_mem(PacketPtr pkt) {
    if (pkt->cmd == MemCmd::M2SReq) {
        assert(pkt->isRead());
        assert(pkt->needsResponse());
    } else if (pkt->cmd == MemCmd::M2SRwD) {
        assert(pkt->isWrite());
        assert(pkt->needsResponse());
    }
    return cxl_mem_latency_;
}

CXLMemory::Memory::Memory(const AddrRange& range, CXLMemory& owner)
    : range(range),
    owner(owner) {
    pmemAddr = new uint8_t[range.size()];
    DPRINTF(CXLMemory, "initial range start=0x%lx, range size=0x%lx\n", range.start(), range.size());
}

void CXLMemory::Memory::access(PacketPtr pkt) {
    PciBar *bar = owner.BARs[0];
    range = RangeSize(bar->addr(), bar->size());
    // DPRINTF(CXLMemory, "final range start=0x%lx, range size=0x%lx\n", range.start(), range.size());
    if (pkt->cacheResponding()) {
        DPRINTF(CXLMemory, "Cache responding to %#llx: not responding\n", pkt->getAddr());
        return;
    }

    if (pkt->cmd == MemCmd::CleanEvict || pkt->cmd == MemCmd::WritebackClean) {
        DPRINTF(CXLMemory, "CleanEvict  on 0x%x: not responding\n", pkt->getAddr());
        return;
    }
    
    // assert(pkt->getAddrRange().isSubset(range));

    uint8_t* host_addr = toHostAddr(pkt->getAddr());
    // DPRINTF(CXLMemory, "host_addr = %p, pkt->getAddr = 0x%lx, pmemAddr = %p, range.start = 0x%lx\n", 
    //     *host_addr, pkt->getAddr(), *pmemAddr, range.start());
    if (pkt->cmd == MemCmd::SwapReq) {

        if (pkt->isAtomicOp()) {
            if (pmemAddr) {
                pkt->setData(host_addr);
                (*(pkt->getAtomicOp()))(host_addr);
            }
        } else {
            std::vector<uint8_t> overwrite_val(pkt->getSize());
            uint64_t condition_val64;
            uint32_t condition_val32;

            panic_if(!pmemAddr,
                     "Swap only works if there is real memory "
                     "(i.e. null=False)");

            bool overwrite_mem = true;
            // keep a copy of our possible write value, and copy what is at the
            // memory address into the packet
            pkt->writeData(&overwrite_val[0]);  // Write the data of the pkt to the vector
            pkt->setData(host_addr);            // Write the data of host_addr to pkt

            if (pkt->req->isCondSwap()) {
                if (pkt->getSize() == sizeof(uint64_t)) {
                    condition_val64 = pkt->req->getExtraData();
                    overwrite_mem = !std::memcmp(&condition_val64, host_addr, sizeof(uint64_t));
                } else if (pkt->getSize() == sizeof(uint32_t)) {
                    condition_val32 = (uint32_t)pkt->req->getExtraData();
                    overwrite_mem = !std::memcmp(&condition_val32, host_addr, sizeof(uint32_t));
                } else
                    panic("Invalid size for conditional read/write\n");
            }

            if (overwrite_mem)
                std::memcpy(host_addr, &overwrite_val[0], pkt->getSize());

            assert(!pkt->req->isInstFetch());
        }
    } else if (pkt->isRead()) {
        assert(!pkt->isWrite());
        if (pmemAddr) {
            pkt->setData(host_addr);
            DPRINTF(CXLMemory, "%s read due to %s\n", __func__, pkt->print());
            // std::cout << "read data = " << pkt->getPtr<uint8_t>() << "\n";
        }
    } else if (pkt->isInvalidate() || pkt->isClean()) {
        assert(!pkt->isWrite());
        // in a fastmem system invalidating and/or cleaning packets
        // can be seen due to cache maintenance requests

        // no need to do anything
    } else if (pkt->isWrite()) {
        if (pmemAddr) {
            pkt->writeData(host_addr);
            DPRINTF(CXLMemory, "%s write due to %s\n", __func__, pkt->print());
            // std::cout << "write data = " << pkt->getPtr<uint8_t>() << "\n";
        }
        assert(!pkt->req->isInstFetch());
    } else {
        panic("Unexpected packet %s", pkt->print());
    }
    if (pkt->needsResponse()) {
        pkt->makeResponse();
    }
}

} // namespace gem5
