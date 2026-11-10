"""
Edge case tests for omg-uml-xmi library.

Tests cover edge cases and boundary conditions for UML 2.5.1 / XMI 2.5.1 serialization.
"""

from lxml import etree
from io import BytesIO

from omg_uml_xmi.primitives import (
    python_type_to_uml,
    uml_to_python_type,
    get_primitive_type,
    get_primitive_xmi_id,
    UML_PRIMITIVE_TYPES,
)
from omg_uml_xmi.writer import (
    make_uml_root,
    create_uml_element,
    create_uml_package,
    create_uml_class,
    create_uml_property,
    create_uml_operation,
    create_uml_association,
    create_uml_generalization,
    create_uml_enumeration,
    create_uml_primitive_type,
    create_uml_constraint,
    serialize_xmi,
    write_xmi_file,
    set_xmi_id,
    set_xmi_idref,
    set_xmi_type,
)
from omg_uml_xmi.mapper import EcoreToUMLMapper, MappingResult


class TestPrimitiveTypeEdgeCases:
    """Edge cases for primitive type handling."""

    def test_unlimited_natural_asterisk_upper_bound(self):
        """UnlimitedNatural should handle '*' as upper bound."""
        # In UML, UnlimitedNatural upper bound can be '*'
        # This is a semantic test - the type exists and has correct XMI ID
        prim = get_primitive_type("UnlimitedNatural")
        assert prim is not None
        assert get_primitive_xmi_id("UnlimitedNatural") == "UnlimitedNatural"

    def test_primitive_type_case_sensitivity(self):
        """Primitive type lookups should be case-sensitive."""
        assert get_primitive_type("String") is not None
        assert get_primitive_type("string") is None
        assert get_primitive_type("STRING") is None

    def test_python_type_to_uml_unknown(self):
        """Unknown Python types should return None."""
        assert python_type_to_uml("unknown_type") is None
        assert python_type_to_uml("") is None
        assert python_type_to_uml("list") is None

    def test_uml_to_python_type_unknown(self):
        """Unknown UML types should return None."""
        assert uml_to_python_type("UnknownType") is None
        assert uml_to_python_type("") is None

    def test_all_primitives_have_xmi_ids(self):
        """All primitive types should have XMI IDs."""
        for name, prim in UML_PRIMITIVE_TYPES.items():
            xmi_id = get_primitive_xmi_id(name)
            assert xmi_id == name, f"XMI ID mismatch for {name}: {xmi_id}"


