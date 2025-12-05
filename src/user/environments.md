# Environments

## Installing and configuring `conda`

Before you can create any e3 environments, you will need a working - and properly
configured - conda environment. See [Getting Started](../getting-started/installation.md).

## Creating e3 environments

An e3 environment is a virtual (conda) environment containing the EPICS module *require*.
What else goes into the environment is dictated by you and your needs; you can create
different environments for different IOCs on the same host (even with different EPICS base
versions), or you can test an IOC against different module versions.

The following examples demonstrate different approaches to creating environments.

Let's create one containing [*StreamDevice*](https://paulscherrerinstitute.github.io/StreamDevice/):

:::{code-block} console
$ conda create -n e3-and-stream epics-base require stream
:::

:::{dropdown} Show conda output
:icon: terminal
:color: info
:animate: fade-in

:::{code-block} console
:class: no-copybutton

$ conda create -n e3-and-stream epics-base require stream
Channels:
 - ess-conda-local
 - conda-forge
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/johndoe/miniforge3/envs/e3-and-stream

  added / updated specs:
    - epics-base
    - require
    - stream


The following NEW packages will be INSTALLED:

  asyn               ess-conda-local/linux-64::asyn-4.44.2-h4abd79c_0
  epics-base         conda-forge/linux-64::epics-base-7.0.9.0-h2f0025b_0
  pcre               conda-forge/linux-64::pcre-8.45-h9c3ff4c_0
  readline           conda-forge/linux-64::readline-8.2-h8228510_1
  require            ess-conda-local/linux-64::require-5.1.1-h6f9ad6c_0
  stream             ess-conda-local/linux-64::stream-2.8.25-hc22a8e2_0
  (... additional dependencies ...)

Proceed ([y]/n)? y

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate e3-and-stream
#
# To deactivate an active environment, use
#
#     $ conda deactivate
:::

Note how conda automatically resolves and installs `asyn` as a dependency of `stream`.

:::

If you only need the pvAccess executables (e.g. `pvget`, `pvput`):

:::{code-block} console
$ conda create --name=epics epics-base
:::

:::{note}
This creates a basic EPICS environment (not technically e3, as it lacks *require*) using conda-forge's
[EPICS base package](https://anaconda.org/conda-forge/epics-base/). Useful when you only need
EPICS tools without the e3 module loading system.
:::

If you have more specific needs, you can pin versions, e.g.:

:::{code-block} console
$ conda create --name=my-special-e3-env epics-base=7.0.8.1 require asyn sequencer
:::

You can also create an environment from an `environment.yml` file (a standard
conda environment specification in YAML):

:::{code-block} yaml
dependencies:
  - epics-base=7.0.9
  - require>5
  - modbus
  - s7plc
:::

Then create the environment with:

:::{code-block} console
$ conda env create --file=environment.yml
:::

### Using your e3 environments

Activate the environment:

:::{code-block} console
$ conda activate e3-and-stream
:::

You can now test that this worked by starting an IOC:

:::{code-block} console
(e3-and-stream) $ iocsh

       ,----.     ,--. ,-----.  ,-----.           ,--.            ,--.,--.
 ,---. '.-.  |    |  |'  .-.  ''  .--./     ,---. |  ,---.  ,---. |  ||  |
| .-. :  .' <     |  ||  | |  ||  |        (  .-' |  .-.  || .-. :|  ||  |
\   --./'-'  |    |  |'  '-'  ''  '--'\    .-'  `)|  | |  |\   --.|  ||  |
 `----'`----'     `--' `-----'  `-----'    `----' `--' `--' `----'`--'`--'

Starting e3 IOC shell version 6.0.0
...
test >
:::

:::{tip}
Exit the IOC by typing `exit` at the console, or by pressing `^ d` (<Ctrl> + d).
:::

You can see which packages are installed in the environment by running:

:::{code-block} console
$ conda list
# packages in environment at /home/johndoe/miniconda3/envs/e3-and-stream:
#
# Name                    Version                   Build  Channel
...
asyn                      4.44.2               h4abd79c_0    ess-conda-local
...
require                   5.1.1                h6f9ad6c_0    ess-conda-local
...
stream                    2.8.25               hc22a8e2_0    ess-conda-local
...
:::

You can test any of these modules by running, for example:

:::{code-block} console
(e3-and-stream) $ iocsh -r asyn  # -r is shorthand for the `require` call
:::

:::{tip}
The `e3-and-stream` environment will contain `asyn` ([*asyn*](https://github.com/epics-modules/asyn))
as that is a dependency of `stream`.
:::
