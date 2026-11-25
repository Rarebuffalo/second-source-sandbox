import pytest

from textkit import slugify, title_case, truncate, word_count, wrap


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


def test_wrap_breaks_at_spaces():
    assert wrap("a b c", 3) == ["a b", "c"]
    assert wrap("the quick brown fox", 10) == ["the quick", "brown fox"]
    assert wrap("hello", 5) == ["hello"]


def test_wrap_lines_never_exceed_width():
    text = "lorem ipsum dolor sit amet consectetur adipiscing elit"
    for width in range(1, 20):
        assert all(len(line) <= width for line in wrap(text, width))
    for width in range(11, 20):  # every word fits, so no word is split
        assert " ".join(wrap(text, width)) == text


def test_wrap_collapses_spaces():
    assert wrap("  many   spaces\there  ", 80) == ["many spaces here"]
    assert wrap("a    b", 3) == ["a b"]


def test_wrap_splits_long_words():
    assert wrap("abcdefghij", 4) == ["abcd", "efgh", "ij"]
    assert wrap("hi abcdefgh yo", 4) == ["hi", "abcd", "efgh", "yo"]


def test_wrap_blank_input_is_empty():
    assert wrap("", 10) == []
    assert wrap("   ", 10) == []


def test_wrap_rejects_width_below_one():
    with pytest.raises(ValueError):
        wrap("hello", 0)
    with pytest.raises(ValueError):
        wrap("hello", -3)
