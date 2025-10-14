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

Key options include:

- `-r, --require MODULE` - Load module(s) using `require`
- `-c, --command COMMAND` - Execute IOC shell command(s)
- `-d, --database FILE` - Load database file(s)
- `--iocname NAME` - Set the IOC name
- `-i, --no-init` - Skip automatic `iocInit` call
- `--debug` - Enable debug output
- `--debugger [gdb|lldb|valgrind]` - Run under debugger
- `-V, --version` - Print version and exit
- `-h, --help` - Show help message

## Examples

### Start interactive shell

```console
$ iocsh
```

### Run a startup script

```console
$ iocsh st.cmd
```

### Load modules from command line

```console
$ iocsh -r iocstats -r asyn
```

### Quick testing with commands

```console
$ iocsh -r iocstats -c 'dbpr "*", 1'
```

### Run under debugger

```console
$ iocsh --debugger gdb st.cmd
```

## Implementation details

Internally, `iocsh`:

1. Creates a temporary startup script combining all command-line options
2. Automatically loads the `require` module
3. Processes `-r`, `-c`, and `-d` options in order
4. Appends `iocInit` unless `--no-init` is specified or `iocInit` is already in the script
5. Executes `softIocPVX` with the temporary script

:::{seealso}
**Related topics:**

- [An e3 IOC](../1-getting-started/2-e3-ioc.md) - Creating startup scripts
- [`require` function](3-require-function.md) - Loading modules in scripts
- [Environments](../2-user/1-environments.md) - Setting up e3 environments

:::
