# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

"""
Two-System x86 Linux configuration: host X86Board + DeviceX86Board
sharing CXL DRAM through host_board.cxl_mem_bus. Both Systems run
TIMING-only and terminate via a serial-output barrier.

What this configuration proves:
  - Host X86Board (with its CXLBridge, CXLMemory, CXLNMPDevice) and
    DeviceX86Board (with its device_iobridge) coexist under one Root.
  - device_board.device_iobridge attaches to host_board.cxl_mem_bus as
    the THIRD master (alongside CXLMemory.mem_req_port and
    CXLNMPDevice.mem_port — both UNCHANGED).
  - Per-System readfile machinery works (each gets its own readfile
    via the kernel_disk_workload `readfile=` kwarg).
  - The existing regression tests still pass against the same gem5
    binary.

Topology:

  Root.systems
    └── device_board : DeviceX86Board
           membus → device_iobridge → ┐
                                      ▼
  Root.board                    host_board.cxl_mem_bus (CXLMemBar)
    └── host_board : X86Board   ↑     ↑
           processor → membus → CXLBridge → CXLMemory.mem_req_port
                                            CXLNMPDevice.mem_port
                                            (existing wiring, untouched)

Earlier attempts and the lessons we kept:

  Attempt A — dual KVM on both Systems:
     gem5 hung at "Starting simulation..." with both serial consoles
     silent. Concluded at the time: multiple KvmVMs in one gem5 process
     is unsupported.
     RESOLVED — that conclusion was wrong. The hang was an eventq_index
     collision: each processor's incorporate_processor numbers its KVM
     cores' event queues from 1 independently (base_cpu_processor.py:
     75-79), so the host core and device core 0 shared queue 1 — one
     thread, two vCPUs, and KVM's per-thread signal/timer setup
     (cpu/kvm/base.cc:254-261) starved one of them inside KVM_RUN.
     With globally disjoint queues (TwoSystemSimulator._instantiate)
     both Systems boot Linux under KVM concurrently (--dual-kvm, proven
     2026-07). Multi-KvmVM per process works: KvmVM is per-System with
     its own /dev/kvm+VM fds (vm.cc:316-324). --kvm-boot builds on
     this: KVM boot -> switch BOTH to ATOMIC at the boot barrier ->
     workload under ATOMIC.

  Attempt B — KVM on host, TIMING on device from tick 0:
     Host's Linux reached MP-BIOS init then panicked at the
     8254/IO-APIC timer check. A byte-level diff of every host
     interrupt SimObject against a known-working single-System
     baseline confirmed no structural leak — the bug is purely
     runtime. gem5 KVM's guest TSC drifts from simulated time when a
     concurrent TIMING System on another System consumes large amounts
     of real time per simulated quantum. Linux's check_timer sees a
     TSC-vs-PIT ratio anomaly and gives up.
     Lesson: KVM is incompatible with a concurrent active TIMING CPU
     on another System.

  Attempt C — both TIMING + count-based exit handler
     (`yield False; yield True` expecting 2 m5_exit events):
     Host booted, printed PASS, called `m5 exit;` — handler yielded
     False. But the host's userspace then terminated, Linux's last
     thread context suspended, and gem5 fired a SECOND ExitEvent.EXIT
     with cause "exiting with last active thread context"
     (src/python/gem5/simulate/exit_event.py:82-83). Handler yielded
     True on that event. Simulation ended while the device was still
     in systemd-init.
     Lesson: Linux's natural process-exit emits exit events that the
     Simulator categorises identically to explicit `m5 exit;`. Exit
     counting is fragile.

This config:
  - HOST   = SimpleProcessor(TIMING). No KVM.
  - DEVICE = SimpleProcessor(TIMING). No KVM.
  - Termination = SERIAL-OUTPUT BARRIER. The exit handler reads both
    Systems' Pc.com_1.device files after every ExitEvent.EXIT and
    only yields True when BOTH PASS strings have appeared. Every
    other exit event (Linux shutdown, last-thread suspension,
    repeated m5_exits from looping rc.local hooks, etc.) is just an
    "opportunity to recheck the barrier."
  - This is safe because the Terminal SimObject sets
    `outfile->stream()->setf(std::ios::unitbuf)` at construction
    (src/dev/serial/terminal.cc:131), so the file reflects guest
    serial output character-by-character with no buffering.
  - Wall-clock: ~25-30 min cold boot for each System, in parallel.

Checkpoint/restore modes (added for fast iteration):

  --take-checkpoint DIR : normal cold boot of both Systems; the guests
     then PARK ALIVE in a minimal liveness loop (heartbeat + m5 exit +
     sleep — deliberately dumb: no readfile re-read, no cmp/cp, so this
     run validates the checkpoint MECHANISM only). When the serial
     barrier is met, m5.checkpoint(DIR) is taken at a quiescent point
     (NMP untouched, no DMA in flight) and the run exits. The exact
     argv is recorded in DIR/TAKE_CMDLINE.txt for precise replay.
  --restore DIR : rebuild the IDENTICAL config (same core counts,
     memory sizes, --is_asic) and restore from DIR instead of
     cold-booting. Success = both heartbeats appear in the FRESH
     outdir's serial files (the boot-time PASS strings live in the
     take-run's outdir and never reappear post-restore).

  HISTORY — the first take/restore attempt failed exactly where the
  original caveat predicted: CXLMemory::recvFunctional was an empty
  stub, so memWriteback() at checkpoint time silently dropped every
  dirty CXL-backed (NUMA node 1) cache line, and the restored host
  panicked on zeroed node-1 page tables. Fixed in cxl_memory.{hh,cc}
  (queue-sweeping functional forward, mirroring CXLBridge). The fix is
  now validated by this config: the device writes an ASCII sentinel
  into CXL DRAM during the take-run's parked state and every heartbeat
  re-reads it; the restore barrier requires the sentinel to read back
  correctly (device path), and host survival validates the host
  functional-write path (its node-1 page tables must round-trip).

  CONSEQUENCE of the dumb park loop: this checkpoint cannot have new
  work injected at restore (the parked script reads nothing beyond the
  sentinel address). The readfile-injection park loop comes in a LATER
  take-run — one more cold dual-boot — once this mechanism is proven.
"""

import argparse
import os
import sys
from pathlib import Path

import m5
import m5.ticks
from m5.objects import (
    AddrRange,
    Root,
)
from m5.util.convert import toMemorySize

from gem5.components.boards.device_x86_board import DeviceX86Board
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.cachehierarchies.classic.private_l1_private_l2_shared_l3_cache_hierarchy import (
    PrivateL1PrivateL2SharedL3CacheHierarchy,
)
from gem5.components.cachehierarchies.classic.private_l1_private_l2_shared_l3_integrity_verifier_cache_hierarchy import (
    PrivateL1PrivateL2SharedL3IntegrityVerifierCacheHierarchy,
)
from gem5.components.memory.single_channel import (
    DIMM_DDR5_4400,
    SingleChannelDDR3_1600,
    SingleChannelDDR4_3200,
)
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.components.processors.switchable_processor import SwitchableProcessor
from gem5.isas import ISA
from gem5.resources.resource import (
    DiskImageResource,
    KernelResource,
)
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires


# =============================================================================
# TwoSystemSimulator — same pattern as the earlier single-system stub
# variant, extended to also call
# _pre/_post_instantiate on the second System (which now actually has
# CPU/cache plumbing that needs the lifecycle hooks).
# =============================================================================
class TwoSystemSimulator(Simulator):
    def __init__(self, *args, device_board, **kwargs):
        self._device_board = device_board
        super().__init__(*args, **kwargs)

    def _instantiate(self) -> None:
        if self._instantiated:
            return

        # Both boards run _connect_things.
        self._board._pre_instantiate()
        self._device_board._pre_instantiate()

        # DUAL-KVM FIX (proven by the --dual-kvm experiment): each
        # processor's incorporate_processor numbers its KVM cores' event
        # queues from 1 INDEPENDENTLY (base_cpu_processor.py:75-79; the
        # same per-processor numbering exists in switchable_processor.py:
        # 96-106, so SimpleSwitchableProcessor under --kvm-boot collides
        # identically), so with two boards the host core and device core 0
        # both land on queue 1 — one thread hosting two vCPUs from two
        # VMs. KVM's counter/timer signal delivery is set up per-thread
        # ("to ensure that signals are delivered to the right threads",
        # cpu/kvm/base.cc:254-261), so a shared queue can leave a vCPU
        # stuck in KVM_RUN with no timer kick — Attempt A's silent hang.
        # Renumber ALL KVM cores across BOTH boards into one global 1..N
        # range (queue 0 stays reserved for every non-CPU SimObject, which
        # incorporate_processor already assigned; a SwitchableProcessor's
        # get_cores() returns its CURRENT cores — the KVM start cores —
        # and its switched-out ATOMIC cores stay on queue 0). This must
        # happen after _pre_instantiate (which assigns the colliding
        # indices) and before m5.instantiate (which sizes the event-queue
        # array).
        kvm_cores = [
            c
            for proc in (self._board.processor, self._device_board.processor)
            for c in proc.get_cores()
            if c.is_kvm_core()
        ]
        for i, core in enumerate(kvm_cores):
            core.get_simobject().eventq_index = i + 1
        if kvm_cores:
            queues = [c.get_simobject().eventq_index for c in kvm_cores]
            assert len(set(queues)) == len(queues), (
                "KVM event-queue renumbering failed to produce disjoint "
                f"queues: {queues}"
            )
            print(
                f"[kvm-eventq] {len(kvm_cores)} KVM cores on disjoint event "
                f"queues {queues} (queue 0 = all other SimObjects)"
            )

        # Both Systems attached to Root: host via the canonical `board=`
        # kwarg, device via the new VectorParam.System added to Root.py
        # by the earlier single-system stub variant.
        root = Root(
            full_system=self._full_system
            if self._full_system is not None
            else self._board.is_fullsystem(),
            board=self._board,
            systems=[self._device_board],
        )
        self._root = root

        # Both processors use KVM, so sim_quantum is required for KVM
        # scheduling regardless of which we check. Set it unconditionally.
        host_proc = self._board.processor
        dev_proc = self._device_board.processor
        any_kvm = (
            any(c.is_kvm_core() for c in host_proc.get_cores())
            or any(c.is_kvm_core() for c in dev_proc.get_cores())
            or (
                isinstance(host_proc, SwitchableProcessor)
                and any(c.is_kvm_core() for c in host_proc._all_cores())
            )
            or (
                isinstance(dev_proc, SwitchableProcessor)
                and any(c.is_kvm_core() for c in dev_proc._all_cores())
            )
        )
        if any_kvm:
            m5.ticks.fixGlobalFrequency()
            root.sim_quantum = m5.ticks.fromSeconds(0.001)

        if self._board._checkpoint:
            m5.instantiate(self._board._checkpoint.as_posix())
        else:
            m5.instantiate(self._checkpoint_path)

        self._instantiated = True
        self._board._post_instantiate()
        self._device_board._post_instantiate()


def _serial_contains(path: str, needle: str) -> bool:
    """Return True iff `needle` appears in the file at `path`. Returns
    False if the file doesn't exist yet (Terminal creates it lazily on
    first write).
    """
    try:
        with open(path, "rb") as f:
            return needle.encode() in f.read()
    except FileNotFoundError:
        return False


def serial_barrier_handler(
    host_serial_path: str,
    device_serial_path: str,
    host_pass: str = "host boot OK",
    device_pass: str = "device boot OK",
    checkpoint_dir: str = None,
    transfer_trigger=None,
):
    """Generator that yields True iff both Systems' PASS strings have
    appeared in their serial output. The Terminal SimObject is
    unit-buffered (src/dev/serial/terminal.cc:131), so a read against
    these files mid-simulation reflects guest output up to the last
    character emitted.

    The handler ignores WHICH exit event fired — every event is
    treated as just an opportunity to recheck the barrier. This is
    robust against:
      - explicit `m5 exit;` from our scripts,
      - "exiting with last active thread context" when Linux idles
        a System's only CPU after userspace dies,
      - any future hook (rc.local loops, kernel panic shims, etc.).

    Yields False forever until both PASS strings are seen, then
    yields True once to terminate the run loop.

    If `checkpoint_dir` is set, m5.checkpoint(checkpoint_dir) is called
    at the moment the barrier is met, BEFORE yielding True. At that
    point both guests are parked in their liveness loops: NMP device
    untouched, no DMA in flight — the quiescent point required because
    none of the custom CXL objects (cxl_bridge.cc, cxl_memory.cc,
    cxl_nmp_device.cc) implements serialize() or drain().

    HONEST CAVEAT — a clean checkpoint here is EVIDENCE, NOT PROOF that
    the CXL path survives save/restore. m5.checkpoint() runs
    memWriteback() first, and the host kernel enrolls CXL DRAM as
    NUMA-node-1 RAM, so dirty CXL-backed cache lines (if any exist at
    boot) must flush FUNCTIONALLY through CXLBridge -> CXLMemory.
    CXLBridge supports functional access (cxl_bridge.cc:477); CXLMemory
    has no functional-path code of its own. And the restored run
    deliberately never reads CXL memory back. CXL-path integrity across
    checkpoint/restore remains UNVERIFIED until a later run has a
    restored guest read back known CXL contents.
    """
    while True:
        # --runtime-transfer: checked BEFORE the barrier so the transfer
        # lands even if this same activation ends the run.
        if transfer_trigger is not None:
            transfer_trigger()
        host_done = _serial_contains(host_serial_path, host_pass)
        dev_done = _serial_contains(device_serial_path, device_pass)
        if host_done and dev_done:
            if checkpoint_dir is not None:
                print(
                    f"[barrier] both PASS strings seen — "
                    f"writing checkpoint to {checkpoint_dir}"
                )
                # Same pattern as stdlib save_checkpoint_generator:
                # m5.checkpoint() drains, runs memWriteback over both
                # Systems, then serializes the global simObjectList.
                m5.checkpoint(checkpoint_dir)
                # Record the exact invocation so the restore run can
                # replay an identical topology (restore matches
                # checkpoint sections to SimObject paths; core count,
                # memory sizes and --is_asic must not drift).
                with open(
                    os.path.join(checkpoint_dir, "TAKE_CMDLINE.txt"), "w"
                ) as f:
                    f.write("taken by: " + " ".join(sys.argv) + "\n")
                    # Machine-readable record; the restore-time check
                    # parses this line and rejects a differing
                    # --device-cores rather than failing at opaque
                    # section-mismatch time.
                    f.write(f"device_cores: {args.device_cores}\n")
                print("[barrier] checkpoint written — ending simulation")
            print(
                f"[barrier] both PASS strings seen "
                f"(host_done={host_done}, dev_done={dev_done}) "
                f"— ending simulation"
            )
            yield True
        else:
            print(
                f"[barrier] exit handled; barrier not met "
                f"(host_done={host_done}, dev_done={dev_done}) "
                f"— continuing"
            )
            yield False


