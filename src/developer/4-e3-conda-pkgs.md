# Module creation

This tutorial demonstrates the complete end-to-end workflow for creating and
packaging an EPICS module for e3. We'll create a simple example module called
`exampleModule`, showing how all the pieces from previous chapters fit together.

## Overview

The tutorial covers:

1. **Creating an EPICS module** using `makeBaseApp` and/or `makeSupport`
2. **Setting up the recipe repository** to package the module
3. **Creating the build script** for conda-build integration
4. **Integrating with e3** using makefiles and recipes from previous chapters
5. **Testing the complete workflow**

:::{note}
This tutorial integrates concepts from:

- [Building modules](1-conda-build.md) - build environment and conda-build usage
- [Module build recipes](2-recipes.md) - recipe structure and meta.yaml details
- [Module build configurations](3-module-makefiles.md) - e3 makefile creation

For detailed EPICS module development guidance, refer to:

- [Creating an IOC Application](https://docs.epics-controls.org/en/latest/getting-started/creating-ioc.html)
- [EPICS Application Developer's Guide](https://docs.epics-controls.org/en/latest/AppDevGuide/index.html)

We recommend storing modules in the ESS GitLab
[epics-modules](https://gitlab.esss.lu.se/epics-modules) namespace and
submitting them to the
[EPICS modules database](https://epics-controls.org/resources-and-support/modules/)
for community awareness.
:::

:::{tip}
If you already have an existing EPICS module that you want to package, you can skip to
[Step 2: Package the module](#step-2-package-the-module).
:::

## Step 1: Create the EPICS module

We'll create a simple example module called `exampleModule` using EPICS base tools.

### 1.1 Set up the module directory

```console
$ mkdir exampleModule
$ cd exampleModule
$ git init
```

### 1.2 Create the application structure

Create the basic EPICS application structure, e.g. using `makeBaseApp`;

```console
$ makeBaseApp.pl -t example exampleModule
$ makeBaseApp.pl -i -t example exampleModule
```

This creates the standard EPICS application structure with `configure/`, `exampleModuleApp/`, and other directories.

::::{note}
`makeBaseApp` scaffolds an IOC application; installable module artifacts are provided via the e3 makefile in Step 4.
::::

### 1.3 Create device support (optional)

If your module needs device support, use `makeSupport`:

```console
$ makeSupport.pl -t devGpib exampleModule
```

This creates device support files in `exampleModuleSup/` directory, including:

- `devExampleModule.c` - Device support implementation
- `exampleModule.dbd` - Database definition file

### 1.4 Module structure overview

Your module now has a typical EPICS structure:

```console
$ tree -L 2
.
├── configure/
├── exampleModuleApp/
├── exampleModuleSup/     # If device support was created
├── db/
├── iocBoot/
└── Makefile
```

::::{note}
The actual implementation of device support, database files, and application
code is beyond the scope of this tutorial. Refer to the EPICS documentation
links provided earlier for detailed development guidance.
::::

## Step 2: Package the module

Now we'll create a separate repository for the conda recipe. This separation
allows for independent versioning, cleaner CI/CD, community contributions, and
site-specific customizations separate from upstream.

### 2.1 Create recipe repository structure

```console
$ mkdir exampleModule-recipe
$ cd exampleModule-recipe
$ mkdir -p recipe src
$ git init
```

For detailed information about recipe repository structure and organization
principles, see [Module build recipes](2-recipes.md).

### 2.2 Create the build script

Create a `build.sh` script for consistent building:

```bash
#!/bin/bash
LIBVERSION=${PKG_VERSION}

make clean
make MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION}
make MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION} install
```

Place this script in `recipe/build.sh` - conda-build will automatically execute it during the build process.

Make it executable:

```console
$ chmod +x build.sh
```

### 2.3 Create the e3 makefile

Create `src/Makefile` following the guidance in
[Module build configurations](3-module-makefiles.md). Start with the minimal
example and extend based on your module's needs.

### 2.4 Create the conda recipe

Tag the source repository:

```console
$ cd ../exampleModule
$ git tag v1.0.0
$ git push origin v1.0.0
```

Create `recipe/meta.yaml` with basic structure. For comprehensive details on
meta.yaml sections and options, see
[Module build recipes](2-recipes.md).

```yaml
{% set name = "exampleModule" %}
{% set version = "1.0.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  - url: https://gitlab.esss.lu.se/epics-modules/{{ name }}/-/archive/v{{ version }}/{{ name }}-v{{ version }}.tar.gz
    sha256: <checksum>
  - path: ../src

build:
  number: 0
  run_exports:
    - {{ pin_subpackage(name, max_pin='x.x.x') }}

requirements:
  build:
    - {{ compiler('cxx') }}
    - make
    - perl
  host:
    - epics-base
    - require

test:
  requires:
    - run-iocsh
  commands:
    - run-iocsh -r {{ name|lower }}

about:
  home: https://gitlab.esss.lu.se/epics-modules/exampleModule
  license: BSD-3-Clause
  license_file: LICENSE
  summary: "EPICS example module"
```

Add any needed site-specific files (IOC shell snippets, templates, patches) to
the `src/` directory as described in
[Module build recipes](2-recipes.md).

::::{tip}
Compute the checksum from the exact tarball URL you use:

```console
$ curl -L "https://gitlab.esss.lu.se/epics-modules/{{ name }}/-/archive/v{{ version }}/{{ name }}-v{{ version }}.tar.gz" | shasum -a 256
```

::::

::::{caution}
Always specify the correct license. This is crucial for legal compliance and
package distribution.
:::::

#### ESS recipe best practices

- Prefer `source: url` tarballs with a `sha256`; use tags for traceability. Add
  `path: ../src` only for site-specific overlays.
- Keep requirements minimal and in the correct layer:
   - build: compilers, `make`, `perl`
   - host: `epics-base`, `require`, and module-specific dependencies
- Avoid version pins inside the recipe; rely on global pinning files (see
  [Pinning and variants]).
- Use `run_exports` only when producing libraries consumed by others, and choose
  an appropriate pin width (`x.x`/`x.x.x`) based on ABI stability.
- Always include `license` and `license_file` under `about`.
- Do not hardcode system paths in `build.sh` or Makefiles; use `${PREFIX}`/
  `$(PREFIX)`.
- Don’t vendor other packages or ship static libraries.
- Increment `build: number` when changing the recipe without changing upstream
  version.
- Tests: keep `run-iocsh` and consider `test -f` checks for key installed files.

[Pinning and variants]: 1-conda-build.md#pinning-and-variants

### 2.6 Build and test

#### Local build

Create a clean build environment and run a local build:

```console
$ conda create -n conda-build conda-build conda-verify
$ conda activate conda-build
$ conda build recipe
```

Artifacts are written under your `conda-bld` folder. You can install the fresh
build for local testing using `--use-local` (see below).

#### Build with pinning files (recommended)

For consistent builds across ESS infrastructure, apply variant pinning as
described in [Pinning and variants](1-conda-build.md#pinning-and-variants).

#### Test build using Docker

For production-like testing, use the ESS conda-build Docker image:

```console
$ docker run --rm -v $(pwd):/workspace \
  registry.esss.lu.se/ics-docker/conda-build:latest \
  conda-build recipe
```

#### Test the package

```console
$ conda install --use-local examplemodule
$ run-iocsh -r examplemodule
```

You can also inspect installed files with `ls` or `tree` under your prefix.
Prefer declaring required files via your makefile/recipe rather than checking
them ad-hoc.

#### Debugging builds

If builds fail, open an interactive debug environment to investigate:

```console
$ conda debug recipe
```

This reproduces the build environment, allowing you to run build steps manually.

:::::{tip}
Recipe development is iterative: Creating conda recipes often involves trial
and error, especially when adapting existing modules. Don't expect the first
attempt to work perfectly - iterate based on build logs and error messages.
:::::

### 2.7 Repository structure and CI

Your final repository structure should look like:

```console
exampleModule-recipe/
├── LICENSE
├── README.md
├── recipe/
│   ├── meta.yaml
│   └── build.sh
└── src/
    ├── Makefile
    ├── iocsh/            # IOC shell snippets (if needed)
    ├── template/         # Database templates (if needed)
    └── patches/          # Source patches (if needed)
```

Only include directories and files that you actually use.

::::{note}
For ESS-hosted recipes, include the standard CI configuration to build and release packages:

```yaml
include:
  - project: 'ics-infrastructure/gitlab-ci-yml'
    file: 'E3CondaBuild.gitlab-ci.yml'
```

::::

## Summary

This tutorial showed the complete end-to-end workflow integrating concepts from previous chapters:

1. **EPICS module creation** using standard EPICS tools
2. **Recipe repository setup** with separation of concerns
3. **Build script creation** for conda-build integration
4. **e3 integration** using makefiles and recipes
5. **Package building and testing** with proper pinning

For production use, consider adding comprehensive tests and documentation.

---

:::{seealso}

- Back: [Module build configurations](3-module-makefiles.md)

:::
