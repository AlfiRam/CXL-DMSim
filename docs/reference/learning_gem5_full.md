# Learning gem5 — Full Documentation Corpus

Source: https://www.gem5.org/documentation/learning_gem5/  (repo: github.com/gem5/website)
Compiled for offline / LLM context use. Sections follow the site's left-nav order.

---

## Table of Contents

- **Introduction**
  - Learning gem5
- **Getting Started**
  - Building gem5
  - Creating a simple configuration script
  - Adding cache to configuration script
  - Understanding gem5 statistics and output
  - Using the default configuration scripts
  - Extending gem5 for ARM
- **Modifying / Extending gem5**
  - Setting up your development environment
  - Creating a very simple SimObject
  - Debugging gem5
  - Event-driven programming
  - Adding parameters to SimObjects and more events
  - Creating SimObjects in the memory system
  - Creating a simple cache object
  - ARM Power Modelling
  - ARM DVFS Support
- **Modeling Cache Coherence with Ruby**
  - Introduction to Ruby
  - MSI example cache protocol
  - Declaring a state machine
  - In port code blocks
  - Action code blocks
  - Transition code blocks
  - MSI Directory implementation
  - Compiling a SLICC protocol
  - Configuring a simple Ruby system
  - Running the simple Ruby system
  - Debugging SLICC Protocols
  - Configuring for a standard protocol
- **gem5 101**
  - gem5 101
  - Homework 1 for CS 752
  - Homework 2 for CS 752
  - Homework 3 for CS 752
  - Homework 4 for CS 752
  - Homework 5 for CS 752
  - Homework 6 - Programming multi-core

---


# ═══ Introduction ═══


## Learning gem5

*Source: https://www.gem5.org/documentation/learning_gem5/introduction/*

# Introduction

The goal of this document is to give you a thorough
introduction on how to use gem5 and the gem5 codebase. The purpose of
this document is not to provide a detailed description of every feature
in gem5. After reading this document, you should feel comfortable using
gem5 in the classroom and for computer architecture research.
Additionally, you should be able to modify and extend gem5 and then
contribute your improvements to the main gem5 repository.

This document is colored by my personal experiences with gem5 over the
past six years as a graduate student at the University of
Wisconsin-Madison. The examples presented are just one way to do it.
Unlike Python, whose mantra is "There should be one-- and preferably
only one --obvious way to do it." (from The Zen of Python. See
[The Zen of Python](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python){:target="_blank"}), in gem5 there are a number of different ways to
accomplish the same thing. Thus, many of the examples presented in this
book are my opinion of the best way to do things.

One important lesson I have learned (the hard way) is when using complex
tools like gem5, it is important to actually understand how it works
before using it.

You can find the source for this book at
<https://github.com/gem5/website/tree/stable/_pages/documentation/learning_gem5/>.

## What is gem5?

gem5 is a modular discrete event driven computer system simulator platform. That means that:

1. gem5's components can be rearranged, parameterized, extended or replaced easily to suit your needs.
2. It simulates the passing of time as a series of discrete events.
3. Its intended use is to simulate one or more computer systems in various ways.
4. It's more than just a simulator; it's a simulator platform that lets you use as many of its premade components as you want to build up your own simulation system.

gem5 is written primarily in C++ and python and most components are provided under a BSD style license.
It can simulate a complete system with devices and an operating system in full system mode (FS mode), or user space only programs where system services are provided directly by the simulator in syscall emulation mode (SE mode).
There are varying levels of support for executing Alpha, ARM, MIPS, Power, SPARC, RISC-V, and 64 bit x86 binaries on CPU models including two simple single CPI models, an out of order model, and an in order pipelined model.
A memory system can be flexibly built out of caches and crossbars or the Ruby simulator which provides even more flexible memory system modeling.

There are many components and features not mentioned here, but from just this partial list it should be obvious that gem5 is a sophisticated and capable simulation platform.
Even with all gem5 can do today, active development continues through the support of individuals and some companies, and new features are added and existing features improved on a regular basis.

## Capabilities out of the box
gem5 is designed for use in computer architecture research, but if you're trying to research something new and novel it probably won't be able to evaluate your idea out of the box. If it could, that probably means someone has already evaluated a similar idea and published about it.

To get the most out of gem5, you'll most likely need to add new capabilities specific to your project's goals. gem5's modular design should help you make modifications without having to understand every part of the simulator.

As you add the new features you need, please consider contributing your changes back to gem5. That way others can take advantage of your hard work, and gem5 can become an even better simulator.

## Asking for help
Please visit our [Ask a question](/ask-a-question) page.

Before reporting a problem, please read [Reporting Problems](/documentation/reporting_problems).


---


# ═══ Getting Started ═══


## Building gem5

*Source: https://www.gem5.org/documentation/learning_gem5/part1/building/*

Building gem5
=============

This chapter covers the details of how to set up a gem5 development
environment and build gem5.

If you have a pre-built binary
-----------------------------

If you are running gem5 using a pre-built binary, you can skip this section.
The pre-built binary uses the ALL build and can be used to run all ISAs and all Ruby coherence protocols.

Requirements for gem5
---------------------

See [gem5 requirements](http://www.gem5.org/documentation/general_docs/building#dependencies) for more details.

On Ubuntu, you can install all of the required dependencies with the
following command. The requirements are detailed below.

```bash
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python-dev python
```

1. git ([Git](https://git-scm.com/)):
    :   The gem5 project uses [Git](https://git-scm.com/) for version
        control. [Git](https://git-scm.com/) is a distributed version
        control system. More information about
        [Git](https://git-scm.com/) can be found by following the link.
        Git should be installed by default on most platforms. However,
        to install Git in Ubuntu use

    ```bash
    sudo apt install git
    ```

2. gcc 10+
    :   You may need to use environment variables to point to a
        non-default version of gcc.

        On Ubuntu, you can install a development environment with

        ```bash
        sudo apt install build-essential
        ```

       **We support GCC Versions >=10, up to GCC 13**

3.  [SCons 3.0+](http://www.scons.org/)
    :   gem5 uses SCons as its build environment. SCons is like make on
        steroids and uses Python scripts for all aspects of the build
        process. This allows for a very flexible (if slow) build system.

        To get SCons on Ubuntu use

    ```bash
    sudo apt install scons
    ```

4.  Python 3.6+
    :   gem5 relies on the Python development libraries. To install
        these on Ubuntu use

    ```bash
    sudo apt install python3-dev
    ```

5.  [protobuf](https://developers.google.com/protocol-buffers/) 2.1+ (**Optional**)
    :   "Protocol buffers are a language-neutral, platform-neutral
        extensible mechanism for serializing structured data." In gem5,
        the [protobuf](https://developers.google.com/protocol-buffers/)
        library is used for trace generation and playback.
        [protobuf](https://developers.google.com/protocol-buffers/) is
        not a required package, unless you plan on using it for trace
        generation and playback.

    ```bash
    sudo apt install libprotobuf-dev protobuf-compiler libgoogle-perftools-dev
    ```

6. [Boost](https://www.boost.org/) (**Optional**)
    :   The Boost library is a set of general purpose C++ libraries. It is a
        necessary dependency if you wish to use the SystemC implementation.
        ```
        sudo apt install libboost-all-dev
        ```

Getting the code
----------------

Change directories to where you want to download the gem5 source. Then,
to clone the repository, use the `git clone` command.

```bash
git clone https://github.com/gem5/gem5
```

You can now change directories to `gem5` which contains all of the gem5
code.

Your first gem5 build
---------------------

Let's start by building a basic x86 system. As of gem5 v22.1, you can
compile the ALL build, which includes all ISAs. As of gem5 v24.1, the
ALL build also includes all Ruby cache coherence protocols. This is
relevant if you are using the ruby-intro-chapter.

To build gem5, we will use SCons. SCons uses the SConstruct file
(`gem5/SConstruct`) to set up a number of variables and then uses the
SConscript file in every subdirectory to find and compile all of the
gem5 source.

SCons automatically creates a `gem5/build` directory when first
executed. In this directory you'll find the files generated by SCons,
the compiler, etc. There will be a separate directory for each set of
options (ISA and cache coherence protocol) that you use to compile gem5.

There are a number of default compilations options in the `build_opts`
directory. These files specify the parameters used to build gem5 which have
non-default values. We'll use the ALL defaults. You can look at the file
`build_opts/ALL` to see the (kconfig) settings which have non-default values.
For gem5 <= 23.0, You can also specify these options on the command line to
override any default values. For gem5 >= 23.1, You can use kconfig tools like
setconfig, menuconfig, or guiconfig to modify these settings in an existing
build directory.

```bash
python3 `which scons` build/ALL/gem5.opt -j9
```

> **gem5 binary types**
>
> The SCons scripts in gem5 currently have 3 different binaries you can
> build for gem5: debug, opt, and fast. These names are
> mostly self-explanatory, but detailed below.
>
> debug
> :   Built with no optimizations and debug symbols. This binary is
>     useful when using a debugger to debug if the variables you need to
>     view are optimized out in the opt version of gem5. Running with
>     debug is slow compared to the other binaries.
>
> opt
> :   This binary is build with most optimizations on (e.g., -O3), but
>     with debug symbols included. This binary is much faster than
>     debug, but still contains enough debug information to be able to
>     debug most problems.
>
> fast
> :   Built with all optimizations on (including link-time optimizations
>     on supported platforms) and with no debug symbols. Additionally,
>     any asserts are removed, but panics and fatals are still included.
>     fast is the highest performing binary, and is much smaller than
>     opt. However, fast is only appropriate when you feel that it is
>     unlikely your code has major bugs.
>
The main argument passed to SCons is what you want to build,
`build/ALL/gem5.opt`. In this case, we are building gem5.opt (an
optimized binary with debug symbols). We want to build gem5 in the
directory build/ALL. Since this directory currently doesn't exist, SCons
will look in `build_opts` to find the parameters for the ALL build. (Note:
I'm using -j9 here to execute the build on 9 of my 8 cores on my
machine. You should choose an appropriate number for your machine,
usually cores+1.)

The output should look something like below (For gem5 >= 24.1):

```txt
    scons: Reading SConscript files ...
    Mkdir("/local.chinook/gem5/gem5-tutorial/gem5/build/ALL/gem5.build")
    Checking for linker -Wl,--as-needed support... (cached) yes
    Checking for compiler -gz support... (cached) yes
    Checking for linker -gz support... (cached) yes
    Info: Using Python config: python3-config
    Checking for C header file Python.h... (cached) yes
    Checking Python version... (cached) 3.12.3
    Checking for accept(0,0,0) in C++ library None... (cached) yes
    Checking for zlibVersion() in C++ library z... (cached) yes
    Checking for C library tcmalloc_minimal... (cached) yes
    Building in /home/bees/gem5-4th-worktree/build/ALL
    "build_tools/kconfig_base.py" "/home/bees/gem5-4th-worktree/build/ALL/gem5.build/Kconfig" "/home/bees/gem5-4th-worktree/src/Kconfig" 
    Checking for C header file fenv.h... (cached) yes
    Checking for C header file png.h... (cached) yes
    Checking for clock_nanosleep(0,0,NULL,NULL) in C library None... (cached) yes
    Checking for C header file valgrind/valgrind.h... (cached) yes
    Checking for pkg-config package hdf5-serial... (cached) yes
    Checking for H5Fcreate("", 0, 0, 0) in C library hdf5... (cached) yes
    Checking for H5::H5File("", 0) in C++ library hdf5_cpp... (cached) yes
    Checking for pkg-config package protobuf... (cached) yes
    Checking for shm_open("/test", 0, 0) in C library None... (cached) yes
    Checking for backtrace_symbols_fd((void *)1, 0, 0) in C library None... (cached) yes
    Checking size of struct kvm_xsave ... (cached) yes
    Checking for C header file capstone/capstone.h... (cached) yes
    Checking for C header file linux/kvm.h... (cached) yes
    Checking for timer_create(CLOCK_MONOTONIC, NULL, NULL) in C library None... (cached) yes
    Checking for member exclude_host in struct perf_event_attr...(cached) yes
    Checking for C header file linux/if_tun.h... (cached) yes 
    Checking whether __i386__ is declared... (cached) no
    Checking whether __x86_64__ is declared... (cached) yes
    Checking for compiler -Wno-self-assign-overloaded support... (cached) yes
    Checking for linker -Wno-free-nonheap-object support... (cached) yes
    BUILD_TLM not set, not building CHI-TLM integration

    scons: done reading SConscript files.
    scons: Building targets ...
    [     CXX] ALL/base/Graphics.py.cc -> .o
    [    LINK]  -> ALL/gem5py_m5
    [     CXX] src/base/atomicio.cc -> ALL/base/atomicio.o
    [     CXX] src/base/bitfield.cc -> ALL/base/bitfield.o

     ....
     .... <lots of output>
     ....
 [SO Param] m5.objects.Uart, Uart8250 -> ALL/params/Uart8250.hh
 [     CXX] ALL/python/_m5/param_SimpleUart.cc -> .o
 [     CXX] ALL/enums/TerminalDump.cc -> .o
 [     CXX] ALL/python/_m5/param_Uart8250.cc -> .o
 [     CXX] src/dev/serial/serial.cc -> ALL/dev/serial/serial.o
 [     CXX] src/dev/serial/simple.cc -> ALL/dev/serial/simple.o
 [     CXX] src/dev/serial/terminal.cc -> ALL/dev/serial/terminal.o
 [     CXX] src/dev/serial/uart.cc -> ALL/dev/serial/uart.o
 [     CXX] src/dev/serial/uart8250.cc -> ALL/dev/serial/uart8250.o
 [     CXX] ALL/debug/Terminal.cc -> .o
 [     CXX] ALL/debug/TerminalVerbose.cc -> .o
 [     CXX] ALL/debug/Uart.cc -> .o
 [     CXX] ALL/python/m5/defines.py.cc -> .o
 [     CXX] ALL/python/m5/info.py.cc -> .o
 [     CXX] src/base/date.cc -> ALL/base/date.o
 [    LINK]  -> ALL/gem5.opt
scons: done building targets.
```

When compilation is finished you should have a working gem5 executable
at `build/ALL/gem5.opt`. The compilation can take a very long time,
often 15 minutes or more, especially if you are compiling on a remote
file system like AFS or NFS.

Common errors
-------------

### Wrong gcc version

```txt
    Error: gcc version 5 or newer required.
           Installed version: 4.4.7
```

Update your environment variables to point to the right gcc version, or
install a more up to date version of gcc. See
building-requirements-section.

### Python in a non-default location

If you use a non-default version of Python, (e.g., version 3.6 when 2.5
is your default), there may be problems when using SCons to build gem5.
RHEL6 version of SCons uses a hardcoded location for Python, which
causes the issue. gem5 often builds successfully in this case, but may
not be able to run. Below is one possible error you may see when you run
gem5.

```txt
    Traceback (most recent call last):
      File "........../gem5-stable/src/python/importer.py", line 93, in <module>
        sys.meta_path.append(importer)
    TypeError: 'dict' object is not callable
```

To fix this, you can force SCons to use your environment's Python
version by running `` python3 `which scons` build/ALL/gem5.opt `` instead
of `scons build/ALL/gem5.opt`.

### M4 macro processor not installed

If the M4 macro processor isn't installed you'll see an error similar to
this:

```txt
    ...
    Checking for member exclude_host in struct perf_event_attr...yes
    Error: Can't find version of M4 macro processor.  Please install M4 and try again.
```

Just installing the M4 macro package may not solve this issue. You may
nee to also install all of the `autoconf` tools. On Ubuntu, you can use
the following command.

```bash
sudo apt-get install automake
```

### Protobuf 3.12.3 problem

Compiling gem5 using protobuf might result in the following error,

```txt
In file included from build/X86/cpu/trace/trace_cpu.hh:53,
                 from build/X86/cpu/trace/trace_cpu.cc:38:
build/X86/proto/inst_dep_record.pb.h:49:51: error: 'AuxiliaryParseTableField' in namespace 'google::protobuf::internal' does not name a type; did you mean 'AuxillaryParseTableField'?
   49 |   static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
```

The root cause of the problem is discussed here: [https://gem5.atlassian.net/browse/GEM5-1032].

To resolve this problem, you may need to update the version of ProtocolBuffer,

```bash
sudo apt update
sudo apt install libprotobuf-dev protobuf-compiler libgoogle-perftools-dev
```

After that, you may need to clean the gem5 build folder **before** recompiling gem5,

```bash
python3 `which scons` --clean --no-cache        # cleaning the build folder
python3 `which scons` build/ALL/gem5.opt -j 9   # re-compiling gem5
```

If the problem persists, you may need to completely remove the gem5 build folder **before** compiling gem5 again,

```bash
rm -rf build/                                   # completely removing the gem5 build folder
python3 `which scons` build/ALL/gem5.opt -j 9   # re-compiling gem5
```


---


## Creating a simple configuration script

*Source: https://www.gem5.org/documentation/learning_gem5/part1/simple_config/*

Creating a simple configuration script
======================================

This chapter of the tutorial will walk you through how to set up a
simple simulation script for gem5 and to run gem5 for the first time.
It's assumed that you've completed the first chapter of the tutorial and
have successfully built gem5 with an executable `build/ALL/gem5.opt`.

Our configuration script is going to model a very simple system. We'll
have just one simple CPU core. This CPU core will be connected to a
system-wide memory bus. And we'll have a single DDR3 memory channel,
also connected to the memory bus.

gem5 configuration scripts
--------------------------

The gem5 binary takes, as a parameter, a Python script which sets up and
executes the simulation. In this script, you create a system to
simulate, create all of the components of the system, and specify all of
the parameters for the system components. Then, from the script, you can
begin the simulation.

<!-- This script is completely user-defined. You can choose to use any valid
Python code in the configuration scripts. This book provides on example
of a style that relies heavily on classes and inheritance in Python. As a
gem5 user, it's up to you how simple or complicated to make your
configuration scripts. -->

<!--  Most of these scripts are all-encompassing and
allow users to specify almost all options on the command line. Instead
of starting with these complex script, in this book we are going to
start with the most simple script that can run gem5 and build from
there. Hopefully, by the end of this section you'll have a good idea of
how simulation scripts work. -->

There are a number of example configuration scripts that ship with gem5
in `configs/examples`.
The scripts most relevant to a beginner to gem5 are located in `configs/examples/gem5-library`.
These are scripts that are intended to be used with the gem5 standard library,
which provides components that can be connected together to form a complete system.

---

> **An aside on SimObjects**
>
> gem5's modular design is built around the **SimObject** type. Most of
> the components in the simulated system are SimObjects: CPUs, caches,
> memory controllers, buses, etc. gem5 exports all of these objects from
> their `C++` implementation to python. Thus, from the python
> configuration script you can create any SimObject, set its parameters,
> and specify the interactions between SimObjects.
>
> See [SimObject details](http://doxygen.gem5.org/release/current/classgem5_1_1SimObject.html#details) for more information.

---

Setting up a configuration script for gem5 v24.1
================================================

**Notice: The content of this section is taken from part 1, section 2 of the 2024 gem5 bootcamp. The slides for the bootcamp can be found [here](https://bootcamp.gem5.org/#01-Introduction/02-getting-started)**

Let's start by creating a new config file and opening it:

```bash
mkdir configs/tutorial/part1/
touch configs/tutorial/part1/simple.py
```

This is just a normal python file that will be executed by the embedded
python in the gem5 executable. Therefore, you can use any features and
libraries available in python.

To set up a basic configuration script, we can start by adding our imports:

```python
from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
```

Next, add a board to your script:

```python
board = X86DemoBoard()
```

The X86DemoBoard is a prebuilt board that doesn't require further configuration and can be used as a complete system as-is. It is not recommended for use in research, however.

The source can be found in the gem5 repository at [src/python/gem5/prebuilt/demo/x86_demo_board.py](https://github.com/gem5/gem5/blob/stable/src/python/gem5/prebuilt/demo/x86_demo_board.py)

It has the following properties:

* 3GiB DualChannelDDR4_2400 memory
* A 2 core processor using gem5's `TIMING` model
* A private L1, shared L2 cache hierarchy with 64 KiB data and instruction caches and a 8MiB L2 cache.

As of gem5 v24.1, the X86DemoBoard can support both SE (system emulation) and FS (full system) simulations.

Next, let's set a workload to run on the board:

```python
board.set_workload(
    obtain_resource("x86-ubuntu-24.04-boot-no-systemd")
)
```

The function `obtain_resource` downloads workloads and resources.
For the `x86-ubuntu-24.04-boot-no-systemd`, it downloads a disk image and kernel, and sets default parameters.

The workload boots Ubuntu without systemd.
There are three exit events in the workload, and the simulation can exit or perform other operations at each exit event.
To change the behavior at an exit event, we will need to set up an exit event handler.

However, we will only run the simulation for 20 billion ticks, or 20 ms, in this example:

```python
sim = Simulator(board)
sim.run(20_000_000_000) # 20 billion ticks or 20 ms
```

To run the simulation after setting up the configuration script, use the following command:

```bash
./build/ALL/gem5.opt configs/tutorial/part1/simple.py
```

If you are using a pre-built gem5 binary, use the following command:

```bash
gem5 configs/tutorial/part1/simple.py
```

The output should look something like this:

```txt
gem5 Simulator System.  https://www.gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 version 24.1.0.0
gem5 compiled Dec 13 2024 14:59:49
gem5 started Dec 16 2024 13:07:46
gem5 executing on amarillo, pid 543078
command line: ./build/ALL/gem5.opt gem5-dev/testing-website-tutorial/tutorial/part1/simple.py

warn: The X86DemoBoard is solely for demonstration purposes. This board is not known to be be representative of any real-world system. Use with caution.
info: Using default config
warn: Max ticks has already been set prior to setting it through the run call. In these cases the max ticks set through the `run` function is used
Global frequency set at 1000000000000 ticks per second
warn: board.workload.acpi_description_table_pointer.rsdt adopting orphan SimObject param 'entries'
src/mem/dram_interface.cc:690: warn: DRAM device capacity (16384 Mbytes) does not match the address range assigned (2048 Mbytes)
src/mem/dram_interface.cc:690: warn: DRAM device capacity (16384 Mbytes) does not match the address range assigned (2048 Mbytes)
src/sim/kernel_workload.cc:46: info: kernel located at: /home/bees/.cache/gem5/x86-linux-kernel-5.4.0-105-generic
      0: board.pc.south_bridge.cmos.rtc: Real-time clock set to Sun Jan  1 00:00:00 2012
board.pc.com_1.device: Listening for connections on port 3467
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/dev/intel_8254_timer.cc:128: warn: Reading current count from inactive timer.
board.remote_gdb: Listening for connections on port 7003
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
build/ALL/arch/x86/generated/exec-ns.cc.inc:27: warn: instruction 'fninit' unimplemented

```

Setting up a configuration script for gem5 v21.0
==============

Creating a config file
----------------------

Let's start by creating a new config file and opening it:

```bash
mkdir configs/tutorial/part1/
touch configs/tutorial/part1/simple.py
```

This is just a normal python file that will be executed by the embedded
python in the gem5 executable. Therefore, you can use any features and
libraries available in python.

<!-- The first thing we'll do in this file is import the m5 library and all
SimObjects that we've compiled.

```python
import m5
from m5.objects import *
``` -->

Next, we'll create the first SimObject: the system that we are going to
simulate. The `System` object will be the parent of all the other
objects in our simulated system. The `System` object contains a lot of
functional (not timing-level) information, like the physical memory
ranges, the root clock domain, the root voltage domain, the kernel (in
full-system simulation), etc. To create the system SimObject, we simply
instantiate it like a normal python class:

```python
system = System()
```

Now that we have a reference to the system we are going to simulate,
let's set the clock on the system. We first have to create a clock
domain. Then we can set the clock frequency on that domain. Setting
parameters on a SimObject is exactly the same as setting members of an
object in python, so we can simply set the clock to 1 GHz, for instance.
Finally, we have to specify a voltage domain for this clock domain.
Since we don't care about system power right now, we'll just use the
default options for the voltage domain.

```python
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
```

Once we have a system, let's set up how the memory will be simulated. We
are going to use *timing* mode for the memory simulation. You will
almost always use timing mode for the memory simulation, except in
special cases like fast-forwarding and restoring from a checkpoint. We
will also set up a single memory range of size 512 MB, a very small
system. Note that in the python configuration scripts, whenever a size
is required you can specify that size in common vernacular and units
like `'512MB'`. Similarly, with time you can use time units (e.g.,
`'5ns'`). These will automatically be converted to a common
representation, respectively.

```python
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]
```

Now, we can create a CPU. We'll start with the most simple timing-based
CPU in gem5 for the X86 ISA, *X86TimingSimpleCPU*. This CPU model executes each instruction
in a single clock cycle to execute, except memory requests, which flow
through the memory system. To create the CPU you can simply just
instantiate the object:

```python
system.cpu = X86TimingSimpleCPU()
```

If we wanted to use the RISCV ISA we could use `RiscvTimingSimpleCPU` or if
we wanted to use the ARM ISA we could use `ArmTimingSimpleCPU`. However, we
will continue to use the X86 ISA for this exercise.


Next, we're going to create the system-wide memory bus:

```
system.membus = SystemXBar()
```

Now that we have a memory bus, let's connect the cache ports on the CPU
to it. In this case, since the system we want to simulate doesn't have
any caches, we will connect the I-cache and D-cache ports directly to
the membus. In this example system, we have no caches.

```
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
```

---
> **An aside on gem5 ports**
>
> To connect memory system components together, gem5 uses a port
> abstraction. Each memory object can have two kinds of ports,
> *request ports* and *response ports*. Requests are sent from
> a request port to a response port, and responses are sent from
> a response port to a request port. When connecting ports, you
> must connect a request port to a response port.
>
> Connecting ports together is easy to do from the python configuration
> files. You can simply set the request port `=` to the response port
> and they will be connected. For instance:
>
> ```python
> system.cpu.icache_port = system.l1_cache.cpu_side
> ```
>
> In this example, the cpu's `icache_port` is a request port, and the cache's
> `cpu_side` is a response port. The request port and the response port can be
> on either side of the `=` and the same connection will be made. After making
> the connection, the requestor can send requests to the responder. There is a
> lot of magic going on behind the scenes to set up the connection, the details
> of which are unimportant to most users.
>
> Another notable kind of magic of the `=` of two ports in a gem5 Python
> configuration is that, it is allowed to have one port on one side, and an
> array of ports on the other side. For example:
>
> ```python
> system.cpu.icache_port = system.membus.cpu_side_ports
> ```
>
> In this example, the cpu's `icache_port` is a request port, and the membus's
> `cpu_side_ports` is an array of response ports. In this case, a new response
> port is spawned on the `cpu_side_ports`, and this newly created port will be
> connected to the request port.
>
> We will discuss ports and MemObject in more detail in the [MemObject chapter](http://www.gem5.org/documentation/learning_gem5/part2/memoryobject/).

---

Next, we need to connect up a few other ports to make sure that our
system will function correctly. We need to create an I/O controller on
the CPU and connect it to the memory bus. Also, we need to connect a
special port in the system up to the membus. This port is a
functional-only port to allow the system to read and write memory.

Connecting the PIO and interrupt ports to the memory bus is an
x86-specific requirement. Other ISAs (e.g., ARM) do not require these 3
extra lines.

```
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports
```

Next, we need to create a memory controller and connect it to the
membus. For this system, we'll use a simple DDR3 controller and it will
be responsible for the entire memory range of our system.

```
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
```

After those final connections, we've finished instantiating our
simulated system! Our system should look like the figure below.

![A simple system configuration without
caches.](/pages/static/figures/simple_config.png)

Next, we need to set up the process we want the CPU to execute. Since we
are executing in syscall emulation mode (SE mode), we will just point
the CPU at the compiled executable. We'll execute a simple "Hello world"
program. There's already one that is compiled that ships with gem5, so
we'll use that. You can specify any application built for x86 and that's
been statically compiled.

> **Full system vs syscall emulation**
>
> gem5 can run in two different modes called "syscall emulation" and
> "full system" or SE and FS modes. In full system mode (covered later
> full-system-part), gem5 emulates the entire hardware system and runs
> an unmodified kernel. Full system mode is similar to running a virtual
> machine.
>
> Syscall emulation mode, on the other hand, does not emulate all of the
> devices in a system and focuses on simulating the CPU and memory
> system. Syscall emulation is much easier to configure since you are
> not required to instantiate all of the hardware devices required in a
> real system. However, syscall emulation only emulates Linux system
> calls, and thus only models user-mode code.
>
> If you do not need to model the operating system for your research
> questions, and you want extra performance, you should use SE mode.
> However, if you need high fidelity modeling of the system, or OS
> interaction like page table walks are important, then you should use
> FS mode.

First, we have to create the process (another SimObject). Then we set
the processes command to the command we want to run. This is a list
similar to argv, with the executable in the first position and the
arguments to the executable in the rest of the list. Then we set the CPU
to use the process as it's workload, and finally create the functional
execution contexts in the CPU.

```
binary = 'tests/test-progs/hello/bin/x86/linux/hello'

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()
```

The final thing we need to do is instantiate the system and begin
execution. First, we create the `Root` object. Then we instantiate the
simulation. The instantiation process goes through all of the SimObjects
we've created in python and creates the `C++` equivalents.

As a note, you don't have to instantiate the python class then specify
the parameters explicitly as member variables. You can also pass the
parameters as named arguments, like the `Root` object below.

```
root = Root(full_system = False, system = system)
m5.instantiate()
```

Finally, we can kick off the actual simulation! As a side now, gem5 is
now using Python 3-style `print` functions, so `print` is no longer a
statement and must be called as a function.

```
print("Beginning simulation!")
exit_event = m5.simulate()
```

And once simulation finishes, we can inspect the state of the system.

```
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
```

Running gem5
------------

Now that we've created a simple simulation script (the full version of
which can be found in the gem5 code base at
[configs/learning\_gem5/part1/simple.py](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part1/simple.py)
) we're ready to run gem5. gem5 can take many parameters, but requires just
one positional argument, the simulation script. So, we can simply run gem5
from the root gem5 directory as:

```
build/ALL/gem5.opt configs/tutorial/part1/simple.py
```

The output should be:

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 17 2021 22:05:20
    gem5 executing on amarillo, pid 75197
    command line: build/X86/gem5.opt configs/tutorial/part1/simple.py

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 490394000 because exiting with last active thread context

Parameters in the configuration file can be changed and the results
should be different. For instance, if you double the system clock, the
simulation should finish faster. Or, if you change the DDR controller to
DDR4, the performance should be better.

Additionally, you can change the CPU model to `X86MinorCPU` to model an
in-order CPU, or `X86O3CPU` to model an out-of-order CPU. However,
note that `X86O3CPU` currently does not work with simple.py, because
`X86O3CPU` requires a system with separate instruction and data caches
(`X86O3CPU` does work with the configuration in the next section).

All gem5 BaseCPU's take the naming format `{ISA}{Type}CPU`. Ergo, if we wanted
a RISCV Minor CPU we'd use `RiscvMinorCPU`.

The Valid ISAs are:
* Riscv
* Arm
* X86
* Sparc
* Power
* Mips

The CPU types are:
* AtomicSimpleCPU
* O3CPU
* TimingSimpleCPu
* KvmCPU
* MinorCPU

Next, we will add caches to our configuration file to model a more
complex system.


---


## Adding cache to configuration script

*Source: https://www.gem5.org/documentation/learning_gem5/part1/cache_config/*

More complex config for gem5 v24.1
===============================

**Notice: The material in the following section is taken from section 2, part 1 of the 2024 gem5 bootcamp. The link to the slides is [here](https://bootcamp.gem5.org/#02-Using-gem5/01-stdlib)**

In the previous section, we learned the basics of setting up a Python configuration script for use with gem5.
The previous section's config script uses the X86DemoBoard, which is pre-configured with caches, memory, etc.
In this section, we will learn how to use other components in the gem5 standard library to set up a simulation.

What is the gem5 standard library?
----------------------------------

The gem5 standard library provides a set of predefined components that can be used to define a system in a configuration script.
Without the standard library, you would have to define every part of your simulation, potentially resulting in scripts with hundreds of lines of code even for the most basic of simulations.

Main Idea
---------

Due to its modular, object-oriented design, gem5 can be thought of as a set of components that can be plugged together to form a simulation.
The types of components are boards, processors, memory systems, and cache hierarchies:

- Board: The "backbone" of the system. You plug components into the board. The board also contains the system-level things like devices, workload, etc. It's the boards job to negotiate the connections between other components.
- Processor: Processors connect to boards and have one or more cores.
- Cache hierarchy: A cache hierarchy is a set of caches that can be connected to a processor and memory system.
- Memory system: A memory system is a set of memory controllers and memory devices that can be connected to the cache hierarchy.

Relationship to gem5 models
---------------------------

The C++ code in gem5 specifies parameterized models (typically referred to "SimObjects" in most gem5 literature).
These models are then instantiated in the pre-made Python scripts in the gem5 standard library.

The standard library is a way to wrap these models in a standard API into, what we call, components.

The gem5 models are fine grained concepts, while components are coarser grained and typically contain many models instantiated with sensible parameters.
For example, a gem5 model could be a core, and a component could be a processor with multiple cores that also specifies bus connections and sets parameters to sensible vlaues.

If you want to create a new component you are encouraged to extend (i.e., subclass) the components in the standard library or create new components.
This allows you to choose the models within the component and the value of their parameters.

Setting up the configuration script
-----------------------------------
First, let's make a configuration file:

```bash
mkdir configs/tutorial/part1/
touch configs/tutorial/part1/components.py
```

Let's add our imports:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
```

Next, let's add our cache hierarchy:

```python
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16KiB",
    l1d_assoc=8,
    l1i_size="16KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)
```

MESITwoLevelCacheHierarchy is a component that represents a two-level MESI cache hierarchy.
This uses the Ruby memory model. See [here]https://bootcamp.gem5.org/#02-Using-gem5/05-cache-hierarchies for more information about caches in gem5.

The component for the cache hierarchy is parameterized with the sizes and associativities of the L1 and L2 caches.

Next, let's add a memory system:

```python
memory = SingleChannelDDR4_2400()
```

This component represents a single-channel DDR3 memory system.

There is a size parameter that can be used to specify the size of the memory system of the simulated system.
You can reduce the size to save simulation time, or use the default for the memory type (e.g., one channel of DDR3 defaults to 8 GiB).
There are also multi channel memories available. You can see [these](https://bootcamp.gem5.org/#02-Using-gem5/06-memory) gem5 2024 bootcamp slides for more information.

Next, let's add a processor:

```python
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1)
```

The `SimpleProcessor` is a component that allows you to customize the model for the underlying cores.
The `cpu_type` parameter specifies the type of CPU model to use.

Next, let's add a board and plug in components:

```python
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

The SimpleBoard can run any ISA in Syscall Emulation (SE) mode.
It is "Simple" due the relative simplicity of SE mode.
Most boards are tied to a specific ISA and require more complex designs to run Full System (FS) simulation.
You can find the boards in the gem5 standard library at `src/python/gem5/components/boards`. The demo boards are located in `src/python/gem5/prebuilt/demo`.

Next, set up the workload:

```python
board.set_workload(obtain_resource("arm-gapbs-bfs-run"))
```

The obtain_resource function downloads the files needed to run the specified workload.
In this case "arm-gapbs-bfs-run" is a BFS workload from the GAP Benchmark Suite.
You can see more information about this resources at the gem5 resources website [here](https://resources.gem5.org/resources/arm-gapbs-bfs-run?version=1.0.0).
In general, you can browse all gem5 resources at the [gem5 resources website](https://resources.gem5.org/).

Next, set up the simulation:

```python
simulator = Simulator(board=board)
simulator.run()
```

You can now run the simulation using

```bash
./build/ALL/gem5.opt configs/tutorial/part1/components.py

```

The output should look something like this:

```txt
gem5 Simulator System.  https://www.gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 version 24.1.0.0
gem5 compiled Dec 13 2024 14:59:49
gem5 started Dec 16 2024 16:34:29
gem5 executing on amarillo, pid 575999
command line: ./build/ALL/gem5.opt gem5-dev/testing-website-tutorial/tutorial/part1/components.py

info: Using default config
Global frequency set at 1000000000000 ticks per second
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
board.remote_gdb: Listening for connections on port 7003
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
src/mem/ruby/system/Sequencer.cc:704: warn: Replacement policy updates recently became the responsibility of SLICC state machines. Make sure to setMRU() near callbacks in .sm files!
src/sim/syscall_emul.cc:86: warn: ignoring syscall set_robust_list(...)
src/sim/syscall_emul.cc:97: warn: ignoring syscall rseq(...)
      (further warnings will be suppressed)
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/syscall_emul.hh:1117: warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
      Returning '/home/bees/.cache/gem5/arm-gapbs-bfs'
src/arch/arm/insts/pseudo.cc:174: warn:         instruction 'bti' unimplemented
src/sim/syscall_emul.cc:86: warn: ignoring syscall mprotect(...)
src/sim/syscall_emul.cc:86: warn: ignoring syscall sched_getaffinity(...)
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
Generate Time:       0.00503
Build Time:          0.00201
Graph has 1024 nodes and 10496 undirected edges for degree: 10
Trial Time:          0.00011
Trial Time:          0.00010
Trial Time:          0.00010
Trial Time:          0.00009
Trial Time:          0.00011
Trial Time:          0.00010
Trial Time:          0.00010
Trial Time:          0.00010
Trial Time:          0.00010
Trial Time:          0.00013
Average Time:        0.00010

```

gem5 stdlib File Structure
--------------------------

The gem5 stdlib is located in `src/python/gem5/`.
Of interest here are the `components` and `prebuilt` folders:

```txt
gem5/src/python/gem5/components
----/boards
----/cachehierarchies
----/memory
----/processors

gem5/src/python/gem5/prebuilt
----/demo
----/riscvmatched
```

The `components` folder contains components with which you can build systems. The `prebuilt` folder contains various prebuilt systems, including demo systems for the X86, Arm, and RISC-V isas, and riscvmatched, which is a model of SiFive Unmatched.

```txt
gem5/src/python/gem5/components
----/boards
    ----/simple
    ----/arm_board
    ----/riscv_board
    ----/x86_board
----/cachehierarchies
----/memory
----/processors
```

Boards are what components plug into. The SimpleBoard has SE mode only, the ArmBoard has FS mode only, and X86Board and RiscvBoard have both FS and SE mode.

gem5/src/python/gem5/components
----/boards
----/cachehierarchies
    ----/chi
    ----/classic
    ----/ruby
----/memory
----/processors

Cache hierarchy components have a fixed interface to processors and memory.

- Ruby: detailed cache coherence and interconnect
- CHI: Arm CHI-based protocol implemented in Ruby
- Classic caches: Hierarchy of crossbars with inflexible coherence

As of gem5 v24.1, it is possible to use any Ruby cache coherence protocol with the ALL gem5 build.
This is the build included in pre-compiled binaries.

```txt
gem5/src/python/gem5/components
----/boards
----/cachehierarchies
----/memory
    ----/single_channel
    ----/multi_channel
    ----/dramsim
    ----/dramsys
    ----/hbm
----/processors
```

The memory directory contains pre-configured (LP)DDR3/4/5 DIMMs. Single and multi channel memory systems are available.
There is integration with DRAMSim and DRAMSys, which while not needed for accuracy, is useful for comparisons.
The `hbm` directory is an HBM stack.

```txt
gem5/src/python/gem5/components
----/boards
----/cachehierarchies
----/memory
----/processors
    ----/generators
    ----/simple
    ----/switchable
```

The `processors` directory mostly contains configurable processors to build off of.

Generators create synthetic traffic, but act like processors. They have linear, random, and more interesting patterns.

Simple processors only have default parameters and one ISA.

Switchable processors allow you to change processor types during simulation.

More on processors
------------------

Processors are made up of cores.
Cores have a "BaseCPU" as a member. This is the actual CPU model.
`Processor` is what interfaces with `CacheHierarchy` and `Board`
Processors are organized, structured sets of cores. They define how cores connect with each other and with outside components and the board though standard interface.

**gem5 has three (or four or five) different processor models**

They are as follows:

`CPUTypes.TIMING`: A simple in-order CPU model
This is a "single cycle" CPU. Each instruction takes the time to fetch and executes immediately.
Memory operations take the latency of the memory system.
OK for doing memory-centric studies, but not good for most research.

`CPUTypes.O3`: An out-of-order CPU model
Highly detailed model based on the Alpha 21264.
Has ROB, physical registers, LSQ, etc.
Don't use SimpleProcessor if you want to configure this.

`CPUTypes.MINOR`: An in-order core model
A high-performance in-order core model.
Configurable four-stage pipeline
Don't use SimpleProcessor if you want to configure this.

`CPUTypes.ATOMIC`: Used in "atomic" mode (more later)
`CPUTypes.KVM`: This is covered in detail in the [2024 gem5 bootcamp](https://bootcamp.gem5.org/#02-Using-gem5/08-accelerating-simulation).


FS vs SE mode
-------------

SE mode relays application syscalls to the host OS. This means we don't need to simulate an OS for applications to run.

In addition, we can access host resources such as files of libraries to dynamically link in.

Don't treat SE mode as "FS but faster": You must understand what you're simulating and whether it will impact results.
Not all syscalls will ever be implemented: We'd love to have all the syscalls implemented but Linux changes rapidly. We try to cover common use-cases but we can't cover everything. If a Syscall is missing, you can implement it, ignore it, or use FS mode.
Binaries with elevated privileges do not work in SE mode: If you're running a binary that requires elevated privileges, you'll need to run it in FS mode.

FS mode does everything SE mode does (and more!) but can take longer to get to the region of interest. You have to wait for the OS to boot each time (unless you accelerate the simulation).

However, as SE mode doesn't simulate the OS, you risk missing important events triggered via syscalls, I/O, or the operating system, which may mean your simulated system doesn't properly reflect the real system.

Think through what SE mode is doing and if it's right for your use-case. If in doubt, use FS mode. It's (generally) not worth the risk using SE mode if you're not sure.

Full Boot Example
-----------------

For an example of a configuration file that runs the entire boot of Ubuntu 24.04 on an X86 system, see [the gem5 stdlib documentation](../../gem5-stdlib/2-tutorial-x86-fs.md). Of note is that we need to define an exit event handler in order to get through the entire boot:

```python
def exit_event_handler():
    print("First exit: kernel booted")
    yield False  # gem5 is now executing systemd startup
    print("Second exit: Started `after_boot.sh` script")
    # The after_boot.sh script is executed after the kernel and systemd have
    # booted.
    # Here we switch the CPU type to Timing.
    print("Switching to Timing CPU")
    processor.switch()
    yield False  # gem5 is now executing the `after_boot.sh` script
    print("Third exit: Finished `after_boot.sh` script")
    # The after_boot.sh script will run a script if it is passed via
    # m5 readfile. This is the last exit event before the simulation exits.
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
```

At the first exit event, the generator yields False to continue the simulation. At the second exit event, the generator switches the CPUs, then yields False again. At the third exit event, it yields `True` to end the simulation.

There are various types of exit events. The Simulator has default behavior for these events, but they can be overridden.

```python
ExitEvent.EXIT
ExitEvent.CHECKPOINT
ExitEvent.FAIL
ExitEvent.SWITCHCPU
ExitEvent.WORKBEGIN
ExitEvent.WORKEND
ExitEvent.USER_INTERRUPT
ExitEvent.MAX_TICK
```

Key idea: The Simulator object controls simulation
--------------------------------------------------

To place our idea of gem5:

models (or SimObjects) are the fine-grained objects that are connected together in Python scripts to form a simulation.
components are the coarse-grained objects that are connected defined as a set of configured models in Python scripts to form and delivered as part of the Standard Library
The standard library allows users to specify a board and specify the properties of the board by specify the components that are connected to it.
The Simulator takes a board and launches the simulation and gives an API which allows for control of the simulation: specifying the simulation stopping and restarting condition, replacing components "on the fly", defining when the simulation should stop and start, etc.
See [src/python/gem5/simulate/simulator.py](https://github.com/gem5/gem5/blob/stable/src/python/gem5/simulate/simulator.py) for the Simulator source.

Simulator parameters are as follows:

board: The Board to simulate (required)
full_system: Whether to simulate a full system (default: False, can be inferred from the board, not needed specified in most cases)
on_exit_event: A complex data structure that allows you to control the simulation. The simulator exits for many reasons, this allows you to customize what happens. We just saw an example.
checkpoint_path: If we're restoring from a checkpoint, this is the path to the checkpoint. More on checkpoints later.
id: An optional name for this simulation. Used in multisim. More on this in the future.

Some useful functions are below:

run(): Run the simulation
get/set_max_ticks(max_tick): Set the absolute tick to stop simulation. Generates a MAX_TICK exit event that can be handled.
schedule_max_insts(inst_number): Set the number of instructions to run before stopping. Generates a MAX_INSTS exit event that can be handled. Note that if running multiple cores, this happens if any core reaches this number of instructions.
get_stats(): Get the statistics from the simulation. Returns a dictionary of statistics.

See [src/python/gem5/simulate/simulator.py](https://github.com/gem5/gem5/blob/stable/src/python/gem5/simulate/simulator.py) for more details.

Creating new standard library components
-----------------------------------------

The gem5 standard library is designed around extension and encapsulation, not parametarization.
If you want to create a component with different parameters, extend using object-oriented semantics.

We will now create a new component. We will specialize/extend the "BaseCPUProcessor" to create an ARM processor with a singular out-of-order core.

First, let's add our imports:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from m5.objects import ArmO3CPU
from m5.objects import TournamentBP
```

Next, let's make a new subclass to specialize the core's parameters:

```python
class MyOutOfOrderCore(BaseCPUCore):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        super().__init__(ArmO3CPU(), ISA.ARM)
        self.core.fetchWidth = width
        self.core.decodeWidth = width
        self.core.renameWidth = width
        self.core.issueWidth = width
        self.core.wbWidth = width
        self.core.commitWidth = width

        self.core.numROBEntries = rob_size

        self.core.numPhysIntRegs = num_int_regs
        self.core.numPhysFloatRegs = num_fp_regs

        self.core.branchPred = TournamentBP()

        self.core.LQEntries = 128
        self.core.SQEntries = 128
```

Next, let's make a processor using this core. The `BaseCPUProcessor` assumes a list of cores that are `BaseCPUCores`. We'll just make one core and pass the parameters to it:

```python
class MyOutOfOrderProcessor(BaseCPUProcessor):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        cores = [MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs)]
        super().__init__(cores)
```

Next, let's use these components to set up a processor for the simulation:

```python
my_ooo_processor = MyOutOfOrderProcessor(
    width=8, rob_size=192, num_int_regs=256, num_fp_regs=256
)
```

Finally, let's set up the rest of the simulation:

```python
main_memory = SingleChannelDDR4_2400(size="2GB")

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)
board = SimpleBoard(
    processor=my_ooo_processor,
    memory=main_memory,
    cache_hierarchy=cache_hierarchy,
    clk_freq="3GHz",
)

board.set_workload(obtain_resource("arm-gapbs-bfs-run"))

simulator = Simulator(board)
simulator.run()
```

You can now run this simulation with the following command, assuming that your configuration script is named `config.py`:

```bash
./build/ALL/gem5.opt config.py
```

If you have a pre-built binary, you can simply use the following command:

```bash
gem5 config.py
```

gem5 v21.0: Adding cache to the configuration script
====================================================

Using the [previous configuration script as a starting point](http://www.gem5.org/documentation/learning_gem5/part1/simple_config/),
this chapter will walk through a more complex configuration. We will add
a cache hierarchy to the system as shown in
the figure below. Additionally, this chapter
will cover understanding the gem5 statistics output and adding command
line parameters to your scripts.

![A system configuration with a two-level cache
hierarchy.](/pages/static/figures/advanced_config.png)

Creating cache objects
----------------------

We are going to use the classic caches, instead of ruby-intro-chapter,
since we are modeling a single CPU system and we don't care about
modeling cache coherence. We will extend the Cache SimObject and
configure it for our system. First, we must understand the parameters
that are used to configure Cache objects.

> **Classic caches and Ruby**
>
> gem5 currently has two completely distinct subsystems to model the
> on-chip caches in a system, the "Classic caches" and "Ruby". The
> historical reason for this is that gem5 is a combination of m5 from
> Michigan and GEMS from Wisconsin. GEMS used Ruby as its cache model,
> whereas the classic caches came from the m5 codebase (hence
> "classic"). The difference between these two models is that Ruby is
> designed to model cache coherence in detail. Part of Ruby is SLICC, a
> language for defining cache coherence protocols. On the other hand,
> the classic caches implement a simplified and inflexible MOESI
> coherence protocol.
>
> To choose which model to use, you should ask yourself what you are
> trying to model. If you are modeling changes to the cache coherence
> protocol or the coherence protocol could have a first-order impact on
> your results, use Ruby. Otherwise, if the coherence protocol isn't
> important to you, use the classic caches.
>
> A long-term goal of gem5 is to unify these two cache models into a
> single holistic model.

### Cache

The Cache SimObject declaration can be found in src/mem/cache/Cache.py.
This Python file defines the parameters which you can set of the
SimObject. Under the hood, when the SimObject is instantiated these
parameters are passed to the C++ implementation of the object. The
`Cache` SimObject inherits from the `BaseCache` object shown below.

Within the `BaseCache` class, there are a number of *parameters*. For
instance, `assoc` is an integer parameter. Some parameters, like
`write_buffers` have a default value, 8 in this case. The default
parameter is the first argument to `Param.*`, unless the first argument
is a string. The string argument of each of the parameters is a
description of what the parameter is (e.g.,
`tag_latency = Param.Cycles("Tag lookup latency")` means that the
`` tag_latency `` controls "The hit latency for this cache").

Many of these parameters do not have defaults, so we are required to set
these parameters before calling `m5.instantiate()`.

* * * * *

Now, to create caches with specific parameters, we are first going to
create a new file, `caches.py`, in the same directory as simple.py,
`configs/tutorial/part1`. The first step is to import the SimObject(s)
we are going to extend in this file.

```
from m5.objects import Cache
```

Next, we can treat the BaseCache object just like any other Python class
and extend it. We can name the new cache anything we want. Let's start
by making an L1 cache.

```
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
```

Here, we are setting some of the parameters of the BaseCache that do not
have default values. To see all of the possible configuration options,
and to find which are required and which are optional, you have to look
at the source code of the SimObject. In this case, we are using
BaseCache.

We have extended `BaseCache` and set most of the parameters that do not
have default values in the `BaseCache` SimObject. Next, let's two more
sub-classes of L1Cache, an L1DCache and L1ICache

```
class L1ICache(L1Cache):
    size = '16kB'

class L1DCache(L1Cache):
    size = '64kB'
```

Let's also create an L2 cache with some reasonable parameters.

```
class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
```

Now that we have specified all of the necessary parameters required for
`BaseCache`, all we have to do is instantiate our sub-classes and
connect the caches to the interconnect. However, connecting lots of
objects up to complex interconnects can make configuration files quickly
grow and become unreadable. Therefore, let's first add some helper
functions to our sub-classes of `Cache`. Remember, these are just Python
classes, so we can do anything with them that you can do with a Python
class.

To the L1 cache let's add two functions, `connectCPU` to connect a CPU
to the cache and `connectBus` to connect the cache to a bus. We need to
add the following code to the `L1Cache` class.

```
def connectCPU(self, cpu):
    # need to define this in a base class!
    raise NotImplementedError

def connectBus(self, bus):
    self.mem_side = bus.cpu_side_ports
```

Next, we have to define a separate `connectCPU` function for the
instruction and data caches, since the I-cache and D-cache ports have a
different names. Our `L1ICache` and `L1DCache` classes now become:

```
class L1ICache(L1Cache):
    size = '16kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '64kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
```

Finally, let's add functions to the `L2Cache` to connect to the
memory-side and CPU-side bus, respectively.

```
def connectCPUSideBus(self, bus):
    self.cpu_side = bus.mem_side_ports

def connectMemSideBus(self, bus):
    self.mem_side = bus.cpu_side_ports
```

The full file can be found in the gem5 source at
[`configs/learning_gem5/part1/caches.py`](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part1/caches.py).

Adding caches to the simple config file
------------------------------------

Now, let's add the caches we just created to the configuration script we
created in the [last chapter](http://www.gem5.org/documentation/learning_gem5/part1/simple_config/).

First, let's copy the script to a new name.

```
cp ./configs/tutorial/part1/simple.py ./configs/tutorial/part1/two_level.py
```

First, we need to import the names from the `caches.py` file into the
namespace. We can add the following to the top of the file (after the
m5.objects import), as you would with any Python source.

```
from caches import *
```

Now, after creating the CPU, let's create the L1 caches:

```
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
```

And connect the caches to the CPU ports with the helper function we
created.

```
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
```

You need to *remove* the following two lines which connected the cache
ports directly to the memory bus.

```
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
```

We can't directly connect the L1 caches to the L2 cache since the L2
cache only expects a single port to connect to it. Therefore, we need to
create an L2 bus to connect our L1 caches to the L2 cache. The, we can
use our helper function to connect the L1 caches to the L2 bus.

```
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
```

Next, we can create our L2 cache and connect it to the L2 bus and the
memory bus.

```
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)
```

Note that `system.membus = SystemXBar()` has been defined before
`system.l2cache.connectMemSideBus` so we can pass it to
`system.l2cache.connectMemSideBus`. Everything else in the file
stays the same! Now we have a complete configuration with a
two-level cache hierarchy. If you run the current file, `hello`
should now finish in 57467000 ticks. The full script can
be found in the gem5 source at
[`configs/learning_gem5/part1/two_level.py`](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part1/two_level.py).

Adding parameters to your script
--------------------------------

When performing experiments with gem5, you don't want to edit your
configuration script every time you want to test the system with
different parameters. To get around this, you can add command-line
parameters to your gem5 configuration script. Again, because the
configuration script is just Python, you can use the Python libraries
that support argument parsing. Although pyoptparse is officially
deprecated, many of the configuration scripts that ship with gem5 use it
instead of pyargparse since gem5's minimum Python version used to be
2.5. The minimum Python version is now 3.6, so Python's argparse is a better
option when writing new scripts that don't need to interact with the
current gem5 scripts. To get started using :pyoptparse, you can consult
the online Python documentation.

To add options to our two-level cache configuration, after importing our
caches, let's add some options.

```
import argparse

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("binary", default="", nargs="?", type=str,
                    help="Path to the binary to execute.")
parser.add_argument("--l1i_size",
                    help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size",
                    help="L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l2_size",
                    help="L2 cache size. Default: 256kB.")

options = parser.parse_args()
```
Note that if you wanted to pass the binary file's path the way shown above
and use it through options, you should specify it as `options.binary`.
For example:

```
system.workload = SEWorkload.init_compatible(options.binary)
```

Now, you can run
`build/ALL/gem5.opt configs/tutorial/part1/two_level.py --help` which
will display the options you just added.

Next, we need to pass these options onto the caches that we create in
the configuration script. To do this, we'll simply change two\_level\_opts.py
to pass the options into the caches as a parameter to their constructor
and add an appropriate constructor, next.

```
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)
...
system.l2cache = L2Cache(options)
```

In caches.py, we need to add constructors (`__init__` functions in
Python) to each of our classes. Starting with our base L1 cache, we'll
just add an empty constructor since we don't have any parameters which
apply to the base L1 cache. However, we can't forget to call the super
class's constructor in this case. If the call to the super class
constructor is skipped, gem5's SimObject attribute finding function will
fail and the result will be
"`RuntimeError: maximum recursion depth exceeded`" when you try to
instantiate the cache object. So, in `L1Cache` we need to add the
following after the static class members.

```
def __init__(self, options=None):
    super(L1Cache, self).__init__()
    pass
```

Next, in the `L1ICache`, we need to use the option that we created
(`l1i_size`) to set the size. In the following code, there is guards for
if `options` is not passed to the `L1ICache` constructor and if no
option was specified on the command line. In these cases, we'll just use
the default we've already specified for the size.

```
def __init__(self, options=None):
    super(L1ICache, self).__init__(options)
    if not options or not options.l1i_size:
        return
    self.size = options.l1i_size
```

We can use the same code for the `L1DCache`:

```
def __init__(self, options=None):
    super(L1DCache, self).__init__(options)
    if not options or not options.l1d_size:
        return
    self.size = options.l1d_size
```

And the unified `L2Cache`:

```
def __init__(self, options=None):
    super(L2Cache, self).__init__()
    if not options or not options.l2_size:
        return
    self.size = options.l2_size
```

With these changes, you can now pass the cache sizes into your script
from the command line like below.

```
build/ALL/gem5.opt configs/tutorial/part1/two_level.py --l2_size='1MB' --l1d_size='128kB'
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:00:33
    gem5 executing on amarillo, pid 83118
    command line: build/X86/gem5.opt configs/tutorial/part1/two_level.py --l2_size=1MB --l1d_size=128kB

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 57467000 because exiting with last active thread context

The full scripts can be found in the gem5 source at
[`configs/learning_gem5/part1/caches.py`](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part1/caches.py) and
[`configs/learning_gem5/part1/two_level.py`](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part1/two_level.py).


---


## Understanding gem5 statistics and output

*Source: https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/*

Understanding gem5 statistics and output
========================================

In addition to any information which your simulation script prints out,
after running gem5, there are three files generated in a directory
called `m5out`:

**config.ini**
:   Contains a list of every SimObject created for the simulation and
    the values for its parameters.

**config.json**
:   The same as config.ini, but in json format.

**stats.txt**
:   A text representation of all of the gem5 statistics registered for
    the simulation.

config.ini
----------

This file is the definitive version of what was simulated. All of the
parameters for each SimObject that is simulated, whether they were set
in the configuration scripts or the defaults were used, are shown in
this file.

Below is pulled from the config.ini generated when the `simple.py`
configuration file from
[simple-config-chapter](http://www.gem5.org/documentation/learning_gem5/part1/simple_config/)
is run.

    [root]
    type=Root
    children=system
    eventq_index=0
    full_system=false
    sim_quantum=0
    time_sync_enable=false
    time_sync_period=100000000000
    time_sync_spin_threshold=100000000

    [system]
    type=System
    children=clk_domain cpu dvfs_handler mem_ctrl membus
    boot_osflags=a
    cache_line_size=64
    clk_domain=system.clk_domain
    default_p_state=UNDEFINED
    eventq_index=0
    exit_on_work_items=false
    init_param=0
    kernel=
    kernel_addr_check=true
    kernel_extras=
    kvm_vm=Null
    load_addr_mask=18446744073709551615
    load_offset=0
    mem_mode=timing

    ...

    [system.membus]
    type=CoherentXBar
    children=snoop_filter
    clk_domain=system.clk_domain
    default_p_state=UNDEFINED
    eventq_index=0
    forward_latency=4
    frontend_latency=3
    p_state_clk_gate_bins=20
    p_state_clk_gate_max=1000000000000
    p_state_clk_gate_min=1000
    point_of_coherency=true
    point_of_unification=true
    power_model=
    response_latency=2
    snoop_filter=system.membus.snoop_filter
    snoop_response_latency=4
    system=system
    use_default_range=false
    width=16
    master=system.cpu.interrupts.pio system.cpu.interrupts.int_slave system.mem_ctrl.port
    slave=system.cpu.icache_port system.cpu.dcache_port system.cpu.interrupts.int_master system.system_port

    [system.membus.snoop_filter]
    type=SnoopFilter
    eventq_index=0
    lookup_latency=1
    max_capacity=8388608
    system=system

Here we see that at the beginning of the description of each SimObject
is first its name as created in the configuration file surrounded by
square brackets (e.g., `[system.membus]`).

Next, every parameter of the SimObject is shown with its value,
including parameters not explicitly set in the configuration file. For
instance, the configuration file sets the clock domain to be 1 GHz (1000
ticks in this case). However, it did not set the cache line size (which
is 64 in the `system`) object.

The `config.ini` file is a valuable tool for ensuring that you are
simulating what you think you're simulating. There are many possible
ways to set default values, and to override default values, in gem5. It
is a "best-practice" to always check the `config.ini` as a sanity check
that values set in the configuration file are propagated to the actual
SimObject instantiation.

stats.txt
---------

gem5 has a flexible statistics generating system. gem5 statistics is
covered in some detail on the [gem5 stats](
https://www.gem5.org/documentation/general_docs/statistics/). Each instantiation of a SimObject
has it's own statistics. At the end of simulation, or when special
statistic-dumping commands are issued, the current state of the
statistics for all SimObjects is dumped to a file.

First, the statistics file contains general statistics about the
execution:

    ---------- Begin Simulation Statistics ----------
    simSeconds                                   0.000057                       # Number of seconds simulated (Second)
    simTicks                                     57467000                       # Number of ticks simulated (Tick)
    finalTick                                    57467000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset) (Tick)
    simFreq                                  1000000000000                       # The number of ticks per simulated second ((Tick/Second))
    hostSeconds                                      0.03                       # Real time elapsed on the host (Second)
    hostTickRate                               2295882330                       # The number of ticks simulated per host second (ticks/s) ((Tick/Second))
    hostMemory                                     665792                       # Number of bytes of host memory used (Byte)
    simInsts                                         6225                       # Number of instructions simulated (Count)
    simOps                                          11204                       # Number of ops (including micro ops) simulated (Count)
    hostInstRate                                   247382                       # Simulator instruction rate (inst/s) ((Count/Second))
    hostOpRate                                     445086                       # Simulator op (including micro ops) rate (op/s) ((Count/Second))

    ---------- Begin Simulation Statistics ----------
    simSeconds                                   0.000490                       # Number of seconds simulated (Second)
    simTicks                                    490394000                       # Number of ticks simulated (Tick)
    finalTick                                   490394000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset) (Tick)
    simFreq                                  1000000000000                       # The number of ticks per simulated second ((Tick/Second))
    hostSeconds                                      0.03                       # Real time elapsed on the host (Second)
    hostTickRate                              15979964060                       # The number of ticks simulated per host second (ticks/s) ((Tick/Second))
    hostMemory                                     657488                       # Number of bytes of host memory used (Byte)
    simInsts                                         6225                       # Number of instructions simulated (Count)
    simOps                                          11204                       # Number of ops (including micro ops) simulated (Count)
    hostInstRate                                   202054                       # Simulator instruction rate (inst/s) ((Count/Second))
    hostOpRate                                     363571                       # Simulator op (including micro ops) rate (op/s) ((Count/Second))

The statistic dump begins with
`---------- Begin Simulation Statistics ----------`. There may be
multiple of these in a single file if there are multiple statistic dumps
during the gem5 execution. This is common for long running applications,
or when restoring from checkpoints.

Each statistic has a name (first column), a value (second column), and a
description (last column preceded by \#) followed by the unit of the
statistic.

Most of the statistics are self explanatory from their descriptions. A
couple of important statistics are `sim_seconds` which is the total
simulated time for the simulation, `sim_insts` which is the number of
instructions committed by the CPU, and `host_inst_rate` which tells you
the performance of gem5.

Next, the SimObjects' statistics are printed. For instance, the CPU
statistics, which contains information on the number of syscalls,
statistics for cache system and translation buffers, etc.

    system.clk_domain.clock                          1000                       # Clock period in ticks (Tick)
    system.clk_domain.voltage_domain.voltage            1                       # Voltage in Volts (Volt)
    system.cpu.numCycles                            57467                       # Number of cpu cycles simulated (Cycle)
    system.cpu.numWorkItemsStarted                      0                       # Number of work items this cpu started (Count)
    system.cpu.numWorkItemsCompleted                    0                       # Number of work items this cpu completed (Count)
    system.cpu.dcache.demandHits::cpu.data           1941                       # number of demand (read+write) hits (Count)
    system.cpu.dcache.demandHits::total              1941                       # number of demand (read+write) hits (Count)
    system.cpu.dcache.overallHits::cpu.data          1941                       # number of overall hits (Count)
    system.cpu.dcache.overallHits::total             1941                       # number of overall hits (Count)
    system.cpu.dcache.demandMisses::cpu.data          133                       # number of demand (read+write) misses (Count)
    system.cpu.dcache.demandMisses::total             133                       # number of demand (read+write) misses (Count)
    system.cpu.dcache.overallMisses::cpu.data          133                       # number of overall misses (Count)
    system.cpu.dcache.overallMisses::total            133                       # number of overall misses (Count)
    system.cpu.dcache.demandMissLatency::cpu.data     14301000                       # number of demand (read+write) miss ticks (Tick)
    system.cpu.dcache.demandMissLatency::total     14301000                       # number of demand (read+write) miss ticks (Tick)
    system.cpu.dcache.overallMissLatency::cpu.data     14301000                       # number of overall miss ticks (Tick)
    system.cpu.dcache.overallMissLatency::total     14301000                       # number of overall miss ticks (Tick)
    system.cpu.dcache.demandAccesses::cpu.data         2074                       # number of demand (read+write) accesses (Count)
    system.cpu.dcache.demandAccesses::total          2074                       # number of demand (read+write) accesses (Count)
    system.cpu.dcache.overallAccesses::cpu.data         2074                       # number of overall (read+write) accesses (Count)
    system.cpu.dcache.overallAccesses::total         2074                       # number of overall (read+write) accesses (Count)
    system.cpu.dcache.demandMissRate::cpu.data     0.064127                       # miss rate for demand accesses (Ratio)
    system.cpu.dcache.demandMissRate::total      0.064127                       # miss rate for demand accesses (Ratio)
    system.cpu.dcache.overallMissRate::cpu.data     0.064127                       # miss rate for overall accesses (Ratio)
    system.cpu.dcache.overallMissRate::total     0.064127                       # miss rate for overall accesses (Ratio)
    system.cpu.dcache.demandAvgMissLatency::cpu.data 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.demandAvgMissLatency::total 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.overallAvgMissLatency::cpu.data 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.overallAvgMissLatency::total 107526.315789                       # average overall miss latency ((Cycle/Count))
    ...
    system.cpu.mmu.dtb.rdAccesses                    1123                       # TLB accesses on read requests (Count)
    system.cpu.mmu.dtb.wrAccesses                     953                       # TLB accesses on write requests (Count)
    system.cpu.mmu.dtb.rdMisses                        11                       # TLB misses on read requests (Count)
    system.cpu.mmu.dtb.wrMisses                         9                       # TLB misses on write requests (Count)
    system.cpu.mmu.dtb.walker.power_state.pwrStateResidencyTicks::UNDEFINED     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.mmu.itb.rdAccesses                       0                       # TLB accesses on read requests (Count)
    system.cpu.mmu.itb.wrAccesses                    7940                       # TLB accesses on write requests (Count)
    system.cpu.mmu.itb.rdMisses                         0                       # TLB misses on read requests (Count)
    system.cpu.mmu.itb.wrMisses                        37                       # TLB misses on write requests (Count)
    system.cpu.mmu.itb.walker.power_state.pwrStateResidencyTicks::UNDEFINED     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.power_state.pwrStateResidencyTicks::ON     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.thread_0.numInsts                        0                       # Number of Instructions committed (Count)
    system.cpu.thread_0.numOps                          0                       # Number of Ops committed (Count)
    system.cpu.thread_0.numMemRefs                      0                       # Number of Memory References (Count)
    system.cpu.workload.numSyscalls                    11                       # Number of system calls (Count)

Later in the file is memory controller statistics. This has information like
the bytes read by each component and the average bandwidth used by those
components.

    system.mem_ctrl.bytesReadWrQ                        0                       # Total number of bytes read from write queue (Byte)
    system.mem_ctrl.bytesReadSys                    23168                       # Total read bytes from the system interface side (Byte)
    system.mem_ctrl.bytesWrittenSys                     0                       # Total written bytes from the system interface side (Byte)
    system.mem_ctrl.avgRdBWSys               403153113.96105593                       # Average system read bandwidth in Byte/s ((Byte/Second))
    system.mem_ctrl.avgWrBWSys                 0.00000000                       # Average system write bandwidth in Byte/s ((Byte/Second))
    system.mem_ctrl.totGap                       57336000                       # Total gap between requests (Tick)
    system.mem_ctrl.avgGap                      158386.74                       # Average gap between requests ((Tick/Count))
    system.mem_ctrl.requestorReadBytes::cpu.inst        14656                       # Per-requestor bytes read from memory (Byte)
    system.mem_ctrl.requestorReadBytes::cpu.data         8512                       # Per-requestor bytes read from memory (Byte)
    system.mem_ctrl.requestorReadRate::cpu.inst 255033323.472601681948                       # Per-requestor bytes read from memory rate ((Byte/Second))
    system.mem_ctrl.requestorReadRate::cpu.data 148119790.488454252481                       # Per-requestor bytes read from memory rate ((Byte/Second))
    system.mem_ctrl.requestorReadAccesses::cpu.inst          229                       # Per-requestor read serviced memory accesses (Count)
    system.mem_ctrl.requestorReadAccesses::cpu.data          133                       # Per-requestor read serviced memory accesses (Count)
    system.mem_ctrl.requestorReadTotalLat::cpu.inst      6234000                       # Per-requestor read total memory access latency (Tick)
    system.mem_ctrl.requestorReadTotalLat::cpu.data      4141000                       # Per-requestor read total memory access latency (Tick)
    system.mem_ctrl.requestorReadAvgLat::cpu.inst     27222.71                       # Per-requestor read average memory access latency ((Tick/Count))
    system.mem_ctrl.requestorReadAvgLat::cpu.data     31135.34                       # Per-requestor read average memory access latency ((Tick/Count))
    system.mem_ctrl.dram.bytesRead::cpu.inst        14656                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesRead::cpu.data         8512                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesRead::total           23168                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesInstRead::cpu.inst        14656                       # Number of instructions bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesInstRead::total        14656                       # Number of instructions bytes read from this memory (Byte)
    system.mem_ctrl.dram.numReads::cpu.inst           229                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.numReads::cpu.data           133                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.numReads::total              362                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.bwRead::cpu.inst       255033323                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwRead::cpu.data       148119790                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwRead::total          403153114                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwInstRead::cpu.inst    255033323                       # Instruction read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwInstRead::total      255033323                       # Instruction read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::cpu.inst      255033323                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::cpu.data      148119790                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::total         403153114                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.readBursts                   362                       # Number of DRAM read bursts (Count)
    system.mem_ctrl.dram.writeBursts                    0                       # Number of DRAM write bursts (Count)


---


## Using the default configuration scripts

*Source: https://www.gem5.org/documentation/learning_gem5/part1/example_configs/*

gem5 v24.1: Using the gem5 standard library configuration scripts
=================================================================

The introduction of the gem5 standard library has changed the way
that gem5 configuration scripts are written. Many of the older
configuration scripts mentioned in the gem5 v21.0 section below are
now deprecated in favor of configuration scripts for the gem5 standard
library, located at `configs/example/gem5_library`.

A brief look at the directory structure is as follows:

```txt
gem5_library
    |
    |- caches       #contains a configuration script for the octopi cache
    |
    |- checkpoints  #scripts for taking and restoring from checkpoints
    |
    |- dramsys      #scripts for using gem5 with dramsys
    |
    |- looppoints   #scripts for taking and restoring from looppoints
    |
    |- multisim     #scripts for launching multiple simulations at once using multisim
    |
    |- spatter_gen  #scripts for SpatterGen
    |
    |- (various example configuration scripts not sorted into a subdirectory)

```

The example configuration scripts placed directly in the gem5_library directory
are similar to what you've seen in previous parts of Learning gem5, but with more
variety, e.g. different ISAs, boards, and workloads. The source for these scripts
can be viewed [here](https://github.com/gem5/gem5/tree/stable/configs/example/gem5_library).

gem5 v21.0: Using the default configuration scripts
=======================================

In this chapter, we'll explore using the default configuration scripts
that come with gem5. gem5 ships with many configuration scripts that
allow you to use gem5 very quickly. However, a common pitfall is to use
these scripts without fully understanding what is being simulated. It is
important when doing computer architecture research with gem5 to fully
understand the system you are simulating. This chapter will walk you
through some important options and parts of the default configuration
scripts.

In the last few chapters you have created your own configuration scripts
from scratch. This is very powerful, as it allows you to specify every
single system parameter. However, some systems are very complex to set
up (e.g., a full-system ARM or x86 machine). Luckily, the gem5
developers have provided many scripts to bootstrap the process of
building systems.

A tour of the directory structure
---------------------------------

All of gem5's configuration files can be found in `configs/`. The
directory structure is shown below:

    configs/boot:
    bbench-gb.rcS  bbench-ics.rcS  hack_back_ckpt.rcS  halt.sh

    configs/common:
    Benchmarks.py   Caches.py  cpu2000.py    FileSystemConfig.py  GPUTLBConfig.py   HMC.py       MemConfig.py   Options.py     Simulation.py
    CacheConfig.py  cores      CpuConfig.py  FSConfig.py          GPUTLBOptions.py  __init__.py  ObjectList.py  SimpleOpts.py  SysPaths.py

    configs/dist:
    sw.py

    configs/dram:
    lat_mem_rd.py  low_power_sweep.py  sweep.py

    configs/example:
    apu_se.py  etrace_replay.py  garnet_synth_traffic.py  hmctest.py    hsaTopology.py  memtest.py  read_config.py  ruby_direct_test.py      ruby_mem_test.py     sc_main.py
    arm        fs.py             hmc_hello.py             hmc_tgen.cfg  memcheck.py     noc_config  riscv           ruby_gpu_random_test.py  ruby_random_test.py  se.py

    configs/learning_gem5:
    part1  part2  part3  README

    configs/network:
    __init__.py  Network.py

    configs/nvm:
    sweep_hybrid.py  sweep.py

    configs/ruby:
    AMD_Base_Constructor.py  CHI.py        Garnet_standalone.py  __init__.py              MESI_Three_Level.py  MI_example.py      MOESI_CMP_directory.py  MOESI_hammer.py
    CHI_config.py            CntrlBase.py  GPU_VIPER.py          MESI_Three_Level_HTM.py  MESI_Two_Level.py    MOESI_AMD_Base.py  MOESI_CMP_token.py      Ruby.py

    configs/splash2:
    cluster.py  run.py

    configs/topologies:
    BaseTopology.py  Cluster.py  CrossbarGarnet.py  Crossbar.py  CustomMesh.py  __init__.py  MeshDirCorners_XY.py  Mesh_westfirst.py  Mesh_XY.py  Pt2Pt.py

Each directory is briefly described below:

**boot/**
:   These are rcS files which are used in full-system mode. These files
    are loaded by the simulator after Linux boots and are executed by
    the shell. Most of these are used to control benchmarks when running
    in full-system mode. Some are utility functions, like
    `hack_back_ckpt.rcS`. These files are covered in more depth in the
    chapter on full-system simulation.

**common/**
:   This directory contains a number of helper scripts and functions to
    create simulated systems. For instance, `Caches.py` is similar to
    the `caches.py` and `caches_opts.py` files created in previous
    chapters.

    `Options.py` contains a variety of options that can be set on the
    command line. Like the number of CPUs, system clock, and many, many
    more. This is a good place to look to see if the option you want to
    change already has a command line parameter.

    `CacheConfig.py` contains the options and functions for setting
    cache parameters for the classic memory system.

    `MemConfig.py` provides some helper functions for setting the memory
    system.

    `FSConfig.py` contains the necessary functions to set up full-system
    simulation for many different kinds of systems. Full-system
    simulation is discussed further in it's own chapter.

    `Simulation.py` contains many helper functions to set up and run
    gem5. A lot of the code contained in this file manages saving and
    restoring checkpoints. The example configuration files below in
    `examples/` use the functions in this file to execute the gem5
    simulation. This file is quite complicated, but it also allows a lot
    of flexibility in how the simulation is run.

**dram/**
:   Contains scripts to test DRAM.

**example/**
:   This directory contains some example gem5 configuration scripts that
    can be used out-of-the-box to run gem5. Specifically, `se.py` and
    `fs.py` are quite useful. More on these files can be found in the
    next section. There are also some other utility configuration
    scripts in this directory.

**learning_gem5/**
:   This directory contains all gem5 configuration scripts found in the
    learning\_gem5 book.

**network/**
:   This directory contains the configurations scripts for a HeteroGarnet
    network.

**nvm/**
:   This directory contains example scripts using the NVM interface.

**ruby/**
:   This directory contains the configurations scripts for Ruby and its
    included cache coherence protocols. More details can be found in the
    chapter on Ruby.

**splash2/**
:   This directory contains scripts to run the splash2 benchmark suite
    with a few options to configure the simulated system.

**topologies/**
:   This directory contains the implementation of the topologies that
    can be used when creating the Ruby cache hierarchy. More details can
    be found in the chapter on Ruby.

Using `se.py` and `fs.py`
-------------------------

In this section, I'll discuss some of the common options that can be
passed on the command line to `se.py` and `fs.py`. More details on how
to run full-system simulation can be found in the full-system simulation
chapter. Here I'll discuss the options that are common to the two files.

Most of the options discussed in this section are found in Options.py
and are registered in the function `addCommonOptions`. This section does
not detail all of the options. To see all of the options, run the
configuration script with `--help`, or read the script's source code.

First, let's simply run the hello world program without any parameters:

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello
```

And we get the following as output:

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:33:42
    gem5 executing on amarillo, pid 85168
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 5943000 because exiting with last active thread context

However, this isn't a very interesting simulation at all! By default,
gem5 uses the atomic CPU and uses atomic memory accesses, so there's no
real timing data reported! To confirm this, you can look at
m5out/config.ini. The CPU is shown on line 51:

    [system.cpu]
    type=X86AtomicSimpleCPU
    children=interrupts isa mmu power_state tracer workload
    branchPred=Null
    checker=Null
    clk_domain=system.cpu_clk_domain
    cpu_id=0
    do_checkpoint_insts=true
    do_statistics_insts=true

To actually run gem5 in timing mode, let's specify a CPU type. While
we're at it, we can also specify sizes for the L1 caches.

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:36:10
    gem5 executing on amarillo, pid 85269
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 454646000 because exiting with last active thread context

Now, let's check the config.ini file and make sure that these options
propagated correctly to the final system. If you search
`m5out/config.ini` for "cache", you'll find that no caches were created!
Even though we specified the size of the caches, we didn't specify that
the system should use caches, so they weren't created. The correct
command line should be:

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB --caches
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:37:03
    gem5 executing on amarillo, pid 85560
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB --caches

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 31680000 because exiting with last active thread context

On the last line, we see that the total time went from 454646000 ticks
to 31680000, much faster! Looks like caches are probably enabled now.
But, it's always a good idea to double check the `config.ini` file.

    [system.cpu.dcache]
    type=Cache
    children=power_state replacement_policy tags
    addr_ranges=0:18446744073709551615
    assoc=2
    clk_domain=system.cpu_clk_domain
    clusivity=mostly_incl
    compressor=Null
    data_latency=2
    demand_mshr_reserve=1
    eventq_index=0
    is_read_only=false
    max_miss_count=0
    move_contractions=true
    mshrs=4
    power_model=
    power_state=system.cpu.dcache.power_state
    prefetch_on_access=false
    prefetcher=Null
    replace_expansions=true
    replacement_policy=system.cpu.dcache.replacement_policy
    response_latency=2
    sequential_access=false
    size=65536
    system=system
    tag_latency=2
    tags=system.cpu.dcache.tags
    tgts_per_mshr=20
    warmup_percentage=0
    write_allocator=Null
    write_buffers=8
    writeback_clean=false
    cpu_side=system.cpu.dcache_port
    mem_side=system.membus.cpu_side_ports[2]

Some common options `se.py` and `fs.py`
---------------------------------------

All of the possible options are printed when you run:

```
build/X86/gem5.opt configs/example/se.py --help
```

Below are a few important options from that list:


* `--cpu-type=CPU_TYPE`

    * The type of cpu to run with. This is an important parameter to always set. The default is atomic, which doesn’t perform a timing simulation.

* `--sys-clock=SYS_CLOCK`

    * Top-level clock for blocks running at system speed.

* `--cpu-clock=CPU_CLOCK`

    * Clock for blocks running at CPU speed. This is separate from the system clock above.

* `--mem-type=MEM_TYPE`

    * Type of memory to use. Options include different DDR memories, and the ruby memory controller.

* `--caches`

    * Perform the simulation with classic caches.

* `--l2cache`

    * Perform the simulation with an L2 cache, if using classic caches.

* `--ruby`

    * Use Ruby instead of the classic caches as the cache system simulation.

* `-m TICKS, --abs-max-tick=TICKS`

    * Run to absolute simulated tick specified including ticks from a restored checkpoint. This is useful if you only want simulate for a certain amount of simulated time.

* `-I MAXINSTS, --maxinsts=MAXINSTS`

    * Total number of instructions to simulate (default: run forever). This is useful if you want to stop simulation after a certain number of instructions has been executed.

* `-c CMD, --cmd=CMD`

    * The binary to run in syscall emulation mode.

* `-o OPTIONS, --options=OPTIONS`

    * The options to pass to the binary, use ” ” around the entire string. This is useful when you are running a command which takes options. You can pass both arguments and options (e.g., –whatever) through this variable.

* `--output=OUTPUT`

    * Redirect stdout to a file. This is useful if you want to redirect the output of the simulated application to a file instead of printing to the screen. Note: to redirect gem5 output, you have to pass a parameter before the configuration script.

* `--errout=ERROUT`

    * Redirect stderr to a file. Similar to above.


---


## Extending gem5 for ARM

*Source: https://www.gem5.org/documentation/learning_gem5/part1/extending_configs*

Extending gem5 for ARM
======================

This chapter assumes you've already built a basic x86 system with
gem5 and created a simple configuration script.

Downloading ARM Binaries
------------------------

Let's start by downloading some ARM benchmark binaries. Begin
from the root of the gem5 folder:

```
mkdir -p cpu_tests/benchmarks/bin/arm
cd cpu_tests/benchmarks/bin/arm
wget dist.gem5.org/dist/v22-0/test-progs/cpu-tests/bin/arm/Bubblesort
wget dist.gem5.org/dist/v22-0/test-progs/cpu-tests/bin/arm/FloatMM
```

We'll use these to further test our ARM system.

Building gem5 to run ARM Binaries
---------------------------------

Just as we did when we first built our basic x86 system, we run
the same command, except this time we want it to compile with the
default ARM configurations. To do so, we just replace x86 with ARM:  

```
scons build/ARM/gem5.opt -j 20
```

When compilation is finished you should have a working gem5 executable
at `build/ARM/gem5.opt`.

Modifying simple.py to run ARM Binaries
---------------------------------------

Before we can run any ARM binaries with our new system, we'll have
to make a slight tweak to our simple.py.

If you recall when we created our simple configuration script, it was
noted that we did not have to connect the PIO and interrupt ports to
the memory bus for any ISA other than for an x86 system. So let's
remove those 3 lines:

```
system.cpu.createInterruptController()
#system.cpu.interrupts[0].pio = system.membus.mem_side_ports
#system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
#system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports
```

You can either delete or comment them out as above. Next let's set
the processes command to one of our ARM benchmark binaries:

```
process.cmd = ['cpu_tests/benchmarks/bin/arm/Bubblesort']
```

If you'd like to test a simple hello program as before, just
replace x86 with arm:

```
process.cmd = ['tests/test-progs/hello/bin/arm/linux/hello']
```

Running gem5
------------

Simply run it as before, except replace X86 with ARM:

```
build/ARM/gem5.opt configs/tutorial/simple.py
```

If you set your process to be the Bubblesort benchmark, your
output should look like this:

```
gem5 Simulator System.  http://gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 compiled Oct  3 2019 16:02:35
gem5 started Oct  6 2019 13:22:25
gem5 executing on amarillo, pid 77129
command line: build/ARM/gem5.opt configs/tutorial/simple.py

Global frequency set at 1000000000000 ticks per second
warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
0: system.remote_gdb: listening for remote gdb on port 7002
Beginning simulation!
info: Entering event queue @ 0.  Starting simulation...
info: Increasing stack size by one page.
warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
      Returning '/home/jtoya/gem5/cpu_tests/benchmarks/bin/arm/Bubblesort'
-50000
Exiting @ tick 258647411000 because exiting with last active thread context
```

ARM Full System Simulation
--------------------------
To run an ARM FS Simulation, there are some changes required to the setup.

If you haven't already, from the gem5 repository's root directory, `cd` into
the directory `util/term/` by running

```bash
$ cd util/term/
```

and then compile the `m5term` binary by running

```bash
$ make
```

The gem5 repository comes with example system setups and configurations. These
can be found in the `configs/example/arm/` directory.

A collection of full system Linux image files are available
[here](https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries).
Save these in a directory and remember the path to it. For example, you could
store them in

```
/path/to/user/gem5/fs_images/
```

The `fs_images` directory will be assumed to contain the extracted FS images
for the rest of this example.

With the image(s) downloaded, execute the following command in your terminal:

```bash
$ export IMG_ROOT=/absolute/path/to/fs_images/<image-directory-name>
```

replacing "\<image-directory-name\>" with the name of the directory extracted
from the downloaded image file, without the angle-brackets.

We are now ready to run a FS ARM simulation. From the root of the gem5
repository, run:

```bash
$ ./build/ARM/gem5.opt configs/example/arm/fs_bigLITTLE.py \
    --caches \
    --bootloader="$IMG_ROOT/binaries/<bootloader-name>" \
    --kernel="$IMG_ROOT/binaries/<kernel-name>" \
    --disk="$IMG_ROOT/disks/<disk-image-name>" \
    --bootscript=path/to/bootscript.rcS
```

replacing anything in angle-brackets with the name of the directory or file,
without the angle-brackets.

You can then attach to the simulation by, in a different terminal window,
running:

```bash
$ ./util/term/m5term 3456
```

The full details of what the `fs_bigLITTLE.py` script supports can be gotten by
running:

```bash
$ ./build/ARM/gem5.opt configs/example/arm/fs_bigLITTLE.py --help
```

> **An aside on FS simulations:**
>
> Note that FS simulations take a long time; like "1 hour to load the kernel"
> long time! There are ways to "fast-forward" a simulation and then resume the
> detailed simulation at the interesting point, but these are beyond the scope
> of this chapter.


---


# ═══ Modifying / Extending gem5 ═══


## Setting up your development environment

*Source: https://www.gem5.org/documentation/learning_gem5/part2/environment/*

Setting up your development environment
=======================================

This is going to talk about getting started developing gem5.

gem5-style guidelines
---------------------

When modifying any open source project, it is important to follow the
project's style guidelines. Details on gem5 style can be found on the
gem5 [Coding Style page](http://www.gem5.org/documentation/general_docs/development/coding_style/).

To help you conform to the style guidelines, gem5 includes a script
which runs whenever you commit a changeset in git. This script should be
automatically added to your .git/config file by SCons the first time you
build gem5. Please do not ignore these warnings/errors. However, in the
rare case where you are trying to commit a file that doesn't conform to
the gem5 style guidelines (e.g., something from outside the gem5 source
tree) you can use the git option `--no-verify` to skip running the style
checker.

The key takeaways from the style guide are:

-   Use 4 spaces, not tabs
-   Sort the includes
-   Use capitalized camel case for class names, camel case for member
    variables and functions, and snake case for local variables.
-   Document your code

git branches
------------

Most people developing with gem5 use the branch feature of git to track
their changes. This makes it quite simple to commit your changes back to
gem5. Additionally, using branches can make it easier to update gem5
with new changes that other people make while keeping your own changes
separate. The [Git book](https://git-scm.com/book/en/v2) has a great
[chapter](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
describing the details of how to use branches.


---


## Creating a very simple SimObject

*Source: https://www.gem5.org/documentation/learning_gem5/part2/helloobject/*

Creating a *very* simple SimObject
==================================

**Note**: gem5 has SimObject named `SimpleObject`. Implementing another
`SimpleObject` SimObject will result in confusing compiler issues.

Almost all objects in gem5 inherit from the base SimObject type.
SimObjects export the main interfaces to all objects in gem5. SimObjects
are wrapped `C++` objects that are accessible from the `Python`
configuration scripts.

SimObjects can have many parameters, which are set via the `Python`
configuration files. In addition to simple parameters like integers and
floating point numbers, they can also have other SimObjects as
parameters. This allows you to create complex system hierarchies, like
real machines.

In this chapter, we will walk through creating a simple "HelloWorld"
SimObject. The goal is to introduce you to how SimObjects are created
and the required boilerplate code for all SimObjects. We will also
create a simple `Python` configuration script which instantiates our
SimObject.

In the next few chapters, we will take this simple SimObject and expand
on it to include [debugging support](../debugging), [dynamic
events](../events), and [parameters](../parameters).

> **Using git branches**
>
> It is common to use a new git branch for each new feature you add to
> gem5.
>
> The first step when adding a new feature or modifying something in
> gem5, is to create a new branch to store your changes. Details on git
> branches can be found in the Git book.
>
> ```
> git checkout -b hello-simobject
> ```

Step 1: Create a Python class for your new SimObject
----------------------------------------------------

Each SimObject has a Python class which is associated with it. This
Python class describes the parameters of your SimObject that can be
controlled from the Python configuration files. For our simple
SimObject, we are just going to start out with no parameters. Thus, we
simply need to declare a new class for our SimObject and set it's name
and the C++ header that will define the C++ class for the SimObject.

We can create a file, `HelloObject.py`, in `src/learning_gem5/part2`.
If you have cloned the gem5 repository you'll have the files mentioned
in this tutorial completed under `src/learning_gem5/part2` and
`configs/learning_gem5/part2`. You can delete these or move them
elsewhere to follow this tutorial.

```python
from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"
    cxx_class = "gem5::HelloObject"
```

[//]: # You can find the complete file
[//]: # [here](/_static/scripts/part2/helloobject/HelloObject.py)

It is not required that the `type` be the same as the name of the class,
but it is convention. The `type` is the C++ class that you are wrapping
with this Python SimObject. Only in special circumstances should the
`type` and the class name be different.

The `cxx_header` is the file that contains the declaration of the class
used as the `type` parameter. Again, the convention is to use the name
of the SimObject with all lowercase and underscores, but this is only
convention. You can specify any header file here.

The `cxx_class` is an attribute specifying the newly created SimObject
is declared within the gem5 namespace. Most SimObjects in the gem5 code
base are declared within the gem5 namespace!

Step 2: Implement your SimObject in C++
---------------------------------------

Next, we need to create `hello_object.hh` and `hello_object.cc` in
`src/learning_gem5/part2/` directory which will implement the `HelloObject`.

We'll start with the header file for our `C++` object. By convention,
gem5 wraps all header files in `#ifndef/#endif` with the name of the
file and the directory its in so there are no circular includes.

SimObjects should be declared within the gem5 namespace. Therefore,
we declare our class within the `namespace gem5` scope.

The only thing we need to do in the file is to declare our class. Since
`HelloObject` is a SimObject, it must inherit from the C++ SimObject
class. Most of the time, your SimObject's parent will be a subclass of
SimObject, not SimObject itself.

The SimObject class specifies many virtual functions. However, none of
these functions are pure virtual, so in the simplest case, there is no
need to implement any functions except for the constructor.

The constructor for all SimObjects assumes it will take a parameter
object. This parameter object is automatically created by the build
system and is based on the `Python` class for the SimObject, like the
one we created above. The name for this parameter type is generated
automatically from the name of your object. For our "HelloObject" the
parameter type's name is "HelloObjectParams".

The code required for our simple header file is listed below.

```cpp
#ifndef __LEARNING_GEM5_HELLO_OBJECT_HH__
#define __LEARNING_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

namespace gem5
{

class HelloObject : public SimObject
{
  public:
    HelloObject(const HelloObjectParams &p);
};

} // namespace gem5

#endif // __LEARNING_GEM5_HELLO_OBJECT_HH__
```

[//]: # You can find the complete file
[//]: # [here](/_pages/static/scripts/part2/helloobject/hello_object.hh).

Next, we need to implement *two* functions in the `.cc` file, not just
one. The first function, is the constructor for the `HelloObject`. Here
we simply pass the parameter object to the SimObject parent and print
"Hello world!"

Normally, you would **never** use `std::cout` in gem5. Instead, you
should use debug flags. In the [next chapter](../debugging), we
will modify this to use debug flags instead. However, for now, we'll
simply use `std::cout` because it is simple.

```cpp
#include "learning_gem5/part2/hello_object.hh"

#include <iostream>

namespace gem5
{

HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params)
{
    std::cout << "Hello World! From a SimObject!" << std::endl;
}

} // namespace gem5
```

**Note**: If the constructor of your SimObject follows the following
signature,

```cpp
Foo(const FooParams &)
```

then a `FooParams::create()` method will be automatically defined. The purpose
of the `create()` method is to call the SimObject constructor and return an
instance of the SimObject. Most SimObject will follow this pattern; however,
if your SimObject does not follow this pattern,
[the gem5 SimObject documetation](http://doxygen.gem5.org/release/current/classSimObject.html#details)
provides more information about manually implementing the `create()` method.


[//]: # You can find the complete file
[//]: # [here](/_pages/static/scripts/part2/helloobject/hello_object.cc).


Step 3: Register the SimObject and C++ file
-------------------------------------------

In order for the `C++` file to be compiled and the `Python` file to be
parsed we need to tell the build system about these files. gem5 uses
SCons as the build system, so you simply have to create a SConscript
file in the directory with the code for the SimObject. If there is
already a SConscript file for that directory, simply add the following
declarations to that file.

This file is simply a normal `Python` file, so you can write any
`Python` code you want in this file. Some of the scripting can become
quite complicated. gem5 leverages this to automatically create code for
SimObjects and to compile the domain-specific languages like SLICC and
the ISA language.

In the SConscript file, there are a number of functions automatically
defined after you import them. See the section on that...

To get your new SimObject to compile, you simply need to create a new
file with the name "SConscript" in the `src/learning_gem5/part2` directory. In
this file, you have to declare the SimObject and the `.cc` file. Below
is the required code.

```python
Import('*')

SimObject('HelloObject.py', sim_objects=['HelloObject'])
Source('hello_object.cc')
```

[//]: # You can find the complete file
[//]: # [here](/_pages/static/scripts/part2/helloobject/SConscript).

Step 4: (Re)-build gem5
-----------------------

To compile and link your new files you simply need to recompile gem5.
The below example assumes you are using the x86 ISA, but nothing in our
object requires an ISA so, this will work with any of gem5's ISAs.

```
scons build/ALL/gem5.opt
```

Step 5: Create the config scripts to use your new SimObject
-----------------------------------------------------------

Now that you have implemented a SimObject, and it has been compiled into
gem5, you need to create or modify a `Python` config file `run_hello.py` in
`configs/learning_gem5/part2` to instantiate your object. Since your object
is very simple a system object is not required! CPUs are not needed, or
caches, or anything, except a `Root` object. All gem5 instances require a
`Root` object.

Walking through creating a *very* simple configuration script, first,
import m5 and all of the objects you have compiled.

```python
import m5
from m5.objects import *
```

Next, you have to instantiate the `Root` object, as required by all gem5
instances.

```python
root = Root(full_system = False)
```

Now, you can instantiate the `HelloObject` you created. All you need to
do is call the `Python` "constructor". Later, we will look at how to
specify parameters via the `Python` constructor. In addition to creating
an instantiation of your object, you need to make sure that it is a
child of the root object. Only SimObjects that are children of the
`Root` object are instantiated in `C++`.

```python
root.hello = HelloObject()
```

Finally, you need to call `instantiate` on the `m5` module and actually
run the simulation!

```python
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
```

[//]: # You can find the complete file
[//]: # [here](/_pages/static/scripts/part2/helloobject/run_hello.py).

Remember to rebuild gem5 after modifying files in the src/ directory. The
command line to run the config file is in the output below after
'command line:'. The output should look something like the following:

Note: If the code for the future section "Adding parameters to SimObjects
and more events", (goodbye_object) is in your `src/learning_gem5/part2`
directory, run_hello.py will cause an error. If you delete those files or
move them outside of the gem5 directory `run_hello.py` should give the output
below.
```
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled May  4 2016 11:37:41
    gem5 started May  4 2016 11:44:28
    gem5 executing on mustardseed.cs.wisc.edu, pid 22480
    command line: build/X86/gem5.opt configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
    Hello World! From a SimObject!
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Exiting @ tick 18446744073709551615 because simulate() limit reached
```
Congrats! You have written your first SimObject. In the next chapters,
we will extend this SimObject and explore what you can do with
SimObjects.


---


## Debugging gem5

*Source: https://www.gem5.org/documentation/learning_gem5/part2/debugging/*

Debugging gem5
==============

In the [previous chapters](../helloobject) we covered how to
create a very simple SimObject. In this chapter, we will replace the
simple print to `stdout` with gem5's debugging support.

gem5 provides support for `printf`-style tracing/debugging of your code
via *debug flags*. These flags allow every component to have many
debug-print statements, without all of them enabled at the same time.
When running gem5, you can specify which debug flags to enable from the
command line.

Using debug flags
-----------------

For instance, when running the first simple.py script from
simple-config-chapter, if you enable the `DRAM` debug flag, you get the
following output. Note that this generates *a lot* of output to the
console (about 7 MB).

```
    build/ALL/gem5.opt --debug-flags=DRAM configs/learning_gem5/part1/simple.py | head -n 50
```

    gem5 Simulator System.  http://gem5.org
    DRAM device capacity (gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  3 2017 16:03:38
    gem5 started Jan  3 2017 16:09:53
    gem5 executing on chinook, pid 19223
    command line: build/X86/gem5.opt --debug-flags=DRAM configs/learning_gem5/part1/simple.py

    Global frequency set at 1000000000000 ticks per second
          0: system.mem_ctrl: Memory capacity 536870912 (536870912) bytes
          0: system.mem_ctrl: Row buffer size 8192 bytes with 128 columns per row buffer
          0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
          0: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
          0: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
          0: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
          0: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
          0: system.mem_ctrl: Adding to read queue
          0: system.mem_ctrl: Request scheduled immediately
          0: system.mem_ctrl: Single request, going to a free rank
          0: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
          0: system.mem_ctrl: Activate at tick 0
          0: system.mem_ctrl: Activate bank 0, rank 0 at tick 0, now got 1 active
          0: system.mem_ctrl: Access to 400, ready at 46250 bus busy until 46250.
      46250: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
      46250: system.mem_ctrl: number of read entries for rank 0 is 0
      46250: system.mem_ctrl: Responding to Address 400..   46250: system.mem_ctrl: Done
      77000: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
      77000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
      77000: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
      77000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
      77000: system.mem_ctrl: Adding to read queue
      77000: system.mem_ctrl: Request scheduled immediately
      77000: system.mem_ctrl: Single request, going to a free rank
      77000: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
      77000: system.mem_ctrl: Access to 400, ready at 101750 bus busy until 101750.
     101750: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
     101750: system.mem_ctrl: number of read entries for rank 0 is 0
     101750: system.mem_ctrl: Responding to Address 400..  101750: system.mem_ctrl: Done
     132000: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
     132000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
     132000: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
     132000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
     132000: system.mem_ctrl: Adding to read queue
     132000: system.mem_ctrl: Request scheduled immediately
     132000: system.mem_ctrl: Single request, going to a free rank
     132000: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
     132000: system.mem_ctrl: Access to 400, ready at 156750 bus busy until 156750.
     156750: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
     156750: system.mem_ctrl: number of read entries for rank 0 is 0

Or, you may want to debug based on the exact instruction the CPU is
executing. For this, the `Exec` debug flag may be useful. This debug
flags shows details of how each instruction is executed by the simulated
CPU.

```
    build/ALL/gem5.opt --debug-flags=Exec configs/learning_gem5/part1/simple.py | head -n 50
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  3 2017 16:03:38
    gem5 started Jan  3 2017 16:11:47
    gem5 executing on chinook, pid 19234
    command line: build/X86/gem5.opt --debug-flags=Exec configs/learning_gem5/part1/simple.py

    Global frequency set at 1000000000000 ticks per second
          0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    warn: ClockedObject: More than one power state change request encountered within the same simulation tick
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
      77000: system.cpu T0 : @_start    : xor   rbp, rbp
      77000: system.cpu T0 : @_start.0  :   XOR_R_R : xor   rbp, rbp, rbp : IntAlu :  D=0x0000000000000000
     132000: system.cpu T0 : @_start+3    : mov r9, rdx
     132000: system.cpu T0 : @_start+3.0  :   MOV_R_R : mov   r9, r9, rdx : IntAlu :  D=0x0000000000000000
     187000: system.cpu T0 : @_start+6    : pop rsi
     187000: system.cpu T0 : @_start+6.0  :   POP_R : ld   t1, SS:[rsp] : MemRead :  D=0x0000000000000001 A=0x7fffffffee30
     250000: system.cpu T0 : @_start+6.1  :   POP_R : addi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee38
     250000: system.cpu T0 : @_start+6.2  :   POP_R : mov   rsi, rsi, t1 : IntAlu :  D=0x0000000000000001
     360000: system.cpu T0 : @_start+7    : mov rdx, rsp
     360000: system.cpu T0 : @_start+7.0  :   MOV_R_R : mov   rdx, rdx, rsp : IntAlu :  D=0x00007fffffffee38
     415000: system.cpu T0 : @_start+10    : and    rax, 0xfffffffffffffff0
     415000: system.cpu T0 : @_start+10.0  :   AND_R_I : limm   t1, 0xfffffffffffffff0 : IntAlu :  D=0xfffffffffffffff0
     415000: system.cpu T0 : @_start+10.1  :   AND_R_I : and   rsp, rsp, t1 : IntAlu :  D=0x0000000000000000
     470000: system.cpu T0 : @_start+14    : push   rax
     470000: system.cpu T0 : @_start+14.0  :   PUSH_R : st   rax, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x0000000000000000 A=0x7fffffffee28
     491000: system.cpu T0 : @_start+14.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee28
     546000: system.cpu T0 : @_start+15    : push   rsp
     546000: system.cpu T0 : @_start+15.0  :   PUSH_R : st   rsp, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x00007fffffffee28 A=0x7fffffffee20
     567000: system.cpu T0 : @_start+15.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee20
     622000: system.cpu T0 : @_start+16    : mov    r15, 0x40a060
     622000: system.cpu T0 : @_start+16.0  :   MOV_R_I : limm   r8, 0x40a060 : IntAlu :  D=0x000000000040a060
     732000: system.cpu T0 : @_start+23    : mov    rdi, 0x409ff0
     732000: system.cpu T0 : @_start+23.0  :   MOV_R_I : limm   rcx, 0x409ff0 : IntAlu :  D=0x0000000000409ff0
     842000: system.cpu T0 : @_start+30    : mov    rdi, 0x400274
     842000: system.cpu T0 : @_start+30.0  :   MOV_R_I : limm   rdi, 0x400274 : IntAlu :  D=0x0000000000400274
     952000: system.cpu T0 : @_start+37    : call   0x9846
     952000: system.cpu T0 : @_start+37.0  :   CALL_NEAR_I : limm   t1, 0x9846 : IntAlu :  D=0x0000000000009846
     952000: system.cpu T0 : @_start+37.1  :   CALL_NEAR_I : rdip   t7, %ctrl153,  : IntAlu :  D=0x00000000004001ba
     952000: system.cpu T0 : @_start+37.2  :   CALL_NEAR_I : st   t7, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x00000000004001ba A=0x7fffffffee18
     973000: system.cpu T0 : @_start+37.3  :   CALL_NEAR_I : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee18
     973000: system.cpu T0 : @_start+37.4  :   CALL_NEAR_I : wrip   , t7, t1 : IntAlu :
    1042000: system.cpu T0 : @__libc_start_main    : push   r15
    1042000: system.cpu T0 : @__libc_start_main.0  :   PUSH_R : st   r15, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x0000000000000000 A=0x7fffffffee10
    1063000: system.cpu T0 : @__libc_start_main.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee10
    1118000: system.cpu T0 : @__libc_start_main+2    : movsxd   rax, rsi
    1118000: system.cpu T0 : @__libc_start_main+2.0  :   MOVSXD_R_R : sexti   rax, rsi, 0x1f : IntAlu :  D=0x0000000000000001
    1173000: system.cpu T0 : @__libc_start_main+5    : mov  r15, r9
    1173000: system.cpu T0 : @__libc_start_main+5.0  :   MOV_R_R : mov   r15, r15, r9 : IntAlu :  D=0x0000000000000000
    1228000: system.cpu T0 : @__libc_start_main+8    : push r14

In fact, the `Exec` flag is actually an agglomeration of multiple debug
flags. You can see this, and all of the available debug flags, by
running gem5 with the `--debug-help` parameter.

```
    build/ALL/gem5.opt --debug-help
```

    Base Flags:
        Activity: None
        AddrRanges: None
        Annotate: State machine annotation debugging
        AnnotateQ: State machine annotation queue debugging
        AnnotateVerbose: Dump all state machine annotation details
        BaseXBar: None
        Branch: None
        Bridge: None
        CCRegs: None
        CMOS: Accesses to CMOS devices
        Cache: None
        CacheComp: None
        CachePort: None
        CacheRepl: None
        CacheTags: None
        CacheVerbose: None
        Checker: None
        Checkpoint: None
        ClockDomain: None
    ...
    Compound Flags:
        All: Controls all debug flags. It should not be used within C++ code.
            All Base Flags
        AnnotateAll: All Annotation flags
            Annotate, AnnotateQ, AnnotateVerbose
        CacheAll: None
            Cache, CacheComp, CachePort, CacheRepl, CacheVerbose, HWPrefetch
        DiskImageAll: None
            DiskImageRead, DiskImageWrite
    ...
    XBar: None
        BaseXBar, CoherentXBar, NoncoherentXBar, SnoopFilter

Adding a new debug flag
-----------------------

In the [previous chapters](../helloobject), we used a simple
`std::cout` to print from our SimObject. While it is possible to use the
normal C/C++ I/O in gem5, it is highly discouraged. So, we are now going
to replace this and use gem5's debugging facilities instead.

When creating a new debug flag, we first have to declare it in a
SConscript file. Add the following to the SConscript file in the
directory with your hello object code (`src/learning_gem5/SConscript`).

```python
DebugFlag('HelloExample')
```

This declares a debug flag of "HelloExample". Now, we can use this in debug
statements in our SimObject.

By declaring the flag in the SConscript file, a debug header is
automatically generated that allows us to use the debug flag. The header
file is in the `debug` directory and has the same name (and
capitalization) as what we declare in the SConscript file. Therefore, we
need to include the automatically generated header file in any files
where we plan to use the debug flag.

In the `hello_object.cc` file, we need to include the header file.

```cpp
#include "base/trace.hh"
#include "debug/HelloExample.hh"
```

Now that we have included the necessary header file, let's replace the
`std::cout` call with a debug statement like so.

```cpp
DPRINTF(HelloExample, "Created the hello object\n");
```

`DPRINTF` is a C++ macro. The first parameter is a *debug flag* that has
been declared in a SConscript file. We can use the flag `HelloExample` since we
declared it in the `src/learning_gem5/SConscript` file. The rest of the
arguments are variable and can be anything you would pass to a `printf`
statement.

Now, if you recompile gem5 and run it with the "HelloExample" debug flag, you
get the following result.

```
scons build/ALL/gem5.opt
build/ALL/gem5.opt --debug-flags=HelloExample configs/learning_gem5/part2/run_hello.py
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 09:40:10
    gem5 started Jan  4 2017 09:41:01
    gem5 executing on chinook, pid 29078
    command line: build/X86/gem5.opt --debug-flags=HelloExample configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Exiting @ tick 18446744073709551615 because simulate() limit reached

You can find the updated SConcript file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part2/SConscript)
and the updated hello object code
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part2/hello_object.cc).

Debug output
------------

For each dynamic `DPRINTF` execution, three things are printed to
`stdout`. First, the current tick when the `DPRINTF` is executed.
Second, the *name of the SimObject* that called `DPRINTF`. This name is
usually the Python variable name from the Python config file. However,
the name is whatever the SimObject `name()` function returns. Finally,
you see whatever format string you passed to the `DPRINTF` function.

You can control where the debug output goes with the `--debug-file`
parameter. By default, all of the debugging output is printed to
`stdout`. However, you can redirect the output to any file. The file is
stored relative to the main gem5 output directory, not the current
working directory.

Using functions other than DPRINTF
----------------------------------

`DPRINTF` is the most commonly used debugging function in gem5. However,
gem5 provides a number of other functions that are useful in specific
circumstances. All debugging functions are available in the
[reference documentation](http://doxygen.gem5.org/release/current/base_2trace_8hh.html).

> These functions are like the previous functions `:cppDDUMP`,
> `:cppDPRINTF`, and `:cppDPRINTFR` except they do not take a flag as a
> parameter. Therefore, these statements will *always* print whenever
> debugging is enabled.

All of these functions are only enabled if you compile gem5 in "opt" or
"debug" mode. All other modes use empty placeholder macros for the above
functions. Therefore, if you want to use debug flags, you must use
either "gem5.opt" or "gem5.debug".


---


## Event-driven programming

*Source: https://www.gem5.org/documentation/learning_gem5/part2/events/*

Event-driven programming
========================

gem5 is an event-driven simulator. In this chapter, we will explore how
to create and schedule events. We will be building from the simple
`HelloObject` from [hello-simobject-chapter](../helloobject).

Creating a simple event callback
--------------------------------

In gem5's event-driven model, each event has a callback function in
which the event is *processed*. Generally, this is a class that inherits
from :cppEvent. However, gem5 provides a wrapper function for creating
simple events.

In the header file for our `HelloObject`, we simply need to declare a
new function that we want to execute every time the event fires
(`processEvent()`). This function must take no parameters and return
nothing.

Next, we add an `Event` instance. In this case, we will use an
`EventFunctionWrapper` which allows us to execute any function.

We also add a `startup()` function that will be explained below.

```cpp
class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventFunctionWrapper event;

  public:
    HelloObject(const HelloObjectParams &p);

    void startup() override;
};
```

Next, we must construct this event in the constructor of `HelloObject`.
The `EventFuntionWrapper` takes two parameters, a function to execute
and a name. The name is usually the name of the SimObject that owns the
event. When printing the name, there will be an automatic
".wrapped\_function\_event" appended to the end of the name.

The first parameter is simply a function that takes no parameters and
has no return value (`std::function<void(void)>`). Usually, this is a
simple lambda function that calls a member function. However, it can be
any function you want. Below, we captute `this` in the lambda (`[this]`)
so we can call member functions of the instance of the class.

```cpp
HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params), event([this]{processEvent();}, name())
{
    DPRINTF(HelloExample, "Created the hello object\n");
}
```

We also must define the implementation of the process function. In this
case, we'll simply print something if we are debugging.

```cpp
void
HelloObject::processEvent()
{
    DPRINTF(HelloExample, "Hello world! Processing the event!\n");
}
```

Scheduling events
-----------------

Finally, for the event to be processed, we first have to *schedule* the
event. For this we use the :cppschedule function. This function
schedules some instance of an `Event` for some time in the future
(event-driven simulation does not allow events to execute in the past).

We will initially schedule the event in the `startup()` function we
added to the `HelloObject` class. The `startup()` function is where
SimObjects are allowed to schedule internal events. It does not get
executed until the simulation begins for the first time (i.e. the
`simulate()` function is called from a Python config file).

```cpp
void
HelloObject::startup()
{
    schedule(event, 100);
}
```

Here, we simply schedule the event to execute at tick 100. Normally, you
would use some offset from `curTick()`, but since we know the startup()
function is called when the time is currently 0, we can use an explicit
tick value.

The output when you run gem5 with the "HelloExample" debug flag is now

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 11:01:46
    gem5 started Jan  4 2017 13:41:38
    gem5 executing on chinook, pid 1834
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
        100: hello: Hello world! Processing the event!
    Exiting @ tick 18446744073709551615 because simulate() limit reached

More event scheduling
---------------------

We can also schedule new events within an event process action. For
instance, we are going to add a latency parameter to the `HelloObject`
and a parameter for how many times to fire the event. In the [next
chapter](parameters-chapter) we will make these parameters accessible
from the Python config files.

To the HelloObject class declaration, add a member variable for the
latency and number of times to fire.

```cpp
class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventFunctionWrapper event;

    const Tick latency;

    int timesLeft;

  public:
    HelloObject(const HelloObjectParams &p);

    void startup() override;
};
```

Then, in the constructor add default values for the `latency` and
`timesLeft`.

```cpp
HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params), event([this]{processEvent();}, name()),
    latency(100), timesLeft(10)
{
    DPRINTF(HelloExample, "Created the hello object\n");
}
```

Finally, update `startup()` and `processEvent()`.

```cpp
void
HelloObject::startup()
{
    schedule(event, latency);
}

void
HelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(HelloExample, "Hello world! Processing the event! %d left\n", timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(HelloExample, "Done firing!\n");
    } else {
        schedule(event, curTick() + latency);
    }
}
```

Now, when we run gem5, the event should fire 10 times, and the
simulation will end after 1000 ticks. The output should now look like
the following.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 13:53:35
    gem5 started Jan  4 2017 13:54:11
    gem5 executing on chinook, pid 2326
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
        100: hello: Hello world! Processing the event! 9 left
        200: hello: Hello world! Processing the event! 8 left
        300: hello: Hello world! Processing the event! 7 left
        400: hello: Hello world! Processing the event! 6 left
        500: hello: Hello world! Processing the event! 5 left
        600: hello: Hello world! Processing the event! 4 left
        700: hello: Hello world! Processing the event! 3 left
        800: hello: Hello world! Processing the event! 2 left
        900: hello: Hello world! Processing the event! 1 left
       1000: hello: Hello world! Processing the event! 0 left
       1000: hello: Done firing!
    Exiting @ tick 18446744073709551615 because simulate() limit reached

You can find the updated header file
[here](/_pages/static/scripts/part2/events/hello_object.hh) and the
implementation file
[here](/_pages/static/scripts/part2/events/hello_object.cc).


---


## Adding parameters to SimObjects and more events

*Source: https://www.gem5.org/documentation/learning_gem5/part2/parameters/*

Adding parameters to SimObjects and more events
===============================================

One of the most powerful parts of gem5's Python interface is the ability
to pass parameters from Python to the C++ objects in gem5. In this
chapter, we will explore some of the kinds of parameters for SimObjects
and how to use them building off of the simple `HelloObject` from the
[previous chapters](http://www.gem5.org/documentation/learning_gem5/part2/helloobject/).

Simple parameters
-----------------

First, we will add parameters for the latency and number of times to
fire the event in the `HelloObject`. To add a parameter, modify the
`HelloObject` class in the SimObject Python file
(`src/learning_gem5/part2/HelloObject.py`). Parameters are set by adding new
statements to the Python class that include a `Param` type.

For instance, the following code has a parameter `time_to_wait` which is
a "Latency" parameter and `number_of_fires` which is an integer
parameter.

```python
class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")
```

`Param.<TypeName>` declares a parameter of type `TypeName`. Common types
are `Int` for integers, `Float` for floats, etc. These types act like
regular Python classes.

Each parameter declaration takes one or two parameters. When given two
parameters (like `number_of_fires` above), the first parameter is the
*default value* for the parameter. In this case, if you instantiate a
`HelloObject` in your Python config file without specifying any value
for number\_of\_fires, it will take the default value of 1.

The second parameter to the parameter declaration is a short description
of the parameter. This must be a Python string. If you only specify a
single parameter to the parameter declaration, it is the description (as
for `time_to_wait`).

gem5 also supports many complex parameter types that are not just
builtin types. For instance, `time_to_wait` is a `Latency`. `Latency`
takes a value as a time value as a string and converts it into simulator
**ticks**. For instance, with a default tick rate of 1 picosecond
(10\^12 ticks per second or 1 THz), `"1ns"` is automatically converted
to 1000. There are other convenience parameters like `Percent`,
`Cycles`, `MemorySize` and many more.

Once you have declared these parameters in the SimObject file, you need
to copy their values to your C++ class in its constructor. The following
code shows the changes to the `HelloObject` constructor.

```cpp
HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params),
    event(*this),
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
{
    DPRINTF(Hello, "Created the hello object with the name %s\n", myName);
}
```

Here, we use the parameter's values for the default values of latency
and timesLeft. Additionally, we store the `name` from the parameter
object to use it later in the member variable `myName`. Each `params`
instantiation has a name which comes from the Python config file when it
is instantiated.

However, assigning the name here is just an example of using the params
object. For all SimObjects, there is a `name()` function that always
returns the name. Thus, there is never a need to store the name like
above.

To the HelloObject class declaration, add a member variable for the
name.

```cpp
class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventWrapper event;

    const std::string myName;

    const Tick latency;

    int timesLeft;

  public:
    HelloObject(HelloObjectParams *p);

    void startup() override;
};
```

When we run gem5 with the above, we get the following error:

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 14:46:36
    gem5 started Jan  4 2017 14:46:52
    gem5 executing on chinook, pid 3422
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
    fatal: hello.time_to_wait without default or user set value

This is because the `time_to_wait` parameter does not have a default
value. Therefore, we need to update the Python config file
(`run_hello.py`) to specify this value.

```python
root.hello = HelloObject(time_to_wait = '2us')
```

Or, we can specify `time_to_wait` as a member variable. Either option is
exactly the same because the C++ objects are not created until
`m5.instantiate()` is called.

```python
root.hello = HelloObject()
root.hello.time_to_wait = '2us'
```

The output of this simple script is the following when running the the
`Hello` debug flag.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 14:46:36
    gem5 started Jan  4 2017 14:50:08
    gem5 executing on chinook, pid 3455
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object with the name hello
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    2000000: hello: Hello world! Processing the event! 0 left
    2000000: hello: Done firing!
    Exiting @ tick 18446744073709551615 because simulate() limit reached

You can also modify the config script to fire the event multiple times.

Other SimObjects as parameters
------------------------------

You can also specify other SimObjects as parameters. To demonstrate
this, we are going to create a new SimObject, `GoodbyeObject`. This
object is going to have a simple function that says "Goodbye" to another
SimObject. To make it a little more interesting, the `GoodbyeObject` is
going to have a buffer to write the message, and a limited bandwidth to
write the message.

First, declare the SimObject in the SConscript file:

```python
Import('*')

SimObject('HelloObject.py', sim_objects=['HelloObject', 'GoodbyeObject'])
Source('hello_object.cc')
Source('goodbye_object.cc')

DebugFlag('Hello')
```

The new SConscript file can be downloaded
[here](/_pages/static/scripts/part2/parameters/SConscript).

Next, you need to declare the new SimObject in a SimObject Python file.
Since the `GoodbyeObject` is highly related to the `HelloObject`, we
will use the same file. You can add the following code to
`HelloObject.py`.

This object has two parameters, both with default values. The first
parameter is the size of a buffer and is a `MemorySize` parameter.
Second is the `write_bandwidth` which specifies the speed to fill the
buffer. Once the buffer is full, the simulation will exit.

```python
class GoodbyeObject(SimObject):
    type = 'GoodbyeObject'
    cxx_header = "learning_gem5/part2/goodbye_object.hh"
    cxx_class = "gem5::GoodbyeObject"

    buffer_size = Param.MemorySize('1kB',
                                   "Size of buffer to fill with goodbye")
    write_bandwidth = Param.MemoryBandwidth('100MB/s', "Bandwidth to fill "
                                            "the buffer")
```

The updated `HelloObject.py` file can be downloaded
[here](/_pages/static/scripts/part2/parameters/HelloObject.py).

Now, we need to implement the `GoodbyeObject`.

```cpp
#ifndef __LEARNING_GEM5_GOODBYE_OBJECT_HH__
#define __LEARNING_GEM5_GOODBYE_OBJECT_HH__

#include <string>

#include "params/GoodbyeObject.hh"
#include "sim/sim_object.hh"

class GoodbyeObject : public SimObject
{
  private:
    void processEvent();

    /**
     * Fills the buffer for one iteration. If the buffer isn't full, this
     * function will enqueue another event to continue filling.
     */
    void fillBuffer();

    EventWrapper<GoodbyeObject, &GoodbyeObject::processEvent> event;

    /// The bytes processed per tick.
    float bandwidth;

    /// The size of the buffer we are going to fill.
    int bufferSize;

    /// The buffer we are putting our message in.
    char *buffer;

    /// The message to put into the buffer.
    std::string message;

    /// The amount of the buffer we've used so far.
    int bufferUsed;

  public:
    GoodbyeObject(GoodbyeObjectParams *p);
    ~GoodbyeObject();

    /**
     * Called by an outside object. Starts off the events to fill the buffer
     * with a goodbye message.
     *
     * @param name the name of the object we are saying goodbye to.
     */
    void sayGoodbye(std::string name);
};

#endif // __LEARNING_GEM5_GOODBYE_OBJECT_HH__
```

```cpp
#include "learning_gem5/part2/goodbye_object.hh"

#include "base/trace.hh"
#include "debug/Hello.hh"
#include "sim/sim_exit.hh"

GoodbyeObject::GoodbyeObject(const GoodbyeObjectParams &params) :
    SimObject(params), event(*this), bandwidth(params.write_bandwidth),
    bufferSize(params.buffer_size), buffer(nullptr), bufferUsed(0)
{
    buffer = new char[bufferSize];
    DPRINTF(Hello, "Created the goodbye object\n");
}

GoodbyeObject::~GoodbyeObject()
{
    delete[] buffer;
}

void
GoodbyeObject::processEvent()
{
    DPRINTF(Hello, "Processing the event!\n");
    fillBuffer();
}

void
GoodbyeObject::sayGoodbye(std::string other_name)
{
    DPRINTF(Hello, "Saying goodbye to %s\n", other_name);

    message = "Goodbye " + other_name + "!! ";

    fillBuffer();
}

void
GoodbyeObject::fillBuffer()
{
    // There better be a message
    assert(message.length() > 0);

    // Copy from the message to the buffer per byte.
    int bytes_copied = 0;
    for (auto it = message.begin();
         it < message.end() && bufferUsed < bufferSize - 1;
         it++, bufferUsed++, bytes_copied++) {
        // Copy the character into the buffer
        buffer[bufferUsed] = *it;
    }

    if (bufferUsed < bufferSize - 1) {
        // Wait for the next copy for as long as it would have taken
        DPRINTF(Hello, "Scheduling another fillBuffer in %d ticks\n",
                bandwidth * bytes_copied);
        schedule(event, curTick() + bandwidth * bytes_copied);
    } else {
        DPRINTF(Hello, "Goodbye done copying!\n");
        // Be sure to take into account the time for the last bytes
        exitSimLoop(buffer, 0, curTick() + bandwidth * bytes_copied);
    }
}
```

The header file can be downloaded
[here](/_pages/static/scripts/part2/parameters/goodbye_object.hh) and the
implementation can be downloaded
[here](/_pages/static/scripts/part2/parameters/goodbye_object.cc).

The interface to this `GoodbyeObject` is simple a function `sayGoodbye`
which takes a string as a parameter. When this function is called, the
simulator builds the message and saves it in a member variable. Then, we
begin filling the buffer.

To model the limited bandwidth, each time we write the message to the
buffer, we pause for the latency it takes to write the message. We use a
simple event to model this pause.

Since we used a `MemoryBandwidth` parameter in the SimObject
declaration, the `bandwidth` variable is automatically converted into
ticks per byte, so calculating the latency is simply the bandwidth times
the bytes we want to write the buffer.

Finally, when the buffer is full, we call the function `exitSimLoop`,
which will exit the simulation. This function takes three parameters,
the first is the message to return to the Python config script
(`exit_event.getCause()`), the second is the exit code, and the third is
when to exit.

### Adding the GoodbyeObject as a parameter to the HelloObject

First, we will also add a `GoodbyeObject` as a parameter to the
`HelloObject`. To do this, you simply specify the SimObject class name
as the `TypeName` of the `Param`. You can have a default, or not, just
like a normal parameter.

```python
class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")

    goodbye_object = Param.GoodbyeObject("A goodbye object")
```

The updated `HelloObject.py` file can be downloaded
[here](/_pages/static/scripts/part2/parameters/HelloObject.py).

Second, we will add a reference to a `GoodbyeObject` to the
`HelloObject` class.
Don't forget to include `goodbye_object.hh` at the top of the `hello_object.hh` file!

```cpp
#include <string>

#include "learning_gem5/part2/goodbye_object.hh"
#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventWrapper event;

    /// Pointer to the corresponding GoodbyeObject. Set via Python
    GoodbyeObject* goodbye;

    /// The name of this object in the Python config file
    const std::string myName;

    /// Latency between calling the event (in ticks)
    const Tick latency;

    /// Number of times left to fire the event before goodbye
    int timesLeft;

  public:
    HelloObject(const HelloObjectParams &p);

    void startup() override;
};
```

Then, we need to update the constructor and the process event function
of the `HelloObject`. We also add a check in the constructor to make
sure the `goodbye` pointer is valid. It is possible to pass a null
pointer as a SimObject via the parameters by using the `NULL` special
Python SimObject. We should *panic* when this happens since it is not a
case this object has been coded to accept.

```cpp
#include "learning_gem5/part2/hello_object.hh"

#include "debug/Hello.hh"

HelloObject::HelloObject(HelloObjectParams &params) :
    SimObject(params),
    event(*this),
    goodbye(params.goodbye_object),
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
{
    DPRINTF(Hello, "Created the hello object with the name %s\n", myName);
    panic_if(!goodbye, "HelloObject must have a non-null GoodbyeObject");
}
```

Once we have processed the number of event specified by the parameter,
we should call the `sayGoodbye` function in the `GoodbyeObject`.

```cpp
void
HelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(Hello, "Hello world! Processing the event! %d left\n", timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(Hello, "Done firing!\n");
        goodbye->sayGoodbye(myName);
    } else {
        schedule(event, curTick() + latency);
    }
}
```

You can find the updated header file
[here](/_pages/static/scripts/part2/parameters/hello_object.hh) and the
implementation file
[here](/_pages/static/scripts/part2/parameters/hello_object.cc).

### Updating the config script

Lastly, we need to add the `GoodbyeObject` to the config script. Create
a new config script, `hello_goodbye.py` and instantiate both the hello
and the goodbye objects. For instance, one possible script is the
following.

```python
import m5
from m5.objects import *

root = Root(full_system = False)

root.hello = HelloObject(time_to_wait = '2us', number_of_fires = 5)
root.hello.goodbye_object = GoodbyeObject(buffer_size='100B')

m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
```

You can download this script
[here](/_pages/static/scripts/part2/parameters/hello_goodbye.py).

Running this script generates the following output.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 15:17:14
    gem5 started Jan  4 2017 15:18:41
    gem5 executing on chinook, pid 3838
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/hello_goodbye.py

    Global frequency set at 1000000000000 ticks per second
          0: hello.goodbye_object: Created the goodbye object
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    2000000: hello: Hello world! Processing the event! 4 left
    4000000: hello: Hello world! Processing the event! 3 left
    6000000: hello: Hello world! Processing the event! 2 left
    8000000: hello: Hello world! Processing the event! 1 left
    10000000: hello: Hello world! Processing the event! 0 left
    10000000: hello: Done firing!
    10000000: hello.goodbye_object: Saying goodbye to hello
    10000000: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10152592: hello.goodbye_object: Processing the event!
    10152592: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10305184: hello.goodbye_object: Processing the event!
    10305184: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10457776: hello.goodbye_object: Processing the event!
    10457776: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10610368: hello.goodbye_object: Processing the event!
    10610368: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10762960: hello.goodbye_object: Processing the event!
    10762960: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10915552: hello.goodbye_object: Processing the event!
    10915552: hello.goodbye_object: Goodbye done copying!
    Exiting @ tick 10944163 because Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goo

You can modify the parameters to these two SimObjects and see how the
overall execution time (Exiting @ tick **10944163**) changes. To run
these tests, you may want to remove the debug flag so there is less
output to the terminal.

In the next chapters, we will create a more complex and more useful
SimObject, culminating with a simple blocking uniprocessor cache
implementation.


---


## Creating SimObjects in the memory system

*Source: https://www.gem5.org/documentation/learning_gem5/part2/memoryobject/*

Creating SimObjects in the memory system
========================================

In this chapter, we will create a simple memory object that sits between
the CPU and the memory bus. In the [next chapter](../simplecache)
we will take this simple memory object and add some logic to it to make
it a very simple blocking uniprocessor cache.

gem5 request and response ports
---------------------------

Before diving into the implementation of a memory object, we should
first understand gem5's request and response port interface. As previously
discussed in [simple-config-chapter](../../part1/simple_config), all memory objects are connected
together via ports. These ports provide a rigid interface between these
memory objects.

These ports implement three different memory system *modes*: timing,
atomic, and functional. The most important mode is *timing mode*. Timing
mode is the only mode that produces correct simulation results. The
other modes are only used in special circumstances.

*Atomic mode* is useful for fastforwarding simulation to a region of
interest and warming up the simulator. This mode assumes that no events
will be generated in the memory system. Instead, all of the memory
requests execute through a single long callchain. It is not required to
implement atomic accesses for a memory object unless it will be used
during fastforward or during simulator warmup.

*Functional mode* is better described as *debugging mode*. Functional
mode is used for things like reading data from the host into the
simulator memory. It is used heavily in syscall emulation mode. For
instance, functional mode is used to load the binary in the
`process.cmd` from the host into the simulated system's memory so the
simulated system can access it. Functional accesses should return the
most up-to-date data on a read, no matter where the data is, and should
update all possible valid data on a write (e.g., in a system with caches
there may be multiple valid cache blocks with the same address).

### Packets

In gem5, `Packets` are sent across ports. A `Packet` is made up of a
`MemReq` which is the memory request object. The `MemReq` holds
information about the original request that initiated the packet such as
the requestor, the address, and the type of request (read, write, etc.).

Packets also have a `MemCmd`, which is the *current* command of the
packet. This command can change throughout the life of the packet (e.g.,
requests turn into responses once the memory command is satisfied). The
most common `MemCmd` are `ReadReq` (read request), `ReadResp` (read
response), `WriteReq` (write request), `WriteResp` (write response).
There are also writeback requests (`WritebackDirty`, `WritebackClean`)
for caches and many other command types.

Packets also either keep the data for the request, or a pointer to the
data. There are options when creating the packet whether the data is
dynamic (explicitly allocated and deallocated), or static (allocated and
deallocated by the packet object).

Finally, packets are used in the classic caches as the unit to track
coherency. Therefore, much of the packet code is specific to the classic
cache coherence protocol. However, packets are used for all
communication between memory objects in gem5, even if they are not
directly involved in coherence (e.g., DRAM controllers and the CPU
models).

All of the port interface functions accept a `Packet` pointer as a
parameter. Since this pointer is so common, gem5 includes a typedef for
it: `PacketPtr`.

### Port interface

There are two types of ports in gem5: request ports and response ports.
Whenever you implement a memory object, you will implement at least one
of these types of ports. To do this, you create a new class that
inherits from either `RequestPort` or `ResponsePort` for request and response
ports, respectively. Request ports send requests (and receive response),
and response ports receive requests (and send responses).

The figure below outlines the simplest interaction between a request
and response port. This figure shows the interaction in timing mode. The
other modes are much simpler and use a simple callchain between the
requestor and the responder.

![Simple request-response interaction when both can accept the request and
the response.](/_pages/static/figures/requestor_responder_1.png)

As mentioned above, all of the port interfaces require a `PacketPtr` as
a parameter. Each of these functions (`sendTimingReq`, `recvTimingReq`,
etc.), accepts a single parameter, a `PacketPtr`. This packet is the
request or response to send or receive.

To send a request packet, the requestor calls `sendTimingReq`. In turn,
(and in the same callchain), the function `recvTimingReq` is called on
the responder with the same `PacketPtr` as its sole parameter.

The `recvTimingReq` has a return type of `bool`. This boolean return
value is directly returned to the calling requestor. A return value of
`true` signifies that the packet was accepted by the responder. A return
value of `false`, on the other hand, means that the responder was unable to
accept and the request must be retried sometime in the future.

In the figure above, first, the requestor sends a timing request by
calling `sendTimingReq`, which in turn calls `recvTimingResp`. The
responder, returns true from `recvTimingReq`, which is returned from the
call to `sendTimingReq`. The requestor continue executing, and the responder
does whatever is necessary to complete the request (e.g., if it is a
cache, it looks up the tags to see if there is a match to the address in
the request).

Once the responder completes the request, it can send a response to the
requestor. The responder calls `sendTimingResp` with the response packet (this
should be the same `PacketPtr` as the request, but it should now be a
response packet). In turn, the request function `recvTimingResp` is
called. The requestor's `recvTimingResp` function returns `true`, which is
the return value of `sendTimingResp` in the responder. Thus, the interaction
for that request is complete.

Later, in the example section we will show the example code for
these functions.

It is possible that the requestor or responder is busy when they receive a
request or a response. The figure below shows the case where the responder
is busy when the original request was sent.

![Simple requestor-responder interaction when the responder is
busy](/_pages/static/figures/requestor_responder_2.png)

In this case, the responder returns `false` from the `recvTimingReq`
function. When a requestor receives false after calling `sendTimingReq`, it
must wait until the its function `recvReqRetry` is executed. Only when
this function is called is the requestor allowed to retry calling
`sendTimingRequest`. The above figure shows the timing request failing
once, but it could fail any number of times. Note: it is up to the
requestor to track the packet that fails, not the responder. The responder *does
not* keep the pointer to the packet that fails.

Similarly, this figure shows the case when the requestor is busy at
the time the responder tries to send a response. In this case, the responder
cannot call `sendTimingResp` until it receives a `recvRespRetry`.

![Simple requestor-responder interaction when the requestor is
busy](/_pages/static/figures/requestor_responder_3.png)

Importantly, in both of these cases, the retry codepath can be a single
call stack. For instance, when the requestor calls `sendRespRetry`,
`recvTimingReq` can also be called in the same call stack. Therefore, it
is easy to incorrectly create an infinite recursion bug, or other bugs.
It is important that before a memory object sends a retry, that it is
ready *at that instant* to accept another packet.

Simple memory object example
----------------------------

In this section, we will build a simple memory object. Initially, it
will simply pass requests through from the CPU-side (a simple CPU) to
the memory-side (a simple memory bus). See the figure below.
It will have a single memory-side requestor port, to send requests to the memory bus,
and two cpu-side ports for the instruction and data cache ports of the
CPU. In the next chapter [simplecache-chapter](../simplecache), we will add the logic
to make this object a cache.

![System with a simple memory object which sits between a CPU and the
memory bus.](/pages/static/figures/simple_memobj.png)

### Declare the SimObject

Just like when we were creating the simple SimObject in
[hello-simobject-chapter](../helloobject), the first step is to create a SimObject Python
file. We will call this simple memory object `SimpleMemobj` and create
the SimObject Python file in `src/learning_gem5/simple_memobj`.

```python
from m5.params import *
from m5.proxy import *
from m5.SimObject import SimObject

class SimpleMemobj(SimObject):
    type = 'SimpleMemobj'
    cxx_header = "learning_gem5/part2/simple_memobj.hh"

    inst_port = ResponsePort("CPU side port, receives requests")
    data_port = ResponsePort("CPU side port, receives requests")
    mem_side = RequestPort("Memory side port, sends requests")
```

For this object, we inherit from `SimObject`. The
`SimObject` class has a pure virtual functions that we will have to
define in our C++ implementation, `getPort`.

This object's parameters are three ports. Two ports for the CPU to
connect the instruction and data ports and a port to connect to the
memory bus. These ports do not have a default value, and they have a
simple description.

It is important to remember the names of these ports. We will explicitly
use these names when implementing `SimpleMemobj` and defining the
`getPort` function.

You can download the SimObject file
[here](/_pages/static/scripts/part2/memoryobject/SimpleMemobj.py).

Of course, you also need to create a SConscript file in the new
directory as well that declares the SimObject Python file. You can
download the SConscript file
[here](/_pages/static/scripts/part2/memoryobject/SConscript).

### Define the SimpleMemobj class

Now, we create a header file for `SimpleMemobj`.

```cpp
#include "mem/port.hh"
#include "params/SimpleMemobj.hh"
#include "sim/sim_object.hh"

class SimpleMemobj : public SimObject
{
  private:

  public:

    /** constructor
     */
    SimpleMemobj(SimpleMemobjParams *params);
};
```

### Define a response port type

Now, we need to define classes for our two kinds of ports: the CPU-side
and the memory-side ports. For this, we will declare these classes
inside the `SimpleMemobj` class since no other object will ever use
these classes.

Let's start with the response port, or the CPU-side port. We are going to
inherit from the `ResponsePort` class. The following is the required code
to override all of the pure virtual functions in the `ResponsePort` class.

```cpp
class CPUSidePort : public ResponsePort
{
  private:
    SimpleMemobj *owner;

  public:
    CPUSidePort(const std::string& name, SimpleMemobj *owner) :
        ResponsePort(name, owner), owner(owner)
    { }

    AddrRangeList getAddrRanges() const override;

  protected:
    Tick recvAtomic(PacketPtr pkt) override { panic("recvAtomic unimpl."); }
    void recvFunctional(PacketPtr pkt) override;
    bool recvTimingReq(PacketPtr pkt) override;
    void recvRespRetry() override;
};
```

This object requires five functions to be defined.

This object also has a single member variable, its owner, so it can call
functions on that object.

### Define a request port type

Next, we need to define a request port type. This will be the memory-side
port which will forward request from the CPU-side to the rest of the
memory system.

```cpp
class MemSidePort : public RequestPort
{
  private:
    SimpleMemobj *owner;

  public:
    MemSidePort(const std::string& name, SimpleMemobj *owner) :
        RequestPort(name, owner), owner(owner)
    { }

  protected:
    bool recvTimingResp(PacketPtr pkt) override;
    void recvReqRetry() override;
    void recvRangeChange() override;
};
```

This class only has three pure virtual functions that we must override.

### Defining the SimObject interface

Now that we have defined these two new types `CPUSidePort` and
`MemSidePort`, we can declare our three ports as part of `SimpleMemobj`.
We also need to declare the pure virtual function in the
`SimObject` class, `getPort`. The
function is used by gem5 during the initialization phase to connect
memory objects together via ports.

```cpp
class SimpleMemobj : public SimObject
{
  private:

    <CPUSidePort declaration>
    <MemSidePort declaration>

    CPUSidePort instPort;
    CPUSidePort dataPort;

    MemSidePort memPort;

  public:
    SimpleMemobj(SimpleMemobjParams *params);

    Port &getPort(const std::string &if_name,
                  PortID idx=InvalidPortID) override;
};
```

You can download the header file for the `SimpleMemobj`
[here](/_pages/static/scripts/part2/memoryobject/simple_memobj.hh).

### Implementing basic SimObject functions

For the constructor of `SimpleMemobj`, we will simply call the
`SimObject` constructor. We also need to initialize all of the ports.
Each port's constructor takes two parameters: the name and a pointer to
its owner, as we defined in the header file. The name can be any string,
but by convention, it is the same name as in the Python SimObject file. We also initialize blocked to be false.

```cpp
#include "learning_gem5/part2/simple_memobj.hh"
#include "debug/SimpleMemobj.hh"

SimpleMemobj::SimpleMemobj(SimpleMemobjParams *params) :
    SimObject(params),
    instPort(params->name + ".inst_port", this),
    dataPort(params->name + ".data_port", this),
    memPort(params->name + ".mem_side", this), blocked(false)
{
}
```

Next, we need to implement the interfaces to get the ports. This
interface is made of the function `getPort`.
The function takes two parameters. The `if_name` is the Python
variable name of the interface for *this* object. 

To implement `getPort`, we compare the `if_name` and check to see
if it is `mem_side` as specified in our Python SimObject file. If it is,
then we return the `memPort` object. If the name is `"inst_port"`, then we return the
instPort, and if the name is `data_port` we return the data port. If not, then we pass the request name to our parent. 

```cpp
Port &
SimpleMemobj::getPort(const std::string &if_name, PortID idx)
{
    panic_if(idx != InvalidPortID, "This object doesn't support vector ports");

    // This is the name from the Python SimObject declaration (SimpleMemobj.py)
    if (if_name == "mem_side") {
        return memPort;
    } else if (if_name == "inst_port") {
        return instPort;
    } else if (if_name == "data_port") {
        return dataPort;
    } else {
        // pass it along to our super class
        return SimObject::getPort(if_name, idx);
    }
}
```


### Implementing request and response port functions

The implementation of both the request and response port is relatively
simple. For the most part, each of the port functions just forwards the
information to the main memory object (`SimpleMemobj`).

Starting with two simple functions, `getAddrRanges` and `recvFunctional`
simply call into the `SimpleMemobj`.

```cpp
AddrRangeList
SimpleMemobj::CPUSidePort::getAddrRanges() const
{
    return owner->getAddrRanges();
}

void
SimpleMemobj::CPUSidePort::recvFunctional(PacketPtr pkt)
{
    return owner->handleFunctional(pkt);
}
```

The implementation of these functions in the `SimpleMemobj` are equally
simple. These implementations just pass through the request to the
memory side. We can use `DPRINTF` calls here to track what is happening
for debug purposes as well.

```cpp
void
SimpleMemobj::handleFunctional(PacketPtr pkt)
{
    memPort.sendFunctional(pkt);
}

AddrRangeList
SimpleMemobj::getAddrRanges() const
{
    DPRINTF(SimpleMemobj, "Sending new ranges\n");
    return memPort.getAddrRanges();
}
```

Similarly for the `MemSidePort`, we need to implement `recvRangeChange`
and forward the request through the `SimpleMemobj` to the response port.

```cpp
void
SimpleMemobj::MemSidePort::recvRangeChange()
{
    owner->sendRangeChange();
}
```

```cpp
void
SimpleMemobj::sendRangeChange()
{
    instPort.sendRangeChange();
    dataPort.sendRangeChange();
}
```

### Implementing receiving requests

The implementation of `recvTimingReq` is slightly more complicated. We
need to check to see if the `SimpleMemobj` can accept the request. The
`SimpleMemobj` is a very simple blocking structure; we only allow a
single request outstanding at a time. Therefore, if we get a request
while another request is outstanding, the `SimpleMemobj` will block the
second request.

To simplify the implementation, the `CPUSidePort` stores all of the
flow-control information for the port interface. Thus, we need to add an
extra member variable, `needRetry`, to the `CPUSidePort`, a boolean that
stores whether we need to send a retry whenever the `SimpleMemobj`
becomes free. Then, if the `SimpleMemobj` is blocked on a request, we
set that we need to send a retry sometime in the future.

```cpp
bool
SimpleMemobj::CPUSidePort::recvTimingReq(PacketPtr pkt)
{
    if (!owner->handleRequest(pkt)) {
        needRetry = true;
        return false;
    } else {
        return true;
    }
}
```

To handle the request for the `SimpleMemobj`, we first check if the
`SimpleMemobj` is already blocked waiting for a response to another
request. If it is blocked, then we return `false` to signal the calling
request port that we cannot accept the request right now. Otherwise, we
mark the port as blocked and send the packet out of the memory port. For
this, we can define a helper function in the `MemSidePort` object to
hide the flow control from the `SimpleMemobj` implementation. We will
assume the `memPort` handles all of the flow control and always return
`true` from `handleRequest` since we were successful in consuming the
request.

```cpp
bool
SimpleMemobj::handleRequest(PacketPtr pkt)
{
    if (blocked) {
        return false;
    }
    DPRINTF(SimpleMemobj, "Got request for addr %#x\n", pkt->getAddr());
    blocked = true;
    memPort.sendPacket(pkt);
    return true;
}
```

Next, we need to implement the `sendPacket` function in the
`MemSidePort`. This function will handle the flow control in case its
peer response port cannot accept the request. For this, we need to add a
member to the `MemSidePort` to store the packet in case it is blocked.
It is the responsibility of the sender to store the packet if the
receiver cannot receive the request (or response).

This function simply sends the packet by calling the function
`sendTimingReq`. If the send fails, then this object stores the packet in
the `blockedPacket` member function so it can send the packet later
(when it receives a `recvReqRetry`). This function also contains some
defensive code to make sure there is not a bug and we never try to
overwrite the `blockedPacket` variable incorrectly.

```cpp
void
SimpleMemobj::MemSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");
    if (!sendTimingReq(pkt)) {
        blockedPacket = pkt;
    }
}
```

Next, we need to implement the code to resend the packet. In this
function, we try to resend the packet by calling the `sendPacket`
function we wrote above.

```cpp
void
SimpleMemobj::MemSidePort::recvReqRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    sendPacket(pkt);
}
```

### Implementing receiving responses

The response codepath is similar to the receiving codepath. When the
`MemSidePort` gets a response, we forward the response through the
`SimpleMemobj` to the appropriate `CPUSidePort`.

```cpp
bool
SimpleMemobj::MemSidePort::recvTimingResp(PacketPtr pkt)
{
    return owner->handleResponse(pkt);
}
```

In the `SimpleMemobj`, first, it should always be blocked when we
receive a response since the object should be waiting for the response.
Before sending the packet back to the CPU side, we need to mark that the
object is no longer blocked. This must be done *before calling
`sendTimingResp`*. Otherwise, it is possible to get stuck in an infinite
loop as it is possible that the request port has a single callchain between
receiving a response and sending another request.

After unblocking the `SimpleMemobj`, we check to see if the packet is an
instruction or data packet and send it back across the appropriate port.
Finally, since the object is now unblocked, we may need to notify the
CPU side ports that they can now retry their requests that failed.

```cpp
bool
SimpleMemobj::handleResponse(PacketPtr pkt)
{
    assert(blocked);
    DPRINTF(SimpleMemobj, "Got response for addr %#x\n", pkt->getAddr());

    blocked = false;

    // Simply forward to the memory port
    if (pkt->req->isInstFetch()) {
        instPort.sendPacket(pkt);
    } else {
        dataPort.sendPacket(pkt);
    }

    instPort.trySendRetry();
    dataPort.trySendRetry();

    return true;
}
```

Similar to how we implemented a convenience function for sending packets
in the `MemSidePort`, we can implement a `sendPacket` function in the
`CPUSidePort` to send the responses to the CPU side. This function calls
`sendTimingResp` which will in turn call `recvTimingResp` on the peer
request port. If this call fails and the peer port is currently blocked,
then we store the packet to be sent later.

```cpp
void
SimpleMemobj::CPUSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");

    if (!sendTimingResp(pkt)) {
        blockedPacket = pkt;
    }
}
```

We will send this blocked packet later when we receive a
`recvRespRetry`. This function is exactly the same as the `recvReqRetry`
above and simply tries to resend the packet, which may be blocked again.

```cpp
void
SimpleMemobj::CPUSidePort::recvRespRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    sendPacket(pkt);
}
```

Finally, we need to implement the extra function `trySendRetry` for the
`CPUSidePort`. This function is called by the `SimpleMemobj` whenever
the `SimpleMemobj` may be unblocked. `trySendRetry` checks to see if a
retry is needed which we marked in `recvTimingReq` whenever the
`SimpleMemobj` was blocked on a new request. Then, if the retry is
needed, this function calls `sendRetryReq`, which in turn calls
`recvReqRetry` on the peer request port (the CPU in this case). 

```cpp
void
SimpleMemobj::CPUSidePort::trySendRetry()
{
    if (needRetry && blockedPacket == nullptr) {
        needRetry = false;
        DPRINTF(SimpleMemobj, "Sending retry req for %d\n", id);
        sendRetryReq();
    }
}
```
In addition to this function, to finish the file add the create function for SimpleMemobj.
```cpp
SimpleMemobj*
SimpleMemobjParams::create()
{
    return new SimpleMemobj(this);
}
```
You can download the implementation for the `SimpleMemobj`
[here](/_pages/static/scripts/part2/memoryobject/simple_memobj.cc).

The following figure shows the relationships between
the `CPUSidePort`, `MemSidePort`, and `SimpleMemobj`. This figure shows
how the peer ports interact with the implementation of the
`SimpleMemobj`. Each bold function is one that we had to implement, and
the non-bold functions are the port interfaces to the peer ports. The
colors highlight one API path through the object (e.g., receiving a
request or updating the memory ranges).

![Interaction between SimpleMemobj and its ports](/_pages/static/figures/memobj_api.png)

For this simple memory object, packets are just forwarded from the
CPU-side to the memory side. However, by modifying `handleRequest` and
`handleResponse`, we can create rich featureful objects, like a cache in
the [next chapter](../simplecache).

### Create a config file

This is all of the code needed to implement a simple memory object! In
the [next chapter](../simplecache), we will take this framework
and add some caching logic to make this memory object into a simple
cache. However, before that, let's look at the config file to add the
SimpleMemobj to your system.

This config file builds off of the simple config file in
[simple-config-chapter](../../part1/simple_config). However, instead of connecting the CPU directly
to the memory bus, we are going to instantiate a `SimpleMemobj` and
place it between the CPU and the memory bus.

```python
import m5
from m5.objects import *

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = X86TimingSimpleCPU()

system.memobj = SimpleMemobj()

system.cpu.icache_port = system.memobj.inst_port
system.cpu.dcache_port = system.memobj.data_port

system.membus = SystemXBar()

system.memobj.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print ("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
```

You can download this config script
[here](/_pages/static/scripts/part2/memoryobject/simple_memobj.py).

Now, when you run this config file you get the following output.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  5 2017 13:40:18
    gem5 started Jan  9 2017 10:17:17
    gem5 executing on chinook, pid 5138
    command line: build/X86/gem5.opt configs/learning_gem5/part2/simple_memobj.py

    Global frequency set at 1000000000000 ticks per second
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    warn: CoherentXBar system.membus has no snooping ports attached!
    warn: ClockedObject: More than one power state change request encountered within the same simulation tick
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 507841000 because target called exit()

If you run with the `SimpleMemobj` debug flag, you can see all of the
memory requests and responses from and to the CPU.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  5 2017 13:40:18
    gem5 started Jan  9 2017 10:18:51
    gem5 executing on chinook, pid 5157
    command line: build/X86/gem5.opt --debug-flags=SimpleMemobj configs/learning_gem5/part2/simple_memobj.py

    Global frequency set at 1000000000000 ticks per second
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
          0: system.memobj: Got request for addr 0x190
      77000: system.memobj: Got response for addr 0x190
      77000: system.memobj: Got request for addr 0x190
     132000: system.memobj: Got response for addr 0x190
     132000: system.memobj: Got request for addr 0x190
     187000: system.memobj: Got response for addr 0x190
     187000: system.memobj: Got request for addr 0x94e30
     250000: system.memobj: Got response for addr 0x94e30
     250000: system.memobj: Got request for addr 0x190
     ...

You may also want to change the CPU model to the out-of-order model
(`X86O3CPU`). When using the out-of-order CPU you will potentially see
a different address stream since it allows multiple memory requests
outstanding at a once. When using the out-of-order CPU, there will now
be many stalls because the `SimpleMemobj` is blocking.


---


## Creating a simple cache object

*Source: https://www.gem5.org/documentation/learning_gem5/part2/simplecache/*

Creating a simple cache object
==============================

In this chapter, we will take the framework for a memory object we
created in the [last chapter](../memoryobject) and add caching
logic to it.

SimpleCache SimObject
---------------------

After creating the SConscript file, that you can download
[here](/_pages/static/scripts/part2/simplecache/SConscript), we can create
the SimObject Python file. We will call this simple memory object
`SimpleCache` and create the SimObject Python file in
`src/learning_gem5/simple_cache`.

```python
from m5.params import *
from m5.proxy import *
from MemObject import MemObject

class SimpleCache(MemObject):
    type = 'SimpleCache'
    cxx_header = "learning_gem5/simple_cache/simple_cache.hh"

    cpu_side = VectorResponsePort("CPU side port, receives requests")
    mem_side = RequestPort("Memory side port, sends requests")

    latency = Param.Cycles(1, "Cycles taken on a hit or to resolve a miss")

    size = Param.MemorySize('16kB', "The size of the cache")

    system = Param.System(Parent.any, "The system this cache is part of")
```

There are a couple of differences between this SimObject file and the
one from the [previous chapter](../memoryobject). First, we have a
couple of extra parameters. Namely, a latency for cache accesses and the
size of the cache. parameters-chapter goes into more detail about these
kinds of SimObject parameters.

Next, we include a `System` parameter, which is a pointer to the main
system this cache is connected to. This is needed so we can get the
cache block size from the system object when we are initializing the
cache. To reference the system object this cache is connected to, we use
a special *proxy parameter*. In this case, we use `Parent.any`.

In the Python config file, when a `SimpleCache` is instantiated, this
proxy parameter searches through all of the parents of the `SimpleCache`
instance to find a SimObject that matches the `System` type. Since we
often use a `System` as the root SimObject, you will often see a
`system` parameter resolved with this proxy parameter.

The third and final difference between the `SimpleCache` and the
`SimpleMemobj` is that instead of having two named CPU ports
(`inst_port` and `data_port`), the `SimpleCache` use another special
parameter: the `VectorPort`. `VectorPorts` behave similarly to regular
ports (e.g., they are resolved via `getPort`),
but they allow this object to connect to multiple peers. Then, in the
resolution functions the parameter we ignored before (`PortID idx`) is
used to differentiate between the different ports. By using a vector
port, this cache can be connected into the system more flexibly than the
`SimpleMemobj`.

Implementing the SimpleCache
----------------------------

Most of the code for the `SimpleCache` is the same as the
`SimpleMemobj`. There are a couple of changes in the constructor and the
key memory object functions.

First, we need to create the CPU side ports dynamically in the
constructor and initialize the extra member functions based on the
SimObject parameters.

```cpp
SimpleCache::SimpleCache(SimpleCacheParams *params) :
    MemObject(params),
    latency(params->latency),
    blockSize(params->system->cacheLineSize()),
    capacity(params->size / blockSize),
    memPort(params->name + ".mem_side", this),
    blocked(false), outstandingPacket(nullptr), waitingPortId(-1)
{
    for (int i = 0; i < params->port_cpu_side_connection_count; ++i) {
        cpuPorts.emplace_back(name() + csprintf(".cpu_side[%d]", i), i, this);
    }
}
```

In this function, we use the `cacheLineSize` from the system parameters
to set the `blockSize` for this cache. We also initialize the capacity
based on the block size and the parameter and initialize other member
variables we will need below. Finally, we must create a number of
`CPUSidePorts` based on the number of connections to this object. Since
the `cpu_side` port was declared as a `VectorResponsePort` in the SimObject
Python file, the parameter automatically has a variable
`port_cpu_side_connection_count`. This is based on the Python name of
the parameter. For each of these connections we add a new `CPUSidePort`
to a `cpuPorts` vector declared in the `SimpleCache` class.

We also add one extra member variable to the `CPUSidePort` to save its
id, and we add this as a parameter to its constructor.

Next, we need to implement the `getPort` function. On the memory side, 
this is straightforward as there is only one port. However, on the CPU side,
we now need to return the port corresponding to the requested ID.

```cpp
Port &
SimpleCache::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "mem_side") {
        panic_if(idx != InvalidPortID,
                 "Mem side of simple cache not a vector port");
        return memPort;
    } else if (if_name == "cpu_side" && idx < cpuPorts.size()) {
        return cpuPorts[idx];
    } else {
        return ClockedObject::getPort(if_name, idx);
    }
}
```

The implementation of the `CPUSidePort` and the `MemSidePort` is almost
the same as in the `SimpleMemobj`. The only difference is we need to add
an extra parameter to `handleRequest` that is the id of the port which
the request originated. Without this id, we would not be able to forward
the response to the correct port. The `SimpleMemobj` knew which port to
send replies based on whether the original request was an instruction or
data accesses. However, this information is not useful to the
`SimpleCache` since it uses a vector of ports and not named ports.

The new `handleRequest` function does two different things than the
`handleRequest` function in the `SimpleMemobj`. First, it stores the
port id of the request as discussed above. Since the `SimpleCache` is
blocking and only allows a single request outstanding at a time, we only
need to save a single port id.

Second, it takes time to access a cache. Therefore, we need to take into
account the latency to access the cache tags and the cache data for a
request. We added an extra parameter to the cache object for this, and
in `handleRequest` we now use an event to stall the request for the
needed amount of time. We schedule a new event for `latency` cycles in
the future. The `clockEdge` function returns the *tick* that the *nth*
cycle in the future occurs on.

```cpp
bool
SimpleCache::handleRequest(PacketPtr pkt, int port_id)
{
    if (blocked) {
        return false;
    }
    DPRINTF(SimpleCache, "Got request for addr %#x\n", pkt->getAddr());

    blocked = true;
    waitingPortId = port_id;

    schedule(new AccessEvent(this, pkt), clockEdge(latency));

    return true;
}
```

The `AccessEvent` is a little more complicated than the `EventWrapper`
we used in events-chapter. Instead of using an `EventWrapper`, in the
`SimpleCache` we will use a new class. The reason we cannot use an
`EventWrapper`, is that we need to pass the packet (`pkt`) from
`handleRequest` to the event handler function. The following code is the
`AccessEvent` class. We only need to implement the `process` function,
that calls the function we want to use as our event handler, in this
case `accessTming`. We also pass the flag `AutoDelete` to the event
constructor so we do not need to worry about freeing the memory for the
dynamically created object. The event code will automatically delete the
object after the `process` function has executed.

```cpp
class AccessEvent : public Event
{
  private:
    SimpleCache *cache;
    PacketPtr pkt;
  public:
    AccessEvent(SimpleCache *cache, PacketPtr pkt) :
        Event(Default_Pri, AutoDelete), cache(cache), pkt(pkt)
    { }
    void process() override {
        cache->accessTiming(pkt);
    }
};
```

Now, we need to implement the event handler, `accessTiming`.

```cpp
void
SimpleCache::accessTiming(PacketPtr pkt)
{
    bool hit = accessFunctional(pkt);
    if (hit) {
        pkt->makeResponse();
        sendResponse(pkt);
    } else {
        <miss handling>
    }
}
```

This function first *functionally* accesses the cache. This function
`accessFunctional` (described below) performs the functional access of
the cache and either reads or writes the cache on a hit or returns that
the access was a miss.

If the access is a hit, we simply need to respond to the packet. To
respond, you first must call the function `makeResponse` on the packet.
This converts the packet from a request packet to a response packet. For
instance, if the memory command in the packet was a `ReadReq` this gets
converted into a `ReadResp`. Writes behave similarly. Then, we can send
the response back to the CPU.

The `sendResponse` function does the same things as the `handleResponse`
function in the `SimpleMemobj` except that it uses the `waitingPortId`
to send the packet to the right port. In this function, we need to mark
the `SimpleCache` unblocked before calling `sendPacket` in case the peer
on the CPU side immediately calls `sendTimingReq`. Then, we try to send
retries to the CPU side ports if the `SimpleCache` can now receive
requests and the ports need to be sent retries.

```cpp
void SimpleCache::sendResponse(PacketPtr pkt)
{
    int port = waitingPortId;

    blocked = false;
    waitingPortId = -1;

    cpuPorts[port].sendPacket(pkt);
    for (auto& port : cpuPorts) {
        port.trySendRetry();
    }
}
```

* * * * *

Back to the `accessTiming` function, we now need to handle the cache
miss case. On a miss, we first have to check to see if the missing
packet is to an entire cache block. If the packet is aligned and the
size of the request is the size of a cache block, then we can simply
forward the request to memory, just like in the `SimpleMemobj`.

However, if the packet is smaller than a cache block, then we need to
create a new packet to read the entire cache block from memory. Here,
whether the packet is a read or a write request, we send a read request
to memory to load the data for the cache block into the cache. In the
case of a write, it will occur in the cache after we have loaded the
data from memory.

Then, we create a new packet, that is `blockSize` in size and we call
the `allocate` function to allocate memory in the `Packet` object for
the data that we will read from memory. Note: this memory is freed when
we free the packet. We use the original request object in the packet so
the memory-side objects know the original requestor and the original
request type for statistics.

Finally, we save the original packet pointer (`pkt`) in a member
variable `outstandingPacket` so we can recover it when the `SimpleCache`
receives a response. Then, we send the new packet across the memory side
port.

```cpp
void
SimpleCache::accessTiming(PacketPtr pkt)
{
    bool hit = accessFunctional(pkt);
    if (hit) {
        pkt->makeResponse();
        sendResponse(pkt);
    } else {
        Addr addr = pkt->getAddr();
        Addr block_addr = pkt->getBlockAddr(blockSize);
        unsigned size = pkt->getSize();
        if (addr == block_addr && size == blockSize) {
            DPRINTF(SimpleCache, "forwarding packet\n");
            memPort.sendPacket(pkt);
        } else {
            DPRINTF(SimpleCache, "Upgrading packet to block size\n");
            panic_if(addr - block_addr + size > blockSize,
                     "Cannot handle accesses that span multiple cache lines");

            assert(pkt->needsResponse());
            MemCmd cmd;
            if (pkt->isWrite() || pkt->isRead()) {
                cmd = MemCmd::ReadReq;
            } else {
                panic("Unknown packet type in upgrade size");
            }

            PacketPtr new_pkt = new Packet(pkt->req, cmd, blockSize);
            new_pkt->allocate();

            outstandingPacket = pkt;

            memPort.sendPacket(new_pkt);
        }
    }
}
```

On a response from memory, we know that this was caused by a cache miss.
The first step is to insert the responding packet into the cache.

Then, either there is an `outstandingPacket`, in which case we need to
forward that packet to the original requestor, or there is no
`outstandingPacket` which means we should forward the `pkt` in the
response to the original requestor.

If the packet we are receiving as a response was an upgrade packet
because the original request was smaller than a cache line, then we need
to copy the new data to the outstandingPacket packet or write to the
cache on a write. Then, we need to delete the new packet that we made in
the miss handling logic.

```cpp
bool
SimpleCache::handleResponse(PacketPtr pkt)
{
    assert(blocked);
    DPRINTF(SimpleCache, "Got response for addr %#x\n", pkt->getAddr());
    insert(pkt);

    if (outstandingPacket != nullptr) {
        accessFunctional(outstandingPacket);
        outstandingPacket->makeResponse();
        delete pkt;
        pkt = outstandingPacket;
        outstandingPacket = nullptr;
    } // else, pkt contains the data it needs

    sendResponse(pkt);

    return true;
}
```

### Functional cache logic

Now, we need to implement two more functions: `accessFunctional` and
`insert`. These two functions make up the key components of the cache
logic.

First, to functionally update the cache, we first need storage for the
cache contents. The simplest possible cache storage is a map (hashtable)
that maps from addresses to data. Thus, we will add the following member
to the `SimpleCache`.

```cpp
std::unordered_map<Addr, uint8_t*> cacheStore;
```

To access the cache, we first check to see if there is an entry in the
map which matches the address in the packet. We use the `getBlockAddr`
function of the `Packet` type to get the block-aligned address. Then, we
simply search for that address in the map. If we do not find the
address, then this function returns `false`, the data is not in the
cache, and it is a miss.

Otherwise, if the packet is a write request, we need to update the data
in the cache. To do this, we write the data from the packet to the
cache. We use the `writeDataToBlock` function which writes the data in
the packet to the write offset into a potentially larger block of data.
This function takes the cache block offset and the block size (as a
parameter) and writes the correct offset into the pointer passed as the
first parameter.

If the packet is a read request, we need to update the packet's data
with the data from the cache. The `setDataFromBlock` function performs
the same offset calculation as the `writeDataToBlock` function, but
writes the packet with the data from the pointer in the first parameter.

```cpp
bool
SimpleCache::accessFunctional(PacketPtr pkt)
{
    Addr block_addr = pkt->getBlockAddr(blockSize);
    auto it = cacheStore.find(block_addr);
    if (it != cacheStore.end()) {
        if (pkt->isWrite()) {
            pkt->writeDataToBlock(it->second, blockSize);
        } else if (pkt->isRead()) {
            pkt->setDataFromBlock(it->second, blockSize);
        } else {
            panic("Unknown packet type!");
        }
        return true;
    }
    return false;
}
```

Finally, we also need to implement the `insert` function. This function
is called every time the memory side port responds to a request.

The first step is to check if the cache is currently full. If the cache
has more entries (blocks) than the capacity of the cache as set by the
SimObject parameter, then we need to evict something. The following code
evicts a random entry by leveraging the hashtable implementation of the
C++ `unordered_map`.

On an eviction, we need to write the data back to the backing memory in
case it has been updated. For this, we create a new `Request`-`Packet`
pair. The packet uses a new memory command: `MemCmd::WritebackDirty`.
Then, we send the packet across the memory side port (`memPort`) and
erase the entry in the cache storage map.

Then, after a block has potentially been evicted, we add the new address
to the cache. For this we simply allocate space for the block and add an
entry to the map. Finally, we write the data from the response packet in
to the newly allocated block. This data is guaranteed to be the size of
the cache block since we made sure to make a new packet in the cache
miss logic if the packet was smaller than a cache block.

```cpp
void
SimpleCache::insert(PacketPtr pkt)
{
    if (cacheStore.size() >= capacity) {
        // Select random thing to evict. This is a little convoluted since we
        // are using a std::unordered_map. See http://bit.ly/2hrnLP2
        int bucket, bucket_size;
        do {
            bucket = random_mt.random(0, (int)cacheStore.bucket_count() - 1);
        } while ( (bucket_size = cacheStore.bucket_size(bucket)) == 0 );
        auto block = std::next(cacheStore.begin(bucket),
                               random_mt.random(0, bucket_size - 1));

        RequestPtr req = new Request(block->first, blockSize, 0, 0);
        PacketPtr new_pkt = new Packet(req, MemCmd::WritebackDirty, blockSize);
        new_pkt->dataDynamic(block->second); // This will be deleted later

        DPRINTF(SimpleCache, "Writing packet back %s\n", pkt->print());
        memPort.sendTimingReq(new_pkt);

        cacheStore.erase(block->first);
    }
    uint8_t *data = new uint8_t[blockSize];
    cacheStore[pkt->getAddr()] = data;

    pkt->writeDataToBlock(data, blockSize);
}
```

Creating a config file for the cache
------------------------------------

The last step in our implementation is to create a new Python config
script that uses our cache. We can use the outline from the
[last chapter](../memoryobject) as a starting point. The only
difference is we may want to set the parameters of this cache (e.g., set
the size of the cache to `1kB`) and instead of using the named ports
(`data_port` and `inst_port`), we just use the `cpu_side` port twice.
Since `cpu_side` is a `VectorPort`, it will automatically create
multiple port connections.

```python
import m5
from m5.objects import *

...

system.cache = SimpleCache(size='1kB')

system.cpu.icache_port = system.cache.cpu_side
system.cpu.dcache_port = system.cache.cpu_side

system.membus = SystemXBar()

system.cache.mem_side = system.membus.cpu_side_ports

...
```

The Python config file can be downloaded
[here](/_pages/static/scripts/part2/simplecache/simple_cache.py).

Running this script should produce the expected output from the hello
binary.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan 10 2017 17:38:15
    gem5 started Jan 10 2017 17:40:03
    gem5 executing on chinook, pid 29031
    command line: build/X86/gem5.opt configs/learning_gem5/part2/simple_cache.py

    Global frequency set at 1000000000000 ticks per second
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    warn: CoherentXBar system.membus has no snooping ports attached!
    warn: ClockedObject: More than one power state change request encountered within the same simulation tick
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 56082000 because target called exit()

Modifying the size of the cache, for instance to 128 KB, should improve
the performance of the system.

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan 10 2017 17:38:15
    gem5 started Jan 10 2017 17:41:10
    gem5 executing on chinook, pid 29037
    command line: build/X86/gem5.opt configs/learning_gem5/part2/simple_cache.py

    Global frequency set at 1000000000000 ticks per second
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    warn: CoherentXBar system.membus has no snooping ports attached!
    warn: ClockedObject: More than one power state change request encountered within the same simulation tick
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 32685000 because target called exit()

Adding statistics to the cache
------------------------------

Knowing the overall execution time of the system is one important
metric. However, you may want to include other statistics as well, such
as the hit and miss rates of the cache. To do this, we need to add some
statistics to the `SimpleCache` object.

First, we need to declare the statistics in the `SimpleCache` object.
They are part of the `Stats` namespace. In this case, we'll make four
statistics. The number of `hits` and the number of `misses` are just
simple `Scalar` counts. We will also add a `missLatency` which is a
histogram of the time it takes to satisfy a miss. Finally, we'll add a
special statistic called a `Formula` for the `hitRatio` that is a
combination of other statistics (the number of hits and misses).

```cpp
class SimpleCache : public MemObject
{
  private:
    ...

    Tick missTime; // To track the miss latency

    Stats::Scalar hits;
    Stats::Scalar misses;
    Stats::Histogram missLatency;
    Stats::Formula hitRatio;

  public:
    ...

    void regStats() override;
};
```

Next, we have to define the function to override the `regStats` function
so the statistics are registered with gem5's statistics infrastructure.
Here, for each statistic, we give it a name based on the "parent"
SimObject name and a description. For the histogram statistic, we also
need to initialize it with how many buckets we want in the histogram.
Finally, for the formula, we simply need to write the formula down in
code.

```cpp
void
SimpleCache::regStats()
{
    // If you don't do this you get errors about uninitialized stats.
    MemObject::regStats();

    hits.name(name() + ".hits")
        .desc("Number of hits")
        ;

    misses.name(name() + ".misses")
        .desc("Number of misses")
        ;

    missLatency.name(name() + ".missLatency")
        .desc("Ticks for misses to the cache")
        .init(16) // number of buckets
        ;

    hitRatio.name(name() + ".hitRatio")
        .desc("The ratio of hits to the total accesses to the cache")
        ;

    hitRatio = hits / (hits + misses);

}
```

Finally, we need to use update the statistics in our code. In the
`accessTiming` class, we can increment the `hits` and `misses` on a hit
and miss respectively. Additionally, on a miss, we save the current time
so we can measure the latency.

```cpp
void
SimpleCache::accessTiming(PacketPtr pkt)
{
    bool hit = accessFunctional(pkt);
    if (hit) {
        hits++; // update stats
        pkt->makeResponse();
        sendResponse(pkt);
    } else {
        misses++; // update stats
        missTime = curTick();
        ...
```

Then, when we get a response, we need to add the measured latency to our
histogram. For this, we use the `sample` function. This adds a single
point to the histogram. This histogram automatically resizes the buckets
to fit the data it receives.

```cpp
bool
SimpleCache::handleResponse(PacketPtr pkt)
{
    insert(pkt);

    missLatency.sample(curTick() - missTime);
    ...
```

The complete code for the `SimpleCache` header file can be downloaded
[here](/_pages/static/scripts/part2/simplecache/simple_cache.hh), and the
complete code for the implementation of the `SimpleCache` can be
downloaded
[here](/_pages/static/scripts/part2/simplecache/simple_cache.cc).

Now, if we run the above config file, we can check on the statistics in
the `stats.txt` file. For the 1 KB case, we get the following
statistics. 91% of the accesses are hits and the average miss latency is
53334 ticks (or 53 ns).

    system.cache.hits                                8431                       # Number of hits
    system.cache.misses                               877                       # Number of misses
    system.cache.missLatency::samples                 877                       # Ticks for misses to the cache
    system.cache.missLatency::mean           53334.093501                       # Ticks for misses to the cache
    system.cache.missLatency::gmean          44506.409356                       # Ticks for misses to the cache
    system.cache.missLatency::stdev          36749.446469                       # Ticks for misses to the cache
    system.cache.missLatency::0-32767                 305     34.78%     34.78% # Ticks for misses to the cache
    system.cache.missLatency::32768-65535             365     41.62%     76.40% # Ticks for misses to the cache
    system.cache.missLatency::65536-98303             164     18.70%     95.10% # Ticks for misses to the cache
    system.cache.missLatency::98304-131071             12      1.37%     96.47% # Ticks for misses to the cache
    system.cache.missLatency::131072-163839            17      1.94%     98.40% # Ticks for misses to the cache
    system.cache.missLatency::163840-196607             7      0.80%     99.20% # Ticks for misses to the cache
    system.cache.missLatency::196608-229375             0      0.00%     99.20% # Ticks for misses to the cache
    system.cache.missLatency::229376-262143             0      0.00%     99.20% # Ticks for misses to the cache
    system.cache.missLatency::262144-294911             2      0.23%     99.43% # Ticks for misses to the cache
    system.cache.missLatency::294912-327679             4      0.46%     99.89% # Ticks for misses to the cache
    system.cache.missLatency::327680-360447             1      0.11%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::360448-393215             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::393216-425983             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::425984-458751             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::458752-491519             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::491520-524287             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::total                   877                       # Ticks for misses to the cache
    system.cache.hitRatio                        0.905780                       # The ratio of hits to the total access

And when using a 128 KB cache, we get a slightly higher hit ratio. It
seems like our cache is working as expected!

    system.cache.hits                                8944                       # Number of hits
    system.cache.misses                               364                       # Number of misses
    system.cache.missLatency::samples                 364                       # Ticks for misses to the cache
    system.cache.missLatency::mean           64222.527473                       # Ticks for misses to the cache
    system.cache.missLatency::gmean          61837.584812                       # Ticks for misses to the cache
    system.cache.missLatency::stdev          27232.443748                       # Ticks for misses to the cache
    system.cache.missLatency::0-32767                   0      0.00%      0.00% # Ticks for misses to the cache
    system.cache.missLatency::32768-65535             254     69.78%     69.78% # Ticks for misses to the cache
    system.cache.missLatency::65536-98303             106     29.12%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::98304-131071              0      0.00%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::131072-163839             0      0.00%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::163840-196607             0      0.00%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::196608-229375             0      0.00%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::229376-262143             0      0.00%     98.90% # Ticks for misses to the cache
    system.cache.missLatency::262144-294911             2      0.55%     99.45% # Ticks for misses to the cache
    system.cache.missLatency::294912-327679             1      0.27%     99.73% # Ticks for misses to the cache
    system.cache.missLatency::327680-360447             1      0.27%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::360448-393215             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::393216-425983             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::425984-458751             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::458752-491519             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::491520-524287             0      0.00%    100.00% # Ticks for misses to the cache
    system.cache.missLatency::total                   364                       # Ticks for misses to the cache
    system.cache.hitRatio                        0.960894                       # The ratio of hits to the total access


---


## ARM Power Modelling

*Source: https://www.gem5.org/documentation/learning_gem5/part2/arm_power_modelling/*

ARM Power Modelling
===================

It is possible to model and monitor the energy and power usage of a gem5
simulation. This is done by using various stats already recorded by gem5 in a
`MathExprPowerModel`; a way to model power usage through mathematical
equations. This chapter of the tutorial details what the various components
required for power modelling are and explains how to add them to an existing
ARM simulation.

This chapter draws on the `fs_power.py` configuration script, provided in the
`configs/example/arm` directory, and also provides instructions for how to
extend this script or other scripts.

Note that power models can only be applied when using the more detailed
"timing" CPUs.

An overview of how power modelling is built into gem5 and which other parts of
the simulator they interact with can be found in [Sascha Bischoff's
presentation](https://youtu.be/3gWyUWHxVj4) from the 2017 ARM Research Summit.

Dynamic Power States
--------------------

Power Models consist of two functions which describe how to calculate the power
consumption in different power states. The power states are (from
`src/sim/PowerState.py`):

- `UNDEFINED`: Invalid state, no power state derived information is available.
   This state is the default.
- `ON`: The logic block is actively running and consuming dynamic and leakage
   energy depending on the amount of processing required.
- `CLK_GATED`: The clock circuity within the block is gated to save dynamic
   energy, the power supply to the block is still on and leakage energy is
   being consumed by the block.
- `SRAM_RETENTION`: The SRAMs within the logic blocks are pulled into retention
   state to reduce leakage energy further.
- `OFF`: The logic block is power gated and is not consuming any energy.

A Power Model is assigned to each of the states, apart from `UNDEFINED`, using
the `PowerModel` class's `pm` field. It is a list containing 4 Power Models,
one for each state, in the following order:

0. `ON`
1. `CLK_GATED`
2. `SRAM_RETENTION`
3. `OFF`

Note that although there are 4 different entries, these do not have to be
different Power Models. The provided `fs_power.py` file uses one Power Model
for the `ON` state and then the same Power Model for the remaining states.

Power Usage Types
-----------------

The gem5 simulator models 2 types of power usage:

- **static**: The power used by the simulated system regardless of activity.
- **dynamic**: The power used by the system due to various types of activity.

A Power Model must contain an equation for modelling both of these (although
that equation can be as simple as `st = "0"` if, for example, static power is
not desired or irrelevant in that Power Model).

MathExprPowerModels
-------------------

The provided Power Models in `fs_power.py` extend the `MathExprPowerModel`
class. `MathExprPowerModels` are specified as strings containing mathematical
expressions for how to calculate the power used by the system. They typically
contain a mix of stats and automatic variables, e.g. temperature, for example:

```python
class CpuPowerOn(MathExprPowerModel):
    def __init__(self, cpu_path, **kwargs):
        super(CpuPowerOn, self).__init__(**kwargs)
        # 2A per IPC, 3pA per cache miss
        # and then convert to Watt
        self.dyn = "voltage * (2 * {}.ipc + 3 * 0.000000001 * " \
                   "{}.dcache.overall_misses / sim_seconds)".format(cpu_path,
                                                                    cpu_path)
        self.st = "4 * temp"
```

(The above power model is taken from the provided `fs_power.py` file.)

We can see that the automatic variables (`voltage` and `temp`)  do not require
a path, whereas component-specific stats (the CPU's Instructions Per Cycle
`ipc`) do.  Further down in the file, in the `main` function, we can see that
the CPU object has a `path()` function which returns the component's "path" in
the system, e.g. `system.bigCluster.cpus0`. The `path` function is provided by
`SimObject` and so can be used by any object in the system which extends this,
for example the l2 cache object uses it a couple of lines further down from
where the CPU object uses it.

(Note the division of `dcache.overall_misses` by `sim_seconds` to convert to
Watts. This is a _power_ model, i.e. energy over time, and not an energy model.
It is good to be cautious when using these terms as they are often used
interchangeably, but mean very specific things when it comes to power and
energy simulation/modelling.)

Extending an existing simulation
--------------------------------

The provided `fs_power.py` script extends the existing `fs_bigLITTLE.py` script
by importing it and then modifying the values. As part of this, several loops
are used to iterate through the descendants of the SimObjects to apply the
Power Models to. So to extend an existing simulation to support power models,
it can be helpful to define a helper function which does this:

```python
def _apply_pm(simobj, power_model, so_class=None):
    for desc in simobj.descendants():
        if so_class is not None and not isinstance(desc, so_class):
            continue

        desc.power_state.default_state = "ON"
        desc.power_model = power_model(desc.path())
```

The function above takes a SimObject, a Power Model, and optionally a class
that the SimObject's descendant have to instantiate in order for the PM to be
applied. If no class is specified, the PM is applied to all the descendants.

Whether you decide to use the helper function or not, you now need to define
some Power Models. This can be done by following the pattern seen in
`fs_power.py`:

0. Define a class for each of the power states you are interested in. These
   classes should extend `MathExprPowerModel`, and contain a `dyn` and an `st`
   field. Each of these fields should contain a string describing how to
   calculate the respective type of power in this state. Their constructors
   should take a path to be used through `format` in the strings describing the
   power calculation equation, and a number of kwargs to be passed to the
   super-constructor.
1. Define a class to hold all the Power Models defined in the previous step.
   This class should extend `PowerModel` and contain a single field `pm` which
   contains a list of 4 elements: `pm[0]` should be an instance of the Power
   Model for the "ON" power state; `pm[1]` should be an instance of the Power
   Model for the "CLK_GATED" power state; etc. This class's constructor should
   take the path to pass on to the individual Power Models, and a number of
   kwargs which are passed to the super-constructor.
2. With the helper function and the above classes defined, you can then extend
   the `build` function to take these into account and optionally add a
   command-line flag in the `addOptions` function if you want to be able to
   toggle the use of the models.

> **Example implementation:**
>
> ```python
> class CpuPowerOn(MathExprPowerModel):
>     def __init__(self, cpu_path, **kwargs):
>         super(CpuPowerOn, self).__init__(**kwargs)
>         self.dyn = "voltage * 2 * {}.ipc".format(cpu_path)
>         self.st = "4 * temp"
>
>
> class CpuPowerClkGated(MathExprPowerModel):
>     def __init__(self, cpu_path, **kwargs):
>         super(CpuPowerOn, self).__init__(**kwargs)
>         self.dyn = "voltage / sim_seconds"
>         self.st = "4 * temp"
>
>
> class CpuPowerOff(MathExprPowerModel):
>     dyn = "0"
>     st = "0"
>
>
> class CpuPowerModel(PowerModel):
>     def __init__(self, cpu_path, **kwargs):
>         super(CpuPowerModel, self).__init__(**kwargs)
>         self.pm = [
>             CpuPowerOn(cpu_path),       # ON
>             CpuPowerClkGated(cpu_path), # CLK_GATED
>             CpuPowerOff(),              # SRAM_RETENTION
>             CpuPowerOff(),              # OFF
>         ]
>
> [...]
>
> def addOptions(parser):
>     [...]
>     parser.add_argument("--power-models", action="store_true",
>                         help="Add power models to the simulated system. "
>                              "Requires using the 'timing' CPU."
>     return parser
>
>
> def build(options):
>     root = Root(full_system=True)
>     [...]
>     if options.power_models:
>         if options.cpu_type != "timing":
>             m5.fatal("The power models require the 'timing' CPUs.")
>
>         _apply_pm(root.system.bigCluster.cpus, CpuPowerModel
>                   so_class=m5.objects.BaseCpu)
>         _apply_pm(root.system.littleCluster.cpus, CpuPowerModel)
>
>     return root
>
> [...]
> ```

Stat Names
----------

The stat names are usually the same as can be seen in the `stats.txt` file
produced in the `m5out` directory after a simulation. However, there are some
exceptions:

- The CPU clock is referred to as `clk_domain.clock` in `stats.txt` but is
  accessed in power models using `clock_period` and _not_ `clock`.

Stat dump frequency
-------------------

By default, gem5 dumps simulation stats to the `stats.txt` file every simulated
second. This can be controlled through the `m5.stats.periodicStatDump`
function, which takes the desired frequency for dumping stats measured in
simulated ticks, not seconds. Fortunately, `m5.ticks` provides a `fromSeconds`
function for ease of usability.

Below is an example of how stat dumping frequency affects result resolution,
taken from [Sascha Bischoff's presentation](https://youtu.be/3gWyUWHxVj4) slide
16:

![A picture comparing a less detailed power graph with a more detailed one; a 1
second sampling interval vs a 1 millisecond sampling
interval.](/pages/static/figures/empowering_the_masses_slide16.png)

How frequently stats are dumped directly affects the resolution of the graphs
that can be produced based on the `stats.txt` file. However, it also affects
the size of the output file. Dumping stats every simulated second vs. every
simulated millisecond increases the file size by a factor of several hundreds.
Therefore, it makes sense to want to control the stat dump frequency.

Using the provided `fs_power.py` script, this can be done as follows:

```python
[...]

def addOptions(parser):
    [...]
    parser.add_argument("--stat-freq", type=float, default=1.0,
                        help="Frequency (in seconds) to dump stats to the "
                             "'stats.txt' file. Supports scientific notation, "
                             "e.g. '1.0E-3' for milliseconds.")
    return parser

[...]

def main():
    [...]
    m5.stats.periodicStatDump(m5.ticks.fromSeconds(options.stat_freq))
    bL.run()

[...]
```

The stat dump frequency could then be specified using
```
--stat-freq <val>
```
when invoking the simulation.

Common Problems
---------------

- gem5 crashes when using the provided `fs_power.py`, with the message `fatal:
  statistic '' (160) was not properly initialized by a regStats() function`
- gem5 crashes when using the provided `fs_power.py`, with the message `fatal:
  Failed to evaluate power expressions: [...]`

These are due to gem5's stats framework recently having been refactored.
Getting the latest version of the gem5 source code and re-building should fix
the problem. If this is not desirable, the following two sets of patches are
required:

1. [https://gem5-review.googlesource.com/c/public/gem5/+/26643](https://gem5-review.googlesource.com/c/public/gem5/+/26643)
2. [https://gem5-review.googlesource.com/c/public/gem5/+/26785](https://gem5-review.googlesource.com/c/public/gem5/+/26785)

These can be checked out and applied by following the download instructions at
their respective links.


---


## ARM DVFS Support

*Source: https://www.gem5.org/documentation/learning_gem5/part2/arm_dvfs_support/*

ARM DVFS modelling
==================

Like most modern CPUs, ARM CPUs support DVFS. It is possible to model this and,
for example, monitor the resulting power usage in gem5. DVFS modelling is done
through the use of two components of Clocked Objects: Voltage Domains and Clock
Domains. This chapter details the different components and shows different ways
to add them to an existing simulation.

Voltage Domains
---------------

Voltage Domains dictate the voltage values the CPUs can use. If no VD is
specified when running a Full System simulation in gem5, a default value of
1.0 Volts is used. This is to avoid forcing users to consider voltage when they
are not interested in simulating this.

Voltage Domains can be constructed from either a single value or a list of
values, passed to the `VoltageDomain` constructor using the `voltage` kwarg. If
a single value and multiple frequencies are specified, the voltage is used for
all the frequencies in the Clock Domain. If a list of voltage values is
specified, its number of entries must match the number of entries in the
corresponding Clock Domain and the entries must be arranged in _descending_
order. As with real hardware, a Voltage Domain applies to the entire processor
socket. This means that if you want to have different VDs for the different
processors (e.g. for a big.LITTLE setup) you need to make sure the big and the
LITTLE cluster are on different sockets (check the `socket_id` value associated
with the clusters).

There are 2 ways to add a VD to an existing CPU/simulation, one is more
flexible, the other is more straightforward. The first method adds command-line
flags to the provided `configs/example/arm/fs_bigLITTLE.py` file, while the
second method adds custom classes.

1. The most flexible way to add Voltage Domains to a simulation is to use
   command-line flags. To add a command-line flag, find the `addOptions`
   function in the file and add the flag there, optionally with some help
   text.  
   An example supporting both a single and multiple voltages:

   ```python
   def addOptions(parser):
       [...]
       parser.add_argument("--big-cpu-voltage", nargs="+", default="1.0V",
                           help="Big CPU voltage(s).")
       return parser
   ```

   The voltage domain value(s) could then be specified with

   ```
   --big-cpu-voltage <val1>V [<val2>V [<val3>V [...]]]
   ```

   This would then be accessed in the `build` function using
   `options.big_cpu_voltage`.  The `nargs="+"` ensures that at least one
   argument is required.
   Example usage in `build`:

   ```python
   def build(options):
       [...]
       # big cluster
       if options.big_cpus > 0:
           system.bigCluster = big_model(system, options.big_cpus,
                                         options.big_cpu_clock,
                                         options.big_cpu_voltage)
       [...]
   ```

   A similar flag and additions to the `build` function could be added to
   support specifying voltage values for the LITTLE CPU. This approach allows
   for very easy specification and modification of the voltages. The only
   downside to this method is that the multiple command line arguments, some
   being in list form, could clutter up the command used to invoke the
   simulator.

2. The less flexible way to specify Voltage Domains is by creating sub-classes
   of the `CpuCluster`. Similar to the existing `BigCluster` and
   `LittleCluster` sub-classes, these will extend the `CpuCluster` class.
   In the constructor of the subclass, in addition to specifying a CPU-type, we
   also define a lists of values for the Voltage Domain and pass this to the
   call to the `super` constructor using the kwarg `cpu_voltage`.
   Here is an example, for adding voltage to a `BigCluster`:

   ```python
   class VDBigCluster(devices.CpuCluster):
       def __init__(self, system, num_cpus, cpu_clock=None, cpu_voltage=None):
           # use the same CPU as the stock BigCluster
           abstract_cpu = ObjectList.cpu_list.get("O3_ARM_v7a_3")
           # voltage value(s)
           my_voltages = [ '1.0V', '0.75V', '0.51V']

           super(VDBigCluster, self).__init__(
               cpu_voltage=my_voltages,
               system=system,
               num_cpus=num_cpus,
               cpu_type=abstract_cpu,
               l1i_type=devices.L1I,
               l1d_type=devices.L1D,
               wcache_type=devices.WalkCache,
               l2_type=devices.L2
           )
   ```

   Adding voltages to the `LittleCluster` could then be done by defining a
   similar `VDLittleCluster` class.

   With the subclass(es) defined, we still need to add an entry to the
   `cpu_types` dictionary in the file, specifying a string name as the key and
   a pair of classes as the value, e.g:

   ```python
   cpu_types = {
       [...]
       "vd-timing" : (VDBigCluster, VDLittleCluster)
   }
   ```

   The CPUs with VDs could then be used by passing

   ```
   --cpu-type vd-timing
   ```

   to the command invoking the simulation.

   Since any modifications to the voltage values have to be done by finding the
   right subclass and modifying its code, or adding more subclasses and
   `cpu_types` entries, this approach is a lot less flexible than the
   flag-based approach.

Clock Domains
-------------

Voltage Domains are used in conjunction with Clock Domains. As previously
mentioned, if no custom voltage values have been specified, a default value of
1.0V is used for all values in the Clock Domain.

Types of Clock Domain
In contrast to Voltage Domains, there are 3 types of Clock Domains (from
`src/sim/clock_domain.hh`):

- `ClockDomain` -- provides a clock to a group of Clocked Objects bundled under
  the same Clock Domain. The CDs are in turn grouped into Voltage Domains. The
  CDs provide support for a hierarchical structure with "Source" and "Derived"
  Clock Domains.
- `SrcClockDomain` -- provides the notion of a CD that is connected to a
  tunable clock source. It maintains the clock period and provides the methods
  for setting/getting the clock, as well as the configuration parameters for
  the CD that a handler is going to manage. This includes frequency values at
  various performance levels, a Domain ID, and the current performance level.
  Note that a performance level as requested by the software corresponds to one
  of the frequency operation points the CD can operate at.
- `DerivedClockDomain` -- provides the notion of a CD that is connected to a
  parent CD which can either be a `SrcClockDomain` or a `DerivedClockDomain`.
  It maintains the clock divider and provides methods for getting the clock.

Adding Clock Domains to an existing simulation
----------------------------------------------

This example will use the same provided files as the VD examples, i.e.
`configs/example/arm/fs_bigLITTLE.py` and `configs/example/arm/devices.py`.

Like VDs, CDs can be a single value or a list of values. If a list of clock
speeds is given, the same rules apply as for a list of voltages given to a VD,
i.e. the number of values in the CD must match the number of values in the VD;
and the clock speeds must be given in _descending_ order. The provided files
come with support for specifying the clock as a single value (through the
`--{big,little}-cpu-clock` flags), but not as a list of values.
Extending/Modifying the behaviour of the provided flags is the simplest and
most flexible way to add support for multi-value CDs, but it is also possible
to do it by adding subclasses.

1. To add multi-value support to the existing `--{big,little}-cpu-clock` flags,
   locate the `addOptions` function in the
   `configs/example/arm/fs_bigLITTLE.py` file. Amongst the various
   `parser.add_argument` calls, find the ones that add the CPU-clock flags and
   replace the kwarg `type=str` with `nargs="+"`:
   ```python
   def addOptions(parser):
       [...]
       parser.add_argument("--big-cpu-clock", nargs="+", default="2GHz",
                           help="Big CPU clock frequency.")
       parser.add_argument("--little-cpu-clock", nargs="+", default="1GHz",
                           help="Little CPU clock frequency.")
       [...]
   ```
   With this, multiple frequencies can be specified similarly to the flag used
   for VDs:
   ```
   --{big,little}-cpu-clock <val1>GHz [<val2>MHz [<val3>MHz [...]]]
   ```

   Since this modifies existing flags, the flags' values are already wired up
   to the relevant constructors and kwargs in the `build` function, so there is
   nothing to be modified there.

2. To add CDs in a subclass, the process is very similar to the process of
   adding VDs as a subclass. The difference is that instead of specifying
   voltages and using the `cpu_voltage` kwarg, we specify clock values and use
   the `cpu_clock` kwarg in the `super` call:
   ```python
   class CDBigCluster(devices.CpuCluster):
       def __init__(self, system, num_cpus, cpu_clock=None, cpu_voltage=None):
           # use the same CPU as the stock BigCluster
           abstract_cpu = ObjectList.cpu_list.get("O3_ARM_v7a_3")
           # clock value(s)
           my_freqs = [ '1510MHz', '1000MHz', '667MHz']

           super(VDBigCluster, self).__init__(
               cpu_clock=my_freqs,
               system=system,
               num_cpus=num_cpus,
               cpu_type=abstract_cpu,
               l1i_type=devices.L1I,
               l1d_type=devices.L1D,
               wcache_type=devices.WalkCache,
               l2_type=devices.L2
           )
   ```
   This could be combined with the VD example so as to specify both VDs and CDs
   for the cluster.

   As with adding VDs using this approach, you would need to define a class for
   each of the CPU-types you wanted to use and specify their name-cpuPair value
   in the `cpu_types` dictionary. This method also has the same limitations and
   is a lot less flexible than the flag-based approach.

Making sure CDs have a valid DomainID
-------------------------------------

Regardless of which of the previous methods are used, there are some additional
modifications required. These concern the provided
`configs/example/arm/devices.py` file.

In the file, locate the `CpuClusters` class and find the place where
`self.clk_domain` is initialised to a `SrcClockDomain`. As noted in the comment
concerning `SrcClockDomain` above, these have a Domain ID. If this is not set,
as is the case in the provided setup, then the default ID of `-1` will be used.
Instead of this, change the code to make sure the Domain ID is set:

```python
[...]
self.clk_domain = SrcClockDomain(clock=cpu_clock,
                                 voltage_domain=self.voltage_domain,
                                 domain_id=system.numCpuClusters())
[...]
```

The `system.numCpuClusters()` is used here since the CD applies to the entire
cluster, i.e. it will be 0 for the first cluster, 1 for the second cluster,
etc.

If you don't set the Domain ID, you will get the following error when trying to
run a DVFS-capable simulation as some internal checks catch the default Domain
ID:

```
fatal: fatal condition domain_id == SrcClockDomain::emptyDomainID occurred:
DVFS: Controlled domain system.bigCluster.clk_domain needs to have a properly
assigned ID.
```

The DVFS Handler
----------------

If you specify VDs and CDs and then try to run your simulation, it will most
likely run, but you might notice the following warning in the output:

```
warn: Existing EnergyCtrl, but no enabled DVFSHandler found.
```

The VDs and CDs have been added, but there is no `DVFSHandler` which the system
can interface with to adjust the values. The simplest way to fix this is to add
another command-line flag, in the `configs/example/arm/fs_bigLITTLE.py` file.

As in the VD and CD examples, locate the `addOptions` function and append the
following code to it:

```python
def addOptions(parser):
    [...]
    parser.add_argument("--dvfs", action="store_true",
                        help="Enable the DVFS Handler.")
    return parser
```

Then, locate the `build` function and append this code to it:

```python
def build(options):
    [...]
    if options.dvfs:
        system.dvfs_handler.domains = [system.bigCluster.clk_domain,
                                       system.littleCluster.clk_domain]
        system.dvfs_handler.enable = options.dvfs

    return root
```

With this in place, you should now be able to run a DVFS-capable simulation by
using the `--dvfs` flag when invoking the simulation, with the option to
specify the voltage and frequency operating points of both the big and the
LITTLE cluster as necessary.


---


# ═══ Modeling Cache Coherence with Ruby ═══


## Introduction to Ruby

*Source: https://www.gem5.org/documentation/learning_gem5/part3/MSIintro/*

## Introduction to Ruby

Ruby comes from the [multifacet GEMS project](http://research.cs.wisc.edu/gems/).
Ruby provides a detailed cache memory and cache coherence models as well as a detailed network model (Garnet).

Ruby is flexible. It can model many different kinds of coherence
implementations, including broadcast, directory, token, region-based
coherence, and is simple to extend to new coherence models.

Ruby is a mostly drop-in replacement for the classic memory system.
There are interfaces between the classic gem5 MemObjects and Ruby, but
for the most part, the classic caches and Ruby are not compatible.

In this part of the book, we will first go through creating an example
protocol from the protocol description to debugging and running the
protocol.

Before diving into a protocol, we will first talk about some of the
architecture of Ruby. The most important structure in Ruby is the
controller, or state machine. Controllers are implemented by writing a
SLICC state machine file.

SLICC is a domain-specific language (Specification Language including
Cache Coherence) for specifying coherence protocols. SLICC files end in
".sm" because they are *state machine* files. Each file describes
states, transitions from a begin to an end state on some event, and
actions to take during the transition.

Each coherence protocol is made up of multiple SLICC state machine
files. These files are compiled with the SLICC compiler which is written
in Python and part of the gem5 source. The SLICC compiler takes the
state machine files and output a set of C++ files that are compiled with
all of gem5's other files. These files include the SimObject declaration
file as well as implementation files for SimObjects and other C++
objects.

Currently, gem5 supports compiling only a single coherence protocol at a
time. For instance, you can compile MI\_example into gem5 (the default,
poor performance, protocol), or you can use MESI\_Two\_Level. But, to
use MESI\_Two\_Level, you have to recompile gem5 so the SLICC compiler
can generate the correct files for the protocol. We discuss this further
in the compilation section \<MSI-building-section\>

Now, let's dive into implementing our first coherence protocol!


---


## MSI example cache protocol

*Source: https://www.gem5.org/documentation/learning_gem5/part3/cache-intro/*

## MSI example cache protocol

Before we implement a cache coherence protocol, it is important to have
a solid understanding of cache coherence. This section leans heavily on
the great book *A Primer on Memory Consistency and Cache Coherence* by
Daniel J. Sorin, Mark D. Hill, and David A. Wood which was published as
part of the Synthesis Lectures on Computer Architecture in 2011
([DOI:10.2200/S00346ED1V01Y201104CAC016](https://doi.org/10.2200/S00346ED1V01Y201104CAC016)).
If you are unfamiliar with cache coherence, I strongly advise reading that book before continuing.

In this chapter, we will be implementing an MSI protocol.
(An MSI protocol has three stable states, modified with read-write permission, shared with read-only permission, and invalid with no permissions.)
We will implement this as a three-hop directory protocol (i.e., caches can send data directly to other caches without going through the directory).
Details for the protocol can be found in Section 8.2 of *A Primer on Memory Consistency and Cache Coherence* (pages 141-149).
It will be helpful to print out Section 8.2 to reference as you are implementing the protocol.

You can download the Second Edition [via this link](https://link.springer.com/content/pdf/10.1007/978-3-031-01764-3.pdf).

## First steps to writing a protocol

Let's start by creating a new directory for our protocol at src/learning\_gem5/MSI\_protocol.
In this directory, like in all gem5 source directories, we need to create a file for SCons to know what to compile.
However, this time, instead of creating a `SConscript` file, we are
going to create a `SConsopts` file. (The `SConsopts` files are processed
before the `SConscript` files and we need to run the SLICC compiler
before SCons executes.)

We need to create a `SConsopts` file with the following:

```python
Import('*')

main.Append(ALL_PROTOCOLS=['MSI'])

main.Append(PROTOCOL_DIRS=[Dir('.')])
```

We do two things in this file. First, we register the name of our
protocol (`'MSI'`). Since we have named our protocol MSI, SCons will
assume that there is a file named `MSI.slicc` which specifies all of the
state machine files and auxiliary files. We will create that file after
writing all of our state machine files. Second, the `SConsopts` files
tells the SCons to look in the current directory for files to pass to
the SLICC compiler.

You can download the `SConsopts` file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/SConsopts).

### Writing a state machine file

The next step, and most of the effort in writing a protocol, is to
create the state machine files. State machine files generally follow the
outline:

Parameters
:   These are the parameters for the SimObject that will be generated
    from the SLICC code.

Declaring required structures and functions
:   This section declares the states, events, and many other required
    structures for the state machine.

In port code blocks
:   Contain code that looks at incoming messages from the (`in_port`)
    message buffers and determines what events to trigger.

Actions
:   These are simple one-effect code blocks (e.g., send a message) that
    are executed when going through a transition.

Transitions
:   Specify actions to execute given a starting state and an event and
    the final state. This is the meat of the state machine definition.

Over the next few sections we will go over how to write each of these components of the protocol.


---


## Declaring a state machine

*Source: https://www.gem5.org/documentation/learning_gem5/part3/cache-declarations/*

Let's start on our first state machine file! First, we will create the
L1 cache controller for our MSI protocol.

Create a file called `MSI-cache.sm` and the following code declares the
state machine.

```cpp
machine(MachineType:L1Cache, "MSI cache")
    : <parameters>
{
    <All state machine code>
}
```

The first thing you'll notice about the state machine code is that is
looks very C++-like. The state machine file is like creating a C++
object in a header file, if you included all of the code there as well.
When in doubt, C++ syntax with *probably* work in SLICC. However, there
are many cases where C++ syntax is incorrect syntax for SLICC as well as
cases where SLICC extends the syntax.

With `MachineType:L1Cache`, we are naming this state machine `L1Cache`.
SLICC will generate many different objects for us from the state machine
using that name. For instance, once this file is compiled, there will be
a new SimObject: `L1Cache_Controller` that is the cache controller. Also
included in this declaration is a description of this state machine:
"MSI cache".

There are many cases in SLICC where you must include a description to go
along with the variable. The reason for this is that SLICC was
originally designed to just describe, not implement, coherence
protocols. Today, these extra descriptions serve two purposes. First,
they act as comments on what the author intended each variable, or
state, or event, to be used for. Second, many of them are still exported
into HTML when building the HTML tables for the SLICC protocol. Thus,
while browsing the HTML table, you can see the more detailed comments
from the author of the protocol. It is important to be clear with these
descriptions since coherence protocols can get quite complicated.

## State machine parameters

Proceeding the `machine()` declaration is a colon, after which all of
the parameters to the state machine are declared. These parameters are
directly exported to the SimObject that is generated by the state
machine.

For our MSI L1 cache, we have the following parameters:

```cpp
machine(MachineType:L1Cache, "MSI cache")
: Sequencer *sequencer;
  CacheMemory *cacheMemory;
  bool send_evictions;

  <Message buffer declarations>

  {

  }
```

First, we have a `Sequencer`. This is a special class that is
implemented in Ruby to interface with the rest of gem5. The Sequencer is
a gem5 `MemObject` with a slave port so it can accept memory requests
from other objects. The sequencer accepts requests from a CPU (or other
master port) and converts the gem5 the packet into a `RubyRequest`.
Finally, the `RubyRequest` is pushed onto the `mandatoryQueue` of the
state machine. We will revisit the `mandatoryQueue` in
the [in-port section](../cache-in-ports).

Next, there is a `CacheMemory` object. This is what holds the cache data
(i.e., cache entries). The exact implementation, size, etc. is
configurable at runtime.

Finally, we can specify any other parameters we would like, similar to a
general `SimObject`. In this case, we have a boolean variable
`send_evictions`. This is used for out-of-order core models to notify
the load-store queue if an address is evicted after a load to squash a
load if it is speculative.

Next, also in the parameter block (i.e., before the first open bracket),
we need to declare all of the message buffers that this state machine
will use. Message buffers are the interface between the state machine
and the Ruby network. Messages are sent and received via the message
buffers. Thus, for each virtual channel in our protocol we need a
separate message buffer.

The MSI protocol needs three different virtual networks. Virtual
networks are needed to prevent deadlock (e.g., it is bad if a response
gets stuck behind a stalled request). In this protocol, the highest
priority is responses (virtual network 2), followed by forwarded
requests (virtual network 1), then requests have the lowest priority
(virtual network 0). See Sorin et al. for details on why these three
virtual networks are needed.

The following code declares all of the needed message buffers.

```cpp
machine(MachineType:L1Cache, "MSI cache")
: Sequencer *sequencer;
  CacheMemory *cacheMemory;
  bool send_evictions;

  MessageBuffer * requestToDir, network="To", virtual_network="0", vnet_type="request";
  MessageBuffer * responseToDirOrSibling, network="To", virtual_network="2", vnet_type="response";

  MessageBuffer * forwardFromDir, network="From", virtual_network="1", vnet_type="forward";
  MessageBuffer * responseFromDirOrSibling, network="From", virtual_network="2", vnet_type="response";

  MessageBuffer * mandatoryQueue;

{

}
```

We have five different message buffers: two "To", two "From", and one
special message buffer. The "To" message buffers are similar to slave
ports in gem5. These are the message buffers that this controller uses
to send messages to other controllers in the system. The "From" message
buffers are like slave ports. This controller receives messages on
"From" buffers from other controllers in the system.

We have two different "To" buffers, one for low priority requests, and
one for high priority responses. The priority for the networks are not
inherent. The priority is based on the order that other controllers look
at the message buffers. It is a good idea to number the virtual networks
so that higher numbers mean higher priority, but the virtual network
number is ignored by Ruby except that messages on network 2 can only go
to other message buffers on network 2 (i.e., messages can't jump from
one network to another).

Similarly, there is two different ways this cache can receive messages,
either as a forwarded request from the directory (e.g., another cache
requests a writable block and we have a readable copy) or as a response
to a request this controller made. The response is higher priority than
the forwarded requests.

Finally, there is a special message buffer, the `mandatoryQueue`. This
message buffer is used by the `Sequencer` to convert gem5 packets into
Ruby requests. Unlike the other message buffers, `mandatoryQueue` does
not connect to the Ruby network. Note: the name of this message buffer
is hard-coded and must be exactly "mandatoryQueue".

As previously mentioned, this parameter block is converted into the
SimObject description file. Any parameters you put in this block will be
SimObject parameters that are accessible from the Python configuration
files. If you look at the generated file L1Cache\_Controller.py, it will
look very familiar. Note: This is a generated file and you should never
modify generated files directly!

```python
from m5.params import *
from m5.SimObject import SimObject
from Controller import RubyController

class L1Cache_Controller(RubyController):
    type = 'L1Cache_Controller'
    cxx_header = 'mem/protocol/L1Cache_Controller.hh'
    sequencer = Param.RubySequencer("")
    cacheMemory = Param.RubyCache("")
    send_evictions = Param.Bool("")
    requestToDir = Param.MessageBuffer("")
    responseToDirOrSibling = Param.MessageBuffer("")
    forwardFromDir = Param.MessageBuffer("")
    responseFromDirOrSibling = Param.MessageBuffer("")
    mandatoryQueue = Param.MessageBuffer("")
```

## State declarations

The next part of the state machine is the state declaration. Here, we
are going to declare all of the stable and transient states for the
state machine. We will follow the naming convention in Sorin et al. For
instance, the transient state "IM\_AD" corresponds to moving from
Invalid to Modified waiting on acks and data. These states come directly
from the left column of Table 8.3 in Sorin et al.

```cpp
state_declaration(State, desc="Cache states") {
    I,      AccessPermission:Invalid,
                desc="Not present/Invalid";

    // States moving out of I
    IS_D,   AccessPermission:Invalid,
                desc="Invalid, moving to S, waiting for data";
    IM_AD,  AccessPermission:Invalid,
                desc="Invalid, moving to M, waiting for acks and data";
    IM_A,   AccessPermission:Busy,
                desc="Invalid, moving to M, waiting for acks";

    S,      AccessPermission:Read_Only,
                desc="Shared. Read-only, other caches may have the block";

    // States moving out of S
    SM_AD,  AccessPermission:Read_Only,
                desc="Shared, moving to M, waiting for acks and 'data'";
    SM_A,   AccessPermission:Read_Only,
                desc="Shared, moving to M, waiting for acks";

    M,      AccessPermission:Read_Write,
                desc="Modified. Read & write permissions. Owner of block";

    // States moving to Invalid
    MI_A,   AccessPermission:Busy,
                desc="Was modified, moving to I, waiting for put ack";
    SI_A,   AccessPermission:Busy,
                desc="Was shared, moving to I, waiting for put ack";
    II_A,   AccessPermission:Invalid,
                desc="Sent valid data before receiving put ack. "Waiting for put ack.";
}
```

Each state has an associated access permission: "Invalid", "NotPresent",
"Busy", "Read\_Only", or "Read\_Write". The access permission is used
for *functional* accesses to the cache. Functional accesses are
debug-like accesses when the simulator wants to read or update the data
immediately. One example of this is reading in files in SE mode which
are directly loaded into memory.

For functional accesses all caches are checked to see if they have a
corresponding block with matching address. For functional reads, *all*
of the blocks with a matching address that have read-only or read-write
permission are accessed (they should all have the same data). For
functional writes, all blocks are updated with new data if they have
busy, read-only, or read-write permission.

## Event declarations

Next, we need to declare all of the events that are triggered by
incoming messages for this cache controller. These events come directly
from the first row in Table 8.3 in Sorin et al.

```cpp
enumeration(Event, desc="Cache events") {
    // From the processor/sequencer/mandatory queue
    Load,           desc="Load from processor";
    Store,          desc="Store from processor";

    // Internal event (only triggered from processor requests)
    Replacement,    desc="Triggered when block is chosen as victim";

    // Forwarded request from other cache via dir on the forward network
    FwdGetS,        desc="Directory sent us a request to satisfy GetS. We must have the block in M to respond to this.";
    FwdGetM,        desc="Directory sent us a request to satisfy GetM. We must have the block in M to respond to this.";
    Inv,            desc="Invalidate from the directory.";
    PutAck,         desc="Response from directory after we issue a put. This must be on the fwd network to avoid deadlock.";

    // Responses from directory
    DataDirNoAcks,  desc="Data from directory (acks = 0)";
    DataDirAcks,    desc="Data from directory (acks > 0)";

    // Responses from other caches
    DataOwner,      desc="Data from owner";
    InvAck,         desc="Invalidation ack from other cache after Inv";

    // Special event to simplify implementation
    LastInvAck,     desc="Triggered after the last ack is received";
}
```

## User-defined structures

Next, we need to define some structures that we will use in other places
in this controller. The first one we will define is `Entry`. This is the
structure that is stored in the `CacheMemory`. It only needs to contain
data and a state, but it may contain any other data you want. Note: The
state that this structure is storing is the `State` type that was
defined above, not a hardcoded state type.

You can find the abstract version of this class (`AbstractCacheEntry`)
in `src/mem/ruby/slicc_interface/AbstractCacheEntry.hh`. If you want to
use any of the member functions of `AbstractCacheEntry`, you need to
declare them here (this isn't used in this protocol).

```cpp
structure(Entry, desc="Cache entry", interface="AbstractCacheEntry") {
    State CacheState,        desc="cache state";
    DataBlock DataBlk,       desc="Data in the block";
}
```

Another structure we will need is a TBE. TBE is the "transaction buffer
entry". This stores information needed during transient states. This is
*like* an MSHR. It functions as an MSHR in this protocol, but the entry
is also allocated for other uses. In this protocol, it will store the
state (usually needed), data (also usually needed), and the number of
acks that this block is currently waiting for. The `AcksOutstanding` is
used for the transitions where other controllers send acks instead of
the data.

```cpp
structure(TBE, desc="Entry for transient requests") {
    State TBEState,         desc="State of block";
    DataBlock DataBlk,      desc="Data for the block. Needed for MI_A";
    int AcksOutstanding, default=0, desc="Number of acks left to receive.";
}
```

Next, we need a place to store all of the TBEs. This is an externally
defined class; it is defined in C++ outside of SLICC. Therefore, we need
to declare that we are going to use it, and also declare any of the
functions that we will call on it. You can find the code for the
`TBETable` in src/mem/ruby/structures/TBETable.hh. It is templatized on
the TBE structure defined above, which gets a little confusing, as we
will see.

```cpp
structure(TBETable, external="yes") {
  TBE lookup(Addr);
  void allocate(Addr);
  void deallocate(Addr);
  bool isPresent(Addr);
}
```

The `external="yes"` tells SLICC to not look for the definition of this
structure. This is similar to declaring a variable `extern` in C/C++.

## Other declarations and definitions required

Finally, we are going to go through some boilerplate of declaring
variables, declaring functions in `AbstractController` that we will use
in this controller, and defining abstract functions in
`AbstractController`.

First, we need to have a variable that stores a TBE table. We have to do
this in SLICC because it is not until this time that we know the true
type of the TBE table since the TBE type was defined above. This is some
particularly tricky (or nasty) code to get SLICC to generate the right
C++ code. The difficulty is that we want templatize `TBETable` based on
the `TBE` type above. The key is that SLICC mangles the names of all
types declared in the machine with the machine's name. For instance,
`TBE` is actually L1Cache\_TBE in C++.

We also want to pass a parameter to the constructor of the `TBETable`.
This is a parameter that is actually part of the `AbstractController`,
thus we need to use the C++ name for the variable since it doesn't have
a SLICC name.

```cpp
TBETable TBEs, template="<L1Cache_TBE>", constructor="m_number_of_TBEs";
```

If you can understand the above code, then you are an official SLICC
ninja!

Next, any functions that are part of AbstractController need to be
declared, if we are going to use them in the rest of the file. In this
case, we are only going to use `clockEdge()`:

```cpp
Tick clockEdge();
```

There are a few other functions we're going to use in actions. These
functions are used in actions to set and unset implicit variables
available in action code-blocks. Action code blocks will be explained in
detail in the action section \<MSI-actions-section\>. These may be
needed when a transition has many actions.

```cpp
void set_cache_entry(AbstractCacheEntry a);
void unset_cache_entry();
void set_tbe(TBE b);
void unset_tbe();
```

Another useful function is `mapAddressToMachine`. This allows us to
change the address mappings for banked directories or caches at runtime
so we don't have to hardcode them in the SLICC file.

```cpp
MachineID mapAddressToMachine(Addr addr, MachineType mtype);
```

Finally, you can also add any functions you may want to use in the file
and implement them here. For instance, it is convenient to access cache
blocks by address with a single function. Again, in this function there
is some SLICC trickery. We need to access "by pointer" since the cache
block is something that we need to be mutable later ("by reference"
would have been a better name). The cast is also necessary since we
defined a specific `Entry` type in the file, but the `CacheMemory` holds
the abstract type.

```cpp
// Convenience function to look up the cache entry.
// Needs a pointer so it will be a reference and can be updated in actions
Entry getCacheEntry(Addr address), return_by_pointer="yes" {
    return static_cast(Entry, "pointer", cacheMemory.lookup(address));
}
```

The next set of boilerplate code rarely changes between different
protocols. There's a set of functions that are pure-virtual in
`AbstractController` that we must implement.

`getState`
:   Given a TBE, cache entry, and address return the state of the block.
    This is called on the block to decide which transition to execute
    when an event is triggered. Usually, you return the state in the TBE
    or cache entry, whichever is valid.

`setState`
:   Given a TBE, cache entry, and address make sure the state is set
    correctly on the block. This is called at the end of the transition
    to set the final state on the block.

`getAccessPermission`
:   Get the access permission of a block. This is used during functional
    access to decide whether or not to functionally access the block. It
    is similar to `getState`, get the information from the TBE if valid,
    cache entry, if valid, or the block is not present.

`setAccessPermission`
:   Like `getAccessPermission`, but sets the permission.

`functionalRead`
:   Functionally read the data. It is possible the TBE has more
    up-to-date information, so check that first. Note: testAndRead/Write
    defined in src/mem/ruby/slicc\_interface/Util.hh

`functionalWrite`
:   Functionally write the data. Similarly, you may need to update the
    data in both the TBE and the cache entry.

```cpp
State getState(TBE tbe, Entry cache_entry, Addr addr) {
    // The TBE state will override the state in cache memory, if valid
    if (is_valid(tbe)) { return tbe.TBEState; }
    // Next, if the cache entry is valid, it holds the state
    else if (is_valid(cache_entry)) { return cache_entry.CacheState; }
    // If the block isn't present, then it's state must be I.
    else { return State:I; }
}

void setState(TBE tbe, Entry cache_entry, Addr addr, State state) {
  if (is_valid(tbe)) { tbe.TBEState := state; }
  if (is_valid(cache_entry)) { cache_entry.CacheState := state; }
}

AccessPermission getAccessPermission(Addr addr) {
    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        return L1Cache_State_to_permission(tbe.TBEState);
    }

    Entry cache_entry := getCacheEntry(addr);
    if(is_valid(cache_entry)) {
        return L1Cache_State_to_permission(cache_entry.CacheState);
    }

    return AccessPermission:NotPresent;
}

void setAccessPermission(Entry cache_entry, Addr addr, State state) {
    if (is_valid(cache_entry)) {
        cache_entry.changePermission(L1Cache_State_to_permission(state));
    }
}

void functionalRead(Addr addr, Packet *pkt) {
    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        testAndRead(addr, tbe.DataBlk, pkt);
    } else {
        testAndRead(addr, getCacheEntry(addr).DataBlk, pkt);
    }
}

int functionalWrite(Addr addr, Packet *pkt) {
    int num_functional_writes := 0;

    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        num_functional_writes := num_functional_writes +
            testAndWrite(addr, tbe.DataBlk, pkt);
        return num_functional_writes;
    }

    num_functional_writes := num_functional_writes +
            testAndWrite(addr, getCacheEntry(addr).DataBlk, pkt);
    return num_functional_writes;
}
```


---


## In port code blocks

*Source: https://www.gem5.orgdocumentation/learning_gem5/part3/cache-in-ports/*

After declaring all of the structures we need in the state machine file,
the first "functional" part of the file are the "in ports". This section
specifies what *events* to *trigger* on different incoming messages.

However, before we get to the in ports, we must declare our out ports.

```cpp
out_port(request_out, RequestMsg, requestToDir);
out_port(response_out, ResponseMsg, responseToDirOrSibling);
```

This code essentially just renames `requestToDir` and
`responseToDirOrSibling` to `request_out` and `response_out`. Later in
the file, when we want to *enqueue* messages to these message buffers we
will use the new names `request_out` and `response_out`. This also
specifies the exact implementation of the messages that we will send
across these ports. We will look at the exact definition of these types
below in the file `MSI-msg.sm`.

Next, we create an *in port code block*. In SLICC, there are many cases
where there are code blocks that look similar to `if` blocks, but they
encode specific information. For instance, the code inside an
`in_port()` block is put in a special generated file:
`L1Cache_Wakeup.cc`.

All of the `in_port` code blocks are executed in order (or based on the
priority if it is specified). On each active cycle for the controller,
the first `in_port` code is executed. If it is successful, it is
re-executed to see if there are other messages that can be consumed on
the port. If there are no messages or no events are triggered, then the
next `in_port` code block is executed.

There are three different kinds of *stalls* that can be generated when
executing `in_port` code blocks. First, there is a parameterized limit
for the number of transitions per cycle at each controller. If this
limit is reached (i.e., there are more messages on the message buffers
than the transition per cycle limit), then all `in_port` will stop
processing and wait to continue until the next cycle. Second, there
could be a *resource stall*. This happens if some needed resource is
unavailable. For instance, if using the `BankedArray` bandwidth model,
the needed bank of the cache may be currently occupied. Third, there
could be a *protocol stall*. This is a special kind of action that
causes the state machine to stall until the next cycle.

It is important to note that protocol stalls and resource stalls prevent
**all** `in_port` blocks from executing. For instance, if the first
`in_port` block generates a protocol stall, none of the other ports will
be executed, blocking all messages. This is why it is important to use
the correct number and ordering of virtual networks.

Below, is the full code for the `in_port` block for the highest priority
messages to our L1 cache controller, the response from directory or
other caches. Next we will break the code block down to explain each
section.

```cpp
in_port(response_in, ResponseMsg, responseFromDirOrSibling) {
    if (response_in.isReady(clockEdge())) {
        peek(response_in, ResponseMsg) {
            Entry cache_entry := getCacheEntry(in_msg.addr);
            TBE tbe := TBEs[in_msg.addr];
            assert(is_valid(tbe));

            if (machineIDToMachineType(in_msg.Sender) ==
                        MachineType:Directory) {
                if (in_msg.Type != CoherenceResponseType:Data) {
                    error("Directory should only reply with data");
                }
                assert(in_msg.Acks + tbe.AcksOutstanding >= 0);
                if (in_msg.Acks + tbe.AcksOutstanding == 0) {
                    trigger(Event:DataDirNoAcks, in_msg.addr, cache_entry,
                            tbe);
                } else {
                    trigger(Event:DataDirAcks, in_msg.addr, cache_entry,
                            tbe);
                }
            } else {
                if (in_msg.Type == CoherenceResponseType:Data) {
                    trigger(Event:DataOwner, in_msg.addr, cache_entry,
                            tbe);
                } else if (in_msg.Type == CoherenceResponseType:InvAck) {
                    DPRINTF(RubySlicc, "Got inv ack. %d left\n",
                            tbe.AcksOutstanding);
                    if (tbe.AcksOutstanding == 1) {
                        trigger(Event:LastInvAck, in_msg.addr, cache_entry,
                                tbe);
                    } else {
                        trigger(Event:InvAck, in_msg.addr, cache_entry,
                                tbe);
                    }
                } else {
                    error("Unexpected response from other cache");
                }
            }
        }
    }
}
```

First, like the out\_port above "response\_in" is the name we'll use
later when we refer to this port, and "ResponseMsg" is the type of
message we expect on this port (since this port processes responses to
our requests). The first step in all `in_port` code blocks is to check
the message buffer to see if there are any messages to be processed. If
not, then this `in_port` code block is skipped and the next one is
executed.

```cpp
in_port(response_in, ResponseMsg, responseFromDirOrSibling) {
    if (response_in.isReady(clockEdge())) {
        . . .
    }
}
```

Assuming there is a valid message in the message buffer, next, we grab
that message by using the special code block `peek`. Peek is a special
function. Any code inside a peek statement has a special variable
declared and populated: `in_msg`. This contains the message (of type
ResponseMsg in this case as specified by the second parameter of the
`peek` call) at the head of the port. Here, `response_in` is the port we
want to peek into.

Then, we need to grab the cache entry and the TBE for the incoming
address. (We will look at the other parameters in response message
below.) Above, we implemented getCacheEntry. It will return either the
valid matching entry for the address, or an invalid entry if there is
not a matching cache block.

For the TBE, since this is a response to a request this cache controller
initiated, there *must* be a valid TBE in the TBE table. Hence, we see
our first debug statement, an *assert*. This is one of the ways to ease
debugging of cache coherence protocols. It is encouraged to use asserts
liberally to make debugging easier.

```cpp
peek(response_in, ResponseMsg) {
    Entry cache_entry := getCacheEntry(in_msg.addr);
    TBE tbe := TBEs[in_msg.addr];
    assert(is_valid(tbe));

    . . .
}
```

Next, we need to decide what event to trigger based on the message. For
this, we first need to discuss what data response messages are carrying.

To declare a new message type, first create a new file for all of the
message types: `MSI-msg.sm`. In this file, you can declare any
structures that will be *globally* used across all of the SLICC files
for your protocol. We will include this file in all of the state machine
definitions via the `MSI.slicc` file later. This is similar to including
global definitions in header files in C/C++.

In the `MSI-msg.sm` file, add the following code block:

```cpp
structure(ResponseMsg, desc="Used for Dir->Cache and Fwd message responses",
          interface="Message") {
    Addr addr,                   desc="Physical address for this response";
    CoherenceResponseType Type,  desc="Type of response";
    MachineID Sender,            desc="Node who is responding to the request";
    NetDest Destination,         desc="Multicast destination mask";
    DataBlock DataBlk,           desc="data for the cache line";
    MessageSizeType MessageSize, desc="size category of the message";
    int Acks,                    desc="Number of acks required from others";

    // This must be overridden here to support functional accesses
    bool functionalRead(Packet *pkt) {
        if (Type == CoherenceResponseType:Data) {
            return testAndRead(addr, DataBlk, pkt);
        }
        return false;
    }

    bool functionalWrite(Packet *pkt) {
        // No check on message type required since the protocol should read
        // data block from only those messages that contain valid data
        return testAndWrite(addr, DataBlk, pkt);
    }
}
```

The message is just another SLICC structure similar to the structures
we've defined before. However, this time, we have a specific interface
that it is implementing: `Message`. Within this message, we can add any
members that we need for our protocol. In this case, we first have the
address. Note, a common "gotcha" is that you *cannot* use "Addr" with a
capitol "A" for the name of the member since it is the same name as the
type!

Next, we have the type of response. In our case, there are two types of
response data and invalidation acks from other caches after they have
invalidated their copy. Thus, we need to define an *enumeration*, the
`CoherenceResponseType`, to use it in this message. Add the following
code *before* the `ResponseMsg` declaration in the same file.

```cpp
enumeration(CoherenceResponseType, desc="Types of response messages") {
    Data,       desc="Contains the most up-to-date data";
    InvAck,     desc="Message from another cache that they have inv. the blk";
}
```

Next, in the response message type, we have the `MachineID` which sent
the response. `MachineID` is the *specific machine* that sent the
response. For instance, it might be directory 0 or cache 12. The
`MachineID` contains both the `MachineType` (e.g., we have been creating
an `L1Cache` as declared in the first `machine()`) and the specific
*version* of that machine type. We will come back to machine version
numbers when configuring the system.

Next, all messages need a *destination*, and a *size*. The destination
is specified as a `NetDest`, which is a bitmap of all the `MachineID` in
the system. This allows messages to be broadcast to a flexible set of
receivers. The message also has a size. You can find the possible
message sizes in `src/mem/ruby/protocol/RubySlicc_Exports.sm`.

This message may also contain a data block and the number acks that are
expected. Thus, we can include these in the message definition as well.

Finally, we also have to define functional read and write functions.
These are used by Ruby to inspect in-flight messages on function reads
and writes. Note: This functionality currently is very brittle and if
there are messages in-flight for an address that is functionally read or
written the functional access may fail.

You can download the complete `MSI-msg.sm` file 
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-msg.sm).

Now that we have defined the data in the response message, we can look
at how we choose which action to trigger in the `in_port` for response
to the cache.

```cpp
// If it's from the directory...
if (machineIDToMachineType(in_msg.Sender) ==
            MachineType:Directory) {
    if (in_msg.Type != CoherenceResponseType:Data) {
        error("Directory should only reply with data");
    }
    assert(in_msg.Acks + tbe.AcksOutstanding >= 0);
    if (in_msg.Acks + tbe.AcksOutstanding == 0) {
        trigger(Event:DataDirNoAcks, in_msg.addr, cache_entry,
                tbe);
    } else {
        trigger(Event:DataDirAcks, in_msg.addr, cache_entry,
                tbe);
    }
} else {
    // This is from another cache.
    if (in_msg.Type == CoherenceResponseType:Data) {
        trigger(Event:DataOwner, in_msg.addr, cache_entry,
                tbe);
    } else if (in_msg.Type == CoherenceResponseType:InvAck) {
        DPRINTF(RubySlicc, "Got inv ack. %d left\n",
                tbe.AcksOutstanding);
        if (tbe.AcksOutstanding == 1) {
            // If there is exactly one ack remaining then we
            // know it is the last ack.
            trigger(Event:LastInvAck, in_msg.addr, cache_entry,
                    tbe);
        } else {
            trigger(Event:InvAck, in_msg.addr, cache_entry,
                    tbe);
        }
    } else {
        error("Unexpected response from other cache");
    }
}
```

First, we check to see if the message comes from the directory or
another cache. If it comes from the directory, we know that it *must* be
a data response (the directory will never respond with an ack).

Here, we meet our second way to add debug information to protocols: the
`error` function. This function breaks simulation and prints out the
string parameter similar to `panic`.

Next, when we receive data from the directory, we expect that the number
of acks we are waiting for will never be less than 0. The number of acks
we're waiting for is the current acks we have received
(tbe.AcksOutstanding) and the number of acks the directory has told us
to be waiting for. We need to check it this way because it is possible
that we have received acks from other caches before we get the message
from the directory that we need to wait for acks.

There are two possibilities for the acks, either we have already
received all of the acks and now we are getting the data (data from dir
acks==0 in Table 8.3), or we need to wait for more acks. Thus, we check
this condition and trigger two different events, one for each
possibility.

When triggering transitions, you need to pass four parameters. The first
parameter is the event to trigger. These events were specified earlier
in the `Event` declaration. The next parameter is the (physical memory)
address of the cache block to operate on. Usually this is the same as
the address of the `in_msg`, but it may be different, for instance, on a
replacement the address is for the block being replaced. Next is the
cache entry and the TBE for the block. These may be invalid if there are
no valid entries for the address in the cache or there is not a valid
TBE in the TBE table.

When we implement actions below, we will see how these last three
parameters are used. They are passed into the actions as implicit
variables: `address`, `cache_entry`, and `tbe`.

If the `trigger` function is executed, after the transition is complete,
the `in_port` logic is executed again, assuming there have been fewer
transitions than that maximum transitions per cycle. If there are other
messages in the message buffer more transitions can be triggered.

If the response is from another cache instead of the directory, then
other events are triggered, as shown in the code above. These events
come directly from Table 8.3 in Sorin et al.

Importantly, you should use the `in_port` logic to check all conditions.
After an event is triggered, it should only have a *single code path*.
I.e., there should be no `if` statements in any action blocks. If you
want to conditionally execute actions, you should use different states
or different events in the `in_port` logic.

The reason for this constraint is the way Ruby checks resources before
executing a transition. In the generated code from the `in_port` blocks
before the transition is actually executed all of the resources are
checked. In other words, transitions are atomic and either execute all
of the actions or none. Conditional statements inside the actions
prevents the SLICC compiler from correctly tracking the resource usage
and can lead to strange performance, deadlocks, and other bugs.

After specifying the `in_port` logic for the highest priority network,
the response network, we need to add the `in_port` logic for the forward
request network. However, before specifying this logic, we need to
define the `RequestMsg` type and the `CoherenceRequestType` which
contains the types of requests. These two definitions go in the
`MSI-msg.sm` file *not in MSI-cache.sm* since they are global
definitions.

It is possible to implement this as two different messages and request
type enumerations, one for forward and one for normal requests, but it
simplifies the code to use a single message and type.

```cpp
enumeration(CoherenceRequestType, desc="Types of request messages") {
    GetS,       desc="Request from cache for a block with read permission";
    GetM,       desc="Request from cache for a block with write permission";
    PutS,       desc="Sent to directory when evicting a block in S (clean WB)";
    PutM,       desc="Sent to directory when evicting a block in M";

    // "Requests" from the directory to the caches on the fwd network
    Inv,        desc="Probe the cache and invalidate any matching blocks";
    PutAck,     desc="The put request has been processed.";
}
```

```cpp
structure(RequestMsg, desc="Used for Cache->Dir and Fwd messages",  interface="Message") {
    Addr addr,                   desc="Physical address for this request";
    CoherenceRequestType Type,   desc="Type of request";
    MachineID Requestor,         desc="Node who initiated the request";
    NetDest Destination,         desc="Multicast destination mask";
    DataBlock DataBlk,           desc="data for the cache line";
    MessageSizeType MessageSize, desc="size category of the message";

    bool functionalRead(Packet *pkt) {
        // Requests should never have the only copy of the most up-to-date data
        return false;
    }

    bool functionalWrite(Packet *pkt) {
        // No check on message type required since the protocol should read
        // data block from only those messages that contain valid data
        return testAndWrite(addr, DataBlk, pkt);
    }
}
```

Now, we can specify the logic for the forward network `in_port`. This
logic is straightforward and triggers a different event for each request
type.

```cpp
in_port(forward_in, RequestMsg, forwardFromDir) {
    if (forward_in.isReady(clockEdge())) {
        peek(forward_in, RequestMsg) {
            // Grab the entry and tbe if they exist.
            Entry cache_entry := getCacheEntry(in_msg.addr);
            TBE tbe := TBEs[in_msg.addr];

            if (in_msg.Type == CoherenceRequestType:GetS) {
                trigger(Event:FwdGetS, in_msg.addr, cache_entry, tbe);
            } else if (in_msg.Type == CoherenceRequestType:GetM) {
                trigger(Event:FwdGetM, in_msg.addr, cache_entry, tbe);
            } else if (in_msg.Type == CoherenceRequestType:Inv) {
                trigger(Event:Inv, in_msg.addr, cache_entry, tbe);
            } else if (in_msg.Type == CoherenceRequestType:PutAck) {
                trigger(Event:PutAck, in_msg.addr, cache_entry, tbe);
            } else {
                error("Unexpected forward message!");
            }
        }
    }
}
```

The final `in_port` is for the mandatory queue. This is the lowest
priority queue, so it must be lowest in the state machine file. The
mandatory queue has a special message type: `RubyRequest`. This type is
specified in `src/mem/protocol/RubySlicc_Types.sm` It contains two
different addresses, the `LineAddress` which is cache-block aligned and
the `PhysicalAddress` which holds the original request's address and may
not be cache-block aligned. It also has other members that may be useful
in some protocols. However, for this simple protocol we only need the
`LineAddress`.

```cpp
in_port(mandatory_in, RubyRequest, mandatoryQueue) {
    if (mandatory_in.isReady(clockEdge())) {
        peek(mandatory_in, RubyRequest, block_on="LineAddress") {
            Entry cache_entry := getCacheEntry(in_msg.LineAddress);
            TBE tbe := TBEs[in_msg.LineAddress];

            if (is_invalid(cache_entry) &&
                    cacheMemory.cacheAvail(in_msg.LineAddress) == false ) {
                Addr addr := cacheMemory.cacheProbe(in_msg.LineAddress);
                Entry victim_entry := getCacheEntry(addr);
                TBE victim_tbe := TBEs[addr];
                trigger(Event:Replacement, addr, victim_entry, victim_tbe);
            } else {
                if (in_msg.Type == RubyRequestType:LD ||
                        in_msg.Type == RubyRequestType:IFETCH) {
                    trigger(Event:Load, in_msg.LineAddress, cache_entry,
                            tbe);
                } else if (in_msg.Type == RubyRequestType:ST) {
                    trigger(Event:Store, in_msg.LineAddress, cache_entry,
                            tbe);
                } else {
                    error("Unexpected type from processor");
                }
            }
        }
    }
}
```

There are a couple of new concepts shown in this code block. First, we
use `block_on="LineAddress"` in the peek function. What this does is
ensure that any other requests to the same cache line will be blocked
until the current request is complete.

Next, we check if the cache entry for this line is valid. If not, and
there are no more entries available in the set, then we need to evict
another entry. To get the victim address, we can use the `cacheProbe`
function on the `CacheMemory` object. This function uses the
parameterized replacement policy and returns the physical (line) address
of the victim.

Importantly, when we trigger the `Replacement` event *we use the address
of the victim block* and the victim cache entry and tbe. Thus, when we
take actions in the replacement transitions we will be acting on the
victim block, not the requesting block. Additionally, we need to
remember to *not* remove the requesting message from the mandatory queue
(pop) until it has been satisfied. The message should not be popped
after the replacement is complete.

If the cache block was found to be valid, then we simply trigger the
`Load` or `Store` event.


---


## Action code blocks

*Source: https://www.gem5.org/documentation/learning_gem5/part3/cache-actions/*

## Action code blocks

The next section of the state machine file is the action blocks. The
action blocks are executed during a transition from one state to
another, and are called by the transition code blocks (which we will
discuss in the next section \<MSI-transitions-section\>). Actions are
*single action* blocks. Some examples are "send a message to the
directory" and "pop the head of the buffer". Each action should be small
and only perform a single action.

The first action we will implement is an action to send a GetS request
to the directory. We need to send a GetS request to the directory
whenever we want to read some data that is not in the Modified or Shared
states in our cache. As previously mentioned, there are three variables
that are automatically populated inside the action block (like the
`in_msg` in `peek` blocks). `address` is the address that was passed
into the `trigger` function, `cache_entry` is the cache entry passed
into the `trigger` function, and `tbe` is the TBE passed into the
`trigger` function.

```cpp
action(sendGetS, 'gS', desc="Send GetS to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:GetS;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        // See mem/protocol/RubySlicc_Exports.sm for possible sizes.
        out_msg.MessageSize := MessageSizeType:Control;
        // Set that the requestor is this machine so we get the response.
        out_msg.Requestor := machineID;
    }
}
```

When specifying the action block, there are two parameters: a
description and a "shorthand". These two parameters are used in the HTML
table generation. The shorthand shows up in the transition cell, so it
should be as short as possible. SLICC provides a special syntax to allow
for bold (''), superscript ('\^'), and spaces ('\_') in the shorthand to
help keep them short. Second, the description also shows up in the HTML
table when you click on a particular action. The description can be
longer and help explain what the action does.

Next, in this action we are going to send a message to the directory on
the `request_out` port as declared above the `in_port` blocks. The
`enqueue` function is similar to the `peek` function since it requires a
code block. `enqueue`, however, has the special variable `out_msg`. In
the `enqueue` block, you can modify the `out_msg` with the current data.

The `enqueue` block takes three parameters, the message buffer to send
the message, the type of the message, and a latency. This latency (1
cycle in the example above and throughout this cache controller) is the
*cache latency*. This is where you specify the latency of accessing the
cache, in this case for a miss. Below we will see that specifying the
latency for a hit is similar.

Inside the `enqueue` block is where the message data is populated. For
the address of the request, we can use the automatically populated
`address` variable. We are sending a GetS message, so we use that
message type. Next, we need to specify the destination of the message.
For this, we use the `mapAddressToMachine` function that takes the
address and the machine type we are sending to. This will look up in the
correct `MachineID` based on the address. We call `Destination.add`
because `Destination` is a `NetDest` object, or a bitmap of all
`MachineID`.

Finally, we need to specify the message size (from
`mem/protocol/RubySlicc_Exports.sm`) and set ourselves as the requestor.
By setting this `machineID` as the requestor, it will allow the
directory to respond to this cache or forward it to another cache to
respond to this request.

Similarly, we can create actions for sending other get and put requests.
Note that get requests represent requests for data and put requests
represent requests where we downgrading or evicting our copy of the
data.

```cpp
action(sendGetM, "gM", desc="Send GetM to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:GetM;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.MessageSize := MessageSizeType:Control;
        out_msg.Requestor := machineID;
    }
}

action(sendPutS, "pS", desc="Send PutS to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:PutS;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.MessageSize := MessageSizeType:Control;
        out_msg.Requestor := machineID;
    }
}

action(sendPutM, "pM", desc="Send putM+data to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:PutM;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.DataBlk := cache_entry.DataBlk;
        out_msg.MessageSize := MessageSizeType:Data;
        out_msg.Requestor := machineID;
    }
}
```

Next, we need to specify an action to send data to another cache in the
case that we get a forwarded request from the directory for another
cache. In this case, we have to peek into the request queue to get other
data from the requesting message. This peek code block is exactly the
same as the ones in the `in_port`. When you nest an `enqueue` block in a
`peek` block both `in_msg` and `out_msg` variables are available. This
is needed so we know which other cache to send the data to.
Additionally, in this action we use the `cache_entry` variable to get
the data to send to the other cache.

```cpp
action(sendCacheDataToReq, "cdR", desc="Send cache data to requestor") {
    assert(is_valid(cache_entry));
    peek(forward_in, RequestMsg) {
        enqueue(response_out, ResponseMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceResponseType:Data;
            out_msg.Destination.add(in_msg.Requestor);
            out_msg.DataBlk := cache_entry.DataBlk;
            out_msg.MessageSize := MessageSizeType:Data;
            out_msg.Sender := machineID;
        }
    }
}
```

Next, we specify actions for sending data to the directory and sending
an invalidation ack to the original requestor on a forward request when
this cache does not have the data.

```cpp
action(sendCacheDataToDir, "cdD", desc="Send the cache data to the dir") {
    enqueue(response_out, ResponseMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceResponseType:Data;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.DataBlk := cache_entry.DataBlk;
        out_msg.MessageSize := MessageSizeType:Data;
        out_msg.Sender := machineID;
    }
}

action(sendInvAcktoReq, "iaR", desc="Send inv-ack to requestor") {
    peek(forward_in, RequestMsg) {
        enqueue(response_out, ResponseMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceResponseType:InvAck;
            out_msg.Destination.add(in_msg.Requestor);
            out_msg.DataBlk := cache_entry.DataBlk;
            out_msg.MessageSize := MessageSizeType:Control;
            out_msg.Sender := machineID;
        }
    }
}
```

Another required action is to decrement the number of acks we are
waiting for. This is used when we get a invalidation ack from another
cache to track the total number of acks. For this action, we assume that
there is a valid TBE and modify the implicit `tbe` variable in the
action block.

Additionally, we have another example of making debugging easier in
protocols: `APPEND_TRANSITION_COMMENT`. This function takes a string, or
something that can easily be converted to a string (e.g., `int`) as a
parameter. It modifies the *protocol trace* output, which we will
discuss in the [debugging section](../MSIdebugging). On each
protocol trace line that executes this action it will print the total
number of acks this cache is still waiting on. This is useful since the
number of remaining acks is part of the cache block state.

```cpp
action(decrAcks, "da", desc="Decrement the number of acks") {
    assert(is_valid(tbe));
    tbe.AcksOutstanding := tbe.AcksOutstanding - 1;
    APPEND_TRANSITION_COMMENT("Acks: ");
    APPEND_TRANSITION_COMMENT(tbe.AcksOutstanding);
}
```

We also need an action to store the acks when we receive a message from
the directory with an ack count. For this action, we peek into the
directory's response message to get the number of acks and store them in
the (required to be valid) TBE.

```cpp
action(storeAcks, "sa", desc="Store the needed acks to the TBE") {
    assert(is_valid(tbe));
    peek(response_in, ResponseMsg) {
        tbe.AcksOutstanding := in_msg.Acks + tbe.AcksOutstanding;
    }
    assert(tbe.AcksOutstanding > 0);
}
```

The next set of actions are to respond to CPU requests on hits and
misses. For these actions, we need to notify the sequencer (the
interface between Ruby and the rest of gem5) of the new data. In the
case of a store, we give the sequencer a pointer to the data block and
the sequencer updates the data in-place.

```cpp
action(loadHit, "Lh", desc="Load hit") {
    assert(is_valid(cache_entry));
    cacheMemory.setMRU(cache_entry);
    sequencer.readCallback(address, cache_entry.DataBlk, false);
}

action(externalLoadHit, "xLh", desc="External load hit (was a miss)") {
    assert(is_valid(cache_entry));
    peek(response_in, ResponseMsg) {
        cacheMemory.setMRU(cache_entry);
        // Forward the type of machine that responded to this request
        // E.g., another cache or the directory. This is used for tracking
        // statistics.
        sequencer.readCallback(address, cache_entry.DataBlk, true,
                               machineIDToMachineType(in_msg.Sender));
    }
}

action(storeHit, "Sh", desc="Store hit") {
    assert(is_valid(cache_entry));
    cacheMemory.setMRU(cache_entry);
    // The same as the read callback above.
    sequencer.writeCallback(address, cache_entry.DataBlk, false);
}

action(externalStoreHit, "xSh", desc="External store hit (was a miss)") {
    assert(is_valid(cache_entry));
    peek(response_in, ResponseMsg) {
        cacheMemory.setMRU(cache_entry);
        sequencer.writeCallback(address, cache_entry.DataBlk, true,
                               // Note: this could be the last ack.
                               machineIDToMachineType(in_msg.Sender));
    }
}

action(forwardEviction, "e", desc="sends eviction notification to CPU") {
    if (send_evictions) {
        sequencer.evictionCallback(address);
    }
}
```

In each of these actions, it is vital that we call `setMRU` on the cache
entry. The `setMRU` function is what allows the replacement policy to
know which blocks are most recently accessed. If you leave out the
`setMRU` call, the replacement policy will not operate correctly!

On loads and stores, we call the `read/writeCallback` function on the
`sequencer`. This notifies the sequencer of the new data or allows it to
write the data into the data block. These functions take four parameters
(the last parameter is optional): address, data block, a boolean for if
the original request was a miss, and finally, an optional `MachineType`.
The final optional parameter is used for tracking statistics on where
the data for the request was found. It allows you to track whether the
data comes from cache-to-cache transfers or from memory.

Finally, we also have an action to forward evictions to the CPU. This is
required for gem5's out-of-order models to squash speculative loads if
the cache block is evicted before the load is committed. We use the
parameter specified at the top of the state machine file to check if
this is needed or not.

Next, we have a set of cache management actions that allocate and free
cache entries and TBEs. To create a new cache entry, we must have space
in the `CacheMemory` object. Then, we can call the `allocate` function.
This allocate function doesn't actually allocate the host memory for the
cache entry since this controller specialized the `Entry` type, which is
why we need to pass a `new Entry` to the `allocate` function.

Additionally, in these actions we call `set_cache_entry`,
`unset_cache_entry`, and similar functions for the TBE. These set and
unset the implicit variables that were passed in via the `trigger`
function. For instance, when allocating a new cache block, we call
`set_cache_entry` and in all actions proceeding `allocateCacheBlock` the
`cache_entry` variable will be valid.

There is also an action that copies the data from the cache data block
to the TBE. This allows us to keep the data around even after removing
the cache block until we are sure that this cache no longer are
responsible for the data.

```cpp
action(allocateCacheBlock, "a", desc="Allocate a cache block") {
    assert(is_invalid(cache_entry));
    assert(cacheMemory.cacheAvail(address));
    set_cache_entry(cacheMemory.allocate(address, new Entry));
}

action(deallocateCacheBlock, "d", desc="Deallocate a cache block") {
    assert(is_valid(cache_entry));
    cacheMemory.deallocate(address);
    // clear the cache_entry variable (now it's invalid)
    unset_cache_entry();
}

action(writeDataToCache, "wd", desc="Write data to the cache") {
    peek(response_in, ResponseMsg) {
        assert(is_valid(cache_entry));
        cache_entry.DataBlk := in_msg.DataBlk;
    }
}

action(allocateTBE, "aT", desc="Allocate TBE") {
    assert(is_invalid(tbe));
    TBEs.allocate(address);
    // this updates the tbe variable for other actions
    set_tbe(TBEs[address]);
}

action(deallocateTBE, "dT", desc="Deallocate TBE") {
    assert(is_valid(tbe));
    TBEs.deallocate(address);
    // this makes the tbe variable invalid
    unset_tbe();
}

action(copyDataFromCacheToTBE, "Dct", desc="Copy data from cache to TBE") {
    assert(is_valid(cache_entry));
    assert(is_valid(tbe));
    tbe.DataBlk := cache_entry.DataBlk;
}
```

The next set of actions are for managing the message buffers. We need to
add actions to pop the head message off of the buffers after the message
has been satisfied. The `dequeue` function takes a single parameter, a
time for the dequeue to take place. Delaying the dequeue for a cycle
prevents the `in_port` logic from consuming another message from the
same message buffer in a single cycle.

```cpp
action(popMandatoryQueue, "pQ", desc="Pop the mandatory queue") {
    mandatory_in.dequeue(clockEdge());
}

action(popResponseQueue, "pR", desc="Pop the response queue") {
    response_in.dequeue(clockEdge());
}

action(popForwardQueue, "pF", desc="Pop the forward queue") {
    forward_in.dequeue(clockEdge());
}
```

Finally, the last action is a stall. Below, we are using a "z\_stall",
which is the simplest kind of stall in SLICC. By leaving the action
blank, it generates a "protocol stall" in the `in_port` logic which
stalls all messages from being processed in the current message buffer
and all lower priority message buffer. Protocols using "z\_stall" are
usually simpler, but lower performance since a stall on a high priority
buffer can stall many requests that may not need to be stalled.

```cpp
action(stall, "z", desc="Stall the incoming request") {
    // z_stall
}
```

There are two other ways to deal with messages that cannot currently be
processed that can improve the performance of protocols. (Note: We will
not be using these more complicated techniques in this simple example
protocol.) The first is `recycle`. The message buffers have a `recycle`
function that moves the request on the head of the queue to the tail.
This allows other requests in the buffer or requests in other buffers to
be processed immediately. `recycle` actions often improve the
performance of protocols significantly.

However, `recycle` is not very realistic when compared to real
implementations of cache coherence. For a more realistic
high-performance solution to stalling messages, Ruby provides the
`stall_and_wait` function on message buffers. This function takes the
head request and moves it into a separate structure tagged by an
address. The address is user-specified, but is usually the request's
address. Later, when the blocked request can be handled, there is
another function `wakeUpBuffers(address)` which will wake up all
requests stalled on `address` and `wakeUpAllBuffers()` that wakes up all
of the stalled requests. When a request is "woken up" it is placed back
into the message buffer to be subsequently processed.


---


## Transition code blocks

*Source: https://www.gem5.org/documentation/learning_gem5/part3/cache-transitions/*

## Transition code blocks

Finally, we've reached the final section of the state machine file! This
section contains the details for all of the transitions between states
and what actions to execute during the transition.

So far in this chapter we have written the state machine top to bottom
one section at a time. However, in most cache coherence implementations
you will find that you need to move around between sections. For
instance, when writing the transitions you will realize you forgot to
add an action, or you notice that you actually need another transient
state to implement the protocol. This is the normal way to write
protocols, but for simplicity this chapter goes through the file top to
bottom.

Transition blocks consist of two parts. First, the first line of a
transition block contains the begin state, event to transition on, and
end state (the end state may not be required, as we will discuss below).
Second, the transition block contains all of the actions to execute on
this transition. For instance, a simple transition in the MSI protocol
is transitioning out of Invalid on a Load.

```cpp
transition(I, Load, IS_D) {
    allocateCacheBlock;
    allocateTBE;
    sendGetS;
    popMandatoryQueue;
}
```

First, you specify the transition as the "parameters" to the
`transition` statement. In this case, if the initial state is `I` and
the event is `Load` then transition to `IS_D` (was invalid, going to
shared, waiting for data). This transition is straight out of Table 8.3
in Sorin et al.

Then, inside the `transition` code block, all of the actions that will
execute are listed in order. For this transition first we allocate the
cache block. Remember that in the `allocateCacheBlock` action the newly
allocated entry is set to the entry that will be used in the rest of the
actions. After allocating the cache block, we also allocate a TBE. This
could be used if we need to wait for acks from other caches. Next, we
send a GetS request to the directory, and finally we pop the head entry
off of the mandatory queue since we have fully handled it.

```cpp
transition(IS_D, {Load, Store, Replacement, Inv}) {
    stall;
}
```

In this transition, we use slightly different syntax. According to Table
8.3 from Sorin et al., we should stall if the cache is in IS\_D on
loads, stores, replacements, and invalidates. We can specify a single
transition statement for this by including multiple events in curly
brackets as above. Additionally, the final state isn't required. If the
final state isn't specified, then the transition is executed and the
state is not updated (i.e., the block stays in its beginning state). You
can read the above transition as "If the cache block is in state IS\_D
and there is a load, store, replacement, or invalidate stall the
protocol and do not transition out of the state." You can also use curly
brackets for beginning states, as shown in some of the transitions
below.

Below is the rest of the transitions needed to implement the L1 cache
from the MSI protocol.

```cpp
transition(IS_D, {DataDirNoAcks, DataOwner}, S) {
    writeDataToCache;
    deallocateTBE;
    externalLoadHit;
    popResponseQueue;
}

transition({IM_AD, IM_A}, {Load, Store, Replacement, FwdGetS, FwdGetM}) {
    stall;
}

transition({IM_AD, SM_AD}, {DataDirNoAcks, DataOwner}, M) {
    writeDataToCache;
    deallocateTBE;
    externalStoreHit;
    popResponseQueue;
}

transition(IM_AD, DataDirAcks, IM_A) {
    writeDataToCache;
    storeAcks;
    popResponseQueue;
}

transition({IM_AD, IM_A, SM_AD, SM_A}, InvAck) {
    decrAcks;
    popResponseQueue;
}

transition({IM_A, SM_A}, LastInvAck, M) {
    deallocateTBE;
    externalStoreHit;
    popResponseQueue;
}

transition({S, SM_AD, SM_A, M}, Load) {
    loadHit;
    popMandatoryQueue;
}

transition(S, Store, SM_AD) {
    allocateTBE;
    sendGetM;
    popMandatoryQueue;
}

transition(S, Replacement, SI_A) {
    sendPutS;
    forwardEviction;
}

transition(S, Inv, I) {
    sendInvAcktoReq;
    deallocateCacheBlock;
    forwardEviction;
    popForwardQueue;
}

transition({SM_AD, SM_A}, {Store, Replacement, FwdGetS, FwdGetM}) {
    stall;
}

transition(SM_AD, Inv, IM_AD) {
    sendInvAcktoReq;
    forwardEviction;
    popForwardQueue;
}

transition(SM_AD, DataDirAcks, SM_A) {
    writeDataToCache;
    storeAcks;
    popResponseQueue;
}

transition(M, Store) {
    storeHit;
    popMandatoryQueue;
}

transition(M, Replacement, MI_A) {
    sendPutM;
    forwardEviction;
}

transition(M, FwdGetS, S) {
    sendCacheDataToReq;
    sendCacheDataToDir;
    popForwardQueue;
}

transition(M, FwdGetM, I) {
    sendCacheDataToReq;
    deallocateCacheBlock;
    popForwardQueue;
}

transition({MI_A, SI_A, II_A}, {Load, Store, Replacement}) {
    stall;
}

transition(MI_A, FwdGetS, SI_A) {
    sendCacheDataToReq;
    sendCacheDataToDir;
    popForwardQueue;
}

transition(MI_A, FwdGetM, II_A) {
    sendCacheDataToReq;
    popForwardQueue;
}

transition({MI_A, SI_A, II_A}, PutAck, I) {
    deallocateCacheBlock;
    popForwardQueue;
}

transition(SI_A, Inv, II_A) {
    sendInvAcktoReq;
    popForwardQueue;
}
```

You can download the complete `MSI-cache.sm` file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-cache.sm).


---


## MSI Directory implementation

*Source: https://www.gem5.org/documentation/learning_gem5/part3/directory/*

Implementing a directory controller is very similar to the L1 cache
controller, except using a different state machine table. The state
machine fore the directory can be found in Table 8.2 in Sorin et al.
Since things are mostly similar to the L1 cache, this section mostly
just discusses a few more SLICC details and a few differences between
directory controllers and cache controllers. Let's dive straight in and
start modifying a new file `MSI-dir.sm`.

```cpp
machine(MachineType:Directory, "Directory protocol")
:
  DirectoryMemory * directory;
  Cycles toMemLatency := 1;

MessageBuffer *forwardToCache, network="To", virtual_network="1",
      vnet_type="forward";
MessageBuffer *responseToCache, network="To", virtual_network="2",
      vnet_type="response";

MessageBuffer *requestFromCache, network="From", virtual_network="0",
      vnet_type="request";

MessageBuffer *responseFromCache, network="From", virtual_network="2",
      vnet_type="response";

MessageBuffer *requestToMemory;

MessageBuffer *responseFromMemory;

{
. . .
}
```

First, there are two parameter to this directory controller,
`DirectoryMemory` and a `toMemLatency`. The `DirectoryMemory` is a
little weird. It is allocated at initialization time such that it can
cover *all* of physical memory, like a complete directory *not a
directory cache*. I.e., there are pointers in the `DirectoryMemory`
object for every 64-byte block in physical memory. However, the actual
entries (as defined below) are lazily created via `getDirEntry()`. We'll
see more details about `DirectoryMemory` below.

Next, is the `toMemLatency` parameter. This will be used in the
`enqueue` function when enqueuing requests to model the directory
latency. We didn't use a parameter for this in the L1 cache, but it is
simple to make the controller latency parameterized. This parameter
defaults to 1 cycle. It is not required to set a default here. The
default is propagated to the generated SimObject description file as the
default to the SimObject parameter.

Next, we have the message buffers for the directory. Importantly, *these
need to have the same virtual network numbers* as the message buffers in
the L1 cache. These virtual network numbers are how the Ruby network
directs messages between controllers.

There is also two more special message buffers: `requestToMemory` and `responseFromMemory`.
This is similar to the `mandatoryQueue`, except instead of being like a
responder port for CPUs it is like a requestor port. The `responseFromMemory` and `requestToMemory`
buffers will deliver responses sent across the the memory port and send requests across the memory port, as we will see below in the action section.

After the parameters and message buffers, we need to declare all of the
states, events, and other local structures.

```cpp
state_declaration(State, desc="Directory states",
                  default="Directory_State_I") {
    // Stable states.
    // NOTE: These are "cache-centric" states like in Sorin et al.
    // However, The access permissions are memory-centric.
    I, AccessPermission:Read_Write,  desc="Invalid in the caches.";
    S, AccessPermission:Read_Only,   desc="At least one cache has the blk";
    M, AccessPermission:Invalid,     desc="A cache has the block in M";

    // Transient states
    S_D, AccessPermission:Busy,      desc="Moving to S, but need data";

    // Waiting for data from memory
    S_m, AccessPermission:Read_Write, desc="In S waiting for mem";
    M_m, AccessPermission:Read_Write, desc="Moving to M waiting for mem";

    // Waiting for write-ack from memory
    MI_m, AccessPermission:Busy,       desc="Moving to I waiting for ack";
    SS_m, AccessPermission:Busy,       desc="Moving to I waiting for ack";
}

enumeration(Event, desc="Directory events") {
    // Data requests from the cache
    GetS,         desc="Request for read-only data from cache";
    GetM,         desc="Request for read-write data from cache";

    // Writeback requests from the cache
    PutSNotLast,  desc="PutS and the block has other sharers";
    PutSLast,     desc="PutS and the block has no other sharers";
    PutMOwner,    desc="Dirty data writeback from the owner";
    PutMNonOwner, desc="Dirty data writeback from non-owner";

    // Cache responses
    Data,         desc="Response to fwd request with data";

    // From Memory
    MemData,      desc="Data from memory";
    MemAck,       desc="Ack from memory that write is complete";
}

structure(Entry, desc="...", interface="AbstractCacheEntry", main="false") {
    State DirState,         desc="Directory state";
    NetDest Sharers,        desc="Sharers for this block";
    NetDest Owner,          desc="Owner of this block";
}
```

In the `state_declaration` we define a default. For many things in SLICC
you can specify a default. However, this default must use the C++ name
(mangled SLICC name). For the state below you have to use the controller
name and the name we use for states. In this case, since the name of the
machine is "Directory" the name for "I" is "Directory"+"State" (for the
name of the structure)+"I".

Note that the permissions in the directory are "memory-centric".
Whereas, all of the states are cache centric as in Sorin et al.

In the `Entry` definition for the directory, we use a NetDest for both
the sharers and the owner. This makes sense for the sharers, since we
want a full bitvector for all L1 caches that may be sharing the block.
The reason we also use a `NetDest` for the owner is to simply copy the
structure into the message we send as a response as shown below.D
Note that we add one extra parameter to the `Entry` declaration: `main="false"`.
This extra parameter tells the replacement policy that this `Entry` is special and should be ignored.
In the `DirectoryMemory` we are tracking *all* of the backing memory locations, so there is no need for a replacement policy.

In this implementation, we use a few more transient states than in Table
8.2 in Sorin et al. to deal with the fact that the memory latency in
unknown. In Sorin et al., the authors assume that the directory state
and memory data is stored together in main-memory to simplify the
protocol. Similarly, we also include new actions: the responses from
memory.

Next, we have the functions that need to overridden and declared. The
function `getDirectoryEntry` either returns the valid directory entry,
or, if it hasn't been allocated yet, this allocates the entry.
Implementing it this way may save some host memory since this is lazily
populated.

```cpp
Tick clockEdge();

Entry getDirectoryEntry(Addr addr), return_by_pointer = "yes" {
    Entry dir_entry := static_cast(Entry, "pointer", directory[addr]);
    if (is_invalid(dir_entry)) {
        // This first time we see this address allocate an entry for it.
        dir_entry := static_cast(Entry, "pointer",
                                 directory.allocate(addr, new Entry));
    }
    return dir_entry;
}

State getState(Addr addr) {
    if (directory.isPresent(addr)) {
        return getDirectoryEntry(addr).DirState;
    } else {
        return State:I;
    }
}

void setState(Addr addr, State state) {
    if (directory.isPresent(addr)) {
        if (state == State:M) {
            DPRINTF(RubySlicc, "Owner %s\n", getDirectoryEntry(addr).Owner);
            assert(getDirectoryEntry(addr).Owner.count() == 1);
            assert(getDirectoryEntry(addr).Sharers.count() == 0);
        }
        getDirectoryEntry(addr).DirState := state;
        if (state == State:I)  {
            assert(getDirectoryEntry(addr).Owner.count() == 0);
            assert(getDirectoryEntry(addr).Sharers.count() == 0);
        }
    }
}

AccessPermission getAccessPermission(Addr addr) {
    if (directory.isPresent(addr)) {
        Entry e := getDirectoryEntry(addr);
        return Directory_State_to_permission(e.DirState);
    } else  {
        return AccessPermission:NotPresent;
    }
}
void setAccessPermission(Addr addr, State state) {
    if (directory.isPresent(addr)) {
        Entry e := getDirectoryEntry(addr);
        e.changePermission(Directory_State_to_permission(state));
    }
}

void functionalRead(Addr addr, Packet *pkt) {
    functionalMemoryRead(pkt);
}

int functionalWrite(Addr addr, Packet *pkt) {
    if (functionalMemoryWrite(pkt)) {
        return 1;
    } else {
        return 0;
    }
```

Next, we need to implement the ports for the cache. First we specify the
`out_port` and then the `in_port` code blocks. The only difference
between the `in_port` in the directory and in the L1 cache is that the
directory does not have a TBE or cache entry. Thus, we do not pass
either into the `trigger` function.

```cpp
out_port(forward_out, RequestMsg, forwardToCache);
out_port(response_out, ResponseMsg, responseToCache);

in_port(memQueue_in, MemoryMsg, responseFromMemory) {
    if (memQueue_in.isReady(clockEdge())) {
        peek(memQueue_in, MemoryMsg) {
            if (in_msg.Type == MemoryRequestType:MEMORY_READ) {
                trigger(Event:MemData, in_msg.addr);
            } else if (in_msg.Type == MemoryRequestType:MEMORY_WB) {
                trigger(Event:MemAck, in_msg.addr);
            } else {
                error("Invalid message");
            }
        }
    }
}

in_port(response_in, ResponseMsg, responseFromCache) {
    if (response_in.isReady(clockEdge())) {
        peek(response_in, ResponseMsg) {
            if (in_msg.Type == CoherenceResponseType:Data) {
                trigger(Event:Data, in_msg.addr);
            } else {
                error("Unexpected message type.");
            }
        }
    }
}

in_port(request_in, RequestMsg, requestFromCache) {
    if (request_in.isReady(clockEdge())) {
        peek(request_in, RequestMsg) {
            Entry e := getDirectoryEntry(in_msg.addr);
            if (in_msg.Type == CoherenceRequestType:GetS) {

                trigger(Event:GetS, in_msg.addr);
            } else if (in_msg.Type == CoherenceRequestType:GetM) {
                trigger(Event:GetM, in_msg.addr);
            } else if (in_msg.Type == CoherenceRequestType:PutS) {
                assert(is_valid(e));
                // If there is only a single sharer (i.e., the requestor)
                if (e.Sharers.count() == 1) {
                    assert(e.Sharers.isElement(in_msg.Requestor));
                    trigger(Event:PutSLast, in_msg.addr);
                } else {
                    trigger(Event:PutSNotLast, in_msg.addr);
                }
            } else if (in_msg.Type == CoherenceRequestType:PutM) {
                assert(is_valid(e));
                if (e.Owner.isElement(in_msg.Requestor)) {
                    trigger(Event:PutMOwner, in_msg.addr);
                } else {
                    trigger(Event:PutMNonOwner, in_msg.addr);
                }
            } else {
                error("Unexpected message type.");
            }
        }
    }
}
```

The next part of the state machine file is the actions.
First, we define actions for sending memory reads and writes.
For this, we will use the special `memQueue_out` port that we defined above.
If we `enqueue` messages on this port, they will be translated into "normal" gem5 `PacketPtr`s and sent across the memory port defined in the configuration.
We will see how to connect this port in the
configuration section \<MSI-config-section\>. Note that we need two
different actions to send data to memory for both requests and responses
since there are two different message buffers (virtual networks) that
data might arrive on.

```cpp
action(sendMemRead, "r", desc="Send a memory read request") {
    peek(request_in, RequestMsg) {
        enqueue(memQueue_out, MemoryMsg, toMemLatency) {
            out_msg.addr := address;
            out_msg.Type := MemoryRequestType:MEMORY_READ;
            out_msg.Sender := in_msg.Requestor;
            out_msg.MessageSize := MessageSizeType:Request_Control;
            out_msg.Len := 0;
        }
    }
}

action(sendDataToMem, "w", desc="Write data to memory") {
    peek(request_in, RequestMsg) {
        DPRINTF(RubySlicc, "Writing memory for %#x\n", address);
        DPRINTF(RubySlicc, "Writing %s\n", in_msg.DataBlk);
        enqueue(memQueue_out, MemoryMsg, toMemLatency) {
            out_msg.addr := address;
            out_msg.Type := MemoryRequestType:MEMORY_WB;
            out_msg.Sender := in_msg.Requestor;
            out_msg.MessageSize := MessageSizeType:Writeback_Data;
            out_msg.DataBlk := in_msg.DataBlk;
            out_msg.Len := 0;
        }
    }
}

action(sendRespDataToMem, "rw", desc="Write data to memory from resp") {
    peek(response_in, ResponseMsg) {
        DPRINTF(RubySlicc, "Writing memory for %#x\n", address);
        DPRINTF(RubySlicc, "Writing %s\n", in_msg.DataBlk);
        enqueue(memQueue_out, MemoryMsg, toMemLatency) {
            out_msg.addr := address;
            out_msg.Type := MemoryRequestType:MEMORY_WB;
            out_msg.Sender := in_msg.Sender;
            out_msg.MessageSize := MessageSizeType:Writeback_Data;
            out_msg.DataBlk := in_msg.DataBlk;
            out_msg.Len := 0;
        }
}
```

In this code, we also see the last way to add debug information to SLICC
protocols: `DPRINTF`. This is exactly the same as a `DPRINTF` in gem5,
except in SLICC only the `RubySlicc` debug flag is available.

Next, we specify actions to update the sharers and owner of a particular
block.

```cpp
action(addReqToSharers, "aS", desc="Add requestor to sharer list") {
    peek(request_in, RequestMsg) {
        getDirectoryEntry(address).Sharers.add(in_msg.Requestor);
    }
}

action(setOwner, "sO", desc="Set the owner") {
    peek(request_in, RequestMsg) {
        getDirectoryEntry(address).Owner.add(in_msg.Requestor);
    }
}

action(addOwnerToSharers, "oS", desc="Add the owner to sharers") {
    Entry e := getDirectoryEntry(address);
    assert(e.Owner.count() == 1);
    e.Sharers.addNetDest(e.Owner);
}

action(removeReqFromSharers, "rS", desc="Remove requestor from sharers") {
    peek(request_in, RequestMsg) {
        getDirectoryEntry(address).Sharers.remove(in_msg.Requestor);
    }
}

action(clearSharers, "cS", desc="Clear the sharer list") {
    getDirectoryEntry(address).Sharers.clear();
}

action(clearOwner, "cO", desc="Clear the owner") {
    getDirectoryEntry(address).Owner.clear();
}
```

The next set of actions send invalidates and forward requests to caches
that the directory cannot deal with alone.

```cpp
action(sendInvToSharers, "i", desc="Send invalidate to all sharers") {
    peek(request_in, RequestMsg) {
        enqueue(forward_out, RequestMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceRequestType:Inv;
            out_msg.Requestor := in_msg.Requestor;
            out_msg.Destination := getDirectoryEntry(address).Sharers;
            out_msg.MessageSize := MessageSizeType:Control;
        }
    }
}

action(sendFwdGetS, "fS", desc="Send forward getS to owner") {
    assert(getDirectoryEntry(address).Owner.count() == 1);
    peek(request_in, RequestMsg) {
        enqueue(forward_out, RequestMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceRequestType:GetS;
            out_msg.Requestor := in_msg.Requestor;
            out_msg.Destination := getDirectoryEntry(address).Owner;
            out_msg.MessageSize := MessageSizeType:Control;
        }
    }
}

action(sendFwdGetM, "fM", desc="Send forward getM to owner") {
    assert(getDirectoryEntry(address).Owner.count() == 1);
    peek(request_in, RequestMsg) {
        enqueue(forward_out, RequestMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceRequestType:GetM;
            out_msg.Requestor := in_msg.Requestor;
            out_msg.Destination := getDirectoryEntry(address).Owner;
            out_msg.MessageSize := MessageSizeType:Control;
        }
    }
}
```

Now we have responses from the directory. Here we are peeking into the
special buffer `responseFromMemory`. You can find the definition of
`MemoryMsg` in `src/mem/protocol/RubySlicc_MemControl.sm`.

```cpp
action(sendDataToReq, "d", desc="Send data from memory to requestor. May need to send sharer number, too") {
    peek(memQueue_in, MemoryMsg) {
        enqueue(response_out, ResponseMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceResponseType:Data;
            out_msg.Sender := machineID;
            out_msg.Destination.add(in_msg.OriginalRequestorMachId);
            out_msg.DataBlk := in_msg.DataBlk;
            out_msg.MessageSize := MessageSizeType:Data;
            Entry e := getDirectoryEntry(address);
            // Only need to include acks if we are the owner.
            if (e.Owner.isElement(in_msg.OriginalRequestorMachId)) {
                out_msg.Acks := e.Sharers.count();
            } else {
                out_msg.Acks := 0;
            }
            assert(out_msg.Acks >= 0);
        }
    }
}

action(sendPutAck, "a", desc="Send the put ack") {
    peek(request_in, RequestMsg) {
        enqueue(forward_out, RequestMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceRequestType:PutAck;
            out_msg.Requestor := machineID;
            out_msg.Destination.add(in_msg.Requestor);
            out_msg.MessageSize := MessageSizeType:Control;
        }
    }
}
```

Then, we have the queue management and stall actions.

```cpp
action(popResponseQueue, "pR", desc="Pop the response queue") {
    response_in.dequeue(clockEdge());
}

action(popRequestQueue, "pQ", desc="Pop the request queue") {
    request_in.dequeue(clockEdge());
}

action(popMemQueue, "pM", desc="Pop the memory queue") {
    memQueue_in.dequeue(clockEdge());
}

action(stall, "z", desc="Stall the incoming request") {
    // Do nothing.
}
```

Finally, we have the transition section of the state machine file. These
mostly come from Table 8.2 in Sorin et al., but there are some extra
transitions to deal with the unknown memory latency.

```cpp
transition({I, S}, GetS, S_m) {
    sendMemRead;
    addReqToSharers;
    popRequestQueue;
}

transition(I, {PutSNotLast, PutSLast, PutMNonOwner}) {
    sendPutAck;
    popRequestQueue;
}

transition(S_m, MemData, S) {
    sendDataToReq;
    popMemQueue;
}

transition(I, GetM, M_m) {
    sendMemRead;
    setOwner;
    popRequestQueue;
}

transition(M_m, MemData, M) {
    sendDataToReq;
    clearSharers; // NOTE: This isn't *required* in some cases.
    popMemQueue;
}

transition(S, GetM, M_m) {
    sendMemRead;
    removeReqFromSharers;
    sendInvToSharers;
    setOwner;
    popRequestQueue;
}

transition({S, S_D, SS_m, S_m}, {PutSNotLast, PutMNonOwner}) {
    removeReqFromSharers;
    sendPutAck;
    popRequestQueue;
}

transition(S, PutSLast, I) {
    removeReqFromSharers;
    sendPutAck;
    popRequestQueue;
}

transition(M, GetS, S_D) {
    sendFwdGetS;
    addReqToSharers;
    addOwnerToSharers;
    clearOwner;
    popRequestQueue;
}

transition(M, GetM) {
    sendFwdGetM;
    clearOwner;
    setOwner;
    popRequestQueue;
}

transition({M, M_m, MI_m}, {PutSNotLast, PutSLast, PutMNonOwner}) {
    sendPutAck;
    popRequestQueue;
}

transition(M, PutMOwner, MI_m) {
    sendDataToMem;
    clearOwner;
    sendPutAck;
    popRequestQueue;
}

transition(MI_m, MemAck, I) {
    popMemQueue;
}

transition(S_D, {GetS, GetM}) {
    stall;
}

transition(S_D, PutSLast) {
    removeReqFromSharers;
    sendPutAck;
    popRequestQueue;
}

transition(S_D, Data, SS_m) {
    sendRespDataToMem;
    popResponseQueue;
}

transition(SS_m, MemAck, S) {
    popMemQueue;
}

// If we get another request for a block that's waiting on memory,
// stall that request.
transition({MI_m, SS_m, S_m, M_m}, {GetS, GetM}) {
    stall;
}
```

You can download the complete `MSI-dir.sm` file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-dir.sm).


---


## Compiling a SLICC protocol

*Source: https://www.gem5.org/documentation/learning_gem5/part3/MSIbuilding/*

## Building the MSI protocol

### The SLICC file

Now that we have finished implementing the protocol, we need to compile
it. You can download the complete SLICC files below:

- [MSI-cache.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-cache.sm)
- [MSI-dir.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-dir.sm)
- [MSI-msg.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-msg.sm)

Before building the protocol, we need to create one more file:
`MSI.slicc`. This file tells the SLICC compiler which state machine
files to compile for this protocol. The first line contains the name of
our protocol. Then, the file has a number of `include` statements. Each
`include` statement has a file name. This filename can come from any of
the env variable `PROTOCOL_DIRS` directories. We declared the current
directory as part of the `PROTOCOL_DIRS` in the SConsopts file
(`main.Append(PROTOCOL_DIRS=[Dir('.')])`). The other directory is
`src/mem/protocol/`. These files are included like C++ header files.
Effectively, all of the files are processed as one large SLICC file.
Thus, any files that declare types that are used in other files must
come before the files they are used in (e.g., `MSI-msg.sm` must come
before `MSI-cache.sm` since `MSI-cache.sm` uses the `RequestMsg` type).

```cpp
protocol "MSI";
include "RubySlicc_interfaces.slicc";
include "MSI-msg.sm";
include "MSI-cache.sm";
include "MSI-dir.sm";
```

You can download the fill file
[here](https://github.com/gem5/gem5/blob/stable/src/learning_gem5/part3/MSI.slicc).

### Add new config options RUBY_PROTOCOL_MSI (gem5 >= 23.1)

Note: If users use the gem5 version newer than 23.0, they need to do some additional
steps to set up the Kconfig file. Otherwise, users can skip the steps to
`Compiling a protocol with SCons` section.

Then You need to added the MSI protocol in the `learning_gem5/part3/Kconfig`
file to let scons enable build gem5 with MSI protocol.

```
# Set the PROTOCOL="MSI" if the RUBY_PROTOCOL_MSI=y
config PROTOCOL
    default "MSI" if RUBY_PROTOCOL_MSI

# Add the new choice RUBY_PROTOCOL_MSI
cont_choice "Ruby protocol"
    config RUBY_PROTOCOL_MSI
        bool "MSI"
endchoice
```

In the `src/Kconfig`

```
rsource "base/Kconfig"
rsource "mem/ruby/Kconfig"
rsource "learning_gem5/part3/Kconfig"
```

Please add the `learning_gem5/part3/Kconfig` below the `mem/ruby/Kconfig`.

### Compiling a protocol with SCons

#### In the older gem5 versions (gem5 <= 23.0)

Most SCons defaults (found in `build_opts/`) specify the protocol as
`MI_example`, an example, but poor performing protocol. Therefore, we
cannot simply use a default build name (e.g., `X86` or `ARM`). We have
to specify the SCons options on the command line. The command line below
will build our new protocol with the X86 ISA.

```sh
scons build/X86_MSI/gem5.opt --default=X86 PROTOCOL=MSI SLICC_HTML=True
```

This command will build `gem5.opt` in the directory `build/X86_MSI`. You
can specify *any* directory here. This command line has two new
parameters: `--default` and `PROTOCOL`. First, `--default` specifies
which file to use in `build_opts` for defaults for all of the SCons
variables (e.g., `ISA`, `CPU_MODELS`). Next, `PROTOCOL` *overrides* any
default for the `PROTOCOL` SCons variable in the default specified.
Thus, we are telling SCons to specifically compile our new protocol, not
whichever protocol was specified in `build_opts/X86`.

There is one more variable on this command line to build gem5:
`SLICC_HTML=True`. When you specify this on the building command line,
SLICC will generate the HTML tables for your protocol. You can find the
HTML tables in `<build directory>/mem/protocol/html`. By default, the
SLICC compiler skips building the HTML tables because it impacts the
performance of compiling gem5, especially when compiling on a network
file system.

After gem5 finishes compiling, you will have a gem5 binary with your new
protocol! If you want to build another protocol into gem5, you have to
change the `PROTOCOL` SCons variable. Thus, it is a good idea to use a
different build directory for each protocol, especially if you will be
comparing protocols.

When building your protocol, you will likely encounter errors in your
SLICC code reported by the SLICC compiler. Most errors include the file
and line number of the error. Sometimes, this line number is the line
*after* the error occurs. In fact, the line number can be far below the
actual error. For instance, if the curly brackets do not match
correctly, the error will report the last line in the file as the
location.

#### In the newer gem5 version (gem5 >= 23.1)

Most Kconfig defaults (found in `build_opts/`) specify the protocol as
`MI_example`, an example, but poor performing protocol. Therefore, we
cannot simply use a default build name (e.g., `X86` or `ARM`). We have
to specify the Kconfig options through `menuconfig`, `setconfig`, etc.
The command lines below will build our new protocol with the X86 ISA.

```sh
scons defconfig build/X86_MSI build_opts/X86
scons setconfig build/X86_MSI RUBY_PROTOCOL_MSI=y SLICC_HTML=y
scons build/X86_MSI/gem5.opt
```

This command will build `gem5.opt` in the directory `build/X86_MSI`. You
can specify *any* directory here. The first command tells SCons to create a
new build directory, and use the defaults in `build_opts/X86` to configure it.
The second command uses the `setconfig` kconfig tool use `RUBY_PROTOCOL_MSI=y`
to update the `PROTOCOL` and `SLICC_HTML` options in the `build/X86_MSI`
directory's configuration. You can also use other tools like `menuconfig` to
update these settings interactively. Finally, the last command tells SCons to
build in our build directory using this new configuration.

There is one more kconfig setting we're changing: `SLICC_HTML=y`. When
you specify this, SLICC will generate the HTML tables for your protocol.
You can find the HTML tables in `<build directory>/mem/protocol/html`. By
default, the SLICC compiler skips building the HTML tables because it impacts
the performance of compiling gem5, especially when compiling on a network
file system.

After gem5 finishes compiling, you will have a gem5 binary with your new
protocol! If you want to build another protocol into gem5, you have to
set the `RUBY_PROTOCOL_{NAME}=y` in setconfig step to change the `PROTOCOL`
kconfig variable. Thus, it is a good idea to use a different build directory
for each protocol, especially if you will be comparing protocols.

When building your protocol, you will likely encounter errors in your
SLICC code reported by the SLICC compiler. Most errors include the file
and line number of the error. Sometimes, this line number is the line
*after* the error occurs. In fact, the line number can be far below the
actual error. For instance, if the curly brackets do not match
correctly, the error will report the last line in the file as the
location.

For gem5 kconfig document, see
[here](https://www.gem5.org/documentation/general_docs/kconfig_build_system/)


---


## Configuring a simple Ruby system

*Source: https://www.gem5.org/documentation/learning_gem5/part3/configuration/*

## A configuration script for the MSI protocol

First, create a new configuration directory in `configs/`. Just like all
gem5 configuration files, we will have a configuration run script. For
the run script, we can start with `simple.py` from
simple-config-chapter. Copy this file to `simple_ruby.py` in your new
directory.

We will make a couple of small changes to this file to use Ruby instead
of directly connecting the CPU to the memory controllers.

First, so we can test our *coherence* protocol, let's use two CPUs.

```python
system.cpu = [X86TimingSimpleCPU(), X86TimingSimpleCPU()]
```

Next, after the memory controllers have been instantiated, we are going
to create the cache system and set up all of the caches. Add the
following lines *after the CPU interrupts have been created, but before
instantiating the system*.

```python
system.caches = MyCacheSystem()
system.caches.setup(system, system.cpu, [system.mem_ctrl])
```

Like the classic cache example in cache-config-chapter, we are going to
create a second file that contains the cache configuration code. In this
file we are going to have a class called `MyCacheSystem` and we will
create a `setup` function that takes as parameters the CPUs in the
system and the memory controllers.

You can download the complete run script
[here](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part3/simple_ruby.py).

### Cache system configuration

Now, let's create a file `msi_caches.py`. In this file, we will create
four classes: `MyCacheSystem` which will inherit from `RubySystem`,
`L1Cache` and `Directory` which will inherit from the SimObjects created
by SLICC from our two state machines, and `MyNetwork` which will inherit
from `SimpleNetwork`.

#### L1 Cache

Let's start with the `L1Cache`. First, we will inherit from
`L1Cache_Controller` since we named our L1 cache "L1Cache" in the state
machine file. We also include a special class variable and class method
for tracking the "version number". For each SLICC state machine, you
have to number them in ascending order from 0. Each machine of the same
type should have a unique version number. This is used to differentiate
the individual machines. (Hopefully, in the future this requirement will
be removed.)

```python
class L1Cache(L1Cache_Controller):

    _version = 0
    @classmethod
    def versionCount(cls):
        cls._version += 1 # Use count for this particular type
        return cls._version - 1
```

Next, we implement the constructor for the class.

```python
def __init__(self, system, ruby_system, cpu):
    super(L1Cache, self).__init__()

    self.version = self.versionCount()
    self.cacheMemory = RubyCache(size = '16kB',
                           assoc = 8,
                           start_index_bit = self.getBlockSizeBits(system))
    self.clk_domain = cpu.clk_domain
    self.send_evictions = self.sendEvicts(cpu)
    self.ruby_system = ruby_system
    self.connectQueues(ruby_system)
```

We need the CPUs in this function to grab the clock domain and system is
needed for the cache block size. Here, we set all of the parameters that
we named in the state machine file (e.g., `cacheMemory`). We will set
`sequencer` later. We also hardcode the size an associativity of the
cache. You could add command line parameters for these options, if it is
important to vary them at runtime.

Next, we implement a couple of helper functions. First, we need to
figure out how many bits of the address to use for indexing into the
cache, which is a simple log operation. We also need to decide whether
to send eviction notices to the CPU. Only if we are using the
out-of-order CPU and using x86 or ARM ISA should we forward evictions.

```python
def getBlockSizeBits(self, system):
    bits = int(math.log(system.cache_line_size, 2))
    if 2**bits != system.cache_line_size.value:
        panic("Cache line size not a power of 2!")
    return bits

def sendEvicts(self, cpu):
    """True if the CPU model or ISA requires sending evictions from caches
       to the CPU. Three scenarios warrant forwarding evictions to the CPU:
       1. The O3 model must keep the LSQ coherent with the caches
       2. The x86 mwait instruction is built on top of coherence
       3. The local exclusive monitor in ARM systems
    """
    return True
```

Finally, we need to implement `connectQueues` to connect all of the
message buffers to the Ruby network. First, we create a message buffer
for the mandatory queue. Since this is an L1 cache and it will have a
sequencer, we need to instantiate this special message buffer. Next, we
instantiate a message buffer for each buffer in the controller. All of
the "to" buffers we must set the "master" to the network (i.e., the
buffer will send messages into the network), and all of the "from"
buffers we must set the "slave" to the network. These *names* are the
same as the gem5 ports, but *message buffers are not currently
implemented as gem5 ports*. In this protocol, we are assuming the
message buffers are ordered for simplicity.

```python
def connectQueues(self, ruby_system):
    self.mandatoryQueue = MessageBuffer()

    self.requestToDir = MessageBuffer(ordered = True)
    self.requestToDir.master = ruby_system.network.slave
    self.responseToDirOrSibling = MessageBuffer(ordered = True)
    self.responseToDirOrSibling.master = ruby_system.network.slave
    self.forwardFromDir = MessageBuffer(ordered = True)
    self.forwardFromDir.slave = ruby_system.network.master
    self.responseFromDirOrSibling = MessageBuffer(ordered = True)
    self.responseFromDirOrSibling.slave = ruby_system.network.master
```

#### Directory

Now, we can similarly implement the directory. There are three
differences from the L1 cache. First, we need to set the address ranges
for the directory. Since each directory corresponds to a particular
memory controller for a subset of the address range (possibly), we need
to make sure the ranges match. The default address ranges for Ruby
controllers is `AllMemory`.

Next, we need to set the master port `memory`. This is the port that
sends messages when `queueMemoryRead/Write` is called in the SLICC code.
We set it the to the memory controller port. Similarly, in
`connectQueues` we need to instantiate the special message buffer
`responseFromMemory` like the `mandatoryQueue` in the L1 cache.

```python
class DirController(Directory_Controller):

    _version = 0
    @classmethod
    def versionCount(cls):
        cls._version += 1 # Use count for this particular type
        return cls._version - 1

    def __init__(self, ruby_system, ranges, mem_ctrls):
        """ranges are the memory ranges assigned to this controller.
        """
        if len(mem_ctrls) > 1:
            panic("This cache system can only be connected to one mem ctrl")
        super(DirController, self).__init__()
        self.version = self.versionCount()
        self.addr_ranges = ranges
        self.ruby_system = ruby_system
        self.directory = RubyDirectoryMemory()
        # Connect this directory to the memory side.
        self.memory = mem_ctrls[0].port
        self.connectQueues(ruby_system)

    def connectQueues(self, ruby_system):
        self.requestFromCache = MessageBuffer(ordered = True)
        self.requestFromCache.slave = ruby_system.network.master
        self.responseFromCache = MessageBuffer(ordered = True)
        self.responseFromCache.slave = ruby_system.network.master

        self.responseToCache = MessageBuffer(ordered = True)
        self.responseToCache.master = ruby_system.network.slave
        self.forwardToCache = MessageBuffer(ordered = True)
        self.forwardToCache.master = ruby_system.network.slave

        self.responseFromMemory = MessageBuffer()
```

#### Ruby System

Now, we can implement the Ruby system object. For this object, the
constructor is simple. It just checks the SCons variable `PROTOCOL` to
be sure that we are using the right configuration file for the protocol
that was compiled. We cannot create the controllers in the constructor
because they require a pointer to the this object. If we were to create
them in the constructor, there would be a circular dependence in the
SimObject hierarchy which will cause infinite recursion in when the
system in instantiated with `m5.instantiate`.

```python
class MyCacheSystem(RubySystem):

    def __init__(self):
        if buildEnv['PROTOCOL'] != 'MSI':
            fatal("This system assumes MSI from learning gem5!")

        super(MyCacheSystem, self).__init__()
```

Instead of create the controllers in the constructor, we create a new
function to create all of the needed objects: `setup`. First, we create
the network. We will look at this object next. With the network, we need
to set the number of virtual networks in the system.

Next, we instantiate all of the controllers. Here, we use a single
global list of the controllers to make it easier to connect them to the
network later. However, for more complicated cache topologies, it can
make sense to use multiple lists of controllers. We create one L1 cache
for each CPU and one directory for the system.

Then, we instantiate all of the sequencers, one for each CPU. Each
sequencer needs a pointer to the instruction and data cache to simulate
the correct latency when initially accessing the cache. In more
complicated systems, you also have to create sequencers for other
objects like DMA controllers.

After creating the sequencers, we set the sequencer variable on each L1
cache controller.

Then, we connect all of the controllers to the network and call the
`setup_buffers` function on the network.

We then have to set the "port proxy" for both the Ruby system and the
`system` for making functional accesses (e.g., loading the binary in SE
mode).

Finally, we connect all of the CPUs to the ruby system. In this example,
we assume that there are only CPU sequencers so the first CPU is
connected to the first sequencer, and so on. We also have to connect the
TLBs and interrupt ports (if we are using x86).

```python
def setup(self, system, cpus, mem_ctrls):
    self.network = MyNetwork(self)

    self.number_of_virtual_networks = 3
    self.network.number_of_virtual_networks = 3

    self.controllers = \
        [L1Cache(system, self, cpu) for cpu in cpus] + \
        [DirController(self, system.mem_ranges, mem_ctrls)]

    self.sequencers = [RubySequencer(version = i,
                            # I/D cache is combined and grab from ctrl
                            icache = self.controllers[i].cacheMemory,
                            dcache = self.controllers[i].cacheMemory,
                            clk_domain = self.controllers[i].clk_domain,
                            ) for i in range(len(cpus))]

    for i,c in enumerate(self.controllers[0:len(self.sequencers)]):
        c.sequencer = self.sequencers[i]

    self.num_of_sequencers = len(self.sequencers)

    self.network.connectControllers(self.controllers)
    self.network.setup_buffers()

    self.sys_port_proxy = RubyPortProxy()
    system.system_port = self.sys_port_proxy.slave

    for i,cpu in enumerate(cpus):
        cpu.icache_port = self.sequencers[i].slave
        cpu.dcache_port = self.sequencers[i].slave
        isa = buildEnv['TARGET_ISA']
        if isa == 'x86':
            cpu.interrupts[0].pio = self.sequencers[i].master
            cpu.interrupts[0].int_master = self.sequencers[i].slave
            cpu.interrupts[0].int_slave = self.sequencers[i].master
        if isa == 'x86' or isa == 'arm':
            cpu.itb.walker.port = self.sequencers[i].slave
            cpu.dtb.walker.port = self.sequencers[i].slave
```

#### Network

Finally, the last object we have to implement is the network. The
constructor is simple, but we need to declare an empty list for the list
of network interfaces (`netifs`).

Most of the code is in `connectControllers`. This function implements a
*very simple, unrealistic* point-to-point network. In other words, every
controller has a direct link to every other controller.

The Ruby network is made of three parts: routers that route data from
one router to another or to external controllers, external links that
link a controller to a router, and internal links that link two routers
together. First, we create a router for each controller. Then, we create
an external link from that router to the controller. Finally, we add all
of the "internal" links. Each router is connected to all other routers
to make the point-to-point network.

```python
class MyNetwork(SimpleNetwork):

    def __init__(self, ruby_system):
        super(MyNetwork, self).__init__()
        self.netifs = []
        self.ruby_system = ruby_system

    def connectControllers(self, controllers):
        self.routers = [Switch(router_id = i) for i in range(len(controllers))]

        self.ext_links = [SimpleExtLink(link_id=i, ext_node=c,
                                        int_node=self.routers[i])
                          for i, c in enumerate(controllers)]

        link_count = 0
        self.int_links = []
        for ri in self.routers:
            for rj in self.routers:
                if ri == rj: continue # Don't connect a router to itself!
                link_count += 1
                self.int_links.append(SimpleIntLink(link_id = link_count,
                                                    src_node = ri,
                                                    dst_node = rj))
```

You can download the complete `msi_caches.py` file
[here](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part3/msi_caches.py).


---


## Running the simple Ruby system

*Source: https://www.gem5.org/documentation/learning_gem5/part3/running/*

## Running the simple Ruby system

Now, we can run our system with the MSI protocol!

As something interesting, below is a simple multithreaded program (note:
as of this writing there is a bug in gem5 preventing this code from
executing).

```cpp
#include <iostream>
#include <thread>

using namespace std;

/*
 * c = a + b
 */
void array_add(int *a, int *b, int *c, int tid, int threads, int num_values)
{
    for (int i = tid; i < num_values; i += threads) {
        c[i] = a[i] + b[i];
    }
}


int main(int argc, char *argv[])
{
    unsigned num_values;
    if (argc == 1) {
        num_values = 100;
    } else if (argc == 2) {
        num_values = atoi(argv[1]);
        if (num_values <= 0) {
            cerr << "Usage: " << argv[0] << " [num_values]" << endl;
            return 1;
        }
    } else {
        cerr << "Usage: " << argv[0] << " [num_values]" << endl;
        return 1;
    }

    unsigned cpus = thread::hardware_concurrency();

    cout << "Running on " << cpus << " cores. ";
    cout << "with " << num_values << " values" << endl;

    int *a, *b, *c;
    a = new int[num_values];
    b = new int[num_values];
    c = new int[num_values];

    if (!(a && b && c)) {
        cerr << "Allocation error!" << endl;
        return 2;
    }

    for (int i = 0; i < num_values; i++) {
        a[i] = i;
        b[i] = num_values - i;
        c[i] = 0;
    }

    thread **threads = new thread*[cpus];

    // NOTE: -1 is required for this to work in SE mode.
    for (int i = 0; i < cpus - 1; i++) {
        threads[i] = new thread(array_add, a, b, c, i, cpus, num_values);
    }
    // Execute the last thread with this thread context to appease SE mode
    array_add(a, b, c, cpus - 1, cpus, num_values);

    cout << "Waiting for other threads to complete" << endl;

    for (int i = 0; i < cpus - 1; i++) {
        threads[i]->join();
    }

    delete[] threads;

    cout << "Validating..." << flush;

    int num_valid = 0;
    for (int i = 0; i < num_values; i++) {
        if (c[i] == num_values) {
            num_valid++;
        } else {
            cerr << "c[" << i << "] is wrong.";
            cerr << " Expected " << num_values;
            cerr << " Got " << c[i] << "." << endl;
        }
    }

    if (num_valid == num_values) {
        cout << "Success!" << endl;
        return 0;
    } else {
        return 2;
    }
}
```

With the above code compiled as `threads`, we can run gem5!

```sh
build/MSI/gem5.opt configs/learning_gem5/part6/simple_ruby.py
```

The output should be something like the following. Most of the warnings
are unimplemented syscalls in SE mode due to using pthreads and can be
safely ignored for this simple example.

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Sep  7 2017 12:39:51
    gem5 started Sep 10 2017 20:56:35
    gem5 executing on fuggle, pid 6687
    command line: build/MSI/gem5.opt configs/learning_gem5/part6/simple_ruby.py

    Global frequency set at 1000000000000 ticks per second
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    0: system.remote_gdb.listener: listening for remote gdb #1 on port 7001
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    warn: Replacement policy updates recently became the responsibility of SLICC state machines. Make sure to setMRU() near callbacks in .sm files!
    warn: ignoring syscall access(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall access(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall mprotect(...)
    warn: ignoring syscall set_robust_list(...)
    warn: ignoring syscall rt_sigaction(...)
          (further warnings will be suppressed)
    warn: ignoring syscall rt_sigprocmask(...)
          (further warnings will be suppressed)
    info: Increasing stack size by one page.
    info: Increasing stack size by one page.
    Running on 2 cores. with 100 values
    warn: ignoring syscall mprotect(...)
    warn: ClockedObject: Already in the requested power state, request ignored
    warn: ignoring syscall set_robust_list(...)
    Waiting for other threads to complete
    warn: ignoring syscall madvise(...)
    Validating...Success!
    Exiting @ tick 9386342000 because exiting with last active thread context
```


---


## Debugging SLICC Protocols

*Source: https://www.gem5.org/documentation/learning_gem5/part3/MSIdebugging/*

In this section, I present the steps that I took while debugging the MSI
protocol implemented earlier in this chapter. Learning to debug
coherence protocols is a challenge. The best way is by working with
others who have written SLICC protocols in the past. However, since you,
the reader, cannot look over my shoulder while I am debugging a
protocol, I am trying to present the next-best thing.

Here, I first present some high-level suggestions to tackling protocol
errors. Next, I discuss some details about deadlocks, and how to
understand protocol traces that can be used to fix them. Then, I present
my experience debugging the MSI protocol in this chapter in a
stream-of-consciousness style. I will show the error that was generated,
then the solution to the error, sometimes with some commentary of the
different tactics I tried to solve the error.

## General debugging tips

Ruby has many useful debug flags. However, the most useful, by far, is
`ProtocolTrace`. Below, you will see several examples of using the
protocol trace to debug a protocol. The protocol trace prints every
transition for all controllers. Thus, you can simply trace the entire
execution of the cache system.

Other useful debug flags include:

RubyGenerated
:   Prints a bunch of stuff from the ruby generated code.

RubyPort/RubySequencer
:   See the details of sending/receiving messages into/out of ruby.

RubyNetwork
:   Prints entire network messages including the sender/receiver and the
    data within the message for all messages. This flag is useful when
    there is a data mismatch.

The first step to debugging a Ruby protocol is to run it with the Ruby
random tester. The random tester issues semi-random requests into the
Ruby system and checks to make sure the returned data is correct. To
make debugging faster, the random tester issues read requests from one
controller for a block and a write request for the same cache block (but
a different byte) from a different controller. Thus, the Ruby random
tester does a good job exercising the transient states and race
conditions in the protocol.

Unfortunately, the random tester's configuration is slightly different
than when using normal CPUs. Thus, we need to use a different
`MyCacheSystem` than before. You can download this different cache
system file
[here](/_pages/static/scripts/part3/configs/test_caches.py) and you
can download the modified run script
[here](/_pages/static/scripts/part3/configs/ruby_test.py). The test
run script is mostly the same as the simple run script, but creates the
`RubyRandomTester` instead of CPUs.

It is often a good idea to first run the random tester with a single
"CPU". Then, increase the number of loads from the default of 100 to
something that takes a few minutes to execute on your host system. Next,
if there are no errors, then increase the number of "CPUs" to two and
reduce the number of loads to 100 again. Then, start increasing the
number of loads. Finally, you can increase the number of CPUs to
something reasonable for the system you are trying to simulate. If you
can run the random tester for 10-15 minutes, you can be slightly
confident that the random tester isn't going to find any other bugs.

Once you have your protocol working with the random tester, you can move
on to using real applications. It is likely that real applications will
expose even more bugs in the protocol. If at all possible, it is much
easier to debug your protocol with the random tester than with real
applications!

## Understanding Protocol Traces

Unfortunately, despite extensive effort to catch bugs in them, coherence
protocols (even heavily tested ones) will have bugs. Sometimes these
bugs are relatively simple fixes, while other times the bugs will be
very insidious and difficult to track down. In the worst case, the bugs
will manifest themselves as deadlocks: bugs that literally prevent the
application from making progress. Another similar problem is livelocks:
where the program runs forever due to a cycle somewhere in the system.
Whenever livelocks or deadlocks occur, the next thing to do is generate
a protocol trace. Traces print a running list of every transition that
is happening in the memory system: memory requests starting and
completing, L1 and directory transitions, etc. You can then use these
traces to identify why the deadlock is occurring. However, as we will
discuss in more detail below, debugging deadlocks in protocol traces is
often extremely challenging.

Here, we discuss what appears in the protocol trace to help explain what
is happening. To start with, lets look at a small snippet of a protocol
trace (we will discuss the details of this trace further below):

```protocoltrace
    ...
    4541   0    L1Cache         Replacement   MI_A>MI_A   [0x4ac0, line 0x4ac0]
    4542   0    L1Cache              PutAck   MI_A>I      [0x4ac0, line 0x4ac0]
    4549   0  Directory              MemAck   MI_M>I      [0x4ac0, line 0x4ac0]
    4641   0        Seq               Begin       >       [0x4aec, line 0x4ac0] LD
    4652   0    L1Cache                Load      I>IS_D   [0x4ac0, line 0x4ac0]
    4657   0  Directory                GetS      I>S_M    [0x4ac0, line 0x4ac0]
    4669   0  Directory             MemData    S_M>S      [0x4ac0, line 0x4ac0]
    4674   0        Seq                Done       >       [0x4aec, line 0x4ac0] 33 cycles
    4674   0    L1Cache       DataDirNoAcks   IS_D>S      [0x4ac0, line 0x4ac0]
    5321   0        Seq               Begin       >       [0x4aec, line 0x4ac0] ST
    5322   0    L1Cache               Store      S>SM_AD  [0x4ac0, line 0x4ac0]
    5327   0  Directory                GetM      S>M_M    [0x4ac0, line 0x4ac0]
```

Every line in this trace has a set pattern in terms of what information
appears on that line. Specifically, the fields are:

1. Current Tick: the tick the print is occurs in
2. Machine Version: The number of the machine where this request is
   coming from. For example, if there are 4 L1 caches, then the numbers
   would be 0-3. Assuming you have 1 L1 Cache per core, you can think
   of this as representing the core the request is coming from.
3. Component: which part of the system is doing the print. Generally,
   `Seq` is shorthand for Sequencer, `L1Cache` represents the L1 Cache,
   "Directory" represents the directory, and so on. For L1 caches and
   the directory, this represents the name of the machine type (i.e.,
   what is after "MachineType:" in the `machine()` definition).
4. Action: what the component is doing. For example, "Begin" means the
   Sequencer has received a new request, "Done" means that the
   Sequencer is completing a previous request, and "DataDirNoAcks"
   means that our DataDirNoAcks event is being triggered.
5. Transition (e.g., MI\_A\>MI\_A): what state transition this action
   is doing (format: "currentState\>nextState"). If no transition is
   happening, this is denoted with "\>".
6. Address (e.g., [0x4ac0, line 0x4ac0]): the physical address of the
   request (format: [wordAddress, lineAddress]). This address will
   always be cache-block aligned except for requests from the
   `Sequencer` and `mandatoryQueue`.
7. (Optional) Comments: optionally, there is one additional field to
   pass comments. For example, the "LD" , "ST", and "33 cycles" lines
   use this extra field to pass additional information to the trace --
   such as identifying the request as a load or store. For SLICC
   transitions, `APPEND_TRANSITION_COMMENT` often use this, as we
   [discussed previously](../cache-actions/).

Generally, spaces are used to separate each of these fields (the space
between the fields are added implicitly, you do not need to add them).
However, sometimes if a field is very long, there may be no spaces or
the line may be shifted compared to other lines.

Using this information, let's analyze the above snippet. The first
(tick) field tells us that this trace snippet is showing what was
happening in the memory system between ticks 4541 and 5327. In this
snippet, all of the requests are coming from L1Cache-0 (core 0) and
going to Directory-0 (the first bank of the directory). During this
time, we see several memory requests and state transitions for the cache
line 0x4ac0, both at the L1 caches and the directory. For example, in
tick 5322, the core executes a store to 0x4ac0. However, it currently
does not have that line in Modified in its cache (it is in Shared after
the core loaded it from ticks 4641-4674), so it needs to request
ownership for that line from the directory (which receives this request
in tick 5327). While waiting for ownership, L1Cache-0 transitions from S
(Shared) to SM\_AD (a transient state -- was in S, going to M, waiting
for Ack and Data).

To add a print to the protocol trace, you will need to add a print with
these fields with the ProtocolTrace flag. For example, if you look at
`src/mem/ruby/system/Sequencer.cc`, you can see where the
`Seq               Begin` and `Seq                Done` trace prints
come from (search for ProtocolTrace).

## Errors I ran into debugging MSI

```termout
    gem5.opt: build/MSI/mem/ruby/system/Sequencer.cc:423: void Sequencer::readCallback(Addr, DataBlock&, bool, MachineType, Cycles, Cycles, Cycles): Assertion `m_readRequestTable.count(makeLineAddress(address))' failed.
```

I'm made a silly mistake. It was that I called readCallback in externalStoreHit
instead of writeCallback. It's good to start simple!

```termout
    gem5.opt: build/MSI/mem/ruby/network/MessageBuffer.cc:220: Tick MessageBuffer::dequeue(Tick, bool): Assertion `isReady(current_time)' failed.
```

I ran gem5 in GDB to get more information. Look at
L1Cache\_Controller::doTransitionWorker. The current transition is:
event=L1Cache\_Event\_PutAck, state=L1Cache\_State\_MI\_A,
<next_state=@0x7fffffffd0a0>: L1Cache\_State\_FIRST This is more simply
MI\_A-\>I on a PutAck See it's in popResponseQueue.

The problem is that the PutAck is on the forward network, not the
response network.

```termout
    panic: Invalid transition
    system.caches.controllers0 time: 3594 addr: 3264 event: DataDirAcks state: IS_D
```

Hmm. I think this shouldn't have happened. The needed acks should always
be 0 or you get data from the owner. Ah. So I implemented sendDataToReq
at the directory to always send the number of sharers. If we get this
response in IS\_D we don't care whether or not there are sharers. Thus,
to make things more simple, I'm just going to transition to S on
DataDirAcks. This is a slight difference from the original
implementation in Sorin et al.

Well, actually, I think it's that we send the request after we add
ourselves to the sharer list. The above is *incorrect*. Sorin et al.
were not wrong! Let's try not doing that!

So, I fixed this by checking to see if the requestor is the *owner*
before sending the data to the requestor at the directory. Only if the
requestor is the owner do we include the number of sharers. Otherwise,
it doesn't matter at all and we just set the sharers to 0.

```termout
    panic: Invalid transition system.caches.controllers0 time: 5332
    addr: 0x4ac0 event: Inv state: SM\_AD
```

First, let's look at where Inv is triggered. If you get an invalidate...
only then. Maybe it's that we are on the sharer list and shouldn't be?

We can use protocol trace and grep to find what's going on.

```sh
build/MSI/gem5.opt --debug-flags=ProtocolTrace configs/learning_gem5/part6/ruby_test.py | grep 0x4ac0
```

```termout
    ...
    4541   0    L1Cache         Replacement   MI_A>MI_A   [0x4ac0, line 0x4ac0]
    4542   0    L1Cache              PutAck   MI_A>I      [0x4ac0, line 0x4ac0]
    4549   0  Directory              MemAck   MI_M>I      [0x4ac0, line 0x4ac0]
    4641   0        Seq               Begin       >       [0x4aec, line 0x4ac0] LD
    4652   0    L1Cache                Load      I>IS_D   [0x4ac0, line 0x4ac0]
    4657   0  Directory                GetS      I>S_M    [0x4ac0, line 0x4ac0]
    4669   0  Directory             MemData    S_M>S      [0x4ac0, line 0x4ac0]
    4674   0        Seq                Done       >       [0x4aec, line 0x4ac0] 33 cycles
    4674   0    L1Cache       DataDirNoAcks   IS_D>S      [0x4ac0, line 0x4ac0]
    5321   0        Seq               Begin       >       [0x4aec, line 0x4ac0] ST
    5322   0    L1Cache               Store      S>SM_AD  [0x4ac0, line 0x4ac0]
    5327   0  Directory                GetM      S>M_M    [0x4ac0, line 0x4ac0]
```

Maybe there is a sharer in the sharers list when there shouldn't be? We
can add a defensive assert in clearOwner and setOwner.

```cpp
action(setOwner, "sO", desc="Set the owner") {
    assert(getDirectoryEntry(address).Sharers.count() == 0);
    peek(request_in, RequestMsg) {
        getDirectoryEntry(address).Owner.add(in_msg.Requestor);
    }
}

action(clearOwner, "cO", desc="Clear the owner") {
    assert(getDirectoryEntry(address).Sharers.count() == 0);
    getDirectoryEntry(address).Owner.clear();
}
```

Now, I get the following error:

```termout
    panic: Runtime Error at MSI-dir.sm:301: assert failure.
```

This is in setOwner. Well, actually this is OK since we need to have the
sharers still set until we count them to send the ack count to the
requestor. Let's remove that assert and see what happens. Nothing. That
didn't help anything.

When are invalidations sent from the directory? Only on S-\>M\_M. So,
here, we need to remove ourselves from the invalidation list. I think we
need to keep ourselves in the sharer list since we subtract one when
sending the number of acks.

Note: I'm coming back to this a little later. It turns out that both of
these asserts are wrong. I found this out when running with more than
one CPU below. The sharers are set before clearing the Owner in M-\>S\_D
on a GetS.

So, onto the next problem!

```termout
    panic: Deadlock detected: current_time: 56091 last_progress_time: 6090 difference:  50001 processor: 0
```

Deadlocks are the worst kind of error. Whatever caused the deadlock is
ancient history (i.e., likely happened many cycles earlier), and often
very hard to track down.

Looking at the tail of the protocol trace (note: sometimes you must put
the protocol trace into a file because it grows *very* big) I see that
there is an address that is trying to be replaced. Let's start there.

```protocoltrace
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
    56091   0    L1Cache         Replacement   SM_A>SM_A   [0x5ac0, line 0x5ac0]
```

Before this replacement got stuck I see the following in the protocol
trace. Note: this is 50000 cycles in the past!

```protocoltrace
    ...
    5592   0    L1Cache               Store      S>SM_AD  [0x5ac0, line 0x5ac0]
    5597   0  Directory                GetM      S>M_M    [0x5ac0, line 0x5ac0]
    ...
    5641   0  Directory             MemData    M_M>M      [0x5ac0, line 0x5ac0]
    ...
    5646   0    L1Cache         DataDirAcks  SM_AD>SM_A   [0x5ac0, line 0x5ac0]
```

Ah! This clearly should not be DataDirAcks since we only have a single
CPU! So, we seem to not be subtracting properly. Going back to the
previous error, I was wrong about needing to keep ourselves in the list.
I forgot that we no longer had the -1 thing. So, let's remove ourselves
from the sharing list before sending the invalidations when we
originally get the S-\>M request.

So! With those changes the Ruby tester completes with a single core.
Now, to make it harder we need to increase the number of loads we do and
then the number of cores.

And, of course, when I increase it to 10,000 loads there is a deadlock.
Fun!

What I'm seeing at the end of the protocol trace is the following.

```protocoltrace
    144684   0    L1Cache         Replacement   MI_A>MI_A   [0x5bc0, line 0x5bc0]
    ...
    144685   0  Directory                GetM   MI_M>MI_M   [0x54c0, line 0x54c0]
    ...
    144685   0    L1Cache         Replacement   MI_A>MI_A   [0x5bc0, line 0x5bc0]
    ...
    144686   0  Directory                GetM   MI_M>MI_M   [0x54c0, line 0x54c0]
    ...
    144686   0    L1Cache         Replacement   MI_A>MI_A   [0x5bc0, line 0x5bc0]
    ...
    144687   0  Directory                GetM   MI_M>MI_M   [0x54c0, line 0x54c0]
    ...
```

This is repeated for a long time.

It seems that there is a circular dependence or something like that
causing this deadlock.

Well, it seems that I was correct. The order of the in\_ports really
matters! In the directory, I previously had the order: request,
response, memory. However, there was a memory packet that was blocked
because the request queue was blocked, which caused the circular
dependence and the deadlock. The order *should* be memory, response, and
request. I believe the memory/response order doesn't matter since no
responses depend on memory and vice versa.

Now, let's try with two CPUs. First thing I run into is an assert
failure. I'm seeing the first assert in setState fail.

```cpp
void setState(Addr addr, State state) {
    if (directory.isPresent(addr)) {
        if (state == State:M) {
            assert(getDirectoryEntry(addr).Owner.count() == 1);
            assert(getDirectoryEntry(addr).Sharers.count() == 0);
        }
        getDirectoryEntry(addr).DirState := state;
        if (state == State:I)  {
            assert(getDirectoryEntry(addr).Owner.count() == 0);
            assert(getDirectoryEntry(addr).Sharers.count() == 0);
        }
    }
}
```

To track this problem down, let's add a debug statement (DPRINTF) and
run with protocol trace. First I added the following line just before
the assert. Note that you are required to use the RubySlicc debug flag.
This is the only debug flag included in the generated SLICC files.

```cpp
DPRINTF(RubySlicc, "Owner %s\n", getDirectoryEntry(addr).Owner);
```

Then, I see the following output when running with ProtocolTrace and
RubySlicc.

```gem5trace
    118   0  Directory             MemData    M_M>M      [0x400, line 0x400]
    118: system.caches.controllers2: MSI-dir.sm:160: Owner [NetDest (16) 1 0  -  -  - 0  -  -  -  -  -  -  -  -  -  -  -  -  - ]
    118   0  Directory                GetM      M>M      [0x400, line 0x400]
    118: system.caches.controllers2: MSI-dir.sm:160: Owner [NetDest (16) 1 1  -  -  - 0  -  -  -  -  -  -  -  -  -  -  -  -  - ]
```

It looks like when we process the GetM when in state M we need to first
clear the owner before adding the new owner. The other options is in
setOwner we could have Set the Owner specifically instead of adding it
to the NetDest.

Oooo! This is a new error!

```termout
    panic: Runtime Error at MSI-dir.sm:229: Unexpected message type..
```

What is this message that fails? Let's use the RubyNetwork debug flag to
try to track down what message is causing this error. A few lines above
the error I see the following message whose destination is the
directory.

The destination is a NetDest which is a bitvector of MachineIDs. These
are split into multiple sections. I know I'm running with two CPUs, so
the first two 0's are for the CPUs, and the other 1 must be fore the
directory.

```gem5trace
    2285: PerfectSwitch-2: Message: [ResponseMsg: addr = [0x8c0, line 0x8c0] Type = InvAck Sender = L1Cache-1 Destination = [NetDest (16) 0 0  -  -  - 1  -  -  -  -  -  -  -  -  -  -  -  -  - ] DataBlk = [ 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0xb1 0xb2 0xb3 0xb4 0xca 0xcb 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 ] MessageSize = Control Acks = 0 ]
```

This message has the type InvAck, which is clearly wrong! It seems that
we are setting the requestor wrong when we send the invalidate (Inv)
message to the L1 caches from the directory.

Yes. This is the problem. We need to make the requestor the original
requestor. This was already correct for the FwdGetS/M, but I missed the
invalidate somehow. On to the next error!

```termout
    panic: Invalid transition
    system.caches.controllers0 time: 2287 addr: 0x8c0 event: LastInvAck state: SM_AD
```

This seems to be that I am not counting the acks correctly. It could
also be that the directory is much slower than the other caches at
responding since it has to get the data from memory.

If it's the latter (which I should be sure to verify), what we could do
is include an ack requirement for the directory, too. Then, when the
directory sends the data (and the owner, too) decrement the needed acks
and trigger the event based on the new ack count.

Actually, that first hypothesis was not quite right. I printed out the
number of acks whenever we receive an InvAck and what's happening is
that the other cache is responding with an InvAck before the directory
has told it how many acks to expect.

So, what we need to do is something like what I was talking about above.
First of all, we will need to let the acks drop below 0 and add the
total acks to it from the directory message. Then, we are going to have
to complicate the logic for triggering last ack, etc.

Ok. So now we're letting the tbe.Acks drop below 0 and then adding the
directory acks whenever they show up.

Next error: This is a tough one. The error is now that the data doesn't
match as it should. Kind of like the deadlock, the data could have been
corrupted in the ancient past. I believe the address is the last one in
the protocol trace.

```termout
    panic: Action/check failure: proc: 0 address: 19688 data: 0x779e6d0
    byte\_number: 0 m\_value+byte\_number: 53 byte: 0 [19688, value: 53,
    status: Check\_Pending, initiating node: 0, store\_count: 4]Time:
    5843
```

So, it could be something to do with ack counts, though I don't think
this is the issue. Either way, it's a good idea to annotate the protocol
trace with the ack information. To do this, we can add comments to the
transition with APPEND\_TRANSITION\_COMMENT.

```cpp
action(decrAcks, "da", desc="Decrement the number of acks") {
    assert(is_valid(tbe));
    tbe.Acks := tbe.Acks - 1;
    APPEND_TRANSITION_COMMENT("Acks: ");
    APPEND_TRANSITION_COMMENT(tbe.Acks);
}
```

```protocoltrace
    5737   1    L1Cache              InvAck  SM_AD>SM_AD  [0x400, line 0x400] Acks: -1
```

For these data issues, the debug flag RubyNetwork is useful because it
prints the value of the data blocks at every point it is in the network.
For instance, for the address in question above, it looks like the data
block is all 0's after loading from main-memory. I believe this should
have valid data. In fact, if we go back in time some we see that there
was some non-zero elements.

```protocoltrace
    5382   1    L1Cache                 Inv      S>I      [0x4cc0, line 0x4cc0]
```

```gem5trace
    5383: PerfectSwitch-1: Message: [ResponseMsg: addr = [0x4cc0, line
    0x4cc0] Type = InvAck Sender = L1Cache-1 Destination = [NetDest (16) 1
    0 - - - 0 - - - - - - - - - - - - - ] DataBlk = [ 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x35 0x36 0x37 0x61 0x6d 0x6e 0x6f 0x70 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 ] MessageSize = Control Acks =
    0 ] ... ... ... 5389 0 Directory MemData M\_M\    >M [0x4cc0, line 0x4cc0]
    5390: PerfectSwitch-2: incoming: 0 5390: PerfectSwitch-2: Message:
    [ResponseMsg: addr = [0x4cc0, line 0x4cc0] Type = Data Sender =
    Directory-0 Destination = [NetDest (16) 1 0 - - - 0 - - - - - - - - -
    - - - - ] DataBlk = [ 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
    0x0 ] MessageSize = Data Acks = 1 ]
```

It seems that memory is not being updated correctly on the M-\>S
transition. After lots of digging and using the MemoryAccess debug flag
to see exactly what was being read and written to main memory, I found
that in sendDataToMem I was using the request\_in. This is right for
PutM, but not right for Data. We need to have another action to send
data from response queue!

```termout
    panic: Invalid transition
    system.caches.controllers0 time: 44381 addr: 0x7c0 event: Inv state: SM_AD
```

Invalid transition is my personal favorite kind of SLICC error. For this
error, you know exactly what address caused it, and it's very easy to
trace through the protocol trace to find what went wrong. However, in
this case, nothing went wrong, I just forgot to put this transition in!
Easy fix!


---


## Configuring for a standard protocol

*Source: https://www.gem5.org/documentation/learning_gem5/part3/simple-MI_example/*

You can easily adapt the simple example configurations from this part to
the other SLICC protocols in gem5. In this chapter, we will briefly look
at an example with `MI_example`, though this can be easily extended to
other protocols.

However, these simple configuration files will only work in syscall
emulation mode. Full system mode adds some complications such as DMA
controllers. These scripts can be extended to full system.

For `MI_example`, we can use exactly the same runscript as before
(`simple_ruby.py`), we just need to implement a different
`MyCacheSystem` (and import that file in `simple_ruby.py`). Below, is
the classes needed for `MI_example`. There are only a couple of changes
from `MSI`, mostly due to different naming schemes. You can download the
file
[here](https://github.com/gem5/gem5/blob/stable/configs/learning_gem5/part3/ruby_caches_MI_example.py).

```python
class MyCacheSystem(RubySystem):

    def __init__(self):
        if buildEnv['PROTOCOL'] != 'MI_example':
            fatal("This system assumes MI_example!")

        super(MyCacheSystem, self).__init__()

    def setup(self, system, cpus, mem_ctrls):
        """Set up the Ruby cache subsystem. Note: This can't be done in the
           constructor because many of these items require a pointer to the
           ruby system (self). This causes infinite recursion in initialize()
           if we do this in the __init__.
        """
        # Ruby's global network.
        self.network = MyNetwork(self)

        # MI example uses 5 virtual networks
        self.number_of_virtual_networks = 5
        self.network.number_of_virtual_networks = 5

        # There is a single global list of all of the controllers to make it
        # easier to connect everything to the global network. This can be
        # customized depending on the topology/network requirements.
        # Create one controller for each L1 cache (and the cache mem obj.)
        # Create a single directory controller (Really the memory cntrl)
        self.controllers = \
            [L1Cache(system, self, cpu) for cpu in cpus] + \
            [DirController(self, system.mem_ranges, mem_ctrls)]

        # Create one sequencer per CPU. In many systems this is more
        # complicated since you have to create sequencers for DMA controllers
        # and other controllers, too.
        self.sequencers = [RubySequencer(version = i,
                                # I/D cache is combined and grab from ctrl
                                icache = self.controllers[i].cacheMemory,
                                dcache = self.controllers[i].cacheMemory,
                                clk_domain = self.controllers[i].clk_domain,
                                ) for i in range(len(cpus))]

        for i,c in enumerate(self.controllers[0:len(cpus)]):
            c.sequencer = self.sequencers[i]

        self.num_of_sequencers = len(self.sequencers)

        # Create the network and connect the controllers.
        # NOTE: This is quite different if using Garnet!
        self.network.connectControllers(self.controllers)
        self.network.setup_buffers()

        # Set up a proxy port for the system_port. Used for load binaries and
        # other functional-only things.
        self.sys_port_proxy = RubyPortProxy()
        system.system_port = self.sys_port_proxy.slave

        # Connect the cpu's cache, interrupt, and TLB ports to Ruby
        for i,cpu in enumerate(cpus):
            cpu.icache_port = self.sequencers[i].slave
            cpu.dcache_port = self.sequencers[i].slave
            isa = buildEnv['TARGET_ISA']
            if isa == 'x86':
                cpu.interrupts[0].pio = self.sequencers[i].master
                cpu.interrupts[0].int_master = self.sequencers[i].slave
                cpu.interrupts[0].int_slave = self.sequencers[i].master
            if isa == 'x86' or isa == 'arm':
                cpu.itb.walker.port = self.sequencers[i].slave
                cpu.dtb.walker.port = self.sequencers[i].slave

class L1Cache(L1Cache_Controller):

    _version = 0
    @classmethod
    def versionCount(cls):
        cls._version += 1 # Use count for this particular type
        return cls._version - 1

    def __init__(self, system, ruby_system, cpu):
        """CPUs are needed to grab the clock domain and system is needed for
           the cache block size.
        """
        super(L1Cache, self).__init__()

        self.version = self.versionCount()
        # This is the cache memory object that stores the cache data and tags
        self.cacheMemory = RubyCache(size = '16kB',
                               assoc = 8,
                               start_index_bit = self.getBlockSizeBits(system))
        self.clk_domain = cpu.clk_domain
        self.send_evictions = self.sendEvicts(cpu)
        self.ruby_system = ruby_system
        self.connectQueues(ruby_system)

    def getBlockSizeBits(self, system):
        bits = int(math.log(system.cache_line_size, 2))
        if 2**bits != system.cache_line_size.value:
            panic("Cache line size not a power of 2!")
        return bits

    def sendEvicts(self, cpu):
        """True if the CPU model or ISA requires sending evictions from caches
           to the CPU. Two scenarios warrant forwarding evictions to the CPU:
           1. The O3 model must keep the LSQ coherent with the caches
           2. The x86 mwait instruction is built on top of coherence
           3. The local exclusive monitor in ARM systems
        """
        return True

    def connectQueues(self, ruby_system):
        """Connect all of the queues for this controller.
        """
        self.mandatoryQueue = MessageBuffer()
        self.requestFromCache = MessageBuffer(ordered = True)
        self.requestFromCache.master = ruby_system.network.slave
        self.responseFromCache = MessageBuffer(ordered = True)
        self.responseFromCache.master = ruby_system.network.slave
        self.forwardToCache = MessageBuffer(ordered = True)
        self.forwardToCache.slave = ruby_system.network.master
        self.responseToCache = MessageBuffer(ordered = True)
        self.responseToCache.slave = ruby_system.network.master

class DirController(Directory_Controller):

    _version = 0
    @classmethod
    def versionCount(cls):
        cls._version += 1 # Use count for this particular type
        return cls._version - 1

    def __init__(self, ruby_system, ranges, mem_ctrls):
        """ranges are the memory ranges assigned to this controller.
        """
        if len(mem_ctrls) > 1:
            panic("This cache system can only be connected to one mem ctrl")
        super(DirController, self).__init__()
        self.version = self.versionCount()
        self.addr_ranges = ranges
        self.ruby_system = ruby_system
        self.directory = RubyDirectoryMemory()
        # Connect this directory to the memory side.
        self.memory = mem_ctrls[0].port
        self.connectQueues(ruby_system)

    def connectQueues(self, ruby_system):
        self.requestToDir = MessageBuffer(ordered = True)
        self.requestToDir.slave = ruby_system.network.master
        self.dmaRequestToDir = MessageBuffer(ordered = True)
        self.dmaRequestToDir.slave = ruby_system.network.master

        self.responseFromDir = MessageBuffer()
        self.responseFromDir.master = ruby_system.network.slave
        self.dmaResponseFromDir = MessageBuffer(ordered = True)
        self.dmaResponseFromDir.master = ruby_system.network.slave
        self.forwardFromDir = MessageBuffer()
        self.forwardFromDir.master = ruby_system.network.slave
        self.responseFromMemory = MessageBuffer()

class MyNetwork(SimpleNetwork):
    """A simple point-to-point network. This doesn't not use garnet.
    """

    def __init__(self, ruby_system):
        super(MyNetwork, self).__init__()
        self.netifs = []
        self.ruby_system = ruby_system

    def connectControllers(self, controllers):
        """Connect all of the controllers to routers and connect the routers
           together in a point-to-point network.
        """
        # Create one router/switch per controller in the system
        self.routers = [Switch(router_id = i) for i in range(len(controllers))]

        # Make a link from each controller to the router. The link goes
        # externally to the network.
        self.ext_links = [SimpleExtLink(link_id=i, ext_node=c,
                                        int_node=self.routers[i])
                          for i, c in enumerate(controllers)]

        # Make an "internal" link (internal to the network) between every pair
        # of routers.
        link_count = 0
        self.int_links = []
        for ri in self.routers:
            for rj in self.routers:
                if ri == rj: continue # Don't connect a router to itself!
                link_count += 1
                self.int_links.append(SimpleIntLink(link_id = link_count,
                                                    src_node = ri,
                                                    dst_node = rj))
```


---


# ═══ gem5 101 ═══


## gem5 101

*Source: https://www.gem5.org/documentation/learning_gem5/gem5_101/*

# gem5 101

This is a six part course which will help you pick up the basics of gem5, and
illustrate some common uses. This course is based around the assignments from a
particular offering of architecture courses, CS 752 and CS 757, taught at the
University of Wisconsin-Madison.

**IMPORTANT NOTE:** Links to the homework parts here were translated to
markdown from a, now non-existent, wiki. Best efforts have been made to
preserve the content in its original state but these homework assignments
may still:

1. Be out of date and incompatible with the latest versions of gem5.
2. Contain dead-links or references to out-of-date resources.

We do not guarantee these homework assignments can be completed easily in their
current state.

## First steps with gem5, and Hello World!
[Part I](/documentation/learning_gem5/gem5_101/homework-1)

In part I, you will first learn to download and build gem5 correctly, create a simple configuration script for a simple system, write a simple C program and run a gem5 simulation. You will then introduce a two-level cache hierarchy in your system (fun stuff). Finally, you get to view the effect of changing system parameters such as memory types, processor frequency and complexity on the performance of your simple program.

## Getting down and dirty
[Part II](/documentation/learning_gem5/gem5_101/homework-2)

For part II, we had used gem5 capabilities straight out of the box. Now, we will witness the flexibility and usefulness of gem5 by extending the simulator functionality. We walk you through the implementation of an x86 instruction (FSUBR), which is currently missing from gem5. This will introduce you to gem5's language for describing instruction sets, and illustrate how instructions are decoded and broken down into micro-ops which are ultimately executed by the processor.

## Pipelining solves everything
[Part III](/documentation/learning_gem5/gem5_101/homework-3)

From the ISA, we now move on to the processor micro-architecture. Part III introduces the various different cpu models implemented in gem5, and analyzes the performance of a pipelined implementation. Specifically, you will learn how the latency and bandwidth of different pipeline stages affect overall performance. Also, a sample usage of gem5 pseudo-instructions is also included at no additional cost.

## Always be experimenting
[Part IV](/documentation/learning_gem5/gem5_101/homework-4)

Exploiting instruction-level parallelism (ILP) is a useful way of improving single-threaded performance. Branch prediction and predication are two common techniques of exploiting ILP. In this part, we use gem5 to verify the hypothesis that graph algorithms that avoid branches perform better than algorithms that use branches. This is a useful exercise in understanding how to incorporate gem5 into your research process.

## Cold, hard, cache
[Part V](/documentation/learning_gem5/gem5_101/homework-5)

After looking at the processor core, we now turn our attention to the cache hierarchy. We continue our focus on experimentation, and consider tradeoffs in cache design such as replacement policies and set-associativity. Furthermore, we also learn more about the gem5 simulator, and create our first simObject!

## Single-core is so two-thousand and late
[Part VI](/documentation/learning_gem5/gem5_101/homework-6)

For this last part, we go both multi-core and full system at the same time! We analyze the performance of a simple application on giving it more computational resources (cores). We also boot a full-fledged unmodified operating system (Linux) on the target system simulated by gem5. Most importantly, we teach you how to create your own, simpler version of the dreaded fs.py configuration script, one that you can feel comfortable modifying.

## Complete!
Congrats, you are now familiar with the fundamentals of gem5. You are now allowed to wear the “Bro, do you even gem5?” t-shirt (if you manage to find one).