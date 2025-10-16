# e3 documentation

Source for e3 documentation hosted on GitLab pages: https://e3.pages.ess.eu

The URL relies on this project's path, see https://docs.gitlab.com/user/project/pages/getting_started_part_one/#gitlab-pages-default-domain-names.

The documentation is built using
[Sphinx](http://www.sphinx-doc.org/en/master/index.html) and
[MyST](https://myst-parser.readthedocs.io/en/latest/index.html), stylized with
the [Furo](https://pradyunsg.me/furo/) theme. All files are written in
Markdown, none in reStructuredText.

The deployment is updated on merge into the default (`main`) branch.

## Build locally

With conda: `conda env create -f environment.yml && conda activate e3-docs-dev && make html`

Or use the same container as CI:
`docker run --rm -v $(pwd):/docs registry.esss.lu.se/ics-docker/sphinx sphinx-build -M html src build`

## MyST

Supports all the syntax of the CommonMark Markdown but also several extensions
to CommonMark (often called [MyST Markdown syntax](https://myst-parser.readthedocs.io/en/latest/using/syntax.html)).
Additional features include [sphinx-design](https://sphinx-design.readthedocs.io/) components and copy buttons on code blocks.
