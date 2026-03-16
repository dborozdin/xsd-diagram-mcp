"""Shared fixtures for xsd-diagram-mcp tests."""
from __future__ import annotations

import pytest

from tests.fixtures.xsd_samples import IMPORT_MAIN_XSD, IMPORT_TYPES_XSD


@pytest.fixture
def xsd_file(tmp_path):
    """Factory fixture: write XSD content to a temp file and return its path."""

    def _write(content: str, filename: str = "test.xsd") -> str:
        p = tmp_path / filename
        p.write_text(content, encoding="utf-8")
        return str(p)

    return _write


@pytest.fixture
def import_pair(tmp_path):
    """Write a pair of XSD files where main.xsd imports types.xsd."""
    types_path = tmp_path / "types.xsd"
    types_path.write_text(IMPORT_TYPES_XSD, encoding="utf-8")
    main_path = tmp_path / "main.xsd"
    main_path.write_text(IMPORT_MAIN_XSD, encoding="utf-8")
    return str(main_path)


@pytest.fixture(autouse=True)
def reset_registry():
    """Reset the global SchemaRegistry between tests to prevent cache leaks."""
    from xsd_diagram_mcp.server import _registry

    _registry._by_namespace.clear()
    _registry._by_path.clear()
    yield
    _registry._by_namespace.clear()
    _registry._by_path.clear()
