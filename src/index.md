# ESS EPICS Environment (e3)

:::{important}
**Major Update: e3 is now powered by conda!**

These are the **new documentation pages** for the redesigned ESS EPICS Environment (e3). We have made a major technical
and architectural switch to a conda-based approach for better package management and reproducibility.

**Looking for the previous e3 documentation?** The original build-tools based documentation can still be found at
[http://e3.pages.esss.lu.se/e3-build-tools](http://e3.pages.esss.lu.se/e3-build-tools/) (note that secure HTTP
currently does not work).

Please beware that we currently are in the midst of the transition, and that some examples here in this documentation
might not yet work without alterations.
:::

Welcome to the documentation for ESS EPICS Environment (e3) - a toolkit designed to simplify EPICS development and
deployment at the European Spallation Source.

## What is e3?

e3 is a design concept and toolkit that:

- **Simplifies development** by abstracting away low-level EPICS complexities
- **Manages dependencies** automatically across EPICS modules

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

e3 evolved from ESS's previous EPICS environments (CODAC, EEE) and is based on PSI's EPICS environment. It uses a
fork of PSI's require module, git, and module wrappers to manage dependencies and site-specific modifications.

The toolkit handles complex dependency chains, compiles shared libraries, and manages installations - with much of
the heavy lifting done by conda.

:::{note}
e3 focuses on EPICS environments and module management. IOC management tools (systemd, procServ, conserver) and
client applications (CS-Studio, DisplayBuilder, ChannelFinder) are separate systems.
:::

## EPICS resources

- Website: [epics-controls.org](https://epics-controls.org/)
- Documentation: [docs.epics-controls.org](https://docs.epics-controls.org/)

::::{tip}
For questions, see [EPICS chat](https://epics-controls.org/epics-chat/) and [tech-talk mailing lists](https://epics-controls.org/resources-and-support/mailing-lists/).
::::

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting Started
:glob:
1-getting-started/1*
1-getting-started/2*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: User Documentation
:glob:
2-user/1*
2-user/2*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Developer Documentation
:glob:
3-developer/1*
3-developer/2*
3-developer/3*
3-developer/4*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Knowledge Base
:glob:
4-kb/1*
4-kb/2*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Maintainer Documentation
:glob:
5-maintainer/1*
```
