# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-10

### Added
- UML 2.5.1 / XMI 2.5.1 serialization for Python
- Primitive types: String, Integer, Boolean, Real, UnlimitedNatural
- Ecore ↔ UML model mapping (EcoreToUMLMapper, UMLToEcoreMapper)
- XMI serialization/deserialization with UML 2.5.1 namespaces
- Primitive type mappings (Python ↔ UML)
- UML 2.5.1 / XMI 2.5.1 serializer for Python
- Minimal Sphinx documentation with ReadTheDocs deployment
- Distribution test for wheel/sdist build and install verification
- CI workflow for distribution test on release tags
- Complete PyPI metadata (classifiers, project URLs, keywords)
- CHANGELOG.md following Keep a Changelog format

### Fixed
- Fixed autosummary errors in Sphinx build by removing scope creep

### Security
- No security issues in this release