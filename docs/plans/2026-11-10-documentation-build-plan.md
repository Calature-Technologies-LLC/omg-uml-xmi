# Documentation Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create minimal Sphinx documentation build with ReadTheDocs deployment for auto-generated API reference from docstrings.

**Architecture:** Minimal Sphinx setup with autodoc/napoleon/viewcode extensions, auto-generated API reference via `.. automodule::` for all public modules in `src/omg_uml_xmi/`, deployed to ReadTheDocs with `.readthedocs.yaml` config. Only `latest` version for v1, semantic versioning ready.

**Tech Stack:** Sphinx 7.x, sphinx-rtd-theme, autodoc, napoleon, viewcode, intersphinx; lxml for XML; pyecore for model mapping.

**Spec:** `docs/superpowers/specs/2026-11-10-documentation-build-design.md`

## Global Constraints

- Python 3.12+ (from pyproject.toml)
- Dependencies: `sphinx>=7,<8`, `sphinx-rtd-theme>=2,<3` (already in `docs` extras)
- Output URL: `https://omg-uml-xmi.readthedocs.io` (from pyproject.toml)
- Versioning: Semantic versioning, only `latest` for v1
- Examples: Generated from tests (placeholder for v1)
- URL: `https://omg-uml-xmi.readthedocs.io` (from pyproject.toml)

## Review Focus

1. **Missing docstrings**: Auto-generated API will have empty sections for undocumented modules/classes/functions — ensure at least module-level docstrings exist
2. **Import cycles**: Autodoc may fail on circular imports in `src/omg_uml_xmi/` — test imports early
3. **Missing docstrings on public API**: Auto-generated API will show empty sections — at minimum module-level docstrings needed
4. **Import errors during build**: Sphinx imports modules during build — all imports must resolve
4. **ReadTheDocs build failures**: RTD uses different environment — test locally with same Python version

---

### Task 1: Create docs/ directory structure and conf.py

**Files:**
- Create: `docs/conf.py`
- Create: `docs/requirements.txt`
- Create: `docs/Makefile`
- Create: `docs/make.bat`

**Interfaces:**
- Consumes: None (first task)
- Produces: Sphinx configuration, requirements for RTD, build scripts

- [ ] **Step 1: Write failing test for conf.py existence**

```python
# tests/docs/test_conf.py
def test_conf_py_exists():
    import os
    assert os.path.exists("docs/conf.py"), "docs/conf.py should exist"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/docs/test_conf.py -v`
Expected: FAIL with "docs/conf.py should exist"

- [ ] **Step 3: Create docs/conf.py with Sphinx config**

```python
# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'omg-uml-xmi'
copyright = '2024, Calature Technologies'
author = 'Devin Hedge'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pyecore': ('https://pyecore.readthedocs.io/en/stable/', None),
}

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
```

- [ ] **Step 4: Create docs/requirements.txt**

```
sphinx>=7,<8
sphinx-rtd-theme>=2,<3
```

- [ ] **Step 5: Create docs/Makefile and docs/make.bat**

```makefile
# docs/Makefile
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help Makefile

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

```bat
@echo off
REM docs/make.bat
if "%1" == "" goto help
python -m sphinx %1 %2 %3 %4 %5 %6 %7 %8 %9
goto end

:help
python -m sphinx -M help . _build
:end
```

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest tests/docs/test_conf.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add docs/conf.py docs/requirements.txt docs/Makefile docs/make.bat tests/docs/test_conf.py
git commit -m "docs: add Sphinx conf.py, requirements, and build scripts"
```

---

### Task 2: Create index.rst and core documentation pages

**Files:**
- Create: `docs/index.rst`
- Create: `docs/installation.rst`
- Create: `docs/examples.rst`
- Create: `docs/changelog.rst`

**Interfaces:**
- Consumes: `docs/conf.py` (Task 1)
- Produces: Landing page, installation guide, examples placeholder, changelog link

- [ ] **Step 1: Write failing test for index.rst**

```python
# tests/docs/test_pages.py
def test_index_rst_exists():
    import os
    assert os.path.exists("docs/index.rst"), "docs/index.rst should exist"

def test_installation_rst_exists():
    import os
    assert os.path.exists("docs/installation.rst"), "docs/installation.rst should exist"

def test_examples_rst_exists():
    import os
    assert os.path.exists("docs/examples.rst"), "docs/examples.rst should exist"

def test_changelog_rst_exists():
    import os
    assert os.path.exists("docs/changelog.rst"), "docs/changelog.rst should exist"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/docs/test_pages.py -v`
