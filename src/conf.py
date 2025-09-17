"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options.
For a full list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os


project = "ESS EPICS Environment (e3)"
copyright = "2022, European Spallation Source ERIC"
author = "European Spallation Source ERIC"

# The full version, including alpha/beta/rc tags
try:
    # CI_COMMIT_REF_NAME is defined by GitLab Runner
    # The branch or tag name for which project is built
    release = os.environ["CI_COMMIT_REF_NAME"]
except KeyError:
    # Fallback in dev mode
    release = os.popen("git describe").read().strip()

# Sphinx's version/release pair
version = release


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "myst_parser",             # Markdown support
    "sphinx_design",           # Design components (tabs, grids, cards)
    "sphinx.ext.intersphinx",  # Cross-references to other docs
    "sphinx.ext.viewcode",     # "View Source" links
    "sphinx.ext.todo",         # TODO directive support
    "sphinx_copybutton",       # Copy buttons on code blocks
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "_legacy",
    "CONTRIBUTING.md",
    "MAINTAINING.md"
]

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
html_theme = "furo"

# Theme options are theme-specific
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2980B9",
        "color-brand-content": "#2980B9",
        "color-admonition-title--note": "#2980B9",
        "color-admonition-title--tip": "#2980B9",
        "color-admonition-title--important": "#2980B9",
        "color-admonition-title--caution": "#E67E22",
        "color-admonition-title--warning": "#E74C3C",
        "font-stack": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        "font-stack--monospace": "'JetBrains Mono', 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace",
        "font-size--small": "0.875rem",
        "font-size--small--2": "0.8125rem",
        "font-size--small--3": "0.75rem",
        "font-size--small--4": "0.6875rem",
        "font-size--normal": "1rem",
        "font-size--large": "1.125rem",
        "font-size--large--2": "1.25rem",
        "font-size--large--3": "1.5rem",
        "font-size--large--4": "1.875rem",
        "font-size--large--5": "2.25rem",
        "font-size--large--6": "3rem",
        "line-height": "1.6",
        "line-height--heading": "1.2",
        "font-weight--normal": "400",
        "font-weight--bold": "600",
        "font-weight--heading": "600",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3498DB",
        "color-brand-content": "#3498DB",
        "color-admonition-title--note": "#3498DB",
        "color-admonition-title--tip": "#3498DB",
        "color-admonition-title--important": "#3498DB",
        "color-admonition-title--caution": "#F39C12",
        "color-admonition-title--warning": "#E74C3C",
        "font-stack": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        "font-stack--monospace": "'JetBrains Mono', 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace",
        "font-weight--normal": "400",
        "font-weight--bold": "600",
        "font-weight--heading": "600",
    },
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "source_repository": "https://gitlab.esss.lu.se/e3/e3.pages.esss.lu.se",
    "source_branch": "master",
    "source_directory": "src/",
    "source_edit_link": "https://gitlab.esss.lu.se/e3/e3.pages.esss.lu.se/-/edit/master/src/{filename}",
    "source_view_link": "https://gitlab.esss.lu.se/e3/e3.pages.esss.lu.se/-/blob/master/src/{filename}",
    "sidebar_hide_name": False,
    "footer_icons": [
        {
            "name": "GitLab",
            "url": "https://gitlab.esss.lu.se/e3/e3.pages.esss.lu.se",
            "html": "",
            "class": "",
        },
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (relative to this directory) to use as a favicon
# of the docs. This file should be a Windows icon file (.ico) being 16x16 or
# 32x32 pixels large.
# html_favicon = None

html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "e3": ("http://e3.pages.esss.lu.se/", None),
    "epics": ("https://docs.epics-controls.org/en/latest/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx.
language = "en"

myst_admonition_enable = True
myst_deflist_enable = True
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
]

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = "any"
keep_warnings = False
add_module_names = True
show_authors = False
pygments_style = "sphinx"

# If true, `todo` and `todoList` directives produce output
todo_include_todos = True

# Ignore highlighting ansi in notebooks
suppress_warnings = [
    "misc.highlighting_failure",
    "myst.header",
    "myst.xref_missing",
]

# Copybutton configuration for prompts in code blocks
copybutton_prompt_text = r">>> |\\.\\.\\. |\\$ |In \\[(\\d*)\\]: | {2,5}\\.\\.\\.: | {5,8}: "
copybutton_prompt_is_regexp = True
