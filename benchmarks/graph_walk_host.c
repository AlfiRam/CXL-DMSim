/*
 * graph_walk_host.c — host side of the CXL graph-walk comparison.
 *
 *   mode "host"   (config 1): build the CSR graph in the cacheable
 *     carve, flush it, then run gw_walk() on the HOST CPU, bracketed by
 *     m5_reset_stats/m5_dump_reset_stats (dump-AND-reset, so the
 *     automatic end-of-simulation dump emits only the post-bracket
 *     tail instead of bracket+tail masquerading as a second answer;
 *     the FIRST block is identical either way).
 *   mode "device" (config 2): build + flush the same graph, ship
 *     blob_walk through the mailbox (OP_WALK, in-place pointer ABI),
 *     then bracket [reset .. doorbell .. poll .. DONE .. dump]. The
 *     bracket deliberately INCLUDES dispatch and completion detection:
 *     that is the honest cost of offloading. The checksum is verified
 *     against a local recompute AFTER the bracket.
 *
 * Graph construction and the flush pass are OUTSIDE both brackets —
 * they are setup, not the measured work. The flush is required because
 * nothing keeps the two Systems' caches consistent (no coherence
 * agent): the host builds the graph through a CACHEABLE mapping
 * (/dev/mem WITHOUT O_SYNC — the measured cache_probe result this
 * whole workload rests on), so without CLFLUSH the device would read
 * stale DRAM. Per-line CLFLUSH is the only user-mode option (wbinvd is
 * ring-0). The flush line count is printed: it is the modeled cost of
 * the §6.2 self-invalidation step.
 *
 * Usage:
 *   graph_walk_host <host|device> <phys_base> <region_size>
 *                   <nodes> <degree> <steps> <seed>
 *
 * Every exit path prints a line beginning "GRAPH WALK"; the f2 barrier
 * keys on the guest-side GRAPHWALK_DONE echo that follows this program
 * unconditionally (CACHEPROBE_DONE discipline).
 *
 * Build: gcc -O2 -static with libm5 (m5_reset_stats/
 * m5_dump_reset_stats — the memory_stride_access.c precedent). Runs
 * under TIMING, where magic-instruction m5ops are supported.
 */

#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <time.h>
#include <unistd.h>

#include <gem5/m5ops.h>

#include "cxl_mailbox.h"
#include "graph_walk.h"
#include "blob_walk_bytes.h"   /* generated: cxl_blob_walk[], _len */

#define LINE 64ULL

/* Poll period for config 2's completion detection (inside the
 * bracket). MB_POLL_US env overrides; 0 = busy-spin. */
static long g_poll_us = 1000;

/* Completion-wait budget in SIMULATED SECONDS, not iterations (same
 * rationale as host_offload.c): the historical literal 200,000 tries was
 * a 200 s budget only at the 1 ms default period; under MB_POLL_US=0 the
 * same count collapses to ~60 ms and a long walk would report a spurious
 * TIMEOUT. Sleeping converts the budget to an exact iteration cap before
 * the loop, adding NO clock calls inside the bracket (at the default
 * period this is exactly 200,000 tries). Busy-spin checks a deadline
 * every SPIN_CHECK iterations. MB_TIMEOUT_S overrides. */
#define POLL_TIMEOUT_S 200             /* == 200,000 * 1000 us */
#define SPIN_CHECK     256
static long g_timeout_s = POLL_TIMEOUT_S;

