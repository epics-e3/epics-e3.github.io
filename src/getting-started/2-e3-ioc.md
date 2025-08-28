# An e3 IOC

Two core ideas in e3 are:

1. dynamically loading libraries, and
2. wrapping community modules rather than forking them.

e3 has no IOC application build step. Each IOC runs `iocsh`, and startup scripts
use `require` to load libraries and set up data-file search paths.

You can then start an IOC by running:

```console
(e3) $ iocsh
```

:::{important}
Every IOC starts from `iocsh`. The `require` function brings the right libraries
and data files into the runtime without rebuilding.
:::

## Creating a startup script

:::{tip}
Prerequisites: activate an environment with EPICS base, require, and any modules
your script uses. The examples assume iocStats is installed.
:::

A minimal startup script:

```shell
# st.cmd
require iocstats  # or `require(iocstats)` if you prefer
```

:::{caution}
The last line of the file must end in a newline or that line will not be executed.
:::

:::{note}
`iocInit()` is called implicitly. You can skip this with `iocsh --no-init`. See
`iocsh --help` for more options.
:::

### A slightly more complete example

A more realistic startup script might look like:

```shell
# st.cmd
require device
require sequencer

epicsEnvSet("P", "Foo")
epicsEnvSet("R", "Bar")

iocshLoad("${device_DIR}init.iocsh", "PREFIX=$(P)-$(R):")
dbLoadRecords("${device_DIR}device.template", "PREFIX=$(P)-$(R):")

afterInit("seq device_control")
```

## Starting the IOC

```console
(e3) $ iocsh st.cmd
```

:::{note}
The require module produces a few PVs, for example to expose which modules are
loaded. To set the correct PV names, the environment variable `$IOCNAME` must be
set before starting your IOC.
:::

---

:::{seealso}

- Back: [Getting started with e3](1-getting-started.md)
- Next: [Environments](../user/1-environments.md)

:::
