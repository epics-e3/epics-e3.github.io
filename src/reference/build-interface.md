# `require`'s build interface

This page documents the build-time interface provided by `require` for building EPICS modules in e3.

## Build variables

- `MODULE` - Name of the module from the perspective of `require`
- `LIBVERSION` - Version of the module from the perspective of `require`

### What to build and install

- `SOURCES` - Source files to compile into the shared library
- `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
- `HEADERS` - Header files to install with the module
- `TEMPLATES` - Database or template files to install in the
  `$(module_DB)` path
- `SUBS` - Substitutions files to inflate to `.db`-files and install in the `$(module_DB)` path
- `TMPS` - Template files to inflate to `.db`-files and install in the `$(module_DB)` path
- `SCRIPTS` - Script files to install in `$(module_DIR)`
- `BINS` - Executables to install and place on `$(PATH)`

Files listed in `SUBS` or `TMPS` are processed automatically during the build using EPICS [msi](https://docs.epics-controls.org/projects/base/en/latest/msi.html)
(Macro Substitution and Include tool). The resulting `.db` files are installed in `$(module_DB)`.

### What to link against

- `USR_LIBS` - EPICS support libraries to link against

### Other macros

- `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories

For advanced usage (custom compiler flags, linker options, etc.), see EPICS base's
[Application Developer's Guide: Build Facility](https://docs.epics-controls.org/en/latest/build-system/specifications.html).
Variables like `USR_CPPFLAGS`, `USR_CXXFLAGS`, and `USR_LDFLAGS` may be needed depending on your build requirements.

## Build targets

The `require` build system provides several make targets:

:::{code-block} console
$ make help
---------------------------------------
Available targets
---------------------------------------
all             Build and install current module
install         Install module to $(E3_MODULES_INSTALL_LOCATION)
uninstall       Uninstall the current module
build           Build current module
debug           Displays information about the build process
clean           Deletes temporary build files
help            Show this help message
---------------------------------------
:::

:::{tip}
Additional targets may be available depending on your module configuration. Use `make help` to see all targets for
a specific module.
:::

:::{seealso}
**Related topics:**

- [Module build configurations](../developer/makefiles.md) - Setting up makefiles
- [Building modules](../developer/building-modules.md) - Using conda-build

:::
