/*
 * cache_probe.c — empirical cacheability probe for a /dev/mem mapping of a
 * Reserved (memmap= carved) physical range, run on the HOST guest.
 *
 * Question it answers: does mmap(/dev/mem) of a Reserved carve WITHOUT
 * O_SYNC yield a CACHEABLE (write-back) mapping on this guest kernel
 * (Linux 5.4.49, x86-64), where the O_SYNC mapping is known-UC?
 *
 * MEASUREMENT (v2 — the first run was defeated by clock resolution):
 * this guest's CLOCK_MONOTONIC is jiffy-granular (~999,848 ns per tick,
 * HZ=1000; every v1 reading was an exact multiple), so a warm cacheable
 * pass (~16K lines at a few ns each) read as 0 ns. Fixes:
 *
 *   - The startup measures and prints the actual clock quantum.
 *   - Warm time comes from a BLOCK of passes long enough to span many
 *     quanta: 8 passes for O_SYNC (~39 ms at the measured ~300 ns/line
 *     UC latency = ~39 quanta) and 128 for no-O_SYNC (>= ~21 quanta at
 *     a plausible 10 ns/line hit; ~128 ms at the 61 ns/line ceiling the
 *     v1 zeros already imply).
 *   - rdtsc supplies per-line precision: gem5's x86 TSC is
 *     regVal + curCycle() (src/arch/x86/isa.cc:231-233), one count per
 *     simulated CPU cycle, monotonic and self-consistent because the
 *     probe runs entirely in the single post-switch TIMING mode. The
 *     tick rate is CALIBRATED against the clock over the long O_SYNC
 *     block rather than assumed. Verdicts never rest on rdtsc; the
 *     block clock decides, rdtsc quotes.
 *   - A warm block too fast for the clock is CACHEABLE by upper bound
 *     ((reading + 1 quantum) / accesses), never INCONCLUSIVE: too fast
 *     to time is the strongest evidence of caching, not an absence of
 *     evidence.
 *
 * The probe never writes a byte of the probed range in either mode
 * (randomized visit order lives in heap memory; the mailbox shares the
 * window). Modes run sequentially with full munmap/close between them
 * (x86 PAT tracks a memtype per physical range). smaps VmFlags proved
 * uninformative for cacheability in v1 (identical in both modes), so it
 * is demoted to a one-line mapping confirmation.
 *
 * Output discipline (host_offload.c precedent): every exit path prints
 * a final line beginning "CACHE PROBE"; per-mode verdicts grep as
 * "CACHE PROBE VERDICT". The f2 barrier keys on the guest-side
 * CACHEPROBE_DONE echo that follows this program unconditionally.
 *
 * Usage: cache_probe <phys_base> <size>     (e.g. 0x140000000 0x2000000)
 *
 * Build: gcc -O2 -static -Wall (see benchmarks/Makefile). No m5ops.
 */

#define _GNU_SOURCE
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/mman.h>
#include <time.h>
#include <unistd.h>

#define LINE            64ULL
#define WS_BYTES        (1ULL << 20)   /* 1 MiB working set: > 48kB L1D,
                                        * < 2MB L2 / 96MB L3            */
#define WARM_PASSES_UC  8              /* O_SYNC warm block             */
#define WARM_PASSES_WB  128            /* no-O_SYNC warm block          */
#define RATIO_CACHED    3.0            /* cold/warm >= this -> CACHEABLE */
#define RATIO_UNCACHED  1.5            /* cold/warm <= this -> UNCACHEABLE */

static volatile uint64_t g_sink;

/* Measured clock quantum (ns) and rdtsc calibration (ticks per ns);
 * tpn stays 0 until a mode's span covers >= 5 quanta. */
static uint64_t g_quantum;
static double g_tpn;

