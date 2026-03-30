(module_load)=

# `require`'s module load

The `require` module is essentially a library loader that loads EPICS modules on
the running IOC. This article will describe `require`'s kernel implementation:
self registering, module loading and module registry.

:::{seealso}
**Related topics:**

- [`require`'s build process](../build-process.md)
:::

## Self registration

The [`init.cpp`](https://gitlab.esss.lu.se/epics-modules/require/-/blob/83f71357ea7e5899445101deaa85f0fbd9f2df09/require-ess/src/init.cpp)
is the most important file in require. It implements the self registration
mechanism that allows `require` to offload dependency loading to the system
loader. It has a single function, `__module_library_init()`,
that at first will load the `<module_name>.dbd` from the libraries directory.
Then the module registers the record device driver by calling `Registration()`.
It registers itself to `require` via `register_module()`, that sets up `require`'s
own PVs and environment variables about the loaded module. Finally the following
environment variables are updated calling `setup_db_path()`: `module_DB`,
`TEMPLATES` and `EPICS_DB_INCLUDE_PATH`.

This file is embedded into every module build for e3 by `driver.Makefile`. Just
after creating the `<module_name>_registerRecordDeviceDriver`, the inclusion of
`init.cpp` replaces a direct call to `Registration()`. This is unfortunately
necessary to avoid initialization order issues.

:::{code-block} makefile
# Create file to fill registry from dbd file. Because of c++ static
# initialization order fiasco all static initialization needs to be
# in a single function. Therefore the last line of
# module_registerRecordDeviceDriver.cpp, that would run Registration()
# for initialization, is removed. Then init.cpp is appended and
# __module_library_init() is initializes the library and calls
# Registration().
${REGISTRYFILE}: ${MODULEDBD}
	$(PERL) $(EPICS_BASE_HOST_BIN)/registerRecordDeviceDriver.pl $< ${PRJ_SYMBOL}_registerRecordDeviceDriver | grep -v 'iocshRegisterCommon();' > $@
	sed -i'.bak' -E '/^.*= Registration\(\)\;$$/d' $@
	echo "#include <init.cpp>" >> $@
:::

:::{note}
See [C++ Static Initialization Order Fiasco](https://en.cppreference.com/w/cpp/language/siof.html) for background on the workaround above.
:::

## Module loading

The modules built with e3 must declare all other modules they depend on as linked libraries,
[see documentation](https://docs.epics-controls.org/en/latest/build-system/specifications.html#specifying-dependant-libraries-to-be-linked-when-creating-a-library).
The module `calc` depends on `sscan` and `sequencer`, which is defined in its Makefile: 
`USR_LIBS += sscan sequencer`. When `require calc` is called, `require` will try to load `calc` using `dlopen`, and
that will automatically load the library dependencies, starting with `sscan` and `sequencer`.

:::{note}
As we use `conda` for package dependency and version handling, `require` does not have to care about these.
:::

The loading is done by `require_priv`, which also validates that the library is a `require`-compatible EPICS module:

:::{code-block} C
static int require_priv(const char *module) {
  void *lib_handle = NULL;
  char lib[PATH_MAX] = {0};
  void *symbol_address = NULL;
  char *dlsym_error = NULL;

  debug("Trying to load module=\"%s\".\n", module);
  debug("Load the library if file exists.\n");
  snprintf(lib, PATH_MAX, PREFIX "%s" EXT, module);
  lib_handle = dlopen(lib, RTLD_NOW | RTLD_GLOBAL);
  if (lib_handle == NULL) {
    errlogPrintf("Error loading module: %s.\n", module);
    dlsym_error = dlerror();
    if (dlsym_error != NULL)
      errlogPrintf("%s\n", dlsym_error);
    return -1;
  }
  symbol_address = dlsym(lib_handle, E3_SYMBOL);
  dlsym_error = dlerror();
  if (dlsym_error != NULL || symbol_address == NULL) {
    dlclose(lib_handle);
    errlogPrintf(PREFIX "%s" EXT " is not an EPICS module.\n", module);
    if (dlsym_error != NULL)
      errlogPrintf("%s\n", dlsym_error);
    return -1;
  }
  return 0;
}
:::

:::{note}
Notice that `require` will check for the `__module_lib_version` symbol to check
if the library is an e3 compatible EPICS module.
:::

## Module registry

`require` holds a linked list with information of every module loaded. The module
structure holds modules name, version, and path. This list of loaded modules and
their versions is also what later is exposed in PV form (See [The `require` function](../reference/require.md)).
