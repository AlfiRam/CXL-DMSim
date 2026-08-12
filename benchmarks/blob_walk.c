/*
 * blob_walk.c — the graph random walk as a position-independent code
 * blob, shipped through the mailbox and executed on the device with an
 * IN-PLACE pointer to the device's own mapping of the graph region
 * (OP_WALK; struct gw_args ABI in graph_walk.h).
 *
 * The kernel itself is gw_walk() from graph_walk.h — the SAME inline
 * function the host executor compiles, so the two configurations
 * cannot drift. Freestanding: no libc, no relocations (build gate in
 * the Makefile verifies, per blob_xtea.c's discipline).
 */

#include <stdint.h>

#include "graph_walk.h"

uint64_t
entry(void *argp)
{
    const struct gw_args *a = (const struct gw_args *)argp;
    return gw_walk(a->row_offsets, a->col_indices, a->nodes, a->steps,
                   a->seed);
}