static uint64_t
now_ns(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static uint32_t
read_status(volatile struct cxl_mailbox *mb)
{
    mb_clflush(&mb->status);
    mb_mfence();
    return mb->status;
}

int
main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    if (argc != 8) {
        printf("usage: graph_walk_host <host|device> <phys_base> "
               "<region_size> <nodes> <degree> <steps> <seed>\n");
        printf("GRAPH WALK ERROR bad-arguments\n");
        return 1;
    }
    const char *mode = argv[1];
    int is_device = strcmp(mode, "device") == 0;
    if (!is_device && strcmp(mode, "host") != 0) {
        printf("GRAPH WALK ERROR unknown mode '%s'\n", mode);
        return 1;
    }
    uint64_t base   = strtoull(argv[2], NULL, 0);
    uint64_t size   = strtoull(argv[3], NULL, 0);
    uint64_t nodes  = strtoull(argv[4], NULL, 0);
    uint64_t degree = strtoull(argv[5], NULL, 0);
    uint64_t steps  = strtoull(argv[6], NULL, 0);
    uint64_t seed   = strtoull(argv[7], NULL, 0);
    if (!base || !size || nodes < 2 || !degree || !steps) {
        printf("GRAPH WALK ERROR bad parameters\n");
        return 1;
    }

    const char *pe = getenv("MB_POLL_US");
    if (pe)
        g_poll_us = atol(pe);
    const char *te = getenv("MB_TIMEOUT_S");
    if (te)
        g_timeout_s = atol(te);
    if (g_timeout_s <= 0)
        g_timeout_s = POLL_TIMEOUT_S;

    /* Region layout + bounds. */
    uint64_t offs_off = GW_OFFS_OFF;
    uint64_t offs_bytes = (nodes + 1) * sizeof(uint32_t);
    uint64_t cols_off = (offs_off + offs_bytes + LINE - 1) & ~(LINE - 1);
    uint64_t cols_bytes = nodes * degree * sizeof(uint32_t);
    uint64_t used = cols_off + cols_bytes;
    if (used > size) {
        printf("GRAPH WALK ERROR graph (0x%llx B) exceeds region "
               "(0x%llx B)\n", (unsigned long long)used,
               (unsigned long long)size);
        return 1;
    }

    printf("[gw] poll period: %ld us%s; poll budget: %ld s\n",
           g_poll_us, g_poll_us == 0 ? " (busy-spin)" : "", g_timeout_s);
    printf("=== graph_walk_host: mode=%s N=%llu D=%llu steps=%llu "
           "seed=%llu CSR=0x%llx B @ phys 0x%llx ===\n",
           mode, (unsigned long long)nodes, (unsigned long long)degree,
           (unsigned long long)steps, (unsigned long long)seed,
           (unsigned long long)used, (unsigned long long)base);

    /* CACHEABLE mapping: /dev/mem WITHOUT O_SYNC (measured cacheable,
     * warm 12.87 ns/line vs 274.62 UC — cache_probe result). */
    int fd = open("/dev/mem", O_RDWR);
    if (fd < 0) {
        printf("GRAPH WALK ERROR open /dev/mem: %s\n", strerror(errno));
        return 1;
    }
    void *gmap = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED,
                      fd, (off_t)base);
    if (gmap == MAP_FAILED) {
        printf("GRAPH WALK ERROR mmap graph region: %s (host needs "
               "the memmap= carve in its kernel args)\n",
               strerror(errno));
        close(fd);
        return 1;
    }

    /* ---- Build the CSR graph in place (OUTSIDE the bracket) ---- */
    struct gw_header *hdr = (struct gw_header *)gmap;
    uint32_t *offs = (uint32_t *)((char *)gmap + offs_off);
    uint32_t *cols = (uint32_t *)((char *)gmap + cols_off);

    uint64_t t_build0 = now_ns();
    for (uint64_t i = 0; i <= nodes; i++)
        offs[i] = (uint32_t)(i * degree);
    /* Edge targets from a SEPARATE deterministic LCG stream (the walk
     * seed is reserved for the walk itself). */
    uint64_t erng = seed ^ 0x9E3779B97F4A7C15ULL;
    for (uint64_t i = 0; i < nodes * degree; i++)
        cols[i] = (uint32_t)(gw_rng_next(&erng) % nodes);
    hdr->magic = GW_MAGIC;
    hdr->nodes = nodes;
    hdr->degree = degree;
    hdr->steps = steps;
    hdr->seed = seed;
    hdr->offs_off = offs_off;
    hdr->cols_off = cols_off;
    hdr->reserved = 0;
    uint64_t t_build1 = now_ns();

    /* ---- Flush (OUTSIDE the bracket): §6.2 self-invalidation as
     * user-mode CLFLUSH, one line at a time. Without this the device
     * reads stale DRAM under the host's dirty cached lines. ---- */
    uint64_t flush_lines = 0;
    for (uint64_t off = 0; off < used; off += LINE) {
        mb_clflush((volatile char *)gmap + off);
        flush_lines++;
    }
    mb_mfence();
    uint64_t t_flush = now_ns();
    printf("[gw] build %llu ms; flushed %llu lines (%llu ms) -- "
           "modeled 6.2 self-invalidation cost, outside the bracket\n",
           (unsigned long long)((t_build1 - t_build0) / 1000000),
           (unsigned long long)flush_lines,
           (unsigned long long)((t_flush - t_build1) / 1000000));

    uint64_t sum = 0, t0, t1;

    if (!is_device) {
        /* ================= config 1: host runs the walk ========== */
        m5_reset_stats(0, 0);
        t0 = now_ns();
        sum = gw_walk(offs, cols, nodes, steps, seed);
        t1 = now_ns();
        m5_dump_reset_stats(0, 0);

        printf("GRAPH WALK RESULT mode=host checksum=0x%llx "
               "steps=%llu guest_ms=%llu\n",
               (unsigned long long)sum, (unsigned long long)steps,
               (unsigned long long)((t1 - t0) / 1000000));
        munmap(gmap, size);
        close(fd);
        return 0;
    }

    /* ================= config 2: ship to the device ============== */
    /* Mailbox mapping stays O_SYNC/UC — it is the control channel and
     * its contract depends on UC (cxl_mailbox.h). */
    int mfd = open("/dev/mem", O_RDWR | O_SYNC);
    if (mfd < 0) {
        printf("GRAPH WALK ERROR open /dev/mem (mailbox): %s\n",
               strerror(errno));
        munmap(gmap, size);
        close(fd);
        return 1;
    }
    void *mmb = mmap(NULL, MB_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
                     mfd, (off_t)MB_BASE);
    if (mmb == MAP_FAILED) {
        printf("GRAPH WALK ERROR mmap mailbox: %s (host needs "
               "memmap=16M$0x2ff000000)\n", strerror(errno));
        munmap(gmap, size);
        close(fd);
        close(mfd);
        return 1;
    }
    volatile struct cxl_mailbox *mb = (volatile struct cxl_mailbox *)mmb;

    if (cxl_blob_walk_len > MB_SIZE - MB_DATA_OFF) {
        printf("GRAPH WALK ERROR blob too large\n");
        goto fail;
    }

    /* Arm the mailbox: blob in the data region, descriptor = graph
     * region base/size; everything else rides the in-region header. */
    memcpy((char *)mmb + MB_DATA_OFF, cxl_blob_walk, cxl_blob_walk_len);
    mb->magic = MB_MAGIC;
    mb->version = MB_VERSION;
    mb->data_off = MB_DATA_OFF;
    mb->data_len = cxl_blob_walk_len;
    mb->arg0 = base;
    mb->arg1 = size;
    mb->arg2 = 0;
    mb->arg3 = 0;
    mb->result = 0;
    mb->status = STATUS_IDLE;
    mb_flush_range((volatile void *)mb, sizeof(*mb));
    mb_flush_range((volatile char *)mmb + MB_DATA_OFF,
                   cxl_blob_walk_len);

    /* ---- --graph-transfer: hand verification authority over the graph
     * region to the device BEFORE dispatch, and OUTSIDE the bracket.
     *
     * Armed purely by the environment (the MB_POLL_US idiom): the config
     * exports MB_XFER_MARKER with the exact string its exit-handler
     * trigger greps for, so this program hardcodes no marker and the two
     * cannot drift. Absent the variable this block does nothing.
     *
     * Order, and why each step is where it is:
     *   1. PRINT the marker FIRST. The trigger greps the serial FILE, so
     *      the bytes must have travelled libc -> tty -> UART -> Terminal
     *      before the exit is serviced. Printing ahead of the sleep gives
     *      that path the whole sleep to complete. Firing early is not a
     *      risk: no other guest emits an exit event in this window (the
     *      device is inside device_offload's doorbell poll, which uses
     *      usleep and no m5op).
     *   2. QUIESCE. releaseHeldRegion refuses (fatal) while any packet
     *      with a region address is outstanding in the host verifier,
     *      and the host's L1D/L2/L3 prefetchers will have been streaming
     *      through the region during the build and flush. Sleeping stops
     *      the demand stream, so no new prefetches are generated and the
     *      outstanding ones retire. Best effort: nothing here can prove
     *      the region is quiet -- the release's own check is the proof,
     *      and it is loud when it fails.
     *   3. m5_exit(0). Ends the simulate() slice; the handler runs with
     *      simulation paused and performs release-then-acquire; the run
     *      resumes (yield False) and this program continues. The exit
     *      event is scheduled at the current tick, so it is serviced
     *      before this CPU's next instruction -- which is what puts the
     *      whole migration strictly before the doorbell below.
     * All of this precedes m5_reset_stats, so the migration is setup and
     * both arms bracket identical work. ---- */
    const char *xfer_marker = getenv("MB_XFER_MARKER");
    if (xfer_marker && *xfer_marker) {
        const char *qe = getenv("MB_XFER_QUIESCE_US");
        long quiesce_us = qe ? atol(qe) : 0;
        printf("[gw] authority transfer: emitting marker, then "
               "quiescing %ld us\n", quiesce_us);
        printf("%s\n", xfer_marker);
        if (quiesce_us > 0)
            usleep(quiesce_us);
        m5_exit(0);
        printf("[gw] resumed after authority transfer; dispatching\n");
    }

    /* ---- The bracket: dispatch + device execution + completion
     * detection. Deliberately includes the doorbell write and the
     * polling — that is what offloading costs end to end. ---- */
    m5_reset_stats(0, 0);
    t0 = now_ns();

    mb->command = OP_WALK;
    mb_clflush(&mb->command);
    mb_mfence();

    uint32_t st = STATUS_IDLE;
    int done = 0;
    long tries = (g_poll_us > 0)
        ? (long)(((uint64_t)g_timeout_s * 1000000ULL) /
                 (uint64_t)g_poll_us)
        : LONG_MAX;
    uint64_t deadline =
        now_ns() + (uint64_t)g_timeout_s * 1000000000ULL;
    for (long t = 0; t < tries; t++) {
        st = read_status(mb);
        if (st == STATUS_DONE || st == STATUS_ERROR) {
            done = 1;
            break;
        }
        if (g_poll_us > 0)
            usleep(g_poll_us);
        else if ((t & (SPIN_CHECK - 1)) == 0 && now_ns() >= deadline)
            break;
    }
    t1 = now_ns();
    m5_dump_reset_stats(0, 0);

    if (!done || st == STATUS_ERROR) {
        printf("GRAPH WALK %s mode=device (status=%u)\n",
               done ? "FAIL" : "TIMEOUT", st);
        goto fail;
    }

    mb_clflush(&mb->result);
    mb_mfence();
    sum = mb->result;

    /* Correctness proof, OUTSIDE the bracket: recompute the identical
     * walk locally and compare. */
    uint64_t expect = gw_walk(offs, cols, nodes, steps, seed);
    printf("GRAPH WALK RESULT mode=device checksum=0x%llx "
           "expected=0x%llx %s steps=%llu guest_ms=%llu\n",
           (unsigned long long)sum, (unsigned long long)expect,
           sum == expect ? "OK" : "MISMATCH",
           (unsigned long long)steps,
           (unsigned long long)((t1 - t0) / 1000000));
    munmap(mmb, MB_SIZE);
    close(mfd);
    munmap(gmap, size);
    close(fd);
    return sum == expect ? 0 : 1;

fail:
    munmap(mmb, MB_SIZE);
    close(mfd);
    munmap(gmap, size);
    close(fd);
    return 1;
}
