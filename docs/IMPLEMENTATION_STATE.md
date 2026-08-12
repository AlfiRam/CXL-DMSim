# Implementation State

What the engine and its surrounding machinery **are**, as the tree stands
2026-08-12. Written so a future session can read this instead of reconstructing
the state from `git log` and three stale surveys.

Companion documents, all **older and partly superseded** — see §9 for exactly
which of their claims to distrust: `GEM5_PRIMER.md` (still accurate; it
describes gem5, not this fork), `INTEGRITY_ENGINE_EXTENSION_SURVEY.md`,
`TWO_VERIFIER_SUBSTRATE.md`.

Tags: **[READ]** seen at the cited line now; **[INFERRED]** with stated basis;
**[NOT FOUND]** looked for, absent; **[CONSEQUENCE]** derived. Abbreviations:
`cc` = `src/mem/integrity_verifier.cc`, `hh` = `src/mem/integrity_verifier.hh`,
`py` = `src/mem/IntegrityVerifier.py`, `f2` =
`configs/example/gem5_library/x86-cxl-f2-test.py`, `bmt` =
`src/mem/mtree/timing_bmt.cc`.

> **The single most important thing in this document.** A great deal has been
> built and almost none of it has been run. §3 is the section that says which
> is which. Nothing below should be read as "working" unless §3 says it ran.

---

## 1. Mechanism table

One row per mechanism. "Mode" is where the mechanism's *effect* is reachable,
not merely where the code compiles.

