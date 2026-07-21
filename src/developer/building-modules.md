# Building modules

The ESS EPICS environment (e3) builds packages with `conda-build`, following
conda-forge’s global pinnings and layering ESS site constraints on top. This
page covers setting up a dedicated build environment, building a package
locally, and using the pinning file.

:::{important}
This guide assumes you are comfortable with git, Linux command line, and basic build systems.
You must also have `conda` (or `mamba`) installed and configured per
[Getting started with e3](../getting-started/installation.md).

If you need to review these prerequisites, see the [main documentation page](../index.md#prerequisites) for external resources.
:::

:::{note}
**About this guide's structure:**

This developer documentation follows a learn-by-doing approach. We start with conda-build
to set up working build environments (managing all dependencies automatically), then overview
recipe structure conceptually, before diving into makefile implementation details, and finally conda recipe
formulation. This flow ensures you have functional tooling before encountering the complexity of manual
builds and packaging.
:::

## Setting up a build environment

To build EPICS modules (or any conda package), you need `conda-build`. You can
install this into an environment of your choice:

:::{code-block} console
(base) $ conda install conda-build
:::

:::{tip}
We recommend using a clean environment for building, to keep build tooling and its
dependencies isolated:

:::{code-block} console
$ conda create --name=conda-build conda-build conda-verify
$ conda activate conda-build
:::

:::

(building-a-conda-package)=

## Building a conda package - an example with iocStats

We would typically be able to build a conda package just by doing:

:::{code-block} console
(base) $ git clone https://gitlab.esss.lu.se/e3/recipes/iocstats-recipe
(base) $ cd iocstats-recipe
(base) $ conda build --no-long-test-prefix recipe
:::

Where running the above commands would resolve build (and host) requirements and download these, before it builds iocStats
itself. However, our e3 environment is built on top of conda-forge, which uses explicit dependency declarations. In particular,
iocStats' conda recipe contains a dependency macro `stdlib('c')` (read more [here](https://conda-forge.org/news/2024/03/24/stdlib-migration/))
which must first be processed. This leads us to the next topic: pinning files.

:::{note}
If you still would like to run the steps above, it should still build on most platforms if you remove or comment
out the line containing `stdlib('c')` in `./recipe/meta.yaml`.
:::

:::{important}
Always pass `--no-long-test-prefix`. By default, `conda-build` runs the package tests in an environment
whose path is padded to 255 characters. That is long enough to break EPICS macro expansion of
`$(<module>_DIR)`, so recipes whose tests load an iocsh snippet fail on a file that does exist. The ESS
CI templates pass this flag for the same reason.
:::

::::{tip}
Rather than repeating the flag on every build, set it once in `~/.condarc` and leave it out of the
commands that follow:

:::{code-block} yaml
conda-build:
  long_test_prefix: false
:::

Unlike the channel settings, this one has no `conda config` equivalent and must be edited by hand.
::::

## Pinning and variants

Pinning aligns dependency versions across packages to ensure ABI compatibility
and consistent solver outcomes.

- We follow conda-forge's global pins for compilers and core libraries
  ([conda-forge-pinning-feedstock](https://github.com/conda-forge/conda-forge-pinning-feedstock))
- We layer ESS-specific pins via the e3 pinning repository
  ([e3-pinning](https://gitlab.esss.lu.se/e3/recipes/e3-pinning/))

:::{note}
We pin dependencies to ensure ABI (Application Binary Interface) compatibility; this
means that compiled binaries link and run correctly against their dependency versions
(headers, symbols, calling conventions). Pinning helps avoid silent breakage.
:::

Download variant-config files (preferably outside your recipe repository) and pass
them on the command line using `-m` (`--variant-config-files`). To always use the latest
upstream pins, download them when you build:

:::{code-block} console
(base) $ curl -fsSL -o /tmp/conda_forge_pins.yaml https://raw.githubusercontent.com/conda-forge/conda-forge-pinning-feedstock/main/recipe/conda_build_config.yaml
(base) $ curl -fsSL -o /tmp/e3_pins.yaml https://gitlab.esss.lu.se/e3/recipes/e3-pinning/-/raw/main/conda_build_config.yaml
:::

:::{caution}
Up-to-date pinning files are essential to avoid build failures and dependency conflicts.
:::

Thus, if we wanted to re-build the earlier iocStats example with conda-forge
and ESS pinning applied:

:::{code-block} console
(base) $ conda build -m /tmp/conda_forge_pins.yaml -m /tmp/e3_pins.yaml --no-long-test-prefix recipe
:::

Artifacts are written to your build folder (e.g.
`~/miniforge3/conda-bld/linux-64/<name>-<version>-<build>.conda`).

## Configuring conda for development

To install a package you have just built, prepend your build folder (shown above as
`~/miniforge3/conda-bld`) to the [user configuration](../getting-started/installation.md#configuring-conda),
so it takes precedence over the released packages:

:::{code-block} console
(conda-build) $ conda config --prepend channels ~/miniforge3/conda-bld
:::

::::{note}
Your `~/.condarc` will then list it at the top of `channels`:

:::{code-block} yaml
channels:
  - ~/miniforge3/conda-bld
  - ess-conda-local
  - conda-forge
:::
::::

You can then install and test the fresh build as usual:

:::{code-block} console
(conda-build) $ conda install <package-name>
:::

:::{note}
Upstream documentation usually suggests `conda install --use-local`. With `conda-build` in an
environment of its own that can quietly miss your build, so prepend the folder explicitly instead.
:::

:::{tip}
Just as with other `conda` (or `mamba`) related actions, there is ample documentation available
from upstream.

- Anaconda: [Conda-build documentation](https://docs.conda.io/projects/conda-build/en/stable/)
- Conda forge: [Maintainer documentation](https://conda-forge.org/docs/maintainer/)

:::
