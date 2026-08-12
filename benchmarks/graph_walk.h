/*
 * graph_walk.h — shared contract for the CXL graph-walk comparison.
 *
 * ONE definition of the measured kernel, included by BOTH executors:
 *   - graph_walk_host.c   (config 1: host CPU runs gw_walk directly)
 *   - blob_walk.c         (config 2: device NMP runs gw_walk as a
 *                          shipped position-independent blob)
 * Sharing this header is what guarantees the two configurations walk
 * the identical sequence: same LCG, same start node, same step
 * recurrence. Identical checksums are config 2's correctness proof.
 *
 * The kernel is a RANDOM WALK over a fixed-out-degree CSR graph: two
 * dependent loads per step (row_offsets[cur] then col_indices[...]),
 * no frontier, no visited set — it isolates the cost of one dependent
 * access to CXL-resident data. Fixed out-degree keeps `degree` nonzero
 * by construction, so the modulo is always defined.
 *
 * Everything here must stay freestanding-safe (no libc): blob_walk.c
 * compiles with the BLOB_CFLAGS discipline.
 *
 * In-region layout (built by the host, read by the device through its
 * OWN cacheable /dev/mem mapping of the same physical carve):
 *
 *   region + 0            struct gw_header
 *   region + hdr.offs_off uint32_t row_offsets[nodes + 1]
 *   region + hdr.cols_off uint32_t col_indices[nodes * degree]
 */

#ifndef GRAPH_WALK_H
#define GRAPH_WALK_H

#include <stdint.h>

#define GW_MAGIC     0xC5A9C511A11CULL   /* "CSR walk" sanity value */
#define GW_OFFS_OFF  4096ULL             /* row_offsets after header page */

struct gw_header {
    uint64_t magic;     /* GW_MAGIC                                    */
    uint64_t nodes;     /* node count N                                */
    uint64_t degree;    /* fixed out-degree D (>= 1)                   */
    uint64_t steps;     /* walk length                                 */
    uint64_t seed;      /* walk RNG seed (shared by both configs)      */
    uint64_t offs_off;  /* region-relative offset of row_offsets       */
    uint64_t cols_off;  /* region-relative offset of col_indices       */
    uint64_t reserved;
};

/* Blob argument block for OP_WALK: pointers are into the DEVICE's own
 * mapping of the graph region (in-place — no operand copy). */
struct gw_args {
    const uint32_t *row_offsets;
    const uint32_t *col_indices;
    uint64_t nodes;
    uint64_t steps;
    uint64_t seed;
};

static inline uint64_t
gw_rng_next(uint64_t *s)
{
    *s = *s * 6364136223846793005ULL + 1442695040888963407ULL;
    return *s >> 16;
}

/* The measured kernel. Two dependent loads per step; `sum` is the
 * checksum both configurations must agree on. */
static inline uint64_t
gw_walk(const uint32_t *row_offsets, const uint32_t *col_indices,
        uint64_t nodes, uint64_t steps, uint64_t seed)
{
    uint64_t rng = seed;
    uint64_t cur = gw_rng_next(&rng) % nodes;
    uint64_t sum = 0;
    for (uint64_t i = 0; i < steps; i++) {
        uint32_t base = row_offsets[cur];
        uint32_t degree = row_offsets[cur + 1] - base;
        cur = col_indices[base + (gw_rng_next(&rng) % degree)];
        sum += cur;
    }
    return sum;
}

#endif /* GRAPH_WALK_H */
