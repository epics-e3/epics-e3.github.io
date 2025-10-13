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

- [Building modules](1-conda-build.md) - build environment and conda-build usage
- [Module build recipes](2-recipes.md) - recipe structure and meta.yaml details
- [Module build configurations](3-module-makefiles.md) - e3 makefile creation

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

This creates the standard EPICS application structure with `configure/`, `exampleModuleApp/`, `iocBoot/`, and more.

:::{note}
The EPICS base utility `makeBaseApp` scaffolds an IOC application; installable module artifacts are provided
via the e3 makefile in [2.3 Create the e3 makefile](#23-create-the-e3-makefile).
:::

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

:::{note}
The actual implementation of device support, database files, and application
code is beyond the scope of this tutorial. Refer to the EPICS documentation
links provided earlier for detailed development guidance.
:::

Once you have a version you are satisfied, which has been reviewed and merged into the default branch,
you should apply a git tag with the version information for this. Generally, the first version you publish/release
should be `1.0.0`.

:::{tip}
We encourage use of [semantic versioning](https://semver.org/).
:::

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

Create `recipe/meta.yaml` with a minimal structure.

For background and all available fields, see conda-build’s documentation: [Defining metadata (meta.yaml)](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html).

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
    - {{ compiler('c') }}    # If you are are using .c sources
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
```

:::{tip}
Use jinja2 filters when upstream version format differs from the URL or tag format:

```yaml
{% set version = "1.2" %}
source:
  url: .../-/archive/v{{ version | replace('.', '-') }}/...tar.gz
```

:::

Add any needed site-specific files (IOC shell snippets, templates, patches) to
the `src/` directory as described in
[Module build recipes](2-recipes.md).

:::{tip}
Compute the checksum from the exact tarball URL you use:

```console
$ curl -L "https://gitlab.esss.lu.se/epics-modules/{{ name }}/-/archive/v{{ version }}/{{ name }}-v{{ version }}.tar.gz" | shasum -a 256
```

:::

:::{important}
Always specify the correct license. This is crucial for legal compliance and package distribution.
:::

#### ESS recipe best practices

- Prefer `source: url` tarballs with a `sha256`; use tags for traceability.
- Have `version` be bound to upstream version and using jinja2 for separator conversion
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
- Tests: Utilise `run-iocsh` and consider `test -f` checks for key installed files.

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
  conda-build /workspace/recipe
```

#### Test the package

```console
$ conda install --use-local examplemodule
$ iocsh -r examplemodule
```

:::{tip}
You can also inspect installed files with `ls` or `tree` under your prefix.
Prefer declaring required files via your recipe rather than checking them ad-hoc.
:::

#### Debugging builds

If builds fail, open an interactive debug environment to investigate:

```console
$ conda debug recipe
```

This reproduces the build environment, allowing you to run build steps manually.

:::{tip}
**Recipe development is iterative:** Creating conda recipes often involves trial
and error, especially when adapting existing modules. Don't expect the first
attempt to work perfectly - iterate based on build logs and error messages.
:::

### 2.7 Repository structure overview

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

:::{important}
Only include directories and files that you actually use.
:::

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

:::{seealso}
**Related topics:**

- Quick reference for build variables: [`require`'s build interface](../4-kb/1-build-interface.md)

:::
