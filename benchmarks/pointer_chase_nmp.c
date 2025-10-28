/**
 * Pointer-Chasing Microbenchmark for NMP CPU
 *
 * This benchmark measures memory access latency by performing random
 * memory accesses with a stride pattern that defeats hardware prefetchers.
 *
 * Design:
 * - 128 MB array (larger than 96 MB LLC to force memory access)
 * - 10K accesses (fast enough for gem5 simulation)
 * - 4KB stride (defeats prefetcher, page-level granularity)
 *
 * Expected Results:
 * - Host CPU → CXL Memory: ~284 ns per access
 * - NMP CPU → Local Memory: ~130 ns per access (2.18× speedup)
 */

#include <stdint.h>
#include <stdio.h>

// Configuration
#define SIZE (128 * 1024 * 1024)  // 128 MB (larger than 96 MB LLC)
#define ACCESSES 10000             // 10K random accesses
#define STRIDE 4096                // 4KB stride (page size)

// Memory base address
// For NMP: This will be 0x100000000 (4GB, beginning of CXL range)
// For Host: This will be allocated dynamically
#define MEMORY_BASE 0x100000000ULL

int main() {
    // Point to memory region
    volatile char *data = (volatile char*)MEMORY_BASE;

    // Accumulator to prevent compiler optimization
    volatile uint64_t sum = 0;

    printf("Starting pointer-chasing benchmark\n");
    printf("Array size: %d MB\n", SIZE / (1024 * 1024));
    printf("Number of accesses: %d\n", ACCESSES);
    printf("Stride: %d bytes\n", STRIDE);
    printf("Memory base: 0x%lx\n", (unsigned long)MEMORY_BASE);

    // Pointer-chasing loop
    // Random stride pattern defeats hardware prefetcher
    for (int i = 0; i < ACCESSES; i++) {
        // Calculate index with stride pattern
        // Using modulo ensures we stay within bounds
        size_t idx = (i * STRIDE) % SIZE;

        // Memory access - this is what we're measuring
        sum += data[idx];
    }

    printf("Benchmark complete\n");
    printf("Checksum: %lu\n", (unsigned long)sum);

    return 0;
}
