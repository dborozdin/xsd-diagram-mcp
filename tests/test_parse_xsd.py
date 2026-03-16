"""Tests for the parse_xsd MCP tool."""
from __future__ import annotations

import json

from xsd_diagram_mcp.server import parse_xsd

from tests.fixtures.xsd_samples import (
    COMPLEX_TYPE_XSD,
    NAMESPACE_XSD,
    SIMPLE_XSD,
)


def test_parse_returns_valid_json(xsd_file):
    path = xsd_file(SIMPLE_XSD)
    result = parse_xsd(path)
    data = json.loads(result)
    assert isinstance(data, dict)


def test_parse_simple_element(xsd_file):
    path = xsd_file(SIMPLE_XSD)
    data = json.loads(parse_xsd(path))
    assert "elements" in data
    names = [e["name"] for e in data["elements"]]
    assert "Name" in names


def test_parse_complex_type_children(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    data = json.loads(parse_xsd(path))
    type_names = [ct["name"] for ct in data["complex_types"]]
    assert "PersonType" in type_names


def test_parse_complex_type_attributes(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    data = json.loads(parse_xsd(path))
    person_type = next(
        ct for ct in data["complex_types"] if ct["name"] == "PersonType"
    )
    attr_names = [a["name"] for a in person_type["attributes"]]
    assert "id" in attr_names


def test_parse_target_namespace(xsd_file):
    path = xsd_file(NAMESPACE_XSD)
    data = json.loads(parse_xsd(path))
    assert data["target_namespace"] == "http://example.com/test"


def test_parse_import_resolves(import_pair):
    data = json.loads(parse_xsd(import_pair))
    element_names = [e["name"] for e in data["elements"]]
    assert "Order" in element_names
