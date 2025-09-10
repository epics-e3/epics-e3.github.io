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
