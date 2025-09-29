# Building modules

The ESS EPICS environment (e3) builds packages with `conda-build`, following
conda-forge’s global pinnings and layering ESS site constraints on top. This
page covers setting up a dedicated build environment, building a package
locally, and using the pinning file.

:::{important}
This guide assumes you are comfortable with git, Linux command line, and basic build systems.
You must also have `conda` (or `mamba`) installed and configured per
[Getting started with e3](../1-getting-started/1-getting-started.md).

If you need to review these prerequisites, see the [main documentation page](../index.md#prerequisites) for external resources.
:::

## Setting up a build environment

All you strictly need to be able to build EPICS modules---or any other conda
package---is `conda-build`. You can install this into an environment of your choice:

```console
(base) $ conda install conda-build
```

:::{tip}
We recommend using a clean environment for building, to keep build tooling and its
dependencies isolated.

```console
$ conda create --name=conda-build conda-build conda-verify
$ conda activate conda-build
```

:::

## Building a conda package - an example with iocStats

We would typically be able to build a conda package just by doing:

```console
(base) $ git clone https://gitlab.esss.lu.se/e3/recipes/iocstats-recipe
(base) $ cd iocstats-recipe
(base) $ conda build recipe
```

Where running the above commands would resolve build (and host) requirements and download these, before it builds iocStats
itself. However, our e3 environment is built on top of conda-forge, which uses modern conventions. In particular,
iocstats' conda recipe contains a dependency macro `stdlib('c')` (read more [here](https://conda-forge.org/news/2024/03/24/stdlib-migration/))
which first must be processed. This leads us to the next topic: pinning files.

:::{note}
If you still would like to run the steps above, it should still build on most platforms if you remove or comment
out the line containing `stdlib('c')` in `./recipe/meta.yaml`.
:::

## Pinning and variants

Pinning aligns dependency versions across packages to ensure ABI compatibility
and consistent solver outcomes.

- We follow conda-forge’s global pins for compilers and core libraries.
- We layer ESS-specific pins via the e3 pinning repository (main branch):
  [`https://gitlab.esss.lu.se/e3/recipes/e3-pinning/`](https://gitlab.esss.lu.se/e3/recipes/e3-pinning/)

:::{note}
We pin dependencies to ensure ABI (Application Binary Interface) compatibility; this
means that compiled binaries link and run correctly against their dependency versions
(headers, symbols, calling conventions). Pinning helps avoid silent breakage.
:::

Download variant-config files (preferably outside your recipe) repository and pass
them on the command line using `-m` (`--variant-config-files`). To always use the latest
upstream pins, download them when you build:

```console
(base) $ curl -fsSL -o /tmp/conda_forge_pins.yaml \
  https://raw.githubusercontent.com/conda-forge/conda-forge-pinning-feedstock/main/recipe/conda_build_config.yaml
(base) $ curl -fsSL -o /tmp/e3_pins.yaml \
  https://gitlab.esss.lu.se/e3/recipes/e3-pinning/-/raw/main/conda_build_config.yaml
```

:::{caution}
Up-to-date pinning files are essential to avoid build failures and dependency conflicts.
:::

Thus, if we wanted to re-build the earlier iocstats example with conda-forge
and ESS pinning applied:

```console
(base) $ conda build \
  -m /tmp/conda_forge_pins.yaml \
  -m /tmp/e3_pins.yaml \
  recipe
```

Artifacts are written under your build folder (e.g.
`~/miniforge3/conda-bld/linux-64/<name>-<version>-<build>.tar.bz2`). You can install the
fresh build if you want to test it out:

```console
(conda-build) $ conda install --use-local <package-name>
```

:::{tip}
Just as with other `conda` (or `mamba`) related actions, there is ample documentation available
from upstream.

- Anaconda: [Conda-build documentation](https://docs.conda.io/projects/conda-build/en/stable/)
- Conda forge: [Maintainer documentation](https://conda-forge.org/docs/maintainer/)

:::
