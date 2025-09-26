# Module build configurations

This chapter explains the `require` build system interface for e3 module
makefiles. You will learn which variables to set, what they do, and how
to build and install a module locally using `make` (with dependencies provided
by your conda environment). We will not (yet) use conda's build tools.

:::{note}
This guide assumes familiarity with makefiles and build systems. If you need a refresher:

- [GNU Make manual](https://www.gnu.org/software/make/manual/) - comprehensive reference
- [Make tutorial](https://makefiletutorial.com/) - practical introduction
- [EPICS build system](https://docs.epics-controls.org/en/latest/build-system/specifications.html) - EPICS-specific
  build concepts

:::

## `require`'s build interface

Include `driver.makefile` from `require` and declare what to build and install - as well as pass
flags to the compiler and/or linker - using environment variables. The ones available from require are:

- `SOURCES` - Source files to compile into the shared library
- `DBDS` - Database definition files to include
- `HEADERS` - Header files that should be installed
- `TEMPLATES` - Database or template files that should be installed
- `TMPS` - Templates files to inflate to db-file and install
- `SUBS` - Substitutions files to inflate the template file to db-file and install
- `SCRIPTS` - Script files that should be installed

:::{tip}
Quick reference for common variables is available here:
[`require`'s build interface](../4-kb/1-build-interface.md). For build targets, see [`require`'s build targets](../4-kb/2-build-targets.md).
:::

The variables above handle most module build needs, but `require` inherits EPICS base's complete build system.
When you need custom compiler flags, linking options, etc. beyond what these variables provide, refer to EPICS
base's build documentation: [Application Developer's Guide: Build Facility](https://docs.epics-controls.org/en/latest/build-system/specifications.html).

A very small makefile can be as simple as:

```make
# This row is default, and must be included in all e3 makefiles
include $(E3_REQUIRE_TOOLS)/driver.makefile

# Install database files and a "snippet" (.iocsh file)
# The $(where_am_I) variable is provided by require and will point to the module's root directory
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

:::{caution}
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

TEMPLATES += $(wildcard template/*.db)
TEMPLATES += $(wildcard template/*.template)

USR_DBFLAGS += -I$(where_am_I)/template

SUBS += $(wildcard template/*.substitutions)
```

### 4) Build and install

To build, we will need to pass some additional variables to require:

```console
(iocstats-build) $ make -f e3.makefile MODULE=iocstats build
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
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/posix/osdPIDInfo.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/posix/osdHostInfo.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/posix/osdSystemInfo.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/default/osdBootInfo.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/default/osdIFErrors.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/default/osdSuspTasks.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/default/osdClustInfo.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/default/osdWorkspaceUsage.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/Linux/osdMemUsage.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/Linux/osdFdUsage.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/Linux/osdCpuUtilization.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/os/Linux/osdCpuUsage.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/devIocStatsTest.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/devIocStatsSub.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/devIocStatsWaveform.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/devIocStatsString.c
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall -Werror-implicit-function-declaration             -std=gnu17  -mtune=generic     -m64  -fPIC           -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c  ../devIocStats/devIocStatsAnalog.c
Expanding iocstats.dbd
perl -CSD /home/johndoe/miniconda3/envs/iocstats-build/epics/bin/linux-x86_64/dbdExpand.pl -A -I ../devIocStats/ -I /home/johndoe/miniconda3/envs/iocstats-build/epics/dbd -o iocstats.dbd ../devIocStats/devIocStats.dbd
Device 'IOC stats' refers to unknown record type 'ai'.
Record type 'ai' declared.
Device 'IOC stats' refers to unknown record type 'ao'.
Record type 'ao' declared.
Device 'IOC stats' refers to unknown record type 'stringin'.
Record type 'stringin' declared.
Device 'IOC stats' refers to unknown record type 'waveform'.
Record type 'waveform' declared.
perl -CSD /home/johndoe/miniconda3/envs/iocstats-build/epics/bin/linux-x86_64/registerRecordDeviceDriver.pl iocstats.dbd iocstats_registerRecordDeviceDriver | grep -v 'iocshRegisterCommon();' > iocstats_registerRecordDeviceDriver.cpp
sed -i'.bak' -E '/^.*= Registration\(\)\;$/d' iocstats_registerRecordDeviceDriver.cpp
echo "#include <init.cpp>" >> iocstats_registerRecordDeviceDriver.cpp
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET          -DUSE_TYPED_RSET  -D_X86_64_ -DUNIX  -Dlinux             -MD -DMODULE_NAME='"iocstats"' -DLIBVERSION='"dev"'    -O3 -g   -Wall              -mtune=generic              -m64  -fPIC          -I/home/johndoe/miniconda3/envs/iocstats-build/epics-modules/require/ -I. -I../devIocStats/ -I../devIocStats//os/Linux -I../devIocStats//os/posix -I../devIocStats//os/default -I../devIocStats/os/Linux/ -I../devIocStats/os/default/ -I../devIocStats/os/posix/  -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/compiler/gcc -I/home/johndoe/miniconda3/envs/iocstats-build/epics/include/os/Linux              -I/home/johndoe/miniconda3/envs/iocstats-build/include           -c iocstats_registerRecordDeviceDriver.cpp
/home/johndoe/miniconda3/envs/iocstats-build/bin/x86_64-conda-linux-gnu-g++ -o libiocstats.so  -shared -fPIC -Wl,-hlibiocstats.so -L/home/johndoe/miniconda3/envs/iocstats-build/lib -Wl,-rpath,/home/johndoe/miniconda3/envs/iocstats-build/lib                  -rdynamic -Wl,--disable-new-dtags -Wl,-rpath,/home/johndoe/miniconda3/envs/iocstats-build/lib -Wl,-rpath-link,/home/johndoe/miniconda3/envs/iocstats-build/lib -L/home/johndoe/miniconda3/envs/iocstats-build/lib -Wl,-rpath-link,/home/johndoe/miniconda3/envs/iocstats-build/epics/lib/linux-x86_64 -m64                   iocstats_registerRecordDeviceDriver.o devIocStatsAnalog.o devIocStatsString.o devIocStatsSub.o devIocStatsTest.o devIocStatsWaveform.o osdCpuUsage.o osdCpuUtilization.o osdFdUsage.o osdMemUsage.o osdBootInfo.o osdClustInfo.o osdIFErrors.o osdSuspTasks.o osdWorkspaceUsage.o osdHostInfo.o osdPIDInfo.o osdSystemInfo.o      -lpthread    -lm -lrt -ldl -lgcc
make[2]: Leaving directory '/home/johndoe/iocStats/O.7.0.9.0_linux-x86_64'
make[1]: Leaving directory '/home/johndoe/iocStats'
```

:::

:::{note}
We have to define `MODULE` for require to know the name of the module in question.
:::

This compiles the sources against the EPICS base in your environment.

To install the module into the e3 layout, we would then just run the install command:

```console
(iocstats-build) $ make -f e3.makefile MODULE=iocstats install
```

:::{dropdown} Show install log
:icon: code
:color: primary
:animate: fade-in

```console
MAKING EPICS VERSION 7.0.9.0
make -f e3.makefile T_A=linux-x86_64 install
make[1]: Entering directory '/home/johndoe/iocStats'
make[2]: Entering directory '/home/johndoe/iocStats/O.7.0.9.0_linux-x86_64'
Installing generic include file /home/johndoe/miniconda3/envs/iocstats-build/include/devIocStatsOSD.h
Installing generic include file /home/johndoe/miniconda3/envs/iocstats-build/include/devIocStats.h
Installing module dbd file(s) iocstats.dbd to /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/iocstats/dbd
perl -CSD /home/johndoe/miniconda3/envs/iocstats-build/epics/bin/linux-x86_64/installEpics.pl  -d -m444 iocstats.dbd /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/iocstats/dbd
mkdir /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/iocstats
mkdir /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/iocstats/dbd
Installing module library /home/johndoe/miniconda3/envs/iocstats-build/lib/libiocstats.so
perl -CSD /home/johndoe/miniconda3/envs/iocstats-build/epics/bin/linux-x86_64/installEpics.pl  -d -m755 libiocstats.so /home/johndoe/miniconda3/envs/iocstats-build/lib
make[2]: Leaving directory '/home/johndoe/iocStats/O.7.0.9.0_linux-x86_64'
make[1]: Leaving directory '/home/johndoe/iocStats'
```

:::

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

       ,----.     ,--. ,-----.  ,-----.           ,--.            ,--.,--.
 ,---. '.-.  |    |  |'  .-.  ''  .--./     ,---. |  ,---.  ,---. |  ||  |
| .-. :  .' <     |  ||  | |  ||  |        (  .-' |  .-.  || .-. :|  ||  |
\   --./'-'  |    |  |'  '-'  ''  '--'\    .-'  `)|  | |  |\   --.|  ||  |
 `----'`----'     `--' `-----'  `-----'    `----' `--' `--' `----'`--'`--'

Starting e3 IOC shell version 6.0.0rc2
DEBUG: PID for iocsh 364538
DEBUG: Script path is /home/johndoe/miniconda3/envs/iocstats-build/bin/iocsh
DEBUG: Executed from /home/johndoe/iocStats
DEBUG: Temporary startup script at /tmp/tmp9ilgca6g
DEBUG: Running command `softIocPVX -D /home/johndoe/miniconda3/envs/iocstats-build/pvxs/dbd/softIocPVX.dbd /tmp/tmp9ilgca6g`
INFO: PVXS QSRV2 is loaded, permitted, and ENABLED.
epicsEnvSet REQUIRE_IOC "TEST:johndoe-364538"
epicsEnvSet IOCSH_TOP "/home/johndoe/iocStats"
epicsEnvSet IOCSH_PS1 "localhost-364538 > "
errlogInit2 2048 2047
dlload /home/johndoe/miniconda3/envs/iocstats-build/lib/librequire.so
Loading dbd file /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/require/dbd/require.dbd
Loading module info records for require
require iocstats
Loading dbd file /home/johndoe/miniconda3/envs/iocstats-build/epics-modules/iocstats/dbd/iocstats.dbd
Loading module info records for iocstats
No template path found for iocstats. Skipping.
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.9
## Rev. 2025-09-15T12:50+0000
## Rev. Date build date/time:
############################################################################
iocRun: All initialization complete
localhost-364538 >
```

:::

If everything is wired correctly, the module libraries and database definitions
are available, and all data files (database files, snippets, etc.) can be loaded.
