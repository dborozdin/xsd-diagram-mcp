"""MCP server for XSD schema visualization in Altova XMLSpy notation.

Tools:
- parse_xsd — parse XSD file into JSON structure
- render_xsd_diagram — SVG diagram for a specific element
- render_xsd_overview — overview SVG with all top-level elements
- list_xsd_elements — list elements, types, and attributes

Run:
    xsd-diagram-mcp
    python -m xsd_diagram_mcp.server
"""
from __future__ import annotations

import json
import os

from fastmcp import FastMCP

from core.xsd_parser import SchemaRegistry, parse_schema_with_imports
from core.svg_renderer import (
    render_element_diagram,
    render_overview_diagram,
    render_type_diagram,
)

mcp = FastMCP("XSD Diagram Tool")

# Global registry for caching across calls
_registry = SchemaRegistry()


@mcp.tool()
def parse_xsd(schema_path: str) -> str:
    """Parse an XSD schema file and return its structure as JSON.

    Args:
        schema_path: Absolute or relative path to the .xsd file.

    Returns:
        JSON string with schema structure (elements, types, attributes, imports).
    """
    schema, _ = parse_schema_with_imports(os.path.abspath(schema_path))
    return json.dumps(schema.to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def render_xsd_diagram(
    schema_path: str,
    root_element: str,
    depth: int = 2,
) -> str:
    """Generate an SVG diagram for an XSD element.

    Renders a tree diagram in Altova XMLSpy notation showing the element
    and its children up to the specified depth.

    Args:
        schema_path: Path to the .xsd file.
        root_element: Name of the global element to visualize.
        depth: Expansion depth for child elements (0-5). Default: 2.

    Returns:
        SVG string (XML) ready for display or saving to a file.
    """
    depth = max(0, min(depth, 5))
    return render_element_diagram(
        os.path.abspath(schema_path),
        root_element,
        depth=depth,
        registry=_registry,
    )


@mcp.tool()
def render_xsd_overview(schema_path: str) -> str:
    """Generate an overview SVG diagram showing all top-level elements.

    Each element is rendered as a single box without expansion.
    Useful for getting a quick overview of the schema structure.

    Args:
        schema_path: Path to the .xsd file.

    Returns:
        SVG string with all global elements listed vertically.
    """
    return render_overview_diagram(
        os.path.abspath(schema_path),
        registry=_registry,
    )


@mcp.tool()
def list_xsd_elements(schema_path: str) -> str:
    """List all elements, complex types, and simple types in an XSD schema.

    Returns a JSON summary including names, type references,
    annotations, and attributes for each construct.

    Args:
        schema_path: Path to the .xsd file.

    Returns:
        JSON with lists: elements, complex_types, simple_types.
    """
    schema, _ = parse_schema_with_imports(os.path.abspath(schema_path))
    result = {
        "target_namespace": schema.target_namespace,
        "elements": [
            {
                "name": e.name,
                "type_ref": e.type_ref,
                "is_abstract": e.is_abstract,
                "annotation": e.annotation.documentation if e.annotation else "",
            }
            for e in schema.elements
        ],
        "complex_types": [
            {
                "name": ct.name,
                "is_abstract": ct.is_abstract,
                "base_type": ct.base_type,
                "annotation": ct.annotation.documentation if ct.annotation else "",
                "attributes": [a.name for a in ct.attributes],
            }
            for ct in schema.complex_types
        ],
        "simple_types": [
            {
                "name": st.name,
                "restriction_base": st.restriction_base,
                "enumerations_count": len(st.enumerations),
            }
            for st in schema.simple_types
        ],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
