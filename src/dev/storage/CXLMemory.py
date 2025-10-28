from m5.objects.PciDevice import *
from m5.params import *


class CXLMemory(PciDevice):
    type = "CXLMemory"
    cxx_header = "dev/storage/cxl_memory.hh"
    cxx_class = "gem5::CXLMemory"

    cxl_rsp_port = ResponsePort(
        "This port sends responses to and receives requests from the Host"
    )
    mem_req_port = RequestPort(
        "This port sends requests to and receives responses from the back-end memory media"
    )
    nmp_mem_port = RequestPort(
        "NMP CPU memory port - direct access to backend memory (bypasses CXL controller)"
    )

    rsp_size = Param.Unsigned(48, "The number of responses to buffer")
    req_size = Param.Unsigned(48, "The number of requests to buffer")

    proto_proc_lat = Param.Latency(
        "15ns",
        "Latency of the CXL controller processing CXL.mem sub-protocol packets",
    )
    cxl_mem_range = Param.AddrRange(
        "2GB",
        "CXL expander memory range that can be identified as system memory",
    )

    # ========================================================================
    # Near-Memory Processor (NMP) Configuration
    # ========================================================================
    enable_nmp = Param.Bool(
        False,
        "Enable Near-Memory Processor at CXL device for local memory access",
    )

    nmp_binary = Param.String(
        "",
        "Path to binary executable to run on NMP CPU (e.g., pointer-chasing benchmark)",
    )

    nmp_start_addr = Param.Addr(
        0x100000000,
        "Physical address where NMP execution starts (default: 4GB, beginning of CXL memory range)",
    )

    nmp_cpu_type = Param.String(
        "TimingSimpleCPU",
        "Type of CPU to use for NMP (TimingSimpleCPU, AtomicSimpleCPU, or MinorCPU)",
    )

    VendorID = 0x8086
    DeviceID = 0x7890
    Command = 0x0
    Status = 0x280
    Revision = 0x0
    ClassCode = 0x05
    SubClassCode = 0x00
    ProgIF = 0x00
    InterruptLine = 0x1F
    InterruptPin = 0x01

    # Primary
    BAR0 = PciMemBar(size="2GB")
    BAR1 = PciMemUpperBar()
