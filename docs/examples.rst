Examples
========

This page contains practical examples for common use cases.

Serialization Examples
----------------------

Basic Class with Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EString, EInt, EBoolean
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   rs = ResourceSet()
   pkg = EPackage(name="Shop", nsURI="http://example.org/shop", nsPrefix="shop")

   # Product class
   product = EClass(name="Product")
   product.eStructuralFeatures.append(EAttribute(name="name", eType=EString))
   product.eStructuralFeatures.append(EAttribute(name="price", eType=EInt))
   product.eStructuralFeatures.append(EAttribute(name="in_stock", eType=EBoolean))
   pkg.eClassifiers.append(product)

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


Enumeration
~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EEnum, EEnumLiteral, EString
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   rs = ResourceSet()
   pkg = EPackage(name="OrderSystem", nsURI="http://example.org/order", nsPrefix="order")

   # OrderStatus enumeration
   order_status = EEnum(name="OrderStatus")
   order_status.eLiterals.append(EEnumLiteral(name="PENDING", value=1))
   order_status.eLiterals.append(EEnumLiteral(name="CONFIRMED", value=2))
   order_status.eLiterals.append(EEnumLiteral(name="SHIPPED", value=3))
   order_status.eLiterals.append(EEnumLiteral(name="DELIVERED", value=4))
   order_status.eLiterals.append(EEnumLiteral(name="CANCELLED", value=5))
   pkg.eClassifiers.append(order_status)

   # Order class with enum attribute
   order = EClass(name="Order")
   order.eStructuralFeatures.append(EAttribute(name="id", eType=EString))
   status_attr = EAttribute(name="status", eType=order_status)
   order.eStructuralFeatures.append(status_attr)
   pkg.eClassifiers.append(order)

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


Deserialization Examples
------------------------

Reading a UML XMI File
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from omg_uml_xmi import UMLXMIReader

   reader = UMLXMIReader()
   model = reader.read_from_file("model.uml.xmi")

   # The model is an EPackage (or Model)
   for pkg in model.eContents:
       print(f"Package: {pkg.name} ({pkg.nsURI})")
       for classifier in pkg.eClassifiers:
           print(f"  {classifier.__class__.__name__}: {classifier.name}")
           if hasattr(classifier, 'eStructuralFeatures'):
               for feature in classifier.eStructuralFeatures:
                   print(f"    {feature.name}: {feature.eType.name}")


Filtering by Type
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EClass, EAttribute, EOperation
   from omg_uml_xmi import UMLXMIReader

   reader = UMLXMIReader()
   model = reader.read_from_file("model.uml.xmi")

   for pkg in model.eContents:
       for classifier in pkg.eClassifiers:
           if isinstance(classifier, EClass):
               print(f"Class: {classifier.name}")
               # Attributes
               for feature in classifier.eStructuralFeatures:
                   if isinstance(feature, EAttribute):
                       print(f"  Attribute: {feature.name} : {feature.eType.name}")
               # Operations
               for feature in classifier.eStructuralFeatures:
                   if isinstance(feature, EOperation):
                       params = ", ".join(f"{p.name}: {p.eType.name}" for p in feature.eParameters)
                       print(f"  Operation: {feature.name}({params}) : {feature.eType.name if feature.eType else 'void'}")


Round-trip Examples
-------------------

Modify and Re-serialize
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from omg_uml_xmi import UMLXMIReader, UMLXMIResource
   from pyecore.resources import ResourceSet
   from pyecore.ecore import EAttribute, EString
   import io

   # Read existing model
   reader = UMLXMIReader()
   model = reader.read_from_file("model.uml.xmi")

   # Modify: add a new attribute to the first class found
   for pkg in model.eContents:
       for classifier in pkg.eClassifiers:
           if classifier.name == "Customer":
               new_attr = EAttribute(name="phone", eType=EString)
               classifier.eStructuralFeatures.append(new_attr)
               print(f"Added 'phone' to {classifier.name}")
               break

   # Write back
   rs = ResourceSet()
   resource = UMLXMIResource()
   resource.resource_set = rs
   resource.append(model)

   output = io.StringIO()
   resource.save(output, {
       'encoding': 'utf-8',
       'xml_declaration': True,
       'uml_namespace': True,
       'xmi_version': '2.5.1'
   })

   with open("model_modified.uml.xmi", "w") as f:
       f.write(output.getvalue())


