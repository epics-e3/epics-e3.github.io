# An e3 IOC

In e3, there is no IOC application build step. Each IOC runs `iocsh`, and startup scripts
use `require` to dynamically load libraries and set up data-file search paths at runtime.

## A startup script

:::{tip}
The examples below assume you have activated the e3 environment created in the previous section,
with `iocstats` installed as shown in [Getting started](installation.md).
:::

A minimal startup script:

:::{code-block} shell
# st.cmd
require iocstats  # or `require(iocstats)` if you prefer
:::

:::{caution}
The last line of the file must end in a newline or that line will not be executed.
:::

Run it with:

:::{code-block} console
(e3) $ iocsh st.cmd
:::

:::{dropdown} Show IOC output
:icon: code
:color: primary
:animate: fade-in

:::{code-block} console
:class: no-copybutton

       ,----.     ,--. ,-----.  ,-----.           ,--.            ,--.,--.
 ,---. '.-.  |    |  |'  .-.  ''  .--./     ,---. |  ,---.  ,---. |  ||  |
| .-. :  .' <     |  ||  | |  ||  |        (  .-' |  .-.  || .-. :|  ||  |
\   --./'-'  |    |  |'  '-'  ''  '--'\    .-'  `)|  | |  |\   --.|  ||  |
 `----'`----'     `--' `-----'  `-----'    `----' `--' `--' `----'`--'`--'
Starting e3 IOC shell version 6.0.0
DEBUG: PID for iocsh 730796
DEBUG: Script path is /home/johndoe/.local/share/mamba/envs/e3/bin/iocsh
DEBUG: Executed from /home/johndoe
DEBUG: Temporary startup script at /tmp/tmplt13wpcv
DEBUG: Running command `softIocPVX -D /home/johndoe/.local/share/mamba/envs/e3/pvxs/dbd/softIocPVX.dbd /tmp/tmplt13wpcv`
INFO: PVXS QSRV2 is loaded, permitted, and ENABLED.
epicsEnvSet REQUIRE_IOC "TEST:johndoe-730796"
epicsEnvSet IOCNAME "TEST:johndoe-730796"
epicsEnvSet IOCSH_TOP "/home/johndoe"
epicsEnvSet IOCSH_PS1 "TEST:johndoe-730796 > "
errlogInit2 2048 2047
dlload /home/johndoe/.local/share/mamba/envs/e3/lib/librequire.so
Loading dbd file /home/johndoe/.local/share/mamba/envs/e3/epics-modules/require/dbd/require.dbd.
Loading module info records for require.
require iocstats
Loading dbd file /home/johndoe/.local/share/mamba/envs/e3/epics-modules/iocstats/dbd/iocstats.dbd.
Loading module info records for iocstats.
iocInit
Starting iocInit
############################################################################
## EPICS R7.0.9
## Rev. 0000-00-00T00:00+0000
## Rev. Date build date/time:
############################################################################
iocRun: All initialization complete
TEST:johndoe-730796 >
:::

:::

:::{note}
`iocInit()` is called implicitly. You can skip this with `iocsh --no-init`. See
`iocsh --help` for more options.
:::

### A slightly more complete example

A more realistic startup script might look like:

:::{code-block} shell
# st.cmd
require device
require sequencer

epicsEnvSet("P", "Foo")
epicsEnvSet("R", "Bar")

iocshLoad("${device_DIR}init.iocsh", "PREFIX=$(P)-$(R):")
dbLoadRecords("${device_DIR}device.template", "PREFIX=$(P)-$(R):")

afterInit("seq device_control")
:::