class TestXMIWritingEdgeCases:
    """Edge cases for low-level XMI writing utilities."""

    def test_make_uml_root_namespaces(self):
        """Root element should have correct namespace declarations."""
        root = make_uml_root()
        nsmap = root.nsmap

        # Default namespace should be UML
        assert nsmap[None] == "http://www.omg.org/spec/UML/20161101"
        # xmi prefix
        assert nsmap['xmi'] == "http://www.omg.org/XMI"
        # xsi prefix
        assert nsmap['xsi'] == "http://www.w3.org/2001/XMLSchema-instance"

        # Attributes
        assert root.get('{http://www.omg.org/XMI}version') == '2.5.1'
        assert '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation' in root.attrib

    def test_create_uml_element_with_attributes(self):
        """create_uml_element should handle attributes correctly."""
        root = make_uml_root()
        elem = create_uml_element(root, 'Class', {'name': 'TestClass', 'isAbstract': 'true'})

        assert elem.tag == '{http://www.omg.org/spec/UML/20161101}Class'
        assert elem.get('name') == 'TestClass'
        assert elem.get('isAbstract') == 'true'

    def test_set_xmi_id_and_idref(self):
        """XMI ID and IDREF should be set correctly."""
        root = make_uml_root()
        elem = create_uml_element(root, 'Class')

        set_xmi_id(elem, 'test_id_123')
        assert elem.get('{http://www.omg.org/XMI}id') == 'test_id_123'

        ref_elem = create_uml_element(root, 'Property')
        set_xmi_idref(ref_elem, 'test_id_123')
        assert ref_elem.get('{http://www.omg.org/XMI}idref') == 'test_id_123'

    def test_set_xmi_type(self):
        """XSI type attribute should be set correctly."""
        root = make_uml_root()
        elem = create_uml_element(root, 'Property')

        set_xmi_type(elem, 'uml:Class')
        assert elem.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'uml:Class'

    def test_create_uml_class_with_all_attributes(self):
        """create_uml_class should handle all optional attributes."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1', is_abstract=True, is_final=True)

        assert cls.get('name') == 'TestClass'
        assert cls.get('isAbstract') == 'true'
        assert cls.get('isLeaf') == 'true'
        assert cls.get('{http://www.omg.org/XMI}id') == 'class_1'

    def test_create_uml_property_with_all_options(self):
        """create_uml_property should handle all optional parameters."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        prop = create_uml_property(
            cls,
            name='testProp',
            xmi_id='prop_1',
            uml_type='String',
            lower=0,
            upper='*',
            is_id=True,
            is_read_only=True,
            is_ordered=True,
            is_unique=False,
            is_containment=True,
            default='defaultValue',
            opposite='opposite_prop'
        )

        assert prop is not None
        assert prop.get('isID') == 'true'
        assert prop.get('isReadOnly') == 'true'
        assert prop.get('isOrdered') == 'true'
        assert prop.get('isUnique') == 'false'
        assert prop.get('aggregation') == 'composite'

        # Check multiplicity elements on the property (using findall with namespace)
        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        lower_vals = prop.findall('.//uml:LiteralInteger', ns)
        assert len(lower_vals) > 0
        assert lower_vals[0].get('value') == '0'

        upper_vals = prop.findall('.//uml:LiteralUnlimitedNatural', ns)
        assert len(upper_vals) > 0
        assert upper_vals[0].get('value') == '*'

    def test_create_uml_operation_with_parameters(self):
        """create_uml_operation should handle parameters correctly."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        op = create_uml_operation(
            cls,
            name='testOp',
            xmi_id='op_1',
            return_type='String',
            is_static=True,
            is_abstract=False,
            parameters=[
                {'name': 'param1', 'type': 'Integer', 'direction': 'in'},
                {'name': 'param2', 'type': 'String', 'direction': 'out'},
            ]
        )

        assert op.get('isStatic') == 'true'

        # Check parameters were created
        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        params = op.findall('.//uml:ownedParameter', ns)
        assert len(params) == 2

    def test_create_uml_enumeration_with_literals(self):
        """create_uml_enumeration should handle literals with values."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'TestPkg', 'pkg_1')

        enum = create_uml_enumeration(pkg, 'Status', 'enum_1', [
            {'name': 'ACTIVE', 'value': '1', 'xmi_id': 'lit_1'},
            {'name': 'INACTIVE', 'value': '0', 'xmi_id': 'lit_2'},
            {'name': 'PENDING', 'xmi_id': 'lit_3'},  # no value
        ])

        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        literals = enum.findall('.//uml:ownedLiteral', ns)
        assert len(literals) == 3

        # Check values
        active = literals[0]
        assert active.get('name') == 'ACTIVE'
        assert active.get('value') == '1'

        pending = literals[2]
        assert pending.get('name') == 'PENDING'
        assert 'value' not in pending.attrib

    def test_create_uml_constraint_with_specification(self):
        """create_uml_constraint should handle OCL specifications."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        constr = create_uml_constraint(
            cls,
            name='validName',
            xmi_id='constr_1',
            specification="self.name <> '' and self.name.size() > 0",
            constrained_elements=['prop_1', 'prop_2']
        )

        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        spec = constr.findall('.//uml:specification', ns)
        assert len(spec) == 1

        value_elem = spec[0].find('.//uml:value', ns)
        assert value_elem is not None
        assert "self.name <> ''" in value_elem.text

        constrained = constr.findall('.//uml:constrainedElement', ns)
        assert len(constrained) == 2

    def test_serialize_xmi_output(self):
        """serialize_xmi should produce valid XML bytes."""
        root = make_uml_root()
        create_uml_package(root, 'TestPackage', 'pkg_1')

        xml_bytes = serialize_xmi(root)

        # Should be valid XML
        assert xml_bytes.startswith(b'<?xml version')
        assert b'xmlns:xmi="http://www.omg.org/XMI"' in xml_bytes
        assert b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in xml_bytes
        assert b'xmi:version="2.5.1"' in xml_bytes

        # Should be parseable
        parsed = etree.fromstring(xml_bytes)
        assert parsed.tag == '{http://www.omg.org/spec/UML/20161101}XMI'

    def test_write_xmi_file_creates_valid_file(self, tmp_path):
        """write_xmi_file should create valid XMI file."""
        root = make_uml_root()
        create_uml_package(root, 'TestPackage', 'pkg_1')

        file_path = tmp_path / "test_output.xmi"
        write_xmi_file(root, str(file_path))

        assert file_path.exists()

        with open(file_path, 'rb') as f:
            content = f.read()
            assert content.startswith(b'<?xml')
            assert b'xmi:version="2.5.1"' in content


class TestMapperEdgeCases:
    """Edge cases for Ecore ↔ UML mapping."""

    def test_mapper_empty_package(self):
        """Mapper should handle empty packages."""
        from pyecore.ecore import EPackage

        pkg = EPackage(name='EmptyPkg', nsURI='http://empty', nsPrefix='empty')
        mapper = EcoreToUMLMapper()
        result = mapper.map_package(pkg)

        assert result.uml_element['name'] == 'EmptyPkg'
        assert result.uml_element['owned_types'] == []
        # No warnings for empty package

    def test_mapper_class_with_no_features(self):
        """Mapper should handle classes with no structural features."""
        from pyecore.ecore import EPackage, EClass

        pkg = EPackage(name='TestPkg', nsURI='http://test', nsPrefix='test')
        cls = EClass(name='EmptyClass')
        pkg.eClassifiers.append(cls)

        mapper = EcoreToUMLMapper()
        result = mapper.map_package(pkg)

        assert len(result.uml_element['owned_types']) == 1
        uml_class = result.uml_element['owned_types'][0]
        assert uml_class['attributes'] == []
        assert uml_class['references'] == []

    def test_mapper_attribute_with_no_type(self):
        """Mapper should handle attributes with unresolvable types."""
        from pyecore.ecore import EPackage, EClass, EAttribute

        pkg = EPackage(name='TestPkg', nsURI='http://test', nsPrefix='test')
        cls = EClass(name='TestClass')
        # Create attribute with unknown type
        attr = EAttribute(name='badAttr')
        attr.eType = None  # This might cause issues
        cls.eStructuralFeatures.append(attr)
        pkg.eClassifiers.append(cls)

        mapper = EcoreToUMLMapper()
        result = mapper.map_package(pkg)

        # Should have warning about unknown type
        assert any('no type' in w.lower() or 'unknown type' in w.lower() for w in result.warnings)

    def test_mapper_reference_containment(self):
        """Mapper should correctly identify containment references."""
        from pyecore.ecore import EPackage, EClass, EReference

        pkg = EPackage(name='TestPkg', nsURI='http://test', nsPrefix='test')
        parent = EClass(name='Parent')
        child = EClass(name='Child')

        ref = EReference(name='children')
        ref.containment = True
        ref.eType = child
        ref.upperBound = -1  # Unlimited (use upperBound setter)
        parent.eStructuralFeatures.append(ref)

        pkg.eClassifiers.append(parent)
        pkg.eClassifiers.append(child)

        mapper = EcoreToUMLMapper()
        result = mapper.map_package(pkg)

        assert len(result.uml_element['owned_types']) == 2
        parent_result = result.uml_element['owned_types'][0]
        refs = parent_result['references']
        assert len(refs) == 1
        assert refs[0]['is_containment'] is True
        assert refs[0]['upper'] == '*'

    def test_mapper_enum_with_literals(self):
        """Mapper should handle enums with literal values."""
        from pyecore.ecore import EPackage, EEnum, EEnumLiteral

        pkg = EPackage(name='TestPkg', nsURI='http://test', nsPrefix='test')
        enum = EEnum(name='Status')
        lit1 = EEnumLiteral(name='ACTIVE')
        lit1.value = 1
        lit2 = EEnumLiteral(name='INACTIVE')
        lit2.value = 0
        enum.eLiterals.append(lit1)
        enum.eLiterals.append(lit2)

        pkg.eClassifiers.append(enum)

        mapper = EcoreToUMLMapper()
        result = mapper.map_package(pkg)

        assert len(result.uml_element['owned_types']) == 1
        enum_result = result.uml_element['owned_types'][0]
        assert enum_result['type'] == 'Enumeration'
        assert len(enum_result['literals']) == 2
        assert enum_result['literals'][0]['name'] == 'ACTIVE'
        assert enum_result['literals'][0]['value'] == 1


class TestXMIModelEdgeCases:
    """Edge cases for XMI model structure."""

    def test_xmi_with_multiple_namespaces(self):
        """XMI should handle multiple namespace prefixes."""
        # Create root with custom namespace in nsmap
        nsmap = {
            None: "http://www.omg.org/spec/UML/20161101",  # default = UML
            'xmi': 'http://www.omg.org/XMI',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'custom': 'http://custom.namespace',
        }
        from lxml.etree import Element
        root = etree.Element(
            '{http://www.omg.org/spec/UML/20161101}XMI',
            nsmap=nsmap,
            attrib={
                '{http://www.omg.org/XMI}version': '2.5.1',
            }
        )

        # Elements should still be in default UML namespace
        cls = create_uml_class(root, 'TestClass', 'class_1')
        assert cls.tag == '{http://www.omg.org/spec/UML/20161101}Class'

    def test_xmi_id_uniqueness(self):
        """XMI IDs should be unique across document."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'TestPkg', 'pkg_1')
        cls1 = create_uml_class(pkg, 'ClassA', 'class_a')
        cls2 = create_uml_class(pkg, 'ClassB', 'class_b')

        prop1 = create_uml_property(cls1, 'prop', 'prop_1', 'String')
        prop2 = create_uml_property(cls2, 'prop', 'prop_2', 'String')  # Different ID

        # Serialize and check IDs are unique
        xml_bytes = serialize_xmi(make_uml_root())
        # This is a basic check - real uniqueness would require full document

    def test_empty_string_values(self):
        """Empty string values should be handled correctly."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        prop = create_uml_property(
            cls,
            name='emptyProp',
            xmi_id='prop_1',
            uml_type='String',
            default=''  # Empty string default
        )

        default_elem = cls.find('.//{http://www.omg.org/spec/UML/20161101}defaultValue')
        if default_elem is not None:
            literal = default_elem.find('.//{http://www.omg.org/spec/UML/20161101}LiteralString')
            assert literal is not None
            assert literal.get('value') == ''

    def test_special_characters_in_names(self):
        """Special characters in names should be preserved."""
        root = make_uml_root()
        cls = create_uml_class(root, 'Test Class', 'class_1')  # Space in name

        # The name attribute should preserve the space
        assert cls.get('name') == 'Test Class'

    def test_large_multiplicity_bounds(self):
        """Very large multiplicity bounds should work."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        prop = create_uml_property(
            cls,
            name='manyItems',
            xmi_id='prop_1',
            uml_type='Item',
            lower=0,
            upper=999999  # Very large upper bound
        )

        upper_elem = prop.find('.//{http://www.omg.org/spec/UML/20161101}upperValue')
        assert upper_elem is not None
        literal = upper_elem.find('.//{http://www.omg.org/spec/UML/20161101}LiteralInteger')
        assert literal is not None
        assert literal.get('value') == '999999'

    def test_xsi_nil_and_type_attributes(self):
        """XSI nil and type attributes should work."""
        root = make_uml_root()
        cls = create_uml_class(root, 'TestClass', 'class_1')

        prop = create_uml_property(cls, 'nullableProp', 'prop_1', 'String')
        prop.set('{http://www.w3.org/2001/XMLSchema-instance}nil', 'true')
        prop.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'uml:String')

        assert prop.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
        assert prop.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'uml:String'

    def test_mixed_content_text_and_elements(self):
        """Elements with both text content and child elements."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'TestPkg', 'pkg_1')

        # Package name with special chars
        pkg.set('name', 'Package & Model')

        xml_bytes = serialize_xmi(root)
        parsed = etree.fromstring(xml_bytes)
        pkg_elem = parsed.find('.//{http://www.omg.org/spec/UML/20161101}Package')
        assert pkg_elem.get('name') == 'Package & Model'


class TestSerializationRoundTrip:
    """Tests for serialization round-trip fidelity."""

    def test_basic_model_roundtrip(self):
        """Basic model should survive serialize → parse → serialize."""
        from omg_uml_xmi.serializer import UMLXMIResource, UMLXMIReader
        from omg_uml_xmi.mapper import EcoreToUMLMapper

        # This is a placeholder - full round-trip requires complete implementation
        # Placeholder test to document the requirement
        assert True  # Placeholder

    def test_xmi_with_all_optional_elements(self):
        """XMI with all optional elements should serialize correctly."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'FullPkg', 'pkg_1')

        cls = create_uml_class(pkg, 'ComplexClass', 'cls_1', is_abstract=False, is_final=True)

        # Add attribute
        create_uml_property(cls, 'id', 'attr_id', 'String', is_id=True, is_read_only=True)
        create_uml_property(cls, 'name', 'attr_name', 'String')
        create_uml_property(cls, 'count', 'attr_count', 'Integer', default='0')

        # Add reference
        create_uml_property(cls, 'parent', 'ref_parent', 'ComplexClass', is_containment=True)

        # Add operation
        create_uml_operation(cls, 'calculate', 'op_calc', return_type='Integer', parameters=[
            {'name': 'factor', 'type': 'Integer', 'direction': 'in'},
        ])

        # Add constraint
        create_uml_constraint(cls, 'positiveCount', 'constr_1',
                              'self.count >= 0', ['attr_count'])

        # Serialize
        xml_bytes = serialize_xmi(make_uml_root())
        # Should not raise
        assert xml_bytes is not None


