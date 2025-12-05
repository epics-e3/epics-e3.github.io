# The `iocsh` executable

The `iocsh` executable is the entry point for starting EPICS IOCs in e3. It wraps the EPICS
`softIocPVX` executable and provides convenient options for loading modules and executing commands.

## Description

`iocsh` starts an EPICS IOC shell (based on `softIocPVX`) with support for dynamic module loading
via `require`. It can execute a startup script, load modules directly from the command line,
and perform automatic initialization.

The IOC shell is an interactive command environment where you can:

- Load and configure EPICS modules
- Create and load database records
- Set environment variables
- Execute IOC shell commands
- Initialize and run the IOC

## Options

:::{note}
Run `iocsh --help` for the complete list of options and their usage.
:::

:::{code-block} console
$ iocsh --help
usage: IOC shell for e3 [-h] [-V] [-r MODULE] [-c COMMAND] [-d DATABASE]
                        [--debugger [{gdb,lldb,valgrind}]]
                        [--debugger-args DEBUGGER_ARGS] [--debug] [-i]
                        [--iocname IOCNAME]
                        [file]

ESS EPICS environment (e3) wrapper for softIocPVA

positional arguments:
  file                  Path to startup script

options:
  -h, --help            show this help message and exit
  -V, --version         Print version and exit
  -r, --require MODULE  Load module(s), optionally with version using the
                        syntax `module,version`
  -c, --command COMMAND
                        Execute command(s)
  -d, --database DATABASE
                        Load database file(s) (`dbLoadRecords`)
  --debugger [{gdb,lldb,valgrind}]
                        Run with selected debugger. To pass arguments, use
                        --debuger-args "args"
  --debugger-args DEBUGGER_ARGS
                        Arguments to pass to debugger
  --debug
  -i, --no-init
  --iocname IOCNAME     IOC name (generates fallback if not set)
:::

## Examples

### Start interactive shell

:::{code-block} console
$ iocsh
:::

### Run a startup script

:::{code-block} console
$ iocsh st.cmd
:::

### Load modules from command line

:::{code-block} console
$ iocsh -r iocstats -r asyn
:::

### Quick testing with commands

:::{code-block} console
$ iocsh -r iocstats -c 'dbpr "*", 1'
:::

### Run under debugger

:::{code-block} console
$ iocsh --debugger gdb st.cmd
:::

## Implementation details

Internally, `iocsh`:

1. Creates a temporary startup script combining all command-line options
2. Automatically loads the `require` module
3. Processes `-r`, `-c`, and `-d` options in order
4. Appends `iocInit` unless `--no-init` is specified or `iocInit` is already in the script
5. Executes `softIocPVX` with the temporary script

:::{seealso}
**Related topics:**

- [An e3 IOC](../getting-started/your-first-ioc.md) - Creating startup scripts
- [`require` function](require.md) - Loading modules in scripts
- [Environments](../user/environments.md) - Setting up e3 environments

:::
