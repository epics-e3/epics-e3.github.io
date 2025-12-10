# Module creation

This tutorial demonstrates the complete end-to-end workflow for creating and
packaging an EPICS module for e3. We'll create a simple example module called
`exampleModule`, showing how all the pieces from previous chapters fit together.

## Overview

The tutorial covers:

1. **Creating an EPICS module** using `makeBaseApp` and `makeSupport`
2. **Setting up the recipe repository** to package the module
3. **Creating the build script** for conda-build integration
4. **Integrating with e3** using makefiles and recipes from previous chapters
5. **Testing the complete workflow**

:::{note}
This tutorial integrates concepts from:

- [Building modules](building-modules.md) - build environment and conda-build usage
- [Module build recipes](recipes.md) - recipe structure and meta.yaml details
- [Module build configurations](makefiles.md) - e3 makefile creation

For detailed EPICS module development guidance, refer to:

- [Creating an IOC application](https://docs.epics-controls.org/en/latest/getting-started/creating-ioc.html)
- [EPICS application developer's guide](https://docs.epics-controls.org/en/latest/AppDevGuide/index.html)

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

:::{code-block} console
$ mkdir exampleModule
$ cd exampleModule
$ git init
:::

### 1.2 Create the application structure

Create the basic EPICS application structure using `makeBaseApp`:

:::{code-block} console
$ makeBaseApp.pl -t example exampleModule
$ makeBaseApp.pl -i -t example exampleModule
:::

This creates the standard EPICS application structure with `configure/`, `exampleModuleApp/`, `iocBoot/`, and more.

:::{note}
The EPICS base utility `makeBaseApp` scaffolds an IOC application; installable module artifacts are provided
via the e3 makefile in [2.3 Create the e3 makefile](#23-create-the-e3-makefile).
:::

### 1.3 Create device support (optional)

If your module needs device support, use `makeSupport`:

:::{code-block} console
$ makeSupport.pl -t devGpib exampleModule
:::

This creates device support files in `exampleModuleSup/` directory, including:

- `devExampleModule.c` - Device support implementation
- `exampleModule.dbd` - Database definition file

### 1.4 Module structure overview

Your module now has a typical EPICS structure:

:::{code-block} console
$ tree -L 2
.
├── configure/
├── exampleModuleApp/
├── exampleModuleSup/     # If device support was created
├── db/
├── iocBoot/
└── Makefile
:::

:::{note}
The actual implementation of device support, database files, and application
code is beyond the scope of this tutorial. Refer to the EPICS documentation
links provided earlier for detailed development guidance.
:::

After your code has been reviewed and merged into the default branch, tag the release with a version number.
Your first published release should typically be `1.0.0`.

:::{tip}
We encourage use of [semantic versioning](https://semver.org/).
:::

## Step 2: Package the module

Now we'll create a separate repository for the conda recipe. This separation
allows for independent versioning, cleaner CI/CD, community contributions, and
site-specific customizations separate from upstream.

### 2.1 Create recipe repository structure

:::{code-block} console
$ mkdir exampleModule-recipe
$ cd exampleModule-recipe
$ mkdir -p recipe src
$ git init
:::

For detailed information about recipe repository structure and organization
principles, see [Module build recipes](recipes.md).

### 2.2 Create the build script

Create `recipe/build.sh` - this is the standard build script for all e3 modules:

:::{code-block} bash
:class: no-copybutton

#!/bin/bash
make clean
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION}
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION} install
:::

conda-build will automatically execute this script during the build process.

:::{tip}
You can use the [cookiecutter-e3-recipe](https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe)
template to scaffold a recipe repository with the standard structure and files.
:::

Make it executable:

:::{code-block} console
$ chmod +x recipe/build.sh
:::

### 2.3 Create the e3 makefile

Create `src/Makefile` following the guidance in
[Module build configurations](makefiles.md). Start with the minimal
example and extend based on your module's needs.

### 2.4 Create the conda recipe

Create `recipe/meta.yaml` with a minimal structure.

For background and all available fields, see conda-build’s documentation: [Defining metadata (meta.yaml)](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html).

:::{code-block} yaml
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
    - {{ compiler('c') }}    # If you are using .c sources
    - {{ stdlib('c') }}
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
:::

:::{tip}
Use jinja2 filters when upstream version format differs from the URL or tag format. This can be useful when upstream
uses a different version format like `R1-2` or `v1-2-3-4`. For example:

:::{code-block} yaml
{% set version = "1.2" %}

source:
  url: .../-/archive/R{{ version | replace('.', '-') }}/...tar.gz
:::

:::

:::{note}
**Advanced testing:**

The `test:` section can also include integration tests (pytest with run-iocsh/p4p) or C/C++ unit tests.
Simulated devices (e.g., using [lewis](https://github.com/ISISComputingGroup/lewis)) can be used for testing hardware behavior.

For an example with pytest integration tests, see [displayform-recipe](https://gitlab.esss.lu.se/e3/recipes/displayform-recipe).

See also: [pytest](https://docs.pytest.org/), [run-iocsh](https://e3.pages.ess.eu/run-iocsh/), [p4p](https://mdavidsaver.github.io/p4p/)
:::

Add any needed site-specific files (IOC shell snippets, templates, patches) to
the `src/` directory as described in
[Module build recipes](recipes.md).

:::{tip}
Compute the checksum from the exact tarball URL you use:

:::{code-block} console
$ curl -L "https://gitlab.esss.lu.se/epics-modules/{{ name }}/-/archive/v{{ version }}/{{ name }}-v{{ version }}.tar.gz" | shasum -a 256
:::

:::

:::{important}
Always specify the correct license. This is crucial for legal compliance and package distribution.
:::

#### ESS recipe best practices

- Prefer `source: url` tarballs with a `sha256`; use tags for traceability.
- Bind `version` to upstream version, using jinja2 filters for separator conversion
- Version considerations:
  - Avoid pre-release versions (rc, dev, alpha, beta) in production environments
  - Be aware that conda treats `1.1rc1` > `1.0.0` (may be prioritized unexpectedly)
  - Prefer `>=1.0.0` versions for production deployments when possible
- Keep requirements minimal and in the correct layer:
   - build: compilers, `make`, `perl`
   - host: `epics-base`, `require`, and module-specific dependencies
- Avoid version pins inside the recipe; rely on global pinning files where e3-pinning overrides conda-forge
  (see [Pinning and variants]).
- Use `run_exports` only when producing libraries consumed by others to ensure ABI stability.
- Always include `license` and `license_file` under `about`.
- Do **not** hardcode system paths in `build.sh` or Makefiles; use `$(PREFIX)`.
- Don’t bundle vendor libraries with your package - create separate conda packages for these.
- Increment build number when changing the recipe without changing upstream version.
- Tests: Prefer `run-iocsh -r <module>` over `test -f *.so`; it dynamically loads the library.
  Add `test -f` checks for other key installed files as needed.

[Pinning and variants]: building-modules.md#pinning-and-variants

#### Contributing to conda-forge

If you're packaging libraries, SDKs, or tools that could benefit users beyond the EPICS community, consider
contributing them to [conda-forge](https://conda-forge.org/) rather than keeping them in organization-specific channels.

:::{tip}
Good candidates for conda-forge contributions include:

- Vendor SDKs and hardware drivers with broad applicability
- General-purpose scientific libraries
- Development tools and utilities

EPICS modules themselves stay in e3-specific channels due to their specialized nature.
:::

See conda-forge's [Contributing packages](https://conda-forge.org/docs/maintainer/adding_pkgs/) guide for
details on the submission process.

### 2.5 Build and test

#### Local build

Create a clean build environment and run a local build:

:::{code-block} console
$ conda create -n conda-build conda-build conda-verify
$ conda activate conda-build
$ conda build recipe
:::

::::{tip}
If a freshly published dependency is not being resolved during `conda build`, clear the local index cache and retry:

:::{code-block} console
$ conda clean --index-cache
:::
::::

Artifacts are written to your `conda-bld` folder. You can install the fresh
build for local testing using `--use-local` (see below).

#### Build with pinning files (recommended)

For consistent builds across ESS infrastructure, apply variant pinning as
described in [Pinning and variants](building-modules.md#pinning-and-variants).

#### Test build using Docker

For production-like testing, use the ESS conda-build Docker image:

:::{code-block} console
$ docker run --rm -v $(pwd):/workspace \
  registry.esss.lu.se/ics-docker/conda-build:latest \
  conda-build /workspace/recipe
:::

#### Test the package

:::{code-block} console
$ conda install --use-local examplemodule
$ iocsh -r examplemodule
:::

:::{tip}
You can also inspect installed files with `ls` or `tree` under your prefix.
Prefer declaring required files via your recipe rather than checking them ad-hoc.
:::

#### Debugging builds

If builds fail, open an interactive debug environment to investigate:

:::{code-block} console
$ conda debug recipe
:::

This reproduces the build environment, allowing you to run build steps manually.

:::{tip}
**Recipe development is iterative:** Creating conda recipes often involves trial
and error, especially when adapting existing modules. Don't expect the first
attempt to work perfectly - iterate based on build logs and error messages.
:::

### 2.6 Repository structure overview

Your final repository structure should look like:

:::{code-block} console
$ tree
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
:::

:::{important}
Only include directories and files that you actually use.
:::

::::{note}
For ESS-hosted recipes, include the standard CI configuration to build and release packages:

:::{code-block} yaml
include:
  - project: 'ics-infrastructure/gitlab-ci-yml'
    file: 'E3CondaBuild.gitlab-ci.yml'
:::

::::

## Summary

This tutorial showed the complete end-to-end workflow integrating concepts from previous chapters:

1. **EPICS module creation** using standard EPICS tools
2. **Recipe repository setup** with separation of concerns
3. **Build script creation** for conda-build integration
4. **e3 integration** using makefiles and recipes
5. **Package building and testing** with proper pinning

For production use, consider adding comprehensive tests and documentation.

:::{seealso}
**Related topics:**

- Quick reference for build variables: [`require`'s build interface](../reference/build-interface.md)

:::
