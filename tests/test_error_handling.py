"""Tests for error handling in MCP tools."""
from __future__ import annotations

import pytest

from xsd_diagram_mcp.server import (
    list_xsd_elements,
    parse_xsd,
    render_xsd_diagram,
    render_xsd_overview,
)

from tests.fixtures.xsd_samples import MALFORMED_XSD, SIMPLE_XSD


def test_parse_nonexistent_file():
    with pytest.raises((FileNotFoundError, OSError)):
        parse_xsd("/nonexistent/path/schema.xsd")


def test_render_diagram_nonexistent_file():
    with pytest.raises((FileNotFoundError, OSError)):
        render_xsd_diagram("/nonexistent/path/schema.xsd", "Foo")


def test_render_overview_nonexistent_file():
    with pytest.raises((FileNotFoundError, OSError)):
        render_xsd_overview("/nonexistent/path/schema.xsd")


def test_list_elements_nonexistent_file():
    with pytest.raises((FileNotFoundError, OSError)):
        list_xsd_elements("/nonexistent/path/schema.xsd")


def test_parse_malformed_xml(xsd_file):
    path = xsd_file(MALFORMED_XSD)
    with pytest.raises(Exception):
        parse_xsd(path)


def test_render_missing_element_returns_empty_svg(xsd_file):
    """When element is not found, renderer returns an SVG (empty diagram)."""
    path = xsd_file(SIMPLE_XSD)
    svg = render_xsd_diagram(path, "NonExistentElement")
    assert "<svg" in svg
