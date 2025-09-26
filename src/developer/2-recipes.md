# Module build recipes

This chapter introduces how e3 recipe repositories are structured and how a
minimal conda recipe is organised.

## Recipe repository layout

A typical repository contains a `recipe/` directory with the conda recipe, and a
`src/` directory for site-specific files (patches, IOC shell snippets, databases,
examples):

```console
$ tree
.
├── LICENSE
├── README.md
├── recipe
│   ├── meta.yaml
│   └── build.sh
└── src
    ├── iocsh/            # startup snippets
    ├── template/         # db/templates/substitutions
    ├── patches/          # source patches (if needed)
    └── cmds/             # example/test startup scripts
```

:::{note}
Keep variant pinning files outside the repository and pass them with
`--variant-config-files` (`-m`). Some recipes may include their own additional pins;
layer site/global pinning externally.
:::

## Minimal conda recipe

A recipe lives in `recipe/` and consists of `meta.yaml` and a build script.

- `meta.yaml` defines name, version, source, requirements, test, and metadata.
- `build.sh` contains the build/install steps for Linux.

At a high level, `meta.yaml` includes:

- `package`: name and version
- `source`: where to get the upstream source
- `build`: number, script, and optional features
- `requirements`: split into `build`, `host`, `run`
- `test`: requirements, commands, and test files
- `about` and `extra`: metadata

:::{tip}

- `build` requirements are for the build tools (e.g. cmake, make, pkg-config).
- `host` requirements are the libraries the package is compiled against.
- `run` requirements are needed at runtime by consumers of the package.

:::

## Variants and pinning (overview)

Variants define which compiler, Python, or ABI versions to build against. Pinning
ensures binary compatibility across packages.

- Follow conda-forge pins and layer ESS pins for consistent builds across e3.
- Provide pins via `--variant-config-files` at build time (see previous chapter).

## Site-specific modifications (overview)

ESS recipes often bundle site-specific content alongside upstream modules:

- Patches: small changes not yet accepted upstream
- IOC shell snippets: configuration fragments for `require`
- Databases and templates: installed for use by IOCs

These assets are typically installed by the module's makefile(s) or the recipe's `build.sh`
into the module layout expected by `require`.

:::{note}
This approach of "module wrappers" is explained in detail in [IOCs and modules](../user/2-iocs-and-modules.md#module-wrappers).
The build configuration is covered in [Module build configurations](3-module-makefiles.md).
:::

### Upstream collaboration

- Prefer contributing generally useful fixes to upstream modules (merge/pull requests) rather than carrying long-lived patches.
- Keep site-specific changes in `src/patches/` (small, focused) and document them clearly in the commit where you add them.