| # | Mechanism | Flag | Files | Reachable in |
|---|---|---|---|---|
| 1 | Address normalization (walk indexes 0-based protected offsets; init() requires exactly one protected range) | none (always on) | cc, hh | fatal: **elaboration**; offset math: **TIMING walk only** |
| 2 | CXL-only host verifier | `--host-integrity` | hier¹, f2 | construction/init/config.ini: **elaboration**; verification: **TIMING only** |
| 3 | Held-region root state (acquire/release roles, covering-node derivation, release-side walk panic) | `--held-region` (+ `--held-region-offset/-size`) | cc, hh, py, SConscript, hier, board², f2 | derivation + fatals: **elaboration**; acquire termination and release panic: **TIMING walk only** |
| 4 | Runtime transfer writer (`cxx_exports`, marker-triggered release→acquire) | `--runtime-transfer` | cc, hh, py, f2 | writer executes **at pause time in any mode**; its installed predicates observable **TIMING only** |
| 5 | M2 §6.2 MAC-interval handoff (older, kept, inert at defaults) | `--device-handoff` | cc, hh, py, board, f2, guest | init mapping: **elaboration**; predicate: **TIMING walk only** |
| 6 | Read-block gate — completion (holds host `status` poll, releases from a store's payload) | `--read-block` | `src/mem/ReadBlockGate.py`, `read_block_gate.{hh,cc}`, x86_board, f2 | **TIMING only** (fatals under atomic) |
| 7 | Read-block gate — dispatch (second instance; holds the **device** `command` poll) | `--dispatch-block` | same files, second instance | **TIMING only** |
| 8 | Passive CXL traffic observer at S1 | `--observe-cxl` | `CxlTrafficObserver.py`, `cxl_traffic_observer.{hh,cc}`, x86_board, f2 | counts **TIMING only**; forwards in all modes |
| 9 | Cacheability probe | `--cache-probe` | `benchmarks/cache_probe.c`, f2 | guest program; **TIMING** for a fidelity verdict |
| 10 | Graph-walk workload (host arm / device arm) | `--graph-walk host\|device` | `benchmarks/graph_walk{.h,_host.c}`, `blob_walk.c`, `device_offload.c`, f2 | **TIMING** (parser refuses atomic) |
| 11 | Guest-driven authority migration during a graph walk | `--graph-transfer` | `graph_walk_host.c`, f2 | marker+release at **pause instant**; effects **TIMING only** |
| 12 | Leaf-attachment hop correction + re-derived covering-node condition | none (always on) | `bmt`, cc | **elaboration** (derivation, cross-check) + **TIMING walk** (depth) |
| 13 | Foreign-requestorId guard | none (always on) | `mem_ctrl.cc`, `qos/mem_ctrl.cc` (+ pre-existing `abstract_mem.cc`) | **TIMING** (the atomic path was already guarded) |
| 14 | Host cache resize; `--cxl-latency`; `--host-like-device` | flags as named | f2 | **elaboration** (they configure; effects show in any timed mode) |
| 15 | Time-equivalent poll budgets, `MB_TIMEOUT_S` threaded | `--timeout-s` (+ `--poll-us`) | three guests, f2 | guest software, any mode |

¹ `src/python/gem5/components/cachehierarchies/classic/private_l1_private_l2_shared_l3_integrity_verifier_cache_hierarchy.py`
² `src/python/gem5/components/boards/device_x86_board.py`

---

## 2. What the engine is now

### 2.1 The verifier

`AbstractIntegrityVerifier : ClockedObject` (hh:70), concrete subclass
`IntegrityVerifier` contributing only delay policy. **Params** (py): four
`VectorParam.AddrRange` range lists (`dram_full/os_ranges`,
`cxl_full/os_ranges`, py:106-113), `integrity_allocation_mode`,
`integrity_tree_type`, `integrity_tree_arity` (py:115-125),
`integrity_hashing_latency` = 40 cycles, `xor_latency` = 2 (py:99-103),
`unified_upstream_cache` (py:89, set by no config [NOT FOUND]),
`handoff_range_start/size` (py:134-137), `held_region_start/size/role`
(py:155-161), and the concrete subclass's four `0t` delays (py:173-177).
**Exports** (py:71-74): `releaseHeldRegion`, `acquireHeldRegion` — the engine's
only `cxx_exports`.

**Members added since the port**: `protectedOsRange` (hh, cached at init);
`handoffRangeStart/Size/Active`, `handoffMacStart/End` (hh:183-187);
`heldRegionStart/Size/Active/Role/Range`, `heldRootNode` (hh:207-212).

**Methods** (hh): `init` (:79); `releaseHeldRegion`/`acquireHeldRegion`
(:106-107); `getProtectedOffset` (:468); `deriveCoveringNode` (:486);
`checkAndDeriveHeldRegion` (:495); `regionOutstandingPackets` (:506);
`getParentNode` (:511); `parentNodeIsSecureRoot` (:513);
`getIntegrityNodeLocation` (:529); `generateMetadataRequest` ×2 (:536,543);
`handlePacket` (:628); the hash/XOR completion chain (:661-707); and the
port/queue/ordering machinery inherited from the port.

### 2.2 The tree, after the leaf-attachment correction

The counter→tree hop now attaches at the **leaf layer** (bmt, Counter case:
`return (treeNodes - leaves) + (indexOfType(index) / arity);`). Previously it
attached at `firstOfType(TreeNode)` = 0, folding the tree onto its own top.
**This correction is in the working tree only, not in HEAD** (`git show
HEAD:src/mem/mtree/timing_bmt.cc` still shows the old comment) [READ].

**Sizing chain**, re-derived this session for the configured case (protected
2 GiB, arity 4, 64 B block, 4096 B page):

```
macCount     = ceilDiv(2^31, 64)          = 33,554,432
macNodes     = ceilDiv(macCount, 4)       =  8,388,608
counterNodes = ceilDiv(macCount, 4096/64) =    524,288
leaves       = ceilDiv(counterNodes, 4)   =    131,072
height       = ceil(log4 131072) + 1      = 9 + 1 = 10
non_leaf     = 4^9 / 3                    =     87,381   (= layers 0..8)
treeNodes    = 87,381 + 131,072           =    218,453
dataSize     = 218,453 + 524,288 + 8,388,608 = 9,131,349 nodes
             = 584,406,336 B = 557.3 MiB of metadata
MAC base     = treeNodes + counterNodes   =    742,741
firstLeaf    = treeNodes - leaves         =     87,381   (leaf layer = [87381, 218453))
```

**No sizing expression changed** with the hop correction — `dataSize` and the
MAC base are identical before and after [READ + worked].

**Ragged leaf layer**: layer 9 has capacity `4^9` = 262,144 but only 131,072
leaves are allocated (50 % populated). This is harmless: the allocated leaves
span exactly `131,072 × 16,384` = 2 GiB, so containment implies allocation
(`off + size ≤ 2 GiB` divided by the 16 KiB granule *is*
`leafIdx + arity^levels ≤ leaves`). The containment assert in
`deriveCoveringNode` is what closes it.

### 2.3 Covering-node condition, stated as a condition

A region `[offStart, offStart+size)` in protected-offset space has an exact
covering node **iff** either

- `offStart == 0 && size == protectedSize` → node **0** (the root); or
- `size == gran · arity^levels` for some `levels ≥ 0`, where `gran = arity ·
  PAGE` (= 16,384 B here), **and** `offStart % size == 0` (alignment equals
  size).

and then, hand-checkably,

```
coveringNode = layerBase(height - 1 - levels) + offStart / size
layerBase(m) = (arity^m - 1) / (arity - 1)          # first index of layer m
```

For this configuration the admissible sizes are **16 KiB, 64 KiB, 256 KiB,
1 MiB, 4 MiB, 16 MiB, 64 MiB, 256 MiB, 1 GiB**, each aligned to itself, plus
the 2 GiB root. The `arity·j + 1 ≥ leaves` clause of the old (folded)
condition is **gone**, and offset 0 is now admissible.

Worked examples, re-derived: 16 KiB at offset `0x2000_0000` → `levels = 0`,
node **120,149** (= 87,381 + 32,768). 64 MiB at offset `0x4000_0000` →
`levels = 6`, `layerBase(3) = 21`, `+ 16` → node **37**.

`deriveCoveringNode` keeps a `panic_if` cross-checking the closed form against
the tree's own hops over the whole `levels`-step climb, plus edge-exclusivity
asserts.

---

## 3. Proven versus written — read this before trusting anything above

The mode boundary, from the code: **ATOMIC** — the verifier's `recvAtomic` is
`delayReq + delayResp + sendAtomic`, no walk, no `packetLookup`; the gates
forward (and fatal on an atomic read of a gated slot); the observer forwards
without counting. **TIMING** — `processReq`/`processResp` are the only entries
to `handlePacket` and thence the walk. **KVM** — CXL DRAM is mapped as a KVM
memslot, so guest accesses **never become packets**; every inline object is
blind. **Elaboration** — constructors and `init()`, every mode.

### What has actually run

| Thing | Status |
|---|---|
| Two-System boot, KVM→ATOMIC and KVM→TIMING switch | ran |
| Cacheability probe | ran; established a `memmap=` Reserved carve mapped **without** `O_SYNC` is cacheable (warm ~12.9 ns/line vs ~274.6 UC) |
| Graph walk, host arm and device arm, checksums matching | ran, both arms, at two sizes |
| Read-block gate, completion side | ran under TIMING |
| `--host-like-device`, `--cxl-latency` | ran |

### What has NOT run — do not describe any of this as working

- **No integrity walk has ever executed against a workload.** Every integrity
  flow to date was ATOMIC or boot-only. Mechanisms 1-5 have had their
  elaboration-time behaviour exercised (fatals, derivations, config.ini) and
  their *walk* behaviour never.
- **The leaf-attachment correction has never been exercised at depth.** Its
  arithmetic was verified exhaustively on paper (all 174,762 admissible
  regions) and by the in-code `panic_if`; no walk has traversed the corrected
  hop.
- **No held region has ever been released while anyone was reading it.** The
  release precondition (`regionOutstandingPackets` scanning `packetLookup`) has
  never met a live region.
- **No device-side read has ever been held.** Mechanism 7 compiles; the device
  guest's poll loop was written assuming its reads return promptly.
- **The traffic observer has never been spliced in a run.** No object has ever
  been spliced at S1 at all.
- **`--graph-transfer` has never run.** Neither has any combined
  mechanism+measurement configuration.
- **The foreign-requestorId guard's TIMING path has never been exercised**, and
  it exists precisely because the device arm's first verified TIMING traffic
  would hit it.

### Depth arithmetic, for what a first walk would cost

Under leaf attachment every counter attaches at layer 9, so the walk is a
constant **9 tree hops → 12 metadata fetches per chain** (1 MAC + 1 counter +
10 tree nodes counting the terminating root). Under the old fold the depth was
variable, 0-9, averaging **8.11** hops → 11.11 fetches. So the correction costs
**+0.89 fetches, ≈ +8 %**, and removes a pathology in which data at protected
offset 0 walked MAC→counter→root in **3** fetches. The graph region at offset
`0x4000_0000` attached at layer 8 before and layer 9 after: **exactly +1
fetch**. Metadata cache capacity is 128 KiB / 64 B = **2,048 nodes** against a
graph tree working set of 4,096 leaves + 1,365 ancestors = **5,461** — so the
extra fetch is largely not absorbed. An acquired device walk terminating at
node 37 (layer 3) fetches 9 instead of 12, a 25 % reduction: that is the
acquire's measurable signature.

---

## 4. Flag composition matrix

Every exclusion below is a `parser.error` in f2. **R** = guards a real
resource conflict; **S** = scoping, i.e. the flows would compose but the
measurement was scoped that way.

| Exclusion | Kind | Reason from the code |
|---|---|---|
| `--device-handoff` requires `--device-integrity`, requires `--offload` | R | it rides the mailbox and needs a verifier |
| `--held-region` requires both integrity flags | R | host releases, device acquires; both verifiers must exist |
| `--held-region` × `--device-handoff` | R | two walk-termination authorities on one verifier; the verifier `init()` fatals |
| `--runtime-transfer` requires both integrity flags | R | same as held-region |
| `--runtime-transfer` × `--held-region` | R | both populate the same state; verifier fatals on double population |
| `--runtime-transfer` × `--device-handoff` | R | M2 blocks the runtime writer at the mutation point |
| `--runtime-transfer` × `--offload`/checkpoint/restore | R | all rewrite `host_cmd` |
| `--graph-walk` × `--offload`/`--cache-probe`/checkpoint/restore/`--runtime-transfer` | R | **all rewrite `host_cmd` by plain assignment, and `PASS_HOST` is a first-match elif chain — removing this yields a hang, not a crash** |
| `--graph-walk` × `--device-handoff` | S | explicitly "excluded ON PURPOSE, not as a leftover" — M2 stays out of measurement flows until chosen |
| `--graph-walk` composes with `--host-integrity`, `--device-integrity`, `--held-region`, `--read-block` | — | the fence that used to block these was scoping and was narrowed |
| `--graph-transfer` requires `--graph-walk device` + both integrity flags | R | the migration exists so the *device* walks a region whose authority it holds |
| `--graph-transfer` × `--held-region` | R | `--held-region` populates at `init()`, before the guest builds the graph, so the host is already Releaser when it writes the CSR and the first store hits the walk-entry panic |
| `--cache-probe` × `--offload`/checkpoint/restore/`--runtime-transfer` | R | host command |
| `--cache-probe` × integrity family / `--read-block` | S | "measures the PLAIN path" |
| `--read-block`, `--dispatch-block`, `--observe-cxl`, `--graph-walk` × `--atomic` | R | the mechanism cannot exist outside timing; silently measuring nothing is the worst outcome |
| same four × `--dual-kvm`; × `--kvm-boot` unless `--kvm-dest timing` | R | KVM produces no packets; an ATOMIC workload phase counts nothing |
| `--read-block`/`--dispatch-block` × checkpoint/restore | R | a held load blocks the pre-checkpoint drain (`TimingSimpleCPU::drain` refuses with an access outstanding) |
| `--host-like-device` × `--host-integrity` | R | the verifier splice lives in the SharedL3 hierarchy the ablation removes |
| `--kvm-dest` without `--kvm-boot`; `--kvm-boot` × `--atomic`; `--kvm-boot` × `--dual-kvm` | R | mode coherence |
| `--dual-kvm` × a long list | S | boot-only experiment, kept variable-free |

---

## 5. Address map

CXL window `[0x1_0000_0000, 0x3_0000_0000)` — 8 GiB. Base is a literal
(f2:1310); size derives from `host_cxl_memory.get_size()` (f2:1311).

| Region | Range (default) | Created by | Values | Guest view |
|---|---|---|---|---|
| Mailbox | `[0x2_FF00_0000, 0x3_0000_0000)`, 16 MiB | `--offload`, `--graph-walk device` | derived from window constants (f2:1312-1313) | Reserved via `memmap=` |
| Completion slot (`status`) | `mailbox + 72`, 4 B | `--read-block` | `_RB_SLOT_OFF = 72` literal + header drift check (f2:1323) | — |
| Dispatch slot (`command`) | `mailbox + 68`, 4 B | `--dispatch-block` | `_DB_SLOT_OFF = 68` literal + same drift check (f2:1331) | — |
| Verifiers' protected range | `[0x1_0000_0000, 0x1_8000_0000)`, 2 GiB | both integrity flags | `_CXL_PROTECTED_SIZE` literal "2GiB" (f2:1474), mirrored to the device board's carve and asserted equal | RAM, minus carves |
| Integrity metadata carve | `[0x1_8000_0000, 0x2_FF00_0000)`; metadata occupies the first 584,406,336 B → ends `0x1_A2D5_5540` | `--host-integrity` | derived | Reserved via `memmap=` |
| Held region | default `[0x1_2000_0000, +16 KiB)`; aligned config `[0x1_4000_0000, +64 MiB)` | `--held-region`/`--runtime-transfer`/`--graph-transfer` | **parameters** `--held-region-offset/-size` (f2:1486-1488) | Reserved via `memmap=` |
| Graph carve | `[0x1_4000_0000, +35 MiB)` at N=524288/D=16 | `--graph-walk` | base literal `_GW_BASE` (f2:1437); **size computed** from `--graph-nodes/--graph-degree` | Reserved via `memmap=`; mapped **without** `O_SYNC` → cacheable |
| Cache-probe carve | `[0x1_4000_0000, +32 MiB)` | `--cache-probe` | literals (f2:1397-1398) — **same base as the graph carve**; the two flags are mutually exclusive | Reserved |
| Observed range (observer) | = the protected range | `--observe-cxl` | derived from `_CXL_WINDOW_BASE`/`_CXL_PROTECTED_SIZE` | — |

**Graph CSR size**, re-derived: `offs_off = (4096 + (N+1)·4 + 63) & ~63` =
2,101,312; `bytes = offs_off + N·D·4` = **35,655,744 = 34.00 MiB**; carve
rounds to 36,700,160 (35 MiB). It sits at protected offset `0x4000_0000`,
which is 64 MiB-aligned, so the smallest admissible held region containing it
is **64 MiB** → node **37**. When the held region contains the graph carve, f2
emits **one** `memmap=` entry rather than two nested ones.

---

## 6. Modelling boundaries — what this engine does not do

Stated plainly because several claims above are otherwise easy to over-read.

1. **The integrity engine stores no node values.** Both live trees are mocks
   (`TimingBmt::isMocking()` and `TimingTree::isMocking()` return `true`); the
   only value-carrying tree, `IntegrityTree` (`isMocking() → false`), is
   **never instantiated** [NOT FOUND].
2. **No hashes are computed and no comparisons are performed.** The "hash" is a
   40-cycle timer and the "XOR" a 2-cycle timer; `completeXor →
   completeIntegrityVerification` runs unconditionally. **Verification cannot
   fail.**
3. **The verifier never reads a packet payload.** Grepping
   `getPtr|getConstPtr|setData` across `cc` returns **zero** hits.
4. **There is no metadata write path.** `TimingBmt::processWrite` is an empty
   body with no callers outside `mtree/`; the metadata-write branch is
   `fatal("Unimplemented metadata writes")` (cc:1470); and the metadata update
   on a data write is a **commented-out TODO** (cc:1496,
   `// metadataCache->modify(parentNode);`).
5. **A counter here is an address that generates a read, not a number held
   anywhere.** [CONSEQUENCE] Any derived counter would have nowhere to live and
   nothing to be checked against.
6. **Dispatch and completion are hardware-*timed*, not hardware-*started*.**
   Nothing can cause a device core to execute an instruction it would not
   otherwise have executed: no interrupt path from a host-System object exists
   [NOT FOUND], no exported method resumes a blocked thread, and the only
   cross-System C++ linkage is the port peer pointer created by binding
   `device_iobridge` to `cxl_mem_bus`. The only external lever is **the value
   and timing of a load the device has already issued.** The gates make the
   wait free and exact; the device still issues the load it blocks on.
7. **The observer counts traffic and cannot represent a counter.** Its coverage
   structure is one *saturating bit* per line — set membership, not magnitude —
   nothing in it is reachable by another SimObject, and it acts on no packet.
8. **Metadata is verified inbound but not outbound.** Dirty metadata evicted by
   the metadata cache reaches memory as an ordinary, *untagged* writeback: the
   metadata tag is set at exactly one site (cc:1198, in
   `generateMetadataRequest`), so cache-generated writebacks never carry it.
9. **Host DRAM is unprotected** in the `CxlOnly` configuration both verifiers
   use — an accepted modelling boundary, not an oversight.
10. **Host and device caches are not coherent** over shared CXL lines. The
    workload's correctness depends on the guest's explicit `clflush` sweep;
    nothing in the simulator enforces it.

---

## 7. Known traps — plausible wrong answers rather than errors

1. **Reading the wrong stats block.** `m5_dump_reset_stats` now dumps *and*
   resets, so block 1 is the bracket and block 2 the tail. `_gw_summary` hard-
   codes `blocks[1]`; the observer summary sums event counters across all
   blocks and takes coverage from the last (it is cumulative, recomputed at
   each dump, and does not reset). A future flow that dumps before the bracket
   shifts the numbering and both summaries would quietly describe the wrong
   block.
2. **The hand-synced mailbox offsets.** `_RB_SLOT_OFF = 72` and
   `_DB_SLOT_OFF = 68` are literals validated by a startup check that greps
   `benchmarks/cxl_mailbox.h` for `uint32_t status;` / `uint32_t command;`
   carrying `off 72` / `off 68`. **The check validates the header's comment,
   not `offsetof`** — a reordering that updates code and comment together
   drifts undetected, and a drifted slot means the gate holds the wrong bytes.
3. **A timed-out arm produces a valid-looking bracket.** `stats.txt` carries no
   timeout marker, so a bracket containing a full poll budget of fruitless
   polling looks like a slow but valid measurement. **Only the serial
   `TIMEOUT` line says otherwise. Always read the serial before trusting a
   bracket.**
4. **Two derivations drifting together.** `deriveCoveringNode`'s `panic_if`
   compares a closed form against the tree's own hops — but it cannot catch
   both being wrong the *same* way, which is exactly how the original fold
   survived. The symptom would be walk depth: metadata fetches per chain ≈ 11
   instead of ≈ 12.
5. **Mixed walk depths if a transfer lands late.** If the device began walking
   before an acquire landed, early walks climb to node 0 (12 fetches) and later
   ones stop at node 37 (9), silently averaging. `[gw-summary]`'s
   metadata/data ratio compared across the `--graph-transfer` pair is the
   evidence; an unchanged ratio means the transfer did nothing.
6. **`enable_nmp` routes around the observer's splice.** With the NMP bypass
   on, `membus` is wired straight to `cxl_mem_bus`, around `CXLMemory` and
   therefore around S1. f2 passes `enable_nmp=False`, so S1 is complete
   *today*; it is not complete in general.
7. **The completion gate's first host poll passes unheld, by design.** The host
   writes `mb->status = STATUS_IDLE` while arming — a store to the gate's slot
   with no read held — which sets `pendingStore`, so the next status read is
   forwarded rather than held. Expected; three slot stores and three slot reads
   with only the last read held is the *correct* signature, not a fault.
8. **NEW — the dispatch gate holds only the FIRST dispatch per boot.**
   `device_offload` acks by writing `mb->command = OP_NONE` when work
   completes. That store sets the dispatch gate's `pendingStore`, so the next
   device poll read is forwarded unheld and the device reverts to spinning. All
   current flows dispatch exactly once, so it does not bite — but a multi-
   dispatch flow would silently lose the mechanism after the first task.
9. **NEW — the `--cache-probe` and `--dual-kvm` reject lists are stale.**
   Neither mentions `--dispatch-block`, `--observe-cxl`, or `--graph-transfer`.
   `--cache-probe --dispatch-block` composes today: the gate arms over a
   mailbox no cache-probe flow uses, sees zero reads, and fires its
   zero-observation warn. Loud rather than silent, but the exclusion lists no
   longer say what they claim to say.
10. **NEW — a held read defeats every guest-side timeout.** Poll budgets are
    now time-equivalent, but both the iteration cap and the deadline are
    evaluated at *loop boundaries* a held reader never reaches. The gate's own
    `hold_timeout` (default 100 s simulated) is the only bound; it panics on
    expiry. Without it an unreleased hold hangs the run in silence.
11. **NEW — coverage over the protected range reads misleadingly low.** The
    observer's observed range is the full 2 GiB carve, so a 34 MiB graph yields
    ≈1.7 % coverage. The meaningful figure is the **absolute distinct-line
    count** against the CSR's own line count (35,655,744 / 64 = 557,121 lines).
12. **NEW — a line may never be written back at all.** Coverage counts lines
    whose *write-back* crossed the observation point. With a 16 MiB L3, much of
    a 34 MiB graph can still be resident and dirty at measurement time. Low
    coverage may be a true statement about what is observable, not a defect.
13. **NEW — `CleanEvict` is invisible to a write-keyed observer.** It crosses
    with neither `IsWrite` nor `HasData` (packet.cc:102-103). The observer
    counts it separately for exactly this reason. Anything else that keys on
    writes will miss clean-line evictions entirely.
14. **NEW — the two gates chain, and order matters.** With both armed the chain
    is `bus → completion gate → dispatch gate → MemCtrl`. Their slots are
    disjoint 4-byte words in the *same* 64 B line, so the whole-line `clflush`
    (a `CleanInvalidReq`, neither read nor write) is forwarded by both — this
    was verified, and had `CleanInvalidReq` carried `IsWrite` it would have
    triggered a release with garbage.
15. **NEW — the KVM blind spot is total, not partial.** Interleaved CXL ranges
    are merged into one backing store and mapped as a KVM memslot, so guest
    accesses never become packets. Every inline object observes *nothing*
    until the switch to TIMING — and a zero it reports is not a measurement.

---

## 8. Git state

Branch `main`, HEAD **`df393b89c0`** "mem, configs: Add two-verifier authority
transfer over CXL region" — which contains the original four changes
(normalization, host verifier, held root state, runtime transfer) across 7
files. **Everything in §1 rows 6-15, plus the leaf-attachment correction
(row 12), is uncommitted working-tree state.**

Modified but uncommitted: `benchmarks/{Makefile, cxl_mailbox.h,
device_offload.c, host_offload.c}`, `f2`, `src/mem/{SConscript,
integrity_verifier.cc, integrity_verifier.hh, mem_ctrl.cc,
mtree/timing_bmt.cc, qos/mem_ctrl.cc}`, `src/mem/{ReadBlockGate.py,
read_block_gate.cc, read_block_gate.hh}` (added), `src/python/gem5/components/
boards/x86_board.py`, both classic cache-hierarchy files. Untracked:
`benchmarks/{blob_walk.c, blob_walk_bytes.h, cache_probe.c, graph_walk.h,
graph_walk_host.c}` and binaries, `src/mem/{CxlTrafficObserver.py,
cxl_traffic_observer.cc, cxl_traffic_observer.hh}`, and **`docs/` itself is
untracked** — this document included.

`src/mem/mtree/` is no longer byte-identical to the ported original: the hop
correction touches `timing_bmt.cc` (one expression plus its comment). Every
other mtree file is unchanged.

---

## 9. Superseded conclusions in the older documents

Do not distrust those files wholesale — they were correct when written and they
are the record of how the fold was found. Distrust these specific claims:

- **SURVEY §3.1-§3.3 and CONTRADICTIONS #3** — the counter→tree hop attaching
  at the top of the heap, the non-contiguous coverage, the dead
  `[leaves, treeNodes)` index range, and "proper-subtree coverage of contiguous
  regions essentially does not exist". **Superseded by the leaf-attachment
  correction** (§2.2/§2.3). Coverage is now contiguous and the admissible
  region family is `arity^k`.
- **SURVEY §3.2's two-shape condition** (whole range, or 16 KiB with
  `arity·j + 1 ≥ leaves`). **Superseded**; the `arity·j + 1` clause was a fold
  artifact and offset 0 is now admissible.
