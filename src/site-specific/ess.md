# European Spallation Source

:::{important}
Here you find configurations specific for using e3 inside the European Spallation Source. These configurations
will not work if you don't have access to internal network.
:::

## Quickstart

:::{code-block} console
$ # Configure conda to use ESS packages (after installing conda/miniforge)
$ conda config --prepend channels ess-conda-local
$ conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
$ conda config --set channel_priority strict
$
$ # Create and activate an environment with EPICS base and require
$ conda create --name=e3 epics-base require
$ conda activate e3
$
$ # Start an IOC
$ iocsh
:::

## Configure conda

Configure your machine to find packages in the ESS conda channel:

:::{code-block} console
$ conda config --prepend channels ess-conda-local
$ conda config --set channel_alias https://artifactory.esss.lu.se/artifactory/api/conda
$ conda config --set channel_priority strict
:::

:::{note}
Your configuration is stored at `~/.condarc`. After the commands above, it will look
like:

:::{code-block} yaml
channels:
  - ess-conda-local
  - conda-forge
channel_alias: https://artifactory.esss.lu.se/artifactory/api/conda
channel_priority: strict
:::

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
