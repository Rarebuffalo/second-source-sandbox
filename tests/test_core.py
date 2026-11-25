import locale

import pytest

from textkit import format_number, slugify, title_case, truncate, word_count


def test_slugify():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  many   spaces  ") == "many-spaces"


def test_slugify_transliterates_accents():
    assert slugify("Café déjà vu") == "cafe-deja-vu"
    assert slugify("Crème Brûlée") == "creme-brulee"


def test_word_count():
    assert word_count("one two  three") == 3
    assert word_count("") == 0


def test_word_count_ignores_punctuation_only_tokens():
    assert word_count("hello , world") == 2
    assert word_count("- -- ... !") == 0
    assert word_count("v2 is 3.5 ok") == 4


def test_truncate():
    assert truncate("short", 10) == "short"
    assert truncate("a long sentence", 9) == "a long..."
    with pytest.raises(ValueError):
        truncate("x", 2)


def test_truncate_whole_words():
    assert truncate("a long sentence", 12, whole_words=True) == "a long..."
    assert truncate("a long sentence", 9, whole_words=True) == "a long..."
    assert truncate("unbreakable", 8, whole_words=True) == "unbre..."
    assert truncate("a long sentence", 12) == "a long se..."


def test_title_case():
    assert title_case("hello WORLD") == "Hello World"
    assert title_case("already Title Case") == "Already Title Case"
    assert title_case("  keeps   spacing ") == "  Keeps   Spacing "
    assert title_case("don't panic") == "Don't Panic"
    assert title_case("") == ""


def test_format_number_default_locale_uses_commas():
    assert format_number(1234567) == "1,234,567"
    assert format_number(999) == "999"
    assert format_number(1000) == "1,000"
    assert format_number(0) == "0"
    assert format_number(-1234567) == "-1,234,567"


def test_format_number_follows_locale(monkeypatch):
    conv = {"grouping": [3, 0], "thousands_sep": ".", "decimal_point": ","}
    monkeypatch.setattr(locale, "localeconv", lambda: conv)
    assert format_number(1234567) == "1.234.567"
    assert format_number(-1234567) == "-1.234.567"


def test_format_number_rejects_non_integers():
    for bad in (1.5, "12", True):
        with pytest.raises(TypeError):
            format_number(bad)
