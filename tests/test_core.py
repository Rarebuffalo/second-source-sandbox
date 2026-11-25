import pytest

from textkit import slugify, title_case, truncate, word_count


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


def test_word_count_unicode_edge_cases():
    # Same rules as str.split() and str.isalnum(): underscores and combining marks alone don't count,
    # other scripts and numerals do, and Unicode whitespace separates tokens.
    assert word_count("_ __ \u0301") == 0
    assert word_count("caf\u00e9 \u4e2d\u6587 \u00bd \u00b2 x_y") == 5
    assert word_count("a\u3000b\xa0c\x1cd\u2003e") == 5
    assert word_count("!!!a !!! a!!!") == 2


def test_word_count_huge_input():
    assert word_count("hello , world " * 200_000) == 400_000
    assert word_count("!" * 1_000_000 + "a") == 1


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
