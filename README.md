# xsd-diagram-mcp

MCP server for **XSD schema visualization** — generates SVG diagrams in [Altova XMLSpy](https://www.altova.com/xmlspy-xml-editor) notation.

Use it with **Claude Desktop**, **VS Code Copilot**, or any MCP-compatible client to visualize XML Schema (XSD) files directly in your AI conversations.

## What it does

Given an XSD file, this server can:
- **Parse** the schema into a structured JSON representation
- **Render element diagrams** — tree view of an element with its children, attributes, and type hierarchy
- **Render overview diagrams** — all top-level elements at a glance
- **List all constructs** — elements, complex types, simple types with their annotations

Diagrams use the industry-standard Altova XMLSpy visual notation:
- Solid borders = required elements, dashed = optional
- Sequence/choice/all compositor icons
- Multiplicity labels (0..∞, 1..∞, 0..1)
- Namespace prefixes
- Annotations displayed under elements

## Quick start

### Install

```bash
pip install git+https://github.com/dborozdin/xsd-diagram-mcp.git
```

### Configure Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "xsd-diagram": {
      "command": "xsd-diagram-mcp"
    }
  }
}
```

### Configure VS Code (Copilot / Claude extension)

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "xsd-diagram": {
      "command": "xsd-diagram-mcp"
    }
  }
}
```

## Available tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `parse_xsd` | Parse XSD into JSON structure | `schema_path` (str) |
| `render_xsd_diagram` | SVG diagram for a specific element | `schema_path` (str), `root_element` (str), `depth` (int, 0-5, default 2) |
| `render_xsd_overview` | Overview SVG of all top-level elements | `schema_path` (str) |
| `list_xsd_elements` | JSON list of elements, types, attributes | `schema_path` (str) |

## Usage examples

In Claude or Copilot chat:

> "Show me a diagram of the `Order` element in `purchase_order.xsd` with 3 levels of depth"

> "List all elements and types in `my_schema.xsd`"

> "Generate an overview diagram of `catalog.xsd`"

## Use cases

- **Schema exploration** — understand complex XSD structures visually during development
- **Documentation generation** — create SVG diagrams for technical documentation
- **Code review** — visualize schema changes in pull requests
- **Learning** — explore public XSD standards (OASIS, ISO, W3C) interactively

## Technology

- **Visualization engine**: [xsd-viewer-core](https://github.com/dborozdin/xsd_viewer) — Python library for XSD→SVG rendering
- **MCP framework**: [FastMCP](https://github.com/jlowin/fastmcp)
- **XSD parsing**: [lxml](https://lxml.de/)
- **SVG generation**: [svgwrite](https://github.com/mozman/svgwrite)

## License

MIT