static uint64_t
now_ns(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static inline uint64_t
rdtsc(void)
{
    uint32_t lo, hi;
    __asm__ __volatile__("lfence; rdtsc" : "=a"(lo), "=d"(hi) :: "memory");
    return ((uint64_t)hi << 32) | lo;
}

/* Empirical clock resolution: shortest positive step over a few edges.
 * Prints the fact the v1 run made us infer from GCDs. */
static uint64_t
measure_quantum(void)
{
    uint64_t best = UINT64_MAX;
    for (int i = 0; i < 4; i++) {
        uint64_t a = now_ns(), b;
        do { b = now_ns(); } while (b == a);
        if (b - a < best)
            best = b - a;
    }
    return best;
}

static uint64_t g_lcg = 0x243F6A8885A308D3ULL;
static uint64_t
lcg_next(void)
{
    g_lcg = g_lcg * 6364136223846793005ULL + 1442695040888963407ULL;
    return g_lcg >> 16;
}

/* One randomized read pass over the working set. */
static void
one_pass(volatile const uint64_t *m, const uint32_t *order, uint64_t nlines)
{
    uint64_t sum = 0;
    for (uint64_t i = 0; i < nlines; i++)
        sum += m[(uint64_t)order[i] * (LINE / sizeof(uint64_t))];
    g_sink = sum;
}

/* Confirm the mapping exists in /proc/self/maps (one line; the VmFlags
 * corroboration proved uninformative for cacheability and is gone). */
static void
confirm_mapping(const void *vaddr)
{
    FILE *f = fopen("/proc/self/maps", "r");
    int found = 0;
    if (f) {
        char line[512];
        unsigned long long lo, hi;
        unsigned long long t = (unsigned long long)(uintptr_t)vaddr;
        while (fgets(line, sizeof(line), f))
            if (sscanf(line, "%llx-%llx ", &lo, &hi) == 2 &&
                t >= lo && t < hi && strstr(line, "/dev/mem")) {
                found = 1;
                break;
            }
        fclose(f);
    }
    printf("[probe]   mapping %s in /proc/self/maps (smaps VmFlags "
           "carries no cacheability bit; not dumped)\n",
           found ? "confirmed" : "NOT FOUND");
}

/*
 * Probe one mode. Verdict characters: 'C' cacheable, 'U' uncacheable,
 * 'I' inconclusive (now reachable only on genuinely intermediate
 * measurements, never on a too-fast pass), 'F' open/mmap failed.
 */
static char
probe_mode(int use_osync, uint64_t base, uint64_t size,
           const uint32_t *order, uint64_t nlines,
           double *cold_out, double *warm_out)
{
    const char *tag = use_osync ? "O_SYNC" : "no-O_SYNC";
    const uint64_t warm_passes = use_osync ? WARM_PASSES_UC
                                           : WARM_PASSES_WB;
    *cold_out = 0.0;
    *warm_out = 0.0;

    int fd = open("/dev/mem", O_RDONLY | (use_osync ? O_SYNC : 0));
    if (fd < 0) {
        printf("[probe] %s: open(/dev/mem) FAILED errno=%d (%s)\n",
               tag, errno, strerror(errno));
        return 'F';
    }
    void *map = mmap(NULL, size, PROT_READ, MAP_SHARED, fd, (off_t)base);
    if (map == MAP_FAILED) {
        printf("[probe] %s: mmap(0x%llx, 0x%llx) FAILED errno=%d (%s)\n",
               tag, (unsigned long long)base, (unsigned long long)size,
               errno, strerror(errno));
        close(fd);
        return 'F';
    }
    printf("[probe] %s: mapped phys 0x%llx (+0x%llx) at %p\n",
           tag, (unsigned long long)base, (unsigned long long)size, map);
    confirm_mapping(map);

    volatile const uint64_t *m = (volatile const uint64_t *)map;

    /* Cold pass, bracketed by both clocks. */
    uint64_t c0 = now_ns(), r0 = rdtsc();
    one_pass(m, order, nlines);
    uint64_t r1 = rdtsc(), c1 = now_ns();

    /* Warm block: warm_passes passes timed as ONE interval. */
    uint64_t cb0 = now_ns(), rb0 = rdtsc();
    for (uint64_t p = 0; p < warm_passes; p++)
        one_pass(m, order, nlines);
    uint64_t rb1 = rdtsc(), cb1 = now_ns();

    munmap(map, size);
    close(fd);

    /* Calibrate rdtsc once, from the first mode whose full span covers
     * >= 5 quanta (the O_SYNC mode's ~44 ms normally; <= 2.5% error at
     * 40 quanta). The TSC rate is CPU-cycle-constant across modes. */
    uint64_t span_clk = cb1 - c0;
    if (g_tpn == 0.0 && span_clk >= 5 * g_quantum && rb1 > r0)
        g_tpn = (double)(rb1 - r0) / (double)span_clk;

    const double n_cold = (double)nlines;
    const double n_warm = (double)(warm_passes * nlines);

    /* Cold per-line: rdtsc when calibrated (sub-ns resolution), else
     * the clock reading with quantum error. */
    double cold_pl = g_tpn > 0.0
        ? (double)(r1 - r0) / g_tpn / n_cold
        : (double)(c1 - c0) / n_cold;

    /* Warm per-line: the block clock is the VERDICT number (resolution
     * solved by block length); the +1-quantum upper bound covers blocks
     * the clock still cannot see. rdtsc quoted alongside. */
    double warm_clk = (double)(cb1 - cb0);
    double warm_pl = warm_clk / n_warm;
    double warm_pl_ub = (warm_clk + (double)g_quantum) / n_warm;
    double warm_pl_tsc = g_tpn > 0.0
        ? (double)(rb1 - rb0) / g_tpn / n_warm
        : 0.0;

    printf("[probe] %s: cold  %10.0f ns clock  (%8.2f ns/line%s)\n",
           tag, (double)(c1 - c0), cold_pl,
           g_tpn > 0.0 ? ", tsc" : ", clock-quantum-limited");
    printf("[probe] %s: warm block N=%llu  %10.0f ns  "
           "(%8.2f ns/line, ub %.2f%s%.2f tsc)\n",
           tag, (unsigned long long)warm_passes, warm_clk, warm_pl,
           warm_pl_ub, g_tpn > 0.0 ? ", " : ", no-cal ",
           warm_pl_tsc);

    *cold_out = cold_pl;
    *warm_out = warm_pl > 0.0 ? warm_pl : warm_pl_ub;

    /* Verdict. A block too fast for the clock classifies by the upper
     * bound: warm_ub << cold is cacheability, not inconclusiveness. */
    char verdict;
    double ratio;
    if (warm_pl_ub * RATIO_CACHED <= cold_pl) {
        verdict = 'C';
        ratio = cold_pl / (warm_pl > 0.0 ? warm_pl : warm_pl_ub);
    } else if (warm_pl * RATIO_UNCACHED >= cold_pl && warm_pl > 0.0) {
        verdict = 'U';
        ratio = cold_pl / warm_pl;
    } else {
        verdict = 'I';
        ratio = warm_pl > 0.0 ? cold_pl / warm_pl : 0.0;
    }

    printf("CACHE PROBE VERDICT %s: %s  cold %.2f ns/line, warm %.2f "
           "ns/line%s, ratio %s%.2f\n",
           tag,
           verdict == 'C' ? "CACHEABLE"
                          : verdict == 'U' ? "UNCACHEABLE"
                                           : "INCONCLUSIVE",
           cold_pl, warm_pl > 0.0 ? warm_pl : warm_pl_ub,
           warm_pl > 0.0 ? "" : " (upper bound)",
           warm_pl > 0.0 ? "" : ">=", ratio);
    return verdict;
}

int
main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    if (argc != 3) {
        printf("usage: cache_probe <phys_base> <size>\n");
        printf("CACHE PROBE ERROR bad-arguments\n");
        return 1;
    }
    uint64_t base = strtoull(argv[1], NULL, 0);
    uint64_t size = strtoull(argv[2], NULL, 0);
    long pg = sysconf(_SC_PAGESIZE);
    if (base == 0 || size == 0 || (base % (uint64_t)pg) != 0) {
        printf("CACHE PROBE ERROR base/size invalid (base must be "
               "page-aligned, both nonzero)\n");
        return 1;
    }

    uint64_t ws = size < WS_BYTES ? size : WS_BYTES;
    uint64_t nlines = ws / LINE;
    if (nlines < 1024) {
        printf("CACHE PROBE ERROR region too small (%llu lines; want "
               ">= 1024 for a stable verdict)\n",
               (unsigned long long)nlines);
        return 1;
    }

    g_quantum = measure_quantum();
    printf("=== cache_probe v2: phys 0x%llx size 0x%llx, working set "
           "0x%llx (%llu lines), warm blocks %d/%d passes ===\n",
           (unsigned long long)base, (unsigned long long)size,
           (unsigned long long)ws, (unsigned long long)nlines,
           WARM_PASSES_UC, WARM_PASSES_WB);
    printf("[probe] clock quantum: %llu ns%s\n",
           (unsigned long long)g_quantum,
           g_quantum > 100000 ? " (jiffy-granular, as v1 inferred)" : "");

    uint32_t *order = malloc(nlines * sizeof(uint32_t));
    if (!order) {
        printf("CACHE PROBE ERROR malloc order array failed\n");
        return 1;
    }
    for (uint64_t i = 0; i < nlines; i++)
        order[i] = (uint32_t)i;
    for (uint64_t i = nlines - 1; i > 0; i--) {
        uint64_t j = lcg_next() % (i + 1);
        uint32_t t = order[i]; order[i] = order[j]; order[j] = t;
    }

    double cold_sync, warm_sync, cold_nosync, warm_nosync;
    char v_sync = probe_mode(1, base, size, order, nlines,
                             &cold_sync, &warm_sync);
    char v_nosync = probe_mode(0, base, size, order, nlines,
                               &cold_nosync, &warm_nosync);
    free(order);

    const char *name[256] = {0};
    name['C'] = "CACHEABLE"; name['U'] = "UNCACHEABLE";
    name['I'] = "INCONCLUSIVE"; name['F'] = "MAP-FAILED";

    /* Anchor self-check (v1-proven): O_SYNC is UC by the mailbox
     * contract; if the harness measures it cacheable, distrust both. */
    if (v_sync == 'C') {
        printf("CACHE PROBE ERROR harness-invalid: O_SYNC mapping "
               "measured CACHEABLE — known-UC baseline failed, "
               "distrust both verdicts\n");
        return 1;
    }

    /* The quotable cross-mode number: UC latency over warm no-O_SYNC
     * latency for the same lines. */
    double uc_over_wb = (warm_sync > 0.0 && warm_nosync > 0.0)
        ? warm_sync / warm_nosync : 0.0;

    printf("CACHE PROBE RESULT osync=%s nosync=%s cold_osync=%.2fns "
           "cold_nosync=%.2fns warm_osync=%.2fns warm_nosync=%.2fns "
           "uc_over_wb=%.1f\n",
           name[(unsigned char)v_sync], name[(unsigned char)v_nosync],
           cold_sync, cold_nosync, warm_sync, warm_nosync, uc_over_wb);
    return (v_sync == 'F' && v_nosync == 'F') ? 1 : 0;
}
