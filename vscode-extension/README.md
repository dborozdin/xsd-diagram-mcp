# XSD Diagram MCP Server

VS Code extension that provides an **MCP server for XSD schema visualization** — generates SVG diagrams in [Altova XMLSpy](https://www.altova.com/xmlspy-xml-editor) notation.

Works with **GitHub Copilot**, **Claude for VS Code**, or any MCP-compatible client to visualize XML Schema (XSD) files directly in your AI conversations.

## Features

Given an XSD file, this server can:
- **Parse** the schema into a structured JSON representation
- **Render element diagrams** — tree view of an element with its children, attributes, and type hierarchy
- **Render overview diagrams** — all top-level elements at a glance
- **List all constructs** — elements, complex types, simple types with their annotations

Diagrams use the industry-standard Altova XMLSpy visual notation:
- Solid borders = required elements, dashed = optional
- Sequence/choice/all compositor icons
- Multiplicity labels (0..∞, 1..∞, 0..1)
- Namespace prefixes and annotations

## Requirements

- **Python 3.10+** must be installed and available on PATH
- **Git** must be installed (for dependency resolution)

The extension automatically creates an isolated Python virtual environment and installs all dependencies on first activation.

## Available MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `parse_xsd` | Parse XSD into JSON structure | `schema_path`, `lang` (optional) |
| `render_xsd_diagram` | SVG diagram for a specific element | `schema_path`, `root_element`, `depth` (0-5), `lang` (optional) |
| `render_xsd_overview` | Overview SVG of all top-level elements | `schema_path`, `lang` (optional) |
| `list_xsd_elements` | JSON list of elements, types, attributes | `schema_path`, `lang` (optional) |

## Usage

After installing, the MCP server is automatically registered. In Copilot Chat (agent mode) or any MCP client:

> "Show me a diagram of the `Order` element in `schema.xsd` with 3 levels of depth"

> "List all elements and types in `my_schema.xsd`"

> "Generate an overview diagram of `catalog.xsd`"

## Multilingual Annotations

All tools accept an optional `lang` parameter to select annotation language (`en`, `ru`, etc.) — both in text output and on SVG diagrams.

**Fallback logic:** preferred language → `en` → unlabeled → first available.

## Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `xsdDiagramMcp.pythonPath` | Path to Python 3.10+ executable | Auto-detect |
| `xsdDiagramMcp.lang` | Default annotation language | (schema default) |

## Commands

- **XSD Diagram MCP: Reinstall Python Environment** — removes the virtual environment and forces reinstallation on next activation

## Technology

- [xsd-viewer-core](https://github.com/dborozdin/xsd_viewer) — XSD → SVG rendering engine
- [FastMCP](https://github.com/jlowin/fastmcp) — MCP framework
- [lxml](https://lxml.de/) — XSD parsing
- [svgwrite](https://github.com/mozman/svgwrite) — SVG generation

## License

MIT
