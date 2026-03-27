
# `require's` module load

The `require` module is essentially a library loader that loads EPICS modules on
the running IOC. This article will describe `require's` internals for version
6.0.0. Previous versions of `require` have many differences from the current
approach.

## Self registration

The most important bit to understand `require` is
[`init.cpp`](https://gitlab.esss.lu.se/epics-modules/require/-/blob/83f71357ea7e5899445101deaa85f0fbd9f2df09/require-ess/src/init.cpp)
self registration code. It holds a single function, `__module_library_init()`,
that at first will load the `<module_name>.dbd` from the libraries directory.
Then the module registers the record device driver by calling `Registration()`
and register itself to `require` via `register_module()` - this sets up `require's`
own PVs with information about the loaded module. Finally the template environment
variables are updated - `module_DB`, `TEMPLATES` and `EPICS_DB_INCLUDE_PATH`.

This file is embedded into every module build for e3 by `driver.Makefile`. Just
after creating the `module_registerRecordDeviceDriver`, the inclusion of
`init.cpp` replaces a direct call to `Registration()`. This unfortunately
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

:::{seealso}
[`require's` build process](../build-process.md)
:::

## Dependency handling

The modules built with e3 must specify as dependent library all other modules
it depends, [see documentation] (https://docs.epics-controls.org/en/latest/build-system/specifications.html#specifying-dependant-libraries-to-be-linked-when-creating-a-library).
When `require foo` is called `require` will load `foo` using `dlopen` but
and that will automatically load all dependent modules. For example, `calc`
Makefile will have `USR_LIBS += sscan sequencer`.

:::{note}
Package dependency and version handling are done by conda.
:::

Once `require` loads the first required module the system loader will take
care of the dependency chain. The `require_priv` function will load the
required module:

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
if the library is a e3 compatible EPICS module.
:::

## Module registry

`require` holds a linked list with information of every module loaded. The module
structure holds modules name, version, and path. The list of loaded modules and
their versions are then exported in PV form.
