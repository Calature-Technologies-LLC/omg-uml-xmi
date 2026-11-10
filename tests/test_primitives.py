"""
Tests for UML 2.5.1 primitive types.
"""

from omg_uml_xmi.primitives import (
    UML_PRIMITIVE_TYPES,
    get_primitive_type,
    python_type_to_uml,
    uml_to_python_type,
    get_all_primitive_types,
    get_primitive_xmi_id,
)


class TestUMLPrimitiveTypes:
    """Tests for UML primitive type definitions."""

    def test_all_primitives_defined(self):
        """All five UML 2.5.1 primitive types should be defined."""
        assert len(UML_PRIMITIVE_TYPES) == 5
        assert "String" in UML_PRIMITIVE_TYPES
        assert "Integer" in UML_PRIMITIVE_TYPES
        assert "Boolean" in UML_PRIMITIVE_TYPES
        assert "Real" in UML_PRIMITIVE_TYPES
        assert "UnlimitedNatural" in UML_PRIMITIVE_TYPES

    def test_primitive_type_structure(self):
        """Each primitive type should have correct structure."""
        string_type = UML_PRIMITIVE_TYPES["String"]
        assert string_type.name == "String"
        assert string_type.xmi_id == "String"
        assert string_type.uml_type == "String"

    def test_get_primitive_type(self):
        """get_primitive_type should return correct type."""
        result = get_primitive_type("String")
        assert result is not None
        assert result.name == "String"

        result = get_primitive_type("NonExistent")
        assert result is None

    def test_python_type_to_uml(self):
        """Python type to UML primitive mapping."""
        assert python_type_to_uml("str") == "String"
        assert python_type_to_uml("int") == "Integer"
        assert python_type_to_uml("bool") == "Boolean"
        assert python_type_to_uml("float") == "Real"
        assert python_type_to_uml("EString") == "String"
        assert python_type_to_uml("EInt") == "Integer"
        assert python_type_to_uml("EBoolean") == "Boolean"
        assert python_type_to_uml("EDouble") == "Real"
        assert python_type_to_uml("EBigInteger") == "UnlimitedNatural"
        assert python_type_to_uml("unknown") is None

    def test_uml_to_python_type(self):
        """UML primitive to Python type mapping."""
        assert uml_to_python_type("String") == "str"
        assert uml_to_python_type("Integer") == "int"
        assert uml_to_python_type("Boolean") == "bool"
        assert uml_to_python_type("Real") == "float"
        assert uml_to_python_type("UnlimitedNatural") == "int"
        assert uml_to_python_type("unknown") is None

    def test_get_all_primitive_types(self):
        """get_all_primitive_types should return all types."""
        all_types = get_all_primitive_types()
        assert len(all_types) == 5
        names = {t.name for t in all_types}
        assert names == {"String", "Integer", "Boolean", "Real", "UnlimitedNatural"}

    def test_get_primitive_xmi_id(self):
        """get_primitive_xmi_id should return correct XMI IDs."""
        assert get_primitive_xmi_id("String") == "String"
        assert get_primitive_xmi_id("Integer") == "Integer"
        assert get_primitive_xmi_id("Boolean") == "Boolean"
        assert get_primitive_xmi_id("Real") == "Real"
        assert get_primitive_xmi_id("UnlimitedNatural") == "UnlimitedNatural"
        assert get_primitive_xmi_id("unknown") is None