def kvm_boot_barrier_handler(
    host_serial_path: str,
    device_serial_path: str,
    boot_host: str,
    boot_dev: str,
    done_host: str,
    done_dev: str,
    host_processor,
    device_processor,
    host_readfile_path: str,
    device_readfile_path: str,
    host_phase2: str,
    device_phase2: str,
    transfer_trigger=None,
    dest_label: str = "ATOMIC",
):
    """Two-phase barrier for --kvm-boot.

    Phase 1 (KVM boot): every exit event rechecks the serials for BOTH
    boot PASS strings. The guests park in a heartbeat/poll loop after
    their PASS echo, so exit events keep arriving — this is what makes
    the barrier robust to the KVM serial-drain race (a PASS string can
    land in the file AFTER the exit event of the m5op that followed it;
    diagnosed on the --dual-kvm smoke run, where the run's LAST event
    preceded the device's PASS landing and the barrier starved).

    At the barrier: BOTH processors switch KVM->ATOMIC together, never
    per-System — a lone ATOMIC System coexisting with a still-booting
    KVM System recreates Attempt B's TSC-drift hazard (module
    docstring). m5.switchCpus does the takeover and flips each System's
    memory mode itself (m5/simulate.py, "Change the memory mode if
    required"). The workload is then RELEASED by rewriting each board's
    readfile with the phase-2 script: pseudo_inst::readfile re-opens
    the file on every call (src/sim/pseudo_inst.cc:376-384), so the
    guests' poll loops observe the marker on their next iteration and
    exec the workload — entirely under ATOMIC.

    Phase 2 (ATOMIC workload): terminate when both completion strings
    appear. The phase-2 scripts end in the same heartbeat loop, so the
    completion strings are also drain-race-immune.
    """
    switched = False
    while True:
        # --runtime-transfer: the marker is emitted by the phase-2 (post-
        # switch, ATOMIC) host script, so this fires in the second phase;
        # checking every activation is harmless before then.
        if transfer_trigger is not None:
            transfer_trigger()
        if not switched:
            hb = _serial_contains(host_serial_path, boot_host)
            db = _serial_contains(device_serial_path, boot_dev)
            if hb and db:
                print(
                    "[kvm-boot] boot barrier met — switching BOTH "
                    f"processors KVM->{dest_label} together"
                )
                with open(host_readfile_path, "w") as f:
                    f.write(host_phase2)
                with open(device_readfile_path, "w") as f:
                    f.write(device_phase2)
                host_processor.switch()
                device_processor.switch()
                switched = True
                print(
                    "[kvm-boot] switch complete; phase-2 workload "
                    f"injected via readfile — continuing under {dest_label}"
                )
                yield False
            else:
                print(
                    f"[kvm-boot] boot barrier not met "
                    f"(host={hb}, dev={db}) — continuing under KVM"
                )
                yield False
        else:
            hd = _serial_contains(host_serial_path, done_host)
            dd = _serial_contains(device_serial_path, done_dev)
            if hd and dd:
                print(
                    "[kvm-boot] workload barrier met "
                    f"(host_done={hd}, dev_done={dd}) — ending simulation"
                )
                yield True
            else:
                print(
                    f"[kvm-boot] post-switch; workload barrier not met "
                    f"(host={hd}, dev={dd}) — continuing"
                )
                yield False


def make_transfer_trigger(
    marker: str,
    host_serial_path: str,
    host_hierarchy,
    device_board,
    base: int,
    size: int,
):
    """One-shot runtime-transfer trigger for --runtime-transfer, shared by
    both exit handlers (called at the top of every handler activation).

    When `marker` appears in the host serial file: with simulation paused
    (we are between m5.simulate() slices), call releaseHeldRegion on the
    HOST verifier, then acquireHeldRegion on the DEVICE verifier — in that
    order, in this one activation. Python is single-threaded and no event
    runs between the two calls, so the ordered pair is atomic in simulated
    time: the neither-holds window has zero simulated duration.

    Takes the host HIERARCHY (not the verifier): the host verifier is
    created late, inside incorporate_cache during _pre_instantiate, so it
    does not exist when this trigger is constructed. By the time any exit
    event fires, instantiate has completed and `.verifier` (and the
    exported C++ methods, forwarded via the SimObject wrapper) exist. The
    device verifier is a plain board attribute available from board
    construction.
    """
    state = {"done": False}

    def maybe_fire():
        if state["done"]:
            return
        if not _serial_contains(host_serial_path, marker):
            return
        host_verifier = host_hierarchy.verifier
        device_verifier = device_board.cxl_verifier
        # ORDER MATTERS: release first, then acquire. Reversing this would
        # create a dual-holder state, the exact failure mode the paused-
        # instant pair exists to exclude.
        host_node = host_verifier.releaseHeldRegion(base, size)
        device_node = device_verifier.acquireHeldRegion(base, size)
        assert host_node == device_node, (
            f"[transfer] covering-node mismatch: host={host_node} "
            f"device={device_node} — identical geometry should derive "
            f"identical nodes"
        )
        print(
            f"[transfer] host RELEASED then device ACQUIRED "
            f"[{base:#x}..{base + size:#x}) at tick {m5.curTick()} — "
            f"covering node {host_node} (host == device), zero simulated "
            f"time between the two mutations"
        )
        state["done"] = True

    return maybe_fire


# =============================================================================
# CLI
# =============================================================================
requires(isa_required=ISA.X86)

parser = argparse.ArgumentParser(
    description="Two-System x86 Linux smoke test."
)
parser.add_argument(
    "--is_asic",
    type=str,
    nargs="?",
    choices=["True", "False"],
    default="True",
    help="ASIC vs FPGA CXL device latency model (host-side only).",
)
parser.add_argument(
    "--take-checkpoint",
    metavar="DIR",
    default=None,
    help="Cold-boot both Systems; when the serial barrier is met "
    "(both guests booted and parked in their liveness loops), "
    "checkpoint into DIR and exit cleanly.",
)
parser.add_argument(
    "--restore",
    metavar="DIR",
    default=None,
    help="Restore both Systems from the checkpoint in DIR instead of "
    "cold-booting. The config must be IDENTICAL to the "
    "--take-checkpoint run (same core counts, memory sizes, "
    "--is_asic) — see TAKE_CMDLINE.txt inside DIR.",
)
parser.add_argument(
    "--atomic",
    action="store_true",
    help="Boot both Systems under ATOMIC CPUs instead of TIMING. "
    "Dev-speed variant for functional work (the host->device handshake): "
    "iterates in minutes, NO timing fidelity. Use TIMING (the default) "
    "for timing-accurate/benchmark runs.",
)
parser.add_argument(
    "--dual-kvm",
    action="store_true",
    help="EXPERIMENT: boot BOTH Systems under KVM cores. Exists purely to "
    "answer one question — does dual-KVM boot when the two Systems' KVM "
    "vCPUs are on DISJOINT event queues? (Attempt A in the module docstring "
    "hung with both serials silent; the suspected cause is the stdlib's "
    "per-processor eventq numbering, base_cpu_processor.py:75-79, which "
    "lands the host core and device core 0 on the SAME queue — KVM's "
    "signal/timer setup is thread-specific, base.cc:254-261. "
    "TwoSystemSimulator._instantiate renumbers the queues disjointly.) "
    "Boot-only smoke test: not combinable with any other mode flag.",
)
parser.add_argument(
    "--kvm-boot",
    action="store_true",
    help="Boot BOTH Systems under KVM (fast, minutes), then switch BOTH to "
    "ATOMIC at the boot barrier and run the workload under ATOMIC. Uses "
    "SimpleSwitchableProcessor(KVM->ATOMIC) per board plus the disjoint "
    "event-queue renumbering proven by --dual-kvm. The guests park in a "
    "heartbeat/poll loop after boot; when both PASS strings are in serial "
    "the handler switches both processors TOGETHER (never per-System — "
    "Attempt B's TSC hazard) and releases the workload by rewriting each "
    "board's readfile (m5 readfile re-reads the file per call, "
    "pseudo_inst.cc:376). Composes with --offload/--device-integrity/"
    "--device-handoff; the workload runs entirely under the destination "
    "mode (--kvm-dest, default ATOMIC).",
)
parser.add_argument(
    "--kvm-dest",
    choices=["atomic", "timing"],
    default="atomic",
    help="Destination CPU mode for the --kvm-boot switch (default: atomic). "
    "'timing' boots both Systems under KVM (fast), then switches BOTH "
    "together to TIMING at the boot barrier -- the only practical way to "
    "exercise the integrity walk (recvAtomic performs no walk), since a "
    "cold two-System TIMING boot is impractical. One variable feeds both "
    "processors' switch_core_type, so the two Systems cannot be given "
    "different destinations; the barrier handler switches them in one "
    "activation as before (a lone KVM System racing a TIMING one is the "
    "TSC-drift hazard). Only meaningful with --kvm-boot.",
)
parser.add_argument(
    "--kvm-no-perf",
    action="store_true",
    help="With --dual-kvm/--kvm-boot: set usePerf=False on every KVM core. "
    "Diagnostic fallback ONLY — use if the KVM run dies at startup with a "
    "perf_event_open error (host perf_event_paranoid too strict) so a perf "
    "permission failure is not misread as the Attempt-A hang.",
)
parser.add_argument(
    "--device-cores",
    type=int,
    default=2,
    metavar="N",
    help="Number of device cores (default: 2, the historical hardcoded "
    "value). Used by BOTH device-processor branches (KVM and non-KVM). "
    "Use 1 under --kvm-boot/--dual-kvm to sidestep the wait-for-SIPI AP "
    "unpark issue (a parked KVM AP has no re-park path once a stray "
    "interrupt wakes it; see the comment at the device-processor "
    "construction). Checkpoints record this value; --restore rejects a "
    "mismatch.",
)
parser.add_argument(
    "--offload",
    action="store_true",
    help="MVP host->device code offload over a shared CXL mailbox. Host "
    "carves the top 16 MiB of CXL as Reserved (memmap=) and runs "
    "/home/cxl_benchmark/host_offload; device runs device_offload. "
    "Intended with --atomic. Requires both binaries installed in the "
    "guest image (benchmarks/Makefile `install`).",
)
parser.add_argument(
    "--device-integrity",
    action="store_true",
    help="Splice an IntegrityVerifier on the DEVICE System's read-from-CXL "
    "(ingress) path, between the device membus and device_iobridge. The "
    "verifier protects the shared CXL window (CxlOnly, TimingBmt) and is "
    "inert/pass-through for the offload mailbox region. Default off. Under "
    "--atomic the gate is build+boot+routing (config.ini), not stats.",
)
parser.add_argument(
    "--device-handoff",
    action="store_true",
    help="§6.2 range-keyed subtree handoff (requires --device-integrity). The "
    "host hands the device AUTHORITY over a contiguous region at the start of "
    "the device's protected CXL window; the device verifier re-roots its "
    "integrity walk for that range. The host offload runs the OP_HANDOFF "
    "dispatch: XTEA blob ships in the mailbox (control channel) but the "
    "key/plaintext operands are written INTO the handed-off protected region "
    "(data path); the device prints the handoff receipt, reads the operands "
    "out of the region, executes the blob, and returns the ciphertext. A "
    "second host memmap= carve makes the region /dev/mem-mmappable. Default "
    "off. Under --atomic the gate is config + receipt + ciphertext match "
    "(functional data-binding), not stats.",
)
parser.add_argument(
    "--host-integrity",
    action="store_true",
    help="Splice an IntegrityVerifier below the HOST System's shared L3, "
    "protecting the SAME CXL window as the device verifier: CxlOnly, "
    "TimingBmt, identical arity and identical protected/full ranges, so both "
    "verifiers compute identical node indices and identical metadata "
    "addresses for the same physical byte. Host DRAM goes UNPROTECTED in "
    "this mode (accepted modeling boundary). Adds a memmap= Reserved carve "
    "for the integrity region to the host kernel args so the host page "
    "allocator stays out of the metadata. Independent of --device-integrity; "
    "combine both for the two-verifier configuration. Default off -> the "
    "host gets the stock non-verifier hierarchy, unchanged.",
)
parser.add_argument(
    "--held-region",
    action="store_true",
    help="Give BOTH verifiers held-region root state over the same 16 KiB "
    "region of the protected CXL window (requires --host-integrity and "
    "--device-integrity): the host verifier RELEASES it (any host walk into "
    "the region panics -- denial-by-assertion) and the device verifier "
    "ACQUIRES it (its walk terminates at the region's covering tree node "
    "instead of node 0). The region defaults to 16 KiB at protected offset "
    "0x20000000 (absolute 0x120000000) and is settable with "
    "--held-region-offset/--held-region-size -- any size-aligned "
    "16 KiB/64 KiB/.../1 GiB region qualifies. "
    "A memmap= Reserved carve keeps the host page allocator "
    "off the released region. Static param-time population -- no runtime "
    "transfer yet. Default off.",
)
parser.add_argument(
    "--held-region-offset",
    type=lambda s: int(s, 0),
    default=0x20000000,
    metavar="OFF",
    help="Protected-range offset of the held region (default 0x20000000, "
    "today's value). Must be aligned to --held-region-size; the verifier "
    "derives the covering tree node at init() and fatals with the "
    "admissible-shape list if the region has none. Set this together with "
    "--held-region-size to make the handed-off region BE the region a "
    "--graph-walk device arm then walks (offset 0x40000000, size 64MiB).",
)
parser.add_argument(
    "--held-region-size",
    type=str,
    default="16KiB",
    metavar="SIZE",
    help="Size of the held region (default 16KiB, today's value). Must be "
    "one of the arity^k admissible shapes -- 16KiB, 64KiB, 256KiB, 1MiB, "
    "4MiB, 16MiB, 64MiB, 256MiB, 1GiB for arity 4 over the 2 GiB carve -- "
    "and the offset must be aligned to it. 64MiB is the smallest shape "
    "that contains the default graph CSR.",
)
parser.add_argument(
    "--runtime-transfer",
    action="store_true",
    help="Runtime writer for the held-region root state (requires "
    "--host-integrity and --device-integrity). Both verifiers boot INERT; "
    "when the host guest emits the transfer marker over serial, the exit "
    "handler -- with simulation paused between simulate() slices -- calls "
    "releaseHeldRegion on the HOST verifier, then acquireHeldRegion on the "
    "DEVICE verifier, in that order, in ONE handler activation: zero "
    "simulated time between the two mutations. Same 16 KiB region as "
    "--held-region (offset 0x20000000); both calls return the covering "
    "node and the handler cross-checks they agree. Mutually exclusive "
    "with --held-region (static population of the same state) and "
    "--device-handoff (M2 authority on the device verifier). The region's "
    "memmap= Reserved carve is still emitted at boot (kernel args are "
    "fixed at boot; release happens later). Composes with the smoke/boot "
    "flows only (default TIMING, --atomic, --kvm-boot). Default off.",
)
parser.add_argument(
    "--read-block",
    action="store_true",
    help="Splice a ReadBlockGate on each CXL DRAM channel (between "
    "cxl_mem_bus and the MemCtrl): a host TIMING read of the mailbox "
    "STATUS slot is HELD, unanswered, until a store to that slot arrives "
    "(the device's STATUS_BUSY/STATUS_DONE writes), then completed with "
    "the stored value -- read-blocking completion, no polling. The gate "
    "is value-blind; the BUSY release is intended (the guest loop's next "
    "load is simply held again). Stores are FORWARDED as well as "
    "observed, so DRAM stays authoritative. Requires a timing workload "
    "phase: refuses --atomic, --dual-kvm, --kvm-boot with atomic "
    "destination, and checkpointing (a held load blocks the drain). "
    "Default off -> the bus-to-MemCtrl wiring is byte-identical.",
)
parser.add_argument(
    "--poll-us",
    type=int,
    default=1000,
    metavar="US",
    help="Host offload poll period in simulated microseconds, threaded "
    "into the guest as the MB_POLL_US environment variable "
    "(host_offload.c reads it at startup; compiled-in default 1000). "
    "0 = busy-spin (no usleep at all). Exists so the polling baseline "
    "can be swept rather than asserted. Only meaningful with --offload.",
)
parser.add_argument(
    "--timeout-s",
    type=int,
    default=200,
    metavar="S",
    help="Poll budget in SIMULATED seconds, threaded to every guest "
    "poller as MB_TIMEOUT_S (host_offload, device_offload, "
    "graph_walk_host). The budget is time-equivalent, so changing "
    "--poll-us does not change how long a poller waits. ONE knob for "
    "all three: the historical budgets were asymmetric by inheritance "
    "(graph_walk_host 200 s, the two offload guests 100 s) and this "
    "default preserves the LARGER one, so no run that used to succeed "
    "can now time out. NOTE this does not order the two waits: the "
    "device's doorbell wait starts before the host reaches the "
    "doorbell, so a slow host build can still exhaust the device "
    "first -- both then print TIMEOUT and the run ends diagnosably.",
)
parser.add_argument(
    "--cache-probe",
    action="store_true",
    help="Run the /dev/mem cacheability probe (benchmarks/cache_probe.c) "
    "instead of a workload: the host kernel gets a dedicated Reserved "
    "carve (memmap=32M$0x140000000) and the host guest runs cache_probe "
    "against it, measuring whether an O_SYNC and a no-O_SYNC mapping of "
    "the carve are cacheable. The run terminates on the probe's "
    "completion echo whether the probe passes, fails, or errors. "
    "Measures the PLAIN path: mutually exclusive with the offload/"
    "integrity/handoff/held-region/runtime-transfer/read-block/"
    "checkpoint machinery. Composes with the default TIMING flow and "
    "with --kvm-boot (use --kvm-dest timing for a timing-fidelity "
    "verdict). Grep the host serial for 'CACHE PROBE'. Default off.",
)
parser.add_argument(
    "--graph-walk",
    choices=["host", "device"],
    default=None,
    help="Run the CXL graph-walk comparison workload instead of a "
    "smoke test. 'host' (config 1): the host CPU runs the random walk "
    "over a CSR graph resident in a CACHEABLE CXL carve, missing to "
    "CXL from its own hierarchy. 'device' (config 2): the host builds "
    "the same graph, flushes it, and ships the walk to the device NMP "
    "via OP_WALK (in-place pointer blob); the bracket includes dispatch "
    "and completion detection. Both modes walk the IDENTICAL sequence "
    "(shared seed/steps via gw_header) and must print identical "
    "checksums. m5_reset_stats/m5_dump_stats bracket the work; compare "
    "simTicks of the bracketed dump between the two runs. NO integrity "
    "verifier in either mode. Requires a TIMING workload phase. Grep "
    "host serial for 'GRAPH WALK'. Default off.",
)
parser.add_argument(
    "--graph-nodes",
    type=int,
    default=65536,
    metavar="N",
    help="Graph node count for --graph-walk (default 65536 -- a small "
    "smoke size whose CSR fits in the host L3; scale up to exceed it).",
)
parser.add_argument(
    "--graph-degree",
    type=int,
    default=8,
    metavar="D",
    help="Fixed out-degree for --graph-walk (default 8). CSR bytes = "
    "4*((N+1) + N*D) plus a header page.",
)
parser.add_argument(
    "--graph-steps",
    type=int,
    default=1000000,
    metavar="S",
    help="Walk length for --graph-walk (default 1e6). Two dependent "
    "loads per step.",
)
parser.add_argument(
    "--graph-transfer",
    action="store_true",
    help="Runtime authority migration DRIVEN BY the graph-walk guest "
    "(requires --graph-walk device, --host-integrity, --device-integrity). "
    "Both verifiers boot INERT; graph_walk_host.c builds and flushes the "
    "CSR, quiesces the region, prints the transfer marker and calls "
    "m5_exit, and the exit handler -- simulation paused -- calls "
    "releaseHeldRegion on the HOST verifier then acquireHeldRegion on the "
    "DEVICE verifier. Only then does the host ring the doorbell, so the "
    "device walks a region whose authority it already holds and its walks "
    "terminate at the region's covering node instead of node 0. The "
    "release lands OUTSIDE the measurement bracket (before "
    "m5_reset_stats), so both arms bracket identical work. Uses the "
    "--held-region-offset/--held-region-size geometry: pass 0x40000000 "
    "and 64MiB to make the handed-off region the region the graph "
    "occupies. DISTINCT from --runtime-transfer, which owns host_cmd "
    "itself and therefore remains incompatible with --graph-walk. "
    "Default off.",
)
parser.add_argument(
    "--dispatch-block",
    action="store_true",
    help="Mirror of --read-block, on the device's side of the "
    "handshake: hold the DEVICE's doorbell poll read of the mailbox "
    "command word until the HOST's store to that same word arrives, "
    "then complete it from the store's payload. The device blocks on "
    "one load instead of waking every poll period, so its pickup "
    "becomes exact instead of quantised (expected saving: half the "
    "poll period, ~500 us at the 1000 us default, against a ~160 ns "
    "link round trip). Implemented as a SECOND INSTANCE of the same "
    "gate chained per channel, so the two holds cannot interfere. "
    "THIS IS NOT DISPATCH IN HARDWARE: the device still issues the "
    "load it blocks on; what moves into hardware is the timing of the "
    "release, not the decision to start. Requires a TIMING workload "
    "phase. Default off.",
)
parser.add_argument(
    "--observe-cxl",
    action="store_true",
    help="Splice a passive CxlTrafficObserver at S1 (between the CXL "
    "controller's memory-side port and cxl_mem_bus), where ALL host "
    "traffic to CXL DRAM passes undivided by channel. It forwards every "
    "packet verbatim in every mode, acts on none, and adds no latency; "
    "under TIMING it classifies each request into stats: write-backs by "
    "command (WritebackDirty/Clean, WriteClean), CleanEvict counted "
    "SEPARATELY because it carries no payload and is not a write, "
    "demand vs prefetch, verifier metadata traffic by tag rather than "
    "by address, and reads. It also reports distinct-line coverage over "
    "the observed range. IT HOLDS NO COUNTER and derives none: the "
    "integrity engine stores no node values, so a derived counter would "
    "have nowhere to live and nothing to check against. This supports a "
    "claim about OBSERVABILITY and COST only. Observed range = the "
    "protected CXL OS carve. Requires a TIMING workload phase (under "
    "KVM no packet is produced at all). Default off.",
)
parser.add_argument(
    "--graph-transfer-quiesce-us",
    type=int,
    default=2000,
    metavar="US",
    help="Simulated microseconds graph_walk_host.c sleeps after the "
    "flush, before emitting the --graph-transfer marker (default 2000). "
    "Best-effort quiesce: releaseHeldRegion fatals if ANY packet with a "
    "region address is still outstanding in the host verifier, and three "
    "host prefetchers feed that seam. With no demand stream during the "
    "sleep no new prefetches are generated and outstanding ones retire, "
    "but nothing guarantees emptiness -- raise this if the release "
    "fatals with 'packet(s) with region addresses are still outstanding'.",
)
parser.add_argument(
    "--cxl-latency",
    type=int,
    default=None,
    metavar="NS",
    help="Modeled HOST-side CXL crossing cost in ns, ONE-WAY (applied "
    "symmetrically per direction, so a load round-trip pays 2x). Maps "
    "onto the host path's three fixed components: the two protocol-"
    "processing latencies stay at their model values (CXLBridge "
    "proto_proc_lat 12ns + CXLMemory proto_proc_lat 15ns ASIC / 60ns "
    "FPGA) and the remainder goes to CXLBridge bridge_lat (the link-"
    "flight term). Default (flag absent): parameters untouched -- "
    "today's 50+12+15 = 77ns one-way. The DEVICE's path (its 50ns "
    "device_iobridge) is deliberately NOT touched: the device sits on "
    "the far side of the link and this knob models the host's crossing "
    "only. The banner prints the mapping in effect.",
)
parser.add_argument(
    "--host-like-device",
    action="store_true",
    help="ABLATION flag, not a new default: give the HOST the device's "
    "core and cache configuration -- same hierarchy class "
    "(PrivateL1PrivateL2, i.e. NO L3 at all), same L1I/L1D/L2 sizes "
    "and associativities, same 1.5GHz clock -- read from the device's "
    "own single-sourced configuration so the two cannot drift. Its "
    "purpose is to isolate what memory PLACEMENT alone buys in the "
    "graph-walk comparison, by removing the core and cache asymmetry. "
    "The device is never changed. Off by default; with it off the "
    "host is exactly as today. Incompatible with --host-integrity "
    "(which requires the SharedL3 verifier hierarchy).",
)
args = parser.parse_args()
if args.take_checkpoint and args.restore:
    parser.error("--take-checkpoint and --restore are mutually exclusive.")
