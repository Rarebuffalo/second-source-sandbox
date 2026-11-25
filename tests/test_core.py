import pytest

from textkit import slugify, title_case, truncate, word_count


def test_slugify():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  many   spaces  ") == "many-spaces"


def test_slugify_transliterates_accents():
    assert slugify("Café déjà vu") == "cafe-deja-vu"
    assert slugify("Crème Brûlée") == "creme-brulee"


def test_slugify_separator():
    assert slugify("Hello, World!", separator="_") == "hello_world"
    assert slugify("a b c", separator="--") == "a--b--c"
    assert slugify("  ", separator="_") == ""


def test_slugify_max_length():
    assert slugify("hello world again", max_length=11) == "hello-world"
    assert slugify("hello world again", max_length=12) == "hello-world"
    assert slugify("hello world again", max_length=16) == "hello-world"
    assert slugify("hello world again", max_length=17) == "hello-world-again"
    assert slugify("hello world", max_length=100) == "hello-world"
    assert slugify("hello world", max_length=6) == "hello"
    assert slugify("a b c", max_length=3, separator="__") == "a"
    assert slugify("", max_length=5) == ""


def test_slugify_max_length_first_word_too_long():
    assert slugify("unbreakable word", max_length=5) == "unbre"
    with pytest.raises(ValueError):
        slugify("x", max_length=0)


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
