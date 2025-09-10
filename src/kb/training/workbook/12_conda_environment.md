# 12. Conda Environment

## conda-build

[conda-build] is only required if you want to build conda packages locally. It's
not directly needed to work with e3.

Install conda-build in the base environment:

```console
conda install -y -n base -c conda-forge conda-build
```

```{note}
The base environment shall be writeable by the current user to run this command.
```

## Cookiecutter

[Cookiecutter](https://cookiecutter.readthedocs.io) creates projects from
templates. It's used to easily create new e3 wrappers, recipes or IOCs for
development. It's not required to run e3.

### Cookiecutter installation

[Cookiecutter] is a Python tool. It can be installed with `pip`.  Note that you
should **never run** `sudo pip install`. This can override system packages.

[Cookiecutter] can be installed in different ways (`pip install --user` or using
[pipx](https://pipxproject.github.io/pipx/)).  As conda is installed, let's use
it.

```console
[iocuser@host:~]$ conda create -y -c conda-forge -n cookiecutter python=3 cookiecutter
```

Add an alias to your `.bashrc`:

```console
[iocuser@host:~]$ echo "alias cookiecutter='~/miniconda/envs/cookiecutter/bin/cookiecutter'" >> ~/.bashrc
```

Reload the `.bashrc` file

```console
[iocuser@host:~] source ~/.bashrc
```

You should be able to run `cookiecutter`:

```console
[iocuser@host:~]$ cookiecutter --version
Cookiecutter 1.7.2 from /home/iocuser/miniconda/envs/cookiecutter/lib/python3.8/site-packages (Python 3.8)
```

### Cookiecutter configuration

Create the file `~/.cookiecutterrc` with your name:

```bash
default_context:
    full_name: "Your Name"
```

This will override the variable `full_name` from any cookiecutter template with
your name.  It will become the default value and avoid you having to enter it
every time you create a new project.  Note that you could add to that file other
variables.

Add the following aliases to your `.bashrc`:

```console
[iocuser@host:~]$ echo "alias e3-wrapper='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-wrapper.git'" >> ~/.bashrc
[iocuser@host:~]$ echo "alias e3-recipe='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-recipe.git'" >> ~/.bashrc
[iocuser@host:~]$ echo "alias e3-ioc='cookiecutter git+https://gitlab.esss.lu.se/ics-cookiecutter/cookiecutter-e3-ioc.git'" >> ~/.bashrc
```

To create a new e3 wrapper, recipe or IOC, just run `e3-wrapper`, `e3-recipe` or
`e3-ioc`.

[conda]: https://docs.conda.io/en/latest/
[conda-build]: https://docs.conda.io/projects/conda-build/en/latest/index.html
[cookiecutter]: https://cookiecutter.readthedocs.io
