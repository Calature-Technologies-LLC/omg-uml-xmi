# Configuration file for the Sphinx documentation builder.

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
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Templates
templates_path = ["_templates"]

# Files and directories to exclude from the build
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/__pycache__",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_title = f"{project} v{version}"
html_short_title = project

# Master document (for Sphinx < 2.0 compatibility)
master_doc = "index"

# Default role for inline markup
default_role = "py:obj"

# Primary domain
primary_domain = "py"