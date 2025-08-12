# Getting started with e3

The ESS EPICS environment (e3) uses [conda](https://docs.conda.io/en/latest/) for
environment and package management and explicitly builds on [conda-forge](https://conda-forge.org/):
we follow conda-forge’s global pinning file and use their repodata for dependency
resolution. ESS site-specific packages (typically EPICS modules) are hosted on an
internal conda channel in our Artifactory.

## Quick start

```console
$ # Configure conda to use ESS packages (after installing conda/miniforge)
$ conda config --prepend channels ess-internal-conda
$ conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
$ conda config --set channel_priority strict
$
$ # Create and activate an environment with EPICS base and require
$ conda create --name=e3 epics-base require
$ conda activate e3
$
$ # Start an IOC
$ iocsh
```

## Installing conda

Install from conda-forge: [https://conda-forge.org/download/](https://conda-forge.org/download/)

:::{tip}
If you prefer `mamba`, you can substitute `mamba` for `conda` in the commands below.
:::

## Configuring conda

Configure your machine to find packages in the ESS conda channel:

```console
$ conda config --prepend channels ess-internal-conda
$ conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
$ conda config --set channel_priority strict
```

:::{note}
Your configuration is stored at `~/.condarc`. After the commands above, it will look
like:

```yaml
channels:
  - ess-internal-conda
  - conda-forge
channel_alias: https://artifactory.esss.lu.se/artifactory/api/conda
channel_priority: strict
```

:::

:::{important}
Keep the channel order exactly as shown and use `channel_priority: strict`. This
ensures that ESS packages get prioritised and avoids environment conflicts.
:::

:::{caution}
It is important to not mix Anaconda channels with conda-forge as the two are incompatible.
See [Transitioning from Anaconda's `default` channels](https://conda-forge.org/docs/user/transitioning_from_defaults/)
for more information.
:::

## Creating an e3 (conda) environment

Conda manages virtual environments; you control their contents.

To create an environment containing EPICS base and require:

```console
$ conda create --name=e3 epics-base require
```

This tells conda to create an environment named `e3` with EPICS base, require,
and all dependencies.

If you only need the pvAccess executables (e.g. `pvget`, `pvput`):

```console
$ conda create --name=epics epics-base
```

If you have more specific needs, you can pin versions, e.g.:

```console
$ conda create --name=my-special-e3-env epics-base=7.0.8.1 require asyn sequencer
```

You can also create an environment from an `environment.yml` file (a standard
conda environment specification in YAML):

```yaml
dependencies:
  - epics-base=7.0.9
  - require>5
  - modbus
  - s7plc
```

Then create the environment with:

```console
$ conda env create --file=environment.yml
```

## Using conda environments

Once you have created an environment, activate it with:

```console
$ conda activate e3
```

You can deactivate the currently active environment with:

```console
(e3) $ conda deactivate
```

:::{tip}
You can see all of your installed environments with:

```console
$ conda info --envs

# conda environments:
#
base                 * /Users/iocuser/miniforge3
e3                     /Users/iocuser/miniforge3/envs/e3
epics                  /Users/iocuser/miniforge3/envs/epics
my-special-e3-env      /Users/iocuser/miniforge3/envs/my-special-e3-env
```

:::

## Installing an e3 module

Install e3 modules like any other conda package. To add the [iocStats](https://github.com/epics-modules/iocStats)
module, install its e3 conda package `iocstats`:[^casing]

::::{tab-set}
::: {tab-item} Activated environment

```console
(e3) $ conda install iocstats
```

:::
::: {tab-item} Outside any environment

```console
$ conda install --name=e3 iocstats
```

:::
::::

:::{tip}
Both Anaconda - the creators of conda - as well as conda forge have ample documentation,
including instructions for getting started, advice on common issues, and cheatsheets
for commands. See their docs for more information at:

- Anaconda: [Working with conda](https://www.anaconda.com/docs/tools/working-with-conda/main)
- Conda forge: [User documentation](https://conda-forge.org/docs/user/)

:::

[^casing]: conda package names are lowercase only.

:::{seealso}

- Next: [An e3 IOC](2-e3-ioc.md)

:::
