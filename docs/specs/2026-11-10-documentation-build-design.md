---
title: "Documentation Build Design — Sphinx + ReadTheDocs"
description: "Design for Sphinx documentation build with ReadTheDocs deployment"
doc_type: "design"
author: "Devin Hedge"
version: "1.0"
last_updated: "2026-11-10"
status: "approved"
category: "documentation"
tags: ["sphinx", "readthedocs", "documentation", "pypi-ready"]
related_issues: ["#1"]
---

# Documentation Build Design — Sphinx + ReadTheDocs

## Intent and Why

The `omg-uml-xmi` library has no documentation build. Users cannot find API documentation, installation guides, or usage examples. This blocks PyPI publication readiness.

**Goal**: Minimal Sphinx documentation build deployed to ReadTheDocs with auto-generated API reference from docstrings.

---

## Goals, Non-Goals, Anti-Goals

### Goals
- [ ] Sphinx `conf.py` with autodoc, napoleon, viewcode
- [ ] Auto-generated API reference from all public modules
- [ ] ReadTheDocs `.readthedocs.yaml` configuration
- [ ] Local build via `make docs` or `sphinx-build`
- [ ] ReadTheDocs project configured for `omg-uml-xmi.readthedocs.io`
- [ ] Builds `latest` version with semantic versioning

### Non-Goals (v1)
- Custom landing page with project overview/badges
- Custom sidebar structure beyond auto-generated
- Custom CSS/branding
- Version dropdown (only `latest` for v1)
- Custom CSS/logo

### Anti-Goals
- Manual API documentation writing
- Custom sidebar structure beyond auto-generated
- Diagram/layout support (UMLDI) - not in scope

---

## Constraints

| Constraint | Detail |
|------------|--------|
| Python | 3.12+ (pyproject.toml) |
| Dependencies | `sphinx>=7,<8`, `sphinx-rtd-theme>=2,<3` (already in `docs` extras) |
| Output URL | `https://omg-uml-xmi.readthedocs.io` (already in pyproject.toml) |
| Versioning | Semantic versioning, only `latest` for v1 |
| Examples | Generated from tests (auto-discovery) |

---

## Approaches Considered

### Approach 1: Minimal Sphinx + ReadTheDocs (Selected)
- **What**: Minimal Sphinx with autodoc, napoleon, viewcode; auto-generated API; RTD config
- **Trade-offs**: Fast, standard, auto-generates API, basic navigation, version later
- **Why**: Fastest to working docs, URL reserved, can enhance later

### Approach 2: Full-Featured Docs
- **What**: Custom landing page, custom sidebar, custom CSS, examples from tests
- **Trade-offs**: Professional, user-friendly, but 2-3 hours vs 30 min
- **Rejected**: Over-engineering for v1

### Approach 3: GitHub Pages instead of RTD
- **What**: Sphinx + GitHub Actions → GitHub Pages
- **Trade-offs**: No external dependency, but complex CI, no auto versioning
- **Rejected**: RTD is standard for Python, URL reserved

---

## Design Decisions

| Decision | Detail |
|----------|--------|
| Sphinx extensions | `autodoc`, `napoleon`, `viewcode`, `intersphinx` |
| Theme | `sphinx_rtd_theme` |
| API generation | `.. automodule::` with `:members:`, `:undoc-members:`, `:show-inheritance:` |
| Module discovery | Auto-discover all public modules in `src/omg_uml_xmi/` |
| Examples | Auto-discovered from `tests/` (later enhancement) |
| Versioning | Only `latest` for v1, semantic versioning ready |

---

## File Structure

```
docs/
├── Makefile
├── make.bat
├── conf.py
├── index.rst
├── api.rst
├── installation.rst
├── examples.rst
├── changelog.rst
├── requirements.txt
└── .readthedocs.yaml
```

---

## Implementation Plan

1. **Create `docs/` directory structure**
2. **Write `docs/conf.py`** with extensions, theme, autodoc config
3. **Write `docs/index.rst`** - main landing page with toctree
4. **Write `docs/api.rst`** - auto-generated API reference
5. **Write `docs/installation.rst`** - pip install instructions
6. **Write `docs/examples.rst`** - placeholder for test-generated examples
7. **Write `docs/changelog.rst`** - link to CHANGELOG.md
8. **Write `docs/conf.py`** - Sphinx config with extensions
9. **Write `docs/.readthedocs.yaml`** - RTD config
10. **Write `docs/Makefile` and `make.bat`** - local build
11. **Write `docs/requirements.txt`** - for RTD
12. **Test local build** with `make docs`
13. **Configure ReadTheDocs project** at readthedocs.org

---

## Acceptance Criteria

- [ ] `make docs` builds HTML in `docs/_build/html/`
- [ ] `sphinx-build -b html docs docs/_build/html` works
- [ ] `docs/_build/html/index.html` loads with navigation
- [ ] API reference shows all public modules/classes/functions
- [ ] ReadTheDocs builds `latest` successfully
- [ ] URL `https://omg-uml-xmi.readthedocs.io` serves docs

---

## Open Questions (Resolved)

1. **Custom landing page?** → No, auto-generated API sufficient for v1
2. **Specific modules to prioritize?** → All modules, no priority
4. **Examples from tests?** → Generate from tests (placeholder for now)
5. **Versioning?** → Just `latest` for v1, semantic versioning ready

---

## Approval

**Status**: Ready for implementation

**Next Step**: Invoke `superpowers:writing-plans` to create implementation plan, then execute.