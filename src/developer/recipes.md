# Module build recipes

This chapter introduces how e3 recipe repositories are structured and how a
minimal conda recipe is organised.

## Recipe repository layout

A typical repository contains a `recipe/` directory with the conda recipe, and a
`src/` directory for site-specific files (patches, IOC shell snippets, databases,
examples):

:::{code-block} console
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
:::

:::{note}
Keep variant pinning files outside the repository and pass them with
`--variant-config-files` (`-m`). Some recipes may include their own additional pins;
layer site/global pinning externally.
:::

## Minimal conda recipe

A recipe lives in `recipe/` and consists of `meta.yaml` and a build script.

- `meta.yaml` defines name, version, source, requirements, test, and metadata.
- `build.sh` contains the build/install steps for Linux.

`meta.yaml` serves as both the package manifest (name, version, license, documentation) and (partial) build definition,
specifying what to build, where to get the source, how to compile it, what it depends on, and how to test it.
The file uses a structured format to declare package metadata and build requirements that conda-build processes.

:::{tip}
Understanding conda requirements:

- `build` requirements are tools needed during compilation (e.g. cmake, make, pkg-config)
- `host` requirements are libraries the package compiles against
- `run` requirements are needed at runtime by users of the package

:::

:::{seealso}
Complete recipes with all `meta.yaml` fields filled out are demonstrated in [Module creation](packaging-modules.md),
which walks through the entire packaging workflow. For comprehensive meta.yaml reference, see conda-build's
[Defining metadata](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html).
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
into the module layout expected by `require`. This approach allows us to package
community modules with site-specific enhancements while avoiding forks of upstream
source code.

:::{seealso}
Build configuration details are covered in [Module build configurations](makefiles.md).
:::

### Upstream collaboration

- Prefer contributing generally useful fixes to upstream modules (merge/pull requests) rather than carrying long-lived patches.
- Keep site-specific changes in `src/patches/` (small, focused) and document them clearly in the commit where you add them.
