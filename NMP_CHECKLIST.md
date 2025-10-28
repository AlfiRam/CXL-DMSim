# NMP Implementation Checklist

Quick checklist to verify NMP implementation is ready for testing.

## ✅ Implementation Complete

### Core Files Modified
- [x] `src/dev/storage/cxl_memory.hh` - Header with NMP infrastructure
- [x] `src/dev/storage/cxl_memory.cc` - Implementation with CPU logic
- [x] `src/dev/storage/CXLMemory.py` - Python parameters

### Configuration Files Created
- [x] `configs/example/gem5_library/x86-cxl-nmp-run.py` - Main config script

### Benchmarks Created
- [x] `benchmarks/pointer_chase_nmp.c` - NMP benchmark (static)
- [x] `benchmarks/pointer_chase_host.c` - Host benchmark (dynamic)
- [x] `benchmarks/compile.sh` - Compilation script
- [x] `benchmarks/pointer_chase_nmp` - Compiled binary (888KB)
- [x] `benchmarks/pointer_chase_host` - Compiled binary (16KB)

### Documentation Created
- [x] `NMP_EXPERIMENTS.md` - Complete experiment guide
- [x] `NMP_IMPLEMENTATION_SUMMARY.md` - Implementation details
- [x] `NMP_CHECKLIST.md` - This checklist

### Scripts Created
- [x] `run_nmp_experiments.sh` - Automated experiment runner

---

## ⏳ Next Steps (Your Action Required)

### 1. Rebuild gem5 (Required)
```bash
cd /home/malfiram/CXL-DMSim
scons build/X86/gem5.opt -j16
```
⏱️ Expected time: 15-30 minutes

### 2. Run Prerequisites Check
```bash
./run_nmp_experiments.sh check
```
✅ Should confirm all files are ready

### 3. Run Experiments
```bash
# Option 1: Run everything automatically
./run_nmp_experiments.sh both

# Option 2: Run step-by-step
./run_nmp_experiments.sh host    # Baseline (30-60 min)
./run_nmp_experiments.sh nmp     # NMP (15-30 min)
./run_nmp_experiments.sh analyze # Results
```

---

## Verification Steps

### After Building gem5
```bash
# Check binary exists
ls -lh build/X86/gem5.opt

# Expected: ~500MB executable
```

### After Running Host Baseline
```bash
# Check output directory
ls -lh m5out_baseline_host/stats.txt

# Extract key metric
grep "simSeconds" m5out_baseline_host/stats.txt
```

### After Running NMP Experiment
```bash
# Check output directory
ls -lh m5out_nmp/stats.txt

# Extract NMP statistics
grep "nmp" m5out_nmp/stats.txt
```

### Success Indicators
```
✓ nmpExecutions > 0      (CPU executed)
✓ nmpMemReads > 0        (Memory accessed)
✓ nmpAccessLatency < 284 (Faster than host)
✓ Speedup ≈ 2.18×        (Matches hypothesis)
```

---

## Quick Command Reference

### Build
```bash
scons build/X86/gem5.opt -j16
```

### Run Host Baseline
```bash
build/X86/gem5.opt \
  --outdir=m5out_baseline_host \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on host \
  --test-cmd lmbench_cxl.sh
```

### Run NMP Experiment
```bash
build/X86/gem5.opt \
  --outdir=m5out_nmp \
  configs/example/gem5_library/x86-cxl-nmp-run.py \
  --run-on nmp \
  --nmp-binary benchmarks/pointer_chase_nmp
```

### Analyze Results
```bash
# Host latency
grep "simSeconds" m5out_baseline_host/stats.txt

# NMP statistics
grep "nmpMemReads" m5out_nmp/stats.txt
grep "nmpAccessLatency" m5out_nmp/stats.txt
```

---

## Files to Commit (After Validation)

Once experiments validate successfully, commit these files:

### Core Implementation
```
src/dev/storage/cxl_memory.hh
src/dev/storage/cxl_memory.cc
src/dev/storage/CXLMemory.py
```

### Configuration
```
configs/example/gem5_library/x86-cxl-nmp-run.py
```

### Benchmarks
```
benchmarks/pointer_chase_nmp.c
benchmarks/pointer_chase_host.c
benchmarks/compile.sh
benchmarks/pointer_chase_nmp (binary - optional)
benchmarks/pointer_chase_host (binary - optional)
```

### Documentation
```
NMP_RESEARCH_CONTEXT.md
NMP_EXPERIMENTS.md
NMP_IMPLEMENTATION_SUMMARY.md
NMP_CHECKLIST.md
```

### Scripts
```
run_nmp_experiments.sh
```

---

## Troubleshooting Quick Reference

### Build Fails
1. Check gem5 version: `git log --oneline -1`
2. Clean build: `scons -c && scons build/X86/gem5.opt -j16`
3. Check includes: Look for missing header errors

### Experiment Fails
1. Check prerequisites: `./run_nmp_experiments.sh check`
2. Verify file paths in config script
3. Check disk space: `df -h`

### No NMP Activity (nmpExecutions = 0)
1. Check CPU initialization logs in simulation output
2. Verify `enable_nmp = True` in configuration
3. Check NMP CPU was registered with CXL device

### Wrong Results (Speedup < 2.0×)
1. Verify nmpMemPort bypasses CXL controller
2. Check that NMP CPU is using local memory path
3. Compare access latency distributions

---

## Expected Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 1 | Rebuild gem5 | 15-30 min |
| 2 | Run host baseline | 30-60 min |
| 3 | Run NMP experiment | 15-30 min |
| 4 | Analyze results | 5-10 min |
| **Total** | | **65-130 min** |

---

## Success Criteria

### ✅ Implementation Success
- [x] All files created
- [x] Benchmarks compiled
- [x] Documentation complete

### ⏳ Experimental Success (Pending)
- [ ] gem5 builds successfully
- [ ] Host baseline runs without errors
- [ ] NMP experiment runs without errors
- [ ] NMP CPU executes (nmpExecutions > 0)
- [ ] NMP CPU accesses memory (nmpMemReads > 0)
- [ ] Speedup ≥ 2.0× achieved
- [ ] Results validate hypothesis

---

## Contact & Support

If you encounter issues:

1. **Check documentation:** `NMP_EXPERIMENTS.md`
2. **Review implementation:** `NMP_IMPLEMENTATION_SUMMARY.md`
3. **Debug logs:** Look in `m5out/simout` and `m5out/simerr`
4. **gem5 docs:** https://www.gem5.org/documentation/

---

## Notes

- Simulation times are estimates (varies by hardware)
- Use `--outdir` to avoid overwriting previous results
- Statistics are in gem5 format (see gem5 docs for details)
- NMP CPU bypasses CXL protocol for direct memory access

---

**Status:** ✅ Ready for Testing
**Next Action:** Rebuild gem5 and run experiments
**Documentation:** See NMP_EXPERIMENTS.md for detailed instructions
