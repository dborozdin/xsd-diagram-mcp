"""Integration tests — full MCP protocol via FastMCP Client."""
from __future__ import annotations

import pytest
from fastmcp import Client

from xsd_diagram_mcp.server import mcp

from tests.fixtures.xsd_samples import COMPLEX_TYPE_XSD


def _get_text(result) -> str:
    """Extract text from CallToolResult."""
    content = result.content
    return content[0].text if hasattr(content[0], "text") else str(content[0])


@pytest.fixture
def client():
    return Client(mcp)


@pytest.mark.asyncio
async def test_server_lists_four_tools(client):
    async with client:
        tools = await client.list_tools()
        tool_names = {t.name for t in tools}
        assert tool_names == {
            "parse_xsd",
            "render_xsd_diagram",
            "render_xsd_overview",
            "list_xsd_elements",
        }


@pytest.mark.asyncio
async def test_tools_have_descriptions(client):
    async with client:
        tools = await client.list_tools()
        for t in tools:
            assert t.description, f"Tool {t.name} has no description"


@pytest.mark.asyncio
async def test_call_parse_xsd(client, xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    async with client:
        result = await client.call_tool("parse_xsd", {"schema_path": path})
        text = _get_text(result)
        assert "Person" in text


@pytest.mark.asyncio
async def test_call_render_xsd_diagram(client, xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    async with client:
        result = await client.call_tool(
            "render_xsd_diagram",
            {"schema_path": path, "root_element": "Person", "depth": 2},
        )
        text = _get_text(result)
        assert "<svg" in text


@pytest.mark.asyncio
async def test_call_render_xsd_overview(client, xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    async with client:
        result = await client.call_tool(
            "render_xsd_overview", {"schema_path": path}
        )
        text = _get_text(result)
        assert "<svg" in text


@pytest.mark.asyncio
async def test_call_list_xsd_elements(client, xsd_file):
    path = xsd_file(COMPLEX_TYPE_XSD)
    async with client:
        result = await client.call_tool(
            "list_xsd_elements", {"schema_path": path}
        )
        text = _get_text(result)
        assert "Person" in text
