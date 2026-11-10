"""
Ecore ↔ UML model mapping.

Maps between PyEcore Ecore metamodel and UML 2.5.1 metamodel.
"""

from dataclasses import dataclass

from pyecore.ecore import EClass, EEnum, EEnumLiteral, EPackage

from omg_uml_xmi.primitives import (
    python_type_to_uml,
)


@dataclass(frozen=True)
class MappingResult:
    """Result of a mapping operation."""

    uml_element: object
    warnings: list[str]


class EcoreToUMLMapper:
    """Maps PyEcore Ecore models to UML 2.5.1 elements."""

    # Ecore to UML metaclass mapping
    ECORE_TO_UML_METACLASS = {
        "EPackage": "Package",
        "EClass": "Class",
        "EAttribute": "Property",
        "EReference": "Property",
        "EEnum": "Enumeration",
        "EEnumLiteral": "EnumerationLiteral",
        "EDataType": "PrimitiveType",
    }

    def __init__(self):
        self._uml_factory = None  # Will be initialized lazily

    def map_package(self, ecore_package) -> MappingResult:
        """Map an EPackage to a UML Package."""
        warnings = []

        # In a full implementation, this would create UML Package element
        # with proper UML namespace, visibility, etc.
        uml_package = {
            "type": "Package",
            "name": ecore_package.name,
            "namespace_uri": ecore_package.nsURI,
            "namespace_prefix": ecore_package.nsPrefix,
            "owned_types": [],
            "xmi_id": f"{ecore_package.name}_package",
        }

        # Map owned classifiers
        for classifier in ecore_package.eClassifiers:
            if classifier.eClass.name == "EClass":
                class_result = self.map_class(classifier)
                if class_result.uml_element:
                    uml_package["owned_types"].append(class_result.uml_element)
                warnings.extend(class_result.warnings)
            elif classifier.eClass.name == "EEnum":
                enum_result = self.map_enum(classifier)
                if enum_result.uml_element:
                    uml_package["owned_types"].append(enum_result.uml_element)
                warnings.extend(enum_result.warnings)
            elif classifier.eClass.name == "EDataType":
                # Primitive types handled separately
                pass

        return MappingResult(uml_element=uml_package, warnings=warnings)

    def map_class(self, ecore_class) -> MappingResult:
        """Map an EClass to a UML Class."""
        warnings = []

        uml_class = {
            "type": "Class",
            "name": ecore_class.name,
            "is_abstract": ecore_class.abstract,
            "is_final": getattr(ecore_class, 'leaf', False),
            "attributes": [],
            "references": [],
            "xmi_id": f"{ecore_class.name}_class",
        }

        # Map structural features
        for feature in ecore_class.eStructuralFeatures:
            if feature.eClass.name == "EAttribute":
                attr_result = self.map_attribute(feature)
                if attr_result.uml_element:
                    uml_class["attributes"].append(attr_result.uml_element)
                warnings.extend(attr_result.warnings)
            elif feature.eClass.name == "EReference":
                ref_result = self.map_reference(feature)
                if ref_result.uml_element:
                    uml_class["references"].append(ref_result.uml_element)
                warnings.extend(ref_result.warnings)

        return MappingResult(uml_element=uml_class, warnings=warnings)

    def map_attribute(self, ecore_attr) -> MappingResult:
        """Map an EAttribute to a UML Property (attribute)."""
        warnings: list[str] = []

        if ecore_attr.eType is None:
            warnings.append(
                f"Attribute {ecore_attr.name} has no type, defaulting to String"
            )
            uml_type = "String"
        else:
            uml_type = python_type_to_uml(ecore_attr.eType.name)
            if not uml_type:
                warnings.append(
                    f"Unknown type {ecore_attr.eType.name} for attribute {ecore_attr.name}, defaulting to String"
                )
                uml_type = "String"

        uml_property = {
            "type": "Property",
            "name": ecore_attr.name,
            "type": uml_type,
            "is_id": getattr(ecore_attr, "is_id", False),
            "is_read_only": getattr(ecore_attr, "is_read_only", False),
            "lower": ecore_attr.lower,
            "upper": ecore_attr.upper if ecore_attr.upper != -1 else "*",
            "default": getattr(ecore_attr, "default", None),
            "xmi_id": f"{ecore_attr.name}_attr",
        }

        return MappingResult(uml_element=uml_property, warnings=warnings)

    def map_reference(self, ecore_ref) -> MappingResult:
        """Map an EReference to a UML Property (association end)."""
        warnings: list[str] = []

        uml_property = {
            "type": "Property",
            "name": ecore_ref.name,
            "type": ecore_ref.eType.name,  # Reference to another class
            "is_containment": ecore_ref.containment,
            "lower": ecore_ref.lower,
            "upper": ecore_ref.upper if ecore_ref.upper != -1 else "*",
            "opposite": ecore_ref.eOpposite.name if ecore_ref.eOpposite else None,
            "xmi_id": f"{ecore_ref.name}_ref",
        }

        return MappingResult(uml_element=uml_property, warnings=warnings)

    def map_enum(self, ecore_enum) -> MappingResult:
        """Map an EEnum to a UML Enumeration."""
        warnings: list[str] = []

        literals = []
        for literal in ecore_enum.eLiterals:
            literals.append(
                {
                    "type": "EnumerationLiteral",
                    "name": literal.name,
                    "value": literal.value,
                    "xmi_id": f"{literal.name}_lit",
                }
            )

        uml_enum = {
            "type": "Enumeration",
            "name": ecore_enum.name,
            "literals": literals,
            "xmi_id": f"{ecore_enum.name}_enum",
        }

        return MappingResult(uml_element=uml_enum, warnings=warnings)


class UMLToEcoreMapper:
    """Maps UML 2.5.1 elements to PyEcore Ecore models."""

    def __init__(self):
        pass  # PyEcore uses direct class instantiation

    def map_package(self, uml_package) -> EPackage:
        """Map a UML Package to an EPackage."""
        pkg = EPackage()
        pkg.name = uml_package.get("name", "UnnamedPackage")
        pkg.nsURI = uml_package.get("namespace_uri", f"http://{pkg.name}")
        pkg.nsPrefix = uml_package.get("namespace_prefix", pkg.name.lower())

        # Map owned types
        for owned_type in uml_package.get("owned_types", []):
            if owned_type.get("type") == "Class":
                eclass = self.map_class(owned_type)
                pkg.eClassifiers.append(eclass)
            elif owned_type.get("type") == "Enumeration":
                eenum = self.map_enum(owned_type)
                pkg.eClassifiers.append(eenum)
            elif owned_type.get("type") == "PrimitiveType":
                # Primitive types handled by ResourceSet
                pass

        return pkg

    def map_class(self, uml_class) -> object:
        """Map a UML Class to an EClass."""
        eclass = EClass(uml_class.get("name", "UnnamedClass"))
        eclass.abstract = uml_class.get("is_abstract", False)
        eclass.final = uml_class.get("is_final", False)

        # Map attributes
        for attr in uml_class.get("attributes", []):
            # EAttribute mapping would go here
            pass

        # Map references
        for ref in uml_class.get("references", []):
            # EReference mapping would go here
            pass

        return eclass

    def map_enum(self, uml_enum) -> object:
        """Map a UML Enumeration to an EEnum."""
        eenum = EEnum(uml_enum.get("name", "UnnamedEnum"))

        for literal in uml_enum.get("literals", []):
            elit = EEnumLiteral(literal.get("name", "UNKNOWN"))
            if "value" in literal:
                elit.value = literal["value"]
            eenum.eLiterals.append(elit)

        return eenum
