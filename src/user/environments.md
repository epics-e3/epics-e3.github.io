# Environments

## Installing and configuring `conda`

Before you can create any e3 environments, you will need a working---and properly
configured---conda environment. See [Getting Started](../getting-started/installation.md).

## Creating e3 environments

An e3 environment is a virtual (conda) environment containing the EPICS module *require*.
What else goes into the environment is dictated by you and your needs.

To exemplify this, we will create several separate environments.

Let's create one containing [*StreamDevice*](https://paulscherrerinstitute.github.io/StreamDevice/):

:::{code-block} console
$ conda create -n e3-and-stream epics-base require stream
:::

If you only need the pvAccess executables (e.g. `pvget`, `pvput`):

:::{code-block} console
$ conda create --name=epics epics-base
:::

:::{note}
This creates a basic EPICS environment (not technically e3) using conda-forge's EPICS base package.
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

Activate the environment you just created that contains stream:

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
DEBUG: PID for iocsh 16709
DEBUG: Script path is /home/johndoe/miniconda3/envs/e3-and-stream/bin/iocsh
DEBUG: Executed from /home/johndoe
DEBUG: Temporary startup script at /var/folders/0r/h6b_p_h10yj328dtzyg660fw0000gn/T/tmp_pgpzcfh
DEBUG: Running command `softIocPVX -D /home/johndoe/miniconda3/envs/e3-and-stream/pvxs/dbd/softIocPVX.dbd /var/folders/0r/h6b_p_h10yj328dtzyg660fw0000gn/T/tmp_pgpzcfh`
INFO: PVXS QSRV2 is loaded, permitted, and ENABLED.
epicsEnvSet REQUIRE_IOC "test"
epicsEnvSet IOCNAME "test"
epicsEnvSet IOCSH_TOP "/home/johndoe
epicsEnvSet IOCSH_PS1 "test > "
errlogInit2 2048 2047
dlload /home/johndoe/miniconda3/envs/e3-and-stream/lib/librequire.so
Loading dbd file /home/johndoe/miniconda3/envs/e3-and-stream/epics-modules/require/dbd/require.dbd.
Loading module info records for require.
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.9
## Rev. 0000-00-00T00:00+0000
## Rev. Date build date/time:
############################################################################
iocRun: All initialization complete
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

You can test any of these modules by running, for example,

:::{code-block} console
(e3-and-stream) $ iocsh -r asyn  # -r is shorthand for the `require` call
:::

:::{tip}
The `e3-and-stream` environment will contain `asyn` ([*asyn*](https://github.com/epics-modules/asyn))
as that is a dependency of `stream`.
:::
