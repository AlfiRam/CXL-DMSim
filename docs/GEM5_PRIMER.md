# gem5 Primer

A durable primer for editing this gem5 fork (gem5 **v23.1.0.0** — see §9), distilled from a
full sequential read of the two scraped documentation files in this repository:

- `learning_gem5_full.md` (tutorial corpus, 10,017 lines) — cited as **[L:lines]**
- `gem5_documentation_full.md` (reference corpus, 17,329 lines) — cited as **[D:lines]**

Claims marked **(inference)** are not stated verbatim in either document; everything else has a
pointer back to the source text. Where the docs describe a convention older or newer than what
this v23.1 repo uses, that is flagged inline and collected in §9.

---

## 1. The SimObject lifecycle, end to end

### 1.1 The Python declaration

Every SimObject *type* is declared twice: once as a Python class and once as a C++ class. The
Python class declares the parameters and ports; the build system generates the glue.

```python
# src/<dir>/HelloObject.py
from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    type = 'HelloObject'                                # C++ class being wrapped
    cxx_header = "learning_gem5/part2/hello_object.hh"  # header declaring that class
    cxx_class = "gem5::HelloObject"                     # fully-qualified (gem5 namespace)

    time_to_wait = Param.Latency("Time before firing the event")          # no default => required
    number_of_fires = Param.Int(1, "Number of times to fire")             # default = 1
    goodbye_object = Param.GoodbyeObject("Another SimObject as a param")  # SimObject-valued param
```

- `type` conventionally equals the class name; `cxx_class` is needed because SimObjects live in
  `namespace gem5` [L:2794–2820].
- `Param.<TypeName>(default, "description")` — first arg is the default *unless it is a string*,
  in which case it is the description and there is no default [L:3595–3618, L:1509–1517].
- Rich param types do unit conversion at config time: `Param.Latency("2us")` becomes **ticks**,
  `Param.MemoryBandwidth('100MB/s')` becomes ticks-per-byte, plus `Cycles`, `MemorySize`,
  `Percent`, etc. [L:3619–3626, L:3910–3917].
- A SimObject-valued param may be set to the special Python `NULL`; the C++ side then receives a
  null pointer and should `panic_if(!ptr, ...)` if it can't handle that [L:3984–4006].
- **Proxy parameters**: `system = Param.System(Parent.any, "...")` searches *up* the config
  hierarchy at instantiation for the nearest object of matching type. This is the standard way an
  object finds its `System` (e.g., for `system->cacheLineSize()`) [L:4941–4952, L:4976–4990].
- Ports are declared in the same Python class:
  `inst_port = ResponsePort("desc")`, `mem_side = RequestPort("desc")`,
  `cpu_side = VectorResponsePort("desc")` [L:4285–4297, L:4916–4933].

### 1.2 The generated Params struct and the C++ class

```cpp
// hello_object.hh — include guard named after path, per convention [L:2827–2833]
#include "params/HelloObject.hh"   // generated from the Python class
#include "sim/sim_object.hh"

namespace gem5 {
class HelloObject : public SimObject
{
  public:
    HelloObject(const HelloObjectParams &p);   // constructor signature matters — see below
};
} // namespace gem5
```

- The Params type name is generated from the object name: `HelloObject` → `HelloObjectParams`
  [L:2843–2848]. Each Python param appears as a member (`params.time_to_wait`), already
  converted to simulator units; `params.name` carries the instance's config-hierarchy name
  [L:3632–3653].
- **If and only if** the constructor has the exact shape `Foo(const FooParams &)`, a
  `FooParams::create()` method is auto-generated for you. Any other signature means you must
  write `create()` yourself [L:2903–2915].
- A vector port `cpu_side` gives the Params struct an automatic
  `port_cpu_side_connection_count` member — the number of peers actually connected in the
  config — which you use to size a `std::vector` of port objects in the constructor
  [L:4984–4999].
