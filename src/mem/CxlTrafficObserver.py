# Copyright (c) 2026 CXL-NMP
# SPDX-License-Identifier: BSD-3-Clause
#
# Passive inline traffic observer for the CXL controller's memory-side
# port (S1: CXLMemory.mem_req_port -> cxl_mem_bus).
#
# IT HOLDS NO COUNTER. This object exists to answer an OBSERVABILITY and
# COST question -- which host traffic to the protected region crosses
# this point, and what an inline object there costs -- and nothing else.
# It stores no value that could stand in for an encryption counter, it
# never computes or compares one, and nothing it holds is readable by
# any other SimObject. See the header comment in cxl_traffic_observer.hh
# for the full statement of what it deliberately does not do.

from m5.objects.ClockedObject import ClockedObject
from m5.params import *
from m5.proxy import *  # Used for Parent.any


class CxlTrafficObserver(ClockedObject):
    type = "CxlTrafficObserver"
    cxx_header = "mem/cxl_traffic_observer.hh"
    cxx_class = "gem5::CxlTrafficObserver"

    cpu_side_port = ResponsePort(
        "Controller-facing port; receives requests, sends responses"
    )
    mem_side_port = RequestPort(
        "Bus-facing port; sends requests, receives responses"
    )

    system = Param.System(Parent.any, "System that the observer belongs to.")

    # The range whose traffic is classified as "protected". No default:
    # an unset range would silently classify everything as out-of-range,
    # which is the failure this object exists to avoid.
    observe_addr = Param.Addr("Base of the observed (protected) range")
    observe_size = Param.Addr("Size in bytes of the observed range")

    # Line granularity for the distinct-line coverage bitmap. One
    # SATURATING BIT per line -- set-membership, never a magnitude.
    line_size = Param.Unsigned(64, "Line granularity for coverage")
