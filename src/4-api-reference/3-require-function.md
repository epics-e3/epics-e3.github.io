# The `require` function

The `require` function is used in IOC startup scripts to dynamically load EPICS modules
and make their libraries, database definitions, and data files available to the IOC.

## Syntax

```shell
require(module)
require module
```

Both forms are equivalent. The parentheses are optional.

## Arguments

- `module` - Name of the module to load (case-sensitive; module names are lowercase)

## Behavior

When `require` is called, it:

1. Loads the module's shared library (`.so` file)
2. Loads the module's database definition file (`.dbd`)
3. Sets up environment variables pointing to the module's data files (`<module>_DIR`, `<module>_DB`)
4. Creates module information PVs

## Examples

After requiring a module, you can access its data files through environment variables:

```shell
require iocstats

# Load a database from the iocstats module
dbLoadRecords("${iocstats_DB}/iocAdminSoft.db", "IOC=$(IOCNAME)")
```

## Module information PVs

`require` creates PVs that expose information about loaded modules, e.g. `$(IOCNAME):LoadedModules`.

:::{tip}
Set the IOC name using the `--iocname` flag:

```console
$ iocsh --iocname MY-IOC-01 st.cmd
```

If not specified, an auto-generated name is used.
:::

:::{seealso}
**Related topics:**

- [An e3 IOC](../1-getting-started/2-e3-ioc.md) - Creating startup scripts
- [IOCs and modules](../2-user/2-iocs-and-modules.md) - Module concepts
- [`iocsh` executable](2-iocsh.md) - Command-line interface

:::