if args.offload and (args.take_checkpoint or args.restore):
    parser.error(
        "--offload cannot be combined with --take-checkpoint/--restore."
    )
if args.device_handoff and not args.device_integrity:
    parser.error("--device-handoff requires --device-integrity.")
if args.device_handoff and not args.offload:
    parser.error("--device-handoff requires --offload (it rides the mailbox).")
if args.held_region and not (args.host_integrity and args.device_integrity):
    parser.error(
        "--held-region requires both --host-integrity and --device-integrity "
        "(host releases, device acquires -- both verifiers must exist)."
    )
if args.held_region and args.device_handoff:
    parser.error(
        "--held-region and --device-handoff are mutually exclusive: both "
        "install walk-termination authority on the device verifier, and the "
        "verifier refuses to hold both (init() fatal)."
    )
if args.runtime_transfer and not (
    args.host_integrity and args.device_integrity
):
    parser.error(
        "--runtime-transfer requires both --host-integrity and "
        "--device-integrity (host releases, device acquires -- both "
        "verifiers must exist)."
    )
if args.runtime_transfer and args.held_region:
    parser.error(
        "--runtime-transfer and --held-region are mutually exclusive: both "
        "populate the same held-region state (runtime writer vs static "
        "params; the verifier also fatals on double population)."
    )
if args.runtime_transfer and args.device_handoff:
    parser.error(
        "--runtime-transfer and --device-handoff are mutually exclusive: "
        "M2 authority on the device verifier blocks the runtime writer "
        "(verifier fatal at the mutation point)."
    )
if args.runtime_transfer and (
    args.offload or args.take_checkpoint or args.restore
):
    parser.error(
        "--runtime-transfer composes only with the smoke/boot flows "
        "(default TIMING, --atomic, --kvm-boot); not with "
        "--offload/--take-checkpoint/--restore."
    )
# A checkpoint encodes its CPU class + mem_mode; ATOMIC and TIMING cannot
# cross-restore. Fail fast rather than at opaque section-mismatch time.
if args.atomic and (args.take_checkpoint or args.restore):
    parser.error(
        "--atomic cannot be combined with --take-checkpoint/--restore: "
        "a checkpoint's CPU class and mem_mode are mode-specific."
    )
# --dual-kvm is a boot-only experiment (does dual-KVM boot with disjoint
# event queues?). Reject every other mode flag so the result answers
# exactly that question, with no offload/verifier/checkpoint variables.
if args.dual_kvm and (
    args.atomic
    or args.offload
    or args.take_checkpoint
    or args.restore
    or args.device_integrity
    or args.device_handoff
    or args.host_integrity
    or args.read_block
    or args.cache_probe
):
    parser.error(
        "--dual-kvm is a boot-only smoke test; it cannot be combined with "
        "--atomic/--offload/--take-checkpoint/--restore/--device-integrity/"
        "--device-handoff/--host-integrity/--read-block/--cache-probe."
    )
# --read-block interlocks. A held read cannot exist outside timing mode
# (the gate's recvAtomic must return synchronously; it fatals at init
# under plain atomic), and a load held across a drain point hangs the
# run (TimingSimpleCPU refuses to drain with an access outstanding), so
# checkpointing is out until the gate is quiesce-aware.
if args.read_block and args.atomic:
    parser.error(
        "--read-block cannot be combined with --atomic: a held read "
        "cannot exist outside timing mode (the gate would fatal at "
        "init anyway)."
    )
if args.read_block and args.kvm_boot and args.kvm_dest != "timing":
    parser.error(
        "--read-block with --kvm-boot requires --kvm-dest timing: the "
        "workload phase must run under TIMING for a read to be held; "
        "an ATOMIC workload would silently measure nothing."
    )
if args.read_block and (args.take_checkpoint or args.restore):
    parser.error(
        "--read-block cannot be combined with --take-checkpoint/"
        "--restore: a held load blocks the pre-checkpoint drain, and "
        "the gate carries no serialization."
    )
if args.poll_us < 0:
    parser.error("--poll-us must be >= 0 (0 = busy-spin).")
# --cache-probe interlocks: the probe replaces the host workload, so it
# cannot combine with anything that hardwires host_cmd (--offload,
# checkpointing, --runtime-transfer); and it exists to measure the PLAIN
# host->CXL path, so the verifier/handoff/held/read-block machinery must
# not be instantiated in the same run.
if args.cache_probe and args.offload:
    parser.error(
        "--cache-probe and --offload are mutually exclusive: both "
        "hardwire the host command."
    )
if args.cache_probe and (args.take_checkpoint or args.restore):
    parser.error(
        "--cache-probe cannot be combined with --take-checkpoint/"
        "--restore: both replace the host command and park loops."
    )
if args.cache_probe and args.runtime_transfer:
    parser.error(
        "--cache-probe and --runtime-transfer are mutually exclusive: "
        "both rewrite the host command."
    )
if args.cache_probe and (
    args.host_integrity
    or args.device_integrity
    or args.device_handoff
    or args.held_region
    or args.read_block
):
    parser.error(
        "--cache-probe measures the plain host->CXL path; it cannot be "
        "combined with --host-integrity/--device-integrity/"
        "--device-handoff/--held-region/--read-block."
    )
# --graph-walk interlocks: it replaces the host command and measures the
# PLAIN path (no verifier in either config -- that is a later step), and
# a TIMING workload phase is required for the measurement to mean
# anything.
if args.graph_walk and (
    args.offload
    or args.cache_probe
    or args.take_checkpoint
    or args.restore
    or args.runtime_transfer
):
    parser.error(
        "--graph-walk cannot be combined with --offload/--cache-probe/"
        "--take-checkpoint/--restore/--runtime-transfer: they rewrite "
        "the host command."
    )
# --graph-walk now COMPOSES with --host-integrity, --device-integrity,
# --held-region, and --read-block: the first mechanism+measurement
# combined runs. The graph carve lies inside the verifiers' protected
# range, so with integrity on, every graph access is verified traffic
# (the walk's first exercise under a workload). Only the M2 handoff
# stays fenced, and DELIBERATELY so -- not as a leftover: it is
# static, param-time, device-side-only, with no release side, and it
# must not be reachable from a measurement flow until it is chosen
# explicitly.
if args.graph_walk and args.device_handoff:
    parser.error(
        "--graph-walk with --device-handoff is excluded ON PURPOSE, "
        "not as a leftover: the static M2 authority mechanism stays "
        "unreachable from measurement flows until chosen explicitly."
    )
if args.graph_walk and args.atomic:
    parser.error(
        "--graph-walk requires a TIMING workload phase; --atomic would "
        "measure atomic-mode latency estimates."
    )
if args.graph_walk and args.dual_kvm:
    parser.error("--graph-walk cannot be combined with --dual-kvm.")
if args.graph_walk and args.kvm_boot and args.kvm_dest != "timing":
    parser.error(
        "--graph-walk with --kvm-boot requires --kvm-dest timing."
    )
if args.graph_walk and (args.graph_nodes < 2 or args.graph_degree < 1
                        or args.graph_steps < 1):
    parser.error("--graph-nodes >= 2, --graph-degree >= 1, "
                 "--graph-steps >= 1 required.")
# --graph-transfer: the graph-walk guest drives the runtime migration.
# Note this does NOT weaken the host_cmd conflict above -- the
# --runtime-transfer FLAG stays rejected against --graph-walk, because
# that flow assigns host_cmd itself. What becomes reachable here is the
# transfer CAPABILITY (maybe_fire), which is flow-agnostic: it greps the
# serial file and is invoked from every handler activation regardless of
# which flow built the guest command.
if args.graph_transfer and args.graph_walk != "device":
    parser.error(
        "--graph-transfer requires --graph-walk device: the migration "
        "exists so the DEVICE walks a region whose authority it holds."
    )
if args.graph_transfer and not (
    args.host_integrity and args.device_integrity
):
    parser.error(
        "--graph-transfer requires both --host-integrity and "
        "--device-integrity (host releases, device acquires -- both "
        "verifiers must exist)."
    )
if args.graph_transfer and args.held_region:
    parser.error(
        "--graph-transfer and --held-region are mutually exclusive. "
        "--held-region populates the held state from params at init(), "
        "i.e. BEFORE the guest runs, so the host is already the Releaser "
        "when graph_walk_host.c writes the CSR and the first store hits "
        "the walk-entry panic. --graph-transfer is the runtime form: "
        "both verifiers boot inert and the release happens after the "
        "flush."
    )
if args.graph_transfer_quiesce_us < 0:
    parser.error("--graph-transfer-quiesce-us must be >= 0.")
# --observe-cxl: the observer counts only on the TIMING path, and under
# KVM the CXL ranges are a KVM memslot so no packet exists to observe.
# Reject the combinations that can NEVER reach TIMING rather than let
# the run report a zero that looks like a measurement.
if args.dispatch_block and args.atomic:
    parser.error(
        "--dispatch-block cannot be combined with --atomic: a held "
        "read cannot exist outside timing mode (the gate fatals at "
        "init anyway)."
    )
if args.dispatch_block and args.dual_kvm:
    parser.error(
        "--dispatch-block cannot be combined with --dual-kvm: the run "
        "never leaves KVM, where CXL DRAM is a KVM memslot and guest "
        "accesses never become packets. Nothing would be held."
    )
if args.dispatch_block and args.kvm_boot and args.kvm_dest != "timing":
    parser.error(
        "--dispatch-block with --kvm-boot requires --kvm-dest timing: "
        "an ATOMIC workload phase produces no held read."
    )
if args.dispatch_block and (args.take_checkpoint or args.restore):
    parser.error(
        "--dispatch-block cannot be combined with --take-checkpoint/"
        "--restore: a held load blocks the pre-checkpoint drain."
    )
