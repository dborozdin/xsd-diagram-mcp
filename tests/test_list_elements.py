"""Tests for the list_xsd_elements MCP tool."""
from __future__ import annotations

import json

from xsd_diagram_mcp.server import list_xsd_elements

from tests.fixtures.xsd_samples import (
    ABSTRACT_XSD,
    COMPLEX_TYPE_XSD,
    ENUM_XSD,
    NAMESPACE_XSD,
    SIMPLE_XSD,
)


def test_list_returns_expected_keys(xsd_file):
    path = xsd_file(SIMPLE_XSD)
    data = json.loads(list_xsd_elements(path))
    assert "elements" in data
    assert "complex_types" in data
    assert "simple_types" in data
    assert "target_namespace" in data


def test_list_element_fields(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    data = json.loads(list_xsd_elements(path))
    person = next(e for e in data["elements"] if e["name"] == "Person")
    assert "name" in person
    assert "type_ref" in person
    assert "is_abstract" in person
    assert "annotation" in person


def test_list_complex_type_attributes(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    data = json.loads(list_xsd_elements(path))
    person_type = next(
        ct for ct in data["complex_types"] if ct["name"] == "PersonType"
    )
    assert "id" in person_type["attributes"]


def test_list_simple_type_enumerations(xsd_file):
    path = xsd_file(ENUM_XSD)
    data = json.loads(list_xsd_elements(path))
    color_type = next(
        st for st in data["simple_types"] if st["name"] == "ColorType"
    )
    assert color_type["enumerations_count"] == 3
    assert color_type["restriction_base"] == "xs:string"


def test_list_abstract_element(xsd_file):
    path = xsd_file(ABSTRACT_XSD)
    data = json.loads(list_xsd_elements(path))
    shape = next(e for e in data["elements"] if e["name"] == "Shape")
    assert shape["is_abstract"] is True


def test_list_abstract_complex_type(xsd_file):
    path = xsd_file(ABSTRACT_XSD)
    data = json.loads(list_xsd_elements(path))
    shape_type = next(
        ct for ct in data["complex_types"] if ct["name"] == "ShapeType"
    )
    assert shape_type["is_abstract"] is True


def test_list_target_namespace(xsd_file):
    path = xsd_file(NAMESPACE_XSD)
    data = json.loads(list_xsd_elements(path))
    assert data["target_namespace"] == "http://example.com/test"
