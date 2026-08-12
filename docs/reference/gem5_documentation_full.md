# gem5 Documentation — Full Corpus (excluding Learning gem5)

Source: https://www.gem5.org/documentation/  (repo: github.com/gem5/website)
Verbatim page Markdown; only YAML frontmatter stripped, section headers + source URLs added.
NOTE: The 'Learning gem5' tutorial set is deliberately omitted here — it's in the separate learning_gem5_full.md file. Together the two cover all of /documentation/ with no overlap.

---

## Table of Contents

- **Documentation Home**
  - gem5 documentation
- **General Documentation (main reference)**
  - index.md
  - gem5-resources
  - Checkpoints
  - Common errors within gem5
  - gem5-resources
  - Kconfig Build System
  - Setting Up and Using KVM on your machine
  - M5ops
  - Moving Active Changes from Gerrit to GitHub
  - Power and Thermal Model
  - "Architecture Support"
  - "ARM implementation"
  - ISA Parser
  - X86 Micro-op ISA
  - Building gem5
  - Building EXTRAS
  - "Compiling Workloads"
  - "gem5's CPU models"
  - Execution Basics
  - Minor CPU Model
  - Out of order CPU model
  - Simple CPU Models
  - Trace CPU Model
  - "Visualization"
  - Debugging and Testing
  - Debugger-based Debugging
  - Debugging Simulated Code
  - Trace-based Debugging
  - Garnet Synthetic Traffic
  - Ruby Random Tester
  - "Developing gem5"
  - "C/C++ Coding Style"
  - "Release Procedures"
  - "Full system support"
  - "Building Android Marshmallow"
  - "Building ARM Kernel"
  - Devices
  - Creating disk images
  - "Guest Binaries"
  - "m5 term"
  - "Supported Kernels and Disk Images for gem5 stable"
  - Full System AMD GPU model
  - AMD VEGA GPU model
  - "Memory system"
  - "Classic memory system coherence"
  - "Classic caches"
  - "gem5_memory_syste"
  - "Indexing Policies"
  - "Replacement Policies"
  - "Introduction"
  - "CHI"
  - "Garnet standalone"
  - "MESI two level"
  - "MI example"
  - "MOESI CMP directory"
  - "MOESI CMP token"
  - "MOESI hammer"
  - "Cache Coherence Protocols"
  - "Garnet 2.0"
  - "Garnet Synthetic Traffic"
  - "HeteroGarnet (Garnet 3.0)"
  - "Interconnection network"
  - "SLICC"
  - Statistics
  - Statistics API
- **gem5 Standard Library (stdlib)**
  - Standard Library Overview
  - Hello World Tutorial
  - X86 Full-System Tutorial
  - Developing Your Own Components Tutorial
  - How To Create Your Own Board Using The gem5 Standard Library
  - Local Resources Support in gem5
  - Suites in gem5
  - Setting gem5 Resources data sources to support local resources
- **gem5art**
  - Zen and the art of gem5 experiments
  - Summary
  - Artifacts
  - Runs
  - Tasks
  - Disk Images
  - FAQ
  - Boot Tutorial
  - NPB Tutorial
  - PARSEC Tutorial
  - SPEC Tutorial
  - Microbench Tutorial
- **Reporting Problems**
  - Reporting Problems

---


# ═══ Documentation Home ═══


## gem5 documentation

*Source: https://www.gem5.org/documentation/*

# gem5 Documentation

## gem5 Bootcamp 2024

As of gem5 v24.0, the most comprehensive, up to date guide for learning how to use gem5 is the
material from the [summer 2024 gem5 bootcamp](https://bootcamp.gem5.org/).

## Learning gem5

**Notice: Many parts of Learning gem5 are outdated. Some sections of Learning gem5 have been updated for gem5 v24.1 based on content from the 2024 gem5 bootcamp, but others have not. Proceed with caution!**

[Learning gem5](learning_gem5/introduction/) gives a prose-heavy introduction to using gem5 for computer architecture research written by Jason Lowe-Power.
This is a great resource for junior researchers who plan on using gem5 heavily for a research project.

It covers details of how gem5 works starting with [how to create configuration scripts](learning_gem5/part1/simple_config).
It then goes on to describe [how to modify and extend](learning_gem5/part2/environment) gem5 for your research including [creating `SimObjects`](learning_gem5/part2/helloobject), [using gem5's event-driven simulation infrastructure](learning_gem5/part2/events), and [adding memory system objects](learning_gem5/part2/memoryobject).
In [Learning gem5 Part 3](learning_gem5/part3/MSIintro) the [Ruby cache coherence model](/documentation/general_docs/ruby) is discussed in detail including a full implementation of an MSI cache coherence protocol.

More Learning gem5 parts are coming soon including:
* CPU models and ISAs
* Debugging gem5
* **Your idea here!**

Note: this has been migrated from learning.gem5.org and there are minor problems due to this migration (e.g., missing links, bad formatting).
Please contact Jason (jason@lowepower.com) or create a PR if you find any errors!

## gem5 101

[gem5 101](learning_gem5/gem5_101) is a set of assignments mostly from Wisconsin's graduate computer architecture classes (CS 752, CS 757, and CS 758) which will help you learn to use gem5 for research.

## gem5 API documentation

You can find the doxygen-based documentation here: <http://doxygen.gem5.org/release/current/index.html>

## Other general gem5 documentation

See the navigation on the left side of the page!


---


# ═══ General Documentation (main reference) ═══


## index.md



---


## gem5-resources

*Source: https://www.gem5.org/documentation/general_docs/gem5-apis/*

For complete documentation of all methods and variables tagged as APIs, please
see our [Doxygen Module page](
http://doxygen.gem5.org/release/v20-1-0-0/modules.html).

# The gem5 API

In efforts to improve product stability, the gem5 development team is gradually
tagging methods and variables within gem5 as APIs which developers will need to
undergo specific procedures to change. Our goal with the gem5 API is to provide
a stable interface for users to build gem5 models, and extend the gem5
code-base, with guarantees these APIs will not change in a dramatic sudden
manner between gem5 releases.

## How is the gem5 API documented?

We document the gem5 APIs using the [Doxygen documentation generation tool](
https://www.doxygen.nl/index.html). This means you may see the API tagged
at the level of source-code and via our [web-based documentation](
http://doxygen.gem5.org). We use Doxygen's `@ingroup` tag, to specify a
method/variables as part of the gem5 API. We break the API down into
sub-domains such as `api_simobject` or `api_ports`, though all the gem5 APIs
are tagged with the prefix `api_`. For example, we tag SimObject's `params()`
function as follows:

```cpp
/**
* @return This function returns the cached copy of the object parameters.
*
* @ingroup api_simobject
*/
const Params *params() const { return _params; }
```

Via Doxygen automatic generation, the list of gem5 APIs can be found on the
[Doxygen module page](http://doxygen.gem5.org/release/current/modules.html).
In this example, the entire list of SimObject APIs are noted in the
[SimObject API page](
http://doxygen.gem5.org/release/current/group__api__simobject.html). The
definitions of different API groups can be found in
[`src/doxygen/group_definitions.hh`](
https://github.com/gem5/gem5/blob/stable/src/doxygen/group_definitions.hh).

### Notes for developers

If a developer wishes to tag a new method/variable as part of the gem5 API,
the gem5 community should be consulted. APIs are intended to stay unaltered for
some time. To avoid the gem5 project becoming encumbered with "too many APIs",
we strongly advise those wishing to extend the API to communicate to the
gem5 development team as to why the API will be of value. The
[gem5 Discussion page](https://github.com/orgs/gem5/discussions/categories/gem5-dev)
is a good communication channel for this.

## How can the API change?

We do not guarantee the gem5 API will never change over time. gem5 is a
product under continual development which must adapt to the needs of the
computer architecture research community. However, we guarantee that API
changes will follow strict guidelines outlined below.

1. When an API method or variable is altered, it will be done so in a way in
which the new API will exist alongside the old, with the old API tagged as
deprecated and still functional.

2. The old, deprecated API will exist for two gem5 major cycles before being
removed entirely from code-base, though gem5 developers may choose to keep a
deprecated API in the code-base for longer. For example, if an API is tagged as
deprecated in gem5 21.0, it will also still exist (still tagged as deprecated)
in gem5 21.1. It may be removed entirely in gem5 21.2, though this will be left
to the discretion of the gem5 developers.

3. The gem5 deprecated C++ APIs will be tagged with the C++ deprecated
attribute (`[[deprecated(<msg>)]]`). When utilizing a deprecated C++ API, a
warning will be given at compilation time specifying which API to transition
to. The gem5 deprecated Python parameter APIs are wrapped with our [bespoke
`DeprecatedParam` class](
https://github.com/gem5/gem5/blob/bd13e8e206e6c86581cf9afa904ef1060351a4b0/src/python/m5/params.py#L2166).
Python parameters wrapped in this class will throw an warning when used and
specify which API to transition to.

### Notes for Developers

Prior to making any changes to the gem5 API the [gem5-dev mailing list](
/ask-a-question/) should be consulted. Changing the API, for whatever reason,
**will** be subject to higher scrutiny than other changes. Developers should
be prepared to provide compelling arguments as to why the API needs changed. We
strongly recommend API changes are discussed or they may be rejected during the
code review.

When creating a new API the old API must be tagged as deprecated and the new
API created to exist alongside the old. **It is of upmost importance that the
old, deprecated API is maintained and not deleted**.

As an example, take the following code:

```cpp
/**
 * @ingroup api_bitfield
 */
inline uint64_t
mask(int first, int last)
{
    return mbits((uint64_t)-1LL, first, last);
}
```

This function is part of the gem5 bitfield API. It is a basic mask function
that takes the MSB (first) and the LSB (last) for the generation of a 64-bit.
Let us assume there is a good argument that this function should be replaced
with one that takes the MSB (first), and the length of the mask instead.

To start, the old API needs maintained (i.e., not changed) and tagged with the
`[[deprecated(<msg>)]]` tag. The message (`<msg>`) Should state the new API
to use, and the API tagging should be removed. The new API should then be
created and tagged. So, using our example:

```cpp
[[deprecated("Use mask_length instead.")]]
inline uint64_t
mask(int first, int last)
{
    return mbits((uint64_t)-1LL, first, last);
}

/**
 * @ingroup api_bitfield
 */
inline uint64_t
mask_length(int first, int length)
{
    return mbits((uint64_t)-1LL, first, first + length);
}
```

Here a new function, `mask_length`, has been created. It has been tagged
correctly via Doxygen. The old API, `mask` exists but has the
`[[deprecated]]` annotation added. The message provided states which API
replaces it.

The developer then needs to replace all usage of `mask` in the code-base with
`mask_length`. A warning will be given at compile time if `mask` is used,
stating that it is deprecated and to "Use mask\_length instead.".

Occasionally there may be need to change the python API interface, which
relates to tagged APIs. For example, let's take the below code:

```python
class TLBCoalescer(ClockedObject):
    type = 'TLBCoalescer'
    cxx_class = 'TLBCoalescer'
    cxx_header = 'gpu-compute/tlb_coalescer.hh'

    ...

    slave    = VectorResponsePort("Port on side closer to CPU/CU")
    master   = VectorRequestPort("Port on side closer to memory")

   ...
```

[In recent revisions](
https://github.com/gem5/gem5/tree/392c1ced53827198652f5eda58e1874246b024f4)
the terms `master` and `slave` have been replaced. Though, the `slave` and
`master` terminology are widely used, so much so we consider them part of the
old API. We therefore wish to deprecate this API is a safe manner while
changing `master` and `slave` with `cpu_side_ports` and `mem_side_ports`. To
do so we would maintain the `master` and `slave` variables but utilize our
[`DeprecatedParam` Class](
https://github.com/gem5/gem5/blob/bd13e8e206e6c86581cf9afa904ef1060351a4b0/src/python/m5/params.py#L2166)
to produce warnings when and if these deprecated variables are used. Working on
our example, we would produce the following:

```python
class TLBCoalescer(ClockedObject):
    type = 'TLBCoalescer'
    cxx_class = 'TLBCoalescer'
    cxx_header = 'gpu-compute/tlb_coalescer.hh'

    ...

    cpu_side_ports = VectorResponsePort("Port on side closer to CPU/CU")
    slave    = DeprecatedParam(cpu_side_ports,
                        '`slave` is now called `cpu_side_ports`')
    mem_side_ports = VectorRequestPort("Port on side closer to memory")
    master   = DeprecatedParam(mem_side_ports,
                        '`master` is now called `mem_side_ports`')

   ...
```

Note the use of `DeprecatedParam` that both ensures `master` and `slave` still
function by redirecting to `mem_side_ports` and `cpu_side_ports` respectively,
as well as providing a comment explaining why this API was deprecated. This
will be displayed to the user as a warning if `master` or `slave` are ever
used.

As with all changes to the gem5 source, these changes will have to go through
our Gerrit code review system before being merged into the `develop` branch,
and eventually making its way to our `stable` branch as part of a gem5 release.
In line with our API policy, these deprecated APIs must exist in a
marked-as-deprecated state for two gem5 major release cycles. After this they
may be removed though developers are under no requirement to do so.


---


## Checkpoints

*Source: https://www.gem5.org/documentation/general_docs/checkpoints/*

# Checkpoints

Checkpoints are essentially snapshots of a simulation. You would want to use a checkpoint when your simulation takes an extremely long time (which is almost always the case) so you can resume from that checkpoint at a later time with the DerivO3CPU.

## Creation

First of all, you need to create a checkpoint. Each checkpoint as saved in a new directory named 'cpt.TICKNUMBER', where TICKNUMBER refers to the tick value at which this checkpoint was created. There are several ways in which a checkpoint can be created:

* After booting the gem5 simulator, execute the command m5 checkpoint. One can execute the command manually using m5term, or include it in a run script to do this automatically after the Linux kernel has booted up.
* There is a pseudo instruction that can be used for creating checkpoints. For example, one may include this pseudo instruction in an application program, so that the checkpoint is created when the application has reached a certain state.
* The option **-****-take-checkpoints** can be provided to the python scripts (fs.py, ruby_fs.py) so that checkpoints are dumped periodically. The option **-****-checkpoint-at-end** can be used for creating the checkpoint at the end of the simulation. Take a look at the file **configs/common/Options.py** for these options.

While creating checkpoints with Ruby memory model, it is necessary to use the MOESI hammer protocol. This is because checkpointing the correct memory state requires that the caches are flushed to the memory. This flushing operation is currently supported only with the MOESI hammer protocol.

## Restoring

Restoring from a checkpoint can usually be easily done from the command line, e.g.:

```console
  build/ALL/gem5.debug configs/example/fs.py -r N
  OR
  build/ALL/gem5.debug configs/example/fs.py --checkpoint-restore=N
```

The number N is integer that represents checkpoint number which usually starts from 1 then increases incrementally to 2,3,4...

By default, gem5 assumes that the checkpoint is to be restored using Atomic CPUs. This may not work if the checkpoint was recorded using Timing / Detailed / Inorder CPU. One can mention the option <br /> **-****-restore-with-cpu \<CPU Type\>** on the command line. The cpu type supplied with this option is then used for restoring from the checkpoint.

## Detailed example: Parsec

In the following section we would describe how checkpoints are created for workloads PARSEC benchmark suite. However similar procedure can be followed to create checkpoint for other workloads beyond PARSEC suite. Following are the high level steps of creating checkpoint:

1. Annotate each workload with start and end of Region of Interest and with start and end of work units in the program.
2. Take a checkpoint at the start of the Region of Interest.
3. Simulate the whole program in the Region of Interest and periodically take checkpoints.
4. Analyse the statistics corresponding to periodic checkpoints and select the most interesting section of the program execution.
5. Take warm up cache trace for Ruby before reaching most interesting portion of the program and take the final checkpoint.
In each of the following sections we explain each of the above steps in more details.

### Annotating workloads

Annotation is required for two purposes: for defining region of program beyond the initialization section of a program and for defining logical units of work in each of the workloads.

Workloads in PARSEC benchmark suite, already has annotating demarcating start and end of portion of program without program initialization section and program finalization section. We just use gem5 specific annotation for start of Region of Interest. The start of the Region of Interest (ROI) is marked by **m5_roi_begin()** and the end of ROI is demarcated by **m5_roi_end()**.

Due to large simulation time its not always possible to simulate whole program. Moreover, unlike single threaded programs, simulating for a given number instructions in multi-threaded workloads is not a correct way to simulate portion of a program due to possible presence of instructions spinning on synchronization variable. Thus it is important define semantically meaningful logical units of work in each workload. Simulating for a given number of workuints in a multi-threaded workloads gives a reasonable way of simulating portion of workloads as the problem of instructions spinning on synchronization variables.

# Switchover/Fastforwarding

## Sampling

Sampling (switching between functional and detailed models) can be implemented via your Python script. In your script you can direct the simulator to switch between two sets of CPUs. To do this, in your script setup a list of tuples of (oldCPU, newCPU). If there are multiple CPUs you wish to switch simultaneously, they can all be added to that list. For example:

```python
run_cpu1 = SimpleCPU()
switch_cpu1 = DetailedCPU(switched_out=True)
run_cpu2 = SimpleCPU()
switch_cpu2 = FooCPU(switched_out=True)
switch_cpu_list = [(run_cpu1,switch_cpu1),(run_cpu2,switch_cpu2)]
```

Note that the CPU that does not immediately run should have the parameter "switched_out=True". This keeps those CPUs from adding themselves to the list of CPUs to run; they will instead get added when you switch them in.

In order for gem5 to instantiate all of your CPUs, you must make the CPUs that will be switched in a child of something that is in the configuration hierarchy. Unfortunately at the moment some configuration limitations force the switch CPU to be placed outside of the System object. The Root object is the next most convenient place to place the CPU, as shown below:

```python
m5.simulate(500)  # simulate for 500 cycles
m5.switchCpus(switch_cpu_list)
m5.simulate(500)  # simulate another 500 cycles after switching
```

Note that gem5 may have to simulate for a few cycles prior to switching CPUs due to any outstanding state that may be present in the CPUs being switched out.


---


## Common errors within gem5

*Source: https://www.gem5.org/documentation/general_docs/common-errors/*

Here are some common issues that users run into when using gem5, and information on how to fix them on how to fix them.

## Build errors

If your gem5 compilation fails with the following message:

```txt
[    LINK]  -> ALL/gem5.opt
collect2: fatal error: ld terminated with signal 9 [Killed]
compilation terminated.
scons: *** [build/ALL/gem5.opt] Error 1
scons: building terminated because of errors.
```

This indicates that your machine has run out of memory while trying to build
gem5 and has killed the process as a result.
If this occurs, try compiling gem5 with fewer threads, as this will consume
less memory.
If there are other processes using large amounts of memory on your system, try
building gem5 when more memory is available.

## Segmentation Fault

A segfault error can occur and will output to the terminal like the following:

```bash
gem5 has encountered a segmentation fault!

— BEGIN LIBC BACKTRACE —
gem5/build/X86/gem5.opt(_Z15print_backtracev+0x2c)[0x55ead536d5bc]
gem5/build/X86/gem5.opt(+0x1030b8f)[0x55ead537fb8f]
/lib/x86_64-linux-gnu/libpthread.so.0(+0x128a0)[0x7f50fb78b8a0]
/lib/x86_64-linux-gnu/libgcc_s.so.1(_Unwind_Resume+0xcf)[0x7f50fa12ad9f]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder10decodeInstENS_11ExtMachInstE+0x5d19e)[0x55ead4e5ea8e]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder6decodeENS_11ExtMachInstEm+0x244)[0x55ead4dc74a4]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder6decodeERNS_7PCStateE+0x22b)[0x55ead4dc779b]
gem5/build/X86/gem5.opt(_ZN12DefaultFetchI9O3CPUImplE5fetchERb+0x942)[0x55ead54695f2]
gem5/build/X86/gem5.opt(_ZN12DefaultFetchI9O3CPUImplE4tickEv+0xd3)[0x55ead546a7b3]
gem5/build/X86/gem5.opt(_ZN9FullO3CPUI9O3CPUImplE4tickEv+0x12b)[0x55ead5448e3b]
gem5/build/X86/gem5.opt(_ZN10EventQueue10serviceOneEv+0xa5)[0x55ead5375a95]
gem5/build/X86/gem5.opt(_Z9doSimLoopP10EventQueue+0x87)[0x55ead539a7b7]
gem5/build/X86/gem5.opt(_Z8simulatem+0xcba)[0x55ead539b80a]
gem5/build/X86/gem5.opt(+0x11d3431)[0x55ead5522431]
gem5/build/X86/gem5.opt(+0x6df0b4)[0x55ead4a2e0b4]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x64d7)[0x7f50fba38c47]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x5bf6)[0x7f50fba38366]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCode+0x19)[0x7f50fba325d9]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x6ac0)[0x7f50fba39230]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x5bf6)[0x7f50fba38366]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCode+0x19)[0x7f50fba325d9]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyRun_StringFlags+0x76)[0x7f50fbae26f6]
gem5/build/X86/gem5.opt(_Z6m5MainiPPc+0x83)[0x55ead537e823]
gem5/build/X86/gem5.opt(main+0x38)[0x55ead48d5068]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xe7)[0x7f50f9d4ab97]
gem5/build/X86/gem5.opt(_start+0x2a)[0x55ead48fd37a]
— END LIBC BACKTRACE —
```

It is important to note that in order to verify that you're encountering a segfault error, scroll above the back trace output and verify the line `gem5 has encountered a segmentation fault!` has outputted.
The cause of such error is usually the result of an error within your C++ files causing an incorrect address access.
The best way to debug segfaults within gem5 is to use gdb, to which we provide documentation [here](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/debugger_based_debugging).

## Fatal

A fatal error typically occurs when a simulation configuration is invalid and cannot be processed by the gem5 simulator.
The fatal error is preceded by the file that this error came from, which is usually a good indicator of where to look for what went wrong.
For example, in the error below, `gem5/src/cpu/base.cc` would be a good starting point to debug this error.

```bash
build/ALL/cpu/base.cc:186: fatal: Number of processes (cpu.workload) (0) assigned to the CPU does not equal number of threads (1).
```

This type of error can cover situations such as wrong file types or invalid values being passed to gem5, or unconnected ports, just to name a couple examples.
This should give you more information on the issue at hand, but if there still isn't enough information, using some of the [debugging techniques](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) within gem5, such as gdb or debug flags may help.


## Panic

If you encounter a panic error, that usually indicates that something is wrong with gem5 itself.
Some of the more common panic errors within gem5 are unrecognized values or unimplemented functions being used.
To debug these errors, you can start by looking into the file this error was generated by, which is indicated right before the panic error in your terminal.
For example, in the error below, it would be best to start looking at `gem5/src/sim/mem_pool.cc`

```bash
build/ARM/sim/mem_pool.cc:45: panic: assert(_totalPages > 0) failed
```

This should give you more information on the issue at hand, though similar to fatal errors above, if there still isn't enough information, using some of the [debugging techniques](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) within gem5 may help.

## Python Script Errors

For any type of Python error, such as an AttributeError or OSError, it is best to start out by looking below the error message, where you should see a trace output.
The first file and line number should indicate where the error occurred.
For example, with the error below, you should start by looking to `build/ARM/python/m5/SimObject.py(908)`, and if that doesn't give enough information, move onto `configs/example/gem5_library/arm-ubuntu-run.py(70)`.

```bash
AttributeError: Class PrivateL1PrivateL2CacheHierarchy has no parameter l1_size

At:
  build/ARM/python/m5/SimObject.py(908): __setattr__
  configs/example/gem5_library/arm-ubuntu-run.py(70): <module>
  build/ARM/python/m5/main.py(597): main
```

Similarly, if you receive a trace back error as shown below, you'll also want to refer to the very bottom of the output to get an idea as to where to start debugging.  In this IOError example, you'd first want to look towards `gem5/configs/common/SysPaths.py`

```bash
Traceback (most recent call last):
File "<string>", line 1, in <module>
File "/opt/gem5/src/python/m5/main.py", line 389, in main
exec filecode in scope
File "./configs/example/fs.py", line 327, in <module>
test_sys = build_test_system(np)
File "./configs/example/fs.py", line 96, in build_test_system
options.ruby, cmdline=cmdline)
File "/opt/gem5/configs/common/FSConfig.py", line 580, in
makeLinuxX86System
makeX86System(mem_mode, numCPUs, mdesc, self, Ruby)
File "/opt/gem5/configs/common/FSConfig.py", line 506, in makeX86System
disk2.childImage(disk('linux-bigswap2.img'))
File "/opt/gem5/configs/common/SysPaths.py", line 45, in disk
return searchpath(disk.path, filename)
File "/opt/gem5/configs/common/SysPaths.py", line 41, in searchpath
raise IOError, "Can't find file '%s' on path." % filename
IOError: Can't find file 'linux-bigswap2.img' on path.
```

Looking within this file should give you more information to help debug, though if this isn't enough, you can look [here](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) to enable trace based debugging for further information.

## PreCommit

If you're running into errors when pushing code to the develop branch, one potential issue is that you may not be passing the precommit checks that gem5 requires before any changes are submitted.
If you see within Gerrit that you have the following error on your verified check, you can navigate to the logs that were output by the tests.

```bash
Kokoro presubmit build finished with status: FAILURE
```

If the output in these logs contains anything like the line below, you need to verify that your changes match the coding style within gem5.

```bash
trim trailing whitespace.................................................Failed
```

In order to ensure your code passes these checks, you should install and run precommit on your changes.
You can install it by running the lines below.

```bash
pip install pre-commit
pre-commit install
```

Additionally, you could instead run `util/pre-commit-install.sh` to set it up.
From here, pre-commit will always run whenever you use `git commit`.
However, if you've already committed these files, you can manually check that pre-commit still passes by running `pre-commit run --files <files to format>` to check specific files, `pre-commit run --all-files` for testing the entire directory, or `pre-commit run <hook_id>` for individual hooks.
When running these commands, pre-commit will both detect any style issues, and automatically reformat the files for you.

## Change-ID

If you're running into issues getting you continuous integration tests to pass on GitHub, you may be forgetting to add a Change-Id to your commit message.
Though we have migrated away from using Gerrit, we still require the addition of a Change-Id.
In order to amend your commit and have all our checks pass, you must install the commit message hook from Gerrit.
You can install and update your commit by running the following commands below.

```bash
n f=.git/hooks/commit-msg ; mkdir -p  ;  curl -Lo  https://gerrit-review.googlesource.com/tools/hooks/commit-msg ; chmod +x
git commit --amend --no-edit
```

If you want more information on the commit message hook, read [here](https://gerrit-review.googlesource.com/Documentation/cmd-hook-commit-msg.html), and if you want to know more about Change-Ids, look [here](https://gerrit-review.googlesource.com/Documentation/user-changeid.html)

## Further Issues

If you continue to run into errors using gem5, feel free to [ask for help](/ask-a-question).
In addition, you can find information on how to report errors that may potentially need fixes [here](https://www.gem5.org/documentation/reporting_problems/) if other channels don't cover all the information you need.


---


## gem5-resources

*Source: https://www.gem5.org/documentation/general_docs/gem5_resources/*

# gem5 Resources

gem5 Resources is a repository providing sources for artifacts known and
proven compatible with the gem5 architecture simulator. These resources
are not necessary for the compilation or running of gem5, but may aid users
in producing certain simulations.

## Why gem5 Resources?

gem5 has been designed with flexibility in mind. Users may simulate a wide
variety of hardware, with an equally wide variety of workloads. However,
requiring users to find and configure workloads for gem5 (their own disk
images, their own OS boots, their own tests, etc.) is a significant
investment, and a hurdle to many.

The purpose of gem5 Resources is therefore __to provide a stable set of
commonly used resources, with proven and documented compatibility with gem5__.
In addition to this, gem5 resources also puts emphasis on __reproducibility
of experiments__ by providing citable, stable resources, tied to a particular
release of gem5.

## Where can I obtain the gem5 Resources?

To find a specific resource with the gem5 Resources, we recommend using the [gem5 Resources Website](https://resources.gem5.org). Detailed information on how searching, filtering and sorting works on this website is on this [help page](https://resources.gem5.org/help).

The gem5 Resources are hosted on our Google Cloud Bucket. Links to the
resources can be found [gem5 resources README.md file](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md).
The resource metadata is stored in a MongoDB database hosted on MongoDB Atlas.
To request updates to gem5 resources, create an issue or mail gem5-dev.

## Using a Resource from the gem5 Resources Website in gem5

When you find the Resource that you want to use in your simulation, navigate to the 'Usage' tab of that Resource.

For the purpose of this tutorial, let's assume that the Resource you are looking for is `riscv-hello`, found [here](https://resources.gem5.org/resources/riscv-hello).In the ['Usage'](https://resources.gem5.org/resources/riscv-hello/usage) tab of this Resource, you will find the code that can be pasted in a gem5 simulation to use this Resource.

In this case, the code is `obtain_resource(resource_id="riscv-hello")`.

To use the `obtain_resource` function, you require the following import statement:

```
from gem5.resources.resource import obtain_resource
```

The `obtain_resource` function accepts the following parameters:

- `resource_id`: The ID of the Resource you want to use.
- `resource_version`: An optional parameter that specifies the version of the Resource you want to use. If not specified, the latest version of the Resource compatible with the version of gem5 being used will be used.
- `clients`: An optional parameter that specifies the list of clients that gem5 would search for the Resource in. If not specified, gem5 will search for the Resource in all clients specified in the `src/python/gem5_default_config.py` file. By default, gem5 will use the public MongoDB metadata database to find resources. This can be overridden to specify your own local resource metadata.

## Using a Workload from the gem5 Resources Website in gem5

When you find the Workload that you want to use in your simulation, navigate to the 'Usage' tab of that Workload.

For the purpose of this tutorial, let's assume that the Workload you are looking for is `riscv-ubuntu-20.04-boot`, found [here](https://resources.gem5.org/resources/riscv-ubuntu-20.04-boot). In the ['Usage'](https://resources.gem5.org/resources/riscv-ubuntu-20.04-boot/usage) tab of this Workload, you will find the code that can be pasted in a gem5 simulation to use this Workload.

In this case, the code is `Workload("riscv-ubuntu-20.04-boot")`.

To use the `Workload` class, you require the following import statement:

```
from gem5.resources.workload import Workload
```

The `Workload` class accepts the following parameters:

- `workload_name`: The name of the Workload you want to use.
- `resource_directory`: An optional parameter that specifies where any resources should be download and accessed from.
- `resource_version`: An optional parameter that specifies the version of the Resource that should be used. If not specified, the latest version of the Resource compatible with the version of gem5 being used will be used.
- `clients`: An optional parameter that specifies a list of clients that gem5 would search for the Resource in. If not specified, gem5 will search for the Resource in all clients specified in the `src/python/gem5_default_config.py` file.

## Using a Custom Resource in gem5

To use a Custom Resource in gem5, we recommend using one of the supported data sources formats in gem5. Currently, we support MongoDB Atlas, local JSON files and remote JSON files.

You can use your own config file by overriding the `GEM5_DEFAULT_CONFIG` variable while running a file.

NOTE: Any Custom Resource you add must be compliant with the [gem5 Resources Schema](https://resources.gem5.org/gem5-resources-schema.json).

There is a utility in `utils/gem5-resources-manager` which provides a GUI for updating and creating resources for both the public resources (only modifiable by gem5 admins) and local resource metadata.
You can find more information on the gem5 Resources Manager in the README file.

## How do I obtain the gem5 Resource sources?

gem5 resources sources may be obtained from
<https://github.com/gem5/gem5-resources>:

```bash
git clone https://github.com/gem5/gem5-resources
```

The HEAD of the `stable` branch will point towards a set of resource sources
compatible with the latest release of gem5 (which can be obtained via
`git clone https://github.com/gem5/gem5.git`).

Please consult the [README.md](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md)
file for information on compiling individual gem5 resources. Where license
permits, the [README.md](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md)
file will provide a link to download the compiled resource from our
dist.gem5.org Google Cloud Bucket.

## How is gem5 Resources repository constructed?

The structure of this repository is as follows:

* **README.md** : This README will outline each resources, their origin,
how they have been modified to work with gem5 (if applicable), relevant
licensing information, and compilation instructions. This should be the first
port-of-call for those looking to use a gem5 resource.
* **src** : The resource sources. The gem5 resources can be found in this
directory. Each sub-directory outlines a resource. Each resource contains its
own README.md file documenting relevant information -- compilation
instructions, usage notes, etc.
* **CHANGELOG.md** : This CHANGELOG will outline the changes in a particular resource across its versions.

### Versioning

Each resource can have multiple versions. A version is in the form of
`<major>.<minor>.<patch>`. The versioning scheme is based on [Semantic
Versioning](https://semver.org/). Each version of a resource is linked to one
or more gem5 versions (e.g., v20.0, v20.1, v20.2, etc.).

By default, gem5 uses the latest version of a resource compatible with the
version of gem5 being used. However, users may specify a particular version
of a resource to use. If a user specifies a version of a resource that is not
compatible with the version of gem5 being used, gem5 will throw a warning.
You may still use the resource at your own risk.

### Citing a Resource

We strongly recommend gem5 Resources are cited in publications to aid in
replication of experiments, tutorials, etc.

To cite as a URL, please use the following formats:

```
# For the git repository at a particular revision:
https://github.com/gem5/gem5-resources/<revision>/src/<resource>

# For the git repository at a particular tag:
https://github.com/gem5/gem5-resources/tree/<branch>/src/<resource>
```

Alternatively, as BibTex:

```
@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://github.com/gem5/gem5-resources/<revision>/src/<resource>}},
  note = {Git repository at revision '<revision>'}
}

@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://github.com/gem5/gem5-resources/tree/<branch>/src/<resource>}},
  note = {Git repository at tag '<tag>'}
}
```

## How to I contribute to gem5 Resources?

Changes to the gem5 Resources repository are made to the develop branch via our
Gerrit code review system. Therefore, to make changes, first clone the
repository:

```
git clone https://github.com/gem5/gem5-resources.git
```

Then make changes and commit. When ready, push to Gerrit with:

```
git push origin HEAD:refs/for/stable
```

This will add resources to be used in the latest release of gem5.

To contribute resources to the next release of gem5,
```
git clone https://github.com/gem5/gem5-resources.git
git checkout --track origin/develop
```

Then make changes, commit, and push with:

```
git push origin HEAD:refs/for/develop
```

Commit message heads should not exceed 65 characters and start with the tag
`resources:`. The description after the header must not exceed 72 characters.

E.g.:

```
resources: Adding a new resources X

This is where the description of this commit will occur taking into
note the 72 character line limit.
```

We strongly advise contributors follow our [Style Guide](
/documentation/general_docs/development/coding_style/) where
possible and appropriate.

Any change will then be reviewed via our [Gerrit code review system](
https://gem5-review.googlesource.com). Once fully accepted and merged into
the gem5 resources repository, please contact Bobby R. Bruce
([bbruce@ucdavis.edu](mailto:bbruce@ucdavis.edu)) to have any compiled sources
uploaded to the gem5 resources bucket.


---


## Kconfig Build System

*Source: https://www.gem5.org/documentation/general_docs/kconfig_build_system/*

This guide is intended for advanced users who need to build gem5 (>=23.1) with
multiple ISAs or customize the build options, such as the Ruby memory protocol.
Familiarity with the Kconfig system is required.

## Build gem5 with the Kconfig Build System

```bash
scons [OPTIONS] Kconfig_command TARGET
```

Supported Kconfig commands include:

- `defconfig`
- `setconfig`
- `menuconfig`
- `guiconfig`
- `listnewconfig`
- `oldconfig`
- `olddefconfig`
- `savedefconfig`

The most common options are `defconfig`, `setconfig` and `menuconfig`.
Use can use `scons --help` to list these commands with additional information.

To build gem5 with Kconfig, there are now two steps.
The first is the initial configuration, which sets up a build directory with
the desired configuration. The second is building the target.
this is done with the `defconfig` command.
For example:

```bash
scons defconfig gem5_build build_opts/ALL
```

This will create a configuration in  `gem5_build` build directory based on
that specified in`build_opts/ALL`. The exact path of this configuration is
stored in `gem5_build/gem5.build/config`.

The second step is to build the target in the configured build directory.
This is done with `scons` as usual.
For example:


```bash
scons -j$(nproc) gem5_build/gem5.opt
```

Note: In order to maintain backward compatibility with the old build scheme,
users need to avoid using the "build" directory for Kconfig builds.

To build gem5 Kconfig with customized Kconfig options, an additional step
is required between **initial configuration** and **building the target**.

This step is to set up the Kconfig options in the configured build directory.
There are two ways to set up the Kconfig options.
The first is to directly set the Kconfig options in the command line with the
`setconfig` command. For example:

```bash
scons setconfig gem5_build USE_KVM=y
```

This will set the `USE_KVM` option to `y` in the configuration, thus enabling
KVM support.

The second way is to use the `menuconfig` command to open the menuconfig
editor.
The menuconfig editor allows you to view and edit config values and view help.
For example:

```bash

```bash
scons menuconfig gem5_build
```

## Details of Kconfig Commands

### defconfig

The `defconfig` command sets up a config using values specified in a defconfig file, or if no value is
given, uses the default values. The second argument specifies the defconfig file. All
default gem5 defconfig files are located in the build_opts directory. Users
can also use their own defconfig files.

For example:

```bash
scons defconfig gem5_build build_opts/RISCV
```

To use your own defconfig file:

```bash
scons defconfig gem5_build $HOME/foo/bar/myconfig
```

### setconfig

The `setconfig` command sets values in an existing config directory as specified on the command line.

The users or developers can get the Kconfig options via `menuconfig` or
`guiconfig`.

For example, to enable gem5 is built in systemc kernel:

```bash
scons setconfig gem5_build USE_SYSTEMC=y
```

### menuconfig

The `menuconfig` command opens the menuconfig editor.
This editor allows you to view and edit config values
and view help text. `menuconfig` runs in the CLI.

```bash
scons menuconfig gem5_build
```

If is successful, the CLI will look like this:

![](/assets/img/kconfig/menuconfig.png)

The user can use the arrow keys to navigate the menu, and the enter key to
select a menu item. The user can also use the space bar to select or deselect
an option. The user can also use the search function to find a specific
option. The user can also use the `?` key to view help text for a specific
option.
Below is a screenshot of the help text for the `USE_ARM_ISA` option:

![](/assets/img/kconfig/menuconfig_details.png)

If the `gem5_build` directory does not exist, SCons will set up a build
directory at the path `gem5_build` with default options and then invoke
menuconfig so you can set up its configuration.

### guiconfig

The `guiconfig` command opens the guiconfig editor.
This editor will let you view and edit config values,
and view help text. guiconfig runs as a graphical application. The command
requires `python3-tk` package be installed in the system.

```bash
scons guiconfig gem5_build
```

If is successful, it will create new windows to show up like:

![](/assets/img/kconfig/guiconfig.png)


### savedefconfig

Te=he `savedefconfig` command saves the current configuration to a defconfig.
You can use menuconfig to set up a
configuration with the options you care about, and then use `savedefconfig` to
create a minimal configuration file. These files are suitable for use in the
build_opts directory. The second argument specifies the filename for the new
defconfig file.

A saved defconfig is a good way to see what
options have been set to something interesting, and an easier way to
pass a config to someone else to use, to put in bug reports, etc.

```bash
scons savedefconfig gem5_build new_def_config
```

### listnewconfig

The `listnewconfig` command lists which option settings are new in the Kconfig and which are not currently
set in the existing config file.

```bash
scons listnewconfig gem5_build
```

### oldconfig

The `oldconfig` command updates the existing config setting new values for the desired options. This is
similar to `olddefconfig` except it asks what values you want
for the new settings.

```bash
scons oldconfig gem5_build
```

### oldsaveconfig

The `oldsaveconfig` command updates an existing config by setting new values for the desired options. This is
similar to the `oldconfig` option, except it uses the default for any new
setting.

```bash
scons oldsaveconfig gem5_build
```

Users can get help by running `scons -h` to get details of Kconfig commands.

## Report a Bug

If an issue is encountered we recommend you report the issue by saving the
configuration used and distributing it.
To do so, the `savedefconfig` command can be used:

```bash
scons savedefconfig gem5_build new_config
```

Alternatively, the configuration can be found in the
`gem5_build/gem5.build/config` file.


# Reference

1. Kconfig website: https://www.kernel.org/doc/html/next/kbuild/kconfig-language.html


---


## Setting Up and Using KVM on your machine

*Source: https://www.gem5.org/documentation/general_docs/using_kvm/*

Kernel-based Virtual Machine (KVM) is a Linux kernel module allowing creating a virtual machine managed by the kernel.
On recent x86 and ARM processors, KVM supports hardware-assisted virtualization, enabling running the virtual machine at close to native speed.
gem5's `KVMCPU` enables this feature in gem5, with the trade-offs being architectual statistics are not being recorded by gem5.
Some statistics can be optionally gathered via `perf` when using `KVMCPU`, but this option requires `root` permission.

In order to use gem5's `KVMCPU` to fast-forward your simulation, you must have a KVM compatible processor and have KVM installed on your machine.
This page will guide you through the process of enabling KVM on your machine and using it with gem5.

Note: The following tutorial assumes an X86 Linux host machine.
Various parts of this tutorial may not be applicable to other architectures or different operating systems.
At present KVM support is available for X86 and ARM simulations (with respective X86 and ARM hosts).

## Ensuring system compatibility

In order to see if your processor supports hardware virtualization, run the following command:

```console
grep -E -c '(vmx|svm)' /proc/cpuinfo
```

If the command returns 0, your processor does not support hardware virtualization.
If the command returns 1 or more, your processor does support hardware virtualization

You may still have to ensure it is enabled in your bios.
The processes for doing so varies from depending on manufacturer and model.
Please consult your motherboard's manual for more information on this.

Finally, it is recommended that you use a 64-bit kernel on your host machine.
The limitations of using a 32-bit kernel on your host machine are as follows:

* You can only allocate 2GB of memory for your VMs
* You can only create 32-bit VMs.

This can severely limit the usefulness of KVM in for gem5 simulations.

## Enabling KVM

For KVM to function directly with gem5, the following dependencies must be installed:

```console
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
```

Next, you need to add your user to the `kvm` and `libvirt` groups.
Run the two commands below:

```console
sudo adduser `id -un` libvirt
sudo adduser `id -un` kvm
```

After this, you need to leave then re-connect to your account.
If you are using SSH, disconnect all your session and login again.
Now if you run the `groups` command below you should see `kvm` and `libvirt`.

## Proving KVM is working

The "configs/example/gem5_library/x86-ubuntu-run-with-kvm.py" file is a gem5 configuration that will create a simulation which boots a Ubuntu 24.04 image using KVM.
It can be executed with the following:

```console
scons build/ALL/gem5.opt -j`nproc`
./build/ALL/gem5.opt configs/example/gem5_library/x86-ubuntu-run-with-kvm.py
```

If you are using a pre-built gem5 binary, use the following command:

```console
gem5 configs/example/gem5_library/x86-ubuntu-run-with-kvm.py

```

If the simulation runs successfully, you have successfully installed KVM and can use it with gem5.

## `KVMCPU`, fast-forwarding, and `perf`

`perf` is a feature in Linux allowing users to access performance counters.
By default, `perf` is enabled by `KVMCPU` to collect statistics, such as the number of executed instructions.
Typically, `perf` requires some system privileges to setup.
Otherwise, you'll see related permission issues, such as `kernel.perf_event_paranoid` value is too high.

However, if you'd like to fast-forward the simulation and do not intent to collect the statistics of the fast-forwarded phase, you can choose not to use `perf` when using `KVMCPU`.
The `KVMCPU` SimObject has a parameter called `usePerf`, which specifies if the `KVMCPU` should collect statistics using `perf`.
This option is enabled by default.

The following is an example of turning `perf` off,
[https://github.com/gem5/gem5/blob/stable/configs/example/gem5\_library/x86-ubuntu-run-with-kvm-no-perf.py](https://github.com/gem5/gem5/blob/stable/configs/example/gem5_library/x86-ubuntu-run-with-kvm-no-perf.py).


---


## M5ops

*Source: https://www.gem5.org/documentation/general_docs/m5ops/*

# M5ops

This page explains the special opcodes that can be used in M5 to do checkpoints etc. The m5 utility program (on our disk image and in util/m5/*) provides some of this functionality on the command line. In many cases it is best to insert the operation directly in the source code of your application of interest. You should be able to link with the appropriate libm5.a file and the m5ops.h header file has prototypes for all the functions.
A tutorial on using the M5ops was given as a part of the gem5 2022 Bootcamp. A recording of this event can be found [here](https://youtu.be/TeHKMVOWUAY).

## Building M5 and libm5

In order to build m5 and libm5.a for your target ISA, run the following command in the util/m5/ directory.

```bash
scons build/{TARGET_ISA}/out/m5
```

The list of target ISAs is shown below.

* x86
* arm (arm-linux-gnueabihf-gcc)
* thumb (arm-linux-gnueabihf-gcc)
* sparc (sparc64-linux-gnu-gcc)
* arm64 (aarch64-linux-gnu-gcc)
* riscv (riscv64-unknown-linux-gnu-gcc)

Note if you are using a x86 system for other ISAs you need to have the cross-compiler installed. The name of the cross-compiler is shown inside the parentheses in the list above.

See [util/m5/README.md](https://github.com/gem5/gem5/blob/stable/util/m5/README.md) for more details.

## The m5 Utility (FS mode)

The m5 utility (see util/m5/) can be used in FS mode to issue special instructions to trigger simulation specific functionality. It currently offers the following options:

* initparam: Deprecated, present only for old binary compatibility
* exit [delay]: Stop the simulation in delay nanoseconds.
* resetstats [delay [period]]: Reset simulation statistics in delay nanoseconds; repeat this every period nanoseconds.
* dumpstats [delay [period]]: Save simulation statistics to a file in delay nanoseconds; repeat this every period nanoseconds.
* dumpresetstats [delay [period]]: same as dumpstats; resetstats
* checkpoint [delay [period]]: Create a checkpoint in delay nanoseconds; repeat this every period nanoseconds.
* readfile: Print the file specified by the config parameter system.readfile. This is how the the rcS files are copied into the simulation environment.
* debugbreak: Call debug_break() in the simulator (causes simulator to get SIGTRAP signal, useful if debugging with GDB).
* switchcpu: Cause an exit event of type, "switch cpu," allowing the Python to switch to a different CPU model if desired.
* workbegin: Cause an exit evet of type, "workbegin", that could be used to mark the begining of an ROI.
* workend: Cause an exit event of type, "workend", that could be used to mark the termination of an ROI.

## Other M5 ops

These are other M5 ops that aren't useful in command line form.

* quiesce: De-schedule the CPUs tick() call until some asynchronous event wakes it (an interrupt)
* quiesceNS: Same as above, but automatically wakes after a number of nanoseconds if it's not woken up prior
* quiesceCycles: Same as above but with CPU cycles instead of nanoseconds
* quisceTIme: The amount of time the CPU was quiesced for
* addsymbol: Add a symbol to the simulators symbol table. For example when a kernel module is loaded

## Using gem5 ops in Java code

These ops can also be used in Java code. These ops allow gem5 ops to be called from within java programs like the following:

```python
import jni.gem5Op;

public  class HelloWorld {

   public static void main(String[] args) {
       gem5Op gem5 = new gem5Op();
       System.out.println("Rpns0:" + gem5.rpns());
       System.out.println("Rpns1:" + gem5.rpns());
   }

   static {
       System.loadLibrary("gem5OpJni");
   }
}
```

When building you need to make sure classpath includes gem5OpJni.jar:

```javascript
javac -classpath $CLASSPATH:/path/to/gem5OpJni.jar HelloWorld.java
```

and when running you need to make sure both the java and library path are set:

```javascript
java -classpath $CLASSPATH:/path/to/gem5OpJni.jar -Djava.library.path=/path/to/libgem5OpJni.so HelloWorld
```

## Using gem5 ops with Fortran code

gem5's special opcodes (psuedo instructions) can be used with Fortran programs. In the Fortran code, one can add calls to C functions that invoke the special opcode. While creating the final binary, compile the object files for the Fortran program and the C program (for opcodes) together. I found the documentation provided [here](https://gcc.gnu.org/wiki/GFortranGettingStarted) useful. Read the section **-****- Compiling a mixed C-Fortran program**.

The idea of using gem5 ops with Fortran code is essentially to compile the m5 ops C code to an object file, and then link the object file against the binary calling the m5 ops.
The C function calling convention in Fortran is such that, if the function name in C code is `void foo_bar_(void)`, then in Fortran, you can call the function by `call foo_bar`.

## Linking M5 to your C/C++ code

In order to link m5 to your code, first build `libm5.a` as described in the section above.

Then

* Include `gem5/m5ops.h` in your source file(s)
* Add `gem5/include` to your compiler's include search path
* Add `gem5/util/m5/build/{TARGET_ISA}/out` to the linker search path
* Link against `libm5.a`

For example, this could be achieved by adding the following to your Makefile:

```
CFLAGS += -I$(GEM5_PATH)/include
LDFLAGS += -L$(GEM5_PATH)/util/m5/build/$(TARGET_ISA)/out -lm5
```

Here is a simple Makefile example:

```make
TARGET_ISA=x86

GEM5_HOME=$(realpath ./)
$(info   GEM5_HOME is $(GEM5_HOME))

CXX=g++

CFLAGS=-I$(GEM5_HOME)/include

LDFLAGS=-L$(GEM5_HOME)/util/m5/build/$(TARGET_ISA)/out -lm5

OBJECTS= hello_world

all: hello_world

hello_world:
	$(CXX) -o $(OBJECTS) hello_world.cpp $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(OBJECTS)
```


## Using the "_addr" version of M5ops

The "_addr" version of m5ops triggers the same simulation specific functionality as the default m5ops, but they use different trigger mechanisms. Below is a quote from the m5 utility README.md explaining the trigger mechanisms.

```markdown
The bare function name as defined in the header file will use the magic instruction based trigger mechanism, what would have historically been the default.

Some macros at the end of the header file will set up other declarations which mirror all of the other definitions, but with an “_addr” and “_semi” suffix. These other versions will trigger the same gem5 operations, but using the “magic” address or semihosting trigger mechanisms. While those functions will be unconditionally declared in the header file, a definition will exist in the library only if that trigger mechanism is supported for that ABI.
```

*Note*: The macros generating the "_addr" and "_semi" m5ops are called `M5OP`, which are defined in `util/m5/abi/*/m5op_addr.S` and `util/m5/abi/*/m5op_semi.S`.

In order to use the "_addr" version of m5ops, you need to include the m5_mmap.h header file, pass the "magic" address (e.g., "0xFFFF0000" for x86, and "0x10010000" for arm64/riscv) to m5op_addr, then call the map_m5_mem() to open /dev/mem. You can insert m5ops by adding "_addr" at the end of the original m5ops functions.

Here is a simple example using the "_addr" version of the m5ops:

```c
#include <gem5/m5ops.h>
#include <m5_mmap.h>
#include <stdio.h>

#define GEM5

int main(void) {
#ifdef GEM5
    m5op_addr = 0xFFFF0000;
    map_m5_mem();
    m5_work_begin_addr(0,0);
#endif

    printf("hello world!\n");

#ifdef GEM5
    m5_work_end_addr(0,0);
    unmap_m5_mem();
#endif
}
```

*Note*: You'll need to add a new header location for the compiler to find the `m5_mmap.h`.
If you are following the example Makefile above, you can add the following line below where CFLAGS is defined,

```c
CFLAGS += $(GEM5_PATH)/util/m5/src/
```

When you run the applications with m5ops inserted in FS mode with a KVM CPU, this error might appear.

    ```illegal instruction (core dumped)```

This is because m5ops instructions are not valid instructions to the host. Using the "_addr" version of the m5ops can fix this issue, so it is necessary to use the "_addr" version if you want to integrate m5ops into your applications or use the m5 binary utility when running with KVM CPUs.


---


## Moving Active Changes from Gerrit to GitHub

*Source: https://www.gem5.org/documentation/general_docs/moving_to_github/*

# Moving Active Changes from Gerrit to GitHub

As we transition to using GitHub to host the gem5 project, we need to have a way to move any active changes from Gerrit onto GitHub for review.  If your change won’t be ready to be merged by the time Gerrit becomes read-only, follow the steps below to create a pull request with your changes for review on GitHub.

* Go to https://github.com/gem5/gem5 and create a fork of the gem5 repository, making sure to uncheck the box “Copy the stable branch only”
* Once you create this fork, clone your forked repository, then run `git checkout --track origin/develop` so that your changes are on top of the develop branch
* Now that your forked repository is set up, navigate to https://gem5-review.googlesource.com/q/status:open+-is:wip and find your changes
* Once you’ve opened your change, click the “Download” button on the right side of the screen, and copy the command to cherry-pick your change
* Cherry pick your change to your forked repository, and handle any merge conflicts that may come up.  If these changes are part of a relation change, make sure to cherry pick every part of it.
* Once all changes are cherry picked, run `git push origin` to update your forked repository
* Now that all the changes are up, you can create a pull request. To do so, open your repository on https://github.com, and hit the Contribute button in the middle of the page.  Make sure you’re on the develop branch when doing so.  Once you hit Contribute, a button saying “Open pull request” should appear.
* This navigates you to a page to create a pull request.  For the base repository, it should be gem5/gem5, and the branch should be develop.  Any pull requests to the stable branch will be ignored.  The head repository will be your forked repository, and the branch should also be develop.  In the body of your pull request, you can include a link to your changes from Gerrit, so any comments can be easily accessible.  In addition, on the right hand side of the page, you can add reviewers, so you can request anyone that looked over your changes on Gerrit to review your pull request
* Once you’re happy with your pull request, you can hit the “Create pull request” button at the bottom of the page.

If you’re a first-time contributor to the gem5 GitHub repository, you will need a positive review of your pull request before any continuous integration tests can be run.  For your change to be merged, you need both the positive review, as well as for these tests to pass.  Finally a gem5 maintainer will squash and merge your changes once all prior checks pass.


---


## Power and Thermal Model

*Source: https://www.gem5.org/documentation/general_docs/thermal_model*

# Power and Thermal Model

This document gives an overview of the power and thermal modelling
infrastructure in Gem5.

The purpose is to give a high level view of all the pieces involved and how
they interact with each other and the simulator.

## Class overview

Classes involved in the power model are:

* [PowerModel](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalResistor.html):
Represents a power model for a hardware component.
* [PowerModelState](
http://doxygen.gem5.org/release/current/classgem5_1_1PowerModelState.html): Represents a
power model for a hardware component in a certain power state. It is an
abstract class that defines an interface that must be implemented for each
model.
* [MathExprPowerModel](
http://doxygen.gem5.org/release/current/classgem5_1_1MathExprPowerModel.html): Simple
implementation of [PowerModelState](
http://doxygen.gem5.org/release/current/classgem5_1_1PowerModelState.html) that assumes
that power can be modeled using a simple power.

Classes involved in the thermal model are:

* [ThermalModel](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalModel.html):
Contains the system thermal model logic and state. It performs the power query
and temperature update. It also enables gem5 to query for temperature (for OS
reporting).
* [ThermalDomain](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalDomain.html):
Represents an entity that generates heat. It's essentially a group of
[SimObjects](http://doxygen.gem5.org/release/current/classgem5_1_1SubSystem.html) grouped
under a SubSystem component that have its own thermal behaviour.
* [ThermalNode](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalNode.html):
Represents a node in the thermal circuital equivalent. The node has a
temperature and interacts with other nodes through connections (thermal
resistors and capacitors).
* [ThermalReference](
http://doxygen.gem5.org/release/current/classgem5_1_1ThermalReference.html): Temperature
reference for the thermal model (essentially a thermal node with a fixed
temperature), can be used to model air or any other constant temperature
domains.
* [ThermalEntity](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalEntity.html):
A thermal component that connects two thermal nodes and models a thermal
impedance between them. This class is just an abstract interface.
* [ThermalResistor](
http://doxygen.gem5.org/release/current/classgem5_1_1ThermalResistor.html): Implements
[ThermalEntity](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalEntity.html) to
model a thermal resistance between the two nodes it connects. Thermal
resistances model the capacity of a material to transfer heat (units in K/W).
* [ThermalCapacitor](
http://doxygen.gem5.org/release/current/classgem5_1_1ThermalCapacitor.html): Implements
[ThermalEntity](http://doxygen.gem5.org/release/current/classgem5_1_1ThermalEntity.html) to
model a thermal capacitance. Thermal capacitors are used to model material's
thermal capacitance, this is, the ability to change a certain material
temperature (units in J/K).

## Thermal model

The thermal model works by creating a circuital equivalent of the simulated
platform. Each node in the circuit has a temperature (as voltage equivalent)
and power flows between nodes (as current in a circuit).

To build this equivalent temperature model the platform is required to group
the power actors (any component that has a power model) under SubSystems and
attach ThermalDomains to those subsystems. Other components might also be
created (like ThermalReferences) and connected all together by creating thermal
entities (capacitors and resistors).

Last step to conclude the thermal model is to create the [ThermalModel](
http://doxygen.gem5.org/release/current/classgem5_1_1ThermalModel.html) instance itself and
attach all the instances used to it, so it can properly update them at runtime.
Only one thermal model instance is supported right now and it will
automatically report temperature when appropriate (ie. platform sensor
devices).

## Power model

Every [ClockedObject](
http://doxygen.gem5.org/release/current/classgem5_1_1ClockedObject.html) has a power model
associated. If this power model is non-null power will be calculated at every
stats dump (although it might be possible to force power evaluation at any
other point, if the power model uses the stats, it is a good idea to keep both
events in sync). The definition of a power model is quite vague in the sense
that it is as flexible as users want it to be. The only enforced contraints so
far is the fact that a power model has several power state models, one for each
possible power state for that hardware block. When it comes to compute power
consumption the power is just the weighted average of each power model.

A power state model is essentially an interface that allows us to define two
power functions for dynamic and static. As an example implementation a class
called [MathExprPowerModel](
http://doxygen.gem5.org/release/current/classgem5_1_1MathExprPowerModel.html) has been
provided. This implementation allows the user to define a power model as an
equation involving several statistics. There's also some automatic (or "magic")
variables such as "temp", which reports temperature.


---


## "Architecture Support"

*Source: https://www.gem5.org/documentation/general_docs/architecture_support/*

# Architecture Support

{: .outdated-notice}
The information and hyperlinks in this page may not be accurate.

## Alpha

Gem5 models a DEC Tsunami based system.
In addition to the normal Tsunami system that support 4 cores, we have an extension which supports 64 cores (a custom PALcode and patched Linux kernel is required).
The simulated system looks like an Alpha 21264 including the BWX, MVI, FIX, and CIX to user level code.
For historical reasons the processor executes EV5 based PALcode.

It can boot unmodified Linux 2.4/2.6, FreeBSD, or L4Ka::Pistachio as well as applications in syscall emulation mode.
Many years ago it was possible to boot HP/Compaq's Tru64 5.1 operating system.
We no longer actively maintain that capability, however, and it does not currently work.

## ARM

The ARM Architecture models within gem5 support an [ARMv8-A](https://developer.arm.com/docs/den0024/latest/armv8-a-architecture-and-processors/armv8-a) profile of the ARM® architecture with multi-processor extensions.
This includes both AArch32 and AArch64 state.
In AArch32, this include support for [Thumb®](https://www.embedded.com/introduction-to-arm-thumb/), Thumb-2, VFPv3 (32 double register variant) and [NEON™](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon), and Large Physical Address Extensions (LPAE).
Optional features of the architecture that are not currently supported are [TrustZone®](https://developer.arm.com/ip-products/security-ip/trustzone), ThumbEE, [Jazelle®](https://en.wikipedia.org/wiki/Jazelle), and [Virtualization](https://developer.arm.com/docs/100942/0100/aarch64-virtualization).

In full system mode gem5 is able to boot uni- or multi-processor Linux and bare metal applications built with ARM's compilers.
Newer Linux versions work out of the box (if used with gem5's DTBs) we also provide gem5-specific Linux kernels with custom configurations and custom drivers Additionally, statically linked Linux binaries can be run in ARM's syscall emulation mode.

## POWER

Support for the POWER ISA within gem5 is currently limited to syscall emulation only and is based on the [POWER ISA v3.0B](https://ftp.libre-soc.org/PowerISA_public.v3.0B.pdf).
A big-endian, 32-bit processor is modeled.
Most common instructions are available (enough to run all the SPEC CPU2000 integer benchmarks).
Floating point instructions are available but support may be patchy.
In particular, the Floating-Point Status and Control Register (FPSCR) is generally not updated at all.
There is no support for vector instructions.

Full system support for POWER would require a significant amount of effort and is not currently being developed.
However, if there is interest in pursuing this, a set of patches-in-progress that make a start towards this can be obtained from [Tim](mailto:timothy.jones@cl.cam.ac.uk).

## SPARC

The gem5 simulator models a single core of a UltraSPARC T1 processor (UltraSPARC Architecture 2005).

It can boot Solaris like the Sun T1 Architecture simulator tools do (building the hypervisor with specific defines and using the HSMID virtual disk driver).
Multiprocessor support was never completed for full-system SPARC.
With syscall emulation gem5 supports running Linux or Solaris binaries.
New versions of Solaris no longer support generating statically compiled binaries which gem5 requires.

## x86

X86 support within the gem5 simulator includes a generic x86 CPU with 64 bit extensions, more similar to AMD's version of the architecture than Intel's but not strictly like either.
Unmodified versions of the Linux kernel can be booted in UP and SMP configurations, and patches are available for speeding up boot.
SSE and 3dnow are implemented, but the majority of x87 floating point is not.
Most effort has been focused on 64 bit mode, but compatibility mode and legacy modes have some support as well.
Real mode works enough to bootstrap an AP, but hasn't been extensively tested.
The features of the architecture that are exercised by Linux and standard Linux binaries are implemented and should work, but other areas may not.
64 and 32 bit Linux binaries are supported in syscall emulation mode.

## MIPS


## RISC-V


---


## "ARM implementation"

*Source: https://www.gem5.org/documentation/general_docs/architecture_support/arm_implementation/*

# ARM Implementation

## Supported features and modes

The ARM Architecture models within gem5 support an [ARMv8.0-A](https://developer.arm.com/docs/den0024/latest/armv8-a-architecture-and-processors/armv8-a) profile of the ARM® architecture with multi-processor extensions.
This includes both AArch32 and AArch64 state at all ELs. This basically means supporting:

* [EL2: Virtualization](https://developer.arm.com/docs/100942/0100/aarch64-virtualization)
* [EL3: TrustZone®](https://developer.arm.com/ip-products/security-ip/trustzone)

The baseline model is ARMv8.0 compliant, we also support some mandatory/optional ARMv8.x features (with x > 0)

### From gem5 v21.2

The best way to get a synced version of Arm architectural features is to have a look at the [ArmExtension](https://github.com/gem5/gem5/blob/develop/src/arch/arm/ArmSystem.py) enum
used by the release object and the available example releases provided within the same file.

A user can choose one of the following options:

* Use the default release
* Use another example release (e.g. Armv82)
* Generate a custom release from the available ArmExtension enum values

### Before gem5 v21.2

The best way to get a synced version of Arm architectural features is to have a look at Arm ID registers and boolean values:

* [src/arch/arm/ArmISA.py](https://github.com/gem5/gem5/blob/v21.1.0.2/src/arch/arm/ArmISA.py)
* [src/arch/arm/ArmSystem.py](https://github.com/gem5/gem5/blob/v21.1.0.2/src/arch/arm/ArmSystem.py)


---


## ISA Parser

*Source: https://www.gem5.orgdocumentation/general_docs/architecture_support/isa_parser/*

# ISA Parser

The gem5 ISA description language is a custom language designed specifically for generating the class definitions and decoder function needed by gem5. This section provides a practical, informal overview of the language itself. A formal grammar for the language is embedded in the "yacc" portion of the parser (look for the functions starting with p\_ in isa\_parser.py). A second major component of the parser processes C-like code specifications to extract instruction characteristics; this aspect is covered in the section [Code parsing](#code-parsing).
At the highest level, an ISA description file is divided into two parts: a declarations section and a decode section. The decode section specifies the structure of the decoder and defines the specific instructions returned by the decoder. The declarations section defines the global information (classes, instruction formats, templates, etc.) required to support the decoder. Because the decode section is the focus of the description file, we will begin the discussion there.

## The decode section

The decode section of the description is a set of nested decode blocks. A decode block specifies a field of a machine instruction to decode and the result to be provided for particular values of that field. A decode block is similar to a C switch statement in both syntax and semantics. In fact, each decode block in the description file generates a switch statement in the resulting decode function.
Let's begin with a (slightly oversimplified) example:

{% raw %}
```
decode OPCODE {
  0: add({{ Rc = Ra + Rb; }});
  1: sub({{ Rc = Ra - Rb; }});
}
```
{% endraw %}

A decode block begins with the keyword `decode` followed by the name of the instruction field to decode. The latter must be defined in the declarations section of the file using a bitfield definition (see [Bitfield definitions](#bitfield-definitions)). The remainder of the decode block is a list of statements enclosed in braces. The most common statement is an integer constant and a colon followed by an instruction definition. This statement corresponds to a 'case' statement in a C switch (but note that the 'case' keyword is omitted for brevity). A comma-separated list of integer constants may be used to allow a single decode statement to apply to any of a set of bitfield values.

{% raw %}
Instruction definitions are similar in syntax to C function calls, with the instruction mnemonic taking the place of the function name. The comma-separated arguments are used when processing the instruction definition. In the example above, the instruction definitions each take a single argument, a ''code literal''. A code literal is operationally similar to a string constant, but is delimited by double braces (`{{` and `}}`). Code literals may span multiple lines without escaping the end-of-line characters. No backslash escape processing is performed (e.g., `\t` is taken literally, and does not produce a tab). The delimiters were chosen so that C-like code contained in a code literal would be formatted nicely by emacs C-mode.
{% endraw %}

A decode statement may specify a nested decode block in place of an instruction definition. In this case, if the bitfield specified by the outer block matches the given value(s), the bitfield specified by the inner block is examined and an additional switch is performed.

It is also legal, as in C, to use the keyword `default` in place of an integer constant to define a default action. However, it is more common to use the decode-block default syntax discussed in the section [Decode block defaults](#decode-block-defaults) below.

### Specifying instruction formats

When the ISA description file is processed, each instruction definition does in fact invoke a function call to generate the appropriate C++ code for the decode file. The function that is invoked is determined by the instruction format. The instruction format determines the number and type of the arguments given to the instruction definition, and how they are processed to generate the corresponding output. Note that the term "instruction format" as used in this context refers solely to one of these definition-processing functions, and does not necessarily map one-to-one to the machine instruction formats defined by the ISA.
The one oversimplification in the previous example is that no instruction format was specified. As a result, the parser does not know how to process the instruction definitions.

Instruction formats can be specified in two ways. An explicit format specification can be given before the mnemonic, separated by a double colon (::), as follows:


{% raw %}
```
decode OPCODE {
  0: Integer::add({{ Rc = Ra + Rb; }});
  1: Integer::sub({{ Rc = Ra - Rb; }});
}
```
{% endraw %}

In this example, both instruction definitions will be processed using the format Integer. A more common approach specifies the format for a set of definitions using a format block, as follows:

{% raw %}
```
decode OPCODE {
  format Integer {
    0: add({{ Rc = Ra + Rb; }});
    1: sub({{ Rc = Ra - Rb; }});
  }
}
```
{% endraw %}

In this example, the format "Integer" applies to all of the instruction definitions within the inner braces. The two examples are thus functionally equivalent. There are few restrictions on the use of format blocks. A format block may include only a subset of the statements in a decode block. Format blocks and explicit format specifications may be mixed freely, with the latter taking precedence. Format and decode blocks can be nested within each other arbitrarily. Note that a closing brace will always bind with the nearest format or decode block, making it syntactically impossible to generate format or decode blocks that do not nest fully inside the enclosing block.

At any point where an instruction definition occurs without an explicit format specification, the format associated with the innermost enclosing format block will be used. If a definition occurs with no explicit format and no enclosing format block, a runtime error will be raised.

### Decode block defaults

Default cases for decode blocks can be specified by `default:` labels, as in C switch statements. However, it is common in ISA descriptions that unspecified cases correspond to unknown or illegal instruction encodings. To avoid the requirement of a `default:` case in every decode block, the language allows an alternate default syntax that specifies a default case for the current decode block and any nested decode block with no explicit default. This alternate default is specified by giving the `default` keyword and an instruction definition after the bitfield specification (prior to the opening brace). Specifying the outermost decode block as follows:

```
decode OPCODE default Unknown::unknown() {
   [...]
}
```

is thus (nearly) equivalent to adding `default: Unknown::unknown();` inside every decode block that does not otherwise specify a default case.

_Note: The appropriate format definition (see _[Format definitions](#format-definitions)_) is invoked each time an instruction definition is encountered.  Thus there is a semantic difference between having a single block-level default and a default within each nested block, which is that the former will invoke the format definition once, while the latter could result in multiple invocations of the format definition.  If the format definition generates header, decoder, or exec output, then that output will be included multiple times in the corresponding files, which typically leads to multiple definition errors when the C++ gets compiled.  If it is absolutely necessary to invoke the format definition for a single instruction multiple times, the format definition should be written to produce _only_ decode-block output, and all needed header, decoder, and exec output should be produced once using_ `output` _blocks (see _[Output blocks](#output-blocks])_)._

### Preprocessor directive handling

The decode block may also contain C preprocessor directives. These directives are not processed by the parser; instead, they are passed through to the C++ output to be processed when the C++ decoder is compiled. The parser does not recognize any specific directives; any line with a # in the first column is treated as a preprocessor directive.
The directives are copied to all of the output streams (the header, the decoder, and the execute files; see [Format definitions](#format-definitions). The directives maintain their position relative to the code generated by the instruction definitions within the decode block. The net result is that, for example, #ifdef/#endif pairs that surround a set of instruction definitions will enclose both the declarations generated by those definitions and the corresponding case statements within the decode function. Thus #ifdef and similar constructs can be used to delineate instruction definitions that will be conditionally compiled into the simulator based on preprocessor symbols (e.g., FULL\_SYSTEM). It should be emphasized that #ifdef does not affect the ISA description parser. In an #ifdef/#else/#endif construct, all of the instruction definitions in both parts of the conditional will be processed. Only during the subsequent C++ compilation of the decoder will one or the other set of definitions be selected.

## The declaration section

As mentioned above, the decode section of the ISA description (consisting of a single outer decode block) is preceded by the declarations section. The primary purpose of the declarations section is to define the instruction formats and other supporting elements that will be used in the decode block, as well as supporting C++ code that is passed almost verbatim to the generated output.
This section describes the components that appear in the declaration section: [Format definitions](#format-definitions), [Template definitions](#template-definitions), [Output blocks](#output-blocks), [Let blocks](#let-blocks), [Bitfield definitions](#bitfield-definitions), [Operand and operand type definitions](#operand-and-operand-type-definitions), and [Namespace declaration](#namespace-declaration).

### Format definitions

An instruction format is basically a Python function that takes the arguments supplied by an instruction definition (found inside a decode block) and generates up to four pieces of C++ code. The pieces of C++ code are distinguished by where they appear in the generated output.
 1. The ''header output'' goes in the header file (decoder.hh) that is included in all the generated source files (decoder.cc and all the per-CPU-model execute .cc files). The header output typically contains the C++ class declaration(s) (if any) that correspond to the instruction.
 2. The ''decoder output'' goes before the decode function in the same source file (decoder.cc). This output typically contains definitions that do not need to be visible to the `execute()` methods: inline constructor definitions, non-inline method definitions (e.g., for disassembly), etc.
 3. The ''exec output'' contains per-CPU model definitions, i.e., the `execute()` methods for the instruction class.
 4. The ''decode block'' contains a statement or block of statements that go into the decode function (in the body of the corresponding case statement). These statements take control once the bit pattern specified by the decode block is recognized, and are responsible for returning an appropriate instruction object.

The syntax for defining an instruction format is as follows:

{% raw %}
```
def format FormatName(arg1, arg2) {{
    [code omitted]
}};
```
{% endraw %}

In this example, the format is named "FormatName". (By convention, instruction format names begin with a capital letter and use mixed case.) Instruction definitions using this format will be expected to provide two arguments (`arg1` and `arg2`). The language also supports the Python variable-argument mechanism: if the final parameter begins with an asterisk (e.g., `*rest`), it receives a list of all the otherwise unbound arguments from the call site.

Note that the next-to-last syntactic token in the format definition (prior to the semicolon) is simply a code literal (string constant), as described above. In this case, the text within the code literal is a Python code block. This Python code will be called at each instruction definition that uses the specified format.

In addition to the explicit arguments, the Python code is supplied with two additional parameters: `name`, which is bound to the instruction mnemonic, and `Name`, which is the mnemonic with the first letter capitalized (useful for forming C++ class names based on the mnemonic).

The format code block specifies the generated code by assigning strings to four special variables: `header_output`, `decoder_output`, `exec_output`, and `decode_block`. Assignment is optional; for any of these variables that does not receive a value, no code will be generated for the corresponding section. These strings may be generated by whatever method is convenient. In practice, nearly all instruction formats use the support functions provided by the ISA description parser to specialize code templates based on characteristics extracted automatically from C-like code snippets. Discussion of these features is deferred to the [Code parsing](#code-parsing) page.

Although the ISA description is completely independent of any specific simulator CPU model, some C++ code (particularly the exec output) must be specialized slightly for each model. This specialization is handled by automatic substitution of CPU-model-specific symbols. These symbols start with `CPU_` and are treated specially by the parser. Currently there is only one model-specific symbol, `CPU_exec_context`, which evaluates to the model's execution context class name. As with templates (see [Template definitions](#template-definitions)), references to CPU-specific symbols use Python key-based format strings; a reference to the `CPU_exec_context` symbol thus appears in a string as `%(CPU_exec_context)s`.

If a string assigned to `header_output`, `decoder_output`, or `decode_block` contains a CPU-specific symbol reference, the string is replicated once for each CPU model, and each instance has its CPU-specific symbols substituted according to that model. The resulting strings are then concatenated to form the final output. Strings assigned to `exec_output` are always replicated and subsituted once for each CPU model, regardless of whether they contain CPU-specific symbol references. The instances are not concatenated, but are tracked separately, and are placed in separate per-CPU-model files (e.g., simple\_cpu\_exec.cc).

### Template definitions

As discussed in section Format definitions above, the purpose of an instruction format is to process the arguments of an instruction definition and generate several pieces of C++ code. These code pieces are usually generated by specializing a code template. The description language provides a simple syntax for defining these templates: the keywords `def template`, the template name, the template body (a code literal), and a semicolon. By convention, template names start with a capital letter, use mixed case, and end with "Declare" (for declaration (header output) templates), "Decode" (for decode-block templates), "Constructor" (for decoder output templates), or "Execute" (for exec output templates).
For example, the simplest useful decode template is as follows:

{% raw %}
```
def template BasicDecode {{
    return new %(class_name)s(machInst);
}};
```
{% endraw %}

An instruction format would specialize this template for a particular instruction by substituting the actual class name for `%(class_name)s`. (Template specialization relies on the Python string format operator `%`. The term `%(class_name)s` is an extension of the C `%s` format string indicating that the value of the symbol `class_name` should be substituted.) The resulting code would then cause the C++ decode function to create a new object of the specified class when the particular instruction was recognized.

Templates are represented in the parser as Python objects. A template is used to generate a string typically by calling the template object's `subst()` method. This method takes a single argument that specifies the mapping of substitution symbols in the template (e.g., `%(class_name)s`) to specific values. If the argument is a dictionary, the dictionary itself specifies the mapping. Otherwise, the argument must be another Python object, and the object's attributes are used as the mapping. In practice, the argument to `subst()` is nearly always an instance of the parser's InstObjParams class; see the [InstObjParams class](#the-instobjparams-class). A template may also reference other templates (e.g., `%(BasicDecode)s`) in addition to symbols specified by the `subst()` argument; these will be interpolated into the result by `subst()` as well.

Template references to CPU-model-specific symbols (see [Format definitions](#format-definitions)) are not expanded by `subst()`, but are passed through intact. This feature allows them to later be expanded appropriately according to whether the result is assigned to `exec_output` or another output section. However, when a template containing a CPU-model-specific symbol is referenced by another template, then the former template is replicated and expanded into a single string before interpolation, as with templates assigned to `header_output` or `decoder_output`. This policy guarantees that only templates directly containing CPU-model-specific symbols will be replicated, never templates that contain such symbols indirectly. This last feature is used to interpolate per-CPU declarations of the `execute()` method into the instruction class declaration template (see the `BasicExecDeclare` template in the Alpha ISA description).

### Output blocks

Output blocks allow the ISA description to include C++ code that is copied nearly verbatim to the output file. These blocks are useful for defining classes and local functions that are shared among multiple instruction objects. An output block has the following format:

{% raw %}
```
output <destination> {{
    [code omitted]
}};
```
{% endraw %}

The `<destination>` keyword must be one of `header`, `decoder`, or `exec`. The code within the code literal is treated as if it were assigned to the `header_output` `decoder_output`, or `exec_output` variable within an instruction format, respectively, including the special processing of CPU-model-specific symbols. The only additional processing performed on the code literal is substitution of bitfield operators, as used in instruction definitions (see [Bitfield operators](#bitfield-operators), and interpolation of references to templates.

### Let blocks

Let blocks provide for global Python code. These blocks consist simply of the keyword `let` followed by a code literal (double-brace delimited string) and a semicolon.
The code literal is executed immediately by the Python interpreter. The parser maintains the execution context across let blocks, so that variables and functions defined in one let block will be accessible in subsequent let blocks. This context is also used when executing instruction format definitions. The primary purpose of let blocks is to define shared Python data structures and functions for use in instruction formats. The parser exports a limited set of definitions into this execution context, including the set of defined templates (see [Template definitions](#template-definitions), the `InstObjParams` and `CodeBlock` classes (see [Code parsing](#code-parsing)), and the standard Python `string` and `re` (regular expression) modules.

### Bitfield definitions

A bitfield definition provides a name for a bitfield within a machine instruction. These names are typically used as the bitfield specifications in decode blocks. The names are also used within other C++ code in the decoder file, including instruction class definitions and decode code.
The bitfield definition syntax is demonstrated in these examples:

```
def bitfield OPCODE <31:26>;
def bitfield IMM <12>;
def signed bitfield MEMDISP <15:0>;
```

The specified bit range is inclusive on both ends, and bit 0 is the least significant bit; thus the OPCODE bitfield in the example extracts the most significant six bits from a 32-bit instruction. A single index value extracts a one-bit field, IMM. The extracted value is zero-extended by default; with the additional signed keyword, as in the MEMDISP example, the extracted value will be sign extended. The implementation of bitfields is based on preprocessor macros and C++ template functions, so the size of the resulting value will depend on the context.

To fully understand where bitfield definitions can be used, we need to go under the hood a bit. A bitfield definition simply generates a C++ preprocessor macro that extracts the specified bitfield from the implicit variable `machInst`. The machine instruction parameter to the decode function is also called `machInst`; thus any use of a bitfield name that ends up inside the decode function (such as the argument of a decode block or the decode piece of an instruction format's output) will implicitly reference the instruction currently being decoded. The binary machine instruction stored in the `StaticInst` object is also named `machInst`, so any use of a bitfield name in a member function of an instruction object will reference this stored value. This data member is initialized in the `StaticInst` constructor, so it is safe to use bitfield names even in the constructors of derived objects.

### Operand and operand type definitions

These statements specify the operand types that can be used in the code blocks that express the functional operation of instructions. See [Operand type qualifiers](#operand-type-qualifiers)  and [Instruction parsing](#instruction-operands).

### Namespace declaration

The final component of the declaration section is the namespace declaration, consisting of the keyword `namespace` followed by an identifier and a semicolon. Exactly one namespace declaration must appear in the declarations section. The resulting C++ decode function, the declarations resulting from the instruction definitions in the decode block, and the contents of any `declare` statements occurring after then namespace declaration will be placed in a C++ namespace with the specified name. The contents of `declare` statements occurring before the namespace declaration will be outside the namespace.


## ISA parser

### Formats

### operands

### decode tree

### let blocks

### microcode assembler
#### microops
#### macroops
#### directives
#### rom object

### Lots more stuff

# Code parsing

To a large extent, the power and flexibility of the ISA description mechanism stem from the fact that the mapping from a brief instruction definition provided in the decode block to the resulting C++ code is performed in a general-purpose programming language (Python). (This function is performed by the "instruction format" definition described above in [Format definitions](#format-definitions). Technically, the ISA description language allows any arbitrary Python code to perform this mapping. However, the parser provides a library of Python classes and functions designed to automate the process of deducing an instruction's characteristics from a brief description of its operation, and generating the strings required to populate declaration and decode templates. This library represents roughly half of the code in isa\_parser.py.

Instruction behaviors are described using C++ with two extensions: bitfield operators and operand type qualifiers. To avoid building a full C++ parser into the ISA description system (or conversely constraining the C++ that could be used for instruction descriptions), these extensions are implemented using regular expression matching and substitution. As a result, there are some syntactic constraints on their usage. The following two sections discuss these extensions in turn. The third section discusses operand parsing, the technique by which the parser automatically infers most instruction characteristics. The final two sections discuss the Python classes through which instruction formats interact with the library: `CodeBlock`, which analyzes and encapsulates instruction description code; and the instruction object parameter class, `InstObjParams`, which encapsulates the full set of parameters to be substituted into a template.

### Bitfield operators

Simple bitfield extraction can be performed on rvalues using the `<:>` postfix operator. Bit numbering matches that used in global bitfield definitions (see [Bitfield definitions](#bitfield-definitions)). For example, `Ra<7:0>` extracts the low 8 bits of register `Ra`. Single-bit fields can be specified by eliminating the latter operand, e.g. `Rb<31:>`. Unlike in global bitfield definitions, the colon cannot be eliminated, as it becomes too difficult to distinguish bitfield operators from template arguments. In addition, the bit index parameters must be either identifiers or integer constants; expressions are not allowed. The bit operator will apply either to the syntactic token on its left, or, if that token is a closing parenthesis, to the parenthesized expression.

### Operand type qualifiers

The effective type of an instruction operand (e.g., a register) may be specified by appending a period and a type qualifier to the operand name. The list of type qualifiers is architecture-specific; the `def operand_types` statement in the ISA description is used to specify it. The specification is in the form of a Python dictionary which maps a type extension to type name. For example, the Alpha ISA definition is as follows:

{% raw %}
```
def operand_types {{
    'sb' : 'int8_t',
    'ub' : 'uint8_t',
    'sw' : 'int16_t',
    'uw' : 'uint16_t',
    'sl' : 'int32_t',
    'ul' : 'uint32_t',
    'sq' : 'int64_t',
    'uq' : 'uint64_t',
    'sf' : 'float',
    'df' : 'double'
}};
```
{% endraw %}

Thus the Alpha 32-bit add instruction addl could be defined as:
```
Rc.sl = Ra.sl + Rb.sl;
```
The operations are performed using the types specified; the result will be converted from the specified type to the appropriate register value (in this case by sign-extending the 32-bit result to 64 bits, since Alpha integer registers are 64 bits in size).

Type qualifiers are allowed only on recognized instruction operands (see [Instruction operands](#instruction-operands)).

### Instruction operands

Most of the automation provided by the parser is based on its recognition of the operands used in the instruction definition code. Most relevant instruction characteristics can be inferred from the operands: floating-point vs. integer instructions can be recognized by the registers used, an instruction that reads from a memory location is a load, etc. In combination with the bitfield operands and type qualifiers described above, most instructions can be described in a single line of code. In addition, most of the differences between simulator CPU models lies in the operand access mechanisms; by generating the code for these accesses automatically, a single description suffices for a variety of situations.

The ISA description provides a list of recognized instruction operands and their characteristics via the `def operands` statement. This statement specifies a Python dictionary that maps operand strings to a five-element tuple.  The elements of the tuple specify the operand as follows:

1. the operand class, which must be one of the strings "IntReg", "FloatReg", "Mem", "NPC", or "ControlReg", indicating an integer register, floating-point register, memory location, the next program counter (NPC), or a control register, respectively. 
2. the default type of the operand (an extension string defined in the `def operand_types` block),
3. a specifier indicating how specific instances of the operand are decoded (e.g., a bitfield name),
4. a string or triple of strings indicating the instruction flags that can be inferred when the operand is used, and
5. a sort priority used to control the order of operands in disassembly.

For example, a simplified subset of the Alpha ISA operand traits map is as follows:

{% raw %}
```
def operands {{
    'Ra': ('IntReg', 'uq', 'RA', 'IsInteger', 1),
    'Rb': ('IntReg', 'uq', 'RB', 'IsInteger', 2),
    'Rc': ('IntReg', 'uq', 'RC', 'IsInteger', 3),
    'Fa': ('FloatReg', 'df', 'FA', 'IsFloating', 1),
    'Fb': ('FloatReg', 'df', 'FB', 'IsFloating', 2),
    'Fc': ('FloatReg', 'df', 'FC', 'IsFloating', 3),
    'Mem': ('Mem', 'uq', None, ('IsMemRef', 'IsLoad', 'IsStore'), 4),
    'NPC': ('NPC', 'uq', None, ( None, None, 'IsControl'), 4)
}};
```
{% endraw %}

The operand named `Ra` is an integer register, default type `uq` (unsigned quadword), uses the `RA` bitfield from the instruction, implies the `IsInteger` instruction flag, and has a sort priority of 1 (placing it first in any list of operands).

For the instruction flag element, a single string (such as `'IsInteger'` implies an unconditionally inferred instruction flag. If the flag operand is a triple, the first element is unconditional, the second is inferred when the operand is a source, and the third when it is a destination. Thus the `('IsMemRef', 'IsLoad', 'IsStore')` element for memory references indicates that any instruction with a memory operand is marked as a memory reference. In addition, if the memory operand is a source, the instruction is marked as a load, while if the operand is a destination, the instruction is marked a store. Similarly, the `(None, None, 'IsControl')` tuple for the NPC operand indicates that any instruction that writes to the NPC is a control instruction, but instructions which merely reference NPC as a source do not receive any default flags.

Note that description code parsing uses regular expressions, which limits the ability of the parser to infer the nature of a partciular operand.  In particular, destination operands are distinguished from source operands solely by testing whether the operand appears on the left-hand side of an assignment operator (`=`). Destination operands that are assigned to in a different fashion, e.g. by being passed by reference to other functions, must still appear on the left-hand side of an assignment to be properly recognized as destinations.  The parser also does not recognize C compound assignments, e.g., `+=`.  If an operand is both a source and a destination, it must appear on both the left- and right-hand sides of `=`.

Another limitation of regular-expression-based code parsing is that control flow in the code block is not recognized.  Combined with the details of how register updates are performed in the CPU models, this means that destinations cannot be updated conditionally.  If a particular register is recognized as a destination register, that register will always be updated at the end of the `execute()` method, and thus the code must assign a valid value to that register along each possible code path within the block.

### The CodeBlock class

An instruction format requests processing of a string containing instruction description code by passing the string to the CodeBlock constructor. The constructor performs all of the needed analysis and processing, storing the results in the returned object. Among the CodeBlock fields are:

* `orig_code`: the original code string.
* `code`: a processed string containing legal C++ code, derived from the original code by substituting in the bitfield operators and munging operand type qualifiers (s/\./\_/) to make valid C++ identifiers.
* `constructor`: code for the constructor of an instruction object, initializing various C++ object fields including the number of operands and the register indices of the operands.
* `exec_decl`: code to declare the C++ variables corresponding to the operands, for use in an execution emulation function.
* `*_rd`: code to read the actual operand values into the corresponding C++ variables for source operands. The first part of the name indicates the relevant CPU model (currently simple and dtld are supported).
* `*_wb`: code to write the C++ variable contents back to the appropriate register or memory location. Again, the first part of the name reflects the CPU model.
* `*_mem_rd`, `*_nonmem_rd`, `*_mem_wb`, `*_nonmem_wb`: as above, but with memory and non-memory operands segregated.
* `flags`: the set of instruction flags implied by the operands.
* `op_class`: a basic guess at the instruction's operation class (see OpClass) based on the operand types alone.

### The InstObjParams class

Instances of the InstObjParams class encapsulate all of the parameters needed to substitute into a code template, to be used as the argument to a template's `subst()` method (see Template definitions). 

```python
class InstObjParams(object):
    def __init___(self, parser, 
                  mem, class_name, base_class = '',
                  snippets = {}, opt_args = []):
```

The first three constructor arguments populate the object's `mnemonic`, `class_name`, and (optionally) `base_class` members. The fourth (optional) argument is a CodeBlock object; all of the members of the provided CodeBlock object are copied to the new object, making them accessible for template substitution. Any remaining arguments are interpreted as either additional instruction flags (appended to the `flags` list inherited from the CodeBlock argument, if any), or as an operation class (overriding any `op_class` from the CodeBlock).


---


## X86 Micro-op ISA

*Source: https://www.gem5.orgdocumentation/general_docs/architecture_support/x86_microop_isa/*

# Register Ops
These microops typically take two sources and produce one result. Most have a version that operates on only registers and a version which operates on registers and an immediate value. Some optionally set flags according to their operation. Some of them can be predicated. 

### Add
Addition.

#### add Dest, Src1, Src2
Dest # Dest <- Src1 + Src2

Adds the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### addi Dest, Src1, Imm
Dest # Dest <- Src1 + Imm

Adds the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The carry out of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The carry from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Adc
Add with carry.

#### adc Dest, Src1, Src2
Dest # Dest <- Src1 + Src2 + CF

Adds the contents of the Src1 and Src2 registers and the carry flag and puts the result in the Dest register.

#### adci Dest, Src1, Imm
Dest # Dest <- Src1 + Imm + CF

Adds the contents of the Src1 register, the immediate Imm, and the carry flag and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The carry out of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The carry from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Sub
Subtraction.

#### sub Dest, Src1, Src2
Dest # Dest <- Src1 - Src2

Subtracts the contents of the Src2 register from the Src1 register and puts the result in the Dest register.

#### subi Dest, Src1, Imm
Dest # Dest <- Src1 - Imm

Subtracts the contents of the immediate Imm from the Src1 register and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The borrow into of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The borrow from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Sbb

Subtract with borrow.

#### sbb Dest, Src1, Src2
Dest # Dest <- Src1 - Src2 - CF

Subtracts the contents of the Src2 register and the carry flag from the Src1 register and puts the result in the Dest register.

#### sbbi Dest, Src1, Imm
Dest # Dest <- Src1 - Imm - CF

Subtracts the immediate Imm and the carry flag from the Src1 register and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The borrow into of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The borrow from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Mul1s

Signed multiply.

#### mul1s Src1, Src2
ProdHi:ProdLo # Src1 * Src2

Multiplies the unsigned contents of the Src1 and Src2 registers and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### mul1si Src1, Imm
ProdHi:ProdLo # Src1 * Imm

Multiplies the unsigned contents of the Src1 register and the immediate Imm and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### Flags
This microop does not set any flags.

### Mul1u

Unsigned multiply.

#### mul1u Src1, Src2
ProdHi:ProdLo # Src1 * Src2

Multiplies the unsigned contents of the Src1 and Src2 registers and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### mul1ui Src1, Imm
ProdHi:ProdLo # Src1 * Imm

Multiplies the unsigned contents of the Src1 register and the immediate Imm and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### Flags
This microop does not set any flags.

### Mulel

Unload multiply result low.

#### mulel Dest
Dest # Dest <- ProdLo

Moves the value of the internal ProdLo register into the Dest register.

#### Flags
This microop does not set any flags.

### Muleh

Unload multiply result high.

#### muleh Dest
Dest # Dest <- ProdHi

Moves the value of the internal ProdHi register into the Dest register.

#### Flags
This microop optionally sets the CF, ECF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Whether ProdHi is non-zero.
OF	   | Whether ProdHi is zero.

### Div1

First stage of division.

#### div1 Src1, Src2
Quotient * Src2 + Remainder # Src1
Divisor # Src2

Begins a division operation where the contents of SrcReg1 is the high part of the dividend and the contents of SrcReg2 is the divisor. The remainder from this partial division is put in the internal register Remainder. The quotient is put in the internal register Quotient. The divisor is put in the internal register Divisor.

#### div1i Src1, Imm:
Quotient * Imm + Remainder # Src1
Divisor # Imm

Begins a division operation where the contents of SrcReg1 is the high part of the dividend and the immediate Imm is the divisor. The remainder from this partial division is put in the internal register Remainder. The quotient is put in the internal register Quotient. The divisor is put in the internal register Divisor.

#### Flags
This microop does not set any flags.

### Div2

Second and later stages of division.

#### div2 Dest, Src1, Src2
Quotient * Divisor + Remainder # original Remainder with bits shifted in from Src1

Dest # Dest <- Src2 - number of bits shifted in above

Performs subsequent steps of division following a div1 instruction. The contents of the register Src1 is the low portion of the dividend. The contents of the register Src2 denote the number of bits in Src1 that have not yet been used before this step in the division. Dest is set to the number of bits in Src1 that have not been used after this step. The internal registers Quotient, Divisor, and Remainder are updated by this instruction.

If there are no remaining bits in Src1, this instruction does nothing except optionally compute flags.

#### div2i Dest, Src1, Imm
Quotient * Divisor + Remainder # original Remainder with bits shifted in from Src1

Dest # Dest <- Imm - number of bits shifted in above

Performs subsequent steps of division following a div1 instruction. The contents of the register Src1 is the low portion of the dividend. The immediate Imm denotes the number of bits in Src1 that have not yet been used before this step in the division. Dest is set to the number of bits in Src1 that have not been used after this step. The internal registers Quotient, Divisor, and Remainder are updated by this instruction.

If there are no remaining bits in Src1, this instruction does nothing except optionally compute flags.

#### Flags
This microop optionally sets the EZF flag.

Flag       | Meaning
---------- | ------------------------------------------
EZF	   | Whether there are any remaining bits in Src1 after this step.

### Divq

Unload division quotient.

#### divq Dest
Dest # Dest <- Quotient

Moves the value of the internal Quotient register into the Dest register.

#### Flags
This microop does not set any flags.

### Divr

Unload division remainder.

#### divr Dest
Dest # Dest <- Remainder

Moves the value of the internal Remainder register into the Dest register.

#### Flags
This microop does not set any flags.

### Or

Logical or.

#### or Dest, Src1, Src2
Dest # Dest <- Src1 | Src2

Computes the bitwise or of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### ori Dest, Src1, Imm
Dest # Dest <- Src1 | Imm

Computes the bitwise or of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### And

Logical And

#### and Dest, Src1, Src2
Dest # Dest <- Src1 & Src2

Computes the bitwise and of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### andi Dest, Src1, Imm
Dest # Dest <- Src1 & Imm

Computes the bitwise and of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### Xor

Logical exclusive or.

#### xor Dest, Src1, Src2
Dest # Dest <- Src1 | Src2

Computes the bitwise xor of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### xori Dest, Src1, Imm
Dest # Dest <- Src1 | Imm

Computes the bitwise xor of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### Sll

Logical left shift.

#### sll Dest, Src1, Src2
Dest # Dest <- Src1 << Src2

Shifts the contents of the Src1 register to the left by the value in the Src2 register and writes the result into the Dest register. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### slli Dest, Src1, Imm
Dest # Dest <- Src1 << Imm

Shifts the contents of the Src1 register to the left by the value in the immediate Imm and writes the result into the Dest register. The shift amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | The exclusive OR of what this instruction would set the CF flag to, if requested, and the most significant bit of the result.

### Srl

Logical right shift.

#### srl Dest, Src1, Src2
Dest # Dest <- Src1 >>(logical) Src2

Shifts the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. Bits which are shifted in sign extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### srli Dest, Src1, Imm
Dest # Dest <- Src1 >>(logical) Imm

Shifts the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. Bits which are shifted in sign extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
SF	   | The most significant bit of the original value to shift.

### Sra

Arithmetic right shift.

#### sra Dest, Src1, Src2
Dest # Dest <- Src1 >>(arithmetic) Src2

Shifts the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. Bits which are shifted in zero extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### srai Dest, Src1, Imm
Dest # Dest <- Src1 >>(arithmetic) Imm

Shifts the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. Bits which are shifted in zero extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | Cleared.

### Ror

Rotate right.

#### ror Dest, Src1, Src2
Rotates the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rori Dest, Src1, Imm
Rotates the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The most significant bit of the result.
OF	   | The exclusive OR of the most two significant bits of the original value.

### Rcr

Rotate right through carry.

#### rcr Dest, Src1, Src2
Rotates the contents of the Src1 register through the carry flag and to the right by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rcri Dest, Src1, Imm
Rotates the contents of the Src1 register through the carry flag and to the right by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | The exclusive OR of the CF flag before the rotate and the most significant bit of the original value.

### Rol

Rotate left.

#### rol Dest, Src1, Src2
Rotates the contents of the Src1 register to the left by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### roli Dest, Src1, Imm
Rotates the contents of the Src1 register to the left by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The least significant bit of the result.
OF	   | The exclusive OR of the most and least significant bits of the result.

### Rcl

Rotate left through carry.

#### rcl Dest, Src1, Src2
Rotates the contents of the Src1 register through the carry flag and to the left by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rcli Dest, Src1, Imm
Rotates the contents of the Src1 register through the carry flag and to the left by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit rotated out of the result.
OF	   | The exclusive OR of CF before the rotate and the most significant bit of the result.

### Mov

Move.

#### mov Dest, Src1, Src2
Dest # Src1 <- Src2

Merge the contents of the Src2 register into the contents of Src1 and put the result into the Dest register.

#### movi Dest, Src1, Imm
Dest # Src1 <- Imm

Merge the contents of the immediate Imm into the contents of Src1 and put the results into the Dest register.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Sext

Sign extend.

#### sext Dest, Src1, Imm
Dest # Dest <- sign_extend(Src1, Imm)

Sign extend the value in the Src1 register starting at the bit position in the immediate Imm, and put the result in the Dest register.

#### Flags
This microop does not set any flags.

### Zext

Zero extend.

#### zext Dest, Src1, Imm
Dest # Dest <- zero_extend(Src1, Imm)

Zero extend the value in the Src1 register starting at the bit position in the immediate Imm, and put the result in the Dest register.

#### Flags
This microop does not set any flags.

### Ruflag

Read user flag.

#### ruflag Dest, Imm
Reads the user level flag stored in the bit position specified by the immediate Imm and stores it in the register Dest.

The mapping between values of Imm and user level flags is show in the following table.

Imm        | Flag
---------- | ------------------------------------------
0          | CF (carry flag)
2          | PF (parity flag)
3          | ECF (emulation carry flag)
4          | AF (auxiliary flag)
5          | EZF (emulation zero flag)
6          | ZF (zero flag)
7          | CF (sign flag)
10         | CF (direction flag)
11         | CF (overflow flag)

#### Flags
The EZF flag is always set. In the future this may become optional.


### Ruflags

Read all user flags.

#### ruflags Dest
Dest # user flags

Store the user level flags into the Dest register.

#### Flags
This microop does not set any flags.

### Wruflags

Write all user flags.

#### wruflags Src1, Src2
user flags # Src1 ^ Src2

Set the user level flags to the exclusive or of the Src1 and Src2 registers.

#### wruflagsi Src1, Imm
user flags # Src1 ^ Imm

Set the user level flags to the exclusive or of the Src1 register and the immediate Imm.

#### Flags
See above.

### Rdip

Read the instruction pointer.

#### rdip Dest
Dest # rIP

Set the Dest register to the current value of rIP.

#### Flags
This microop does not set any flags.

### Wrip

Write the instruction pointer.

#### wrip Src1, Src2
rIP # Src1 + Src2

Set the rIP to the sum of the Src1 and Src2 registers. This causes a macroop branch at the end of the current macroop.

#### wripi Src1, Imm
micropc # Src1 + Imm

Set the rIP to the sum of the Src1 register and immediate Imm. This causes a macroop branch at the end of the current macroop.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Chks
Check selector.

Not yet implemented.

# Load/Store Ops

### Ld
Load.
#### ld Data, Seg, Sib, Disp
Loads the integer register Data from memory.

### Ldf
Load floating point.
#### ldf Data, Seg, Sib, Disp
Loads the floating point register Data from memory.

### Ldm
Load multimedia.
#### ldm Data, Seg, Sib, Disp
Load the multimedia register Data from memory.
This is not implemented and may never be.

### Ldst
Load with store check.
#### Ldst Data, Seg, Sib, Disp
Load the integer register Data from memory while also checking if a store to that location would succeed.
This is not implemented currently.

### Ldstl
Load with store check, locked.
#### Ldst Data, Seg, Sib, Disp
Load the integer register Data from memory while also checking if a store to that location would succeed, and also provide the semantics of the "LOCK" instruction prefix.
This is not implemented currently.

### St
Store.
#### st Data, Seg, Sib, Disp
Stores the integer register Data to memory.

### Stf
Store floating point.
#### stf Data, Seg, Sib, Disp
Stores the floating point register Data to memory.

### Stm
Store multimedia.
#### stm Data, Seg, Sib, Disp
Store the multimedia register Data to memory.
This is not implemented and may never be.

### Stupd
Store with base update.
#### Stupd Data, Seg, Sib, Disp
Store the integer register Data to memory and update the base register.

### Lea
Load effective address.
#### lea Data, Seg, Sib, Disp
Calculates the address for this combination of parameters and stores it in Data.

### Cda
Check data address.
#### cda Seg, Sib, Disp
Check whether the data address is valid.
This is not implemented currently.

### Cdaf
CDA with cache line flush.
#### cdaf Seg, Sib, Disp
Check whether the data address is valid, and flush cache lines
This is not implemented currently.

### Cia
Check instruction address.
#### cia Seg, Sib, Disp
Check whether the instruction address is valid.
This is not implemented currently.

### Tia
TLB invalidate address
#### tia Seg, Sib, Disp
Invalidate the tlb entry which corresponds to this address.
This is not implemented currently.

# Load immediate Op

### Limm
#### limm Dest, Imm
Stores the 64 bit immediate Imm into the integer register Dest.

# Floating Point Ops

### Movfp
#### movfp Dest, Src
Dest # Src

Move the contents of the floating point register Src into the floating point register Dest.

This instruction is predicated.

### Xorfp
#### xorfp Dest, Src1, Src2
Dest # Src1 ^ Src2

Compute the bitwise exclusive or of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Sqrtfp
#### sqrtfp Dest, Src
Dest # sqrt(Src)

Compute the square root of the floating point register Src and put the result in floating point register Dest.

### Addfp
#### addfp Dest, Src1, Src2
Dest # Src1 + Src2

Compute the sum of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Subfp
#### subfp Dest, Src1, Src2
Dest # Src1 - Src2

Compute the difference of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Mulfp
#### mulfp Dest, Src1, Src2
Dest # Src1 * Src2

Compute the product of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Divfp
#### divfp Dest, Src1, Src2
Dest # Src1 / Src2

Divide Src1 by Src2 and put the result in the floating point register Dest.

### Compfp
#### compfp Src1, Src2
Compare floating point registers Src1 and Src2.

### Cvtf_i2d
#### cvtf_i2d Dest, Src
Convert integer register Src into a double floating point value and store the result in the lower part of Dest.

### Cvtf_i2d_hi
#### cvtf_i2d_hi Dest, Src
Convert integer register Src into a double floating point value and store the result in the upper part of Dest.

### Cvtf_d2i
#### cvtf_d2i Dest, Src
Convert floating point register Src into an integer value and store the result in the integer register Dest.

# Special Ops

### Fault
Generate a fault.
#### fault fault_code
Uses the C++ code fault_code to allocate a Fault object to return.

### Lddha
Set the default handler for a fault.
This is not implemented currently.

### Ldaha
Set the alternate handler for a fault
This is not implemented currently.

# Sequencing Ops
These microops are used for control flow withing microcode

### Br

Microcode branch. This is never considered the last microop of a sequence. If it appears at the end of a macroop, it is assumed that it branches to microcode in the ROM.

#### br target
micropc # target

Set the micropc to the 16 bit immediate target.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Eret

Return from emulation. This instruction is always considered the last microop in a sequence. When executing from the ROM, it is the only way to return to normal instruction decoding.

#### eret

Return from emulation.

#### Flags
This microop does not set any flags. It is optionally predicated.


---


## Building gem5

*Source: https://www.gem5.org/documentation/general_docs/building*

# Building gem5

## Supported operating systems and environments

gem5 has been designed with a Linux environment in mind. We test regularly
on **Ubuntu 22.04** and **Ubuntu 24.04** to ensure gem5 functions well in
these environments. Though **any Linux based OS should function if the correct
dependencies are installed**. We ensure that gem5 is compilable with both gcc
and clang (see [Dependencies](#dependencies)  below for compiler version
information).

As of gem5 21.0, **we support building and running gem5 with Python 3.6+
only**. gem5 20.0 was our last version of gem5 to provide support for Python
2.

If running gem5 in a suitable OS/environment is not possible, we have provided
pre-prepared [Docker](https://www.docker.com/) images which may be used to
compile and run gem5. Please see our [Docker](#docker) section below for more
information on this.

## Dependencies

* **git** : gem5 uses git for version control.
* **gcc**: gcc is used to compiled gem5. **Version >=10 must be used**. We
support up to gcc Version 13.
* **Clang**: Clang can also be used. At present, we support Clang 7 to
Clang 16 (inclusive).
* **SCons** : gem5 uses SCons as its build environment. SCons 3.0 or greater
must be used.
* **Python 3.6+** : gem5 relies on Python development libraries. gem5 can be
compiled and run in environments using Python 3.6+.
* **protobuf 2.1+** (Optional): The protobuf library is used for trace
generation and playback.
* **Boost** (Optional): The Boost library is a set of general purpose C++
libraries. It is a necessary dependency if you wish to use the SystemC
implementation.

### Setup on Ubuntu 24.04 (gem5 >= v24.0)

If compiling gem5 on Ubuntu 24.04, or related Linux distributions, you may
install all these dependencies using APT:

```bash
sudo apt install build-essential scons python3-dev git pre-commit zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    libboost-all-dev  libhdf5-serial-dev python3-pydot python3-venv python3-tk mypy \
    m4 libcapstone-dev libpng-dev libelf-dev pkg-config wget cmake doxygen clang-format
```

### Setup on Ubuntu 22.04 (gem5 >= v21.1)

If compiling gem5 on Ubuntu 22.04, or related Linux distributions, you may
install all these dependencies using APT:

```bash
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev libboost-all-dev pkg-config python3-tk clang-format-15
```

You may need to configure `clang-format-15` as the default
`clang-format` for your system.

```bash
# Configure clang-format-15 and git-clang-format-15 as the system defaults.
sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-15 150 \
        --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-15 \
        --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-15

# [Optional] Add other alternative versions, and select version 15 as the default version.
sudo update-alternatives --config clang-format
```

### Setup on Ubuntu 20.04 (gem5 >= v21.0)

If compiling gem5 on Ubuntu 20.04, or related Linux distributions, you may
install all these dependencies using APT:

```bash
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python-is-python3 libboost-all-dev pkg-config gcc-10 g++-10 \
    python3-tk clang-format-18
```

You may need to configure `clang-format-18` as the default
`clang-format` for your system.

```bash
# Configure clang-format-18 and git-clang-format-18 as the system defaults.
sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-18 180 \
        --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-18 \
        --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-18

# [Optional] Add other alternative versions, and select version 18 as the default version.
sudo update-alternatives --config clang-format
```

### Docker

For users struggling to setup an environment to build and run gem5, we provide
the following Docker Images:

Ubuntu 24.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0](
https://ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0)
([source Dockerfile](https://github.com/gem5/gem5/blob/v24.0.0.0/util/dockerfiles/ubuntu-24.04_all-dependencies/Dockerfile)).

Ubuntu 24.04 with minimum dependencies:
[ghcr.io/gem5/ubuntu-24.04_min-dependencies:v24-0](
https://ghcr.io/gem5/ubuntu-24.04_min-dependencies:v24-0)
([source Dockerfile](https://github.com/gem5/gem5/blob/v24.0.0.0/util/dockerfiles/ubuntu-24.04_min-dependencies/Dockerfile)).

Ubuntu 22.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-22.04_all-dependencies/Dockerfile)).

Ubuntu 20.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-20.04_all-dependencies/Dockerfile)).

Ubuntu 18.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-18.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-18.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-18.04_all-dependencies/Dockerfile)).

To obtain a docker image:

```bash
docker pull <image>
```

E.g., for Ubuntu 20.04 with all optional dependencies:

```bash
docker pull ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0
```

Then, to work within this environment, we suggest using the following:

```bash
docker run -u $UID:$GID --volume <gem5 directory>:/gem5 --rm -it <image>
```

Where `<gem5 directory>` is the full path of the gem5 in your file system, and
`<image>` is the image pulled (e.g.,
ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0`).

From this environment, you will be able to build and run gem5 from the `/gem5`
directory.

## Getting the code

```bash
git clone https://github.com/gem5/gem5
```

## Building with SCons

gem5's build system is based on SCons, an open source build system implemented
in Python. You can find more information about scons at <http://www.scons.org>.
The main scons file is called SConstruct and is found in the root of the source
tree. Additional scons files are named SConscript and are found throughout the
tree, usually near the files they're associated with.

Within the root of the gem5 directory, gem5 can be built with SCons using:

```bash
scons build/{ISA}/gem5.{variant} -j {cpus}
```

where `{ISA}` is the target (guest) Instruction Set Architecture, and
`{variant}` specifies the compilation settings. For most intents and purposes
`opt` is a good target for compilation. The `-j` flag is optional and allows
for parallelization of compilation with `{cpus}` specifying the number of
threads. A single-threaded compilation from scratch can take up to 2 hours on
some systems. We therefore strongly advise allocating more threads if possible.
However, compilation of gem5 is compute and memory intensive and increasing the
number of threads also increases memory usage. If using a machine with less
memory, it is recommended to use fewer threads (e.g. `-j 1` or `-j 2`).

The valid ISAs are:

* ALL - recommended, as it has all ISAs and all Ruby protocols as of gem5 v24.1
* ARM
* NULL
* MIPS
* POWER
* RISCV
* SPARC
* X86

The valid build variants are:

* **debug** has optimizations turned off. This ensures that variables won't be
optimized out, functions won't be unexpectedly inlined, and control flow will
not behave in surprising ways. That makes this version easier to work with in
tools like gdb, but without optimizations this version is significantly slower
than the others. You should choose it when using tools like gdb and valgrind
and don't want any details obscured, but other wise more optimized versions are
recommended.
* **opt** has optimizations turned on and debugging functionality like asserts
and DPRINTFs left in. This gives a good balance between the speed of the
simulation and insight into what's happening in case something goes wrong. This
version is best in most circumstances.
* **fast** has optimizations turned on and debugging functionality compiled
out. This pulls out all the stops performance wise, but does so at the expense
of run time error checking and the ability to turn on debug output. This
version is recommended if you're very confident everything is working correctly
and want to get peak performance from the simulator.

These versions are summarized in the following table.

|Build variant|Optimizations|Run time debugging support|
|-------------|-------------|--------------------------|
|**debug**    |             |X                         |
|**opt**      |X            |X                         |
|**fast**     |X            |                          |

For example, to build gem5 on 4 threads with `opt` and with all ISAs:

```bash
scons build/ALL/gem5.opt -j 4
```

In addition, users may make use of the "gprof" and "pperf" build options to
enable profiling:

* **gprof** allows gem5 to be used with the gprof profiling tool. It can be
enabled by compiling with the `--gprof` flag. E.g.,
`scons build/ALL/gem5.debug --gprof`.
* **pprof** allows gem5 to be used with the pprof profiling tool. It can be
enabled by compiling with the `--pprof` flag. E.g.,
`scons build/ALL/gem5.debug --pprof`.

## Build with Kconfig

Please see [here](https://www.gem5.org/documentation/general_docs/kconfig_build_system/)

## Usage

Once compiled, gem5 can then be run using:

```console
./build/{ISA}/gem5.{variant} [gem5 options] {simulation script} [script options]
```

If you are building gem5 from a pre-compiled binary, gem5 can be run with the following command:

```console
gem5 [gem5 options] {simulation script} [script options]
```

Running with the `--help` flag will display all the available options:

```txt
Usage
=====
  gem5.opt [gem5 options] script.py [script options]

gem5 is copyrighted software; use the --copyright option for details.

Options
=======
--help, -h              show this help message and exit
--build-info, -B        Show build information
--copyright, -C         Show full copyright information
--readme, -R            Show the readme
--outdir=DIR, -d DIR    Set the output directory to DIR [Default: m5out]
--redirect-stdout, -r   Redirect stdout (& stderr, without -e) to file
--redirect-stderr, -e   Redirect stderr to file
--silent-redirect       Suppress printing a message when redirecting stdout or
                        stderr
--stdout-file=FILE      Filename for -r redirection [Default: simout.txt]
--stderr-file=FILE      Filename for -e redirection [Default: simerr.txt]
--listener-mode={on,off,auto}
                        Port (e.g., gdb) listener mode (auto: Enable if
                        running interactively) [Default: auto]
--allow-remote-connections
                        Port listeners will accept connections from anywhere
                        (0.0.0.0). Default is only localhost.
--interactive, -i       Invoke the interactive interpreter after running the
                        script
--pdb                   Invoke the python debugger before running the script
--path=PATH[:PATH], -p PATH[:PATH]
                        Prepend PATH to the system path when invoking the
                        script
--quiet, -q             Reduce verbosity
--verbose, -v           Increase verbosity
-m mod                  run library module as a script (terminates option
                        list)
-c cmd                  program passed in as string (terminates option list)
-P                      Don't prepend the script directory to the system path.
                        Mimics Python 3's `-P` option.
-s                      IGNORED, only for compatibility with python. don'tadd
                        user site directory to sys.path; also PYTHONNOUSERSITE

Statistics Options
------------------
--stats-file=FILE       Sets the output file for statistics [Default:
                        stats.txt]
--stats-help            Display documentation for available stat visitors

Configuration Options
---------------------
--dump-config=FILE      Dump configuration output file [Default: config.ini]
--json-config=FILE      Create JSON output of the configuration [Default:
                        config.json]
--dot-config=FILE       Create DOT & pdf outputs of the configuration
                        [Default: config.dot]
--dot-dvfs-config=FILE  Create DOT & pdf outputs of the DVFS configuration
                        [Default: none]

Debugging Options
-----------------
--debug-break=TICK[,TICK]
                        Create breakpoint(s) at TICK(s) (kills process if no
                        debugger attached)
--debug-help            Print help on debug flags
--debug-flags=FLAG[,FLAG]
                        Sets the flags for debug output (-FLAG disables a
                        flag)
--debug-start=TICK      Start debug output at TICK
--debug-end=TICK        End debug output at TICK
--debug-file=FILE       Sets the output file for debug. Append '.gz' to the
                        name for it to be compressed automatically [Default:
                        cout]
--debug-activate=EXPR[,EXPR]
                        Activate EXPR sim objects
--debug-ignore=EXPR     Ignore EXPR sim objects
--remote-gdb-port=REMOTE_GDB_PORT
                        Remote gdb base port (set to 0 to disable listening)

Help Options
------------
--list-sim-objects      List all built-in SimObjects, their params and default
                        values
```

## Using EXTRAS

The [EXTRAS](/documentation/general_docs/building/EXTRAS) scons variable can be
used to build additional directories of source files into gem5 by setting it to
a colon delimited list of paths to these additional directories. EXTRAS is a
handy way to build on top of the gem5 code base without mixing your new source
with the upstream source. You can then manage your new body of code however you
need to independently from the main code base.


---


## Building EXTRAS

*Source: https://www.gem5.org/documentation/general_docs/building/EXTRAS*

# Building EXTRAS
The `EXTRAS` SCons option is a way to add functionality in gem5 without adding your files to the gem5 source tree. Specifically, it allows you to identify one or more directories that will get compiled in with gem5 as if they appeared under the 'src' part of the gem5 tree, without requiring the code to be actually located under 'src'. It's present to allow user to compile in additional functionality (typically additional SimObject classes) that isn't or can't be distributed with gem5. This is useful for maintaining local code that isn't suitable for incorporating into the gem5 source tree, or third-party code that can't be incorporated due to an incompatible license. Because the EXTRAS location is completely independent of the gem5 repository, you can keep the code under a different version control system as well.

The main drawback of the EXTRAS feature is that, by itself, it only supports adding code to gem5, not modifying any of the base gem5 code. 

One use of the EXTRAS feature is to support EIO traces. The trace reader for EIO is licensed under the SimpleScalar license, and due to the incompatibility of that license with gem5's BSD license, the code to read these traces is not included in the gem5 distribution. Instead, the EIO code is distributed via a separate "encumbered" [repository](https://github.com/gem5/gem5).

The following examples show how to compile the EIO code. By adding to or modifying the extras path, any other suitable extra could be compiled in. To compile in code using EXTRAS simply execute the following

```js
 scons EXTRAS=/path/to/encumbered build/<ISA>/gem5.opt
```

In the root of this directory you should have a SConscript that uses the ```Source()``` and ```SimObject()``` scons functions that are used in the rest of M5 to compile the appropriate sources and add any SimObjects of interest. If you want to add more than one directory, you can set EXTRAS to a colon-separated list of paths.

Note that EXTRAS is a "sticky" parameter, so after a value is provided to scons once, the value will be reused for future scons invocations targeting the same build directory (```build/<ISA>``` in this case) as long as it is not overridden. Thus you only need to specify EXTRAS the first time you build a particular configuration or if you want to override a previously specified value.
To run a regression with EXTRAS use a command line similar to the following:
```js
 ./util/regress --scons-opts = "EXTRAS=/path/to/encumbered" -j 2 quick
```


---


## "Compiling Workloads"

*Source: https://www.gem5.org/documentation/general_docs/compiling_workloads/*

# Compiling Workloads

## Cross Compilers

A cross compiler is a compiler set up to run on one ISA but generate binaries which run on another. 
You may need one if you intend to simulate a system which uses a particular ISA, Alpha for instance, but don't have access to actual Alpha hardware.  

There are various sources for cross compilers. The following are some of them.

1. [ARM](https://packages.debian.org/stretch/gcc-arm-linux-gnueabihf).
2. [RISC-V](https://github.com/riscv/riscv-gnu-toolchain).

## QEMU

Alternatively, you can use QEMU and a disk image to run the desired ISA in emulation. 
To create more recent disk images, see [this page](/documentation/general_docs/fullsystem/disk). 
The following is a youtube video of working with image files using qemu on Ubuntu 12.04 64bit. 
<iframe width="560" height="315" src="https://www.youtube.com/embed/Oh3NK12fnbg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


---


## "gem5's CPU models"

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/*

## gem5 bootcamp 2022 module on using CPU models

gem5 bootcamp (2022) had a session on learning the use of different gem5 CPU models.
The slides presented in the session can be found [here](https://ucdavis365-my.sharepoint.com/:p:/g/personal/jlowepower_ucdavis_edu/EYRn68yb9nZJk9Puf7dV40YBm25hQ91WCXnEwyjqniqeVQ?e=7Xo0).

The youtube video of the recorded bootcamp module on gem5 CPU models is available [here](https://youtu.be/cDv-g-c0XCY).


---


## Execution Basics

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/execution_basics*

# Execution basic

## gem5 bootcamp 2022 module on instruction execution

gem5 bootcamp (2022) had a session on learning how instructions work in gem5 and how to add new instructions in gem5.
The slides presented in the session can be found [here](https://ucdavis365-my.sharepoint.com/:p:/g/personal/jlowepower_ucdavis_edu/EeRIKzkdUJBDlaa9AmzERusBp28hxMfkyIOp-_2H5L9AqQ?e=RoMFUD).

The youtube video of the recorded bootcamp module on gem5 instructions is available [here](https://youtu.be/Z5B02jkNpck).

# StaticInsts #
The StaticInst provides all static information and methods for a binary instruction.

It holds the following information/methods:

* Flags to tell what kind of instruction it is (integer, floating point, branch, memory barrier, etc.)
* The op class of the instruction
* The number of source and destination registers
* The number of integer and FP registers used
* Method to decode a binary instruction into a StaticInst
* Virtual function execute(), which defines how the specific architectural actions taken for an instruction (e.g. read r1, r2, add them and store in r3.)
* Virtual functions to handle starting and completing memory operations
* Virtual functions to execute the address calculation and memory access separately for models that split memory operations into two operations
* Method to disassemble the instruction, printing it out in a human readable format. (e.g. addq r1 r2 r3)

It does not have dynamic information, such as the PC of the instruction or the values of the source registers or the result. This allows a 1 to 1 mapping of StaticInst to unique binary machine instructions. We take advantage of this fact by caching the mapping of a binary instruction to a StaticInst in a hash_map, allowing us to decode a binary instruction only once, and directly using the StaticInst the rest of the time.

Each ISA instruction derives from StaticInst and implements its own constructor, the execute() function, and, if it is a memory instruction, the memory access functions. See ISA_description_system for details about how these ISA instructions are specified.
# DynInsts #
The DynInst is used to hold dynamic information about instructions. This is necessary for more detailed models or out-of-order models, both of which may need extra information beyond the [StaticInsts](#staticinsts) in order to correctly execute instructions.
Some of the dynamic information that it stores includes:
* The PC of the instruction
* The renamed register indices of the source and destination registers
* The predicted next-PC
* The instruction result
* The thread number of the instruction
* The CPU the instruction is executing on
* Whether or not the instruction is squashed

Additionally the DynInst provides the ExecContext interface. When ISA instructions are executed, the DynInst is passed in as the ExecContext, handling all accesses of the ISA to CPU state.

Detailed CPU models can derive from DynInst and create their own specific DynInst subclasses that implement any additional state or functions that might be needed. See src/cpu/o3/alpha/dyn_inst.hh for an example of this.
# Microcode support #
# ExecContext #
The ExecContext describes the interface that the ISA uses to access CPU state. Although there is a file `src/cpu/exec_context.hh`, it is purely for documentation purposes and classes do not derive from it. Instead, ExecContext is an implicit interface that is assumed by the ISA.

The ExecContext interface provides methods to:
* Read and write PC information
* Read and write integer, floating point, and control registers
* Read and write memory
* Record and return the address of a memory access, prefetching, and trigger a system call
* Trigger some full-system mode functionality

Example implementations of the ExecContext interface include:
* SimpleCPU
* DynInst

See the ISA description page for more details on how an instruction set is implemented.
# ThreadContext #
ThreadContext is the interface to all state of a thread for anything outside of the CPU. It provides methods to read or write state that might be needed by external objects, such as the PC, next PC, integer and FP registers, and IPRs. It also provides functions to get pointers to important thread-related classes, such as the ITB, DTB, System, kernel statistics, and memory ports. It is an abstract base class; the CPU must create its own ThreadContext by either deriving from it, or using the templated ProxyThreadContext class.
## ProxyThreadContext ##
The ProxyThreadContext class provides a way to implement a ThreadContext without having to derive from it. ThreadContext is an abstract class, so anything that derives from it and uses its interface will pay the overhead of virtual function calls. This class is created to enable a user-defined Thread object to be used wherever ThreadContexts are used, without paying the overhead of virtual function calls when it is used by itself. The user-defined object must simply provide all the same functions as the normal ThreadContext, and the ProxyThreadContext will forward all calls to the user-defined object. See the code of [SimpleThread](http://gem5.org/SimpleThread) for an example of using the ProxyThreadContext.
## Difference vs. ExecContext ##
The ThreadContext is slightly different than the ExecContext. The ThreadContext provides access to an individual thread's state; an ExecContext provides ISA access to the CPU (meaning it is implicitly multithreaded on SMT systems). Additionally the ThreadState is an abstract class that exactly defines the interface; the ExecContext is a more implicit interface that must be implemented so that the ISA can access whatever state it needs. The function calls to access state are slightly different between the two. The ThreadContext provides read/write register methods that take in an architectural register index. The ExecContext provides read/write register methdos that take in a StaticInst and an index, where the index refers to the i'th source or destination register of that [StaticInsts](#staticinsts). Additionally the ExecContext provides read and write methods to access memory, while the ThreadContext does not provide any methods to access memory.
# ThreadState #
The ThreadState class is used to hold thread state that is common across CPU models, such as the thread ID, thread status, kernel statistics, memory port pointers, and some statistics of number of instructions completed. Each CPU model can derive from ThreadState and build upon it, adding in thread state that is deemed appropriate. An example of this is [SimpleThread](http://gem5.org/SimpleThread), where all of the thread's architectural state has been added in. However, it is not necessary (or even feasible in some cases) for all of the thread's state to be centrally located in a ThreadState derived class. The DetailedCPU keeps register values and rename maps in its own classes outside of ThreadState. ThreadState is only used to provide a more convenient way to centrally locate some state, and provide sharing across CPU models.
# Faults #
# Registers #
## Register types - float, int, misc ##
## Indexing - register spaces stuff ##
See [Register Indexing](#register-indexing) for a more thorough treatment.

A "nickle tour" of flattening and register indexing in the CPU models.

First, an instruction has identified that it needs register such and such as determined by its encoding (or the fact that it always uses a certain register, or ...). For the sake of argument, lets say we're talking about SPARC, the register is %g1, and the second bank of globals is active. From the instructions point of view, the unflattened register is %g1, which, likely, is just represented by the index 1.

Next, we need to map from the instruction's view of the register file(s) down to actual storage locations. Think of this like virtual memory. The instruction is working within an index space which is like a virtual address space, and it needs to be mapped down to the flattened space which is like physical memory. Here, the index 1 is likely mapped to, say, 9, where 0-7 is the first bank of globals and 8-15 is the second.

This is the point where the CPU gets involved. The index 9 refers to an actual register the instruction expects to access, and it's the CPU's job to make that happen. Before this point, all the work was done by the ISA with no insight available to the CPU, and beyond this point all the work is done by the CPU with no insight available to the ISA.

The CPU is free to provide a register directly like the simple CPU by having an array and just reading and writing the 9th element on behalf of the instruction. The CPU could, alternatively, do something complicated like renaming and mapping the flattened index further into a physical register like O3.

One important property of all this, which makes sense if you think about the virtual memory analogy, is that the size of the index space before flattening has nothing to do with the size after. The virtual memory space could be very large (presumably with gaps) and map to a smaller physical space, or it could be small and map to a larger physical space where the extra is for, say, other virtual spaces used at other times. You need to make sure you're using the right size (post flattening) to size your tables because that's the space of possible options.

One other tricky part comes from the fact that we add offsets into the indices to distinguish ints from floats from miscs. Those offsets might be one thing in the preflattening world, but then need to be something else in the post flattening world to keep things from landing on top of each other without leaving gaps. It's easy to make a mistake here, and it's one of the reasons I don't like this offset idea as a way to keep the different types separate. I'd rather see a two dimensional index where the second coordinate was a register type. But in the world as it exists today, this is something you have to keep track of.
# PCs #
# Register Indexing # 
CPU register indexing in gem5 is a complicated by the need to support multiple ISAs with sometimes very different register semantics (register windows, condition codes, mode-based alternate register sets, etc.). In addition, this support has evolved gradually as new ISAs have been added, so older code may not take advantage of newer features or terminology.
# Types of Register Indices #
There are three types of register indices used internally in the CPU models: relative, unified, and flattened.
## Relative ## 
A relative register index is the index that is encoded in a machine instruction. There is a separate index space for each class of register (integer, floating point, etc.), starting at 0. The register class is implied by the opcode. Thus a value of "1" in a source register field may mean integer register 1 (e.g., "%r1") or floating point register 1 (e.g., "%f1") depending on the type of the instruction.
## Unified ##
While relative register indices are good for keeping instruction encodings compact, they are ambiguous, and thus not convenient for things like managing dependencies. To avoid this ambiguity, the decoder maps the relative register indices into a unified register space by adding class-specific offsets to relocate each relative index range into a unique position. Integer registers are unmodified, and continue to start at zero. Floating-point register indices are offset by (at least) the number of integer registers, so that the first FP register (e.g., "%f0") gets a unified index that is greater than that of the last integer register. Similarly, miscellaneous (a.k.a. control) registers are mapped past the end of the FP register index space.
## Flattened ##
Unified register indices provide an unambiguous description of all the registers that are accessible as instruction operands at a given point in the execution. Unfortunately, due to the complex features of some ISAs, they do not always unambiguously identify the actual state that the instruction is referencing. For example, in ISAs with register windows (notably SPARC), a particular register identifier such as "%o0" will refer to a different register after a "save" or "restore" operation than it did previously. Several ISAs have registers that are hidden in normal operation, but get mapped on top of ordinary registers when an interrupt occurs (e.g., ARM's mode-specific registers), or under explicit supervisor control (e.g., SPARC's "alternate globals").

We solve this problem by maintaining a flattened register space which provides a distinct index for every unique register storage location. For example, the integer portion of the SPARC flattened register space has distinct indices for the globals and the alternate globals, as well as for each of the available register windows. The "flattening" process of translating from a unified or relative register index to a flattened register index varies by ISA. On some ISAs, the mapping is trivial, while others use table lookups to do the translation.

A key distinction between the generation of unified and flattened register indices is that the former can always be done statically while the latter often depends on dynamic processor state. That is, the translation from relative to unified indices depends only on the context provided by the instruction itself (which is convenient as the translation is done in the decoder). In contrast, the mapping to a flattened register index may depend on processor state such as the interrupt level or the current window pointer on SPARC.

## Combining Register Index Types ##
Although the typical progression for modifying register indices is relative -> unified -> flattened, it turns out that relative vs. unified and flattened vs. unflattened are orthogonal attributes. Relative vs. unified indicates whether the index is relative to the base register for its register class (integer, FP, or misc) or has the base offset for its class added in. Flattened vs. unflattened indicates whether the index has been adjusted to account for runtime context such as register window adjustments or alternate register file modes. Thus a relative flattened register index is one in which the runtime context has been accounted for, but is still expressed relative to the base offset for its class.

A single set of class-specific offsets is used to generate unified indices from relative indices regardless of whether the indices are flattened or unflattened. Thus the offsets must be large enough to separate the register classes even when flattened addresses are being used. As a result, the unflattened unified register space is often discontiguous.
# Illustrations #
As an illustration, consider a hypothetical architecture with four integer registers (%r0-%r4), three FP registers (%f0-%f2), and two misc/control registers (%msr0-%msr1). In addition, the architecture supports a complete set of alternate integer and FP registers for fast context switching.

The resulting register file layout, along with the unified flattened register file indices, is shown at right. Although the indices in the picture range from 0 to 15, the actual set of valid indices depends on the type of index and (for relative indices) the register class as well:

| Relative unflattened | Int: 0-3; FP: 0-2; Misc: 0-1 |
| Unified unflattened   | 0-3, 8-10, 14-15             |
| Relative flattened   | Int: 0-7; FP: 0-5; Misc: 0-1 |
| Unified flattened     | 0-15                         |

In this example, register %f1 in the alternate FP register file could be referred to via the relative flattened index 4 as well as the relative unflattened index 1, the unified unflattened index 9, or the unified flattened index 12. Note that the difference between the relative and unified indices is always 8 (regardless of flattening), and the difference between the unflattened and flattened indices is 3 (regardless of relative vs. unified status). ![gem5-regs](/assets/img/gem5-regs.png)
# Caveats #
* Although the gem5 code is unfortunately not always clear about which type of register index is expected by a particular function, functions whose name incorporates a register class (e.g., readIntReg()) expect a relative register index, and functions that expect a flattened index often have "flat" in the function name.
* Although the general case is complicated, the common case can be deceptively simple. For example, because integer registers start at the beginning of the unified register space, relative and unified register indices are identical for integer registers. Furthermore, in an architecture with no (or rarely-used) alternate integer registers, the unflattened and flattened indices are (almost always) the same as well, meaning that all four types of register indices are interchangeable in this case. While this situation seems to be a simplification, it also tends to hide bugs where the wrong register index type is used.
* The description above is intended to illustrate the typical usage of these index types. There may be exceptions that don't precisely   follow this description, but I got tired of writing "typically" in every sentence.
* The terms 'relative' and 'unified' were invented for use in this documentation, so you are unlikely see them in the code until the code starts catching up with this page.
* This discussion pertains only to the architectural registers. An out-of-order CPU model such as O3 adds another layer of complexity by renaming these architectural registers (using the flattened register indices) to an underlying physical register file.


## ISA and CPU Independence ##

gem5 tries to keep CPU models ISA independent to make it easier to use any ISA with different CPU models. gem5 relies on two generic interfaces to make this independence possible: static instructions and execution context (both are discussed above).
Static instructions allow CPU to manage instructions and the execution context allow ISA or instructions to interact with the CPU. Following picture provides a high level overview of
what components in gem5 are ISA dependent or independent:

![ISA dependent or independent components of gem5](/assets/img/ISAInd.png)

**Source of the above figure:** Modular ISA-Independent Full-System Simulation (Ch 5 of Processor and System-on-Chip Simulation), G. Black, N. Binkert, and S. Reinhardt, A. Saidi.
[Link](https://link.springer.com/content/pdf/10.1007/978-1-4419-6175-4.pdf).


---


## Minor CPU Model

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu*

Minor CPU Model

This document contains a description of the structure and function of the
[Minor](http://doxygen.gem5.org/release/current/namespaceMinor.html) gem5 in-order
processor model.

It is recommended reading for anyone who wants to understand
[Minor](http://doxygen.gem5.org/release/current/namespaceMinor.html)'s internal
organisation, design decisions, C++ implementation and Python configuration. A
familiarity with gem5 and some of its internal structures is assumed. This
document is meant to be read alongside the
[Minor](http://doxygen.gem5.org/release/current/namespaceMinor.html) source code
and to explain its general structure without being too slavish about naming
every function and data type.

## What is Minor?

[Minor](http://doxygen.gem5.org/release/current/namespaceMinor.html) is an in-order
processor model with a fixed pipeline but configurable data structures and
execute behaviour. It is intended to be used to model processors with strict
in-order execution behaviour and allows visualisation of an instruction's
position in the pipeline through the MinorTrace/minorview.py format/tool. The
intention is to provide a framework for micro-architecturally correlating the
model with a particular, chosen processor with similar capabilities.

## Design Philosophy

### Multithreading

The model isn't currently capable of multithreading but there are THREAD
comments in key places where stage data needs to be arrayed to support
multithreading.

### Data structures

Decorating data structures with large amounts of life-cycle information is
avoided. Only instructions
([MinorDynInst](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html)) contain a
significant proportion of their data content whose values are not set at
construction.

All internal structures have fixed sizes on construction. Data held in queues
and FIFOs ([MinorBuffer](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorBuffer.html),
[FUPipeline](
http://doxygen.gem5.org/release/current/classMinor_1_1FUPipeline.html)) should have
a [BubbleIF](http://doxygen.gem5.org/release/current/classMinor_1_1BubbleIF.html)
interface to allow a distinct 'bubble'/no data value option for each type.

Inter-stage 'struct' data is packaged in structures which are passed by value.
Only [MinorDynInst](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html), the line
data in [ForwardLineData](
http://doxygen.gem5.org/release/current/classMinorCPU.html#a36a7ec6a8c5a6d27fd013d8b0238029d)
and the memory-interfacing objects [Fetch1::FetchRequest](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1_1_1FetchRequest.html)
and [LSQ::LSQRequest](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ_1_1LSQRequest.html) are
`::new` allocated while running the model.

## Model structure

Objects of class [MinorCPU](
http://doxygen.gem5.org/release/current/classMinorCPU.html) are provided by the
model to gem5. [MinorCPU](
http://doxygen.gem5.org/release/current/classMinorCPU.html) implements the
interfaces of (cpu.hh) and can provide data and instruction interfaces for
connection to a cache system. The model is configured in a similar way to other
gem5 models through Python. That configuration is passed on to
[MinorCPU::pipeline](
http://doxygen.gem5.org/release/current/classMinorCPU.html#a36a7ec6a8c5a6d27fd013d8b0238029d)
(of class [Pipeline](
http://doxygen.gem5.org/release/current/classMinor_1_1Pipeline.html)) which
actually implements the processor pipeline.

The hierarchy of major unit ownership from [MinorCPU](
http://doxygen.gem5.org/release/current/classMinorCPU.html) down looks like this:

```
MinorCPU
--- Pipeline - container for the pipeline, owns the cyclic 'tick' event mechanism and the idling (cycle skipping) mechanism.
--- --- Fetch1 - instruction fetch unit responsible for fetching cache lines (or parts of lines from the I-cache interface).
--- --- --- Fetch1::IcachePort - interface to the I-cache from Fetch1.
--- --- Fetch2 - line to instruction decomposition.
--- --- Decode - instruction to micro-op decomposition.
--- --- Execute - instruction execution and data memory interface.
--- --- --- LSQ - load store queue for memory ref. instructions.
--- --- --- LSQ::DcachePort - interface to the D-ache from Execute.
```

## Key data structures

### Instruction and line identity: Instld (`dyn_inst.hh`)

```
- T/S.P/L - for fetched cache lines
- T/S.P/L/F - for instructions before Decode
- T/S.P/L/F.E - for instructions from Decode onwards
```

for example:

```
- 0/10.12/5/6.7
```

[InstId](http://doxygen.gem5.org/release/current/classMinor_1_1InstId.html) fields
are:

|Field|Symbol|Generated by|Checked by|Function|
|:----|:-----|:-----------|:---------|:-------|
|InstId::threadId|T|[Fetch1](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) | Everywhere the thread number is needed| Thread number (currently always 0).
|InstId::streamSeqNum|S|[Execute](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html) | Fetch1, Fetch2, Execute (to discard lines/insts) | Stream sequence number as chosen by Execute. Stream sequence numbers change after changes of PC (branches, exceptions) in Execue and are used to separate pre and post brnach instrucion streams.|
|InstId::predictionSeqNum|[Fetch2](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html)| Fetch2 (while discarding lines after prediction)| Prediction sequence numbers represent branch prediction decisions. This is used by Fetch2 to mark lines/instructions/ according to the last followed branch prediction made by Fetch2. Fetch2 can signal to Fetch1 that it should change its fetch address and mark lines with a new prediction sequence number (which it will only do if the stream sequence number Fetch1 expects matches that of the request).
|InstId::lineSeqNum|[Fetch1](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html)| (just for debugging) | Line fetch sequence number of this cache line or the line this instruction was extracted from.|
|InstId::fetchSeqNum|[Fetch2](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) | Fetch2 (as the inst. sequence number for branches) | Instruction fetch order assigned by Fetch2 when lines are decomposed into instructions.|
|InstId::execSeqNum|[Decode](http://doxygen.gem5.org/release/current/classMinor_1_1Decode.html)|Execute (to check instruction identify in queues/FUs/LSQ| Instruction order after micro-op decomposition|

The sequence number fields are all independent of each other and although, for
instance, [InstId::execSeqNum](
http://doxygen.gem5.org/release/current/classMinor_1_1InstId.html#a064b0e4480268559e68510311be2a9b0)
for an instruction will always be >= [InstId::fetchSeqNum](
http://doxygen.gem5.org/release/current/classMinor_1_1InstId.html#a06677e68051a2a52f384e55e9368e33d),
the comparison is not useful.

The originating stage of each sequence number field keeps a counter for that
field which can be incremented in order to generate new, unique numbers.


### Instructi ns: MinorDynInst (`dyn_inst.hh`)

[MinorDynInst](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html) represents
an instruction's progression through the pipeline. An instruction can be three
things:

|Things                |Predicate                                                                                                                         |Explanation|
|:---------------------|:---------------------------------------------------------------------------------------------------------------------------------|:----------|
|A bubble              |[MinorDynInst::isBubble()](http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#a24e835fa495026ca63ffec43ee9cc07e) | no instruction at all, just a space-filler|
|A fault               |[MinorDynInst::isFault()](http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#a24029f3cd1835928d572737a548a824e)  | a fault to pass down the pipeline in an insturction's clothing|
|A decoded instruction |[MinorDynInst::isInst()](http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#adc55cdcf9f7c6588bb27eddb4c7fe38e)   | instructions are actually passed to the gem5 decoder in Fetch2 and so are created fully decoded. MinorDynInst::staticInst is the decoded instruction form. |

Instructions are reference counted using the gem5 [RefCountingPtr](
http://doxygen.gem5.org/release/current/classRefCountingPtr.html) 
([base/refcnt.hh](http://doxygen.gem5.org/release/current/refcnt_8hh.html))
wrapper. They therefore usually appear as MinorDynInstPtr in code. Note that as
[RefCountingPtr](http://doxygen.gem5.org/release/current/classRefCountingPtr.html)
initialises as nullptr rather than an object that supports
[BubbleIF::isBubble](
http://doxygen.gem5.org/release/current/classMinor_1_1BubbleIF.html#a7ce121301dba2e89b94235d96bf339ae)
passing raw MinorDynInstPtrs to [Queues](
http://doxygen.gem5.org/release/current/classMinor_1_1Queue.html) and other similar
structures from stage.hh without boxing is dangerous.

### ForwardLineData (`pipe_data.hh`)

ForwardLineData is used to pass cache lines from Fetch1 to Fetch2. Like
MinorDynInsts, they can be bubbles ([ForwardLineData::isBubble()](
http://doxygen.gem5.org/release/current/classMinor_1_1ForwardLineData.html#a46789690719acf167be0a57c9d7d4f8f)),
fault-carrying or can contain a line (partial line) fetched by Fetch1. The data
carried by ForwardLineData is owned by a Packet object returned from memory and
is explicitly memory managed and do must be deleted once processed (by Fetch2
deleting the Packet).

### ForwardInstData (`pipe_data.hh`)

ForwardInstData can contain up to [ForwardInstData::width()](
http://doxygen.gem5.org/release/current/classMinor_1_1ForwardInstData.html#ad5db21f655f2f1dfff69e6f6d5cc606e)
instructions in its [ForwardInstData::insts](
http://doxygen.gem5.org/release/current/classMinor_1_1ForwardInstData.html#ab54a61c683376aaf5a12ea19ab758340)
vector. This structure is used to carry instructions between Fetch2, Decode and
Execute and to store input buffer vectors in Decode and Execute.

### Fetch1::FetchRequest (`fetch1.hh`)

FetchRequests represent I-cache line fetch requests. The are used in the memory
queues of Fetch1 and are pushed into/popped from [Packet::senderState](
http://doxygen.gem5.org/release/current/classPacket.html#ad1dd4fa4370e508806fe4a8253a0ad12)
while traversing the memory system.

FetchRequests contain a memory system Request ([mem/request.hh](
http://doxygen.gem5.org/release/current/request_8hh.html)) for that fetch access, a
packet (Packet, [mem/packet.hh](
http://doxygen.gem5.org/release/current/packet_8hh.html)), if the request gets to
memory, and a fault field that can be populated with a TLB-sourced prefetch
fault (if any).

### LSQ::LSQRequest (`execute.hh`)

LSQRequests are similar to FetchRequests but for D-cache accesses. They carry
the instruction associated with a memory access.

## The pipeline

```
------------------------------------------------------------------------------
    Key:

    [] : inter-stage BufferBuffer
    ,--.
    |  | : pipeline stage
    `--'
    ---> : forward communication
    <--- : backward communication

    rv : reservation information for input buffers

                ,------.     ,------.     ,------.     ,-------.
 (from  --[]-v->|Fetch1|-[]->|Fetch2|-[]->|Decode|-[]->|Execute|--> (to Fetch1
 Execute)    |  |      |<-[]-|      |<-rv-|      |<-rv-|       |     & Fetch2)
             |  `------'<-rv-|      |     |      |     |       |
             `-------------->|      |     |      |     |       |
                             `------'     `------'     `-------'
------------------------------------------------------------------------------
```

The four pipeline stages are connected together by [MinorBuffer](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorBuffer.html) FIFO
(stage.hh, derived ultimately from [TimeBuffer](
http://doxygen.gem5.org/release/current/classTimeBuffer.html)) structures which
allow inter-stage delays to be modelled. There is a [MinorBuffers](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorBuffer.html) between
adjacent stages in the forward direction (for example: passing lines from
Fetch1 to Fetch2) and, between Fetch2 and Fetch1, a buffer in the backwards
direction carrying branch predictions.

Stages Fetch2, Decode and Execute have input buffers which, each cycle, can
accept input data from the previous stage and can hold that data if the stage
is not ready to process it. Input buffers store data in the same form as it is
received and so Decode and Execute's input buffers contain the output
instruction vector ([ForwardInstData](
http://doxygen.gem5.org/release/current/classMinor_1_1ForwardInstData.html)
([pipe_data.hh](http://doxygen.gem5.org/release/current/pipe__data_8hh.html))) from
their previous stages with the instructions and bubbles in the same positions
as a single buffer entry.

Stage input buffers provide a [Reservable](
http://doxygen.gem5.org/release/current/classMinor_1_1Reservable.html) (stage.hh)
interface to their previous stages, to allow slots to be reserved in their
input buffers, and communicate their input buffer occupancy backwards to allow
the previous stage to plan whether it should make an output in a given cycle.

### Event handling: MinorActivityRecorder (`activity.hh`, `pipeline.hh`)

Minor is essentially a cycle-callable model with some ability to skip cycles
based on pipeline activity. External events are mostly received by callbacks
(e.g. [Fetch1::IcachePort::recvTimingResp](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1_1_1IcachePort.html#aec62b3d89dfe61e8528cdcdf3729eeab))
and cause the pipeline to be woken up to service advancing request queues.

[Ticked](http://doxygen.gem5.org/release/current/classgem5_1_1Ticked.html) (sim/ticked.hh)
is a base class bringing together an evaluate member function and a provided
[SimObject](http://doxygen.gem5.org/release/current/classgem5_1_1SimObject.html). It
provides a [Ticked::start](
http://doxygen.gem5.org/release/current/classTicked.html#a798d1e248c27161de6eb2bc6fef5e425)/stop
interface to start and pause clock events from being periodically issued.
[Pipeline](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Pipeline.html) is
a derived class of Ticked.

During evaluate calls, stages can signal that they still have work to do in the
next cycle by calling either [MinorCPU::activityRecorder](
http://doxygen.gem5.org/release/current/classgem5_1_1MinorCPU.html#ae3b03c96ee234e2c5c6c68f4567245a7)->activity()
(for non-callable related activity) or MinorCPU::wakeupOnEvent(<stageId>) (for
stage callback-related 'wakeup' activity).

[Pipeline::evaluate](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Pipeline.html#af07fdce00c8937e9de5b6450a1cd62bf)
contains calls to evaluate for each unit and a test for pipeline idling which
can turns off the clock tick if no unit has signalled that it may become active
next cycle.

Within Pipeline ([pipeline.hh](
http://doxygen.gem5.org/release/current/pipeline_8hh.html)), the stages are
evaluated in reverse order (and so will ::evaluate in reverse order) and their
backwards data can be read immediately after being written in each cycle
allowing output decisions to be 'perfect' (allowing synchronous stalling of the
whole pipeline). Branch predictions from Fetch2 to Fetch1 can also be
transported in 0 cycles making fetch1ToFetch2BackwardDelay the only
configurable delay which can be set as low as 0 cycles.

The [MinorCPU::activateContext](
http://doxygen.gem5.org/release/current/classgem5_1_1MinorCPU.html#a854596342bfb9dd889437e494c4ddb27)
and [MinorCPU::suspendContext](
http://doxygen.gem5.org/release/current/classgem5_1_1MinorCPU.html#ae6aa9b1bb798d8938f0b35e11d9e68b8)
interface can be called to start and pause threads (threads in the MT sense)
and to start and pause the pipeline. Executing instructions can call this
interface (indirectly through the ThreadContext) to idle the CPU/their threads.

### Each pipeline stage

In general, the behaviour of a stage (each cycle) is:

```
    evaluate:
        push input to inputBuffer
        setup references to input/output data slots

        do 'every cycle' 'step' tasks

        if there is input and there is space in the next stage:
            process and generate a new output
            maybe re-activate the stage

        send backwards data

        if the stage generated output to the following FIFO:
            signal pipe activity

        if the stage has more processable input and space in the next stage:
            re-activate the stage for the next cycle

        commit the push to the inputBuffer if that data hasn't all been used
```

The Execute stage differs from this model as its forward output (branch) data
is unconditionally sent to Fetch1 and Fetch2. To allow this behaviour, Fetch1
and Fetch2 must be unconditionally receptive to that data.

### Fetch1 stage

[Fetch1](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) is
responsible for fetching cache lines or partial cache lines from the I-cache
and passing them on to [Fetch2](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) to be decomposed
into instructions. It can receive 'change of stream' indications from both
[Execute](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html) and
[Fetch2](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) to
signal that it should change its internal fetch address and tag newly fetched
lines with new stream or prediction sequence numbers. When both Execute and
[Fetch2](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) signal
changes of stream at the same time, [Fetch1](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) takes
[Execute](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html)'s
change.

Every line issued by [Fetch1](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) will bear a
unique line sequence number which can be used for debugging stream changes.

When fetching from the I-cache, [Fetch1](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html)  will ask for
data from the current fetch address (Fetch1::pc) up to the end of the 'data
snap' size set in the parameter fetch1LineSnapWidth. Subsequent autonomous line
fetches will fetch whole lines at a snap boundary and of size fetch1LineWidth.

[Fetch1](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) will
only initiate a memory fetch if it can reserve space in [Fetch2](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) input buffer.
That input buffer serves an the fetch queue/LFL for the system.

[Fetch1](http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html)
contains two queues: requests and transfers to handle the stages of translating
the address of a line fetch (via the TLB) and accommodating the
request/response of fetches to/from memory.

Fetch requests from [Fetch1](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) are pushed into
the requests queue as newly allocated FetchRequest objects once they have been
sent to the ITLB with a call to itb->translateTiming.

A response from the TLB moves the request from the requests queue to the
transfers queue. If there is more than one entry in each queue, it is possible
to get a TLB response for request which is not at the head of the requests
queue. In that case, the TLB response is marked up as a state change to
Translated in the request object, and advancing the request to transfers (and
the memory system) is left to calls to [Fetch1::stepQueues](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html#ac143710b93ec9f55bfc3e2882ef2fe4c)
which is called in the cycle following any event is received.

[Fetch1::tryToSendToTransfers](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html#a9ace21e8131caf360190ea876cfa2934)
---
layout: documentation
title: Execution Basics
doc: gem5 documentation
parent: cpu_models
permalink: /documentation/general_docs/cpu_models/execution_basics
---

is responsible for moving requests between the two queues and issuing requests
to memory. Failed TLB lookups (prefetch aborts) continue to occupy space in the
queues until they are recovered at the head of transfers.

Responses from memory change the request object state to Complete and
[Fetch1::evaluate](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html#a68a0a88ce6ee3dd170c977318cfb4ca9)
can pick up response data, package it in the [ForwardLineData](
http://doxygen.gem5.org/release/current/classMinor_1_1ForwardLineData.html) object,
and forward it to [Fetch2](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html)'s input buffer.

As space is always reserved in [Fetch2::inputBuffer](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html#afdaa27275e2f605d9aaa637e8c39f96d),
setting the input buffer's size to 1 results in non-prefetching behaviour.

When a change of stream occurs, translated requests queue members and completed
transfers queue members can be unconditionally discarded to make way for new
transfers.

### Fetch2 stage

Fetch2 receives a line from Fetch1 into its input buffer. The data in the head
line in that buffer is iterated over and separated into individual instructions
which are packed into a vector of instructions which can be passed to
[Decode](http://doxygen.gem5.org/release/current/classMinor_1_1Decode.html).
Packing instructions can be aborted early if a fault is found in either the
input line as a whole or a decomposed instruction.

#### Branch prediction

Fetch2 contains the branch prediction mechanism. This is a wrapper around the branch predictor interface provided by gem5 (cpu/pred/...).

Branches are predicted for any control instructions found. If prediction is
attempted for an instruction, the [MinorDynInst::triedToPredict](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#a905b0516019ae7f47b5795ceda33f5cd)
flag is set on that instruction.

When a branch is predicted to take, the [MinorDynInst::predictedTaken](http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#aa57659ef9d30162ddcf10fcb0f3963ac) flag is set and [MinorDynInst::predictedTarget](http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#a5eaf9547bcaefa2c0fd37f32c828691b) is set to the predicted target PC value. The predicted branch instruction is then packed into Fetch2's output vector, the prediction sequence number is incremented, and the branch is communicated to Fetch1.

After signalling a prediction, Fetch2 will discard its input buffer contents
and will reject any new lines which have the same stream sequence number as
that branch but have a different prediction sequence number. This allows
following sequentially fetched lines to be rejected without ignoring new lines
generated by a change of stream indicated from a 'real' branch from Execute
(which will have a new stream sequence number).

The program counter value provided to Fetch2 by Fetch1 packets is only updated
when there is a change of stream. Fetch2::havePC indicates whether the PC will
be picked up from the next processed input line. Fetch2::havePC is necessary to
allow line-wrapping instructions to be tracked through decode.

Branches (and instructions predicted to branch) which are processed by Execute
will generate BranchData ([pipe_data.hh](
http://doxygen.gem5.org/release/current/pipe__data_8hh.html)) data explaining the
outcome of the branch which is sent forwards to Fetch1 and Fetch2. Fetch1 uses
this data to change stream (and update its stream sequence number and address
for new lines). Fetch2 uses it to update the branch predictor. Minor does not
communicate branch data to the branch predictor for instructions which are
discarded on the way to commit.

BranchData::BranchReason ([pipe_data.hh](
http://doxygen.gem5.org/release/current/pipe__data_8hh.html)) encodes the possible
branch scenarios:


|Branch enum val.          | In Execute                                                   | Fetch1 reaction                                                        | Fetch2 reaction             |
|:-------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------------------|:----------------------------|
|No Branch                 |(output bubble data)                                          |-                                                                       |-                            |
|CorrectlyPredictedBranch  |Predicted, taken                                              |-                                                                       |Update BP as taken branch    |
|UnpredictedBranch         |Not predicted, taken and was taken                            |New stream                                                              |Update BP as taken branch    |
|BadlyPredictedBranch      |Predicted, not taken                                          |New stream to restore to old Inst. source                               |Update BP as not taken branch|
|BadlyPredictedBranchTarget|Predicted, taken, but to a different target than predicted one|New stream                                                              |Update BTB to new target     |
|SuspendThread             |Hint to suspend fetch                                         |Suspend fetch for this thread (branch to next inst. as wakeup fetch addr|-                            |
|Interrupt                 |Interrupt detected                                            |New stream                                                              |-                            |


---
layout: documentation
title: Execution Basics
doc: gem5 documentation
parent: cpu_models
permalink: /documentation/general_docs/cpu_models/execution_basics
---

### Decode Stage

[Decode](http://doxygen.gem5.org/release/current/classMinor_1_1Decode.html) takes a
vector of instructions from [Fetch2](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html) (via its input
buffer) and decomposes those instructions into micro-ops (if necessary) and
packs them into its output instruction vector.

The parameter executeInputWidth sets the number of instructions which can be
packed into the output per cycle. If the parameter decodeCycleInput is true,
[Decode](http://doxygen.gem5.org/release/current/classMinor_1_1Decode.html) can try
to take instructions from more than one entry in its input buffer per cycle.

### Execute Stage

Execute provides all the instruction execution and memory access mechanisms. An
instructions passage through Execute can take multiple cycles with its precise
timing modelled by a functional unit pipeline FIFO.

A vector of instructions (possibly including fault 'instructions') is provided
to Execute by Decode and can be queued in the Execute input buffer before being
issued. Setting the parameter executeCycleInput allows execute to examine more
than one input buffer entry (more than one instruction vector). The number of
instructions in the input vector can be set with executeInputWidth and the
depth of the input buffer can be set with parameter executeInputBufferSize.

#### Functional units

The Execute stage contains pipelines for each functional unit comprising the
computational core of the CPU. Functional units are configured via the
executeFuncUnits parameter. Each functional unit has a number of instruction
classes it supports, a stated delay between instruction issues, and a delay
from instruction issue to (possible) commit and an optional timing annotation
capable of more complicated timing.

Each active cycle, [Execute::evaluate](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#a2d6ca9a694bf99ef82da7759cba8c3da)
performs this action:

```
    Execute::evaluate:
        push input to inputBuffer
        setup references to input/output data slots and branch output slot

        step D-cache interface queues (similar to Fetch1)

        if interrupt posted:
            take interrupt (signalling branch to Fetch1/Fetch2)
        else
            commit instructions
            issue new instructions

        advance functional unit pipelines

        reactivate Execute if the unit is still active

        commit the push to the inputBuffer if that data hasn't all been used
```

#### Functional unit FIFOs



Functional units are implemented as SelfStallingPipelines (stage.hh). These are
[TimeBuffer](http://doxygen.gem5.org/release/current/classTimeBuffer.html) FIFOs
with two distinct 'push' and 'pop' wires. They respond to
[SelfStallingPipeline::advance](
http://doxygen.gem5.org/release/current/classMinor_1_1SelfStallingPipeline.html#ad933640bc6aab559c009302e478c3768)
in the same way as TimeBuffers unless there is data at the far, 'pop', end of
the FIFO. A 'stalled' flag is provided for signalling stalling and to allow a
stall to be cleared. The intention is to provide a pipeline for each functional
unit which will never advance an instruction out of that pipeline until it has
been processed and the pipeline is explicitly unstalled.

The actions 'issue', 'commit', and 'advance' act on the functional units.

#### Issue

Issuing instructions involves iterating over both the input buffer instructions
and the heads of the functional units to try and issue instructions in order.
The number of instructions which can be issued each cycle is limited by the
parameter executeIssueLimit, how executeCycleInput is set, the availability of
---
layout: documentation
title: Execution Basics
doc: gem5 documentation
parent: cpu_models
permalink: /documentation/general_docs/cpu_models/execution_basics
---

pipeline space and the policy used to choose a pipeline in which the
instruction can be issued.

At present, the only issue policy is strict round-robin visiting of each
pipeline with the given instructions in sequence. For greater flexibility,
better (and more specific policies) will need to be possible.

Memory operation instructions traverse their functional units to perform their
EA calculations. On 'commit', the [ExecContext](
http://doxygen.gem5.org/release/current/classMinor_1_1ExecContext.html)::initiateAcc
execution phase is performed and any memory access is issued (via.
ExecContext::{read,write}Mem calling [LSQ::pushRequest](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ.html#a18594a4baa4eef7bfc3be45c03f4d544))
to the [LSQ](http://doxygen.gem5.org/release/current/classMinor_1_1LSQ.html).

Note that faults are issued as if they are instructions and can (currently) be
issued to any functional unit.

Every issued instruction is also pushed into the Execute::inFlightInsts queue.
Memory ref. instructions are pushing into Execute::inFUMemInsts queue.

#### Commit

Instructions are committed by examining the head of the Execute::inFlightInsts
queue (which is decorated with the functional unit number to which the
instruction was issued). Instructions which can then be found in their
functional units are executed and popped from Execute::inFlightInsts.

Memory operation instructions are committed into the memory queues (as
described above) and exit their functional unit pipeline but are not popped
from the Execute::inFlightInsts queue. The Execute::inFUMemInsts queue provides
ordering to memory operations as they pass through the functional units
(maintaining issue order). On entering the LSQ, instructions are popped from
Execute::inFUMemInsts.

If the parameter executeAllowEarlyMemoryIssue is set, memory operations can be
sent from their FU to the LSQ before reaching the head of
Execute::inFlightInsts but after their dependencies are met.
[MinorDynInst::instToWaitFor](
http://doxygen.gem5.org/release/current/classMinor_1_1MinorDynInst.html#ac72a9dcff570bbaf24da9ee74392e6d0)
is marked up with the latest dependent instruction execSeqNum required to be
committed for a memory operation to progress to the LSQ.

Once a memory response is available (by testing the head of
Execute::inFlightInsts against [LSQ::findResponse](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ.html#a458abe5d220a0f66600bf339bceb2100)),
commit will process that response (ExecContext::completeAcc) and pop the
instruction from Execute::inFlightInsts.

Any branch, fault or interrupt will cause a stream sequence number change and
signal a branch to Fetch1/Fetch2. Only instructions with the current stream
sequence number will be issued and/or committed.

#### Advance

All non-stalled pipeline are advanced and may, thereafter, become stalled.
Potential activity in the next cycle is signalled if there are any instructions
remaining in any pipeline.

#### Scoreboard

The scoreboard ([Scoreboard](
http://doxygen.gem5.org/release/current/classMinor_1_1Scoreboard.html)) is used to
control instruction issue. It contains a count of the number of in flight
instructions which will write each general purpose CPU integer or float
register. Instructions will only be issued where the scoreboard contains a
count of 0 instructions which will write to one of the instructions source
registers.

Once an instruction is issued, the scoreboard counts for each destination
register for an instruction will be incremented.

The estimated delivery time of the instruction's result is marked up in the scoreboard by adding the length of the issued-to FU to the current time. The timings parameter on each FU provides a list of additional rules for calculating the delivery time. These are documented in the parameter comments in MinorCPU.py.

On commit, (for memory operations, memory response commit) the scoreboard counters for an instruction's source registers are decremented. will be decremented.

#### Execute::inFlightInsts

The Execute::inFlightInsts queue will always contain all instructions in flight
in [Execute](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html) in
the correct issue order. [Execute::issue](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#af0b90170a273f1a0d41f4164ba3fe456)
is the only process which will push an instruction into the queue.
[Execute::commit](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#ac2da0ae4202602ce4ad976f33a004237)
is the only process that can pop an instruction.

#### LSQ

The [LSQ](http://doxygen.gem5.org/release/current/classMinor_1_1LSQ.html) can
support multiple outstanding transactions to memory in a number of conservative
cases.

There are three queues to contain requests: requests, transfers and the store
buffer. The requests and transfers queue operate in a similar manner to the
queues in Fetch1. The store buffer is used to decouple the delay of completing
store operations from following loads.

Requests are issued to the DTLB as their instructions leave their functional
unit. At the head of requests, cacheable load requests can be sent to memory
and on to the transfers queue. Cacheable stores will be passed to transfers
unprocessed and progress that queue maintaining order with other transactions.

The conditions in [LSQ::tryToSendToTransfers](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ.html#a7d7b8ddc7c69fd9eb3b8594fe261d8e8)
dictate when requests can be sent to memory.

All uncacheable transactions, split transactions and locked transactions are
processed in order at the head of requests. Additionally, store results
residing in the store buffer can have their data forwarded to cacheable loads
(removing the need to perform a read from memory) but no cacheable load can be
issue to the transfers queue until that queue's stores have drained into the
store buffer.

At the end of transfers, requests which are [LSQ::LSQRequest::Complete](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ_1_1LSQRequest.html#a429d50f5dd6be4217d5dba93f8c289d3a81b9dbf6670e396d0266949d59b57428)
(are faulting, are cacheable stores, or have been sent to memory and received a
response) can be picked off by Execute and either committed
(ExecContext::completeAcc) and, for stores, be sent to the store buffer.

Barrier instructions do not prevent cacheable loads from progressing to memory
but do cause a stream change which will discard that load. Stores will not be
committed to the store buffer if they are in the shadow of the barrier but
before the new instruction stream has arrived at Execute. As all other memory
transactions are delayed at the end of the requests queue until they are at the
head of Execute::inFlightInsts, they will be discarded by any barrier stream
change.

After commit, [LSQ::BarrierDataRequest](
http://doxygen.gem5.org/release/current/classMinor_1_1LSQ_1_1BarrierDataRequest.html)
requests are inserted into the store buffer to track each barrier until all
preceding memory transactions have drained from the store buffer. No further
memory transactions will be issued from the ends of FUs until after the barrier
has drained.

#### Draining

Draining is mostly handled by the [Execute](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html) stage. When
initiated by calling [MinorCPU::drain](
http://doxygen.gem5.org/release/current/classMinorCPU.html#a3191c9247cd80dfc603bfcd154cf09a0),
[Pipeline::evaluate](
http://doxygen.gem5.org/release/current/classMinor_1_1Pipeline.html#af07fdce00c8937e9de5b6450a1cd62bf)
checks the draining status of each unit each cycle and keeps the pipeline
active until draining is complete. It is Pipeline that signals the completion
of draining. Execute is triggered by [MinorCPU::drain](
http://doxygen.gem5.org/release/current/classMinorCPU.html#a3191c9247cd80dfc603bfcd154cf09a0)
and starts stepping through its [Execute::DrainState](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40)
state machine, starting from state Execute::NotDraining, in this order:

|State|Meaning|
|[Execute::NotDraining](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40aeecf47987ef0d4aa0a6a59403d085ec9)|Not trying to drain, normal execution|
|[Execute::DrainCurrentInst](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40aec53785380b6256e2baa889739311570)|Draining micro-ops to complete inst.|
|[Execute::DrainHaltFetch](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40a516d421a79c458d376bedeb067fc207f)|Halt fetching instructions|
|[Execute::DrainAllInsts](http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40ade3ca2567fed8d893896d71bb95f13ca)|Discarding all instructions presented|

When complete, a drained Execute unit will be in the [Execute::DrainAllInsts](
http://doxygen.gem5.org/release/current/classMinor_1_1Execute.html#aeb21dbbbbde40d8cdc68e9b17ddd3d40ade3ca2567fed8d893896d71bb95f13ca)
state where it will continue to discard instructions but has no knowledge of
the drained state of the rest of the model.

## Debug options

The model provides a number of debug flags which can be passed to gem5 with the
`–debug-flags` option.

The available flags are:

|Debug flag      | Unit which will generate debugging output |
|:---------------|:------------------------------------------|
|Activity        | [Debug](http://doxygen.gem5.org/release/current/namespaceDebug.html) ActivityMonitor actions |
|Branch          | [Fetch2](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch2.html) and [Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) branch prediction decisions |
|[MinorCPU](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1MinorCPU.html)      | CPU global actions such as wakeup/thread suspension |
|[Decode](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Decode.html) | [Decode](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Decode.html) |
|MinorExec       | [Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) behaviour |
|Fetch           |[Fetch1](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch1.html) and [Fetch2](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch2.html) |
|MinorInterrupt  | [Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) interrupt handling  |
|MinorMem        | [Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) memory interactions |
|MinorScoreboard | [Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) scoreboard activity |
|MinorTrace      | Generate MinorTrace cyclic state trace output (see below) |
|MinorTiming     | MinorTiming instruction timing modification operations    |

The group flag [Minor](http://doxygen.gem5.org/release/current/namespaceminor.html)
enables all the flags beginning with [Minor](
http://doxygen.gem5.org/release/current/namespaceMinor.html).

## MinorTrace and minorview.py

The debug flag MinorTrace causes cycle-by-cycle state data to be printed which
can then be processed and viewed by the minorview.py tool. This output is very
verbose and so it is recommended it only be used for small examples.

### MinorTrace format

There are three types of line outputted by MinorTrace:

#### MinorTrace - Ticked unit cycle state

For example:

```
 110000: system.cpu.dcachePort: MinorTrace: state=MemoryRunning in_tlb_mem=0/0
```

For each time step, the MinorTrace flag will cause one MinorTrace line to be
printed for every named element in the model.

#### MinorInst - summaries of instructions issued by Decode

[Decode](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Decode.html)

For example:

```
 140000: system.cpu.execute: MinorInst: id=0/1.1/1/1.1 addr=0x5c \
                             inst="  mov r0, #0" class=IntAlu
```

MinorInst lines are currently only generated for instructions which are committed.

#### MinorLine - summaries of line fetches issued by Fetch1

[Fetch1](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch1.html)

For example:

```
  92000: system.cpu.icachePort: MinorLine: id=0/1.1/1 size=36 \
                                vaddr=0x5c paddr=0x5c
```

### minorview.py

Minorview (util/minorview.py) can be used to visualise the data created by
MinorTrace.

```
usage: minorview.py [-h] [--picture picture-file] [--prefix name]
                   [--start-time time] [--end-time time] [--mini-views]
                   event-file

Minor visualiser

positional arguments:
  event-file

optional arguments:
  -h, --help            show this help message and exit
  --picture picture-file
                        markup file containing blob information (default:
                        <minorview-path>/minor.pic)
  --prefix name         name prefix in trace for CPU to be visualised
                        (default: system.cpu)
  --start-time time     time of first event to load from file
  --end-time time       time of last event to load from file
  --mini-views          show tiny views of the next 10 time steps
```

Raw debugging output can be passed to minorview.py as the event-file. It will
pick out the MinorTrace lines and use other lines where units in the simulation
are named (such as system.cpu.dcachePort in the above example) will appear as
'comments' when units are clicked on the visualiser.

Clicking on a unit which contains instructions or lines will bring up a speech
bubble giving extra information derived from the MinorInst/MinorLine lines.

`–start-time` and `–end-time` allow only sections of debug files to be loaded.

`–prefix` allows the name prefix of the CPU to be inspected to be supplied.
This defaults to `system.cpu`.

In the visualiser, The buttons Start, End, Back, Forward, Play and Stop can be
used to control the displayed simulation time.

The diagonally striped coloured blocks are showing the [InstId](
http://doxygen.gem5.org/release/current/classMinor_1_1InstId.html) of the
instruction or line they represent. Note that lines in [Fetch1](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch1.html) and f1ToF2.F
only show the id fields of a line and that instructions in [Fetch2](
http://doxygen.gem5.org/release/current/classMinor_1_1Fetch2.html), f2ToD, and
decode.inputBuffer do not yet have execute sequence numbers. The T/S.P/L/F.E
buttons can be used to toggle parts of [InstId](
http://doxygen.gem5.org/release/current/classMinor_1_1InstId.html) on and off to
make it easier to understand the display. Useful combinations are:

|Combination|Reason                                                                                                                      |
|:----------|:---------------------------------------------------------------------------------------------------------------------------|
|E          |just show the final execute sequence number                                                                                 |
|F/E        |show the instruction-related numbers                                                                                        |
|S/P        |show just the stream-related numbers (watch the stream sequence change with branches and not change with predicted branches)|
|S/E        |show instructions and their stream                                                                                          |

The key to the right shows all the displayable colours (some of the colour
choices are quite bad!):

|Symbol |Meaning                                                      |
|:------|:------------------------------------------------------------|
|U      |Uknown data                                                  |
|B      |Blocked stage                                                |
|-      |Bubble                                                       |
|E      |Empty queue slot                                             |
|R      |Reserved queue slot                                          |
|F      |Fault                                                        |
|r      |Read (used as the leftmost stripe on data in the dcachePort) |
|w      |Write " "                                                    |
|0 to 9 |last decimal digit of the corresponding data                 |

```
    ,---------------.         .--------------.  *U
    | |=|->|=|->|=| |         ||=|||->||->|| |  *-  <- Fetch queues/LSQ
    `---------------'         `--------------'  *R
    === ======                                  *w  <- Activity/Stage activity
                              ,--------------.  *1
    ,--.      ,.      ,.      | ============ |  *3  <- Scoreboard
    |  |-\[]-\||-\[]-\||-\[]-\| ============ |  *5  <- Execute::inFlightInsts
    |  | :[] :||-/[]-/||-/[]-/| -. --------  |  *7
    |  |-/[]-/||  ^   ||      |  | --------- |  *9
    |  |      ||  |   ||      |  | ------    |
[]->|  |    ->||  |   ||      |  | ----      |
    |  |<-[]<-||<-+-<-||<-[]<-|  | ------    |->[] <- Execute to Fetch1,
    '--`      `'  ^   `'      | -' ------    |        Fetch2 branch data
             ---. |  ---.     `--------------'
             ---' |  ---'       ^       ^
                  |   ^         |       `------------ Execute
  MinorBuffer ----' input       `-------------------- Execute input buffer
                    buffer
```

Stages show the colours of the instructions currently being
generated/processed.

Forward FIFOs between stages show the data being pushed into them at the
current tick (to the left), the data in transit, and the data available at
their outputs (to the right).

The backwards FIFO between [Fetch2](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch2.html) and [Fetch1](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch1.html) shows branch
prediction data.

In general, all displayed data is correct at the end of a cycle's activity at
the time indicated but before the inter-stage FIFOs are ticked. Each FIFO has,
therefore an extra slot to show the asserted new input data, and all the data
currently within the FIFO.

Input buffers for each stage are shown below the corresponding stage and show
the contents of those buffers as horizontal strips. Strips marked as reserved
(cyan by default) are reserved to be filled by the previous stage. An input
buffer with all reserved or occupied slots will, therefore, block the previous
stage from generating output.

Fetch queues and [LSQ](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1LSQ.html) show the
lines/instructions in the queues of each interface and show the number of
lines/instructions in TLB and memory in the two striped colours of the top of
their frames.

Inside [Execute](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html), the horizontal
bars represent the individual FU pipelines. The vertical bar to the left is the
input buffer and the bar to the right, the instructions committed this cycle.
The background of [Execute](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) shows
instructions which are being committed this cycle in their original FU pipeline
positions.

The strip at the top of the [Execute](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) block shows the
current streamSeqNum that [Execute](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) is committing.
A similar stripe at the top of [Fetch1](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch1.html) shows that
stage's expected streamSeqNum and the stripe at the top of [Fetch2](
http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Fetch2.html) shows its
issuing predictionSeqNum.

The scoreboard shows the number of instructions in flight which will commit a
result to the register in the position shown. The scoreboard contains slots for
each integer and floating point register.

The Execute::inFlightInsts queue shows all the instructions in flight in
[Execute](http://doxygen.gem5.org/release/current/classgem5_1_1minor_1_1Execute.html) with
the oldest instruction (the next instruction to be committed) to the right.

`Stage activity` shows the signalled activity (as E/1) for each stage (with CPU
miscellaneous activity to the left)

`Activity` show a count of stage and pipe activity.

### minor.pic format

The minor.pic file (src/minor/minor.pic) describes the layout of the models
blocks on the visualiser. Its format is described in the supplied minor.pic
file.


---


## Out of order CPU model

*Source: https://www.gem5.org/documentation//general_docs/cpu_models/O3CPU*

# **O3CPU**

Table of Contents

 1. [Pipeline stages](##Pipeline-stages)
 2. [Execute-in-execute model](##Execute-in-execute-model)
 3. [Template Policies](##Template-Policies)
 4. [ISA independence](##ISA-independence)
 5. [Interaction with ThreadContext](##Interaction-with-ThreadContext**)

The O3CPU is our new detailed model for the v2.0 release. It is an out of order CPU model loosely based on the Alpha 21264. This page will give you a general overview of the O3CPU model, the pipeline stages and the pipeline resources. We have made efforts to keep the code well documented, so please browse the code for exact details on how each part of the O3CPU works.


## **Pipeline stages**
* Fetch
  
     Fetches instructions each cycle, selecting which thread to fetch from based on the policy selected. This stage is where the DynInst is first created. Also handles branch prediction.
    
* Decode
  
  Decodes instructions each cycle. Also handles early resolution of PC-relative unconditional branches.

* Rename
  
  Renames instructions using a physical register file with a free list. Will stall if there are not enough registers to rename to, or if back-end resources have filled up. Also handles any serializing instructions at this point by stalling them in rename until the back-end drains.

* Issue/Execute/Writeback
  
  Our simulator model handles both execute and writeback when the execute() function is called on an instruction, so we have combined these three stages into one stage. This stage (IEW) handles dispatching instructions to the instruction queue, telling the instruction queue to issue instruction, and executing and writing back instructions.

* Commit
  
   Commits instructions each cycle, handling any faults that the instructions may have caused. Also handles redirecting the front-end in the case of a branch misprediction.


## **Execute-in-execute model**

For the O3CPU, we've made efforts to make it highly timing accurate. In order to do this, we use a model that actually executes instructions at the execute stage of the pipeline. Most simulator models will execute instructions either at the beginning or end of the pipeline; SimpleScalar and our old detailed CPU model both execute instructions at the beginning of the pipeline and then pass it to a timing backend. This presents two potential problems: first, there is the potential for error in the timing backend that would not show up in program results. Second, by executing at the beginning of the pipeline, the instructions are all executed in order and out-of-order load interaction is lost. Our model is able to avoid these deficiencies and provide an accurate timing model.

## **Template Policies**

The O3CPU makes heavy use of template policies to obtain a level of polymorphism without having to use virtual functions. It uses template policies to pass in an "Impl" to almost all of the classes used within the O3CPU. This Impl has defined within it all of the important classes for the pipeline, such as the specific Fetch class, Decode class, specific DynInst types, the CPU class, etc. It allows any class that uses it as a template parameter to be able to obtain full type information of any of the classes defined within the Impl. By obtaining full type information, there is no need for the traditional virtual functions/base classes which are normally used to provide polymorphism. The main drawback is that the CPU must be entirely defined at compile time, and that the templated classes require manual instantiation. See `src/cpu/o3/impl.hh ` and `src/cpu/o3/cpu_policy.hh` for example Impl classes.

## **ISA independence**

The O3CPU has been designed to try to separate code that is ISA dependent and code that is ISA independent. The pipeline stages and resources are all mainly ISA independent, as well as the lower level CPU code. The ISA dependent code implements ISA-specific functions. For example, the AlphaO3CPU implements Alpha-specific functions, such as hardware return from error interrupt (hwrei()) or reading the interrupt flags. The lower level CPU, the FullO3CPU, handles orchestrating all of the pipeline stages and handling other ISA-independent actions. We hope this separation makes it easier to implement future ISAs, as hopefully only the high level classes will have to be redefined.

## **Interaction with ThreadContext**

The [ThreadContext](/documentation/general_docs/cpu_models/execution_basics) provides interface for external objects to access thread state within the CPU. However, this is slightly complicated by the fact that the O3CPU is an out-of-order CPU. While it is well defined what the architectural state is at any given cycle, it is not well defined what happens if that architectural state is changed. Thus it is feasible to do reads to the ThreadContext without much effort, but doing writes to the ThreadContext and altering register state requires the CPU to flush the entire pipeline. This is because there may be in flight instructions that depend on the register that has been changed, and it is unclear if they should or should not view the register update. Thus accesses to the ThreadContext have the potential to cause slowdown in the CPU simulation.

## **Backend Pipeline**
### Compute Instructions
Compute instructions are simpler as they do not access memory and
do not interact with the LSQ. Included below is a high-level calling chain
(only important functions) with a description about the functionality of each.

```cpp
Rename::tick()->Rename::RenameInsts()
IEW::tick()->IEW::dispatchInsts()
IEW::tick()->InstructionQueue::scheduleReadyInsts()
IEW::tick()->IEW::executeInsts()
IEW::tick()->IEW::writebackInsts()
Commit::tick()->Commit::commitInsts()->Commit::commitHead()
```

- Rename (`Rename::renameInsts()`).
As suggested by the name, registers are renamed and the instruction
is pushed to the IEW stage. It checks that the IQ/LSQ can hold the new
instruction.
- Dispatch (`IEW::dispatchInsts()`).
This function inserts the renamed instruction into the IQ and LSQ.
- Schedule (`InstructionQueue::scheduleReadyInsts()`)
The IQ manages the ready instructions (operands ready) in a ready list,
and schedules them to an available FU. The latency of the FU is set here,
and instructions are sent to execution when the FU done.
- Execute (`IEW::executeInsts()`).
Here `execute()` function of the compute instruction is invoked and
sent to commit. Please note `execute()` will write results to the destiniation
register.
- Writeback (`IEW::writebackInsts()`).
Here `InstructionQueue::wakeDependents()` is invoked. Dependent
instructions will be added to the ready list for scheduling.
- Commit (`Commit::commitInsts()`).
Once the instruction reaches the head of ROB, it will be committed and
released from ROB.

### Load Instruction
Load instructions share the same path as compute instructions until
execution.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeLoad()
    ->StaticInst::initiateAcc()
      ->LSQ::pushRequest()
        ->LSQUnit::read()
          ->LSQRequest::buildPackets()
          ->LSQRequest::sendPacketToCache()
    ->LSQUnit::checkViolation()
DcachePort::recvTimingResp()->LSQRequest::recvTimingResp()
  ->LSQUnit::completeDataAccess()
    ->LSQUnit::writeback()
      ->StaticInst::completeAcc()
      ->IEW::instToCommit()
IEW::tick()->IEW::writebackInsts()
```

- `LSQUnit::executeLoad()` will initiate the access by invoking the
instruction's `initiateAcc()` function. Through the execution context interface,
`initiateAcc()` will call `initiateMemRead()` and eventually be directed
to `LSQ::pushRequest()`.
- `LSQ::pushRequest()` will allocate a `LSQRequest` to track all states, and
start translation. When the translation completes, it will
record the virtual address and invoke `LSQUnit::read()`.
- `LSQUnit::read()` will check if the load is aliased with any previous
store.
  - If can it can forward, then it will schedule `WritebackEvent` for the next
cycle.
  - If it is aliased but cannot forward, it calls
  `InstructionQueue::rescheduleMemInst()` and `LSQReuqest::discard()`.
  - Otherwise, it send packets to the cache.
- `LSQUnit::writeback()` will invoke `StaticInst::completeAcc()`, which
will write a loaded value to the destination register. The
instruction is then pushed to the commit queue. `IEW::writebackInsts()`
will then mark it done and wake up its dependents. Starting from here it
shares same path as compute instructions.

### Store Instruction
Store instructions are similar to load instructions, but only writeback
to cache after committed.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeStore()
    ->StaticInst::initiateAcc()
      ->LSQ::pushRequest()
        ->LSQUnit::write()
    ->LSQUnit::checkViolation()
Commit::tick()->Commit::commitInsts()->Commit::commitHead()
IEW::tick()->LSQUnit::commitStores()
IEW::tick()->LSQUnit::writebackStores()
  ->LSQRequest::buildPackets()
  ->LSQRequest::sendPacketToCache()
  ->LSQUnit::storePostSend()
DcachePort::recvTimingResp()->LSQRequest::recvTimingResp()
  ->LSQUnit::completeDataAccess()
    ->LSQUnit::completeStore()
```

- Unlike `LSQUnit::read()`, `LSQUnit::write()` will only copy the store
data, but not send the packet to cache, as the store is not committed yet.
- After the store is committed, `LSQUnit::commitStores()` will mark the SQ
entry as `canWB` so that `LSQUnit::writebackStores()` will send
the store request to cache.
- Finally, when the response comes back, `LSQUnit::completeStore()` will
release the SQ entries.

### Branch Misspeculation

Branch misspeculation is handled in `IEW::executeInsts()`. It will
notify the commit stage to start squashing all instructions in the ROB
on the misspeculated branch.

```cpp
IEW::tick()->IEW::executeInsts()->IEW::squashDueToBranch()
```

### Memory Order Misspeculation

The `InstructionQueue` has a `MemDepUnit` to track memory order dependence.
The IQ will not schedule an instruction if MemDepUnit states there is
dependency.

In `LSQUnit::read()`, the LSQ will search for possible aliasing store and
forward if possible. Otherwise, the load is blocked and rescheduled for when
the blocking store completes by notifying the MemDepUnit.

Both `LSQUnit::executeLoad/Store()` will call `LSQUnit::checkViolation()`
to search the LQ for possible misspeculation. If found, it will set
`LSQUnit::memDepViolator` and `IEW::executeInsts()` will start later to
squash the misspeculated instructions.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeLoad()
    ->StaticInst::initiateAcc()
    ->LSQUnit::checkViolation()
  ->IEW::squashDueToMemOrder()
```


---


## Simple CPU Models

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU*

# **SimpleCPU**
The SimpleCPU is a purely functional, in-order model that is suited for cases where a detailed model is not necessary. This can include warm-up periods, client systems that are driving a host, or just testing to make sure a program works.

It has recently been re-written to support the new memory system, and is now broken up into three classes:

**Table of Contents**


  1. [**BaseSimpleCPU**](#basesimplecpu)
  2. [**AtomicSimpleCPU**](#atomicsimplecpu)
  3. [**TimingSimpleCPU**](#timingsimplecpu)

## **BaseSimpleCPU**
The BaseSimpleCPU serves several purposes:
  * Holds architected state, stats common across the SimpleCPU models.
  * Defines functions for checking for interrupts, setting up a fetch request, handling pre-execute setup, handling post-execute actions, and advancing the PC to the next instruction. These functions are also common across the SimpleCPU models.
  * Implements the ExecContext interface.

The BaseSimpleCPU can not be run on its own. You must use one of the classes that inherits from BaseSimpleCPU, either AtomicSimpleCPU or TimingSimpleCPU.

## **AtomicSimpleCPU**
The AtomicSimpleCPU is the version of SimpleCPU that uses atomic memory accesses (see [Memory systems](../memory_system/index.html#access-types) for details). It uses the latency estimates from the atomic accesses to estimate overall cache access time. The AtomicSimpleCPU is derived from BaseSimpleCPU, and implements functions to read and write memory, and also to tick, which defines what happens every CPU cycle. It defines the port that is used to hook up to memory, and connects the CPU to the cache.

![AtomicSimpleCPU](/assets/img/AtomicSimpleCPU.jpg)

## **TimingSimpleCPU**
The TimingSimpleCPU is the version of SimpleCPU that uses timing memory accesses (see [Memory systems](../memory_system/index.html#access-types) for details). It stalls on cache accesses and waits for the memory system to respond prior to proceeding. Like the AtomicSimpleCPU, the TimingSimpleCPU is also derived from BaseSimpleCPU, and implements the same set of functions. It defines the port that is used to hook up to memory, and connects the CPU to the cache. It also defines the necessary functions for handling the response from memory to the accesses sent out.

![TimingSimpleCPU](/assets/img/TimingSimpleCPU.jpg)


---


## Trace CPU Model

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/TraceCPU*

# **TraceCPU**
 Table of Contents


1. [Overview](##Overveiw)


 1. [Elastic Trace Generation](##Elastic-Trace-Generation)
       1. [Scripts and options](##Scripts-and-options)
       2. [Trace file format](###Trace-file-formats)





 2. [Replay with Trace CPU](#replay-with-trace-cpu)
       1. [Scripts and options](##Scripts-and-options)




## **Overview**
The Trace CPU model plays back elastic traces, which are dependency and timing annotated traces generated by the Elastic Trace Probe attached to the O3 CPU model. The focus of the Trace CPU model is to achieve memory-system (cache-hierarchy, interconnects and main memory) performance exploration in a fast and reasonably accurate way instead of using the detailed but slow O3 CPU model. The traces have been developed for single-threaded benchmarks simulating in both SE and FS mode. They have been correlated for 15 memory-sensitive SPEC 2006 benchmarks and a handful of HPC proxy apps by interfacing the Trace CPU with classic memory system and varying cache design parameters and DRAM memory type. In general, elastic traces can be ported to other simulation environments.

 **Publication**:

[Exploring System Performance using Elastic Traces: Fast, Accurate and Portable"](https://ieeexplore.ieee.org/document/7818336) Radhika Jagtap, Stephan Diestelhorst, Andreas Hansson, Matthias Jung and Norbert Wehn SAMOS 2016

**Trace generation and replay methodology**

![Methodology block diagram showing elastic trace generation using O3 CPU and replay using Trace CPU
](/assets/img/Etrace_methodology.jpg)

## **Elastic Trace Generation**
The Elastic Trace Probe Listener listens to Probe Points inserted in O3 CPU pipeline stages. It monitors each instruction and creates a dependency graph by recording data Read-After-Write dependencies and order dependencies between loads and stores. It writes the instruction fetch request trace and the elastic data memory request trace as two separate files as shown below.

![Elastic trace file generation](/assets/img/Etraces_output.jpg)

### **Trace file formats**

The elastic data memory trace and fetch request trace are both encoded using google protobuf.

##### **Elastic Trace fields in protobuf format**

Fields    | Discritption
-------------- | -------------
required uint64 seq_num &nbsp;   | Instruction number used as an id for tracking dependencies
required RecordType type &nbsp;    | RecordType enum has values: INVALID, LOAD, STORE, COMP
optional uint64 p_addr &nbsp; 	| Physical memory address if instruction is a load/store
optional uint32 size &nbsp; 	| Size in bytes of data if instruction is a load/store
optional uint32 flags &nbsp; 	| 	Flags or attributes of the access, ex. Uncacheable
required uint64 rob_dep &nbsp;  |   Past instruction number on which there is order (ROB) dependency
required uint64 comp_delay &nbsp;       |	Execution delay between the completion of the last dependency and the execution of the instruction &nbsp;
repeated uint64 reg_dep &nbsp;              | Past instruction number on which there is RAW data dependency
optional uint32 weight &nbsp; | 	To account for committed instructions that were filtered out
optional uint64 pc &nbsp; | Instruction address, i.e. the program counter
optional uint64 v_addr &nbsp; | 	Virtual memory address if instruction is a load/store
optional uint32 asid &nbsp; | Address Space ID

A decode script in Python is available at `util/decode_inst_dep_trace.py` that outputs the trace in ASCII format.

**Example of a trace in ASCII**

    1,356521,COMP,8500::

    2,35656,1,COMP,0:,1:

    3,35660,1,LOAD,1748752,4,74,500:,2:

    4,35660,1,COMP,0:,3:

    5,35664,1,COMP,3000::,4

    6,35666,1,STORE,1748752,4,74,1000:,3:,4,5

    7,35666,1,COMP,3000::,4

    8,35670,1,STORE,1748748,4,74,0:,6,3:,7

    9,35670,1,COMP,500::,7

Each record in the instruction fetch trace has the following fields.

Fields    | Discritption
-------------- | -------------
required uint64 tick &nbsp;   |	Timestamp of the access
required uint32 cmd	&nbsp;    | Read or Write (in this case always Read)
required uint64 addr &nbsp;	| Physical memory address
required uint32 size &nbsp;	| Size in bytes of data
optional uint32 flags &nbsp;	| Flags or attributes of the access
optional uint64 pkt_id &nbsp;  |   Id of the access
optional uint64 pc  &nbsp;     |	Instruction address, i.e. the program counter



The decode script in Python at `util/decode_packet_trace.py` can be used to output the trace in ASCII format.


**Compile dependencies**:

You need to install google protocol buffer as the traces are recorded using this.

```sh

sudo apt-get install protobuf-compiler
sudo apt-get install libprotobuf-dev

```

### **Scripts and options**
#### SE mode
```
build/ARM/gem5.opt configs/example/arm/etrace_se.py \
    --inst-trace-file fetchtrace.proto.gz \
    --data-trace-file deptrace.proto.gz \
    [WORKLOAD]
```
#### FS mode
Create a checkpoint for your region of interest and resume from the checkpoint but with O3 CPU model and tracing enabled.
```
# Checkpoint generation
# NOTE: fs.py is deprecated and will be removed. Do not rely too much on it
build/ARM/gem5.opt --outdir=m5out/bbench \
    ./configs/deprecated/example/fs.py [fs.py options] \
    --benchmark bbench-ics
```
```
# Checkpoint restore
# NOTE: fs.py is deprecated and will be removed. Do not rely too much on it
build/ARM/gem5.opt --outdir=m5out/bbench/capture_10M \
    ./configs/deprecated/example/fs.py [fs.py options] \
    --cpu-type=arm_detailed --caches \
    --elastic-trace-en --data-trace-file=deptrace.proto.gz --inst-trace-file=fetchtrace.proto.gz \
    --mem-type=SimpleMemory \
    --checkpoint-dir=m5out/bbench -r 0 --benchmark bbench-ics -I 10000000
```

## **Replay with Trace CPU**

The execution trace generated above is then consumed by the Trace CPU as illustrated below.

![Trace_cpu_top_level](/assets/img/Trace_cpu_top_level.jpg)

The Trace CPU model inherits from the Base CPU and interfaces with data and instruction L1 caches. A diagram of the Trace CPU explaining the major logic and control blocks is shown below.

![Trace_CPU_details](/assets/img/Trace_cpu_detail.jpg)

### **Scripts and options**

* A trace replay script in the examples folder can be used to play back SE and FS generated traces
    * `build/ARM/gem5.opt [gem5.opt options] -d bzip_10Minsts_replay configs/example/etrace_replay.py [options] --caches --data-trace-file=bzip_10Minsts/deptrace.proto.gz --inst-trace-file=bzip_10Minsts/fetchtrace.proto.gz --mem-size=4GB`






Fields    | Discritption
-------------- | -------------
required uint64 seq_num    |	Timestamp of the access
required RecordType type    | Read or Write (in this case always Read)
optional uint64 p_addr	| Physical memory address if instruction is a load/store
optional uint32 size	| Size in bytes of data if instruction is a load/store
optional uint32 flags	| Flags or attributes of the access, ex. Uncacheable
required uint64 rob_dep | Past instruction number on which there is order (ROB) dependency
required uint64 comp_delay | Execution delay between the completion of the last dependency and the execution of the instruction
repeated uint64 reg_dep | Past instruction number on which there is RAW data dependency
optional uint32 weight | To account for committed instructions that were filtered out
optional uint64 pc	| Instruction address, i.e. the program counter
optional uint64 v_addr | Virtual memory address if instruction is a load/store
optional uint32 asid |	Address Space ID


---


## "Visualization"

*Source: https://www.gem5.org/documentation/general_docs/cpu_models/visualization/*

# Visualization
This page contains information about different types of information visualization that is integrated or can be used with gem5.

## O3 Pipeline Viewer
The o3 pipeline viewer is a text based viewer of the out-of-order CPU pipeline. It shows when instructions are fetched (f), decoded (d), renamed (n), dispatched (p), issued (i), completed (c), and retired (r). It is very useful for understanding where the pipeline is stalling or squashing in a reasonable small sequence of code. Next to the colorized viewer that wraps around is the tick the current instruction retired, the pc of that instruction, it's disassembly, and the o3 sequence number for that instruction.

![o3pipeviewer](/assets/img/O3pipeview.png)

To generate output line you see above you first need to run an experiment with the o3 cpu:

```./build/ARM/gem5.opt --debug-flags=O3PipeView --debug-start=<first tick of interest> --debug-file=trace.out configs/example/se.py --cpu-type=detailed --caches -c <path to binary> -m <last cycle of interest>```

Then you can run the script to generate a trace similar to the above (500 is the number of ticks per clock (2GHz) in this case):

```./util/o3-pipeview.py -c 500 -o pipeview.out --color m5out/trace.out```

You can view the output in color by piping the file through less:

```less -r pipeview.out```

When CYCLE_TIME (-c) is wrong, Right square brackets in output may not aligned to the same column. Default value of CYCLE_TIME is 1000. Be careful.

The script has some additional integrated help: (type ‘./util/o3-pipeview.py --help’ for help).

## Minor Viewer
The [new page](minor_view) on minor viewer is yet to be made, refer to [old page](http://pages.cs.wisc.edu/~swilson/gem5-docs/minor.html#trace) for documentation.


---


## Debugging and Testing

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/*

TODO


---


## Debugger-based Debugging

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/debugger_based_debugging*

# Debugger-based Debugging

If traces alone are not sufficient, you'll need to inspect what gem5 is doing
in detail using a debugger (e.g., gdb). You definitely want to use the
`gem5.debug` binary if you reach this point. Ideally, looking at traces should
at least allow you to narrow down the range of cycles in which you think
something is going wrong. The fastest way to reach that point is to use a
`DebugEvent`, which goes on gem5's event queue and forces entry into the
debugger when the specified cycle is reached by sending the process a `SIGTRAP`
signal. You'll need to to start gem5 under the debugger or have the debugger
attached to the gem5 process for this to work.

You can create one or more DebugEvents when you invoke gem5 using the
`--debug-break=100` parameter. You can also create new DebugEvents from the
debugger prompt using the `schedBreak()` function. The following example
session illustrates both of these approaches:

```
% gdb m5/build/ALL/gem5.debug
GNU gdb 6.1
Copyright 2002 Free Software Foundation, Inc.
[...]
(gdb) run --debug-break=2000 configs/run.py
Starting program: /z/stever/bk/m5/build/ALL/gem5.debug --debug-break=2000 configs/run.py
M5 Simulator System
[...]
warn: Entering event queue @ 0.  Starting simulation...

Program received signal SIGTRAP, Trace/breakpoint trap.
0xffffe002 in ?? ()
(gdb) p curTick
$1 = 2000
(gdb) c
Continuing.

(gdb) call schedBreak(3000)
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xffffe002 in ?? ()
(gdb) p _curTick
$3 = 3000
(gdb)
```

gem5 includes a number of functions specifically intended to be called from the
debugger (e.g., using the gdb `call` command, as in the `schedBreak()` example
above). Many of these are "dump" functions which display internal simulator
data structures. For example, `eventq_dump()` displays the events scheduled on
the main event queue. Most of the other dump functions are associated with
particular objects, such as the instruction queue and the ROB in the detailed
CPU model. These include:

|Function                                    |Effect                                                   |
|:-------------------------------------------|:--------------------------------------------------------|
|`schedBreak(<tick>)`                        |Schedule a `SIGTRAP` to occur at `<tick>`                |
|`setDebugFlag("<flag>")`                    |Enable a debug flag from the debugger                    |
|`clearDebugFlag("<flag>")`                  |Disable a debug flags from the debugger                  |
|`eventqDump()`                              |Print out all events on the event queue                  |
|`takeCheckpoint(<tick>)`                    |Create a checkpoint at cycle `<tick>`                    |
|`SimObject::find("system.qualified.name")`  |Returns the pointer to the object with the specified name|

<!---
The following has been commented out as the link the classic
memory system has yet to be migrated over to the website.

Additional gdb-accessible features for debugging coherence protocols in the
classic memory system are documented [here]{
http://gem5.org/Classic_Memory_System#Debugging}.
-->

## Debugging Python with PDB

You can debug configuration scripts with the [Python debug (PDB)](
https://docs.python.org/3/library/pdb.html) just as you would other Python
scripts. You can enter PDB before your configuration script is executed by
giving the `--pdb` argument to the gem5 binary. Another approach is to put the
following line in your configuration script wherever you would like to enter the debugger:

```python
import pdb; pdb.set_trace()
```

Note that the Python files under `src` are compiled in to the gem5 binary, so you
must rebuild the binary if you add this line (or make other changes) in these
files. Alternatively, you can set the `M5_OVERRIDE_PY_SOURCE` environment
variable to "true" (see `src/python/importer.py`).

See the [official PDB documentation](
https://docs.python.org/3/library/pdb.html) for more details on using PDB.

## Using Valgrind

Valgrind is a dynamic analysis tool used (primarily) to profile a target
application and detect the source of run-time errors, as well as detect memory
leaks.

For Valgrind to function, the target gem5 binary must have been compiled to
include debugging information. Therefore, the `gem5.debug` binaries must be
used. Due to difficulties with Valgrind working with tcmalloc, `gem5.debug`
must be compiled using the `--without-tcmalloc` flag:

```bash
scons --without-tcmalloc build/ALL/gem5.debug
```

To run a check using Valgrind, execute the following:

```bash
valgrind --leak-check=yes --suppressions=util/valgrind-suppressions build/ALL/gem5.debug {gem5 arguments}
```

The above will run the gem5 and do two things:

1. Give a stack trace if a run-time error is received.
2. Give information about potential memory leaks.

The `util/valgrind-suppressions` file contains a set of warnings that are
reported by Valgrind but are not considered a problem by gem5 developers.
**Valgrind is known to provide false positives. `util/valgrind-suppressions`
should be updated as these false positives are revealed**. More information
about suppressing Valgrind warnings can be found in the [Valgrind User Manual](
http://valgrind.org/docs/manual/manual-core.html#manual-core.suppress).

If a run-time error is received, Valgrind will return an output which looks like
the following (taken from the [Valgrind Quick Start Guide](
http://valgrind.org/docs/manual/quick-start.html)):

```txt
==19182== Invalid write of size 4
==19182==    at 0x804838F: f (example.c:6)
==19182==    by 0x80483AB: main (example.c:11)
```

In this output:

* 19182 is the process ID
* `Invalid write` is what kind of error.
* Below this error is the stack trace. In this example the leak occurred at
line 6 in `example.c`. This line is contained within function `f` which was
called by the `main` method at line 11 (also in `example.c`).
* `0x804838F` is the code address. This is usually not important.

Valgrind may also return warnings about memory leaks, such as:

```txt
==19182== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
==19182==    at 0x1B8FF5CD: malloc (vg_replace_malloc.c:130)
==19182==    by 0x8048385: f (a.c:5)
==19182==    by 0x80483AB: main (a.c:11)
```

The stack trace will tell you where the memory leak occurred. If Valgrind
states that a block of memory was "definitely lost" then there is a memory
leak. However, if Valgrind states that a block was "probably lost", Valgrind
has reason to believe memory is leaking but perhaps not (this is normally if
the code is doing something complex with pointers).

If Valgrind returns an output in which a root cause is difficult to determine,
try running Valgrind with `--track-origins=yes`. This will increase execution
time but will provide more information.

The [Valgrind User Manual](https://valgrind.org/docs/manual/manual.html) should
be consulted for more advanced features.


---


## Debugging Simulated Code

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/debugging_simulated_code*

# Debugging Simulated Code

gem5 has built-in support for gdb's remote debugger interface. If you are
interested in monitoring what the code on the simulated machine is doing
(the kernel, in FS mode, or program, in SE mode) you can fire up gdb on the
host platform and have it talk to the simulated gem5 system as if it were a
real machine/process (only better, since gem5 executions are deterministic and
gem5's remote debugger interface is guaranteed not to perturb execution on the
simulated system).

If you are simulating a system that uses a different ISA from the host you're
running on, you'll need a cross-architecture gdb; see below for instructions.
If you are simulating the native ISA of your host, you can very likely just use
the pre-installed native gdb.

When gem5 is run, each CPU listens for a remote debugging connection on a TCP
port. The first port allocated is generally 7000, though if a port is in use,
the next port will be tried.

To attach the remote debugger, it's necessary to have a copy of the kernel and
of the source. Also to view the kernel's call stack, you must make sure Linux
was built with the necessary debug configuration parameters enabled. To run the
remote debugger, do the following (assuming host=localhost and port=7000):

```
gdb-multiarch <path-to-linux>/vmlinux
GNU gdb (Ubuntu 8.2-0ubuntu1~18.04) 8.2
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

(gdb) target remote <host>:<port>
```

The gem5 simulator is already running and the target remote command connects to
the already running simulator and stops it in the middle of execution. You can
set breakpoints and use the debugger to debug the kernel. It is also possible
to use the remote debugger to debug console code. Setting that up
is similar, but a how to will be left for future work.

If you're using both the remote debugger and the debugger on the simulator, it
is possible to trigger the remote debugger from the main debugger by doing a
`call debugger()`. Before you do this you'll need to figure out what CPU (the
cpu id) you want to debug and set `current_debugger` to that `cpuid`. If you
only have one cpu, then it will be `cpuid 0`, however if there are multiple
cpus you will need to match the cpu id with the corresponding port number for
the remote gdb session. For example, using the following sample output from
gem5, calling the kernel debugger for cpu 3 requires the kernel debugger to be
listening on port 7001.

```
%./build/<ISA>/gem5.debug configs/example/fs.py
...
making dual system
Global frequency set at 1000000000000 ticks per second
Listening for testsys connection on port 3456
Listening for drivesys connection on port 3457
0: testsys.remote_gdb.listener: listening for remote gdb #0 on port 7002
0: testsys.remote_gdb.listener: listening for remote gdb #1 on port 7003
0: testsys.remote_gdb.listener: listening for remote gdb #2 on port 7000
0: testsys.remote_gdb.listener: listening for remote gdb #3 on port 7001
0: drivesys.remote_gdb.listener: listening for remote gdb #4 on port 7004
0: drivesys.remote_gdb.listener: listening for remote gdb #5 on port 7005
0: drivesys.remote_gdb.listener: listening for remote gdb #6 on port 7006
0: drivesys.remote_gdb.listener: listening for remote gdb #7 on port 7007
```

## Getting a cross-architecture gdb

To use a remote debugger with gem5, the most important part is that you have
gdb compiled to work with the target system you're simulating.
The recommended approach is to install the gdb-multiarch package,
providing a single gdb binary usable for multiple ISAs (archs)

```
% sudo apt-get update -y
% sudo apt-get install -y gdb-multiarch
```

It is possible to compile a non-native architecture gdb on
the host machine as an alternative. All that must be done is add the `--target=`
option to configure when you compile gdb. You may also get pre-compiled
debuggers with cross compilers. See Download for links to some cross compilers
that include debuggers.

```
% wget http://ftp.gnu.org/gnu/gdb/<gdb-version>.tar.gz
% tar xfz <gdb-version>.tar.gz
% cd <gdb-version>
% ./configure --target=<isa>
<configure output....>
% make
<make output...this may take a while>
```

The end result is gdb/gdb which will work for remote debugging.

## Target-specific instructions

### ARM Target

If you're planning to debug an ARM kernel you'll need a reasonably new version
of gdb (7.1 or greater). Additionally, you'll have to manually specify the
`tspecs` like this (port number may be different). The `tspec` file is
available in the gdb source code:

```
set remote Z-packet on
set tdesc filename path/to/features/arm-with-neon.xml
symbol-file <path to vmlinux used for gem5>
target remote <ip addr of host running gem5 or if local host 127.0.0.1>:7000
```


---


## Trace-based Debugging

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging*

# Trace-based Debugging

## Introduction

The simplest method of debugging is to have gem5 print out traces of what it's
doing. The simulator contains many DPRINTF statements that print trace messages
describing potentially interesting events. Each DPRINTF is associated with a
debug flag (e.g., `Bus`, `Cache`, `Ethernet`, `Disk`, etc.). To turn on the
messages for a particular flag, use the `--debug-flags` command line argument.
Multiple flags can be specified by giving a list of strings, e.g.:

```
build/<ISA>/gem5.opt --debug-flags=Bus,Cache configs/examples/fs.py
```

would turn on a group of debug flags related to instruction execution but leave
out Tick (timing) information. This is useful if you want to compare execution
between two runs where the same instructions execute but at different rates.

Note that the gem5.fast binary does not support tracing; part of what makes it
faster than gem5.opt is that the DPRINTF code is compiled out.

The `--debug-flags` command line option should come after the gem5 executable
but before the simulation script. This is because debug flags are handled by
gem5 itself, and whether command line options are before or after the
simulation script determine if they're for gem5 or the script.

```
Debugging Options
-----------------
--debug-break=TIME[,TIME]
                        Tick to create a breakpoint
--debug-help            Print help on debug flags
--debug-flags=FLAG[,FLAG]
                        Sets the flags for debug output (-FLAG disables a
                        flag)
--debug-start=TIME      Start debug output at TIME (must be in ticks)
--debug-file=FILE       Sets the output file for debug [Default: cout]
--debug-ignore=EXPR     Ignore EXPR sim objects
```

The complete list of debug/trace flags can be seen by running gem5 with the
`--debug-help` option.

If you find that events of interest are not being traced, feel free to add
DPRINTFs yourself. You can add new debug flags simply by adding `DebugFlag()`
command to any SConscript file (preferably the one nearest where you are using
the new flag). If you use a debug flag in a C++ source file, you would need to
include the header file `debug/<name of debug flag>.hh` in that file.

For more complex bugs, the trace can be useful in simply identifying points in
the simulation where more in-depth investigation is needed. The `--debug-break`
option lets you re-run your simulation under a debugger and stop on a
particular tick as identified by the trace. You can also schedule breakpoints
and enable or disable debug flags from within the debugger itself. See the page
on Debugger Based Debugging for more information.

### The Exec debug flag

The `Exec` compound debug flag is very useful because it turns on instruction
tracing in gem5. It makes the simulator print a disassembled version of each
instruction as it finishes executing, along with other useful information like
the time, pc, the address if it was a memory instruction, etc. These individual
pieces of information can be turned on and off with the base debug flags Exec
controls. For example, you can disable the use of function symbol names in
place of absolute PC addresses (if they're available) by turning off the
ExecSymbol flag (e.g., `--debug-flags=Exec,-ExecSymbol`).

If some supposedly innocuous change has caused gem5 to stop working correctly,
you can compare trace outputs from before and after the change using the
tracediff script in the `src/util` directory. Comments in the script describe
how to use it.

### Reducing trace file size

Trace file can become very large very quickly, but they also compress very well
(e.g. about 90%). If you'd like to make gem5 output a compressed trace, just
add a `.gz` extension to the output file name. For example
`--debug-file=trace.out` will produce an uncompressed file as normal, but
`--debug-file=trace.out.gz` will produce a gzip compressed file. You can use
the zcat program and pipes to process the output. The editor vim also can
uncompress gzip compressed files in memory.

## The tracediff and rundiff utilities

`tracediff` and `rundiff` utilities allow the simple diffing of two streams of
trace data from gem5 to find any differences. It's very handy for debugging why
regression tests fail, figuring out why your minor code change seems to cause
some unrelated execution problem, or comparing the execution of CPU models.

Both utilities are found in the `util` directory. `rundiff` is a simple
diff-like program. Unlike regular diff, this script does not read in the entire
input before comparing its inputs, so it can be used on lengthy outputs piped
from other programs (e.g., gem5 traces). `tracediff` is a front end for
`rundiff` that provides an easy way to run two similar copies of gem5 and diff
their outputs. It takes a common gem5 command line with embedded alternatives
and executes the two alternative commands in separate subdirectories with
output piped to rundiff.

Script arguments are handled uniformly as follows:

* If the argument does not contain a '|' character, it is appended to both
command lines.
* If the argument has a '|" character in it, the text on either size of the '|'
is appended to the respective command lines. Note that you'll have to quote the
arg or escape the '|' with a backslash so that the shell doesn't thing you're
doing a pipe or put quotes around it.
* Arguments with '#' characters are split at those characters, processed for
alternatives ('|'s) as independent terms, then pasted back into a single
argument (without the '#'s). (Sort of inspired by the C preprocessor '##' token
pasting operator.)

In other words, the arguments should look like the command line you want to
run, with '|' used to list the alternatives for the parts that you want to
differ between the two runs.

For example:

```
 % tracediff gem5.opt --opt1 '--opt2|--opt3' --opt4
# would compare these two runs:
gem5.opt --opt1 --opt2 --opt4
gem5.opt --opt1 --opt3 --opt4

% tracediff 'path1|path2#/m5.opt' --opt1 --opt2
# would compare these two runs:
path1/gem5.opt --opt1 --opt2
path2/gem5.opt --opt1 --opt2
```

If you want to add arguments to one run only, just put a '|' in with text only
on one side (`--onlyOn1|`). You can do this with multiple arguments together
too (`|-a -b -c` adds three args to the second run only).

The `-n` argument to tracediff allows you to preview the two generated command
lines without running them.

For tracediff to be useful some trace flags must be enabled. The most common
trace flags to use with tracediff are `--debug-flags=Exec,-ExecTicks` which
removes the timestamp from each trace making it suitable to diff when slight
timing variations are present.

Tracediff is also useful for comparing CPU models when one fails and the other
doesn't. In this case it's best to create a checkpoint before the problem
occurs (this can be done by just creating a bunch of checkpoints and finding
one that fails). If the failure occurs in kernel code, use the
`-ExecUser` debug flag, on the other hand if it occurs in user code try the
`-ExecKernel` debug flag to isolate user code in the trace. You can then
compare the traces and see when the execution diverges.

### Comparing traces across machines

Sometimes gem5 executions differ inexplicably across different environments,
and you'd like to use rundiff to help pinpoint where they diverge. Rather than
try and reproduce those environments on the same machine, you can use netcat
with rundiff to compare traces from gem5 instances running on separate systems
across the network.

First, start rundiff running on one machine, configured to compare the trace
output from a local instance of gem5 with the output of a netcat "server".
Since the network is likely to be the bottleneck, we'll compress the trace
going across netcat, which means we need to uncompress it as it arrives. For
example (choosing port number 33335 arbitrarily):

```
util/rundiff 'gem5.opt --debug-flag=Exec <gem5 args> |' 'nc -d -l 33335 | gunzip -c |' >& tracediff.out &
```

Now go to the second machine, start a copy of gem5 there, and ship its
compressed trace output to the netcat instance running on the first machine.
For example:

```
gem5.opt --debug-flag=Exec <gem5 args> |& gzip -c |& nc <hostname> 33335
```

## Internal Exec tracing implementation (InstTracer)

The "Trace-based debugging" section above talked about how to use the `Exec`
trace flag to print information about each instruction as it completes. That
functionality is actually implemented by an `InstTracer` object which collects
information about instructions as the execute. These objects can be swapped
out, and different objects can do different things with the information they
collect. For instance, the `IntelTrace` object prints out a trace in a
different format which is compatible with an external tool. The objects can
also do more than just print a trace. `NativeTrace` objects send information
about architectural state over a socket to the statetrace tool (described
below) instruction by instruction to validate execution. `InstTracer` objects
are `SimObjects` which are assigned to the `tracer` parameter of each CPU. If
you want to install a different tracer, just assign it to that parameter on the
CPU of interest.

When writing your own `InstTracer`, you'll write at least two different
classes, one which inherits from `InstTracer` and one that inherits from
`InstRecord`. The `InstTracer` class's main responsibility is to generate
`InstRecord` objects which are associated with a particular instruction. By
subclassing `InstTracer`, you'll be able to return your own specialized version
of `InstRecord` which is the class that really does most of the work.

The `InstRecord` class have a number of fields which hold information about the
history of an instruction. For instance, `InstRecord` records the instruction's
PC, what address it used if it accessed memory, a "data" value which it
produced (multiple data values aren't handled), etc. The `InstRecord` function
also has a pointer to a `ThreadContext` which can be used to read out
architectural state. When an instruction is finished executing, the
`InstRecord`'s `dump()` virtual function is called to process the record. For
the default `InstTracer`, this is where the instruction's assembly language
form, etc., is printed which is the output you see when you turn on `Exec`. For
`NativeTrace`, this is where architectural state is gathered up to send to
statetrace.

### Disassembling instructions with third party disassembler

Most of the gem5 tracers (inheriting from InstTracer mentioned above) will print/dump
the dynamic instruction stream together with other information (e.g. destination
register values). The disassembly is generated on the fly by querying the instruction
to be traced (StaticInst).
Every StaticInst is supposed to define a generateDisassembly method which returns the
instruction mnemonic (opcode + operand list) as a string.

From gem5 v23.1 it will be possible to hook different disassemblers to every InstTracer.
A disassembler will have to implement the InstDisassembler interface defined in
src/sim/insttracer.hh

By default the native disassembler (relying on generateDisassembly) will be used.
To change the disassembler with a custom one (say it is called MyDisassembler),
just amend the config file with:

```
cpu.tracer.disassembler = MyDisassembler()
```

#### Capstone disassembler

gem5 v23.1 introduces the [integration with the Capstone disassembler](https://github.com/gem5/gem5/pull/494).
[Capstone](http://www.capstone-engine.org/) is an open source disassembler already used
by other projects (like QEMU).

To compile gem5 with capstone support, it is necessary to install capstone first.
Then the capstone disassembler will have to be instantiated in the config script. At the
time of the writing only the Arm version of the disassembler has been implemented.
Therefore the line to be added to the script will have to be (assuming it is an Arm
simulation):

```
cpu.tracer.disassembler = ArmCapstoneDisassembler()
```

## Comparing traces with a real machine

The statetrace tool runs alongside gem5 and compares execution of a workload on
a real machine with execution in gem5. In the simulator and the real system,
the workload is allowed to run one instruction at a time. After each
instruction, architectural state is collected and compared and any differences
are reported. It can be tricky to get it set up and producing useful results
(described below), but it's an extremely valuable tool for debugging because it
tends to quickly pinpoint exactly where a problem is coming from, likely saving
many hours of painful debugging per bug.

### Native Trace

In gem5, a NativeTrace `InstTracer` object (described above) needs to be
installed on the CPU that will run the workload of interest. When execution
starts, the tracer will wait for the state trace utility to connect to it.
Then, after each instruction executes, it uses the `ThreadContext` pointer in
the `InstRecord` object to gather architectural state from the currently
running process. It also reads in architectural state gather by state trace
through the connection they established. The two versions of state are
compared, and any meaningful differences are reported. The exact makeup of the
state and how it should be compared is very ISA dependent on ISA, so each ISA
defines its own version of NativeTrace. These specialized classes can handle
things like expected differences when registers may become undefined, or
situations where execution skips ahead for one reason or another.

### statetrace utility

The statetrace utility is found in the util directory and is responsible for
running the workload on the real machine. It uses the ptrace mechanism provided
by the Linux kernel to single step the target process and to access its state.
It uses scons, but is independent of scons as used by the rest of gem5. To
build a version of statetrace suitable for a particular ISA, use the
`build/${ARCH}/statetrace` target where `${ARCH}` is replaced by the ISA of
interest. Currently recognized values for `${ARCH}` are `amd64`, `arm`, `i686`,
and `sparc`. You can override the compiler used for any ISA using the CXX scons
argument, and the compiler used for a particular ISA with `${ARCH}CXX`. For
instance, to build an arm version of statetrace, you could run:

```
cd util/statetrace
scons ARMCXX=arm-softfloat-linux-gnueabi-g++ build/arm/statetrace
```

statetrace accepts four flags, `-h` to print the help, `--host` to specify what
ip and port gem5 is listening at, `-i` to print out what's on the initial stack
frame, and `-nt` to disable tracing. `-nt` is typically used with `-i` to get
information about a processes initial stack without running it. The end of the
command line options is marked with two dashes. Next, put the command line you
want statetrace to run.

The exact text of the program name and arguments matters because these will be
passed to the process on its stack. Longer values take up more room on the
stack, that displaces other items to different addresses, and statetrace clog
up with lots of unimportant differences. For instance, if you need to run a
program found in your home directory in a gem5 subdirectory and you run this
command:

```
statetrace -- ~/gem5/my_benchmark arg1 arg2
```

You must also override arg0 in gem5 to be `~/gem5/my_benchmark`.

### Tuning

statetrace is a very sensitive system, and any minor difference between
simulated execution and real execution could produce lots and lots of spurious
differences. In order to get useful information from statetrace you'll need to
adjust the real system and gem5 so that everything lines up perfectly. I
normally create a patch which has all the modifications I've made to gem5 for
statetrace. Then I can easily remove them or reapply them for as I find and fix
problems. Mercurial queues is useful for managing that patch and patches for my
fixes. The following is an incomplete list of the differences you may have to
correct.

Address randomization: To improve security, Linux will randomize the address
space of processes, moving around their stack and heap areas. This makes it
harder for an attacker to predict what memory will look like, but it also
thoroughly defeats statetrace. To disable it, echo `0` into
`/proc/sys/kernel/randomize_va_space`. You'll almost certainly need root
permissions to do that.

argv values: Be sure to use _exactly_ the same text for each argument to your
program in gem5 and on the real system. This includes arg0, the program name.

File block size: Glibc uses the block size associated with a file to decide how
to buffer it. Different behavior will throw off execution and prevent
statetrace from working. You can change the block size gem5 reports in the
`convertStatBuf` and `convertStat64Buf` functions in `src/sim/syscall_emul.hh`.

Initial stack contents: Depending on your version of Linux, the contents of the
initial stack may be different. You can use the `-i` and `-nt` options to print
out the content of the initial stack on the real machine. statetrace attempts
to interpret the initial stack so you can more easily see what's on it. You'll
need to adjust how gem5 sets up the stack to match your real system. This code
is typically in a file called `process.cc` in the appropriate arch directory.
gem5's code has been painstakingly constructed so that it sets up a stack as
identically to Linux as possible, but the underlying mechanism would change.
Also, Linux puts a collection of auxiliary vectors on the initial stack. These
are type, value pairs which let the kernel provide extra information to the
process as it starts. From time to time Linux introduces a new type of
auxiliary vector and adds it to the stack. You may need to dig into the Linux
source and emulate any new entries.

### Caveats

Because statetrace is very sensitive to any changes in execution, it can't be
used with programs that don't behave in very predictable ways. For instance, if
a program reads in a random value from `/dev/random` and uses that in a
calculation (or worse in control flow) then that program can't be used. Less
obviously, if the program relies on the system time which is unpredictable, it
also can't be used. Generally speaking, many benchmarks try to be very
deterministic so that they can be used to generate reproducible data. That
makes them work well with statetrace.

Statetrace can't be used at the operating system level for at least two main
reasons. First, no system is implemented or will be implemented in the
foreseeable future for single stepping an operating system. Second, real
operating systems are not determinstic. Interrupts from hardware devices will
almost certainly come in at unpredictable times, some devices will return
unpredictable data, and gem5 is much less likely to exactly match the behavior
of a system at that level where firmware and other implementation details are
non longer abstracted away. Second the amount of state that's relevant at the
system level is typically larger than at the user level, especially in complex
ISAs like `x86`. Gathering, comparing, and transporting all that extra state
would significantly impact performance.

Not all implementations of ptrace actually work properly. For instance when I
last used statetrace with `ARM`, certain functions called into a region of
memory set up by the kernel which had kernel specific implementations of for
various operations. Ptrace relied on software breakpoints which work by
replacing the next instruction in the program with one that will trap. Because
the region of memory really belonged to the kernel, ptrace couldn't modify it
to install a breakpoint. The process "escaped" single stepped execution and
quickly ran to completion, leaving gem5 waiting for an update that never came.

statetrace isn't able to track changes to memory. Because memory is very large
and there isn't a convenient way to detect modifications to it, statetrace only
tracks register based architectural state. If an instruction changes registers
correctly but stores the wrong value to memory and/or to the wrong address,
that problem may not be detected for many instructions. Fortunately, those
sorts of errors are the exception.

To compare execution to a real machine, you ideally need to have a real machine
at your disposal. It's still quite possible, however, to run statetrace inside
an emulator like qemu. That's likely a little slower and compares execution
against the emulator and not real hardware, but it can still help identify
bugs.

### ISA support

Currently `SPARC`, `ARM`, and `x86` support state. ARM's support is currently
the most sophisticated, only sending differences in state across the connection
which improves performance, and only printing when differences start or stop
which reduces output and improves readability. Those features are planned to be
ported to the other ISAs. Hopefully that code can be factored out and put into
the base `NativeTrace` class so that all ISAs can use it easily.


---


## Garnet Synthetic Traffic

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/directed_testers/garnet_synthetic_traffic/*

# Garnet Synthetic Traffic

The Garnet Synthetic Traffic provides a framework for simulating the Garnet
network with controlled inputs. This is useful for network testing/debugging,
or for network-only simulations with synthetic traffic.

**Note: The garnet synthetic traffic injector only works with Garnet_standalone
coherence protocol.**

## Related Files

* `configs/example/garnet_synth_traffic.py` : file to invoke the network tester
* `src/cpu/tester/garnet_sythetic_taffic/GarnetSyntheticTraffic.*` : files
implementing the tester

## How to run

First build gem5 with the Garnet_standalone coherence protocol. This protocol
is ISA-agnostic, and hence we build it with the NULL ISA.

For gem5 <= 23.0:

```
scons build/NULL/gem5.debug PROTOCOL=Garnet_standalone
```

For gem5 >= 23.1

```
scons defconfig build/NULL build_opts/NULL
scons setconfig build/NULL RUBY_PROTOCOL_GARNET_STANDALONE=y
scons build/NULL/gem5.debug
```

Example command:

```
./build/NULL/gem5.debug configs/example/garnet_synth_traffic.py  \
--num-cpus=16 \
--num-dirs=16 \
--network=garnet2.0 \
--topology=Mesh_XY \
--mesh-rows=4  \
--sim-cycles=1000 \
--synthetic=uniform_random \
--injectionrate=0.01
```

## Parameterized Options

|System Configuration &nbsp; &nbsp; &nbsp;         |Description                                                                              |
|:---------------------|:----------------------------------------------------------------------------------------|
|`--num-cpus`          |Number of cpus. This is the number of source (injection) nodes in the network.           |
|`--num-dirs`          |Number of directories. This is the number of destination (ejection) nodes in the network.|
|`--network`           |Network model: simple or garnet2.0. Use garnet2.0 for running synthetic traffic.         |
|`--topology`          |Topology for connecting the cpus and dirs to the network routers/switches.               |
|`--mesh-rows`         |The number of rows in the mesh. Only valid when --topology is Mesh* MeshDirCorners*      |

<br>
<br>

|Network Configuration &nbsp;       |Description                                                                                                                             |
|:---------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
|`--router-latency`    | Default number of pipeline stages in the garnet router. Has to be >= 1. Can be over-ridden on a per router basis in the topology file. |
|`--link-latency`      | Default latency of each link in the network. Has to be >= 1. Can be over-ridden on a per link basis in the topology file.              |
|`--vcs-per-vnet`      | Number of VCs per Virtual Network.                                                                                                     |
|`--link-width-bits`   | Width in bits for all links inside the garnet network. Default = 128.                                                                  |

<br>
<br>

|Traffic Injection Configuration &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  |Description |
|:---------------------|:-----------|
|`--sim-cycles`        | Total number of cycles for which the simulation should run. |
|`--synthetic`         | The type of synthetic traffic to be injected. The following synthetic traffic patterns are currently supported: `uniform_random`, `tornado`, `bit_complement`, `bit_reverse`, `bit_rotation`, `neighbor`, `shuffle`, and `transpose` |
|`--injectionrate`     | Traffic Injection Rate in `packets/node/cycle`. It can take any decimal value between 0 and 1. The number of digits of precision after the decimal point can be controlled by `--precision` which is set to 3 as default in `garnet_synth_traffic.py`. |
|`--single-sender-id`  | Only inject from this sender. To send from all nodes, set to -1. |
|`--single-dest-id`    | Only send to this destination. To send to all destinations as specified by the synthetic traffic pattern, set to -1. |
|`--num-packets-max`   | Maximum number of packets to be injected by each cpu node. Default value is -1 (keep injecting till sim-cycles). |
|`--inj-vnet`          | Only inject in this vnet (0, 1 or 2). 0 and 1 are 1-flit, 2 is 5-flit. Set to -1 to inject randomly in all vnets. |

<br>
<br>

## Implementation of Garnet Synthetic Traffic

The synthetic traffic injector is implemente in `GarnetSnytheticTraffic.cc`.
The sequence of steps involved in generating and sending a packet are as
follows.

* Every cycle, each cpu performs a bernouli trial with probability equal to
--injectionrate to determine whether to generate a packet or not.
* If `--num-packets-max` is non negative, each cpu stops generating new packets
after generating `--num-packets-max` number of packets. The injector terminates
after `--sim-cycles`.
* If the cpu has to generate a new packet, it computes the destination for the
new packet based on the synthetic traffic type (`--synthetic`).
* This destination is embedded into the bits after block offset in the packet
address.
* The generated packet is randomly tagged as a `ReadReq`, or an `INST_FETCH`,
or a `WriteReq`, and sent to the Ruby Port
(`src/mem/ruby/system/RubyPort.hh/cc`).
* The Ruby Port converts the packet into a `RubyRequestType:LD`,
`RubyRequestType:IFETCH`, and `RubyRequestType:ST`, respectively, and sends it
to the Sequencer, which in turn sends it to the Garnet_standalone cache
controller.
* The cache controller extracts the destination directory from the packet
address.
* The cache controller injects the `LD`, `IFETCH` and `ST` into virtual
networks 0, 1 and 2 respectively.
* `LD` and `IFETCH` are injected as control packets (8 bytes), while `ST` is
injected as a data packet (72 bytes).
* The packet traverses the network and reaches the directory.
* The directory controller simply drops it.


---


## Ruby Random Tester

*Source: https://www.gem5.org/documentation/general_docs/debugging_and_testing/directed_testers/ruby_random_tester/*

# Ruby Random Tester

A cache coherence protocol usually has several different types of state
machines, with state machine having several different states. For example, the
`MESI CMP` directory protocol has four different state machines (`L1`, `L2`,
`directory`, `dma`). Testing such a protocol for functional correctness is a
challenging task. gem5 provides a random tester for testing coherence
protocols. It is called the Ruby Random Tester. The source files related to the
tester are present in the directory `src/cpu/testers/rubytest`. The file
`configs/examples/ruby_random_test.py` is used for configuration and execution
of the test. For example, the following command can be used for testing a
protocol:

```bash
./build/NULL/gem5.fast ./configs/example/ruby_random_test.py
```

Note: As of gem5 v24.1, the above command will not work if the ALL build is used.

Though one can specify many different options to the random tester, some of
them are note worthy.

|Parameter         |Description                                                       |
|:-----------------|:-----------------------------------------------------------------|
|`-n`, `--num-cpus`|Number of cpus injecting load/store requests to the memory system.|
|`--num-dirs`      |Number of directory controllers in the system.                    |
|`-m`, `--maxtick` |Number of cycles to simulate.                                     |
|`-l`, `--checks`  |Number of loads to be performed.                                  |
|`--random_seed`   |Seed for initialization of the random number generator.           |

Testing a coherence protocol with the random tester is a tedious task and
requires patience. First, build gem5 with the protocol to be tested. Then, run
the ruby random tester as mentioned above. Initially one should run the tester
with a single processor, and few loads. It is likely that one would encounter
problems. Use the debug flags to get a trace of the events ocurring in the
system. You may find the flag `ProtocolTrace` particularly useful. As these are
rectified, keep on increasing the number of loads, say by a factor of 10 each
time till one can execute one to ten million loads. Once it starts working for
a single processor, a similar process now needs to be followed for a two
processor system, followed by larger systems.

Theoretical approaches exist for [verifying coherence protocols](
https://doi.org/10.1145/248621.248624), but gem5 currently does not include any
testers based on those.


---


## "Developing gem5"

*Source: https://www.gem5.org/documentation/general_docs/development/*




---


## "C/C++ Coding Style"

*Source: https://www.gem5.org/documentation/general_docs/development/coding_style/*

# C/C++ Coding Style

We strive to maintain a consistent coding style in the gem5 C/C++ source code to make the source more readable and maintainable. This necessarily involves compromise among the multiple developers who work on this code. We feel that we have been successful in finding such a compromise, as each of the primary M5 developers is annoyed by at least one of the rules below. We ask that you abide by these guidelines as well if you develop code that you would like to contribute back to M5. An Emacs c++-mode style embodying the indentation rules is available in the source tree at util/emacs/m5-c-style.el.

## Indentation and Line Breaks

Indentation will be 4 spaces per level, though namespaces should not increase the indentation.

* Exception: labels followed by colons (case and goto labels and public/private/protected modifiers) are indented two spaces from the enclosing context.

Indentation should use spaces only (no tabs), as tab widths are not always set consistently, and tabs make output harder to read when used with tools such as diff.

Lines must be a maximum of 79 characters long.

## Braces

For control blocks (if, while, etc.), opening braces must be on the same line as the control keyword with a space between the closing parenthesis and the opening brace.

* Exception: for multi-line expressions, the opening brace may be placed on a separate line to distinguish the control block from the statements inside the block.

```c++
if (...) {
    ...
}

// exception case
for (...;
     ...;
     ...) // brace could be up here
{ // but this is optionally OK *only* when the 'for' spans multiple lines
    ...
}
```

'Else' keywords should follow the closing 'if' brace on the same line, as follows:

```c++
if (...) {
    ...
} else if (...) {
    ...
} else {
    ...
}
```

Blocks that consist of a single statement that fits on a single line may optionally omit the braces. Braces are still required if the single statement spans multiple lines, or if the block is part of an else/if chain where other blocks have braces.

```c++
// This is OK with or without braces
if (a > 0)
    --a;

// In the following cases, braces are still required
if (a > 0) {
    obnoxiously_named_function_with_lots_of_args(verbose_arg1,
                                                 verbose_arg2,
                                                 verbose_arg3);
}

if (a > 0) {
    --a;
} else {
    underflow = true;
    warn("underflow on a");
}
```

For function definitions or class declarations, the opening brace must be in the first column of the following line.

In function definitions, the return type should be on one line, followed by the function name, left-justified, on the next line. As mentioned above, the opening brace should also be on a separate line following the function name.

See examples below:

```c++
int
exampleFunc(...)
{
    ...
}

class ExampleClass
{
  public:
    ...
};
```

Functions should be preceded by a block comment describing the function.

Inline function declarations longer than one line should not be placed inside class declarations. Most functions longer than one line should not be inline anyway.

## Spacing

There should be:

* one space between keywords (if, for, while, etc.) and opening parentheses
* one space around binary operators (+, -, <, >, etc.) including assignment operators (=, +=, etc.)
* no space around '=' when used in parameter/argument lists, either to bind default parameter values (in Python or C++) or to bind keyword arguments (in Python)
* no space between function names and opening parentheses for arguments
* no space immediately inside parentheses, except for very complex expressions. Complex expressions are preferentially broken into multiple simpler expressions using temporary variables.


For pointer and reference argument declarations, either of the following are acceptable:

```c++
FooType *fooPtr;
FooType &fooRef;
```

or

```c++
FooType* fooPtr;
FooType& fooRef;
```
However, style should be kept consistent within a file. If you are editing an existing file, please keep consistent with the existing code. If you are writing new code in a new file, feel free to choose the style of your preference.

## Naming

Class and type names are mixed case, start with an uppercase letter, and do not contain underscores (e.g., ClassName). Exception: names that are acronyms should be all upper case (e.g., CPU). Class member names (method and variables, including const variables) are mixed case, start with a lowercase letter, and do not contain underscores (e.g., aMemberVariable). Class members that have accessor methods should have a leading underscore to indicate that the user should be using an accessor. The accessor functions themselves should have the same name as the variable without the leading underscore.

Local variables are lower case, with underscores separating words (e.g., local_variable). Function parameters should use underscores and be lower case.

C preprocessor symbols (constants and macros) should be all caps with underscores. However, these are deprecated, and should be replaced with const variables and inline functions, respectively, wherever possible.

```c++
class FooBarCPU
{
  private:
    static const int minLegalFoo = 100;  // consts are formatted just like other vars
    int _fooVariable;   // starts with '_' because it has public accessor functions
    int barVariable;    // no '_' since it's internal use only

  public:
    // short inline methods can go all on one line
    int fooVariable() const { return _fooVariable; }

    // longer inline methods should be formatted like regular functions,
    // but indented
    void
    fooVariable(int new_value)
    {
        assert(new_value >= minLegalFoo);
        _fooVariable = new_value;
    }
};
```

## #includes

Whenever possible favor C++ includes over C include. E.g. choose cstdio, not stdio.h.

The block of #includes at the top of the file should be organized. We keep several sorted groups. This makes it easy to find #include and to avoid duplicate #includes.

Always include Python.h first if you need that header. This is mandated by the integration guide. The next header file should be your main header file (e.g., for foo.cc you'd include foo.hh first). Having this header first ensures that it is independent and can be included in other places without missing dependencies.

```c++
// Include Python.h first if you need it.
#include <Python.h>

// Include your main header file before any other non-Python headers (i.e., the one with the same name as your cc source file)
#include "main_header.hh"

// C includes in sorted order
#include <fcntl.h>
#include <sys/time.h>

// C++ includes
#include <cerrno>
#include <cstdio>
#include <string>
#include <vector>

// Shared headers living in include/. These are used both in the simulator and utilities such as the m5 tool.
#include <gem5/asm/generic/m5ops.h>

// M5 includes
#include "base/misc.hh"
#include "cpu/base.hh"
#include "params/BaseCPU.hh"
#include "sim/system.hh"
```

## File structure and modularity

Source files (.cc files) should never contain extern declarations; instead, include the header file associated with the .cc file in which the object is defined. This header file should contain extern declarations for all objects exported from that .cc file. This header should also be included in the defining .cc file. The key here is that we have a single external declaration in the .hh file that the compiler will automatically check for consistency with the .cc file. (This isn't as important in C++ as it was in C, since linker name mangling will now catch these errors, but it's still a good idea.)

When sufficient (i.e., when declaring only pointers or references to a class), header files should use forward class declarations instead of including full header files.

Header files should never contain using namespace declarations at the top level. This forces all the names in that namespace into the global namespace of any source file including that header file, which basically completely defeats the point of using namespaces. It is OK to use using namespace declarations at the top level of a source (.cc) file since the effect is entirely local to that .cc file. It's also OK to use them in _impl.hh files, since for practical purposes these are source (not header) files despite their extension.

## Documenting the code

Each file/class/member should be documented using doxygen style comments.Doxygen allows users to quickly create documentation for our code by extracting the relavent information from the code and comments. It is able to document all the code structures including classes, namespaces, files, members, defines, etc. Most of these are quite simple to document, you only need to place a special documentation block before the declaration. The Doxygen documentation within gem5 is processed every night and the following web pages are generated: [Doxygen](http://doxygen.gem5.org/release/current/index.html)

### Using Doxygen

The special documentation blocks take the form of a javadoc style comment. A javadoc comment is a C style comment with 2 *'s at the start, like this:

```c++
/**
 * ...documentation...
 */
```

The intermediate asterisks are optional, but please use them to clearly delineate the documentation comments.

The documentation within these blocks is made up of at least a brief description of the documented structure, that can be followed by a more detailed description and other documentation. The brief description is the first sentence of the comment. It ends with a period followed by white space or a new line. For example:

```c++
/**
 * This is the brief description. This is the start of the detailed
 * description. Detailed Description continued.
 */
```

If you need to have a period in the brief description, follow it with a backslash followed by a space.

```c++
/**
 * e.g.\ This is a brief description with an internal period.
 */
```
Blank lines within these comments are interpreted as paragraph breaks to help you make the documentation more readble.

### Special commands

Placing these comments before the declaration works in most cases. For files however, you need to specify that you are documenting the file. To do this you use the @file special command. To document the file that you are currently in you just need to use the command followed by your comments. To comment a separate file (we shouldn't have to do this) you can supply the name directly after the file command. There are some other special commands we will be using quite often. To document functions we will use @param and @return or @retval to document the parameters and the return value. @param takes the name of the paramter and its description. @return just describes the return value, while @retval adds a name to it. To specify pre and post conditions you can use @pre and @post.

Some other useful commands are @todo and @sa. @todo allows you to place reminders of things to fix/implement and associate them with a specific class or member/function. @sa lets you place references to another piece of documentation (class, member, etc.). This can be useful to provide links to code that would be helpful in understanding the code being documented.

### Example of Simple Documentation

Here is a simple header file with doxygen comments added.

```c++
/**
 * @file
 * Contains an example of documentation style.
 */

#include <vector>

/**
 * Adds two numbers together.
 */
#define DUMMY(a,b) (a+b)

/**
 * A simple class description. This class does really great things in detail.
 *
 * @todo Update to new statistics model.
 */
class foo
{
  /** This variable stores blah, which does foo and has invariants x,y,z
         @warning never set this to 0
         @invariant foo
    */
   int myVar;

 /**
  * This function does something.
  * @param a The number of times to do it.
  * @param b The thing to do it to.
  * @return The number of times it was done.
  *
  * @sa DUMMY
  */
 int bar(int a, long b);


 /**
  * A function that does bar.
  * @retval true if there is a problem, false otherwise.
  */
 bool manchu();

};
```

### Grouping

Doxygen also allows for groups of classes and member (or other groups) to be declared. We can use these to create a listing of all statistics/global variables. Or just to comment about the memory hierarchy as a whole. You define a group using @defgroup and then add to it using @ingroup or @addgroup. For example:

```c++
/**
 * @defgroup statistics Statistics group
 */

/**
  * @defgroup substat1 Statistitics subgroup
  * @ingroup statistics
  */

/**
 *  A simple class.
 */
class foo
{
  /**
   * Collects data about blah.
   * @ingroup statistics
   */
  Stat stat1;

  /**
   * Collects data about the rate of blah.
   * @ingroup statistics
   */
  Stat stat2;

  /**
   * Collects data about flotsam.
   * @ingroup statistics
   */
  Stat stat3;

  /**
   * Collects data about jetsam.
   * @ingroup substat1
   */
  Stat stat4;

};
```

This places stat1-3 in the statistics group and stat4 in the subgroup. There is a shorthand method to place objects in groups. You can use @{ and @} to mark the start and end of group inclusion. The example above can be rewritten as:

```c++
/**
 * @defgroup statistics Statistics group
 */

/**
  * @defgroup substat1 Statistitics subgroup
  * @ingroup statistics
  */

/**
 *  A simple class.
 */
class foo
{
  /**
   * @ingroup statistics
   * @{
   */

  /** Collects data about blah.*/
  Stat stat1;
  /** Collects data about the rate of blah. */
  Stat stat2;
  /** Collects data about flotsam.*/
  Stat stat3;

  /** @} */

  /**
   * Collects data about jetsam.
   * @ingroup substat1
   */
  Stat stat4;

};
```

It remains to be seen what groups we can come up with.

### Other features

Not sure what other doxygen features we want to use.

## M5 Status Messages
### Fatal v. Panic

There are two error functions defined in `src/base/logging.hh:` `panic()` and `fatal()`. While these two functions have roughly similar effects (printing an error message and terminating the simulation process), they have distinct purposes and use cases. The distinction is documented in the comments in the header file, but is repeated here for convenience because people often get confused and use the wrong one.

* `panic()` should be called when something happens that should never ever happen regardless of what the user does (i.e., an actual m5 bug). `panic()` calls `abort()` which can dump core or enter the debugger.
* `fatal()` should be called when the simulation cannot continue due to some condition that is the user's fault (bad configuration, invalid arguments, etc.) and not a simulator bug. `fatal()` calls `exit(1)`, i.e., a "normal" exit with an error code.

The reasoning behind these definitions is that there's no need to panic if it's just a silly user error; we only panic if m5 itself is broken. On the other hand, it's not hard for users to make errors that are fatal, that is, errors that are serious enough that the m5 process cannot continue.
### Inform, Warn and Hack

The file `src/base/logging.hh` also houses 3 functions that alert the user to various conditions happening within the simulation: `inform()`, `warn()` and `hack()`. The purpose of these functions is strictly to provide simulation status to the user so none of these functions will stop the simulator from running.

* `inform()` and `inform_once()` should be called for informative messages that users should know, but not worry about. `inform_once()` will only display the status message generated by the `inform_once()` function the first time it is called.

* `warn()` and `warn_once()` should be called when some functionality isn't necessarily implemented correctly, but it might work well enough. The idea behind a `warn()` is to inform the user that if they see some strange behavior shortly after a `warn()` the description might be a good place to go looking for an error.

* `hack()` should be called when some functionality isn't implemented nearly as well as it could or should be but for expediency or history sake hasn't been fixed.
* `inform()` Provides status messages and normal operating messages to the console for the user to see, without any connotations of incorrect behavior.


---


## "Release Procedures"

*Source: https://www.gem5.org/documentation/general_docs/development/release_procedures/*

Information on when releases are carried out, how the community is notified, versioning information, and how to contribute to a release can be found in our [CONTRIBUTING.md document](https://github.com/gem5/gem5/blob/stable/CONTRIBUTING.md#releases).
The purpose of this document is to outline specific procedures carried out during a release.

## gem5 repository

The [gem5 git repository](https://github.com/gem5/gem5) has two branches, [stable](https://github.com/gem5/gem5/tree/stable) and [develop](https://github.com/gem5/gem5/tree/develop).
The HEAD of the stable branch is the latest official release of gem5 and will be tagged as such.
Users are not permitted to submit patches to the stable branch, and instead submit patches to the develop branch.
At least two weeks prior to a release a staging branch is created from the develop branch.
This staging branch is rigorously tested and only bug fixes or inconsequential changes (format fixes, typo fixes, etc.) are permitted to be be submitted to this branch.

The staging branch is updated with the following changes:

* The `-werror` is removed.
This ensures that gem5 compiles on newer compilers as new/stricter compiler warnings are incorporated.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/43425>.
* The [Doxygen "Project Number" field](https://github.com/gem5/gem5/blob/v21.0.1.0/src/Doxyfile#34) is updated to the version ID.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/47079>.
* The [`src/base/version.cc`](https://github.com/gem5/gem5/blob/stable/src/base/version.cc) file is updated to state the version ID.
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/47079>.
* The [`ext/testlib/configuration.py`](https://github.com/gem5/gem5/blob/stable/ext/testlib/configuration.py)  file's `default.resource_url` field is updated to point towards the correct Google Cloud release bucket (see [the Cloud Bucket release procedures](#gem5-resources-google-cloud-bucket)).
For example: <https://gem5-review.googlesource.com/c/public/gem5/+/44725>.
* The Resource downloader, `src/python/gem5/resources/downloader.py`, has a function `def _resources_json_version_required()`. This must be updated to the correct version of the `resources.json` file to use (see the [gem5 resources repository release procedures](#gem5-resources-repository)) for more information on this).
* The `tests/weekly.sh`, `tests/nightly.sh`, `tests/compiler-tests.sh`, and `tests/jenkins/presubmit.sh` should be updated ensure they remain stable across different gem5 releases. This is achieved by:
    1. Fix the docker pulls images by appending the version (example [here](https://gem5-review.googlesource.com/c/public/gem5/+/54470). This will be done after following the [docker image release procedures](#the-docker-images).
    2. Ensure the download links are downloading from the correct Google Cloud bucket for the release version.
* Hardcode the `rocm_patches/ROCclr.patch` download link in `util/dockerfiles/gcn-gpu` to the correct Google bucket.
* Update the `ext/sst/README.md` file for the current version. This simply means updating the download links.
See [here](https://gem5-review.googlesource.com/c/public/gem5/+/54703) for an example of how this is done.

When the staging branch is confirmed to be in a satisfactory state, it will be merged into both develop and stable.
There is then two additional actions:

1. The above changes to the staging branch are reverted on the develop branch.
2. The stable branch is tagged with the latest release version id at its HEAD.
    * For example, `git tag -a v21.1.0.0 -m "gem5 version 21.1.0.0" && git push --tags`

The [RELEASE-NOTES.md](https://github.com/gem5/gem5/blob/stable/RELEASE-NOTES.md) should be updated to notify the community of the major changes in this release.
This can be done on the develop branch prior to the creation of the staging branch, or on the staging branch.
It has been customary to create a blog post on <http://www.gem5.org> outlining the release.
While appreciated, it is not mandatory.

**Important notes:**
* You must a member of the "Project Owners" or "google/gem5-admins@googlegroups.com" Gerrit permission groups to push to the stable branch.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing to the gem5 stable branch.

## gem5 resources repository

The [gem5 resources git repository](https://github.com/gem5/gem5-resources) has two branches, [stable](https://github.com/gem5/gem5-resources/tree/stable) and [develop](https://github.com/gem5/gem5-resources/tree/develop).
The HEAD of the stable branch contains the source for resources with known compatibility to the most recently release of gem5.
E.g., if the current release of gem5 is v22.3, the head of gem5 resources repository will contain the source for resources with known compatibility with v22.3.
The develop branch contains sources compatible with the develop branch of the gem5 repository.
Unlike the gem5 repo, changes to the gem5 resources repo may be submitted to the stable branch permitting the changes are compatible with the latest release of gem5.

As with the gem5 repository, a staging branch is created at least two weeks prior to a release.
The purpose of this staging branch is identical to that of the main gem5 repository, and it is merged into both the stable and develop branches upon a gem5 release.
Prior to this the following changes should be applied to the staging branch:

* A new Google Cloud Bucket directory should be created for that version (see the [the Cloud Bucket release procedures](#gem5-resources-google-cloud-bucket)), and all the resources from the staging branch must match that found within that Google Cloud Bucket directory (i.e., the compiled resources within the bucket are built from the sources in the staging branch).
* URL download links in the resources repo should be updated to point towards the correct Google Cloud Bucket directory.
* The `resources.json` file, found in the root of the repository, must be updated for the current release.
[This patch](https://gem5-review.googlesource.com/c/public/gem5-resources/+/54403) shows an example of doing this.
The `version` field must be updated to the version that matches that in the `src/python/gem5/resources/downloader.py` file.
The `previous-version` list must be updated to support all versions prior, inclusive of develop.
Each previous version must map to a file that may be downloaded.
* The `resources.json` `url_base` field must be updated to the correct directory from the Google Cloud Bucket.

When merged into the develop branch, the URL download links should reverted back to `http://dist.gem5.org/dist/develop`.

Immediately prior to merging, the stable branch is tagged with the previous release version ID.
For example, if the staging branch is for `v22.2,` and the content on the stable branch is for `v22.1`, the stable branch will be tagged as `v22.1` immediately prior to the merge.
This is because we want users to be able to revert the gem5 resources to get sources compatible with previous gem5 releases.
Therefore, if a user wished to get the resources sources compatible with the the v20.1 release, they'd checkout the revision tagged as `v20.1` on the stable branch.

### gem5 resources Google Cloud Bucket

The built gem5 resources are found within the gem5 Google Cloud Bucket.

The [gem5 resources git repository](#gem5-resources-repository) contains sources of the gem5 resources, these are then compiled and stored in the Google Cloud Bucket.
The gem5 resources repo [README.md](https://github.com/gem5/gem5-resources/blob/stable/README.md) contains links to download the built resources from the Google Cloud Bucket.

The Google Cloud Bucket, like the gem5 resources repository, is versioned.
Each resource is stored under `http://dist.gem5.org/dist/{major version}`.
E.g., the PARSEC Benchmark image, for version 20.1, is stored at <http://dist.gem5.org/dist/v20-1/images/x86/ubuntu-18-04/parsec.img.gz>, while the image for version 21.0 is stored at <http://dist.gem5.org/dist/v21-0/images/x86/ubuntu-18-04/parsec.img.gz> (note the `.` substitution with `-` for the version in the URL).
The build for the develop branch is found under <http://dist.gem5.org/dist/develop>.

As the gem5 resources staging branch is from develop, the easiest way to create a copy of the develop bucket directory:

```
gsutil -m cp -r gs://dist.gem5.org/dist/develop gsutil -m cp -r gs://dist.gem5.org/dist/{major version}
```

The develop bucket _should_ be in-sync with the changes on develop.
Though this is worth checking.
Naturally, any changes on the staging branch must be reflected in the Cloud Bucket accordingly.

**Important notes:**
* Due to legacy reason <http://dist.gem5.org/dist/current> is used to store legacy resources related to v19 of gem5.
* Special permissions are needed to push to the Google Cloud Bucket.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing resources to the bucket.

## The docker images

Currently hosted in [`util/dockerfiles`](https://github.com/gem5/gem5/tree/stable/util/dockerfiles/) in the gem5 repository, we have a series of Dockerfiles which can be built to produce environments in which gem5 can be built and run.
These images are mostly used for testing purposes.
The [`ubuntu-20.04_all-dependencies`](https://github.com/gem5/gem5/tree/stable/util/dockerfiles/ubuntu-20.04_all-dependencies/) Dockerfile is the one most suitable for users who wish to build and execute gem5 in a supported environment.

We provide pre-built Docker images hosted at <ghcr.io> under "gem5".
All the Dockerfiles found in `util/dockerfiles` have been built and stored there.
For instance, `ubuntu-20.04_all-dependencies` can be found at <ghcr.io/gem5/ubuntu-20.04_all-dependencies> (and can thereby be obtained with `docker pull ghcr.io/gem5/ubuntu-20.04_all-dependencies`).

The Docker images are continually built from the Dockerfiles found on the develop branch.
Therefore the docker image with the `latest` tag is that in-sync with the Dockerfiles found on the gem5 repo's develop branch.
Upon a release of the latest version of gem5, when the staging branches are merged into develop, the built images hosted at <ghcr.io> will be tagged with the gem5 version number.
So, upon the release of `v23.2`, the images will be tagged with `v23-2`
The purpose of this is so users of an older versions of gem5, may obtain images compatible with their release.
I.e., a user of gem5 `v21.0` may obtain the `v21.0` version of the `ubuntu-20.04_all-dependencies` with `docker pull ghcr.io/gem5/ubuntu-20.04_all-dependencies:v21-0`.

**Important notes:**
* If changes to the Dockerfile are done on the staging branch, then these changes will need to be pushed to <ghcr.io> manually.
* Special permissions are needed to push to the <ghcr.io>.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing images.
* It is a future goal of ours to move [the Dockerfiles from `util/dockerfiles` to gem5-resources](https://gem5.atlassian.net/browse/GEM5-1044).

## gem5 website repository

The [gem5 website git repository](https://github.com/gem5/website/) has two branches, [stable](https://github.com/gem5/website/tree/stable) and [develop](https://github.com/gem5/website/tree/develop).
The stable branch is what is built and viewable at <http://www.gem5.org>, and is up-to-date with the current gem5 release.
E.g., if the current release of gem5, on its stable branch, is `v20.1`, the documentation on the stable branch will related to `v20.1`.
The develop branch contains the state of the website for the upcoming gem5 release.
E.g., it contains the changes needed to apply to the website when the new version of gem5 is released.

As the stable branch may be updated at any time (as long as those updates relate to the current release), stable is merged periodically into develop.
As with the gem5 resources, and the main gem5 repository, a staging branch is created from the develop branch at least two weeks prior to a gem5 release.

The staging branch needs updated so that the documentation is up-to-date with the upcoming release.
Of particular note, references to gem5 resources, hosted on the Google Cloud bucket should be updated.
For example, links to, say <http://dist.gem5.org/dist/v21-0/images/x86/ubuntu-18-04/parsec.img.gz>, would need to be updated to <http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/parsec.img.gz> when transitioning from `v21-0` to `v21-1`.

Upon a new major gem5 release, the develop branch is merged into stable.
The website repo is tagged with the preceding version prior to merging the staging branch into stable.
This is identical to the gem5 resources repository.
For example, if the current release is v21.1.0.4 and the next release is v21.2.0.0, immediately prior to the release of v21.2.0.0 the stable branch will be tagged as v21.1.0.4 then the develop branch merged into stable.
This ensures that a user may revert the website back to its state as of a previous release, if needed.

## gem5 Doxygen

The [gem5 Doxygen website](http://doxygen.gem5.org) is created by the [Doxygen documentation generator](https://www.doxygen.nl/index.html).
It can be created in gem5 repo as follows:

```
cd src
doxygen
```

The html will be output to `src/doxygen/html`.

The gem5 Doxygen website is hosted as a static webpage in a Google Cloud Bucket.
The directory structure is as follows:

```
doxygen.gem5.org/
    - develop/              # Contains the Doxygen for the gem5 develop branch.
        - index.html
        ...
    - release/              # An archive of the Doxygen for every gem5 release.
        - current/          # Doxygen for the current gem5 release.
            - index.html
            ...
        - v21-0-1-0/
            - index.html
            ...
        - v21-0-0-0/
            - index.html
            ...
        - v20-1-0-5/
            - index.html
            ...
        ...
    - index.html           # Redirects to release/current/index.html.
```

Therefore, the Doxygen for the latest release can be obtained at <http://doxygen.gem5.org/>, for the develop branch at <http://doxygen.gem5.org/develop>, and for past releases at <http://doxygen.gem5.org/release/{version}> (e.g., <http://doxygen.gem5.org/release/v20-1-0-5>).

After a gem5 release the following code is run on the gem5 repository stable branch

```
cd src
doxygen

gsutil -m rm gs://doxygen.gem5.org/release/current/*
gsutil -m cp -r doxygen/html/* gs://doxygen.gem5.org/release/current/
gsutil -m cp -r gs://doxygen.gem5.org/release/current gs://doxygen.gem5.org/release/{version id}
```

The final step is to add a link to this gem5 Doxygen version on the website, via the [`_data/documentation.yml` file](https://github.com/gem5/website/blob/stable/_data/documentation.yml).
For example: <https://gem5-review.googlesource.com/c/public/gem5-website/+/43385>.


**Important Notes:**
* The gem5 develop branch Doxygen website is updated daily via an automated build process.
The footer on the Doxygen website will state when the page was generated.
* Special permissions are needed to push to the Google Cloud Bucket.
Please contact Bobby R. Bruce (bbruce@ucdavis.edu) for help pushing to the Google Cloud Bucket.

## Minor and Hotfix releases

The previous sections have focus on major gem5 releases.
Minor and hotfix releases of gem5 should never change any API or features in a major way.
As such, for minor and hotfix releases of gem5 we only carry out the release procedures for the [gem5 code repository](#gem5-repository) and the [gem5 Doxygen website](#gem5-doxygen).
The latter may be unnecessary depending on the change/changes, but this is a low cost endeavor.


---


## "Full system support"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/*




---


## "Building Android Marshmallow"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/building_android_m*

# Building Android Marshmallow

This guide gives detailed step-by-step instructions on building an Android Marshmallow image along with a working kernel and .dtb file that work with gem5.

## Overview
To successfully run Android in gem5, an image, a compatible kernel and a device tree blob.dtb file configured for the simulator are necessary. This guide shows how to build Android Marshmallow 32bit version using a 3.14 kernel with Mali support. An extra section will be added in the future on how to build the 4.4 kernel with Mali.

## Pre-requisites
This guide assumes a 64-bit system running 14.04 LTS Ubuntu. Before starting it is important first to set up our system correctly. To do this the following packages need to be installed through shell.

**Tip: Always check for the up-to-date prerequisites at the Android build page.**

Update and install all the dependencies. This can be done with the following commands:

```
sudo apt-get update

sudo apt-get install openjdk-7-jdk git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev ccache libgl1-mesa-dev libxml2-utils xsltproc unzip
```

Also, make sure to have repo correctly installed [(instructions here)](https://source.android.com/source/downloading.html#installing-repo).

Ensure that the default JDK is OpenJDK 1.7:

```
javac -version
```

To cross-compile the kernel (32bit) and for the device tree we will need the following packages to be installed:

```
sudo apt-get install gcc-arm-linux-gnueabihf device-tree-compiler
```

Before getting started, as a final step make sure to have the gem5 binaries and busybox for 32-bit ARM.

For the gem5 binaries just do the following starting from your gem5 directory:
```
cd util/m5
make -f Makefile.arm
cd ../term
make
cd ../../system/arm/simple_bootloader/
make
```

For busybox you can find the guide [here](http://wiki.beyondlogic.org/index.php?title=Cross_Compiling_BusyBox_for_ARM).

## Building Android
We build Android Marshmallow using an AOSP running build based on the release for the Pixel C. The AOSP provides [other builds](https://source.android.com/source/build-numbers.html#source-code-tags-and-builds), which are untested with this guide.

**Tip: Synching with repo will take a long time. Use the -jN flag to speed up the make process, where N is the number of parallel jobs to run.**

Make a directory and pull the Android repository:

```
mkdir android
cd android
repo init --depth=1 -u https://android.googlesource.com/platform/manifest -b android-6.0.1_r63
repo sync -c -jN
```

Before you start the AOSP build, you will need to make one change to the build system to enable building libion.so, which is used by the Mali driver. Edit the file `aosp/system/core/libion/Android.mk` to change `LOCAL_MODULE_TAGS` for libion from 'optional' to 'debug'. Here is the output of `repo diff`: 

```
  --- a/system/core/libion/Android.mk
  +++ b/system/core/libion/Android.mk
  @@ -3,7 +3,7 @@ LOCAL_PATH := $(call my-dir)
  include $(CLEAR_VARS)
  LOCAL_SRC_FILES := ion.c
  LOCAL_MODULE := libion
  -LOCAL_MODULE_TAGS := optional
  +LOCAL_MODULE_TAGS := debug
  LOCAL_SHARED_LIBRARIES := liblog
  LOCAL_C_INCLUDES := $(LOCAL_PATH)/include $(LOCAL_PATH)/kernel-headers
  LOCAL_EXPORT_C_INCLUDE_DIRS := $(LOCAL_PATH)/include
  $(LOCAL_PATH)/kernel-headers
```

Source the environment setup and build Android:

**Tip: For root access and "debuggability" [sic] we choose userdebug. Build can be done in different modes as seen** [here](https://source.android.com/source/building.html#choose-a-target).
**Tip: Making Android will take a long time. Use the -jN flag to speed up the make process, where N is the number of parallel jobs to run.**

***Make sure to do this in a bash shell.***

```
source build/envsetup.sh
lunch aosp_arm-userdebug
make -jN
```

## Creating an Android image

After a successful build, we create an image of Android and add the init files and binaries that configure the system for gem5. The following example creates a 3GB image.

**Tip: If you want to add applications or data, make the image large enough to fit the build and anything else that is meant to be written into it.**

Create an empty image to flash the Android build and attach the image to a loopback device:

```
dd if=/dev/zero of=myimage.img bs=1M count=2560
sudo losetup /dev/loop0 myimage.img
```

We now need to create three partitions: AndroidRoot (1.5GB), AndroidData (1GB), and AndroidCache (512MB).

First, partition the device:

```
sudo fdisk /dev/loop0
```

Update the partition table:

```
sudo partprobe /dev/loop0
```

Name the partitions / Define filesystem as ext4:

```
sudo mkfs.ext4 -L AndroidRoot /dev/loop0p1
sudo mkfs.ext4 -L AndroidData /dev/loop0p
sudo mkfs.ext4 -L AndroidCache /dev/loop0p3
```

Mount the Root partition to a directory:

```
sudo mkdir -p /mnt/androidRoot
sudo mount /dev/loop0p1 /mnt/androidRoot
```

Load the build to the partition:

```
cd /mnt/androidRoot
sudo zcat <path/to/build/android>/out/target/product/generic/ramdisk.img | sudo cpio -i
sudo mkdir cache
sudo mkdir /mnt/tmp
sudo mount -oro,loop <path/to/build/android>/out/target/product/generic/system.img /mnt/tmp
sudo cp -a /mnt/tmp/* system/
sudo umount /mnt/tmp
```

Download and unpack the [overlays](http://dist.gem5.org/dist/current/arm/kitkat-overlay.tar.bz2) that are necessary from the [gem5 Android KitKat page](http://old.gem5.org/Android_KitKat.html "wikilink") and make the following changes to the `init.gem5.rc` file. Here is the output of `repo diff`: 

```
  --- /kitkat_overlay/init.gem5.rc
  +++ /m_overlay/init.gem5.rc
  @@ -1,21 +1,13 @@
  +
   on early-init
       mount debugfs debugfs /sys/kernel/debug
  
   on init
  -    export LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/vendor/lib/egl
  -
  -    # See storage config details at http://source.android.com/tech/storage/
  -    mkdir /mnt/media_rw/sdcard 0700 media_rw media_rw
  -    mkdir /storage/sdcard 0700 root root
  +    # Support legacy paths
  +    symlink /sdcard /mnt/sdcard
       chmod 0666 /dev/mali0
       chmod 0666 /dev/ion
  -
  -    export EXTERNAL_STORAGE /storage/sdcard
  -
  -    # Support legacy paths
  -    symlink /storage/sdcard /sdcard
  -    symlink /storage/sdcard /mnt/sdcard
  
   on fs
       mount_all /fstab.gem5
  @@ -60,7 +52,6 @@
       group root
       oneshot
  
  -# fusewrapped external sdcard daemon running as media_rw (1023)
  -service fuse_sdcard /system/bin/sdcard -u 1023 -g 1023 -d
  /mnt/media_rw/sdcard /storage/sdcard
  +service fingerprintd /system/bin/fingerprintd
       class late_start
  -    disabled
  +    user system
```

Add the Android overlays and configure their permissions:

```
sudo cp -r <path/to/android/overlays>/* /mnt/androidRoot/
sudo chmod ug+x /mnt/androidRoot/init.gem5.rc
/mnt/androidRoot/gem5/postboot.sh
```

Add the m5 and busybox binaries under the sbin directory and make them executable:

```
sudo cp <path/to/gem5>/util/m5/m5 /mnt/androidRoot/sbin
sudo cp <path/to/busybox>/busybox /mnt/androidRoot/sbin
sudo chmod a+x /mnt/androidRoot/sbin/busybox /mnt/androidRoot/sbin/m5
```

Make the directories readable and searchable:

```
sudo chmod a+rx /mnt/androidRoot/sbin/ /mnt/androidRoot/gem5/
```

Remove the boot animation:

```
sudo rm /mnt/androidRoot/system/bin/bootanimation
```

Download and unpack the Mali drivers, for gem5 Android 4.4, from [here](https://developer.arm.com/downloads/-/mali-drivers/midgard-kernel). Then, make the directories for the drivers and copy them:

```
sudo mkdir -p /mnt/androidRoot/system/vendor/lib/egl
sudo mkdir -p /mnt/androidRoot/system/vendor/lib/hw
sudo cp <path/to/userspace/Mali/drivers>/lib/egl/libGLES_mali.so /mnt/androidRoot/system/vendor/lib/egl
sudo cp <path/to/userspace/Mali/drivers>/lib/hw/gralloc.default.so /mnt/androidRoot/system/vendor/lib/hw
```

Change the permissions

```
sudo chmod 0755 /mnt/androidRoot/system/vendor/lib/hw
sudo chmod 0755 /mnt/androidRoot/system/vendor/lib/egl
sudo chmod 0644 /mnt/androidRoot/system/vendor/lib/egl/libGLES_mali.so
sudo chmod 0644 /mnt/androidRoot/system/vendor/lib/hw/gralloc.default.so
```

Unmount and remove loopback device:

```
cd /..
sudo umount /mnt/androidRoot
sudo losetup -d /dev/loop0
```

## Building the Kernel (3.14)

After successfully setting up the image, a compatible kernel needs to be built and a .dtb file generated.

Clone the repository containing the gem5 specific kernel:

```
git clone -b ll_20140416.0-gem5 https://github.com/gem5/linux-arm-gem5.git
```

Make the following changes to the kernel gem5 config file at `<path/to/kernel/repo>/arch/arm/configs/vexpress_gem5_defconfig`. Here is the output of `repo diff`:

```
  --- a/arch/arm/configs/vexpress_gem5_defconfig
  +++ b/arch/arm/configs/vexpress_gem5_defconfig
  @@ -200,4 +200,15 @@ CONFIG_EARLY_PRINTK=y
  CONFIG_DEBUG_PREEMPT=n
  # CONFIG_CRYPTO_ANSI_CPRNG is not set
  # CONFIG_CRYPTO_HW is not set
  +CONFIG_MALI_MIDGARD=y
  +CONFIG_MALI_MIDGARD_DEBUG_SYS=y
  +CONFIG_ION=y
  +CONFIG_ION_DUMMY=y
  CONFIG_BINARY_PRINTF=y
  +CONFIG_NET_9P=y
  +CONFIG_NET_9P_VIRTIO=y
  +CONFIG_9P_FS=y
  +CONFIG_9P_FS_POSIX_ACL=y
  +CONFIG_9P_FS_SECURITY=y
  +CONFIG_VIRTIO_BLK=y
  +CONFIG_VMSPLIT_3G=y
  +CONFIG_DNOTIFY=y
  +CONFIG_FUSE_FS=y
```

For the device tree, add the Mali GPU device and increase the memory to 1.8GB. Do this with the following changes at `<path/to/kernel/repo>/arch/arm/boot/dts/vexpress-v2p-ca15-tc1-gem5.dts.` Here is the output of `repo diff`:

```
  --- a/arch/arm/boot/dts/vexpress-v2p-ca15-tc1-gem5.dts
  +++ b/arch/arm/boot/dts/vexpress-v2p-ca15-tc1-gem5.dts
  @@ -45,7 +45,7 @@
  
           memory@80000000 {
                   device_type = "memory";
  -                reg = <0 0x80000000 0 0x40000000>;
  +                reg = <0 0x80000000 0 0x74000000>;
           };
  
          hdlcd@2b000000 {
  @@ -59,6 +59,14 @@
  //                mode = "3840x2160MR-16@60"; // UHD4K mode string
                    framebuffer = <0 0x8f000000 0 0x01000000>;
            };
  +
  +    gpu@0x2d000000 {
  +        compatible = "arm,mali-midgard";
  +        reg = <0 0x2b400000 0 0x4000>;
  +        interrupts = <0 86 4>, <0 87 4>, <0 88 4>;
  +        interrupt-names = "JOB", "MMU", "GPU";
  +    };
  +
  /*
          memory-controller@2b0a0000 {
                    compatible = "arm,pl341", "arm,primecell";
```

Download and unpack the userspace matching Mali kernel drivers for gem5 from [http://malideveloper.arm.com/resources/drivers/open-source-mali-midgard-gpu-kernel-drivers/ here]. Copy them to the gpu driver directory:

```
cp -r <path/to/kernelspace/Mali/drivers>/driver/product/kernel/drivers/gpu/arm/ drivers/gpu
```

Change the following in `<path/to/kernelspace/Mali/drivers>/drivers/video/Kconfig` and `<path/to/kernelspace/Mali/drivers>/drivers/gpu/Makefile` based on the following diffs:

Here is the output of the Kconfig `repo diff`:

```
  --- a/drivers/video/Kconfig
  +++ b/drivers/video/Kconfig
  @@ -23,6 +23,8 @@ source "drivers/gpu/host1x/Kconfig"
  
  source "drivers/gpu/drm/Kconfig"
  
  +source "drivers/gpu/arm/Kconfig"
  +
   config VGASTATE
          tristate
          default n
```

Here is the output of the drivers/gpu/Makefile `repo diff`:

```
  --- a/drivers/gpu/Makefile
  +++ b/drivers/gpu/Makefile
  @@ -1,2 +1,2 @@
  -obj-y                += drm/ vga/
  +obj-y                += drm/ vga/ arm/
```

Finally, build the kernel and the .dtb file.

**Tip: Use the -jN flag to speed up the make process, where N is the number of parallel jobs to run.**

Build the kernel:
```
make CROSS_COMPILE=arm-linux-gnueabihf- ARCH=arm vexpress_gem5_defconfig
make CROSS_COMPILE=arm-linux-gnueabihf- ARCH=arm vmlinux -jN
```

Create the .dtb file:

```
dtc -I dts -O dtb arch/arm/boot/dts/vexpress-v2p-ca15-tc1-gem5.dts > vexpress-v2p-ca15-tc1-gem5.dtb
```

## Testing the build

Make the following changes to example/fs.py. Here is the output ``repo diff``:

```
  --- a/configs/example/fs.py Thu Jun 02 20:34:39 2016 +0100
  +++ b/configs/example/fs.py Fri Jun 10 15:37:29 2016 -0700
  @@ -144,6 +144,13 @@
       if is_kvm_cpu(TestCPUClass) or is_kvm_cpu(FutureClass):
           test_sys.vm = KvmVM()
  
  +    test_sys.gpu = NoMaliGpu(
  +        gpu_type="T760",
  +        ver_maj=0, ver_min=0, ver_status=1,
  +        int_job=118, int_mmu=119, int_gpu=120,
  +        pio_addr=0x2b400000,
  +        pio=test_sys.membus.master)
  +
      if options.ruby:
          # Check for timing mode because ruby does not support atomic accesses
          if not (options.cpu_type == "detailed" or options.cpu_type == "timing"):
```

And the changes to FS config to either enable or disable software rendering.

```
  --- a/configs/common/FSConfig.py Thu Jun 02 20:34:39 2016 +0100
  +++ b/configs/common/FSConfig.py Thu Jun 16 10:23:44 2016 -0700
  @@ -345,7 +345,7 @@
  
             # release-specific tweaks
             if 'kitkat' in mdesc.os_type():
  -                cmdline += " androidboot.hardware=gem5 qemu=1 qemu.gles=0 " + \
  +                cmdline += " androidboot.hardware=gem5 qemu=1 qemu.gles=1 " + \
                            "android.bootanim=0"
  
         self.boot_osflags = fillInCmdline(mdesc, cmdline
```

Set the following M5\_PATH:

```
M5_PATH=. build/ARM/gem5.opt configs/example/fs.py --cpu-type=atomic --mem-type=SimpleMemory --os-type=android-kitkat --disk-image=myimage.img --machine-type=VExpress_EMM --dtb-filename=vexpress-v2p-ca15-tc1-gem5.dtb -n 1 --mem-size=1800MB
```

## Building older versions of Android

gem5 has support for running even older versions of Android like KitKat. The documentation to do so, as well as the necessary drivers and files required, can be found on the old wiki [here](http://old.gem5.org/Android_KitKat.html).


---


## "Building ARM Kernel"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/building_arm_kernel*

# Building ARM Kernel

This page contains instructions for building up-to-date kernels for gem5 running on ARM. 

If you don't want to build the Kernel (or a disk image) on your own you could still [download a
prebuilt version](./guest_binaries).

## Prerequisites
These instructions are for running headless systems. That is a more "server" style system where there is no frame-buffer. The description has been created using the latest known-working tag in the repositories linked below, however the tables in each section list previous tags that are known to work. To built the kernels on an x86 host you'll need ARM cross compilers and the device tree compiler. If you're running a reasonably new version of Ubuntu or Debian you can get required software through apt:

```
apt-get install  gcc-arm-linux-gnueabihf gcc-aarch64-linux-gnu device-tree-compiler
```

If you can't use these pre-made compilers the next easiest way to obtain the
required compilers from ARM:
- [Cortex A cross-compilers](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads)
- [Cortex RM cross-compilers](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)

Download (one of) these and make sure the binaries are on your `PATH`.

Depending on the exact source of your cross compilers, the compiler names used below will required small changes.

To actually run the kernel, you'll need to download or compile gem5's
bootloader. See the [bootloaders](#bootloaders) section in this documents for
details.

## Linux 4.x
Newer gem5 kernels for ARM (v4.x and later) are based on the vanilla Linux kernel and typically have a small number of patches to make them work better with gem5. The patches are optional and you should be able to use a vanilla kernel as well. However, this requires you to configure the kernel yourself. Newer kernels all use the VExpress\_GEM5\_V1 gem5 platform for both AArch32 and AArch64.

# Kernel Checkout
To checkout the kernel, execute the following command:

```
git clone https://gem5.googlesource.com/arm/linux
```

The repository contains a tag per gem5 kernel releases and working branches for major Linux revisions. Check the [project page](https://gem5-review.googlesource.com/#/admin/projects/arm/linux) for a list of tags and branches. The clone command will, by default, check out the latest release branch. To checkout the v4.14 branch, execute the following in the repository:
```
git checkout -b gem5/v4.14
```

# Kernel build
To compile the kernel, execute the following commands in the repository:

```
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- gem5_defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j `nproc`
```

Testing the just built kernel:

```
./build/ARM/gem5.opt configs/example/arm/starter_fs.py --kernel=/tmp/linux-arm-gem5/vmlinux \
    --disk-image=ubuntu-18.04-arm64-docker.img
```

# Bootloaders
There are two different bootloaders for gem5. One of 32-bit kernels and one for 64-bit kernels. They can be compiled using the following command:

```
make -C system/arm/bootloader/arm
make -C system/arm/bootloader/arm64
```

# Device Tree Blobs
The required DTB files to describe the hardware to the OS ship with gem5. To build them, execute this command:

```
make -C system/arm/dt
```

We recommend to use these device tree files only if you are planning to amend them. If not, we recommend you to rely on DTB autogeneration: by running a FS script without the --dtb option, gem5 will automatically generate the DTB on the fly depending on the instantiated platform.

Once you have compiled the binaries, put them in the binaries directory in your
`M5_PATH`.


---


## Devices

*Source: https://www.gem5.orgdocumentation/general_docs/fullsystem/devices*

# Devices in full system mode

## I/O Device Base Classes

The base classes in src/dev/\*_device.\* allow devices to be created with reasonable ease.
The classes and virtual functions that must be implemented are listed below.
Before reading the following it will help to be familiar with the [Memory_System](../memory_system).

### PioPort

The PioPort class is a programmed I/O port that all devices that are sensitive to an address range use.
The port takes all the memory access types and roles them into one `read()` and `write()` call that the device must respond to.
The device must also provide the `addressRanges()` function with which it returns the address ranges it is interested in.
If desired a device could have more than one PIO port.
However in the normal case it would only have one port and return multiple ranges when the `addressRange()` function is called. The only time multiple PIO ports would be desirable is if your device wanted to have separate connection to two memory objects.

### PioDevice

This is the base class which all devices senstive to an address range inherit from.
There are three pure virtual functions which all devices must implement `addressRanges()`, `read()`, and `write()`.
The magic to choose which mode we are in, etc is handled by the PioPort so the device doesn't have to bother.

Parameters for each device should be in a Params struct derived from `PioDevice::Params`.

### BasicPioDevice

Since most PioDevices only respond to one address range `BasicPioDevice` provides an `addressRanges()` and parameters for the normal pio delay and the address to which the device responds to.
Since the size of the device normally isn't configurable a parameter is not used for this and anything that inherits from this class is expected to write it's size into pioSize in its constructor.

### DmaPort

The DmaPort (in dma_device.hh) is used only for device mastered accesses.
The `recvTimingResp()` method must be available to responses (nacked or not) to requests it makes.
The port has two public methods `dmaPending()` which returns if the dma port is busy (e.g. It is still trying to send out all the pieces of the last request).
All the code to break requests up into suitably sized chunks, collect the potentially multiple responses and respond to the device is accessed through `dmaAction()`.
A command, start address, size, completion event, and possibly data is handed to the function which will then execute the completion events `process()` method when the request has been completed.
Internally the code uses `DmaReqState` to manage what blocks it has received and to know when to execute the completion event.

### DmaDevice

This is the base class from which a DMA non-pci device would inherit from, however none of those exist currently within M5. The class does have some methods `dmaWrite()`, `dmaRead()` that select the appropriate command from a DMA read or write operation.

### NIC Devices

The gem5 simulator has two different Network Interface Cards (NICs) devices that can be used to connect together two simulation instances over a simulated ethernet link.

#### Getting a list of packets on the ethernet link

You can get a list of the packet on the ethernet link by creating a Etherdump object, setting it's file parameter, and setting the dump parameter on the EtherLink to it.
This is easily accomplished with our fs.py example configuration by adding the command line option \-\-etherdump=\<filename\>. The resulting file will be named \<file\> and be in a standard pcap format.
This file can be read with [wireshark](https://www.wireshark.org/) or anything else that understands the pcap format.


### PCI devices
```
To do: Explanation of platforms and systems, how they’re related, and what they’re each for
```


---


## Creating disk images

*Source: https://www.gem5.orgdocumentation/general_docs/fullsystem/disks*

# Creating disk images for full system mode

In full-system mode, gem5 relies on a disk image with an installed operating system to run simulations.
A disk device in gem5 gets its initial contents from disk image.
The disk image file stores all the bytes present on the disk just as you would find them on an actual device.
Some other systems also use disk images which are in more complicated formats and which provide compression, encryption, etc. gem5 currently only supports raw images, so if you have an image in one of those other formats, you'll have to convert it into a raw image before you can use it in a simulation.
There are often tools available which can convert between the different formats.

There are multiple ways of creating a disk image which can be used with gem5.
Following are four different methods to build disk images:

- Using gem5 utils to create a disk image
- Using gem5 utils and chroot to create a disk image
- Using QEMU to create a disk image
- Using Packer to create a disk image

All of these methods are independent of each other.
Next, we will discuss each of these methods one by one.

## 1) Using gem5 utils to create a disk image

```md
Disclaimer: This is from the old website and some of the stuff in this method can be out-dated.

```
Because a disk image represents all the bytes on the disk itself, it contains more than just a file system.
For hard drives on most systems, the image starts with a partition table.
Each of the partitions in the table (frequently only one) is also in the image.
If you want to manipulate the entire disk you'll use the entire image, but if you want to work with just one partition and/or the file system on it, you'll need to specifically select that part of the image.
The losetup command (discussed below) has a -o option which lets you specify where to start in an image.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Oh3NK12fnbg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><div class='thumbcaption'>A youtube video of working with image files using qemu on Ubuntu 12.04 64bit. Video resolution can be set to 1080</div>


### Creating an empty image

You can use the ./util/gem5img.py script provided with gem5 to build the disk image.
It's a good idea to understand how to build an image in case something goes wrong or you need to do something in an unusual way.
However, in this mehtod, we are using gem5img.py script to go through the process of building and formatting an image.
If you want to understand the guts of what it's doing see below.
Running gem5img.py may require you to enter the sudo password.
*You should never run commands as the root user that you don't understand! You should look at the file util/gem5img.py and ensure that it isn't going to do anything malicious to your computer!*

You can use the "init" option with gem5img.py to create an empty image, "new", "partition", or "format" to perform those parts of init independently, and "mount" or "umount" to mount or unmount an existing image.

### Mounting an image

To mount a file system on your image file, first find a loopback device and attach it to your image with an appropriate offset as will be described further in the [Formatting](#formatting) section.

```sh
mount -o loop,offset=32256 foo.img
```

<iframe width="560" height="315" src="https://www.youtube.com/embed/OXH1oxQbuHA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><div class='thumbcaption'>A youtube video of add file using mount on Ubuntu 12.04 64bit. Video resolution can be set to 1080</div>

### Unmounting

To unmount an image, use the umount command like you normally would.

```sh
umount
```

### Image Contents

Now that you can create an image file and mount it's file system, you'll want to actually put some files in it.
You're free to use whatever files you want, but the gem5 developers have found that Gentoo stage3 tarballs are a great starting point.
They're essentially an almost bootable and fairly minimal Linux installation and are available for a number of architectures.

If you choose to use a Gentoo tarball, first extract it into your mounted image.
The /etc/fstab file will have placeholder entries for the root, boot, and swap devices.
You'll want to update this file as apporpriate, deleting any entries you aren't going to use (the boot partition, for instance).
Next, you'll want to modify the inittab file so that it uses the m5 utility program (described elsewhere) to read in the init script provided by the host machine and to run that.
If you allow the normal init scripts to run, the workload you're interested in may take much longer to get started, you'll have no way to inject your own init script to dynamically control what benchmarks are started, for instance, and you'll have to interact with the simulation through a simulated terminal which introduces non-determinism.

#### Modifications

By default gem5 does not store modifications to the disk back to the underlying image file.
Any changes you make will be stored in an intermediate COW layer and thrown away at the end of the simulation.
You can turn off the COW layer if you want to modify the underlying disk.

#### Kernel and bootloader

Also, generally speaking, gem5 skips over the bootloader portion of boot and loads the kernel into simulated memory itself. This means that there's no need to install a bootloader like grub to your disk image, and that you don't have to put the kernel you're going to boot from on the image either.
The kernel is provided separately and can be changed out easily without having to modify the disk image.

### Manipulating images with loopback devices

#### Loopback devices

Linux supports loopback devices which are devices backed by files.
By attaching one of these to your disk image, you can use standard Linux commands on it which normally run on real disk devices.
You can use the mount command with the "loop" option to set up a loopback device and mount it somewhere.
Unfortunately you can't specify an offset into the image, so that would only be useful for a file system image, not a disk image which is what you need.
You can, however, use the lower level losetup command to set up a loopback device yourself and supply the proper offset.
Once you've done that, you can use the mount command on it like you would on a disk partition, format it, etc.
If you don't supply an offset the loopback device will refer to the whole image, and you can use your favorite program to set up the partitions on it.

### Working with image files

To create an empty image from scratch, you'll need to create the file itself, partition it, and format (one of) the partition(s) with a file system.

####  Create the actual file

First, decide how large you want your image to be.
It's a good idea to make it large enough to hold everything you know you'll need on it, plus some breathing room.
If you find out later it's too small, you'll have to create a new larger image and move everything over.
If you make it too big, you'll take up actual disk space unnecessarily and make the image harder to work with.
Once you've decided on a size you'll want to actually create the file.
Basically, all you need to do is create a file of a certain size that's full of zeros.
One approach is to use the dd command to copy the right number of bytes from /dev/zero into the new file.
Alternatively you could create the file, seek in it to the last byte, and write one zero byte.
All of the space you skipped over will become part of the file and is defined to read as zeroes, but because you didn't explicitly write any data there, most file systems are smart enough to not actually store that to disk.
You can create a large image that way but take up very little space on your physical disk.
Once you start writing to the file later that will change, and also if you're not careful, copying the file may expand it to its full size.

#### Partitioning

First, find an available loopback device using the losetup command with the -f option.

```sh
losetup -f
```

Next, use losetup to attach that device to your image.
If the available device was /dev/loop0 and your image is foo.img, you would use a command like this.

```sh
losetup /dev/loop0 foo.img
```

/dev/loop0 (or whatever other device you're using) will now refer to your entire image file.
Use whatever partitioning program you like on it to set up one (or more) paritions.
For simplicity it's probably a good idea to create only one parition that takes up the entire image.
We say it takes up the entire image, but really it takes up all the space except for the partition table itself at the beginning of the file, and possibly some wasted space after that for DOS/bootloader compatibility.

From now on we'll want to work with the new partition we created and not the whole disk, so we'll free up the loopback device using losetup's -d option

```sh
losetup -d /dev/loop0
```

#### Formatting

First, find an available loopback device like we did in the partitioning step above using losetup's -f option.

```sh
losetup -f
```

We'll attach our image to that device again, but this time we only want to refer to the partition we're going to put a file system on.
For PC and Alpha systems, that partition will typically be one track in, where one track is 63 sectors and each sector is 512 bytes, or 63 * 512 = 32256 bytes.
The correct value for you may be different, depending on the geometry and layout of your image.
In any case, you should set up the loopback device with the -o option so that it represents the partition you're interested in.

```sh
losetup -o 32256 /dev/loop0 foo.img
```

Next, use an appropriate formating command, often mke2fs, to put a file system on the partition.

```sh
mke2fs /dev/loop0
```

You've now successfully created an empty image file.
You can leave the loopback device attached to it if you intend to keep working with it (likely since it's still empty) or clean it up using losetup -d.

```sh
losetup -d /dev/loop0
```

Don't forget to clean up the loopback device attached to your image with the losetup -d command.

```sh
losetup -d /dev/loop0
```

## 2) Using gem5 utils and chroot to create a disk image

The discussion in this section assumes that you have already checked out a version of gem5 and can build and run gem5 in full-system mode.
We will use the x86 ISA for gem5 in this discussion, and this is mostly applicable to other ISAs as well.

### Creating a blank disk image

The first step is to create a blank disk image (usually a .img file).
This is similar to what we did in the first metod.
We can use the gem5img.py script provided by gem5 developers.
To create a blank disk image, which is formatted with ext2 by default, simply run the following.

```
> util/gem5img.py init ubuntu-14.04.img 4096
```

This command creates a new image, called "ubuntu-14.04.img" that is 4096 MB.
This command may require you to enter the sudo password, if you don't have permission to create loopback devices.
*You should never run commands as the root user that you don't understand! You should look at the file util/gem5img.py and ensure that it isn't going to do anything malicious to your computer!*

We will be using util/gem5img.py heavily throughout this section, so you may want to understand it better.
If you just run `util/gem5img.py`, it displays all of the possible commands.

```
Usage: %s [command] <command arguments>
where [command] is one of
    init: Create an image with an empty file system.
    mount: Mount the first partition in the disk image.
    umount: Unmount the first partition in the disk image.
    new: File creation part of "init".
    partition: Partition part of "init".
    format: Formatting part of "init".
Watch for orphaned loopback devices and delete them with
losetup -d. Mounted images will belong to root, so you may need
to use sudo to modify their contents
```

### Copying root files to the disk

Now that we have created a blank disk, we need to populate it with all of the OS files.
Ubuntu distributes a set of files explicitly for this purpose.
You can find the [Ubuntu core](https://wiki.ubuntu.com/Core) distribution for 14.04 at <http://cdimage.ubuntu.com/releases/14.04/release/>. Since we are simulating an x86 machine, we will use `ubuntu-core-14.04-core-amd64.tar.gz`.
Download whatever image is appropriate for the system you are simulating.

Next, we need to mount the blank disk and copy all of the files onto the disk.

```
mkdir mnt
../../util/gem5img.py mount ubuntu-14.04.img mnt
wget http://cdimage.ubuntu.com/ubuntu-core/releases/14.04/release/ubuntu-core-14.04-core-amd64.tar.gz
sudo tar xzvf ubuntu-core-14.04-core-amd64.tar.gz -C mnt
```

The next step is to copy a few required files from your working system onto the disk so we can chroot into the new disk. We need to copy `/etc/resolv.conf` onto the new disk.

```
sudo cp /etc/resolv.conf mnt/etc/
```

### Setting up gem5-specific files

#### Create a serial terminal

By default, gem5 uses the serial port to allow communication from the host system to the simulated system. To use this, we need to create a serial tty.
Since Ubuntu uses upstart to control the init process, we need to add a file to /etc/init which will initialize our terminal.
Also, in this file, we will add some code to detect if there was a script passed to the simulated system.
If there is a script, we will execute the script instead of creating a terminal.

Put the following code into a file called /etc/init/tty-gem5.conf

```
# ttyS0 - getty
#
# This service maintains a getty on ttyS0 from the point the system is
# started until it is shut down again, unless there is a script passed to gem5.
# If there is a script, the script is executed then simulation is stopped.

start on stopped rc RUNLEVEL=[12345]
stop on runlevel [!12345]

console owner
respawn
script
   # Create the serial tty if it doesn't already exist
   if [ ! -c /dev/ttyS0 ]
   then
      mknod /dev/ttyS0 -m 660 /dev/ttyS0 c 4 64
   fi

   # Try to read in the script from the host system
   /sbin/m5 readfile > /tmp/script
   chmod 755 /tmp/script
   if [ -s /tmp/script ]
   then
      # If there is a script, execute the script and then exit the simulation
      exec su root -c '/tmp/script' # gives script full privileges as root user in multi-user mode
      /sbin/m5 exit
   else
      # If there is no script, login the root user and drop to a console
      # Use m5term to connect to this console
      exec /sbin/getty --autologin root -8 38400 ttyS0
   fi
end script
```

#### Setup localhost

We also need to set up the localhost loopback device if we are going to use any applications that use it.
To do this, we need to add the following to the `/etc/hosts` file.

```
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

#### Update fstab

Next, we need to create an entry in `/etc/fstab` for each partition we want to be able to access from the simulated system. Only one partition is absolutely required (`/`); however, you may want to add additional partitions, like a swap partition.

The following should appear in the file `/etc/fstab`.

```
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system>    <mount point>   <type>  <options>   <dump>  <pass>
/dev/hda1      /       ext3        noatime     0 1
```

#### Copy the `m5` binary to the disk

gem5 comes with an extra binary application that executes pseudo-instructions to allow the simulated system to interact with the host system.
To build this binary, run `make -f Makefile.<isa>` in the `gem5/m5` directory, where `<isa>` is the ISA that you are simulating (e.g., x86). After this, you should have an `m5` binary file.
Copy this file to /sbin on your newly created disk.

After updating the disk with all of the gem5-specific files, unless you are going on to add more applications or copying additional files, unmount the disk image.

```
> util/gem5img.py umount mnt
```

### Install new applications

The easiest way to install new applications on to your disk, is to use `chroot`.
This program logically changes the root directory ("/") to a different directory, mnt in this case.
Before you can change the root, you first have to set up the special directories in your new root. To do
this, we use `mount -o bind`.

```
> sudo /bin/mount -o bind /sys mnt/sys
> sudo /bin/mount -o bind /dev mnt/dev
> sudo /bin/mount -o bind /proc mnt/proc
```

After binding those directories, you can now `chroot`:

```
> sudo /usr/sbin/chroot mnt /bin/bash
```

At this point you will see a root prompt and you will be in the `/`
directory of your new disk.

You should update your repository information.

```
> apt-get update
```

You may want to add the universe repositories to your list with the
following commands.
Note: The first command is require in 14.04.

```
> apt-get install software-properties-common
> add-apt-repository universe
> apt-get update
```

Now, you are able to install any applications you could install on a
native Ubuntu machine via `apt-get`.

Remember, after you exit you need to unmount all of the directories we
used bind on.

```
> sudo /bin/umount mnt/sys
> sudo /bin/umount mnt/proc
> sudo /bin/umount mnt/dev
```


## 3) Using QEMU to create a disk image

This method is a follow-up on the previous method to create a disk image.
We will see how to create, edit and set up a disk image using qemu instead of relying on gem5 tools.
This section assumes that you have installed qemu on your system.
In Ubuntu, this can be done with

```
sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
```

### Step 1: Create an empty disk
Using the qemu disk tools, create a blank raw disk image.
In this case, I chose to create a disk named "ubuntu-test.img" that is 8GB.

```
qemu-img create ubuntu-test.img 8G
```

### Step 2: Install ubuntu with qemu
Now that we have a blank disk, we are going to use qemu to install Ubuntu on the disk.
It is encouraged that you use the server version of Ubuntu since gem5 does not have great support for displays.
Thus, the desktop environment isn't very useful.

First, you need to download the installation CD image from the [Ubuntu website](https://www.ubuntu.com/download/server).

Next, use qemu to boot off of the CD image, and set the disk in the system to be the blank disk you created above.
Ubuntu needs at least 1GB of memory to install correctly, so be sure to configure qemu to use at least 1GB memory.

```
qemu-system-x86_64 -hda ../gem5-fs-testing/ubuntu-test.img -cdrom ubuntu-16.04.1-server-amd64.iso -m 1024 -enable-kvm -boot d
```

With this, you can simply follow the on-screen directions to install Ubuntu to the disk image.
The only gotcha in the installation is that gem5's IDE drivers don't seem to play nicely with logical paritions.
Thus, during the Ubuntu install, be sure to manually partition the disk and remove any logical partitions.
You don't need any swap space on the disk anyway, unless you're doing something specifically with swap space.

### Step 3: Boot up and install needed software

Once you have installed Ubuntu on the disk, quit qemu and remove the `-boot d` option so that you are not booting off of the CD anymore.
Now, you can again boot off of the main disk image you have installed Ubuntu on.

Since we're using qemu, you should have a network connection (although [ping won't
work](http://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29)).
When booting in qemu, you can just use `sudo apt-get install` and
install any software you need on your disk.

```
qemu-system-x86_64 -hda ../gem5-fs-testing/ubuntu-test.img -cdrom ubuntu-16.04.1-server-amd64.iso -m 1024 -enable-kvm
```

### Step 4: Update init script

By default, gem5 expects a modified init script which loads a script off of the host to execute in the guest.
To use this feature, you need to follow the steps below.

Alternatively, you can install the precompiled binaries for x86 found on this [website](http://cs.wisc.edu/~powerjg/files/gem5-guest-tools-x86.tgz).
From qemu, you can run the following, which completes the above steps for you.

```
wget http://cs.wisc.edu/~powerjg/files/gem5-guest-tools-x86.tgz
tar xzvf gem5-guest-tools-x86.tgz
cd gem5-guest-tools/
sudo ./install
```

Now, you can use the `system.readfile` parameter in your Python config scripts. This file will automatically be loaded (by the `gem5init` script) and executed.

### Manually installing the gem5 init script

First, build the m5 binary on the host.

```
cd util/m5
make -f Makefile.x86
```

Then, copy this binary to the guest and put it in `/sbin`. Also, create a link from `/sbin/gem5`.

Then, to get the init script to execute when gem5 boots, create file /lib/systemd/system/gem5.service with the following:

```
[Unit]
Description=gem5 init script
Documentation=http://gem5.org
After=getty.target

[Service]
Type=idle
ExecStart=/sbin/gem5init
StandardOutput=tty
StandardInput=tty-force
StandardError=tty

[Install]
WantedBy=default.target
```

Enable the gem5 service and **disable the ttyS0 service**.
If your disk boots up to a login prompt, it might be caused by not disabling the ttyS0 service.

```
systemctl enable gem5.service
```

Finally, create the init script that is executed by the service. In
`/sbin/gem5init`:

```
#!/bin/bash -

CPU=`cat /proc/cpuinfo | grep vendor_id | head -n 1 | cut -d ' ' -f2-`
echo "Got CPU type: $CPU"

if [ "$CPU" != "M5 Simulator" ];
then
    echo "Not in gem5. Not loading script"
    exit 0
fi

# Try to read in the script from the host system
/sbin/m5 readfile > /tmp/script
chmod 755 /tmp/script
if [ -s /tmp/script ]
then
    # If there is a script, execute the script and then exit the simulation
    su root -c '/tmp/script' # gives script full privileges as root user in multi-user mode
    sync
    sleep 10
    /sbin/m5 exit
fi
echo "No script found"
```

### Problems and (some) solutions

You might run into some problems while following this method.
Some of the issues and solutions are discussed on this [page](http://www.lowepower.com/jason/setting-up-gem5-full-system.html).

## 4) Using Packer to create a disk image

This section discusses an automated way of creating gem5-compatible disk images with Ubuntu server installed. We make use of packer to do this which makes use of a .json template file to build and configure a disk image. The template file could be configured to build a disk image with specific benchmarks installed. The mentioned template file can be found [here](/assets/files/packer_template.json).


### Building a Simple Disk Image with Packer

#### a. How It Works, Briefly
We use [Packer](https://www.packer.io/) and [QEMU](https://www.qemu.org/) to automate the process of disk creation.
Essentially, QEMU is responsible for setting up a virtual machine and all interactions with the disk image during the building process.
The interactions include installing Ubuntu Server to the disk image, copying files from your machine to the disk image, and running scripts on the disk image after Ubuntu is installed.
However, we will not use QEMU directly.
Packer provides a simpler way to interact with QEMU using a JSON script, which is more expressive than using QEMU from command line.

#### b. Install Required Software/Dependencies
If not already installed, QEMU can be installed using:
```shell
sudo apt-get install qemu
```
Download the Packer binary from [the official website](https://www.packer.io/downloads.html).

#### c. Customize the Packer Script
The default packer script `template.json` should be modified and adapted according to the required disk image and the avaiable resources for the build proces. We will rename the default template to `[disk-name].json`. The variables that should be modified appear at the end of `[disk-name].json` file, in `variables` section.
The configuration files that are used to build the disk image, and the directory structure is shown below:
```shell
disk-image/
    [disk-name].json: packer script
    Any experiment-specific post installation script
    post-installation.sh: generic shell script that is executed after Ubuntu is installed
    preseed.cfg: preseeded configuration to install Ubuntu
```

##### i. Customizing the VM (Virtual Machine)
In `[disk-name].json`, following variables are available to customize the VM:

| Variable         | Purpose     | Example  |
| ---------------- |-------------|----------|
| [vm_cpus](https://www.packer.io/docs/builders/qemu.html#cpus) **(should be modified)** | number of host CPUs used by VM | "2": 2 CPUs are used by the VM |
| [vm_memory](https://www.packer.io/docs/builders/qemu.html#memory) **(should be modified)**| amount of VM memory, in MB | "2048": 2 GB of RAM are used by the VM |
| [vm_accelerator](https://www.packer.io/docs/builders/qemu.html#accelerator) **(should be modified)** | accelerator used by the VM e.g. Kvm | "kvm": kvm will be used |

<br />

##### ii. Customizing the Disk Image
In `[disk-name].json`, disk image size can be customized using following variable:

| Variable        | Purpose     | Example  |
| ---------------- |-------------|----------|
| [image_size](https://www.packer.io/docs/builders/qemu.html#disk_size) **(should be modified)** | size of the disk image, in megabytes | "8192": the image has the size of 8 GB  |
| [image_name] | name of the built disk image | "boot-exit"  |

<br />

##### iii. File Transfer
While building a disk image, users would need to move their files (benchmarks, data sets etc.) to
the disk image. In order to do this file transfer, in `[disk-name].json` under `provisioners`, you could add the following:

```shell
{
    "type": "file",
    "source": "post_installation.sh",
    "destination": "/home/gem5/",
    "direction": "upload"
}
```
The above example copies the file `post_installation.sh` from the host to `/home/gem5/` in the disk image.
This method is also capable of copying a folder from host to the disk image and vice versa.
It is important to note that the trailing slash affects the copying process [(more details)](https://www.packer.io/docs/provisioners/file.html#directory-uploads).
The following are some notable examples of the effect of using slash at the end of the paths.

| `source`        | `destination`     | `direction`  |  `Effect`  |
| ---------------- |-------------|----------|-----|
| `foo.txt` | `/home/gem5/bar.txt` | `upload` | copy file (host) to file (image) |
| `foo.txt` | `bar/` | `upload` | copy file (host) to folder (image) |
| `/foo` | `/tmp` | `upload` | `mkdir /tmp/foo` (image);  `cp -r /foo/* (host) /tmp/foo/ (image)`; |
| `/foo/` | `/tmp` | `upload` | `cp -r /foo/* (host) /tmp/ (image)` |

If `direction` is `download`, the files will be copied from the image to the host.

**Note**: [This is a way to run script once after installing Ubuntu without copying to the disk image](#customizingscripts3).

##### iv. Install Benchmark Dependencies
To install the dependencies, you can use a bash script `post_installation.sh`, which will be run after the Ubuntu installation and file copying is done.
For example, if we want to install `gfortran`, add the following in `post_installation.sh`:
```shell
echo '12345' | sudo apt-get install gfortran;
```
In the above example, we assume that the user password is `12345`.
This is essentially a bash script that is executed on the VM after the file copying is done, you could modify the script as a bash script to fit any purpose.

##### v. Running Other Scripts on Disk Image
In `[disk-name].json`, we could add more scripts to `provisioners`.
Note that the files are on the host, but the effects are on the disk image.
For example, the following example runs `post_installation.sh` after Ubuntu is installed,
{% raw %}
```sh
{
    "type": "shell",
    "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
    "scripts":
    [
        "post-installation.sh"
    ]
}
```
{% endraw %}

#### d. Build the Disk Image

##### i. Build
In order to build a disk image, the template file is first validated using:
```sh
./packer validate [disk-name].json
```
Then, the template file can be used to build the disk image:
```sh
./packer build [disk-name].json
```

On a fairly recent machine, the building process should not take more than 15 minutes to complete.
The disk image with the user-defined name (image_name) will be produced in a folder called [image_name]-image.
[We recommend to use a VNC viewer in order to inspect the building process](#inspect).

##### ii. Inspect the Building Process
While the building of disk image takes place, Packer will run a VNC (Virtual Network Computing) server and you will be able to see the building process by connecting to the VNC server from a VNC client. There are a plenty of choices for VNC client. When you run the Packer script, it will tell you which port is used by the VNC server. For example, if it says `qemu: Connecting to VM via VNC (127.0.0.1:5932)`, the VNC port is 5932.
To connect to VNC server from the VNC client, use the address `127.0.0.1:5932` for a port number 5932.
If you need port forwarding to forward the VNC port from a remote machine to your local machine, use SSH tunneling
```shell
ssh -L 5932:127.0.0.1:5932 <username>@<host>
```
This command will forward port 5932 from the host machine to your machine, and then you will be able to connect to the VNC server using the address `127.0.0.1:5932` from your VNC viewer.

**Note**: While Packer is installing Ubuntu, the terminal screen will display "waiting for SSH" without any update for a long time.
This is not an indicator of whether the Ubuntu installation produces any errors.
Therefore, we strongly recommend using VNC viewer at least once to inspect the image building process.


---


## "Guest Binaries"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries*

* TOC
{:toc}

We provide a set of useful prebuilt binaries users can download (in case they don't want to
recompile them from scratch).

There are two ways of downloading them:

* Via Manual Download
* Via Google Cloud Utilities

## Manual Download

Here follows a list of prebuilt binaries to be downloaded by just clicking the link:

### Arm FS Binaries

##### Latest Linux Kernel Image / Bootloader (**recommended**)

The tarball below contains a set of binaries: the Linux kernel and a set of bootloaders

* <http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2>

##### Latest Linux Disk Images (**recommended**)

* <http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2>

  Partition table: yes

  gem5 init:
  * default (using m5 ops): `/init.gem5`
  * kvm (using m5 --addr ops): `/init.addr.gem5`
  * fast models (using m5 --semi ops): `/init.semi.gem5`

* <http://dist.gem5.org/dist/v22-0/arm/disks/aarch32-ubuntu-natty-headless.img.bz2>

##### Old Linux Kernel/Disk Image

These images are not supported. If you run into problems, we will do our best to help, but there is no guarantee these will work with the latest gem5 version

###### Disk images only

* <http://dist.gem5.org/dist/current/arm/disks/aarch64-ubuntu-trusty-headless.img.bz2>
* <http://dist.gem5.org/dist/current/arm/disks/linaro-minimal-aarch64.img.bz2>
* <http://dist.gem5.org/dist/current/arm/disks/linux-aarch32-ael.img.bz2>

###### Disk and kernel images

* <http://dist.gem5.org/dist/current/arm/aarch-system-20170616.tar.xz>
* <http://dist.gem5.org/dist/current/arm/aarch-system-20180409.tar.xz>
* <http://dist.gem5.org/dist/current/arm/arm-system-dacapo-2011-08.tgz>
* <http://dist.gem5.org/dist/current/arm/arm-system.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/arm64-system-02-2014.tgz>
* <http://dist.gem5.org/dist/current/arm/kitkat-overlay.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/linux-arm-arch.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/vmlinux-emm-pcie-3.3.tar.bz2>
* <http://dist.gem5.org/dist/current/arm/vmlinux.arm.smp.fb.3.2.tar.gz>

## Google Cloud Utilities (gsutil)

gsutil is a Python application that lets you access Cloud Storage from the command line.
Please have a look at the following documentation which will guide you through the process
of installing the utility

* [gsutil tool](https://cloud.google.com/storage/docs/gsutil)

Once installed (NOTE: It require you to provide a valid google account) it will be possible to inspect/download gem5 binaries via the following command line.

```
gsutil cp -r gs://dist.gem5.org/dist/<binary>
```


---


## "m5 term"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/m5term*

# m5 term
The m5term program allows the user to connect to the simulated console interface that full-system gem5 provides. Simply change into the util/term directory and build m5term:
```
% cd gem5/util/term
% make
gcc  -o m5term term.c
% make install
sudo install -o root -m 555 m5term /usr/local/bin
```
The usage of m5term is:
```
./m5term <host> <port>
```
	<host> is the host that is running gem5

	<port> is the console port to connect to. gem5 defaults to
	using port 3456, but if the port is used, it will try the next
	higher port until it finds one available.

	If there are multiple systems running within one simulation,
	there will be a console for each one.  (The first system's
	console will be on 3456 and the second on 3457 for example)

	m5term uses '~' as an escape character.  If you enter
	the escape character followed by a '.', the m5term program
	will exit.

m5term can be used to interactively work with the simulator, though users must often set various terminal settings to get things to work

A slightly shortened example of m5term in action:

	% m5term localhost 3456
	==== m5 slave console: Console 0 ====
	M5 console
	Got Configuration 127
	memsize 8000000 pages 4000
	First free page after ROM 0xFFFFFC0000018000
	HWRPB 0xFFFFFC0000018000 l1pt 0xFFFFFC0000040000 l2pt 0xFFFFFC0000042000 l3pt_rpb 0xFFFFFC0000044000 l3pt_kernel 0xFFFFFC0000048000 l2reserv 0xFFFFFC0000046000
	CPU Clock at 2000 MHz IntrClockFrequency=1024
	Booting with 1 processor(s)
	...
	...
	VFS: Mounted root (ext2 filesystem) readonly.
	Freeing unused kernel memory: 480k freed
	init started:  BusyBox v1.00-rc2 (2004.11.18-16:22+0000) multi-call binary

	PTXdist-0.7.0 (2004-11-18T11:23:40-0500)

	mounting filesystems...
	EXT2-fs warning: checktime reached, running e2fsck is recommended
	loading script...
	Script from M5 readfile is empty, starting bash shell...
	# ls
	benchmarks  etc         lib         mnt         sbin        usr
	bin         floppy      lost+found  modules     sys         var
	dev         home        man         proc        tmp         z
	#


---


## "Supported Kernels and Disk Images for gem5 stable"

*Source: https://www.gem5.org/documentation/general_docs/fullsystem/supported_disks_and_kernels*

# Supported Kernels and Disk Images for gem5 v25.0

This document outlines the kernel and disk image combinations used in gem5 v25.0, the level of support for each configuration, and additional components included in the kernels.

## Supported Architectures

* X86
* ARM
* RISC-V

## Kernel and Disk Image Pairings

The following kernel versions are used with each base disk image:

* **Ubuntu 22.04 disk images** use **kernel 5.15**
* **Ubuntu 24.04 disk images** (including `npb` and `gapbs` variants) use **kernel 6.8.12**

This pairing is consistent across all three ISAs: X86, ARM, and RISC-V.

Each disk image includes the kernel modules corresponding to its kernel version (e.g., the 24.04 images contain modules for kernel 6.8.12).

## How Kernels Were Chosen

The kernel versions used in gem5 v25.0 match the default versions shipped with Ubuntu 22.04 (5.15) and 24.04 (6.8.12). These were chosen to maintain compatibility with a wide variety of tools while minimizing custom maintenance overhead. Aligning with Ubuntu’s LTS distributions ensures we use stable, well-tested kernels without requiring custom patches.

## Included Kernel Module

All images include the `gem5-bridge` kernel module, which enables use of m5 annotations (e.g., `m5_exit`, `m5_reset_stats`) without requiring root access in the simulated system. This module is pre-installed within the disk image and matches the included kernel.

## Disk Images Overview

| Disk Image Name      | Ubuntu Version | Benchmarks Included |
| -------------------- | -------------- | ------------------- |
| `ubuntu-22.04`       | 22.04          | No                  |
| `ubuntu-24.04`       | 24.04          | No                  |
| `ubuntu-24.04-npb`   | 24.04          | Yes (NPB)           |
| `ubuntu-24.04-gapbs` | 24.04          | Yes (GAPBS)         |

These disk images are available for X86, ARM, and RISC-V.

## Support Status

* Only the combinations listed above (Ubuntu 22.04 with 5.15 and Ubuntu 24.04 with 6.8.12) are **regularly tested** and supported in gem5 v25.0.
* Other kernel versions or pairings **may not work** and are not guaranteed to be compatible with gem5 v25.0.


---


## Full System AMD GPU model

*Source: https://www.gem5.org/documentation/general_docs/gpu_models/gpufs*

# **Full System AMD GPU model**

The Full System AMD GPU model simulates a GPU at the "gfx9" ISA level, as opposed to the intermediate language level. This page will give you a general overview of how to use this model, the software stack the model uses, and provide resources that detail the model and how it is implemented. **It is recommended to use Full System instead of System Emulation as Full System supports the latest versions of the GPU software stack.**

## Requirements

The Full System GPU model is primarily designed to simulate discrete GPUs using a native software stack without modification. This means that the CPU portion of simulation is not configured for detailed simulation -- only the GPU is detailed. The [ROCm software stack](https://rocm.docs.amd.com/en/latest/) limits usage to officially supported gfx9 devices listed in the [ROCm documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). Currently gem5 provides configurations for Vega10 (gfx900), MI210/MI250X (gfx90a), and MI300X (gfx942).

*Note:* Previously supported "gfx9" devices in older versions of ROCm still work in most cases (gfx900, gfx906). As mentioned in the ROCm documentation, these may result in runtime errors for prebuilt ROCm libraries.

The CPU portion of code is ideally fast-forwarded using the KVM CPU model. Since the software stack is x86 you will need an x86 Linux host with KVM enabled to run Full System efficiently. The atomic CPU can also be used to run on non-x86 hosts or where KVM is not usable. See the [Running without KVM](#Running-without-kvm) section for details.

## **Using the model**

Several places in this guide assume that gem5 and gem5-resources are located in the same base directory.

The [gem5 repository](https://github.com/gem5/gem5) contains the base code of the GPU model.
The [gem5-resources repository](https://github.com/gem5/gem5-resources/) contains files needed to create a disk image for Full System and comes with a number of sample applications that can be used to get started with the model. We recommend users start with [square](https://resources.gem5.org/resources/square), as it is a simple, heavily tested application that should run relatively quickly.

#### Building gem5

The GPU model requires the GPU_VIPER cache coherence protocol which is implemented in Ruby and the Full System software stack is only supported in a simulated X86 environment. The VEGA_X86 build option uses the GPU_VIPER protocol and x86. Therefore, gem5 must be built using the VEGA_X86 build option:

```
scons build/VEGA_X86/gem5.opt
```

The Full System GPU model is built similarly to a CPU only version of gem5. Refer to the [building gem5](https://www.gem5.org/documentation/general_docs/building) documentation for how to build gem5, including number of build threads, linker options, and gem5 binary targets.

#### Building Disk Image and Kernel

Just like a CPU only version of gem5, the Full System GPU model requires a disk image and kernel to run. The [gem5-resources repository](https://github.com/gem5/gem5-resources/) provides a one-step disk image builder to create a disk image for the GPU model with all of the software requirements installed.

From your base directory with gem5 and gem5-resources cloned, navigate to [gem5-resources/src/x86-ubuntu-gpu-ml](https://github.com/gem5/gem5-resources/tree/stable/src/x86-ubuntu-gpu-ml). This directory contains a file `./build.sh` to create the disk image in one step. Building the disk depends on the [packer](https://www.packer.io/) tool which uses [QEMU](https://www.qemu.org/) as a backend. See the [BUILDING.md](https://github.com/gem5/gem5-resources/blob/stable/src/x86-ubuntu-gpu-ml/BUILDING.md) guide for troubleshooting. Generally, the disk image can be created in one step using the following command:

```
./build.sh
```

This process takes approximately 15-20 minutes and is mostly bound by download speed as a majority of the time is spent downloading Ubuntu packages.

Building the disk image will also extract the Linux kernel. The extracted Linux kernel *must* be used with the disk image. In other words, you cannot input an arbitrary kernel to gem5 otherwise the GPU driver may not load successfully.

After this process your environment should contain:
* Disk image: `gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml`
* Kernel: `gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml`

#### Building GPU applications

The GPU model is designed to run unmodified GPU binaries. If you have an application which runs on AMD GPU hardware and that hardware is supported in gem5, you can run the same binary in gem5. Note that as this is simulation, the application will need to be scaled down to a reasonable size to simulate in a realistic amount of time.

Building applications for the GPU model is similar to [cross compiling](https://www.gem5.org/documentation/general_docs/compiling_workloads/) when the simulated ISA does not match the host. Either you must have the development tools installed locally or containerization like Docker can be used. Docker images to build GPU applications are provided with gem5 in [util/dockerfiles/gpu-fs](https://github.com/gem5/gem5/tree/stable/util/dockerfiles/gpu-fs). You may either build this image or use the gem5 provided image at `ghcr.io/gem5/gpu-fs`. This docker image provides a specific version of ROCm. The ROCm version in the Dockerfile must match the ROCm version on the disk image being used to simulate gem5. The docker and disk image versions are synced upon gem5 releases. The instructions below show an example using the pre-built gem5 docker on GitHub container registry (ghcr.io).

[Square](https://github.com/gem5/gem5-resources/tree/stable/src/gpu/square) is a simple application provided in gem5-resources which can be used to get started with the model. Generally, the `src/gpu` directory of gem5-resources contains a `Makefile.default` which is used to build a native application and `Makefile.gpufs` which contains application annotated with [m5ops](https://www.gem5.org/documentation/general_docs/m5ops/) that will only run within gem5.

To build square using the gem5 provided docker image, navigate to the square directory and use the `Makefile.default` Makefile:

```
cd gem5-resources/src/gpu/square
docker run --rm -u $UID:$GID -v $PWD:$PWD -w $PWD ghcr.io/gem5/gpu-fs make -f Makefile.default
```

The square binary should then be located at `gem5-resources/src/gpu/square/bin.default/square.default`

#### Testing GPU application

The GPU model provides multiple gfx9 configurations to simulate GPU applications. The configurations specify the ISA (e.g., gfx942, gfx90a) and generally a minimally sized device. *They are not intended to be indicative of real hardware measurements*. In the gem5 repository, these are:
* MI300X: `configs/example/gpufs/mi300.py`
* MI210 / MI250: `configs/example/gpufs/mi200.py`

The GPU model uses config script based configuration (i.e., not [standard library](https://www.gem5.org/documentation/gem5-stdlib/overview)) which uses command line arguments as the primary way to modify simulation parameters. However, most common configuration options are set by the top-level scripts (e.g., `configs/example/gpufs/mi300.py`). The main required arguments are disk image, kernel, and application.

Using the disk image and kernel created above and the square binary built above, square can be run with the following command:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default
```

In Full System the output of the simulator and the output of the simulated system are shown in two separate locations. By default, the gem5 output prints to the terminal where gem5 is run. The simulated terminal output is located in the gem5 output directory which is `m5out` by default.

Once gem5 completes (or while running) the output of the Full System simulation can be seen in `m5out/system.pc.com_1.device`. For the square example, the application will print "PASSED!" to the simulated terminal output upon successful completion.

#### Using Python or shell scripts

Python scripts such as PyTorch, TensorFlow, etc. and shell scripts can be passed directly as the value of the `--app` command line. For example, the following minimal PyTorch application can be run directly when saved as `pytorch_test.py`:

```
#!/usr/bin/env python3

import torch

x = torch.rand(5, 3).to('cuda')
y = torch.rand(3, 5).to('cuda')

z = x @ y
```

For example:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app ./pytorch_test.py
```

#### Input files

The GPU model configuration files are designed to copy the file provided to the `--app` option into the simulator. **Full System gem5 cannot read files from your host system!** If your application requires input files, they must be copied into the disk image. See instructions for [extending the disk image](https://github.com/gem5/gem5-resources/blob/stable/src/x86-ubuntu-gpu-ml/BUILDING.md) for ways to do this.

If your application requires input files, it is recommended to create a shell script and pass the shell script to the `--app` option. The shell script should be written with paths relative to the disk image paths as it will run within gem5. For example, if your application requires `foo.dat`, create a shell script such as:

```
#!/bin/bash

# We have previously copied foo.dat to /data outside of simulation.
cd /data
my_gpu_app -i foo.dat
```

## Advanced Usage

#### Running without KVM

The AtomicSimpleCPU can also be used in situations where the host is not x86 or KVM is not available. To enable the Atomic CPU, you will need to modify your config (e.g., `configs/example/gpufs/mi300.py`) and replace `args.cpu_type = "X86KvmCPU"` with `args.cpu_type = "AtomicSimpleCPU"`.

Note that this will slow down the CPU portion of your simulation potentially by 100x. It is possible to speed this up using [checkpoints](https://www.gem5.org/documentation/general_docs/checkpoints/).

#### Checkpoints

The config scripts provided allow for checkpointing after Linux boots out of the box. It is recommended to use this when using the atomic CPU. To create a checkpoint after boot, simply add a `--checkpoint-dir` to the command line with a directory to place the checkpoint. For example:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default --checkpoint-dir square-cpt
```

The checkpoint can then be restored and re-simulating the application will take significantly less time. To restore a checkpoint, replace the `--checkpoint-dir` option with `--restore-dir`:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default --restore-dir square-cpt
```

Checkpoints can also be taken using the `m5_checkpoint(..)` [pseudo instruction]() or by checkpointing in the python configs after an exit event. For example, kernel exit events can be enabled using `--exit-at-gpu-task=-1` and the config can be modified to create a checkpoint at the *Nth* kernel by checking the current task number in `configs/example/gpufs/runfs.py`.

Note that checkpoints are currently not supported within a GPU kernel. Thus, checkpoints must be taken when no GPU kernels are running.

#### Build GPU custom applications

If you want to build an application that is not part of gem5-resources, you will want to build the GPU application targeting either `gfx90a` (MI210 and MI250), `gfx942` (MI300X), or both. For example:

```
hipcc my_gpu_app.cpp -o my_gpu_app --offload-arch=gfx90a,gfx942
```

You can build without a docker image on an x86 Linux host by installing the rocm-dev package after setting up a package manager following the steps in the [ROCm Linux documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/).

#### Modifying GPU configuration

The configurations in `configs/example/gpufs/` are helper configurations that interface with `configs/example/gpufs/runfs.py` and set meaningful default values for a specific device. Some parameters of interest in this file are the number of compute units, the GPU topology, the system memory size, and the CPU type.

Some of these parameters *only* modify the value in gem5 and do not change the simulated device. In particular the dgpu_mem_size parameter does not change the amount of memory seen by the device driver and is hardcoded to 16GB in C++. Changing this value will result in a gem5 fatal.

The supported cpu_types are X86KvmCPU and AtomicSimpleCPU as timing CPUs do not support the disjointed Ruby network required to simulate a discrete GPU.

Other parameters related to GPU can be found in `configs/example/gpufs/system/amdgpu.py` which creates the compute units for the GPU. See the ComputeUnit class in `src/gpu-compute/GPU.py` for all available options. Note that not all possible combinations of options can be tested. Options such as queue sizes and latencies are generally safe to modify.


---


## AMD VEGA GPU model

*Source: https://www.gem5.org/documentation/general_docs/gpu_models/vega*

# **System Emulation AMD VEGA GPU model**

Table of Contents

1. [Using the model](#Using-the-model)
2. [ROCm](#ROCm)
3. [Documentation and Tutorials](#Documentation-and-Tutorials)

The AMD VEGA GPU is a model that simulates a GPU at the VEGA ISA level, as opposed to the intermediate language level. This page will give you a general overview of how to use this model, the software stack the model uses, and provide resources that detail the model and how it is implemented.

## **Using the model**

Currently, the AMD VEGA GPU model in gem5 is supported on the stable and develop branch.

The [gem5 repository](https://github.com/gem5/gem5) comes with a dockerfile located in `util/dockerfiles/gcn-gpu/`. This dockerfile contains the drivers and libraries needed to run the GPU model. A pre-built version of the docker image is hosted at `ghcr.io/gem5-test/gcn-gpu:v23-1`.
The [gem5-resources repository](https://github.com/gem5/gem5-resources/) also comes with a number of sample applications that can be used to verify that the model runs correctly.  We recommend users start with [square](https://resources.gem5.org/resources/square), as it is a simple, heavily tested application that should run relatively quickly.

#### Using the image
The docker image can either be built or pulled from ghcr.io.

To build the docker image from source:
```
# Working directory: gem5/util/dockerfiles/gcn-gpu
docker build -t <image_name> .
```

To pull the pre-built docker image (Note the `v23-1` tag, to get the correct
image for this release):

```
docker pull ghcr.io/gem5-test/gcn-gpu:v23-1
```

You can also put `ghcr.io/gem5-test/gcn-gpu:v23-1` as the image in the docker run command without pulling beforehand and it will be pulled automatically.
#### Building gem5 using the image
See square in [gem5 resources](https://github.com/gem5/gem5-resources/tree/stable/src/gpu/square/) for an example of how to build gem5 in the docker.  Note: these directions assume you are pulling the latest image automatically.

#### Building & running a GPU application using the image
See [gem5 resources](https://github.com/gem5/gem5-resources/tree/stable/src/gpu/) for examples of how to build and run GPU applications in the docker.

## **ROCm**

The AMD VEGA GPU model was designed with enough fidelity to not require an emulated runtime. Instead, the model uses the Radeon Open Compute platform (ROCm). ROCm is an open platform from AMD that implements [Heterogeneous Systems Architecture (HSA)](http://www.hsafoundation.com/) principles. More information about the HSA standard can be found on the HSA Foundation's website. More information about ROCm can be found on the [ROCm website](https://rocmdocs.amd.com/en/latest/)

#### Simulation support for ROCm
The model currently works with system-call emulation (SE) mode and full-system (FS) mode.

In SE mode, all kernel level driver functionality is modeled entirely within the SE mode layer of gem5. In particular, the emulated GPU driver supports the necessary `ioctl()` commands it receives from the userspace code. The source for the emulated GPU driver can be found in:

* The GPU compute driver: `src/gpu-compute/gpu_compute_driver.[hh|cc]`

* The HSA device driver: `src/dev/hsa/hsa_driver.[hh|cc]`

The HSA driver code models the basic functionality for an HSA agent, which is any device that can be targeted by the HSA runtime and accepts Architected Query Language (AQL) packets. AQL packets are a standard format for all HSA agents, and are used primarily to initiate kernel launches on the GPU. The base `HSADriver` class holds a pointer to the HSA packet processor for the device, and defines the interface for any HSA device. An HSA agent does not have to be a GPU, it could be a generic accelerator, CPU, NIC, etc.

The `GPUComputeDriver` derives from `HSADriver` and is a device-specific implementation of an `HSADriver`. It provides the implementation for GPU-specific `ioctl()` calls.

The `src/dev/hsa/kfd_ioctl.h` header must match the `kfd_ioctl.h` header that comes with ROCt. The emulated driver relies on that file to interpret the `ioctl()` codes the thunk uses.

In FS mode, the real amdgpu Linux driver is used and installed as you would on a real machine. The source for the driver can instead be found in the [ROCK-Kernel-Driver](https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver) repository.

#### ROCm toolchain and software stack
The AMD VEGA GPU model supports ROCm versions up to 5.4 in FS mode and 4.0 in SE mode.

The following ROCm components are required in SE mode:
* [Heterogeneous Compute Compiler (HCC)](https://github.com/RadeonOpenCompute/hcc)
* [Radeon Open Compute runtime (ROCr)](https://github.com/RadeonOpenCompute/ROCR-Runtime)
* [Radeon Open Compute thunk (ROCt)](https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface)
* [HIP](https://github.com/ROCm-Developer-Tools/HIP)

The following additional components are used to build and run machine learning programs:
* [hipBLAS](https://github.com/ROCmSoftwarePlatform/hipBLAS/)
* [rocBLAS](https://github.com/ROCmSoftwarePlatform/rocBLAS/)
* [MIOpen](https://github.com/ROCmSoftwarePlatform/MIOpen/)
* [rocm-cmake](https://github.com/RadeonOpenCompute/rocm-cmake/)
* [PyTorch](https://pytorch.org/) (FS mode only)
* [Tensorflow](https://www.tensorflow.org/) - specifically the tensorflow-rocm python package (FS mode only)

For information about installing these components locally, the commands in the GCN3 dockerfile (`util/dockerfiles/gcn-gpu/`) can be followed on an Ubuntu 16 machine.

## **Documentation and Tutorials**

Note that the VEGA ISA is a newer, superset ISA derived from GCN3. Therefore, the contents of the following papers, tutorials, and documentation apply to VEGA as well.

#### GPU Model
Describes the gem5 GPU model with the GCN3 ISA (at the time of writing). VEGA is a newer, superset ISA derived from GCN3. Therefore the contents of the following papers)
* [HPCA 2018](https://ieeexplore.ieee.org/document/8327041)

#### gem5 GCN3 ISCA tutorial
Covers information about the GPU architecture, GCN3 ISA and HW-SW interfaces in gem5. Also provides an introduction to ROCm.
* [gem5 GCN3 ISCA webpage](http://www.gem5.org/events/isca-2018)
* [gem5 GCN3 ISCA slides](http://old.gem5.org/wiki/images/1/19/AMD_gem5_APU_simulator_isca_2018_gem5_wiki.pdf)

#### VEGA ISA
* [VEGA ISA](https://gpuopen.com/documentation/amd-isa-documentation/)

#### ROCm Documentation
Contains further documentation about the ROCm stack, as well as programming guides for using ROCm.
* [ROCm webpage](https://rocmdocs.amd.com/en/latest/)

#### AMDGPU LLVM Information
* [LLVM AMDGPU](https://llvm.org/docs/AMDGPUUsage.html)


---


## "Memory system"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/*

# Memory system

M5's new memory system (introduced in the first 2.0 beta release) was
designed with the following goals:

1.  Unify timing and functional accesses in timing mode. With the old
    memory system the timing accesses did not have data and just
    accounted for the time it would take to do an operation. Then a
    separate functional access actually made the operation visible to
    the system. This method was confusing, it allowed simulated
    components to accidentally cheat, and prevented the memory system
    from returning timing-dependent values, which isn't reasonable for
    an execute-in-execute CPU model.
2.  Simplify the memory system code -- remove the huge amount of
    templating and duplicate code.
3.  Make changes easier, specifically to allow other memory
    interconnects besides a shared bus.

For details on the new coherence protocol, introduced (along with a
substantial cache model rewrite) in 2.0b4, see [Coherence
Protocol](classic-coherence-protocol "wikilink").

### MemObjects

All objects that connect to the memory system inherit from `MemObject`.
This class adds the pure virtual functions `getMasterPort(const
std::string &name, PortID idx)` and `getSlavePort(const std::string
&name, PortID idx)` which returns a port corresponding to the given name
and index. This interface is used to structurally connect the MemObjects
together.

### Ports

The next large part of the memory system is the idea of ports. Ports are
used to interface memory objects to each other. They will always come in
pairs, with a MasterPort and a SlavePort, and we refer to the other port
object as the peer. These are used to make the design more modular. With
ports a specific interface between every type of object doesn't have to
be created. Every memory object has to have at least one port to be
useful. A master module, such as a CPU, has one or more MasterPort
instances. A slave module, such as a memory controller, has one or more
SlavePorts. An interconnect component, such as a cache, bridge or bus,
has both MasterPort and SlavePort instances.

There are two groups of functions in the port object. The `send*`
functions are called on the port by the object that owns that port. For
example to send a packet in the memory system a CPU would call
`myPort->sendTimingReq(pkt)`. Each send function has a
corresponding recv function that is called on the ports peer. So the
implementation of the `sendTimingReq()` call above would simply be
`peer->recvTimingReq(pkt)` on the slave port. Using this method we only
have one virtual function call penalty but keep generic ports that can
connect together any memory system objects.

Master ports can send requests and receive responses, whereas slave
ports receive requests and send responses. Due to the coherence
protocol, a slave port can also send snoop requests and receive snoop
responses, with the master port having the mirrored interface.

### Connections

In Python, Ports are first-class attributes of simulation objects, much
like Params. Two objects can specify that their ports should be
connected using the assignment operator. Unlike a normal variable or
parameter assignment, port connections are symmetric: `A.port1 =
B.port2` has the same meaning as `B.port2 = A.port1`. The notion of
master and slave ports exists in the Python objects as well, and a check
is done when the ports are connected together.

Objects such as busses that have a potentially unlimited number of ports
use "vector ports". An assignment to a vector port appends the peer to a
list of connections rather than overwriting a previous connection.

In C++, memory ports are connected together by the python code after all
objects are instantiated.

### Request

A request object encapsulates the original request issued by a CPU or
I/O device. The parameters of this request are persistent throughout the
transaction, so a request object's fields are intended to be written at
most once for a given request. There are a handful of constructors and
update methods that allow subsets of the object's fields to be written
at different times (or not at all). Read access to all request fields is
provided via accessor methods which verify that the data in the field
being read is valid.

The fields in the request object are typically not available to devices
in a real system, so they should normally be used only for statistics or
debugging and not as architectural values.

Request object fields include:

- Virtual address. This field may be invalid if the request was issued
  directly on a physical address (e.g., by a DMA I/O device).
- Physical address.
- Data size.
- Time the request was created.
- The ID of the CPU/thread that caused this request. May be invalid if
  the request was not issued by a CPU (e.g., a device access or a
  cache writeback).
- The PC that caused this request. Also may be invalid if the request
  was not issued by a CPU.

### Packet

A Packet is used to encapsulate a transfer between two objects in the
memory system (e.g., the L1 and L2 cache). This is in contrast to a
Request where a single Request travels all the way from the requester to
the ultimate destination and back, possibly being conveyed by several
different Packets along the way.

Read access to many packet fields is provided via accessor methods which
verify that the data in the field being read is valid.

A packet contains the following all of which are accessed by accessors
to be certain the data is valid:

- The address. This is the address that will be used to route the
  packet to its target (if the destination is not explicitly set) and
  to process the packet at the target. It is typically derived from
  the request object's physical address, but may be derived from the
  virtual address in some situations (e.g., for accessing a fully
  virtual cache before address translation has been performed). It may
  not be identical to the original request address: for example, on a
  cache miss, the packet address may be the address of the block to
  fetch and not the request address.
- The size. Again, this size may not be the same as that of the
  original request, as in the cache miss scenario.
- A pointer to the data being manipulated.
    - Set by `dataStatic()`, `dataDynamic()`, and `dataDynamicArray()`
      which control if the data associated with the packet is freed
      when the packet is, not, with `delete`, and with `delete []`
      respectively.
    - Allocated if not set by one of the above methods `allocate()`
      and the data is freed when the packet is destroyed. (Always safe
      to call).
    - A pointer can be retrived by calling `getPtr()`
    - `get()` and `set()` can be used to manipulate the data in the
      packet. The get() method does a guest-to-host endian conversion
      and the set method does a host-to-guest endian conversion.
- A status indicating Success, BadAddress, Not Acknowleged, and
  Unknown.
- A list of command attributes associated with the packet
    - Note: There is some overlap in the data in the status field and
      the command attributes. This is largely so that a packet can be
      easily reinitialized when nacked or easily reused with atomic or
      functional accesses.
- A `SenderState` pointer which is a virtual base opaque structure
  used to hold state associated with the packet but specific to the
  sending device (e.g., an MSHR). A pointer to this state is returned
  in the packet's response so that the sender can quickly look up the
  state needed to process it. A specific subclass would be derived
  from this to carry state specific to a particular sending device.
- A `CoherenceState` pointer which is a virtual base opaque structure
  used to hold coherence-related state. A specific subclass would be
  derived from this to carry state specific to a particular coherence
  protocol.
- A pointer to the request.

### Access Types

There are three types of accesses supported by the ports.

1.  **Timing** - Timing accesses are the most detailed access. They
    reflect our best effort for realistic timing and include the
    modeling of queuing delay and resource contention. Once a timing
    request is successfully sent at some point in the future the device
    that sent the request will either get the response or a NACK if the
    request could not be completed (more below). Timing and Atomic
    accesses can not coexist in the memory system.
2.  **Atomic** - Atomic accesses are a faster than detailed access. They
    are used for fast forwarding and warming up caches and return an
    approximate time to complete the request without any resource
    contention or queuing delay. When a atomic access is sent the
    response is provided when the function returns. Atomic and timing
    accesses can not coexist in the memory system.
3.  **Functional** - Like atomic accesses functional accesses happen
    instantaneously, but unlike atomic accesses they can coexist in the
    memory system with atomic or timing accesses. Functional accesses
    are used for things such as loading binaries, examining/changing
    variables in the simulated system, and allowing a remote debugger to
    be attached to the simulator. The important note is when a
    functional access is received by a device, if it contains a queue of
    packets all the packets must be searched for requests or responses
    that the functional access is effecting and they must be updated as
    appropriate. The `Packet::intersect()` and `fixPacket()` methods can
    help with this.

### Packet allocation protocol

The protocol for allocation and deallocation of Packet objects varies
depending on the access type. (We're talking about low-level C++
`new`/`delete` issues here, not anything related to the coherence
protocol.)

- *Atomic* and *Functional* : The Packet object is owned by the
  requester. The responder must overwrite the request packet with the
  response (typically using the `Packet::makeResponse()` method).
  There is no provision for having multiple responders to a single
  request. Since the response is always generated before
  `sendAtomic()` or `sendFunctional()` returns, the requester can
  allocate the Packet object statically or on the stack.
- *Timing* : Timing transactions are composed of two one-way messages,
  a request and a response. In both cases, the Packet object must be
  dynamically allocated by the sender. Deallocation is the
  responsibility of the receiver (or, for broadcast coherence packets,
  the target device, typically memory). In the case where the receiver
  of a request is generating a response, it *may* choose to reuse the
  request packet for its response to save the overhead of calling
  `delete` and then `new` (and gain the convenience of using
  `makeResponse()`). However, this optimization is optional, and the
  requester must not rely on receiving the same Packet object back in
  response to a request. Note that when the responder is not the
  target device (as in a cache-to-cache transfer), then the target
  device will still delete the request packet, and thus the responding
  cache must allocate a new Packet object for its response. Also,
  because the target device may delete the request packet immediately
  on delivery, any other memory device wishing to reference a
  broadcast packet past the point where the packet is delivered must make
  a copy of that packet, as the pointer to the packet that is
  delivered cannot be relied upon to stay valid.

### Timing Flow control

Timing requests simulate a real memory system, so unlike functional and
atomic accesses their response is not instantaneous. Because the timing
requests are not instantaneous, flow control is needed. When a timing
packet is sent via `sendTiming()` the packet may or may not be accepted,
which is signaled by returning true or false. If false is returned the
object should not attempt to sent anymore packets until it receives a
`recvRetry()` call. At this time it should again try to call
`sendTiming()`; however the packet may again be rejected. Note: The
original packet does not need to be resent, a higher priority packet can
be sent instead. Once `sendTiming()` returns true, the packet may still
not be able to make it to its destination. For packets that require a
response (i.e. `pkt->needsResponse()` is true), any memory object can
refuse to acknowledge the packet by changing its result to `Nacked` and
sending it back to its source. However, if it is a response packet, this
can not be done. The true/false return is intended to be used for local
flow control, while nacking is for global flow control. In both cases a
response can not be nacked.

### Response and Snoop ranges

Ranges in the memory system are handled by having devices that are
sensitive to an address range provide an implementation for
`getAddrRanges` in their slave port objects. This method returns an
`AddrRangeList` of addresses it responds to. When these ranges change
(e.g. from PCI configuration taking place) the device should call
`sendRangeChange()` on its slave port so that the new ranges are
propagated to the entire hierarchy. This is precisely what happens
during `init()`; all memory objects call `sendRangeChange()`, and a
flurry of range updates occur until everyones ranges have been
propagated to all busses in the system.


---


## "Classic memory system coherence"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/classic-coherence-protocol/*

# Classic Memory System coherence

M5 2.0b4 introduced a substantially rewritten and streamlined cache
model, including a new coherence protocol. (The old pre-2.0 cache model
had been patched up to work with the new [Memory
System](/documentation/general_docs/memory_system/) introduced in 2.0beta, but not
rewritten to take advantage of the new memory system's features.)

The key feature of the new coherence protocol is that it is designed to
work with more-or-less arbitrary cache hierarchies (multiple caches each
on multiple levels). In contrast, the old protocol restricted sharing to
a single bus.

In the real world, a system architecture will have limits on the number
or configuration of caches that the protocol can be designed to
accommodate. It's not practical to design a protocol that's fully
realistic and yet efficient for arbitrary configurations. In order to
enable our protocol to work on (nearly) arbitrary configurations, we
currently sacrifice a little bit of realism and a little bit of
configurability. Our intent is that this protocol is adequate for
researchers studying aspects of system behavior other than coherence
mechanisms. Researchers studying coherence specifically will probably
want to replace the default coherence mechanism with implementations of
the specific protocols under investigation.

The protocol is a MOESI snooping protocol. Inclusion is **not**
enforced; in a CMP configuration where you have several L1s whose total
capacity is a significant fraction of the capacity of the common L2 they
share, inclusion can be very inefficient.

Requests from upper-level caches (those closer to the CPUs) propagate
toward memory in the expected fashion: an L1 miss is broadcast on the
local L1/L2 bus, where it is snooped by the other L1s on that bus and
(if none respond) serviced by the L2. If the request misses in the L2,
then after some delay (currently set equal to the L2 hit latency), the
L2 will issue the request on its memory-side bus, where it will possibly
be snooped by other L2s and then be issued to an L3 or memory.

Unfortunately, propagating snoop requests incrementally back up the
hierarchy in a similar fashion is a source of myriad nearly intractable
race conditions. Real systems don't typically do this anyway; in general
you want a single snoop operation at the L2 bus to tell you the state of
the block in the whole L1/L2 hierarchy. There are a handful of methods
for this:

1.  just snoop the L2, but enforce inclusion so that the L2 has all the
    info you need about the L1s as well---an idea we've already rejected
    above
2.  keep an extra set of tags for all the L1s at the L2 so those can be
    snooped at the same time (see the Compaq Piranha)---reasonable, if
    you're hierarchy's not too deep, but now you've got to size the tags
    in the lower-level caches based on the number, size, and
    configuration of the upper-level caches, which is a configuration
    pain
3.  snoop the L1s in parallel with the L2, something that's not hard if
    they're all on the same die (I believe Intel started doing this with
    the Pentium Pro; not sure if they still do with the Core2 chips or
    not, or if AMD does this as well, but I suspect so)---also
    reasonable, but adding explicit paths for these snoops would also
    make for a very cumbersome configuration process

We solve this dilemma by introducing "express snoops", which are special
snoop requests that get propagated up the hierarchy instantaneously and
atomically (much like the atomic-mode accesses described on the [Memory
System](/documentation/general_docs/memory_system) page), even when the system is running
in timing mode. Functionally this behaves very much like options 2 or 3
above, but because the snoops propagate along the regular bus
interconnects, there's no additional configuration overhead. There is
some timing inaccuracy introduced, but if we assume that there are
dedicated paths in the real hardware for these snoops (or for
maintaining the additional copies of the upper-level tags at the
lower-level caches) then the differences are probably minor.

(More to come: how does a cache know when its request is completed? and
other fascinating questions...)

Note: there are still some bugs in this protocol as of 2.0b4,
particularly if you have multiple L2s each with multiple L1s behind it,
but I believe it works for any configuration that worked in 2.0b3.


---


## "Classic caches"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/*

# Classic Caches

The default cache is a non-blocking cache with MSHR (miss status holding
register) and WB (Write Buffer) for read and write misses. The Cache can
also be enabled with prefetch (typically in the last level of cache).

There are multiple possible [replacement policies](/documentation/general_docs/memory_system/replacement_policies) and [indexing
policies](/documentation/general_docs/memory_system/indexing_policies) implemented in gem5. These define, respectively, the possible
blocks that can be used for a block replacement given an address, and
how to use the address information to find a block\'s location. By
default the cache lines are replaced using [LRU (least recently used)](/documentation/general_docs/memory_system/replacement_policies),
and indexed with the [Set Associative](/documentation/general_docs/memory_system/indexing_policies) policy.


# Interconnects

### Crossbars

The two types of traffic in the crossbar are memory-mapped packets and
snooping packets. The memory-mapped requests go down the memory
hierarchy, and responses go up the memory hierarchy (same route back).
The snooping requests go horizontally and up the cache hierarchy,
snooping responses go horizontally and down the hierarchy (same route
back). Normal snoops go horizontally and express snoops go up the cache
hierarchy.

![Bus Connections](/assets/img/Bus.png)

### Bridges

### Others...

# Debugging

There is a feature in the classic memory system for displaying the coherence state of a particular block from within the debugger (e.g., gdb). This feature is built on the classic memory system's support for functional accesses. (Note that this feature is currently rarely used and may have bugs.)

If you inject a functional request with the command set to PrintReq, the packet traverses the memory system (like a regular functional request) but on any object that matches (other queued packet, cache block, etc.) it simply prints out some information about that object.

There's a helper method on Port called printAddr() that takes an address and builds an appropriate PrintReq packet and injects it. Since it propagates using the same mechanism as a normal functional request, it needs to be injected from a port where it will propagate through the whole memory system, such as at a CPU. There are helper printAddr() methods on MemTest, AtomicSimpleCPU, and TimingSimpleCPU objects that simply call printAddr() on their respective cache ports. (Caveat: the latter two are untested.)

Putting it all together, you can do this:

```
(gdb) set print object
(gdb) call SimObject::find(" system.physmem.cache0.cache0.cpu")
$4 = (MemTest *) 0xf1ac60
(gdb) p (MemTest*)$4
$5 = (MemTest *) 0xf1ac60
(gdb) call $5->printAddr(0x107f40)

system.physmem.cache0.cache0
  MSHRs
    [107f40:107f7f] Fill   state:
      Targets:
        cpu: [107f40:107f40] ReadReq
system.physmem.cache1.cache1
  blk VEM
system.physmem
  0xd0
```

... which says that cache0.cache0 has an MSHR allocated for that address to serve a target ReadReq from the CPU, but it's not in service yet (else it would be marked as such); the block is valid, exclusive, and modified in cache1.cache1, and the byte has a value of 0xd0 in physical memory.

Obviously it's not necessarily all the info you'd want, but it's pretty useful. Feel free to extend. There's also a verbosity parameter that's currently not used that could be exploited to have different levels of output.

Note that the extra "p (MemTest*)$4" is needed since although "set print object" displays the derived type, internally gdb still considers the pointer to be of the base type, so if you try and call printAddr directly on the $4 pointer you get this:

```
(gdb) call $4->printAddr(0x400000)
Couldn't find method SimObject::printAddr
```


---


## "gem5_memory_syste"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/gem5_memory_system/*

# The gem5 Memory System

The document describes memory subsystem in gem5 with focus on program flow
during CPU’s simple memory transactions (read or write).

## Model Hierarchy

Model that is used in this document consists of two out-of-order (O3) ARM v7
CPUs with corresponding L1 data caches and Simple Memory. It is created by
running gem5 with the following parameters:

```
configs/example/fs.py –-caches –-cpu-type=arm_detailed –-num-cpus=2
```

Gem5 uses Simulation Objects derived objects as basic blocks for building
memory system. They are connected via ports with established master/slave
hierarchy. Data flow is initiated on master port while the response messages
and snoop queries appear on the slave port.


![Simulation Object hierarchy of the model](/assets/img/gem5_MS_Fig1.PNG)


## CPU

Data [Cache](http://doxygen.gem5.org/release/current/classgem5_1_1cache.html) object
implements a standard cache structure:

![DCache Simulation Objet](/assets/img/gem5_MS_Fig2.PNG)

It is not in the scope of this document to describe O3 CPU model in details, so
here are only a few relevant notes about the model:

**Read access** is initiated by sending message to the port towards DCache
object. If DCache rejects the message (for being blocked or busy) CPU will
flush the pipeline and the access will be re-attempted later on. The access is
completed upon receiving reply message (ReadRep) from DCache.

**Write access** is initiated by storing the request into store buffer whose
context is emptied and sent to DCache on every tick. DCache may also reject the
request. Write access is completed when write reply (WriteRep) message is
received from DCache.

Load & store buffers (for read and write access) don’t impose any restriction
on the number of active memory accesses. Therefore, the maximum number of
outstanding CPU’s memory access requests is not limited by CPU Simulation
Object but by underlying memory system model.

**Split memory access** is implemented.

The message that is sent by CPU contains memory type (Normal, Device, Strongly
Ordered and cachebility) of the accessed region. However, this is not being
used by the rest of the model that takes more simplified approach towards
memory types.

## Data Cache Object

Data [Cache](http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html) object
implements a standard cache structure:

**Cached memory reads** that match particular cache tag (with Valid & Read
flags) will be completed (by sending ReadResp to CPU) after a configurable
time. Otherwise, the request is forwarded to Miss Status and Handling Register
([MSHR](http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html)) block.

**Cached memory writes** that match particular cache tag (with Valid, Read &
Write flags) will be completed (by sending WriteResp CPU) after the same
configurable time. Otherwise, the request is forwarded to Miss Status and
Handling Register(MSHR) block.

**Uncached memory reads** are forwarded to [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) block.

**Uncached memory writes** are forwarded to WriteBuffer block.

**Evicted (& dirty) cache lines** are forwarded to WriteBuffer block.

CPU’s access to Data [Cache](
http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html) is blocked if any of the
following is true:

* [MSHR](http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) block is full.
(The size of MSHR’s buffer is configurable.)
* Writeback block is full. (The size of the block’s buffer is configurable.)
* The number of outstanding memory accesses against the same memory cache line
has reached configurable threshold value – see [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) and Write Buffer for
details.

Data [Cache](http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html) in block
state will reject any request from slave port (from CPU) regardless of whether
it would result in cache hit or miss. Note that incoming messages on master
port (response messages and snoop requests) are never rejected.

[Cache](http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html) hit on uncachable
memory region (unpredicted behaviour according to ARM ARM) will invalidate
cache line and fetch data from memory.

### Tags & Data Block

[Cache](http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html) lines (referred as
blocks in source code) are organised into sets with configurable associativity
and size. They have the following status flags:

* **Valid**. It holds data. Address tag is valid
* **Read**. No read request will be accepted without this flag being set. For
example, cache line is valid and unreadable when it waits for write flag to
complete write access.
* **Write**. It may accept writes. Cache line with Write flags identifies
Unique state – no other cache memory holds the copy.
* **Dirty**. It needs Writeback when evicted.

Read access will hit cache line if address tags match and Valid and Read flags
are set. Write access will hit cache line if address tags match and Valid, Read
and Write flags are set.

### MSHR and Write Buffer Queues

Miss Status and Handling Register ([MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html)) queue holds the list of
CPU’s outstanding memory requests that require read access to lower memory
level. They are:

* Cached Read misses.
* Cached Write misses.
* Uncached reads.

WriteBuffer queue holds the following memory requests:

* Uncached writes.
* Writeback from evicted (& dirty) cache lines.

![MSHR and Write Buffer Blocks](/assets/img/gem5_MS_Fig3.PNG)

Each memory request is assigned to corresponding [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) object (READ or WRITE on
diagram above) that represents particular block (cache line) of memory that has
to be read or written in order to complete the command(s). As shown on gigure
above, cached read/writes against the same cache line have a common [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) object and will be
completed with a single memory access.

The size of the block (and therefore the size of read/write access to lower
memory) is:

* The size of cache line for cached access & writeback;
* As specified in CPU instruction for uncached access.

In general, Data [Cache](http://doxygen.gem5.org/release/current/classgem5_1_1Cache.html)
model distinguishes between just two memory types:

* Normal Cached memory. It is always treated as write back, read and write
allocate.
* Normal uncached, Device and Strongly Ordered types are treated equally (as
uncached memory)

### Memory Access Ordering

An unique order number is assigned to each CPU read/write request(as they
appear on slave port). Order numbers of [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) objects are copied from the
first assigned read/write.

Memory read/writes from each of these two queues are executed in order
(according to the assigned order number). When both queues are not empty the
model will execute memory read from [MSHR](
http://doxygen.gem5.org/release/current/classgem5_1_1MSHR.html) block unless WriteBuffer is
full. It will, however, always preserve the order of read/writes on the same
(or overlapping) memory cache line (block).

In summary:

* Order of accesses to cached memory is not preserved unless they target the
same cache line. For example, the accesses #1, #5 & #10 will complete
simultaneously in the same tick (still in order). The access #5 will complete
before #3.
* Order of all uncached memory writes is preserved. Write#6 always completes
before Write#13.
* Order to all uncached memory reads is preserved. Read#2 always completes
before Read#8.
* The order of a read and a write uncached access is not necessarily preserved
unless their access regions overlap. Therefore, Write#6 always completes before
Read#8 (they target the same memory block). However, Write#13 may complete
before Read#8.

## Coherent Bus Object


![Coherent Bus Object](/assets/img/gem5_MS_Fig4.PNG)


Coherent Bus object provides basic support for snoop protocol:

All requests on the slave port are forwarded to the appropriate master port.
Requests for cached memory regions are also forwarded to other slave ports (as
snoop requests).

Master port replies are forwarded to the appropriate slave port.

Master port snoop requests are forwarded to all slave ports.

Slave port snoop replies are forwarded to the port that was the source of the
request. (Note that the source of snoop request can be either slave or master
port.)

The bus declares itself blocked for a configurable period of time after any of
the following events:

* A packet is sent (or failed to be sent) to a slave port.
* A reply message is sent to a master port.
* Snoop response from one slave port is sent to another slave port.

The bus in blocked state rejects the following incoming messages:

* Slave port requests.
* Master port replies.
* Master port snoop requests.

## Simple Memory Object

It never blocks the access on slave port.

Memory read/write takes immediate effect. (Read or write is performed when the
request is received).

Reply message is sent after a configurable period of time .

## Message Flow

### Memory Access Ordering

The following diagram shows read access that hits Data Cache line with Valid
and Read flags:

![Read Hit(Read flag must be set in cache line)](/assets/img/gem5_MS_Fig5.PNG)

Cache miss read access will generate the following sequence of messages:

![Read Miss with snoop reply](/assets/img/gem5_MS_Fig6.PNG)

Note that bus object never gets response from both DCache2 and Memory object.
It sends the very same ReadReq package (message) object to memory and data
cache. When Data Cache wants to reply on snoop request it marks the message
with MEM_INHIBIT flag that tells Memory object not to process the message.

### Memory Access Ordering

The following diagram shows write access that hits DCache1 cache line with
Valid & Write flags:

![Write Hit (with Write flag set in cache line)](/assets/img/gem5_MS_Fig7.PNG)

Next figure shows write access that hits DCache1 cache line with Valid but no
Write flags – which qualifies as write miss. DCache1 issues UpgradeReq to
obtain write permission. DCache2::snoopTiming will invalidate cache line that
has been hit. Note that UpgradeResp message doesn’t carry data.

![Write Miss – matching tag with no Write flag](/assets/img/gem5_MS_Fig8.PNG)

The next diagram shows write miss in DCache. ReadExReq invalidates cache line
in DCache2. ReadExResp carries the content of memory cache line.

![Miss - no matching tag](/assets/img/gem5_MS_Fig9.PNG)


---


## "Indexing Policies"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/indexing_policies/*

# Indexing Policies

Indexing policies determine the locations to which a block is mapped
based on its address.

The most important methods of indexing policies are getPossibleEntries()
and regenerateAddr():

-   getPossibleEntries() determines the list of entries a given address
    can be mapped to.
-   regenerateAddr() uses the address information stored in an entry to
    determine its full original address.

For further information on Cache Indexing Policies, please refer to the
wikipedia articles on [Placement Policies](https://en.wikipedia.org/wiki/Cache_Placement_Policies) and
[Associativity](https://en.wikipedia.org/wiki/CPU_cache#Associativity%7C).

Set Associative {#set_associative}
---------------

The set associative indexing policy is the standard for table-like
structures, and can be further divided into Direct-Mapped (or 1-way
set-associative), Set-Associative and Full-Associative (N-way
set-associative, where N is the number of table entries).

A set associative cache can be seen as a skewed associative cache whose
skewing function maps to the same value for every way.

Skewed Associative {#skewed_associative}
------------------

The skewed associative indexing policy has a variable mapping based on a
hash function, so a value x can be mapped to different sets, based on
the way being used. Gem5 implements skewed caches as described in
["Skewed-Associative
Caches", from Seznec et al](https://www.researchgate.net/publication/220758754_Skewed-associative_Caches).

Note that there are only a limited number of implemented hashing
functions, so if the number of ways is higher than that number then a
sub-optimal automatically generated hash function is used.


---


## "Replacement Policies"

*Source: https://www.gem5.org/documentation/general_docs/memory_system/replacement_policies/*

# Replacement Policies

Gem5 has multiple implemented replacement policies. Each one uses its
specific replacement data to determine a replacement victim on
evictions.

All of the replacement policies prioritize victimizing invalid blocks.

A replacement policy consists of a reset(), touch(), invalidate() and
getVictim() methods. Each of which handles the replacement data
differently.

-   reset() is used to initialize a replacement data (i.e., validate).
    It should be called only on entry insertion, and must not be called
    again until invalidation. The first touch to an entry must always be
    a reset().
-   touch() is used on accesses to the replacement data, and as such
    should be called on entry accesses. It updates the replacement data.
-   invalidate() is called whenever an entry is invalidated, possibly
    due to coherence handling. It makes the entry as likely to be
    evicted as possible on the next victim search. An entry does not
    need to be invalidated before a reset() is done. When the simulation
    starts all entries are invalid.
-   getVictim() is called when there is a miss, and an eviction must be
    done. It searches among all replacement candidates for an entry with
    the worst replacement data, generally prioritizing the eviction of
    invalid entries.

We briefly describe the replacement policies implemented in Gem5. If
further information is required, the [Cache Replacement Policies
Wikipedia page](https://en.wikipedia.org/wiki/Cache_replacement_policies), or the respective papers can be studied.

Random
------

The simplest replacement policy; it does not need replacement data, as
it randomly selects a victim among the candidates.

Least Recently Used (LRU) {#least_recently_used_lru}
-------------------------

Its replacement data consists of a last touch timestamp, and the victim
is chosen based on it: the oldest it is, the more likely its respective
entry is to be victimized.

Tree Pseudo Least Recently Used (TreePLRU) {#tree_pseudo_least_recently_used_treeplru}
------------------------------------------

A variation of the LRU that uses a binary tree to keep track of the
recency of use of the entries through 1-bit pointers.

Bimodal Insertion Policy (BIP) {#bimodal_insertion_policy_bip}
------------------------------

The [Bimodal Insertion Policy] is similar to the LRU, however, blocks
have a probability of being inserted as the MRU, according to a bimodal
throttle parameter (btp). The highest btp is, the highest is the
likelihood of a new block being inserted as MRU.

LRU Insertion Policy (LIP) {#lru_insertion_policy_lip}
--------------------------

The [LRU Insertion Policy][Bimodal Insertion Policy] consists of a LRU
replacement policy that instead of inserting blocks with the most recent
last touch timestamp, it inserts them as the LRU entry. On subsequent
touches to the block, its timestamp is updated to be the MRU, as in LRU.
It can also be seen as a BIP where the likelihood of inserting a new
block as the most recently used is 0%.

Most Recently Used (MRU) {#most_recently_used_mru}
------------------------

The Most Recently Used policy chooses replacement victims by their
recency, however, as opposed to LRU, the newer the entry is, the more
likely it is to be victimized.

Least Frequently Used (LFU) {#least_frequently_used_lfu}
---------------------------

The victim is chosen using the reference frequency. The least referenced
entry is chosen to be evicted, regardless of the amount of times it has
been touched, or how much time has passed since its last touch.

First-In, First-Out (FIFO) {#first_in_first_out_fifo}
--------------------------

The victim is chosen using the insertion timestamp. If no invalid
entries exist, the oldest one is victimized, regardless of the amount of
times it has been touched.

Second-Chance {#second_chance}
-------------

The [Second-Chance] replacement policy is similar to FIFO, however
entries are given a second chance before being victimized. If an entry
would have been the next to be victimized, but its second chance bit is
set, this bit is cleared, and the entry is re-inserted at the end of the
FIFO. Following a miss, an entry is inserted with its second chance bit
cleared.

Not Recently Used (NRU) {#not_recently_used_nru}
-----------------------

Not Recently Used (NRU) is an approximation of LRU that uses a single
bit to determine if a block is going to be re-referenced in the near or
distant future. If the bit is 1, it is likely to not be referenced soon,
so it is chosen as the replacement victim. When a block is victimized,
all its co-replacement candidates have their re-reference bit
incremented.

Re-Reference Interval Prediction (RRIP) {#re_reference_interval_prediction_rrip}
---------------------------------------

[Re-Reference Interval Prediction (RRIP)] is an extension of NRU that
uses a re-reference prediction value to determine if blocks are going to
be re-used in the near future or not. The higher the value of the RRPV,
the more distant the block is from its next access. From the original
paper, this implementation of RRIP is also called Static RRIP (SRRIP),
as it always inserts blocks with the same RRPV.

Bimodal Re-Reference Interval Prediction (BRRIP) {#bimodal_re_reference_interval_prediction_brrip}
------------------------------------------------

[Bimodal Re-Reference Interval Prediction
(BRRIP)][Re-Reference Interval Prediction (RRIP)] is an extension of
RRIP that has a probability of not inserting blocks as the LRU, as in
the Bimodal Insertion Policy. This probability is controlled by the
bimodal throtle parameter (btp).

  [Second-Chance]: https://apps.dtic.mil/docs/citations/AD0687552
  [Re-Reference Interval Prediction (RRIP)]: https://dl.acm.org/citation.cfm?id=1815971
  [Cache Replacement Policies Wikipedia page]: https://en.wikipedia.org/wiki/Cache_replacement_policies
  [Bimodal Insertion Policy]: https://dl.acm.org/citation.cfm?id=1250709


---


## "Introduction"

*Source: https://www.gem5.org/documentation/general_docs/ruby/*

# Ruby

Ruby implements a detailed simulation model for the memory subsystem. It
models inclusive/exclusive cache hierarchies with various replacement
policies, coherence protocol implementations, interconnection networks,
DMA and memory controllers, various sequencers that initiate memory
requests and handle responses. The models are modular, flexible and
highly configurable. Three key aspects of these models are:

1.  Separation of concerns -- for example, the coherence protocol
    specifications are separate from the replacement policies and cache
    index mapping, the network topology is specified separately from the
    implementation.
2.  Rich configurability -- almost any aspect affecting the memory
    hierarchy functionality and timing can be controlled.
3.  Rapid prototyping -- a high-level specification language, SLICC, is
    used to specify functionality of various controllers.

The following picture, taken from the GEMS tutorial in ISCA 2005, shows
a high-level view of the main components in Ruby.
![ruby_overview.jpg](/assets/img/Ruby_overview.jpg)

For a tutorial-based approach to Ruby see [Part III of Learning gem5](/documentation/learning_gem5/part3/)

### SLICC + Coherence protocols:

***[SLICC](slicc)*** stands for *Specification Language for
Implementing Cache Coherence*. It is a domain specific language that is
used for specifying cache coherence protocols. In essence, a cache
coherence protocol behaves like a state machine. SLICC is used for
specifying the behavior of the state machine. Since the aim is to model
the hardware as close as possible, SLICC imposes constraints on the
state machines that can be specified. For example, SLICC can impose
restrictions on the number of transitions that can take place in a
single cycle. Apart from protocol specification, SLICC also combines
together some of the components in the memory model. As can be seen in
the following picture, the state machine takes its input from the input
ports of the inter-connection network and queues the output at the
output ports of the network, thus tying together the cache / memory
controllers with the inter-connection network itself.

![slicc_overview.jpg](/assets/img/Slicc_overview.jpg)

The following cache coherence protocols are supported:

1.  **[MI_example](MI_example)**: example protocol, 1-level
    cache.
2.  **[MESI_Two_Level](MESI_Two_Level)**: single chip,
    2-level caches, strictly-inclusive hierarchy.
3.  **[MOESI_CMP_directory](MOESI_CMP_directory)**:
    multiple chips, 2-level caches, non-inclusive (neither strictly
    inclusive nor exclusive) hierarchy.
4.  **[MOESI_CMP_token](MOESI_CMP_token)**: 2-level caches.
    TODO.
5.  **[MOESI_hammer](MOESI_hammer)**: single chip, 2-level
    private caches, strictly-exclusive hierarchy.
6.  **[Garnet_standalone](Garnet_standalone)**: protocol to
    run the Garnet network in a standalone manner.
7.  **MESI Three Level**: 3-level caches,
    strictly-inclusive hierarchy. Based on MESI Two Level with an extra L0 cache.
8.  **[CHI](CHI)**: flexible protocol that implements Arm's AMBA5 CHI transactions.
    Supports configurable cache hierarchy with both MESI or MOESI coherency.

Commonly used notations and data structures in the protocols have been
described in detail [here](cache-coherence-protocols).

### Protocol independent memory components

1.  **Sequencer**
2.  **Cache Memory**
3.  **Replacement Policies**
4.  **Memory Controller**

In general cache coherence protocol independent components comprises of
the Sequencer, Cache Memory structure, Cache Replacement policies and
the Memory controller. The Sequencer class is responsible for feeding
the memory subsystem (including the caches and the off-chip memory) with
load/store/atomic memory requests from the processor. Every memory
request when completed by the memory subsystem also send back the
response to the processor via the Sequencer. There is one Sequencer for
each hardware thread (or core) simulated in the system. The Cache Memory
models a set-associative cache structure with parameterizable size,
associativity, replacement policy. L1, L2, L3 caches (if exists)in the
system are instances of Cache Memory. The Cache Replacement policies are
kept modular from the Cache Memory, so that different instances of Cache
Memory can use different replacement policies of their choice. Currently
two replacement polices -- LRU and Pseudo-LRU -- are distributed with
the release. Memory Controller is responsible for simulating and
servicing any request that misses on all the on-chip caches of the
simulated system. Memory Controller currently simple, but models DRAM
ban contention, DRAM refresh faithfully. It also models close-page
policy for DRAM buffer.

### Interconnection Network

The interconnection network connects the various components of the
memory hierarchy (cache, memory, dma controllers) together.

![Interconnection_network.jpg](/assets/img/Interconnection_network.jpg
"Interconnection_network.jpg")

The key components of an interconnection network are:

1.  **Topology**
2.  **Routing**
3.  **Flow Control**
4.  **Router Microarchitecture**

***More details about the network model implementation are described
[here](Interconnection_Network).***

Alternatively, Interconnection network could be replaced with the
external simulator [TOPAZ](https://github.com/ceunican/tpzsimul). This
simulator is ready to run within gem5 and adds a significant number of
features
over original ruby network simulator. It includes, new advanced router
micro-architectures, new topologies, precision-performance adjustable
router models, mechanisms to speed-up network simulation, etc.
 
## Life of a memory request in Ruby

In this section we will provide a high level overview of how a memory
request is serviced by Ruby as a whole and what components in Ruby it
goes through. For detailed operations within each components though,
refer to previous sections describing each component in isolation.

1.  A memory request from a core or hardware context of gem5 enters the
    jurisdiction of Ruby through the ***RubyPort::recvTiming***
    interface (in src/mem/ruby/system/RubyPort.hh/cc). The number of
    Rubyport instantiation in the simulated system is equal to the
    number of hardware thread context or cores (in case of
    *non-multithreaded* cores). A port from the side of each core is
    tied to a corresponding RubyPort.
2.  The memory request arrives as a gem5 packet and RubyPort is
    responsible for converting it to a RubyRequest object that is
    understood by various components of Ruby. It also finds out if the
    request is for some PIO or not and maneuvers the packet to correct
    PIO. Finally once it has generated the corresponding RubyRequest
    object and ascertained that the request is a *normal* memory request
    (not PIO access), it passes the request to the
    ***Sequencer::makeRequest*** interface of the attached Sequencer
    object with the port (variable *ruby_port* holds the pointer to
    it). Observe that Sequencer class itself is a derived class from the
    RubyPort class.
3.  As mentioned in the section describing Sequencer class of Ruby,
    there are as many objects of Sequencer in a simulated system as the
    number of hardware thread context (which is also equal to the number
    of RubyPort object in the system) and there is an one-to-one mapping
    between the Sequencer objects and the hardware thread context. Once
    a memory request arrives at the ***Sequencer::makeRequest***, it
    does various accounting and resource allocation for the request and
    finally pushes the request to the Ruby's coherent cache hierarchy
    for satisfying the request while accounting for the delay in
    servicing the same. The request is pushed to the Cache hierarchy by
    enqueueing the request to the *mandatory queue* after accounting for
    L1 cache access latency. The *mandatory queue* (variable name
    *m_mandatory_q_ptr*) effectively acts as the interface between
    the Sequencer and the SLICC generated cache coherence files.
4.  L1 cache controllers (generated by SLICC according to the coherence
    protocol specifications) dequeues request from the *mandatory queue*
    and looks up the cache, makes necessary coherence state transitions
    and/or pushes the request to the next level of cache hierarchy as
    per the requirements. Different controller and components of SLICC
    generated Ruby code communicates among themselves through
    instantiations of *MessageBuffer* class of Ruby
    (src/mem/ruby/buffers/MessageBuffer.cc/hh) , which can act as
    ordered or unordered buffer or queues. Also the delays in servicing
    different steps for satisfying a memory request gets accounted for
    scheduling enqueue-ing and dequeue-ing operations accordingly. If
    the requested cache block may be found in L1 caches and with
    required coherence permissions then the request is satisfied and
    immediately returned. Otherwise the request is pushed to the next
    level of cache hierarchy through *MessageBuffer*. A request can go
    all the way up to the Ruby's Memory Controller (also called
    Directory in many protocols). Once the request get satisfied it is
    pushed upwards in the hierarchy through *MessageBuffer*s.
5.  The *MessageBuffers* also act as entry point of coherence messages
    to the on-chip interconnect modeled. The MesageBuffers are connected
    according to the interconnect topology specified. The coherence
    messages thus travel through this on-chip interconnect accordingly.
6.  Once the requested cache block is available at L1 cache with desired
    coherence permissions, the L1 cache controller informs the
    corresponding Sequencer object by calling its ***readCallback*** or
    **'writeCallback**'' method depending upon the type of the request.
    Note that by the time these methods on Sequencer are called the
    latency of servicing the request has been implicitly accounted for.
7.  The Sequencer then clears up the accounting information for the
    corresponding request and then calls the
    ***RubyPort::ruby_hit_callback*** method. This ultimately returns
    the result of the request to the corresponding port of the core/
    hardware context of the frontend (gem5).

## Directory Structure

  - **src/mem/**
      - **protocols**: SLICC specification for coherence protocols
      - **slicc**: implementation for SLICC parser and code generator
      - **ruby**
          - **common**: frequently used data structures, e.g. Address
            (with bit-manipulation methods), histogram, data block
          - **filters**: various Bloom filters (stale code from GEMS)
          - **network**: Interconnect implementation, sample topology
            specification, network power calculations, message buffers
            used for connecting controllers
          - **profiler**: Profiling for cache events, memory controller
            events
          - **recorder**: Cache warmup and access trace recording
          - **slicc_interface**: Message data structure, various
            mappings (e.g. address to directory node), utility functions
            (e.g. conversion between address & int, convert address to
            cache line address)
          - **structures**: Protocol independent memory components –
            CacheMemory, DirectoryMemory
          - **system**: Glue components – Sequencer, RubyPort,
            RubySystem


---


## "CHI"

*Source: https://www.gem5.org/documentation/general_docs/ruby/CHI/*

# CHI

The CHI ruby protocol provides a single cache controller that can be reused at multiple levels of the cache hierarchy and configured to model multiple instances of MESI and MOESI cache coherency protocols. This implementation is based of [Arm's AMBA 5 CHI specification](https://developer.arm.com/documentation/ihi0050/D/) and provides a scalable framework for the design space exploration of large SoC designs.

- [CHI overview and terminology](#chi-overview)
- [Protocol overview](#protocol-overview)
- [Protocol implementation](#protocol-implementation)
  - [Transaction allocation](#transaction-allocation)
  - [Transaction initialization](#transaction-initialization)
  - [Transaction execution](#transaction-execution)
  - [Transaction finalization](#transaction-finalization)
  - [Hazard handling](#hazard-handling)
  - [Performance modeling](#performance-modeling)
  - [Cache block allocation and replacement modeling](#cache-block-allocation-and-replacement-modeling)
- [Supported CHI transactions](#supported-chi-transactions)
  - [Supported requests](#supported-requests)
  - [Supported snoops](#supported-snoops)
  - [Writeback and evictions](#writeback-and-evictions)
  - [Hazards](#hazards)
  - [Other implementations notes](#other-implementations-notes)
  - [Protocol table](#protocol-table)

## CHI overview and terminology

CHI (Coherent Hub Interface) provides a component architecture and transaction-level specification to model MESI and MOESI cache coherency. CHI defines three main components as shown in the figure below:

[chi_components]: /assets/img/ruby_chi/chi_components.png
![CHI components][chi_components]

- the request node initiates transactions and sends requests towards memory. A request node can be a *fully coherent request node (**RNF**)*, meaning the request node caches data locally and should respond to snoop requests.
- the interconnect (ICN) which is the responder for request nodes. At protocol level the interconnect is a component encapsulating the *fully coherent home nodes (**HNF**)* of the system.
- the *slave nodes (**SNF**)*, which interface with the memory controllers.

An HNF is the point of coherency (PoC) and point of serialization (PoS) for a specific address range. The HNF is responsible for issuing any required snoop requests to RNFs or memory access requests to SNFs in order to complete a transaction. The HNF can also encapsulate a shared last-level cache and include a directory for targeted snoops.

The [CHI specification](https://developer.arm.com/documentation/ihi0050/D/) also defines specific types of nodes for non-coherent requesters (RNI) and non-coherent address ranges (HNI and SNI), e.g., memory ranges belonging to IO components. In Ruby, IO accesses don't go though the cache coherency protocol so only CHI's fully coherent node types are implemented. In this documentation we interchangeably use the terms RN / RNF, HN / HNF, and SN/SNF. We also use the terms **upstream** and **downstream** to refer to components in the previous (i.e. towards the cpu) and next  (i.e. towards memory) levels in the memory hierarchy, respectively.

## Protocol overview

The CHI protocol implementation consists mainly of two controllers:

- `Memory_Controller` (**src/mem/ruby/protocol/chi/CHI-mem.sm**) implements a CHI slave node. It receives memory read or write requests from the home nodes and interfaces with gem5’s classic memory controllers.
- `Cache_Controller` (**src/mem/ruby/protocol/chi/CHI-cache.sm**) generic cache controller state machine.

In order to allow fully flexible cache hierarchies, `Cache_Controller` can be configured to model any cache level (e.g. L1D, priv. L2, shared L3) within both request and home nodes. Furthermore it also supports multiple features not available in other Ruby protocols:

- configurable cache block allocation and deallocation policies for each request type.
- unified or separate transaction buffers for incoming and outgoing requests.
- MESI or MOESI operation.
- directory and cache tag and data array stalls.
- parameters to inject latency in multiple steps of the request handling flow. This allows us to more closely calibrate the performance.

The implementation defines the following cache states:

- `I`: line is invalid
- `SC`: line is shared and clean
- `UC`: line is exclusive/unique and clean
- `SD`: line is shared and dirty
- `UD`: line exclusive/unique and dirty
- `UD_T`: `UD` with timeout. When a store conditional fails and causes the line to transition from I to UD, we transition to `UD_T` instead if the number of failures is above a certain threshold (configuration defined). In `UD_T` the line cannot be evicted from the requester for a given number of cycles (also configuration defined); after which the lines goes to UD. This is necessary to avoid livelocks in certain scenarios.

The figure below gives an overview of the state transitions when the controller is configured as a L1 cache:

[sm_l1_cache]: /assets/img/ruby_chi/sm_l1_cache.svg
![L1 cache state machine][sm_l1_cache]

Transitions are annotated with the incoming request from the cpu (or generated internally, e.g. *Replacements*) and the resulting outgoing request sent downstream. For simplicity, the figure omits requests that do not change states (e.g., cache hits) and invalidating snoops (final state is always `I`). For simplicity, it also shows only the typical state transitions in a MOESI protocol. In CHI the final state will ultimately be determined by the type of data returned by the responder (e.g., requester may receive `UD` or `UC` data in  response to a `ReadShared`).

The figures below show the transition for a *intermediate-level* cache controller (e.g., priv. L2, shared L3, HNF, etc):

[sm_lx_cache]: /assets/img/ruby_chi/sm_lx_cache.svg
![Intermediate cache state machine][sm_lx_cache]

[sm_lx_dir]: /assets/img/ruby_chi/sm_lx_dir.svg
![Intermediate cache directory states][sm_lx_dir]

As in the previous case, cache hits are omitted for simplicity. In addition to the cache states, the following directory states are defined to track lines present in an upstream cache:

- `RU`:an upstream requester has line in UC or UD
- `RSC`: one or more upstream requesters have line in SC
- `RSD`: one upstream requester has line in SD; others may have it in SC
- `RUSC`: `RSC` + current domain stills has exclusive access
- `RUSD`: `RSD` + current domain stills has exclusive access

When the line is present both in the local cache and upstream caches the following combined states are possible:

- `UD_RSC`, `SD_RSC`, `UC_RSC`, `SC_RSC`
- `UD_RU`, `UC_RU`
- `UD_RSD`, `SD_RSD`

The `RUSC` and `RUSD` states (omitted in the figures above) are used to keep track of lines for which the controller still has exclusive access permissions without having it in it’s local cache. This is possible in a non-inclusive cache where a local block can be deallocated without back-invalidating upstream copies.

When a cache controller is a HNF (home node), the state transactions are basically the same as a intermediate level cache, except for these differences:

- A `ReadNoSnp` is sent to obtain data from downstream, as the only downstream components are the SNs (slave nodes).
- On a cache and directory miss, DMT (direct memory transfer) is used if enabled.
- On a cache miss and directory hit, DCT (direct cache transfer) is used if enabled.

For more information on DCT and DMT transactions, see Sections 1.7 and 2.3.1 in the [CHI specification](https://developer.arm.com/documentation/ihi0050/D/). DMT and DCT are CHI features that allow the data source for a request to send data directly to the original requester. On a DMT request, the SN sends data directly to the RN (instead of sending first to the HN, which would then forwards to the RN), while with DCT, the HN requests that a RN being snooped (the snoopee) to send a copy of the line directly the original requester. With DCT enabled, the HN may also request that the snoopee to send the data to both the HN and the original requester, so the HN can also cache the data. This depends on the allocation policy defined by the configuration parameters. Notice that the allocation policy also changes the cache state transitions. For simplicity, the figure above illustrates an inclusive cache.

The following is a list of the main configuration parameters of the cache controller that affect the protocol behavior (please refer to the protocol SLICC specification for details and a full list of parameters)

- `downstream_destinations`: defines the destinations for requests sent downstream and is used to build the cache hierarchy. Refer to the `create_system` function in `configs/ruby/CHI.py` for an example of how to setup a system with private L1I, L1D and L2 caches for each core.
- `is_HN`: Set when the controller is used as a home node and point of coherency for an address range. Must be false for every other cache level.
- `enable_DMT` and `enable_DCT`: when the controller is a home node, this enables direct memory transfers and direct cache transfers for incoming read requests.
- `allow_SD`: allow the shared dirty state. This switches between MOESI and MESI operation.
- `alloc_on_readshared`, `alloc_on_readunique`, and `alloc_on_readonce`: whether or not to allocate a cache block to store data used to respond to the corresponding read request.
- `alloc_on_writeback`: whether or not to allocate a cache block to store data received from a writeback request.
- `dealloc_on_unique` and `dealloc_on_shared`: deallocate the local cache block if the line becomes unique or shared in an upstream cache.
- `dealloc_backinv_unique` and `dealloc_backinv_shared`: if a local cache block is deallocated due to a replacement, also invalidates any unique or shared copy of the line in upstream caches.
- `number_of_TBEs`,`number_of_snoop_TBEs`, and `number_of_repl_TBEs`: number of entries in the TBE tables for incoming requests, incoming snoops, and replacements.
- `unify_repl_TBEs`: replacements use the same TBE slot as the request that triggered it. In this case `number_of_repl_TBEs` is ignored.

These parameters affect the cache controller performance:

- `read_hit_latency` and `read_miss_latency`: pipeline latencies for a read request thar hits or misses in the local cache, respectively.
- `snoop_latency`: pipeline latency for an incoming snoop.
- `write_fe_latency` and `write_be_latency`: front-end and back-end pipeline latencies for handling write requests. Front-end latency is applied between sending the acknowledgement response and the next action to be taken. Back-end is applied to the requester between receiving the acknowledgement and sending the write data.
- `allocation_latency`: latency between TBE allocation and transaction initialization.
- `cache`: `CacheMemory` attached to this controller includes parameters such as size, associativity, tag and data latency, and number of banks.

Section [Protocol implementation](#protocol-implementation) gives an overview of the protocol implementation while Section [Supported CHI transactions](#supported-chi-transactions) describe the implemented subset of the the AMBA 5 CHI spec. The next sections refer to specific files in the protocol source code and include SLICC snippets of the protocol. Some snippets where slightly simplified compared to the actual SLICC specification.

## Protocol implementation

The Figure below gives an overview of the cache controller implementation.

[cache_cntrl_arch]: /assets/img/ruby_chi/cache_cntrl_arch.png
![Cache controller architecture][cache_cntrl_arch]

In Ruby, a cache controller is implemented by defining a state machine using SLICC language. Transitions in the state machine are triggered by messages arriving at input queues. On our particular implementation, separate incoming and outgoing messages queues are defined for each CHI channel. Incoming request and snoop messages that
start a new transaction go through the same *Request allocation* process, where we allocate a transaction buffer entry (TBE) and move the request or snoop to an internal queue of transactions that are ready to
be initiated. If the transaction buffer is full, the request is rejected and a retry message is sent.

The actions to be performed for a message dequeued from the input / rdy queues depends on the state of the target cache line. The data state of the line is stored in the cache if the line is cached locally, while the
directory state is stored in a directory entry if the line is present in any upstream cache. For lines with outstanding requests, the transient state is kept in the TBE and copied back to the cache and/or directory
when the transaction finishes. The figure below describes the phases in the transaction lifetime and the interactions between the main components in the cache controller (input/output ports, TBETable, Cache, Directory and the SLICC state machine). The phases are described in more details in the subsequent sections.

[transaction_phases]: /assets/img/ruby_chi/transaction_phases.png
![Transaction lifetime][transaction_phases]

### Transaction allocation

The code snippet below shows how an incoming request in the `reqIn` port is handled. The `reqIn` port receives incoming messages from CHI's request channel:

    in_port(reqInPort, CHIRequestMsg, reqIn) {
      if (reqInPort.isReady(clockEdge())) {
        peek(reqInPort, CHIRequestMsg) {
          if (in_msg.allowRetry) {
            trigger(Event:AllocRequest, in_msg.addr, 
                  getCacheEntry(in_msg.addr), getCurrentActiveTBE(in_msg.addr));
          } else {
            trigger(Event:AllocRequestWithCredit, in_msg.addr,
                  getCacheEntry(in_msg.addr), getCurrentActiveTBE(in_msg.addr));
          }
        }
      }
    }

The `allowRetry` field indicates messages that can be retried. Requests that cannot be retried are only sent by a requester that previously received credit (see `RetryAck` and `PCrdGrant` in the CHI specification). The transition triggered by `Event:AllocRequest` or `Event:AllocRequestWithCredit` executes a single action which either reserves space in the TBE table for the request and moves it to the `reqRdy` queue, or sends a `RetryAck` message):

    action(AllocateTBE_Request) {
      if (storTBEs.areNSlotsAvailable(1)) {
        // reserve a slot for this request
        storTBEs.incrementReserved();
        // Move request to rdy queue
        peek(reqInPort, CHIRequestMsg) {
          enqueue(reqRdyOutPort, CHIRequestMsg, allocation_latency) {
            out_msg := in_msg;
          }
        }
      } else {
        // we don't have resources to track this request; enqueue a retry
        peek(reqInPort, CHIRequestMsg) {
          enqueue(retryTriggerOutPort, RetryTriggerMsg, 0) {
            out_msg.addr := in_msg.addr;
            out_msg.event := Event:SendRetryAck;
            out_msg.retryDest := in_msg.requestor;
            retryQueue.emplace(in_msg.addr,in_msg.requestor);
          }
        }
      }
      reqInPort.dequeue(clockEdge());
    }

Notice we don’t create and send a `RetryAck` message directly from this action. Instead we create a separate trigger event in the internal `retryTrigger` queue. This is necessary to prevent resource stalls from halting this action. Section [Performance modeling](#performance-modeling) below explains resource stalls in more details.

Incoming request from a `Sequencer` object (typically connected to a CPU when the controller is used as a L1 cache) and snoop requests arrive through the `seqIn` and `snpIn` ports and are handled similarly, except for:

- they do not support retries. If there are no TBEs available, a resource stall is generated and we try again next cycle.
- snoops allocate TBEs from a separate TBETable to avoid deadlocks.

### Transaction initialization

Once a request has been allocated a TBE and moved to the `reqRdy` queue, an event is triggered to initiate the transaction. We trigger a different event for each different request type:

    in_port(reqRdyPort, CHIRequestMsg, reqRdy) {
      if (reqRdyPort.isReady(clockEdge())) {
        peek(reqRdyPort, CHIRequestMsg) {
          CacheEntry cache_entry := getCacheEntry(in_msg.addr);
          TBE tbe := getCurrentActiveTBE(in_msg.addr);
          trigger(reqToEvent(in_msg.type), in_msg.addr, cache_entry, tbe);
        }
      }
    }

Each request requires different initialization actions depending on the initial state of the line. To illustrate this processes, let’s use as example a `ReadShared` request for a line in the `SC_RSC` state (shared
clean in local cache and shared clean in an upstream cache):

    transition(SC_RSC, ReadShared, BUSY_BLKD) {
      Initiate_Request;
      Initiate_ReadShared_Hit;
      Profile_Hit;
      Pop_ReqRdyQueue;
      ProcessNextState;
    }

- `Initiate_Request` initializes the allocated TBE. This actions copies any state and data allocated in the local cache and directory to the TBE.
- `Initiate_ReadShared_Hit` sets-up the set of actions that need to be executed to complete this specific request (see below).
- `Profile_Hit` updates cache statistics.
- `Pop_ReqRdyQueue` removes request message form the `reqRdy` queue.
- `ProcessNextState` executes the next action defined by `Initiate_ReadShared_Hit`.

`Initiate_ReadShared_Hit` is defined as follows:

    action(Initiate_ReadShared_Hit) {
      tbe.actions.push(Event:TagArrayRead);
      tbe.actions.push(Event:ReadHitPipe);
      tbe.actions.push(Event:DataArrayRead);
      tbe.actions.push(Event:SendCompData);
      tbe.actions.push(Event:WaitCompAck);
      tbe.actions.pushNB(Event:TagArrayWrite);
    }

`tbe.actions` stores the list of events that need to be triggered in order to complete an action. In this particular case, `TagArrayRead`, `ReadHitPipe`, and `DataArrayRead` introduces delays to model the cache
controller pipeline latency and reading the cache/directory tag array and cache data array (see Section [Performance modeling](#performance-modeling)). `SendCompData` sets-up and sends the data responses for the `ReadShared` request and `WaitCompAck` sets-up the TBE to expect the completion acknowledgement from the requester. Finally, `TagArrayWrite` introduces the delay of updating the directory state to track the new sharer.

### Transaction execution

After initialization, the line will transition to the `BUSY_BLKD` state as show in `transition(SC_RSC, ReadShared, BUSY_BLKD)`. `BUSY_BLKD` is a transient state indicating the line has now an outstanding transaction. In this state, the transaction is driven either by incoming response messages in the `rspIn` and `datIn` ports or trigger events defined in `tbe.actions`.

The `ProcessNextState` action is responsible for checking `tbe.actions` and enqueuing trigger event messages into `actionTriggers` at the end of all transitions to the `BUSY_BLKD` state. `ProcessNextState` first checks for pending response messages. If there are no pending messages, it enqueues a message to `actionTriggers` in order to trigger the the event at the head of `tbe.actions`. If there are pending responses, then `ProcessNextState` does nothing as the transaction will proceed once all expected responses are received.

Pending responses are tracked by the `expected_req_resp` and `expected_snp_resp` fields in the TBE. For instance, the `ExpectCompAck` action, executed from the transition triggered by `WaitCompAck`, is defined as follows:

    action(ExpectCompAck) {
      tbe.expected_req_resp.addExpectedRespType(CHIResponseType:CompAck);
      tbe.expected_req_resp.addExpectedCount(1);
    }

This causes the transaction to wait until a `CompAck` response is received.

Some actions can be allowed to execute when the transaction has pending responses. This actions are enqueued using `tbe.actions.pushNB` (i.e., push / non-blocking). In the example above `tbe.actions.pushNB(Event:TagArrayWrite)` models a tag write being performed while the transactions waits for the `CompAck` response.

### Transaction finalization

The transaction ends when it has no more pending responses and `tbe.actions` is empty. `ProcessNextState` checks for this condition and enqueues a “finalizer” trigger message into `actionTriggers`. When handling this event, the current cache line state and sharing/ownership information determines the final stable state of the line. Data and state information are updated in the cache and directory, if necessary, and the TBE is deallocated.

### Hazard handling

Each controller allows only one active transaction per cache line. If a new request or snoop arrives while the cache line is in a transient state, this creates a hazard as defined in the CHI standard. We handle hazards as follows:

**Request hazards:** a TBE is allocated as described previously, but the new transaction initialization is delayed until the current transaction finishes and the line is back to a stable state. This is done by moving
the request message from `reqRdy` to a separate *stall buffer*. All stalled messages are added back to `reqRdy` when the current transaction finishes and are handled in their original order of arrival.

**Snoop hazards:** the CHI spec does not allow snoops to be stalled by an existing request. If a transaction is waiting on a response for a request sent downstream (e.g. we sent a `ReadShared` and are waiting for
the data response) we must accept and handle the snoop. The snoop can be stalled only if the request has already been accepted by the responder and is guaranteed to complete (e.g. a `ReadShared` with pending data but
already acked with a `RespSepData` response). To distinguish between these conditions we use the `BUSY_INTR` transient state.

`BUSY_INTR` indicates the transaction can be interrupted by a snoop. When a snoop arrives for a line in this state, a snoop TBE is allocated as described previously and its state is initialized based on the currently active TBE. The snoop TBE then becomes the currently active TBE. Any cache state and sharing/ownership changes caused by snoop are copied back to the original TBE before deallocating the snoop. When a snoop arrives for a line in `BUSY_BLKD` state, we stall the snoop until the current transaction either finishes or transitions to `BUSY_INTR`.

### Performance modeling

As described previously, the cache line state is known immediately when a transaction is initialized and the cache line can be read and written without any latency. This makes it easier to implement the functional
aspects of the protocol. To model timing we use explicit actions to introduce latency to a transaction. For example, in the `ReadShared` code snippet:

    action(Initiate_ReadShared_Hit) {
      tbe.actions.push(Event:TagArrayRead);
      tbe.actions.push(Event:ReadHitPipe);
      tbe.actions.push(Event:DataArrayRead);
      tbe.actions.push(Event:SendCompData);
      tbe.actions.push(Event:WaitCompAck);
      tbe.actions.pushNB(Event:TagArrayWrite);
    }

`TagArrayRead`, `ReadHitPipe`, `DataArrayRead`, and `TagArrayWrite` don’t have any functional significance. They are there to introduce latencies that would exist in a real cache controller pipeline, in this case: tag read latency, hit pipeline latency, data array read latency, and tag update latency. The latency introduced by these action is defined by configuration parameters.

In addition to explicitly added latencies. SLICC has the concept of *resource stalls* to model resource contention. Given a set of actions executed during a transition, the SLICC compiler automatically generates
code which checks if all resources needed by those actions are available. If any resource is unavailable, a resource stall is generated and the transition is not executed. A message that causes a resource stall remains in the input queue and the protocol attempts to trigger the transition again the next cycle.

Resources are detected by the SLICC compiler in different ways:

1. Implicitly. This is the case for output ports. If an action enqueues new messages, the availability of the output port is automatically checked.
2. Adding the `check_allocate` statement to an action.
3. Annotating the transition with a resource type.

We use (2) to check availability of TBEs. See the snippet below:

    action(AllocateTBE_Snoop) {
      // No retry for snoop requests; just create resource stall
      check_allocate(storSnpTBEs);
      ...
    }

This signals the SLICC compiler to check if the `storSnpTBEs` structure has a TBE slot available before executing any transition that includes the `AllocateTBE_Snoop` action.

The snippet below exemplifies (3):

    transition({BUSY_INTR,BUSY_BLKD}, DataArrayWrite) {DataArrayWrite} {
      ...
    }

The `DataArrayWrite` annotation signals the SLICC compiler to check for availability of the `DataArrayWrite` resource type. *Resource request types* used in these annotations must be explicitly defined by the protocol, as well as how to check them. In our protocol we defined the following types to check for the availability of banks in the cache tag and data arrays:

    enumeration(RequestType) {
      TagArrayRead;
      TagArrayWrite;
      DataArrayRead;
      DataArrayWrite;
    }

    void recordRequestType(RequestType request_type, Addr addr) {
      if (request_type == RequestType:DataArrayRead) {
        cache.recordRequestType(CacheRequestType:DataArrayRead, addr);
      }
      ...
    }

    bool checkResourceAvailable(RequestType request_type, Addr addr) {
      if (request_type == RequestType:DataArrayRead) {
        return cache.checkResourceAvailable(CacheResourceType:DataArray, addr);
      }
      ...
    }

The implementation of `checkResourceAvailable` and `recordRequestType` are required by SLICC compiler when we use annotations on transactions.

### Cache block allocation and replacement modeling

Consider the following transaction initialization code for a ReadShared miss:

    action(Initiate_ReadShared_Miss) {
      tbe.actions.push(Event:ReadMissPipe);
      tbe.actions.push(Event:TagArrayRead);
      tbe.actions.push(Event:SendReadShared);
      tbe.actions.push(Event:SendCompData);
      tbe.actions.push(Event:WaitCompAck);
      tbe.actions.push(Event:CheckCacheFill);
      tbe.actions.push(Event:TagArrayWrite);
    }

All transactions that modify a cache line or received cache line data as a result of a snoop or a request sent downstream, use the `CheckCacheFill` action trigger event. This event triggers a transition that perform the following actions:

- Checks if we need to store the current cache line data in the local cache.
- Checks if we already have a cache block allocated for that line. If not, attempts to allocate a block. If block not available, a victim block is selected for replacement.
- Models the latency of a cache fill.

When a replacement is performed, a new transaction is initialized to keep track of any WriteBack or Evict request sent downstream and/or snoops for backinvalidation (if the cache controller is configured the
enforce inclusivity). Depending on the configuration parameters, the TBE for the replacement uses resources from a dedicated TBETable or reuses the same resources of the TBE that triggered the replacement. In both
cases, the transaction that triggered the replacement completes without waiting for the replacement process.

Notice `CheckCacheFill` does not actually writes data to the cache block. If only ensures a cache block is allocated if needed, triggers replacements, and models the cache fill latencies. As described previously, TBE data is copied to the cache if needed during the transaction finalization.

## Supported CHI transactions

All transactions are implemented as described in the [AMBA5 CHI Issue D specification](https://developer.arm.com/documentation/ihi0050/D/). The next sections provide a more detailed explanation of the implementation-specific choices not fixed by the public document.

### Supported requests

The following incoming requests are supported:

- `ReadShared`
- `ReadNotSharedDirty`
- `ReadUnique`
- `CleanUnique`
- `ReadOnce`
- `WriteUniquePtl` and `WriteUniqueFull`

When receiving any request the clusivity configuration parameters are evaluated during the transaction initialization and the `doCacheFill` and `dataToBeInvalid` flags are set in the transaction buffer entry allocated for the request. `doCacheFill` indicates we should keep any valid copy of the line in the local cache;`dataToBeInvalid` indicates we must invalidate the local copy when completing the transaction.

When receiving `ReadShared` or `ReadUnique`, if the data is present at the local cache in the required state (e.g. `UC` or `UD` for `ReadUnique`), a `CompData` response is send to the requester. The response type depends on the value of `dataToBeInvalid`.

- If `dataToBeInvalid==true`
  - The unique and/or dirty state is always propagated
  - For a `ReadNotSharedDirty`, `CompData_SC` is always sent if local state is `SD` and the line is written-back using `WriteCleanFull`
- Else:
  - In response to a `ReadUnique`: propagate dirty state, i.e., `CompData_UD` or `CompData_UC`.
  - In response to a `ReadShared` or `ReadNotSharedDirty`: send `CompData_SC`. If `fwd_unique_on_readshared` configuration parameter is set, the `ReadShared` is handled as a `ReadUnique` if the line doesn't have other sharers.

When receiving a `ReadOnce`, `CompData_I` is always sent if the data is present at the local cache. For `WriteUniquePtl` handling see below.

If there is a cache miss, multiple actions may be performed depending on whether or not `doCacheFill` and `dataToBeInvalid==false`; and DCT or DMT is enabled:

- `ReadShared` / `ReadNotSharedDirty`:
  - If dir state is `RSD` or `RU`:
    - If DCT disabled: send `SnpShared` to owner; cache the line locally (if `doCacheFill`) and send response to requester.
    - If DCT enabled: send `SnpSharedFwd` to owner; if `doCacheFill==true`, the `retToSrc` field is set so the line can be cached locally.
  - If dir state is `RSC`:
    - If DCT disabled: send `SnpOnce` to one of the sharers; cache the line locally (if `doCacheFill`) and send
        response to requester.
    - If DCT enabled: send `SnpSharedFwd` to one of the sharers; if `doCacheFill==true`, the `retToSrc` field is set so the line can be cached locally.
  - Otherwise: issue a `ReadShared` / `ReadNotSharedDirty` or `ReadNoSnp` (if HNF). In the HNF configuration, `ReadNoSnp` is issued with DMT if DMT is enabled.
  - For `ReadNotSharedDirty`, `SnpNotSharedDirty` and `SnpNotSharedDirtyFwd` is sent instead.
- `ReadUnique`:
  - If dir state is `RU,RUSD,RUSC`:
    - If DCT disabled or clusivity is inclusive: send `SnpUnique` to owner; cache the line locally (if `doCacheFill `) and sent response to requester.
    - If DCT enabled and clusivity is exclusive: send `SnpUniqueFwd` to owner.
  - If dir state is `RSC`/`RSD`:
    - Send `SnpUnique` with `retToSrc=true` to invalidate sharers and obtain dirty line (in case of `RSD`)
    - If not HNF: send `CleanUnique` downstream to obtain unique permissions.
  - Otherwise: issue a `ReadUnique` or `ReadNoSnp` (if HNF). In the HNF configuration, `ReadNoSnp` is issued with DMT if DMT is enabled.
  - For `RUSC` amd `RSC`, if multiple sharers, only one sharer is selected as target of the above snoops. The other sharers are invalidated using `SnpUnique` with `retToSrc=false`.
- `ReadOnce`:
  - If dir entry exists:
    - If DCT disabled: send `SnpOnce` to one of the sharers; send received data response to requester.
    - If DCT enabled: send `SnpOnceFwd` to one of the sharers.
  - Otherwise: issue a `ReadOnce` or `ReadNoSnp` (if HNF). In the HNF configuration, `ReadNoSnp` is issued with DMT if DMT is enabled.
- `CleanUnique`:
  - Send `SnpCleanInvalid` to all sharers/owner except original requestor.
  - If not HNF: send `CleanUnique` downstream to obtain unique permissions.
  - If has dirty line, requestor has clean line, and `doCacheFill==false`: writeback the line with `WriteCleanFull`.
- `WriteUniquePtl`/`WriteUniqueFull`:
  - If data present in local cache on UC or UD states:
    - Issue `SnpCleanInvalid` if there are any sharers.
    - Perform the write in the local cache.
  - If no UC/UD data locally:
    - If HNF:
      - Issue `SnpCleanInvalid` if there are any sharers.
      - Merge any received snoop response data with the WriteUnique data.
      - If has a full line and `doCacheFill` set, cache the line locally, otherwise writeback to memory (`WriteNoSnp` or `WriteNoSnpPtl`).
    - If no HNF:
      - Forwards the `WriteUniquePtl` and any received data to the downstream cache.
      - Incoming snoops will cause any locally cached data to become invalid while handling the request.

### Supported snoops

The cache controller issues and accepts the following snoops:

- `SnpShared` and `SnpSharedFwd`
- `SnpNotSharedDirty` and `SnpNotSharedDirtyFwd`
- `SnpUnique` and `SnpUniqueFwd`
- `SnpCleanInvalid`
- `SnpOnce` and `SnpOnceFwd`

The snoop response is generated according to the current state of the line as defined in the specification. Data is returned with the snoop response depending on the data state and the value of `retToSrc`  set by the snooper. If `retToSrc` is set, the snoop response always includes data.

- `SnpShared` / `SnpNotSharedDirty`:
  - Snoopee always returns data is the line is dirty, unique or `retToSrc`.
  - `retToSrc` is set if the snooper needs to cache the line.
  - Final snoopee state always shared clean.
- `SnpUnique`:
  - Snoopee always returns data is the line is dirty, unique or `retToSrc`.
  - `retToSrc` is set if the snooper needs to cache the line.
  - Final snoopee state always invalid.
- `SnpCleanInvalid`:
  - Same as *SnpUnique*, except data is not returned if line is unique and clean.
- `SnpSharedFwd`:
  - `retToSrc` is set if the snooper needs to cache the line.
  - Line forwarded as dirty if dirty
  - Final snoopee state always shared clean
- `SnpNotSharedDirtyFwd`:
  - `retToSrc` is set if the snooper needs to cache the line.
  - Always returns data if line was dirty at the snoopee; line always forwarded as clean.
  - Final snoopee state always shared clean.
- `SnpUniqueFwd`:
  - Same as SnpUnique, except data is never returned to the snooper (as defined by the spec)
- `SnpOnce`:
  - Always generated with `retToSrc=true` and snoopee always returns data.
  - Accepted in any state (except invalid). Final snoopee state does not change.
- `SnpOnceFwd`:
  - Same as SnpOnce, except data is never returned to the snooper.

If the snoopee has sharers in any state, the same request is sent upstream to all sharers. For SnpSharedFwd/SnpNotSharedDirtyFwd and SnpUniqueFwd, a SnpShared/SnpNotSharedFwd or SnpUnique is sent, respectively. For a received SnpOnce, a SnpOnce is sent upstream only if the line is not present locally. In this particular implementation, there is always a directory entry for upstream caches that have the line. *Snoops are never sent to caches that do not have the line*.

### Writeback and evictions

A writeback is triggered internally by the controller when a cache line needs to be evicted due to capacity reasons (*cache maintenance operations are currently not supported*). See Section [Cache block allocation and replacement modeling](#cache-block-allocation-and-replacement-modeling) for more information on replacements. These internal events are generated depending on the configurations parameters of the controller:

- `GlobalEviction`: evict a line from the current and all upstream caches. This applies if `dealloc_backinv_unique` or `dealloc_backinv_shared` parameters are set.
- `LocalEviction`: evict a line without backinvaliding upstream caches.

First we deallocate the local cache block (so the request that cause the eviction can allocate a new block and finish). For GlobalEviction, a `SnpCleanInvalid` is sent to all upstream caches. Once all snoops responses are received (possibly with dirty data), a LocalEviction is performed. The LocalEviction is done by issuing the appropriate request as follows:

- `WriteBackFull`, if the the line is dirty
- `WriteEvictFull`, if the line is unique and clean
- `WriteCleanFull`, if the the line is dirty, but there are clean sharers
- `Evict`, if the line is shared and clean

For a HNF configuration the behavior changes slightly: `WriteNoSnp` to the SNF is used instead of `WriteBackFull` and no requests are issued if the line is clean.

The `WriteBack*` and `Evict` requests are handled at the downstream cache as follows:

- `WriteBackFull` / `WriteEvictFull` / `WriteCleanFull`:
  - If `alloc_on_writeback`, a cache block may need to be allocated. If there are no free blocks, a LocalEviction is triggered for a cache line in the target cache set. The victim line is selected based on the replacement policy implemented by object pointed by the `cache` parameter (which can be configured separately).
  - Send a `CompDBIDResp` to the requester.
  - Once data is received, update local cache and remove requestor from directory (if `WriteBackFull` / `WriteEvictFull`).
- `Evict`:
  - Remove requestor from directory and reply with `Comp\_I`.

### Hazards

A request for a line that currently has an outstanding transaction is always stalled until the transaction completes. Snoops received while there is an outstanding request are handled following the requirements
in the specification:

- For an outstanding `CleanUnique`:
  - Snoop response is sent immediately and the current line state is changed accordingly.
  - Notice we don't model the **UCE** and **UDP** states from the CHI spec. If the line is invalidated while the requester waits for a `CleanUnique` response, it immediately follows up with a `ReadUnique`.
- For outstanding `WriteBackFull`/`WriteEvictFull`/`WriteCleanFull` that have not yet been acked with a `CompDBIDResp`; or Evict before `Comp_I` is received:
  - Snoop response is sent immediately and the current line state is changed accordingly.
  - The state of the line that will be written back will the state after the snoop.
- If a snoop is received while the current transaction is waiting for snoop responses from upstream caches, the incoming snoop is stalled until all pending responses from upstream are received and any follow-up request is sent. This can happen in these scenarios:
  - During a global replacement
  - An accepted `ReadUnique` that required snooping upstream caches

Multiple snoops may be received while there is an outstanding transaction. In this particular implementation, a `SnpShared` or `SnpSharedFwd` may be followed by a `SnpUnique` or `SnpCleanInvalid`. However, it's not possible to have concurrent snoops coming from the downstream cache.

Both incoming requests and snoops require the allocation of a TBE. To prevent deadlocks when transaction buffers are full, a separate buffer is used to allocate snoop TBEs. Snoops do not allow retry, so if the snoop TBE table is full messages in the snpIn port are stalled, potentially causing severe congestion in the snoop channel in the interconnect.

### Other implementations notes

- If an HNF uses DMT, it will send `ReadNoSnpSep` instead of `ReadNoSnp` if the `enable_DMT_early_dealloc` configuration parameter is set. This allow the HNF to deallocate the TBE earlier.
- Order bit field is not implemented, thus `ReadReceipt` responses are never used except for `ReadNoSnpSep`. Request ordering, when required, is enforced by Ruby by serializing requests at the requester. At the cache controller, requests to the same line are handled in the order of arrival. Requests to different lines can be handled in any order, however they are typically handled in order of arrival given that there are resources available.
- Exclusive accesses and atomic requests are not implemented. Ruby has its own global monitor in the Sequencer to manage exclusive load and stores. Atomic operations also handled by Ruby and they only require a `ReadUnique` at the protocol level.
- `CompAck` response is always sent when stated as optional in the spec. Requesters always wait for `CompAck` (if required or optional) before finalizing the transaction and deallocating resources.
- Separate `Comp` and `DBIDresp` used only for `WriteUnique` requests. `DBIDresp` is sent after receiving all snoop responses; `Comp` is sent after `DBIDresp` and accounting for the front-end write latency (`write_fe_latency`).
- Memory attribute fields are not implemented.
- `DoNotGoToSD` field is not implemented.
- `CBusy` is not implemented.
- `WriteDataCancel` responses are never used.
- Error handling is not implemented.
- Cache stashing is not implemented.
- Atomic transactions are not implemented.
- DMV transactions are not implemented.
- Any request not listed in the protocol table below is not supported in this implementation.

### Protocol table

[Click here](/assets/img/ruby_chi/protocol_table.htm)


---


## "Garnet standalone"

*Source: https://www.gem5.org/documentation/general_docs/ruby/Garnet_standalone/*

# Garnet Standalone

This is a dummy cache coherence protocol that is used to operate Garnet
in a standalone manner. This protocol works in conjunction with the
[Garnet Synthetic Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)
injector.

### Related Files

  - **src/mem/protocols**
      - **Garnet_standalone-cache.sm**: cache controller specification
      - **Garnet_standalone-dir.sm**: directory controller
        specification
      - **Garnet_standalone-msg.sm**: message type specification
      - **Garnet_standalone.slicc**: container file

### Cache Hierarchy

This protocol assumes a 1-level cache hierarchy. The role of the cache
is to simply send messages from the cpu to the appropriate directory
(based on the address), in the appropriate virtual network (based on the
message type). It does not track any state. Infact, no CacheMemory is
created unlike other protocols. The directory receives the messages from
the caches, but does not send any back. The goal of this protocol is to
enable simulation/testing of just the interconnection network.

### Stable States and Invariants

| States | Invariants                        |
| ------ | --------------------------------- |
| **I**  | Default state of all cache blocks |

### Cache controller

  - Requests, Responses, Triggers:
      - Load, Instruction fetch, Store from the core.

The network tester (in src/cpu/testers/networktest/networktest.cc)
generates packets of the type **ReadReq**, **INST_FETCH**, and
**WriteReq**, which are converted into **RubyRequestType:LD**,
**RubyRequestType:IFETCH**, and **RubyRequestType:ST**, respectively, by
the RubyPort (in src/mem/ruby/system/RubyPort.hh/cc). These messages
reach the cache controller via the Sequencer. The destination for these
messages is determined by the traffic type, and embedded in the address.
More details can be found [here](/documentation/general_docs/debugging_and_testing/directed_testers/ruby_random_tester).

  - Main Operation:
      - The goal of the cache is only to act as a source node in the
        underlying interconnection network. It does not track any
        states.
      - On a **LD** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Control** (8 bytes) in the
            request vnet (0).
          - Note: vnet 0 could also be made to broadcast, instead of
            sending a directed message to a particular directory, by
            uncommenting the appropriate line in the *a_issueRequest*
            action in Network_test-cache.sm
      - On a **IFETCH** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Control** (8 bytes) in the
            forward vnet (1).
      - On a **ST** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Data** (72 bytes) in the
            response vnet (2).
      - Note: request, forward and response are just used to
        differentiate the vnets, but do not have any physical
        significance in this protocol.

### Directory controller

  - Requests, Responses, Triggers:
      - **MSG** from the cores

  - Main Operation:
      - The goal of the directory is only to act as a destination node
        in the underlying interconnection network. It does not track any
        states.
      - The directory simply pops its incoming queue upon receiving the
        message.

### Other features

   This protocol assumes only 3 vnets.
  - It should only be used when running [Garnet Synthetic
        Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic).


---


## "MESI two level"

*Source: https://www.gem5.org/documentation/general_docs/ruby/MESI_Two_Level/*

# MESI Two Level

### **Protocol Overview**

  - This protocol models **two-level cache hierarchy**. The L1 cache is
    private to a core, while the L2 cache is shared among the cores. L1
    Cache is split into Instruction and Data cache.
  - **Inclusion** is maintained between the L1 and L2 cache.
  - At high level the protocol has four stable states, **M**, **E**,
    **S** and **I**. A block in **M** state means the blocks is writable
    (i.e. has exclusive permission) and has been dirtied (i.e. its the
    only valid copy on-chip). **E** state represent a cache block with
    exclusive permission (i.e. writable) but is not written yet. **S**
    state means the cache block is only readable and possible multiple
    copies of it exists in multiple private cache and as well as in the
    shared cache. **I** means that the cache block is invalid.
  - The on-chip cache coherence is maintained through **Directory
    Coherence** scheme, where the directory information is co-located
    with the corresponding cache blocks in the shared L2 cache.
  - The protocol has four types of controllers -- **L1 cache controller,
    L2 cache controller, Directory controller** and **DMA controller**.
    L1 cache controller is responsible for managing L1 Instruction and
    L1 Data Cache. Number of instantiations of L1 cache controller is
    equal to the number of cores in the simulated system. L2 cache
    controller is responsible for managing the shared L2 cache and for
    maintaining coherence of on-chip data through directory coherence
    scheme. The Directory controller acts as interface to the Memory
    Controller/Off-chip main memory and is also responsible for coherence
    across multiple chips/and external coherence request from DMA
    controller. DMA controller is responsible for satisfying coherent
    DMA requests.
  - One of the primary optimizations in this protocol is that if a L1
    Cache request a data block even for read permission, the L2 cache
    controller if finds that no other core has the block, it returns the
    cache block with exclusive permission. This is an optimization done
    in anticipation that a cache blocks read would be written by the
    same core soon and thus save an extra request with this
    optimization. This is exactly why **E** state exists (i.e. when a
    cache block is writable but not yet written).
  - The protocol supports *silent eviction* of *clean* cache blocks from
    the private L1 caches. This means that cache blocks which have not
    been written to and has readable permission only can drop the cache
    block from the private L1 cache without informing the L2 cache. This
    optimization helps reducing write-back traffic to the L2 cache
    controller.

### **Related Files**

  - **src/mem/protocols**
      - **MESI_CMP_directory-L1cache.sm**: L1 cache controller
        specification
      - **MESI_CMP_directory-L2cache.sm**: L2 cache controller
        specification
      - **MESI_CMP_directory-dir.sm**: directory controller
        specification
      - **MESI_CMP_directory-dma.sm**: dma controller specification
      - **MESI_CMP_directory-msg.sm**: coherence message type
        specifications. This defines different field of different type
        of messages that would be used by the given protocol
      - **MESI_CMP_directory.slicc**: container file

### **Controller Description**

### **L1 cache
controller**

| States            | Invariants and Semantic/Purpose of the state                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M**             | The cache block is held in exclusive state by **only one L1 cache**. There are no sharers of this block. The data is potentially is the only valid copy in the system. The copy of the cache block is **writable** and as well as **readable**.                                                                                                                                                                                                                                                                                                                                                                                   |
| **E**             | The cache block is held with exclusive permission by exactly **only one L1 cache**. The difference with the **M** state is that the cache block is writable (and readable) but not yet written.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **S**             | The cache block is held in shared state by 1 or more L1 caches and/or by the L2 cache. The block is only **readable**. No cache can have the cache block with exclusive permission.                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **I / NP**        | The cache block is invalid.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **IS**            | Transient state. This means that **GETS (Read)** request has been issued for the cache block and awaiting for response. The cache block is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **IM**            | Transient state. This means that **GETX (Write)** request has been issued for the cache block and awaiting for response. The cache block is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **SM**            | Transient state. This means the cache block was originally in S state and then **UPGRADE (Write)** request was issued to get exclusive permission for the blocks and awaiting response. The cache block is **readable**.                                                                                                                                                                                                                                                                                                                                                                                                          |
| **IS_I**         | Transient state. This means that while in IS state the cache controller received Invalidation from the L2 Cache's directory. This happens due to race condition due to write to the same cache block by other core, while the given core was trying to get the same cache blocks for reading. The cache block is neither readable nor writable..                                                                                                                                                                                                                                                                                  |
| **M_I**          | Transient state. This state indicates that the cache is trying to replace a cache block in **M** state from its cache and the write-back (PUTX) to the L2 cache's directory has been issued but awaiting write-back acknowledgement.                                                                                                                                                                                                                                                                                                                                                                                              |
| **SINK_WB_ACK** | Transient state. This state is reached when waiting for write-back acknowledgement from the L2 cache's directory, the L1 cache received intervention (forwarded request from other cores). This indicates a race between the issued write-back to the directory and another request from the another cache has happened. This also indicates that the write-back has lost the race (i.e. before it reached the L2 cache's directory, another core's request has reached the L2). This state is essential to avoid possibility of complicated race condition that can happen if write-backs are silently dropped at the directory. |
|  |

### **L2 cache controller**

Recall that the on-chip directory is co-located with the corresponding
cache blocks in the L2 Cache. Thus following states in the L2 cache
block encodes the information about the status and permissions of the
cache blocks in the L2 cache as well as the coherence status of the
cache block that may be present in one or more private L1 caches. Beyond
the coherence states there are also two more important fields per cache
block that aids to make proper coherence actions. These fields are
**Sharers** field, which can be thought of as a bit-vector indicating
which of the private L1 caches potentially have the given cache block.
The other important field is the **Owner** field, which is the identity
of the private L1 cache in case the cache block is held with exclusive
permission in a L1
cache.

| States      | Invariants and Semantic/Purpose of the state                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NP**      | The cache blocks is not present in the on-chip cache hierarchy.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **SS**      | The cache block is present in potentially multiple private caches in only readable mode (i.e.in "S" state in private caches). Corresponding "Sharers" vector with the block should give the identity of the private caches which possibly have the cache block in its cache. The cache block in the L2 cache is valid and **readable**.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **M**       | The cache block is present ONLY in the L2 cache and has exclusive permission. L1 Cache's read/write requests (GETS/GETX) can be satisfied directly from the L2 cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **MT**      | The cache block is in ONE of the private L1 caches with exclusive permission. The data in the L2 cache is potentially stale. The identity of the L1 cache which has the block can be found in the "Owner" field associated with the cache block. Any request for read/write (GETS/GETX) from other cores/private L1 caches need to be forwarded to the owner of the cache block. L2 can not service requests itself.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **M_I**    | Its a transient state. This state indicates that the cache is trying to replace the cache block from its cache and the write-back (PUTX/PUTS) to the Directory controller (which act as interface to Main memory) has been issued but awaiting write-back acknowledgement. The data is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **MT_I**   | Its a transient state. This state indicates that the cache is trying to replace a cache block in **MT** state from its cache. Invalidation to the current owner (private L1 cache) of the cache block has been issued and awaiting write-back from the Owner L1 cache. Note that the this Invalidation (called back-invalidation) is instrumental in making sure that the inclusion is maintained between L1 and L2 caches. The data is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **MCT_I**  | Its a transient state.This state is same as **MT_I**, except that it is known that the data in the L2 cache is in *clean* state. The data is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **I_I**    | Its a transient state. The L2 cache is trying to replace a cache block in the **SS** state and the cache block in the L2 is in *clean* state. Invalidations has been sent to all potential sharers (L1 caches) of the cache block. The L2 cache's directory is waiting for all the required Acknowledgements to arrive from the L1 caches. Note that the this Invalidation (called back-invalidation) is instrumental in making sure that the inclusion is maintained between L1 and L2 caches. The data is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **S_I**    | Its a transient state.Same as **I_I**, except the data in L2 cache for the cache block is *dirty*. This means unlike in the case of **I_I**, the data needs to be sent to the Main memory. The cache block is neither readable nor writable..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **ISS**     | Its a transient state. L2 has received a **GETS (read)** request from one of the private L1 caches, for a cache block that it not present in the on-chip caches. A read request has been sent to the Main Memory (Directory controller) and waiting for the response from the memory. This state is reached only when the request is for data cache block (not instruction cache block). The purpose of this state is that if it is found that only one L1 cache has requested the cache block then the block is returned to the requester with exclusive permission (although it was requested for reading permission). The cache block is neither readable nor writable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **IS**      | Its a transient state. The state is similar to **ISS**, except the fact that if the requested cache block is Instruction cache block or more than one core request the same cache block while waiting for the response from the memory, this state is reached instead of **ISS**. Once the requested cache block arrives from the Main Memory, the block is sent to the requester(s) with read-only permission. The cache block is neither readable nor writable at this state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **IM**      | Its a transient state. This state is reached when a L1 GETX (write) request is received by the L2 cache for a cache blocks that is not present in the on-chip cache hierarchy. The request for the cache block in exclusive mode has been issued to the main memory but response is yet to arrive.The cache block is neither readable nor writable at this state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **SS_MB**  | Its a transient state. In general any state whose name ends with "B" (like this one) also means that it is a *blocking* coherence state. This means the directory awaiting for some response from the private L1 cache ans until it receives the desired response any other request is not entertained (i.e. request are effectively serialized). This particular state is reached when a L1 cache requests a cache block with exclusive permission (i.e. GETX or UPGRADE) and the coherence state of the cache blocks was in **SS** state. This means that the requested cache blocks potentially has readable copies in the private L1 caches. Thus before giving the exclusive permission to the requester, all the readable copies in the L1 caches need to be invalidated. This state indicate that the required invalidations has been sent to the potential sharers (L1 caches) and the requester has been informed about the required number of Invalidation Acknowledgement it needs before it can have the exclusive permission for the cache block. Once the requester L1 cache gets the required number of Invalidation Acknowledgement it informs the director about this by *UNBLOCK* message which allows the directory to move out of this blocking coherence state and thereafter it can resume entertaining other request for the given cache block. The cache block is neither readable nor writable at this state. |
| **MT_MB**  | Its a transient state and also a *blocking* state. This state is reached when L2 cache's directory has sent out a cache block with exclusive permission to a requester L1 cache but yet to receive *UNBLOCK* from the requester L1 cache acknowledging the receipt of exclusive permission. The cache block is neither readable nor writable at this state.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **MT_IIB** | Its a transient state and also a *blocking* state. This state is reached when a read request (GETS) request is received for a cache blocks which is currently held with exclusive permission in another private L1 cache (i.e. directory state is **MT**). On such requests the L2 cache's directory forwards the request to the current owner L1 cache and transitions to this state. Two events need to happen before this cache block can be unblocked (and thus start entertaining further request for this cache block). The current owner cache block need to send a write-back to the L2 cache to update the L2's copy with latest value. The requester L1 cache also needs to send *UNBLOCK* to the L2 cache indicating that it has got the requested cache block with desired coherence permissions. The cache block is neither readable nor writable at this state in the L2 cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **MT_IB**  | Its a transient state and also a *blocking* state. This state is reached when at **MT_IIB** state the L2 cache controller receives the *UNBLOCK* from the requester L1 cache but yet to receive the write-back from the previous owner L1 cache of the block. The cache block is neither readable nor writable at this state in the L2 cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **MT_SB**  | Its a transient state and also a *blocking* state. This state is reached when at **MT_IIB** state the L2 cache controller receives write-back from the previous owner L1 cache for the blocks, while yet to receive the *UNBLOCK* from the current requester for the cache block. The cache block is neither readable nor writable at this state in the L2 cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |


---


## "MI example"

*Source: https://www.gem5.org/documentation/general_docs/ruby/MI_example/*

# MI Example

### Protocol Overview

  - This is a simple cache coherence protocol that is used to illustrate
    protocol specification using SLICC.
  - This protocol assumes a 1-level cache hierarchy. The cache is
    private to each node. The caches are kept coherent by a directory
    controller. Since the hierarchy is only 1-level, there is no
    inclusion/exclusion requirement.
  - This protocol does not differentiate between loads and stores.
  - This protocol cannot implement the semantics of LL/SC instructions,
    because external GETS requests that hit a block within a LL/SC
    sequence steal exclusive permissions, thus causing the SC
    instruction to fail.

### Related Files

  - **src/mem/protocols**
      - **MI_example-cache.sm**: cache controller specification
      - **MI_example-dir.sm**: directory controller specification
      - **MI_example-dma.sm**: dma controller specification
      - **MI_example-msg.sm**: message type specification
      - **MI_example.slicc**: container file

### Stable States and Invariants

| States | Invariants                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------ |
| **M**  | The cache block has been accessed (read/written) by this node. No other node holds a copy of the cache block |
| **I**  | The cache block at this node is invalid                                                                      |

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

### Cache controller

  - Requests, Responses, Triggers:
      - Load, Instruction fetch, Store from the core
      - Replacement from self
      - Data from the directory controller
      - Forwarded request (intervention) from the directory controller
      - Writeback acknowledgement from the directory controller
      - Invalidations from directory controller (on dma activity)

![MI_example_cache_FSM.jpg](/assets/img/MI_example_cache_FSM.jpg
"MI_example_cache_FSM.jpg")

  - Main Operation:
      - On a **load/Instruction fetch/Store** request from the core:
          - it checks whether the corresponding block is present in the
            M state. If so, it returns a hit
          - otherwise, if in I state, it initiates a GETX request from
            the directory controller

     - On a **replacement** trigger from self:
          - it evicts the block, issues a writeback request to the
            directory controller
          - it waits for acknowledgement from the directory controller
            (to prevent races)

     - On a **forwarded request** from the directory controller:
          - This means that the block was in M state at this node when
            the request was generated by some other node
          - It sends the block directly to the requesting node
            (cache-to-cache transfer)
          - It evicts the block from this node

     - **Invalidations** are similar to replacements

### Directory controller

  - Requests, Responses, Triggers:
      - GETX from the cores, Forwarded GETX to the cores
      - Data from memory, Data to the cores
      - Writeback requests from the cores, Writeback acknowledgements to
        the cores
      - DMA read, write requests from the DMA controllers

![MI_example_dir_FSM.jpg](/assets/img/MI_example_dir_FSM.jpg
"MI_example_dir_FSM.jpg")

  - Main Operation:
      - The directory maintains track of which core has a block in the M
        state. It designates this core as owner of the block.
      - On a **GETX** request from a core:
          - If the block is not present, a memory fetch request is
            initiated
          - If the block is already present, then it means the request
            is generated from some other core
              - In this case, a forwarded request is sent to the
                original owner
              - Ownership of the block is transferred to the requestor
      - On a **writeback** request from a core:
          - If the core is owner, the data is written to memory and
            acknowledgement is sent back to the core
          - If the core is not owner, a NACK is sent back
              - This can happen in a race condition
              - The core evicted the block while a forwarded request
                some other core was on the way and the directory has
                already changed ownership for the core
              - The evicting core holds the data till the forwarded
                request arrives
      - On **DMA** accesses (read/write)
          - Invalidation is sent to the owner node (if any). Otherwise
            data is fetched from memory.
          - This ensures that the most recent data is available.

### Other features

  - MI protocols don't support LL/SC semantics. A load from a remote
        core will invalidate the cache block.
  - This protocol has no timeout mechanisms.


---


## "MOESI CMP directory"

*Source: https://www.gem5.org/documentation/general_docs/ruby/MOESI_CMP_directory/*

# MOESI CMP Directory

### Protocol Overview

  - TODO: cache hierarchy

<!-- end list -->

  - In contrast with the MESI protocol, the MOESI protocol introduces an
    additional **Owned** state.
  - The MOESI protocol also includes many coalescing optimizations not
    available in the MESI protocol.

### Related Files

  - **src/mem/protocols**
      - **MOESI_CMP_directory-L1cache.sm**: L1 cache controller
        specification
      - **MOESI_CMP_directory-L2cache.sm**: L2 cache controller
        specification
      - **MOESI_CMP_directory-dir.sm**: directory controller
        specification
      - **MOESI_CMP_directory-dma.sm**: dma controller specification
      - **MOESI_CMP_directory-msg.sm**: message type specification
      - **MOESI_CMP_directory.slicc**: container file

### L1 Cache Controller

#### **Stable States and Invariants**

| States    | Invariants                                                                                                                                                                                                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **MM**    | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state).                                                                                                                                                                                                                                            |
| **MM_W** | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state). Replacements and DMA accesses are not allowed in this state. The block automatically transitions to MM state after a timeout.                                                                                                              |
| **O**     | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                                                                                                                                                               |
| **M**     | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                                                                                                                                                           |
| **M_W**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Only loads and stores are allowed. Silent upgrade happens to MM_W state on store. Replacements and DMA accesses are not allowed in this state. The block automatically transitions to M state after a timeout. |
| **S**     | The cache block is held in shared state by 1 or more nodes. Stores are not allowed in this state.                                                                                                                                                                                                                                                            |
| **I**     | The cache block is invalid.                                                                                                                                                                                                                                                                                                                                  |

#### **FSM Abstraction**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_L1cache_FSM.jpg](/assets/img/MOESI_CMP_directory_L1cache_FSM.jpg
"MOESI_CMP_directory_L1cache_FSM.jpg")

#### **Optimizations**

| States | Description                                                                                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SM** | A GETX has been issued to get exclusive permissions for an impending store to the cache block, but an old copy of the block is still present. Stores and Replacements are not allowed in this state.                                     |
| **OM** | A GETX has been issued to get exclusive permissions for an impending store to the cache block, the data has been received, but all expected acknowledgments have not yet arrived. Stores and Replacements are not allowed in this state. |

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_L1cache_optim_FSM.jpg](/assets/img/MOESI_CMP_directory_L1cache_optim_FSM.jpg
"MOESI_CMP_directory_L1cache_optim_FSM.jpg")

### L2 Cache Controller

#### **Stable States and Invariants**

<table>
<thead>
<tr>
<th> Intra-chip Inclusion </th>
<th> Inter-chip Exclusion </th>
<th> States </th>
<th> Description
</th>
</tr>
</thead>
<tbody>
<tr>
<td> <b><span style="color:#808080">Not in any L1 or L2 at this chip</span></b> </td>
<td> <b>May be present at other chips</b> </td>
<td> <b>NP/I</b> </td>
<td> The cache block at this chip is invalid.
</td></tr>
<tr>
<td rowspan="6"> <b><span style="color:#00CC99">Not in L2, but in 1 or more L1s at this chip</span></b> </td>
<td rowspan="3"><b>May be present at other chips</b> </td>
<td> <b>ILS</b> </td>
<td> The cache block is not present at L2 on this chip. It is shared locally by L1 nodes in this chip.
</td></tr>
<tr>
<td> <b>ILO</b> </td>
<td> The cache block is not present at L2 on this chip. Some L1 node in this chip is an owner of this cache block.
</td></tr>
<tr>
<td> <b>ILOS</b> </td>
<td> The cache block is not present at L2 on this chip. Some L1 node in this chip is an owner of this cache block. There are also L1 sharers of this cache block in this chip.
</td></tr>
<tr>
<td rowspan="3"><b>Not present at any other chip</b> </td>
<td> <b>ILX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held in exclusive mode by some L1 node in this chip.
</td></tr>
<tr>
<td> <b>ILOX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held exclusively by this chip and some L1 node in this chip is an owner of the block.
</td></tr>
<tr>
<td> <b>ILOSX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held exclusively by this chip. Some L1 node in this chip is an owner of the block. There are also L1 sharers of this cache block in this chip.
</td></tr>
<tr>
<td rowspan="3"> <b><span style="color:#99CCFF">In L2, but not in any L1 at this chip</span></b> </td>
<td rowspan="2"><b>May be present at other chips</b> </td>
<td> <b>S</b> </td>
<td> The cache block is not present at L1 on this chip. It is held in shared mode at L2 on this chip and is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>O</b> </td>
<td> The cache block is not present at L1 on this chip. It is held in owned mode at L2 on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>Not present at any other chip</b> </td>
<td> <b>M</b> </td>
<td> The cache block is not present at L1 on this chip. It is present at L2 on this chip and is potentially modified.
</td></tr>
<tr>
<td rowspan="3"> <b><span style="color:#CC99FF">Both in L2, and 1 or more L1s at this chip</span></b> </td>
<td rowspan="2"><b>May be present at other chips</b> </td>
<td> <b>SLS</b> </td>
<td> The cache block is present at L2 in shared mode on this chip. There exists local L1 sharers of the block on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>OLS</b> </td>
<td> The cache block is present at L2 in owned mode on this chip. There exists local L1 sharers of the block on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>Not present at any other chip</b> </td>
<td> <b>OLSX</b> </td>
<td> The cache block is present at L2 in owned mode on this chip. There exists local L1 sharers of the block on this chip. It is held exclusively by this chip.
</td></tr>
</tbody>
</table>

#### **FSM Abstraction**

The controller is described in 2 parts. The first picture shows
transitions between all "intra-chip inclusion" categories and within
categories 1, 3, 4. Transitions within category 2 (Not in L2, but in 1
or more L1s at this chip) are shown in the second picture.

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink"). Transitions
involving other chips are annotated in
<span style="color:#CC3300">brown</span>.**

![MOESI_CMP_directory_L2cache_FSM_part_1.jpg](/assets/img/MOESI_CMP_directory_L2cache_FSM_part_1.jpg
"MOESI_CMP_directory_L2cache_FSM_part_1.jpg")

The second picture below expands the central hexagonal portion of the
above picture to show transitions within category 2 (Not in L2, but in 1
or more L1s at this chip).

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink"). Transitions
involving other chips are annotated in
<span style="color:#CC3300">brown</span>.**

![MOESI_CMP_directory_L2cache_FSM_part_2.jpg](/assets/img/MOESI_CMP_directory_L2cache_FSM_part_2.jpg
"MOESI_CMP_directory_L2cache_FSM_part_2.jpg")

### Directory Controller

#### **Stable States and
Invariants**

| States | Invariants                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M**  | The cache block is held in exclusive state by only 1 node (which is also the owner). There are no sharers of this block. The data is potentially different from that in memory. |
| **O**  | The cache block is owned by exactly 1 node. There may be sharers of this block. The data is potentially different from that in memory.                                          |
| **S**  | The cache block is held in shared state by 1 or more nodes. No node has ownership of the block. The data is consistent with that in memory (Check).                             |
| **I**  | The cache block is invalid.                                                                                                                                                     |

#### **FSM Abstraction**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_dir_FSM.jpg](/assets/img/MOESI_CMP_directory_dir_FSM.jpg
"MOESI_CMP_directory_dir_FSM.jpg")

### Other features

#### **Timeouts**:


---


## "MOESI CMP token"

*Source: https://www.gem5.org/documentation/general_docs/ruby/MOESI_CMP_token/*

# MOESI CMP token

### Protocol Overview

  - This protocol also models a 2-level cache hierarchy.
  - It maintains coherence permission by explicitly exchanging and
    counting tokens.
  - A fix number of token are assigned to each cache block in the
    beginning, the number of token remains unchanged.
  - To write a block, the processor must have all the token for that
    block. For reading at least one token is required.
  - The protocol also has a persistent message support to avoid
    starvation.

### Related Files

  - **src/mem/protocols**
      - **MOESI_CMP_token-L1cache.sm**: L1 cache controller
        specification
      - **MOESI_CMP_token-L2cache.sm**: L2 cache controller
        specification
      - **MOESI_CMP_token-dir.sm**: directory controller specification
      - **MOESI_CMP_token-dma.sm**: dma controller specification
      - **MOESI_CMP_token-msg.sm**: message type specification
      - **MOESI_CMP_token.slicc**: container file

### Controller Description

### **L1 Cache**

| States    | Invariants                                                                                                                                                                                                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **MM**    | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state).                                                                                                                                                                                                                                            |
| **MM_W** | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state). Replacements and DMA accesses are not allowed in this state. The block automatically transitions to MM state after a timeout.                                                                                                              |
| **O**     | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                                                                                                                                                               |
| **M**     | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                                                                                                                                                           |
| **M_W**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Only loads and stores are allowed. Silent upgrade happens to MM_W state on store. Replacements and DMA accesses are not allowed in this state. The block automatically transitions to M state after a timeout. |
| **S**     | The cache block is held in shared state by 1 or more nodes. Stores are not allowed in this state.                                                                                                                                                                                                                                                            |
| **I**     | The cache block is invalid.                                                                                                                                                                                                                                                                                                                                  |

### **L2 cache**

| States | Invariants                                                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NP** | The cache block is held exclusively by this node and is potentially locally modified (similar to conventional "M" state).                                                                                           |
| **O**  | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                      |
| **M**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                  |
| **S**  | The cache line holds the most recent, correct copy of the data. Other processors in the system may hold copies of the data in the shared state, as well. The cache line can be read, but not written in this state. |
| **I**  | The cache line is invalid and does not hold a valid copy of the data.                                                                                                                                               |

### **Directory controller**

| States | Invariants |
| ------ | ---------- |
| **O**  | Owner .    |
| **NO** | Not Owner. |
| **L**  | Locked.    |


---


## "MOESI hammer"

*Source: https://www.gem5.org/documentation/general_docs/ruby/MOESI_hammer/*

# MOESI Hammer

This is an implementation of AMD's Hammer protocol, which is used in
AMD's Hammer chip (also know as the Opteron or Athlon 64). The protocol
implements both the original a HyperTransport protocol, as well as the
more recent ProbeFilter protocol. The protocol also includes a full-bit
directory mode.

### Related Files

  - **src/mem/protocols**
      - **MOESI_hammer-cache.sm**: cache controller specification
      - **MOESI_hammer-dir.sm**: directory controller specification
      - **MOESI_hammer-dma.sm**: dma controller specification
      - **MOESI_hammer-msg.sm**: message type specification
      - **MOESI_hammer.slicc**: container file

### Cache Hierarchy

This protocol implements a 2-level private cache hierarchy. It assigns
separate Instruction and Data L1 caches, and a unified L2 cache to each
core. These caches are private to each core and are controlled with one
shared cache controller. This protocol enforce exclusion between L1 and
L2
caches.

### Stable States and Invariants

| States | Invariants                                                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MM** | The cache block is held exclusively by this node and is potentially locally modified (similar to conventional "M" state).                                                                                           |
| **O**  | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                      |
| **M**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                  |
| **S**  | The cache line holds the most recent, correct copy of the data. Other processors in the system may hold copies of the data in the shared state, as well. The cache line can be read, but not written in this state. |
| **I**  | The cache line is invalid and does not hold a valid copy of the data.                                                                                                                                               |

### Cache controller

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

MOESI_hammer supports cache flushing. To flush a cache line, the cache
controller first issues a GETF request to the directory to block the
line until the flushing is completed. It then issues a PUTF and writes
back the cache line.

![MOESI_hammer_cache_FSM.jpg](/assets/img/MOESI_hammer_cache_FSM.jpg
"MOESI_hammer_cache_FSM.jpg")

### Directory controller

MOESI_hammer memory module, unlike a typical directory protocol, does
not contain any directory state and instead broadcasts requests to all
the processors in the system. In parallel, it fetches the data from the
DRAM and forward the response to the requesters.

probe filter: TODO

#### **Stable States and Invariants**

| States | Invariants                                                           |
| ------ | -------------------------------------------------------------------- |
| **NX** | Not Owner, probe filter entry exists, block in O at Owner.           |
| **NO** | Not Owner, probe filter entry exists, block in E/M at Owner.         |
| **S**  | Data clean, probe filter entry exists pointing to the current owner. |
| **O**  | Data clean, probe filter entry exists.                               |
| **E**  | Exclusive Owner, no probe filter entry.                              |

#### **Controller**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_hammer_dir_FSM.jpg](/assets/img/MOESI_hammer_dir_FSM.jpg
"MOESI_hammer_dir_FSM.jpg")


---


## "Cache Coherence Protocols"

*Source: https://www.gem5.org/documentation/general_docs/ruby/cache-coherence-protocols/*

# Cache Coherence Protocols

## Common Notations and Data Structures

### **Coherence Messages**

These are described in the \<*protocol-name*\>-msg.sm file for each
protocol.

| Message           | Description                                                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ACK/NACK**      | positive/negative acknowledgement for requests that wait for the direction of resolution before deciding on the next action. Examples are writeback requests, exclusive requests.                                               |
| **GETS**          | request for shared permissions to satisfy a CPU's load or IFetch.                                                                                                                                                               |
| **GETX**          | request for exclusive access.                                                                                                                                                                                                   |
| **INV**           | invalidation request. This can be triggered by the coherence protocol itself, or by the next cache level/directory to enforce inclusion or to trigger a writeback for a DMA access so that the latest copy of data is obtained. |
| **PUTX**          | request for writeback of cache block. Some protocols (e.g. MOESI_CMP_directory) may use this only for writeback requests of exclusive data.                                                                                   |
| **PUTS**          | request for writeback of cache block in shared state.                                                                                                                                                                           |
| **PUTO**          | request for writeback of cache block in owned state.                                                                                                                                                                            |
| **PUTO_Sharers** | request for writeback of cache block in owned state but other sharers of the block exist.                                                                                                                                       |
| **UNBLOCK**       | message to unblock next cache level/directory for blocking protocols.                                                                                                                                                           |

### **AccessPermissions**

These are associated with each cache block and determine what operations
are permitted on that block. It is closely correlated with coherence
protocol
states.

| Permissions     | Description                                                                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Invalid**     | The cache block is invalid. The block must first be obtained (from elsewhere in the memory hierarchy) before loads/stores can be performed. No action on invalidates (except maybe sending an ACK). No action on replacements. The associated coherence protocol states are I or NP and are stable states in every protocol. |
| **Busy**        | TODO                                                                                                                                                                                                                                                                                                                         |
| **Read_Only**  | Only operations permitted are loads, writebacks, invalidates. Stores cannot be performed before transitioning to some other state.                                                                                                                                                                                           |
| **Read_Write** | Loads, stores, writebacks, invalidations are allowed. Usually indicates that the block is dirty.                                                                                                                                                                                                                             |

### Data Structures

  - **Message Buffers**:TODO
  - **TBE Table**: TODO
  - **Timer Table**: This maintains a map of address-based timers. For
    each target address, a timeout value can be associated and added to
    the Timer table. This data structure is used, for example, by the L1
    cache controller implementation of the MOESI_CMP_directory
    protocol to trigger separate timeouts for cache blocks. Internally,
    the Timer Table uses the event queue to schedule the timeouts. The
    TimerTable supports a polling-based interface, **isReady()** to
    check if a timeout has occurred. Timeouts on addresses can be set
    using the **set()** method and removed using the **unset()** method.

  - **Related Files**:
      - src/mem/ruby/system/TimerTable.hh: Declares the
                TimerTable class
      - src/mem/ruby/system/TimerTable.cc: Implementation of the
                methods of the TimerTable class, that deals with setting
                addresses & timeouts, scheduling events using the event
                queue.

### Coherence controller FSM Diagrams

  - The Finite State Machines show only the stable states
  - Transitions are annotated using the notation "**Event list**" or
    "**Event list : Action list**" or "**Event list : Action list :
    Event list**". For example, Store : GETX indicates that on a Store
    event, a GETX message was sent whereas GETX : Mem Read indicates
    that on receiving a GETX message, a memory read request was sent.
    Only the main triggers and actions are listed.
  - Optional actions (e.g. writebacks depending on whether or not the
    block is dirty) are enclosed within **\[ \]**
  - In the diagrams, the transition labels are associated with the arc
    that cuts across the transition label or the closest arc.


---


## "Garnet 2.0"

*Source: https://www.gem5.org/documentation/general_docs/ruby/garnet-2/*

**More details of the gem5 Ruby Interconnection Network are
[here](/documentation/general_docs/ruby/interconnection-network/).**

### Garnet2.0: An On-Chip Network Model for Heterogeneous SoCs

Garnet2.0 is a detailed interconnection network model inside gem5. It is
in active development, and patches with more features will be
periodically pushed into gem5. **Additional garnet-related patches and
tool support under development (not part of the repo) can be found at
the** [Garnet page at Georgia
Tech](http://synergy.ece.gatech.edu/tools/garnet).

Garnet2.0 builds upon the original Garnet model which was published in
[2009](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4919636%7CISPASS).

If your use of Garnet contributes to a published paper, please cite the
following paper:

```
    @inproceedings{garnet,
      title={GARNET: A detailed on-chip network model inside a full-system simulator},
      author={Agarwal, Niket and Krishna, Tushar and Peh, Li-Shiuan and Jha, Niraj K},
      booktitle={Performance Analysis of Systems and Software, 2009. ISPASS 2009. IEEE International Symposium on},
      pages={33--42},
      year={2009},
      organization={IEEE}
    }
```

Garnet2.0 provides a cycle-accurate micro-architectural implementation
of an on-chip network router. It leverages the [Topology](
/documentation/general_docs/ruby/interconnection-network#Topology) and [Routing](
/documentation/general_docs/ruby/interconnection-network#Routing) frastructure
provided by gem5's ruby memory system model. The default router is a
state-of-the-art 1-cycle pipeline. There is support to add additional
delay of any number of cycles in any router, by specifying it within the
topology.

Garnet2.0 can also be used to model an off-chip interconnection network
by setting appropriate delays in the routers and links.

- **Related Files**:
  - **src/mem/ruby/network/Network.py**
  - **src/mem/ruby/network/garnet2.0/GarnetNetwork.py**
  - **src/mem/ruby/network/Topology.cc**

## Invocation

The garnet networks can be enabled by adding **--network=garnet2.0**.

## Configuration

Garnet2.0 uses the generic network parameters in Network.py:

- **number_of_virtual_networks**: This is the maximum number of
  virtual networks. The actual number of active virtual networks
  is determined by the protocol.
- **control_msg_size**: The size of control messages in bytes.
  Default is 8. **m_data_msg_size** in Network.cc is set to the
  block size in bytes + control_msg_size.

Additional parameters are specified in garnet2.0/GarnetNetwork.py:

- **ni_flit_size**: flit size in bytes. Flits are the
  granularity at which information is sent from one router to the
  other. Default is 16 (=\> 128 bits). \[This default value of 16
  results in control messages fitting within 1 flit, and data
  messages fitting within 5 flits\]. Garnet requires the
  ni_flit_size to be the same as the bandwidth_factor (in
  network/BasicLink.py) as it does not model variable bandwidth
  within the network. This can also be set from the command line
  with **--link-width-bits**.
- **vcs_per_vnet**: number of virtual channels (VC) per virtual
  network. Default is 4. This can also be set from the command
  line with **--vcs-per-vnet**.
- **buffers_per_data_vc**: number of flit-buffers per VC in the
  data message class. Since data messages occupy 5 flits, this
  value can lie between 1-5. Default is 4.
- **buffers_per_ctrl_vc**: number of flit-buffers per VC in the
  control message class. Since control messages occupy 1 flit, and
  a VC can only hold one message at a time, this value has to be
  1. Default is 1.
- **routing_algorithm**: 0: Weight-based table (default), 1: XY,
  2: Custom. More details below.

## Topology

Garnet2.0 leverages the
[Topology](/documentation/general_docs/ruby/interconnection-network#Topology)
infrastructure
provided by gem5's ruby memory system model. Any heterogeneous topology
can be modeled. Each router in the topology file can be given an
independent latency, which overrides the default. In addition, each link
has 2 optional parameters: src_outport and dst_inport, which are
strings with names of the output and input ports of the source and
destination routers for each link. These can be used inside garnet2.0 to
implement custom routing algorithms, as described next. For instance, in
a Mesh, the west to east links have src_outport set to "west" and
dst_inport" set to "east".

- **Network Components**:
    - **GarnetNetwork**: This is the top level object that
      instantiates all network interfaces, routers, and links.
      Topology.cc calls the methods to add "external links" between
      NIs and routers, and "internal links" between routers.
    - **NetworkInterface**: Each NI connects to one coherence
      controller via MsgBuffer interfaces on one side. It has a link
      to a router on the other. Every protocol message is put into a
      one-flit control or multi (default=5)-flit data (depending on
      its vnet), and injected into the router. Multiple NIs can
      connect to the same router (for e.g., in the Mesh topology,
      cache and dir controllers connect via individual NIs to the same
      router).
    - **Router**: The router manages arbitration for output links, and
      flow control between routers.
    - **NetworkLink**: Network links carry flits. They can be of one
      of 3 types: EXT_OUT_ (router to NI), EXT_IN_ (NI to router),
      and INT_ (internal router to router)
    - **CreditLink**: Credit links carry VC/buffer credits between
      routers for flow control.

## Routing

Garnet2.0 leverages the
[Routing](/documentation/general_docs/ruby/interconnection-network#Routing) infrastructure
provided by gem5's ruby memory system model. The default routing
algorithm is a deterministic table-based routing algorithm with shortest
paths. Link weights can be used to prioritize certain links over others.
See src/mem/ruby/network/Topology.cc for details about how the routing
table is populated.

**Custom Routing**: To model custom routing algorithms, say adaptive, we
provide a framework to name each link with a src_outport and
dst_inport direction, and use these inside garnet to implement routing
algorithms. For instance, in a Mesh, West-first can be implemented by
sending a flit along the "west" outport link till the flit no longer has
any X- hops remaining, and then randomly (or based on next router VC
availability) choosing one of the remaining links. See how
outportComputeXY() is implemented in
src/mem/ruby/network/garnet2.0/RoutingUnit.cc. Similarly,
outportComputeCustom() can be implemented, and invoked by adding
--routing-algorithm=2 in the command line.

**Multicast messages**: The network modeled does not have hardware
multi-cast support within the network. A multi-cast message gets broken
into multiple uni-cast messages at the Network Interface.

## Flow Control

Virtual Channel Flow Control is used in the design. Each VC can hold one
packet. There are two kinds of VCs in the design - control and data. The
buffer depth in each can be independently controlled from
GarnetNetwork.py. The default values are 1-flit deep control VCs, and
4-flit deep data VCs. Default size of control packets is 1-flit, and
data packets is 5-flit.

## Router Microarchitecture

The garnet2.0 router performs the following actions:

1.  **Buffer Write (BW)**: The incoming flit gets buffered in its VC.
2.  **Route Compute (RC)** The buffered flit computes its output port,
    and this information is stored in its VC.
3.  **Switch Allocation (SA)**: All buffered flits try to reserve the
    switch ports for the next cycle. \[The allocation occurs in a
    *separable* manner: First, each input chooses one input VC, using
    input arbiters, which places a switch request. Then, each output
    port breaks conflicts via output arbiters\]. All arbiters in ordered
    virtual networks are *queueing* to maintain point-to-point ordering.
    All other arbiters are *round-robin*.
4.  **VC Selection (VS)**: The winner of SA selects a free VC (if
    HEAD/HEAD_TAIL flit) from its output port.
5.  **Switch Traversal (ST)**: Flits that won SA traverse the crossbar
    switch.
6.  **Link Traversal (LT)**: Flits from the crossbar traverse links to
    reach the next routers.

In the default design, BW, RC, SA, VS, and ST all happen in 1-cycle. LT
happens in the next cycle.

**Multi-cycle Router**: Multi-cycle routers can be modeled by specifying
a per-router latency in the topology file, or changing the default
router latency in src/mem/ruby/network/BasicRouter.py. This is
implemented by making a buffered flit wait in the router for (latency-1)
cycles before becoming eligible for SA.

## Buffer Management

Each router input port has number_of_virtual_networks Vnets, each
with vcs_per_vnet VCs. VCs in control Vnets have a depth of
buffers_per_ctrl_vc (default = 1) and VCs in data Vnets have a depth
of buffers_per_data_vc (default = 4). **Credits are used to relay
information about free VCs, and number of buffers within each VC.**

## Lifecycle of a Network Traversal

  - NetworkInterface.cc::wakeup()
      - Every NI connected to one coherence protocol controller on one
        end, and one router on the other.
      - receives messages from coherence protocol buffer in appropriate
        vnet and converts them into network packets and sends them into
        the network.
          - garnet2.0 adds the ability to capture a network trace at
            this point \[under development\].
      - receives flits from the network, extracts the protocol message
        and sends it to the coherence protocol buffer in appropriate
        vnet.
      - manages flow-control (i.e., credits) with its attached router.
      - The consuming flit/credit output link of the NI is put in the
        global event queue with a timestamp set to next cycle. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - NetworkLink.cc::wakeup()
      - receives flits from NI/router and sends it to NI/router after
        m_latency cycles delay
      - Default latency value for every link can be set from command
        line (see configs/network/Network.py)
      - Per link latency can be overwritten in the topology file
      - The consumer of the link (NI/router) is put in the global event
        queue with a timestamp set after m_latency cycles. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - Router.cc::wakeup()
      - Loop through all InputUnits and call their wakeup()
      - Loop through all OutputUnits and call their wakeup()
      - Call SwitchAllocator's wakeup()
      - Call CrossbarSwitch's wakeup()
      - The router's wakeup function is called whenever any of its
        modules (InputUnit, OutputUnit, SwitchAllocator, CrossbarSwitch)
        have a ready flit/credit to act upon this cycle.

<!-- end list -->

  - InputUnit.cc::wakeup()
      - Read input flit from upstream router if it is ready for this
        cycle
      - For HEAD/HEAD_TAIL flits, perform route computation, and update
        route in the VC.
      - Buffer the flit for (m_latency - 1) cycles and mark it valid
        for SwitchAllocation starting that cycle.
          - Default latency for every router can be set from command
            line (see configs/network/Network.py)
          - Per router latency (i.e., num pipeline stages) can be set in
            the topology file.

<!-- end list -->

  - OutputUnit.cc::wakeup()
      - Read input credit from downstream router if it is ready for this
        cycle
      - Increment the credit in the appropriate output VC state.
      - Mark output VC as free if the credit carries is_free_signal as
        true

<!-- end list -->

  - SwitchAllocator.cc::wakeup()
      - Note: SwitchAllocator performs VC arbitration and selection
        within it.
      - SA-I (or SA-i): Loop through all input VCs at every input port,
        and select one in a round robin manner.
          - For HEAD/HEAD_TAIL flits only select an input VC whose
            output port has at least one free output VC.
          - For BODY/TAIL flits, only select an input VC that has
            credits in its output VC.
      - Place a request for the output port from this VC.
      - SA-II (or SA-o): Loop through all output ports, and select one
        input VC (that placed a request during SA-I) as the winner for
        this output port in a round robin manner.
          - For HEAD/HEAD_TAIL flits, perform outvc allocation (i.e.,
            select a free VC from the output port.
          - For BODY/TAIL flits, decrement a credit in the output vc.
      - Read the flit out from the input VC, and send it to the
        CrossbarSwitch
      - Send a increment_credit signal to the upstream router for this
        input VC.
          - for HEAD_TAIL/TAIL flits, mark is_free_signal as true in
            the credit.
          - The input unit sends the credit out on the credit link to
            the upstream router.
      - Reschedule the Router to wakeup next cycle for any flits ready
        for SA next cycle.

<!-- end list -->

  - CrossbarSwitch.cc::wakeup()
      - Loop through all input ports, and send the winning flit out of
        its output port onto the output link.
      - The consuming flit output link of the router is put in the
        global event queue with a timestamp set to next cycle. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - NetworkLink.cc::wakeup()
      - receives flits from NI/router and sends it to NI/router after
        m_latency cycles delay
      - Default latency value for every link can be set from command
        line (see configs/network/Network.py)
      - Per link latency can be overwritten in the topology file
      - The consumer of the link (NI/router) is put in the global event
        queue with a timestamp set after m_latency cycles. The
        eventqueue calls the wakeup function in the consumer.

## Running Garnet2.0 with Synthetic Traffic

Garnet2.0 can be run in a standalone manner and fed with synthetic
traffic. The details are described here: **[Garnet Synthetic
Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)**


---


## "Garnet Synthetic Traffic"

*Source: https://www.gem5.org/documentation/general_docs/ruby/garnet_synthetic_traffic/*

# Garnet Synthetic Traffic

The Garnet Synthetic Traffic provides a framework for simulating the [Garnet network](/documentation/general_docs/ruby/garnet-2) with controlled inputs. This is useful for network testing/debugging, or for network-only simulations with synthetic traffic.

**Note: The garnet synthetic traffic injector only works with the [Garnet_standalone](/documentation/general_docs/ruby/Garnet_standalone.md) coherence protocol.**

## Related files

* configs/example/garnet_synth_traffic.py: file to invoke the network tester
* src/cpu/testers/garnet_synthetic_traffic: files implementing the tester.
  * GarnetSyntheticTraffic.py
  * GarnetSyntheticTraffic.hh
  * GarnetSyntheticTraffic.cc

## How to run

First build gem5 with the [Garnet_standalone](/documentation/general_docs/ruby/Garnet_standalone.md) coherence protocol. The Garnet_standalone protocol is ISA-agnostic, and hence we build it with the NULL ISA.

For gem5 <= 23.0:

```
scons build/NULL/gem5.debug PROTOCOL=Garnet_standalone
```

For gem5 >= 23.1

```
scons defconfig build/NULL build_opts/NULL
scons setconfig build/NULL RUBY_PROTOCOL_GARNET_STANDALONE=y
scons build/NULL/gem5.debug
```

Example command:

```
./build/NULL/gem5.debug configs/example/garnet_synth_traffic.py  \
        --num-cpus=16 \
        --num-dirs=16 \
        --network=garnet \
        --topology=Mesh_XY \
        --mesh-rows=4  \
        --sim-cycles=1000 \
        --synthetic=uniform_random \
        --injectionrate=0.01
```

## Parameterized Options

| **System Configuration** |  **Description**  |
|------------|-----------|
 | **--num-cpus** | Number of cpus. This is the number of source (injection) nodes in the network. |
 | **--num-dirs** | Number of directories. This is the number of destination (ejection) nodes in the network. |
 | **--network** | Network model: simple or garnet. Use garnet for running synthetic traffic. |
 | **--topology** | Topology for connecting the cpus and dirs to the network routers/switches. More detail about different topologies can be found (here)[Interconnection_Network#Topology]. |
 | **--mesh-rows** | The number of rows in the mesh. Only valid when ''--topology'' is ''Mesh_*'' or ''MeshDirCorners_*''. |



 | **Network Configuration** | **Description** |
 |------------|-----------|
 | **--router-latency** | Default number of pipeline stages in the garnet router. Has to be >= 1.  Can be over-ridden on a per router basis in the topology file. |
 | **--link-latency** | Default latency of each link in the network. Has to be >= 1.  Can be over-ridden on a per link basis in the topology file. |
 | **--vcs-per-vnet** | Number of VCs per Virtual Network. |
 | **--link-width-bits** | Width in bits for all links inside the garnet network. Default = 128. |



 | **Traffic Injection** | **Description** |
 |------------|-----------|
 | **--sim-cycles** | Total number of cycles for which the simulation should run. |
 | **--synthetic** | The type of synthetic traffic to be injected. The following synthetic traffic patterns are currently supported: 'uniform_random', 'tornado', 'bit_complement', 'bit_reverse', 'bit_rotation', 'neighbor', 'shuffle',  and 'transpose'. |
 | **--injectionrate** | Traffic Injection Rate in packets/node/cycle. It can take any decimal value between 0 and 1. The number of digits of precision after the decimal point can be controlled by ''--precision'' which is set to 3 as default in ''garnet_synth_traffic.py''. |
 | **--single-sender-id** | Only inject from this sender. To send from all nodes, set to -1. |
 | **--single-dest-id** | Only send to this destination. To send to all destinations as specified by the synthetic traffic pattern, set to -1. |
 | **--num-packets-max** | Maximum number of packets to be injected by each cpu node. Default value is -1 (keep injecting till sim-cycles). |
 | **--inj-vnet** | Only inject in this vnet (0, 1 or 2). 0 and 1 are 1-flit, 2 is 5-flit. Set to -1 to inject randomly in all vnets. |


## Implementation of Garnet synthetic traffic
The synthetic traffic injector is implemented in GarnetSyntheticTraffic.cc. The sequence of steps involved in generating and sending a packet are as follows.

* Every cycle, each cpu performs a bernouli trial with probability equal to --injectionrate to determine whether to generate a packet or not.
* If --num-packets-max is non negative, each cpu stops generating new packets after generating --num-packets-max number of packets. The injector terminates after --sim-cycles.
* If the cpu has to generate a new packet, it computes the destination for the new packet based on the synthetic traffic type (--synthetic).
* This destination is embedded into the bits after block offset in the packet address.
* The generated packet is randomly tagged as a ReadReq, or an INST_FETCH, or a WriteReq, and sent to the Ruby Port (src/mem/ruby/system/RubyPort.hh/cc).
* The Ruby Port converts the packet into a RubyRequestType:LD, RubyRequestType:IFETCH, and RubyRequestType:ST, respectively, and sends it to the Sequencer, which in turn sends it to the Garnet_standalone cache controller.
* The cache controller extracts the destination directory from the packet address.
* The cache controller injects the LD, IFETCH and ST into virtual networks 0, 1 and 2 respectively.
  * LD and IFETCH are injected as control packets (8 bytes), while ST is injected as a data packet (72 bytes).
* The packet traverses the network and reaches the directory.
* The directory controller simply drops it.


---


## "HeteroGarnet (Garnet 3.0)"

*Source: https://www.gem5.org/documentation/general_docs/ruby/heterogarnet/*

**More details of the gem5 Ruby Interconnection Network are [here](/documentation/general_docs/ruby/interconnection-network "wikilink").**
**Details about the earlier Garnet version can be found [here](/documentation/general_docs/ruby/garnet-2 "wikilink").**

### HeteroGarnet: A Detailed Simulator for Diverse Interconnect Systems
[HeteroGarnet](https://doi.org/10.1109/DAC18072.2020.9218539) improves upon the widely-popular Garnet 2.0 network model by enabling accurate simulation of emerging interconnect systems. Specifically, HeteroGarnet adds support for clock-domain islands, network crossings supporting multiple frequency domains, and network interface controllers capable of attaching to multiple physical links. It also supports variable bandwidth links and routers by introducing a new configurable Serializer-Deserializer component. HeteroGarnet is integrated into the gem5 repository as Garnet 3.0.

HeteroGarnet builds upon the original Garnet model which was published in
[2009](https://doi.org/10.1109/ISPASS.2009.4919636).

If your use of HeteroGarnet contributes to a published paper, please cite the
following paper:

```
    @inproceedings{heterogarnet,
        author={Bharadwaj, Srikant and Yin, Jieming and Beckmann, Bradford and Krishna, Tushar},
        booktitle={2020 57th ACM/IEEE Design Automation Conference (DAC)},
        title={Kite: A Family of Heterogeneous Interposer Topologies Enabled via Accurate Interconnect Modeling},
        year={2020},
        volume={},
        number={},
        pages={1-6},
        doi={10.1109/DAC18072.2020.9218539}
	}
```



## Topology Construction
HeteroGarnet allows users to configure complex topologies using a python configuration file as the topology.
The overall topology configuration could include the complete interconnect definition of the system including
any heterogeneous components. The general flow of defining a topology involves the following steps:

1. Determine the total number of routers in the system and instantiate them.
    1. Use the **Router** class to instantiate individual routers.
    2. Configure properties of each router, such as clock domain, supported flit width, depending on the requirements.
```
routers = Router(id, latency, clock_domain,
                flit_width, supported_vnets,
                vcs_per_vnet)
```

2. Connect the routers which connect to the end points (e.g, Cores, Caches, Directories) using external physical interconnects.
    1. Use **ExternalLink** class to instantiate the links connecting the end points.
    2. Configure properties of each external link, such as clock domain, link width, depending on the requirements.
    3. Enable clock-domain crossings(CDC) and Serializer-Deserializer(SerDes) units at either depending on the interconnect topology.
```
external_link = ExternalLink(id, latency, clock_domain,
                             flit_width, supported_vnets,
                             serdes_enable, cdc_enable)
````

3. Connect the individual routers within the network depending upon the topology.
    1. Use **InternalLink** class to instantiate the links connecting the end points.
    2. Configure properties of each internal link, such as clock domain, link width, depending on the requirements.
    3. Enable clock-domain crossings and Serializer-Deserializer units at either depending on the interconnect topology.
```
internal_link = InternalLink(id, latency, clock_domain,
                             flit_width, supported_vnets,
                             serdes_enable, cdc_enable)
```

Garnet 3.0 also provides several pre-configuration scripts(./configs/Network/Network.py) which automatically do some of the other steps, such as instantiating network interfaces, domain crossings, and SerDes units. The several types of units used to configure the topologies are discussed below.


## Physical Links
The physical link model in Garnet represents the interconnect wire itself. A link is a single entity which has its own latency, width and the types of flit it can transmit. The links also support a credit based back-pressuring mechanism. Similar to the upgraded Garnet 3.0 router, each Garnet 3.0 link can be configured to an operating frequency and width using appropriate parameters. This allows links and routers operating at different frequencies to be connected to each other.

## Network Interface
The network interface controller (NIC) is an object which sits between the network end points (e.g., Caches, DMA nodes) and the interconnection system. The NIC receives messages form the controllers and converts them into fixed-length flits, short for flow control units. These flits are sized appropriately according to the outgoing physical links. The network interface also governs the flow control and buffer management for the outgoing and incoming flits. Garnet 3.0 allows multiple ports to be attached to a single end points. Thus, the NIC decides where a certain message/flit must be scheduled.

## Clock Domain Crossing Units
To support multiple clock domains, Garnet 3.0 introduces Clock Domain Crossing (CDC) unit, as shown in the Figure below (left), which consists of first-In-First-Out (FIFO) buffers and can be instantiated anywhere within the network model. The CDC unit enables architectures with different clock domains across the system. The delay of each CDC unit configurable. The latency can also be calculated dynamically depending on the clock domains connected to it. This enables accurate modeling of DVFS techniques as CDC latencies are generally a function of the operating frequency of producer and consumer.

## Serializer-Deserializer Units
Another critical feature necessary in modeling SoCs and heterogeneous architectures is supporting various interconnect widths across the system. Consider a link between two routers within a GPU and a link between a memory controller and on-chip memory. These two links might be of different widths. To enable such configuration, Garnet 3.0 introduces the Serializer-Deserializer unit as shown in the figure below, which converts flits into appropriate widths at bit-width boundaries. These SerDes units can be instantiated anywhere in the Garnet 3.0 topology similar to the CDC unit described in the previous sub-section.

![SerDes_CDC.png](/assets/img/SerDes_CDC.png)

## Routing
The routing algorithm decides how the flits travel through the topology. The objective of a routing policy is to minimize contention while maximizing the bandwidth offered by the interconnect. Garnet 3.0 provides several standard routing policies that the user can select from.

### Routing Policies.
There are several generic routing  policies that have been proposed for deadlock free routing of flits through the interconnect network.

### Table based routing
Garnet also features table based routing policy which users can select to set custom routing policies using a weight-age based system. Lower weighted links are preferred over links which are configured to have higher weights.



## Flow Control and Buffer Management

Flow control mechanisms determine the buffer allocation in interconnect systems. The aim of a good flow control system is minimize the impact of buffer allocation to the overall latency of a message in the system. Implementation of these mechanisms often involve micro-management of physical packets within the interconnect system.

Coherence messages generated by cache controllers are often broken down into fixed-length flits (flow control units). A set of flits carrying a message is often termed as a packet. A packet could have a head-flit, body-flit, and a tail-flit to carry the contents of the message along with any additional meta data of the packet itself. Several flow control techniques have been proposed and implemented at various granularities of resource allocation.

Garnet 3.0 implements a credit-based flit-level flow control mechanism with support for virtual channels.

### Virtual Channels
Virtual Channels (VCs) in a network act as separate queues which can share physical wires (physical links) between two routers or arbiters. Virtual channels are mainly used to alleviate head-of-line blocking. However, they are also used as a means for deadlock-avoidance.

### Buffer Backpressure
Most implementations of interconnection networks do not tolerate dropping of packets or flits during traversal. Thus, there is a need to strictly manage the flits using backpressuring mechanisms. 

### Credit-based backpressuring
Credit-based backpressuring mechanism is often used for low-latency implementation of flit-stalling. Credits track the number of buffers available at the next intermediate destination by decrementing the overall buffers every time a flit is sent. A credit is then sent back by the destination when it is vacated.

Routers in interconnect systems perform arbitration, allocation of buffers, and flow control within the network. The objective of the router microarchitecture is to minimize the contention within the router while offering minimal per-hop latency for the flits. The complexity of the router microarchitecture also affects the overall energy and area consumption of the interconnect system.


## Life of a Message in Garnet 3.0
In this section we describe the life of a message in the NoC after it is generated by a cache controller unit. We take the case of Garnet 3.0 for describing the process, but the general modeling principles can be extended to other software simulation/modeling tools as well.

![HeteroGarnet_Life.png](/assets/img/HeteroGarnet_Life.png)

The overall flow of the system is shown in detail in figure above. It shows a simple example scenario where a message is generated by a cache controller destined for another cache controller which is connected through routers via physical links, serializer-deserializer units, and clock-domain crossings.

### Injection of Message
The source cache controller creates a message and assigns one or more  cache controllers as the destination. This message is then injected into message queues. A cache controller often has several outgoing and incoming message buffers for different kinds of messages.

### Conversion to Flits.
A network interface controller unit (NIC) is attached to each cache controller. This NIC wakes up and consumes the messages from the message queues. Each message is then converted to unicast messages before being broken down into fixed-length flits according to the size supported by the outgoing physical links. These flits are then scheduled for transmission depending on the availability of buffers at the next hop through one of the output links. The outgoing link is chosen depending on the destination, routing policy, and the type of message.

### Transmission to Local Router.
Each network interface is connected to one or more "local" routers which is could be connected through an "External" link. Once a flit is scheduled, it is transmitted over these external links which deliver the flit to the router after a period of defined latency.

### Router Arbitration.
The flit wakes up the router which is a multi-stage unit. The router houses the input buffers, VC allocation, switch arbitration, and crossbar units. On arrival the flit is first placed in a input buffer queue. There are several input buffer queues in a router which contend for an output link and a VC for the next hop. This is done using the VC allocation and switch arbitration stages. Once a flit is selected for transmission, the crossbar stage directs the flit to the output link. A credit is then sent back to the NIC as the input buffer space is vacated for the next flit to arrive.

### Serialization-Deserialization.
The serialization-deserialization (SerDes) is an optional unit that can be enabled depending on the design requirements. The SerDes units consumes the flits and appropriately converts it into outgoing flit size. In addition to manipulating the data packets, the SerDes also handles the credit system, by serializing or deserializing the credit units.


## Area, Power and Energy Model
Frameworks like Orion2.0 and DSENT provide models for the area and power for the various building blocks of a NoC router and links. HeteroGarnet integrates DSENT as an external tool to report area, power and energy (which depends on activity) at the end of the simulation.


---


## "Interconnection network"

*Source: https://www.gem5.org/documentation/general_docs/ruby/interconnection-network/*

# Interconnection Network

The various components of the interconnection network model inside
gem5's ruby memory system are described here.

## How to invoke the network

**Simple Network**:

```
./build/<ISA>/gem5.debug \
                      configs/example/ruby_random_test.py \
                      --num-cpus=16  \
                      --num-dirs=16  \
                      --network=simple
                      --topology=Mesh_XY  \
                      --mesh-rows=4
```

The default network is simple, and the default topology is crossbar.

**Garnet network**:

```
./build/<ISA>/gem5.debug \
                      configs/example/ruby_random_test.py  \
                      --num-cpus=16 \
                      --num-dirs=16  \
                      --network=garnet2.0 \
                      --topology=Mesh_XY \
                      --mesh-rows=4
```

## Topology

The connection between the various controllers are specified via python
files. All external links (between the controllers and routers) are
bi-directional. All internal links (between routers) are uni-directional
-- this allows a per-direction weight on each link to bias routing
decisions.

- **Related Files**:
    - **src/mem/ruby/network/topologies/Crossbar.py**
    - **src/mem/ruby/network/topologies/CrossbarGarnet.py**
    - **src/mem/ruby/network/topologies/Mesh_XY.py**
    - **src/mem/ruby/network/topologies/Mesh_westfirst.py**
    - **src/mem/ruby/network/topologies/MeshDirCorners_XY.py**
    - **src/mem/ruby/network/topologies/Pt2Pt.py**
    - **src/mem/ruby/network/Network.py**
    - **src/mem/ruby/network/BasicLink.py**
    - **src/mem/ruby/network/BasicRouter.py**



- **Topology Descriptions**:
  - **Crossbar**: Each controller (L1/L2/Directory) is connected to
    a simple switch. Each switch is connected to a central switch
    (modeling the crossbar). This can be invoked from command line
    by **--topology=Crossbar**.
  - **CrossbarGarnet**: Each controller (L1/L2/Directory) is
    connected to every other controller via one garnet router (which
    internally models the crossbar and allocator). This can be
    invoked from command line by **--topology=CrossbarGarnet**.
  - **Mesh_\***: This topology requires the number of directories
    to be equal to the number of cpus. The number of
    routers/switches is equal to the number of cpus in the system.
    Each router/switch is connected to one L1, one L2 (if present),
    and one Directory. The number of rows in the mesh **has to be
    specified** by **--mesh-rows**. This parameter enables the
    creation of non-symmetrical meshes too.
      - **Mesh_XY**: Mesh with XY routing. All x-directional links
        are biased with a weight of 1, while all y-directional links
        are biased with a weight of 2. This forces all messages to
        use X-links first, before using Y-links. It can be invoked
        from command line by **--topology=Mesh_XY**
      - **Mesh_westfirst**: Mesh with west-first routing. All
        west-directional links are biased with a weight of 1, al
        other links are biased with a weight of 2. This forces all
        messages to use west-directional links first, before using
        other links. It can be invoked from command line by
        **--topology=Mesh_westfirst**
  - **MeshDirCorners_XY**: This topology requires the number of
    directories to be equal to 4. number of routers/switches is
    equal to the number of cpus in the system. Each router/switch is
    connected to one L1, one L2 (if present). Each corner
    router/switch is connected to one Directory. It can be invoked
    from command line by **--topology=MeshDirCorners_XY**. The
    number of rows in the mesh **has to be specified** by
    **--mesh-rows**. The XY routing algorithm is used.
  - **Pt2Pt**: Each controller (L1/L2/Directory) is connected to
    every other controller via a direct link. This can be invoked
    from command line by
  - **Pt2Pt**: All to all point-to-point connection

![](http://pwp.gatech.edu/ece-synergy/wp-content/uploads/sites/332/2016/10/topologies.jpg)

**In each topology, each link and each router can independently be
passed a parameter that overrides the defaults (in BasicLink.py and
BasicRouter.py)**:

  - **Link Parameters:**
      - **latency**: latency of traversal within the link.
      - **weight**: weight associated with this link. This parameter is
        used by the routing table while deciding routes, as explained
        next in [Routing](Interconnection_Network#Routing "wikilink").
      - **bandwidth_factor**: Only used by simple network to specify
        width of the link in bytes. This translates to a bandwidth
        multiplier (simple/SimpleLink.cc) and the individual link
        bandwidth becomes bandwidth multiplier x endpoint_bandwidth
        (specified in SimpleNetwork.py). In garnet, the bandwidth is
        specified by ni_flit_size in GarnetNetwork.py)


  - **Internal Link Parameters:**
      - **src_outport**: String with name for output port from source
        router.
      - **dst_inport**: String with name for input port at destination
        router.

These two parameters can be used by routers to implement custom routing
algorithms in garnet2.0

  - **Router Parameters:**
      - **latency**: latency of each router. Only supported by
        garnet2.0.

## Routing

**Table-based Routing (Default):** Based on the topology, shortest
path graph traversals are used to populate *routing tables* at each
router/switch. This is done in src/mem/ruby/network/Topology.cc The
default routing algorithm is table-based and tries to choose the route
with minimum number of link traversals. Links can be given weights in
the topology files to model different routing algorithms. For example,
in Mesh_XY.py and MeshDirCorners_XY.py Y-direction links are given
weights of 2, while X-direction links are given weights of 1, resulting
in XY traversals. In Mesh_westfirst.py, the west-links are given
weights of 1, and all other links are given weights of 2. In garnet2.0,
the routing algorithm randomly chooses between links with equal weights.
In simple network, it statically chooses between links with equal
weights.

**Custom Routing algorithms:** In garnet2.0, we provide additional
support to implement custom (including adaptive) routing algorithms (See
outportComputeXY() in src/mem/ruby/network/garnet2.0/RoutingUnit.cc).
The src_outport and dst_inport fields of the links can be used to give
custom names to each link (e.g., directions if a mesh), and these can be
used inside garnet to implement any routing algorithm. A custom routing
algorithm can be selected from the command line by setting
--routing-algorithm=2. See configs/network/Network.py and
src/mem/ruby/network/garnet2.0/GarnetNetwork.py

## Flow-Control and Router Microarchitecture

Ruby supports two network models, Simple and Garnet, which trade-off
detailed modeling versus simulation speed respectively.

### Simple Network

The default network model in Ruby is the simple network.

- **Related Files**:
    - **src/mem/ruby/network/Network.py**
    - **src/mem/ruby/network/simple**
    - **src/mem/ruby/network/simple/SimpleNetwork.py**

## Configuration

Simple network uses the generic network parameters in Network.py:

- **number_of_virtual_networks**: This is the maximum number of
      virtual networks. The actual number of active virtual networks
      is determined by the protocol.
- **control_msg_size**: The size of control messages in bytes.
      Default is 8. **m_data_msg_size** in Network.cc is set to the
      block size in bytes + control_msg_size.

Additional parameters are specified in simple/SimpleNetwork.py:

- **buffer_size**: Size of buffers at each switch input and
  output ports. A value of 0 implies infinite buffering.
- **endpoint_bandwidth**: Bandwidth at the end points of the
  network in 1000th of byte.
- **adaptive_routing**: This enables adaptive routing based on
  occupancy of output buffers.

## Switch Model

The simple network models hop-by-hop network traversal, but abstracts
out detailed modeling within the switches. The switches are modeled in
simple/PerfectSwitch.cc while the links are modeled in
simple/Throttle.cc. The flow-control is implemented by monitoring the
available buffers and available bandwidth in output links before
sending.

![Simple_network.jpg](/assets/img/Simple_network.jpg "Simple_network.jpg")


### Garnet2.0

Details of the new (2016) Garnet2.0 network are
**[here](garnet-2)**.

## Running the Network with Synthetic Traffic

The interconnection networks can be run in a standalone manner and fed
with synthetic traffic. We recommend doing this with garnet2.0.

**[Running Garnet Standalone with Synthetic Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)**


---


## "SLICC"

*Source: https://www.gem5.org/documentation/general_docs/ruby/slicc/*

# SLICC

SLICC is a domain specific language for specifying cache coherence
protocols. The SLICC compiler generates C++ code for different
controllers, which can work in tandem with other parts of Ruby. The
compiler also generates an HTML specification of the protocol. HTML
generation is turned off by default. To enable HTML output, pass the
option "SLICC_HTML=True" to scons when compiling.

### Input To the Compiler

The SLICC compiler takes, as input, files that specify the controllers
involved in the protocol. The .slicc file specifies the different files
used by the particular protocol under consideration. For example, if
trying to specify the MI protocol using SLICC, then we may use MI.slicc
as the file that specifies all the files necessary for the protocol. The
files necessary for specifying a protocol include the definitions of the
state machines for different controllers, and of the network messages
that are passed on between these controllers.

The files have a syntax similar to that of C++. The compiler, written
using [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/), parses these
files to create an Abstract Syntax Tree (AST). The AST is then traversed
to build some of the internal data structures. Finally the compiler
outputs the C++ code by traversing the tree again. The AST represents
the hierarchy of different structures present with in a state machine.
We describe these structures next.

### Protocol State Machines

In this section we take a closer look at what goes in to a file
containing specification of a state machine.

#### Specifying Data Members

Each state machine is described using SLICC's **machine** datatype. Each
machine has several different types of members. Machines for cache and
directory controllers include cache memory and directory memory data
members respectively. We will use the MI protocol available in
src/mem/protocol as our running example. So here is how you might want
to start writing a state machine

```
machine(MachineType:L1Cache, "MI Example L1 Cache")
  : Sequencer * sequencer,
    CacheMemory * cacheMemory,
    int cache_response_latency = 12,
    int issue_latency = 2 {
      // Add rest of the stuff
    }
```
In order to let the controller receive messages from different
entities in the system, the machine has a number of **Message
Buffers**. These act as input and output ports for the machine. Here
is an example specifying the output ports.

```
 MessageBuffer requestFromCache, network="To", virtual_network="2", ordered="true";
 MessageBuffer responseFromCache, network="To", virtual_network="4", ordered="true";
```

Note that Message Buffers have some attributes that need to be specified
correctly. Another example, this time for specifying the input
ports.

```
 MessageBuffer forwardToCache, network="From", virtual_network="3", ordered="true";
 MessageBuffer responseToCache, network="From", virtual_network="4", ordered="true";
```

Next the machine includes a declaration of the **states** that
machine can possibly reach. In cache coherence protocol, states can
be of two types -- stable and transient. A cache block is said to be
in a stable state if in the absence of any activity (in coming
request for the block from another controller, for example), the
cache block would remain in that state for ever. Transient states
are required for transitioning between stable states. They are
needed when ever the transition between two stable states can not be
done in an atomic fashion. Next is an example that shows how states
are declared. SLICC has a keyword **state_declaration** that has to
be used for declaring
states.

```
state_declaration(State, desc="Cache states") {
   I, AccessPermission:Invalid, desc="Not Present/Invalid";
   II, AccessPermission:Busy, desc="Not Present/Invalid, issued PUT";
   M, AccessPermission:Read_Write, desc="Modified";
   MI, AccessPermission:Busy, desc="Modified, issued PUT";
   MII, AccessPermission:Busy, desc="Modified, issued PUTX, received nack";
   IS, AccessPermission:Busy, desc="Issued request for LOAD/IFETCH";
   IM, AccessPermission:Busy, desc="Issued request for STORE/ATOMIC";
}
```

The states I and M are the only stable states in this example. Again
note that certain attributes have to be specified with the states.

The state machine needs to specify the **events** it can handle and
thus transition from one state to another. SLICC provides the
keyword **enumeration** which can be used for specifying the set of
possible events. An example to shed more light on this -

```
enumeration(Event, desc="Cache events") {
   // From processor
   Load,       desc="Load request from processor";
   Ifetch,     desc="Ifetch request from processor";
   Store,      desc="Store request from processor";
   Data,       desc="Data from network";
   Fwd_GETX,        desc="Forward from network";
   Inv,        desc="Invalidate request from dir";
   Replacement,  desc="Replace a block";
   Writeback_Ack,   desc="Ack from the directory for a writeback";
   Writeback_Nack,   desc="Nack from the directory for a writeback";
}
```

While developing a protocol machine, we may need to define
structures that represent different entities in a memory system.
SLICC provides the keyword **structure** for this purpose. An
example
follows

```
structure(Entry, desc="...", interface="AbstractCacheEntry") {
   State CacheState,        desc="cache state";
   bool Dirty,              desc="Is the data dirty (different than memory)?";
   DataBlock DataBlk,       desc="Data in the block";
}
```

The cool thing about using SLICC's structure is that it automatically
generates for you the get and set functions on different fields. It also
writes a nice print function and overloads the \<\< operator. But in
case you would prefer do everything on your own, you can make use of the
keyword **external** in the declaration of the structure. This would
prevent SLICC from generating C++ code for this structure.

```
structure(TBETable, external="yes") {
   TBE lookup(Address);
   void allocate(Address);
   void deallocate(Address);
   bool isPresent(Address);
}
```

In fact many predefined types exist in src/mem/protocol/RubySlicc_\*.sm
files. You can make use of them, or if you need new types, you can
define new ones as well. You can also use the keyword **interface** to
make use of inheritance features available in C++. Note that currently
SLICC supports public inheritance only.

We can also declare and define functions as we do in C++. There are
certain functions that the compiler expects would always be defined
by the controller. These include
- getState()
- setState()

#### Input for the Machine

Since protocol is state machine, we need to specify how to machine
transitions from one state to another on receiving inputs. As mentioned
before, each machine has several input and output ports. For each input
port, the **in_port** keyword is used for specifying the behavior of
the machine, when a message is received on that input port. An example
follows that shows the syntax for declaring an input
port.

```
in_port(mandatoryQueue_in, RubyRequest, mandatoryQueue, desc="...") {
  if (mandatoryQueue_in.isReady()) {
    peek(mandatoryQueue_in, RubyRequest, block_on="LineAddress") {
      Entry cache_entry := getCacheEntry(in_msg.LineAddress);
      if (is_invalid(cache_entry) &&
          cacheMemory.cacheAvail(in_msg.LineAddress) == false ) {
        // make room for the block
        trigger(Event:Replacement, cacheMemory.cacheProbe(in_msg.LineAddress),
                getCacheEntry(cacheMemory.cacheProbe(in_msg.LineAddress)),
                TBEs[cacheMemory.cacheProbe(in_msg.LineAddress)]);
      }
      else {
        trigger(mandatory_request_type_to_event(in_msg.Type), in_msg.LineAddress,
                cache_entry, TBEs[in_msg.LineAddress]);
      }
    }
  }
}
```

As you can see, in_port takes in multiple arguments. The first
argument, mandatoryQueue_in, is the identifier for the in_port
that is used in the file. The next argument, RubyRequest, is the
type of the messages that this input port receives. Each input port
uses a queue to store the messages, the name of the queue is the
third argument.

The keyword **peek** is used to extract messages from the queue of
the input port. The use of this keyword implicitly declares a
variable **in_msg** which is of the same type as specified in the
input port's declaration. This variable points to the message at the
head of the queue. It can be used for accessing the fields of the
message as shown in the code above.

Once the incoming message has been analyzed, it is time for using
this message for taking some appropriate action and changing the
state of the machine. This done using the keyword **trigger**. The
trigger function is actually used only in SLICC code and is not
present in the generated code. Instead this call is converted in to
a call to the **doTransition()** function which appears in the
generated code. The doTransition() function is automatically
generated by SLICC for each of the state machines. The number of
arguments to trigger depend on the machine itself. In general, the
input arguments for trigger are the type of the message that needs
to processed, the address for which this message is meant for, the
cache and the transaction buffer entries for that address.

**trigger** also increments a counter that is checked before a
transition is made. In one ruby cycle, there is a limit on the
number of transitions that can be carried out. This is done to
resemble more closely to a hardware based state machine. **@TODO:
What happens if there are no more transitions left? Does the wakeup
abort?**

#### Actions

In this section we will go over how the actions that a state machine can
carry out are defined. These actions will be called in to action when
the state machine receives some input message which is then used to make
a transition. Let's go over an example on how the key word **action**
can be made use of.

```
action(a_issueRequest, "a", desc="Issue a request") {
   enqueue(requestNetwork_out, RequestMsg, latency=issue_latency) {
   out_msg.Address := address;
     out_msg.Type := CoherenceRequestType:GETX;
     out_msg.Requestor := machineID;
     out_msg.Destination.add(map_Address_to_Directory(address));
     out_msg.MessageSize := MessageSizeType:Control;
   }
}
```

The first input argument is the name of the action, the next
argument is the abbreviation used for generating the documentation
and last one is the description of the action which used in the HTML
documentation and as a comment in the C++ code.

Each action is converted in to a C++ function of that name. The
generated C++ code implicitly includes up to three input parameters
in the function header, again depending on the machine. These
arguments are the memory address on which the action is being taken,
the cache and transaction buffer entries pertaining to this address.

Next useful thing to look at is the **enqueue** keyword. This
keyword is used for queuing a message, generated as a result of the
action, to an output port. The keyword takes three input arguments,
namely, the name of the output port, the type of the message to be
queued and the latency after which this message can be dequeued.
Note that in case randomization is enabled, the specified latency is
ignored. The use of the keyword implicitly declares a variable
out_msg which is populated by the follow on statements.

#### Transitions

A transition function is a mapping from the cross product of set of
states and set of events to the set of states. SLICC provides the
keyword **transition** for specifying the transition function for state
machines. An example follows --

```
transition(IM, Data, M) {
   u_writeDataToCache;
   sx_store_hit;
   w_deallocateTBE;
   n_popResponseQueue;
}
```

In this example, the initial state is *IM*. If an event of type *Data*
occurs in that state, then final state would be *M*. Before making the
transition, the state machine can perform certain actions on the
structures that it maintains. In the given example,
*u_writeDataToCache* is an action. All these operations are performed
in an atomic fashion, i.e. no other event can occur before the set of
actions specified with the transition has been completed.

For ease of use, sets of events and states can be provided as input
to transition. The cross product of these sets will map to the same
final state. Note that the final state cannot be a set. If for a
particular event, the final state is same as the initial state, then
the final state can be omitted.

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   z_stall;
}
```

### Special Functions

#### Stalling/Recycling/Waiting input ports

One of the more complicated internal features of SLICC and the resulting
state machines is how the deal with the situation when events cannot be
process due to the cache block being in a transient state. There are
several possible ways to deal with this situation and each solution has
different tradeoffs. This sub-section attempts to explain the
differences. Please email the gem5-user list for further follow-up.

##### Stalling the input port

The simplest way to handle events that can't be processed is to simply
stall the input port. The correct way to do this is to include the
"z_stall" action within the transition statement:

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   z_stall;
}
```

Internally SLICC will return a ProtocolStall for this transition and no
subsequent messages from the associated input port will be processed
until the stalled message is processed. However, the other input ports
will be analyzed for ready messages and processed in parallel. While
this is a relatively simple solution, one may notice that stalling
unrelated messages on the same input port will cause excessive and
unnecessary stalls.

One thing to note is **Do Not** leave the transition statement blank
like so:

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   // stall the input port by simply not popping the message
}
```

This will cause SLICC to return success for this transition and SLICC
will continue to repeatedly analyze the same input port. The result is
eventual deadlock.

##### Recycling the input port

The better performance but more unrealistic solution is to recycle the
stalled message on the input port. The way to do this is to use the
"zz_recycleMandatoryQueue"
action:

```
action(zz_recycleMandatoryQueue, "\z", desc="Send the head of the mandatory queue to the back of the queue.") {
   mandatoryQueue_in.recycle();
}
```
```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   zz_recycleMandatoryQueue;
}
```

The result of this action is that the transition returns a Protocol
Stall and the offending message moved to the back of the FIFO input
port. Therefore, other unrelated messages on the same input port can be
processed. The problem with this solution is that recycled messages may
be analyzed and reanalyzed every cycle until an address changes state.

##### Stall and wait the input port

An even better, but more complicated solution is to "stall and wait" the
offending input message. The way to do this is to use the
"z_stallAndWaitMandatoryQueue"
action:

```
action(z_stallAndWaitMandatoryQueue, "\z", desc="recycle L1 request queue") {
   stall_and_wait(mandatoryQueue_in, address);
}
```
```
transition({IS, IM, IS_I, M_I, SM, SINK_WB_ACK}, {Load, Ifetch, Store, L1_Replacement}) {
   z_stallAndWaitMandatoryQueue;
}
```

The result of this action is that the transition returns success, which
is ok because stall_and_wait moves the offending message off the input
port and to a side table associated with the input port. The message
will not be analyzed again until it is woken up. In the meantime, other
unrelated messages will be processed.

The complicated part of stall and wait is that stalled messages must be
explicitly woken up by other messages/transitions. In particular,
transitions that move an address to a base state should wake up
potentially stalled messages waiting for that address:

```
action(kd_wakeUpDependents, "kd", desc="wake-up dependents") {
   wakeUpBuffers(address);
}
```

```
transition(M_I, WB_Ack, I) {
   s_deallocateTBE;
   o_popIncomingResponseQueue;
   kd_wakeUpDependents;
}
```

Replacements are particularly complicated since stalled addresses are
not associated with the same address they are actually waiting to
change. In those situations all waiting messages must be woken
up:

```
action(ka_wakeUpAllDependents, "ka", desc="wake-up all dependents") {
   wakeUpAllBuffers();
}
```

```
transition(I, L2_Replacement) {
   rr_deallocateL2CacheBlock;
   ka_wakeUpAllDependents;
}
```

### Other Compiler Features

- SLICC supports conditional statements in form of **if** and
**else**. Note that SLICC does not support **else if**.

- Each function has return type which can be void as well. Returned
values cannot be ignored.

- SLICC has limited support for pointer variables. is_valid() and
is_invalid() operations are supported for testing whether a given
pointer 'is not NULL' and 'is NULL' respectively. The keyword
**OOD**, which stands for Out of Domain, plays the role of keyword
NULL used in C++.

- SLICC does not support **\!** (the not operator).

- Static type casting is supported in SLICC. The keyword
**static_cast** has been provided for this purpose. For example, in
the following piece of code, a variable of type AbstractCacheEntry
is being casted in to a variable of type Entry.

```
   Entry L1Dcache_entry := static_cast(Entry, "pointer", L1DcacheMemory[addr]);
```

### SLICC Internals

**C++ to Slicc Interface - @note: What do each of these files
do/define???**

- src/mem/protocol/RubySlicc_interaces.sm
    - RubySlicc_Exports.sm
    - RubySlicc_Defines.sm
    - RubySlicc_Profiler.sm
    - RubySlicc_Types.sm
    - RubySlicc_MemControl.sm
    - RubySlicc_ComponentMapping.sm

**Variable Assignments**

- Use the `:=` operator to assign members in class (e.g. a member
defined in RubySlicc_Types.sm):
    - an automatic `m_` is added to the name mentioned in the SLICC
    file.


---


## Statistics

*Source: https://www.gem5.org/documentation/general_docs/statistics/*

# Stats Package
The philosophy of the stats package at the moment is to have a single base class called Stat which is merely a hook into every other aspect of the stat that may be important. Thus, this Stat base class has virtual functions to name, set precision for, set flags for, and initialize size for all the stats. For all Vector based stats, it is very important to do the initialization before using the stat so that appropriate storage allocation can occur. For all other stats, naming and flag setting is also important, but not as important for the actual proper execution of the binary. The way this is set up in the code is to have a regStats() pass in which all stats can be registered in the stats database and initialized.

Thus, to add your own stats, just add them to the appropriate class' data member list, and be sure to initialize/register them in that class' regStats function.

Here is a list of the various initialization functions. Note that all of these return a Stat& reference, thus enabling a clean looking way of calling them all.

* init(various args) //this differs for different types of stats.
   * Average: does not have an init()
   * Vector: init(size_t) //indicates size of vector
   * AverageVector: init(size_t) //indicates size of vector
   * Vector2d: init(size_t x, size_t y) //rows, columns
   * Distribution: init(min, max, bkt) //min refers to minimum value, max the maximum value, and bkt the size of the bkts. In other words, if you have min=0, max=15, and bkt=8, then 0-7 will go into bucket 0, and 8-15 will go into bucket 1.
   * StandardDeviation: does not have an init()
   * AverageDeviation: does not have an init()
   * VectorDistribution: init(size, min, max, bkt) //the size refers to the size of the vector, the rest are the same as for Distributions.
   * VectorStandardDeviation: init(size) //size refers to size of the vector
   * VectorAverageDeviation: init(size) //size refers to size of the vector
   * Formula: does not have an init()
* name(const std::string name) //the name of the stat
* desc(const std::string desc) //a brief description of the stat
* precision(int p) //p refers to how many places after the decimal point to go. p=0 will force rounding to integers.
* prereq(const Stat &prereq) //this indicates that this stat should not be printed unless prereq has a non-zero value. (like if there are 0 cache accesses, don't print cache misses, hits, etc.)
* subname(int index, const std::string subname) //this is for Vector based stats to give a subname to each index of the vector.
* subdesc(int index, const std::string subname) //also for Vector based stats, to give each index a subdesc. For 2d Vectors, the subname goes to each of the rows (x's). The y's can be named using a Vector2d member function ysubname, see code for details.

flags(FormatFlags f) //these are various flags you can pass to the stat, which i'll describe below.

* none -- no special formatting
* total -- this is for Vector based stats, if this flag is set, the total across the Vector will be printed at the end (for those stats which this is supported).
* pdf -- This will print the probability distribution of a stat
* nozero -- This will not print the stat if its value is zero
* nonan -- This will not print the stat if it's Not a Number (nan).
* cdf -- This will print the cumulative distribution of a stat

Below is an example of how to initialize a VectorDistribution:

```
    vector_dist.init(4,0,5,2)
        .name("Dummy Vector Dist")
        .desc("there are 4 distributions with buckets 0-1, 2-3, 4-5")
        .flags(nonan | pdf)
        ;
```
# Stat Types #
## Scalar ## 
The most basic stat is the Scalar. This embodies the basic counting stat. It is a templatized stat and takes two parameters, a type and a bin. The default type is a Counter, and the default bin is NoBin (i.e. there is no binning on this stat). It's usage is straightforward: to assign a value to it, just say foo = 10;, or to increment it, just use ++ or += like for any other type.
## Average ##
This is a "special use" stat, geared toward calculating the average of something over the number of cycles in the simulation. This stat is best explained by example. If you wanted to know the average occupancy of the load-store queue over the course of the simulation, you'd need to accumulate the number of instructions in the LSQ each cycle and at the end divide it by the number of cycles. For this stat, there may be many cycles where there is no change in the LSQ occupancy. Thus, you could use this stat, where you only need to explicitly update the stat when there is a change in the LSQ occupancy. The stat itself will take care of itself for cycles where there is no change. This stat can be binned and it also templatized the same way Stat is.
## Vector ##
A Vector is just what it sounds like, a vector of type T in the template parameters. It can also be binned. The most natural use of Vector is for something like tracking some stat over number of SMT threads. A Vector of size n can be declared just by saying Vector<> foo; and later initializing the size to n. At that point, foo can be accessed as if it were a regular vector or array, like foo[7]++.
## AverageVector ##
An AverageVector is just a Vector of Averages.
## Vector2d ##
A Vector2d is a 2 dimensional vector. It can be named in both the x and y directions, though the primary name is given across the x-dimension. To name in the y-dimension, use a special ysubname function only available to Vector2d's.
## Distribution ##
This is essentially a Vector, but with minor differences. Whereas in a Vector, the index maps to the item of interest for that bucket, in a Distribution you could map different ranges of interest to a bucket. Basically, if you had the bkt parameter of init for a Distribution = 1, you might as well use a Vector.
## StandardDeviation ##
This stat calculates standard deviation over number of cycles in the simulation. It's similar to Average in that it has behavior built into it, but it needs to be updated every cycle.
## AverageDeviation ##
This stat also calculates the standard deviation but it does not need to be updated every cycle, much like Average. It will handle cycles where there is no change itself.
## VectorDistribution ##
This is just a vector of distributions.
## VectorStandardDeviation ##
This is just a vector of standard deviations.
## VectorAverageDeviation ##
This is just a vector of AverageDeviations.
## Histogram ##
This stat puts each sampled value into one bin out of a configurable number of bins. All bins form a contiguous interval and are of equal length. The length of the bins is dynamically extended, if there is a sample value which does not fit into one the existing bins.
## SparseHistogram ##
This stat is similar to a histogram, except that it can only sample natural numbers. SparseHistogram is e.g. suitable for counting the number of accesses to memory addresses.
## Formula ##
This is a Formula stat. This is for anything that requires calculations at the end of the simulation, for example something that is a rate. So, an example of defining a Formula would be:

```
    Formula foo = bar + 10 / num;
```

There are a few subtleties to Formula. If bar and num are both stats(including Formula type), then there is no problem. If bar or num are regular variables, then they must be qualified with constant(bar). This is essentially cast. If you want to use the value of bar or num at the moment of definition, then use constant(). If you want to use the value of bar or num at the moment the formula is calculated (i.e. the end), define num as a Scalar. If num is a Vector, use sum(num) to calculate its sum for the formula. The operation "scalar(num)", which casts a regular variable to a Scalar, does no longer exist.


---


## Statistics API

*Source: https://www.gem5.org/documentation/general_docs/statistics/api*

# Statistics APIs

## Contents
1. [General Statistics Functions](#general-statistics-functions)
2. [Stats::Group - Statistics Container](#stats_group-statistics-container)
3. [Stats Flags](#stats-flags)
4. [Statistic Classes](#statistics-classes)
5. [Appendix: Migrating to the new style of tracking statistics](#appendix_migrating-to-the-new-style-of-tracking-statistics)

---

## General Statistics Functions

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void Stats::dump()`                                 | Dump all stats to registered outputs, e.g. stats.txt.                  |
|`void Stats::reset()`                                | Reset stats.                                                           |

---

## Stats::Group - Statistics Container
Typically, a statistic object can be placed in any `SimObject` as a class variable.
However, [a recent update](https://gem5-review.googlesource.com/c/public/gem5/+/19368)
addresses the hierarchical nature of `SimObject` 's in gem5,
which in turns makes the statistics of the objects hierarchical.
The update introduces the `Stats::Group` class, which is a statistics container
and is aware of the hierarchical structure of `SimObject`'s.
Ideally, this container should contain all stats in a `SimObject`.

**Note**: If you decide to use a `Stats::Group` struct inside of a `SimObject`,
there are typically two ways of doing this:
- Create a subgroup using `Stats::Group(Stats::Group &parent, const std::string &name)` constructor. This is useful when it is desired to have multiple instances of the same stats structure.
- Using `Stats::Group(Stats::Group &parent)` constructor, which merges (i.e. adds) the stats of the current group to the parent group. Thus, the stats added to the current group behave as if they were added to the parent group.

### Stats::Group macros
##### `#define ADD_STAT(n, ...) n(this, # n, __VA_ARGS__)`
Convenience macro to add a stat to a statistics group.

This macro is used to add a stat to a Stats::Group in the
initilization list in the Group's constructor. The macro
automatically assigns the stat to the current group and gives it
the same name as in the class. For example:
```
struct MyStats : public Stats::Group
{
    Stats::Scalar scalar0;
    Stats::Scalar scalar1;

    MyStats(Stats::Group *parent)
        : Stats::Group(parent),
          ADD_STAT(scalar0, "Description of scalar0"),       // equivalent to scalar0(this, "scalar0", "Description of scalar0"), where scalar0 has the follwing constructor
                                                             // Stats::Scalar(Group *parent = nullptr, const char *name = nullptr, const char *desc = nullptr)
          scalar1(this, "scalar1", "Description of scalar1")
     {
     }
};
```


### Stats::Group functions
##### `Group(Group *parent, const char *name = nullptr)`
Construct a new statistics group.

The constructor takes two parameters, a parent and a name. The
parent group should typically be specified. However, there are
special cases where the parent group may be null. One such
special case is SimObjects where the Python code performs late
binding of the group parent.

If the name parameter is NULL, the group gets merged into the
parent group instead of creating a sub-group. Stats belonging
to a merged group behave as if they have been added directly to
the parent group.

##### `virtual void regStats()`
Callback to set stat parameters.

This callback is typically used for complex stats (e.g.,
distributions) that need parameters in addition to a name and a
description. In the case stats objects cannot be initilalized
in the constructor (such as the stats that keep track of the
bus masters, which only can be discovered after the entire
system is instantiated). Stat names and descriptions should
typically be set from the constructor using the `ADD_STAT` macro.

##### `virtual void resetStats()`
Callback to reset stats.

##### `virtual void preDumpStats()`
Callback before stats are dumped. This can be overridden by
objects that need to perform calculations in addition to the
capabiltiies implemented in the stat framework.

##### `void addStat(Stats::Info *info)`
Register a stat with this group. This method is normally called
automatically when a stat is instantiated.

##### `const std::map<std::string, Group *> &getStatGroups() const`
Get all child groups associated with this object.

##### `const std::vector<Info *> &getStats() const`
Get all stats associated with this object.

##### `void addStatGroup(const char *name, Group *block)`
Add a stat block as a child of this block.

This method may only be called from a Group constructor or from
regStats. It's typically only called explicitly from Python
when setting up the SimObject hierarchy.

##### `const Info * resolveStat(std::string name) const`
Resolve a stat by its name within this group.

This method goes through the stats in this group and sub-groups
and returns a pointer to the the stat that matches the provided
name. The input name has to be relative to the name of this
group.

For example, if this group is the `SimObject
system.bigCluster.cpus` and we want the stat
`system.bigCluster.cpus.ipc`, the input param should be the
string "ipc".

---

## Stats Flags

| Flags            | Descriptions                                                   |
|------------------|----------------------------------------------------------------|
| `Stats::none`    | Nothing extra to print.                                        |
| `Stats::total`   | Print the total.                                               |
| `Stats::pdf`     | Print the percent of the total that this entry represents.     |
| `Stats::cdf`     | Print the cumulative percentage of total upto this entry.      |
| `Stats::dist`    | Print the distribution.                                        |
| `Stats::nozero`  | Don't print if this is zero.                                   |
| `Stats::nonan`   | Don't print if this is NAN                                     |
| `Stats::oneline` | Print all values on a single line. Useful only for histograms. |

Note: even though the flags `Stats::init` and `Stats::display` are available, the flags
are not allowed to be set by users.

---

## Statistics Classes

| Class names                                         | Descriptions                                                            |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| [`Stats::Scalar`](#statsscalar)                     | Simple scalar statistic.                                                |
| [`Stats::Average`](#statsaverage)                   | A statistic that calculate the PER TICK average of a value.             |
| [`Stats::Value`](#statsvalue)                       | Similar to Stats::Scalar.                                               |
| [`Stats::Vector`](#statsvector)                     | A vector of scalar statistics.                                          |
| [`Stats::AverageVector`](#statsaveragevector)       | A vector of average statistics.                                         |
| [`Stats::Vector2d`](#statsvector2d)                 | A 2D vector of scalar statistics.                                       |
| [`Stats::Distribution`](#statsdistribution)         | A simple distribution statistic (having convinient min, max sum, etc.). |
| [`Stats::Histogram`](#statshistogram)               | A simple histogram statistic (keeping the frequencies of equally-splitted continuous ranges). |
| [`Stats::SparseHistogram`](#statssparsehistogram)   | Keeps the frequency / histogram of a collection of discrete values.     |
| [`Stats::StandardDeviation`](#statsstandarddeviation)| Calculates the mean and variance of all samples.                       |
| [`Stats::AverageDeviation`](#statsaveragedeviation) | Calculates per tick mean and variance of samples.                       |
| [`Stats::VectorDistribution`](#statsvectordistribution)| A vector of distributions.                                           |
| [`Stats::VectorStandardDeviation`](#statsvectorstandarddeviation)| A vector of standard deviation statistics.                 |
| [`Stats::VectorAverageDeviation`](#statsvectoraveragedeviation)| A vector of average deviation statistics.                    |
| [`Stats::Formula`](#statsformula)                   | Keeps the statistic involving arithmetics of multiple stats objects.    |

**Note:** `Stats::Average` only calculates the average of a scalar over the number of simulated ticks.
In order to get the average of quantity A over quantity B, `Stats::Formula` can be utilized.
For example,
```C++
Stats::Scalar totalReadLatency;
Stats::Scalar numReads;
Stats::Formula averageReadLatency = totalReadLatency/numReads;
```

### Common statistic functions

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`StatClass name(const std::string &name)`            | sets the statistic name, marks the stats to be printed                 |
|`StatClass desc(const std::string &_desc)`           | sets the description for the statistic                                 |
|`StatClass precision(int _precision)`                | sets the precision of the statistic                                    |
|`StatClass flags(Flags _flags)`                      | sets the flags                                                         |
|`StatClass prereq(const Stat &prereq)`               | sets the prerequisite stat                                             |

### `Stats::Scalar`
Storing a signed integer statistic.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void operator++()`                                  | increments the stat by 1 // prefix ++, e.g. `++scalar`                 |
|`void operator--()`                                  | decrements the stat by 1 // prefix --                                  |
|`void operator++(int)`                               | increments the stat by 1 // postfix ++, e.g. `scalar++`                |
|`void operator--(int)`                               | decrements the stat by 1 // postfix --                                 |
|`template <typename U> void operator=(const U &v)`   | sets the scalar to the given value                                     |
|`template <typename U> void operator+=(const U &v)`  | increments the stat by the given value                                 |
|`template <typename U> void operator-=(const U &v)`  | decrements the stat by the given value                                 |
|`size_type size()`                                   | returns 1                                                              |
|`Counter value()`                                    | returns the current value of the stat as an integer                    |
|`Counter value() const`                              | returns the current value of the stat as an integer                    |
|`Result result()`                                    | returns the current value of the stat as a `double`                    |
|`Result total()`                                     | returns the current value of the stat as a `double`                    |
|`bool zero()`                                        | returns `true` if the stat equals to zero, returns `false` otherwise   |
|`void reset()`                                       | resets the stat to 0                                                   |

### `Stats::Average`
Storing an average of an integer quantity, supposely A, over the number of simulated ticks.
The quantity A keeps the same value across all ticks after its latest update and before the next update.
**Note:** the number of simulated ticks is reset when the user calls `Stats::reset()`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`void set(Counter val)`                              | sets the quantity A to the given value                                 |
|`void inc(Counter val)`                              | increments the quantity A by the given value                           |
|`void dec(Counter val)`                              | decrements the quantity A by the given value                           |
|`Counter value()`                                    | returns the current value of A as an integer                           |
|`Result result()`                                    | returns the current average as a `double`                              |
|`bool zero()`                                        | returns `true` if the average equals to zero, returns `false` otherwise|
|`void reset(Info \*info)`                            | keeps the current value of A, does not count the value of A before the current tick|

### `Stats::Value`
Storing a signed integer statistic that is either an integer or an integer that is a result from calling a function or an object's method.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Counter value()`                                    | returns the value as an integer                                        |
|`Result result() const`                              | returns the value as a double                                          |
|`Result total() const`                               | returns the value as a double                                          |
|`size_type size() const`                             | returns 1                                                              |
|`bool zero() const`                                  | returns `true` if the value is zero, returns `false` otherwise         |


### `Stats::Vector`
Storing an array of scalar statistics where each element of the vector has function signatures similar to those of `Stats::Scalar`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type size)`                     | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                 |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index          |
|`void value(VCounter &vec) const`                    | copies the vector of statistics to the given vector of integers        |
|`void result(VResult &vec) const`                    | copies the vector of statistics to the given vector of doubles         |
|`Result total() const`                               | returns the sum of all statistics in the vector as a double            |
|`size_type size() const`                             | returns the size of the vector                                         |
|`bool zero() const`                                  | returns `true` if each statistic in the vector is 0, returns `false` otherwise|
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `vecStats[1]+=9`|

### `Stats::AverageVector`
Storing an array of average statistics where each element of the vector has function signatures similar to those of `Stats::Average`.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type size)`                     | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                 |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index          |
|`void value(VCounter &vec) const`                    | copies the vector of statistics to the given vector of integers        |
|`void result(VResult &vec) const`                    | copies the vector of statistics to the given vector of doubles         |
|`Result total() const`                               | returns the sum of all statistics in the vector as a double            |
|`size_type size() const`                             | returns the size of the vector                                         |
|`bool zero() const`                                  | returns `true` if each statistic in the vector is 0, returns `false` otherwise|
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `avgStats[1].set(9)`|

### `Stats::Vector2d`
Storing a 2-dimensional array of scalar statistics, where each element of the array has function signatures similar to those of `Stats::Scalar`.
This data structure assumes all elements whose the same second dimension index has the same name.

| Function signatures                                 | Descriptions                                                           |
|-----------------------------------------------------|------------------------------------------------------------------------|
|`Derived & init(size_type _x, size_type _y)`         | initializes the vector to the given size (throws an error if attempting to resize an initilized vector)|
|`Derived & ysubname(off_type index, const std::string &subname)` | sets `subname` as the name of the statistics of elements whose the second dimension of `index`|
|`Derived & ysubnames(const char **names)`            | similar to `ysubname()` above, but sets name for all indices of the second dimension|
|`std::string ysubname(off_type i) const`             | returns the name of the statistics of elements whose the second dimension of `i`|
|`size_type size() const`                             | returns the number of elements in the array                            |
|`bool zero()`                                        | returns `true` if the element at row 0 column 0 equals to 0, returns `false` otherwise |
|`Result total()`                                     | returns the sum of all elements as a double
|`void reset()`                                       | sets each element in the array to 0                                    |
|`operator[](off_type index)`                         | gets the reference to the statistic at the given index, e.g. `vecStats[1][2]+=9`|

### `Stats::Distribution`
Storing a distribution of a quantity.
The statistics of the distribution include,
  - the smallest/largest value being sampled
  - the number of values that are smaller/larger than the specified minimum and maximum
  - the sum of all samples
  - the mean, the geometric mean and the standard deviation of the samples
  - histogram within the range of [`min`, `max`] splitted into `(max-min)/bucket_size` equally sized buckets,  where the `min`/`max`/`bucket_size` are inputs to the init() function.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`Distribution & init(Counter min, Counter max, Counter bkt)` | initializes the distribution where `min` is the minimum value being tracked by the distribution's histogram, `max` is the minimum value being tracked by the distribution's histogram, and `bkt` is the number of values in each bucket |
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns the number of bucket in the distribution                       |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset(Info *info)`                                     | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Histogram`)|

### `Stats::Histogram`
Storing a histogram of a quantity given the number of buckets.
All buckets are equally sized.
Different from the histogram of `Stats::Distribution` which keeps track of the samples in a specific range, `Stats::Histogram` keeps track of all samples in its histogram.
Also, while `Stats::Distribution` is parameterized by the number of values in a bucket, `Stats::Histogram`'s sole parameter is the number of buckets.
When a new sample is outside of the current range of all all buckets, the buckets will be resized.
Roughly, two consecutive buckets will be merged until the new sample is inside one of the buckets.

Other than the histogram itself, the statistics of the distribution include,
  - the smallest/largest value being sampled
  - the sum of all samples
  - the mean, the geometric mean and the standard deviation of the samples

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`Histogram & init(size_type size)`                           | initializes the histogram, sets the number of buckets to `size`        |
|`void sample(Counter val, int number)`                       | adds `val` to the histogram `number` times                             |
|`void add(HistStor *)`                                       | merges another histogram to this histogram                             |
|`size_type size() const `                                    | returns the number of buckets                                          |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset(Info *info)`                                     | discards all samples                                                   |

### `Stats::SparseHistogram`
Storing a histogram of a quantity given a set of integral values.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`template <typename U> void sample(const U &v, int n = 1)`   | adds `v` to the histogram `n` times                                    |
|`size_type size() const `                                    | returns the number of entries                                          |
|`bool zero() const`                                          | returns `true` if the number of samples is zero, returns `false` otherwise |
|`void reset()`                                               | discards all samples                                                   |

### `Stats::StandardDeviation`
Keeps track of the standard deviation of a sample.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns 1                                                              |
|`bool zeros() const`                                         | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Distribution`|

### `Stats::AverageDeviation`
Keeps track of the average deviation of a sample.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`void sample(Counter val, int number)`                       | adds `val` to the distribution `number` times                          |
|`size_type size() const`                                     | returns 1                                                              |
|`bool zeros() const`                                         | discards all samples                                                   |
|`add(DistBase &)`                                            | merges the samples from another `Stats` class with `DistBase` (e.g. `Stats::Distribution`|

### `Stats::VectorDistribution`
Storing a vector of distributions where each element of the vector has function signatures similar to those of `Stats::Distribution`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorDistribution & init(size_type size, Counter min, Counter max, Counter bkt)` | initializes a vector of `size` distributions where `min` is the minimum value being tracked by each distribution's histogram, `max` is the minimum value being tracked by each distribution's histogram, and `bkt` is each distribution's the number of values in each bucket |
|`Derived & subname(off_type index, const std::string &name)` | adds a name to the statistic at the given index                        |
|`Derived & subdesc(off_type index, const std::string &desc)` | adds a description to the statistic at the given index                 |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the distribution at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::VectorStandardDeviation`
Storing a vector of standard deviations where each element of the vector has function signatures similar to those of `Stats::StandardDeviation`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorStandardDeviation & init(size_type size)`             | initializes a vector of `size` standard deviations                     |
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                         |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index                  |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the standard deviation at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::VectorAverageDeviation`
Storing a vector of average deviations where each element of the vector has function signatures similar to those of `Stats::AverageDeviation`.

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`VectorAverageDeviation & init(size_type size)`              | initializes a vector of `size` average deviations                      |
|`Derived & subname(off_type index, const std::string &name)`| adds a name to the statistic at the given index                         |
|`Derived & subdesc(off_type index, const std::string &desc)`| adds a description to the statistic at the given index                  |
|`size_type size() const`                                     | returns the number of elements in the vector                           |
|`bool zero() const`                                          | returns `true` if each of distributions has 0 samples, return `false` otherwise |
|`operator[](off_type index)`                                 | gets the reference to the average deviation at the given index, e.g. `dists[1].sample(2,3)`|

### `Stats::Formula`
Storing a statistic that is a result of a series of arithmetic operations on `Stats` objects.
Note that, in the following function, `Temp` could be any of `Stats` class holding statistics (including vector statistics), a formula, or a number (e.g.`int`, `double`, `1.2`).

| Function signatures                                         | Descriptions                                                           |
|-------------------------------------------------------------|------------------------------------------------------------------------|
|`const Formula &operator=(const Temp &r)`                    | assigns an uninitialized `Stats::Formula` to the given root            |
|`const Formula &operator=(const T &v)`                       | assigns the formula to a statistic or another formula or a number      |
|`const Formula &operator+=(Temp r)`                          | adds to the current formula a statistic or another formula or a number  |
|`const Formula &operator/=(Temp r)`                          | divides the current formula by a statistic or another formula or a number |
|`void result(VResult &vec) const`                            | assigns the evaluation of the formula to the given vector; if the formula does *not* have a vector component (none of the variables in the formula is a vector), then the vector size is 1 |
|`Result total() const`                                       | returns the evaluation of the `Stats::Formula` as a double; if the formula does have a vector component (one of the variables in the formula is a vector), then the vector is turned in to a scalar by setting it to the sum all elements in the vector |
|`size_type size() const`                                     | returns 1 if the root element is not a vector, returns the size of the vector otherwise |
|`bool zero()`                                                | returns `true` if all elements in `result()` are 0's, returns `false` otherwise|

An example of using `Stats::Formula`,
```C++
Stats::Scalar totalReadLatency;
Stats::Scalar numReads;
Stats::Formula averageReadLatency = totalReadLatency/numReads;
```

---

## Appendix. Migrating to the new style of tracking statistics

### A new style of tracking statistics
gem5 statistics have a flat structure that are not aware of the hierarchical structure of `SimObject`, which usually contains stat objects.
This causes the problem of different stats having the same name, and more importantly, it was not trivial to manipulating the structure of gem5 statistics.
Also, gem5 did not offer a way to group a collection of stat objects into different groups, which is important to maintain a large number of stat objects.

[A recent commit](https://gem5-review.googlesource.com/c/public/gem5/+/19368) introduces `Stats::Group`, a structure intended to keep all statistics belong to an object.
The new structure offers an explicit way to reflect the hierarchical nature of `SimObject`
`Stats::Group` also makes it more explicit and easier to maintain a large set of `Stats` objects that should be grouped into different collections as one can make several `Stats::Group`'s in a `SimObject` and merges them to the `SimObject`, which is also a `Stats::Group` that is aware of its children `Stats::Group`'s.

Generally, this is a step towards a more structured `Stats` format, which should facilitate the process of manipulating the overall structure of statistics in gem5, such as filtering out statistics and producing `Stats` to more standardized formats such as JSON and XML, which, in turns, have an enormous amount of supported libraries in a variety of programming languages.

### Migrating to the new style of tracking statistics

*Notes*: Migrating to the new style is highly encouraged; however, the legacy style of statistics (i.e. the one with a flat structure) is still supported.

This guide provides a broad look of how to migrate to the new style of gem5 statistics tracking, as well as points out some concrete examples showing how it is being done.

#### `ADD_STAT`
`ADD_STAT` is a macro defined as,
```C++
#define ADD_STAT(n, ...) n(this, # n, __VA_ARGS__)
```
This macro is intended to be used in `Stats::Group` constructors to initilize a `Stats` object.
In other words, `ADD_STAT` is an alias for caling `Stats` object constructors.
For example, `ADD_STAT(stat_name, stat_desc)` is the same as,
```
  stat_name.parent = the `Stats::Group` where stat_name is defined
  stat_name.name = "stat_name"
  stat_name.desc = "stat_desc"
```
This is applicable for most of `Stats` data types with an exception that for `Stats::Formula`, the macro `ADD_STAT` can handle an optional parameter specifying the formula.
For example, `ADD_STAT(ips, "Instructions per Second", n_instructions/sim_seconds)`.


An example use case of `ADD_STAT` (and we refer to this example as "**Example 1**" throughout this section).
This example is also served as a template of constructing a `Stats::Group` struct.
```C++
    protected:
        // Defining the a stat group
        struct StatGroup : public Stats::Group
        {
            StatGroup(Stats::Group *parent); // constructor
            Stats::Histogram histogram;
            Stats::Scalar scalar;
            Stats::Formula formula;
        } stats;

    // Defining the declared constructor
    StatGroup::StatGroup(Stats::Group *parent)
      : Stats::Group(parent),                           // initilizing the base class
        ADD_STAT(histogram, "A useful histogram"),
        scalar(this, "scalar", "A number"),             // this is the same as ADD_STAT(scalar, "A number")
        ADD_STAT(formula, "A formula", scalar1/scalar2)
    {
        histogram
          .init(num_bins);
        scalar
          .init(0)
          .flags(condition ? 1 : 0);
    }
```

#### Moving to the new style
Those are concrete examples of converting stats to the new style: [here](https://gem5-review.googlesource.com/c/public/gem5/+/19370), [here](https://gem5-review.googlesource.com/c/public/gem5/+/19371) and [here](https://gem5-review.googlesource.com/c/public/gem5/+/32794).

Moving stats to the new style involves:
  - Creating a struct `Stats::Group`, and moving all stats variables there. This struct's scope should be `protected`. The declaration of stat variables is usually in the header files.
  - Getting rid of `regStats()`, and moving the initialzation of stat variables to `Stats::Group` constructor as shown in **Example 1**.
  - In both header files and cpp files, all stats variables should be pre-appended by the newly created `Stats::Group` name as the stats are now under the `Stats::Group` struct.
  - Updating the class constructors to initialize `Stats::Group` variable. Usually, it's adding `stats(this)` to the constructors assuming the name of the variable is `stats`.

Some examples,
  - An example of `Stats::Group` declaration is [here](https://github.com/gem5/gem5/blob/v20.0.0.3/src/cpu/testers/traffic_gen/base.hh#L194).
Note that all variables of type starting with `Stats::` have been moved to the struct.
  - An example of a `Stats::Group` constructor that utilizes `ADD_STAT` is [here](https://github.com/gem5/gem5/blob/v20.0.0.3/src/cpu/testers/traffic_gen/base.cc#L332).
  - In the case where a stat variable requiring additional initializations other than `name` and `description`, you can follow [this example](https://github.com/gem5/gem5/blob/v20.0.0.3/src/mem/comm_monitor.cc#L105).


---


# ═══ gem5 Standard Library (stdlib) ═══


## Standard Library Overview

*Source: https://www.gem5.org/documentation/gem5-stdlib/overview*

## An overview of the gem5 standard library

Similar to standard libraries in programming languages, the gem5 standard library is designed to provide users of gem5 with commonly used components, features, and functionality with the goal of improving their productivity.
The gem5 stdlib was introduced in [v21.1](https://github.com/gem5/gem5/tree/v21.1.0.0) in an alpha-release state (then referred to as "gem5 components"), and has been fully released as of [v21.2](https://github.com/gem5/gem5/tree/v21.2.0.0).

For users new to the gem5 standard library, the following tutorials may be of help in understanding how the gem5 stdlib may be used to improve the creation of gem5 simulations.
They include a tutorial on building syscall emulation and full-system simulations, as well as a guide on how to extend the library and contribute.
The [`configs/examples/gem5_library`](https://github.com/gem5/gem5/tree/stable/configs/example/gem5_library) directory in the gem5 repository also contains example scripts which use the library.

The following subsections give a broad overview of the gem5 stdlib packages and what there intended purposes are.

**Note: The documentation/tutorials/etc. related to the standard library have been updated for the v24.1 release.
Please ensure you have the correct version of gem5 before proceeding.**

As part of [gem5's 2022 Bootcamp](/events/boot-camp-2022), the stdlib was taught as a tutorial.
Slides for this tutorial can be found [here](https://raw.githubusercontent.com/gem5bootcamp/gem5-bootcamp-env/main/assets/slides/using-gem5-02-gem5-stdlib-tutorial.pdf).
A video recording of this tutorial can be found [here](https://www.youtube.com/watch?v=vbruiMyIFsA).

The stdlib was also covered during the [2024 gem5 Bootcamp](https://bootcamp.gem5.org/#02-Using-gem5/01-stdlib).

<!-- Could use a nice picture here showing the main modules of the stdlib and how they relate -->

## The gem5 stdlib components package and its design philosophy

The gem5 stdlib components package is the central part of the gem5 stdlib.
With it users can built complex systems from simple components which connect together using standardized APIs.

The metaphor that guided the components package development was that of building a computer using off-the-shelf components.
When building a computer, someone may select components, plug them into a board, and assume the interface between the board and the component have been designed in a way in which they will "just work."
For example, someone can remove a processor from a board and add a different one, compatible with the same socket, without needing to change everything else in their setup.
While there are always limitations to this design philosophy, the components package has a highly modular and extensible design with components of the same type being interchangeable with one another as much as is possible.

At the core of the components package is the idea of a _board_.
This plays a similar role to the motherboard in a real-world system.
While it may contain embedded caches, controllers, and other complex components, its main purpose is to expose standardized interfaces for other hardware to be added and handle communication between them.
For example, a memory device and a processor may be added to a board with the board responsible for communication without the designer of the memory or the processor having to consider this assuming they conform to known APIs.

Typically, a gem5 components package _board_ requires declaration of these three components:

1. The _processor_ : The system processor. A processor component contains at least one _core_ which may be Atomic, O3, Timing, or KVM.
2. The _memory_ system: The memory system, for example, a DDR3_1600.
3. The _cache hierarchies_: This component defines any and all components between the processor and main memory, most notably the cache setup. In the simplest of setups this will connect memory directly to the processor.

The other devices required for full-system simulation, which rarely change between simulations, are handled by the board.

A typical usage of the components may therefore look like:

```python

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR3_1600(size="3GB")

processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

The following tutorials go into greater detail on how to use the components package to create gem5 simulations.

## The gem5 resources package

The gem5 stdlib's resource package is used to obtain and incorporate resources.
A resource, in the context of gem5, is something used in a simulation, or by a simulation, but not directly used to construct a system to be simulated.
Typically these are applications, kernels, disk images, benchmarks, or tests.

As these resources can be hard to find, or hard to create, we provide pre-built resources as part of [gem5-resources](/documentation/general_docs/gem5_resources).
For example, via gem5-resources, a user may download an Ubuntu 18.04 disk image with known compatibility with gem5.
They need not setup this themselves.

A core feature of the gem5 stdlib resource package is that it allows users to _automatically obtain_ prebuilt gem5 resources for their simulation.
A user may specify in their Python config file that a specific gem5 resource is required and, when run, the package will check if there is a local copy on the host system, and if not, download it.

The tutorials will demonstrate how to use the resource package in greater detail, but for now, a typical pattern is as follows:

```python
from gem5.resources.resource import Resource

resource = Resource("riscv-disk-img")

print(f"The resources is available at {resource.get_local_path()}")
```

This will obtain the `riscv-disk-img` resource and store it locally for use in a gem5 simulation.

The resources package references the resources that are available to view at the [gem5 Resources website](https://resources.gem5.org) and the [gem5 Resources repository](https://github.com/gem5/gem5-resources). The website is strongly recommended to get info on what resources are available and where they may be downloaded from.

## The Simulate package

The simulate package is used to run gem5 simulations.
While there is some boilerplate code this module handles on the users behalf, its primary purpose is to provde default behavior and APIs for what we refer to as _Exit Events_.
Exit events are when a simulation exits for a particular reason.

A typical example of an exit event would be a `Workbegin` exit event.
This is used to specify that a Region-of-Interest (ROI) has been reached.
Usually this exit would be used to allow a user to begin logging statistics or to switch to a more detailed CPU model.
Prior to the stdlib, the user would need to specify precisely what the expected behavior was at exit events such as this.
The simulation would exit and the configuration script would contain Python code specifying what to do next.
Now, with the simulate package, there is a default behavior for this kind of event (the stats are reset), and an easy interface to override this behavior with something the user requires.

More information about exit events can be found in the [M5ops documentation](https://www.gem5.org/documentation/general_docs/m5ops/).


---


## Hello World Tutorial

*Source: https://www.gem5.org/documentation/gem5-stdlib/hello-world-tutorial*

## Building a "Hello World" example with the gem5 standard library

In this tutorial we will cover how to create a very basic simulation using gem5 components.
This simulation will setup a system consisting of a single-core processor, running in Atomic mode, connected directly to main memory with no caches, I/O, or other components.
The system will run an X86 binary in syscall emulation (SE) mode.
The binary will be obtained from gem5-resources and which will print a "Hello World!" string to stdout upon execution.

To start we must compile the ALL build for gem5:

```sh
# In the root of the gem5 directory
scons build/ALL/gem5.opt -j <number of threads>
```

As of gem5 v24.1, the ALL build includes all Ruby protocols and all ISAs. If you are using a prebuilt gem5 binary, this step is not necessary.

Then a new Python file should be created (we will refer to this as `hello-world.py` going forward).
The first lines in this file should be the needed imports:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
```

All these libraries are included inside the compiled gem5 binary.
Therefore, you will not need to obtain them from elsewhere.
`from gem5.` indicates we are importing from the `gem5` standard library, and the lines starting with `from gem5.components` are importing components from the gem5 components package.
The `from gem5.resources` line means we are importing from the resources package, and `from gem5.simulate`, the simulate package.
All these packages, `components`, `resources`, and `simulate` are part of the gem5 standard library.

Next we begin specifying the system.
The gem5 library requires the user to specify four main components: the _board_, the _cache hierarchy_, the _memory system_, and the _processor_.

Let's start with the _cache hierarchy_:

```python
cache_hierarchy = NoCache()
```

Here we are using `NoCache()`.
This means, for our system, we are stating there is no cache hierarchy (i.e., no caches).
In the gem5 library the cache hierarchy is a broad term for anything that exists between the processor cores and main memory.
Here we are stating the processor is connected directly to main memory.

Next we declare the _memory system_:

```python
memory = SingleChannelDDR3_1600("1GiB")
```

There exists many memory components to choose from within `gem5.components.memory`.
Here we are using a single-channel DDR3 1600, and setting its size to 1 GiB.
It should be noted that setting the size here is technically optional.
If not set, the `SingleChannelDDR3_1600` will default to 8 GiB.

Then we consider the _processor_:

```python
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.X86)
```

A processor in `gem5.components` is an object which contains a number of gem5 CPU cores, of a particular or varying type (`ATOMIC`, `TIMING`, `KVM`, `O3`, etc.).
The `SimpleProcessor` used in this example is a processor where all the CPU Cores are of an identical type.
It requires two arguments: the `cpu_type`, which we set to `ATOMIC`, and `num_cores`, the number of cores, which we set to one.

Finally we specify which _board_ we are using:

```python
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

While the constructor of each board may vary, they will typically require the user to specify the _processor_, _memory system_, and _cache hierarchy_, as well as the clock frequency to use.
In this example we use the `SimpleBoard`.
The `SimpleBoard` is a very basic system with no I/O which only supports SE-mode and can only work with "classic" cache hierarchies.

At this point in the script we have specified everything we require to simulate our system.
Of course, in order to run a meaningful simulation, we must specify a workload for this system to run.
To do so we add the following lines:

```python
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)
```

The `obtain_resource` function takes a string which specifies which resource, from [gem5-resources](/documentation/general_docs/gem5_resources), is to be obtained for the simulation.
All the gem5 resources can be found on the [gem5 Resources website](https://resources.gem5.org).

If the resource is not present on the host system it'll be automatically downloaded.
In this example we are going to use the `x86-hello-64-static` resource;
an x86, 64-bit, statically compiled binary which will print "Hello World!" to stdout.
After specifying the resource we set the workload via the board's `set_se_binary_workload` function.
As the name suggests `set_se_binary_workload` is a function used to set a binary to be executed in Syscall Execution mode.

You can see and search for available resources on the [gem5 resources website](https://resources.gem5.org/).

This is all that is required to setup your simulation.
From this you simply need to construct and run the `Simulator`:

```python
simulator = Simulator(board=board)
simulator.run()
```

As a recap, your script should look like the following:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Obtain the components.
cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600("1GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.X86)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the workload.
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
```

It can then be executed with:

```sh
./build/ALL/gem5.opt hello-world.py
```

If you are using a pre-built binary, you can execute the simulation with:

```sh
gem5 hello-world.py
```

If setup correctly, the output will look something like:

```text
info: Using default config
Global frequency set at 1000000000000 ticks per second
src/mem/dram_interface.cc:690: warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (1024 Mbytes)
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
board.remote_gdb: Listening for connections on port 7005
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
src/sim/syscall_emul.hh:1117: warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
Hello world!
```

It should be obvious from this point that a _board's_ parameters may be altered to test other designs.
For example, if we want to test a `TIMING` CPU setup we'd change our _processor_ to:

```python
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86)
```

This is all that is required.
The gem5 standard library will reconfigure the design as is necessary.

As another example, consider swapping out a component for another.
In this design we decided on `NoCache` but we could use another classic cache hierarchy, such as `PrivateL1CacheHierarchy`.
To do so we'd change our `cache_hierarchy` parameter:

```python
# We import the cache hierarchy we want.
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy

...

# Then set it.
cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB")
```

Note here that `PrivateL1CacheHierarchy` requires the user to specify the L1 data and instruction cache sizes to be constructed.
No other part of the design need change.
The gem5 standard library will incorporate the cache hierarchy as required.

To recap on what was learned in this tutorial:

* A system can be built with the gem5 components package using _processor_, _cache hierarchy_, _memory system_, and _board_ components.
* Generally speaking, components of the same type are interchangeable as much as is possible. E.g., different _cache hierarchy_ components may be swapped in and out of a design without reconfiguration needed in other components.
* _boards_ contain functions to set workloads.
* The resources package may be used to obtain prebuilt resources from gem5-resources.
These are typically workloads that may be run via set workload functions.
* The simulate package can be used to run a board within a gem5 simulation.


---


## X86 Full-System Tutorial

*Source: https://www.gem5.org/documentation/gem5-stdlib/x86-full-system-tutorial*

## Building an x86 full-system simulation with the gem5 standard library

One of the key ideas behind the gem5 standard library is to allow users to simulate, big, complex systems, with minimal effort.
This is done by making sensible assumptions about the nature of the system to simulate and connecting components in a manner which "makes sense."
While this takes away some flexibility, it massively simplifies simulating typical hardware setups in gem5.
The overarching philosophy is to make the _common case_ simple.

In this tutorial we will build an X86 simulation, capable of running a full-system simulation, booting an Ubuntu operating system, and running a benchmark.
This system will utilize gem5's ability to switch cores, allowing booting of the operating system in KVM fast-forward mode and switching to a detailed CPU model to run the benchmark, and use a MESI Two Level Ruby cache hierarchy in a dual-core setup.
Without using the gem5 library this would take several hundred lines of Python, forcing the user to specify details such as every IO component and exactly how the cache hierarchy is setup.
Here, we will demonstrate how simple this task can be with using the gem5 standard library.

First, we build the ALL binary. This will allow us to run simulations for any ISA, including X86:

```sh
scons build/ALL/gem5.opt -j <number of threads>
```

If you are using a prebuilt gem5 binary, this step is not necessary.

To start, create a new Python file.
We will refer to this as `x86-ubuntu-run.py`.

To begin we add our import statements:

```python
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
```

As in other Python scripts, these are simply classes/functions needed in our script.
They are all included as part of the gem5 binary and therefore do not need to obtained elsewhere.

A good start is to use the `requires` function to specify what kind of gem5 binary/setup is required to run the script:

```python
requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)
```

Here we state that we need gem5 compiled to run the X86 ISA and support the MESI Two Level protocol.
We also require the host system to have KVM.
**NOTE: Please ensure your host system supports KVM. If your system does not please remove the `kvm_required` check here**.
KVM will only work if the host platform and the simulated ISA are the same (e.g., X86 host and X86 simulation). You can learn more about using KVM with gem5 [here](https://www.gem5.org/documentation/general_docs/using_kvm/).

This `requires` call is not required but provides a good safety net to those running the script.
Errors that occur due to incompatible gem5 binaries may not make much sense otherwise.

Next we start specifying the components in our system.
We start with the _cache hierarchy_:

```python
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)
```

Here we setup a MESI Two Level (ruby) cache hierarchy.
Via the constructor we set the L1 data cache and L1 instruction cache to 32 KiB, and the L2 cache to 256 KiB.

Next we setup the _memory system_:

```python
memory = SingleChannelDDR3_1600(size="2GiB")
```

This is quite simple and should be intuitive: A single channel DDR3 1600 setup of size 2GiB.
**Note:** by default the `SingleChannelDDR3_1600` component has a size of 8GiB.
However, due to [a known limitation with the X86Board](https://gem5.atlassian.net/browse/GEM5-1142), we cannot use a memory system greater than 3GiB.
We therefore must set the size.

Next we setup the _processor_:

```python
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=2,
)
```

Here we are utilizing the gem5 standard library's special `SimpleSwitchableProcessor`.
This processor can be used for simulations in which a user wants to switch out one type of core for another during a simulation.
The `starting_core_type` parameter specifies which CPU type to start a simulation with.
In this case a KVM core.
**(Note: If your host system does not support KVM, this simulation will not run. You must change this to another CPU type, such as `CPUTypes.ATOMIC`)**
The `switch_core_type` parameter specifies which CPU type to switch to in a simulation.
In this case we'll be switching from KVM cores to TIMING cores.
The final parameter, `num_cores`, specifies the number of cores within the processor.

With this processor a user can call `processor.switch()` to switch to and from the starting cores and the switch cores, which we will demonstrate later on in this tutorial.

Next we add these components to the _board_:

```python
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

Here we use the `X86Board`.
This is a board used to simulate a typical X86 system in full-system mode.
As a minimum, the board needs the `clk_freq`, `processor`, `memory`, and `cache_hierarchy` parameters specified.
This finalizes our system design.

Now we set the workload to run on the system:

```python
workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
board.set_workload(workload)
```

The `obtain_resource` function acquires the X86 Ubuntu 24.04 boot workload.
This workload contains a kernel resource, parameters to the kernel, a disk image resource, and a string indicating the underlying function that gem5 uses when `board.set_workload()` is called.
You can see these details under the [Raw](https://resources.gem5.org/resources/x86-ubuntu-24.04-boot-with-systemd/raw?database=gem5-resources&version=3.0.0) tab of of the gem5 Resources website page for this workload.

You can also use `set_kernel_disk_workload()` instead of `set_workload()` and set the disk image and kernel resources separately.
This can be used when you want to use your own resources, or a combination of resources that is not provided as a workload on [the gem5 resources website](resources.gem5.org).

**Note: If a user wishes to use their own resource (that is, a resource not prebuilt as part of gem5-resources), they may follow the tutorial [here](../general_docs/gem5_resources). A tutorial is also available at the [2024 gem5 bootcamp website](https://bootcamp.gem5.org/#02-Using-gem5/02-gem5-resources)**

When using the `set_kernel_disk_workload()` function, you can also pass an optional `readfile_contents` argument.
This will be run as a bash script after the system boots up, and can be used to launch a benchmark after the system boots if the disk image has benchmarks installed.
An example can be found [here](https://resources.gem5.org/resources/x86-ubuntu-24.04-npb-ua-b/raw?database=gem5-resources&version=2.0.0)

Finally, we specify how the simulation is to be run with the following:

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
    # readfile_contents. This is the last exit event before the simulation exits.
    yield True


simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
simulator.run()
```

The important thing to note here is the `on_exit_event` argument.
Here we can override default behavior.

The `on_exit_event` parameter is a Python dictionary of exit events and [Python generators](https://wiki.python.org/moin/Generators).
In this tutorial we use the `exit_event_handler` generator to handle exit events of the type `ExitEvent.EXIT`.
There are three `EXIT` exit events in the Ubuntu 24.04 disk image resource used by the workload.
If an exit event handler is not defined, the simulation will end after the first exit event, which takes place after the kernel finishes booting.
Yielding `False` allows the simulation to continue, while yielding `True` ends the simulation.
After the second exit event, we switch the cores from KVM to TIMING, then yield `False` to continue the simulation.
After the third exit event, we yield `True`, ending the simulation.

This completes the setup of our script. To execute the script we run:

```bash
./build/ALL/gem5.opt x86-ubuntu-run.py
```

If you are using a pre-built binary, you can execute the simulation with:

```sh
gem5 hello-world.py
```

You can see the output of the simulator in `m5out/system.pc.com_1.device`.

Below is the configuration script in full.
It mirrors closely the example script at `configs/example/gem5_library/x86-ubuntu-run-with-kvm.py` in the gem5 repository.

```python
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR3_1600(size="2GiB")

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=2,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
board.set_workload(workload)


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
    # readfile_contents. This is the last exit event before the simulation exits.
    yield True


simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
simulator.run()

```

To recap what we learned in this tutorial:

* The `requires` function can be used to specify the gem5 and host requirements for a script.
* The `SimpleSwitchableProcessor` can be used to create a setup in which cores can be switched out for others.
* The `X86Board` can be used to set up full-system simulations.
* Its workload can be set via either `set_workload()` for workload resources, or via `set_kernel_disk_workload()` for separate kernel and disk image resources.
* The `set_kernel_disk_workload()` function accepts a `readfile_contents` argument.
This is processed as a script to be executed after the system boot is complete.
* The `Simulator` module allows for the overriding of exit events using Python generators.


---


## Developing Your Own Components Tutorial

*Source: https://www.gem5.org/documentation/gem5-stdlib/develop-own-components-tutorial*

## Developing your own gem5 standard library components

![gem5 component library design](/assets/img/stdlib/gem5-components-design.png)

The above diagram shows the basic design of the gem5 library components.
There are four important abstract classes: `AbstractBoard`, `AbstractProcessor`, `AbstractMemorySystem`, and `AbstractCacheHierarchy`.
Every gem5 component inherits from one of these to be a gem5 component usable in a design.
The `AbstractBoard` must be constructed by specifying an `AbstractProcessor`, `AbstractMemorySystem`, and an `AbstractCacheHierarchy`.
With this design any board may use any combination of components which inherit from `AbstractProcessor`, `AbstractMemorySystem`, and `AbstractCacheHierarchy`.
For example, using the image as a guide, we can add a `SimpleProcessor`, `SingleChannelDDR3_1600` and a `PrivateL1PrivateL2CacheHierarchy` to an `X86Board`.
If we desire, we can swap out the `PrivateL1PrivateL2CacheHierarchy` for another class which inherits from `AbstractCacheHierarchy`.

In this tutorial we will imagine a user wishes to create a new cache hierarchy.
As you can see from the diagram, there are two subclasses which inherit from `AbstractCacheHierarchy`: `AbstractRubyCacheHierarchy` and `AbstractClassicCacheHierarchy`.
While you _can_ inherit directly from `AbstractCacheHierarchy`, we recommend inheriting from the subclasses (depending on whether you wish to develop a ruby or classic cache hierarchy setup).
We will inherit from the `AbstractClassicCacheHierarchy` class to create a classic cache setup.

To begin, we should create a new Python class which inherits from the `AbstractClassicCacheHierarchy`.
In this example we will call this `UniqueCacheHierarchy`, contained within a file `unique_cache_hierarchy.py`:

```python
from m5.objects import (
    Port,
)

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)


class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):


    def __init__() -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)

    def get_mem_side_port(self) -> Port:
        pass

    def get_cpu_side_port(self) -> Port:
        pass

    def incorporate_cache(self, board: AbstractBoard) -> None:
        pass
```

As with every abstract base class, there are virtual functions which must be implemented.
Once implemented the `UniqueCacheHierarchy` can be used in simulations.
The `get_mem_side_port` and `get_cpu_side_port` are declared in the [AbstractClassicCacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/classic/abstract_classic_cache_hierarchy.py), while `incorporate_cache` is declared in the [AbstractCacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/abstract_cache_hierarchy.py)

The `get_mem_side_port` and `get_cpu_side_port` functions return a `Port` each.
As their name suggests, these are ports used by the board to access the cache hierarchy from the memory side and the cpu side.
These must be specified for all classic cache hierarchy setups.

The `incorporate_cache` function is the function which is called to incorporate the cache into the board.
The contents of this function will vary between cache hierarchy setups but will typically inspect the board it is connected to, and use the board's API to connect the cache hierarchy.

In this example we assume the user is looking to implement a private L1 cache hierarchy, consisting of a data cache and instruction cache for each CPU core.
This has actually already been implemented in the gem5 stdlib as the [PrivateL1CacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/classic/private_l1_cache_hierarchy.py), but for this example we shall duplicate the effort.

First we start by implementing the `get_mem_side_port` and `get_cpu_side_port` functions:

```python
from m5.objects import (
    BadAddr,
    Port,
    SystemXBar,
)

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)


class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):

    def __init__(self) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus = SystemXBar(width=64)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    def incorporate_cache(self, board: AbstractBoard) -> None:
        pass
```

Here we have used a simple memory bus.

Next, we implement the `incorporate_cache` function:

```python
from m5.objects import (
    BadAddr,
    Cache,
    Port,
    SystemXBar,
)

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache


class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):

    def __init__(self) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus = SystemXBar(width=64)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    def incorporate_cache(self, board: AbstractBoard) -> None:
        # Set up the system port for functional access from the simulator.
        board.connect_system_port(self.membus.cpu_side_ports)

        for cntr in board.get_memory().get_memory_controllers():
            cntr.port = self.membus.mem_side_ports

        self.l1icaches = [
            L1ICache(size="32KiB")
            for i in range(board.get_processor().get_num_cores())
        ]

        self.l1dcaches = [
            L1DCache(size="32KiB")
            for i in range(board.get_processor().get_num_cores())
        ]
        # ITLB Page walk caches
        self.iptw_caches = [
            MMUCache(size="8KiB")
            for _ in range(board.get_processor().get_num_cores())
        ]
        # DTLB Page walk caches
        self.dptw_caches = [
            MMUCache(size="8KiB")
            for _ in range(board.get_processor().get_num_cores())
        ]

        if board.has_coherent_io():
            self._setup_io_cache(board)

        for i, cpu in enumerate(board.get_processor().get_cores()):

            cpu.connect_icache(self.l1icaches[i].cpu_side)
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)

            self.l1icaches[i].mem_side = self.membus.cpu_side_ports
            self.l1dcaches[i].mem_side = self.membus.cpu_side_ports

            self.iptw_caches[i].mem_side = self.membus.cpu_side_ports
            self.dptw_caches[i].mem_side = self.membus.cpu_side_ports

            cpu.connect_walker_ports(
                self.iptw_caches[i].cpu_side, self.dptw_caches[i].cpu_side
            )

            int_req_port = self.membus.mem_side_ports
            int_resp_port = self.membus.cpu_side_ports
            cpu.connect_interrupt(int_req_port, int_resp_port)

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="1kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()
```

This completes the code we'd need to create our own cache hierarchy.

To use this code, a user can import it as they would any other Python module.
As long as this code is in gem5's python search path, you can import it.
You can also add `import sys; sys.path.append(<path to new component>)` at the beginning of your gem5 runscript to add the path of this new component to the python search path.

## Contributing your component to the gem5 stdlib

Before contributing your component, you will need to move it into the `src/` directory so that it is compiled into the gem5 binary.

### Compiling your component into the gem5 standard library

The gem5 standard library code resides in `src/python/gem5`.
The basic directory structure is as follows:

```txt
gem5/
    components/                 # All the components to build the system to simulate.
        boards/                 # The boards, typically broken down by ISA target.
            experimental/       # Experimental boards.
        cachehierarchies/       # The Cache Hierarchy components.
            chi/                # CHI protocol cache hierarchies.
            classic/            # Classic cache hierarchies.
            ruby/               # Ruby cache hierarchies.
        memory/                 # Memory systems.
        processors/             # Processors.
    prebuilt/                   # Prebuilt systems, ready to use.
        demo/                   # Prebuilt System for demonstrations. (not be representative of real-world targets).
    resources/                  # Utilities used for referencing and obtaining gem5-resources.
    simulate/                   # A package for the automated running of gem5 simulations.
    utils/                      # General utilities.
```

We recommend putting the `unique_cache_hierarchy.py` in `src/python/gem5/components/cachehierarchies/classic/`.

From then you need to add the following line to `src/python/SConscript`:

```scons
PySource('gem5.components.cachehierarchies.classic',
    'gem5/components/cachehierarchies/classic/unique_cache_hierarchy.py')
```

Then, when you recompile the gem5 binary, the `UniqueCacheHierarchy` class will be included.
To use it in your own scripts you need only include it:

```python
from gem5.components.cachehierarchies.classic.unique_cache_hierarchy import UniqueCacheHierarchy

...

cache_hierarchy = UniqueCacheHierarchy()

...

```

### gem5 Code contribution and review

If you believe your addition to the gem5 stdlib would be beneficial to the gem5 community, you may submit it as a patch.
Please follow our [Contributing Guidelines](/contributing) if you have not contributed to gem5 before or need a reminder on our procedures.

In addition to our normal contribution guidelines, we strongly advise you do the following to your stdlib contribution:

* **Add Documentation**: Classes and methods should be documented using [reStructured text](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).
Please look over other source code in the stdlib to see how this is typically done.
* **Use Python Typing**: Utilize the [Python typing module](https://docs.python.org/3/library/typing.html) to specify parameter and method return types.
* **Use relative imports**: Within the gem5 stdlib, relative imports should be used to reference other modules/package in the stdlib (i.e., that contained in `src/python/gem5`).
* **Format using black**: Please format your Python code with [Python black](https://pypi.org/project/black/), with 79 max line widths: `black --line-length=79 <file/directory>`.
**Note**: Python black does not always enforce line lengths.
For example, it will not reduce string lengths.
You may have to manually reduce the length of some lines.

Code will be reviewed via [GitHub](https://github.com/gem5/gem5) like all other contributions.
We would, however, emphasize that we will not accept patches to the library for simply being functional and tested;
we require some persuasion that the contribution improves the library and benefits the community.
For example, niche components may not be incorporated if they are seen to be low utility while increasing the library's maintenance overhead.


---


## How To Create Your Own Board Using The gem5 Standard Library

*Source: https://www.gem5.org/documentation/gem5-stdlib/develop-stdlib-board*

## How to Create Your Own Board Using the gem5 Standard Library

In this tutorial we will cover how to create a custom board using the gem5 Standard Library.

This tutorial is based on the process used to make the _RiscvMatched_, a RISC-V prebuilt board that inherits from `MinorCPU`. This board can be found at `src/python/gem5/prebuilt/riscvmatched`.

This tutorial will create a single-channeled DDR4 memory of size 2 GiB, a core using the MinorCPU and the RISC-V ISA though the same process can be used for another type or size of memory, ISA and core.

Likewise, this tutorial will utilize the UniqueCacheHierarchy made in the [Developing Your Own Components Tutorial](https://www.gem5.org/documentation/gem5-stdlib/develop-own-components-tutorial), though anyother cache hierarchy may be used.

First, we start by importing the components and stdlib features we require.

``` python
from typing import List

from m5.objects import (
    AddrRange,
    BaseCPU,
    BaseMMU,
    IOXBar,
    Port,
    Process,
)
from m5.objects.RiscvCPU import RiscvMinorCPU

from gem5.components.boards.abstract_system_board import AbstractSystemBoard
from gem5.components.boards.se_binary_workload import SEBinaryWorkload
from gem5.components.cachehierarchies.classic.unique_cache_hierarchy import (
    UniqueCacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.utils.override import overrides
```

We will begin development by creating a specialized CPU core for our board which inherits from an ISA-specific version of the chosen CPU.
Since our ISA is RISC-V and the CPU type we desire is a MinorCPU, we will inherit from `RiscvMinorCPU`.
This is done so that we can set our own parameters to tailor the CPU it to our requirements.
In our example will override a single parameter:  `decodeToExecuteForwardDelay` (the default is 1).
We have called this new CPU core type `UniqueCPU`.

``` python
class UniqueCPU(RiscvMinorCPU):
    decodeToExecuteForwardDelay = 2
```

As `RiscvMinorCPU` inherits from `BaseCPU`, we can incorporate this into the standard library using `BaseCPUCore`, a Standard Library wrapper for `BaseCPU` objects (source code for this can be found at `src/python/gem5/components/processors/base_cpu_core.py`).
The `BaseCPUCore` takes the `BaseCPU` as an argument during construction.
Ergo, we can do the following:

```python
core = BaseCPUCore(core=UniqueCPU(), isa=ISA.RISCV)
```

<!-- **Note**: `BaseCPU` objects require a unique `core_id` to be specified upon construction. -->

Next we must define our processor.
In the gem5 Standard Library a processor is a collection of cores.
In cases, such as ours, we can utilize the library's `BaseCPUProcessor`, a processor which contains `BaseCPUCore` objects (source code can be found in `src/python/gem5/components/processors/base_cpu_processor.py`).
The `BaseCPUProcessor` requires a list of `BaseCPUCore`s.
Therefore:

```python
processor = BaseCPUProcessor(cores=[core])
```

Next we focus on the construction of the board to host our components.
All boards must inherit from `AbstractBoard` and in most cases, gem5's `System` simobject.
Therefore, our board will inherit from `AbstractSystemBoard` in this case; an abstract class that inherits from both.

In order to run simulations with SE mode, we must also inherit from `SEBinaryWorkload`.

All `AbstractBoard`s must specify `clk_freq` (the clock frequency), the `processor`, `memory`, and the `cache_hierarchy`.
We already have our processor, and will use the `UniqueCacheHierarchy` for the `cache_hierarchy` and a `SingleChannelDDR4_2400`, with a size of 2GiB for the memory.

We will call this the `UniqueBoard` and it should look like the following:

``` python
class UniqueBoard(AbstractSystemBoard, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
    ) -> None:
        core = BaseCPUCore(core=UniqueCPU(), isa=ISA.RISCV)
        processor = BaseCPUProcessor(cores=[core])
        memory = SingleChannelDDR4_2400("2GiB")
        cache_hierarchy = UniqueCacheHierarchy()
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )
```

With the contructor complete, we must implement the abstract methods in `AbstractSystemBoard`.
It is useful here to look at the source for `AbstractBoard` in `/src/python/gem5/components/boards/abstract_system_board.py`.

The abstract methods you choose to implement or not will depend on what type of system you are creating.
In our example functions such as `_setup_board`, are unneeded so we will implement them with `pass`.
In other instances we will use `NotImplementedError` for cases where a particular component/feature is not available on this board and an error should be returned if trying to access it.
For example, our board will have no IO bus.
We will therefore implement `has_io_bus` to return `False` and have `get_io_bus` raise a `NotImplementedError` if called.

With the exception of `_setup_memory_ranges`, we do not implement many of the features the `AbstractSystemBoard` requires. The board should look like this:

``` python
class UniqueBoard(AbstractSystemBoard, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
    ) -> None:
        core = BaseCPUCore(core=UniqueCPU(), isa=ISA.RISCV)
        processor = BaseCPUProcessor(cores=[core])
        memory = SingleChannelDDR4_2400("2GiB")
        cache_hierarchy = UniqueCacheHierarchy()
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    @overrides(AbstractSystemBoard)
    def _setup_board(self) -> None:
        pass

    @overrides(AbstractSystemBoard)
    def has_io_bus(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_io_bus(self) -> IOXBar:
        raise NotImplementedError(
            "UniqueBoard does not have an IO Bus. "
            "Use `has_io_bus()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_dma_ports(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_dma_ports(self) -> List[Port]:
        raise NotImplementedError(
            "UniqueBoard does not have DMA Ports. "
            "Use `has_dma_ports()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_coherent_io(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_mem_side_coherent_io_port(self) -> Port:
        raise NotImplementedError(
            "UniqueBoard does not have any I/O ports. Use has_coherent_io to "
            "check this."
        )

    @overrides(AbstractSystemBoard)
    def _setup_memory_ranges(self) -> None:
        memory = self.get_memory()
        self.mem_ranges = [AddrRange(memory.get_size())]
        memory.set_memory_range(self.mem_ranges)
```

This concludes the creation of your custom board for the gem5 standard library.
The completed board is as follows:

```python
from typing import List

from m5.objects import (
    AddrRange,
    BaseCPU,
    BaseMMU,
    IOXBar,
    Port,
    Process,
)
from m5.objects.RiscvCPU import RiscvMinorCPU

from gem5.components.boards.abstract_system_board import AbstractSystemBoard
from gem5.components.boards.se_binary_workload import SEBinaryWorkload
from gem5.components.cachehierarchies.classic.unique_cache_hierarchy import (
    UniqueCacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.utils.override import overrides


class UniqueCPU(RiscvMinorCPU):
    decodeToExecuteForwardDelay = 2


class UniqueBoard(AbstractSystemBoard, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
    ) -> None:
        core = BaseCPUCore(core=UniqueCPU(), isa=ISA.RISCV)
        processor = BaseCPUProcessor(cores=[core])
        memory = SingleChannelDDR4_2400("2GiB")
        cache_hierarchy = UniqueCacheHierarchy()
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    @overrides(AbstractSystemBoard)
    def _setup_board(self) -> None:
        pass

    @overrides(AbstractSystemBoard)
    def has_io_bus(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_io_bus(self) -> IOXBar:
        raise NotImplementedError(
            "UniqueBoard does not have an IO Bus. "
            "Use `has_io_bus()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_dma_ports(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_dma_ports(self) -> List[Port]:
        raise NotImplementedError(
            "UniqueBoard does not have DMA Ports. "
            "Use `has_dma_ports()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_coherent_io(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_mem_side_coherent_io_port(self) -> Port:
        raise NotImplementedError(
            "UniqueBoard does not have any I/O ports. Use has_coherent_io to "
            "check this."
        )

    @overrides(AbstractSystemBoard)
    def _setup_memory_ranges(self) -> None:
        memory = self.get_memory()
        self.mem_ranges = [AddrRange(memory.get_size())]
        memory.set_memory_range(self.mem_ranges)

```

From this you can create a runscript and test your board:

``` python
from unique_board import UniqueBoard

from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

board = UniqueBoard(clk_freq="1.2GHz")

# As we are using the RISCV ISA, "riscv-hello" should work.
board.set_se_binary_workload(obtain_resource("riscv-hello"))

simulator = Simulator(board=board)
simulator.run()
```


---


## Local Resources Support in gem5

*Source: https://www.gem5.org/documentation/gem5-stdlib/local-resources-support*

This tutorial will walk you through the process of creating a WorkloadResource in gem5 and testing it, through the new gem5 Resources infrastructure introduced in gem5 v23.0.

A workload is set to a board in gem5 through the following line:

``` python
board.set_workload(obtain_resource(<ID_OF_WORKLOAD>))
```

The following image shows what a Resource ID is, as viewed on the [gem5 Resources website](https://resources.gem5.org/):
![gem5 resource ID example](/assets/img/stdlib/gem5-resource-id-example.png)

Therefore, the WorkloadResource with ID '<ID_OF_WORKLOAD>' will be parsed and it will be used to construct the function call it defines. 

The function call specified in the `"function"` field of the Workload JSON is then executed on the board, along with any parameters it has defined in the `"additional_parameters"` field.

## Introduction

The gem5 Resources infrastructure allows adding a local JSON data source that can be added to the main gem5 Resources MongoDB database.

We will use the local JSON data source to add a new WorkloadResource to gem5.

## Prerequisites

This tutorial assumes that you already have a pre-compiled Resource that you want to make into a WorkloadResource.

## Defining the Workload

### Defining the Resource JSON

The first step is to define the Resource that is used in a WorkloadResource.
In case the Resource already exists in gem5, you may skip this step.
Let's assume that the Resource we want to wrap in a WorkloadResource is compiled for `RISC-V`, categorized as a `binary`, and has the name `my-benchmark`.

We can define this Resource in a JSON object as follows:

``` json
{
    "category": "binary",
    "id": "my-benchmark",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
    "architecture": "RISCV",
    "is_zipped": false,
    "resource_version": "1.0.0",
    "gem5_versions": [
        "23.0"
    ],
}
```

It is important to initialize all the fields here correctly, as they are used by gem5 to initialize and run the Resource.

To see more about the fields required and not required by the Resources, see the [gem5 Resources JSON Schema](https://github.com/gem5/gem5-resources-website/blob/main/public/gem5-resources-schema.json).

### Defining the Workload JSON

Assuming that the binary of the Resource is uploaded to gem5 Resources cloud, its source code is available on the [gem5-resources GitHub repository](https://github.com/gem5/gem5-resources/) and the Resource is viewable on the [gem5 Resources website](https://resources.gem5.org) , you can now define the Workload JSON.
Let's assume that the WorkloadResource we are building wraps `my-benchmark`, and is called `binary-workload`.

We can define this WorkloadResource in a local JSON file as follows:

``` json
{
    "id": "binary-workload",
    "category": "workload",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
    "architecture": "RISCV",
    "function": "set_se_binary_workload",
    "resource_version": "1.0.0",
    "gem5_versions": [
        "23.0"
    ],
    "resources": {
        "binary": "my-benchmark"
    },
    "additional_parameters": {
        "arguments": ["arg1", "arg2"]
    }
}
```

The `"function"` field defines the function that will be called on the board.
The `"resources"` field defines the Resources that will be passed into the Workload.
The `"additional_parameters"` field defines the additional parameters that will be passed into the WorkloadResource.
So, the WorkloadResource defined above is equivalent to the following line of code:

``` python
board.set_se_binary_workload(binary = obtain_resource("binary_resource"), arguments = ["arg1", "arg2"])
```

To see more about the fields required and not required by the workloads, see the [gem5 Resources JSON Schema](https://github.com/gem5/gem5-resources-website/blob/main/public/gem5-resources-schema.json)

## Testing the Workload

To test the WorkloadResource, we first have to add the local JSON file as a data source for gem5.

This can be done by creating a new JSON file with the following format:

``` json
{
    "sources": {
        "my-resources": {
            "url": "<PATH_TO_JSON_FILE>",
            "isMongo": false,
        }
    }
}
```
On running gem5, if the new JSON config file you have created is present in the current working directory, it will be used as the data source for gem5.
If the JSON file is not present in the current working directory, you can specify the path to the JSON file using the `GEM5_CONFIG` flag while building gem5.

You should now be able to use the WorkloadResource in your simulations through its name, `binary-workload`.

**NOTE**: In order to check if the Resources you specified as part of a WorkloadResource are being passed into the WorkloadResource correctly, you can use the `get_parameters()` function in the WorkloadResource class.
This function returns a dictionary of the Resources passed into the WorkloadResource.
Its implementation can be found in [`src/python/gem5/resources/resource.py`](https://github.com/gem5/gem5/blob/6f5d877b1aacd551749dafa87da26600a4f01155/src/python/gem5/resources/resource.py#L673).

From gem5 v23.1, there are a couple additional ways to define your local `resources.json` file.
Both these ways are through environment variables and are defined through the command line while running a gem5 simulation.

1. `GEM5_RESOURCE_JSON` variable: This variable substitutes all the current data sources used by gem5 with the JSON file present at the path passed in through this variable. 
This is equivalent to a gem5 data source configuration file as follows:

    ``` json
    {
        "sources": {
            "my-resources": {
                "url": $GEM5_RESOURCE_JSON,
                "isMongo": false,
            }
        }
    }
    ```

2. `GEM5_RESOURCE_JSON_APPEND` variable: This variable adds the JSON file present at the path passed in through this variable to all the current data sources used by gem5.
This is equivalent to a gem5 data source configuration file as follows:

    ``` json
    {
        "sources": {
            "my-resources-1": {
                "url": '/local/local.json',
                "isMongo": false,
            },
                    "my-resources-2": {
                "url": $GEM5_RESOURCE_JSON_APPEND,
                "isMongo": false,
            },
        }
    }
    ```

## Support for Local Path to Resources

From gem5 v23.1, support has been added to make a workload of local resources through the method mentioned above.

This method involves making the same JSON object as mentioned in [Defining the Resource JSON](#defining-the-resource-json), with the addition of the "url" field.
This field is used in the gem5 Resources database to indicate where the file for a Resource is.
From gem5 v23.1, this field also accepts the _file_ URI scheme.
You can specify a path on your localhost and gem5 would be able to run it.

With these changes, a JSON object for a local instance of `my-benchmark` would look like:

``` json
{
    "category": "binary",
    "id": "my-benchmark",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
		"url": "file:/<PATH_TO_LOCAL_FILE>",
    "architecture": "RISCV",
    "is_zipped": false,
    "resource_version": "1.1.0",
    "gem5_versions": [
        "23.0"
    ],
}
```

**NOTE**: If you are creating a local version of a Resource with an ID that exists in gem5 Resources, be sure to change the `"resource_version"` field to a resource version that does not exist in the gem5 Resources database to avoid receiving an error while running a gem5 simulation.


---


## Suites in gem5

*Source: https://www.gem5.org/documentation/gem5-stdlib/suites*

## Introduction

Suite is a new category of resource introduced in gem5 version 23.1, which allows users to group workloads.
SuiteResource class is added to the resource specialization.
Pre-made suites on the gem5 resources can be obtained using `obtain_resource()` like all other resources. 

SuiteResource class has `__iter__` and `__len__` functions.
A SuiteResource will behave as an iterator that returns a generator of the workload objects. 

### How to Get a Suite

To get a suite already in gem5 resources, we can use the `obtain_resource` function present in the `[resource.py](http://resource.py)`.

To get a suite with ID “riscv-vertical-microbenchmarks” and version “1.0.0”

```python
suite_obj = obtain_resource(id = "riscv-vertical-microbenchmarks", resource_version="1.0.0")
```

Not specifying the resource_version will return the latest compatible version of the resource.

**NOTE**: The Suite used for the rest of the tutorial is the “riscv-vertical-microbenchmarks”, which exists in gem5 resources, but is only compatible with gem5 version 23.1 and above and with the RISC-V ISA.

### How to Filter a Workload in the Suite by Input Groups

Each suite had a workloads field which is an array containing the ID, version, and input groups of all the workloads in the suite.

The workload field would look like the following:

```python
[
	{
		'id': 'riscv-cca-run',
		'resource_version': '1.0.0',
		'input_group': ['cca']
	},
	{
		'id': 'riscv-cce-run',
		'resource_version': '1.0.0',
		'input_group': ['cce']
	},
	{
		'id': 'riscv-ccm-run',
		'resource_version': '1.0.0',
		'input_group': ['ccm']
	},
	...
]
```

The SuiteResource class has functions that allow users to filter workloads by input groups.
The function `get_input_groups()`  returns a set of all the input groups present in the suite.
The function `with_input_group(str)` returns a SuiteResource object which only has the workloads with the input group passed in as a parameter.
For example, our suite has the workloads field as defined above then, `get_input_groups()` will return the following:

```python
set(['cca','cce','ccm',...])
```

We can use the `with_input_group()` like this:

```python
suite_obj = obtain_resource('riscv-vertical-microbenchmarks')
filtered_suite = suite_obj.with_input_group('cca')
```

This will return a `SuiteResource` with all the workloads that fulfill the case of having input group “cca”, which in this case is the `WorkloadResource` with ID “riscv-cca-run”.

We can also use the `with_input_group()` function along with a for loop and a generator.

```python
for workload in suite_obj.with_input_group('cca')
	board.set_workload(workload)
	simulator = Simulator(board=board)
	simulator.run()
```

### Make a Custom Suite

Custom suites can also be made by directly using the `SuiteResource` class from `[resource.py](http://resource.py)`.
To create a custom suite we will also need `WorkloadResource` objects.

```python
workload1= obtain_resource('workload-1', resource_version='1.0.0')
workload2= obtain_resource('workload-2', resource_version='1.0.0')

suite_obj = SuiteResource(workloads=[workload1, workload2])
```

The above code snippet will create a suite object with two workloads.
We have not defined the `workloads` field in the above suite so the `get_input_group()` and `with_input_group()` functions will throw a warning and return an empty set and a suite object with no workloads respectively.

If the `workloads` field is added then the custom suite will function the same as a suite created by using `obtain_resource`.

```python
workload1= obtain_resource('workload-1', resource_version='1.0.0')
workload2= obtain_resource('workload-2', resource_version='1.0.0')
workloads = [
	{
		'id': 'workload-1',
		'resource_version': '1.0.0',
		'input_group': ['input_group_1', 'input_group_2']
	},
	{
		'id': 'workload-2',
		'resource_version': '1.0.0',
		'input_group': ['input_group_1', 'input_group_3']
	}]
suite_obj = SuiteResource(workloads=[workload1, workload2], worklaods= workloads)
```


---


## Setting gem5 Resources data sources to support local resources

*Source: https://www.gem5.org/documentation/gem5-stdlib/using-local-resources*

gem5 supports using local data sources in the form of a MongoDB Atlas and JSON datasource. gem5 has a default resources config in `src/python/gem5_default_config.py`. This resources config points to the MongoDB Atlas collection of gem5 resources. To utilize data sources other than the main gem5 resources database, you will need to override the gem5-resources-config.

There are several ways to update the gem5 resources configuration:

1. **Setting GEM5_CONFIG environment variable:** You can set the GEM5_CONFIG environment variable to specify a new configuration file. Doing this will replace the default resources configuration with the one you've specified.

2. **Using gem5-config.json:** If a file named gem5-config.json exists in the current working directory, it will take precedence over the default resources configuration.

3. **Fallback to default resources config:** If neither of the above methods is used, the system will resort to using the default resources configuration.

Additionally, if you wish to utilize or add a local resource JSON file to the currently selected config (as mentioned in the above methods), you have two additional methods available:

- **GEM5_RESOURCE_JSON environment variable:** This variable can be employed to override the current resources configuration and make use of a specified JSON file.

- **GEM5_RESOURCE_JSON_APPEND environment variable:** Use this variable to add a JSON file to the existing resources configuration without replacing it.

It's essential to note that overriding or appending doesn't modify the actual configuration files themselves. These methods allow you to temporarily specify or add resource configurations during runtime without altering the original configuration files.

MongoDB Atlas Config Format:

```json
{
    "sources":{
        "example-atlas-config": {
            "dataSource": "datasource name",
            "database": "database name",
            "collection": "collection name",
            "url": "Atlas data API URL",
            "authUrl": "Atlas authentication URL",
            "apiKey": "API key for data API for MongoDB Atlas",
            "isMongo": true
        }
    }
}
```

JSON Config Format:

```json
{
    "sources":{
        "example-json-config": {
            "url": "local path to JSON file or URL to a JSON file",
            "isMongo": false
        }
    }
}
```

### Setting up a MongoDB Atlas Database

You would need to set up an Atlas cluster, steps on setting up an Atlas cluster can be found here:
- https://www.mongodb.com/basics/mongodb-atlas-tutorial

You would also need to enable Atlas dataAPI, steps on enabling dataAPI can be found here:
- https://www.mongodb.com/docs/atlas/app-services/data-api/generated-endpoints/

### Using Multiple Data Sources

gem5 supports the use of more than one data source. The structure of the resource configuration is as follows:

```json
{
    "sources": {
         "gem5-resources": {
            "dataSource": "gem5-vision",
            "database": "gem5-vision",
            "collection": "resources",
            "url": "https://data.mongodb-api.com/app/data-ejhjf/endpoint/data/v1",
            "authUrl": "https://realm.mongodb.com/api/client/v2.0/app/data-ejhjf/auth/providers/api-key/login",
            "apiKey": "OIi5bAP7xxIGK782t8ZoiD2BkBGEzMdX3upChf9zdCxHSnMoiTnjI22Yw5kOSgy9",
            "isMongo": true,
        },
        "data-source-json-1": {
            "url": "path/to/json",
            "isMongo": false,
        },
        "data-source-json-2": {
            "url": "path/to/another/json",
            "isMongo": false,
        },
        // Add more data sources as needed
    }
}
```

The above example shows a gem5 resources config with a MongoDB Atlas data source and 2 JSON data sources. By default gem5 will create a union of all the resources present in all the specified data sources. If you ask to obtain a resource where multiple data sources have the same `id` and `resource_version` of the resource then an error will be thrown. You can also specify a subset of data sources to obtain resources from:

```python
resource = obtain_resource("id", clients=["data-source-json-1"])
```

### Understanding Local Resources

Local resources, in the context of gem5, pertain to resources that users possess and wish to integrate into gem5 but aren't pre-existing in the gem5 resources database.

For users, This offers the flexibility to employ their own resources seamlessly within gem5, bypassing the need to create dedicated resource objects using `BinaryResource(local_path=/path/to/binary)`. Instead, they can directly utilize these local resources through `obtain_resource()`, streamlining the integration process.

### Using Custom Resource Configuration and Local Resources

In this example, we will walk through how to set up your custom configuration and utilize your own local resources. For this illustration, we'll employ a JSON file as our resource data source.

#### Creating a Custom Resource Data Source

Let's begin by creating a local resource. This is a bare bones resource that will serve as an example. To use local resources with `obtain_resource()`, our bare bones resource need to have a binary file. Here we use an empty binary called `fake-binary`. 

**Note**: Make sure that Gem5 binary and `fake-binary` have same ISA target (RISCV here).

Next, let's create the JSON data source. I'll name the file `my-resources.json`. The contents should look like this:

```json
[
    {
        "category": "binary",
        "id": "test-binary",
        "description": "A test binary",
        "architecture": "RISCV",
        "size": 1,
        "tags": [
            "test"
        ],
        "is_zipped": false,
        "md5sum": "6d9494d22b90d817e826b0d762fda973",
        "source": "src/simple",
        "url": "file:// path to fake_binary",
        "license": "",
        "author": [],
        "source_url": "https://github.com/gem5/gem5-resources/tree/develop/src/simple",
        "resource_version": "1.0.0",
        "gem5_versions": [
            "23.0"
        ],
        "example_usage": "obtain_resource(resource_id=\"test-binary\")"
    }
]
```

The JSON file of a resource should adhere to the [gem5 resources schema](https://resources.gem5.org/gem5-resources-schema.json).

**Note**: While the `url` field can be a link, in this case, I'm using a local file.

#### Creating Your Custom Resource Configuration

Create a file named `gem5-config.json` with the following content:

```json
{
    "sources": {
        "my-json-data-source": {
            "url": "path/to/my-resources.json",
            "isMongo": false
        }
    }
}
```

**Note**: It is implied that isMongo = false means that the data source is a JSON data source as gem5 currently only supports 2 types of data sources.

#### Running gem5 with a Local Data Source

First, build gem5 with the ALL build, which contains RISCV:

```bash
scons build/ALL/gem5.opt -j`nproc`
```

Next, run the `local-resource-example.py` file using our local `test-binary` resource:

Using environment variable

```bash
GEM5_RESOURCE_JSON_APPEND=path/to/my-resources.json ./build/ALL/gem5.opt configs/example/gem5_library/local-resource-example.py --resource test-binary
```

or you can overwrite the `gem5_default_config` with our own custom config:

```bash
GEM5_CONFIG=path/to/gem5-config.json ./build/ALL/gem5.opt configs/example/gem5_library/local-resource-example.py --resource test-binary
```

This command will execute the `local-resource-example.py` script using our locally downloaded resource. This script just calls the obtain_resource function and prints the local path of the resource. This script indicates that local resources function similarly as resources on the gem5 resources database.


---


# ═══ gem5art ═══


## Zen and the art of gem5 experiments

*Source: https://www.gem5.org/documentation/gem5art/introduction*

# Zen and the art of gem5 experiments

<img src="/assets/img/gem5art/gem5art.svg" alt="gem5art-logo" width="100%" style="max-width:300px;"/>
<br/>

The gem5art project is a set of Python modules to help make it easier to run experiments with the gem5 simulator.
gem5art contains libraries for *Artifacts, Reproducibility, and Testing.*
You can think of gem5art as a structured [protocol](https://en.wikipedia.org/wiki/Protocol_(science)) for running gem5 experiments.

When running an experiment, there are inputs, steps to run the experiment, and outputs.
gem5art tracks all of these through [Artifacts](main/artifacts).
An artifact is an object, usually a file, which is used as part of the experiment.

The gem5art project contains an interface to store all of these artifacts in a [database](main/artifacts.html#artifactdb).
This database is mainly used to aid reproducibility, for instance, when you want to go back and re-run an experiment.
However, it can also be used to share artifacts with others doing similar experiments (e.g., a disk image with a shared workload).

The database is also used to store results from [gem5 runs](main/run).
Given all of the input artifacts, these runs have enough information to reproduce exactly the same experimental output.
Additionally, there is metadata associated with each gem5 run (e.g., the experiment name, the script name, script parameters, gem5 binary name, etc.) which are useful for aggregating results from many experiments.

These experimental aggregates are useful for testing gem5 as well as conducting research.
We will be using this data by aggregating the data from 100s or 1000s of gem5 experiments to determine the state of gem5's codebase at any particular time.
For instance, as discussed in the [Linux boot tutorial](tutorials/boot-tutorial), we can use this data to determine which Linux kernels, Ubuntu versions, and boot types are currently functional in gem5.

----

One of the underlying themes of gem5art is that you should fully understand each piece of the experiment you're running.
To this end, gem5art requires that every artifact for a particular experiment is *explicitly* defined.
Additionally, we encourage the use of Python scripts at every level of experimentation from the workload and disk image creation to running gem5.
By using Python scripts, you can both automate and document the processes for running your experiments.

Many of the ideas used to develop gem5art came from our experience using gem5 and the pain points of running complex experiments.
Jason Lowe-Power used gem5 extensively during his PhD at University of Wisconsin-Madison.
Through this experience, he made many mistakes and lost an untold number of days trying to reproduce experiments or re-creating artifacts that were accidentally deleted or moved.
gem5art was designed to reduce the likelihood that this happens to other researchers.


---


## Summary

*Source: https://www.gem5.org/documentation/gem5art/main/summary*

# Summary

The primary motivation behind gem5art is to provide an infrastructure to use a structured approach to run experiments with gem5. Particular goals of gem5art include:

- structured gem5 experiments
- easy to use
- resource sharing
- reproducibility
- easy to extend
- documentation of the performed experiments

gem5art is mainly composed of the following components:

- a database to store artifacts (`gem5art-artifacts`)
- python objects to wrap gem5 experiments (`gem5art-run`)
- a celery worker to manage gem5 jobs (`gem5art-tasks`)

The process of performing experiments using gem5 can quickly become complicated due to involvement of multiple components.
This can be intimidating for new users, and it can be difficult to manage even for experienced researchers.
As an example, following is a diagram which shows the interaction that takes place among different components (artifacts) while running full-system experiments with gem5.


![](/assets/img/gem5art/art.png)
<br>
*Figure: Flowchart of gem5 full system mode use case*

Each bubble in the diagram represents a different [artifact](artifacts) which is one small part of a gem5 experiment culminating in the results from the gem5 execution.
All of the lines show dependencies between artifacts (e.g., the disk image depends on the m5 binary).

You can imagine everything in this example to be contained in a base git repository (base repo) artifact which can keep track of changes in files not tracked by other repositories.
[Packer](https://packer.io) is a tool to generate disk images and serves as an input to the disk image artifact.
gem5 source code repo artifact serves as an input to two other artifacts (gem5 binary and m5 utility).
Linux source repository and base repository (specifically kernel config files) are used to build the disk image and multiple artifacts then generate the final results artifact.

gem5art serves as a tool/infrastructure to streamline this entire process and keeps track of things as they change, thus leading to reproducible runs.
Moreover, it allows to share the artifacts used in the above example, among multiple users.
Additionally, gem5art tracks results like all other artifacts, so they can be archived and queried later to aggregate many different gem5 experiments.


## Installing gem5art

gem5art is available as a PyPI package and can be installed using pip.
Since, gem5art requires Python 3, we recommend creating a virtual environment with Python 3 before using gem5art.
Run the following commands to create a virtual environment and install gem5art:

```sh
virtualenv -p python3 venv
source venv/bin/activate
pip install gem5art-artifact gem5art-run gem5art-tasks
```


---


## Artifacts

*Source: https://www.gem5.org/documentation/gem5art/main/artifacts*

# Artifacts

## gem5art artifacts

All unique objects used during gem5 experiments are termed "artifacts" in gem5art.
Examples of artifacts include: gem5 binary, gem5 source code repo, Linux kernel source repo, linux binary, disk image, and packer binary (used to build the disk image).
The goal of this infrastructure is to keep a record of all the artifacts used in a particular experiment and to return the set of used artifacts when the same experiment needs to be performed in the future.

The description of an artifact serves as the documentation of how that artifact was created.
One of the goals of gem5art is for these artifacts to be self contained.
With just the metadata stored with the artifact a third party should be able to perfectly reproduce the artifact.
(We are still working toward this goal.
For instance, we are looking into using docker to create artifacts to separate artifact creation from the host platform its run on.)

Each artifact is characterized by a set of attributes, described below:

- command: command used to build this artifact
- typ: type of the artifact e.g. binary, git repo etc.
- name: name of the artifact
- cwd: current working directory, where the command to build the artifact is run
- path: actual path of the location of the artifact
- inputs: a list of the artifacts used to build the current artifact
- documentation: a docstring explaining the purpose of the artifact and any other useful information that can help to reproduce the artifact

Additionally, each artifact also has the following implicit information.

- hash: an MD5 hash for a binary artifact or a git hash for a git artifact
- time: time of the creation of an artifact
- id: a UUID associated with the artifact
- git: a dictionary containing the origin, current commit and the repo name for a git artifact (will be an empty dictionary for other types of artifacts)

These attribute are not specified by the user, but are generated by gem5art automatically (when the `Artifact` object is created for the first time).

An example of how a user would create a gem5 binary artifact using gem5art is shown below.
In this example, the type, name, and documentation are up to the user of gem5art.
You're encouraged to use names that are easy to remember when you later query the database.
The documentation attribute should be used to completely describe the artifact that you are saving.

```python
gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = '''
      Default gem5 binary compiled for the X86 ISA.
      This was built from the main gem5 repo (github.com/gem5/gem5) without
      any modifications. We recently updated to the current gem5 master
      which has a fix for memory channel address striping.
    '''
)
```

Another goal of gem5art is to enable sharing of artifacts among multiple users, which is achieved through the use of the centralized database.
Basically, whenever a user tries to create a new artifact, the database is searched to find if the same artifact exists there.
If it does, the user can download the matching artifact for use.
Otherwise, the newly created artifact is uploaded to the database for later use.
The use of database also avoids running identical experiments (by generating an error message if a user tries to execute exact run which already exists in the database).

### Creating artifacts

To create an `Artifact`, you must use `registerArtifact` as shown in the above example as well.
This is a factory method which will initially create the artifact.

When calling `registerArtifact`, the artifact will automatically be added to the database.
If it already exists, a pointer to that artifact will be returned.

The parameters to the `registerArtifact` function are meant for *documentation*, not as explicit directions to create the artifact from scratch.
In the future, this feature may be added to gem5art.

Note: While creating new artifacts, warning messages showing that certain attributes (except hash and id) of two artifacts don't match (when artifact similarity is checked in the code) might appear. Users should make sure that they understand the reasons of any such warnings.

### Using artifacts from the database

You can create an artifact with just a UUID if it is already stored in the database.
The behavior will be the same as when creating an artifact that already exists.
All of the properties of the artifact will be populated from the database.

## ArtifactDB

The particular database used in this work is [MongoDB](https://www.mongodb.com/).
We use MongoDB since it can easily store large files (e.g., disk images), is tightly integrated with Python through [pymongo](https://api.mongodb.com/python/current/), and has an interface that is flexible as the needs of gem5art changes.

Currently, it's required to run a database to use gem5.
However, we are planning on changing this default to allow gem5art to be used standalone as well.

gem5art allows you to connect to any database, but by default assumes there is a MongoDB instance running on the localhost at `mongodb://localhost:27017`.
You can use the environment variable `GEM5ART_DB` to specify the default database to connect when running simple scripts, e.g. `GEM5ART_DB=mongodb://<remote>:27017"`.
Additionally, you can specify the location of the database when calling `getDBConnection` in your scripts.

In case no database exists or a user wants their own database, you can create a new database by creating a new directory and running the mongodb docker image.
See the [MongoDB docker documentation](https://hub.docker.com/_/mongo) or the [MongoDB documentation](https://docs.mongodb.com/) for more information.

```sh
docker run -p 27017:27017 -v <absolute path to the created directory>:/data/db --name mongo-<some tag> -d mongo
```

This uses the official [MongoDB Docker image](https://hub.docker.com/_/mongo) to run the database at the default port on the localhost.
If the Docker container is killed, it can be restarted with the same command line and the database should be consistent.

### Connecting to an existing database

By default, gem5art will assume the database is running at `mongodb://localhost:27017`, which is MongoDB's default on the localhost.

The environment variable `GEM5ART_DB` can override this default.

Otherwise, to programmatically set a database URI when using gem5art, you can pass a URI to the `getDatabaseConnection` function.

Currently, gem5art only supports MongoDB database backends, but extending this to other databases should be straightforward.

### Searching the Database

gem5art provides a few convience functions for searching and accessing the database.
These functions can be found in `artifact.common_queries`.

Specifically, we provide the following functions:

- `getByName`: Returns all objects mathching `name` in database.
- `getDiskImages`: Returns a generator of disk images (type = disk image).
- `getLinuxBinaries`: Returns a generator of Linux kernel binaries (type = kernel).
- `getgem5Binaries`: Returns a generator of gem5 binaries (type = gem5 binary).

### Downloading from the Database

You can also download a file associated with an artifact using functions provided by gem5art. A good way to search and download items from the database is by using the Python interactive shell.
You can search the database with the functions provided by the `artifact` module (e.g., `getByName`, `getByType`, etc.).
Then, once you've found the ID of the artifact you'd like to download, you can call `downloadFile`.
See the example below.

```sh
$ python
Python 3.6.8 (default, Oct  7 2019, 12:59:55)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from gem5art.artifact import *
>>> db = getDBConnection()
>>> for i in getDiskImages(db, limit=2): print(i)
...
ubuntu
    id: d4a54de8-3a1f-4d4d-9175-53c15e647afd
    type: disk image
    path: disk-image/ubuntu-image/ubuntu
    inputs: packer:fe8ba737-ffd4-44fa-88b7-9cd072f82979, fs-x86-test:94092971-4277-4d38-9e4a-495a7119a5e5, m5:69dad8b1-48d0-43dd-a538-f3196a894804
    Ubuntu with m5 binary installed and root auto login
ubuntu
    id: c54b8805-48d6-425d-ac81-9b1badba206e
    type: disk image
    path: disk-image/ubuntu-image/ubuntu
    inputs: packer:fe8ba737-ffd4-44fa-88b7-9cd072f82979, fs-x86-test:5bfaab52-7d04-49f2-8fea-c5af8a7f34a8, m5:69dad8b1-48d0-43dd-a538-f3196a894804
    Ubuntu with m5 binary installed and root auto login
>>> for i in getLinuxBinaries(db, limit=2): print(i)
...

vmlinux-5.2.3
    id: 8cfd9fbe-24d0-40b5-897e-beca3df80dd2
    type: kernel
    path: linux-stable/vmlinux-5.2.3
    inputs: fs-x86-test:94092971-4277-4d38-9e4a-495a7119a5e5, linux-stable:25feca9a-3642-458e-a179-f3705266b2fe
    Kernel binary for 5.2.3 with simple config file
vmlinux-5.2.3
    id: 9721d8c9-dc41-49ba-ab5c-3ed169e24166
    type: kernel
    path: linux-stable/vmlinux-5.2.3
    inputs: npb:85e6dd97-c946-4596-9b52-0bb145810d68, linux-stable:25feca9a-3642-458e-a179-f3705266b2fe
    Kernel binary for 5.2.3 with simple config file
>>> from uuid import UUID
>>> db.downloadFile(UUID('8cfd9fbe-24d0-40b5-897e-beca3df80dd2'), 'linux-stable/vmlinux-5.2.3')
```

For another example, assume there is a disk image named  `npb` (containing [NAS Parallel](https://www.nas.nasa.gov/) Benchmarks) in your database and you want to download the disk image to your local directory. You can do the following to download the disk image:

```python
import gem5art.artifact

db = gem5art.artifact.getDBConnection()

disks = gem5art.artifact.getByName(db, 'npb')

for disk in disks:
    if disk.type == 'disk image' and disk.documentation == 'npb disk image created on Nov 20':
        db.downloadFile(disk._id, 'npb')
```

Here, we assume that there can be multiple disk images/artifacts with the name `npb` and we are only interested in downloading the npb disk image with a particular documentation ('npb disk image created on Nov 20'). Also, note that there are other ways to download files from the database (although they will eventually use the `downloadFile` function).

The dual of the `downloadFile` method used above is `upload`.

#### Database schema

Alternative, you can use the pymongo Python module or the mongodb command line interface to interact with the database.
See the [MongoDB documentation](https://docs.mongodb.com/) for more information on how to query the MongoDB database.

gem5art has two collections.
`artifact_database.artifacts` stores all of the metadata for the artifacts and `artifact_database.fs` is a [GridFS](https://docs.mongodb.com/manual/core/gridfs/) store for all of the files.
The files in the GridFS use the same UUIDs as the Artifacts as their primary keys.

You can list all of the details of all of the artifacts by running the following in Python.

```python
#!/usr/bin/env python3

from pymongo import MongoClient

db = MongoClient().artifact_database
for i in db.artifacts.find():
    print(i)
```

gem5art also provides a few methods to search the database for artifacts of a particular type or name. For example, to find all disk images in a database you can do the following:

```python
import gem5art.artifact
db = gem5art.artifact.getDBConnection('mongodb://localhost')
for i in gem5art.artifact.getDiskImages(db):
    print(i)
```

Other similar methods include: `getLinuxBinaries()`, `getgem5Binaries()`

You can use getByName() method to search database for artifacts using the name attribute. For example, to search for gem5 named artifacts:

```python
import gem5art.artifact
db = gem5art.artifact.getDBConnection('mongodb://localhost')
for i in gem5art.artifact.getByName(db, "gem5"):
    print(i)
```


---


## Runs

*Source: https://www.gem5.org/documentation/gem5art/main/run*

# Run

## Introduction

Each gem5 experiment is wrapped inside a run object.
These run objects contain all of the information required to execute the gem5 experiments and can optionally be executed via the gem5art tasks library (or manually with the `run()` function.). gem5Run interacts with the Artifact class of gem5art to ensure reproducibility of gem5 experiments and also stores the current gem5Run object and the output results in the database for later analysis.

## SE and FS mode runs

Next are two methods (for SE (system-emulation) and FS (full-system) modes of gem5) from gem5Run class which give an idea of the required arguments from a user's perspective to create a gem5Run object:

```python

@classmethod
def createSERun(cls,
                name: str,
                gem5_binary: str,
                run_script: str,
                outdir: str,
                gem5_artifact: Artifact,
                gem5_git_artifact: Artifact,
                run_script_git_artifact: Artifact,
                *params: str,
                timeout: int = 60*15) -> 'gem5Run':
.......


@classmethod
def createFSRun(cls,
                name: str,
                gem5_binary: str,
                run_script: str,
                outdir: str,
                gem5_artifact: Artifact,
                gem5_git_artifact: Artifact,
                run_script_git_artifact: Artifact,
                linux_binary: str,
                disk_image: str,
                linux_binary_artifact: Artifact,
                disk_image_artifact: Artifact,
                *params: str,
                timeout: int = 60*15) -> 'gem5Run':
.......

```

For the user it is important to understand different arguments passed to run objects:

- `name`: name of the run, can act as a tag to search the database to find the required runs (it is expected that user will use a unique name for different experiments)
- `gem5_binary`: path to the actual gem5 binary to be used
- `run_script`: path to the python run script that will be used with gem5 binary
- `outdir`: path to the directory where gem5 results should be written
- `gem5_artifact`: gem5 binary git artifact object
- `gem5_git_artifact`: gem5 source git repo artifact object
- `run_script_git_artifact`: run script artifact object
- `linux_binary` (only full-system): path to the actual linux binary to be used (used by run script as well)
- `disk_image` (only full-system): path to the actual disk image to be used (used by run script as well)
- `linux_binary_artifact` (only full-system): linux binary artifact object
- `disk_image_artifact` (only full-system): disk image artifact object
- `params`: other params to be passed to the run script
- `timeout`: longest time in seconds for which the current gem5 job is allowed to execute

The artifact parameters (`gem5_artifact`, `gem5_git_artifact`, and `run_script_git_artifact`) are used to ensure this is reproducible run.
Apart from the above mentioned parameters, gem5Run class also keeps track of other features of a gem5 run e.g., the start time, the end time, the current status of gem5 run, the kill reason (if the run is finished), etc.

While the user can write their own run script to use with gem5 (with any command line arguments), currently when a `gem5Run` object is created for a full-system experiment using `createFSRun` method, it is assumed that the path to the `linux_binary` and `disk_image` is passed to the run script on the command line (as arguments of the `createFSRun` method).

## Running an experiment

The `gem5Run` object has everything needed to run one gem5 execution.
Normally, this will be performed by using the gem5art *tasks* package.
However, it is also possible to manually execute a gem5 run.

The `run` function executes the gem5 experiment.
It takes two optional parameters: a task associated with the run for bookkeeping and an optional directory to execute the run in.

The `run` function executes the gem5 binary by using `Popen`.
This creates another process to execute gem5.
The `run` function is *blocking* and does not return until the child process has completed.

While the child process is running, every 5 seconds the parent python process will update the status in the `info.json` file.

The `info.json` file is the serialized `gem5run` object which contains all of the run information and the current status.

`gem5Run` objects have 7 possible status states.
These are currently simple strings stored in the `status` property.

- `Created`: The run has been created. This is set in the constructor when either `createSRRun` or `createFSRun` is called.
- `Begin run`: When `run()` is called, after the database is checked, we enter the `Begin run` state.
- `Failed artifact check for ...`: The status is set to this when the artifact check fails.
- `Spawning`: Next, just before `Popen` is called, the run enters the `Spawning` state.
- `Running`: Once the parent process begins spinning waiting for the child to finish, the run enters the `Running` state.
- `Finished`: When the child finished with exit code `0`, the run enters the `Finished` state.
- `Failed`: When the child finished with a non-zero exit code, the run enters the `Failed` state.

## Run Already in the Database

When starting a run with gem5art, it might complain that the run already exists in the database.
Basically, before launching a gem5 job, gem5art checks if this run matches an existing run in the database.
In order to uniquely identify a run, a single hash is made out of:

- the runscript
- the parameters passed to the runscript
- the artifacts of the run object which, for an SE run, include: gem5 binary artifact, gem5 source git artifact, run script (experiments repo) artifact. For an FS run, the list of artifacts also include linux binary artifact and disk image artifacts in addition to the artifacts of an SE run.

If this hash already exists in the database, gem5art will not launch a new job based on this run object as a run with same parameters would have already been executed.
In case, user still wants to launch this job, the user will have to remove the existing run object from the database.

## Searching the Database to find Runs

### Utility script

gem5art provides the utility `gem5art-getruns` to search the database and retrieve runs.
Based on the parameters, `gem5art-getruns` will dump the results into a file in the json format.

```
usage: gem5art-getruns [-h] [--fs-only] [--limit LIMIT] [--db-uri DB_URI]
                       [-s SEARCH_NAME]
                       filename

Dump all runs from the database into a json file

positional arguments:
  filename              Output file name

optional arguments:
  -h, --help            show this help message and exit
  --fs-only             Only output FS runs
  --limit LIMIT         Limit of the number of runs to return. Default: all
  --db-uri DB_URI       The database to connect to. Default
                        mongodb://localhost:27017
  -s SEARCH_NAME, --search_name SEARCH_NAME
                        Query for the name field
```

### Manually searching the database

Once you start running the experiments with gem5 and want to know the status of those runs, you can look at the gem5Run artifacts in the database.
For this purpose, gem5art provides a method `getRuns`, which you can use as follows:

```python
import gem5art.run
from gem5art.artifact import getDBConnection
db = getDBConnection()
for i in gem5art.run.getRuns(db, fs_only=False, limit=100):
    print(i)
```

## Searching the Database to find Runs with Specific Names

As discussed above, while creating a FS or SE mode Run object, the user has to pass a name field to recognize
a particular set of runs (or experiments).
We expect that the user will take care to use a name string which fully characterizes a set of experiments and can be thought of as a `Nonce`.
For example, if we are running experiments to test linux kernel boot on gem5, we can use a name field `boot_tests_v1` or `boot_tests_[month_year]` (where month_year correspond to the month and year when the experiments were run).

Later on, the same name can be used to search for relevant gem5 runs in the database.
For this purpose, gem5art provides a method `getRunsByName`, which can be used as follow:

```python
import gem5art.run
from gem5art.artifact import getDBConnection
db = getDBConnection()
for i in gem5art.run.getRunsByName(db, name='boot_tests_v1', fs_only=True, limit=100):
    print(i)
```


---


## Tasks

*Source: https://www.gem5.org/documentation/gem5art/main/tasks*

# Tasks

This package contains two parallel task libraries for running gem5 experiments.
The actual gem5 experiment can be executed with the help of [Python multiprocessing support](https://docs.python.org/3/library/multiprocessing.html), [Celery](http://www.celeryproject.org/) or even without using any job manager (a job can be directly launched by calling `run()` function of gem5Run object).
This package implicitly depends on the gem5art run package.

Please cite the the [gem5art paper](https://arch.cs.ucdavis.edu/papers/2021-3-28-gem5art) when using the gem5art packages.
This documentation can be found on the [gem5 website](http://www.gem5.org/documentation/gem5art/).

## Use of Python Multiprocessing

This is a simple way to run gem5 jobs using Python multiprocessing library.
You can use the following function in your job launch script to execute gem5art run objects:

```python
run_job_pool([a list containing all run objects to execute], num_parallel_jobs = [Number of parallel jobs])
```

## Use of Celery

Celery server can run many gem5 tasks asynchronously.
Once a user creates a gem5Run object (discussed previously) while using gem5art, this object needs to be passed to a method `run_gem5_instance()` registered with Celery app, which is responsible for starting a Celery task to run gem5. The other argument needed by the `run_gem5_instance()` is the current working directory.

Celery server can be started with the following command:

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

This will start a server with events enabled that will accept gem5 tasks as defined in gem5art.
It will autoscale from 0 to desired number of workers.

Celery relies on a message broker `RabbitMQ` for communication between the client and workers.
If not already installed, you need to install `RabbitMQ` on your system (before running celery) using:

```sh
apt-get install rabbitmq-server
```

### Monitoring Celery

Celery does not explicitly show the status of the runs by default.
[flower](https://flower.readthedocs.io/en/latest/), a Python package, is a web-based tool for monitoring and administrating Celery.

To install the flower package,
```sh
pip install flower
```

You can monitor the celery cluster doing the following:

```sh
flower -A gem5art.tasks.celery --port=5555
```
This will start a webserver on port 5555.

### Removing all tasks

```sh
celery -A gem5art.tasks.celery purge
```

### Viewing state of all jobs in celery

```sh
celery -A gem5art.tasks.celery events
```


---


## Disk Images

*Source: https://www.gem5.org/documentation/gem5art/main/disks*

# Disk Images

## Introduction
This section discusses an automated way of creating gem5-compatible disk images with Ubuntu server installed. We make use of [Packer](https://www.packer.io/) which uses .json template files to build and configure a disk image. These template files can be configured to build a disk image with specific benchmarks installed.

## Building a Simple Disk Image with Packer
<a name="packerbriefly"></a>
### a. How It Works, Briefly
We use [Packer](https://www.packer.io/) and [QEMU](https://www.qemu.org/) to automate the process of disk creation.
Essentially, QEMU is responsible for setting up a virtual machine and all interactions with the disk image during the building process.
The interactions include installing Ubuntu Server to the disk image, copying files from your machine to the disk image, and running scripts on the disk image after Ubuntu is installed.
However, we will not use QEMU directly.
Packer provides a simpler way to interact with QEMU using a JSON script, which is more expressive than using QEMU from command line.
<a name="dependencies"></a>
### b. Install Required Software/Dependencies
If not already installed, QEMU can be installed using:
```shell
sudo apt-get install qemu
```
The packer binary can be downloaded from [the official website](https://www.packer.io/downloads.html).
For example, the following command downloads packer version 1.7.2 for Linux platforms,

```sh
wget https://releases.hashicorp.com/packer/1.7.2/packer_1.7.2_linux_amd64.zip
unzip packer_1.7.2_linux_amd64.zip
```

<a name="customizing"></a>
### c. Customize the Packer Script
The default packer script `template.json` should be modified and adapted according to the required disk image and the available resources for the build process. We will rename the default template to `[disk-name].json`. The variables that should be modified appear at the end of `[disk-name].json` file, in `variables` section.
The configuration files that we use to build the disk image, and the directory structure is shown below:
```shell
disk-image/
  experiment-specific-folder/
    [disk-name].json: packer script
    Any experiment-specific post installation script

  shared/
    post-installation.sh: generic shell script that is executed after Ubuntu is installed
    preseed.cfg: pre-seeded configuration to install Ubuntu
```

<a name="customizingVM"></a>
#### i. Customizing the VM (Virtual Machine)
In `[disk-name].json`, following variables are available to customize the VM (to be used for the disk building process):

| Variable         | Purpose     | Example  |
| ---------------- |-------------|----------|
| [vm_cpus](https://www.packer.io/docs/builders/qemu.html#cpus) **(should be modified)** | number of host CPUs used by VM | "2": 2 CPUs are used by the VM |
| [vm_memory](https://www.packer.io/docs/builders/qemu.html#memory) **(should be modified)** | amount of memory used by VM, in megabytes | "2048": 2 GB of RAM are used by the VM |
| [vm_accelerator](https://www.packer.io/docs/builders/qemu.html#accelerator) **(should be modified)** | accelerator used by the VM, e.g. kvm | "kvm": kvm will be used |

<a name="customizingscripts"></a>
#### ii. Customizing the Disk Image
In `[disk-name].json`, disk image size can be customized using following variable:

| Variable        | Purpose     | Example  |
| ---------------- |-------------|----------|
| [image_size](https://www.packer.io/docs/builders/qemu.html#disk_size) **(should be modified)** | size of the disk image, in megabytes | "8192": the image has the size of 8 GB  |
| [image_name] | name of the built disk image | "boot-exit"  |




<a name="customizingscripts2"></a>
#### iii. File Transfer
While building a disk image, users would need to move their files (benchmarks, data sets etc.) to
the disk image. In order to do this file transfer, in `[disk-name].json` under `provisioners`, you could add the following:

```shell
{
    "type": "file",
    "source": "shared/post_installation.sh",
    "destination": "/home/gem5/",
    "direction": "upload"
}
```
The above example copies the file `shared/post_installation.sh` from the host to `/home/gem5/` in the disk image.
This method is also capable of copying a folder from host to the disk image and vice versa.
It is important to note that the trailing slash affects the copying process [(more details)](https://www.packer.io/docs/provisioners/file.html#directory-uploads).
The following are some notable examples of the effect of using slash at the end of the paths.

| `source`        | `destination`     | `direction`  |  `Effect`  |
| ---------------- |-------------|----------|-----|
| `foo.txt` | `/home/gem5/bar.txt` | `upload` | copy file (host) to file (image) |
| `foo.txt` | `bar/` | `upload` | copy file (host) to folder (image) |
| `/foo` | `/tmp` | `upload` | `mkdir /tmp/foo` (image);  `cp -r /foo/* (host) /tmp/foo/ (image)`; |
| `/foo/` | `/tmp` | `upload` | `cp -r /foo/* (host) /tmp/ (image)` |

If `direction` is `download`, the files will be copied from the image to the host.
**Note**: [This is a way to run script once after installing Ubuntu without copying to the disk image](#customizingscripts3).

<a name="customizingscripts3"></a>
#### iv. Install ing Benchmark Dependencies
To install the dependencies, we utilize the bash script `shared/post_installation.sh`, which will be run after the Ubuntu installation and file copying is done.
For example, if we want to install `gfortran`, add the following in `scripts/post_installation.sh`:
```shell
echo '12345' | sudo apt-get install gfortran;
```
In the above example, we assume that the user password is `12345`.
This is essentially a bash script that is executed on the VM after the file copying is done, you could modify the script as a bash script to fit any purpose.
<a name="customizingscripts4"></a>
#### v. Running Other Scripts on Disk Image
In `[disk-name].json`, we could add more scripts to `provisioners`.
Note that the files are on the host, but the effects are on the disk image.
For example, the following example runs `shared/post_installation.sh` after Ubuntu is installed,

{% raw %}
```shell
{
    "type": "shell",
    "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
    "scripts":
    [
        "scripts/post-installation.sh"
    ]
}
```
{% endraw %}

<a name="buildsimple"></a>
### d. Building the Disk Image
<a name="simplebuild"></a>
#### i. Building the Disk Image
In order to build a disk image, the template file is first validated using:
```sh
./packer validate [disk-name].json
```
Then, the template file can be used to build the disk image:
```sh
./packer build [disk-name].json
```

On a fairly recent machine, the building process should not take more than 15 minutes to complete.
The disk image with the user-defined name (image_name) will be produced in a folder called [image_name]-image.
[We recommend to use a VNC viewer in order to inspect the building process](#inspect).
<a name="inspect"></a>
#### ii. Inspecting the Building Process
While the building process of disk image takes place, packer will run a VNC (Virtual Network Computing) server and you will be able to see the building process by connecting to the VNC server from a VNC client. There are a plenty of choices for VNC client. When you run the packer script, it will tell you which port is used by the VNC server. For example, if it says `qemu: Connecting to VM via VNC (127.0.0.1:5932)`, the VNC port is 5932.
To connect to VNC server from the VNC client, use the address `127.0.0.1:5932` for a port number 5932.
If you need port forwarding to forward the VNC port from a remote machine to your local machine, use SSH tunneling
```shell
ssh -L 5932:127.0.0.1:5932 <username>@<host>
```
This command will forward port 5932 from the host machine to your machine, and then you will be able to connect to the VNC server using the address `127.0.0.1:5932` from your VNC viewer.

**Note**: While packer is installing Ubuntu, the terminal screen will display "waiting for SSH" without any update for a long time.
This is not an indicator of whether the Ubuntu installation produces any errors.
Therefore, we strongly recommend using VNC viewer at least once to inspect the image building process.
<a name="checking"></a>


---


## FAQ

*Source: https://www.gem5.org/documentation/gem5art/main/faq*

# Frequently Asked Questions

**What is gem5art?**

gem5art (libraries for artifacts, reproducibility and testing) is a set of python modules to do experiments with gem5 in a reproducible and structured way.

**Do I need celery to run gem5 jobs using gem5art?**

Celery is not required to run gem5 jobs with gem5art.
You can use any other job scheduling tool or no tool at all.
In order to run your job without celery, simply call the run() method of your run object once it is created.
For example, assuming created run object (in a launch script) is called run, you can do the following:

```python
run.run()
```

**Is there a more user-friendly way to launch gem5 jobs?**

You can use python multiprocessing library based function calls (provided by gem5art) to launch multiple gem5 jobs in parallel.
Specifically, you can call the following function in your gem5art launch script:

```python
run_job_pool([a list containing all run objects to execute], num_parallel_jobs = [Number of parralel jobs])
```

**How to access/search the files/artifacts in the database?**

You can use the pymongo API functions to access the files in the database.
gem5art also provides methods that make it easy to access the entries in the database.
You can look at the different available methods [here](artifacts.html#searching-the-database).

**What if I want to re-run an experiment, using the same artifacts?**

As explained in the documentation, when a new run object is created in the launch script,
a hash is created out of the artifacts that this run is dependent on.
This hash is used to check if a the same run exists in the database.
One of the artifacts used to create the hash is runscript artifact (which basically is same as
experiments repository artifact, as gem5 configuration scripts are part of the base experiments
repository).
The easiest way to re-run an experiment is to update the name field of your launch script and commit the changes
in the launch script to the base experiments repository.
Make sure to use the new name field to query the results or runs in the database.

**How can I monitor the status of jobs launched using gem5art launch script?**

Celery does not explicitly show the status of the runs by default.
[flower](https://flower.readthedocs.io/en/latest/), a Python package, is a web-based tool for monitoring and administrating Celery.

To install the flower package,
```sh
pip install flower
```

If you are using celery to run your tasks, you can use celery monitoring tool called flower.
For this purpose, use the following command:

```sh
flower -A gem5art.tasks.celery --port=5555
```

You can access this server on your web browser using `http://localhost:5555`.

Celery also generates some log files in the directory where you are running celery from.
You can also look at those log files to know the status of your jobs.

**How to contribute to gem5art?**

gem5art is open-source.
If you want to add a new feature or fix a bug, you can create a PR on the gem5art github repo.


---


## Boot Tutorial

*Source: https://www.gem5.org/documentation/gem5art/tutorials/boot-tutorial*

# Tutorial: Run Full System Linux Boot Tests

## Introduction
This tutorial explains how to use gem5art to run experiments with gem5. The specific experiment we will be doing is to test booting of various linux kernel versions and simulator configurations.
The main steps to perform such an experiment using gem5art include: setting up the environment, building gem5, creating a disk image, compiling linux kernels, preparing gem5 run script, creating a job launch script (which will also register all of the required artifacts) and finally running this script.

We assume the following directory structure to follow in this tutorial:

```
boot-tests/
  |___ gem5/                                   # gem5 source code
  |
  |___ disk-image/
  |      |___ shared/                          # Auxiliary files needed for disk creation
  |      |___ boot-exit/
  |            |___ boot-exit-image/           # Will be created once the disk is generated
  |            |      |___ boot-exit           # The generated disk image
  |            |___ boot-exit.json             # The Packer script
  |            |___ exit.sh                    # Exits the simulated guest upon booting
  |            |___ post-installation.sh       # Moves exit.sh to guest's .bashrc
  |
  |___ configs
  |      |___ system                           # gem5 system config files
  |      |___ run_exit.py                      # gem5 run script
  |
  |___ linux-configs                           # Folder with Linux kernel configuration files
  |
  |___ linux                                   # Linux source will be downloaded in this folder
  |
  |___ launch_boot_tests.py                    # script to launch jobs and register artifacts
```

## Setting up the environment

First, we need to create the primary directory **boot-tests** which will contain all the created artifacts to run these tests.
This directory also needs to be converted into a git repository.
Through the use of boot-tests git repo, we will try to keep track of changes in those files which are not an artifact themselves or not a part of any other artifact.
An example of such files is gem5 run and config scripts (config-boot-tests).
We want to make sure that we can keep record of any changes in these scripts, so that a particular run of gem5 can be associated with a particular snapshot of these files.
All such files, which are not part of other artifacts, will be a part of the experiments repo artifact (we will show how to register that artifact later in this tutorial).
We also need to add a git remote to this repository pointing to a remote location where we want this repository to be hosted.

Create the main directory named boot-tests and turn it into a git repo:

```sh
mkdir boot-tests
cd boot-tests
git init
git remote add origin https://your-remote-add/boot-tests.git
```

We also need to add a .gitignore file in our git repo, to ignore tracking files we don't care about:

```sh
*.pyc
m5out
.vscode
results
venv
disk-image/packer
disk-image/packer_1.4.3_linux_amd64.zip
disk-image/boot-exit/boot-exit-image/boot-exit
disk-image/packer_cache
gem5
linux-stable/
```

gem5art relies on Python 3, so we suggest creating a virtual environment (inside boot-tests) before using gem5art.

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

gem5art can be installed (if not already) using pip:

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

## Building gem5

Next, we have to clone gem5 and build it. If you want to use the exact gem5 source that was used at the time of creating this tutorial you will have to checkout the relevant commit. If you want to try with the current version of gem5 at the time of reading this tutorial, you can ignore the git checkout command.
See the commands below:

```sh
git clone https://github.com/gem5/gem5
cd gem5
git checkout v20.1.0.0
scons build/X86/gem5.opt -j8
```
You can also add your changes to gem5 source before building it. Make sure to commit any changes you make to gem5 repo and documenting it while registering gem5 artifact in the launch script.
We will look at the details of our launch script later on, but following is how we can register gem5 source and binary artifacts that we just created.

```python
gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/gem5/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 from github and checked out v20.1.0.0'
)

gem5_binary = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/X86/gem5.opt -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)
```

Note, that the use of git checkout command in the `command` field of the gem5_binary artifact (along with the `documentation` field) will be helpful later on to figure out exactly which gem5 source was used to create this gem5 binary.

Also make sure to build the m5 utility at this point which will be moved to the disk image eventually.
m5 utility allows to trigger simulation tasks from inside the simulated system.
For example, it can be used to dump simulation statistics when the simulated system triggers to do so.
We will mainly need m5 to exit the simulation when the simulated system boots linux.

```sh
cd gem5/util/m5/
scons build/x86/out/m5
```

## Creating a disk image
First create a disk-image folder where we will keep all disk image related files:

```sh
mkdir disk-image
```

We will follow the similar directory structure as discussed in [Disk Images](../main/disks) section.
Add a folder named shared for config files which will be shared among all disk images (and will be kept to their defaults) and one folder named boot-exit which is specific to the disk image needed to run experiments of this tutorial.
Add three files [boot-exit.json](https://github.com/darchr/gem5art/blob/master/docs/disks/boot-exit/boot-exit.json), [exit.sh](https://github.com/darchr/gem5art/blob/master/docs/disks/boot-exit/exit.sh) and [post-installation.sh](https://github.com/darchr/gem5art/blob/master/docs/disks/boot-exit/post-installation.sh) in boot-exit/ and [preseed.cfg](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/preseed.cfg) and [serial-getty@.service](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/serial-getty@.service) in shared/.

**boot-exit.json** is our primary configuration file. The provisioners and variables section of this file configure the files that need to be transferred to the disk and other things like disk image's name. **post-installation.sh** (which is a script to run after Ubuntu is installed on the disk image) makes sure that the m5 binary is installed on the system and also moves the contents of our other script (**exit.sh**, which should be already transferred inside the disk image as configured in **boot-exit.json**) to **.bashrc** as **exit.sh** contains the stuff that we want to be executed as soon as the system boots. **exit.sh** just contains one command `m5 exit`, which will eventually terminate the simulation as the system boots up.

Next, download packer (if not already downloaded) in the disk-image folder:

```
cd disk-image/
wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip
unzip packer_1.4.3_linux_amd64.zip
```
Now, to build the disk image, inside the disk-image folder, run:

```
./packer validate boot-exit/boot-exit.json

./packer build boot-exit/boot-exit.json
```

Once this process succeeds, the disk image can be found on `boot-exit/boot-exit-image/boot-exit`.
A similar disk image already created following the above instructions can be found, gzipped, [here](http://dist.gem5.org/dist/v21-2/images/x86/ubuntu-18-04/x86-ubuntu.img.gz).


## Compiling the linux kernel

In this tutorial, we want to experiment with different linux kernels to examine the state of gem5's ability to boot different linux kernels. These tests use following five LTS (long term support) releases of the Linux kernel:

- 4.4.186
- 4.9.186
- 4.14.134
- 4.19.83
- 5.4.49


Let's use an example of kernel v5.4.49 to see how to compile the kernel.
First, add a folder linux-configs to store linux kernel config files. The configuration files of interest are available [here](https://github.com/gem5/gem5-resources/tree/stable/src/linux-kernel).
Then, we will get the linux source and checkout the required linux version (e.g. v5.4.49 in this case).

```
git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
mv linux linux-stable
cd linux-stable
git checkout v{version-no: e.g. 5.4.49}
```
Compile the Linux kernel from its source (using an appropriate config file from linux-configs/):

```
cp ../linux-configs/config.{version-no: e.g. 5.4.49} .config
make -j8
cp vmlinux vmlinux-{version-no: e.g. 5.4.49}
```

Repeat the above process for other kernel versions that we want to use in this experiment.

**Note:** The above instructions are tested with `gcc 7.5.0` and the already compiled Linux binaries can be downloaded from the following links:

- [vmlinux-4.4.186](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.4.186)
- [vmlinux-4.9.186](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.9.186)
- [vmlinux-4.14.134](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.14.134)
- [vmlinux-4.19.83](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.19.83)
- [vmlinux-5.4.49](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-5.4.49)


## gem5 run scripts

Next, we need to add gem5 run scripts. We will do that in a folder named configs-boot-tests.
Get the run script named run_exit.py from [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/x86-ubuntu/configs/run_exit.py), and other system configuration files from
[here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/x86-ubuntu/configs/system).
The run script (run_exit.py) takes the following arguments:
- kernel: compiled kernel to be used for simulation
- disk: built disk image to be used for simulation
- cpu_type: gem5 cpu model (KVM, atomic, timing or O3)
- mem_sys: gem5 memory system (`classic`, `MI_example`, `MESI_Two_Level`, `MOESI_CMP_directory`)
- num_cpus: number of parallel cpus to be simulated
- boot_type: linux kernel boot type (with init or systemd)

An example use of this script is the following:

```sh
gem5/build/X86/gem5.opt configs/run_exit.py [path to the Linux kernel] [path to the disk image] kvm classic 4 init
```

## Database and Celery Server

If not already running/created, you can create a database using:

```sh
`docker run -p 27017:27017 -v <absolute path to the created directory>:/data/db --name mongo-<some tag> -d mongo`
```
in a newly created directory.

If not already installed, install `RabbitMQ` on your system (before running celery) using:

```sh
apt-get install rabbitmq-server
```

Now, run celery server using:

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

**Note:** Celery is not required to run gem5 jobs with gem5art. You can also use python multiprocessing library based function calls (provided by gem5art) to launch these jobs in parallel (we will show how to do that later in our launch script).

## Creating a launch script
Finally, we will create a launch script with the name **launch_boot_tests.py**, which will be responsible for registering the artifacts to be used for these tests and then launching gem5 jobs.

The first thing to do in the launch script is to import required modules and classes:

```python
import os
import sys
from uuid import UUID
from itertools import starmap
from itertools import product

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
import multiprocessing as mp
```
Next, we will register artifacts. For example, to register packer artifact we will add the following lines:

```python
packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August/19 from hashicorp.'
)
```

For our boot-tests repo,

```python
experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/boot_tests.git',
    typ = 'git repo',
    name = 'boot_tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run full system boot tests with gem5 20.1'
)
```

Note that the name of the artifact (returned by the registerArtifact method) is totally up to the user as well as most of the other attributes of these artifacts.

For all other artifacts, add following lines in launch_boot_tests.py:

```python

gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/gem5/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 from github and checked out v20.1.0.0'
)

m5_binary = Artifact.registerArtifact(
    command = 'scons build/x86/out/m5',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/build/x86/out/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

disk_image = Artifact.registerArtifact(
    command = './packer build boot-exit/boot-exit.json',
    typ = 'disk image',
    name = 'boot-disk',
    cwd = 'disk-image',
    path = 'disk-image/boot-exit/boot-exit-image/boot-exit',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu with m5 binary installed and root auto login'
)

gem5_binary = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/X86/gem5.opt -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)

gem5_binary_MESI_Two_Level = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/X86_MESI_Two_Level/gem5.opt --default=X86 PROTOCOL=MESI_Two_Level SLICC_HTML=True -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86_MESI_Two_Level/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)

gem5_binary_MOESI_CMP_directory = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/MOESI_CMP_directory/gem5.opt --default=X86 PROTOCOL=MOESI_CMP_directory -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86_MOESI_CMP_directory/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)

linux_repo = Artifact.registerArtifact(
    command = '''git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo from June 24-2020'
)

linuxes = ['5.4.49', '4.19.83', '4.14.134', '4.9.186', '4.4.186']
linux_binaries = {
    version: Artifact.registerArtifact(
                name = f'vmlinux-{version}',
                typ = 'kernel',
                path = f'linux-stable/vmlinux-{version}',
                cwd = 'linux-stable/',
                command = f'''cd linux-stable;
                git checkout v{version};
                cp ../linux-configs/config.{version} .config;
                make -j8;
                cp vmlinux vmlinux-{version};
                ''',
                inputs = [experiments_repo, linux_repo,],
                documentation = f"Kernel binary for {version} with simple "
                                 "config file",
            )
    for version in linuxes
}
```

Once, all the artifacts are registered the next step is to launch all gem5 jobs. To do that, first we will create a method `createRun` to create gem5art runs based on a few arguments:

```python
def createRun(linux, boot_type, cpu, num_cpu, mem):

    if mem == 'MESI_Two_Level':
        binary_gem5 = 'gem5/build/X86_MESI_Two_Level/gem5.opt'
        artifact_gem5 = gem5_binary_MESI_Two_Level
    elif mem == 'MOESI_CMP_directory':
        binary_gem5 = 'gem5/build/MOESI_CMP_directory/gem5.opt'
        artifact_gem5 = gem5_binary_MOESI_CMP_directory
    else:
        binary_gem5 = 'gem5/build/X86/gem5.opt'
        artifact_gem5 = gem5_binary

    return gem5Run.createFSRun(
        'boot experiments with gem5-20.1',
        binary_gem5,
        'configs-boot-tests/run_exit.py',
        'results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.
            format(linux, cpu, mem, num_cpu, boot_type),
        artifact_gem5, gem5_repo, experiments_repo,
        os.path.join('linux-stable', 'vmlinux'+'-'+linux),
        'disk-image/boot-exit/boot-exit-image/boot-exit',
        linux_binaries[linux], disk_image,
        cpu, mem, num_cpu, boot_type,
        timeout = 10*60*60 #10 hours
        )
```

Next, initialize all the parameters to pass to `createRun` method, depending on the configuration space we want to test:

```python
if __name__ == "__main__":
    boot_types = ['init']
    num_cpus = ['1', '2', '4', '8']
    cpu_types = ['kvm', 'atomic', 'simple', 'o3']
    mem_types = ['MI_example', 'MESI_Two_Level', 'MOESI_CMP_directory']
```

Then, to run actual jobs depending on if you want to use celery or python multiprocessing library, add the following in your launch script:

## If Using Celery

```python
    # For the cross product of tests, create a run object.
    runs = starmap(createRun, product(linuxes, boot_types, cpu_types, num_cpus, mem_types))
    # Run all of these experiments in parallel
    for run in runs:
        run_gem5_instance.apply_async((run, os.getcwd(),))
```

## If Using Python Multiprocessing Library:

```python
    def worker(run):
        run.run()
        json = run.dumpsJson()
        print(json)

    jobs = []
    # For the cross product of tests, create a run object.
    runs = starmap(createRun, product(linuxes, boot_types, cpu_types, num_cpus, mem_types))
    # Run all of these experiments in parallel
    for run in runs:
        jobs.append(run)

    with mp.Pool(mp.cpu_count() // 2) as pool:
         pool.map(worker, jobs)
```

The above lines are responsible for looping through all possible combinations of variables involved in this experiment.
For each combination, a gem5Run object is created and eventually passed to run_gem5_instance to be executed asynchronously if using Celery.
In case of python multiprocessing library, these run objects are pushed to a list and then mapped to a job pool.
Look at the definition of `createFSRun()` [here](../main/run.html) to understand the use of passed arguments.

Here, we are using a timeout of 10 hours, after which the particular gem5 job will be killed (assuming that gem5 should complete the booting process of linux kernel on the given hardware resources). You can configure this time according to your settings.

The complete launch script is available [here:](https://github.com/darchr/gem5art/blob/master/docs/launch-scripts/launch_boot_tests.py).
Finally, make sure you are in python virtual env and then run the script:

```python
python launch_boot_tests.py
```

## Results

Once you start running these experiments, you can access the database to check their status or to find results.
There are different ways to do this. For example, you can use the getRuns method of gem5art as discussed in the Runs section [previously](../main/run.html#searching-the-database-to-find-runs).

You can also directly access the database and access the run artifacts as follows:

```python

#!/usr/bin/env python3
from pymongo import MongoClient

db = MongoClient().artifact_database

linuxes = ['5.4.49', '4.19.83', '4.14.134', '4.9.186', '4.4.186']
boot_types = ['init']
num_cpus = ['1', '2', '4', '8']
cpu_types = ['kvm', 'atomic', 'simple', 'o3']
mem_types = ['MI_example', 'MESI_Two_Level', 'MOESI_CMP_directory']

for linux in linuxes:
    for boot_type in boot_types:
        for cpu in cpu_types:
            for num_cpu in num_cpus:
                for mem in mem_types:
                    for i in db.artifacts.find({'outdir':'/home/username/boot_tests/results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.format(linux, cpu, mem, num_cpu, boot_type)}):print(i)
```

**Note:** Update the "outdir" path in the above lines of code to where your results are stored in your system.

Following plots show the status of linux booting based on the results of the experiments of this tutorial:

![](/assets/img/gem5art//boot_exit_classic_init.svg)
![](/assets/img/gem5art//boot_exit_classic_systemd.svg)
![](/assets/img/gem5art//boot_exit_MI_example_init.svg)
![](/assets/img/gem5art//boot_exit_MI_example_systemd.svg)
![](/assets/img/gem5art//boot_exit_MESI_Two_Level_init.svg)
![](/assets/img/gem5art//boot_exit_MESI_Two_Level_systemd.svg)

You can look [here](https://www.gem5.org/documentation/benchmark_status/gem5-20) for the latest status of these tests on gem5.


---


## NPB Tutorial

*Source: https://www.gem5.org/documentation/gem5art/tutorials/npb-tutorial*

# Tutorial: Run NAS Parallel Benchmarks with gem5

## Introduction
In this tutorial, we will use gem5art to create a disk image for NAS parallel benchmarks ([NPB](https://www.nas.nasa.gov/)) and then run these benchmarks using gem5. NPB belongs to the category of high performance computing (HPC) workloads and consist of 5 kernels and 3 pseudo applications.
Following are their details:

Kernels:
- **IS:** Integer Sort, random memory access
- **EP:** Embarrassingly Parallel
- **CG:** Conjugate Gradient, irregular memory access and communication
- **MG:** Multi-Grid on a sequence of meshes, long- and short-distance communication, memory intensive
- **FT:** discrete 3D fast Fourier Transform, all-to-all communication

Pseudo Applications:
- **BT:** Block Tri-diagonal solver
- **SP:** Scalar Penta-diagonal solver
- **LU:** Lower-Upper Gauss-Seidel solver

There are different classes (A,B,C,D,E and F) of the workloads based on the data size that is used with the benchmarks. Detailed discussion of the data sizes is available [here](https://www.nas.nasa.gov/publications/npb_problem_sizes.html). In this tutorial, we will use only class A of these workloads.

We assume the following directory structure to follow in this tutorial:

```
npb/
  |___ gem5/                               # gem5 source code
  |
  |___ disk-image/
  |      |___ shared/                      # Auxiliary files needed for disk creation
  |      |___ npb/
  |            |___ npb-image/             # Will be created once the disk is generated
  |            |      |___ npb             # The generated disk image
  |            |___ npb.json               # The Packer script to build the disk image
  |            |___ runscript.sh           # Executes a user provided script in simulated guest
  |            |___ post-installation.sh   # Moves runscript.sh to guest's .bashrc
  |            |___ npb-install.sh         # Compiles NPB inside the generated disk image
  |            |___ npb-hooks              # The NPB source (modified to use with gem5).
  |
  |___ config.4.19.83                      # linux kernel configuration file
  |
  |___ configs
  |      |___ system                       # gem5 system config files
  |      |___ run_npb.py                   # gem5 run script to run NPB tests
  |
  |___ linux                               # Linux source and binary will live here
  |
  |___ launch_npb_tests.py                 # script to launch jobs and register artifacts
```


## Setting up the environment

First, we need to create the main directory named **npb-tests** (from where we will run everything) and turn it into a git repository.
Through the use of **npb-tests** git repo, we will try to keep track of changes in those files which are not included in any git repo otherwise.
An example of such files is gem5 run and config scripts.
We want to make sure that we can keep record of any changes in these scripts, so that a particular run of NPB benchmarks can be associated with a particular snapshot of these files.
We also need to add a git remote to this repo pointing to a remote location where we want this repo to be hosted.


```sh
mkdir npb-tests
cd npb-tests
git init
git remote add origin https://your-remote-add/npb-tests.git
```

We also need to add a .gitignore file in our git repo, to avoid tracking those files which are not important or will be tracked through other git repos:

```sh
*.pyc
m5out
.vscode
results
venv
disk-image/packer
disk-image/packer_1.4.3_linux_amd64.zip
disk-image/npb/npb-image/npb
disk-image/npb/npb-hooks
disk-image/packer_cache
gem5
linux-stable/
```

gem5art relies on Python 3, so we suggest creating a virtual environment before using gem5art.

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

gem5art can be installed (if not already) using pip:

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

## Building gem5

Next clone gem5 from GitHub:

```sh
git clone https://github.com/gem5/gem5
```

If you want to use the exact gem5 source that was used at the time of creating this tutorial you will have to checkout the relevant commit. If you want to try with the current version of gem5 at the time of reading this tutorial, you can ignore the git checkout command.

```sh
cd gem5
git checkout v20.1.0.0;
scons build/X86/gem5.opt -j8
```

Also make sure to build the m5 utility which will be moved to the disk image eventually.
m5 utility allows to trigger simulation tasks from inside the simulated system.
For example, it can be used dump simulation statistics when the simulated system triggers to do so.
We will need m5 mainly to exit the simulation when the simulated system will be done with the execution of a particular NPB benchmark.

```sh
cd gem5/util/m5/
scons build/x86/out/m5
```

## Creating a disk image
First create a disk-image folder where we will keep all disk image related files:

```sh
mkdir disk-image
```

We will follow the similar directory structure as discussed in [Disk Images](../main/disks) section.
Add a folder named shared for config files which will be shared among all disk images (and will be kept to their defaults) and one folder named npb which will contain files configured for NPB disk image. Add [preseed.cfg](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/preseed.cfg) and [serial-getty@.service](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/serial-getty@.service) in shared/.

In npb/ we will add the benchmark source first, which will eventually be transferred to the disk image through our npb.json file.

```sh
cd disk-image/npb
git clone https://github.com/darchr/npb-hooks.git
```

This source of NPB has ROI (region of interest) annotations for each benchmark which will be used by gem5 to
separate out simulation statistics of the important parts of a program from the rest of the program.
Basically, gem5 magic instructions are used before and after the ROI which exit the guest and transfer control to gem5 run script which can then do things like dumping or resetting stats or switching to cpu of interest.

Next, we will add few other files in npb/ which will be used for compilation of NPB inside the disk image and eventually running of these benchmarks with gem5.
These files will be moved from host to the disk image using npb.json file as we will soon see.

First, create a file **npb-install.sh**, which will be executed inside the disk image (once it is built) and will install NPB on the disk image:

```sh
# install build-essential (gcc and g++ included) and gfortran

#Compile NPB

echo "12345" | sudo apt-get install build-essential gfortran

cd /home/gem5/NPB3.3-OMP/

mkdir bin

make suite HOOKS=1
```
`HOOKS=1` flag in the above make command enables the ROI annotations while compiling NPB workloads.
We are specifically compiling OpenMP (OMP) version of class A, B, C and D of NPB workloads.

To configure the benchmark build process, the source of NPB which we are using relies on modified **make.def** and **suite.def** files (build system files). Look [here](https://github.com/darchr/npb-hooks/blob/master/NPB3.3.1/NPB3.3-OMP/README.install), to understand the build process of NAS parallel benchmarks.
**suite.def** file is used to determine which workloads (and of which class) do we want to compile when we run **make suite** command (as in the above script).
You can look at the modified suite.def file [here](https://github.com/darchr/npb-hooks/blob/master/NPB3.3.1/NPB3.3-OMP/config/suite.def).

The **make.def** file we are using add OMP flags to the compiler flags to compile OMP version of the benchmarks. We also add another flag **-DM5OP_ADDR=0xFFFF0000** to the compiler flags, which makes sure that the gem5 magic instructions added to the benchmarks will also work in KVM mode.
You can look at the complete file [here](https://github.com/darchr/npb-hooks/blob/master/NPB3.3.1/NPB3.3-OMP/config/make.def).

In npb/, create a file **post-installation.sh** and add following lines to it:

```sh
#!/bin/bash
echo 'Post Installation Started'

mv /home/gem5/serial-getty@.service /lib/systemd/system/

mv /home/gem5/m5 /sbin
ln -s /sbin/m5 /sbin/gem5

# copy and run outside (host) script after booting
cat /home/gem5/runscript.sh >> /root/.bashrc

echo 'Post Installation Done'
```

This **post-installation.sh** script (which is a script to run after Ubuntu is installed on the disk image) installs m5 and copies the contents of **runscript.sh** to **.bashrc**.
Therefore, we need to add those things in runscript.sh which we want to execute as soon as the system boots up.
Create runscript.sh in npb/ and add following lines to it:

```sh
#!/bin/sh

m5 readfile > script.sh
if [ -s script.sh ]; then
    # if the file is not empty, execute it
    chmod +x script.sh
    ./script.sh
    m5 exit
fi
# otherwise, drop to the terminal
```
**runscript.sh** uses **m5 readfile** to read the contents of a script which is how gem5 passes scripts to the simulated system from the host system.
The passed script will then be executed and will be responsible for running benchmark/s which we will look into more later.

Finally, create **npb.json** and add following contents:

{% raw %}
```json
{
    "builders":
    [
        {
            "type": "qemu",
            "format": "raw",
            "accelerator": "kvm",
            "boot_command":
            [
                "{{ user `boot_command_prefix` }}",
                "debian-installer={{ user `locale` }} auto locale={{ user `locale` }} kbd-chooser/method=us ",
                "file=/floppy/{{ user `preseed` }} ",
                "fb=false debconf/frontend=noninteractive ",
                "hostname={{ user `hostname` }} ",
                "/install/vmlinuz noapic ",
                "initrd=/install/initrd.gz ",
                "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
                "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
                "passwd/user-fullname={{ user `ssh_fullname` }} ",
                "passwd/user-password={{ user `ssh_password` }} ",
                "passwd/user-password-again={{ user `ssh_password` }} ",
                "passwd/username={{ user `ssh_username` }} ",
                "-- <enter>"
            ],
            "cpus": "{{ user `vm_cpus`}}",
            "disk_size": "{{ user `image_size` }}",
            "floppy_files":
            [
                "shared/{{ user `preseed` }}"
            ],
            "headless": "{{ user `headless` }}",
            "http_directory": "shared/",
            "iso_checksum": "{{ user `iso_checksum` }}",
            "iso_checksum_type": "{{ user `iso_checksum_type` }}",
            "iso_urls": [ "{{ user `iso_url` }}" ],
            "memory": "{{ user `vm_memory`}}",
            "output_directory": "npb/{{ user `image_name` }}-image",
            "qemuargs":
            [
                [ "-cpu", "host" ],
                [ "-display", "none" ]
            ],
            "qemu_binary":"/usr/bin/qemu-system-x86_64",
            "shutdown_command": "echo '{{ user `ssh_password` }}'|sudo -S shutdown -P now",
            "ssh_password": "{{ user `ssh_password` }}",
            "ssh_username": "{{ user `ssh_username` }}",
            "ssh_wait_timeout": "60m",
            "vm_name": "{{ user `image_name` }}"
        }
    ],
    "provisioners":
    [
        {
            "type": "file",
            "source": "../gem5/util/m5/m5",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "shared/serial-getty@.service",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "npb/runscript.sh",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "npb/npb-hooks/NPB3.3.1/NPB3.3-OMP",
            "destination": "/home/gem5/"
        },
        {
            "type": "shell",
            "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
            "scripts":
            [
                "npb/post-installation.sh",
                "npb/npb-install.sh"
            ]
        }
    ],
    "variables":
    {
        "boot_command_prefix": "<enter><wait><f6><esc><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs>",
        "desktop": "false",
        "image_size": "12000",
        "headless": "true",
        "iso_checksum": "34416ff83179728d54583bf3f18d42d2",
        "iso_checksum_type": "md5",
        "iso_name": "ubuntu-18.04.2-server-amd64.iso",
        "iso_url": "http://old-releases.ubuntu.com/releases/18.04.2/ubuntu-18.04.2-server-amd64.iso",
        "locale": "en_US",
        "preseed" : "preseed.cfg",
        "hostname": "gem5",
        "ssh_fullname": "gem5",
        "ssh_password": "12345",
        "ssh_username": "gem5",
        "vm_cpus": "16",
        "vm_memory": "8192",
        "image_name": "npb"
  }

}
```
{% endraw %}

**npb.json** is our primary .json configuration file. The provisioners and variables section of this file configure the files that need to be transferred to the disk and other things like disk image's name.

Next, download packer (if not already downloaded) in the disk-image folder:

```
cd disk-image/
wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip
unzip packer_1.4.3_linux_amd64.zip
```
Now, to build the disk image inside the disk-image folder, run:

```
./packer validate npb/npb.json

./packer build npb/npb.json
```

Once this process succeeds, the created disk image can be found on `npb/npb-image/npb`.
A disk image already created following the above instructions can be found, gzipped, [here](http://dist.gem5.org/dist/v21-2/images/x86/ubuntu-18-04/npb.img.gz).

## Compiling the linux kernel

In this tutorial, we use one of the LTS (long term support) releases of linux kernel v4.19.83 with gem5 to run NAS parallel benchmarks.
First, get the linux kernel config file from [here](https://github.com/gem5/gem5-resources/tree/stable/src/linux-kernel/linux-configs), and place it in npb-tests folder.
Then, we will get the linux source of version 4.19.83:

```
git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
mv linux linux-stable
cd linux-stable
```
Compile the linux kernel from its source (using already downloaded config file config.4.19.83):

```
cp ../config.4.19.83 .config
make -j8
cp vmlinux vmlinux-4.19.83
```

**Note:** The above instructions are tested with `gcc 7.5.0` and an already compiled Linux binary can be downloaded from the following link:

- [vmlinux-4.19.83](http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.19.83)

## gem5 run scripts

Next, we need to add gem5 run scripts. We will do that in a folder named configs-npb-tests.
Get the run script named run_npb.py from [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/npb/configs/run_npb.py), and other system configuration files from
[here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/npb/configs/system/).

The main script `run_npb.py` expects following arguments:

**kernel:** path to the Linux kernel.

**disk:** path to the npb disk image.

**cpu:** CPU model (`kvm`, `atomic`, `timing`).

**mem_sys:** memory system (`classic`, `MI_example`, `MESI_Two_Level`, `MOESI_CMP_directory`).

**benchmark:** NPB benchmark to execute (`bt.A.x`, `cg.A.x`, `ep.A.x`, `ft.A.x`, `is.A.x`, `lu.A.x`, `mg.A.x`,  `sp.A.x`).

**Note:**
By default, the previously written instructions to build npb disk image will build class `A`,`B`,`C` and `D` of NPB in the disk image.
We have only tested class `A` of the NPB.
Replace `A` with any other class in the above listed benchmark names to test with other classes.

**num_cpus:** number of CPU cores.

## Database and Celery Server

If not already running/created, you can create a database using:

```sh
`docker run -p 27017:27017 -v <absolute path to the created directory>:/data/db --name mongo-<some tag> -d mongo`
```
in a newly created directory.

If not already installed, install `RabbitMQ` on your system (before running celery) using:

```sh
apt-get install rabbitmq-server
```

Now, run celery server using:

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

**Note:** Celery is not required to run gem5 jobs with gem5art. You can also use python multiprocessing library based function calls (provided by gem5art) to launch these jobs in parallel (we will show how to do that later in our launch script).


## Creating a launch script
Finally, we will create a launch script with the name **launch_npb_tests.py**, which will be responsible for registering the artifacts to be used and then launching gem5 jobs.

The first thing to do in the launch script is to import required modules and classes:

```python
import os
import sys
from uuid import UUID
from itertools import starmap
from itertools import product

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
import multiprocessing as mp
```

Next, we will register artifacts. For example, to register packer artifact we will add the following lines:

```python
packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August/19 from hashicorp.'
)
```

For our npb-tests repo,

```python
experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/npb-tests.git',
    typ = 'git repo',
    name = 'npb-tests',
    path =  './',
    cwd = '../',
    documentation = 'main repo to run npb with gem5'
)
```

Note that the name of the artifact (returned by the registerArtifact method) is totally up to the user as well as most of the other attributes of these artifacts.

For all other artifacts, add following lines in launch_npb_tests.py:

```python
gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/gem5/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 from github and checked out v20.1.0.0'
)

m5_binary = Artifact.registerArtifact(
    command = 'scons build/x86/out/m5',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/build/x86/out/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

disk_image = Artifact.registerArtifact(
    command = 'packer build npb.json',
    typ = 'disk image',
    name = 'npb',
    cwd = 'disk-image/npb',
    path = 'disk-image/npb/npb-image/npb',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu with m5 binary and NPB (with ROI annotations: darchr/npb-hooks/) installed.'
)

gem5_binary = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/X86/gem5.opt -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)

gem5_binary_MESI_Two_Level = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout v20.1.0.0;
    scons build/X86_MESI_Two_Level/gem5.opt --default=X86 PROTOCOL=MESI_Two_Level SLICC_HTML=True -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86_MESI_Two_Level/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on v20.1.0.0'
)

linux_repo = Artifact.registerArtifact(
    command = '''git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo from June 24-2020'
)

linux_binary = Artifact.registerArtifact(
    name = 'vmlinux-4.19.83',
    typ = 'kernel',
    path = 'linux-stable/vmlinux-4.19.83',
    cwd = 'linux-stable/',
    command = '''
    cp ../config.4.19.83 .config;
    make -j8;
    cp vmlinux vmlinux-4.19.83;
    ''',
    inputs = [experiments_repo, linux_repo,],
    documentation = "kernel binary for v4.19.83",
)
```

Once, all the artifacts are registered the next step is to launch all gem5 jobs. To do that, first we will create a method `createRun` to create gem5art runs based on a few arguments:


```python

def createRun(bench, clas, cpu, mem, num_cpu):

    if mem == 'MESI_Two_Level':
        binary_gem5 = 'gem5/build/X86_MESI_Two_Level/gem5.opt'
        artifact_gem5 = gem5_binary_MESI_Two_Level
    else:
        binary_gem5 = 'gem5/build/X86/gem5.opt'
        artifact_gem5 = gem5_binary

    return gem5Run.createFSRun(
        'npb with gem5-20.1',
        binary_gem5,
        'configs-npb-tests/run_npb.py',
        f'''results/run_npb_multicore/{bench}/{clas}/{cpu}/{num_cpu}''',
        artifact_gem5, gem5_repo, experiments_repo,
        'linux-stable/vmlinux-4.19.83',
        'disk-image/npb/npb-image/npb',
        linux_binary, disk_image,
        cpu, mem, bench.replace('.x', f'.{clas}.x'), num_cpu,
        timeout = 240*60*60 #240 hours
        )
```

Next, initialize all the parameters to pass to `createRun` method, depending on the configuration space we want to test:

```python
if __name__ == "__main__":
    num_cpus = ['1', '8']
    benchmarks = ['is.x', 'ep.x', 'cg.x', 'mg.x','ft.x', 'bt.x', 'sp.x', 'lu.x']

    classes = ['A']
    mem_sys = ['MESI_Two_Level']
    cpus = ['kvm', 'timing']
```

Then, to run actual jobs depending on if you want to use celery or python multiprocessing library, add the following in your launch script:

## If Using Celery

```python
    # For the cross product of tests, create a run object.
    runs = starmap(createRun, product(benchmarks, classes, cpus, mem_sys, num_cpus))
    # Run all of these experiments in parallel
    for run in runs:
        run_gem5_instance.apply_async((run, os.getcwd(),))
```


## If Using Python Multiprocessing Library:

```python
    def worker(run):
        run.run()
        json = run.dumpsJson()
        print(json)

    jobs = []

    # For the cross product of tests, create a run object.
    runs = starmap(createRun, product(benchmarks, classes, cpus, mem_sys, num_cpus))
    # Run all of these experiments in parallel
    for run in runs:
        jobs.append(run)

    with mp.Pool(mp.cpu_count() // 2) as pool:
         pool.map(worker, jobs)
```

The above lines are responsible for looping through all possible combinations of variables involved in this experiment.
For each combination, a gem5Run object is created and eventually passed to run_gem5_instance to be executed asynchronously if using Celery.
In case of python multiprocessing library, these run objects are pushed to a list and then mapped to a job pool.
Look at the definition of `createFSRun()` [here](../main/run.html) to understand the use of passed arguments.

Here, we are using a timeout of 240 hours, after which the particular gem5 job will be killed (assuming that gem5 should complete the booting process of linux kernel on the given hardware resources). You can configure this time according to your settings.

The complete launch script is available [here:](https://github.com/darchr/gem5art/blob/master/docs/launch-scripts/launch_npb_tests.py).
Finally, make sure you are in python virtual env and then run the script:

```python
python launch_boot_tests.py
```

## Results

Once you run the launch script, the declared artifacts will be registered by gem5art and stored in the database.
Celery will run as many jobs in parallel as allowed by the user (at the time of starting the server).
As soon as a gem5 job finishes, a compressed version of the results will be stored in the database as well.
User can also query the database using the methods discussed in the [Artifacts](../main/artifacts), [Runs](../main/run) sections and [boot-test](boot-tutorial) tutorial previously.

The status of working of the NAS parallel benchmarks on gem5 based on the results from the experiments of this tutorial is following:

![](/assets/img/gem5art//npb_X86KvmCPU_MESI_Two_Level.svg)
![](/assets/img/gem5art//npb_TimingSimpleCPU_MESI_Two_Level.svg)

You can look [here](https://www.gem5.org/documentation/benchmark_status/gem5-20) for the latest status of these tests on gem5.


---


## PARSEC Tutorial

*Source: https://www.gem5.org/documentation/gem5art/tutorials/parsec-tutorial*

# Tutorial: Run PARSEC Benchmarks with gem5

## Introduction

In this tutorial, we will use gem5art to create a disk image for PARSEC benchmarks ([PARSEC](https://dl.acm.org/doi/10.1145/1454115.1454128)) and then run the benchmarks using gem5.
PARSEC is mainly designed to represent the applications that require a vast amount of shared-memory.

Following are their details:

Kernels:
- **canneal:** Simulated cache-aware annealing to optimize routing cost of a chip design
- **dedup:** Next-generation compression with data deduplication
- **streamcluster:** Online clustering of an input stream

Pseudo Applications:
- **blackscholes:** Option pricing with Black-Scholes Partial Differential Equation (PDE)
- **bodytrack:** Body tracking of a person
- **facesim:** Simulates the motions of a human face
- **ferret:** Content similarity search server
- **fluidanimate:** Fluid dynamics for animation purposes with Smoothed Particle Hydrodynamics (SPH) method
- **freqmine:** Frequent itemset mining
- **raytrace:** Real-time raytracing
- **swaptions:** Pricing of a portfolio of swaptions
- **vips:** Image processing ([Project Website](https://github.com/libvips/libvips))
- **x264:** H.264 video encoding ([Project Website](http://www.videolan.org/developers/x264.html))

There are different sizes for possible inputs to each workload. Each size is explained below:
- **test:** very small set of inputs just to test the functionality of the program.
- **simdev:** small set of inputs intended to generate general behaviour of each program. Mainly used for simulators and development.
- **simsmall, simmedium, simlarge:** variable size inputs appropriate for testing microarchitectures with simulators.
- **native:** very large set of inputs intended for native execution.

This tutorial follows the following directory structure (inside the main directory):

- configs-parsec-tests: gem5 run and configuration scripts to run PARSEC
- disk-image: contains packer script and template files used to build a disk image.
The built disk image will be stored in the same folder
- gem5: gem5 [source code](https://github.com/gem5/gem5) and the compiled binary
- linux-stable: linux kernel [source code](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git)  used for full-system experiments
- config.4.19.83: linux kernel config file used for its compilation
- results: directory to store the results of the experiments (generated once gem5 jobs are executed)
- launch_parsec_tests.py:  gem5 jobs launch script (creates all of the needed artifacts as well)


## Setting up the environment
First, we need to create the main directory named parsec-tests (from where we will run everything) and turn it into a git repository.
Through the use of parsec-tests git repo, we will try to keep track of changes in those files which are not included in any git repo otherwise.
An example of such files is gem5 run and config scripts (config-parsec-tests).
We want to make sure that we can keep record of any changes in these scripts, so that a particular run of PARSEC benchmarks can be associated with a particular snapshot of these files.
We also need to add a git remote to this repo pointing to a remote location where we want this repo to be hosted.

```sh
mkdir parsec-tests
cd parsec-tests
git init
git remote add origin https://your-remote-add/parsec-tests.git
```

We also need to add a .gitignore file in our git repo, to avoid tracking those files which are not important or will be tracked through other git repos:

```sh
*.pyc
m5out
.vscode
results
venv
disk-image/packer
disk-image/packer_1.4.3_linux_amd64.zip
disk-image/parsec/parsec-image/parsec
disk-image/parsec/
disk-image/parsec-benchmark/
disk-image/packer_cache
gem5
linux-stable/
```

gem5art relies on Python 3, so we suggest creating a virtual environment before using gem5art.

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

gem5art can be installed (if not already) using pip:

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

## Building gem5

For instructions on how to build gem5 look [here](npb-tutorial##Building-gem5).

## Creating a disk image
First create a disk-image folder where we will keep all disk image related files:

```sh
mkdir disk-image
```

We will follow the similar directory structure as discussed in [Disk Images](../main/disks) section.
Add a folder named shared for config files which will be shared among all disk images (and will be kept to their defaults) and one folder named parsec which will contain files configured for PARSEC disk image. Add [preseed.cfg](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/preseed.cfg) and [serial-getty@.service](https://github.com/darchr/gem5art/blob/master/docs/disks/shared/serial-getty@.service) in shared/.

In parsec/ we will add the benchmark source first, which will eventually be transferred to the disk image through our parsec.json file.

```sh
cd disk-image/parsec-benchmark
git clone https://github.com/darchr/parsec-benchmark.git
```

This source of PARSEC has ROI (region of interest) annotations for each benchmark which will be used by gem5 to
separate out simulation statistics of the important parts of a program from the rest of the program.
Basically, gem5 magic instructions are used before and after the ROI which exit the guest and transfer control to gem5 run script which can then do things like dumping or resetting stats or switching to cpu of interest.

Next, we will add few other files in parsec/ which will be used for compilation of PARSEC inside the disk image and eventually running of these benchmarks with gem5.
These files will be moved from host to the disk image using parsec.json file as we will soon see.

First, create a file parsec-install.sh, which will be executed inside the disk image (once it is built) and will install PARSEC on the disk image:

```sh
# install build-essential (gcc and g++ included) and gfortran

#Compile PARSEC

cd /home/gem5/
su gem5
echo "12345" | sudo -S apt update

# Allowing services to restart while updating some
# libraries.
sudo apt install -y debconf-utils
sudo debconf-get-selections | grep restart-without-asking > libs.txt
sed -i 's/false/true/g' libs.txt
while read line; do echo $line | sudo debconf-set-selections; done < libs.txt
sudo rm libs.txt
##

# Installing packages needed to build PARSEC
sudo apt install -y build-essential
sudo apt install -y m4
sudo apt install -y git
sudo apt install -y python
sudo apt install -y python-dev
sudo apt install -y gettext
sudo apt install -y libx11-dev
sudo apt install -y libxext-dev
sudo apt install -y xorg-dev
sudo apt install -y unzip
sudo apt install -y texinfo
sudo apt install -y freeglut3-dev
##

# Building PARSEC

echo "12345" | sudo -S chown gem5 -R parsec-benchmark/
echo "12345" | sudo -S chgrp gem5 -R parsec-benchmark/
cd parsec-benchmark
./install.sh
./get-inputs
cd ..
echo "12345" | sudo -S chown gem5 -R parsec-benchmark/
echo "12345" | sudo -S chgrp gem5 -R parsec-benchmark/
##
```

In parsec/, create a file post-installation.sh and add following lines to it:

```sh
#!/bin/bash
echo 'Post Installation Started'

mv /home/gem5/serial-getty@.service /lib/systemd/system/

mv /home/gem5/m5 /sbin
ln -s /sbin/m5 /sbin/gem5

# copy and run outside (host) script after booting
cat /home/gem5/runscript.sh >> /root/.bashrc

echo 'Post Installation Done'
```

This post-installation.sh script (which is a script to run after Ubuntu is installed on the disk image) installs m5 and copies the contents of runscript.sh to .bashrc.
Therefore, we need to add those things in runscript.sh which we want to execute as soon as the system boots up.
Create runscript.sh in parsec/ and add following lines to it:

```sh
#!/bin/sh

m5 readfile > script.sh
if [ -s script.sh ]; then
    # if the file is not empty, execute it
    chmod +x script.sh
    ./script.sh
    m5 exit
fi
# otherwise, drop to the terminal
```
runscript.sh uses m5 readfile to read the contents of a script which is how gem5 passes scripts to the simulated system from the host system.
The passed script will then be executed and will be responsible for running benchmark/s which we will look into more later.

Finally, create parsec.json and add following contents:

{% raw %}
```json
{
    "builders":
    [
        {
            "type": "qemu",
            "format": "raw",
            "accelerator": "kvm",
            "boot_command":
            [
                "{{ user `boot_command_prefix` }}",
                "debian-installer={{ user `locale` }} auto locale={{ user `locale` }} kbd-chooser/method=us ",
                "file=/floppy/{{ user `preseed` }} ",
                "fb=false debconf/frontend=noninteractive ",
                "hostname={{ user `hostname` }} ",
                "/install/vmlinuz noapic ",
                "initrd=/install/initrd.gz ",
                "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
                "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
                "passwd/user-fullname={{ user `ssh_fullname` }} ",
                "passwd/user-password={{ user `ssh_password` }} ",
                "passwd/user-password-again={{ user `ssh_password` }} ",
                "passwd/username={{ user `ssh_username` }} ",
                "-- <enter>"
            ],
            "cpus": "{{ user `vm_cpus`}}",
            "disk_size": "{{ user `image_size` }}",
            "floppy_files":
            [
                "shared/{{ user `preseed` }}"
            ],
            "headless": "{{ user `headless` }}",
            "http_directory": "shared/",
            "iso_checksum": "{{ user `iso_checksum` }}",
            "iso_checksum_type": "{{ user `iso_checksum_type` }}",
            "iso_urls": [ "{{ user `iso_url` }}" ],
            "memory": "{{ user `vm_memory`}}",
            "output_directory": "parsec/{{ user `image_name` }}-image",
            "qemuargs":
            [
                [ "-cpu", "host" ],
                [ "-display", "none" ]
            ],
            "qemu_binary":"/usr/bin/qemu-system-x86_64",
            "shutdown_command": "echo '{{ user `ssh_password` }}'|sudo -S shutdown -P now",
            "ssh_password": "{{ user `ssh_password` }}",
            "ssh_username": "{{ user `ssh_username` }}",
            "ssh_wait_timeout": "60m",
            "vm_name": "{{ user `image_name` }}"
        }
    ],
    "provisioners":
    [
        {
            "type": "file",
            "source": "../gem5/util/m5/m5",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "shared/serial-getty@.service",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "parsec/runscript.sh",
            "destination": "/home/gem5/"
        },
        {
            "type": "file",
            "source": "parsec/parsec-benchmark/",
            "destination": "/home/gem5/"
        },
        {
            "type": "shell",
            "execute_command": "echo '{{ user `ssh_password` }}' | {{.Vars}} sudo -E -S bash '{{.Path}}'",
            "scripts":
            [
                "parsce/post-installation.sh",
                "parsec/parsec-install.sh"
            ]
        }
    ],
    "variables":
    {
        "boot_command_prefix": "<enter><wait><f6><esc><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs>",
        "desktop": "false",
        "image_size": "12000",
        "headless": "true",
        "iso_checksum": "34416ff83179728d54583bf3f18d42d2",
        "iso_checksum_type": "md5",
        "iso_name": "ubuntu-18.04.2-server-amd64.iso",
        "iso_url": "http://old-releases.ubuntu.com/releases/18.04.2/ubuntu-18.04.2-server-amd64.iso",
        "locale": "en_US",
        "preseed" : "preseed.cfg",
        "hostname": "gem5",
        "ssh_fullname": "gem5",
        "ssh_password": "12345",
        "ssh_username": "gem5",
        "vm_cpus": "16",
        "vm_memory": "8192",
        "image_name": "parsec"
  }

}
```
{% endraw %}

parsec.json is our primary .json configuration file. The provisioners and variables section of this file configure the files that need to be transferred to the disk and other things like disk image's name.

Next, download packer (if not already downloaded) in the disk-image folder:

```
cd disk-image/
wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip
unzip packer_1.4.3_linux_amd64.zip
```
Now, to build the disk image inside the disk-image folder, run:

```
./packer validate parsec/parsec.json

./packer build parsec/parsec.json
```

## Compiling the linux kernel

Follow the instructions [here](npb-tutorial##Compiling-the-linux-kernel) to compile your linux kernel

## gem5 run scripts

Next, we need to add gem5 run scripts. We will do that in a folder named configs-parsec-tests.
Get the run script named run_parsec.py from [here](https://github.com/darchr/gem5art-experiments/blob/master/gem5-configs/configs-parsec-tests/run_parsec.py), and other system configuration files from
[here](https://github.com/darchr/gem5art/blob/master/docs/gem5-configs/configs-parsec-tests/system/).
The run script (run_parsec.py) takes the following arguments:
- kernel: compiled kernel to be used for simulation
- disk: built disk image to be used for simulation
- cpu: the cpu model to use (e.g. kvm or atomic)
- benchmark: PARSEC workload to run (e.g. blackscholes, bodytrack, facesim, etc.)
- num_cpus: number of parallel cpus to be simulated

## Database and Celery Server

To create a database and start a celery server follow the instructions [here](npb-tutorial##Database-and-Celery-Server).

## Creating a launch script
Finally, we will create a launch script with the name launch_parsec_tests.py, which will be responsible for registering the artifacts to be used and then launching gem5 jobs.

The first thing to do in the launch script is to import required modules and classes:

```python
import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
```

Next, we will register artifacts. For example, to register packer artifact we will add the following lines:

```python
packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.'
)
```

For our parsec-tests repo,

```python
experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/parsec-tests.git',
    typ = 'git repo',
    name = 'parsec-tests',
    path =  './',
    cwd = '../',
    documentation = 'main repo to run parsec with gem5'
)
```

Note that the name of the artifact (returned by the registerArtifact method) is totally up to the user as well as most of the other attributes of these artifacts.

For all other artifacts, add following lines in launch_parsec_tests.py:

```python
parsec_repo = Artifact.registerArtifact(
    command = '''mkdir parsec-benchmark/;
    cd parsec-benchmark;
    git clone https://github.com/darchr/parsec-benchmark.git;''',
    typ = 'git repo',
    name = 'parsec_repo',
    path =  './disk-image/parsec-benchmark/parsec-benchmark/',
    cwd = './disk-image/',
    documentation = 'main repo to copy parsec source to the disk-image'
)

gem5_repo = Artifact.registerArtifact(
    command = '''
        git clone https://github.com/gem5/gem5;
        cd gem5;
        git remote add darchr https://github.com/darchr/gem5;
        git fetch darchr;
        git cherry-pick 6450aaa7ca9e3040fb9eecf69c51a01884ac370c;
        git cherry-pick 3403665994b55f664f4edfc9074650aaa7ddcd2c;
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 master branch from github (Nov 18, 2019) and cherry-picked 2 commits from darchr/gem5'
)

m5_binary = Artifact.registerArtifact(
    command = 'make -f Makefile.x86',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

disk_image = Artifact.registerArtifact(
    command = './packer build parsec/parsec.json',
    typ = 'disk image',
    name = 'parsec',
    cwd = 'disk-image',
    path = 'disk-image/parsec/parsec-image/parsec',
    inputs = [packer, experiments_repo, m5_binary, parsec_repo,],
    documentation = 'Ubuntu with m5 binary and PARSEC installed.'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary'
)

linux_repo = Artifact.registerArtifact(
    command = '''git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo'
)

linux_binary = Artifact.registerArtifact(
    name = 'vmlinux-4.19.83',
    typ = 'kernel',
    path = 'linux-stable/vmlinux-4.19.83',
    cwd = 'linux-stable/',
    command = '''
    cp ../config.4.19.83 .config;
    make -j8;
    cp vmlinux vmlinux-4.19.83;
    ''',
    inputs = [experiments_repo, linux_repo,],
    documentation = "kernel binary for v4.19.83"
)
```

Once, all of the artifacts are registered, the next step is to launch all gem5 jobs. To do that, add the following lines in your script:

```python
if __name__ == "__main__":
    num_cpus = ['1']
    benchmarks = ['blackscholes', 'bodytrack', 'canneal', 'dedup','facesim', 'ferret', 'fluidanimate', 'freqmine', 'raytrace', 'streamcluster', 'swaptions', 'vips', 'x264']

    sizes = ['simsmall', 'simlarge', 'native']
    cpus = ['kvm', 'timing']

    for cpu in cpus:
        for num_cpu in num_cpus:
            for size in sizes:
                if cpu == 'timing' and size != 'simsmall':
                    continue
                for bm in benchmarks:
                    run = gem5Run.createFSRun(
                        'parsec_tests',
                        'gem5/build/X86/gem5.opt',
                        'configs-parsec-tests/run_parsec.py',
                        f'''results/run_parsec/{bm}/{size}/{cpu}/{num_cpu}''',
                        gem5_binary, gem5_repo, experiments_repo,
                        'linux-stable/vmlinux-4.19.83',
                        'disk-image/parsec/parsec-image/parsec',
                        linux_binary, disk_image,
                        cpu, bm, size, num_cpu,
                        timeout = 24*60*60 #24 hours
                        )
                    run_gem5_instance.apply_async((run, os.getcwd(), ))
```
The above lines are responsible for looping through all possible combinations of variables involved in this experiment.
For each combination, a gem5Run object is created and eventually passed to run_gem5_instance to be
executed asynchronously using Celery. Note that when using timingSimpleCPU model only size **simsmall** has been used because the other sizes take more than 24 hours to simulate.


Finally, make sure you are in python virtual env and then run the script:

```python
python launch_parsec_tests.py
```

## Results

Once you run the launch script, the declared artifacts will be registered by gem5art and stored in the database.
Celery will run as many jobs in parallel as allowed by the user (at the time of starting the server).
As soon as a gem5 job finishes, a compressed version of the results will be stored in the database as well.
User can also query the database using the methods discussed in the [Artifacts](../main/artifacts), [Runs](../main/run) sections and [boot-test](boot-tutorial) tutorial previously.

Here is the status of each workload after simulation:

![WorkingStatusKVM](/assets/img/gem5art//WorkingStatusKVM.png)
![WorkingStatusTiming](/assets/img/gem5art//WorkingStatusTiming.png)

Below are the simulation time for KVM and TimingSimple cpu models.

![SimTimeKVM](/assets/img/gem5art//SimTimeKVM.png)
![SimTimeTiming](/assets/img/gem5art//SimTimeTiming.png)

The number of instructions run on each cpu model is shown below:

![InstCountKVM](/assets/img/gem5art//InstCountKVM.png)
![InstCountTiming](/assets/img/gem5art//InstCountTiming.png)


---


## SPEC Tutorial

*Source: https://www.gem5.org/documentation/gem5art/tutorials/spec-tutorial*

# Tutorial: Run SPEC CPU 2017 / SPEC CPU 2006 Benchmarks in Full System Mode with gem5art

## Introduction
In this tutorial, we will demonstrate how to utilize [gem5art](https://github.com/gem5/gem5/tree/stable/util/gem5art) and [gem5-resources](https://github.com/gem5/gem5-resources/tree/stable/) to run [SPEC CPU 2017 benchmarks](https://www.spec.org/cpu2017/) in gem5 full system mode.
The scripts in this tutorial work with gem5art v1.3.0, gem5 20.1.0.4, and gem5-resources 20.1.0.4.

The content of this tutorial is mostly for conducting SPEC CPU 2017 experiments.
However, due to the similarity of SPEC 2006 and SPEC 2017 resources, this tutorial also applies to conducting SPEC 2006 experiment by using `src/spec-2006` folder instead of `src/spec-2017` of gem5-resources.

### gem5-resources
[gem5-resources](https://github.com/gem5/gem5-resources/tree/stable/) is an actively maintained collections of gem5-related resources that are commonly used.
The resources include scripts, binaries and disk images for full system simulation of many commonly used benchmarks.
This tutorial will offer guidance in utilizing gem5-resources for full system simulation.


### gem5 Full System Mode
Different from gem5 SE mode (system emulation mode), the FS mode (full system mode) uses an actual Linux kernel binary instead of emulating the responsibilities of a typical modern OS such as managing page tables and taking care of system calls.
As a result, gem5 FS simulation would be more realistic compared to gem5 SE simulation, especially when the interactions between the workload and the OS are significant part of the simulation.

A typical gem5 full system simulation requires a compiled Linux kernel, a disk image containing compiled benchmarks, and gem5 system configurations.
gem5-resources typically provides all required all of the mentioned resources for every supported benchmark such that one could download the resources and run the experiment without much modification.
However, due to license issue, gem5-resources does not provide a disk image containing SPEC CPU 2017 benchmarks.
In this tutorial, we will provide a set of scripts that generates a disk image containing the benchmarks assuming the ISO file of the SPEC CPU 2017 benchmarks is available.

### Overall Structure of the Experiment
```
spec-2017/
  |___ gem5/                                   # gem5 folder
  |
  |___ disk-image/
  |      |___ shared/
  |      |___ spec-2017/
  |             |___ spec-2017-image/
  |             |      |___ spec-2017          # the disk image will be generated here
  |             |___ spec-2017.json            # the Packer script
  |             |___ cpu2017-1.1.0.iso         # SPEC 2017 ISO (add here)
  |
  |___ configs
  |      |___ system/
  |      |___ run_spec.py                      # gem5 run script
  |
  |___ vmlinux-4.19.83                         # Linux kernel, link to download provided below
  |
  |___ README.md

```

### An Overview of Host System - gem5 Interactions
![**Figure 1.**](/assets/img/gem5art//spec_tutorial_figure1.png)
A visual depict of how gem5 interacts with the host system.
gem5 is configured to do the following: booting the Linux kernel, running the benchmark, and copying the SPEC outputs to the host system.
However, since we are interested in getting the stats only for the benchmark, we will configure gem5 to exit after the kernel is booted, and then we reset the stats before running the benchmark.
We use KVM CPU model in gem5 for Linux booting process to quickly boot the system, and after the process is complete, we switch to the desired detailed CPU to run the benchmark.
Similarly, after the benchmark is complete, gem5 exits to host, which allows us to get the stats at that point.
After that, optionally, we switch the CPU back to KVM, which allows us to quickly write the SPEC output files to the host.

**Note:** gem5 will output the stats again when the gem5 run is complete.
Therefore, we will see two sets of stats in one file in stats.txt.
The stats of the benchmark is the the first part of stats.txt, while the second part of the file contains the stats of the benchmark AND the process of writing output files back to the host.
We are only interested in the first part of stats.txt.

## Setting up the Experiment
In this part, we have two concurrent tasks: setting up the resources and documenting the process using gem5art.
We will structure the [SPEC 2017 resources as laid out by gem5-resources](https://github.com/gem5/gem5-resources/tree/stable/src/spec-2017/).
The script `launch_spec2017_experiment.py` will contain the documentation about the artifacts we create and will also serve as Python script that launches the experiment.

### Acquiring gem5-resources and Setting up the Experiment Folder
First, we clone the gem5-resource repo and check out the stable branch upto the `1fe56ffc94005b7fa0ae5634c6edc5e2cb0b7357` commit, which is the most recent version of gem5-resources that is compatible with gem5 20.1.0.4 as of March 2021.
```sh
git clone https://github.com/gem5/gem5-resources
cd gem5-resources
git checkout 1fe56ffc94005b7fa0ae5634c6edc5e2cb0b7357
```
Since all resources related to the SPEC CPU 2006 benchmark suite are in the `src/spec-2017` and other folders in `src/` are not related to this experiment, we set the root folder of the experiment in the `src/spec-2017` folder of the cloned repo.
To keep track of changes that are specific to `src/spec-2017`, we set up a git structure for the folder.
Also, the git remote pointing to `origin` should also be setup as gem5art will use `origin` information.
In the `gem5-resources` folder,
```sh
cd src/spec-2017
git init
git remote add origin https://remote-address/spec-experiment.git
```
We document the root folder of the experiment in `launch_spec2017_experiment.py` as follows,
```sh
experiments_repo = Artifact.registerArtifact(
    command = '''
        git clone https://github.com/gem5/gem5-resources
        cd gem5-resources
        git checkout 1fe56ffc94005b7fa0ae5634c6edc5e2cb0b7357
        cd src/spec-2017
        git init
        git remote add origin https://remote-address/spec-experiment.git
    ''',
    typ = 'git repo',
    name = 'spec2017 Experiment',
    path =  './',
    cwd = './',
    documentation = '''
        local repo to run spec 2017 experiments with gem5 full system mode;
        resources cloned from https://github.com/gem5/gem5-resources upto commit 1fe56ffc94005b7fa0ae5634c6edc5e2cb0b7357 of stable branch
    '''
)
```
We use `.gitignore` file to ingore changes of certain files and folders.
In this experiment, we will use this `.gitignore` file,
```
*.pyc
m5out
.vscode
results
gem5art-env
disk-image/packer
disk-image/packer_cache
disk-image/spec-2017/spec-2017-image/spec-2017
disk-image/spec-2017/cpu2017-1.1.0.iso
gem5
vmlinux-4.19.83
```
In the script above, we ignore files and folders that we use other gem5art Artifact objects to keep track of them, or the presence of those files and folders do not affect the experiment's results.
For example, `disk-image/packer` is the path to the packer binary which generates the disk image, and newer versions `packer` probably won't affect the content of the disk image.
Another example is that we use another gem5art Artifact object to keep track of `vmlinux-4.19.83`, so we put the name of the file in the `.gitignore` file.

**Note:** You probably notice that there are more than one way of keeping track of the files in the experiment folder: either the git structure of the experiment will keep track of a file, or we can create a separate [gem5art Artifact](../main/artifacts) object to keep track of that file.
The decision of letting the git structure or creating a new Artifact object leads to different outcomes.
The difference lies on the type of the Artifact object (specified by the `typ` parameter): for Artifact objects that has `typ` of `git repo`, gem5art won't upload the files in the git structure to gem5art's database, instead, it will only keep track of the hash of the HEAD commit of the git structure.
However, for Artifact's that do **not** have `typ` that is `git repo`, the file specfied in the `path` parameter will be uploaded to the database.

Essentially, we tend to keep small-size files (such as scripts and texts) in a git structure, and to keep large-size files (such as gem5 binaries and disk images) in Artifact's of type `gem5 binary` or `binary`.
Another important difference is that gem5art does **not** keep track of files in a git Artifact, while it does upload other types of Artifact to its database.

### Building gem5
In this step, we download the source code and build gem5 v20.1.0.4.
In the root folder of the experiment,

```sh
git clone -b v20.1.0.4 https://github.com/gem5/gem5
cd gem5
scons build/X86/gem5.opt -j8
```

We have two artifacts: one is the gem5 source code (the gem5 git repo), and the gem5 binary (`gem5.opt`).
In `launch_spec2017_experiments.py`, we document the step in Artifact objects as follows,

```python
gem5_repo = Artifact.registerArtifact(
    command = '''
        git clone -b v20.1.0.4 https://github.com/gem5/gem5
        cd gem5
        scons build/X86/gem5.opt -j8
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 v20.1.0.4'
)


gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt -j8',
    typ = 'gem5 binary',
    name = 'gem5-20.1.0.4',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'compiled gem5 v20.1.0.4 binary'
)
```

### Building m5
m5 is a binary that facilitates the communication between the host system and the guest system (gem5).
The use of the m5 binary will be demonstrated in the runscripts that we will describe later.
m5 binary will be copied to the disk image so that the guest could run m5 binary during the simulation.
m5 binary should be compiled before we build the disk image.

**Note:** it's important to compile the m5 binary with `-DM5_ADDR=0xFFFF0000` as is default in the SConscript.
This address is used by the guest binary to communicate with the simulator.
If you change the address in the guest binary, you also have to update the simulator to use the new address.
Additionally, when running in KVM, it is required that you use the *address* form of guest<->simulator communication
and not the pseudo instruction form (i.e., using `-DM5_ADDR` is *required* when compiling a guest binary for which
you want to run in KVM mode on gem5).

To compile m5 binary, in the root folder of the experiment,

```sh
cd gem5/util/m5/
scons build/x86/out/m5
```

In `launch_spec2017_experiments.py`, we document the step in an Artifact object as follows,

```python
m5_binary = Artifact.registerArtifact(
    command = 'scons build/x86/out/m5',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/build/x86/out/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)
```

### Building the Disk Image
In this step, we will build the disk image using [packer](https://www.packer.io/).
**Note:** If you are interested in modifying the SPEC configuration file, [Appendix II](#TODO) describes how the scripts that build the disk image work.
Also, more information about using packer and building disk images can be found [here](../main-doc/disks.md).

First, we download the packer binary.
The current version of packer as of December 2020 is 1.6.6.

```sh
cd disk-image/
wget https://releases.hashicorp.com/packer/1.6.6/packer_1.6.6_linux_amd64.zip
unzip packer_1.6.6_linux_amd64.zip
rm packer_1.6.6_linux_amd64.zip
```

In `launch_spec2017_experiments.py`, we document how we obtain the binary as follows,

```python
packer = Artifact.registerArtifact(
    command = '''
        wget https://releases.hashicorp.com/packer/1.6.6/packer_1.6.6_linux_amd64.zip;
        unzip packer_1.6.6_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded from https://www.packer.io/.'
)
```

Second, we build the disk image.
The script `disk-image/spec-2017/spec-2017.json` specifies how the disk image is built.
In this step, we assume the SPEC 2017 ISO file is in the `disk-image/spec-2017` folder and the ISO file name is `cpu2017-1.1.0.iso`.
The path and the name of the ISO file could be changed in the JSON file.

To build the disk image, in the root folder of the experiment,

```sh
cd disk-image/
./packer validate spec-2017/spec-2017.json # validate the script, including checking the input files
./packer build spec-2017/spec-2017.json
```

The process should take about than an hour to complete on a fairly recent machine with a cable internet speed.
The disk image will be in `disk-image/spec-2017/spec-2017-image/spec-2017`.

**Note:** Packer will output a URL to a VNC server that could be connected to to inspect the building process.

**Note:** [More about using packer and building disk images](../main/disks).

Now, in `launch_spec2017_experiments.py`, we make an Artifact object of the disk image.

```python
disk_image = Artifact.registerArtifact(
    command = './packer build spec-2017/spec-2017.json',
    typ = 'disk image',
    name = 'spec-2017',
    cwd = 'disk-image/',
    path = 'disk-image/spec-2017/spec-2017-image/spec-2017',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu Server with SPEC 2017 installed, m5 binary installed and root auto login'
)
```

### Obtaining a Compiled Linux Kernel that Works with gem5
The compiled Linux kernel binaries that is known to work with gem5 can be found here: [https://www.gem5.org/documentation/general_docs/gem5_resources/](https://www.gem5.org/documentation/general_docs/gem5_resources/).

The Linux kernel configurations that are used to compile the Linux kernel binaries are documented and maintained in gem5-resources: [https://github.com/gem5/gem5-resources/tree/stable/src/linux-kernel/](https://github.com/gem5/gem5-resources/tree/stable/src/linux-kernel/).

The following command downloads the compiled Linux kernel of version 4.19.83.
In the root folder of the experiment,

```sh
wget http://dist.gem5.org/dist/v21-2/kernels/x86/static/vmlinux-4.19.83
```

Now, `in launch_spec2017_experiments.py`, we make an Artifact object of the Linux kernel binary.

```python
linux_binary = Artifact.registerArtifact(
    name = 'vmlinux-4.19.83',
    typ = 'kernel',
    path = './vmlinux-4.19.83',
    cwd = './',
    command = ''' wget http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-4.19.83''',
    inputs = [experiments_repo,],
    documentation = "kernel binary for v4.19.83",
)
```

### gem5 System Configurations
The gem5 system configurations can be found in the `configs/` folder.
The gem5 run script located in `configs/run_spec.py`, takes the following parameters:
* `--kernel`: (required) the path to vmlinux file.
* `--disk`: (required) the path to spec image.
* `--cpu`: (required) name of the detailed CPU model.
Currently, we are supporting the following CPU models: kvm, o3, atomic, timing.
More CPU models could be added to getDetailedCPUModel() in run_spec.py.
* `--benchmark`: (required) name of the SPEC CPU 2017 benchmark.
The availability of the benchmarks could be found at the end of the tutorial.
* `--size`: (required) size of the benchmark. There are three options: ref, train, test.
* `--no-copy-logs`: this is an optional parameter specifying whether the spec log files should be copied to the host system.
* `--allow-listeners`: this is an optional parameter specifying whether gem5 should open ports so that gdb or telnet could connect to. No listeners are allowed by default.

We don't use another Artifact object to document this file.
The Artifact repository object of the root folder will keep track of the changes of the script.

**Note:** [The first two parameters of the gem5 run script for full system simulation should always be the path to the linux binary and the path to the disk image, in that order](../main/run)

## Running the Experiment
### Setting up the Python virtual environment
gem5art code works with Python 3.5 or above.

The following script will set up a python3 virtual environment named gem5art-env. In the root folder of the experiment,

```sh
virtualenv -p python3 gem5art-env
```

To activate the virtual environment, in the root folder of the experiment,

```sh
source gem5art-env/bin/activate
```

To install the gem5art dependency (this should be done when we are in the virtual environment),

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

To exit the virtual environment,

```sh
deactivate
```

**Note:** the following steps should be done while using the Python virtual environment.

### Running the Database Server
The following script will run the MongoDB database server in a docker container.

```sh
docker run -p 27017:27017 -v /path/in/host:/data/db --name mongo-1 -d mongo
```

The -p 27017:27017 option maps the port 27017 in the container to port 27017 on the host.
The -v /path/in/host:/data/db option mounts the /data/db folder in the docker container to the folder /path/in/host in the host.
The path of the host folder should an absoblute path, and the database files created by MongoDB will be in that folder.
The --name mongo-1 option specifies the name of the docker container.
We can use this name to identify to the container.
The -d option will let the container run in the background.
mongo is the name of [the offical mongo image](https://hub.docker.com/_/mongo).


### Running Celery Server (optional)
This step is only necessary if you want to use Celery to manage processes.
Inisde the path in the host specified above,

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

### Creating the Launch Script Running the Experiment
Now, we can put together the run script!
In launch_spec2017_experiments.py, we import the required modules and classes at the beginning of the file,

```python
import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_job_pool
```

And then, we put the launch function at the end of launch_spec2017_experiments.py,

```python
if __name__ == "__main__":
    cpus = ['kvm', 'atomic', 'o3', 'timing']
    benchmark_sizes = {'kvm':    ['test', 'ref'],
                       'atomic': ['test'],
                       'o3':     ['test'],
                       'timing': ['test']
                      }
    benchmarks = ["503.bwaves_r", "507.cactuBSSN_r", "508.namd_r", "510.parest_r", "511.povray_r", "519.lbm_r",
                  "521.wrf_r", "526.blender_r", "527.cam4_r", "538.imagick_r", "544.nab_r", "549.fotonik3d_r",
                  "554.roms_r", "997.specrand_fr", "603.bwaves_s", "607.cactuBSSN_s", "619.lbm_s", "621.wrf_s",
                  "627.cam4_s", "628.pop2_s", "638.imagick_s", "644.nab_s", "649.fotonik3d_s", "654.roms_s",
                  "996.specrand_fs", "500.perlbench_r", "502.gcc_r", "505.mcf_r", "520.omnetpp_r", "523.xalancbmk_r",
                  "525.x264_r", "531.deepsjeng_r", "541.leela_r", "548.exchange2_r", "557.xz_r", "999.specrand_ir",
                  "600.perlbench_s", "602.gcc_s", "605.mcf_s", "620.omnetpp_s", "623.xalancbmk_s", "625.x264_s",
                  "631.deepsjeng_s", "641.leela_s", "648.exchange2_s", "657.xz_s", "998.specrand_is"]

    runs = []
    for cpu in cpus:
        for size in benchmark_sizes[cpu]:
            for benchmark in benchmarks:
                run = gem5Run.createFSRun(
                    'gem5 v20.1.0.4 spec 2017 experiment', # name
                    'gem5/build/X86/gem5.opt', # gem5_binary
                    'gem5-configs/run_spec.py', # run_script
                    'results/{}/{}/{}'.format(cpu, size, benchmark), # relative_outdir
                    gem5_binary, # gem5_artifact
                    gem5_repo, # gem5_git_artifact
                    run_script_repo, # run_script_git_artifact
                    'linux-4.19.83/vmlinux-4.19.83', # linux_binary
                    'disk-image/spec2017/spec2017-image/spec2017', # disk_image
                    linux_binary, # linux_binary_artifact
                    disk_image, # disk_image_artifact
                    cpu, benchmark, size, # params
                    timeout = 10*24*60*60 # 10 days
                )
                runs.append(run)


    run_job_pool(runs)
```
The above launch function will run the all the available benchmarks with kvm, atomic, timing, and o3 cpus.
For kvm, both test and ref sizes will be run, while for the rest, only benchmarks of size test will be run.

Note that the line `'results/{}/{}/{}'.format(cpu, size, benchmark), # relative_outdir` specifies how the results folder is structured.
The results folder should be carefully structured so that there does not exist two gem5 runs write to the same place.

### Run the Experiment
Having celery and mongoDB servers running, we can start the experiment.

In the root folder of the experiment,

```sh
python3 launch_spec2017_experiment.py
```

**Note:** The URI to a remote database server could be specified by specifying the environment variable `GEM5ART_DB`.
For example, if the mongo database server is running at `localhost123`, the command to run the launch script would be,
```sh
GEM5ART_DB="mongodb://localhost123" python3 launch_spec2017_experiment.py
```

## Appendix I. Working Status
Not all benchmarks are compiled in the above set up as of March 2020.
The working status of SPEC 2017 workloads is available here: [https://www.gem5.org/documentation/benchmark_status/gem5-20#spec-2017-tests](https://www.gem5.org/documentation/benchmark_status/gem5-20#spec-2017-tests).

## Appendix II. Disk Image Generation Scripts
`disk-image/spec-2017/install-spec2017.sh`: a Bash script that will be executed on the guest machine after Ubuntu Server is installed in the disk image; this script installs depedencies to compile and run SPEC workloads, mounts the SPEC ISO and installs the benchmark suite on the disk image, and creates a SPEC configuration from gcc42 template.


`disk-image/spec-2017/post-installation.sh`: a script that will be executed on the guest machine; this script copies the `serial-getty@.service` file to the `systemd` folder, copies m5 binary to `/sbin`, and appends the content of `runscript.sh` to the disk image's `.bashrc` file, which will be executed after the booting process is done.

`disk-image/spec-2017/runscript.sh`: a script that will be copied to `.bashrc` on the disk image so that the commands in this script will be run immediately after the booting process.

`disk-image/spec-2017/spec-2017.json`: contains a configuration telling Packer how the disk image should be built.


---


## Microbench Tutorial

*Source: https://www.gem5.org/documentation/gem5art/tutorials/microbench-tutorial*

# Tutorial: Run Microbenchmarks with gem5

## Introduction
In this tutorial, we will learn how to run some simple microbenchmarks using gem5art.
Microbenchmarks are small benchmarks designed to test a component of a larger system.
The particular microbenchmarks we are using in this tutorial were originally developed at the
[University of Wisconsin-Madison](https://github.com/VerticalResearchGroup/microbench).
This microbenchmark suite is divided into different control, execution and memory benchmarks.
We will use system emulation (SE) mode of gem5 to run these microbenchmarks with gem5.


This tutorial follows the following directory structure:

- configs-micro-tests: the base gem5 configuration to be used to run SE mode simulations
- gem5: gem5 [source code](https://github.com/gem5/gem5) and the compiled binary

- results: directory to store the results of the experiments (generated once gem5 jobs are executed)
- launch_micro_tests.py: gem5 jobs launch script (creates all of the needed artifacts as well)


## Setting up the environment
First, we need to create the main directory named micro-tests (from where we will run everything) and turn it into a git repository like we did in the previous tutorials.
Next, add a git remote to this repo pointing to a remote location where we want this repo to be hosted.

```sh
mkdir micro-tests
cd micro-tests
git init
git remote add origin https://your-remote-add/micro-tests.git
```

We also need to add a .gitignore file in our git repo to leave unnecessary files untracked:

```
*.pyc
m5out
.vscode
results
gem5
venv
```

Next, we will create a virtual python3 environment before using gem5art.

```sh
virtualenv -p python3 venv
source venv/bin/activate
```
This virtual environment needs to be running in order to run experiments with gem5art.
You can deactivate the environment at any time with the command `deactivate`.

gem5art can be installed (if not already) using pip:

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

## Build gem5

First clone gem5 in your micro-tests repo:

```sh
git clone https://github.com/gem5/gem5
cd gem5
```

Before building gem5, we need to apply a [patch](https://github.com/darchr/gem5/commit/38d07ab0251ea8f5181abc97a534bb60157b2b5d) to the source repo.
As you will later see, we will run gem5 with various memory configs.
**Inf** (SimpleMemory with 0ns latency) and **SingleCycle** (SimpleMemory with 1ns latency) do not use any caches.
Therefore, to implement cacheless SimpleMemory, we need to add support of vector ports in SimpleMemory by applying this patch.
This becomes necessary as we need to connect cpu's icache and dcache ports to the mem_ctrl port (a vector port).
You can download and apply the patch as follows:

```sh
wget https://github.com/darchr/gem5/commit/f0a358ee08aba1563c7b5277866095b4cbb7c36d.patch
git am f0a358ee08aba1563c7b5277866095b4cbb7c36d.patch --reject
```

Now, build gem5:

```sh
scons build/X86/gem5.opt -j8
```

## Download and compile the microbenchmarks
Download the microbenchmarks:

```sh
git clone https://github.com/darchr/microbench.git
```

Commit the source of microbenchmarks to the micro-tests repo, so that the current version of the microbenchmarks repo becomes a part of the micro-tests repository.

```sh
git add microbench/
git commit -m "Add microbenchmarks"
```

Compile the benchmarks:

```sh
cd microbench
make
```

By default, these microbenchmarks are compiled for the x86 ISA, which will be our focus in this tutorial.
You can use the following commands to compile these benchmarks for ARM and RISC-V ISAs if you wish to work with them.

```sh
make ARM

make RISCV
```

## gem5 run scripts

Now, we will add the gem5 run and configuration scripts to a new folder named `configs-micro-tests`.
Get the run script named run_micro.py from [here](https://github.com/darchr/gem5art/blob/master/docs/gem5-configs/configs-micro-tests/run_micro.py), and other system configuration file from
[here](https://github.com/darchr/gem5art/blob/master/docs/gem5-configs/configs-micro-tests/system.py).
The run script (run_micro.py) takes the following arguments:
- **cpu:** cpu type [**TimingSimple:** timing simple cpu model, **DerivO3:** O3 cpu model]
- **memory:** memory type [**Inf:** 0ns latency memory, **SingleCycle:** 1ns latency memory, **SlowMemory:** 100ns latency memory. All types have infinite bandwidth. Caches are only enabled for SlowMemory.]
- **benchmark:** benchmark binary to run with gem5



## Database and Celery Server

If not already running or created, you can create a database using:

```sh
docker run -p 27017:27017 -v <absolute path to the created directory>:/data/db --name mongo-<some tag> -d mongo
```
in a newly created directory.

If not already installed, install `RabbitMQ` on your system (before running celery) using:

```sh
apt-get install rabbitmq-server
```

Now, run the celery server using:

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

## Creating a launch script
Next, we will create a launch script with the name `launch_micro_tests.py`, which will register the artifacts to be used and will start gem5 jobs.

Like we did in previous tutorials, the first step is to import the required modules and classes:

```python
import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
```

Next, we will register the artifacts:

```python
experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/micro-tests.git',
    typ = 'git repo',
    name = 'micro-tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run microbenchmarks with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = '''git clone https://github.com/gem5/gem5;
    cd gem5;
    wget https://github.com/darchr/gem5/commit/38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch;
    git am 38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch --reject;
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'git repo with gem5 cloned on Nov 22 from github (patch applied to support mem vector port)'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'default gem5 x86'
)
```

The number of artifacts is less than what we had to use in previous (full-system) tutorials ([boot](boot-tutorial.md), [npb](npb-tutorial.md)), as expected.

Now to run the benchmarks, we will iterate through possible cpu types, memory types and all of the microbenchmarks from the microbench repository.
We will also register an artifact for each microbenchmark. If you want to run certain benchmarks, you can indicate which ones in the `bm_list` array.

```python

if __name__ == "__main__":

    cpu_types = ['TimingSimple', 'DerivO3']
    mem_types = ['Inf', 'SingleCycle', 'Slow']

    bm_list = []

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    for filename in os.listdir('microbench'):
        if os.path.isdir(f'microbench/{filename}') and filename != '.git':
            bm_list.append(filename)

    # create an artifact for each single microbenchmark
    for bm in bm_list:
        bm = Artifact.registerArtifact(
        command = '''
        cd microbench/{};
        make X86;
        '''.format(bm),
        typ = 'binary',
        name = bm,
        cwd = 'microbench/{}'.format(bm),
        path =  'microbench/{}/bench.X86'.format(bm),
        inputs = [experiments_repo,],
        documentation = 'microbenchmark ({}) binary for X86 ISA'.format(bm)
        )

    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                run = gem5Run.createSERun(
                    'microbench_tests',
                    'gem5/build/X86/gem5.opt',
                    'configs-micro-tests/run_micro.py',
                    'results/X86/run_micro/{}/{}/{}'.format(bm,cpu,mem),
                    gem5_binary,gem5_repo,experiments_repo,
                    cpu,mem,os.path.join('microbench',bm,'bench.X86'))
                run.run()

```

Note that, in contrast to previous tutorials ([boot](boot-tutorial), [npb](npb-tutorial)), we are using `createSERun()` this time, as we want to run gem5 in SE mode.
The full launch script is available [here](https://github.com/darchr/gem5art/blob/master/docs/launch-scripts/launch_micro_tests.py).

Once you run this launch script (as shown below), your microbenchmark experiments will start running, which will simulate execution of microbenchmarks on different cpu and memory types.

```python
python launch_micro_tests.py
```

Later, you can access the database to see the status of these jobs and further analyze the results of your microbenchmark experiments. Happy experimenting!


---


# ═══ Reporting Problems ═══


## Reporting Problems

*Source: https://www.gem5.orgdocumentation/reporting_problems/*

Many of the people in the [gem5 community](/ask-a-question) are happy
to help when someone has a problem or something doesn't work. However, please
keep in mind those working on gem5 have other commitments, so we'd appreciate,
prior to reporting, if users could put in some effort to solving their own
problems, or, at least, gather enough information to help others resolve the
issue.

Below we outline some general advise on issue reporting.

## Prior to reporting a problem

The most important thing to do prior to reporting a problem is to investigate
the issue as much as possible. This may lead you to a solution,
or enable you to provide more information to the gem5 community regarding the
problem. Below are a series of steps/checks we'd advise you carry out before
reporting an issue:

1. Please check if a similar question has already been asked on any of
[our channels](/ask-a-question) (check the archives as well).

2. Ensure you're compiling and running the latest version of [gem5](
https://github.com/gem5/gem5). The issue may have already been resolved.

3. Check changes [currently under review on our GitHub system](
https://github.com/gem5/gem5/pulls/). It's possible a fix to
your issue is already on its way to being merged into the project.

4. Make sure you're running with `gem5.opt` or `gem5.debug`, not `gem5.fast`.
The `gem5.fast` binary compiles out assertion checking for speed, so a problem
that causes a crash or an error on `gem5.fast` may result in a more informative
assertion failure with `gem5.opt` or `gem5.debug`.

5. If it seems appropriate, enable some debug flags (e.g.,`--debug-flags=Foo`
via the CLI). For more information on debug flags, please consult our
[debugging tutorial](/documentation/learning_gem5/part2/debugging).

6. Don't be afraid to debug using GDB if your problem is occurring on the C++
side.

# Reporting a problem

Once you believe you have gathered enough information about your problem. Then
feel free to report it.

* If you have a reason to believe your problem is a bug then please report the
issue on gem5's [GitHub issues](https://github.com/gem5/gem5/issues).
**Please include any information which may aid in someone else reproducing
this bug on their system**. Include the command line argument used, any
relevant system information (as a minimum, what OS are you using, and how
did you compile gem5?), error messages received, program outputs, stack traces,
etc.

* If you choose to ask a question on the [gem5 Discussions page](
https://github.com/orgs/gem5/discussions), please provide any information which
may be helpful. If you have a theory about what the problem might be, please let
us know, but include enough basic information so others can decide whether your
theory is correct or not.


# Solving the problem

If you have solved a problem that you reported, please let the community know
about your solution as a follow-up on your GitHub issue or discussion. If you
have fixed a bug, we'd appreciate if you could submit the fix to the gem5
source. Please see our [beginners guide to contributing](/contributing)
on how to do this.

If your issue is with the content of a gem5 document/tutorial being incorrect,
then please consider submitting a change. Please consult our [README](
https://github.com/gem5/website/blob/stable/README.md)
for more information on how to make contributions to the gem5 website.


---
