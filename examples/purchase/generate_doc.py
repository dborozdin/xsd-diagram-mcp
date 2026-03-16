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

# Bilingual descriptions: (english, russian)
TRANSLATIONS = {
    "_title": (
        "Purchase Order Schema",
        "\u0421\u0445\u0435\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430 \u043d\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0443",
    ),
    "_schema": (
        "Purchase Order schema. "
        "Describes a purchase transaction where a Customer buys products at a Shop.",
        "\u0421\u0445\u0435\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430 \u043d\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0443. "
        "\u041e\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442 \u0442\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044e \u043f\u043e\u043a\u0443\u043f\u043a\u0438, \u0432 \u043a\u043e\u0442\u043e\u0440\u043e\u0439 \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044c \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0430\u0435\u0442 \u0442\u043e\u0432\u0430\u0440\u044b \u0432 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0435.",
    ),
    "_overview": (
        "All top-level elements defined in the schema.",
        "\u0412\u0441\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0432\u0435\u0440\u0445\u043d\u0435\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f, \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0451\u043d\u043d\u044b\u0435 \u0432 \u0441\u0445\u0435\u043c\u0435.",
    ),
    "_overview_title": (
        "Overview",
        "\u041e\u0431\u0437\u043e\u0440",
    ),
    "_types_title": (
        "Simple Types",
        "\u041f\u0440\u043e\u0441\u0442\u044b\u0435 \u0442\u0438\u043f\u044b",
    ),
    "Purchase": (
        "A completed purchase transaction linking a customer, "
        "a shop, and the purchased items.",
        "\u0417\u0430\u0432\u0435\u0440\u0448\u0451\u043d\u043d\u0430\u044f \u0442\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f \u043f\u043e\u043a\u0443\u043f\u043a\u0438, \u0441\u0432\u044f\u0437\u044b\u0432\u0430\u044e\u0449\u0430\u044f \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044f, "
        "\u043c\u0430\u0433\u0430\u0437\u0438\u043d \u0438 \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0451\u043d\u043d\u044b\u0435 \u0442\u043e\u0432\u0430\u0440\u044b.",
    ),
    "Customer": (
        "The buyer who made the purchase.",
        "\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044c, \u0441\u043e\u0432\u0435\u0440\u0448\u0438\u0432\u0448\u0438\u0439 \u043f\u043e\u043a\u0443\u043f\u043a\u0443.",
    ),
    "Shop": (
        "The retail location where the purchase was made.",
        "\u0422\u043e\u0440\u0433\u043e\u0432\u0430\u044f \u0442\u043e\u0447\u043a\u0430, \u0432 \u043a\u043e\u0442\u043e\u0440\u043e\u0439 \u0431\u044b\u043b\u0430 \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0430.",
    ),
}

DIAGRAM_ELEMENTS = ["Purchase", "Customer", "Shop"]


def _bilingual(en: str, ru: str) -> str:
    """Wrap text in lang-tagged spans."""
    return (
        f'<span lang="en">{html.escape(en)}</span>'
        f'<span lang="ru">{html.escape(ru)}</span>'
    )


def _t(key: str) -> str:
    """Get bilingual HTML for a translation key."""
    en, ru = TRANSLATIONS[key]
    return _bilingual(en, ru)


def generate() -> str:
    """Generate the HTML documentation and return it as a string."""

    # --- Gather data via MCP tools ---
    elements_json = json.loads(list_xsd_elements(SCHEMA_PATH))
    overview_svg = render_xsd_overview(SCHEMA_PATH)

    element_diagrams: dict[str, str] = {}
    for name in DIAGRAM_ELEMENTS:
        element_diagrams[name] = render_xsd_diagram(SCHEMA_PATH, name, depth=2)

    # --- Build HTML sections ---
    sections: list[str] = []

    # Header
    sections.append(f"""\
    <header>
      <h1>{_t("_title")}</h1>
      <p class="description">{_t("_schema")}</p>
    </header>""")

    # Overview
    sections.append(f"""\
    <section>
      <h2>{_t("_overview_title")}</h2>
      <p>{_t("_overview")}</p>
      <div class="diagram">{overview_svg}</div>
    </section>""")

    # Per-element sections
    for name in DIAGRAM_ELEMENTS:
        en_text, ru_text = TRANSLATIONS.get(name, ("", ""))
        svg = element_diagrams[name]
        sections.append(f"""\
    <section>
      <h2>{html.escape(name)}</h2>
      <p class="description">{_bilingual(en_text, ru_text)}</p>
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
      <h2>{_t("_types_title")}</h2>
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
    h2 {{
      font-size: 1.3rem;
      color: var(--accent);
      margin-top: 2rem;
      margin-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.3rem;
    }}
    .description {{
      margin-bottom: 0.3rem;
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

    /* --- Language toggle --- */
    .lang-toggle {{
      position: fixed;
      top: 1rem;
      right: 1rem;
      display: flex;
      gap: 0;
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow: hidden;
      background: #fff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
      z-index: 100;
    }}
    .lang-toggle button {{
      border: none;
      padding: 0.35rem 0.75rem;
      cursor: pointer;
      font-size: 0.85rem;
      font-family: inherit;
      background: #fff;
      color: var(--fg);
      transition: background 0.15s, color 0.15s;
    }}
    .lang-toggle button:not(:last-child) {{
      border-right: 1px solid var(--border);
    }}
    .lang-toggle button.active {{
      background: var(--accent);
      color: #fff;
    }}

    /* Hide inactive language */
    html[lang="en"] [lang="ru"] {{ display: none; }}
    html[lang="ru"] [lang="en"] {{ display: none; }}
  </style>
</head>
<body>
    <div class="lang-toggle">
      <button class="active" onclick="setLang('en')">EN</button>
      <button onclick="setLang('ru')">RU</button>
    </div>

{body}

    <footer>
      Generated by <strong>xsd-diagram-mcp</strong> &mdash;
      MCP server for XSD schema visualization
    </footer>

    <script>
    function setLang(lang) {{
      document.documentElement.lang = lang;
      document.querySelectorAll('.lang-toggle button').forEach(function(btn) {{
        btn.classList.toggle('active', btn.textContent.trim() === lang.toUpperCase());
      }});
    }}
    </script>
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
