# ESS EPICS Environment (e3)

ESS' EPICS Environment (e3) is a design concept and a toolkit intended to

1. facilitate development by abstracting away some of the low-level complexities
   intrinsic to large EPICS implementations (primarily dependency management),
   and to
2. allow for more manageable quality control of released modules as well as
   IOCs.

ESS has gone through a few different EPICS environments during its construction
phase. First *CODAC* (from *[ITER](https://www.iter.org/)*), then *EEE* (short
for ESS EPICS Environment), then EEE version 2, and then finally a major revamp
to *e3*. Both EEE and e3 were based off of *[PSI](https://www.psi.ch/en)*'s
EPICS environment.

In short, e3 is a number of EPICS environments and a front-end for users
and developers at ESS to use these, as well as a collection of utilities to set up
and maintain said environments. The intention was twofold with e3: to
simplify life for integrators, but also for a central team managing the
environment. At the core of e3 is a fork of PSI's
[*require*](https://github.com/paulscherrerinstitute/require) module, *git*,
and *module wrappers*.

Two of the key design considerations for e3 were dependency management and
quality management. EPICS modules vary in structure and in quality, and each
site that uses EPICS has their own style and conventions, which will be
reflected in the source code. Furthermore, each module release will have
dependencies upon specific releases of other modules. How e3 deals with these is
to interface all community "modules" with a wrapper. This wrapper links to the
module source code, identifies module dependencies and versions, and contains
our site-specific modifications; patches, database files, GUIs, etc. When a
build occurs, e3 parses these dependency chains to find the necessary
dependencies, compiles shared libraries, inflates and copies database files, and
finally manages installations. This allows us to keep track of what
module version has been built for what version of EPICS base
and *require*, as well as allows for removal of deprecated versions. Many of these
aforementioned steps are, in fact, handled by `conda`.

:::{note}
There is an associated toolsuite (*systemd*,
*procServ*, *conserver*, etc.) used to manage IOCs at ESS, but these are
decoupled from e3, just as client and service applications (such as *CS-Studio*,
*DisplayBuilder*, *ChannelFinder*, and so on) are.
:::

---

```{toctree}
:maxdepth: 2
:caption: Getting Started
:glob:
getting-started/1*
getting-started/2*
```

```{toctree}
:maxdepth: 2
:caption: User Documentation
:glob:
user/1*
user/2*
```

```{toctree}
:maxdepth: 2
:caption: Developer Documentation
:glob:
developer/1*
developer/2*
```

```{toctree}
:maxdepth: 2
:caption: Knowledge-base
kb/guide/index.md
```
