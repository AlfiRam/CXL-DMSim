/**
 * Pointer-Chasing Microbenchmark for Host CPU
 *
 * This is the host version that allocates memory dynamically.
 * Use this for baseline measurements (Host CPU → CXL Memory).
 *
 * Same design as NMP version but with dynamic memory allocation.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Configuration
#define SIZE (128 * 1024 * 1024)  // 128 MB (larger than 96 MB LLC)
#define ACCESSES 10000             // 10K random accesses
#define STRIDE 4096                // 4KB stride (page size)

int main() {
    // Allocate memory dynamically
    // When using numactl, this will be placed in specified NUMA node
    char *data = (char*)malloc(SIZE);
    if (data == NULL) {
        fprintf(stderr, "Failed to allocate %d MB\n", SIZE / (1024 * 1024));
        return 1;
    }

    // Initialize memory to ensure pages are allocated
    memset(data, 0, SIZE);

    // Accumulator to prevent compiler optimization
    volatile uint64_t sum = 0;

    printf("Starting pointer-chasing benchmark (HOST)\n");
    printf("Array size: %d MB\n", SIZE / (1024 * 1024));
    printf("Number of accesses: %d\n", ACCESSES);
    printf("Stride: %d bytes\n", STRIDE);
    printf("Memory address: %p\n", (void*)data);

    // Pointer-chasing loop
    for (int i = 0; i < ACCESSES; i++) {
        size_t idx = (i * STRIDE) % SIZE;
        sum += data[idx];
    }

    printf("Benchmark complete\n");
    printf("Checksum: %lu\n", (unsigned long)sum);

    free(data);
    return 0;
}
