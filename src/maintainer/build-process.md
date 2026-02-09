(require_build)=

# `require`'s build process

:::{note}
This document assumes a familiarity with GNU make. See
- [GNU Make manual](https://www.gnu.org/software/make/manual/) - comprehensive reference
- [Make tutorial](https://makefiletutorial.com/) - practical introduction
:::

The e3 build process is a complicated bit of work. Note that this is in addition
to the conda build process (see [Building modules](../developer/building-modules.md)); we will
assume that you are comfortable with that process and are interested in learning
about the internals of the e3-specific build process.

_In general_ the build scripts for e3 modules built with require will contain
something like (see [Build Targets](../reference/build-interface.md#build-targets)):

:::{code-block} bash
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION}
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION} install
:::

and, as stated in the section on [Module build configurations](../developer/makefiles.md),
the recipe's included `Makefile` must begin with

:::{code-block} makefile
include $(E3_REQUIRE_TOOLS)/driver.makefile
:::

Recall that this script and Makefile are located in the source directory after
all sources have been unpacked and patched.

1. In the source directory: Target architecture `${T_A}` has not been defined,
   so determine the architecture we are building.

   Note that while we only build a single architecture at a time, we need to
   determine `${T_A}` as understood by the EPICS build system.
2. In the source directory: Perform a collection of the relevant files and
   create the directories `O.${EPICSVERSION}_Common` and
   `O.${EPICSVERSION}_${T_A}`.
3. In the directories `O.*`: Build/Install all of the required shared libraries
   and other files for the given version of EPICS base and target architecture.

We will go over each of these steps in more detail, as well as go over an
example build to explain how information is collected and used by the build
process.

## The `make` process for e3

### Overview

We start in the source directory and run
:::{code-block} bash
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION} target
:::

:::{note}
Note that `MODULE` must be provided for many of the build targets, as this is
used to provide the build system with the location of the target build.
:::

Regardless of the target, the build process runs several successive passes in
order to collect all of the necessary information. These are:

1. Collect initial information and determine target architecture
2. Determine architecture-specific information (e.g. sources, configuration)
3. Perform the appropriate build/install/whatever task

### Stage 1: The source directory

On the first pass in the source directory we collect architecture-independent
information. This includes (most) source files, header files, scripts, and
snippets. We also determine which architectures to build for depending, of
course, on the module-specific configuration (e.g. `EXCLUDE_ARCHS`).

We also load all of the [configuration from EPICS base](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L162-L165):

:::{code-block} makefile
EB:=${EPICS_BASE}
-include ${CONFIG}/CONFIG
EPICS_BASE:=${EB}
:::

The redefinition of `EPICS_BASE` is due to the fact that it is overwritten in
`CONFIG_SITE` from EPICS base; see
[here](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/CONFIG#L15)
and [here](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/CONFIG_SITE#L144)

:::{note}
This does depend on your build configuration, and exists to guard against
installations that use `INSTALL_LOCATION` to relocate their EPICS installation.
:::

The sources and other files are handled roughly as [follows](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L197-L198):

:::{code-block} makefile
SRCS = ${SOURCES}
export SRCS
:::

which takes the variable `SOURCES` from the module build configuration and passes
it on to future rounds of the build process.

Note in particular the `export SRCS` line: when make is called recursively,
variables from one run to the next do not persist unless they are `export`ed. It
is also extremely important to note when the variable being exported is
expanded: this happens right before the next iteration of recursive `make` is
called, so even if `SOURCES` will only be defined later (as is the case with the
e3 build process), it will `export` correctly.

Once we have that sorted, we recursively call `make` and move onto the next
round. This next stage is triggered by [the following](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L272-L282):

:::{code-block} makefile
define target_rule
$1-%:
	$${MAKE} -f $${USERMAKEFILE} T_A=$$* $1
endef
$(foreach target,$(RECURSE_TARGETS),$(eval $(call target_rule,$(target))))

.SECONDEXPANSION:

$(foreach target,$(RECURSE_TARGETS),$(eval $(target): $$$$(foreach arch,$$$${BUILD_ARCHS},$(target)-$$$${arch})))
:::

We can simplify this by focusing purely on the build target (one of the
`RECURSE_TARGETS`); in that case this essentially reads

:::{code-block} makefile
build-%: | $(COMMON_DIR)
    ${MAKE} -f ${USERMAKEFILE} T_A=$* build

.SECONDEXPANSION:
build:: $$(foreach arch,$${BUILD_ARCHS},$(target)-$${arch})
:::

i.e. `build` depends on `build-T_A_1`, `build-T_A_2`, etc., each of which trigger
a call to run `make build` again with `T_A` set appropriately.[^secondexpansion]

### Stage 2: Preparing to build `T_A`

For this stage of the build process, we are still in the source directory; the
next stages will be done in the directories `O.$(EPICSVERSION)_Common` or
`O.$(EPICSVERSION)_$(T_A)`, respectively. These directories will also be created
at this point, and are the destination of all intermediate and final output
files (e.g. any generated `.db` or `.dbd` files, `.o` files, and
`lib$(module).so`)

:::{note}
Note that `make clean` simply deletes these directories, removing all generated
files.
:::

We make a final collection of what objects we should build, and
[a final gathering of information](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L295-L298):

:::{code-block} makefile
# Add sources for specific epics types or architectures.
ARCH_PARTS = ${T_A} $(subst -, ,${T_A}) ${OS_CLASS}
VAR_EXTENSIONS = ${EPICSVERSION} ${ARCH_PARTS} ${ARCH_PARTS:%=${EPICSVERSION}_%}
export VAR_EXTENSIONS
:::

allows the developer to have architecture-specific files: for example, if
`T_A = linux-x86_64` then `ARCH_PARTS` will be `linux-x86_64 linux x86_64`:
If we now consider the [next segment](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L301-L303), we see

:::{code-block} makefile
SRCS += $(foreach x, ${VAR_EXTENSIONS}, ${SOURCES_$x})
USR_LIBOBJS += ${LIBOBJS} $(foreach x,${VAR_EXTENSIONS},${LIBOBJS_$x})
export USR_LIBOBJS
:::

which tells us that we can have `SOURCES_x86_64` (or any other part of
`VAR_EXTENSIONS`) to selectively compile code based on architecture and
version.

Finally, [we run](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L326-L327)

:::{code-block} makefile
$(RECURSE_TARGETS): O.${EPICSVERSION}_${T_A}
	@${MAKE} -C O.${EPICSVERSION}_${T_A} -f ../${USERMAKEFILE} $@
:::

Note that due to the argument `-C O.${EPICSVERSION}_${T_A}` we switch to that
directory, using the same `${USERMAKEFILE}` to manage the build process.

### Stage 3: Building `T_A`

We have now collected the majority of the information that we need to build our
module. We will do a little more organisation and preparation, and then the
process will be handed over to the EPICS build system. Note that this part of
`driver.makefile` is by far the most complicated section, and takes some time to
digest.

One way of thinking of this is that the first two passes tell the build system
_what_ to build, while this pass tells it _how_ to build. Some specific details
follow; for examples see the next section.

1. We determine where all of the install paths will be [via](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L352-L360)

   :::{code-block} makefile
   INSTALL_REV     = ${MODULE_LOCATION}
   INSTALL_BIN     = ${INSTALL_PREFIX}/bin
   INSTALL_LIB     = ${INSTALL_PREFIX}/lib
   INSTALL_INCLUDE = ${INSTALL_PREFIX}/include
   INSTALL_DBD     = ${INSTALL_REV}/dbd
   INSTALL_DB      = ${INSTALL_REV}/db
   INSTALL_CONFIG  = ${INSTALL_REV}/cfg
   INSTALL_DOC     = ${INSTALL_REV}/doc
   INSTALL_SCR     = ${INSTALL_REV}
   :::

   :::{note}
   Note that unlike traditional EPICS build systems, we install binaries,
   libraries, and headers at the root level of the install location so that
   they are more readily found on `PATH`.
   :::

2. In this section we heavily use the `vpath` directive to help determine the
   source of the files that need to be compiled and/or installed

3. In order to manage dependencies chains within e3, we inject a custom source
   file into every module which runs the registration functions necessary for the
   module (`init.cpp`)

4. Additional include paths for header files are set here (more generally, this is
   where we set all the compilation and linking flags). [For example](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L400):

   :::{code-block} makefile
   SRC_INCLUDES = $(addprefix -I, $(wildcard $(foreach d,$(call uniq, $(filter-out /%,$(dir ${SRCS:%=../%} ${HDRS:%=../%}))), $d $(addprefix $d/, os/${OS_CLASS} $(POSIX_$(POSIX)) os/default))))
   :::

   This adds the path of every source and header file to the search path when
   compiling source files.

There are of course other details. In general this is one of the most complicated
parts of e3; it can be quite edifying and interesting to understand it but for the
most part it is not truly necessary to understand (until, of course, something
goes wrong!).

## Examples of the `make` process

We will provide a few examples of how `make` processes the data and produces the
desired result. The first is installing a header file, and the second is
actually compiling a source file.

### Installing a header file

Before we go on to the more complicated case of compiling source files, let us
go over the simpler step of having header files be installed so that other
modules may include them. As an example, there are many `.h` files that are
installed with *asyn* and are used by lots of other modules.

Header files are (this is only slightly a lie) installed by adding the line
`HEADERS += header.h` to your `Makefile`. This is then handled by the `install`
target in your makefile. This process then runs as follows.

1. In stage 1 we start with [the following](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L222-L225):

   :::{code-block} makefile
   HDRS = ${HEADERS}
   HDRS += $(RECORDS:%=${COMMON_DIR}/%.h)
   HDRS += ${HEADERS_${EPICSVERSION}}
   export HDRS
   :::

   which passes these on to the variable `HDRS` (as well as collecting a few
   other headers, including version-specific ones if necessary)

2. As noted above, there is one place in the build process that these are relevant:
   in stage 3 (within the directory `O.${EPICSVERSION}_{T_A}`) we have the
   following line:

   :::{code-block} makefile
   SRC_INCLUDES = $(addprefix -I, $(wildcard $(foreach d,$(call uniq, $(filter-out /%,$(dir ${SRCS:%=../%} ${HDRS:%=../%}))), $d $(addprefix $d/, os/${OS_CLASS} $(POSIX_$(POSIX)) os/default))))
   :::

   or, simplified:

   :::{code-block} makefile
   SRC_INCLUDES = $(addprefix -I, $(wildcard $(call uniq, $(filter-out /%,$(dir ${HDRS:%=../%})))))
   :::

   which adds the directory that the header files are located in to the search
   path for include files when compiling.

3. The next time the headers come up is during the install process, and are
   governed by the following:

   :::{code-block} makefile
   vpath %.h $(addprefix ../,$(sort $(dir $(filter-out /%,${HDRS}) ${SRCS}))) $(sort $(dir $(filter /%,${HDRS})))
   # snip
   INSTALL_HDRS = $(addprefix ${INSTALL_INCLUDE}/,$(notdir ${HDRS}))
   # snip
   INSTALLS += ... ${INSTALL_HDRS} ...

   install: ${INSTALLS}
   :::

   and the following from EPICS base [`RULES_BUILD`](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/RULES_BUILD#L547):

   :::{code-block} makefile
   $(INSTALL_INCLUDE)/%: %
        $(ECHO) "Installing generic include file $@"
        @$(INSTALL) -d -m $(INSTALL_PERMISSIONS) $< $(@D)
   :::

   which says that any target within the directory `$(INSTALL_INCLUDE)` has the
   target as a dependency, i.e. `$(INSTALL_INCLUDE)/header.h` depends on
   `header.h`

4. Finally, the `vpath` line above tells `make` where to search for that file,
   and then the instructions tell `make` to run the program defined by
   `$(INSTALL)` to install the file in the target location. Note however that
   there is one potential source of problems here: the dependency is just the
   filename alone, and so if you have the following two header files you would
   like to include: `dir1/header.h` `dir2/header.h` i.e. the same filename, but
   different locations, then only one of these two will be installed.

   In order to avoid this, you can add a path to the variable `KEEP_HEADER_SUBDIRS`,
   which will preserve the directory tree structure of headers under that path.

### Compiling a `.c` file

Building source files at its heart is similar to the above, but the chain of
dependencies is significantly more complicated. As above however, the inclusion
of a source file to be compiled into the shared library is simple: add the line
`SOURCES += $(APPSRC)/file.c` in your `Makefile`.

The next steps are complicated due to being shared among different configure
files.

1. Initially in stage 1 above, we have the line `SRCS = ${SOURCES}` which
   includes your file in the variable `SRCS`.

2. In the EPICS base configure file `CONFIG_COMMON`, we have
   [the following two directives](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/CONFIG_COMMON#L371):

   :::{code-block} makefile
   SRC_FILES = $(LIB_SRCS) $(LIBSRCS) $(SRCS) $(USR_SRCS) $(PROD_SRCS) $(TARGET_SRCS)
   HDEPENDS_FILES = $(addsuffix $(DEP),$(notdir $(basename $(SRC_FILES))))
   :::

   which converts `$(APPSRC)/file.c` into `file.d` in the variable
   `HDEPENDS_FILES`.

3. Next in stage 3, we include `RULES` from EPICS base which includes
   `RULES_BUILD`. This includes [the following](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/RULES_BUILD#L118):

   :::{code-block} makefile
   -include $(HDEPENDS_FILES)
   :::

   which seems quite innocuous, but it is a surprisingly important line: `make`,
   when trying to include a file, will first see if it exists, and if it does
   not, then it will see if it can generate that file. In this case, we have
   [the rule](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/RULES_BUILD#L239)

   :::{code-block} makefile
   %$(DEP):%.c
       @$(RM) $@
       $(HDEPENDS.c) $<
   :::

   which provides a rule to create `file.d` from `file.c`: this runs (once
   again, from [`CONFIG_COMMON`](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/CONFIG_COMMON#L359)):

   :::{code-block} makefile
   HDEPENDS_COMP.c   = $(COMPILE.c) $(HDEPENDS_COMPFLAGS) $(HDEPENDS_ARCHFLAGS)
   :::

   i.e. it compiles the source file with a special flag that produces not only
   `file.o`, but a dependency file `file.d`.

   To wit, on our first pass through in stage 3 we compile all of our source
   files to produce object files and dependency files.

4. We now need to connect the source files to the final shared library. The
   first step is the following from [`driver.makefile`](https://gitlab.esss.lu.se/epics-modules/require/-/blob/6.0.0/require-ess/tools/driver.makefile?ref_type=tags#L362-L372):

   :::{code-block} makefile
   LIBRARY_OBJS = $(strip ${LIBOBJS} $(foreach l,${USR_LIBOBJS},$(addprefix ../,$(filter-out /%,$l))$(filter /%,$l)))

   LIBOBJS += $(addsuffix $(OBJ),$(notdir $(basename $(filter-out %.$(OBJ) %$(LIB_SUFFIX),$(sort ${SRCS})))))
   :::

   which adds `file.o` to `LIBRARY_OBJS`.

5. Next, we look at `LOADABLE_SHRLIBNAME`: roughly speaking, if you end up with
   a non-empty `LIBRARY_OBJS` (as we have above), then this will be
   `lib${PRJ}.so`. In particular, we obtain from [`RULES_BUILD`](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/RULES_BUILD#L326)
   the dependency and build rules:

   :::{code-block} makefile
   $(LOADABLE_SHRLIBNAME): $(LIBRARY_OBJS) $(LIBRARY_RESS) $(SHRLIB_DEPLIBS)

   $(LOADABLE_SHRLIBNAME): $(LOADABLE_SHRLIB_PREFIX)%$(LOADABLE_SHRLIB_SUFFIX):
       @$(RM) $@
       $(LINK.shrlib)
       $(MT_DLL_COMMAND)
   :::

   where the linking command is provided in [`CONFIG.Common.UnixCommon`](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/os/CONFIG.Common.UnixCommon#L96):

   :::{code-block} makefile
   LINK.shrlib = $(CCC) -o $@ $(TARGET_LIB_LDFLAGS) $(SHRLIBDIR_LDFLAGS) $(LDFLAGS)
   LINK.shrlib += $(LIB_LDFLAGS) $(LIBRARY_LD_OBJS) $(LIBRARY_LD_RESS) $(SHRLIB_LDLIBS)
   :::

6. Last but not least, we need to connect this to the target `build`. In
   [`RULES_BUILD`](https://github.com/epics-base/epics-base/blob/R7.0.9/configure/RULES_BUILD#L146)
   we find:

   :::{code-block} makefile
   LIBTARGETS += $(LIBNAME) $(INSTALL_LIBS) $(TESTLIBNAME) \
       $(SHRLIBNAME) $(INSTALL_SHRLIBS) $(TESTSHRLIBNAME) \
       $(DLLSTUB_LIBNAME) $(INSTALL_DLLSTUB_LIBS) $(TESTDLLSTUB_LIBNAME) \
       $(LOADABLE_SHRLIBNAME) $(INSTALL_LOADABLE_SHRLIBS)

   # snip snip
   build: $(OBJSNAME) $(LIBTARGETS) $(PRODTARGETS) $(TESTPRODTARGETS) \
       $(TARGETS) $(TESTSCRIPTS) $(INSTALL_LIB_INSTALLS)
   :::

   and in particular, that `build` depends on `$(LOADABLE_SHRLIBNAME)`.

7. Putting this all together, we have the following chain of dependencies:

   :::{code-block} none
   build -> $(LOADABLE_SHRLIBNAME) -> $(LIBRARY_OBJS)
   :::

   where that last target includes `file.o`.

8. The magic now comes from the fact that we have already built this file back
   when we were creating `file.d`! As such, we can run the linking command, and
   we obtain our shared library, ready to install.

[^secondexpansion]: Why do we need the `.SECONDEXPANSION`? The issue at hand
is because the architecture filters are defined *after* the inclusion of
`driver.makefile`. As such, we take advantage of GNU make's ability to do
a deferred secondary expansion of target dependencies to ensure that we perform
the correct filtering on architectures.
