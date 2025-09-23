# Module build configurations

This chapter explains the `require` build system interface for e3 module
makefiles. You will learn which variables to set, what they do, and how
to build and install a module locally using `make` (with dependencies provided
by your conda environment). We will not (yet) use conda's build tools.

## `require`'s build interface

Include `driver.makefile` from `require` and declare what to build and install - as well as pass
flags to the compiler and/or linker - using environment variables. The ones available from require are:

- `SOURCES` - Source files to compile into the shared library
- `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
- `HEADERS` - Header files that should be installed with the module
- `TEMPLATES` - Database or template files that should be installed in the
  `$(module_DB)` path
- `TMPS` - Templates files to inflate to db-file and install in in the
  `$(module_DB)` path
- `SUBS` - Substitutions files to inflate the template file to db-file and
  install in the `$(module_DB)` path
- `SCRIPTS` - Script files that are installed in `$(module_DIR)`
- `REQUIRED` - Specifies any non source-based dependencies
- `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories

:::{tip}
Quick reference for common variables is available here:
[`require`'s build interface](../kb/1-build-interface.md)
:::

The variables above handle most module build needs, but `require` inherits EPICS base's complete build system.
When you need custom compiler flags, linking options, etc. beyond what these variables provide, refer to EPICS
base's build documentation: [Application Developer's Guide: Build Facility](https://docs.epics-controls.org/en/latest/build-system/specifications.html).

A very small makefile can be as simple as:

```make
# This block is default, and should be included in all e3 makefiles
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(E3_REQUIRE_TOOLS)/driver.makefile

# Install database files and a "snippet" (.iocsh file)
TEMPLATES += $(wildcard $(where_am_I)/template/*.db)
SCRIPTS   += $(where_am_I)/iocsh/example.iocsh
```

## Example: Building iocStats with `make`

Below is a practical example using upstream iocStats sources, with an e3
makefile that tells `require` how to build and install the module.

### 1) Acquire iocStats' source code

```console
$ git clone https://github.com/epics-modules/iocStats.git
$ cd iocStats
```

:::{note}
If we wanted to acquire additional files, or perform "pre-build" actions (patching, etc.),
we would do so at this stage.
:::

### 2) Acquire build tools and dependencies

Create a conda environment that contains `epics-base`, `require`, and a compiler:

```console
$ conda create -n iocstats-build epics-base require gcc gxx
```

:::{note}
Which compiler to use will depend a bit on your platform, but `gcc` (and `gxx`) will work for Linux.
:::

Activate the environment:

```console
$ conda activate iocstats-build
```

### 3) Set up an e3 makefile

Create a makefile - we will name it `e3.makefile` since there already is a file named
`Makefile` in iocStats' repository root.

```make
# e3.makefile
where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(E3_REQUIRE_TOOLS)/driver.makefile

USR_CPPFLAGS += -DUSE_TYPED_RSET

DEVIOCSTATS := devIocStats

HEADERS += $(DEVIOCSTATS)/os/default/devIocStatsOSD.h
HEADERS += $(DEVIOCSTATS)/devIocStats.h

SOURCES += $(DEVIOCSTATS)/devIocStatsAnalog.c
SOURCES += $(DEVIOCSTATS)/devIocStatsString.c
SOURCES += $(DEVIOCSTATS)/devIocStatsWaveform.c
SOURCES += $(DEVIOCSTATS)/devIocStatsSub.c
SOURCES += $(DEVIOCSTATS)/devIocStatsTest.c

SOURCES += $(DEVIOCSTATS)/os/Linux/osdCpuUsage.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdCpuUtilization.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdFdUsage.c
SOURCES += $(DEVIOCSTATS)/os/Linux/osdMemUsage.c

SOURCES += $(DEVIOCSTATS)/os/default/osdWorkspaceUsage.c
SOURCES += $(DEVIOCSTATS)/os/default/osdClustInfo.c
SOURCES += $(DEVIOCSTATS)/os/default/osdSuspTasks.c
SOURCES += $(DEVIOCSTATS)/os/default/osdIFErrors.c
SOURCES += $(DEVIOCSTATS)/os/default/osdBootInfo.c

SOURCES += $(DEVIOCSTATS)/os/posix/osdSystemInfo.c
SOURCES += $(DEVIOCSTATS)/os/posix/osdHostInfo.c
SOURCES += $(DEVIOCSTATS)/os/posix/osdPIDInfo.c

DBDS    += $(DEVIOCSTATS)/devIocStats.dbd

SCRIPTS += iocsh/iocStats.iocsh

TEMPLATES += $(wildcard template/*.db)
TEMPLATES += $(wildcard template/*.template)

USR_DBFLAGS += -I . -I ..
USR_DBFLAGS += -I$(EPICS_BASE)/db
USR_DBFLAGS += -I$(where_am_I)/template

SUBS += $(wildcard template/*.substitutions)
```

### 4) Build and install

To build, we will need to pass some additional variables to require:

```console
(iocstats-build) $ make -f e3.makefile MODULE=iocstats LIBVERSION=dev build
```

:::{dropdown} Show build log
:icon: code
:color: primary
:animate: fade-in

```console
MAKING EPICS VERSION 7.0.9.0
mkdir -p O.7.0.9.0_Common
make -f e3.makefile T_A=linux-x86_64 build
make[1]: Entering directory '/home/johndoe/iocStats'
mkdir -p O.7.0.9.0_linux-x86_64
make[2]: Entering directory '/home/johndoe/iocStats/O.7.0.9.0_linux-x86_64'
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/posix/osdPIDInfo.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/posix/osdHostInfo.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/posix/osdSystemInfo.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/default/osdBootInfo.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/default/osdIFErrors.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/default/osdSuspTasks.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/default/osdClustInfo.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/default/osdWorkspaceUsage.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/Linux/osdMemUsage.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/Linux/osdFdUsage.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/Linux/osdCpuUtilization.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/os/Linux/osdCpuUsage.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/devIocStatsTest.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/devIocStatsSub.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/devIocStatsWaveform.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/devIocStatsString.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c  ../devIocStats/devIocStatsAnalog.c
Expanding iocstats.dbd
perl -CSD /home/johndoe/miniconda3/envs/e3/epics/bin/linux-x86_64/dbdExpand.pl -A -I ../devIocStats/ -I /home/johndoe/miniconda3/envs/e3/epics/dbd -o iocstats.dbd ../devIocStats/devIocStats.dbd
Device 'IOC stats' refers to unknown record type 'ai'.
Record type 'ai' declared.
Device 'IOC stats' refers to unknown record type 'ao'.
Record type 'ao' declared.
Device 'IOC stats' refers to unknown record type 'stringin'.
Record type 'stringin' declared.
Device 'IOC stats' refers to unknown record type 'waveform'.
Record type 'waveform' declared.
perl -CSD /home/johndoe/miniconda3/envs/e3/epics/bin/linux-x86_64/registerRecordDeviceDriver.pl iocstats.dbd iocstats_registerRecordDeviceDriver | grep -v 'iocshRegisterCommon();' > iocstats_registerRecordDeviceDriver.cpp
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall              -mtune=generic              -m64  -fPIC          -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c iocstats_registerRecordDeviceDriver.cpp
echo "char _iocstatsLibRelease[] = \"dev\";" >> iocstats_version_dev.c
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_DSET  -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/ -I/home/johndoe/miniconda3/envs/e3/modules/require/5.1.1.post2/include -I/home/johndoe/miniconda3/envs/e3/epics/include -I/home/johndoe/miniconda3/envs/e3/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/e3/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/e3/include           -c iocstats_version_dev.c
Collecting dependencies
rm -f iocstats.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/johndoe/miniconda3/envs/e3/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/johndoe/miniconda3/envs/e3/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > iocstats.dep.tmp
cat iocstats.dep.tmp | sort -u >> iocstats.dep
/home/johndoe/miniconda3/envs/e3/bin/x86_64-conda-linux-gnu-g++ -o libiocstats.so  -shared -fPIC -Wl,-hlibiocstats.so -L/home/johndoe/miniconda3/envs/e3/modules/iocstats/dev/lib/linux-x86_64 -Wl,-rpath,/home/johndoe/miniconda3/envs/e3/modules/iocstats/dev/lib/linux-x86_64                  -rdynamic -Wl,--disable-new-dtags -Wl,-rpath,/home/johndoe/miniconda3/envs/e3/lib -Wl,-rpath-link,/home/johndoe/miniconda3/envs/e3/lib -L/home/johndoe/miniconda3/envs/e3/lib -Wl,-rpath-link,/home/johndoe/miniconda3/envs/e3/epics/lib/linux-x86_64 -m64                   devIocStatsAnalog.o devIocStatsString.o devIocStatsSub.o devIocStatsTest.o devIocStatsWaveform.o osdCpuUsage.o osdCpuUtilization.o osdFdUsage.o osdMemUsage.o osdBootInfo.o osdClustInfo.o osdIFErrors.o osdSuspTasks.o osdWorkspaceUsage.o osdHostInfo.o osdPIDInfo.o osdSystemInfo.o iocstats_registerRecordDeviceDriver.o iocstats_version_dev.o      -lpthread    -lm -lrt -ldl -lgcc
make[2]: Leaving directory '/home/johndoe/iocStats/O.7.0.9.0_linux-x86_64'
make[1]: Leaving directory '/home/johndoe/iocStats'
```

:::

:::{note}
We have to define `MODULE` and `LIBVERSION` for require to know the name and version, respectively, of the
module in question.
:::

This compiles the sources against the EPICS base in your environment.

To install the module into the e3 layout, we would then just run the install command:

```console
(iocstats-build) $ make -f e3.makefile MODULE=iocstats LIBVERSION=dev install
```

:::{note}
We are already leveraging conda features for things like dependency resolution; you will have seen during
the environment creation step that it pulled down many more packages than just the three we specified, and
packages like `epics-base` and `require` will also set variables and modify paths that we utilise. But you
will see in later chapters that when we diverge from invoking `make` directly, things are further simplified.
:::

### 5) Start an IOC and load iocStats

With the module installed, you can start an IOC shell and load the module:

```console
(iocstats-build) $ iocsh -r iocstats
```

:::{dropdown} Show IOC log
:icon: code
:color: primary
:animate: fade-in

```console
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

:::

If everything is wired correctly, the module libraries and database definitions
are available, and all data files (database files, snippets, etc.) can be loaded.

---

:::{seealso}

- Back: [Module build recipes](2-recipes.md)
- Next: [Module creation](4-e3-conda-pkgs.md)

:::
