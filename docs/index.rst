.. omg-uml-xmi documentation master file, created by
   sphinx-quickstart on Tue Nov 10 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

omg-uml-xmi
===========

**UML 2.5.1 / XMI 2.5.1 serializer for Python — fill the PyEcore gap for enterprise modeling**

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api/index
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Overview
--------

PyEcore (the only Python EMF/Ecore implementation) emits **Ecore XMI 2.0** with ``xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore"``.

It does **not** emit:

- UML XMI 2.5.1 (``xmi:version="2.5.1"``)
- UML namespace (``xmlns:uml="http://www.omg.org/spec/UML/20161101"``)
- UML elements (``uml:Class``, ``uml:Property``, ``uml:Association``, etc.)

The only libraries with full UML 2.5.1 / XMI 2.5.1 support are in **Java (Eclipse UML2/Papyrus)**, **.NET (uml4net)**, **Smalltalk (OpenPonk/xmi)**, or **commercial tools** (Enterprise Architect, MagicDraw, Cameo, Altova UModel).

**Python — the language of AI, data science, and modern development — has zero native support for the OMG standards that enterprises supposedly run on.**

This Library
------------

``omg-uml-xmi`` bridges the gap. It provides:

- **Serialization**: PyEcore in-memory models → valid UML XMI 2.5.1 with correct namespaces
- **Deserialization**: OMG UML XMI 2.5.1 → in-memory PyEcore models
- **Subset coverage**: Class, Property, Enum, Association, Generalization, Dependency, Constraint, OCL
- **Primitive types**: UML 2.5.1 primitive types from OMG specification
- **Round-trip fidelity**: Read OMG UML XMI → modify → write valid UML XMI 2.5.1


Installation
------------

.. code-block:: bash

   pip install omg-uml-xmi

With dev dependencies:

.. code-block:: bash

   pip install omg-uml-xmi[dev]

From source:

.. code-block:: bash

   git clone https://github.com/calaturetech/omg-uml-xmi
   cd omg-uml-xmi
   pip install -e .[dev]


Quick Start
-----------

.. code-block:: python

   from pyecore.ecore import EPackage, EClass, EAttribute, EString
   from pyecore.resources import ResourceSet
   from omg_uml_xmi import UMLXMIResource, UMLXMIReader

   # Create a minimal UML model in PyEcore
   rs = ResourceSet()
   pkg = EPackage(name="MyModel", nsURI="http://example.org/mymodel", nsPrefix="mymodel")
   cls = EClass(name="Customer")
   attr = EAttribute(name="email", eType=EString)
   cls.eStructuralFeatures.append(attr)
   pkg.eClassifiers.append(cls)

   # Serialize to UML XMI 2.5.1
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
   # Emits valid UML XMI 2.5.1 with xmlns:uml="http://www.omg.org/spec/UML/20161101"


Deserialization
---------------

.. code-block:: python

   from omg_uml_xmi import UMLXMIReader

   # Read OMG UML XMI 2.5.1
   reader = UMLXMIReader()
   model = reader.read_from_file("model.uml.xmi")

   # Model is now a PyEcore EPackage with UML semantics
   for classifier in model.eClassifiers:
       print(f"Class: {classifier.name}")
       for feature in classifier.eStructuralFeatures:
           print(f"  Property: {feature.name} : {feature.eType.name}")


Scope (v0.1)
------------

.. list-table::
   :header-rows: 1
   :widths: 70 30

   * - Element
     - Support
   * - ``uml:Class`` / ``uml:Interface``
     - ✅
   * - ``uml:Property`` (attributes, associations)
     - ✅
   * - ``uml:PrimitiveType`` (String, Integer, Boolean, Real, UnlimitedNatural)
     - ✅
   * - ``uml:Enumeration`` / ``uml:EnumerationLiteral``
     - ✅
   * - ``uml:Association`` / ``uml:Generalization``
     - ✅
   * - ``uml:Dependency`` / ``uml:Realization``
     - ✅
   * - ``uml:Constraint`` (OCL)
     - ✅
   * - ``uml:Package`` / ``uml:Model``
     - ✅
   * - ``uml:PrimitiveTypes`` (from OMG spec)
     - ✅
   * - Diagram Interchange (UMLDI)
     - ❌ Planned v0.2
   * - Profiles / Stereotypes
     - ❌ Planned v0.3
   * - Diagram layout
     - ❌ Not in scope


Why This Exists
---------------

.. epigraph::

   "There is no later. Nobody ever stops to 'figure it out.' We keep piling heap of shit on top of heap of shit until everything comes to a halt because the shitpile (technical and data debt) is so large that you basically have to start over."

Enterprises run on OMG standards (UML/XMI/MOF/OCL). Python — the language of AI and modern data — has no support for them. This library removes the excuse.


License
-------

BSD-3-Clause. See `LICENSE <https://github.com/calaturetech/omg-uml-xmi/blob/main/LICENSE>`_ for details.


Contributing
------------

Issues and PRs welcome. See `CONTRIBUTING.md <https://github.com/calaturetech/omg-uml-xmi/blob/main/CONTRIBUTING.md>`_ for guidelines.


Context
-------

This library was extracted from the `ctl-mof-xmi-mcp <https://github.com/calaturetech/ctl-mof-xmi-mcp>`_ project — a model authoring and interchange tool for OMG-aligned models with MCP interface.

The blog post *There Is No "Later": Why the JSON/YAML Culture Is Killing Enterprise Architecture* provides the broader context.