if args.observe_cxl and args.atomic:
    parser.error(
        "--observe-cxl cannot be combined with --atomic: the observer "
        "counts only on the TIMING path, so the run would report zero "
        "and that zero would not be a measurement."
    )
if args.observe_cxl and args.dual_kvm:
    parser.error(
        "--observe-cxl cannot be combined with --dual-kvm: the run "
        "never leaves KVM, where CXL DRAM is a KVM memslot and guest "
        "accesses never become packets. Nothing would be observable."
    )
if args.observe_cxl and args.kvm_boot and args.kvm_dest != "timing":
    parser.error(
        "--observe-cxl with --kvm-boot requires --kvm-dest timing: an "
        "ATOMIC workload phase produces no counted traffic."
    )
if args.host_like_device and args.host_integrity:
    parser.error(
        "--host-like-device and --host-integrity are incompatible: the "
        "verifier splice lives in the SharedL3 hierarchy the ablation "
        "removes."
    )
# --cxl-latency mapping: the two protocol-processing terms are fixed
# model values; the remainder is the CXLBridge link-flight term. The
# result is applied post-construction (params are plain Python until
# m5.instantiate), so with the flag absent nothing is touched.
_CXL_BRIDGE_PROTO_NS = 12
_CXL_CTRL_PROTO_NS = 15 if args.is_asic == "True" else 60
if args.cxl_latency is not None:
    _cxl_proto_sum = _CXL_BRIDGE_PROTO_NS + _CXL_CTRL_PROTO_NS
    if args.cxl_latency <= _cxl_proto_sum:
        parser.error(
            f"--cxl-latency must exceed the fixed protocol terms "
            f"({_cxl_proto_sum}ns = bridge {_CXL_BRIDGE_PROTO_NS} + "
            f"controller {_CXL_CTRL_PROTO_NS}); the remainder is the "
            f"bridge link-flight term."
        )
    _cxl_bridge_ns = args.cxl_latency - _cxl_proto_sum
if args.kvm_boot and args.dual_kvm:
    parser.error(
        "--kvm-boot and --dual-kvm are mutually exclusive (--dual-kvm is "
        "the boot-only experiment; --kvm-boot is the production KVM->ATOMIC "
        "flow)."
    )
if args.kvm_dest != "atomic" and not args.kvm_boot:
    parser.error(
        "--kvm-dest only selects the --kvm-boot switch destination; it "
        "does nothing without --kvm-boot."
    )
if args.kvm_boot and args.atomic:
    parser.error(
        "--kvm-boot already ends in ATOMIC (KVM boot, ATOMIC workload); "
        "drop --atomic."
    )
if args.kvm_boot and (args.take_checkpoint or args.restore):
    parser.error(
        "--kvm-boot cannot be combined with --take-checkpoint/--restore "
        "yet: switched-out cores and the mid-run readfile rewrite are not "
        "part of the proven checkpoint mechanism."
    )
if args.kvm_no_perf and not (args.dual_kvm or args.kvm_boot):
    parser.error("--kvm-no-perf only applies to --dual-kvm/--kvm-boot.")
if args.device_cores < 1:
    parser.error("--device-cores must be >= 1.")
# A checkpoint serializes per-core state (CPU threads, per-core lapic
# pendingInit/startedUp — interrupts.cc:774-801), so restoring with a
# different device core count fails at opaque section-mismatch time.
# Fail fast instead, using the count recorded in TAKE_CMDLINE.txt.
# Checkpoints predating --device-cores carry no record; they were all
# taken with the then-hardcoded 2.
if args.restore:
    _taken_cores = 2
    try:
        with open(os.path.join(args.restore, "TAKE_CMDLINE.txt")) as _f:
            for _line in _f:
                if _line.startswith("device_cores:"):
                    _taken_cores = int(_line.split(":", 1)[1])
    except FileNotFoundError:
        pass
    if _taken_cores != args.device_cores:
        parser.error(
            f"checkpoint {args.restore} was taken with device_cores="
            f"{_taken_cores}, but this run requests --device-cores "
            f"{args.device_cores}. Per-core state is serialized per core, "
            f"so the topologies must match exactly; re-run with "
            f"--device-cores {_taken_cores}."
        )

# Dev-speed vs timing-accurate selector. ATOMIC flips BOTH Systems'
# SimpleProcessors; each board's incorporate_processor then sets its own
# System.mem_mode to 'atomic' automatically (base_cpu_processor.py:99).
# Classic caches are retained in either mode ('atomic', not the KVM/Ruby
# 'atomic_noncaching' downgrade). ATOMIC + the custom CXL objects is
# already proven by x86-cxl-run.py's atomic-boot path.
# --dual-kvm flips both to KVM cores instead (mem_mode becomes
# 'atomic_noncaching' via the same incorporate_processor path; caches are
# present but bypassed — irrelevant for the boot-only experiment).
_cpu_type = (
    CPUTypes.KVM
    if args.dual_kvm
    else CPUTypes.ATOMIC
    if args.atomic
    else CPUTypes.TIMING
)

# --kvm-boot switch destination (--kvm-dest). ONE variable feeds BOTH
# boards' switch_core_type -- same never-drift idiom as --device-cores --
# so the two Systems cannot be built with different destinations; the
# barrier handler then switches both together in one activation, as it
# always has (the TSC-drift hazard is a lone KVM System racing a switched
# one, so together-ness is load-bearing).
_kvm_switch_type = (
    CPUTypes.TIMING if args.kvm_dest == "timing" else CPUTypes.ATOMIC
)


# =============================================================================
# Host X86Board — same configuration as x86-cxl-ptr-chase-test.py so
# the host-side regression test still passes against the same gem5 binary.
# (Memories are constructed before the cache hierarchy because the
# --host-integrity carve below needs the CXL window size.)
# =============================================================================
host_memory = DIMM_DDR5_4400(size="3GB")
if args.is_asic == "True":
    host_cxl_memory = DIMM_DDR5_4400(size="8GB")
else:
    host_cxl_memory = SingleChannelDDR4_3200(size="8GB")

# ---- CXL window geometry, single-sourced for this config ----
# The Python-side source for the mailbox size and window base used by BOTH
# the --offload memmap= carve (below) and the --host-integrity carve. The
# remaining copies of these constants live in benchmarks/cxl_mailbox.h
# (MB_BASE/MB_SIZE, guest C -- cannot import Python) and in
# device_x86_board.py's default derivation (its "16MiB" full-range exclusion
# and "2GiB" protected carve) -- left in place, out of this change's scope.
# The geometry-agreement assert after device_board construction catches any
# drift between here and the device board's internal derivation.
_CXL_WINDOW_BASE = 0x100000000  # matches x86_board.py's cxl_mem_start
_CXL_WINDOW_SIZE = int(host_cxl_memory.get_size())
_CXL_MAILBOX_SIZE = toMemorySize("16MiB")  # == MB_SIZE in cxl_mailbox.h
_CXL_MAILBOX_BASE = _CXL_WINDOW_BASE + _CXL_WINDOW_SIZE - _CXL_MAILBOX_SIZE

# --read-block slot: the mailbox STATUS field. Derived from the
# single-sourced mailbox base above, NOT a fourth base literal. The 72
# is `offsetof(struct cxl_mailbox, status)` -- MUST match the "off 72"
# field in benchmarks/cxl_mailbox.h (u32 status; the neighbouring
# `command` u32 at off 68 shares the same 64B line but does NOT
# intersect the 4-byte slot, so the device's doorbell polls are never
# held). The whole slot sits in one 64B line, hence on exactly one
# DRAM channel at the 64B interleave granule.
_RB_SLOT_OFF = 72
_RB_SLOT_ADDR = _CXL_MAILBOX_BASE + _RB_SLOT_OFF
_RB_SLOT_SIZE = 4

# --dispatch-block gates the DEVICE's doorbell poll: the same mechanism
# pointed the other way. The device polls `command`, which is the word
# ADJACENT to `status` in the same 64B line but a disjoint 4-byte slot,
# so the two gates can never match each other's word.
_DB_SLOT_OFF = 68
_DB_SLOT_ADDR = _CXL_MAILBOX_BASE + _DB_SLOT_OFF
_DB_SLOT_SIZE = 4


def _check_mailbox_slot(field, off, flag):
    """Drift check for a hand-synced mailbox field offset.

    No mechanism in this repo derives a config value from a guest
    header, and reimplementing the C struct layout here would just be a
    second drift surface -- so instead FAIL LOUDLY at startup if the
    header both guests compile no longer documents `field` at `off`.
    ONE source of truth (the header) shared by both slots; adding the
    command slot adds no new hand-synced literal beyond the offset this
    very check validates.
    """
    hdr = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "benchmarks", "cxl_mailbox.h",
    )
    try:
        with open(hdr) as f:
            decls = [
                l.rstrip() for l in f if f"uint32_t {field};" in l
            ]
    except OSError as e:
        print(f"fatal: {flag} slot drift-check cannot read {hdr}: {e}")
        sys.exit(1)
    if len(decls) != 1 or f"off {off}" not in decls[0]:
        print(
            f"fatal: {flag} slot offset drift: expected one "
            f"'uint32_t {field};' declaration carrying 'off {off}' in "
            f"benchmarks/cxl_mailbox.h, found {decls!r}. The gate would "
            f"silently hold the wrong bytes; re-sync the offset with "
            f"the struct."
        )
        sys.exit(1)


if args.read_block:
    _check_mailbox_slot("status", _RB_SLOT_OFF, "--read-block")
if args.dispatch_block:
    _check_mailbox_slot("command", _DB_SLOT_OFF, "--dispatch-block")
    if (len(_status_decls) != 1
            or f"off {_RB_SLOT_OFF}" not in _status_decls[0]):
        print(
            f"fatal: --read-block slot offset drift: expected one "
            f"'uint32_t status;' declaration carrying 'off "
            f"{_RB_SLOT_OFF}' in benchmarks/cxl_mailbox.h, found "
            f"{_status_decls!r}. The gate would silently hold the "
            f"wrong bytes; re-sync _RB_SLOT_OFF with the struct."
        )
        sys.exit(1)

# --cache-probe carve: 32 MiB at absolute 0x1_4000_0000, chosen clear of
# every other carve this config can emit (checked against this file's
# own constants, not remembered):
#   handoff   [0x1_0000_0000, 0x1_0010_0000)  (cxl_os start + 1 MiB)
#   held      [0x1_2000_0000, 0x1_2000_4000)  (DEFAULT; now settable via
#             --held-region-offset/--held-region-size, and deliberately
#             set to overlap the graph carve in the aligned configuration)
#   integrity [0x1_8000_0000, 0x2_FF00_0000)  (_host_cxl_os_end..full_end)
#   mailbox   [0x2_FF00_0000, 0x3_0000_0000)  (_CXL_MAILBOX_BASE + 16M)
# Probe carve [0x1_4000_0000, 0x1_4200_0000) touches none of them (the
# interlocks forbid those flags anyway; the clearance is for future
# composition). The probe itself maps and READS this range only.
_CACHE_PROBE_BASE = 0x140000000
_CACHE_PROBE_SIZE = toMemorySize("32MiB")
_cache_probe_cmd = (
    f"/home/cxl_benchmark/cache_probe "
    f"{_CACHE_PROBE_BASE:#x} {_CACHE_PROBE_SIZE:#x}"
)
# Completion echo, emitted by the guest AFTER the probe exits regardless
# of its status (';' sequencing), so the barrier terminates on failed
# probes too. Quote-split like _xfer_marker_echo so no script text ever
# contains the contiguous marker. The probe's own final "CACHE PROBE
# RESULT/ERROR" line lands in serial just before it and carries the
# verdict; the barrier cannot key on "CACHE PROBE" directly because the
# per-mode VERDICT lines print mid-probe and would end the run early.
_CACHE_PROBE_DONE = "CACHEPROBE_DONE"
_cache_probe_done_echo = "echo 'CACHEPROBE_''DONE'"

# Runtime-transfer marker. The HOST guest emits it over serial; the exit
# handler greps the serial file for it and performs the paused-instant
# transfer. ONE SOURCE OF TRUTH: _XFER_MARKER. Both the shell echo (the
# --runtime-transfer flow) and the MB_XFER_MARKER environment value (the
# --graph-transfer flow, where graph_walk_host.c prints the string it is
# handed and hardcodes nothing) are derived from it right here, so the C
# guest and the Python trigger cannot drift. Both derivations are
# QUOTE-SPLIT (same discipline as _kvm_marker_grep): adjacent quoted
# shell strings concatenate, so the script text never contains the
# contiguous marker -- only the executed echo, or the exported value,
# carries it. Distinct from every PASS/boot string the barriers key on.
_XFER_MARKER = "F2XFER_RELEASE_GO"
_XFER_SPLIT = 7  # len("F2XFER_"); keeps the emitted text byte-identical
_xfer_marker_sh = (
    f"'{_XFER_MARKER[:_XFER_SPLIT]}''{_XFER_MARKER[_XFER_SPLIT:]}'"
)
_xfer_marker_echo = f"echo {_xfer_marker_sh}"

# --graph-walk carve + command. Same base as the cache-probe carve (the
# two flags are mutually exclusive), sized from the graph parameters:
# header page + (N+1)*4 offsets (64B-aligned) + N*D*4 edges, rounded up
# to MiB for memmap=. The SEED is fixed here and travels to both
# executors through one command line and the in-region gw_header, which
# is what makes the two configs' walks identical.
_GW_BASE = 0x140000000
_GW_SEED = 42
if args.graph_walk:
    _gw_offs = (4096 + (args.graph_nodes + 1) * 4 + 63) & ~63
    _gw_bytes = _gw_offs + args.graph_nodes * args.graph_degree * 4
    _GW_CARVE = max(2 << 20, (_gw_bytes + (1 << 20) - 1) & ~((1 << 20) - 1))
    assert _GW_BASE + _GW_CARVE <= 0x180000000, (
        "graph carve would reach the integrity-carve region; shrink "
        "--graph-nodes/--graph-degree"
    )
    # --graph-transfer arms the guest through the environment (the
    # MB_POLL_US idiom): MB_XFER_MARKER both ENABLES the guest's
    # release signal and supplies the exact string the trigger greps
    # for, so there is nothing to keep in sync by hand. Absent the
    # flag no variables are exported and the command is byte-identical
    # to what it was.
    #
    # MB_POLL_US/MB_TIMEOUT_S are threaded unconditionally: this guest
    # reads both (its completion poll drives config 2's bracket), and
    # until now received neither, so --poll-us was silently ignored here
    # and the budget was whatever was compiled in. At the flag defaults
    # both values equal the compiled-in ones, so behaviour is unchanged.
    _gw_env = (
        f"MB_POLL_US={args.poll_us} MB_TIMEOUT_S={args.timeout_s} "
    )
    if args.graph_transfer:
        _gw_env += (
            f"MB_XFER_MARKER={_xfer_marker_sh} "
            f"MB_XFER_QUIESCE_US={args.graph_transfer_quiesce_us} "
        )
    _gw_cmd = (
        f"{_gw_env}/home/cxl_benchmark/graph_walk_host {args.graph_walk} "
        f"{_GW_BASE:#x} {_GW_CARVE:#x} {args.graph_nodes} "
        f"{args.graph_degree} {args.graph_steps} {_GW_SEED}"
    )
_GW_DONE = "GRAPHWALK_DONE"
_gw_done_echo = "echo 'GRAPHWALK_''DONE'"
_CXL_PROTECTED_SIZE = toMemorySize("2GiB")  # == device board's default carve

# --held-region geometry. The region must have an EXACT covering tree node.
# Counters attach at the tree's LEAF layer, so coverage is contiguous and the
# admissible shapes are the arity^k family: for arity 4 over the 2 GiB carve,
# a size of 16 KiB, 64 KiB, 256 KiB, 1 MiB, 4 MiB, 16 MiB, 64 MiB, 256 MiB or
# 1 GiB, each aligned to its OWN size (plus the whole 2 GiB range at node 0).
# Offset 0 is admissible; there is no lower bound on the offset. The verifier
# re-derives and enforces all of this at init(); any other region fatals.
# This 16 KiB region at offset 0x20000000 derives covering node 120149
# (= first leaf 87381 + 0x20000000/16KiB); it is kept where it was so the
# measurement stays comparable, not because lower offsets are unavailable.
_HELD_REGION_OFFSET = args.held_region_offset
_HELD_REGION_SIZE = toMemorySize(args.held_region_size)
_HELD_REGION_BASE = _CXL_WINDOW_BASE + _HELD_REGION_OFFSET

