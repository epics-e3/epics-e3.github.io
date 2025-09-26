# `require`s build targets

This page provides a comprehensive reference for the make targets available when building EPICS modules in e3.
These targets are provided by the `require` build system.

## Getting help

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

- [Module build configurations](../developer/3-module-makefiles.md) - Setting up makefiles
- [`require`'s build interface](1-build-interface.md) - Available build variables
- [Building modules](../developer/1-conda-build.md) - Using conda-build

:::
