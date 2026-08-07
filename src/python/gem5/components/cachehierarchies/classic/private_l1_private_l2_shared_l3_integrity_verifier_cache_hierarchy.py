# Copyright (c) 2024 CXL-NMP
# SPDX-License-Identifier: BSD-3-Clause
#
# Fresh, minimal integrity-verifier cache hierarchy for the host-to-host DRAM
# bring-up (Phase-2, step 3). It subclasses the stock
# PrivateL1PrivateL2SharedL3CacheHierarchy and overrides incorporate_cache() to
# splice an IntegrityVerifier between the shared L3 (LLC) and the memory bus,
# hanging a ClassicMetadataCache off the verifier's metadata ports.
#
# This is authored FRESH on purpose: the baseline's
# *_integrity_verifier hierarchy imports partition SimObjects
# (IntegrityPartitionManager, DataLocationPartitionManager, partitioning
# policies) at module top, which this port did NOT build. Importing it would
# ImportError at config-parse time. This file imports ONLY IntegrityVerifier
# and ClassicMetadataCache -- nothing partition-related, no PageSwapper.

from m5.objects import (
    AddrRange,
    IntegrityVerifier,
    L2XBar,
    L3XBar,
)
from m5.util.convert import toMemorySize

from ....isas import ISA
from ....utils.override import *
from ...boards.abstract_board import AbstractBoard
from ..abstract_cache_hierarchy import AbstractCacheHierarchy
from .caches.l1dcache import L1DCache
from .caches.l1icache import L1ICache
from .caches.l2cache import L2Cache
from .caches.l3cache import L3Cache
from .caches.metadata import ClassicMetadataCache
from .caches.mmu_cache import MMUCache
from .private_l1_private_l2_shared_l3_cache_hierarchy import (
    PrivateL1PrivateL2SharedL3CacheHierarchy,
)


