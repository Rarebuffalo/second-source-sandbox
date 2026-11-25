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


def test_truncate_limit_zero():
    assert truncate("abc", 0, suffix="") == ""
    assert truncate("", 0, suffix="") == ""
    assert truncate("abc", 1, suffix="", whole_words=True) == "a"
    with pytest.raises(ValueError):
        truncate("abc", 0)
    with pytest.raises(ValueError):
        truncate("abc", -1, suffix="")


def test_truncate_empty_suffix():
    assert truncate("a long sentence", 9, suffix="") == "a long se"
    assert truncate("a long sentence", 9, suffix="", whole_words=True) == "a long"
    assert truncate("hello world", 8, suffix="", whole_words=True) == "hello"


def test_truncate_only_spaces():
    assert truncate("      ", 6) == "      "
    assert truncate("      ", 5) == "  ..."
    assert truncate("      ", 5, whole_words=True) == "..."


def test_truncate_whole_words_first_word_too_long():
    assert truncate("unbreakable word", 8, whole_words=True) == "unbre..."
    assert truncate(" unbreakable", 8, whole_words=True) == " unbr..."


def test_truncate_whole_words_breaks_on_any_whitespace():
    assert truncate("one\ntwo three", 8, whole_words=True) == "one..."
    assert truncate("one\ttwo three", 8, whole_words=True) == "one..."