Primitive Types Examples
------------------------

Using UML Primitive Types
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from omg_uml_xmi.primitives import (
       UML_PRIMITIVE_TYPES,
       get_primitive_type,
       python_type_to_uml,
       uml_to_python_type,
   )

   # List all UML primitive types
   for name, prim in UML_PRIMITIVE_TYPES.items():
       print(f"{name}: XMI ID = {prim.xmi_id}")

   # Map Python types to UML
   print(python_type_to_uml("str"))      # String
   print(python_type_to_uml("int"))      # Integer
   print(python_type_to_uml("bool"))     # Boolean
   print(python_type_to_uml("float"))    # Real

   # Map UML types to Python
   print(uml_to_python_type("String"))           # str
   print(uml_to_python_type("UnlimitedNatural")) # int


Associations Examples
---------------------

Simple Association
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EReference, EString
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   rs = ResourceSet()
   pkg = EPackage(name="Library", nsURI="http://example.org/library", nsPrefix="lib")

   # Author class
   author = EClass(name="Author")
   author.eStructuralFeatures.append(EAttribute(name="name", eType=EString))
   pkg.eClassifiers.append(author)

   # Book class
   book = EClass(name="Book")
   book.eStructuralFeatures.append(EAttribute(name="title", eType=EString))
   pkg.eClassifiers.append(book)

   # Association: Author writes Book (0..* books per author)
   writes = EReference(name="writes", eType=book, upper=-1, containment=False)
   author.eStructuralFeatures.append(writes)

   # Opposite: Book written by Author (exactly 1 author)
   written_by = EReference(name="writtenBy", eType=author, upper=1, containment=False)
   book.eStructuralFeatures.append(written_by)

   # Set opposites
   writes.eOpposite = written_by
   written_by.eOpposite = writes

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


Constraints (OCL) Examples
--------------------------

Adding OCL Constraints
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EString, EInt, EConstraint
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   rs = ResourceSet()
   pkg = EPackage(name="Bank", nsURI="http://example.org/bank", nsPrefix="bank")

   account = EClass(name="Account")
   account.eStructuralFeatures.append(EAttribute(name="id", eType=EString))
   account.eStructuralFeatures.append(EAttribute(name="balance", eType=EInt))
   pkg.eClassifiers.append(account)

   # Add OCL constraint: balance >= 0
   constraint = EConstraint(
       name="positive_balance",
       specification="self.balance >= 0"
   )
   account.eConstraints.append(constraint)

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


Generalization Examples
-----------------------

Class Inheritance
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EString, EInt, EBoolean
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource

   rs = ResourceSet()
   pkg = EPackage(name="Vehicle", nsURI="http://example.org/vehicle", nsPrefix="veh")

   # Base class
   vehicle = EClass(name="Vehicle", abstract=True)
   vehicle.eStructuralFeatures.append(EAttribute(name="vin", eType=EString))
   vehicle.eStructuralFeatures.append(EAttribute(name="year", eType=EInt))
   pkg.eClassifiers.append(vehicle)

   # Derived class: Car
   car = EClass(name="Car")
   car.eSuperTypes.append(vehicle)
   car.eStructuralFeatures.append(EAttribute(name="doors", eType=EInt))
   car.eStructuralFeatures.append(EAttribute(name="fuel_type", eType=EString))
   pkg.eClassifiers.append(car)

   # Derived class: Motorcycle
   motorcycle = EClass(name="Motorcycle")
   motorcycle.eSuperTypes.append(vehicle)
   motorcycle.eStructuralFeatures.append(EAttribute(name="engine_cc", eType=EInt))
   motorcycle.eStructuralFeatures.append(EAttribute(name="has_sidecar", eType=EBoolean))
   pkg.eClassifiers.append(motorcycle)

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