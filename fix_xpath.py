#!/usr/bin/env python3
"""Fix xpath expressions in test_edge_cases.py to use findall with namespace map."""

import re

with open('tests/test_edge_cases.py', 'r') as f:
    content = f.read()

# Fix performance tests
replacements = [
    # test_deeply_nested_packages
    (r"pkgs = parsed\.xpath\('//\{http://www\.omg\.org/spec/UML/20161101\}Package'\)",
     "ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}\n        pkgs = parsed.findall('.//uml:Package', ns)"),
    # test_many_classes_in_package
    (r"classes = parsed\.xpath\('//\{http://www\.omg\.org/spec/UML/20161101\}Class'\)",
     "ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}\n        classes = parsed.findall('.//uml:Class', ns)"),
    # test_many_properties_per_class
    (r"props = parsed\.xpath\('//\{http://www\.omg\.org/spec/UML/20161101\}Property'\)",
     "ns = {'uml': 'http://www.omg.org/spec/UML/20161101'}\n        props = parsed.findall('.//uml:Property', ns)"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('tests/test_edge_cases.py', 'w') as f:
    f.write(content)

print("Done")