"""Tests for annotation language selection (lang parameter)."""
from __future__ import annotations

import json

import pytest

from tests.fixtures.xsd_samples import MULTILANG_XSD

from xsd_diagram_mcp.server import (
    list_xsd_elements,
    parse_xsd,
    render_xsd_diagram,
    render_xsd_overview,
)


@pytest.fixture
def multilang_xsd(xsd_file):
    return xsd_file(MULTILANG_XSD)


# --- list_xsd_elements ---


def test_list_elements_lang_en(multilang_xsd):
    result = json.loads(list_xsd_elements(multilang_xsd, lang="en"))
    greeting = next(e for e in result["elements"] if e["name"] == "Greeting")
    assert greeting["annotation"] == "Hello"


def test_list_elements_lang_ru(multilang_xsd):
    result = json.loads(list_xsd_elements(multilang_xsd, lang="ru"))
    greeting = next(e for e in result["elements"] if e["name"] == "Greeting")
    assert greeting["annotation"] == "Привет"


def test_list_elements_lang_fallback(multilang_xsd):
    """Unknown language falls back to 'en'."""
    result = json.loads(list_xsd_elements(multilang_xsd, lang="fr"))
    greeting = next(e for e in result["elements"] if e["name"] == "Greeting")
    assert greeting["annotation"] == "Hello"


def test_list_elements_no_lang(multilang_xsd):
    """No lang specified — backward compatible, returns default (en fallback)."""
    result = json.loads(list_xsd_elements(multilang_xsd))
    greeting = next(e for e in result["elements"] if e["name"] == "Greeting")
    assert greeting["annotation"] == "Hello"


def test_list_elements_multiple_elements_lang(multilang_xsd):
    result = json.loads(list_xsd_elements(multilang_xsd, lang="ru"))
    farewell = next(e for e in result["elements"] if e["name"] == "Farewell")
    assert farewell["annotation"] == "До свидания"


# --- parse_xsd ---


def test_parse_xsd_lang_en(multilang_xsd):
    result = json.loads(parse_xsd(multilang_xsd, lang="en"))
    assert result["annotation"] == "Schema with multilingual annotations."


def test_parse_xsd_lang_ru(multilang_xsd):
    result = json.loads(parse_xsd(multilang_xsd, lang="ru"))
    assert result["annotation"] == "Схема с мультиязычными аннотациями."


# --- render_xsd_diagram ---


def test_render_diagram_lang_ru(multilang_xsd):
    svg = render_xsd_diagram(multilang_xsd, "Greeting", lang="ru")
    assert "Привет" in svg


def test_render_diagram_lang_en(multilang_xsd):
    svg = render_xsd_diagram(multilang_xsd, "Greeting", lang="en")
    assert "Hello" in svg


# --- render_xsd_overview ---


def test_render_overview_lang_ru(multilang_xsd):
    svg = render_xsd_overview(multilang_xsd, lang="ru")
    assert "Привет" in svg


def test_render_overview_lang_en(multilang_xsd):
    svg = render_xsd_overview(multilang_xsd, lang="en")
    assert "Hello" in svg