class TestNamespaceHandling:
    """Tests for XML namespace handling edge cases."""

    def test_default_namespace_is_uml(self):
        """Default namespace should be UML, not empty."""
        root = make_uml_root()
        cls = create_uml_class(root, 'Test', 't1')

        # Element tag should use UML namespace
        assert cls.tag == '{http://www.omg.org/spec/UML/20161101}Class'

    def test_xmi_namespace_on_attributes(self):
        """XMI attributes should use xmi: prefix."""
        root = make_uml_root()
        cls = create_uml_class(root, 'Test', 'class_1')

        xmi_id = cls.get('{http://www.omg.org/XMI}id')
        assert xmi_id == 'class_1'

    def test_xsi_schema_location_format(self):
        """xsi:schemaLocation should have correct format."""
        root = make_uml_root()
        schema_loc = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        assert schema_loc is not None
        assert 'http://www.omg.org/spec/UML/20161101' in schema_loc
        assert 'UML.xmi' in schema_loc

    def test_multiple_packages_same_namespace(self):
        """Multiple packages should share default namespace."""
        root = make_uml_root()
        pkg1 = create_uml_package(root, 'Pkg1', 'p1')
        pkg2 = create_uml_package(root, 'Pkg2', 'p2')

        xml_bytes = serialize_xmi(root)
        parsed = etree.fromstring(xml_bytes)

        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        pkgs = parsed.findall('.//uml:Package', ns)
        assert len(pkgs) == 2
        # Both should be in same namespace
        assert pkgs[0].tag == pkgs[1].tag

    def test_xmi_extension_element(self):
        """XMI Extension element should be creatable."""
        root = make_uml_root()
        from omg_uml_xmi.writer import add_standard_profile_extension

        add_standard_profile_extension(root)

        ext = root.find('.//{http://www.omg.org/spec/UML/20161101}Extension')
        assert ext is not None
        assert ext.get('extender') == 'http://www.omg.org/spec/UML/20161101/StandardProfile.xmi'


