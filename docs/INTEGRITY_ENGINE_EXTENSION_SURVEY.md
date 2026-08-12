# Integrity Engine Extension Survey

Substrate investigation for extending the counter-mode-encryption + Bonsai-Merkle-Tree
integrity engine in this repository (`~/CXL-NMP`, gem5 v23.1 base). This document describes
what exists and what constrains a future design. It deliberately does not design anything.

Evidence tags: **[READ]** = seen in this repository at the cited line. **[INFERRED]** =
reasoned from read facts, stated with its basis. **[NOT FOUND]** = looked for, absent.
**[CONSEQUENCE]** = what a change *would* have to touch, derived from a read fact.
All `file:line` references are from this repository unless prefixed `upstream:`.

---

## STEP 0 — The port

### 0.1 Where the engine lives in THIS repo [READ]

| Piece | Path |
|---|---|
| Verifier SimObject decl (Python) | `src/mem/IntegrityVerifier.py` (134 lines) |
| Verifier C++ | `src/mem/integrity_verifier.hh` (935), `src/mem/integrity_verifier.cc` (2228) |
| Tree abstract base | `src/mem/mtree/abstract_tree.hh` / `.cc` |
| BMT tree (default) | `src/mem/mtree/timing_bmt.hh` / `.cc` |
| Plain Merkle tree | `src/mem/mtree/timing_tree.hh` / `.cc` |
| Value-carrying tree (unused, see §0.4, CONTRADICTIONS) | `src/mem/mtree/tree.hh` / `.cc` (`class IntegrityTree`) |
| Geometry helpers | `src/mem/mtree/util.hh` / `.cc` |
| Python geometry mirrors | `src/mem/mtree/TimingBmt.py`, `src/mem/mtree/TimingTree.py` (PySource'd into `gem5.components.memory.mtree`, `src/mem/mtree/SConscript:15-20`) |
| Metadata cache — C++ *model* (unused, see §0.4) | `src/mem/cache/metadata_cache.hh` / `.cc` |
| Metadata cache — the one actually used | `src/python/gem5/components/cachehierarchies/classic/caches/metadata.py:38` (`ClassicMetadataCache(Cache)`) |
| Host cache-hierarchy component | `src/python/gem5/components/cachehierarchies/classic/private_l1_private_l2_shared_l3_integrity_verifier_cache_hierarchy.py` |
| Device-side verifier wiring | `src/python/gem5/components/boards/device_x86_board.py:142-219, 415-451` |
| Request/Packet hooks | `src/mem/request.hh:473-482, 553-580`; `src/mem/packet.hh:636-650` |
| Range-list helpers (engine-added) | `src/base/addr_range_list.hh` |
| Build registration | `src/mem/SConscript:69-75,115,162-170`; `src/mem/mtree/SConscript`; `src/mem/cache/SConscript:38,52-53` |
| Configs that instantiate a verifier | `configs/example/gem5_library/x86-integrity-host-run.py` (host, DramOnly); `configs/example/gem5_library/x86-cxl-f2-test.py` (device, CxlOnly, via `DeviceX86Board`) |

### 0.2 Upstream comparison [READ]

`~/gem5-jerrett` is present, on branch `jerrettl/project2-cxl` (HEAD `efd2e23a87`). Its gem5
base is **v24.1.0.1** (`upstream:src/base/version.cc`); this repo is **v23.1.0.0**
(`src/base/version.cc`) — the port was cross-version.

Byte-identical to upstream: all of `src/mem/mtree/*` (both C++ and the Python mirrors),
`src/mem/cache/metadata_cache.{hh,cc}`, `src/base/addr_range_list.hh` [READ, `diff -q`].

Different from upstream: `src/mem/integrity_verifier.{hh,cc}`, `src/mem/IntegrityVerifier.py`,
`src/mem/packet.hh`, `src/mem/request.hh`, and the hierarchy component (fresh-authored, see
below). The differences fall into three groups:

1. **Excisions.** The upstream engine's PageSwapper (SimObject, request/packet hooks,
   `hasBeenTranslated`/`getPageSwapAddr`), `InstrumentedXBar`, the partition managers
   (`IntegrityPartitionManager`, `DataLocationPartitionManager`, way-partitioning policies),
   the `IntegrityMetadata` debug flag, and the `IntegrityVerifierAll` compound flag were not
   ported [READ, diff of `src/mem/SConscript` and `src/mem/packet.hh`]. The stat code that
   used the page-swapper's translated address was collapsed to `translatedAddr =
   pkt->getAddr()` with an explanatory comment (`src/mem/integrity_verifier.cc:1456-1462`).
   The `*Trans*` stat buckets survive but now double the untranslated buckets.

2. **Fresh-authored config layer.** The hierarchy component was written new for this port
   rather than ported, explicitly to avoid importing the unported partition SimObjects
   (its own header comment, `private_l1_..._integrity_verifier_cache_hierarchy.py:10-16`).
   It drops upstream's unified-L1, unified-upstream-cache, partitioned-metadata-cache, NCX,
   and page-swapper branches, and changes `metadata_cache_size` semantics from an entry
   count (upstream multiplies by 64) to a memory-size string
   (`...integrity_verifier_cache_hierarchy.py:71-72,185-188`). `DeviceX86Board`'s verifier
   wiring (`device_x86_board.py:415-451`) has no upstream counterpart at all.

3. **Additions not in upstream — important.** This repo already contains a partial,
   *statically configured* version of the mechanism you are planning: a "§6.2 range-keyed
   subtree handoff". Concretely:
   - Params `handoff_range_start` / `handoff_range_size` on the verifier
     (`src/mem/IntegrityVerifier.py:110-122`);
   - members + `init()`-time mapping of the address range to a MAC-leaf-index range
     (`src/mem/integrity_verifier.hh:132-144`, `src/mem/integrity_verifier.cc:80-86,229-282`);
   - a widened secure-root predicate: the walk terminates at any MAC node inside
     `[handoffMacStart, handoffMacEnd)` in addition to node 0
     (`src/mem/integrity_verifier.cc:675-692`);
   - board plumbing `cxl_handoff` / `cxl_handoff_size` (`device_x86_board.py:154-219`),
     config flags `--device-integrity` / `--device-handoff`
     (`x86-cxl-f2-test.py:553-575`), and a guest-side `OP_HANDOFF` mailbox opcode
     (`benchmarks/cxl_mailbox.h:45-69`, `benchmarks/host_offload.c:275`,
     `benchmarks/device_offload.c:259`).

   The "§6.2" comments reference a section number of some prior document, not anything in
   this repo [INFERRED from the comment style]. **This mechanism is fixed at elaboration
   (params → `init()`); nothing about it changes at runtime, no region object exists, no
   tree-node id is involved, and no authority is *released* by the host verifier (the host
   config in f2 has no verifier at all — see §5).** So the port has diverged materially in
   exactly the direction you are planning, but only as a static, one-sided, MAC-range
   approximation. Your prompt's premise "almost nothing I described exists" is therefore
   *partly* wrong for this repo; see CONTRADICTIONS #1.

### 0.3 Everything else in this repo describes THIS repo's code, not upstream's.

### 0.4 Two ported-but-dead subsystems worth knowing about up front [READ]

- `IntegrityTree` (`src/mem/mtree/tree.hh:117`) — the only tree that stores actual hash
  bytes (`Block* root; Block** data;`, tree.hh:144-148, `isMocking() == false`,
  tree.hh:131) — is **never instantiated anywhere** (grep over `src/`: only its own
  definition). The trees that run are `TimingTree`/`TimingBmt`, both `isMocking() == true`
  (timing_bmt.hh:188), storing no values.
- The C++ `AbstractMetadataCache`/`MetadataCache`/`PartitionedMetadataCache` model
  (`src/mem/cache/metadata_cache.hh`) is compiled (`src/mem/cache/SConscript:38`) but
  **never instantiated** (grep: no `new MetadataCache`, no member of that type in the
  verifier). The datapath metadata cache is the stock classic `Cache` subclass
  `ClassicMetadataCache` (metadata.py:38). Related verifier state is also dead:
  `pendingMetadataEvictions` is read (`integrity_verifier.cc:703-704`) but never inserted
  into; `outstandingMetadataEvictions` is only sized/printed
  (`integrity_verifier.cc:1713,2083-2098`). So `parentNodeIsPendingEviction()` is
  constant-false [INFERRED from the absence of any insert].

---

## 1. The author's style, concretely

The engine has two authorial layers plus a porter's overlay, and they are visually
distinguishable: the verifier and `timing_bmt.cc` use gem5-style 4-space indentation and
`DPRINTF`; the older `tree.cc`/`timing_tree.cc` use 2-space indentation and `std::cout`
(12 and 16 occurrences respectively [READ, grep]); the port's additions announce themselves
with `§6.2`/"excised in the CXL-NMP port" comment prefixes
(`integrity_verifier.cc:80,229,1457`). "The author's style" below means the verifier/BMT
layer, which is what everything live is written in.

**Polymorphism and division of labor.**
- SimObject side: one abstract base owns *all* mechanism — ports, queues, the walk, stats
  (`AbstractIntegrityVerifier`, declared `abstract = True` in Python,
  `IntegrityVerifier.py:53-57`); the concrete subclass contributes only policy through tiny
  virtual hooks: `delayReq`/`delayResp`/`delaySnoopResp` default to 0 in the base
  (`integrity_verifier.hh:774-788`) and the concrete `IntegrityVerifier` overrides two of
  them with constant param-driven delays (`integrity_verifier.hh:914-931`,
  `integrity_verifier.cc:2195-2226`).
- Helper side: a pure-virtual API class (`AbstractIntegrityTree`, abstract_tree.hh:10-117)
  with concrete implementations; the *user* of the hierarchy holds only the abstract pointer
  (`AbstractIntegrityTree *integrityTree`, integrity_verifier.hh:84). Same shape in the
  (dead) metadata-cache model (metadata_cache.hh:22,164,537).

**How behavior is selected.**
- **Enum params** for structural choices, declared as Python `Enum` classes and registered
  in the SConscript `enums=` list: `IntegrityTreeType`, `IntegrityAllocationMode`,
  `MetadataCacheType` (`IntegrityVerifier.py:41-51`, `src/mem/SConscript:69-75`), consumed
  by `switch`/`if-else` chains in C++ (tree construction switch,
  `integrity_verifier.cc:147-164`; allocation-mode branches, cc:292-335, 713-774).
  Unimplemented enum combinations `panic()` (cc:332-333, 747).
- **Bool params** for wiring variants (`unified_upstream_cache`, IntegrityVerifier.py:72-78).
- **Param-as-sentinel** (porter's layer): `handoff_range_size == 0` disables the feature
  (`IntegrityVerifier.py:120-122`, cc:84).
- **Subclass choice** only for the delay-policy hooks (above). Configs select trees by
  *string→enum param*, not by picking a subclass (hierarchy py:68, 177).

**SimObject vs plain C++ — the discernible rule.** Objects that sit on the packet path,
carry ports, a clock, params, or stats are SimObjects (`AbstractIntegrityVerifier` is a
`ClockedObject`, integrity_verifier.hh:69; the real metadata cache is a stock classic
`Cache` configured in Python, metadata.py:38). Pure arithmetic/bookkeeping is plain C++,
constructed with `new` in the owner's constructor and deleted in its destructor
(tree: cc:147-164, 187-190). Nothing in the engine exposes `PyBindMethod` exports
[NOT FOUND; precedent exists elsewhere in-tree, e.g. `src/cpu/BaseCPU.py:67-70`].

**Timing costs — three tiers.**
1. Parameterized compute latencies in `Cycles`: `integrity_hashing_latency` (default 40),
   `xor_latency` (default 2) (`IntegrityVerifier.py:82-86`), consumed via
   `clockEdge(latency)` when scheduling completion events (cc:897-900, 1015-1018).
2. Parameterized pass-through delays in `Latency` ticks defaulting to `0t`
   (`read_req`/`read_resp`/`write_req`/`write_resp`, IntegrityVerifier.py:130-134) via the
   `delayReq`/`delayResp` hooks — these are the *only* delays applied on the atomic path
   (cc:390-395).
3. Hardcoded: `clockEdge(Cycles(1))` on every port scheduling (cc:1296, 1314, 1333, 1348),
   `Cycles(10)` retry backoff (cc:837, 843), block size 64 and page size 4096 as class
   constants (timing_bmt.hh:95,100), a 64-byte metadata request size (cc:801), a
   500,000,000-tick stuck-packet threshold (cc:1697), and the `CYCLES_*` constants inside
   `TimingTree` (timing_tree.hh:104-163) which the live walk never consults.

**Config-visible state and the Python/C++ geometry sync.** State is exposed to configs
exclusively through construction-time params (including `VectorParam.AddrRange` lists,
IntegrityVerifier.py:88-96). Geometry is *mirrored*, not exported: hand-written Python twins
`TimingBmt`/`TimingTree` re-derive node counts with explicit sync contracts on both sides —
"Note that this should be in sync with the Python version" (timing_bmt.cc:19) / "Note that
this should be in sync with the C++ version" (TimingBmt.py:39), plus "NOTE Sync with
Python" on individual functions (timing_bmt.cc:290, 297). In this repo the mirrors are
compiled in but imported by no config (grep over `configs/` and `src/python/` excluding
`src/mem/mtree`: nothing) [READ]; upstream configs did use them
(upstream:`configs/integrity_verifier/create_board.py`).

**Bookkeeping idiom.** Ordering is enforced with paired FIFO-queue + ready-set structures
(`requestQueue`/`requestReady`, `responseQueue`/`responseReady`,
integrity_verifier.hh:366-390) drained in arrival order (cc:1190-1224, 1242-1258); every
container has add/remove/has helper methods that `assert` invariants and `DPRINTF` the new
size (cc:1522-1574, 1577-1631); lifecycle verbs are tiered `mark*` → `sched*` → `send*`
(hh:610-680); one-shot work is an `Event` subclass with `AutoDelete` holding
`(verifier, pkt)` (hh:436-457, 519-540, 558-579); asserts are used liberally as protocol
documentation (e.g. cc:447-450, 538-539, 578-579, 1286-1292).

**Naming and layout.** C++ files snake_case beside a CamelCase SimObject `.py`
(`src/mem/IntegrityVerifier.py` + `integrity_verifier.cc`); debug flags named per class
with `Init`/`Reqs`/`Resps` suffixes (`src/mem/SConscript:162-170`,
`src/mem/mtree/SConscript:9-13`); stats in a nested `statistics::Group` explicitly named
`"integrity_verifier"` with `ADD_STAT` + units and `Formula` averages wired in the
constructor body (cc:1721-1941), plus a `preDumpStats()` override for derived footprint
stats (cc:1943-1994); section banners `////// API //////` in headers (abstract_tree.hh:28).
New files of each kind would go: tree variants → `src/mem/mtree/` (+ `Source()` +
`DebugFlag()` in its SConscript), verifier-adjacent SimObjects → `src/mem/` (+ SConscript
`SimObject()`/`Source()`), stdlib cache pieces →
`src/python/gem5/components/cachehierarchies/classic/` (+ `PySource` in
`src/python/SConscript` — the hierarchy is registered there), run configs →
`configs/example/gem5_library/` [READ from existing placement].

