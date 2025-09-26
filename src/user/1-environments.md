# Environments

## Installing and configuring `conda`

Before you can create any e3 environments, you will need a working---and properly
configured---conda environment. See [Getting Started](../getting-started/1-getting-started.md).

## Creating e3 environments

An e3 environment is a virtual (conda) environment containing the EPICS module *require*.
What else goes into the environment is dictated by you and your needs.

To exemplify this, we will create several separate environments.

Let's create one containing [*StreamDevice*](https://paulscherrerinstitute.github.io/StreamDevice/):

```console
$ conda create -n e3-and-stream epics-base require stream
```

If you only need the pvAccess executables (e.g. `pvget`, `pvput`)[^conda-forge-base]:

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

### Using your e3 environments

Activate the environment you just created that contains stream:

```console
$ conda activate e3-and-stream
```

You can now test that this worked by starting an IOC:

```console
(e3-and-stream) $ iocsh

       ,----.     ,--. ,-----.  ,-----.           ,--.            ,--.,--.
 ,---. '.-.  |    |  |'  .-.  ''  .--./     ,---. |  ,---.  ,---. |  ||  |
| .-. :  .' <     |  ||  | |  ||  |        (  .-' |  .-.  || .-. :|  ||  |
\   --./'-'  |    |  |'  '-'  ''  '--'\    .-'  `)|  | |  |\   --.|  ||  |
 `----'`----'     `--' `-----'  `-----'    `----' `--' `--' `----'`--'`--'

Starting e3 IOC shell version 5.1.1
WARNING: Environment variable IOCNAME is not set.
DEBUG: PID for iocsh 274446
DEBUG: Script path is /home/johndoe/miniconda3/envs/e3-and-stream/bin/iocsh
DEBUG: Executed from /home/johndoe
DEBUG: Temporary startup script at /tmp/tmp5670yziy
DEBUG: Running command `/home/johndoe/miniconda3/envs/e3-and-stream/epics/bin/linux-x86_64/softIocPVX -D /home/johndoe/miniconda3/envs/e3-and-stream/epics/dbd/softIocPVX.dbd /tmp/tmp5670yziy`
epicsEnvSet REQUIRE_IOC "TEST:johndoe-274446"
epicsEnvSet IOCSH_TOP "/home/johndoe"
epicsEnvSet IOCSH_PS1 "localhost-274446 > "
errlogInit2 2048 2047
dlload /home/johndoe/miniconda3/envs/e3-and-stream/modules/require/5.1.1/lib/linux-x86_64/librequire.so
dbLoadDatabase /home/johndoe/miniconda3/envs/e3-and-stream/modules/require/5.1.1/dbd/require.dbd
require_registerRecordDeviceDriver
Loading module info records for require
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.9
## Rev. 0000-00-00T00:00+0000
## Rev. Date build date/time:
############################################################################
iocRun: All initialization complete
localhost-274446 >
```

:::{tip}
Exit the IOC by typing `exit` at the console, or by pressing `^ d` (<Ctrl> + d).
:::

You can see which packages are installed in the environment by running:

```console
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
```

You can test any of these modules by running, for example,

```console
(e3-and-stream) $ iocsh -r asyn  # -r is shorthand for the `require` call
```

:::{tip}
The `e3-and-stream` environment will contain `asyn` ([*asyn*](https://github.com/epics-modules/asyn))
as that is a dependency of `stream`.
:::

[^conda-forge-base]: This is technically not e3 - we will only be installing default
EPICS base from conda-forge.
