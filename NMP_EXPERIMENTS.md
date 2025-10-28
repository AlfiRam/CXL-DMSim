# NMP (Near-Memory Processing) Experiments Guide

This guide explains how to run baseline validation experiments for Near-Memory Processing (NMP) in CXL-DMSim.

## Research Goal

**Validate that processing at the CXL device provides a latency advantage over remote execution from the host.**

**Hypothesis:** NMP CPU (local to CXL memory) should access memory faster than Host CPU (remote access via CXL link)

**Expected Results:**
- Host CPU → CXL Memory: ~284 ns per access (baseline)
- NMP CPU → Local Memory: ~130 ns per access (experimental)
- **Expected speedup: 2.18×**

---

## Prerequisites

### 1. Build gem5

If you haven't already built gem5:

```bash
# Build gem5 with X86 ISA
scons build/X86/gem5.opt -j16
```

This will take 15-30 minutes depending on your system.

### 2. Verify File System Images

Ensure you have the required kernel and disk image:

```bash
ls -lh fs_files/vmlinux_20240920
ls -lh fs_files/parsec.img
```

Both files should exist in the `fs_files/` directory.

### 3. Compile Benchmarks

```bash
cd benchmarks
./compile.sh
cd ..
```

This creates:
- `pointer_chase_nmp` - Static binary for NMP CPU
- `pointer_chase_host` - Dynamic binary for Host CPU

---

## Experiment 1: Baseline (Host CPU → CXL Memory)

This experiment measures memory access latency when the **host CPU** accesses **CXL memory remotely** via the CXL link.

### Run Baseline Experiment

```bash
build/X86/gem5.opt \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on host \
  --test-cmd lmbench_cxl.sh \
  --cpu-type TIMING \
  --is-asic True
```

### Configuration Details

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--run-on` | `host` | Run benchmark on host CPU |
| `--test-cmd` | `lmbench_cxl.sh` | Use existing lmbench benchmark |
| `--cpu-type` | `TIMING` | Use TimingSimpleCPU for accuracy |
| `--is-asic` | `True` | Simulate CXL ASIC device (284ns) |

### Expected Output

```
CXL-DMSim NMP Experiment
Execution Mode: HOST
CXL Device: ASIC
Host CPU Type: TIMING
Test Command: lmbench_cxl.sh
======================================================================
Running the simulation
Using KVM cpu
...
```

### Results Location

Results will be saved to: `m5out_lmbench_cxl/stats.txt`

To save results to a custom directory:
```bash
build/X86/gem5.opt \
  --outdir=m5out_baseline_host \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on host
```

---

## Experiment 2: NMP (NMP CPU → Local Memory)

This experiment measures memory access latency when the **NMP CPU** at the CXL device accesses **local memory directly**, bypassing the CXL protocol.

### Run NMP Experiment

```bash
build/X86/gem5.opt \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on nmp \
  --nmp-binary benchmarks/pointer_chase_nmp \
  --nmp-cpu-type TimingSimpleCPU \
  --is-asic True
```

### Configuration Details

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--run-on` | `nmp` | Run benchmark on NMP CPU |
| `--nmp-binary` | `benchmarks/pointer_chase_nmp` | NMP benchmark binary |
| `--nmp-cpu-type` | `TimingSimpleCPU` | CPU type for NMP processor |
| `--is-asic` | `True` | Simulate CXL ASIC device |

### Expected Output

```
CXL-DMSim NMP Experiment
Execution Mode: NMP
CXL Device: ASIC
NMP CPU Type: TimingSimpleCPU
NMP Binary: benchmarks/pointer_chase_nmp
======================================================================
[NMP Mode] Configuring Near-Memory Processor at CXL device
  - NMP CPU Type: TimingSimpleCPU
  - NMP Binary: benchmarks/pointer_chase_nmp
  - Created NMP CPU: system.nmp_cpu
  - NMP CPU registered with CXL device
  - NMP CPU configuration complete
  - NMP will access memory locally (bypassing CXL protocol)

[NMP] Initializing Near-Memory Processor...
[NMP] Starting execution at PC=0x100000000, SP=0x1ffef0000
[NMP] Initialization complete
...
```

### Results Location

Results will be saved to: `m5out/stats.txt`

To save to a custom directory:
```bash
build/X86/gem5.opt \
  --outdir=m5out_nmp \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on nmp
```

---

## Analyzing Results

### Host Mode Statistics

Check `m5out_baseline_host/stats.txt` for:

```bash
grep "simSeconds" m5out_baseline_host/stats.txt
```

**Key Metrics:**
- `simSeconds` - Total execution time
- Calculate: `avg_latency = simSeconds / num_accesses`

### NMP Mode Statistics

Check `m5out_nmp/stats.txt` for NMP-specific statistics:

```bash
grep "nmp" m5out_nmp/stats.txt
```

**Key Metrics:**
```
board.pc.south_bridge.cxlmemory.nmpMemReads         # Read count
board.pc.south_bridge.cxlmemory.nmpMemWrites        # Write count
board.pc.south_bridge.cxlmemory.nmpAccessLatency    # Latency distribution
board.pc.south_bridge.cxlmemory.nmpActiveCycles     # Active cycles
board.pc.south_bridge.cxlmemory.nmpExecutions       # Execution count
```

