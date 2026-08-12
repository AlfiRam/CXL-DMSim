# Two-Verifier Substrate

What exists in this repository that a two-verifier configuration would meet, and what
breaks. Companion to `INTEGRITY_ENGINE_EXTENSION_SURVEY.md` (cited as **[survey §n]**) and
`GEM5_PRIMER.md` (**[primer §n]**). This document does not design a configuration, a
handoff, or a region mechanism; it names substrate facts and leaves choices open.

Tags: **[READ]** at the cited line; **[INFERRED]** with stated basis; **[NOT FOUND]**
looked for, absent; **[CONSEQUENCE]** derived requirement. All sizes computed with gem5's
binary units: `"3GB"` = 3·2³⁰ = 3,221,225,472 B (`toMemorySize` →
`toBinaryInteger`, `src/python/m5/util/convert.py:260-261`; `"G"` maps to gibi,
convert.py:58,92) [READ].

---

## 1. Can the f2 host board take a verifier at all?

**What the host board is** [READ]. `x86-cxl-f2-test.py` builds the host as a stock
`X86Board` (f2:714-722) with the stock, non-verifier
`PrivateL1PrivateL2SharedL3CacheHierarchy` (f2:678-688), `host_memory =
DIMM_DDR5_4400(size="3GB")` (f2:695), `cxl_memory` of 8 GB (f2:696-699), `enable_nmp=False`
(f2:721). No verifier exists on the host side [survey §5, re-confirmed].

**The only host-verifier recipe in the repo** is
`PrivateL1PrivateL2SharedL3IntegrityVerifierCacheHierarchy` (hierarchy py:40-49), used
solely by `x86-integrity-host-run.py`. Swapping it into the f2 host board would meet the
following assumptions, each named with whether f2's host board satisfies it:

1. **Same base topology and ports.** The verifier hierarchy subclasses the exact hierarchy
   the f2 host already uses (py:40-42) and reproduces it up to the L3→membus hop
   (py:108-172), splicing `L3.mem_side → verifier → membus` (py:174-182). Its
   `get_mem_side_port`/`get_cpu_side_port` are inherited membus ports
   (`private_l1_private_l2_shared_l3_cache_hierarchy.py:116-121`). **Satisfied** — the
   board-side taps still find what they expect: `X86Board` attaches its `CXLBridge` to
   `get_mem_side_port()` (x86_board.py:197-200) and its `apicbridge` to
   `get_cpu_side_port()` (x86_board.py:241-244). [CONSEQUENCE of the splice point: CPU
   traffic to the CXL window (routed membus→CXLBridge, bridge range appended at
   x86_board.py:209-212 since `enable_nmp=False`) would traverse the verifier, because the
   bridge taps the membus *below* the splice; interrupt traffic via apicbridge enters the
   membus cpu-side and does not.]
2. **Primary memory is a single contiguous `[0, size)` range.** The hierarchy's carve reads
   only `board.get_memory().get_size()` and builds `AddrRange(full_size)` /
   `AddrRange(os_size)` based at 0 (py:196-205); `X86Board._setup_memory_ranges` provides
   exactly that (`data_range = AddrRange(memory.get_size())`, x86_board.py:393-403).
   **Satisfied.**
3. **Memory size ≤ 3 GB and > reserve.** X86Board caps at 3 GB (x86_board.py:388-392); f2's
   host memory is exactly "3GB" (f2:695); the hierarchy asserts `os_size > 0`
   (py:200-203). **Satisfied for any reserve < 3 GB.** With the default `"1GiB"` reserve
   (py:71): os = 3·2³⁰ − 2³⁰ = 2³¹ = 2 GiB.
4. **The board connects nothing the hierarchy also connects.** The hierarchy itself wires
   `membus.mem_side_ports` to `board.get_memory().get_mem_ports()` (py:111-112) — the
   *primary* memory only; the CXL DRAM's ports are wired by the board to `cxl_mem_bus`
   (x86_board.py:227-228), not to the hierarchy. **Satisfied.**