- **SURVEY §3.4 and CONTRADICTIONS #2** — the raw-address vs 0-based-offset
  conflict, and MAC indices exceeding `dataSize`. **Resolved** by address
  normalization: the walk subtracts `protectedOsRange.start()`, so the window
  base indexes to 742,741, in range.
- **SUBSTRATE §4 and CONTRADICTIONS #2** — "two verifiers of identical
  (class, arity, total_data) produce pointwise-identical indices … because of
  the missing base handling". **Superseded**: index agreement now additionally
  requires the **same protected-range base**, which the config enforces with an
  explicit geometry assert rather than inheriting by accident.
- **SUBSTRATE §6 scope note (a)** — "under the walk's raw-address convention
  the device verifier never actually computes these counter indices".
  **Superseded** by normalization. Its covering-node *numbers* (node 32,768 at
  offset `0x2000_0000`) were right for the fold and are now **120,149**.
- **SURVEY §1's "[NOT FOUND] no PyBindMethod exports"** — superseded; the
  verifier now exports `releaseHeldRegion`/`acquireHeldRegion`.
- **SURVEY §5's "no config instantiates two verifiers"** — superseded by
  `--host-integrity` + `--device-integrity`.
- **SURVEY §6's "nothing mutates configuration state at runtime"** —
  superseded by the runtime transfer.
