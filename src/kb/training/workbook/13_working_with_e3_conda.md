# 13. Working with conda and e3

## e3 module creation

e3 uses [*require*](https://gitlab.esss.lu.se/epics-modules/require), originally
developed by [PSI](https://github.com/paulscherrerinstitute/require) to
dynamically load modules at runtime. The *require* also includes a
[driver.Makefile](https://gitlab.esss.lu.se/epics-modules/require/-/blob/master/App/tools/driver.makefile)
that shall be used to build a module.  This requires a specific `{module_name}.Makefile`
file that includes this `driver.Makefile`.

To make it easy to create a new e3 module, we provide a cookiecutter template.

## Create the e3 module

Use the `e3-module` alias to create a new module (refer to [cookiecutter_configuration]
to create this alias).  You'll be prompted to enter some values
Press enter to keep the default.

```console
[iocuser@host:dev]$ e3-module
You've downloaded /home/iocuser/.cookiecutters/cookiecutter-e3-module before. Is it okay to delete and re-download it? [yes]: yes
company [European Spallation Source ERIC]:
module_name [mymodule]: foo
full_name [Your name]: John Doe
email [john.doe@ess.eu]:
documentation_page [https://confluence.esss.lu.se/display/IS/Integration+by+ICS]:
Select keep_epics_base_makefiles:
1 - N
2 - Y
Choose from 1, 2 [1]: 2
```

This will create a new module. You can reach the same behavior generating a
template using `makeBaseApp.pl` from EPICS base.

```console
[iocuser@host:dev]$ tree foo/
foo/
├── cmds
│   └── st.cmd
├── configure
│   ├── CONFIG
│   ├── CONFIG_SITE
│   ├── Makefile
│   ├── RELEASE
│   ├── RULES
│   ├── RULES_DIRS
│   ├── RULES.ioc
│   └── RULES_TOP
├── fooApp
│   ├── Db
│   │   └── Makefile
│   ├── Makefile
│   └── src
│       ├── fooMain.cpp
│       └── Makefile
├── foo.Makefile
├── iocsh
│   └── foo.iocsh
├── LICENSE
├── Makefile
├── README.md
└── RELEASE.md
```

Notice the `foo.Makefile` file, this is the main file used to
build and install a conda e3 module.  The standard `Makefile`
allows you to compile the module using the default EPICS build
system if you want. It's important to emphasize that `foo.Makefile`
should not be committed. To prevent commits of this file, it is
recommended to add it to the `.gitignore file`.

## Update the module

Include the necessary files in your module and ensure that you update
the `foo.Makefile` file in accordance with the new changes or updates made
to your module.

## Compile the module

To compile an e3 module in a conda environment, the following packages are
required:

* `make`
* `compilers`
* `tclx`
* `epics-base`
* `require`

Create the `e3-dev` environment with those packages.  If you have other
dependencies, like `asyn`, install them as well.

```console
[iocuser@host:dev]$ conda create -y -n e3-dev epics-base require compilers make tclx
Collecting package metadata (repodata.json): done
Solving environment: done
# --- snip snip ---
```

Activate the `e3-dev` environment and compile your module.
Note that when using the make command, it is essential to specify the MODULE name.
Additionally, you have the option to specify the version; if omitted, the require
command will automatically generate the version as `dev`.

```console
[iocuser@host:dev]$ conda activate e3-dev
(e3-dev) [iocuser@host:dev]$ cd foo
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo
MAKING EPICS VERSION 7.0.7
mkdir -p O.7.0.7_Common
make -f foo.Makefile T_A=linux-x86_64 build
make[1]: Entering directory '/home/iocuser/dev/foo'
mkdir -p O.7.0.7_linux-x86_64
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET           -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall              -mtune=generic              -m64  -fPIC          -I. -I../fooApp/src/ -I/home/iocsuser/miniconda/envs/e3-dev/modules/require/5.0.0/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/os/Linux              -I/home/iocsuser/miniconda/envs/e3-dev/include           -c  ../fooApp/src/fooMain.cpp
echo "char _fooLibRelease[] = \"dev\";" >> foo_version_dev.c
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-gcc  -D_GNU_SOURCE -D_DEFAULT_SOURCE        -DUSE_TYPED_RSET           -D_X86_64_ -DUNIX  -Dlinux             -MD   -O3 -g   -Wall -Werror-implicit-function-declaration              -mtune=generic     -m64  -fPIC           -I. -I../fooApp/src/ -I/home/iocsuser/miniconda/envs/e3-dev/modules/require/5.0.0/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/compiler/gcc -I/home/iocsuser/miniconda/envs/e3-dev/epics/include/os/Linux              -I/home/iocsuser/miniconda/envs/e3-dev/include           -c foo_version_dev.c
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocsuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocsuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
/home/iocsuser/miniconda/envs/e3-dev/bin/x86_64-conda_cos6-linux-gnu-g++ -o libfoo.so  -shared -fPIC -Wl,-hlibfoo.so -L/home/iocsuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64 -Wl,-rpath,/home/iocsuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64                  -rdynamic -m64 -Wl,--disable-new-dtags -Wl,-rpath,/home/iocsuser/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/iocsuser/miniconda/envs/e3-dev/lib -L/home/iocsuser/miniconda/envs/e3-dev/lib -Wl,-rpath-link,/home/iocsuser/miniconda/envs/e3-dev/epics/lib/linux-x86_64                   fooMain.o foo_version_dev.o      -lpthread    -lm -lrt -ldl -lgcc
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[1]: Leaving directory '/home/iocuser/dev/foo'
```

If you have some database to generate, run `make -f foo.Makefile MODULE=foo db_internal`.
In our case, we don't have any template, so the command won't do anything.

```console
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo db_internal
make: Nothing to be done for 'db_internal'.
```

Install the module in the current environment.

```console
(e3-dev) [iocuser@host: foo]$ make -f foo.Makefile MODULE=foo install
MAKING EPICS VERSION 7.0.7
make -f foo.Makefile T_A=linux-x86_64 install
make[1]: Entering directory '/home/iocuser/dev/foo'
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[2]: Entering directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
Collecting dependencies
rm -f foo.dep.tmp
cat *.d 2>/dev/null | sed 's/ /\n/g' | sed -n 's%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([0-9]*\.[0-9]*\.[0-9]*\)/.*%\1 \2%p;s%/home/iocuser/miniconda/envs/e3-dev/modules/*\([^/]*\)/\([^/]*\)/.*%\1 \2%p'| grep -v "include" | sort -u > foo.dep.tmp
cat foo.dep.tmp | sort -u >> foo.dep
Installing scripts ../iocsh/foo.iocsh to /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 ../iocsh/foo.iocsh /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
Installing module library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m755 libfoo.so /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib
mkdir /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
Installing module dependency file /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/foo.dep
perl -CSD /home/iocuser/miniconda/envs/e3-dev/epics/bin/linux-x86_64/installEpics.pl  -d -m644 foo.dep /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64
make[2]: Leaving directory '/home/iocuser/dev/foo/O.7.0.7_linux-x86_64'
make[1]: Leaving directory '/home/iocuser/dev/foo'
```

The module was installed as _dev_ version.  You can check that you can load it:

```console
(e3-dev) [iocuser@host:foo]$ iocsh -r foo
# --- snip snip ---
require foo
Module foo version dev found in /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
# --- snip snip ---
```

You can also use the `cmds/st.cmd` file to test your module.

```console
(e3-dev) [iocuser@host:foo]$ iocsh.bash cmds/st.cmd
# --- snip snip ---
iocshLoad 'cmds/st.cmd',''
# This should be a test startup script
require foo
Module foo version dev found in /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/
Loading library /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev/lib/linux-x86_64/libfoo.so
Loaded foo version dev
foo has no dbd file
Loading module info records for foo
iocshLoad("/home/iocuser/miniconda/envs/e3-dev/modules/foo/dev//foo.iocsh")
# --- snip snip ---
```

You can uninstall the module by running `make -f foo.Makefile uninstall`.

```console
(e3-dev) [iocuser@host:foo]$ make -f foo.Makefile MODULE=foo uninstall
rm -rf /home/iocuser/miniconda/envs/e3-dev/modules/foo/dev
```

During development, you can modify your code, re-compile and re-install as many
times as you want:

```console
make -f foo.Makefile MODULE=foo uninstall
make -f foo.Makefile MODULE=foo
make -f foo.Makefile MODULE=foo db_internal
make -f foo.Makefile MODULE=foo install
```

## e3 recipe creation

To package a module with conda, you have to create a conda recipe.

Use the `e3-recipe` alias to create a new recipe (refer to
[cookiecutter_configuration] to create this alias).  You'll be prompted to
enter some values. Press enter to keep the default.

:::note
You can use your own module, as created above or earlier if you have uploaded
it to your own repository. Here we use `fakemodule` as a working example.
:::

```console
[iocuser@host:dev]$ e3-recipe
company [European Spallation Source ERIC]:
module_name [mymodule]: fakemodule
summary [EPICS fakemodule module]:
module_home [https://gitlab.esss.lu.se/epics-modules]:
module_version [1.0.0]:
```

The `module_home` variable shall point to the group in GitLab where your module
is stored.

This will create the following project:

```console
[iocuser@host:dev]$ tree fakemodule-recipe/
fakemodule-recipe/
├── LICENSE
├── README.md
├── recipe
│   ├── build.sh
│   └── meta.yaml
└── src
    └── fakemodule.Makefile
```

## Update the recipe

Typically, you should only need to update the `recipe/meta.yaml` and the
`fakemodule.Makefile` files.

### meta.yaml

The `meta.yaml` file is the file that defines the recipe.  It describes where to
get the source of the module and the dependencies to build and run the modules.
The file contains many hints in comments. Follow them and remove them when
you've finalized your recipe.

```{note}
The final recipe shouldn't contain any comments!
```

### module.Makefile

The `module.Makefile` should have the same content of the epics-module
`module.Makefile` that you used before in the build/install development stage.

## Build the recipe

To build the recipe, run:

```console
[iocuser@host:foo-recipe]$ conda build recipe
```

In case of failure, check the error message and update your `meta.yaml` file.

If the build was successful, you should see something like that:

````bash
# --- snip snip ---
TEST END: /home/iocuser/miniconda/conda-bld/linux-64/foo-1.0.0-hbd7620e_0.tar.bz2
Renaming work directory,  /home/iocuser/miniconda/conda-bld/foo_1591215967088/work  to  /home/iocuser/miniconda/conda-bld/foo_1591215967088/work_moved_foo-1.0.0-hbd7620e_0_linux-64_main_build_loop
# Automatic uploading is disabled
# If you want to upload package(s) to anaconda.org later, type:

anaconda upload /home/iocuser/miniconda/conda-bld/linux-64/foo-1.0.0-hbd7620e_0.tar.bz2

# To have conda build upload to anaconda.org automatically, use
# $ conda config --set anaconda_upload yes

anaconda_upload is not set.  Not uploading wheels: []
####################################################################################
Resource usage summary:

Total time: 0:00:07.2
CPU usage: sys=0:00:00.0, user=0:00:00.0
Maximum memory usage observed: 2.4M
Total disk usage observed (not including envs): 52B


####################################################################################
````

## Test the built package

You can install the package you built locally by using the `-c local` argument
(to use the local channel).

```console
[iocuser@host:foo-recipe]$ conda create -y -n test -c local foo
# --- snip snip ---
The following NEW packages will be INSTALLED:

  foo                home/iocuser/miniconda/conda-bld/linux-64::foo-1.0.0-hbd7620e_0
# --- snip snip ---
```

Activate your test environment and test your package.