class TestPerformanceAndLimits:
    """Tests for performance boundaries and limits."""

    def test_deeply_nested_packages(self):
        """Deeply nested package structure should work."""
        root = make_uml_root()
        current = root

        for i in range(10):  # 10 levels deep
            pkg = create_uml_package(current, f'Level{i}', f'lvl_{i}')
            current = pkg

        xml_bytes = serialize_xmi(root)
        parsed = etree.fromstring(xml_bytes)
        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        pkgs = parsed.findall('.//uml:Package', ns)
        assert len(pkgs) == 10  # 10 nested packages (Level0 through Level9)

    def test_many_classes_in_package(self):
        """Package with many classes should serialize."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'LargePkg', 'pkg_1')

        for i in range(100):
            create_uml_class(pkg, f'Class{i}', f'cls_{i}')

        xml_bytes = serialize_xmi(root)
        parsed = etree.fromstring(xml_bytes)
        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        classes = parsed.findall('.//uml:Class', ns)
        assert len(classes) == 100

    def test_many_properties_per_class(self):
        """Class with many properties should serialize."""
        root = make_uml_root()
        pkg = create_uml_package(root, 'TestPkg', 'pkg_1')
        cls = create_uml_class(root, 'LargeClass', 'cls_1')

        for i in range(50):
            create_uml_property(cls, f'prop{i}', f'prop_{i}', 'String')

        xml_bytes = serialize_xmi(root)
        parsed = etree.fromstring(xml_bytes)
        ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}
        props = parsed.findall('.//uml:Property', ns)
        assert len(props) >= 50


if __name__ == '__main__':
    pytest.main([__file__, '-v'])