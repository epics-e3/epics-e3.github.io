# Module build recipes

In the previous chapter, we built iocStats using `conda build recipe`. Now let's
look inside that `recipe/` directory to understand how recipes are structured and
what they contain.

## Recipe repository layout

A typical e3 recipe repository (like the iocstats-recipe we just cloned) contains
a `recipe/` directory with the conda recipe, and a `src/` directory for site-specific
files (IOC shell snippets, databases, examples):

:::{code-block} console
$ tree
.
├── LICENSE
├── README.md
├── recipe
│   ├── meta.yaml
│   ├── build.sh
│   └── patch/            # source patches (if needed)
└── src
    ├── iocsh/            # startup snippets
    ├── template/         # db/templates/substitutions
    └── cmds/             # example/test startup scripts
:::

:::{note}
Keep variant pinning files outside the repository and pass them with
`--variant-config-files` (`-m`). Some recipes may include their own additional pins;
layer site/global pinning externally.
:::

## Minimal conda recipe

A recipe lives in `recipe/` and consists of `meta.yaml` and a build script.

- `meta.yaml` defines package metadata (name, version, license), source location, requirements, and tests
- `build.sh` contains the build/install steps for Linux

:::{tip}
Understanding conda requirements:

- `build` requirements are tools needed during compilation (e.g. cmake, make, pkg-config)
- `host` requirements are libraries the package compiles against
- `run` requirements are needed at runtime by users of the package

:::

:::{seealso}
A complete recipe example is shown in [Module creation](packaging-modules.md),
which walks through the entire packaging workflow. For comprehensive `meta.yaml` reference, see conda-build's
[Defining metadata](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html).
:::

## Variants and pinning (overview)

Variants define which compiler, Python, or ABI versions to build against. Pinning
ensures binary compatibility across packages.

- Follow conda-forge pins and layer ESS pins for consistent builds across e3.
- Provide pins via `--variant-config-files` at build time (see [Building modules](building-modules.md#pinning-and-variants)).

## Site-specific modifications (overview)

ESS recipes often bundle site-specific content alongside upstream modules:

- Patches: small changes not yet accepted upstream
- IOC shell snippets: configuration fragments for `require`
- Databases and templates: installed for use by IOCs

These assets are typically installed by the module's makefile(s) or the recipe's `build.sh`
into the module layout expected by `require`. This approach allows us to package
community modules with site-specific enhancements while avoiding forks of upstream
source code.

:::{seealso}
Build configuration details are covered in [Module build configurations](makefiles.md).
:::

### Upstream collaboration

- Prefer contributing generally useful fixes to upstream modules (merge/pull requests) rather than carrying long-lived patches.
- Keep patches in `recipe/patch/` (small, focused) and document them clearly in the commit where you add them.