# --graph-walk + --held-region: the whole point of combining them is that
# the region whose authority the host RELEASES is the region the device
# then WALKS. A run where they are silently different memory produces a
# plausible number measuring nothing, so refuse at parse time. (The
# verifier separately enforces the region's own shape/containment at
# init(); this is the one relationship only the config can see.)
# True whenever a held-region GEOMETRY is in play -- statically populated
# (--held-region), released at runtime by its own flow
# (--runtime-transfer), or released at runtime by the graph-walk guest
# (--graph-transfer). Drives the containment check, the memmap= carve and
# the banner. It does NOT drive the verifiers' held_region_* params:
# those stay keyed on --held-region alone, so both runtime forms boot
# inert and the release happens after the guest has built the region.
_held_geometry_active = bool(
    args.held_region or args.runtime_transfer or args.graph_transfer
)

if args.graph_walk and _held_geometry_active:
    _gw_end = _GW_BASE + _GW_CARVE
    _held_end = _HELD_REGION_BASE + _HELD_REGION_SIZE
    if _GW_BASE < _HELD_REGION_BASE or _gw_end > _held_end:
        # Smallest admissible (arity^k) shape that would contain the graph.
        _adm = toMemorySize("16KiB")
        while _adm < _GW_CARVE:
            _adm *= 4
        parser.error(
            f"graph carve [{_GW_BASE:#x}..{_gw_end:#x}) is not inside the "
            f"held region [{_HELD_REGION_BASE:#x}..{_held_end:#x}). With "
            f"both configured the handed-off region must BE the region the "
            f"device walks. Align them, e.g. --held-region-offset "
            f"{_GW_BASE - _CXL_WINDOW_BASE:#x} --held-region-size "
            f"{_adm >> 20}MiB."
        )

# True when the held-region carve already covers the graph carve, so the
# graph block emits no second (nested, identical-type) memmap= entry.
_gw_carve_covered_by_held = bool(
    args.graph_walk
    and _held_geometry_active
    and _GW_BASE >= _HELD_REGION_BASE
    and _GW_BASE + _GW_CARVE <= _HELD_REGION_BASE + _HELD_REGION_SIZE
)

# (_XFER_MARKER and its derivations are defined above, before the
# graph-walk command that also consumes them.)

# Device memory hierarchy + clock, SINGLE-SOURCED so --host-like-device
# reads the device's real configuration instead of duplicating literals
# (the two cannot drift). Values are the Cortex-A72 mimicry (TRM): L1I
# 48kB 3-way, L1D 32kB 2-way, unified L2 1MB 16-way, 64B lines; the L2
# SIZE (A72 allows 512kB-4MB; 1MB is the BCM2711/Raspberry Pi 4 choice)
# and the 1.5GHz clock (BCM2711; the A72 has no default frequency) are
# implementation choices, not fixed A72 values. NOTE: the A72's L2 is
# SHARED across the cluster; PrivateL1PrivateL2 replicates it per core,
# structurally identical only at --device-cores 1.
_device_cache_params = dict(
    l1d_size="32kB",
    l1d_assoc=2,
    l1i_size="48kB",
    l1i_assoc=3,
    l2_size="1MB",
    l2_assoc=16,
)
_DEVICE_CLK = "1.5GHz"

# Both host_cache branches share the exact same cache geometry.
# Resized 2026-08: the previous 96MB/48-way L3 on a single-core host was
# not a realistic model and forced the CXL-miss working set past 192 MiB
# before the host missed to CXL, making timing-mode runs impractically
# long. This configuration is taken from a published single-core
# evaluation setup: 32kB/8 L1s, 2MB/16 L2, 16MB/32 L3. Total below the
# CXL link: 32K + 2M + 16M = ~18.03 MiB data-side.
_host_cache_params = dict(
    l1d_size="32kB",
    l1d_assoc=8,
    l1i_size="32kB",
    l1i_assoc=8,
    l2_size="2MB",
    l2_assoc=16,
    l3_size="16MB",
    l3_assoc=32,
)

if args.host_integrity:
    # Host-side verifier over the CXL window, CxlOnly. The range derivation
    # MIRRORS DeviceX86Board's default carve (device_x86_board.py) so both
    # verifiers hold IDENTICAL trees over IDENTICAL ranges:
    #   full = [base, base + window - 16MiB)   (mailbox excluded from full so
    #                                           it is neither protected nor
    #                                           metadata -> passes through)
    #   os   = [base, base + 2GiB)             (the protected region)
    #   integrity = [os_end, full_end)         (carved by the verifier ctor)
    # Same tree class/arity and metadata-cache shape as the device verifier
    # (device_x86_board.py defaults: TimingBmt, arity 4, 128KiB/8).
    _host_cxl_full_end = (
        _CXL_WINDOW_BASE + _CXL_WINDOW_SIZE - _CXL_MAILBOX_SIZE
    )
    _host_cxl_os_end = _CXL_WINDOW_BASE + _CXL_PROTECTED_SIZE
    assert _host_cxl_os_end < _host_cxl_full_end, (
        "host CXL integrity os range must fit below the metadata reserve "
        "(CXL window too small for the 2GiB carve)"
    )
    _host_cxl_integrity_full = [
        AddrRange(_CXL_WINDOW_BASE, _host_cxl_full_end)
    ]
    _host_cxl_integrity_os = [AddrRange(_CXL_WINDOW_BASE, _host_cxl_os_end)]
    host_cache = PrivateL1PrivateL2SharedL3IntegrityVerifierCacheHierarchy(
        **_host_cache_params,
        integrity_tree_type="TimingBmt",
        integrity_tree_arity=4,
        integrity_allocation_mode="CxlOnly",
        cxl_integrity_full_ranges=_host_cxl_integrity_full,
        cxl_integrity_os_ranges=_host_cxl_integrity_os,
        # --held-region: the HOST RELEASES the region (the device acquires
        # the same one below). Inert (size 0) unless the flag is set; the
        # role kwarg is ignored by the verifier while size == 0.
        held_region_start=_HELD_REGION_BASE if args.held_region else 0,
        held_region_size=_HELD_REGION_SIZE if args.held_region else 0,
        held_region_role="Releaser",
        metadata_cache_size="128KiB",
        metadata_cache_assoc=8,
    )
elif args.host_like_device:
    # ABLATION, not a new default: give the host EXACTLY the device's
    # hierarchy (same class, sizes, assocs, no L3 at all -- matching
    # the classes means losing the L3, not shrinking it), read from
    # _device_cache_params so the two cannot drift. Together with the
    # matched clock below, this removes the core/cache asymmetry so a
    # graph-walk comparison isolates what memory PLACEMENT alone buys.
    #
    # membus is passed EXPLICITLY: the class's `membus=` default is
    # evaluated once at class-definition time, so two instances built
    # with the default SHARE one SystemXBar -- the host board claims it
    # and the device board then fails elaboration with an orphaned,
    # membus-less hierarchy (the verifier hierarchy dodges the same
    # trap, "Fresh membus per instance"). Parameters stay single-
    # sourced; only the constructed OBJECTS are per-board.
    host_cache = PrivateL1PrivateL2CacheHierarchy(
        **_device_cache_params,
        membus=PrivateL1PrivateL2CacheHierarchy._get_default_membus(),
    )
else:
    host_cache = PrivateL1PrivateL2SharedL3CacheHierarchy(**_host_cache_params)

# Host CPU: TIMING by default, ATOMIC under --atomic, KVM under --dual-kvm.
# Under --kvm-boot: a switchable KVM->(--kvm-dest) pair. The KVM start cores
# and the switch cores share SimObject paths, and m5.switchCpus performs
# the takeover + per-System memory-mode change itself (m5/simulate.py,
# "Change the memory mode if required" -- it derives the mode from the
# incoming cores, so ATOMIC and TIMING destinations both work unchanged).
if args.kvm_boot:
    host_processor = SimpleSwitchableProcessor(
        starting_core_type=CPUTypes.KVM,
        switch_core_type=_kvm_switch_type,
        isa=ISA.X86,
        num_cores=1,
    )
else:
    host_processor = SimpleProcessor(
        cpu_type=_cpu_type,
        isa=ISA.X86,
        num_cores=1,
    )

host_board = X86Board(
    # --host-like-device (ablation): match the device clock too, so the
    # only remaining asymmetry is memory placement.
    clk_freq=_DEVICE_CLK if args.host_like_device else "2.4GHz",
    processor=host_processor,
    memory=host_memory,
    cache_hierarchy=host_cache,
    cxl_memory=host_cxl_memory,
    is_asic=(args.is_asic == "True"),
    enable_nmp=False,
    # --read-block: gates spliced between cxl_mem_bus and each CXL DRAM
    # channel controller. 0/0 (flag off) -> no gates, wiring identical.
    cxl_read_block_addr=_RB_SLOT_ADDR if args.read_block else 0,
    cxl_read_block_size=_RB_SLOT_SIZE if args.read_block else 0,
    # --dispatch-block: the mirror gate over the command word.
    cxl_dispatch_block_addr=_DB_SLOT_ADDR if args.dispatch_block else 0,
    cxl_dispatch_block_size=_DB_SLOT_SIZE if args.dispatch_block else 0,
    # --observe-cxl: observed range = the protected CXL OS carve. Chosen
    # over the held region because it is defined whenever integrity is
    # meaningful (with or without a handoff), it is literally "the
    # protected region" of the claim, and it is a SUPERSET of any held
    # region, so nothing observable is excluded. Cost is bounded: 2 GiB
    # / 64 B = 33,554,432 lines = one 4 MiB coverage bitmap.
    cxl_observe_addr=_CXL_WINDOW_BASE if args.observe_cxl else 0,
    cxl_observe_size=_CXL_PROTECTED_SIZE if args.observe_cxl else 0,
)

# --cxl-latency: retune the host's CXLBridge link-flight term after
# construction (params stay plain Python attrs until m5.instantiate).
# Flag absent -> nothing touched, x86_board.py's 50ns/12ns stand.
if args.cxl_latency is not None:
    host_board.bridge.bridge_lat = f"{_cxl_bridge_ns}ns"


# =============================================================================
# Recover the host's cxl_mem_bus and CXL range — to be shared with the
# device board's device_iobridge as the third master.
# =============================================================================
cxl_mem_bus = host_board.cxl_mem_bus
cxl_mem_range = AddrRange(
    0x100000000, size=host_board.get_cxl_memory().get_size()
)


# =============================================================================
# Device DeviceX86Board — same plumbing used by the standalone CXL
# access test, but pointed at the host's cxl_mem_bus instead of a
# private one
# =============================================================================
# Device memory hierarchy mimicking an ARM Cortex-A72 (TRM values): L1I
# 48kB 3-way, L1D 32kB 2-way, unified L2 1MB 16-way, 64B lines (the
# System-level cache_line_size default). The L2 SIZE (A72 allows
# 512kB-4MB; 1MB is the BCM2711/Raspberry Pi 4 configuration) and the
# 1.5GHz device clock below are implementation choices, not fixed A72
# values. CPU model and ISA are deliberately unchanged -- geometry and
# clock only. NOTE: the A72's L2 is SHARED across the cluster; this
# hierarchy replicates a private L2 per core, which is structurally
# identical only at --device-cores 1 (N cores get N private 1MB L2s).
device_cache = PrivateL1PrivateL2CacheHierarchy(**_device_cache_params)
if args.host_like_device:
    # Regression guard for the shared-default-membus trap (see the
    # host_cache ablation branch): same PARAMETERS, but the host and
    # device hierarchies must be distinct objects with distinct
    # membuses, or the second board to elaborate loses its bus.
    assert host_cache is not device_cache, (
        "host and device share one hierarchy instance"
    )
    assert host_cache.membus is not device_cache.membus, (
        "host and device hierarchies share one membus instance "
        "(class-default membus leaked; pass a fresh one explicitly)"
    )
device_memory = SingleChannelDDR3_1600(size="512MB")

# Device: TIMING-only from tick 0 (dual-KVM fallback documented in the
# module docstring). No switchable processor, no usePerf hack — those
# are KVM-specific concerns.
#
# DEVICE CORE COUNT — --device-cores N (default 2, the historical
# hardcoded value); one variable feeds BOTH branches so the KVM and
# non-KVM paths can never drift. The static plumbing scales correctly
# via get_num_cores(): the IntelMP table and apicbridge range in
# device_x86_board.py, and per-core L1/L2 in the cache hierarchy
# (proven through SMP bring-up by the 2026-07 dual-KVM runs — the old
# claim that multi-core KVM is foreclosed in two-System runs is
# obsolete). The DYNAMIC caveat is under KVM: a wait-for-SIPI AP is
# parked by tc->suspend() with nothing pending (fs_workload.cc:112-120),
# but Interrupts::requestInterrupt unconditionally calls cpu->wakeup()
# (interrupts.cc:271-273) and BaseKvmCPU::wakeup() activates any
# suspended thread — and unlike the simulated CPUs' INIT-microcode halt
# loop, a KVM core has no re-park path. A stray pre-SIPI interrupt
# therefore leaves the AP executing reset-vector garbage until the real
# INIT/SIPI (diagnosed 2026-07 on the nested-KVM machine). Until that
# is fixed, use --device-cores 1 for KVM boots that hit SMP bring-up
# hangs.
if args.kvm_boot:
    device_processor = SimpleSwitchableProcessor(
        starting_core_type=CPUTypes.KVM,
        # Same _kvm_switch_type as the host processor above -- never let
        # the two Systems' destinations drift apart.
        switch_core_type=_kvm_switch_type,
        isa=ISA.X86,
        num_cores=args.device_cores,
    )
else:
    device_processor = SimpleProcessor(
        cpu_type=_cpu_type,  # ATOMIC under --atomic; see _cpu_type above
        isa=ISA.X86,
        num_cores=args.device_cores,
    )

if args.kvm_no_perf:
    # Diagnostic fallback (see --kvm-no-perf help): drop the per-vCPU perf
    # counters so a perf_event_open permission failure can't masquerade as
    # the Attempt-A hang. usePerf defaults True (BaseKvmCPU.py:66); with it
    # False the KVM CPU paces itself by the host timer alone (the
    # usePerfOverflow default is False, so base.cc:103's fatal cannot fire).
    # get_cores() returns the CURRENT cores — under --kvm-boot those are the
    # KVM start cores (the ATOMIC switch cores have no usePerf param, so the
    # is_kvm_core guard matters there).
    for _core in (*host_processor.get_cores(), *device_processor.get_cores()):
        if _core.is_kvm_core():
            _core.get_simobject().usePerf = False

device_board = DeviceX86Board(
    # Cortex-A72 mimicry clock (single-sourced _DEVICE_CLK; rationale at
    # its definition). One SrcClockDomain for the whole board: cores,
    # caches, cxl_verifier, and cxl_metadata_cache share it.
    clk_freq=_DEVICE_CLK,
    processor=device_processor,
    memory=device_memory,
    cache_hierarchy=device_cache,
    cxl_mem_bus=cxl_mem_bus,
    cxl_mem_range=cxl_mem_range,
    # Phase 3 M1: optional device-side verifier on the CXL-ingress path.
    # Default off -> existing offload path unchanged. Ranges default inside
    # the board (CxlOnly: protect bottom 2 GiB, exclude top-16 MiB mailbox).
    cxl_integrity=args.device_integrity,
    # Phase 3 M2: optional range-keyed subtree handoff (the board computes the
    # handed-off region at the start of cxl_os and configures the verifier).
    cxl_handoff=args.device_handoff,
    # Held-region root state: the DEVICE ACQUIRES the region the host
    # releases (same region, opposite roles). Inert (0/0) unless
    # --held-region; the role kwarg is ignored while size == 0.
    cxl_held_region_start=_HELD_REGION_BASE if args.held_region else 0,
    cxl_held_region_size=_HELD_REGION_SIZE if args.held_region else 0,
    cxl_held_region_role="Acquirer",
)