- Still accurate and worth keeping: SURVEY §0.4 and CONTRADICTIONS #4
  (vestigial machinery), CONTRADICTIONS #6 (metadata writeback bypasses
  verification), CONTRADICTIONS #7, §7 (no failure path), and the whole of
  `GEM5_PRIMER.md`.

---

## OPEN AND UNVERIFIED

1. **Whether any of §3's unexercised mechanisms behave as written.** This is
   the dominant uncertainty in the whole tree and no amount of code reading
   removes it.
2. **Whether the verifier's FIFO/retry machinery survives sustained verified
   traffic.** The strict arrival-order drain (verifier-local, not a gem5
   contract) and the `Cycles(10)` retry path have never met a workload's
   concurrency, whose source would be the three host prefetchers.
3. **Whether the release precondition can be satisfied in practice.**
   `regionOutstandingPackets` counts prefetch-generated accesses — the verifier
   makes no prefetch/demand distinction [NOT FOUND] — so a region three
   prefetchers have just streamed through may never be quiet. The guest's
   `--graph-transfer-quiesce-us` sleep is best-effort and proves nothing.
4. **Whether `device_iobridge` tolerates a long-held request.** A held device
   read reserves a response-queue slot for the whole hold; the stock `Bridge`
   has never been asked to hold one for ~10¹¹ ticks.
5. **Whether the marker reaches the serial file before its `m5_exit` is
   serviced.** The `--graph-transfer` ordering depends on the guest kernel's
   tty path completing within the printf; the pre-`m5_exit` sleep makes this
   likely, not certain. If it misses, the transfer fires at the *next* exit
   event — after the walk.
6. **Ragged-geometry paths are untested.** The 2 GiB / arity-4 configuration
   divides evenly at every level, so no `ceilDiv` rounding is exercised. A
   non-power-of-two protected size would be the first real test.
7. **Whether the observer's S1 splice elaborates at all.** No object has ever
   been spliced between `CXLMemory.mem_req_port` and `cxl_mem_bus`, and range
   propagation through that new hop is unverified.
8. **Why the metadata update on a data write was left commented out** — no
   commit message, comment, or document explains it. Named gap, not a
   reconstructed rationale.
9. **Why `unified_upstream_cache` exists but is set by no config** — likewise
   unexplained.
10. **Whether the four committed changes were meant to be a single commit.**
    HEAD squashes all four; nothing records whether that was deliberate.
