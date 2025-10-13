# `require`'s build interface

This page documents the build-time interface provided by `require` for building EPICS modules in e3.

## Build variables

### What to build and install

- `SOURCES` - Source files to compile into the shared library
- `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
- `HEADERS` - Header files that should be installed with the module
- `TEMPLATES` - Database or template files that should be installed in the
  `$(module_DB)` path
- `TMPS` - Templates files to inflate to db-file and install in in the
  `$(module_DB)` path
- `SUBS` - Substitutions files to inflate the template file to db-file and
  install in the `$(module_DB)` path
- `SCRIPTS` - Script files that are installed in `$(module_DIR)`
- `BINS` - Executables that should be installed and be on `$(PATH)`

### What to link against

- `USR_LIBS` - EPICS support libraries to link against

### Other macros

- `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories

See also [Application Developer's Guide: Build Facility](https://docs.epics-controls.org/en/latest/build-system/specifications.html).
Note that especially `USR_*FLAGS` may be needed, depending on your build needs.

## Build targets

This section provides a comprehensive reference for the make targets available when building EPICS modules in e3.
These targets are provided by the `require` build system.

### Getting help

From any module source directory, you can see the available targets:

```console
$ make help
---------------------------------------
Available targets
---------------------------------------
install         Install module to $(E3_MODULES_INSTALL_LOCATION)
uninstall       Uninstall the current module
build           Build current module
debug           Displays information about the build process
clean           Deletes temporary build files
```

:::{tip}
Additional targets may be available depending on your module configuration. Use `make help` to see all targets for
a specific module.
:::

:::{seealso}
**Related topics:**

- [Module build configurations](../3-developer/3-module-makefiles.md) - Setting up makefiles
- [Building modules](../3-developer/1-conda-build.md) - Using conda-build

:::
