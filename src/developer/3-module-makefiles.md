# Module build configurations

This chapter explains the `require` build system interface for e3 module
makefiles. You will learn which variables to set, what they do, and how
to build and install a module locally using `make` (with dependencies provided
by your conda environment). We will not (yet) use conda's build tools.

## `require`'s build interface

Include `driver.makefile` from `require` and declare what to build and install - as well as pass
flags to the compiler and/or linker - using environment variables.

:::{tip}
Quick reference for common variables is available here:
[`require`'s build interface](../kb/1-build-interface.md)
:::

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

# EPICS base accepts CPPFLAGS (and CFLAGS, LDFLAGS, etc.) for user commands as USR_*
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

:::{tip}
For reference, iocStats is already built for e3, and has a makefile:
[`iocstats-recipe/src/Makefile`](https://gitlab.esss.lu.se/e3/recipes/iocstats-recipe/-/blob/master/src/Makefile?ref_type=heads)
(slightly modified above).
:::

### 4) Build and install

To build, we will need to pass some additional variables to require:

```console
(iocstats-build) $ make -f e3.makefile MODULE=iocstats LIBVERSION=dev
```

:::{dropdown} Show build log
:icon: code
:color: primary
:animate: fade-in

```console
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

:::

:::{note}
We have to define `MODULE` and `LIBVERSION` for require to know the name and version, respectively, of the
module in question.
:::

This compiles the sources against the EPICS base in your environment.

To install the module into the e3 layout, we would then just run the install command:

```console
(iocstats-build) $ make -f e3.makefile install
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