5. **Coherent-IO cache hook.** `board.has_coherent_io()` → `self._setup_io_cache(board)`
   (py:146-147; helper on the base class, base py:192). X86Board has coherent IO.
   **Satisfied.**
6. **X86 interrupt wiring via the membus** (py:165-168). **Satisfied.**
7. **Guest kernel argument.** The verifier's carve is only safe if the guest never touches
   the reserve: host-run appends `mem=<os>M` (host-run:181) and documents both the reason
   (a stray OS access into the integrity range trips
   `assert(!rangeListContains(integrityRanges, addr))`, host-run:106-112; the assert at
   `integrity_verifier.cc:447-450`) and the side effect: "the workload is capped to host
   DRAM via `mem=<os>M`, so Linux never enrolls/touches the CXL E820 region at
   0x100000000" (host-run:162-164) [READ]. **Not currently satisfied by f2**: the f2 host
   boots with default kernel args plus, only under `--offload`, `memmap=` carves for the
   mailbox and handoff region (f2:994-1019). A host verifier on f2 needs *some* guest-side
   enforcement of the DRAM reserve, and the existing tool for that (`mem=`) is documented
   to also unmap the entire CXL window from the host guest — see CONTRADICTIONS #1.
8. **What the hierarchy cannot be asked for.** Its constructor accepts only
   `integrity_tree_type/arity/allocation_mode/reserve_size` and metadata-cache size/assoc
   (py:59-74); it assigns **only** `verifier.dram_full_ranges` / `dram_os_ranges`
   (py:204-205). There is no kwarg or code path by which it gives the verifier CXL ranges
   [READ; see §2]. Passing `integrity_allocation_mode="CxlOnly"` through it would reach
   `init()` with empty `cxlIntegrityRanges` and die in `hasValidRanges`
   (`integrity_verifier.cc:292-297,212-216`) [CONSEQUENCE].

Requirement summary: the f2 host board can structurally accept the verifier hierarchy
(items 1-6 hold); the open items are guest-side carve enforcement (item 7) and the fact
that the hierarchy as written can only ever protect host DRAM (item 8).

---

## 2. What ranges would a host verifier get, and would they include CXL?

**Does the derivation know about CXL? No.** The hierarchy's whole range computation is
py:196-205: `full_size = board.get_memory().get_size()` — the *primary* memory only —
then `dram_full_ranges = [AddrRange(full_size)]`, `dram_os_ranges = [AddrRange(os_size)]`.
`board.get_cxl_memory()` is never consulted; the strings "cxl" do not appear in the file
[NOT FOUND]. The obstacle lines are exactly **py:197** (size source) and **py:204-205**
(only `dram_*` assigned).

**Could the verifier's four range vectors express "DRAM plus a CXL window"? Yes, at the
parameter level.** The params exist (`dram_full/os`, `cxl_full/os`,
`IntegrityVerifier.py:88-96`); the constructor carves DRAM and CXL integrity tails
independently (`integrity_verifier.cc:88-112` and 114-137); the tree is sized over the
*sum* of both OS lists (cc:151, 158); under `DramOnly` all metadata is placed in the DRAM
integrity tail regardless of which memory the protected data is in (cc:713-727), and both
`hasValidRanges` (cc:292-294) and `treeSizeValid` (cc:312-320) check only the DRAM side —
so "protect DRAM+CXL, metadata in DRAM" is a *validly elaborating* parameterization.
(`BasicMix` is not: it panics in `treeSizeValid` and `getIntegrityNodeLocation`,
cc:330-334, 743-747.) The device board already demonstrates CXL ranges being fed to a
verifier (device_x86_board.py:427-428).

**But the index arithmetic cannot address the CXL data — worked.** The tree's documented
contract is a linear map from addresses to leaves ("It is assumed that there is a linear
mapping between memory addresses to leaf nodes, starting at the left-most leaf node",
`abstract_tree.hh:63-67`), implemented as raw division with no base subtraction
(`addressToBlockIndex`: `firstOfType(MAC) + address/(64·arity)`, timing_bmt.cc:210-225),
fed the raw packet address (`integrity_verifier.cc:670`) [survey §3.4]. Take the natural
host parameterization on f2: `dram_os = [0, 2 GiB)`, `cxl_os = [0x1_0000_0000,
0x1_8000_0000)` (2 GiB), arity 4, `TimingBmt`. Then total_data = 4 GiB and:

| quantity | value | source |
|---|---|---|
| macCount | 2²⁶ = 67,108,864 | 4 GiB / 64 (timing_bmt.cc:23) |
| macNodes | 2²⁴ = 16,777,216 | /4 (cc:26) |
| counterNodes | 2²⁰ = 1,048,576 | 4 GiB/4096 (cc:58) |
| leaves | 262,144 | /4 (cc:66) |
| height | 10 | ceil(log₄ 262,144)=9, +1 (cc:67) |
| nonLeaf | 4⁹/3 = 87,381 | cc:72 |
| treeNodes | 349,525 | cc:75 |
| macBase = treeNodes+counterNodes | 1,398,101 | timing_bmt.cc:146 |
| dataSize | 18,175,317 | cc:81 |

MAC index for the first CXL byte, address 0x1_0000_0000:
`1,398,101 + 4,294,967,296/256 = 1,398,101 + 16,777,216 = 18,175,317` — **equal to
`dataSize`, one past the last valid node**, so `assert(index < dataSize)` in
`getNodeType` (timing_bmt.cc:252) fails on the first verified CXL access in timing mode
[INFERRED — arithmetic, not executed]. The reason is structural, not a sizing accident:
the linear map spends MAC index space on the *address span*, and the hole
[2 GiB, 4 GiB) between host DRAM and the CXL base consumes exactly the 8,388,608 indices
that the CXL data would need, while the tree is sized by protected *size* (cc:149-160),
not span. **So: the range vectors can express it; the tree's address→index convention
cannot. The obstacle is `timing_bmt.cc:216-218` (raw `address/(hashInputSize·arity)` with
no base handling) together with `integrity_verifier.cc:670` (raw `pkt->getAddr()`), under
the contract at `abstract_tree.hh:63-67`.** Stated plainly: expressing "DRAM plus CXL as
protected" is a configuration exercise; making the walk arithmetic correct for it is not.

**The host's actual view of the CXL window in f2 today** [READ]:
- Physical range: `[0x1_0000_0000, 0x3_0000_0000)` — 8 GiB (f2:729-732; base constant at
  x86_board.py:184-188).
- Routing: CPU → hierarchy membus → `CXLBridge` (range appended when `enable_nmp=False`,
  x86_board.py:209-212) → io bus → `cxlmemory` PCI device → `cxl_mem_bus` (`CXLMemBar`) →
  `cxl_dram` (x86_board.py:191-228). The device System's `device_iobridge` joins
  `cxl_mem_bus` as another master (f2:729-732, device_x86_board.py:407-457).
- Guest visibility: the window is advertised to the host guest as **E820 type-1 (normal
  RAM)** unconditionally (x86_board.py:348-352), and the f2 comments state the host kernel
  enrolls it as NUMA-node-1 RAM (f2:318-322). It is *not* in `System.mem_ranges`
  (x86_board.py:400-403) but its controllers are in `self.memories` (x86_board.py:215-218).
  Under `--offload`, `memmap=` carves Reserve the mailbox 16 MiB and (with
  `--device-handoff`) the handed-off region out of that RAM (f2:994-1019). So yes — the
  host guest has the CXL memory mapped, as ordinary allocatable RAM except for the
  explicit `memmap=` carves.

---

## 3. The carve-out collision, with numbers

Inputs [READ]: window `[0x1_0000_0000, 0x3_0000_0000)` (8 GiB, f2:729-732). Device board
derivation (device_x86_board.py:176-194): `full = [0x1_0000_0000, 0x2_FF00_0000)` (window
minus top 16 MiB mailbox), `os = [0x1_0000_0000, 0x1_8000_0000)` (bottom 2 GiB). Carve
loop (integrity_verifier.cc:114-137, partial-range branch cc:131-135):
`cxlIntegrityRanges = [os.end, full.end) = [0x1_8000_0000, 0x2_FF00_0000)`, size
6,425,673,728 B (6 GiB − 16 MiB). Structure for 2 GiB protected, arity 4, TimingBmt:
9,131,349 nodes × 64 B = **584,406,336 B = 0x22D5_5540** [survey §3.3].

