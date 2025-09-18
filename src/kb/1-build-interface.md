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

## Module dependencies

* `REQUIRED` - Specifies any non source-based dependencies

## Other macros

* `KEEP_HEADER_SUBDIRS` - Preserves the tree structure of the given header
  directories
