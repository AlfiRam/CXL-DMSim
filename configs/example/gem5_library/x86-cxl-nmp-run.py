# Copyright (c) 2021 The Regents of the University of California
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
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
NMP (Near-Memory Processor) CXL Configuration Script

This script configures CXL-DMSim to run experiments with Near-Memory Processing.
It allows comparing memory access latency between:
  - Host CPU accessing CXL memory remotely (baseline)
  - NMP CPU accessing CXL memory locally (experimental)

Usage
-----

Baseline (Host CPU accessing CXL memory):
```
build/X86/gem5.opt configs/example/gem5_library/x86-cxl-nmp-run.py --run-on host
```

NMP Experiment (NMP CPU accessing local memory):
```
build/X86/gem5.opt configs/example/gem5_library/x86-cxl-nmp-run.py --run-on nmp
```
"""

import argparse

import m5

from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_shared_l3_cache_hierarchy import (
    PrivateL1PrivateL2SharedL3CacheHierarchy,
)
from gem5.components.memory.single_channel import (
    DIMM_DDR5_4400,
    SingleChannelDDR4_3200,
)
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import (
    DiskImageResource,
    KernelResource,
)
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

# Requires X86 ISA and KVM support
requires(
    isa_required=ISA.X86,
    kvm_required=True,
)

# ============================================================================
# Argument Parsing
# ============================================================================
parser = argparse.ArgumentParser(
    description="CXL-DMSim NMP experiment configuration"
)

parser.add_argument(
    "--run-on",
    type=str,
    choices=["host", "nmp"],
    default="host",
    help=(
        "Choose execution target: "
        "'host' = Host CPU accesses CXL memory (baseline), "
        "'nmp' = NMP CPU at CXL device accesses local memory (experimental)"
    ),
)

parser.add_argument(
    "--nmp-binary",
    type=str,
    default="benchmarks/pointer_chase_nmp",
    help="Path to benchmark binary for NMP CPU execution",
)

parser.add_argument(
    "--is-asic",
    action="store",
    type=str,
    nargs="?",
    choices=["True", "False"],
    default="True",
    help="Simulate CXL ASIC Device (True) or FPGA Device (False)",
)

parser.add_argument(
    "--num-cpus",
    type=int,
    default=1,
    help="Number of host CPUs (for host execution mode)",
)

parser.add_argument(
    "--cpu-type",
    type=str,
    choices=["TIMING", "O3"],
    default="TIMING",
    help="CPU type for host execution (TIMING or O3)",
)

parser.add_argument(
    "--nmp-cpu-type",
    type=str,
    choices=["TimingSimpleCPU", "AtomicSimpleCPU", "MinorCPU"],
    default="TimingSimpleCPU",
    help="CPU type for NMP processor at CXL device",
)

parser.add_argument(
    "--test-cmd",
    type=str,
    default="lmbench_cxl.sh",
    help="Test command to run (only used in host mode)",
)

args = parser.parse_args()

# ============================================================================
# Cache Hierarchy Configuration
# ============================================================================
cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
    l1d_size="48kB",
    l1d_assoc=6,
    l1i_size="32kB",
    l1i_assoc=8,
    l2_size="2MB",
    l2_assoc=16,
    l3_size="96MB",  # Larger than 128MB benchmark array to force memory access
    l3_assoc=48,
)

# ============================================================================
# Memory Configuration
# ============================================================================
# Host local memory (NUMA Node 0)
memory = DIMM_DDR5_4400(size="3GB")

# CXL memory (NUMA Node 1)
if args.is_asic == "True":
    cxl_memory = DIMM_DDR5_4400(size="8GB")
else:
    cxl_memory = SingleChannelDDR4_3200(size="8GB")

# ============================================================================
# Processor Configuration
# ============================================================================
# Host CPU: KVM for fast boot, then switch to TIMING/O3 for measurement
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.O3 if args.cpu_type == "O3" else CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=args.num_cpus,
)

# Disable perf for KVM cores
for proc in processor.start:
    proc.core.usePerf = False

# ============================================================================
# Board Configuration
# ============================================================================
board = X86Board(
    clk_freq="2.4GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
    cxl_memory=cxl_memory,
    is_asic=(args.is_asic == "True"),
)

# ============================================================================
# NMP Configuration (if running in NMP mode)
# ============================================================================
if args.run_on == "nmp":
    print(f"[NMP Mode] Configuring Near-Memory Processor at CXL device")
    print(f"  - NMP CPU Type: {args.nmp_cpu_type}")
    print(f"  - NMP Binary: {args.nmp_binary}")
    print(f"  - NMP Start Address: 0x100000000 (4GB, beginning of CXL range)")

    # Import CPU classes for NMP instantiation
    from m5.objects import (
        X86ISA,
        X86MMU,
        AtomicSimpleCPU,
        MinorCPU,
        TimingSimpleCPU,
    )

    # Get the system object (needed for CPU creation)
    system = board.get_m5_system()

    # Create NMP CPU based on specified type
    if args.nmp_cpu_type == "TimingSimpleCPU":
        nmp_cpu = TimingSimpleCPU(cpu_id=100)  # ID 100+ for NMP CPUs
    elif args.nmp_cpu_type == "AtomicSimpleCPU":
        nmp_cpu = AtomicSimpleCPU(cpu_id=100)
    elif args.nmp_cpu_type == "MinorCPU":
        nmp_cpu = MinorCPU(cpu_id=100)
    else:
        raise ValueError(f"Unknown NMP CPU type: {args.nmp_cpu_type}")

    # Set up NMP CPU properties
    nmp_cpu.clk_domain = system.cpu_clk_domain  # Same clock as host
    nmp_cpu.switched_out = False
    nmp_cpu.workload = []  # Will load binary later

    # Create MMU for NMP CPU (required for memory management)
    nmp_cpu.mmu = X86MMU()

    # Create ISA for NMP CPU (x86)
    nmp_cpu.isa = [X86ISA() for _ in range(1)]  # 1 thread

    print(f"  - Created NMP CPU: {nmp_cpu.name}")

    # Enable NMP on the CXL device
    # Access path: board.pc.south_bridge.cxlmemory
    board.pc.south_bridge.cxlmemory.enable_nmp = True
    board.pc.south_bridge.cxlmemory.nmp_binary = args.nmp_binary
    board.pc.south_bridge.cxlmemory.nmp_start_addr = 0x100000000
    board.pc.south_bridge.cxlmemory.nmp_cpu_type = args.nmp_cpu_type

    # Register NMP CPU with CXL device
    board.pc.south_bridge.cxlmemory.setNMPCPU(nmp_cpu)

    print(f"  - NMP CPU registered with CXL device")

    # Connect NMP CPU ports to backend memory
    # NMP CPU's instruction and data ports connect to nmp_mem_port
    # which directly accesses backend memory (bypasses CXL protocol)
    # Note: This connection will be finalized in init() after system is instantiated

    print(f"  - NMP CPU configuration complete")
    print(f"  - NMP will access memory locally (bypassing CXL protocol)")
else:
    print(f"[Host Mode] Host CPU will access CXL memory remotely (baseline)")

# ============================================================================
# Workload Configuration
# ============================================================================
if args.run_on == "host":
    # Host mode: Run benchmark from host CPU via Linux
    command = (
        "m5 exit;"
        + "numactl -H;"
        + "m5 resetstats;"
        + f"/home/cxl_benchmark/{args.test_cmd};"
    )
else:
    # NMP mode: Boot minimal system, then trigger NMP execution
    # The NMP CPU will run independently once initialized
    command = (
        "m5 exit;"  # Switch from KVM to TIMING
        + "echo 'NMP CPU will execute benchmark independently';"
        + "m5 resetstats;"
        + "sleep 1;"  # Give NMP CPU time to execute
        + "m5 exit;"  # Exit after NMP completes
    )

# Set kernel and disk image
board.set_kernel_disk_workload(
    kernel=KernelResource(
        local_path="/home/malfiram/CXL-DMSim/fs_files/vmlinux_20240920"
    ),
    disk_image=DiskImageResource(
        local_path="/home/malfiram/CXL-DMSim/fs_files/parsec.img"
    ),
    readfile_contents=command,
)

# ============================================================================
# Simulator Setup
# ============================================================================
simulator = Simulator(
    board=board,
    on_exit_event={ExitEvent.EXIT: (func() for func in [processor.switch])},
)

# ============================================================================
# Run Simulation
# ============================================================================
print("=" * 70)
print(f"CXL-DMSim NMP Experiment")
print(f"Execution Mode: {args.run_on.upper()}")
print(f"CXL Device: {'ASIC' if args.is_asic == 'True' else 'FPGA'}")
if args.run_on == "host":
    print(f"Host CPU Type: {args.cpu_type}")
    print(f"Test Command: {args.test_cmd}")
else:
    print(f"NMP CPU Type: {args.nmp_cpu_type}")
    print(f"NMP Binary: {args.nmp_binary}")
print("=" * 70)

# ============================================================================
# NMP Initialization (if in NMP mode)
# ============================================================================
if args.run_on == "nmp":
    print("\n[NMP] Initializing Near-Memory Processor...")

    # Initialize NMP CPU at CXL device
    board.pc.south_bridge.cxlmemory.initNMPCPU()

    # Calculate stack pointer (top of CXL memory - 1MB for stack)
    cxl_mem_size = 8 * 1024 * 1024 * 1024  # 8GB
    cxl_mem_base = 0x100000000  # 4GB
    stack_size = 1 * 1024 * 1024  # 1MB stack
    stack_ptr = cxl_mem_base + cxl_mem_size - stack_size

    print(
        f"[NMP] Starting execution at PC=0x{args.nmp_start_addr:x}, SP=0x{stack_ptr:x}"
    )

    # Start NMP CPU execution
    # This sets up registers and activates the CPU
    board.pc.south_bridge.cxlmemory.startNMPExecution(
        startPC=0x100000000, stackPtr=stack_ptr  # Start of CXL memory
    )

    print("[NMP] Initialization complete\n")

m5.stats.reset()
simulator.run()

print("\n" + "=" * 70)
print("Simulation Complete!")
print(f"Results saved to: m5out/stats.txt")
print("=" * 70)

# ============================================================================
# Post-Simulation Analysis Instructions
# ============================================================================
if args.run_on == "nmp":
    print("\n[NMP Stats] Check the following in m5out/stats.txt:")
    print("  - board.pc.south_bridge.cxlmemory.nmpMemReads")
    print("  - board.pc.south_bridge.cxlmemory.nmpMemWrites")
    print("  - board.pc.south_bridge.cxlmemory.nmpAccessLatency")
    print("  - board.pc.south_bridge.cxlmemory.nmpActiveCycles")
    print("  - board.pc.south_bridge.cxlmemory.nmpExecutions")
else:
    print("\n[Host Stats] Check simSeconds in m5out/stats.txt")
    print("  Calculate: avg_latency = simSeconds / num_accesses")