**Where the device's metadata lands** [READ arithmetic from
`getIntegrityNodeLocation`: `range.start() + node·64`, cc:713-727, timing_bmt.cc:157-161]:
nodes 0…9,131,348 occupy

```
[0x1_8000_0000, 0x1_A2D5_5540)        (ends ≈ 5.44 GiB below the mailbox)
```

**A hypothetical host verifier also protecting the window** — three parameterizations the
existing code admits, with where its metadata lands:

- **(i) Same `cxl_full`/`cxl_os` lists, `CxlOnly`.** Identical carve → identical integrity
  range → identical node→address map → host metadata **coincides byte-for-byte** with the
  device's `[0x1_8000_0000, 0x1_A2D5_5540)`. Two verifiers would read (and, if metadata
  writebacks occur, write — via the unverified metadata-writeback path, survey
  CONTRADICTIONS #6) the same physical metadata lines, each through its own private
  `ClassicMetadataCache` with no coherence between them: the metadata caches sit on
  private verifier ports, not on any snooped bus (hierarchy py:184-190,
  device_x86_board.py:444-451) [READ wiring; coherence absence INFERRED from the private
  port topology].
- **(ii) Host `DramOnly` with CXL protected.** Metadata goes to the host DRAM tail:
  integrity = `[3 GB − reserve, 3 GB)` = e.g. `[0x8000_0000, 0xC000_0000)` for a 1 GiB
  reserve (host full = `[0, 0xC000_0000)`). **Disjoint** from the device's metadata.
  (This is the parameterization §2 showed elaborates but cannot be walked.)
- **(iii) Host given the window without the mailbox exclusion.** Nothing host-side knows
  the mailbox exists: the constant lives only in `benchmarks/cxl_mailbox.h:41-43` and the
  *device* board's derivation (device_x86_board.py:180-186); `x86_board.py` and the
  verifier hierarchy contain no counterpart [NOT FOUND]. The natural host derivation
  `full = [0x1_0000_0000, 0x3_0000_0000)` yields integrity =
  `[0x1_8000_0000, 0x3_0000_0000)`, which **contains the mailbox**
  `[0x2_FF00_0000, 0x3_0000_0000)`. Two distinct consequences:
  1. *Placement*: metadata still occupies only the first 584,406,336 B of the integrity
     range — top of metadata 0x1_A2D5_5540, margin to the mailbox
     12,868,124,672 − 7,026,857,280 = **5,841,267,392 B ≈ 5.44 GiB**. For metadata to
     reach the mailbox the structure would need to exceed 6,425,673,728 B, i.e. protected
     size ≳ 6,425,673,728 / 0.27214 ≈ 23.6 GB ≈ 22 GiB — impossible inside an 8 GiB
     window. **Metadata never lands on the mailbox at these sizes.**
  2. *Classification*: every mailbox address becomes a member of `integrityRanges`.
     Host mailbox traffic traverses the host verifier (§1 item 1) as ordinary
     non-metadata requests and trips
     `assert(!pkt->isMetadataRequest() && !rangeListContains(integrityRanges, ...))` in
     `processReq` (integrity_verifier.cc:447-450) — an abort in `gem5.opt` on the first
     host mailbox access [INFERRED from routing + predicate; not executed]. The device
     board avoids exactly this by excluding the mailbox from `full`, which keeps it out of
     both `os` and `integrity` membership so it "passes through inert"
     (device_x86_board.py:178-182, 421-423).