if args.host_integrity and args.device_integrity:
    # Geometry-agreement guard. Identical (tree class, arity, os/full ranges)
    # is exactly what makes the two verifiers compute identical node indices
    # and identical metadata addresses for the same physical byte. The device
    # board derives its ranges internally; the host mirrors that derivation
    # above -- assert the mirror has not drifted.
    _dev_full = device_board._cxl_integrity_full_ranges
    _dev_os = device_board._cxl_integrity_os_ranges
    assert (
        len(_dev_full) == 1
        and int(_dev_full[0].start) == int(_host_cxl_integrity_full[0].start)
        and int(_dev_full[0].size()) == int(_host_cxl_integrity_full[0].size())
    ), "host/device CXL integrity FULL ranges have drifted apart"
    assert (
        len(_dev_os) == 1
        and int(_dev_os[0].start) == int(_host_cxl_integrity_os[0].start)
        and int(_dev_os[0].size()) == int(_host_cxl_integrity_os[0].size())
    ), "host/device CXL integrity OS ranges have drifted apart"
    assert (
        device_board._cxl_integrity_tree_type == "TimingBmt"
        and device_board._cxl_integrity_tree_arity == 4
    ), "host/device integrity tree class/arity have drifted apart"


# =============================================================================
# Workloads — distinct readfiles per System so each board's `m5 readfile`
# in the guest reads its own command stream.
# =============================================================================
KERNEL_PATH = "/home/alfi/CXL-NMP/fs_files/vmlinux_20240920"
DISK_PATH = "/home/alfi/CXL-NMP/fs_files/parsec.img"

# Default (smoke-test) mode: one-shot PASS + m5 exit, unchanged.
# Both Systems are TIMING from tick 0 — no leading `m5 exit;` (no switch).
host_cmd = (
    "echo '=== host: X86Board on TIMING ===';"
    + "echo 'host boot OK';"
    + "m5 exit;"
)
device_cmd = (
    "echo '=== device: DeviceX86Board on TIMING ===';"
    + "echo 'device boot OK';"
    + "m5 exit;"
)

# Checkpoint mode: print PASS, then PARK ALIVE in a minimal liveness
# loop. Attempt C (module docstring) showed that after a one-shot
# script ends, guest userspace dies and the last thread context
# suspends — a checkpoint of that state restores a dead guest.
#
# DELIBERATELY DUMB: just heartbeat + m5 exit + sleep. No readfile
# re-read, no cmp/cp. This run validates the checkpoint MECHANISM only
# (first 2-core SMP-TIMING boot, first two-System checkpoint, first
# save/restore over non-serialization-aware CXL objects); a smarter
# readfile-injection loop would entangle a fourth unproven mechanism
# with the restore path. CONSEQUENCE: this checkpoint cannot have new
# work injected at restore — the parked script is baked into guest
# memory and reads nothing. The workload-injection park loop comes in
# a LATER take-run (one more cold boot), once this mechanism is proven.
#
# The heartbeat doubles as the restore marker: a restored run starts
# in a fresh outdir with empty serial files, so the barrier must key
# on output generated POST-restore — which a periodic heartbeat is,
# within ~2 simulated seconds of resume.
_liveness_loop = (
    "while true; do " "echo 'host alive'; " "m5 exit; sleep 2; " "done"
)

# CXL sentinel (device side). The DEVICE sees CXL as a Reserved E820
# region, so /dev/mem access is permitted under STRICT_DEVMEM — the
# same mechanism the proven device_cxl_test binary uses (mmap there,
# dd here). Offset 64 KiB into the CXL range, matching that test's
# TEST_OFFSET. 0x100010000 = 4295032832.
#
# The device writes the sentinel ONCE post-boot, and every heartbeat
# re-reads it from CXL and prints it. Post-restore, device caches are
# cold (never serialized), so the read must traverse device_iobridge
# -> cxl_mem_bus -> DRAM: a true restored-content readback. The HOST
# path (CXLMemory::recvFunctional fix) is validated by host survival —
# the host kernel's own node-1 page tables are the sentinel there.
#
# ACCEPTED RISK: the host kernel owns this address as NUMA-node-1 RAM;
# 17 bytes here could clobber host data if that page is allocated.
# Boot-time node-1 allocations were observed near the TOP of the range
# (the restore-bug crash dump), so bottom+64KiB is very likely free,
# but unguaranteed until a proper shared-scratch carve-out exists.
# There is also no coherence between host caches and device-side CXL
# writes — harmless while the host is parked idle.
_CXL_SENTINEL = "CXLSENTINEL_F2_OK"  # 17 bytes, ASCII so serial shows it
_CXL_SENTINEL_ADDR = 4295032832  # 0x100010000
_write_sentinel = (
    f"printf '%s' '{_CXL_SENTINEL}' | "
    f"dd of=/dev/mem bs=1 seek={_CXL_SENTINEL_ADDR} conv=notrunc 2>/dev/null; "
)
_read_sentinel = (
    f"$(dd if=/dev/mem bs=1 skip={_CXL_SENTINEL_ADDR} "
    f"count={len(_CXL_SENTINEL)} 2>/dev/null)"
)
_device_loop = (
    "while true; do "
    f'echo "device alive CXL={_read_sentinel}"; '
    "m5 exit; sleep 2; "
    "done"
)
# --runtime-transfer (default/--atomic flows): host guest emits the
# transfer marker after its boot PASS, then m5 exit. The Terminal is
# unit-buffered, so the marker is in the serial file at that exit; the
# handler runs the trigger BEFORE its barrier check, so the transfer
# lands even if that exit is the run's last event. The --kvm-boot variant
# instead emits the marker in the phase-2 (post-switch) script, below.
# Nothing quiesces here beyond the boot-time memmap= carve: the host guest
# never touches the region, so the release precondition (no outstanding
# region packets) holds trivially.
if args.runtime_transfer and not args.kvm_boot:
    host_cmd = (
        "echo '=== host: X86Board (runtime-transfer) ===';"
        + "echo 'host boot OK';"
        + _xfer_marker_echo
        + ";m5 exit;"
    )

# --cache-probe (default TIMING flow): the host runs the probe, then the
# unconditional completion echo the barrier keys on. The device keeps
# the stock boot-PASS command. The --kvm-boot variant runs the probe in
# the phase-2 (post-switch) script instead, below.
if args.cache_probe and not args.kvm_boot:
    host_cmd = (
        "echo '=== host: X86Board (cache probe) ===';"
        + "echo 'host boot OK';"
        + _cache_probe_cmd + ";"
        + _cache_probe_done_echo + ";"
        + "m5 exit;"
    )

# --graph-walk (default TIMING flow): host builds+flushes+runs (config
# 1) or builds+flushes+dispatches (config 2); the unconditional done
# echo terminates the barrier either way. In config 2 the device runs
# device_offload, which waits on the doorbell and prints its
# every-exit-path "DEVICE OFFLOAD" prefix.
if args.graph_walk and not args.kvm_boot:
    host_cmd = (
        "echo '=== host: X86Board (graph walk) ===';"
        + "echo 'host boot OK';"
        + _gw_cmd + ";"
        + _gw_done_echo + ";"
        + "m5 exit;"
    )
    if args.graph_walk == "device":
        # MB_POLL_US threads --poll-us to the DEVICE's doorbell poll
        # too (device_offload.c reads it; default 1000 == its
        # compiled-in default). The device pickup latency sits inside
        # config 2's host-side bracket, so it must be tunable.
        device_cmd = (
            "echo 'device boot OK';"
            + f"MB_POLL_US={args.poll_us} "
            + f"MB_TIMEOUT_S={args.timeout_s} "
            + "/home/cxl_benchmark/device_offload;"
            + "m5 exit;"
        )

if args.take_checkpoint or args.restore:
    host_cmd = "echo 'host boot OK'; " + _liveness_loop
    device_cmd = "echo 'device boot OK'; " + _write_sentinel + _device_loop
    # In restore mode these contents are never read by the guests (the
    # parked script reads nothing); they are written only so the
    # config-time file plumbing is identical to the take-run.

# Offload mode (MVP host->device CXL dispatch). Each side runs its offload
# binary from the guest image. The programs rendezvous through the shared
# CXL mailbox (host arms + rings the doorbell, device polls + executes +
# returns a result); they self-synchronize, so host/device boot-order skew
# is harmless. Every exit path of each binary prints its
# "HOST OFFLOAD"/"DEVICE OFFLOAD" prefix, so the barrier (below) ends the
# run on failure (TIMEOUT/ERROR) as well as success. The host's memmap=
# carve-out is added to its kernel_args (below). Intended with --atomic.
if args.offload:
    if args.device_handoff:
        # The board computed the handed-off region (start of cxl_os). Thread its
        # base+size into the host guest so host_offload writes the OP_HANDOFF
        # descriptor AND places the XTEA operands inside the region (at
        # base+HANDOFF_OPS_OFF); the device prints the receipt, reads the
        # operands out of the protected region, and runs the blob. Verifier was
        # already configured with the same range at instantiation.
        _ho_base = device_board._cxl_handoff_start
        _ho_size = device_board._cxl_handoff_size
        # MB_POLL_US threads --poll-us into the guest (sh env-prefix
        # syntax); host_offload.c reads it at startup, 0 = busy-spin.
        _host_work = (
            f"MB_POLL_US={args.poll_us} MB_TIMEOUT_S={args.timeout_s} "
            f"/home/cxl_benchmark/host_offload handoff "
            f"{_ho_base:#x} {_ho_size};"
        )
    else:
        _host_work = (
            f"MB_POLL_US={args.poll_us} MB_TIMEOUT_S={args.timeout_s} "
            f"/home/cxl_benchmark/host_offload;"
        )
    _device_work = (
        f"MB_POLL_US={args.poll_us} MB_TIMEOUT_S={args.timeout_s} "
        f"/home/cxl_benchmark/device_offload;"
    )
    host_cmd = "echo 'host boot OK'; " + _host_work + " m5 exit;"
    device_cmd = "echo 'device boot OK'; " + _device_work + " m5 exit;"

# --kvm-boot: two-phase guest scripts. Phase 1 (the initial readfile) prints
# the boot PASS and PARKS in a heartbeat/poll loop; phase 2 (the workload) is
# injected by the handler at switch time by REWRITING the readfile —
# pseudo_inst::readfile re-opens the file per call (pseudo_inst.cc:376-384).
#
# Why the park loop (and not a one-shot `sleep 2; m5 exit`): (a) the
# early-booting System must wait an UNBOUNDED time for the late one, so no
# fixed number of extra exits suffices; (b) the loop's periodic m5 exits are
# what make the boot barrier immune to the KVM serial-drain race (the PASS
# string can land in the file after the exit event that followed it — the
# diagnosed --dual-kvm hang); (c) polling `m5 readfile` doubles as the
# release mechanism, so the workload provably starts only after the switch.
# This is the same parked-heartbeat pattern the checkpoint path validated.
#
# The grep pattern is quote-split so the phase-1 script does NOT itself
# contain the contiguous marker (else the poll would match its own script
# text and re-exec phase 1 as the workload).
_KVM_PHASE2_MARKER = "KVMBOOT_PHASE2_GO"
_kvm_marker_grep = 'KVMBOOT_"PHASE2"_GO'


def _kvm_phase1(pass_echo: str) -> str:
    return (
        f"echo '{pass_echo}'; "
        "while true; do "
        "m5 exit; "
        f"if m5 readfile | grep -q {_kvm_marker_grep}; then "
        "m5 readfile > /tmp/phase2.sh; sh /tmp/phase2.sh; break; "
        "fi; "
        "sleep 1; "
        "done"
    )


# Post-workload heartbeat: keeps exit events coming so the completion
# strings are also drain-race-immune (the barrier just needs one event
# after the strings land).
_KVM_PHASE2_TAIL = "while true; do m5 exit; sleep 2; done\n"

if args.kvm_boot:
    if args.offload:
        _host_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            f"echo 'host phase2 start ({args.kvm_dest.upper()})'\n"
            f"{_host_work}\n" + _KVM_PHASE2_TAIL
        )
        _device_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            f"echo 'device phase2 start ({args.kvm_dest.upper()})'\n"
            f"{_device_work}\n" + _KVM_PHASE2_TAIL
        )
    elif args.cache_probe:
        # Probe runs post-switch (under --kvm-dest timing this is the
        # timing-fidelity verdict). The completion echo follows the
        # probe unconditionally; the device's phase 2 is the stock
        # post-switch echo, which is its half of the barrier.
        _host_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'host phase2 start (cache probe)'\n"
            f"{_cache_probe_cmd}\n"
            f"{_cache_probe_done_echo}\n" + _KVM_PHASE2_TAIL
        )
        _device_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'device post-switch OK'\n" + _KVM_PHASE2_TAIL
        )
    elif args.graph_walk:
        # Walk (or dispatch) runs post-switch under the TIMING
        # destination the interlock enforces. Config 2's device phase 2
        # runs device_offload (doorbell consumer); config 1's is the
        # stock post-switch echo.
        _host_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'host phase2 start (graph walk)'\n"
            f"{_gw_cmd}\n"
            f"{_gw_done_echo}\n" + _KVM_PHASE2_TAIL
        )
        _dev_work_gw = (
            f"MB_POLL_US={args.poll_us} "
            f"MB_TIMEOUT_S={args.timeout_s} "
            "/home/cxl_benchmark/device_offload\n"
            if args.graph_walk == "device" else ""
        )
        _device_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'device post-switch OK'\n"
            + _dev_work_gw + _KVM_PHASE2_TAIL
        )
    else:
        # Plain --kvm-boot smoke: phase 2 just proves the switch landed and
        # the guests still execute post-switch. Under --runtime-transfer the
        # phase-2 host script also emits the transfer marker (quote-split,
        # so the script text never contains the contiguous marker): the
        # transfer then fires post-switch, under ATOMIC -- where no walk
        # occurs, so it proves the writer mechanics only, not the
        # predicates.
        _xfer_in_phase2 = (
            f"{_xfer_marker_echo}\n" if args.runtime_transfer else ""
        )
        _host_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'host post-switch OK'\n" + _xfer_in_phase2 + _KVM_PHASE2_TAIL
        )
        _device_phase2 = (
            f"# {_KVM_PHASE2_MARKER}\n"
            "echo 'device post-switch OK'\n" + _KVM_PHASE2_TAIL
        )
    host_cmd = _kvm_phase1("host boot OK")
    device_cmd = _kvm_phase1("device boot OK")

host_workload_kwargs = dict(
    kernel=KernelResource(local_path=KERNEL_PATH),
    disk_image=DiskImageResource(local_path=DISK_PATH),
    readfile=os.path.join(m5.options.outdir, "host_readfile"),
    readfile_contents=host_cmd,
)
_host_memmap_args = []
if args.offload:
    # Carve the top 16 MiB of the CXL window as Reserved on the HOST so
    # host_offload can mmap /dev/mem at the mailbox base (0x2ff000000) —
    # the host otherwise enrolls all of CXL as type-1 RAM, which
    # STRICT_DEVMEM blocks from /dev/mem. memmap= also keeps the host page
    # allocator out of it (no clobber). The device board is untouched: it
    # already sees the whole CXL window as Reserved. Reuses the board's own
    # default kernel args + the carve-out. Computed from the window
    # constants above; must match MB_BASE/MB_SIZE in benchmarks/cxl_mailbox.h
    # (for the 8 GiB window this is the historical "memmap=16M$0x2ff000000").
    _host_memmap_args.append(
        f"memmap={_CXL_MAILBOX_SIZE >> 20}M${_CXL_MAILBOX_BASE:#x}"
    )
    if args.device_handoff:
        # Second carve: the handed-off protected region at the BOTTOM of the
        # CXL window. The host enrolls the window as type-1 RAM, so without
        # this the region is host page-allocator memory and STRICT_DEVMEM
        # blocks /dev/mem there — host_offload could neither reach it nor
        # safely write operands into it. Reserved => mmappable + host kernel
        # keeps out (and the mapping is UC, atomic-safe, like the mailbox).
        _ho_base = device_board._cxl_handoff_start
        _ho_size = device_board._cxl_handoff_size
        assert (
            _ho_size % (1 << 20) == 0
        ), "handoff region size must be MiB-aligned for the memmap= carve"
        _host_memmap_args.append(f"memmap={_ho_size >> 20}M${_ho_base:#x}")
if args.host_integrity:
    # Reserve the host verifier's integrity carve so the host page allocator
    # never touches the metadata region: a stray guest access there is a
    # normal (non-metadata) packet inside integrityRanges and trips the
    # verifier's processReq assert. NOT mem= — mem= would unmap the whole
    # CXL window from the host guest. Derivation:
    #   integrity = [os_end, full_end)
    #             = [base + 2GiB, base + window - 16MiB)
    #   size      = window - 2GiB - 16MiB
    # (8 GiB window -> 6144 - 16 = 6128 MiB at 0x180000000.)
    _intg_base = _host_cxl_os_end
    _intg_size = _host_cxl_full_end - _host_cxl_os_end
    assert (
        _intg_size % (1 << 20) == 0
    ), "integrity carve size must be MiB-aligned for the memmap= carve"
    _host_memmap_args.append(f"memmap={_intg_size >> 20}M${_intg_base:#x}")