**What would make an addition look native vs bolted on.** Native: a new enum value plus a
`switch` case that `panic()`s when unimplemented; a new `Cycles` param consumed via
`clockEdge`; a new tracking container with assert-and-DPRINTF helpers; an `AutoDelete`
event; `ADD_STAT`ed counters with units; a Python kwarg threaded board→hierarchy→param; a
sync-comment on any geometry that exists twice; `fatal()` for config errors at `init()`,
`panic()` for engine bugs. Bolted on: runtime setters or `PyBindMethod` exports (none
exist), storing values in the mocked trees, `std::cout`, bypassing the
queue/ready ordering discipline, or keying state off packets outside the
`packetLookup`/req-keyed maps.

---

## 2. The protection predicate and its extension surface

**The predicate** [READ]. `needsVerification(pkt)` (`integrity_verifier.cc:338-352`):

```
(pkt->isRead() || pkt->isWrite()) &&
addr ∈ dramOsRanges ∪ dramIntegrityRanges ∪ cxlOsRanges ∪ cxlIntegrityRanges
```

with `rangeListContains` a linear scan over an `AddrRangeList`
(`src/base/addr_range_list.hh:12-19`). It depends on six `AddrRangeList` members
(integrity_verifier.hh:120-125): the four param-fed lists plus two *derived* integrity
lists computed in the constructor by subtracting OS ranges from full ranges — the carve
loop at cc:88-137 — under the documented structural contract that "the full ranges are
identical to the OS ranges, but there may be additional space at the end"
(integrity_verifier.hh:110-118).