**Answer to the collision question:** coincide (case i), disjoint (case ii), or
classification-collision-without-placement-collision (case iii) — it is entirely a
function of which range lists the second verifier is handed; the carve code itself
contains no cross-verifier awareness of any kind [NOT FOUND: no verifier ever reads
another verifier's ranges].

---

## 4. Geometry agreement between two verifiers, with numbers

**total_data of each** [READ]:
- Device verifier (as f2 configures it with `--device-integrity`): only CXL ranges are
  passed (device_x86_board.py:423-432), so total = `rangeListSize(cxlOsRanges)` =
  **2 GiB** (cc:151,158; os range device_x86_board.py:188-193).
- Host verifier (the only recipe that exists, host-run hierarchy on f2's 3 GB board):
  total = 3·2³⁰ − reserve. With the default `"1GiB"` reserve: **2 GiB — numerically
  identical to the device's.** With any other reserve, different (e.g. reserve
  `"512MiB"` → total 2.5 GiB).

**MAC index each computes for the same physical CXL address** (take
a = 0x1_0000_0000, the window base; `index = macBase + a/256`, timing_bmt.cc:210-225,
fed raw per cc:670):

| verifier | total_data | macBase (=treeNodes+counterNodes) | index for 0x1_0000_0000 | in range? (dataSize) |
|---|---|---|---|---|
| device | 2 GiB | 742,741 | 742,741 + 16,777,216 = **17,519,957** | no (9,131,349) |
| host, reserve 1 GiB | 2 GiB | 742,741 | **17,519,957** | no (9,131,349) |
| host, reserve 512 MiB | 2.5 GiB | 906,581 | **17,683,797** | no (10,485,760+655,360+251,221 = 11,392,341… see below) |

(2.5 GiB derivation: macNodes 10,485,760; counterNodes 655,360; leaves 163,840; height
ceil(log₄ 163,840)=9 → 10; nonLeaf 87,381; treeNodes 251,221; macBase 906,581; dataSize
11,392,341.)

**The finding, stated exactly:** because `addressToBlockIndex` ignores the range lists
entirely, two verifiers of the *same tree class and arity with equal total_data* compute
**identical** indices for any raw physical address — the equal-reserve row agrees at
17,519,957. This refines survey §5 Option B, which called the index spaces "mutually
unrelated": they are unrelated *in meaning* but pointwise identical whenever
`(class, arity, total_data)` match, precisely because of the missing base handling. Both
agreeing values are, however, out of range for both verifiers (17,519,957 ≥ 9,131,349),
so agreement today is agreement between two numbers neither tree can accept
(`assert(index < dataSize)`, timing_bmt.cc:252) [INFERRED, arithmetic].

**Exact configuration under which the two numbers agree:** same tree type
(`TimingTree` computes a different base: `firstLeafIndex = 4^(h−1)/3`,
timing_tree.cc:197-234), same arity, same total_data — nothing else enters the function.
Range bases, allocation modes, and memory types are irrelevant to the *index*.

**Everything that would have to be true for two verifiers to compute the same — and
meaningful — index for the same physical byte** [CONSEQUENCE, each from the cited fact]:
1. Same tree class and arity and total_data (index formula inputs, timing_bmt.cc:10-102,
   210-225).
2. A shared answer to the base-subtraction question: today neither subtracts anything
   (cc:670; timing_bmt.cc:216-218), which yields agreement but invalid indices for any
   region not based at 0 (§2). If normalization were ever introduced, both verifiers
   would additionally need the same base convention for the shared range — the repo's
   only existing precedent for offset normalization is the handoff `init()` code
   (cc:255-269), which is config-time, single-range (`.front()`, cc:238-244), and not on
   the walk path.
3. For the index to designate the same *metadata byte*, additionally the same allocation
   mode and identical integrity range lists, because `getIntegrityNodeLocation` maps
   node→address through the owning verifier's own ranges (cc:708-781). Same index +
   different integrity ranges = different physical metadata (case ii of §3).
4. For the walk sequence (not just the leaf) to agree, the same protected-size rounding:
   `leaves`, `height`, and segment bases all derive from total_data via `ceilDiv`/
   `integerLog` (timing_bmt.cc:23-75), so any size disagreement shifts every parent
   index.

---

## 5. Construction phases in the two-System configuration

All ordering below is [READ] from the f2 config and `src/python/m5/simulate.py`, mapped
onto primer §1.4's phase order (constructors → port wiring → init → regStats → startup →
events).