if _held_geometry_active:
    # Keep the host page allocator off the held/released region: the host
    # verifier panics -- by design -- on any walk into it once it is a
    # Releaser, so only a deliberate access (e.g. /dev/mem at the region
    # base, the release-invariant test) may ever reach it. Emitted at BOOT
    # in both modes (kernel args are fixed at boot) even though under
    # --runtime-transfer the release happens later. K-granularity memmap=
    # for sub-MiB regions (the default 16 KiB), M-granularity otherwise.
    #
    # When a --graph-walk carve nests inside this region (the aligned
    # configuration) this ONE carve serves both purposes: both are plain
    # Reserved ranges, and Reserved is exactly what the graph carve needs
    # too -- allocator kept out, /dev/mem-mmappable, and cacheable when
    # mapped without O_SYNC. The graph block below then emits nothing,
    # rather than nesting a second Reserved carve inside this one.
    assert _HELD_REGION_SIZE % (1 << 10) == 0
    if _HELD_REGION_SIZE % (1 << 20) == 0:
        _host_memmap_args.append(
            f"memmap={_HELD_REGION_SIZE >> 20}M${_HELD_REGION_BASE:#x}"
        )
    else:
        _host_memmap_args.append(
            f"memmap={_HELD_REGION_SIZE >> 10}K${_HELD_REGION_BASE:#x}"
        )
if args.cache_probe:
    # Dedicated Reserved carve for the cacheability probe: keeps the
    # host page allocator out of the probed range and makes it
    # /dev/mem-mmappable under STRICT_DEVMEM (the mailbox precedent).
    assert _CACHE_PROBE_SIZE % (1 << 20) == 0
    _host_memmap_args.append(
        f"memmap={_CACHE_PROBE_SIZE >> 20}M${_CACHE_PROBE_BASE:#x}"
    )
if args.graph_walk:
    # Graph region carve (host side; the device sees the whole window
    # Reserved already). Mapped WITHOUT O_SYNC by both guests ->
    # CACHEABLE (the measured cache_probe result) -- the premise of the
    # whole comparison. Config 2 additionally needs the mailbox carve
    # for dispatch. Skipped when the held-region carve above already
    # covers this range (the aligned configuration): same Reserved type,
    # same purpose, one entry in the guest's e820 instead of two nested.
    if not _gw_carve_covered_by_held:
        _host_memmap_args.append(
            f"memmap={_GW_CARVE >> 20}M${_GW_BASE:#x}"
        )
    if args.graph_walk == "device":
        _host_memmap_args.append(
            f"memmap={_CXL_MAILBOX_SIZE >> 20}M${_CXL_MAILBOX_BASE:#x}"
        )
if _host_memmap_args:
    host_workload_kwargs["kernel_args"] = (
        host_board.get_default_kernel_args() + _host_memmap_args
    )
if args.restore:
    # TwoSystemSimulator._instantiate consults ONLY the host board's
    # _checkpoint (its existing `if self._board._checkpoint:` branch).
    # m5.instantiate(dir) restores ALL SimObjects globally — including
    # everything under Root.systems — so the device board needs no
    # checkpoint reference of its own.
    host_workload_kwargs["checkpoint"] = Path(args.restore)
host_board.set_kernel_disk_workload(**host_workload_kwargs)
device_board.set_kernel_disk_workload(
    kernel=KernelResource(local_path=KERNEL_PATH),
    disk_image=DiskImageResource(local_path=DISK_PATH),
    readfile=os.path.join(m5.options.outdir, "device_readfile"),
    readfile_contents=device_cmd,
)


# =============================================================================
# Run
# =============================================================================
# Serial-output paths. The Terminal SimObject names its output file
# by SimObject path: host_board is attached as Root.board so its
# Pc.com_1.device lives at outdir/board.pc.com_1.device; device_board
# is attached via Root.systems (the VectorParam.System added to
# src/sim/Root.py) and gem5 names the vector's child file
# `systems.pc.com_1.device` (confirmed empirically — gem5 strips the
# index suffix when there's a single entry).
HOST_SERIAL = os.path.join(m5.options.outdir, "board.pc.com_1.device")
DEVICE_SERIAL = os.path.join(m5.options.outdir, "systems.pc.com_1.device")

# Restored runs key on the heartbeats (generated post-restore in the
# fresh outdir), NOT the boot-time PASS strings (printed pre-checkpoint
# into the take-run's outdir).
if args.restore:
    # Sentinel readback IS the restore success criterion (device path);
    # host survival + heartbeat validates the host functional-write path.
    PASS_HOST = "host alive"
    PASS_DEV = f"CXL={_CXL_SENTINEL}"
elif args.take_checkpoint:
    # Require a sentinel heartbeat BEFORE checkpointing, so a broken
    # sentinel write/read can never produce a poisoned checkpoint.
    PASS_HOST = "host boot OK"
    PASS_DEV = f"CXL={_CXL_SENTINEL}"
elif args.cache_probe:
    # Terminate on the guest's unconditional post-probe echo, NOT on the
    # probe's own "CACHE PROBE" prefix: the per-mode VERDICT lines print
    # mid-probe and a device heartbeat exit between them would end the
    # run before the second mode measured. The echo follows the probe
    # via ';' sequencing, so a failed/errored probe still terminates.
    PASS_HOST = _CACHE_PROBE_DONE
    PASS_DEV = (
        "device post-switch OK" if args.kvm_boot else "device boot OK"
    )
elif args.graph_walk:
    # Same unconditional-echo discipline. Config 2's device half keys
    # on device_offload's every-exit-path prefix; config 1's device is
    # a spectator and keys on its boot/post-switch echo.
    PASS_HOST = _GW_DONE
    if args.graph_walk == "device":
        PASS_DEV = "DEVICE OFFLOAD"
    else:
        PASS_DEV = (
            "device post-switch OK" if args.kvm_boot
            else "device boot OK"
        )
elif args.offload:
    # Both offload programs print their prefix on EVERY exit path
    # (OK/FAIL/TIMEOUT/ERROR), so the barrier ends the run on failure as
    # well as success — operator reads the actual status in serial.
    # (Also the phase-2 termination strings under --kvm-boot --offload.)
    PASS_HOST = "HOST OFFLOAD"
    PASS_DEV = "DEVICE OFFLOAD"
elif args.kvm_boot:
    # Plain --kvm-boot smoke: terminate on the phase-2 post-switch echoes
    # (the boot PASS strings only drive the SWITCH barrier in this mode).
    PASS_HOST, PASS_DEV = "host post-switch OK", "device post-switch OK"
else:
    PASS_HOST, PASS_DEV = "host boot OK", "device boot OK"

# --runtime-transfer trigger, shared by both handler flavors (None when
# the flag is off). Constructed here because it needs HOST_SERIAL and the
# board/hierarchy handles; the host verifier itself is dereferenced lazily
# inside the trigger (it is created during _pre_instantiate).
_transfer_trigger = None
# The trigger is a CAPABILITY, not a property of one flow: maybe_fire
# greps the serial file and is invoked from every handler activation, so
# it works for whichever guest emits the marker. --runtime-transfer's own
# script emits it; --graph-transfer has graph_walk_host.c emit it after
# the flush. Constructed identically for both.
if args.runtime_transfer or args.graph_transfer:
    _transfer_trigger = make_transfer_trigger(
        marker=_XFER_MARKER,
        host_serial_path=HOST_SERIAL,
        host_hierarchy=host_cache,
        device_board=device_board,
        base=_HELD_REGION_BASE,
        size=_HELD_REGION_SIZE,
    )

if args.kvm_boot:
    # Two-phase handler: boot barrier (switch BOTH + inject phase 2) then
    # workload barrier (terminate on PASS_HOST/PASS_DEV).
    _exit_handler = kvm_boot_barrier_handler(
        host_serial_path=HOST_SERIAL,
        device_serial_path=DEVICE_SERIAL,
        boot_host="host boot OK",
        boot_dev="device boot OK",
        done_host=PASS_HOST,
        done_dev=PASS_DEV,
        host_processor=host_processor,
        device_processor=device_processor,
        host_readfile_path=os.path.join(m5.options.outdir, "host_readfile"),
        device_readfile_path=os.path.join(
            m5.options.outdir, "device_readfile"
        ),
        host_phase2=_host_phase2,
        device_phase2=_device_phase2,
        transfer_trigger=_transfer_trigger,
        dest_label=args.kvm_dest.upper(),
    )
else:
    _exit_handler = serial_barrier_handler(
        host_serial_path=HOST_SERIAL,
        device_serial_path=DEVICE_SERIAL,
        host_pass=PASS_HOST,
        device_pass=PASS_DEV,
        checkpoint_dir=args.take_checkpoint,
        transfer_trigger=_transfer_trigger,
    )

simulator = TwoSystemSimulator(
    board=host_board,
    device_board=device_board,
    on_exit_event={
        ExitEvent.EXIT: _exit_handler,
    },
)

_cpu_label = (
    f"KVM->{args.kvm_dest.upper()}"
    if args.kvm_boot
    else "KVM"
    if args.dual_kvm
    else "ATOMIC"
    if args.atomic
    else "TIMING"
)
print("=" * 80)
print(f"Two-System smoke test: {_cpu_label}-only + serial-output barrier")
print("=" * 80)
_cpu_mode_desc = (
    "ATOMIC (dev-speed, no timing fidelity)" if args.atomic
    else _cpu_label
)
print(f"  CPU mode       : {_cpu_mode_desc}")
_wallclock_desc = (
    "~minutes cold boot (ATOMIC dev-speed)" if args.atomic
    else f"~minutes KVM boot, then workload under {args.kvm_dest.upper()}"
    if args.kvm_boot
    else "~minutes KVM boot" if args.dual_kvm
    else "both ~25-30 min cold boot (parallel under TIMING)"
)
print(
    f"  Host board     : X86Board  ({_cpu_label}-only)  with CXLNMPDevice etc."
)
print(
    f"  Device board   : DeviceX86Board  ({_cpu_label}-only)  + device_iobridge"
)
if args.host_integrity:
    print(
        f"  Host integrity : CxlOnly TimingBmt arity 4 -- protected "
        f"[{_CXL_WINDOW_BASE:#x}..{_host_cxl_os_end:#x}), integrity "
        f"[{_host_cxl_os_end:#x}..{_host_cxl_full_end:#x})"
    )
    print(
        f"  Host intg carve: memmap="
        f"{(_host_cxl_full_end - _host_cxl_os_end) >> 20}M"
        f"${_host_cxl_os_end:#x} (Reserved; keeps guest off the metadata)"
    )
if args.cache_probe:
    print(
        f"  Cache probe    : host runs cache_probe on Reserved carve "
        f"[{_CACHE_PROBE_BASE:#x}..{_CACHE_PROBE_BASE + _CACHE_PROBE_SIZE:#x})"
    )
    print(
        f"                   (memmap={_CACHE_PROBE_SIZE >> 20}M"
        f"${_CACHE_PROBE_BASE:#x}); grep host serial for 'CACHE PROBE' "
        f"(verdicts + RESULT); run ends on '{_CACHE_PROBE_DONE}'"
    )
_cxl_lat_total = (args.cxl_latency if args.cxl_latency is not None
                  else 50 + _CXL_BRIDGE_PROTO_NS + _CXL_CTRL_PROTO_NS)
_cxl_lat_bridge = (_cxl_bridge_ns if args.cxl_latency is not None else 50)
_cxl_lat_src = ("default, params untouched"
                if args.cxl_latency is None else "--cxl-latency override")
print(
    f"  CXL latency    : {_cxl_lat_total}ns one-way "
    f"(bridge_lat {_cxl_lat_bridge} + bridge proto "
    f"{_CXL_BRIDGE_PROTO_NS} + ctrl proto {_CXL_CTRL_PROTO_NS}; "
    f"{_cxl_lat_src}); device path untouched"
)
_host_hier_desc = (
    f"DEVICE-MATCHED (ablation: PrivateL1PrivateL2, no L3, "
    f"{_DEVICE_CLK})" if args.host_like_device
    else "stock SharedL3 @ 2.4GHz"
)
print(f"  Host hierarchy : {_host_hier_desc}")
if args.graph_walk:
    _gw_cfg = (
        "2 (device NMP)" if args.graph_walk == "device"
        else "1 (host CPU)"
    )
    print(
        f"  Graph walk     : config {_gw_cfg} -- "
        f"N={args.graph_nodes} D={args.graph_degree} "
        f"steps={args.graph_steps} seed={_GW_SEED}"
    )
    print(
        f"                   CSR {_gw_bytes >> 20} MiB in cacheable carve "
        f"[{_GW_BASE:#x}..{_GW_BASE + _GW_CARVE:#x}); grep host serial "
        f"for 'GRAPH WALK'; compare bracketed simTicks in stats.txt"
    )
    # Composition line: these runs get read months from now against
    # numbers in a paper, so the log must state what was instantiated.
    _gw_held_on = _held_geometry_active
    _gw_held_desc = (
        f"[{_HELD_REGION_BASE:#x}.."
        f"{_HELD_REGION_BASE + _HELD_REGION_SIZE:#x})"
        if _gw_held_on else "none"
    )
    print(
        f"  GW composition : host-integrity="
        f"{'ON' if args.host_integrity else 'off'} device-integrity="
        f"{'ON' if args.device_integrity else 'off'} "
        f"held-region={_gw_held_desc} read-block="
        f"{'armed' if args.read_block else 'off'}"
    )
    # Whether this run measured the ALIGNED configuration (the device
    # walks the very bytes whose authority it acquired) or the older
    # disjoint one. A log read months from now has to say which.
    if _gw_held_on:
        _gw_align = (
            "graph INSIDE held region -- device walks the region it "
            "acquired (ALIGNED)"
            if _gw_carve_covered_by_held
            else "graph DISJOINT from held region"
        )
    else:
        _gw_align = "no held region -- plain workload, no authority transfer"
    print(f"  GW alignment   : {_gw_align}")
    if args.graph_transfer:
        print(
            f"  GW transfer    : guest-driven runtime migration ON -- "
            f"quiesce {args.graph_transfer_quiesce_us}us, marker "
            f"'{_XFER_MARKER}', release BEFORE m5_reset_stats (outside "
            f"the bracket)"
        )
        print(
            f"                   expect one '[transfer] host RELEASED "
            f"then device ACQUIRED' line and covering node 37 from BOTH "
            f"verifiers, all before the device's first walk"
        )
    else:
        print(
            f"  GW transfer    : off -- verifiers (if any) keep the "
            f"global root; device walks climb to node 0"
        )
if args.observe_cxl:
    _obs_lines = _CXL_PROTECTED_SIZE // 64
    print(
        f"  CXL observer   : passive, spliced at S1 (CXLMemory."
        f"mem_req_port -> cxl_mem_bus); observing "
        f"[{_CXL_WINDOW_BASE:#x}.."
        f"{_CXL_WINDOW_BASE + _CXL_PROTECTED_SIZE:#x})"
    )
    print(
        f"                   {_obs_lines} lines of 64 B; forwards every "
        f"packet, acts on none, HOLDS NO COUNTER -- observability and "
        f"cost only, no correctness claim"
    )
if args.dispatch_block:
    print(
        f"  Dispatch-block : ReadBlockGate per CXL channel, slot "
        f"[{_DB_SLOT_ADDR:#x}..{_DB_SLOT_ADDR + _DB_SLOT_SIZE:#x}) "
        f"(mailbox command); the DEVICE's doorbell poll read is HELD "
        f"until the host's store arrives"
    )
    print(
        f"                   NOT dispatch in hardware -- the device "
        f"still issues the load; only the release TIMING moves to "
        f"hardware. Pickup becomes exact, not quantised"
    )
if args.read_block:
    print(
        f"  Read-block     : ReadBlockGate per CXL channel, slot "
        f"[{_RB_SLOT_ADDR:#x}..{_RB_SLOT_ADDR + _RB_SLOT_SIZE:#x}) "
        f"(mailbox status); host slot reads HELD until a device store"
    )
    print(
        f"                   arrives; watch each gate's init() inform() "
        f"line and stats group 'read_block_gate'"
    )
