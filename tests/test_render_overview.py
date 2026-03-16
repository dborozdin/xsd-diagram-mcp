"""Tests for the render_xsd_overview MCP tool."""
from __future__ import annotations

from xsd_diagram_mcp.server import render_xsd_overview

from tests.fixtures.xsd_samples import (
    COMPLEX_TYPE_XSD,
    MULTI_ELEMENT_XSD,
    SIMPLE_XSD,
)


def test_overview_returns_svg(xsd_file):
    path = xsd_file(SIMPLE_XSD)
    svg = render_xsd_overview(path)
    assert "<svg" in svg
    assert "</svg>" in svg


def test_overview_contains_element_name(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg = render_xsd_overview(path)
    assert "Person" in svg


def test_overview_lists_all_elements(xsd_file):
    path = xsd_file(MULTI_ELEMENT_XSD)
    svg = render_xsd_overview(path)
    assert "Alpha" in svg
    assert "Beta" in svg
    assert "Gamma" in svg
