# Distribution Test Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create distribution test that verifies the package can be built as a wheel/sdist and installed correctly in a clean environment.

**Architecture:** Test suite using pytest with temporary virtual environments to verify wheel/sdist build and installation. CI job for automated testing on release tags.

**Tech Stack:** pytest, build, virtualenv, pip; Python 3.12+

**Spec:** `docs/superpowers/specs/2026-11-10-distribution-test-design.md`

## Global Constraints

- Python 3.12+ (from pyproject.toml)
- Dependencies: `build`, `pytest`, `virtualenv` (for test isolation)
- CI job for automated testing on release tags
- Test isolation using temporary virtual environments

## Review Focus

1. **Missing build dependencies**: Ensure `build` package is available for wheel/sdist creation
2. **Virtual environment isolation**: Tests must not pollute the test runner's environment
3. **Wheel metadata validation**: Verify wheel contains correct metadata and files
4. **Version consistency**: Installed package version matches pyproject.toml
5. **Cleanup**: Temporary environments must be cleaned up after tests

---

### Task 1: Create test infrastructure for distribution testing

**Files:**
- Create: `tests/packaging/test_distribution.py`
- Create: `tests/packaging/conftest.py` (if needed)

**Interfaces:**
- Consumes: None (first task)
- Produces: Test fixtures for virtual environment management

- [ ] **Step 1: Write failing test for wheel build**

```python
# tests/packaging/test_distribution.py
def test_wheel_build_creates_valid_wheel():
    """Test that pip wheel creates a valid wheel file."""
    import subprocess
    import os
    import glob

    result = subprocess.run(["pip", "wheel", ".", "-w", "dist/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Wheel build failed: {result.stderr}"

    wheels = glob.glob("dist/omg_uml_xmi-*.whl")
    assert len(wheels) == 1, f"Expected 1 wheel, got {len(wheels)}"

    wheel_path = wheels[0]
    assert os.path.exists(wheel_path), "Wheel file should exist"
    assert wheel_path.endswith(".whl"), "Should be a .whl file"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/packaging/test_distribution.py::test_wheel_build_creates_valid_wheel -v`
Expected: FAIL (test not implemented)

- [ ] **Step 3: Add build dependency to pyproject.toml**

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8,<9",
    "pytest-asyncio>=0.23,<1",
    "ruff>=0.5,<1",
    "black>=24,<25",
    "mypy>=1.10,<2",
    "build>=1.0,<2",  # Add this
]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/packaging/test_distribution.py::test_wheel_build_creates_valid_wheel -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml tests/packaging/test_distribution.py
git commit -m "test: add wheel build test for distribution verification"
```

---

### Task 2: Add wheel installation test in clean virtual environment

**Files:**
- Create/Modify: `tests/packaging/test_distribution.py`

**Interfaces:**
- Consumes: Wheel build test (Task 1)
- Produces: Installation verification test

- [ ] **Step 1: Write failing test for wheel installation**

```python
def test_wheel_install_in_clean_env():
    """Test that wheel installs correctly in a clean virtual environment."""
    import subprocess
    import tempfile
    import os
    import glob
    import sys

    # Build wheel first
    result = subprocess.run(["pip", "wheel", ".", "-w", "dist/"], capture_output=True, text=True)
    assert result.returncode == 0

    wheels = glob.glob("dist/omg_uml_xmi-*.whl")
    assert len(wheels) == 1
    wheel_path = wheels[0]

    # Create temporary virtual environment
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = os.path.join(tmpdir, "venv")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        # Determine pip path
        if sys.platform == "win32":
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")

        # Install wheel in clean environment
        result = subprocess.run([pip_path, "install", wheel_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Install failed: {result.stderr}"

        # Verify import works
        result = subprocess.run([python_path, "-c", "import omg_uml_xmi; print(omg_uml_xmi.__version__)"], capture_output=True, text=True)
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "0.1.0" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/packaging/test_distribution.py::test_wheel_install_in_clean_env -v`
Expected: FAIL

- [ ] **Step 3: Implement and verify**

Run: `pytest tests/packaging/test_distribution.py::test_wheel_install_in_clean_env -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add tests/packaging/test_distribution.py
git commit -m "test: add wheel installation test in clean virtual environment"
```

---

### Task 3: Add sdist build and install test

**Files:**
- Create/Modify: `tests/packaging/test_distribution.py`

**Interfaces:**
- Consumes: Wheel build/install tests (Tasks 1-2)
- Produces: SDist build/install verification

- [ ] **Step 1: Write failing test for sdist build**

```python
def test_sdist_build_creates_valid_sdist():
    """Test that python -m build --sdist creates a valid sdist."""
    import subprocess
    import glob
    import os

    result = subprocess.run(["python", "-m", "build", "--sdist"], capture_output=True, text=True)
    assert result.returncode == 0, f"SDist build failed: {result.stderr}"

    sdists = glob.glob("dist/omg_uml_xmi-*.tar.gz")
    assert len(sdists) == 1, f"Expected 1 sdist, got {len(sdists)}"

    sdist_path = sdists[0]
    assert os.path.exists(sdist_path)
    assert sdist_path.endswith(".tar.gz")
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Add sdist install test**

```python
def test_sdist_install_in_clean_env():
    """Test that sdist installs correctly in a clean virtual environment."""
    import subprocess
    import tempfile
    import os
    import glob
    import sys

    # Build sdist
    result = subprocess.run(["python", "-m", "build", "--sdist"], capture_output=True, text=True)
    assert result.returncode == 0

    sdists = glob.glob("dist/omg_uml_xmi-*.tar.gz")
    assert len(sdists) == 1
    sdist_path = sdists[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = os.path.join(tmpdir, "venv")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        if sys.platform == "win32":
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")

        result = subprocess.run([pip_path, "install", sdist_path], capture_output=True, text=True)
        assert result.returncode == 0, f"SDist install failed: {result.stderr}"

        result = subprocess.run([python_path, "-c", "import omg_uml_xmi; print(omg_uml_xmi.__version__)"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "0.1.0" in result.stdout
```

- [ ] **Step 4: Run tests and verify**

Run: `pytest tests/packaging/test_distribution.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/packaging/test_distribution.py
git commit -m "test: add sdist build and install tests"
```

---

### Task 4: Add CI job for automated distribution testing

**Files:**
- Create: `.github/workflows/distribution-test.yml`

**Interfaces:**
- Consumes: All distribution tests (Tasks 1-3)
- Produces: Automated CI verification on release tags

- [ ] **Step 1: Write CI workflow**

```yaml
# .github/workflows/distribution-test.yml
name: Distribution Test

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  distribution-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -e .[dev]
      - name: Run distribution tests
        run: pytest tests/packaging/test_distribution.py -v
```

- [ ] **Step 2: Test workflow locally (act or manual)**

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/distribution-test.yml
git commit -m "ci: add distribution test workflow for release tags"
```

---

## Execution Method

**Recommended: Subagent-driven** — 4 tasks with clear linear dependencies, each independently testable. Fresh reviewer per task catches integration issues early.

**Alternative: Native** — Single-session implementation with final review.

---

## Plan Review

**Spec Coverage Check:**
- ✅ Wheel build test
- ✅ Wheel install test in clean env
- ✅ SDist build test
- ✅ SDist install test in clean env
- ✅ CI job for release tags

**Gaps:** None found.

**Plan saved to:** `docs/superpowers/plans/2026-11-10-distribution-test-plan.md`

**Next:** Please review the plan. Does it capture what you want? Which execution approach: **Subagent-driven** (recommended) or **Native**?