What the predicate actually gates, per call site [READ]:
- Requests: express snoops bypass entirely (cc:431-433); verified *writes* are held for
  verification before forwarding (cc:458-461); verified reads and everything else are
  forwarded and handled on the response (cc:464-471). Non-read/write commands are never
  verified (cc:345-346).
- Responses: verified reads are held for verification (cc:527-531); write responses fall
  through (cc:533-541).
- The predicate sees only traffic that reaches the splice point — below the LLC on the host
  (hierarchy py:174-182: `L3.mem_side → verifier → membus`) or on the device's CXL-ingress
  bridge path (device_x86_board.py:415-451). CPU-side cache hits never reach it
  [INFERRED from the splice topology].
- Metadata traffic is distinguished *not* by this predicate but by the request tag
  (`isMetadataRequest()`, packet.hh:638) and by address-in-integrity-range membership
  (cc:436-443, 578-579).

**Where the range lists come from, who writes them, when** [READ]. Written as Python params
at config-construction time: the host hierarchy computes `[AddrRange(full)]` /
`[AddrRange(os)]` from board memory size minus a `integrity_reserve_size` kwarg
(hierarchy py:192-205); the device board computes CXL-window ranges, excluding the top
16 MiB mailbox from `full` (device_x86_board.py:176-194). Consumed once in the C++
constructor (cc:63-66), validated at `init()` (`hasValidRanges`/`treeSizeValid`,
cc:212-227). Per `GEM5_PRIMER.md` §1.4, params are frozen at `m5.instantiate()`; nothing
re-reads them later. The host config additionally enforces the carve on the *guest* via a
kernel `mem=` argument, because an OS access into the integrity range trips
`assert(!rangeListContains(integrityRanges, addr))` in `processReq`
(x86-integrity-host-run.py:108-112; the assert at cc:447-450).

**Could two protection statuses coexist?**
- The range machinery itself is status-free: `AddrRangeList` + helpers are flat sets of
  disjoint ranges; nothing in them encodes "one status" [READ, addr_range_list.hh]. Adding
  another list is mechanically identical to the existing six.
- What *is* structurally single-status [READ]:
  1. `needsVerification` returns a bool — protected or not; there is no third value
     (cc:338-352).
  2. The constructor's carve logic hard-codes "integrity = full minus OS, at the tail"
     (cc:88-137; contract at hh:110-118).
  3. The stats classify every request into exactly the {dram,cxl} × {Os,Integrity} matrix
     via cascaded `rangeListContains` (cc:1400-1510, 1958-1993); a new status has no bucket.
  4. Asserts pin the two-status world: data requests must *not* be in integrity ranges
     (cc:447-450, 537-539, 1097-1098), metadata requests must be (cc:578-579, 1286-1292,
     1325-1326).
  5. The handoff addition already demonstrates a third status ("protected but re-rooted")
     and chose to express it *outside* the range lists, as a MAC-index interval checked
     only in the secure-root predicate (hh:132-144, cc:686-691) — the range machinery was
     not extended for it. Its `init()` code also assumes a *single* protected region
     (`cxlOsRanges.front()` / `dramOsRanges.front()`, cc:238-244), which is narrower than
     the multi-range contract the rest of the engine honors.
- [CONSEQUENCE, from the five points above] A distinguished region coexisting with ordinary
  protected memory would have to either add a new range list + predicate branch + stat
  buckets + assert updates (the pattern of points 1-4), or follow the handoff precedent of
  an index-interval attribute consulted at specific walk decision points (point 5). Both
  attachment styles exist in the code today; which is right is a design decision this
  document does not make.

---

## 3. Tree geometry and subtree addressability

All arithmetic below is taken from the code, then worked exactly for the configured cases.
Both live configs default to `TimingBmt`, arity 4 (hierarchy py:68-69;
device_x86_board.py:148-149; x86-integrity-host-run.py:80-82).

### 3.1 The maps, as implemented [READ]

`TimingBmt` lays all nodes in one linear index space, 64 B per node
(`simulatedBlockOffset(i) = i·64`, timing_bmt.cc:157-161):

```
[0, treeNodes)                      TreeNode segment
[treeNodes, treeNodes+counterNodes) Counter segment
[treeNodes+counterNodes, dataSize)  MAC segment          (timing_bmt.cc:249-263)
```

Sizing for protected size `T` (timing_bmt.cc:10-102): `macCount = T/64`,
`macNodes = macCount/4`, `counterNodes = T/4096` (64 split counters per 4 KiB page),
`leaves = ceil(counterNodes/arity)`, `height = ceil(log₄ leaves)+1`,
`nonLeaf = 4^(height−1)/3` (integer division), `treeNodes = nonLeaf + leaves`.

Walk hops:
- **data → MAC**: `addressToBlockIndex(a) = firstOfType(MAC) + a/(64·arity)`
  (timing_bmt.cc:210-225), called with the **raw packet address**
  (`getParentNode`, integrity_verifier.cc:660-672). One MAC node covers
  `64·arity = 256 B` of data.
