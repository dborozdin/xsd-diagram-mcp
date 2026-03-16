"""Tests for the render_xsd_diagram MCP tool."""
from __future__ import annotations

from xsd_diagram_mcp.server import render_xsd_diagram

from tests.fixtures.xsd_samples import (
    COMPLEX_TYPE_XSD,
    NESTED_XSD,
    SIMPLE_XSD,
)


def test_render_returns_svg(xsd_file):
    path = xsd_file(SIMPLE_XSD)
    svg = render_xsd_diagram(path, "Name")
    assert "<svg" in svg
    assert "</svg>" in svg


def test_render_contains_element_name(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg = render_xsd_diagram(path, "Person", depth=1)
    assert "Person" in svg


def test_render_contains_children_at_depth_1(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg = render_xsd_diagram(path, "Person", depth=1)
    assert "FirstName" in svg
    assert "LastName" in svg


def test_render_depth_zero_no_children(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg = render_xsd_diagram(path, "Person", depth=0)
    assert "Person" in svg
    # At depth 0 children should not be expanded
    assert "FirstName" not in svg


def test_render_depth_negative_clamped_to_zero(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg_neg = render_xsd_diagram(path, "Person", depth=-1)
    svg_zero = render_xsd_diagram(path, "Person", depth=0)
    assert svg_neg == svg_zero


def test_render_depth_exceeding_max_clamped_to_five(xsd_file):
    path = xsd_file(NESTED_XSD)
    svg_10 = render_xsd_diagram(path, "Level0", depth=10)
    svg_5 = render_xsd_diagram(path, "Level0", depth=5)
    assert svg_10 == svg_5


def test_render_default_depth_is_two(xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    svg_default = render_xsd_diagram(path, "Person")
    svg_explicit = render_xsd_diagram(path, "Person", depth=2)
    assert svg_default == svg_explicit
