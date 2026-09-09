# ESS EPICS Environment (e3)

Welcome to the documentation for ESS EPICS Environment (e3) - a toolkit designed to simplify EPICS development and
deployment at the [European Spallation Source](https://ess.eu).

## What is e3?

e3 is a design concept and toolkit that:

- **Enables dynamic loading** of EPICS modules at runtime without IOC build steps
- **Wraps upstream modules** with site-specific modifications while avoiding forks
- **Resolves dependency graphs** automatically via conda package management
- **Provides isolated environments** to run multiple IOCs with different module sets on the same host

For example, when you install the stream module, conda automatically resolves and installs all its dependencies (such as
asyn and base) in a virtual environment. You can then switch between different versions of any module simply by changing
a single line in your IOC configuration, and you can simultaneously run IOCs that require different versions of e.g.
EPICS base.

## Prerequisites

e3 assumes familiarity with several key technologies. Before getting started, you should be comfortable with:

- **EPICS** - The Experimental Physics and Industrial Control System
   - [docs.epics-controls.org](https://docs.epics-controls.org/)
   - [Getting started guide](https://docs.epics-controls.org/en/latest/getting-started/EPICS_Intro.html)
- **Git** - Version control system used for module management
   - [git-scm.com/doc](https://git-scm.com/doc)
   - [Tutorial](https://git-scm.com/docs/gittutorial)
- **Linux/Unix** - Command line and system administration basics
   - [Command line tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)
- **Make and build systems** - Understanding makefiles and build processes
   - [GNU Make manual](https://www.gnu.org/software/make/manual/)
   - [Make tutorial](https://makefiletutorial.com/)

:::{tip}
If you're new to any of these technologies, we recommend reviewing the linked documentation before proceeding with e3.
:::

## Background

e3 evolved from earlier EPICS environments at ESS and draws inspiration from PSI's EPICS environment. At its core, it uses
the *require* module (originally developed at PSI) combined with conda package management to handle dependencies and
site-specific modifications.

The toolkit handles complex dependency chains, compiles shared libraries, and manages installations - with much of the heavy
lifting done by conda.

:::{note}
e3 focuses on EPICS environments and module management. IOC management tools (systemd, procServ, conserver) and
client applications (CS-Studio, DisplayBuilder, ChannelFinder) are separate systems.
:::

:::{toctree}
:hidden:
:maxdepth: 2
:caption: Getting Started

getting-started/installation
getting-started/your-first-ioc
:::

:::{toctree}
:hidden:
:maxdepth: 2
:caption: User Documentation

user/environments
user/iocs-and-modules
:::

:::{toctree}
:hidden:
:maxdepth: 2
:caption: Developer Documentation

developer/building-modules
developer/recipes
developer/makefiles
developer/packaging-modules
:::

:::{toctree}
:hidden:
:maxdepth: 2
:caption: API Reference

reference/build-interface
reference/iocsh
reference/require
:::

:::{toctree}
:hidden:
:maxdepth: 2
:caption: Maintainer Documentation

maintainer/build-process
maintainer/module-load
:::