- Most SimObjects should not inherit directly from `SimObject`; memory-system objects typically
  inherit `ClockedObject` (the tutorial's older `MemObject` base class no longer exists — §9)
  [L:2835–2838, L:5019].

### 1.3 SConscript registration

```python
Import('*')
SimObject('HelloObject.py', sim_objects=['HelloObject', 'GoodbyeObject'])
Source('hello_object.cc')
Source('goodbye_object.cc')
DebugFlag('HelloExample')
```

One `SimObject()` call per Python file, listing every SimObject class it declares; one
`Source()` per `.cc`; `DebugFlag()` declares debug flags (§6) [L:2946–2951, L:3742–3750].
Ruby protocols use `SConsopts` files instead, processed *before* SConscripts, registering
`ALL_PROTOCOLS` and `PROTOCOL_DIRS` [L:6293–6316]. Stdlib Python goes in `src/python/SConscript`
via `PySource(...)` [D:13125–13130].

### 1.4 From config script to running object

1. The config script instantiates the Python classes and assigns params/ports. Assigning as
   constructor kwargs or as attributes afterwards is *exactly equivalent*, because **no C++
   object exists until `m5.instantiate()` is called** [L:3696–3707].
2. Only SimObjects that are **children of the `Root` object** (reachable through attribute
   assignment) are instantiated in C++. An orphan Python object silently does nothing
   [L:2985–2997]. Every simulation needs exactly one `Root` [L:2974–2975].
3. `m5.instantiate()` walks the hierarchy and constructs the C++ equivalents [L:846–858].
   A required param left unset dies here with
   `fatal: hello.time_to_wait without default or user set value` [L:3679–3694].
4. Port pairs are wired **by the Python framework after all objects are constructed**, by
   calling each object's `getPort(if_name, idx)` during the initialization phase — your C++
   never initiates connection [D:8031–8032, L:4408–4411].
5. During `init()`, every memory object advertises address ranges: all objects call
   `sendRangeChange()` and range updates propagate until every crossbar knows the map
   [D:8201–8212].
6. `startup()` fires when simulation first begins (first `m5.simulate()` /`simulator.run()`).
   **This is the earliest point a SimObject may schedule its own events** [L:3429–3434].
7. `m5.simulate()` / `Simulator.run()` enters the event queue; it returns an exit event whose
   cause is queried with `exit_event.getCause()` [L:864–874].
8. Stats hooks: legacy `regStats()` (must call parent's first), plus `resetStats()` /
   `preDumpStats()` callbacks in the `statistics::Group` world (§6) [L:5464–5477, D:11840–11846].

Ordering summary: **constructor → getPort wiring → init()/range propagation → regStats →
startup() → events**. (The constructor/getPort/init ordering relative to each other is partly
**(inference)** from the docs' phrasing "during the initialization phase"; the docs are explicit
that startup() comes only when simulation begins.)

### 1.5 Ground truth: `m5out/config.ini`

Every run writes `config.ini` (and `.json`) listing *every* instantiated SimObject and *every*
parameter value, defaulted or not. The docs call checking it a best practice: options you pass on
a command line may silently not propagate (classic example: `--l1d_size` without `--caches`
creates no caches at all) [L:1869–1957, L:2360–2390].

---

## 2. Ports and the memory-system protocols

### 2.1 The port abstraction

- Ports come in pairs: a **RequestPort** connects to a **ResponsePort**; requests flow
  request→response, responses flow back. In Python you connect them with `=`, either side may be
  on the left [L:722–744]. Assigning to a *vector* port (`membus.cpu_side_ports`) spawns a new
  port and appends the connection [L:746–757, D:8027–8030].
- `send*` methods are called on your own port; each has a mirrored `recv*` that is invoked on
  the **peer**: `myPort->sendTimingReq(pkt)` becomes `peer->recvTimingReq(pkt)` — one virtual
  call, no other glue [D:8002–8010].
- The idiomatic implementation is a nested port class holding an `owner` pointer, forwarding
  every `recv*` to methods on the owning SimObject [L:4353–4400].
- A ResponsePort must override: `getAddrRanges()`, `recvAtomic`, `recvFunctional`,
  `recvTimingReq`, `recvRespRetry`. A RequestPort must override: `recvTimingResp`,
  `recvReqRetry`, `recvRangeChange` [L:4353–4402].
- Due to coherence, response ports can also *send snoop requests* and request ports receive
  them (mirrored interface) [D:8012–8016].
- The docs' reference section uses the old names MasterPort/SlavePort and a `MemObject` base
  with `getMasterPort`/`getSlavePort` — that is pre-v21 terminology; this repo uses
  RequestPort/ResponsePort and a single `getPort` (§9) [D:7980–8010 vs L:4404–4432].

### 2.2 The three access modes

All three go over the same ports [D:8118–8146], [L:4131–4151]:

| Mode | What happens | What it's for |
|---|---|---|
| **Timing** | Split transactions, queuing, contention, retries. *The only mode that produces correct simulation results.* | real experiments |
| **Atomic** | Entire access completes in one nested call chain; returns an approximate latency (`Tick`); **no events may be scheduled in the memory system** | fast-forward, cache warm-up |
| **Functional** | Instantaneous; **coexists** with either other mode | loading binaries, debugger access, host↔guest data movement |

Timing and atomic accesses **cannot coexist** in one memory system [D:8127–8134]. An object is
not required to implement atomic unless it will be used during fast-forward/warm-up (the
tutorial's SimpleMemobj just `panic("recvAtomic unimpl.")`) [L:4135–4141, L:4366].

Functional accesses must return the most up-to-date data wherever it lives, and a write must
update **every** valid copy. Critically: an object holding *queued packets* must search those
queues on a functional access and fix up any overlapping request/response
[L:4142–4151, D:8135–8146].

### 2.3 The timing protocol, precisely

- `sendTimingReq(pkt)` → peer's `recvTimingReq(pkt)` returns `bool`, and that bool is returned
  to the sender. `true` = accepted; `false` = refused, **the sender must wait for
  `recvReqRetry()` before trying again** — it may not retry on its own schedule
  [L:4205–4248, D:8183–8190].
- **The sender keeps the refused packet. The responder does not keep any pointer to it**
  [L:4246–4248]. Standard idiom: a `blockedPacket` member, `panic_if(blockedPacket != nullptr)`
  before sending, stash on failure, resend from `recvReqRetry()` [L:4606–4646].
- On retry you are not obligated to resend the same packet — a higher-priority packet may be
  sent instead; local flow control only cares that *something* is sent [D:8190–8192].
- The response direction mirrors this: `sendTimingResp` → `recvTimingResp` returns bool; a
  refused response waits for `recvRespRetry()` [L:4250–4255, L:4705–4732].
- To tell a stalled requester it may retry, the responder calls `sendRetryReq()` (→ peer's
  `recvReqRetry()`), typically guarded by a `needRetry` flag it set when it returned false
  [L:4560–4578, L:4734–4752].
- **The retry/response code path can be a single call stack.** `sendRetryReq()` may re-enter
  your `recvTimingReq` before it returns; `sendTimingResp()` may cause the peer to immediately
  send you the next request. Therefore: *update your own state to "unblocked" before calling
  `sendTimingResp`/`sendRetryReq`*, or you get infinite recursion / deadlock
  [L:4257–4262, L:4662–4668, L:5122–5127].
- Responses cannot be refused permanently by nacking; the old docs describe a `Nacked` status
  and packet nacking for global flow control [D:8190–8199] — this mechanism does not exist in
  modern gem5 (§9) **(inference from version drift; the tutorial never mentions nacks)**.

### 2.4 Address ranges and routing

- A ResponsePort answers `getAddrRanges()` with an `AddrRangeList`; interconnects use these to
  route packets. When ranges change (e.g., PCI config), the device calls `sendRangeChange()`;
  during `init()` everyone does this until ranges are fully propagated [D:8201–8212].
- A pass-through object forwards: its response port's `getAddrRanges()` returns
  `memPort.getAddrRanges()`, and its request port's `recvRangeChange()` triggers
  `sendRangeChange()` on the CPU-side ports [L:4495–4550].
- `system.system_port` is a special functional-only port the simulator itself uses to read and
  write memory (binary loading, etc.) — it must be connected in every system [L:764–780].

---

## 3. Packets and requests

### 3.1 Request vs Packet

- A **Request** represents the original CPU/device request and travels logically end-to-end.
  Its fields are written at most once and persist for the whole transaction: virtual address,
  physical address, size, creation time, requestor CPU/thread ID, PC. These fields are for
  stats/debugging, not architectural use [D:8034–8060].
- A **Packet** is one hop-to-hop transfer; a single Request may be conveyed by several packets
  [D:8062–8068]. `PacketPtr` (= `Packet *`) is the universal parameter type of all port methods
  [L:4179–4181].
- A packet's **MemCmd changes over its life**: `ReadReq` becomes `ReadResp` when
  `pkt->makeResponse()` is called; writebacks use `WritebackDirty`/`WritebackClean`
  [L:4155–4165, L:5112–5119].
- The packet's **address and size may differ from the Request's** — e.g., on a cache miss the
  packet addresses the whole block [D:8076–8086]. When upgrading a sub-block access, keep the
  *original* Request in the new packet so requestor/type stats stay correct:
  `new Packet(pkt->req, MemCmd::ReadReq, blockSize)` [L:5159–5205].
- Data handling: `dataStatic()` (packet never frees), `dataDynamic()` (freed with the packet via
  `delete`), or `allocate()` (packet allocates and frees). `getPtr()`, and `get()`/`set()` do
  guest↔host endian conversion [D:8087–8098]. Helpers `writeDataToBlock(ptr, blkSize)` /
  `setDataFromBlock(ptr, blkSize)` handle the offset math into a larger block [L:5268–5298].
- `pkt->needsResponse()`, `isRead()`, `isWrite()`, `getBlockAddr(blkSize)` are the common
  predicates [L:5183–5197].

### 3.2 Ownership and deletion — the actual rules

From the "Packet allocation protocol" [D:8147–8179]:

- **Atomic and Functional**: the Packet is **owned by the requester** for its whole life. The
  responder must overwrite the request packet in place with the response (`makeResponse()`).
  Because the response is produced before `sendAtomic`/`sendFunctional` returns, the packet may
  live on the stack.
- **Timing**: a timing transaction is **two independent one-way messages**. Each message's
  Packet is dynamically allocated by its **sender**, and **deallocation is the responsibility of
  the receiver**. The responder *may* reuse the request packet as the response (an optimization),
  but **the requester must never rely on getting the same Packet object back**.
- Cache-to-cache/broadcast subtlety: when the responder is not the target device, the target
  (e.g., memory) still deletes the request packet — a responding cache must allocate a *new*
  packet for its response, and anyone wanting to reference a broadcast packet after delivery
  must copy it, because the pointer may be deleted on delivery.
- Concrete tutorial example: the cache that created a temporary full-block packet deletes it
  itself after copying data into the original (`delete pkt; pkt = outstandingPacket;`)
  [L:5225–5243], and memory allocated with `dataDynamic()` is freed when that packet is deleted
  [L:5336–5344].

### 3.3 SenderState

`Packet::senderState` is an opaque virtual-base pointer for state private to the sending device
(e.g., an MSHR pointer). It rides with the packet and comes back with the response so the sender
can find its bookkeeping in O(1). Subclass `Packet::SenderState` per device. Devices commonly
push/pop it like a stack as the packet traverses layers (Minor's FetchRequest does exactly this)
[D:8106–8111, D:3466–3471]. There is also a `CoherenceState` pointer described in the old docs
for protocol state [D:8112–8115] (may not exist in this form in v23.1 — §9).

---

## 4. The event-driven core

### 4.1 Ticks, cycles, clock domains

- The global tick frequency is 10^12 ticks/second — **1 tick = 1 picosecond** (every run prints
  `Global frequency set at 1000000000000 ticks per second`) [L:3619–3625, L:607].
- Config-side time/size strings (`'1GHz'`, `'2us'`, `'512MB'`) convert automatically
  [L:674–683].
- Clocking is structured as `SrcClockDomain` (tunable source, holds the period, has a
  `VoltageDomain`, and — for DVFS — a `domain_id` and per-performance-level frequencies) and
  `DerivedClockDomain` (a divider off a parent domain) [L:6034–6058, L:669–672].
- A `ClockedObject` gets `clockEdge(Cycles(n))` — the tick of the *n*-th clock edge in the
  future — which is the correct way to convert a `Param.Cycles` latency to a schedule time
  [L:5039–5062]. Every ClockedObject also has an optional power model evaluated at stats dumps
  [D:1493–1503].

### 4.2 Events and scheduling

Standard idiom for "do something later":

```cpp
class Foo : public SimObject {
    EventFunctionWrapper event;
    void processEvent();
  public:
    Foo(const FooParams &p)
      : SimObject(p), event([this]{ processEvent(); }, name()) {}
    void startup() override { schedule(event, curTick() + latency); }
};
void Foo::processEvent() {
    ...
    if (more_work) schedule(event, curTick() + latency);   // re-arm from inside the handler
}
```

- `EventFunctionWrapper(std::function<void()>, name)` — pass `name()` so trace output is
  attributable; ".wrapped_function_event" is appended automatically [L:3390–3407].
- `schedule(event, tick)` schedules an absolute tick; **events cannot be scheduled in the
  past** [L:3421–3427]. First scheduling belongs in `startup()`, not the constructor
  [L:3429–3434].
- For an event that must carry payload (e.g., a `PacketPtr`), subclass `Event`, implement
  `process()`, and pass `AutoDelete` to the Event constructor so the object frees itself after
  processing: `schedule(new AccessEvent(this, pkt), clockEdge(latency))` [L:5059–5090].
- `exitSimLoop(message, exit_code, when)` ends the simulation from C++; `message` becomes
  `exit_event.getCause()` in Python [L:3919–3923].
- Descheduling: the docs read here never show an explicit `deschedule()` call; Minor's model
  instead *stops its recurring tick* via the `Ticked` start/stop interface when idle
  [D:3543–3562]. **(inference: `deschedule()` exists in the API but is not covered by these
  documents.)**
- Debug helpers from gdb: `eventqDump()`, `schedBreak(tick)` [D:4759–4775].
- The whole simulation is one event queue; component "wakeup" functions (Ruby network, Minor
  pipeline) are just events scheduled on it [D:10594–10706].

---

## 5. Config scripts and the standard library

### 5.1 Hand-built ("classic") config scripts

The canonical skeleton [L:640–908]:

```python
import m5
from m5.objects import *

system = System()
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'                      # must match CPU type
system.mem_ranges = [AddrRange('512MB')]

system.cpu = X86TimingSimpleCPU()               # naming: {Isa}{Type}CPU
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports   # or via caches
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()          # the next 3 lines are x86-ONLY
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports       # functional-only, always needed

system.mem_ctrl = MemCtrl(dram=DDR3_1600_8x8())
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

binary = 'tests/test-progs/hello/bin/x86/linux/hello'
system.workload = SEWorkload.init_compatible(binary)     # gem5 >= v21
process = Process(cmd=[binary])
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
```

- The x86 interrupt-controller wiring and its 3 port lines are an x86-specific requirement;
  ARM/RISC-V etc. do not need them [L:769–780, L:2543–2553].
- Caches are ordinary `Cache` subclasses in Python; connect CPU→L1s→L2XBar→L2→SystemXBar.
  A cache can't accept two ports directly, hence the intermediate `L2XBar` [L:1674–1694].
- Since config classes are plain Python, helper methods (`connectCPU`, `connectBus`) and
  argparse-driven parameters are the normal way to structure them [L:1586–1626, L:1722–1745].
- The old shipped `se.py`/`fs.py` scripts are deprecated in favor of stdlib examples in
  `configs/example/gem5_library` [L:2112–2145, D:4609–4610].

### 5.2 The gem5 standard library (`src/python/gem5/`)

Model: a **board** (backbone; owns devices/workload; negotiates connections) into which you plug
a **processor** (a set of cores wrapping `BaseCPU`s), a **memory system**, and a
**cache hierarchy** (everything between processor and memory) [L:966–975, D:12283–12295].

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

board = SimpleBoard(clk_freq="3GHz",
                    processor=SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86),
                    memory=SingleChannelDDR3_1600("1GiB"),
                    cache_hierarchy=NoCache())
board.set_se_binary_workload(obtain_resource("x86-hello64-static"))
Simulator(board=board).run()
```
[D:12389–12519]

- Boards: `SimpleBoard` (SE only, classic caches only), `X86Board`/`RiscvBoard` (SE+FS),
  `ArmBoard` (FS only), prebuilt demo boards under `prebuilt/` [L:1160–1175, D:12456–12458].
- Cache hierarchies: `classic/` (crossbars, fixed MOESI), `ruby/` (detailed coherence),
  `chi/` (Arm CHI in Ruby) [L:1176–1192].
- Processors: `SimpleProcessor` (identical cores; don't use it if you need to configure O3 or
  Minor internals), `SimpleSwitchableProcessor` (`starting_core_type`/`switch_core_type`, call
  `processor.switch()` at runtime), traffic `generators`, and `BaseCPUProcessor`+`BaseCPUCore`
  for wrapping a hand-parameterized `BaseCPU` subclass [L:1216–1258, D:12688–12705,
  L:1356–1408, D:13219–13241].
- `requires(isa_required=..., coherence_protocol_required=..., kvm_required=...)` gives readable
  errors on incompatible binaries [D:12641–12655].
- Workloads: `obtain_resource("id")` downloads/caches gem5-resources artifacts;
  `board.set_workload(obtain_resource(...))` for FS workload bundles;
  `set_se_binary_workload(binary)` / `set_kernel_disk_workload(...)` (which takes
  `readfile_contents` — a script run in the guest after boot) [L:560–572, D:12726–12742].
- **The Simulator object and exit events**: `Simulator(board, on_exit_event={ExitEvent.EXIT:
  generator})`. The handler is a Python *generator*: each `yield False` continues simulation at
  that exit event, `yield True` ends it. Typical FS flow: first exit = kernel booted, second =
  start of ROI (switch CPUs here), third = done [L:1283–1320, D:12746–12780].
  Exit event types: `EXIT, CHECKPOINT, FAIL, SWITCHCPU, WORKBEGIN, WORKEND, USER_INTERRUPT,
  MAX_TICK` [L:1311–1320]. Without a handler, simulation ends at the first exit event
  [D:12776–12778].
- Simulator API: `run()`, `set_max_ticks()`, `schedule_max_insts()` (fires when *any* core hits
  the count), `get_stats()`, `checkpoint_path=` for restore [L:1333–1348].
- Extending the stdlib = subclass the abstract bases (`AbstractBoard`, `AbstractProcessor`,
  `AbstractMemorySystem`, `AbstractCacheHierarchy`; for caches prefer
  `AbstractClassicCacheHierarchy`/`AbstractRubyCacheHierarchy`). A cache hierarchy implements
  `get_cpu_side_port`, `get_mem_side_port`, and `incorporate_cache(board)`, which uses board
  APIs (`connect_system_port`, `get_memory().get_memory_controllers()`,
  `get_processor().get_cores()`, `cpu.connect_icache/dcache/walker_ports/interrupt`,
  `has_coherent_io`) [D:12898–13088]. Extension by subclassing is the intended style, not
  parameterizing everything [L:1350–1355].
- The exit-event mechanism is built on **m5ops** (guest-side pseudo-instructions): `m5 exit`,
  `m5 workbegin/workend`, `m5 checkpoint`, `m5 dumpstats/resetstats`, `m5 readfile` (how the
  host passes a script into the guest), etc. [D:1194–1246, D:7511–7524 in-guest usage].

### 5.3 Ruby configuration (when hand-building)

Instantiating a SLICC-generated controller means setting every param declared in the `.sm`
machine header, wiring each MessageBuffer to the network (To-buffers → into network,
From-buffers ← from network), giving each controller of a type a unique ascending `version`
starting at 0, creating one `Sequencer` per hardware thread, and building routers/links for the
network yourself. The `RubySystem` setup cannot happen in `__init__` (circular parent refs cause
infinite recursion at instantiate) — use a separate `setup()` [L:8735–9024].

---

## 6. Debugging and observability

### 6.1 Debug flags and DPRINTF

- Never use `std::cout`/printf in gem5 code; use debug flags [L:2879–2884, L:3235–3241].
- Declare the flag in a SConscript: `DebugFlag('HelloExample')`. This generates
  `debug/HelloExample.hh`; include it plus `base/trace.hh`, then
  `DPRINTF(HelloExample, "fmt %d\n", val);` [L:3243–3279, D:5060–5064].
- Enable at runtime: `--debug-flags=Flag1,Flag2` (before the config script on the command
  line), `-Flag` disables one, `--debug-start/--debug-end` bound the ticks, `--debug-file=FILE`
  redirects (path is **relative to m5out**, and a `.gz` suffix compresses)
  [L:3070–3076, D:5038–5055, L:3318–3323, D:5089–5097].
- Output format per line: `tick: object-name: message` — the name is `name()`, i.e. the Python
  config path [L:3308–3316].
- `--debug-help` lists all flags; compound flags (e.g. `Exec`) group base flags; `Exec` prints
  disassembled instruction traces and is the workhorse for CPU-side debugging
  [L:3193–3233, D:5073–5082].
- DPRINTFs exist only in `gem5.opt` and `gem5.debug`; **`gem5.fast` compiles them out and
  removes asserts** [L:3337–3340, D:2928–2932, D:17282–17286].
- `tracediff`/`rundiff` compare two runs' traces; `--debug-flags=Exec,-ExecTicks` makes traces
  diffable across timing changes [D:5099–5156].
- Error/status functions [D:5991–6009]: `panic()` = gem5 bug (aborts, core dump); `fatal()` =
  user/config error (exit(1)); plus `warn()/warn_once()`, `inform()`, `hack()`, and the
  condition forms `panic_if`/`fatal_if` (seen throughout tutorial code).

### 6.2 Stats

Two styles coexist at v23.1:

- **Legacy (flat)**: declare `statistics::Scalar/Vector/Histogram/Formula...` members, override
  `regStats()`, and chain `.name(name() + ".hits").desc("...")`; histograms need `.init(nbuckets)`
  *before use*; vector stats must be `init(size)`d before use. **You must call the parent's
  `regStats()` first** or you get "uninitialized stats" errors [L:5436–5498, D:11668–11745].
  Legacy stats now print a deprecation warning at runtime [L:614].
- **Current (`statistics::Group`)**: put stats in a `struct MyStats : public statistics::Group`,
  initialize them in its constructor with `ADD_STAT(name, "desc")`, construct it with the owning
  SimObject as parent (`stats(this)`). Groups nest with the SimObject hierarchy; `regStats()`
  remains only for stats needing late information [D:11775–11846, D:12198–12231].
- Update sites: `hits++`, `histogram.sample(value)`, `Formula ratio = hits / (hits+misses);`
  (formulas are evaluated at dump time) [L:5501–5533, D:11739–11745].
- Stats land in `m5out/stats.txt`; a file can contain multiple dumps, each bracketed by
  `---------- Begin Simulation Statistics ----------` [L:1959–2006]. `m5.stats.periodicStatDump
  (m5.ticks.fromSeconds(f))` controls dump frequency [L:5823–5867]; guest-side `m5
  dumpstats/resetstats` do it on workload boundaries [D:1226–1228]. C++: `Stats::dump()`,
  `Stats::reset()` [D:11766–11772].

### 6.3 Debugger-based debugging

Use `gem5.debug` under gdb. `--debug-break=TICK` sends SIGTRAP at a tick; from gdb:
`call schedBreak(tick)`, `call setDebugFlag("Flag")`, `eventqDump()`, `takeCheckpoint(tick)`,
`SimObject::find("system.cpu")` [D:4713–4775]. Python config scripts debug with pdb (`--pdb`
or inline `import pdb; pdb.set_trace()`); note Python under `src/` is baked into the binary
(rebuild, or set `M5_OVERRIDE_PY_SOURCE=true`) [D:4785–4800]. The simulated OS/program is
debugged separately via gem5's **remote GDB stub** (one TCP port per CPU, from 7000)
[D:4887–4959]. Classic-cache coherence state for an address can be dumped with
`printAddr()`/PrintReq functional packets from gdb [D:8342–8380].

### 6.4 Checkpointing

- Create: guest `m5 checkpoint`, the checkpoint pseudo-instruction in the workload, or
  `--take-checkpoints`/`--checkpoint-at-end` in the legacy scripts; stdlib exposes
  `ExitEvent.CHECKPOINT` and `checkpoint_path`. Checkpoints are directories `cpt.TICKNUMBER`
  [D:380–392].
- Restore: `-r N`/`--checkpoint-restore=N`. **gem5 restores with atomic CPUs by default**; use
  `--restore-with-cpu=<type>` if the checkpoint should resume on something else [D:394–406].
- Ruby: checkpointing requires flushing caches to memory; the docs state only MOESI_hammer
  supported that flush [D:392].
- CPU switching (the usual reason for checkpoints/fast-forward): build both CPUs, mark the
  not-yet-running one `switched_out=True`, keep it inside the object hierarchy, then
  `m5.switchCpus([(old, new), ...])` between `m5.simulate()` calls; stdlib wraps this as
  `SimpleSwitchableProcessor.switch()` [D:431–451, D:12688–12705].
- KVM notes: `KVMCPU` needs host/guest ISA match, KVM group permissions, and `perf` (or
  `usePerf=False`); guest m5ops **must use the memory-mapped "_addr" variants** under KVM
  because magic instructions are illegal on real hardware [D:1096–1185, D:1342–1380,
  D:16693–16698].

---

## 7. Simulation modes — what each one actually does and does not do

### 7.1 CPU models

- **AtomicSimpleCPU** — functional, in-order, uses *atomic* memory accesses; latency is only the
  estimate the atomic chain returns; no memory-system events, no contention. Good for warm-up
  and fast-forward; not a timing model at all [D:4470–4473].
- **TimingSimpleCPU** — same simple core but uses *timing* accesses: it stalls on every memory
  access and waits for the response. "Single cycle" for non-memory work — every instruction
  otherwise takes one fetch-execute step, so it is fine for memory-centric studies, weak for CPU
  microarchitecture claims [D:4475–4478, L:1242–1246].
- **MinorCPU** — in-order, fixed 4-stage pipeline (Fetch1/Fetch2/Decode/Execute) with
  configurable widths, FU pipelines, scoreboard issue, store buffer LSQ. Visualized with
  MinorTrace/minorview [D:3292–3980].
- **O3CPU** — out-of-order, Alpha-21264-like; ROB, rename, IQ, LSQ; *execute-in-execute* (the
  instruction really executes at the execute stage, so out-of-order load interactions are
  modeled) [D:4261–4300]. **Requires separate I and D caches** — it won't run cacheless configs
  [L:915–919]. Writes to architectural state from outside (ThreadContext) force a full pipeline
  flush [D:4298–4300].
- **KvmCPU** — hardware virtualization; near-native speed, **no architectural stats collected by
  gem5** (some via perf); for fast-forward only [D:1096–1104].
- **TraceCPU** — replays dependency-annotated "elastic traces" recorded from O3; memory-system
  exploration without the O3 cost [D:4488–4520].

CPU naming: `{Isa}{Type}CPU` (`RiscvMinorCPU`, `X86O3CPU`, ...) [L:920–937]. The system's
`mem_mode` ('timing'/'atomic') must match the CPU type; the legacy `se.py` **defaults to the
atomic CPU** — "no real timing data" unless you pass `--cpu-type` (and `--caches`)
[L:2320–2340].

### 7.2 What atomic/timing/functional silently do not do

- Atomic mode: no queuing delay, no resource contention, no events; whole access is one call
  chain [D:8129–8134]. An object may legitimately implement `recvAtomic` as "do the functional
  access, return a fixed latency" — timing-only objects often do exactly this or panic
  [L:4135–4141, L:4366].
- Timing mode with **classic caches** still cheats in one documented place: **express snoops**
  propagate up the hierarchy *instantaneously and atomically* even in timing mode, to sidestep
  race conditions of incremental snooping. Snoop timing up the hierarchy is therefore
  approximate by design [D:8283–8293].
- Classic caches implement a simplified, inflexible MOESI; if coherence itself matters to your
  study, the docs tell you to use Ruby [L:1479–1497, D:8240–8247].
- Functional accesses through Ruby with in-flight messages are described as "very brittle" and
  may fail [L:7073–7078].
- SE mode is not "FS but faster": syscalls are emulated (some just ignored with warnings), there
  is no OS, no page-walk realism, no privileged binaries, and OS-triggered effects are simply
  absent [L:1261–1276, D:16533–16536].

---

## 8. Traps — things the docs explicitly warn about (reread this section)

**Build/registration**

1. A new debug flag **must** be declared with `DebugFlag()` in a SConscript before `DPRINTF`
   can use it; the generated header `debug/<Flag>.hh` must be included [L:3243–3266].
2. `FooParams::create()` is auto-generated **only** for the exact signature
   `Foo(const FooParams &)`; deviate and you must hand-write it [L:2903–2915].
3. Never modify generated files (e.g., SLICC-generated `*_Controller.py`) [L:6506].
4. Don't name a new SimObject `SimpleObject` — one already exists and the collision produces
   confusing compiler errors [L:2741–2743].
5. Style is enforced (pre-commit hook installed by SCons): 4 spaces, sorted includes (own header
   first), CamelCase classes / camelCase members / snake_case locals, 79-column lines
   [L:2702–2717, D:5617–5807].

**Python config**

6. A Python subclass of a SimObject that defines `__init__` **must call
   `super().__init__()`**, or attribute lookup breaks with
   `RuntimeError: maximum recursion depth exceeded` at instantiation [L:1763–1778].
7. Only SimObjects reachable as children of `Root` are instantiated; an unattached object is
   silently ignored [L:2992–2997].
8. Params without defaults must be set before `m5.instantiate()` (else `fatal`) [L:3679–3694].
9. Always sanity-check `m5out/config.ini`; command-line options can fail to propagate (the
   `--l1d_size` without `--caches` trap) [L:1952–1957, L:2360–2390].
10. Ruby system construction cannot happen in `__init__` of the RubySystem subclass (circular
    parent pointer → infinite recursion in `m5.instantiate`); use a post-construction `setup()`
    [L:8885–8893].
11. Each SLICC controller type must be numbered with `version` 0,1,2,... uniquely and
    ascending [L:8742–8758].
12. x86 systems need the interrupt controller + its 3 port connections and `system_port`
    connected; other ISAs must *not* connect the x86 interrupt ports [L:769–780, L:2543–2553].

**Ports / timing protocol**

13. On a failed `sendTimingReq`, **the sender keeps the packet**; the responder stores nothing
    and will not remind you which packet failed [L:4246–4248].
14. After returning false, do not resend until `recvReqRetry()`; after receiving a retry you may
    send a *different* packet [L:4243–4245, D:8190–8192].
15. **Before sending a retry, you must be ready *at that instant* to accept a packet** — the
    retry path can be one call stack, and sloppy state updates create infinite recursion
    [L:4257–4262].
16. Mark yourself unblocked **before** calling `sendTimingResp` — the peer may immediately send
    the next request in the same call chain [L:4662–4668, L:5122–5127].
17. `pkt->makeResponse()` must be called to turn a request packet into a response before sending
    it back [L:5112–5119].
18. Timing packet ownership: sender allocates, receiver deletes; never rely on the response
    being the same Packet object; copy broadcast packets you keep past delivery [D:8154–8179].
19. On a functional access, an object with queued packets must search and fix up all
    overlapping queued requests/responses [D:8140–8146].
20. Address-range changes must be announced with `sendRangeChange()`; pass-through objects must
    forward both `getAddrRanges` and range-change notifications [D:8201–8212, L:4532–4550].
21. Requests smaller than a block that miss must be upgraded to a full-block packet (keeping the
    original Request); accesses spanning two lines are not handleable by a simple cache — panic
    [L:5146–5205].

**Events / stats**

22. Never schedule an event in the past; do initial scheduling in `startup()`, not the
    constructor [L:3421–3434].
23. Heap-allocated one-shot events should use `AutoDelete` or you leak them [L:5071–5090].
24. Legacy `regStats()` overrides must call the parent's `regStats()` first ("If you don't do
    this you get errors about uninitialized stats.") [L:5473–5477]; vector/histogram stats must
    be `init(...)`ed before first use [D:11668–11669].
25. `gem5.fast` removes asserts and DPRINTF — debug with `.opt`/`.debug`; a crash that is silent
    under `.fast` may be an informative assert under `.opt` [D:17282–17286].

**SLICC / Ruby**

26. **No `if` statements inside SLICC actions** — an event must have a single code path;
    conditional behavior belongs in `in_port` logic as different events/states. Transitions are
    atomic and resource-checked before execution; conditionals break resource accounting and
    cause "strange performance, deadlocks, and other bugs" [L:7169–7181].
27. **Never leave a transition body empty to "stall"** — SLICC treats it as success and re-polls
    the same port forever: deadlock. Use `z_stall`, `recycle`, or `stall_and_wait`
    [D:11516–11527].
28. `stall_and_wait` requires explicit wake-ups (`wakeUpBuffers(addr)` on transitions to base
    states, `wakeUpAllBuffers()` after replacements) or messages sleep forever [D:11555–11612].
29. `in_port` order (priority) matters: a protocol/resource stall blocks **all** lower ports.
    A documented deadlock was fixed by reordering directory ports to memory, response, request
    [L:6884–6899, L:9554–9563].
30. The mandatory queue's name must be exactly `mandatoryQueue` [L:6496–6499]; virtual network
    numbers must match across all controllers of a protocol [L:7986–7989].
31. Forgetting `setMRU()` near sequencer callbacks silently breaks replacement policies (gem5
    even warns at runtime) [L:7588–7591, L:1113].
32. A message-struct field cannot be named `Addr` (collides with the type) [L:7037–7041].
33. SLICC has no `else if`, no `!` operator, return values cannot be ignored, and error line
    numbers can point far below the real error (unbalanced braces report the last line)
    [D:11614–11628, L:8631–8638].
34. Use `error()`/`assert()`/`DPRINTF(RubySlicc, ...)`/`APPEND_TRANSITION_COMMENT` liberally;
    debug protocols with the Ruby random tester (start 1 CPU/100 loads, scale up) and
    `--debug-flags=ProtocolTrace` before trying real workloads [L:9219–9273].

**Modes / other**

35. Restoring a checkpoint defaults to atomic CPUs — pass `--restore-with-cpu` if that's wrong
    for you [D:404–406].
36. Under KVM, guest m5ops must be the `_addr` (magic-address) variants — magic instructions
    SIGILL on the host; compile guest tools with `-DM5_ADDR=0xFFFF0000` (or ISA equivalent)
    [D:1376–1380, D:16693–16698].
37. Power models require timing CPUs [L:5623–5624]; DVFS needs `domain_id` set on each
    `SrcClockDomain` (fatal otherwise) and `dvfs_handler.domains`+`enable` [L:6131–6200].
38. `--debug-file` output goes under the outdir (m5out), not the cwd [L:3318–3323].
39. Switched-out CPUs must be constructed with `switched_out=True` and still be attached to the
    object hierarchy [D:431–443].
40. Don't treat SE mode as "FS but faster" — missing syscalls/OS interactions can silently
    invalidate results; when in doubt use FS [L:1268–1276].

---

## 9. Version drift — this repo vs. the documents

**This repository is gem5 v23.1.0.0** (`src/base/version.cc`: `gem5Version = "23.1.0.0"`;
`RELEASE-NOTES.md` top section "Version 23.1"). The two documents mix material from ~v19 wiki
pages through v24.1 tutorials. Concrete discrepancies to watch:

1. **Build configuration**: v23.1 uses the **Kconfig** flow. `scons PROTOCOL=MSI ...` on the
   command line **no longer works here**; use `scons defconfig <dir> build_opts/X` +
   `scons setconfig <dir> RUBY_PROTOCOL_X=y` (the docs describe both, keyed by "gem5 <= 23.0"
   vs ">= 23.1") [D:867–1088, L:8595–8674; RELEASE-NOTES 23.1].
2. **ALL build ≠ all Ruby protocols here.** "As of gem5 v24.1 the ALL build also includes all
   Ruby coherence protocols" [L:230–233, L:1191–1192] — that is *v24.1*; in this v23.1 repo the
   ALL build has one protocol per build and you select it via Kconfig. Similarly,
   X86DemoBoard SE-mode support is listed as v24.1 [L:556].
3. **Old port terminology in the reference doc**: `MemObject` with
   `getMasterPort`/`getSlavePort`, MasterPort/SlavePort, `master`/`slave` port names
   [D:7980–8016] are pre-v21. v23.1 uses `RequestPort`/`ResponsePort`, a single
   `getPort(if_name, idx)`, and `cpu_side_ports`/`mem_side_ports`; old names survive only as
   `DeprecatedParam` warnings [D:329–363]. The `MemObject` base class is gone — tutorial code
   inheriting `MemObject` (SimpleCache, [L:4919–4921, L:4976]) must inherit
   `ClockedObject`/`SimObject` here (the tutorial itself already falls back to
   `ClockedObject::getPort` in one place [L:5019]).
4. **Params by pointer vs const-reference**: parts of the tutorial use the pre-v21 style
   `Foo(FooParams *p)`, `params->name`, and a hand-written `FooParams::create()`
   [L:4449–4456, L:4754–4760]; other parts use the current `const FooParams &`
   [L:2894–2915]. In this repo use the const-reference form and let `create()` be generated.
5. **Nacked packets**: the reference memory-system page describes NACK-based global flow
   control and a `Nacked` packet status [D:8099–8100, D:8193–8199]. This mechanism does not
   exist in modern gem5's classic protocol **(inference)** — do not design against it. Likewise
   the `CoherenceState` packet pointer [D:8112–8115] reflects the old cache model.
6. **Stats**: chained `.name().desc()` in `regStats()` is the legacy style and warns at runtime
   in v23.1 [L:614]; new code should use `statistics::Group`/`ADD_STAT` [D:11775–12240]. Note
   also the namespace: older text writes `Stats::`, current code `gem5::statistics`
   **(inference from the v23.1 namespace reorganization; the docs use `Stats::` throughout)**.
7. **Event wrappers**: the tutorial mixes the old templated
   `EventWrapper<Obj, &Obj::method>` / `event(*this)` [L:3663–3664, L:3802] with the current
   `EventFunctionWrapper` [L:3376–3407]. Use `EventFunctionWrapper` here.
8. **Ruby source layout**: older text says `src/mem/protocol` and
   `src/mem/protocol/RubySlicc_*.sm` [L:6515, L:7068]; in this repo protocols live under
   `src/mem/ruby/protocol` (the CHI section already uses the new path
   [D:9119–9120]). MessageBuffer wiring shown as `.master = network.slave`
   [L:8819–8830] uses the deprecated names; the current params are the renamed
   in/out port equivalents **(inference; the docs only show the old names)**.
9. **Garnet naming**: `--network=garnet2.0` [D:10448] vs `--network=garnet` [D:10760] —
   Garnet is now "garnet" (3.0/HeteroGarnet is the current model) [D:10827].
10. **Legacy config scripts**: `se.py`/`fs.py`, `Options.py`, master/slave port lists in
    config.ini [L:1932–1933], and pyoptparse-based examples reflect pre-stdlib gem5; fs.py is
    explicitly marked deprecated [D:4609–4610]. Prefer stdlib components (§5.2), which this
    v23.1 repo fully supports (Suite/local-JSON resource features described as v23.1 features
    apply here [D:13462, D:13651]).
11. **Capstone disassembler hooks** (`cpu.tracer.disassembler = ...`) exist "from gem5 v23.1" —
    available in this repo [D:5236–5262].
12. Misc old content to ignore: Alpha architecture support [D:1526], `DerivO3CPU` naming
    [D:382], the SPARC/Alpha-era m5term transcript [D:7586], and gem5art tutorials pinned to
    v20.x binaries.

---

## Where the two documents disagree

- Port/packet terminology and flow control: tutorial (request/response ports, no nacks,
  sender-stores-failed-packet) vs reference (master/slave, nacking) — the tutorial matches this
  repo; the reference's memory-system page is older (see §9 items 3, 5).
- Params passing convention: the two documents (and the tutorial internally) disagree between
  pointer and const-ref (§9 item 4); const-ref is correct here.
- Atomic mode's status: the tutorial says implementing atomic is optional for objects not used
  in fast-forward [L:4135–4141]; the reference simply lists it as one of three universal access
  types [D:8129–8134]. Not a real contradiction — the reference describes the interface, the
  tutorial the obligation.
- Build-protocol selection: both PROTOCOL= and Kconfig flows appear; keyed by version (§9
  items 1–2).