1. **Python object phase.** `TwoSystemSimulator._instantiate` (f2:182-273) calls
   `self._board._pre_instantiate()` then `self._device_board._pre_instantiate()`
   (f2:192-193). `_pre_instantiate` → `_connect_things` (abstract_board.py:399-404,
   355-388), which runs `incorporate_memory`, then `incorporate_cache` — **this is where
   each verifier's *Python* object is created** (hierarchy py:176-190 for a host
   verifier; the device's is created earlier, in the board constructor's
   `_setup_io_devices` path, device_x86_board.py:415-451). Host board first, device board
   second (f2:192-193). The stock single-board Simulator does the same at
   simulator.py:511.
2. **Root attachment.** `Root(board=host_board, systems=[device_board])` (f2:236-243);
   `Root.systems` is a `VectorParam.System` added to `src/sim/Root.py:84` by this fork.
   Both Systems live under one Root.
3. **C++ construction.** `m5.instantiate(...)` (f2:265-268) runs `createCCObject()` for
   *every* descendant of Root (simulate.py:133-135). **Both verifiers' C++ constructors —
   and therefore both tree constructions and both carve loops (cc:53-185) — complete in
   this pass, before any `init()` runs.** Relative order between the two subtrees follows
   the `root.descendants()` walk over attachment order (board, then systems)
   [INFERRED from kwarg order; not load-bearing given the phase separation].
4. **Port wiring, then init.** `connectPorts()` for all (simulate.py:136-137), then
   `init()` for all (simulate.py:139-141). **Both verifiers' `init()` — range validation
   and any handoff MAC mapping (cc:192-283) — run here, after both constructors, before
   any simulation.** Then `regStats` (simulate.py:143-145).
5. **The boot barrier is much later, in config Python between simulate slices.** The f2
   "barrier" is host-Python polling both Systems' serial-output files between `m5`
   simulation slices — `_serial_contains` loops at f2:329-345 (default flow) and
   f2:413-437 (`--kvm-boot` flow, which switches both processors when the barrier is
   met). [CONSEQUENCE] Every value either verifier computes at construction or `init()`
   is therefore fixed strictly before either guest begins booting, and the barrier phase
   is ordinary between-`simulate()` Python — the phase in which, per primer §1.4, params
   are already frozen.
6. **Event queues.** By default every SimObject in both Systems is on event queue 0; the
   f2 code renumbers **only KVM cores** onto disjoint queues 1..N, with the comment
   "queue 0 stays reserved for every non-CPU SimObject" (f2:214-232) [READ].
   `root.sim_quantum` is set only when KVM cores are present (f2:245-263). So in the
   TIMING and ATOMIC modes the two Systems — including any verifiers, both membuses, the
   shared `cxl_mem_bus`, and both metadata caches — share the single queue-0 event queue;
   under `--kvm-boot`/`--dual-kvm`, only the cores are elsewhere, and every memory-system
   object still shares queue 0 [READ f2:214-232; INFERRED for verifiers specifically,
   from "every non-CPU SimObject"].

---

## 6. The 16 KiB covering-node region, located concretely

Inputs [READ]: device verifier protected size 2 GiB (device_x86_board.py:188-193), arity 4
(device_x86_board.py:149), `TimingBmt` (device_x86_board.py:148), window base
0x1_0000_0000 (x86_board.py:184-188). Geometry [survey §3.3]: counterNodes = 524,288,
**leaves = 131,072**, treeNodes = 218,453.

Condition [survey §3.2]: attachment node `j = offset/16 KiB` must have no counter-bearing
heap children, i.e. `4j+1 ≥ leaves`.

- `4j+1 ≥ 131,072` → j ≥ 32,767.75 → **lowest j = 32,768**. (Check: j = 32,767 has child
  131,069 < 131,072, which carries counters 524,276-524,279 — non-adjacent → not exact.)
- **Lowest qualifying protected offset** = 32,768 × 16,384 = 536,870,912 =
  **0x2000_0000 (512 MiB)**.
