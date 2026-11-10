Contributing
============

Thank you for your interest in contributing to ``omg-uml-xmi``! This guide covers the development workflow, coding standards, and contribution process.

Development Setup
-----------------

Clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/calaturetech/omg-uml-xmi
   cd omg-uml-xmi
   pip install -e .[dev]

This installs the package with all development dependencies:
- ``pytest`` - Testing framework
- ``pytest-asyncio`` - Async test support
- ``ruff`` - Linting and formatting
- ``black`` - Code formatting
- ``mypy`` - Static type checking
- ``sphinx`` - Documentation building
- ``sphinx-rtd-theme`` - Documentation theme


Running Tests
-------------

Run the full test suite:

.. code-block:: bash

   pytest

Run with coverage:

.. code-block:: bash

   pytest --cov=src/omg_uml_xmi --cov-report=term-missing

Run a specific test file:

.. code-block:: bash

   pytest tests/test_primitives.py -v

Run tests matching a pattern:

.. code-block:: bash

   pytest -k "primitive" -v


Code Quality
------------

Format code with Black:

.. code-block:: bash

   black .

Check formatting without changes:

.. code-block:: bash

   black --check .

Lint with Ruff:

.. code-block:: bash

   ruff check .

Auto-fix linting issues:

.. code-block:: bash

   ruff check --fix .

Type check with MyPy:

.. code-block:: bash

   mypy src/


Pre-commit Hooks
----------------

Install pre-commit hooks to automatically run checks on commit:

.. code-block:: bash

   pip install pre-commit
   pre-commit install

The hooks will run ``black``, ``ruff``, and ``mypy`` on staged files before each commit.


Building Documentation
----------------------

Build HTML documentation:

.. code-block:: bash

   cd docs
   sphinx-build -b html . _build/html

Or use the Makefile:

.. code-block:: bash

   cd docs
   make html

View the built documentation:

.. code-block:: bash

   open docs/_build/html/index.html


Pull Request Process
--------------------

1. **Create a feature branch** from ``main``:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** following the coding standards below.

3. **Write tests** for new functionality. All new code must have test coverage.

4. **Run the full test suite and quality checks**:

   .. code-block:: bash

      pytest
      black --check .
      ruff check .
      mypy src/

5. **Build documentation** to ensure it renders correctly:

   .. code-block:: bash

      cd docs && make html

6. **Commit your changes** with a clear message:

   .. code-block:: bash

      git add .
      git commit -m "feat: add support for XMI extension elements"

   Use conventional commit format:
   - ``feat:`` - New feature
   - ``fix:`` - Bug fix
   - ``docs:`` - Documentation changes
   - ``test:`` - Test additions/changes
   - ``refactor:`` - Code refactoring
   - ``chore:`` - Maintenance tasks

7. **Push and create a Pull Request**:

   .. code-block:: bash

      git push origin feature/your-feature-name

   Then open a PR on GitHub with a clear description of the changes.


Coding Standards
----------------

Python Version
~~~~~~~~~~~~~~

- Target Python 3.12+ (as specified in ``pyproject.toml``)
- Use modern Python features (type hints, match statements, etc.)


Type Hints
~~~~~~~~~~

- All public functions and methods must have type hints
- Use ``from __future__ import annotations`` for forward references
- Prefer ``list[str]`` over ``List[str]`` (Python 3.9+)


Docstrings
~~~~~~~~~~

Use Google-style docstrings (compatible with Napoleon):

.. code-block:: python

   def serialize_model(model: EPackage, output: io.StringIO) -> str:
       """Serialize a UML model to XMI 2.5.1.

       Args:
           model: The PyEcore EPackage to serialize.
           output: StringIO buffer to write the XML output.

       Returns:
           The serialized XMI as a string.

       Raises:
           SerializationError: If the model cannot be serialized.
       """
       ...


Naming Conventions
~~~~~~~~~~~~~~~~~~

- Classes: ``PascalCase`` (e.g., ``UMLXMIResource``)
- Functions/methods: ``snake_case`` (e.g., ``read_from_file``)
- Constants: ``UPPER_SNAKE_CASE`` (e.g., ``UML_NAMESPACE``)
- Private: leading underscore (e.g., ``_internal_method``)


Error Handling
~~~~~~~~~~~~~~

- Use custom exceptions from ``omg_uml_xmi.errors``
- Don't use bare ``except:`` - always specify exception types
- Include context in error messages


Testing Standards
-----------------

- Write tests in ``tests/`` mirroring the source structure
- Use descriptive test names: ``test_<what>_<expected_behavior>``
- One assertion per test when possible
- Use fixtures for common setup
- Mock external dependencies


Test Structure
~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from omg_uml_xmi import UMLXMIReader

   class TestUMLXMIReader:
       """Tests for UMLXMIReader."""

       def test_read_from_file_returns_package(self):
           """read_from_file should return an EPackage."""
           reader = UMLXMIReader()
           model = reader.read_from_file("tests/fixtures/simple.uml.xmi")
           assert isinstance(model, EPackage)

       def test_read_from_file_raises_on_missing(self):
           """read_from_file should raise FileNotFoundError for missing file."""
           reader = UMLXMIReader()
           with pytest.raises(FileNotFoundError):
               reader.read_from_file("nonexistent.uml.xmi")


Release Process
---------------

Releases are managed by maintainers:

1. Update version in ``pyproject.toml`` and ``src/omg_uml_xmi/__init__.py``
2. Update ``CHANGELOG.md``
3. Create a Git tag: ``git tag v0.x.y``
4. Push tag: ``git push origin v0.x.y``
5. GitHub Actions builds and publishes to PyPI


Code of Conduct
---------------

This project follows the `Contributor Covenant <https://www.contributor-covenant.org/>`_ Code of Conduct. By participating, you agree to uphold this code.

Report unacceptable behavior to opensource@calature.com.


Getting Help
------------

- Open an issue on GitHub for bugs or feature requests
- Check existing issues and discussions before opening new ones
- For questions, use GitHub Discussions


License
-------

By contributing, you agree that your contributions will be licensed under the BSD-3-Clause license (same as the project).