if args.offload or args.graph_walk:
    # Every flow with a poller gets the budget line; the period line is
    # offload-specific wording kept as it was.
    print(
        f"  Poll budget    : MB_TIMEOUT_S={args.timeout_s} s simulated "
        f"(time-equivalent; one value for all pollers)"
    )
if args.offload:
    print(
        f"  Poll period    : MB_POLL_US={args.poll_us} "
        f"({'busy-spin' if args.poll_us == 0 else 'usleep'}) threaded "
        f"into host_offload"
    )
if args.held_region:
    print(
        f"  Held region    : [{_HELD_REGION_BASE:#x}.."
        f"{_HELD_REGION_BASE + _HELD_REGION_SIZE:#x}) "
        f"(offset {_HELD_REGION_OFFSET:#x}) -- host=RELEASER, "
        f"device=ACQUIRER; covering node derived+printed at verifier init()"
    )
if args.runtime_transfer:
    print(
        f"  Runtime xfer   : on marker '{_XFER_MARKER}' in host serial -> "
        f"host RELEASES then device ACQUIRES"
    )
    print(
        f"                   [{_HELD_REGION_BASE:#x}.."
        f"{_HELD_REGION_BASE + _HELD_REGION_SIZE:#x}) in ONE paused "
        f"activation; watch for the '[transfer]' line and the two "
        f"verifier inform()s"
    )
print(f"  cxl_mem_bus    : host_board.cxl_mem_bus  (CXLMemBar, 3 masters)")
print(
    f"  CXL range      : 0x100000000, size {host_board.get_cxl_memory().get_size_str()}"
)
print(f"  Host readfile  : {os.path.join(m5.options.outdir, 'host_readfile')}")
print(
    f"  Dev  readfile  : {os.path.join(m5.options.outdir, 'device_readfile')}"
)
print(f"  Host serial    : {HOST_SERIAL}")
print(f"  Dev  serial    : {DEVICE_SERIAL}")
print(f"  Barrier        : sim ends when BOTH PASS strings appear in serial")
print(f"                   ('{PASS_HOST}' AND '{PASS_DEV}')")
print(
    f"  Wall-clock     : {_wallclock_desc}"
)
mode = (
    "take-checkpoint"
    if args.take_checkpoint
    else "restore"
    if args.restore
    else "offload"
    if args.offload
    else "dual-kvm boot experiment"
    if args.dual_kvm
    else "cache-probe"
    if args.cache_probe
    else f"graph-walk ({args.graph_walk})"
    if args.graph_walk
    else "smoke-test"
)
if args.kvm_boot:
    mode += f" (KVM boot -> switch both -> {args.kvm_dest.upper()} workload)"
print(f"  Mode           : {mode}")
if args.kvm_boot:
    print(f"  KVM boot       : both Systems boot under KVM (disjoint event")
    print(f"                   queues); guests park in heartbeat/poll loops.")
    print(f"                   Boot barrier ('host boot OK' AND 'device boot")
    print(
        f"                   OK') -> switch BOTH to "
        f"{args.kvm_dest.upper()} together ->"
    )
    print(f"                   phase-2 workload injected via readfile.")
    print(f"                   Terminates on '{PASS_HOST}' AND '{PASS_DEV}'.")
if args.dual_kvm:
    print(f"  Dual-KVM       : both Systems on KVM cores, event queues")
    print(
        f"                   renumbered disjoint (see [dual-kvm] line above)."
    )
    print(f"                   Success = both serials show kernel boot within")
    print(f"                   ~1 min and both PASS strings in ~2-5 min.")
    print(
        f"                   Attempt-A repro = serials still empty after ~3 min."
    )
if args.offload:
    print(
        f"  Offload        : host_offload -> CXL mailbox @ 0x2ff000000 -> device_offload"
    )
    print(
        f"  Host carve-out : memmap=16M$0x2ff000000 (Reserved, /dev/mem-mmappable)"
    )
    if args.device_handoff:
        _ho_base = device_board._cxl_handoff_start
        _ho_size = device_board._cxl_handoff_size
        print(
            f"  Handoff region : [{_ho_base:#x}..{_ho_base + _ho_size:#x}) "
            f"(protected; verifier re-roots)"
        )
        print(
            f"  Handoff carve  : memmap={_ho_size >> 20}M${_ho_base:#x} "
            f"(host Reserved; operands live at {_ho_base + 0x1000:#x})"
        )
        print(
            f"  Data binding   : blob in mailbox (control), XTEA operands in"
        )
        print(
            f"                   the handed-off PROTECTED region (data path);"
        )
        print(
            f"                   ciphertext match proves the device computed"
        )
        print(f"                   on data read out of the protected region.")
    print(
        f"  Success        : 'HOST OFFLOAD ... OK' AND 'DEVICE OFFLOAD done ...'"
    )
    print(f"  NOTE           : barrier also ends on failure — every exit path")
    print(
        f"                   prints HOST/DEVICE OFFLOAD (OK/FAIL/TIMEOUT/ERROR)."
    )
    print(
        f"                   Requires host_offload + device_offload installed"
    )
    print(
        f"                   in the guest image (benchmarks/Makefile install)."
    )
if args.take_checkpoint:
    print(f"  Checkpoint dir : {args.take_checkpoint}")
    print(f"  Barrier extra  : device must heartbeat 'CXL={_CXL_SENTINEL}'")
    print(f"                   BEFORE the checkpoint is written — a broken")
    print(f"                   sentinel write/read cannot poison the ckpt.")
    print(f"  NOTE           : full validation is the RESTORE run reading")
    print(f"                   the sentinel back from CXL DRAM (and the")
    print(f"                   host surviving, post recvFunctional fix).")
if args.restore:
    print(f"  Restoring from : {args.restore}")
    print(f"  Success        : 'host alive' AND 'CXL={_CXL_SENTINEL}' in")
    print(f"                   the FRESH outdir serial files")
    print(f"  NOTE           : validates restored CXL contents via the")
    print(f"                   device-path sentinel readback; the host")
    print(f"                   functional-write path is validated by host")
    print(f"                   survival (its node-1 page tables must have")
    print(f"                   round-tripped for it to run at all).")
print("=" * 80)

simulator.run()


def _gw_summary():
    """Post-run digest of the FIRST stats block (m5_reset_stats ->
    m5_dump_stats = the measurement bracket; the second block is
    bracket + tail because dump does not reset). Read from stats.txt so
    the numbers match exactly what offline analysis sees.

    Memory-stall caveat, stated precisely: TimingSimpleCPU exposes no
    memory-stall statistic. For this blocking in-order CPU (one
    outstanding access, no overlap) the total DEMAND-MISS latency below
    a cache level equals the CPU time stalled on those misses, so
    overallMissLatency::total / simTicks is an exact stall fraction for
    traffic below that level. It does NOT include L1-HIT service time
    or anything the CPU does between accesses -- that remainder is
    fetch + execute + hit-path stall.
    """
    import re

    path = os.path.join(m5.options.outdir, "stats.txt")
    try:
        with open(path) as f:
            text = f.read()
    except OSError as e:
        print(f"[gw-summary] cannot read {path}: {e}")
        return
    blocks = text.split("---------- Begin Simulation Statistics ----------")
    if len(blocks) < 2:
        print("[gw-summary] no stats blocks found")
        return
    blk = blocks[1]  # FIRST dump = the bracket

    def val(pattern):
        m = re.search(pattern, blk, re.M)
        return float(m.group(1)) if m else None

    sys_prefix = "board" if args.graph_walk == "host" else "systems"
    esc = re.escape(sys_prefix)

    def cache_stats(cache):
        # Single-element SimObjectVectors may or may not carry an index.
        base = rf"^{esc}\.cache_hierarchy\.{cache}0?\."
        return (
            val(base + r"overallMisses::total\s+(\d+)"),
            val(base + r"overallMissLatency::total\s+(\d+)"),
            val(base + r"overallAvgMissLatency::total\s+([\d.]+)"),
        )

    sim_ticks = val(r"^simTicks\s+(\d+)")
    if sim_ticks is None:
        print("[gw-summary] simTicks missing from first block")
        return

    print("=" * 72)
    print(f"[gw-summary] mode={args.graph_walk}  walking System: "
          f"{sys_prefix}  (FIRST stats block = the bracket)")
    print(f"[gw-summary] bracketed: {sim_ticks:.0f} ticks = "
          f"{sim_ticks / 1e9:.2f} ms simulated")

    levels = [("l1dcaches", "L1D"), ("l1icaches", "L1I"),
              ("l2caches", "L2")]
    if args.graph_walk == "host" and not args.host_like_device:
        levels.append(("l3cache", "L3"))
    l1d_lat = None
    l1i_lat = None
    for cache, label in levels:
        misses, lat, avg = cache_stats(cache)
        if misses is None:
            print(f"[gw-summary] {label:4s}: stats not found "
                  f"(naming drift -- check stats.txt by hand)")
            continue
        print(f"[gw-summary] {label:4s}: {misses:>10.0f} misses, "
              f"avg {avg / 1e3 if avg else 0:8.1f} ns below, "
              f"total {lat / 1e9:8.2f} ms")
        if cache == "l1dcaches":
            l1d_lat = lat
        if cache == "l1icaches":
            l1i_lat = lat

    # Committed inst/op counts for the System that ran the walk. Under
    # --kvm-boot BOTH core sets exist in stats.txt with the same leaf
    # names -- processor.start.core.* (the switched-out KVM core,
    # zeroed) and processor.switch.core.* (the TIMING core that did the
    # work) -- so a naive first-match hits the zeroed one. Real paths
    # read from m5out/gw-B2-symcore-h/stats.txt:
    #   board.processor.switch.core.commitStats0.numInsts
    # Non-switch runs have processor.cores*.core instead. Collect every
    # candidate and take the MAX (the active core; switched-out cores
    # report 0), printing which path was used.
    def _core_stat(leaf):
        cands = re.findall(
            rf"^({esc}\.processor\.(?:start|switch|cores\d*)\.core"
            rf"\.commitStats0\.{leaf})\s+(\d+)", blk, re.M)
        if not cands:
            return None, None
        path, v = max(cands, key=lambda c: int(c[1]))
        return path, int(v)

    _ipath, insts = _core_stat("numInsts")
    _, ops = _core_stat("numOps")
    if insts is None:
        print(f"[gw-summary] insts: n/a (no commitStats0.numInsts "
              f"under {sys_prefix}.processor.* in block 1)")
    else:
        print(f"[gw-summary] insts: {insts}  ops: {ops}  "
              f"(from {_ipath})")

    if l1d_lat is not None:
        frac = l1d_lat / sim_ticks
        print(f"[gw-summary] demand-miss stall below L1D: "
              f"{l1d_lat / 1e9:.2f} ms = {frac * 100:.1f}% of bracket "
              f"(exact for this blocking CPU; excludes L1-hit service "
              f"time)")
    if l1i_lat is not None and sim_ticks > 0:
        print(f"[gw-summary] ifetch-miss stall below L1I: "
              f"{l1i_lat / 1e9:.2f} ms = "
              f"{l1i_lat / sim_ticks * 100:.1f}% of bracket")
    if l1d_lat is not None:
        rest = sim_ticks - l1d_lat - (l1i_lat or 0)
        print(f"[gw-summary] remainder (fetch+execute+hit-path stall"
              f"{'+dispatch/poll' if args.graph_walk == 'device' else ''}"
              f"): {rest / 1e9:.2f} ms = "
              f"{rest / sim_ticks * 100:.1f}% of bracket")

    # Integrity walk depth, from the verifier of the System that walked.
    # This is the evidence that distinguishes an ACQUIRED device walk
    # (terminates at the region's covering node, ~9 metadata fetches per
    # chain) from a NON-acquired one (climbs to node 0, ~12) -- and, in a
    # --graph-transfer run, from a MIXED run where some walks started
    # before the acquire landed. The absolute counts are miss-filtered by
    # the metadata cache, so read the RATIO and compare it against the
    # same run without --graph-transfer; a transfer that did nothing
    # leaves it unchanged.
    _vpat = (rf"^{esc}\.(?:cxl_verifier|cache_hierarchy\.verifier)"
             r"\.integrity_verifier\.")
    md = val(_vpat + r"metadataReqHandled\s+(\d+)")
    dd = val(_vpat + r"dataReqHandled\s+(\d+)")
    if md is None or dd is None:
        print("[gw-summary] verifier: no integrity_verifier stats under "
              f"{sys_prefix} in block 1 (no verifier on the walking "
              "System, or naming drift)")
    else:
        print(f"[gw-summary] verifier: {dd:.0f} data reqs, {md:.0f} "
              f"metadata reqs, ratio {md / dd if dd else 0:.3f} "
              f"metadata/data (lower == walks terminating earlier; "
              f"compare across the --graph-transfer pair)")
    print("=" * 72)


def _observer_summary():
    """Post-run digest of the passive S1 observer, in the [gw-summary]
    idiom.

    Event counters are reset by m5_dump_reset_stats, so they are SUMMED
    across every block to give the run total. The coverage figure is
    different in kind: the bitmap is recomputed at each dump and never
    resets, so the LAST block already carries the cumulative value.

    The coverage figure is the point of the object: how many distinct
    protected lines had an observed data write-back, against how many
    lines the observed range holds. It says what is VISIBLE here. It
    says nothing about counter values -- the engine holds none.
    """
    import re

    path = os.path.join(m5.options.outdir, "stats.txt")
    try:
        with open(path) as f:
            text = f.read()
    except OSError as e:
        print(f"[observer] cannot read {path}: {e}")
        return
    blocks = text.split(
        "---------- Begin Simulation Statistics ----------"
    )[1:]
    if not blocks:
        print("[observer] no stats blocks found")
        return

    pre = r"^\S*\.cxl_observer\.cxl_traffic_observer\."

    def total(stat):
        s = 0.0
        found = False
        for b in blocks:
            m = re.search(pre + stat + r"\s+([\d.]+)", b, re.M)
            if m:
                s += float(m.group(1))
                found = True
        return s if found else None

    def last(stat):
        for b in reversed(blocks):
            m = re.search(pre + stat + r"\s+([\d.]+)", b, re.M)
            if m:
                return float(m.group(1))
        return None

    pkts = total("packetsObserved")
    if pkts is None:
        print("[observer] no cxl_traffic_observer stats found (not "
              "spliced, or naming drift)")
        return

    print("=" * 72)
    print(f"[observer] S1 passive observer -- {pkts:.0f} requests seen "
          f"on the timing path")
    if pkts == 0:
        print("[observer] ZERO packets observed. This is NOT a "
              "measurement of zero: the timing path never carried "
              "traffic here (KVM-only or atomic-only phase, or a "
              "splice off the host's CXL path).")
        print("=" * 72)
        return

    wbd = total("inWritebackDirty") or 0
    wbc = total("inWritebackClean") or 0
    wc = total("inWriteClean") or 0
    wo = total("inWritesOtherWithData") or 0
    ce = total("inCleanEvicts") or 0
    print(f"[observer] in-range write-backs: WritebackDirty {wbd:.0f}, "
          f"WritebackClean {wbc:.0f}, WriteClean {wc:.0f}, other "
          f"{wo:.0f}  (total {wbd + wbc + wc + wo:.0f})")
    print(f"[observer] in-range CleanEvict: {ce:.0f} -- carries NO "
          f"payload and is not a write; a write-keyed observer misses "
          f"these entirely")
    print(f"[observer] in-range reads {total('inReads') or 0:.0f}; "
          f"demand {total('inDemand') or 0:.0f} / prefetch "
          f"{total('inPrefetches') or 0:.0f}")
    print(f"[observer] verifier metadata (by tag): reads "
          f"{total('metadataReads') or 0:.0f}, writes "
          f"{total('metadataWrites') or 0:.0f}")
    print(f"[observer] out-of-range: reads {total('outReads') or 0:.0f}, "
          f"writes {total('outWritesWithData') or 0:.0f}, CleanEvict "
          f"{total('outCleanEvicts') or 0:.0f}")

    lo = last("linesObserved")
    lr = last("linesInRange")
    if lo is not None and lr:
        print(f"[observer] COVERAGE: {lo:.0f} distinct lines of "
              f"{lr:.0f} in the observed range had an observed "
              f"data-carrying write-back ({100.0 * lo / lr:.4f}%)")
        print(f"[observer] (cumulative for the run. This is what is "
              f"VISIBLE at S1 -- not a counter, and not a correctness "
              f"claim; the engine stores no counter values.)")
    print("=" * 72)


if args.graph_walk:
    _gw_summary()
if args.observe_cxl:
    _observer_summary()