### Calculate Speedup

```python
# Example analysis
num_accesses = 10000

# From host baseline
host_sim_seconds = 0.00284  # Example: 2.84ms
host_avg_latency = host_sim_seconds / num_accesses
# host_avg_latency = 284 ns

# From NMP experiment (mean from distribution)
nmp_avg_latency = 130  # Example: 130 ns (from stats)

# Calculate speedup
speedup = host_avg_latency / nmp_avg_latency
# speedup = 284 / 130 = 2.18×

print(f"Host latency: {host_avg_latency:.1f} ns")
print(f"NMP latency: {nmp_avg_latency:.1f} ns")
print(f"Speedup: {speedup:.2f}×")
```

---

## Advanced Options

### Compare ASIC vs FPGA

**CXL ASIC (faster):**
```bash
--is-asic True
```

**CXL FPGA (slower):**
```bash
--is-asic False
```

Expected latencies:
- ASIC: 284 ns
- FPGA: 375 ns

### Different NMP CPU Types

**TimingSimpleCPU (default - cycle-accurate):**
```bash
--nmp-cpu-type TimingSimpleCPU
```

**AtomicSimpleCPU (faster simulation, less accurate):**
```bash
--nmp-cpu-type AtomicSimpleCPU
```

**MinorCPU (in-order, more complex):**
```bash
--nmp-cpu-type MinorCPU
```

### Custom Memory Addresses

To change where NMP execution starts:

Edit `configs/example/gem5_library/x86-cxl-nmp-run.py`:
```python
board.pc.south_bridge.cxlmemory.nmp_start_addr = 0x200000000  # Custom address
```

---

## Troubleshooting

### Error: "NMP memory port not connected"

**Problem:** NMP memory port wasn't connected to backend memory.

**Solution:** Check that `nmpMemPort` is properly connected in board configuration.

### Error: "Failed to allocate memory"

**Problem:** Not enough memory for CXL device.

**Solution:** Reduce CXL memory size in configuration:
```python
cxl_memory = DIMM_DDR5_4400(size="4GB")  # Instead of 8GB
```

### Simulation is too slow

**Option 1:** Use AtomicSimpleCPU instead of TimingSimpleCPU:
```bash
--nmp-cpu-type AtomicSimpleCPU
```

**Option 2:** Reduce number of accesses in benchmark:
```c
#define ACCESSES 1000  // Instead of 10000
```

### Can't find vmlinux or disk image

**Problem:** File paths in configuration don't match your setup.

**Solution:** Update paths in `x86-cxl-nmp-run.py`:
```python
board.set_kernel_disk_workload(
    kernel=KernelResource(
        local_path="/your/path/to/vmlinux_20240920"
    ),
    disk_image=DiskImageResource(
        local_path="/your/path/to/parsec.img"
    ),
    ...
)
```

---

## Expected Simulation Times

These are approximate times on a modern workstation:

| Experiment | Boot Time | Benchmark Time | Total |
|------------|-----------|----------------|-------|
| Host Baseline | ~10 min | ~20 min | ~30 min |
| NMP Experiment | ~10 min | ~5 min | ~15 min |

**Note:** NMP experiment may be faster because it bypasses the CXL protocol overhead.

---

## Success Criteria

✅ **Experiment is successful if:**

1. Both experiments complete without errors
2. NMP CPU measured latency < Host CPU latency
3. Speedup is approximately 2× or better
4. Results show ~2.18× speedup (matches hypothesis)

❌ **Investigate if:**

1. NMP latency is higher than host latency
2. Speedup is less than 1.5×
3. Statistics show zero NMP memory accesses

---

## Next Steps

Once baseline validation is complete:

1. **Experiment with different workloads** - Try memory-intensive benchmarks
2. **Vary memory sizes** - Test with different array sizes
3. **Test different access patterns** - Sequential vs random access
4. **Add complexity** - Implement task offloading mechanisms
5. **Secure enclaves** - Add encryption and integrity trees

See `NMP_RESEARCH_CONTEXT.md` for the full research roadmap.

---

## Quick Reference

### Run Host Baseline
```bash
build/X86/gem5.opt configs/example/gem5_library/x86-cxl-nmp-run.py --run-on host
```

### Run NMP Experiment
```bash
build/X86/gem5.opt configs/example/gem5_library/x86-cxl-nmp-run.py --run-on nmp
```

### View Results
```bash
# Host results
less m5out/stats.txt

# NMP results
grep nmp m5out/stats.txt
```

### Compare Results
```bash
# Extract key metrics
grep "simSeconds" m5out_baseline_host/stats.txt
grep "nmpAccessLatency" m5out_nmp/stats.txt
```

---

**For questions or issues, refer to:**
- `NMP_RESEARCH_CONTEXT.md` - Research background and goals
- `README.md` - CXL-DMSim general documentation
- gem5 documentation: https://www.gem5.org/documentation/