- **MAC → Counter**: `firstOfType(Counter) + macIdx/scale`, `scale = 64/4 = 16`
  (timing_bmt.cc:188-203).
- **Counter → tree**: `firstOfType(TreeNode) + counterIdx/arity` — note
  `firstOfType(TreeNode)` is **0** (timing_bmt.cc:136-139,180-186). So counters attach to
  tree indices `[0, leaves)`, i.e. to the **top** of the heap, not to a leaf level.
- **tree → tree**: plain heap climb `(i−1)/arity`, root = index 0, with
  `assert(index != 0)` (timing_bmt.cc:164-178).

The comment on the counter hop says "the tree leaf node that is protecting it"
(timing_bmt.cc:181-182), but the arithmetic does not offset by `nonLeaf` the way
`TimingTree::addressToBlockIndex` does for its real leaf layer (timing_tree.cc:197-234).
Effect [INFERRED, pure arithmetic from the two formulas]: the walk uses an *overlapped
heap* of indices `[0, leaves)` in which every node both carries hashes and has `arity`
counter children `{4j..4j+3}`; the allocated tail `[leaves, treeNodes)` — exactly
`nonLeaf` nodes — is never produced by any hop and is dead index space. See
CONTRADICTIONS #3.

### 3.2 Exact single-covering-node condition, derived

Define counter-relative index `c = offset/4096` for a 0-based protected offset. Tree node
`j` covers, transitively, the counter set

```
C(j) = {4j..4j+3} ∪ ⋃_{k ∈ {4j+1..4j+4}, k < leaves} C(k)          [from the two hop rules]
```

- If `4j+1 ≥ leaves` (no heap children carry counters): `C(j) = {4j..4j+3}` — a contiguous,
  4-counter-aligned block = **4 pages = 16 KiB of data** (arity 4).
