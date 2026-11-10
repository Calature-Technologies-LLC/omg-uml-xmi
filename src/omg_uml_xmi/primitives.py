"""
UML 2.5.1 Primitive Types from OMG specification.

Based on UML 2.5.1 PrimitiveTypes.xmi (ptc/18-01-02)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UMLPrimitiveType:
    """Represents a UML 2.5.1 primitive type."""

    name: str
    xmi_id: str
    uml_type: str  # The UML type name (e.g., "String", "Integer")


# UML 2.5.1 Primitive Types from OMG specification
UML_PRIMITIVE_TYPES: dict[str, UMLPrimitiveType] = {
    "String": UMLPrimitiveType(
        name="String",
        xmi_id="String",
        uml_type="String",
    ),
    "Integer": UMLPrimitiveType(
        name="Integer",
        xmi_id="Integer",
        uml_type="Integer",
    ),
    "Boolean": UMLPrimitiveType(
        name="Boolean",
        xmi_id="Boolean",
        uml_type="Boolean",
    ),
    "Real": UMLPrimitiveType(
        name="Real",
        xmi_id="Real",
        uml_type="Real",
    ),
    "UnlimitedNatural": UMLPrimitiveType(
        name="UnlimitedNatural",
        xmi_id="UnlimitedNatural",
        uml_type="UnlimitedNatural",
    ),
}


# Mapping from Python/PyEcore types to UML primitive types
PYTHON_TO_UML_PRIMITIVE: dict[str, str] = {
    "str": "String",
    "int": "Integer",
    "bool": "Boolean",
    "float": "Real",
    "EString": "String",
    "EInt": "Integer",
    "EBoolean": "Boolean",
    "EDouble": "Real",
    "EBigInteger": "UnlimitedNatural",
}


# Mapping from UML primitive to Python type hints
UML_TO_PYTHON_TYPE: dict[str, str] = {
    "String": "str",
    "Integer": "int",
    "Boolean": "bool",
    "Real": "float",
    "UnlimitedNatural": "int",
}


def get_primitive_type(name: str) -> UMLPrimitiveType | None:
    """
    Get UML primitive type by name.

    Args:
        name: The primitive type name (e.g., "String", "Integer")

    Returns:
        UMLPrimitiveType if found, None otherwise
    """
    return UML_PRIMITIVE_TYPES.get(name)


def python_type_to_uml(python_type: str) -> str | None:
    """
    Convert Python/PyEcore type name to UML primitive type name.

    Args:
        python_type: Python type name (e.g., "str", "EString", "int")

    Returns:
        UML primitive type name if found, None otherwise
    """
    return PYTHON_TO_UML_PRIMITIVE.get(python_type)


def uml_to_python_type(uml_type: str) -> str | None:
    """
    Convert UML primitive type name to Python type hint.

    Args:
        uml_type: UML primitive type name (e.g., "String", "Integer")

    Returns:
        Python type hint if found, None otherwise
    """
    return UML_TO_PYTHON_TYPE.get(uml_type)


def get_all_primitive_types() -> list[UMLPrimitiveType]:
    """Get all UML primitive types as a list."""
    return list(UML_PRIMITIVE_TYPES.values())


# XMI IDs for primitive types (from OMG UML 2.5.1 PrimitiveTypes.xmi)
PRIMITIVE_TYPE_XMI_IDS: dict[str, str] = {
    "String": "String",
    "Integer": "Integer",
    "Boolean": "Boolean",
    "Real": "Real",
    "UnlimitedNatural": "UnlimitedNatural",
}


def get_primitive_xmi_id(uml_type: str) -> str | None:
    """Get the XMI ID for a UML primitive type."""
    return PRIMITIVE_TYPE_XMI_IDS.get(uml_type)
