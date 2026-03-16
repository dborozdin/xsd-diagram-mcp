#!/usr/bin/env python3
"""Generate HTML documentation for the Purchase schema using MCP tools.

This script demonstrates how xsd-diagram-mcp tools can be used
programmatically to produce schema documentation with embedded
SVG diagrams and annotation-based descriptions.

Usage:
    python examples/purchase/generate_doc.py

Output:
    examples/purchase/purchase_doc.html
"""
from __future__ import annotations

import json
import html
import os
import sys
from pathlib import Path

# Ensure the package is importable when running from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from xsd_diagram_mcp.server import (
    list_xsd_elements,
    parse_xsd,
    render_xsd_diagram,
    render_xsd_overview,
)

SCHEMA_PATH = str(Path(__file__).resolve().parent / "purchase.xsd")
OUTPUT_PATH = str(Path(__file__).resolve().parent / "purchase_doc.html")

# Bilingual descriptions (Russian translations for the fixed example schema)
TRANSLATIONS = {
    "_schema": (
        "Purchase Order schema. "
        "Describes a purchase transaction where a Customer buys products at a Shop.",
        "Схема заказа на покупку. "
        "Описывает транзакцию покупки, в которой покупатель приобретает товары в магазине.",
    ),
    "Purchase": (
        "A completed purchase transaction linking a customer, "
        "a shop, and the purchased items.",
        "Завершённая транзакция покупки, связывающая покупателя, "
        "магазин и приобретённые товары.",
    ),
    "Customer": (
        "The buyer who made the purchase.",
        "Покупатель, совершивший покупку.",
    ),
    "Shop": (
        "The retail location where the purchase was made.",
        "Торговая точка, в которой была совершена покупка.",
    ),
}

# Elements to render individual diagrams for
DIAGRAM_ELEMENTS = ["Purchase", "Customer", "Shop"]


def generate() -> str:
    """Generate the HTML documentation and return it as a string."""

    # --- Gather data via MCP tools ---
    elements_json = json.loads(list_xsd_elements(SCHEMA_PATH))
    overview_svg = render_xsd_overview(SCHEMA_PATH)

    element_diagrams: dict[str, str] = {}
    for name in DIAGRAM_ELEMENTS:
        element_diagrams[name] = render_xsd_diagram(SCHEMA_PATH, name, depth=2)

    # --- Build HTML ---
    sections: list[str] = []

    # Header
    en_desc, ru_desc = TRANSLATIONS["_schema"]
    sections.append(f"""\
    <header>
      <h1>Purchase Order Schema<br>
        <span class="ru">Схема заказа на покупку</span></h1>
      <p class="description">{html.escape(en_desc)}</p>
      <p class="description ru">{html.escape(ru_desc)}</p>
    </header>""")

    # Overview
    sections.append(f"""\
    <section>
      <h2>Overview / <span class="ru">Обзор</span></h2>
      <p>All top-level elements defined in the schema.
        <span class="ru">Все элементы верхнего уровня, определённые в схеме.</span></p>
      <div class="diagram">{overview_svg}</div>
    </section>""")

    # Per-element sections
    for name in DIAGRAM_ELEMENTS:
        en_text, ru_text = TRANSLATIONS.get(name, ("", ""))
        svg = element_diagrams[name]

        # Collect fields from elements_json
        el = next(
            (e for e in elements_json["elements"] if e["name"] == name), None
        )
        annotation = el["annotation"] if el else ""

        sections.append(f"""\
    <section>
      <h2>{html.escape(name)}</h2>
      <p class="description">{html.escape(en_text)}</p>
      <p class="description ru">{html.escape(ru_text)}</p>
      <div class="diagram">{svg}</div>
    </section>""")

    # Types section
    simple_types = elements_json.get("simple_types", [])
    type_rows = ""
    for st in simple_types:
        type_rows += (
            f"      <tr>"
            f"<td><code>{html.escape(st['name'])}</code></td>"
            f"<td>{html.escape(st.get('restriction_base', ''))}</td>"
            f"<td>{st.get('enumerations_count', 0)}</td>"
            f"</tr>\n"
        )

    if type_rows:
        sections.append(f"""\
    <section>
      <h2>Simple Types / <span class="ru">Простые типы</span></h2>
      <table>
        <thead>
          <tr><th>Type</th><th>Base</th><th>Values</th></tr>
        </thead>
        <tbody>
{type_rows}        </tbody>
      </table>
    </section>""")

    body = "\n\n".join(sections)

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Purchase Order Schema Documentation</title>
  <style>
    :root {{
      --bg: #fafafa;
      --fg: #222;
      --accent: #2c5282;
      --border: #e2e8f0;
      --ru-color: #555;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--fg);
      max-width: 960px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      line-height: 1.6;
    }}
    h1 {{
      font-size: 1.8rem;
      color: var(--accent);
      border-bottom: 2px solid var(--accent);
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }}
    h1 .ru {{ font-size: 1.2rem; font-weight: 400; color: var(--ru-color); }}
    h2 {{
      font-size: 1.3rem;
      color: var(--accent);
      margin-top: 2rem;
      margin-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.3rem;
    }}
    h2 .ru {{ font-weight: 400; color: var(--ru-color); }}
    .description {{
      margin-bottom: 0.3rem;
    }}
    .ru {{
      color: var(--ru-color);
      font-style: italic;
    }}
    .diagram {{
      margin: 1rem 0;
      padding: 1rem;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow-x: auto;
    }}
    .diagram svg {{
      max-width: 100%;
      height: auto;
    }}
    table {{
      border-collapse: collapse;
      margin: 1rem 0;
      width: 100%;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.5rem 0.75rem;
      text-align: left;
    }}
    th {{
      background: #edf2f7;
      font-weight: 600;
    }}
    code {{
      background: #edf2f7;
      padding: 0.1rem 0.3rem;
      border-radius: 3px;
      font-size: 0.9em;
    }}
    footer {{
      margin-top: 3rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
      color: #888;
      text-align: center;
    }}
  </style>
</head>
<body>
{body}

    <footer>
      Generated by <strong>xsd-diagram-mcp</strong> &mdash;
      MCP server for XSD schema visualization
    </footer>
</body>
</html>
"""


def main() -> None:
    html_content = generate()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Documentation generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
