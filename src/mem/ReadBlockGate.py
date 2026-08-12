# Copyright (c) 2026 CXL-NMP
# SPDX-License-Identifier: BSD-3-Clause
#
# Read-blocking completion gate: an inline object for the
# cxl_mem_bus -> MemCtrl segment that HOLDS a timing read to one
# designated slot until a store to that slot arrives, then completes the
# held read with the stored value. General mechanism: it never inspects
# values and carries no mailbox semantics. N = 1: at most one held read.
#
# All other traffic -- other addresses, writes, flushes, and everything
# under atomic/functional access -- is forwarded verbatim. Address
# ranges pass through unchanged in both directions (the integrity
# verifier's splice precedent), so splicing the gate is invisible to
# crossbar routing.

from m5.objects.ClockedObject import ClockedObject
from m5.params import *
from m5.proxy import *  # Used for Parent.any


class ReadBlockGate(ClockedObject):
    type = "ReadBlockGate"
    cxx_header = "mem/read_block_gate.hh"
    cxx_class = "gem5::ReadBlockGate"

    cpu_side_port = ResponsePort(
        "Bus-facing port; receives requests and sends responses"
    )
    mem_side_port = RequestPort(
        "Memory-controller-facing port; sends requests and receives "
        "responses"
    )

    system = Param.System(Parent.any, "System that the gate belongs to.")

    # No default: forgetting to set the slot is a config error and must
    # fatal at instantiation rather than gate address zero.
    slot_addr = Param.Addr("Base address of the gated slot")
    slot_size = Param.Addr(4, "Size in bytes of the gated slot")

    release_latency = Param.Cycles(
        1,
        "Cycles between accepting a releasing store and completing the "
        "held read with its value.",
    )

    # Which side's wait this instance gates, for logs and panics only.
    # Two instances are chained on the same segment (one per slot); the
    # label is what makes their messages tellable apart.
    slot_label = Param.String(
        "slot", "Human-readable name of the gated slot, for messages"
    )

    # A held read consumes no iterations of the waiting guest's poll
    # loop, so neither its iteration budget nor its time-equivalent
    # deadline can bound the wait -- both are checked at loop
    # boundaries, and a held reader never reaches one. An unreleased
    # hold would therefore hang the run in silence. This deadline
    # converts that into a loud abort. Generous by default: a
    # legitimate wait is bounded by how long the other side takes to
    # build, flush and arm, which with integrity on can be seconds of
    # simulated time.
    hold_timeout = Param.Latency(
        "100s",
        "Maximum simulated time a read may be held before the run is "
        "aborted; 0 disables the deadline (not recommended).",
    )
