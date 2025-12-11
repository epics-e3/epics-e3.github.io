# The `require` function

The `require` function is used in IOC startup scripts to dynamically load EPICS modules
and make their libraries, database definitions, and data files available to the IOC.

## Syntax

:::{code-block} shell
require module
:::

## Behavior

When `require` is called, it:

1. Loads the module's shared library (`.so` file)
2. Loads the module's database definition file (`.dbd`)
3. Sets up environment variables pointing to the module's data files (`${<module>_DIR}`, `${<module>_DB}`)

## Examples

You can access a module's data files through its environment variables:

:::{code-block} shell
require iocstats

# Load a database from the iocstats module
dbLoadRecords("${iocstats_DB}/iocAdminSoft.db", "IOC=$(IOCNAME)")
:::

## Environment information PVs

`require` creates debugging PVs that expose information about loaded modules and components:

- `$(IOCNAME):Require-Version` - require version
- `$(IOCNAME):Require-RtComponents` - runtime components (Q-group)
- `$(IOCNAME):Require-LoadedModules` - loaded modules (Q-group)

::::{tip}
Set the IOC name using the `--iocname` flag:

:::{code-block} console
$ iocsh --iocname MY-IOC-01 st.cmd
:::

If not specified, an auto-generated name is used.
::::

:::{seealso}
**Related topics:**

- [An e3 IOC](../getting-started/your-first-ioc.md) - Creating startup scripts
- [IOCs and modules](../user/iocs-and-modules.md) - Module concepts
- [`iocsh` executable](iocsh.md) - Command-line interface

:::
