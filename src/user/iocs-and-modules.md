# IOCs and modules

:::{note}
The information on these pages assumes that the reader already is familiar with EPICS.
After all, e3 is just ESS' way of managing EPICS packages and site specific configurations.
:::

## An e3 IOC

An e3 IOC is broadly defined by just a startup script, that:

- identifies the modules needed by the IOC,
- defines the values for variables required by the module startup script
  snippets, and
- calls the module startup script snippets.

Shared libraries---and usually also data files like database files---are obtained
from EPICS modules.

As mentioned in [An e3 IOC](../getting-started/your-first-ioc.md), an e3 IOC is started
using the `iocsh` script and dynamically loads any additional modules using the [`require`](../getting-started/your-first-ioc.md#a-startup-script)
command.

## An e3 module

An EPICS module is a set of code, databases, sequences, and/or startup script
snippets that provides generic functionality for a particular device type or
logical function. In e3, an EPICS module can also be specific to one instance of
a device type. Of note here is that e3 does not differentiate between types of
EPICS modules (applications, libraries).

An IOC is built up from one or more modules, based on the requirements of that
particular IOC. A module is not a functional IOC application on its own.

The databases provided by the module are typically in the form of templates. The
template includes macro values for the PV name prefix and potentially other
parameters. These macro values must be defined by the IOC.

### Where modules come from

Modules are distributed as conda packages. At ESS, many modules come from the
upstream EPICS community (like *asyn*, *StreamDevice*, *iocStats*), while others
are developed internally for site-specific needs.

When packaging upstream modules, we may bundle additional site-specific content:

- IOC shell snippets with recommended configurations
- Additional database templates or substitution files
- Small patches (for features not released upstream)

As a user, you don't need to worry about how modules are packaged—just install
them with conda and use them in your IOCs.

### Discovering available modules

Find all available e3 modules in the ESS channel:

:::{code-block} console
$ conda search "*" --channel ess-conda-local
:::

See which packages depend on a specific module:

:::{code-block} console
$ conda repoquery whoneeds require
:::

Search for modules by name pattern:

:::{code-block} console
$ conda search "*stream*"
:::

:::{tip}
To see what's installed in your current environment, use `conda list` as shown
in [Environments](environments.md#using-your-e3-environments).
:::

:::{seealso}
If you need to create or modify modules, see the developer documentation:

- [Building modules](../developer/building-modules.md) - Setting up build environments
- [Module build recipes](../developer/recipes.md) - Recipe structure and organization
- [Module build configurations](../developer/makefiles.md) - Creating e3 makefiles
- [Module creation](../developer/packaging-modules.md) - Complete workflow example

:::
