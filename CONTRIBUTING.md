# Contributing to omg-uml-xmi

Thank you for your interest in contributing! This project aims to fill the PyEcore gap for UML 2.5.1 / XMI 2.5.1 support in Python.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold this code.

## How to Contribute

### Reporting Issues

- Check existing issues first to avoid duplicates
- Use the issue templates when available
- Provide clear reproduction steps, expected vs actual behavior
- Include Python version, OS, and relevant dependency versions

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Make your changes with tests
4. Run the full test suite: `pytest`
5. Run linters: `ruff check . && black --check . && mypy src/`
6. Submit PR with clear description of changes

### Development Setup

```bash
git clone https://github.com/calaturetech/omg-uml-xmi
cd omg-uml-xmi
pip install -e .[dev]
pre-commit install  # optional but recommended
```

### Code Style

- **Formatter**: Black (line length 100)
- **Linter**: Ruff (with extended rules)
- **Type checker**: MyPy (strict mode)
- **Tests**: pytest with asyncio support

Run all checks:
```bash
pytest
ruff check .
black --check .
mypy src/
```

## Project Structure

```
src/omg_uml_xmi/
├── __init__.py           # Public API exports
├── primitives.py         # UML 2.5.1 primitive types
├── mapper.py             # Ecore ↔ UML model mapping
├── serializer.py         # XMI serialization (UMLXMIResource, UMLXMIReader)
└── writer.py             # Low-level XML writing utilities

tests/
├── test_primitives.py
├── test_mapper.py
├── test_serializer.py
├── test_roundtrip.py
└── fixtures/             # Test XMI files
```

## Adding New UML Elements

When adding support for new UML elements:

1. Add the element mapping in `mapper.py` (EcoreToUMLMapper / UMLToEcoreMapper)
2. Add serialization logic in `serializer.py` / `writer.py`
3. Add primitive type if needed in `primitives.py`
3. Add tests in `tests/test_mapper.py` and `tests/test_serializer.py`
4. Add round-trip test in `tests/test_roundtrip.py`
4. Update the scope table in README.md

## Testing Guidelines

- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test serializer + mapper together
- **Round-trip tests**: Read → modify → write → verify equivalence
- **Fixture tests**: Validate against real OMG UML XMI files

## Scope Boundaries

This library intentionally does **not** support (yet):

- UML Diagram Interchange (UMLDI)
- Profiles and Stereotypes
- Diagram layout/visual information
- Non-UML MOF metamodels

These are planned for future versions. Please discuss scope changes in an issue before implementing.

## License

By contributing, you agree that your contributions will be licensed under the [BSD-3-Clause License](LICENSE).

## Questions?

Open a [Discussion](https://github.com/calaturetech/omg-uml-xmi/discussions) or [Issue](https://github.com/calaturetech/omg-uml-xmi/issues).