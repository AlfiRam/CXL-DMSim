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


from typing import (
    List,
    Sequence,
)

from m5.objects import (
    Addr,
    AddrRange,
    BaseXBar,
    Bridge,
    CowDiskImage,
    CXLBridge,
    CXLMemBar,
    CxlTrafficObserver,
    IdeDisk,
    IOXBar,
    Pc,
    Port,
    RawDiskImage,
    ReadBlockGate,
    X86E820Entry,
    X86FsLinux,
    X86IntelMPBus,
    X86IntelMPBusHierarchy,
    X86IntelMPIOAPIC,
    X86IntelMPIOIntAssignment,
    X86IntelMPProcessor,
    X86SMBiosBiosInformation,
)
from m5.params import Latency
from m5.util.convert import toMemorySize

from ...isas import ISA
from ...resources.resource import AbstractResource
from ...utils.override import overrides
from ..cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
from ..memory.abstract_memory_system import AbstractMemorySystem
from ..processors.abstract_processor import AbstractProcessor
from .abstract_system_board import AbstractSystemBoard
from .kernel_disk_workload import KernelDiskWorkload


class X86Board(AbstractSystemBoard, KernelDiskWorkload):
    """
    A board capable of full system simulation for X86.

    **Limitations**
    * Currently, this board's memory is hardcoded to 3GB.
    * Much of the I/O subsystem is hard coded.
    """

    def __init__(
        self,
        clk_freq: str,
        processor: AbstractProcessor,
        memory: AbstractMemorySystem,
        cache_hierarchy: AbstractCacheHierarchy,
        cxl_memory: AbstractMemorySystem,
        is_asic: bool,
        enable_nmp: bool = False,
        # Read-blocking completion gate (ReadBlockGate): when
        # cxl_read_block_size > 0, one gate is spliced between
        # cxl_mem_bus and EACH CXL DRAM channel controller, holding
        # timing reads inside [cxl_read_block_addr, +size) until a
        # store to that slot arrives. Default 0/0 -> no gates, wiring
        # bit-identical.
        cxl_read_block_addr: int = 0,
        cxl_read_block_size: int = 0,
        # Mirror gate: holds the DEVICE's doorbell poll read until the
        # host's store to the same word arrives. Same class, same
        # position, a second instance chained per channel -- see the
        # splice below. 0/0 -> not instantiated.
        cxl_dispatch_block_addr: int = 0,
        cxl_dispatch_block_size: int = 0,
        # Passive traffic observer (CxlTrafficObserver): when
        # cxl_observe_size > 0, one instance is spliced at S1, between
        # CXLMemory.mem_req_port and cxl_mem_bus, where ALL host traffic
        # to CXL DRAM passes undivided by channel. It forwards every
        # packet and acts on none; it holds no counter. Default 0/0 ->
        # not instantiated, wiring bit-identical.
        cxl_observe_addr: int = 0,
        cxl_observe_size: int = 0,
    ) -> None:
        # Set NMP flag BEFORE super().__init__() so it's available during _setup_io_devices()
        # Use object.__setattr__() to bypass gem5's SimObject attribute checking
        # This creates a regular Python attribute, not a gem5 SimObject parameter
        object.__setattr__(self, "enable_nmp", enable_nmp)
        # Same pre-super() stash pattern as enable_nmp: consumed by
        # _setup_io_devices() during super().__init__().
        object.__setattr__(self, "_cxl_read_block_addr", cxl_read_block_addr)
        object.__setattr__(self, "_cxl_read_block_size", cxl_read_block_size)
        object.__setattr__(self, "_cxl_observe_addr", cxl_observe_addr)
        object.__setattr__(self, "_cxl_observe_size", cxl_observe_size)
        object.__setattr__(
            self, "_cxl_dispatch_block_addr", cxl_dispatch_block_addr
        )
        object.__setattr__(
            self, "_cxl_dispatch_block_size", cxl_dispatch_block_size
        )

        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
            cxl_memory=cxl_memory,
            is_asic=is_asic,
            # Note: enable_nmp is NOT passed to parent - it's X86Board-specific
        )

        if self.get_processor().get_isa() != ISA.X86:
            raise Exception(
                "The X86Board requires a processor using the X86 "
                f"ISA. Current processor ISA: '{processor.get_isa().name}'."
            )

    @overrides(AbstractSystemBoard)
    def _connect_things(self) -> None:
        """Override to add NMP bypass connection after cache hierarchy is incorporated."""
        # First, do the standard connection (memory, cache, processor)
        super()._connect_things()

        # Now that cache hierarchy is incorporated and membus exists, set up NMP bypass
        if self.enable_nmp:
            # NOTE: this bypass routes host membus traffic straight to
            # cxl_mem_bus, around the CXLMemory controller -- and so
            # around any observer spliced at S1. The two are mutually
            # exclusive in practice; f2 passes enable_nmp=False.
            # Direct connection: membus → cxl_mem_bus (bypass CXLBridge + CXLMemory)
            # cxl_mem_bus.cpu_side_ports is a VECTOR port - accepts multiple connections:
            # - Connection 1: CXLMemory.mem_req_port (Host path through CXL device)
            # - Connection 2: membus (NMP direct bypass path)
            self.cxl_mem_bus.cpu_side_ports = (
                self.get_cache_hierarchy().membus.mem_side_ports
            )

            print("=" * 80)
            print(
                "[NMP] Near-Memory Processing enabled - Direct membus bypass"
            )
            print(
                f"[NMP]   Host path: membus → CXLBridge(62ns) → CXLMemory(15ns) → cxl_mem_bus → DRAM"
            )
            print(f"[NMP]   NMP path:  membus → cxl_mem_bus → DRAM (DIRECT!)")
            print(f"[NMP]   Savings: ~77ns (bypasses CXLBridge + CXLMemory)")
            print(
                "[NMP]   Note: Both paths share same address space, routing via vector port"
            )
            print("=" * 80)

    @overrides(AbstractSystemBoard)
    def _setup_board(self) -> None:
        self.pc = Pc()

        self.workload = X86FsLinux()

        # North Bridge
        self.iobus = IOXBar()

        # Set up all of the I/O.
        self._setup_io_devices()

        self.m5ops_base = 0xFFFF0000

    def _setup_io_devices(self):
        """Sets up the x86 IO devices.

        .. note::

            This is mostly copy-paste from prior X86 FS setups. Some of it
            may not be documented and there may be bugs.
        """

        # Constants similar to x86_traits.hh
        IO_address_space_base = 0x8000000000000000
        pci_config_address_space_base = 0xC000000000000000
        interrupts_address_space_base = 0xA000000000000000
        APIC_range_size = 1 << 12

        # Setup memory system specific settings.
        if self.get_cache_hierarchy().is_ruby():
            self.pc.attachIO(
                self.get_io_bus(),
                [
                    self.pc.south_bridge.ide.dma,
                    self.pc.south_bridge.cxlmemory.dma,
                ],
            )
        else:
            # # Constants similar to x86_traits.hh
            IO_address_space_base = 0x8000000000000000
            pci_config_address_space_base = 0xC000000000000000
            interrupts_address_space_base = 0xA000000000000000
            APIC_range_size = 1 << 12

            # Configure CXL Device first to get address range
            cxl_mem_start = 0x100000000
            cxl_dram = self.get_cxl_memory()
            cxl_mem_range = AddrRange(
                Addr(cxl_mem_start), size=cxl_dram.get_size()
            )

            # Configure CXLBridge (Host CPU path: Core 0)
            self.bridge = CXLBridge(
                bridge_lat="50ns",
                proto_proc_lat="12ns",
                req_fifo_depth=128,
                resp_fifo_depth=128,
            )
            self.bridge.mem_side_port = self.get_io_bus().cpu_side_ports
            self.bridge.cpu_side_port = (
                self.get_cache_hierarchy().get_mem_side_port()
            )

            self.bridge.ranges = [
                AddrRange(0xC0000000, 0xFFFF0000),
                AddrRange(
                    IO_address_space_base, interrupts_address_space_base - 1
                ),
                AddrRange(pci_config_address_space_base, Addr.max),
            ]
            # Only add CXL memory range to bridge if NMP is disabled
            # When NMP is enabled, the direct membus connection handles CXL memory
            if not self.enable_nmp:
                self.bridge.ranges.append(cxl_mem_range)
            self.pc.south_bridge.cxlmemory.cxl_mem_range = cxl_mem_range
            cxl_dram.set_memory_range([cxl_mem_range])
            cxl_abstract_mems = []
            for mc in cxl_dram.get_memory_controllers():
                cxl_abstract_mems.append(mc.dram)
            self.memories.extend(cxl_abstract_mems)
            self.cxl_mem_bus = CXLMemBar()
            if self._cxl_observe_size:
                # S1 splice: CXLMemory.mem_req_port -> observer ->
                # cxl_mem_bus. Every host access to CXL DRAM funnels
                # through the controller's memory-side port, undivided
                # by channel, so ONE instance sees all of it and needs
                # no interleave arithmetic. It forwards verbatim and
                # acts on nothing; it holds no counter.
                #
                # CAVEAT, load-bearing: S1 is complete for host traffic
                # only while enable_nmp is False. With the NMP bypass on
                # (_connect_things above) the membus is wired straight
                # to cxl_mem_bus, and that traffic would route around
                # this splice entirely.
                self.cxl_observer = CxlTrafficObserver(
                    observe_addr=self._cxl_observe_addr,
                    observe_size=self._cxl_observe_size,
                )
                self.cxl_observer.cpu_side_port = (
                    self.pc.south_bridge.cxlmemory.mem_req_port
                )
                self.cxl_mem_bus.cpu_side_ports = (
                    self.cxl_observer.mem_side_port
                )
            else:
                self.cxl_mem_bus.cpu_side_ports = (
                    self.pc.south_bridge.cxlmemory.mem_req_port
                )
            # Connect NMP device memory port to cxl_mem_bus (DIRECT access - no CXL Bridge overhead)
            self.cxl_mem_bus.cpu_side_ports = (
                self.pc.south_bridge.nmp_device.mem_port
            )
            if self._cxl_read_block_size or self._cxl_dispatch_block_size:
                # Read-blocking gates: one per CXL DRAM channel per
                # gated slot, each handling only what its channel
                # carries. A slot's 64B line lives on exactly one
                # channel, so exactly one gate of each kind ever holds;
                # the others forward everything and report zero holds.
                # Per-channel splicing needs no Python-side interleave
                # arithmetic and survives a channel-count change.
                #
                # When BOTH are armed they are CHAINED per channel:
                #   bus -> completion gate -> dispatch gate -> MemCtrl
                # A second instance of the same class, rather than a
                # second slot inside one: the hold state, the N = 1
                # invariant and the retry logic then stay per-object,
                # so the two holds cannot interfere by construction
                # rather than by a keying discipline. Their slots are
                # disjoint 4-byte words (status at +72, command at +68)
                # so neither gate's store test can ever match the
                # other's word, and each forwards what it does not
                # act on with no added latency.
                _completion = []
                _dispatch = []
                for _, port in cxl_dram.get_mem_ports():
                    _downstream = port
                    if self._cxl_dispatch_block_size:
                        _dg = ReadBlockGate(
                            slot_addr=self._cxl_dispatch_block_addr,
                            slot_size=self._cxl_dispatch_block_size,
                            slot_label="dispatch/device-doorbell-poll",
                        )
                        _dg.mem_side_port = _downstream
                        _downstream = _dg.cpu_side_port
                        _dispatch.append(_dg)
                    if self._cxl_read_block_size:
                        _cg = ReadBlockGate(
                            slot_addr=self._cxl_read_block_addr,
                            slot_size=self._cxl_read_block_size,
                            slot_label="completion/host-status-poll",
                        )
                        _cg.mem_side_port = _downstream
                        _downstream = _cg.cpu_side_port
                        _completion.append(_cg)
                    self.cxl_mem_bus.mem_side_ports = _downstream
                if _completion:
                    self.cxl_read_block_gates = _completion
                if _dispatch:
                    self.cxl_dispatch_block_gates = _dispatch
            else:
                for _, port in cxl_dram.get_mem_ports():
                    self.cxl_mem_bus.mem_side_ports = port

            self.pc.south_bridge.cxlmemory.BAR0.size = cxl_dram.get_size_str()
            if self._is_asic:
                self.pc.south_bridge.cxlmemory.proto_proc_lat = Latency("15ns")
                self.pc.south_bridge.cxlmemory.rsp_size = 48
                self.pc.south_bridge.cxlmemory.req_size = 48
            else:
                self.pc.south_bridge.cxlmemory.proto_proc_lat = Latency("60ns")
                self.pc.south_bridge.cxlmemory.rsp_size = 36
                self.pc.south_bridge.cxlmemory.req_size = 36

            self.apicbridge = Bridge(delay="50ns")
            self.apicbridge.cpu_side_port = self.get_io_bus().mem_side_ports
            self.apicbridge.mem_side_port = (
                self.get_cache_hierarchy().get_cpu_side_port()
            )
            self.apicbridge.ranges = [
                AddrRange(
                    interrupts_address_space_base,
                    interrupts_address_space_base
                    + self.get_processor().get_num_cores() * APIC_range_size
                    - 1,
                )
            ]
            self.pc.attachIO(self.get_io_bus())

        # Add in a Bios information structure.
        self.workload.smbios_table.structures = [X86SMBiosBiosInformation()]

        # Set up the Intel MP table
        base_entries = []
        ext_entries = []
        for i in range(self.get_processor().get_num_cores()):
            bp = X86IntelMPProcessor(
                local_apic_id=i,
                local_apic_version=0x14,
                enable=True,
                bootstrap=(i == 0),
            )
            base_entries.append(bp)
        io_apic = X86IntelMPIOAPIC(
            id=self.get_processor().get_num_cores(),
            version=0x11,
            enable=True,
            address=0xFEC00000,
        )

        self.pc.south_bridge.io_apic.apic_id = io_apic.id
        base_entries.append(io_apic)
        pci_bus = X86IntelMPBus(bus_id=0, bus_type="PCI   ")
        base_entries.append(pci_bus)
        isa_bus = X86IntelMPBus(bus_id=1, bus_type="ISA   ")
        base_entries.append(isa_bus)
        connect_busses = X86IntelMPBusHierarchy(
            bus_id=1, subtractive_decode=True, parent_bus=0
        )
        ext_entries.append(connect_busses)

        pci_dev4_inta = X86IntelMPIOIntAssignment(
            interrupt_type="INT",
            polarity="ConformPolarity",
            trigger="ConformTrigger",
            source_bus_id=0,
            source_bus_irq=0 + (4 << 2),
            dest_io_apic_id=io_apic.id,
            dest_io_apic_intin=16,
        )

        base_entries.append(pci_dev4_inta)

        def assignISAInt(irq, apicPin):
            assign_8259_to_apic = X86IntelMPIOIntAssignment(
                interrupt_type="ExtInt",
                polarity="ConformPolarity",
                trigger="ConformTrigger",
                source_bus_id=1,
                source_bus_irq=irq,
                dest_io_apic_id=io_apic.id,
                dest_io_apic_intin=0,
            )
            base_entries.append(assign_8259_to_apic)

            assign_to_apic = X86IntelMPIOIntAssignment(
                interrupt_type="INT",
                polarity="ConformPolarity",
                trigger="ConformTrigger",
                source_bus_id=1,
                source_bus_irq=irq,
                dest_io_apic_id=io_apic.id,
                dest_io_apic_intin=apicPin,
            )
            base_entries.append(assign_to_apic)

        assignISAInt(0, 2)
        assignISAInt(1, 1)

        for i in range(3, 15):
            assignISAInt(i, i)

        self.workload.intel_mp_table.base_entries = base_entries
        self.workload.intel_mp_table.ext_entries = ext_entries

        entries = [
            # Mark the first megabyte of memory as reserved
            X86E820Entry(addr=0, size="639kB", range_type=1),
            X86E820Entry(addr=0x9FC00, size="385kB", range_type=2),
            # Mark the rest of physical memory as available
            X86E820Entry(
                addr=0x100000,
                size=f"{self.mem_ranges[0].size() - 0x100000:d}B",
                range_type=1,
            ),
        ]

        # Reserve the last 16kB of the 32-bit address space for m5ops
        entries.append(
            X86E820Entry(addr=0xFFFF0000, size="64kB", range_type=2)
        )

        entries.append(
            X86E820Entry(
                addr=0x100000000, size=f"{cxl_mem_range.size()}B", range_type=1
            )
        )

        self.workload.e820_table.entries = entries

    @overrides(AbstractSystemBoard)
    def has_io_bus(self) -> bool:
        return True

    @overrides(AbstractSystemBoard)
    def get_io_bus(self) -> BaseXBar:
        return self.iobus

    @overrides(AbstractSystemBoard)
    def has_dma_ports(self) -> bool:
        return True

    @overrides(AbstractSystemBoard)
    def get_dma_ports(self) -> Sequence[Port]:
        return [
            self.pc.south_bridge.ide.dma,
            self.iobus.mem_side_ports,
            self.pc.south_bridge.cxlmemory.dma,
        ]

    @overrides(AbstractSystemBoard)
    def has_coherent_io(self) -> bool:
        return True

    @overrides(AbstractSystemBoard)
    def get_mem_side_coherent_io_port(self) -> Port:
        return self.iobus.mem_side_ports

    @overrides(AbstractSystemBoard)
    def _setup_memory_ranges(self):
        memory = self.get_memory()

        if memory.get_size() > toMemorySize("3GB"):
            raise Exception(
                "X86Board currently only supports memory sizes up "
                "to 3GB because of the I/O hole."
            )
        data_range = AddrRange(memory.get_size())
        memory.set_memory_range([data_range])
        cpu_abstract_mems = []
        for mc in memory.get_memory_controllers():
            cpu_abstract_mems.append(mc.dram)
        self.memories = cpu_abstract_mems
        # Add the address range for the IO
        self.mem_ranges = [
            data_range,  # All data
            AddrRange(0xC0000000, size=0x100000),  # For I/0
        ]

    @overrides(KernelDiskWorkload)
    def get_disk_device(self):
        return "/dev/hda1"

    @overrides(KernelDiskWorkload)
    def _add_disk_to_board(self, disk_image: AbstractResource):
        ide_disk = IdeDisk()
        ide_disk.driveID = "device0"
        ide_disk.image = CowDiskImage(
            child=RawDiskImage(read_only=True), read_only=False
        )
        ide_disk.image.child.image_file = disk_image.get_local_path()

        # Attach the SimObject to the system.
        self.pc.south_bridge.ide.disks = [ide_disk]

    @overrides(KernelDiskWorkload)
    def get_default_kernel_args(self) -> List[str]:
        return [
            "earlyprintk=ttyS0",
            "console=ttyS0",
            "lpj=7999923",
            "root={root_value}",
            "disk_device={disk_device}",
        ]
