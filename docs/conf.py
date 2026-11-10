# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
from datetime import datetime

# Add the project source directory to sys.path so Sphinx can find the package
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

project = "omg-uml-xmi"
copyright = f"{datetime.now().year}, Calature Technologies"
author = "Devin Hedge"
release = "0.1.0"
version = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = {
    "EClass": "pyecore.ecore.EClass",
    "EPackage": "pyecore.ecore.EPackage",
    "EAttribute": "pyecore.ecore.EAttribute",
    "EReference": "pyecore.ecore.EReference",
    "EOperation": "pyecore.ecore.EOperation",
    "EEnum": "pyecore.ecore.EEnum",
    "EDataType": "pyecore.ecore.EDataType",
    "ResourceSet": "pyecore.resources.ResourceSet",
}

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_class_signature = "separated"

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pyecore": ("https://pyecore.readthedocs.io/en/latest/", None),
    "lxml": ("https://lxml.de/apidoc/", None),
}

# Templates and static files
templates_path = ["_templates"]
html_static_path = ["_static"]

# Files and directories to exclude from the build
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/__pycache__",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_title = f"{project} v{version}"
html_short_title = project
html_favicon = None
html_logo = None

# Context for the theme
html_context = {
    "display_github": True,
    "github_user": "calaturetech",
    "github_repo": "omg-uml-xmi",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# -- Options for other builders ----------------------------------------------

# LaTeX output
latex_documents = [
    ("index", "omg-uml-xmi.tex", "omg-uml-xmi Documentation", "Devin Hedge", "manual"),
]

# Manual page output
man_pages = [
    ("index", "omg-uml-xmi", "omg-uml-xmi Documentation", ["Devin Hedge"], 1),
]

# Texinfo output
texinfo_documents = [
    (
        "index",
        "omg-uml-xmi",
        "omg-uml-xmi Documentation",
        "Devin Hedge",
        "omg-uml-xmi",
        "UML 2.5.1 / XMI 2.5.1 serializer for Python",
        "Software Development",
    ),
]

# Epub output
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ["search.html"]

# -- Extension configuration -------------------------------------------------

# Todo extension
todo_include_todos = True

# Coverage extension
coverage_show_missing_items = True

# -- Custom configuration ----------------------------------------------------

# Master document (for Sphinx < 2.0 compatibility)
master_doc = "index"

# Default role for inline markup
default_role = "py:obj"

# Primary domain
primary_domain = "py"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_css_files = [
    "custom.css",
]

# Add any paths that contain custom JavaScript files here
html_js_files = []

# Suppress warnings
suppress_warnings = [
    "autodoc.import_object",
]

# Nitpick ignore - ignore warnings about missing references
nitpick_ignore = [
    ("py:class", "pyecore.ecore.EClass"),
    ("py:class", "pyecore.ecore.EPackage"),
    ("py:class", "pyecore.ecore.EAttribute"),
    ("py:class", "pyecore.ecore.EReference"),
    ("py:class", "pyecore.ecore.EOperation"),
    ("py:class", "pyecore.ecore.EEnum"),
    ("py:class", "pyecore.ecore.EDataType"),
    ("py:class", "pyecore.resources.ResourceSet"),
    ("py:class", "lxml.etree._Element"),
    ("py:class", "lxml.etree._ElementTree"),
]

# Linkcheck settings
linkcheck_ignore = [
    r"https://github.com/calaturetech/omg-uml-xmi/.*",
]
linkcheck_timeout = 30
linkcheck_retries = 2