# ESS EPICS Environment (e3)

Welcome to the documentation for ESS EPICS Environment (e3) - a toolkit designed to simplify EPICS development and
deployment at the European Spallation Source.

## What is e3?

e3 is a design concept and toolkit that:

- **Simplifies development** by abstracting away low-level EPICS complexities
- **Manages dependencies** automatically across EPICS modules

## Background

e3 evolved from ESS's previous EPICS environments (CODAC, EEE) and is based on PSI's EPICS environment. It uses a
fork of PSI's require module, git, and module wrappers to manage dependencies and site-specific modifications.

The toolkit handles complex dependency chains, compiles shared libraries, and manages installations - with much of
the heavy lifting done by conda.

:::{note}
e3 focuses on EPICS environments and module management. IOC management tools (systemd, procServ, conserver) and
client applications (CS-Studio, DisplayBuilder, ChannelFinder) are separate systems.
:::

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting Started
:glob:
getting-started/1*
getting-started/2*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: User Documentation
:glob:
user/1*
user/2*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Developer Documentation
:glob:
developer/1*
developer/2*
developer/3*
developer/4*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Knowledge Base
:glob:
kb/1*
kb/2*
kb/3*
kb/4*
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Maintainer Documentation
:glob:
maintainer/1*
```
