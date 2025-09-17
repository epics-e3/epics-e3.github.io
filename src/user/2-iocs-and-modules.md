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

As mentioned in [An e3 IOC](../getting-started/2-e3-ioc.md), an e3 IOC is started
using the `iocsh` script and dynamically loads any additional modules using the `require`
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

### Module wrappers

A key design concept in e3 is the notion of a module wrapper. This is used in
order to package community modules with site-specific modifications on top. This
allows us to avoid forking (and diverging) source code, while still allowing for
the customisations we want.

This is done by placing source code patches (for changes that the upstream source
may not want, or is slow to accept) as well as site-specific data files in our
internal package.  At ESS, we do this in the conda recipe (git) projects.

The wrappers---henceforth, *recipes*---are also where we store the build configuration
needed for the module to work together with require.

The file structure of a recipe project will typically look like this:

```console
$ tree
.
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    ├── cmds                    # example, template, or test startup scripts
    │   └── example.cmd
    ├── iocsh                   # snippets
    │   └── config.iocsh
    ├── Makefile                # the build configuration
    └── template                # template, substitution, and database files
        ├── ess.substitutions
        └── some.template
```

---

:::{seealso}

- Back: [Environments](1-environments.md)
- Next: [Building modules](../developer/1-conda-build.md)

:::