- **Absolute physical address in the CXL window** = 0x1_0000_0000 + 0x2000_0000 =
  **0x1_2000_0000**; the region is **[0x1_2000_0000, 0x1_2000_4000)**.
- **Covering tree node index = 32,768** (the tree segment starts at absolute index 0,
  timing_bmt.cc:137-139). It covers exactly counters 131,072-131,075 (relative), i.e.
  protected offsets [0x2000_0000, 0x2000_4000), and nothing else: its own counter block
  is 4j..4j+3 = 131,072..131,075 < counterNodes = 524,288 ✓, and its heap children
  131,073..131,076 are all ≥ leaves so carry no counters ✓.
- Qualifying blocks continue every 16 KiB up to j = 131,071 (offset 2 GiB − 16 KiB); the
  handed-off region's current location — offset 0 (device_x86_board.py:216-218) — is
  covered only by the root [survey §3.3].

Two scope notes. (a) These offsets are protected-offset space, the convention the handoff
`init()` code uses (cc:255-269); under the walk's raw-address convention the device
verifier never actually computes these counter indices for CXL addresses (§2, survey
§3.4). (b) The numbers are properties of the *current* counter→tree hop
(timing_bmt.cc:180-186); the deferred geometry decision would change them, and this
section makes no argument about that decision.

---

## 7. What the existing M2 static-handoff path touches

Everything the current mechanism owns, so it can be accounted for (made inert vs left
running) by whatever replaces it. Inventory only [all READ]:

**Verifier params** — `handoff_range_start`, `handoff_range_size`
(`IntegrityVerifier.py:110-122`); size 0 is the "inactive" sentinel.

**Verifier C++ state** — `handoffRangeStart/Size`, `handoffActive`,
`handoffMacStart/End` (`integrity_verifier.hh:132-144`), initialized in the constructor
(cc:80-86).

**`init()` code** (cc:229-282), comprising: the single-range `osBase`/`osSize`
derivation via `.front()` (cc:238-244); the within-OS-region `fatal` (cc:247-253); the
MAC-granularity (64·arity) alignment `fatal` (cc:255-267); the offset→MAC-index mapping
(cc:269-271); the empty-range `fatal` (cc:272-274); the `inform` banner (cc:276-282).
Any second verifier reuses this same `init()` body, so an active handoff param on either
verifier runs this code against *that verifier's* ranges.

**The walk predicate** — the second clause of `parentNodeIsSecureRoot`
(cc:686-691), consulted at cc:698 (`parentNodeIsPendingEviction`), cc:913
(`handlePacket`), and cc:1641 (`hasOutstandingMetadataRequest`). This is the single
C++ decision point any new re-rooting mechanism would also occupy.

**Board plumbing** — `DeviceX86Board` kwargs `cxl_handoff`, `cxl_handoff_size`
(device_x86_board.py:158-160); the region computation pinned to the *start* of `cxl_os`
with its own alignment/containment asserts (device_x86_board.py:199-219, including the
`cxl_handoff requires cxl_integrity` assert at :203); param pass-through to the verifier
(device_x86_board.py:429-431); the stored `_cxl_handoff_start/_cxl_handoff_size` attrs
that the config later re-reads.

**Config plumbing** — `--device-handoff` flag and its `--device-integrity` interlock
(f2:563-575, 598-611); threading of `device_board._cxl_handoff_start/_size` into the
host guest's `memmap=` carve (f2:1005-1019) and into both guests' command lines /
printed summary (f2:908-915 region, f2:1011-1012, f2:1185-1191).

**Guest-side contract** — `OP_HANDOFF` opcode and `HANDOFF_OPS_OFF` region layout
(`benchmarks/cxl_mailbox.h:45-69`), producer arming (`benchmarks/host_offload.c:275-285`)
and consumer execution (`benchmarks/device_offload.c:259-285`).