class PrivateL1PrivateL2SharedL3IntegrityVerifierCacheHierarchy(
    PrivateL1PrivateL2SharedL3CacheHierarchy
):
    """
    Same topology as PrivateL1PrivateL2SharedL3CacheHierarchy, but with an
    IntegrityVerifier interposed on the path between the shared L3 and the
    memory bus:

        L3.mem_side -> verifier.cpu_side_port
        verifier.mem_side_port -> membus.cpu_side_ports
        verifier.metadata_req_port -> metadata_cache.cpu_side
        metadata_cache.mem_side -> verifier.metadata_resp_port

    The metadata cache hangs entirely off the verifier's two metadata ports; it
    does NOT touch the membus directly (the verifier is the only object that
    reaches the membus). Standard parallel fetch -- no ECC/single-fetch.
    """

    def __init__(
        self,
        l1d_size: str,
        l1i_size: str,
        l2_size: str,
        l3_size: str,
        l1d_assoc: int = 8,
        l1i_assoc: int = 8,
        l2_assoc: int = 16,
        l3_assoc: int = 16,
        integrity_tree_type: str = "TimingBmt",
        integrity_tree_arity: int = 4,
        integrity_allocation_mode: str = "DramOnly",
        integrity_reserve_size: str = "1GiB",
        cxl_integrity_full_ranges: "list | None" = None,
        cxl_integrity_os_ranges: "list | None" = None,
        held_region_start: int = 0,
        held_region_size: int = 0,
        held_region_role: str = "Acquirer",
        metadata_cache_size: str = "128KiB",
        metadata_cache_assoc: int = 8,
    ) -> None:
        """
        :param integrity_tree_type: "TimingBmt" (default, the BMT variant the
            real work targets) or "TimingTree".
        :param integrity_tree_arity: Tree arity (default 4).
        :param integrity_allocation_mode: "DramOnly" (default, host-to-host)
            or "CxlOnly" (host-side verifier over the CXL window; host DRAM
            goes UNPROTECTED -- an accepted modeling boundary).
        :param integrity_reserve_size: DramOnly ONLY. Bytes carved off the TOP
            of host DRAM to hold the integrity structure.
            dram_os_ranges = [0, full - reserve);
            dram_full_ranges = [0, full). MUST be large enough to hold the tree
            for the OS-visible data or the verifier init() fatals
            (treeSizeValid). See the config for the sizing rationale.
            Ignored under CxlOnly (the caller-supplied ranges carry the carve).
        :param cxl_integrity_full_ranges / os_ranges: CxlOnly ONLY. The
            caller-computed CXL range lists handed verbatim to the verifier
            (same kwargs and semantics as DeviceX86Board's
            cxl_integrity_full_ranges / cxl_integrity_os_ranges). The caller
            owns the derivation (window base/size, mailbox exclusion) so that
            a host and a device verifier can be given IDENTICAL ranges.
        :param held_region_start / size / role: held-region root state
            (node-keyed, N=1), TEMPORARY param-time population. size 0
            (default) = inert. role "Acquirer" (walk terminates at the
            region's covering tree node) or "Releaser" (a walk into the
            region panics). The verifier derives the covering node at init()
            and fatals if the region has no exact covering node.
        :param metadata_cache_size / assoc: the on-chip metadata cache.
        """
        # The two modes are mutually exclusive by construction: the verifier's
        # init() fatals unless it holds EXACTLY ONE protected OS range, so the
        # DRAM carve must be SUPPRESSED (not supplemented) under CxlOnly.
        if integrity_allocation_mode == "CxlOnly":
            assert cxl_integrity_full_ranges and cxl_integrity_os_ranges, (
                "CxlOnly requires explicit cxl_integrity_full_ranges and "
                "cxl_integrity_os_ranges"
            )
        else:
            assert integrity_allocation_mode == "DramOnly", (
                "integrity_allocation_mode must be 'DramOnly' or 'CxlOnly'; "
                f"got '{integrity_allocation_mode}'"
            )
            assert (
                cxl_integrity_full_ranges is None
                and cxl_integrity_os_ranges is None
            ), "cxl_integrity_*_ranges are only meaningful under CxlOnly"

        if held_region_size:
            assert held_region_role in ("Acquirer", "Releaser"), (
                "held_region_role must be 'Acquirer' or 'Releaser'; "
                f"got '{held_region_role}'"
            )

        # Fresh membus per instance (avoid the base class's shared default).
        super().__init__(
            l1d_size=l1d_size,
            l1i_size=l1i_size,
            l2_size=l2_size,
            l3_size=l3_size,
            l1d_assoc=l1d_assoc,
            l1i_assoc=l1i_assoc,
            l2_assoc=l2_assoc,
            l3_assoc=l3_assoc,
            membus=PrivateL1PrivateL2SharedL3CacheHierarchy._get_default_membus(),
        )
        self._integrity_tree_type = integrity_tree_type
        self._integrity_tree_arity = integrity_tree_arity
        self._integrity_allocation_mode = integrity_allocation_mode
        self._integrity_reserve_size = integrity_reserve_size
        self._cxl_integrity_full_ranges = cxl_integrity_full_ranges
        self._cxl_integrity_os_ranges = cxl_integrity_os_ranges
        self._held_region_start = held_region_start
        self._held_region_size = held_region_size
        self._held_region_role = held_region_role
        self._metadata_cache_size = metadata_cache_size
        self._metadata_cache_assoc = metadata_cache_assoc

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        # ---- Identical to the stock hierarchy up to the L3->membus hop ----
        board.connect_system_port(self.membus.cpu_side_ports)

        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports = port

        self.l1icaches = [
            L1ICache(
                size=self._l1i_size,
                assoc=self._l1i_assoc,
                writeback_clean=False,
            )
            for i in range(board.get_processor().get_num_cores())
        ]
        self.l1dcaches = [
            L1DCache(size=self._l1d_size, assoc=self._l1d_assoc)
            for i in range(board.get_processor().get_num_cores())
        ]
        self.l2buses = [
            L2XBar() for i in range(board.get_processor().get_num_cores())
        ]
        self.l2caches = [
            L2Cache(size=self._l2_size)
            for i in range(board.get_processor().get_num_cores())
        ]
        self.l3bus = L3XBar()
        self.l3cache = L3Cache(size=self._l3_size, assoc=self._l3_assoc)
        # ITLB Page walk caches
        self.iptw_caches = [
            MMUCache(size="256KiB", writeback_clean=False)
            for _ in range(board.get_processor().get_num_cores())
        ]
        # DTLB Page walk caches
        self.dptw_caches = [
            MMUCache(size="256KiB", writeback_clean=False)
            for _ in range(board.get_processor().get_num_cores())
        ]

        if board.has_coherent_io():
            self._setup_io_cache(board)

        for i, cpu in enumerate(board.get_processor().get_cores()):
            cpu.connect_icache(self.l1icaches[i].cpu_side)
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)

            self.l1icaches[i].mem_side = self.l2buses[i].cpu_side_ports
            self.l1dcaches[i].mem_side = self.l2buses[i].cpu_side_ports
            self.iptw_caches[i].mem_side = self.l2buses[i].cpu_side_ports
            self.dptw_caches[i].mem_side = self.l2buses[i].cpu_side_ports

            self.l2buses[i].mem_side_ports = self.l2caches[i].cpu_side
            self.l3bus.cpu_side_ports = self.l2caches[i].mem_side

            cpu.connect_walker_ports(
                self.iptw_caches[i].cpu_side, self.dptw_caches[i].cpu_side
            )

            if board.get_processor().get_isa() == ISA.X86:
                int_req_port = self.membus.mem_side_ports
                int_resp_port = self.membus.cpu_side_ports
                cpu.connect_interrupt(int_req_port, int_resp_port)
            else:
                cpu.connect_interrupt()

        self.l3bus.mem_side_ports = self.l3cache.cpu_side

        # ---- SPLICE: IntegrityVerifier between the L3 (LLC) and the membus ----
        # Stock hierarchy did: self.membus.cpu_side_ports = self.l3cache.mem_side
        self.verifier = IntegrityVerifier(
            integrity_tree_type=self._integrity_tree_type,
            integrity_tree_arity=self._integrity_tree_arity,
            integrity_allocation_mode=self._integrity_allocation_mode,
        )
        self.verifier.cpu_side_port = self.l3cache.mem_side
        self.membus.cpu_side_ports = self.verifier.mem_side_port

        if self._held_region_size:
            # Held-region root state (node-keyed, N=1): TEMPORARY param-time
            # population. The verifier derives the region's covering tree
            # node at init() and fatals if no exact covering node exists.
            self.verifier.held_region_start = self._held_region_start
            self.verifier.held_region_size = self._held_region_size
            self.verifier.held_region_role = self._held_region_role

        # Metadata cache hangs off the verifier's metadata ports only.
        self.metadata_cache = ClassicMetadataCache(
            size=self._metadata_cache_size,
            assoc=self._metadata_cache_assoc,
        )
        self.metadata_cache.cpu_side = self.verifier.metadata_req_port
        self.verifier.metadata_resp_port = self.metadata_cache.mem_side

        if self._integrity_allocation_mode == "CxlOnly":
            # ---- CXL-only carve (host verifier over the CXL window) ----
            # Assign ONLY the cxl_* range params; the dram_* params stay at
            # their empty defaults. Assigning both would hand the verifier two
            # protected OS ranges and trip its single-protected-range fatal at
            # init(). Host DRAM traffic then passes through the splice
            # unverified (needsVerification is false outside the ranges) --
            # the accepted modeling boundary for this mode.
            self.verifier.cxl_full_ranges = self._cxl_integrity_full_ranges
            self.verifier.cxl_os_ranges = self._cxl_integrity_os_ranges
        else:
            # ---- DRAM range carve-out (unchanged default behavior) ----
            # OS-visible range MUST be strictly smaller than the full range,
            # with the top `reserve` bytes left for the integrity structure;
            # otherwise the verifier init() fatals via
            # hasValidRanges()/treeSizeValid().
            # X86Board lays host DRAM out as a single contiguous [0, size).
            full_size = board.get_memory().get_size()
            reserve = toMemorySize(self._integrity_reserve_size)
            os_size = full_size - reserve
            assert (
                os_size > 0
            ), "integrity_reserve_size (%d) >= total DRAM (%d)" % (
                reserve,
                full_size,
            )
            self.verifier.dram_full_ranges = [AddrRange(full_size)]
            self.verifier.dram_os_ranges = [AddrRange(os_size)]