Expected: FAIL with "should exist"

- [ ] **Step 3: Create docs/index.rst**

```rst
.. omg-uml-xmi documentation master file

Welcome to omg-uml-xmi's documentation!
========================================

**omg-uml-xmi** is a Python library for UML 2.5.1 / XMI 2.5.1 serialization,
filling the PyEcore gap for enterprise modeling.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   api
   examples
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

- [ ] **Step 4: Create docs/installation.rst**

```rst
Installation
============

Prerequisites
-------------

- Python 3.12+
- pip

Install from PyPI
-----------------

.. code-block:: bash

   pip install omg-uml-xmi

Install from Source
-------------------

.. code-block:: bash

   git clone https://github.com/Calature-Technologies-LLC/omg-uml-xmi
   cd omg-uml-xmi
   pip install -e .[dev]

Verify Installation
-------------------

.. code-block:: python

   import omg_uml_xmi
   print(omg_uml_xmi.__version__)
   # 0.1.0
```

- [ ] **Step 5: Create docs/examples.rst**

```rst
Examples
========

.. note::

   Examples are generated from the test suite. See the test files in
   `tests/` for usage patterns.

Basic Usage
-----------

.. code-block:: python

   from omg_uml_xmi import UMLXMIResource, UMLXMIReader
   from omg_uml_xmi.primitives import UMLPrimitiveType

   # Create a minimal UML model
   # ... (examples generated from test suite)
```

- [ ] **Step 6: Create docs/changelog.rst**

```rst
Changelog
=========

See `CHANGELOG.md <https://github.com/Calature-Technologies-LLC/omg-uml-xmi/blob/main/CHANGELOG.md>`_ for full changelog.

Current Version: 0.1.0
---------------------

Released: 2024-11-10

**Added**
- UML 2.5.1 / XMI 2.5.1 serialization for Python
- Primitive types: String, Integer, Boolean, Real, UnlimitedNatural
- Ecore ↔ UML model mapping
- XMI serialization/deserialization with UML 2.5.1 namespaces
- Primitive type mappings (Python ↔ UML)
```

- [ ] **Step 7: Run test to verify pages exist**

Run: `pytest tests/docs/test_pages.py -v`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add docs/index.rst docs/installation.rst docs/examples.rst docs/changelog.rst tests/docs/test_pages.py
git commit -m "docs: add index, installation, examples, changelog pages"
```

---

### Task 3: Create api.rst with auto-generated API reference

**Files:**
- Create: `docs/api.rst`

**Interfaces:**
- Consumes: `docs/conf.py` (Task 1)
- Produces: Auto-generated API reference for all public modules

- [ ] **Step 1: Write failing test for api.rst**

```python
# tests/docs/test_api.py
def test_api_rst_exists():
    import os
    assert os.path.exists("docs/api.rst"), "docs/api.rst should exist"

def test_api_rst_contains_automodule():
    with open("docs/api.rst") as f:
        content = f.read()
        assert ".. automodule:: omg_uml_xmi" in content
        assert ".. automodule:: omg_uml_xmi.primitives" in content
        assert ".. automodule:: omg_uml_xmi.mapper" in content
        assert ".. automodule:: omg_uml_xmi.serializer" in content
        assert ".. automodule:: omg_uml_xmi.writer" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/docs/test_api.py -v`
Expected: FAIL

- [ ] **Step 3: Create docs/api.rst with automodule directives**

```rst
API Reference
=============

.. toctree::
   :maxdepth: 3
   :caption: API Reference:

.. automodule:: omg_uml_xmi
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: omg_uml_xmi.primitives
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: omg_uml_xmi.mapper
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: omg_uml_xmi.serializer
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: omg_uml_xmi.writer
   :members:
   :undoc-members:
   :show-inheritance:
```

- [ ] **Step 4: Run test to verify automodule directives**

Run: `pytest tests/docs/test_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/api.rst tests/docs/test_api.py
git commit -m "docs: add API reference with automodule directives"
```

---

### Task 4: Create .readthedocs.yaml for ReadTheDocs deployment

**Files:**
- Create: `docs/.readthedocs.yaml`

**Interfaces:**
- Consumes: `docs/requirements.txt` (Task 1)
- Produces: ReadTheDocs configuration

- [ ] **Step 1: Write failing test for .readthedocs.yaml**

