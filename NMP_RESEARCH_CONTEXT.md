# NMP Research Context for CXL-DMSim

## Research Background

### CXL-Based Disaggregated Memory
CXL (Compute eXpress Link) enables **memory disaggregation**: remote memory nodes form a pool that can be dynamically partitioned among processor hosts, maximizing memory utilization.

**CXL Protocols:**
- **CXL.io**: Device configuration, MMIO, interrupts (storage use)
- **CXL.cache**: Accelerators participate in cache coherence
- **CXL.mem**: Direct memory access by mapping remote memory into system address space
  - **Key for memory disaggregation** ← Our focus

### Why Near-Memory Processing (NMP) with CXL is Unique

**Three key advantages over local NMP:**

1. **CXL devices already have processing capability**
   - Must parse memory request packets from hosts
   - Already includes logic capable of general computation

2. **No power constraints like CPU socket**
   - Local memories share CPU socket power budget
   - CXL devices have separate power envelope
   - Can add processors without affecting host

3. **Higher latency makes NMP more beneficial** ⭐
   - Local DRAM: ~100-150 ns
   - CXL memory: 3-10× slower (~300-1500 ns)
   - **More latency = greater benefit from processing near data**
   - Moving data is expensive, moving computation is cheap

### Long-Term Vision: Secure Enclave Offloading

**Goal:** Offload data-intensive enclave execution to CXL memory using CXL.mem protocol

**Key challenges:**
- **Subtree migration**: Transfer integrity tree ownership from host to CXL device
  - Host self-invalidates integrity subtree
  - Securely send root to memory device
  - NMP processor works on data using local subtree

- **Completion signaling**: Host polls to know when offloaded task completes

**Unique opportunities:**
1. **Low-cost polling**: CXL controller withholds response until task complete
   - Host enters low power mode (no busy-waiting)
   - Avoids flooding memory hierarchy with poll requests

2. **Automatic counter tracking**: CXL controller sees all host writebacks
   - Can accurately track encryption counter values
   - **Avoid migrating coherence counters** (optimization!)

**Expected benefit:** Substantial performance gains for data-intensive secure workloads

---

## Current Phase: **BASELINE VALIDATION**

### Research Question
Does processing at the CXL device provide a latency advantage over remote execution from the host?

### Hypothesis
NMP CPU (local to CXL memory) should access memory faster than Host CPU (remote access via CXL link)

### What We've Measured So Far
- Host CPU → CXL Memory: **284 ns per access** (measured via lmbench)
- Configuration: NUMA Node 0 (Host CPU + 3GB DRAM), NUMA Node 1 (CXL device + 8GB memory)

### What We Want to Test
Add a CPU **at the CXL memory device** (as a Near-Memory Processor alongside the CXL Controller) and measure its memory access latency when accessing the device's local memory.

**Expected outcome:** Local access should be significantly faster (possibly ~2-10× based on proposal's "3-10× latency" claim)

### Current Architecture
```
┌─────────────────┐          ┌──────────────────────┐
│ NUMA Node 0     │          │ CXL Memory Pool      │
│                 │          │                      │
│ Host CPU        │          │ CXL Controller       │
│ Cache           │──CXL─────│ Memory 8GB           │
│ Local DRAM 3GB  │  Link    │                      │
└─────────────────┘          └──────────────────────┘
```

### Target Architecture
```
┌─────────────────┐          ┌──────────────────────┐
│ NUMA Node 0     │          │ CXL Memory Pool      │
│                 │          │                      │
│ Host CPU        │          │ NMP CPU ← NEW        │
│ Cache           │──CXL─────│ CXL Controller       │
│ Local DRAM 3GB  │  Link    │ Memory 8GB           │
└─────────────────┘          └──────────────────────┘
```

### Benchmark Workload

**Simple pointer-chasing microbenchmark:**
```c
// simple_chase.c
#include <stdint.h>
#include <stdio.h>

#define SIZE (128 * 1024 * 1024)  // 128 MB (larger than 96 MB LLC)
#define ACCESSES 10000             // 10K random accesses

int main() {
    char *data = (char*)0x0;  // Memory address (will be configured)

    volatile uint64_t sum = 0;
    for (int i = 0; i < ACCESSES; i++) {
        // Random stride - defeats prefetcher, forces memory access
        size_t idx = (i * 4096) % SIZE;  // Jump by page size
        sum += data[idx];
    }

    printf("Done: %lu\n", sum);
    return 0;
}
```

**Why this workload:**
- **128 MB array** > 96 MB LLC → guarantees memory accesses (not cache hits)
- **10K accesses** → fast enough for gem5 simulation (~30-60 min expected)
- **Random 4KB stride** → defeats hardware prefetcher
- **Simple** → easy to implement and measure
- **Apples-to-apples** → same workload runs on both host CPU and NMP CPU

**Expected measurements:**
- Host CPU → CXL Memory: 10K × 284 ns = 2.84 ms (remote access)
- NMP CPU → CXL Memory: 10K × 130 ns = 1.30 ms (local access)
- **Speedup: 2.18×**

**Measurement method:**
- Run benchmark in gem5 TIMING mode
- Extract `simSeconds` from stats.txt
- Calculate: avg_latency = simSeconds / ACCESSES
- Compare: host_latency vs nmp_latency

### Scope

**Current focus:**
- Add CPU capability to CXL device
- Run pointer-chasing benchmark on both CPUs
- Measure local vs remote memory access latency
- Validate fundamental NMP advantage

**Out of scope for now:**
- Secure enclaves / encryption
- Integrity trees
- Task offloading mechanisms
- Complex workloads

We're keeping it simple to validate the basic premise before adding complexity.

### Success Criteria
- Benchmark runs successfully on host CPU (baseline)
- CPU at CXL device can run same benchmark
- NMP CPU measured latency < Host CPU latency
- Results show ~2× or better speedup
- Validates that higher CXL latency makes NMP worthwhile

### Timeline
- **Immediate**: Get baseline measurement (host CPU → CXL memory)
- **Next**: Implement NMP CPU at device
- **Goal**: Compare results to validate hypothesis

### Future Phases
Once baseline is validated:
- Add offloading mechanisms (host → NMP task delegation)
- Implement secure enclave support
- Full system with subtree migration and optimized polling

---

## Questions for Implementation

How do we add NMP capability to CXL-DMSim to test this hypothesis?

Consider:
- How is the CXL device currently modeled in this codebase?
- What would be an appropriate CPU model for the NMP processor?
- How should the NMP CPU connect to the device's memory?
- How do we load and run the pointer-chasing benchmark on the NMP CPU?
- What's the best way to measure memory access latency from gem5 stats?