- If `j` has counter-bearing heap children: `C(j)` contains `{4j..4j+3}` and then jumps to
  `{16j+4..16j+19}`. These are adjacent iff `16j+4 = 4j+4`, i.e. **iff j = 0**. For j = 0
  the union telescopes to *all* counters; for any j > 0 there is a gap (the missing block
  belongs to j's heap siblings).

**Therefore, in `TimingBmt` as implemented: a contiguous, aligned data range has a single
tree node whose descendants cover exactly that range and nothing else in only two cases:**

1. the whole protected range (node 0, the root); or
2. a 16 KiB range, 16 KiB-aligned in protected-offset space, whose attachment node
   `j = offset/16 KiB` satisfies `4j+1 ≥ leaves` — i.e. `offset ≥ 16 KiB·(leaves−1)/4`,
   roughly the **top three-quarters** of the protected range.

No range larger than 16 KiB, and no range in the bottom quarter of the address space, ever
has an exact covering node. **For realistic region sizes, single-node subtree
addressability does not exist in this tree.** This is plausibly *why* the earlier handoff
addition keys on MAC-index ranges and says so: "topology-independent, unlike tree node ids"
(integrity_verifier.cc:233-236). The MAC segment, by contrast, is a linear image of the
address space, so any contiguous 256 B-aligned range maps to a contiguous MAC interval
(timing_bmt.cc:210-225) — that is the addressability the code actually offers.

### 3.3 Concrete worked example (the host config's real numbers)

`x86-integrity-host-run.py` defaults: 3 GB DRAM, 1 GiB reserve → protected
`T = 2 GiB = 2³¹` (x86-integrity-host-run.py:85-116), arity 4, `TimingBmt`:

- `macCount = 2²⁵ = 33,554,432`; `macNodes = 2²³ = 8,388,608`
- `counterNodes = 2¹⁹ = 524,288`; `leaves = 2¹⁷ = 131,072`
- `height = ceil(log₄ 131072)+1 = 9+1 = 10`; `nonLeaf = 4⁹/3 = 87,381`
- `treeNodes = 218,453`; `dataSize = 9,131,349` nodes = 584,406,336 B ≈ 557 MiB
  (consistent with the config's "~553MB" note, x86-integrity-host-run.py:102-104)
- Segment bases: Counter at 218,453; MAC at 742,741.

Pick a plausible region: **1 MiB at protected offset 0** (the shape the existing handoff
uses on the device side, `cxl_handoff_size` default "1MiB", device_x86_board.py:159).
- MAC interval: `[742741, 742741+4096)` — contiguous, exactly the region. ✔
- Counter interval: relative counters 0..255.
- Covering tree node: counter 0 attaches to node 0 — the **root**. The only tree node whose
  descendants include counter 0 is the root, which covers all 524,288 counters. **No proper
  covering node exists for this region.** Even though 1 MiB = 4³·16 KiB is a "perfect
  subtree size" on paper, the implemented index math has no node for it.
- The only exactly-covered regions in this config: 16 KiB blocks at offsets
  ≥ 16 KiB·(131,072−1)/4 ≈ **512 MiB**, plus the whole 2 GiB range.

For completeness, `TimingTree` (selectable but not default): a proper heap with real leaf
layer `firstLeaf = 4^(h−1)/3` and leaf coverage 256 B (timing_tree.cc:197-234, 140-147).
There the classical condition holds: size `= 256·4^k` bytes and offset ≡ 0 (mod size)
yields a single covering node k levels up — subject to raggedness at the rounded-up last
level (`leaves = ceil(...)`, timing_tree.cc:30-35), where a covering node may also span
phantom leaves past the protected end [INFERRED, from the ceil]. But `TimingTree` has no
counters or MACs at all (`getNodeType` returns TreeNode always, timing_tree.cc:190-194),
so it is not the BMT semantics the engine models.

### 3.4 Raw address vs 0-based offset — an unresolved convention [READ + INFERRED]

`addressToBlockIndex` divides the raw address with no base subtraction
(timing_bmt.cc:210-225), and `getParentNode` feeds it `pkt->getAddr()` directly (cc:670).
That is exact when the protected range starts at 0 — true for the host config
(`AddrRange(os_size)` starts at 0, hierarchy py:204-205). The device verifier's protected
range starts at 0x1_0000_0000 (device_x86_board.py:180-194). Worked: for a device data
access at the CXL base, MAC index = 742,741 + 2³²/256 = 742,741 + 16,777,216 =
17,519,957 ≥ `dataSize` (9,131,349 for a 2 GiB window) → `assert(index < dataSize)` in
`getNodeType` (timing_bmt.cc:252) would fire on the first timing-mode verified access
[INFERRED — arithmetic only; not executed]. Meanwhile the handoff `init()` code explicitly
normalizes to 0-based offsets before calling the same function ("addressToBlockIndex's
convention", cc:255-269), so walk-computed MAC indices (raw) and handoff MAC bounds
(offset) live in different coordinate systems for any non-zero-based region. The f2
config's own help text says these device flags were gated under `--atomic` ("the gate is
build+boot+routing (config.ini), not stats", x86-cxl-f2-test.py:560-575) — and the atomic
path never walks the tree (§6), so this inconsistency would not have surfaced there. See
CONTRADICTIONS #2.

### 3.5 Pre-elaboration checkability

Yes — expressible in the Python mirror's terms. `TimingBmt.py` reproduces `arity`,
`tree_nodes`, `counter_nodes`, `mac_nodes`, `leaves`, `height` and hardcodes the same
64/4096 constants (TimingBmt.py:34-124), which is everything §3.2's condition needs
(`leaves`, arity, page size). The mirror is already compiled into the binary
(`src/mem/mtree/SConscript:15-20`) though no config in this repo currently imports it
[READ]. The handoff code's own alignment precondition (MAC granularity `64·arity`) is
already checked twice, once in Python (device_x86_board.py:209-213) and once in C++
(cc:258-267) — the existing pattern for such checks.

---

## 4. The root, and what "terminate earlier" would touch

**Every site where the walk decides it has reached the root, or index 0 is special** [READ]:

1. `parentNodeIsSecureRoot(pkt)` — *the* termination predicate
   (integrity_verifier.cc:675-692): metadata packet AND (node == 0 OR, when handoff is
   active, MAC node in `[handoffMacStart, handoffMacEnd)`). Its three call sites:
   - `handlePacket` cc:913-924 — skips generating a parent metadata request ("Consider it
     instantly fulfilled");
   - `hasOutstandingMetadataRequest(pkt)` cc:1639-1643 — reports no pending parent, which
     is what lets `attemptXor` proceed (cc:1004);
   - `parentNodeIsPendingEviction` cc:696-700 — short-circuits the (dead) eviction check.
2. `getParentNode` asserts it is never asked for the parent of node 0 (cc:663-666).
3. `TimingBmt::parentBlockIndex` asserts `index != firstOfType(TreeNode)` (== 0)
   (timing_bmt.cc:174).
4. `TimingTree::parentBlockIndex` throws `-1` for index 0 (timing_tree.cc:140-147), caught
   only by the dead `processWrite*` loops (timing_tree.cc:77-93).
5. `Request::_metadataNode` defaults to 0 for every request (request.hh:494-495, 511, 522)
   — an untagged packet "carries" node 0; only the `isMetadataRequest()` guard in (1)
   keeps that from meaning "root".
6. The dead metadata-cache model uses node 0 as a "no replacement" sentinel
   (metadata_cache.hh:98-100, 352-354).

**What "root" actually is here.** A predicate, not a value. There is no stored root hash
and no on-chip root register anywhere in the verifier or trees [NOT FOUND]. Moreover, the
root *node's contents* live in external memory like every other node: when node 1..4 needs
its parent, `generateMetadataRequest(0)` builds a real read to
`getIntegrityNodeLocation(0)` = the first integrity-range address (cc:783-832, 708-781),
and when that response arrives, `parentNodeIsSecureRoot` is true and it is trusted without
any further check (cc:913-924). Trust is by index, applied per-packet, at walk time. The
handoff addition widened exactly this predicate and nothing else in the C++ walk.

**[CONSEQUENCE] The complete agreement set if the walk terminated at a non-zero node for
some addresses** (each item follows from the cited read fact):

- The three consumers of `parentNodeIsSecureRoot` (sites in item 1) — already unified
  behind one function, so one edit point *for the timing walk*.
- `getParentNode`'s `assert(node != 0)` (item 2) and the tree classes' own root guards
  (items 3, 4) — currently unreachable for a re-rooted node only because termination
  happens before the parent query; any path that queries parents independently of the
  predicate (none exists today [NOT FOUND]) would have to consult the same authority.
- The identity of "which node" must be expressed in a coordinate system the walk can
  check from a *metadata packet alone*: after the first hop, the original data address is
  gone and only `getMetadataNode()` remains (the handoff comment states this exact
  constraint, cc:229-236). Anything keyed on tree-node ids inherits §3's finding that
  covering nodes don't exist for realistic regions in `TimingBmt`.
- Metadata-cache contents are keyed by *address* in the integrity range
  (`ClassicMetadataCache` is a stock address-indexed cache; metadata requests carry
  addresses from `getIntegrityNodeLocation`, cc:794-804). Termination-boundary changes do
  not change addresses, so the cache needs no structural agreement — but stale cached
  ancestors above a new boundary are simply never re-requested, not invalidated
  [INFERRED from the request-driven design; no invalidation API exists on the metadata
  path, NOT FOUND].
- Stats: no root-specific stat exists [NOT FOUND in cc:1721-1994]; metadata requests are
  binned by address region only, so no agreement needed.
- Geometry math: both tree classes structurally terminate every parent chain at index 0
  (items 3, 4); they contain no notion of an alternate root [READ]. The existing handoff
  leaves them untouched by terminating in the verifier instead.
- The atomic and functional paths perform no walk at all (§6), so they encode no root
  assumption to update [READ, cc:390-411].

---

## 5. One tree per verifier

**How many trees exist, who owns them** [READ]. Each `AbstractIntegrityVerifier`
constructs exactly one tree in its constructor — `new TimingTree(...)` or
`new TimingBmt(...)` sized by `rangeListSize(dramOsRanges) + rangeListSize(cxlOsRanges)`
(cc:147-164) — holds it as a raw `AbstractIntegrityTree*` (hh:84), and `delete`s it in its
destructor (cc:187-190). The tree is not a SimObject, has no name, and is invisible to
Python.

**A configuration with two verifiers** [NOT FOUND]. No config in this repo instantiates
two verifiers. `x86-integrity-host-run.py` has one (host, DramOnly);
`x86-cxl-f2-test.py` has at most one (device, CxlOnly, only with `--device-integrity`) —
its host board uses the stock non-verifier hierarchy
(x86-cxl-f2-test.py:678, 714-718, 740, 795-808). So the two-verifier case is hypothetical
today; what follows describes the substrate it would meet. If both existing verifier
sites were enabled together there would be **two tree objects**, one owned by each
verifier, protecting *different* data (host DRAM vs CXL window) with node-index spaces
that are each 0-based over their own `dataSize` and mutually unrelated [INFERRED from
cc:147-164 plus the two configs' ranges].

**Option A — two verifiers share one tree object.** Concrete obstacles [READ]:
- The tree is constructed *inside* the verifier constructor from that verifier's own
  params (cc:147-164); there is no param, setter, or constructor argument by which a tree
  could be passed in.
- Ownership is raw-pointer with `delete` in each owner's destructor (cc:187-190) — naive
  sharing double-frees.
- Because the tree is not a SimObject, a config script has no handle to name a shared
  instance (per `GEM5_PRIMER.md` §1.1, cross-object references in configs travel through
  SimObject-valued params).
- Tree queries are pure functions of `(arity, total_data)` with no mutable state
  (timing_bmt.cc throughout), so sharing would change *identity*, not behavior — the
  observable difference is only whether two verifiers can be told they mean the same
  index space.

**Option B — two independently constructed trees agree on node indices for the same
physical address.** Concrete obstacles:
- Index geometry is determined entirely by `(arity, total_data)` (timing_bmt.cc:10-102),
  so equal inputs give equal geometry — *that* part is deterministic [READ].
- But `addressToBlockIndex` consumes raw addresses (§3.4): two verifiers whose protected
  ranges have different bases compute different indices for the same physical byte, and
  for any non-zero base the indices are out of range outright [INFERRED, §3.4 arithmetic].
- `getIntegrityNodeLocation` maps a node index to a metadata *address* using the owning
  verifier's own integrity ranges (cc:708-781): identical indices in two verifiers
  designate different physical metadata bytes unless their integrity ranges are also
  identical. Agreement on indices without agreement on ranges buys nothing at the
  memory level.
- The two existing verifier sites protect disjoint data with disjoint metadata carve-outs
  (host DRAM tail vs CXL window tail), so today there is no shared physical address for
  them to agree about [READ, hierarchy py:192-205 vs device_x86_board.py:176-194].

**Option C — the tree becomes a SimObject.** What would change, and the style question:
- It would gain a Python class, params (arity, protected size or ranges), a place in the
  config hierarchy, and could then be referenced by a SimObject-valued param from one or
  more verifiers (the mechanism `system = Param.System(Parent.any, ...)` already
  demonstrates in this engine, IntegrityVerifier.py:80).
- Against the style characterized in §1: the author's rule is port-bearing/timed objects
  are SimObjects, pure geometry is plain C++ selected by *enum param* with a hand-synced
  Python mirror (cc:147-164; TimingBmt.py). A tree SimObject replaces the enum-switch
  selection mechanism with config-side subclass choice — a mechanism this engine does not
  currently use for trees — and would make the hand-maintained mirror redundant or
  contradictory. It would be *consistent* with general gem5 practice and with how the
  engine treats the metadata cache (a config-side object wired by the hierarchy), but
  *inconsistent* with how this engine has treated trees to date. Both readings are
  defensible; this document does not choose.
- Concrete mechanical obstacle either way: the constructor currently needs the tree to
  exist before `init()` (tree size validation cc:218-227, handoff mapping cc:258-271);
  a SimObject tree is constructed at instantiation like everything else, so ordering is
  satisfiable, but the verifier's destructor `delete` (cc:187-190) and the
  `#include`-level coupling to concrete tree headers (cc:47-48) are the sites that
  currently assume ownership.

---

## 6. Runtime mutability

**What the verifier/trees can change after elaboration** [READ]. Configuration state:
nothing. Ranges are set in the constructor from params (cc:63-66, 88-145); the handoff MAC
interval is computed once in `init()` (cc:229-282); the trees are immutable geometry
(timing_bmt.cc has no mutating member besides construction). There is no `startup()`
override [NOT FOUND in hh], no setter, no pybind export [NOT FOUND]. Everything that does
mutate at runtime is per-transaction bookkeeping (the queues/sets/maps of hh:154-378,
685-748) and stats. Per `GEM5_PRIMER.md` §1.4/§8.7-8: params are consumed at
`m5.instantiate()`; `init()` runs before simulation; therefore any post-elaboration state
change must arrive through an event- or packet-driven C++ code path, not through params
[CONSEQUENCE].

**Mechanisms that exist in THIS repo by which guest action reaches a memory-system
SimObject at runtime** (named, not selected):

1. **m5ops / pseudo-instructions** — `src/sim/pseudo_inst.{cc,hh}` (e.g. `m5exit` at
   pseudo_inst.cc:178, `workbegin` at :497), including the memory-mapped trigger variant
   at `System.m5ops_base` (`src/sim/System.py:152`). Guest → `exitSimLoop` → Python
   between `simulate()` calls; Python may then invoke *exported* C++ methods. Precedent
   for exported methods: `PyBindMethod("switchOut"/"takeOverFrom")` on BaseCPU
   (`src/cpu/BaseCPU.py:67-70`), `setMemoryMode` on System (`src/sim/System.py:60-61`),
   used at runtime by the stdlib switchable processor and checkpointing
   (`src/python/m5/simulate.py:415-430`). The verifier exports nothing today [NOT FOUND].
2. **MMIO device objects** — `PioDevice`/`BasicPioDevice` (`src/dev/io_device.{hh,cc}`):
   an address-range-claiming SimObject whose `read()`/`write()` run arbitrary C++ when the
   guest touches the range. Many in-tree examples under `src/dev/`.
3. **Address-keyed behavior inside a datapath object** — precedent inside this very
   engine: the verifier keys all decisions on `pkt->getAddr()` against its range lists
   (cc:338-352, 436-443); `CXLBridge` (`src/mem/cxl_bridge.hh:61`) sits on the CXL path as
   a `ClockedObject`. No object in this repo currently *mutates configuration state* on a
   trigger address [NOT FOUND].
4. **The offload mailbox is not a mechanism of this kind.** It is pure guest software over
   shared CXL DRAM (`benchmarks/cxl_mailbox.h:1-70`; producer `host_offload.c`, consumer
   `device_offload.c`) — no SimObject observes it. In the existing `OP_HANDOFF` flow the
   verifier's handoff state was set by *params at config time*, and the mailbox merely
   informs the guests of the same base/size the config already gave the verifier
   (device_x86_board.py:194-219, x86-cxl-f2-test.py:908-915).
5. **Exit-event generators in stdlib configs** — the host-run config already uses the
   boot/ROI exit-event structure with a CPU switch between `simulate()` phases
   (x86-integrity-host-run.py:150-200 region, `processor.switch()` precedent per
   `GEM5_PRIMER.md` §5.2). This is the phase in which mechanism (1)'s Python side runs.

Lifecycle summary per existing configuration path [READ + primer]: params → constructor
(at `m5.instantiate()`); range validation and handoff MAC mapping → `init()`; nothing at
`startup()`; simulation time → only mechanisms 1-3 above can reach the object, and today
none of them touch it.

---

## 7. The absent failure path

**Confirmed: no packet is ever refused, delayed indefinitely, dropped, or marked bad on
integrity grounds.** Verification cannot fail by construction: the trees store no values
(`isMocking()`, timing_bmt.hh:188), the "hash" and "XOR" are pure delays
(`HashCompletionEvent`/`XorCompletionEvent`, cc:895-900, 1012-1023), and
`completeXor` → `completeIntegrityVerification` unconditionally (cc:1028-1039). There is
no comparison anywhere [NOT FOUND].

**Every exit from the verification path** [READ]:

| Exit | Where | Meaning |
|---|---|---|
| Express-snoop bypass | cc:430-433 | never inspected |
| Unified-upstream metadata redirect | cc:436-443 | alternate wiring (unused in configs) |
| Non-verified traffic forwarded | cc:464-471 (req), cc:525-543 (resp) | out of scope of predicate |
| Protocol-level refusal, *flow control only* | `handlePacket` returns false iff `outstandingIntegrityVerification.size() > maxEncQueueSize` (cc:853-861; hh:176) | propagates to `recvTimingReq`/`recvTimingResp` as false → peer retries per the timing protocol |
| Accept-then-internally-retry | pending-eviction (dead) and same-address collision → `saveRetryVerify`, `Cycles(10)` re-attempt (cc:863-884, 834-838) | packet accepted; re-processed later |
| Secure-root instant success | cc:913-924 | trusted by fiat (node 0 / handoff MAC range) |
| Verified completion | `completeIntegrityVerification` → `schedResp` (read data), `schedReq` (write data), `schedMetadataResp` (metadata read) (cc:1043-1091) | the only terminal outcomes |
| Metadata write branch | `fatal("Unimplemented metadata writes")` (cc:1056-1058) | unreachable today (generated metadata requests are reads, cc:808) |
| Atomic / functional | cc:390-395, 403-411 | constant delay / functional forward; no walk at all |

**[CONSEQUENCE] What a failure result would have to do differently, in gem5 protocol
terms** (each from the cited fact + `GEM5_PRIMER.md` §2.3, §3.2, §8.13-18):

- It cannot "refuse" the packet: a timing refusal (returning false) is *flow control* with
  a mandatory later acceptance, and the primer notes no nack mechanism exists in modern
  gem5. Refusal-as-verdict is not expressible.
- It cannot silently not-respond: responses drain strictly in arrival order through
  `responseQueue`/`responseReady` (cc:1227-1258); withholding one response deadlocks every
  younger response behind it [READ: the while loop stops at the first non-ready head].
  A failure path that holds a packet must still eventually `schedResp`/`schedReq` it or
  restructure that ordering.
- The packet-level vocabulary that *does* exist: error command states
  (`pkt->isError()`, packet.hh:632) on a response the verifier already owns at verdict
  time (read responses are held by the verifier when verification completes, cc:527-531,
  1073-1077); or simulator-level `panic`/`fatal` (the engine's existing convention for
  can't-happen vs config error, §1); or side-band signaling through a stats/interrupt/
  device mechanism (§6's list). Write-request verdicts arrive *before* memory is updated
  (writes are verified pre-forwarding, cc:458-461), so a write failure additionally
  decides whether the write is forwarded at all — a choice with no precedent in this code.
- Ownership per primer §3.2 applies at the verdict point: for held read responses the
  verifier is the current owner of a receiver-deletes packet, so converting one into an
  error response is an in-place mutation of a packet it may legitimately keep; nothing
  today ever deletes a data packet in the verifier [READ: only metadata packets are
  deleted, cc:649].

---

## 8. Cache operations over an address range (base gem5, separate from the verifier)

- **Whole-cache writeback/invalidate, simulator-initiated.** `SimObject` virtuals
  `memWriteback()` / `memInvalidate()` (`src/sim/sim_object.hh:298,313`); `BaseCache`
  overrides them (`src/mem/cache/base.hh:853-862`) by walking **every block** via
  `tags->forEachBlk` with `writebackVisitor`/`invalidateVisitor`
  (`src/mem/cache/base.cc:1798-1806, 1823-1846`). Driven from Python by
  `m5.memWriteback(root)` / `m5.memInvalidate(root)` over all descendants
  (`src/python/m5/simulate.py:314-321`). Stated purposes in-tree: checkpointing
  (`checkpoint()` drains then writes back, simulate.py:421-430) and switching to
  cache-less memory modes (`switchCpus` path, simulate.py:415-424). **Not range-scoped.**
- **Per-line cache-maintenance packets, guest-initiated.** `MemCmd::CleanSharedReq` /
  `CleanInvalidReq` (`src/mem/packet.hh:127-129`), built from request flags
  `CLEAN`/`INVALIDATE`/`DST_POC`/`DST_POU` (`src/mem/request.hh:191-199, 1141-1183`;
  command selection packet.hh:1046-1051). On x86, `CLFLUSH`/`CLFLUSHOPT` decode to a real
  `clflushopt` microop plus fence
  (`src/arch/x86/isa/decoder/two_byte_opcodes.isa:761-763`,
  `src/arch/x86/isa/insts/general_purpose/cache_and_memory_management.py`, macroop
  `CLFLUSH_M`). These operate on one line per instruction, from guest code.
- **Eviction-related commands** that exist as vocabulary a memory object sees:
  `WritebackDirty`, `WritebackClean`, `CleanEvict`, `WriteClean` (packet.hh command list;
  the verifier already comments on `CleanEvict` passing through, cc:466-467).
- **Drain** (`m5.drain`, simulate.py:305-311) quiesces in-flight state but does not write
  back or invalidate by itself [READ].
- **Range-scoped writeback/invalidate from inside the simulator: [NOT FOUND].** Greps for
  `flushRange|writebackRange|invalidateRange|cleanRange` over `src/` return nothing. The
  granularities on offer are exactly: one line (guest CMO packet) or one whole cache
  (`memWriteback`/`memInvalidate`). Anything in between does not exist in this tree.

---

## 9. Extension points — a catalogue

Unordered. Each entry: what it is, where, what kind of change it naturally accommodates.

1. **New enum value + constructor switch case.** `IntegrityTreeType` /
   `IntegrityAllocationMode` / `MetadataCacheType` (`IntegrityVerifier.py:41-51`,
   `src/mem/SConscript:69-75`; switches at cc:147-164, 292-335, 713-774). Accommodates: a
   new tree class or a new metadata-placement policy.
2. **New tree subclass of `AbstractIntegrityTree`.** `src/mem/mtree/` + `Source()` /
   `DebugFlag()` in `src/mem/mtree/SConscript:1-13`. The abstract API is the six geometry
   functions + stats (abstract_tree.hh:51-116). Accommodates: different index math,
   different parent relations, different node typing — anything expressible as pure
   geometry.
3. **New params on `AbstractIntegrityVerifier` / `IntegrityVerifier`.** Scalar, `Cycles`,
   `Latency`, `Bool`, `Addr`, or `VectorParam.AddrRange`
   (IntegrityVerifier.py:82-134). The handoff params are the worked example of adding
   config-time state this way. Accommodates: any elaboration-time knob or region
   descriptor.
4. **New `Request`/`Packet` fields with accessor forwarders.** The metadata tag/node/type
   trio is the template: fields + per-constructor initialization + copy-constructor entry
   (request.hh:473-482, 493-495, 510-512, 521-523, 540-543) and one-line forwarders on
   `Packet` (packet.hh:636-650). Accommodates: per-transaction attributes that must
   survive the walk (the handoff comment documents why request-carried state is the only
   thing visible above the first hop, cc:229-236).
5. **The `delayReq`/`delayResp`/`delaySnoopResp` virtual hooks / a new verifier
   subclass.** hh:774-788, concrete example hh:914-931. Accommodates: alternative timing
   policies without touching mechanism.
6. **The four-port pattern + `getPort`.** cc:356-370; port classes hh:206-336. Accommodates:
   an additional port (the string-dispatch and QueuedPort idioms are uniform), e.g. a
   fifth port following `metadata_req_port`'s declaration style
   (IntegrityVerifier.py:59-71).
7. **`Event` subclasses with `AutoDelete`.** `RetryVerifyEvent` / `RetryReqEvent` /
   `HashCompletionEvent` / `XorCompletionEvent` (hh:436-579). Accommodates: any new
   deferred step in the walk, with `saveRetry*`-style scheduling helpers (cc:834-844).
8. **Tracking-container-with-helpers idiom.** The `outstandingMetadataRequests` multimap
   with add/remove/has + DPRINTF size logging (hh:726-748, cc:1577-1673). Accommodates:
   new per-node or per-request walk state.
9. **The stats group.** `IntegrityVerifierStats` with `ADD_STAT` + units + `Formula` +
   `preDumpStats` (hh:793-892, cc:1721-1994). Accommodates: new counters/classifications
   (note §2: region-classification stats are the cascade at cc:1400-1510).
10. **Hierarchy-component kwargs.** The fresh hierarchy threads config knobs
    board→component→param (hierarchy py:64-104, 174-205); `DeviceX86Board` does the same
    for the device seam (device_x86_board.py:142-219). Accommodates: new config surface
    without touching C++.
11. **A new SimObject alongside, wired in the hierarchy.** `ClassicMetadataCache` is the
    precedent: a stock-class subclass configured in Python and hung off the verifier's
    ports (metadata.py:38-69; hierarchy py:184-190). Accommodates: new datapath components
    that talk to the verifier through ports rather than through its internals.
12. **The Python geometry mirror.** `TimingBmt.py`/`TimingTree.py`, compiled in under
    `gem5.components.memory.mtree` (mtree/SConscript:15-20), currently unused by configs
    in this repo. Accommodates: pre-elaboration geometry checks (§3.5) and config-side
    sizing (upstream used `determine_max_protected_size`, TimingBmt.py:139-303).
13. **Debug flags.** Per-class flags in the owning SConscript
    (`src/mem/SConscript:162-170`, mtree/SConscript:9-13). Accommodates: observability for
    any of the above.
14. **m5 pseudo-ops.** `src/sim/pseudo_inst.{cc,hh}` and the `m5ops_base` MMIO window
    (System.py:152). Accommodates: guest-visible operations that surface as exit events or
    C++ calls (§6 item 1) — listed here as an existing attachment point, with no comment
    on use.
15. **Exported methods (`PyBindMethod`).** Not used by the engine, but an in-tree
    mechanism (BaseCPU.py:67-70) by which config-side Python could call into a SimObject
    between `simulate()` phases. Accommodates: runtime-phase invocations from exit-event
    handlers (§6 item 5). Flagged in §1 as a mechanism the engine's author has not used.

---

## CONTRADICTIONS

1. **The prompt's premise vs the repo.** "Almost nothing I described above exists in this
   codebase" is not quite true of *this* repository: a statically-configured,
   MAC-range-keyed, device-side-only re-rooting mechanism ("§6.2 range-keyed subtree
   handoff") already exists end-to-end — params (IntegrityVerifier.py:110-122), init-time
   mapping (cc:229-282), widened root predicate (cc:675-692), board/config plumbing
   (device_x86_board.py:154-219, x86-cxl-f2-test.py:553-575), and a guest protocol
   (`OP_HANDOFF`, benchmarks/cxl_mailbox.h:45-69). It is not in upstream. It is *not* the
   thing you described — no first-class region object, no tree-node subtree, no runtime
   release/acquire, no host-side counterpart — but any survey pretending the field is
   empty would be wrong, and any new mechanism must decide its relationship to this one.

2. **Raw-address vs 0-based-offset coordinate conflict.** `getParentNode` feeds raw packet
   addresses to `addressToBlockIndex` (cc:660-672; timing_bmt.cc:210-225), which is exact
   only when the protected range starts at 0 (host config). The handoff `init()` code uses
   0-based offsets into the protected region and calls that "addressToBlockIndex's
   convention" (cc:255-269). For the device verifier (protected base 0x1_0000_0000,
   device_x86_board.py:180-194) the two conventions disagree, and the raw-address walk
   arithmetic produces MAC indices beyond `dataSize` (§3.4 worked numbers), which would
   trip `assert(index < dataSize)` (timing_bmt.cc:252) on the first timing-mode verified
   CXL access [INFERRED — arithmetic, not executed]. Consistent with this, the f2 config's
   own flag help says the device-integrity/handoff paths were gated under `--atomic`
   ("build+boot+routing … not stats", x86-cxl-f2-test.py:560-575), where no walk occurs.
   Either the device timing path was never exercised, or something I did not find
   normalizes addresses; I found nothing [NOT FOUND].

3. **`TimingBmt`'s counter→tree hop contradicts its own comment and its sibling class.**
   The comment says counters attach to "the tree leaf node that is protecting it"
   (timing_bmt.cc:181-182), but the formula omits the leaf-layer offset that
   `TimingTree::addressToBlockIndex` applies (timing_tree.cc:197-234), attaching counters
   to heap indices `[0, leaves)` — the top of the heap, including the root itself. Two
   consequences derived in §3: (a) `nonLeaf` allocated tree nodes (`[leaves, treeNodes)`)
   are never reachable by any walk — allocated, address-mapped, dead; (b) proper-subtree
   coverage of contiguous regions essentially does not exist. Whether (a)/(b) are bugs or
   accepted mock-timing approximations is not decidable from the code; the timing
   *lengths* of walks remain plausible either way [INFERRED].

4. **Vestigial machinery, catalogued.** The value-carrying `IntegrityTree` — never
   instantiated (§0.4). The C++ `MetadataCache` model family — never instantiated (§0.4).
   `pendingMetadataEvictions` / `outstandingMetadataEvictions` — read/printed but never
   written (cc:703-704, 1713, 2083-2098), making `parentNodeIsPendingEviction` and its
   `saveRetryVerify` branch dead (cc:863-872). `TimingTree::processWrite*` and all
   `CYCLES_*` constants — unreachable from the verifier (only `processWriteTiming` exists
   as public API and nothing calls it [NOT FOUND]). The `IntegrityTree` debug flag is
   declared (mtree/SConscript:9) and used only in dead `tree.cc` code paths (tree.cc:270).
   `MetadataCacheType` enum — registered (SConscript:73) but consumed nowhere in C++
   [NOT FOUND]. `unified_upstream_cache` — fully implemented in C++ (cc:198-209, 436-443,
   1342-1354) but no config in this repo sets it.

5. **Two stats families disagree about what they measure.** The `*Trans*` stat buckets
   still exist and are documented as "location post-translation" (hh:836-891) but, with
   the PageSwapper excised, are now exact duplicates of the untranslated buckets by
   construction (cc:1456-1462, porter's comment says so). Readers of stats.txt will see
   two families that always agree.

6. **The metadata cache's writeback path bypasses verification.** Verified data writes are
   held for verification (cc:458-461), and the metadata-*write* branch of the walk is
   `fatal("Unimplemented metadata writes")` (cc:1056-1058) — yet dirty metadata evicted by
   `ClassicMetadataCache` arrives at `processMetadataReq` as an ordinary writeback (the
   packet is not tagged: the cache creates its own writeback requests) and is forwarded
   straight to memory with no verification and no tree update (cc:565-587). The engine
   thus verifies metadata on the way in but not on the way out. This is inherited from
   upstream (files identical) — a property of the model, not the port [READ + INFERRED].

7. **`needsVerification` includes integrity ranges, but data traffic there is
   simultaneously asserted impossible.** The predicate counts integrity-range addresses as
   needing verification (cc:347-350) while `processReq` asserts data requests are never in
   those ranges (cc:447-450) and `markReqReceived` re-asserts it (cc:1097-1098). Both are
   true only because the guest is externally prevented from touching the carve-out (the
   `mem=` kernel argument, x86-integrity-host-run.py:108-112). The predicate's integrity
   branch is effectively reachable only via the metadata path that doesn't consult it
   [INFERRED].

8. **Root trust is by index, but the root's bytes live in insecure memory.** Node 0 is
   "always trusted/on-chip" per the comment (cc:682), yet its contents are fetched from
   the in-memory integrity range like any other node when a level-1 node needs its parent
   (cc:783-832 via `getIntegrityNodeLocation(0)`), and there is no stored root value
   anywhere (§4). For a mocked tree this is timing-equivalent; as a security model it is a
   comment-vs-mechanism mismatch worth knowing before making the root plural.
