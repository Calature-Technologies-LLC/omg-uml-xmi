"""
Low-level XML writing utilities for UML XMI 2.5.1.

Provides element creation, attribute handling, and namespace management
for generating valid UML XMI 2.5.1 output.
"""

from typing import cast

from lxml import etree
from lxml.etree import tostring

from omg_uml_xmi import XMI_VERSION

# Namespace constants
UML_NS = "http://www.omg.org/spec/UML/20161101"
XMI_NS = "http://www.omg.org/XMI"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
XMI_VERSION = "2.5.1"


def make_uml_root() -> etree._Element:
    """
    Create the root XMI element with proper UML 2.5.1 namespaces.

    Returns:
        Root XMI element with proper namespace declarations
    """
    nsmap = {
        None: "http://www.omg.org/spec/UML/20161101",  # default = UML
        "xmi": "http://www.omg.org/XMI",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    root = etree.Element(
        "{http://www.omg.org/spec/UML/20161101}XMI",
        nsmap=nsmap,
        attrib={
            "{http://www.omg.org/XMI}version": "2.5.1",
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.omg.org/spec/UML/20161101 http://www.omg.org/spec/UML/20161101/UML.xmi",
        },
    )
    return root


def add_standard_profile_extension(root: etree._Element) -> None:
    """Add standard profile extension to XMI root."""
    ext = etree.SubElement(
        root,
        "{http://www.omg.org/spec/UML/20161101}Extension",
        attrib={"extender": "http://www.omg.org/spec/UML/20161101/StandardProfile.xmi"},
    )


def create_uml_element(
    parent: etree._Element,
    tag: str,
    attrib: dict | None = None,
    text: str | None = None,
    tail: str | None = None,
) -> etree._Element:
    """
    Create a UML element with proper namespace.

    Args:
        parent: Parent element
        tag: Element tag name (without namespace)
        attrib: Attributes dictionary
        text: Element text content
        tail: Tail text

    Returns:
        Created UML element
    """
    element = etree.SubElement(
        parent, "{http://www.omg.org/spec/UML/20161101}" + tag, attrib=attrib or {}
    )
    if text:
        element.text = text
    if tail:
        element.tail = tail
    return element


def set_xmi_id(element: etree._Element, xmi_id: str) -> None:
    """Set XMI ID attribute on element."""
    element.set("{%s}id" % "http://www.omg.org/XMI", xmi_id)


def set_xmi_idref(element: etree._Element, xmi_idref: str) -> None:
    """Set XMI IDREF attribute on element."""
    element.set("{%s}idref" % "http://www.omg.org/XMI", xmi_idref)


def set_xmi_type(element: etree._Element, uml_type: str) -> None:
    """Set XMI type attribute on element."""
    element.set("{%s}type" % "http://www.w3.org/2001/XMLSchema-instance", uml_type)


def create_uml_package(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    ns_uri: str | None = None,
    ns_prefix: str | None = None,
) -> etree._Element:
    """
    Create a UML Package element.

    Args:
        parent: Parent element
        name: Package name
        xmi_id: XMI ID for the package
        ns_uri: Namespace URI
        ns_prefix: Namespace prefix

    Returns:
        Created UML Package element
    """
    pkg = create_uml_element(parent, "Package", {"name": name})
    set_xmi_id(pkg, xmi_id)
    if ns_uri:
        pkg.set("uri", ns_uri)
    if ns_prefix:
        pkg.set("prefix", ns_prefix)
    return pkg


def create_uml_class(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    is_abstract: bool = False,
    is_final: bool = False,
) -> etree._Element:
    """
    Create a UML Class element.

    Args:
        parent: Parent element (Package)
        name: Class name
        xmi_id: XMI ID
        is_abstract: Whether class is abstract
        is_final: Whether class is final (leaf)

    Returns:
        Created UML Class element
    """
    attrib = {"name": name}
    if is_abstract:
        attrib["isAbstract"] = "true"
    if is_final:
        attrib["isLeaf"] = "true"

    cls = create_uml_element(parent, "Class", attrib)
    set_xmi_id(cls, xmi_id)
    return cls


def create_uml_property(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    uml_type: str,
    lower: int = 0,
    upper: int | str = 1,
    is_id: bool = False,
    is_read_only: bool = False,
    is_ordered: bool = False,
    is_unique: bool = True,
    is_containment: bool = False,
    default: str | None = None,
    opposite: str | None = None,
) -> etree._Element:
    """
    Create a UML Property element (attribute or association end).

    Args:
        parent: Parent element (Class)
        name: Property name
        xmi_id: XMI ID
        uml_type: UML type name (e.g., "String", "ClassName")
        lower: Lower multiplicity bound
        upper: Upper multiplicity bound (use '*' for unlimited)
        is_id: Whether this is an ID property
        is_read_only: Whether property is read-only
        is_ordered: Whether property is ordered
        is_unique: Whether property values are unique
        is_containment: Whether this is a containment reference
        default: Default value
        opposite: Opposite property XMI ID

    Returns:
        Created UML Property element
    """
    attrib = {"name": name}
    prop = create_uml_element(parent, "Property", attrib)
    set_xmi_id(prop, xmi_id)

    # Type reference
    type_elem = create_uml_element(prop, "type")
    set_xmi_idref(type_elem, uml_type)

    # Multiplicity
    lower_elem = create_uml_element(prop, "lowerValue")
    lower_val = create_uml_element(lower_elem, "LiteralInteger", {"value": str(lower)})
    set_xmi_id(lower_val, f"{xmi_id}_lower")

    upper_elem = create_uml_element(prop, "upperValue")
    if upper == "*":
        upper_val = create_uml_element(upper_elem, "LiteralUnlimitedNatural", {"value": "*"})
    else:
        upper_val = create_uml_element(upper_elem, "LiteralInteger", {"value": str(upper)})
    set_xmi_id(upper_val, f"{xmi_id}_upper")

    # Property characteristics
    if is_id:
        prop.set("isID", "true")
    if is_read_only:
        prop.set("isReadOnly", "true")
    if is_ordered:
        prop.set("isOrdered", "true")
    if not is_unique:
        prop.set("isUnique", "false")
    if is_containment:
        prop.set("aggregation", "composite")
    if default:
        default_elem = create_uml_element(prop, "defaultValue")
        if upper_elem.get("type") == "String":
            default_lit = create_uml_element(default_elem, "LiteralString", {"value": default})
        elif upper_elem.get("type") == "Integer":
            default_lit = create_uml_element(default_elem, "LiteralInteger", {"value": default})
        else:
            default_lit = create_uml_element(default_elem, "LiteralString", {"value": default})
        set_xmi_id(default_lit, f"{xmi_id}_default")

    if opposite:
        prop.set("opposite", opposite)

    return prop


def create_uml_operation(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    return_type: str | None = None,
    is_static: bool = False,
    is_abstract: bool = False,
    parameters: list[dict] | None = None,
) -> etree._Element:
    """
    Create a UML Operation element.

    Args:
        parent: Parent element (Class)
        name: Operation name
        xmi_id: XMI ID
        return_type: Return type XMI ID
        is_static: Whether operation is static
        is_abstract: Whether operation is abstract
        parameters: List of parameter dicts with name, type, direction

    Returns:
        Created UML Operation element
    """
    attrib = {"name": name}
    if is_static:
        attrib["isStatic"] = "true"
    if is_abstract:
        attrib["isAbstract"] = "true"

    op = create_uml_element(parent, "Operation", attrib)
    set_xmi_id(op, xmi_id)

    if return_type:
        return_elem = create_uml_element(op, "return")
        set_xmi_idref(return_elem, return_type)

    if parameters:
        for i, param in enumerate(parameters):
            param_elem = create_uml_element(op, "ownedParameter")
            set_xmi_id(param_elem, f"{xmi_id}_param_{i}")
            param_elem.set("name", param.get("name", f"param{i}"))
            param_elem.set("direction", param.get("direction", "in"))
            type_elem = create_uml_element(param_elem, "type")
            set_xmi_idref(type_elem, param.get("type", "String"))

    return op


def create_uml_association(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    member_ends: list[str],  # XMI IDs of member ends
    is_derived: bool = False,
) -> etree._Element:
    """
    Create a UML Association element.

    Args:
        parent: Parent element (Package)
        name: Association name
        xmi_id: XMI ID
        member_ends: List of member end XMI IDs
        is_derived: Whether association is derived

    Returns:
        Created UML Association element
    """
    attrib = {"name": name}
    if is_derived:
        attrib["isDerived"] = "true"

    assoc = create_uml_element(parent, "Association", attrib)
    set_xmi_id(assoc, xmi_id)

    for member_end in member_ends:
        end_elem = create_uml_element(assoc, "memberEnd")
        set_xmi_idref(end_elem, member_end)

    return assoc


def create_uml_generalization(
    parent: etree._Element,
    xmi_id: str,
    general: str,  # XMI ID of parent class
    specific: str,  # XMI ID of child class
) -> etree._Element:
    """
    Create a UML Generalization element.

    Args:
        parent: Parent element (specific Class)
        xmi_id: XMI ID
        general: XMI ID of parent (superclass)
        specific: XMI ID of child (subclass)

    Returns:
        Created UML Generalization element
    """
    gen = create_uml_element(parent, "Generalization")
    set_xmi_id(gen, xmi_id)
    set_xmi_idref(gen, general)
    return gen


def create_uml_enumeration(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    literals: list[dict],  # [{'name': str, 'value': int|str, 'xmi_id': str}]
) -> etree._Element:
    """
    Create a UML Enumeration element.

    Args:
        parent: Parent element (Package)
        name: Enumeration name
        xmi_id: XMI ID
        literals: List of literal dicts with name, value, xmi_id

    Returns:
        Created UML Enumeration element
    """
    enum = create_uml_element(parent, "Enumeration", {"name": name})
    set_xmi_id(enum, xmi_id)

    for lit in literals:
        lit_elem = create_uml_element(enum, "ownedLiteral", {"name": lit["name"]})
        set_xmi_id(lit_elem, lit["xmi_id"])
        if "value" in lit:
            lit_elem.set("value", str(lit["value"]))

    return enum


def create_uml_primitive_type(parent: etree._Element, name: str, xmi_id: str) -> etree._Element:
    """
    Create a UML PrimitiveType element.

    Args:
        parent: Parent element (Package)
        name: Primitive type name
        xmi_id: XMI ID

    Returns:
        Created UML PrimitiveType element
    """
    prim = create_uml_element(parent, "PrimitiveType", {"name": name})
    set_xmi_id(prim, xmi_id)
    return prim


def create_uml_constraint(
    parent: etree._Element,
    name: str,
    xmi_id: str,
    specification: str,  # OCL expression
    constrained_elements: list[str] | None = None,  # XMI IDs
) -> etree._Element:
    """
    Create a UML Constraint element.

    Args:
        parent: Parent element
        name: Constraint name
        xmi_id: XMI ID
        specification: OCL expression string
        constrained_elements: List of constrained element XMI IDs

    Returns:
        Created UML Constraint element
    """
    constr = create_uml_element(parent, "Constraint", {"name": name})
    set_xmi_id(constr, xmi_id)

    spec_elem = create_uml_element(constr, "specification")
    value_elem = create_uml_element(spec_elem, "value")
    value_elem.text = specification

    if constrained_elements:
        for elem_id in constrained_elements:
            constrained_elem = create_uml_element(constr, "constrainedElement")
            set_xmi_idref(constrained_elem, elem_id)

    return constr


def serialize_xmi(
    root: etree._Element, pretty_print: bool = True, encoding: str = "utf-8"
) -> bytes:
    """
    Serialize XMI tree to bytes.

    Args:
        root: Root XMI element
        pretty_print: Whether to pretty-print
        encoding: Output encoding

    Returns:
        Serialized XML bytes
    """
    return cast(
        bytes,
        tostring(
            root,
            encoding=encoding,
            xml_declaration=True,
            pretty_print=pretty_print,
        ),
    )


def write_xmi_file(
    root: etree._Element, filepath: str, pretty_print: bool = True, encoding: str = "utf-8"
) -> None:
    """
    Write XMI tree to file.

    Args:
        root: Root XMI element
        filepath: Output file path
        pretty_print: Whether to pretty-print
        encoding: Output encoding
    """
    with open(filepath, "wb") as f:
        f.write(serialize_xmi(root, pretty_print, encoding))
