#!/bin/bash
#
# NMP Experiment Runner Script
# Runs baseline and NMP experiments, then compares results
#

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GEM5_BIN="build/X86/gem5.opt"
CONFIG_SCRIPT="configs/example/gem5_library/x86-cxl-nmp-run.py"
OUTDIR_HOST="m5out_baseline_host"
OUTDIR_NMP="m5out_nmp"

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check gem5 binary
    if [ ! -f "$GEM5_BIN" ]; then
        print_error "gem5 binary not found: $GEM5_BIN"
        echo "Please build gem5 first: scons build/X86/gem5.opt -j16"
        exit 1
    fi
    print_success "gem5 binary found"

    # Check configuration script
    if [ ! -f "$CONFIG_SCRIPT" ]; then
        print_error "Configuration script not found: $CONFIG_SCRIPT"
        exit 1
    fi
    print_success "Configuration script found"

    # Check benchmarks
    if [ ! -f "benchmarks/pointer_chase_nmp" ]; then
        print_error "NMP benchmark not found: benchmarks/pointer_chase_nmp"
        echo "Please compile benchmarks: cd benchmarks && ./compile.sh"
        exit 1
    fi
    print_success "NMP benchmark found"

    # Check file system images
    if [ ! -f "fs_files/vmlinux_20240920" ]; then
        print_error "Kernel image not found: fs_files/vmlinux_20240920"
        exit 1
    fi
    print_success "Kernel image found"

    if [ ! -f "fs_files/parsec.img" ]; then
        print_error "Disk image not found: fs_files/parsec.img"
        exit 1
    fi
    print_success "Disk image found"

    echo ""
    print_success "All prerequisites satisfied!"
}

run_host_baseline() {
    print_header "Experiment 1: Host Baseline (Host CPU → CXL Memory)"

    print_info "Configuration:"
    echo "  - Execution: Host CPU"
    echo "  - Target: CXL Memory (remote)"
    echo "  - CPU Type: TIMING"
    echo "  - Output: $OUTDIR_HOST"

    print_info "Starting simulation (this may take 30-60 minutes)..."
    echo ""

    # Run experiment
    $GEM5_BIN \
        --outdir="$OUTDIR_HOST" \
        "$CONFIG_SCRIPT" \
        --run-on host \
        --test-cmd lmbench_cxl.sh \
        --cpu-type TIMING \
        --is-asic True

    if [ $? -eq 0 ]; then
        print_success "Host baseline experiment completed!"
        echo ""
        print_info "Results saved to: $OUTDIR_HOST/stats.txt"
    else
        print_error "Host baseline experiment failed!"
        exit 1
    fi
}

run_nmp_experiment() {
    print_header "Experiment 2: NMP (NMP CPU → Local Memory)"

    print_info "Configuration:"
    echo "  - Execution: NMP CPU at CXL device"
    echo "  - Target: Local memory (bypasses CXL protocol)"
    echo "  - CPU Type: TimingSimpleCPU"
    echo "  - Output: $OUTDIR_NMP"

    print_info "Starting simulation (this may take 15-30 minutes)..."
    echo ""

    # Run experiment
    $GEM5_BIN \
        --outdir="$OUTDIR_NMP" \
        "$CONFIG_SCRIPT" \
        --run-on nmp \
        --nmp-binary benchmarks/pointer_chase_nmp \
        --nmp-cpu-type TimingSimpleCPU \
        --is-asic True

    if [ $? -eq 0 ]; then
        print_success "NMP experiment completed!"
        echo ""
        print_info "Results saved to: $OUTDIR_NMP/stats.txt"
    else
        print_error "NMP experiment failed!"
        exit 1
    fi
}

analyze_results() {
    print_header "Results Analysis"

    if [ ! -f "$OUTDIR_HOST/stats.txt" ]; then
        print_error "Host baseline results not found: $OUTDIR_HOST/stats.txt"
        echo "Please run host baseline first: $0 host"
        exit 1
    fi

    if [ ! -f "$OUTDIR_NMP/stats.txt" ]; then
        print_error "NMP results not found: $OUTDIR_NMP/stats.txt"
        echo "Please run NMP experiment first: $0 nmp"
        exit 1
    fi

    print_info "Extracting metrics..."

    # Extract host metrics
    host_sim_seconds=$(grep "^simSeconds" "$OUTDIR_HOST/stats.txt" | head -1 | awk '{print $2}')

    # Extract NMP metrics
    nmp_reads=$(grep "board.pc.south_bridge.cxlmemory.nmpMemReads" "$OUTDIR_NMP/stats.txt" | awk '{print $2}')
    nmp_writes=$(grep "board.pc.south_bridge.cxlmemory.nmpMemWrites" "$OUTDIR_NMP/stats.txt" | awk '{print $2}')
    nmp_executions=$(grep "board.pc.south_bridge.cxlmemory.nmpExecutions" "$OUTDIR_NMP/stats.txt" | awk '{print $2}')

    echo ""
    print_header "Summary"

    echo -e "${BLUE}Host Baseline:${NC}"
    echo "  simSeconds: $host_sim_seconds"
    echo ""

    echo -e "${BLUE}NMP Experiment:${NC}"
    echo "  nmpMemReads: $nmp_reads"
    echo "  nmpMemWrites: $nmp_writes"
    echo "  nmpExecutions: $nmp_executions"
    echo ""

    # Check for success
    if [ "$nmp_executions" -gt 0 ]; then
        print_success "NMP CPU executed successfully!"
    else
        print_error "NMP CPU did not execute (nmpExecutions = 0)"
    fi

    if [ "$nmp_reads" -gt 0 ]; then
        print_success "NMP CPU accessed memory ($nmp_reads reads)"
    else
        print_error "NMP CPU did not access memory (nmpMemReads = 0)"
    fi

    echo ""
    print_info "Full statistics:"
    echo "  Host: $OUTDIR_HOST/stats.txt"
    echo "  NMP:  $OUTDIR_NMP/stats.txt"
    echo ""
    print_info "For detailed latency analysis:"
    echo "  grep nmpAccessLatency $OUTDIR_NMP/stats.txt"
}

show_usage() {
    echo "NMP Experiment Runner"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  check       Check prerequisites only"
    echo "  host        Run host baseline experiment only"
    echo "  nmp         Run NMP experiment only"
    echo "  both        Run both experiments (default)"
    echo "  analyze     Analyze existing results"
    echo "  clean       Clean output directories"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0             # Run both experiments"
    echo "  $0 check       # Check if ready to run"
    echo "  $0 host        # Run only host baseline"
    echo "  $0 analyze     # Analyze previous results"
}

clean_outputs() {
    print_header "Cleaning Output Directories"

    if [ -d "$OUTDIR_HOST" ]; then
        rm -rf "$OUTDIR_HOST"
        print_success "Removed $OUTDIR_HOST"
    fi

    if [ -d "$OUTDIR_NMP" ]; then
        rm -rf "$OUTDIR_NMP"
        print_success "Removed $OUTDIR_NMP"
    fi

    echo ""
    print_info "Output directories cleaned"
}

# ============================================================================
# Main Script
# ============================================================================

case "${1:-both}" in
    check)
        check_prerequisites
        ;;
    host)
        check_prerequisites
        run_host_baseline
        ;;
    nmp)
        check_prerequisites
        run_nmp_experiment
        ;;
    both)
        check_prerequisites
        run_host_baseline
        run_nmp_experiment
        analyze_results
        ;;
    analyze)
        analyze_results
        ;;
    clean)
        clean_outputs
        ;;
    help)
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac

echo ""
print_success "Done!"
