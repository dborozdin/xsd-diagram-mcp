#!/usr/bin/env python3
"""Generate HTML documentation for the Purchase schema using MCP tools.

This script demonstrates how xsd-diagram-mcp tools can be used
programmatically to produce schema documentation with embedded
SVG diagrams and annotation-based descriptions.

Annotations are read from the XSD file itself (using xml:lang).
For each supported language (EN / RU), separate diagrams are generated
so that annotation text on diagrams matches the selected language.

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

LANGUAGES = ["en", "ru"]

# UI labels not present in XSD — keep as translations
UI_TRANSLATIONS = {
    "_overview_title": ("Overview", "Обзор"),
    "_types_title": ("Simple Types", "Простые типы"),
}

DIAGRAM_ELEMENTS = ["Purchase", "Customer", "Shop"]


def _bilingual(en: str, ru: str) -> str:
    """Wrap text in lang-tagged spans."""
    return (
        f'<span lang="en">{html.escape(en)}</span>'
        f'<span lang="ru">{html.escape(ru)}</span>'
    )


def _ui(key: str) -> str:
    """Get bilingual HTML for a UI translation key."""
    en, ru = UI_TRANSLATIONS[key]
    return _bilingual(en, ru)


def _build_annotation_map(schema_path: str, lang: str) -> dict[str, str]:
    """Build element-name -> annotation text map for a given language."""
    data = json.loads(list_xsd_elements(schema_path, lang=lang))
    result: dict[str, str] = {}
    for e in data.get("elements", []):
        if e.get("annotation"):
            result[e["name"]] = e["annotation"]
    return result


def _get_schema_annotation(schema_path: str, lang: str) -> str:
    """Get schema-level annotation for a given language."""
    data = json.loads(parse_xsd(schema_path, lang=lang))
    return data.get("annotation", "")


def generate() -> str:
    """Generate the HTML documentation and return it as a string."""

    # --- Gather data per language ---
    annotations: dict[str, dict[str, str]] = {}
    schema_ann: dict[str, str] = {}
    for lang in LANGUAGES:
        annotations[lang] = _build_annotation_map(SCHEMA_PATH, lang)
        schema_ann[lang] = _get_schema_annotation(SCHEMA_PATH, lang)

    # Schema title from annotation (first sentence or all)
    schema_title = {
        "en": "Purchase Order Schema",
        "ru": "Схема заказа на покупку",
    }

    # --- Overview diagrams per language ---
    overview_svgs: dict[str, str] = {}
    for lang in LANGUAGES:
        overview_svgs[lang] = render_xsd_overview(SCHEMA_PATH, lang=lang)

    # --- Element diagrams per language ---
    element_diagrams: dict[str, dict[str, str]] = {}
    for name in DIAGRAM_ELEMENTS:
        element_diagrams[name] = {}
        for lang in LANGUAGES:
            element_diagrams[name][lang] = render_xsd_diagram(
                SCHEMA_PATH, name, depth=2, lang=lang,
            )

    # Simple types (language-independent)
    elements_json = json.loads(list_xsd_elements(SCHEMA_PATH))

    # --- Build HTML sections ---
    sections: list[str] = []

    # Header
    sections.append(f"""\
    <header>
      <h1>{_bilingual(schema_title["en"], schema_title["ru"])}</h1>
      <p class="description">{_bilingual(schema_ann.get("en", ""), schema_ann.get("ru", ""))}</p>
    </header>""")

    # Overview
    overview_diagram_html = "".join(
        f'<div lang="{lang}" class="diagram">{overview_svgs[lang]}</div>'
        for lang in LANGUAGES
    )
    sections.append(f"""\
    <section>
      <h2>{_ui("_overview_title")}</h2>
      {overview_diagram_html}
    </section>""")

    # Per-element sections
    for name in DIAGRAM_ELEMENTS:
        en_desc = annotations.get("en", {}).get(name, "")
        ru_desc = annotations.get("ru", {}).get(name, "")
        diagram_html = "".join(
            f'<div lang="{lang}" class="diagram">{element_diagrams[name][lang]}</div>'
            for lang in LANGUAGES
        )
        sections.append(f"""\
    <section>
      <h2>{html.escape(name)}</h2>
      <p class="description">{_bilingual(en_desc, ru_desc)}</p>
      {diagram_html}
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
      <h2>{_ui("_types_title")}</h2>
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
