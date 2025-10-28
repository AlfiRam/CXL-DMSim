#!/bin/bash
#
# Benchmark Compilation Script
# Compiles pointer-chasing benchmarks for both NMP and Host execution
#

set -e  # Exit on error

echo "=========================================="
echo "Compiling NMP Benchmarks"
echo "=========================================="

# Check if gcc is available
if ! command -v gcc &> /dev/null; then
    echo "ERROR: gcc not found. Please install gcc."
    exit 1
fi

# Compile NMP version (static, for NMP CPU at CXL device)
echo "Compiling pointer_chase_nmp (static binary for NMP CPU)..."
gcc -static -O2 -o pointer_chase_nmp pointer_chase_nmp.c
if [ $? -eq 0 ]; then
    echo "✓ pointer_chase_nmp compiled successfully"
    ls -lh pointer_chase_nmp
else
    echo "✗ Failed to compile pointer_chase_nmp"
    exit 1
fi

# Compile Host version (dynamic, for host CPU execution)
echo ""
echo "Compiling pointer_chase_host (dynamic binary for host CPU)..."
gcc -O2 -o pointer_chase_host pointer_chase_host.c
if [ $? -eq 0 ]; then
    echo "✓ pointer_chase_host compiled successfully"
    ls -lh pointer_chase_host
else
    echo "✗ Failed to compile pointer_chase_host"
    exit 1
fi

echo ""
echo "=========================================="
echo "Compilation Complete!"
echo "=========================================="
echo ""
echo "Binaries created:"
echo "  - pointer_chase_nmp  : For NMP CPU (static)"
echo "  - pointer_chase_host : For Host CPU (dynamic)"
echo ""
echo "Next steps:"
echo "  1. Run host baseline:  ./run_experiments.sh host"
echo "  2. Run NMP experiment: ./run_experiments.sh nmp"
echo "=========================================="
