"""
omg-uml-xmi: UML 2.5.1 / XMI 2.5.1 serializer for Python.

Fills the PyEcore gap for enterprise modeling by providing
UML 2.5.1 / XMI 2.5.1 serialization and deserialization.
"""

from omg_uml_xmi.mapper import EcoreToUMLMapper, UMLToEcoreMapper
from omg_uml_xmi.primitives import UML_PRIMITIVE_TYPES, get_primitive_type
from omg_uml_xmi.serializer import UMLXMIReader, UMLXMIResource

__version__ = "0.1.0"
__all__ = [
    "UMLXMIResource",
    "UMLXMIReader",
    "UML_PRIMITIVE_TYPES",
    "get_primitive_type",
    "EcoreToUMLMapper",
    "UMLToEcoreMapper",
    "UML_NAMESPACE",
    "XMI_NAMESPACE",
    "XMI_VERSION",
]

# UML 2.5.1 / XMI 2.5.1 namespace constants
UML_NAMESPACE = "http://www.omg.org/spec/UML/20161101"
XMI_NAMESPACE = "http://www.omg.org/XMI"
XMI_VERSION = "2.5.1"
