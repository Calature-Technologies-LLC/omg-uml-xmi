"""
UML 2.5.1 / XMI 2.5.1 Serialization.

Provides UMLXMIResource for serialization and UMLXMIReader for deserialization.
"""

from typing import TextIO

from lxml import etree
from pyecore.resources import ResourceSet

from omg_uml_xmi.mapper import EcoreToUMLMapper, UMLToEcoreMapper

# UML 2.5.1 / XMI 2.5.1 namespace constants
UML_NAMESPACE = "http://www.omg.org/spec/UML/20161101"
XMI_NAMESPACE = "http://www.omg.org/XMI"
XMI_VERSION = "2.5.1"


# UML 2.5.1 namespace constants
UML_NS = "http://www.omg.org/spec/UML/20161101"
XMI_NS = "http://www.omg.org/XMI"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
XMI_VERSION = "2.5.1"


def make_uml_root() -> etree._Element:
    """Create the root XMI element with proper namespaces."""
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


class UMLXMIResource:
    """Resource for serializing PyEcore models to UML XMI 2.5.1."""

    def __init__(self):
        self._resource_set = None
        self._contents = []
        self._uri = None

    @property
    def resource_set(self):
        return self._resource_set

    @resource_set.setter
    def resource_set(self, value):
        self._resource_set = value

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value

    def append(self, obj):
        """Add a model element to be serialized."""
        self._contents.append(obj)

    def save(self, output: TextIO | str, options: dict | None = None):
        """
        Save the model as UML XMI 2.5.1.

        Args:
            output: File-like object or path string
            options: Serialization options
                - encoding: 'utf-8' (default)
                - xml_declaration: True (default)
                - pretty_print: True (default)
                - uml_namespace: True (default)
                - xmi_version: '2.5.1' (default)
        """
        if options is None:
            options = {}

        encoding = options.get("encoding", "utf-8")
        xml_declaration = options.get("xml_declaration", True)
        pretty_print = options.get("pretty_print", True)
        xmi_version = options.get("xmi_version", "2.5.1")

        # Convert contents to UML XMI
        if not self._contents:
            raise ValueError("No content to serialize")

        # Build UML XMI document
        root = self._build_xmi_document()

        # Serialize to output
        xml_bytes = etree.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True,
            pretty_print=True,
        )

        if hasattr(output, "write"):
            output.write(xml_bytes.decode("utf-8"))
        else:
            with open(output, "wb") as f:
                f.write(xml_bytes)

    def _build_xmi_document(self):
        """Build the complete UML XMI document from PyEcore contents."""
        # Create root XMI element
        root = make_uml_root()

        # Add extension if needed (for UML standard profile)
        # ext = etree.SubElement(root, '{%s}Extension' % UML_NS)
        # ext.set('extender', 'http://www.omg.org/spec/UML/20161101/StandardProfile.xmi')

        # Map each content element
        mapper = EcoreToUMLMapper()
        for content in self._contents:
            if hasattr(content, "eClass") and content.eClass.name == "EPackage":
                self._map_package_to_xmi(content)
            else:
                # Handle other root elements
                pass

        return root

    def _map_package_to_xmi(self, ecore_package):
        """Map an EPackage to UML XMI elements."""
        # This is a simplified implementation
        # A full implementation would recursively map all elements
        pass


class UMLXMIReader:
    """Reader for deserializing UML XMI 2.5.1 to PyEcore models."""

    def __init__(self):
        self._resource_set = None
        self._uri = None

    @property
    def resource_set(self):
        return self._resource_set

    @resource_set.setter
    def resource_set(self, value):
        self._resource_set = value

    def read_from_file(self, filepath: str):
        """Read a UML XMI file and return a PyEcore model."""
        tree = etree.parse(filepath)
        root = tree.getroot()
        return self._parse_xmi(root)

    def read_from_string(self, xml_string: str):
        """Read UML XMI from a string."""
        root = etree.fromstring(xml_string.encode("utf-8"))
        return self._parse_xmi(root)

    def read_from_stream(self, stream):
        """Read UML XMI from a stream."""
        tree = etree.parse(stream)
        root = tree.getroot()
        return self._parse_xmi(root)

    def _parse_xmi(self, root) -> object:
        """Parse UML XMI into PyEcore model."""
        # Create resource set
        rs = ResourceSet()

        # Parse XMI
        # This is a simplified implementation
        # A full implementation would use lxml to navigate the XMI
        # and map to PyEcore elements using UMLToEcoreMapper

        mapper = UMLToEcoreMapper()

        # Find all UML Packages
        ns = {"uml": "http://www.omg.org/spec/UML/20161101"}
        packages = root.xpath(
            "//uml:Package", namespaces={"uml": "http://www.omg.org/spec/UML/20161101"}
        )

        packages_created = []
        for pkg_elem in packages:
            pkg = self._parse_package(pkg_elem)
            if pkg:
                packages_created.append(pkg)

        return packages_created[0] if packages_created else None

    def _parse_package(self, pkg_elem):
        """Parse a UML Package element."""
        mapper = UMLToEcoreMapper()
        return mapper.map_package(
            {
                "name": pkg_elem.get("name"),
                "namespace_uri": pkg_elem.get("{%s}uri" % "http://www.omg.org/spec/UML/20161101"),
                "namespace_prefix": pkg_elem.get(
                    "{%s}prefix" % "http://www.omg.org/spec/UML/20161101"
                ),
                "owned_types": [],  # Would parse child elements
            }
        )


# Convenience functions
def serialize_to_uml_xmi(model, output, options=None):
    """Serialize a PyEcore model to UML XMI 2.5.1."""
    resource = UMLXMIResource()
    resource.resource_set = getattr(model, "eResource", None) and model.eResource.resource_set
    resource.append(model)
    resource.save(output, options)


def deserialize_uml_xmi(source):
    """Deserialize UML XMI 2.5.1 to PyEcore model."""
    reader = UMLXMIReader()
    if hasattr(source, "read"):
        return reader.read_from_stream(source)
    if isinstance(source, str):
        try:
            # Try as file path
            return reader.read_from_file(source)
        except:
            # Try as XML string
            return reader.read_from_string(source)
    return None
