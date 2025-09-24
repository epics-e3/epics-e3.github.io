# `require`'s build interface

## What to build and install

* `SOURCES` - Source files to compile into the shared library
* `DBDS` - Database definition (`.dbd`) files to include in `$(module).dbd`
* `HEADERS` - Header files that should be installed with the module
* `TEMPLATES` - Database or template files that should be installed in the
  `$(module_DB)` path
* `TMPS` - Templates files to inflate to db-file and install in in the
  `$(module_DB)` path
* `SUBS` - Substitutions files to inflate the template file to db-file and
  install in the `$(module_DB)` path
* `SCRIPTS` - Script files that are installed in `$(module_DIR)`
* `BINS` - Executables that should be installed and be on `$(PATH)`

## What to link against

* `USR_LIBS` - EPICS support libraries to link against

## Other macros

* `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories

See also [Application Developer's Guide: Build Facility](https://docs.epics-controls.org/en/latest/build-system/specifications.html).
Note that especially `USR_*FLAGS` may be needed, depending on your build needs.
