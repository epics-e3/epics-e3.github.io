# Article: *require* targets

In this article, we will give a brief
description and overview of some of the targets that are available in e3.

To begin with, if you are in an e3 wrapper directory, you can see some of the
main targets available by typing `make help`

```console
[iocuser@host:e3-iocStats]$ make help
---------------------------------------
Available targets
---------------------------------------
install         Install module to $(E3_MODULES_INSTALL_LOCATION)
uninstall       Uninstall the current module
build           Build current module
debug           Displays information about the build process
clean           Deletes temporary build files
```

The targets fall into several categories.

## Main targets

These are the targets that are used in most cases when building, debugging,
testing, and deploying a module. They are related to the EPICS targets of the
same names, but with some differences.

* `make build`: This will build the module. This will compile all of the files
  specified in the variable `SOURCES` from the module makefile, as well as
  generate a number of necessary files for the installation process.
* `make install`: This will install the compiled and generated files into the
  target location described above. This will also perform any template and
  substitution file expansion.

A few variations on this are the following.

* `make clean`: Deletes all of the temporary files.
* `make all`: Initialises, patches, and then rebuilds the module.

## Additional targets

These are targets that are useful to help diagnose issues, debug, or display
information about the module.

* `make debug`: Runs through the build process, but instead displays data that
  is collected and used throughout the build process (e.g. exactly which files
  are compiled)

[^runiocsh]: In order to use this, you first need to have installed
  [run-iocsh](https://gitlab.esss.lu.se/ics-infrastructure/run-iocsh).
