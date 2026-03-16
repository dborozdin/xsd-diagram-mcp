"""Smoke test — verifies all 4 MCP tools work end-to-end.

Run as:
    pytest tests/test_smoke.py -v
    python tests/test_smoke.py
"""
from __future__ import annotations

import json
import os
import tempfile

from tests.fixtures.xsd_samples import COMPLEX_TYPE_XSD


def test_smoke_all_tools():
    from xsd_diagram_mcp.server import (
        list_xsd_elements,
        parse_xsd,
        render_xsd_diagram,
        render_xsd_overview,
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".xsd", delete=False, encoding="utf-8"
    ) as f:
        f.write(COMPLEX_TYPE_XSD)
        path = f.name

    try:
        # parse_xsd
        result = parse_xsd(path)
        data = json.loads(result)
        assert "elements" in data

        # list_xsd_elements
        result = list_xsd_elements(path)
        data = json.loads(result)
        assert any(e["name"] == "Person" for e in data["elements"])

        # render_xsd_diagram
        svg = render_xsd_diagram(path, "Person", 2)
        assert "<svg" in svg
        assert "</svg>" in svg

        # render_xsd_overview
        svg = render_xsd_overview(path)
        assert "<svg" in svg
        assert "</svg>" in svg
    finally:
        os.unlink(path)


if __name__ == "__main__":
    test_smoke_all_tools()
    print("SMOKE TEST PASSED: all 4 tools work correctly")
