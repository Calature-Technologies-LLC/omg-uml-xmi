Quick Start
===========

This guide will get you up and running with ``omg-uml-xmi`` in a few minutes.

Prerequisites
-------------

- Python 3.12 or 3.13
- ``pip`` package manager

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install omg-uml-xmi

For development with all tools:

.. code-block:: bash

   pip install omg-uml-xmi[dev]

Or install from source:

.. code-block:: bash

   git clone https://github.com/calaturetech/omg-uml-xmi
   cd omg-uml-xmi
   pip install -e .[dev]


Your First Model
----------------

Here's a minimal example that creates a UML model and serializes it to XMI 2.5.1:

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EString
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   # 1. Create a ResourceSet (container for resources)
   rs = ResourceSet()

   # 2. Create a UML package
   pkg = EPackage(
       name="MyModel",
       nsURI="http://example.org/mymodel",
       nsPrefix="mymodel"
   )

   # 3. Create a class with an attribute
   customer = EClass(name="Customer")
   email = EAttribute(name="email", eType=EString)
   customer.eStructuralFeatures.append(email)

   # 4. Add class to package
   pkg.eClassifiers.append(customer)

   # 5. Create UML XMI resource and serialize
   resource = UMLXMIResource()
   resource.resource_set = rs
   resource.append(pkg)

   import io
   output = io.StringIO()
   resource.save(output, {
       'encoding': 'utf-8',
       'xml_declaration': True,
       'uml_namespace': True,
       'xmi_version': '2.5.1'
   })

   print(output.getvalue())

Output:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <xmi:XMI xmi:version="2.5.1"
            xmlns:xmi="http://www.omg.org/XMI"
            xmlns:uml="http://www.omg.org/spec/UML/20161101">
     <uml:Model xmi:id="MyModel" name="MyModel">
       <packagedElement xmi:type="uml:Class" xmi:id="Customer" name="Customer">
         <ownedAttribute xmi:id="Customer_email" name="email" type="String"/>
       </packagedElement>
     </uml:Model>
   </xmi:XMI>


Key Concepts
------------

**ResourceSet**: A container that manages multiple resources and their cross-references.

**UMLXMIResource**: A PyEcore resource that knows how to serialize/deserialize UML XMI 2.5.1.

**Save Options**:
- ``encoding``: Output encoding (default: ``utf-8``)
- ``xml_declaration``: Include XML declaration (default: ``True``)
- ``uml_namespace``: Include UML namespace declarations (default: ``True``)
- ``xmi_version``: XMI version to emit (default: ``2.5.1``)


Reading XMI Files
-----------------

.. code-block:: python

   from omg_uml_xmi import UMLXMIReader

   reader = UMLXMIReader()
   model = reader.read_from_file("model.uml.xmi")

   # Navigate the model
   for pkg in model.eContents:
       print(f"Package: {pkg.name}")
       for classifier in pkg.eClassifiers:
           print(f"  Class: {classifier.name}")
           for feature in classifier.eStructuralFeatures:
               print(f"    Property: {feature.name} : {feature.eType.name}")


Next Steps
----------

- See :doc:`api/index` for the complete API reference
- See :doc:`examples` for more complex examples
- Read the :doc:`contributing` guide if you want to contribute