```python
# tests/docs/test_rtd.py
def test_readthedocs_yaml_exists():
    import os
    assert os.path.exists("docs/.readthedocs.yaml"), "docs/.readthedocs.yaml should exist"

def test_readthedocs_yaml_has_correct_config():
    import yaml
    with open("docs/.readthedocs.yaml") as f:
        config = yaml.safe_load(f)
    assert config.get("build", {}).get("os") == "ubuntu-22.04"
    assert config.get("build", {}).get("tools", {}).get("python") == "3.12"
    assert config.get("python", {}).get("install", {}).get("method") == "pip"
    assert "docs/requirements.txt" in config.get("python", {}).get("install", {}).get("requirements", [])
    assert config.get("formats", []) == ["htmlzip", "pdf"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/docs/test_rtd.py -v`
Expected: FAIL

- [ ] **Step 3: Create docs/.readthedocs.yaml**

```yaml
# docs/.readthedocs.yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
    requirements:
      - docs/requirements.txt

formats:
  - htmlzip
  - pdf

versions:
  - latest

build:
  jobs:
    post_create_environment:
      - pip install -e .[docs]

# Only build latest for v1 (semantic versioning ready for future)
```

- [ ] **Step 4: Run test to verify config**

Run: `pytest tests/docs/test_rtd.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/.readthedocs.yaml tests/docs/test_rtd.py
git commit -m "docs: add ReadTheDocs configuration"
```

---

### Task 5: Test local build and fix issues

**Files:**
- None new (uses all previous tasks)

**Interfaces:**
- Consumes: All previous tasks
- Produces: Verified local build

- [ ] **Step 1: Install docs dependencies**

```bash
pip install -e ".[docs]"
```

- [ ] **Step 2: Run local build**

```bash
cd docs && make html
```

- [ ] **Step 3: Verify build output**

```bash
ls -la docs/_build/html/index.html
# Should exist and be > 1KB
```

- [ ] **Step 4: Fix any build issues** (iterative)

Common fixes:
- Missing docstrings → add module-level docstrings
- Import errors → fix import paths in conf.py
- Missing modules → ensure all modules have `__init__.py` exports

- [ ] **Step 5: Commit any fixes**

```bash
git add -A
git commit -m "docs: fix local build issues"
```

---

### Task 6: Configure ReadTheDocs project and verify deployment

**Files:**
- None new (uses all previous tasks)

**Interfaces:**
- Consumes: All previous tasks
- Produces: Deployed documentation

- [ ] **Step 1: Create ReadTheDocs project**

Go to https://readthedocs.org/dashboard/import
- Connect GitHub account
- Select `Calature-Technologies-LLC/omg-uml-xmi`
- Project name: `omg-uml-xmi`
- Repository URL: `https://github.com/Calature-Technologies-LLC/omg-uml-xmi`

- [ ] **Step 2: Configure project settings**

- Default branch: `main`
- Default version: `latest`
- Python version: 3.12
- Requirements file: `docs/requirements.txt`
- Config file: `docs/.readthedocs.yaml`

- [ ] **Step 3: Trigger first build**

- Trigger build from ReadTheDocs dashboard
- Monitor build logs for errors

- [ ] **Step 4: Verify deployment**

```bash
curl -f https://omg-uml-xmi.readthedocs.io/en/latest/
# Should return 200 OK
```

- [ ] **Step 5: Commit final state**

```bash
git add -A
git commit -m "docs: complete documentation build with ReadTheDocs deployment"
```

---

## Execution Method

**Recommended: Subagent-driven** — 6 tasks with clear dependencies, each independently testable. Fresh reviewer per task ensures quality. Costs more context but catches integration issues early.

**Alternative: Native** — If you prefer single-session implementation with final review.

---

## Plan Review

**Spec Coverage Check:**
- ✅ Sphinx conf.py with extensions
- ✅ Auto-generated API via automodule
- ✅ ReadTheDocs config for latest + semantic versioning
- ✅ Local build scripts (Makefile, make.bat)
- ✅ Core pages: index, installation, examples, changelog, api
- ✅ RTD config with latest + semantic versioning
- ✅ Local build verification
- ✅ RTD deployment

**Gaps:** None found.

**Plan saved to:** `docs/superpowers/plans/2026-11-10-documentation-build-plan.md`

**Next:** Please review the plan. Does it capture what you want? Which execution approach: **Subagent-driven** (recommended) or **Native**?