**Collision surface** [CONSEQUENCE, from the inventory]: the region descriptor currently
exists in three independently-written copies — verifier params, board attrs, and the
guest-visible `memmap=`/descriptor values — with the board as the only coordinator; the
walk-termination authority currently has exactly one C++ home (the predicate); and the
`init()` mapping monopolizes the "address-range → MAC-interval" translation including its
single-range `.front()` assumption. A second verifier or region mechanism touching any of
these either shares them or must make them demonstrably inert; both handoff params
defaulting to 0 is the only existing "inert" state (cc:84).

---

## CONTRADICTIONS

1. **The only carve-enforcement tool and the only CXL-visibility requirement are mutually
   exclusive as written.** A host verifier requires the guest kept out of the DRAM
   reserve, and the one existing mechanism is `mem=<os>M` — which host-run explicitly
   documents as *also* preventing Linux from enrolling or touching the CXL E820 region at
   all (host-run:106-112, 162-164). The f2 host, conversely, requires the CXL window
   mapped (type-1 RAM, x86_board.py:348-352; NUMA node 1, f2:318-322) for every workload
   it runs. No existing kernel-argument recipe in this repo provides "DRAM capped *and*
   CXL visible" simultaneously; f2's `memmap=` carves show a finer-grained tool in use
   for CXL subranges (f2:994-1019), but nothing applies it to the DRAM reserve
   [NOT FOUND].
2. **Survey §5's "mutually unrelated" index spaces, refined.** Because
   `addressToBlockIndex` never consults ranges, two verifiers of identical
   (class, arity, total_data) produce pointwise-identical indices for every raw address
   (§4: both 17,519,957 for the window base at equal 2 GiB totals). The survey's claim
   holds for *meaning* (each index is only defined relative to its own tree and metadata
   ranges) but not for the numbers themselves. Ironically, the same missing base
   subtraction that makes CXL indices invalid (§2) is what makes them agree.
3. **A knob that can only hold its default.** The verifier hierarchy exposes
   `integrity_allocation_mode` (py:70) yet assigns only DRAM ranges (py:204-205), so any
   value except `"DramOnly"` fatals at `init()` (`hasValidRanges`, cc:292-304). Same
   family as survey CONTRADICTIONS #4's dormant machinery, but this one is a live,
   documented kwarg (py:79).
4. **The two boards advertise the same window to their guests with opposite semantics.**
   Host: whole CXL window as E820 type-1 RAM, unconditionally, no carve parameter
   (x86_board.py:348-352). Device: whole window Reserved (per the mailbox contract's
   description and the device board's design, cxl_mailbox.h:19-21,
   device_x86_board.py:136-139 comment). Any host-side protected/metadata split of the
   window therefore has no E820 expression on the host — enforcement would be entirely
   kernel-args (`memmap=`), the same tool already carrying the mailbox and handoff
   carves, while the device side gets it for free.
5. **The mailbox constant has no single owner.** `MB_BASE`/16 MiB exists in
   `benchmarks/cxl_mailbox.h:41-43`, in the device board's `full_end` derivation
   (device_x86_board.py:183-186 — a hardcoded `"16MiB"`), and in f2's host `memmap=`
   string (f2:1005) — three literals that must agree, with a comment-level contract only
   ("Must match MB_BASE/MB_SIZE", f2:1002-1003). A host verifier deriving CXL ranges
   would become a fourth copy site [CONSEQUENCE].
6. **The f2 config's own gating admits the device verifier's timing path is unexercised.**
   `--device-integrity` help: "Under --atomic the gate is build+boot+routing (config.ini),
   not stats" (f2:560-562) — consistent with §2/§4's arithmetic that the timing walk
   would assert on raw CXL addresses (survey CONTRADICTIONS #2). The substrate this
   session describes for a *second* verifier therefore includes a first verifier whose
   own walk has, per the config's text, not been driven in timing mode.
7. **`_setup_memory_ranges`'s 3 GB exception vs the f2 host memory.** The host board is
   configured at exactly the cap ("3GB", f2:695; cap check `> toMemorySize("3GB")`,
   x86_board.py:388) — legal, but it means a host verifier's carve has no headroom to
   grow the reserve by growing memory; any larger reserve shrinks the OS range instead.
   Not a code contradiction; a boxed-in configuration fact worth having on the table.
