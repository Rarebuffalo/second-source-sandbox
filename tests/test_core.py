import pytest

from textkit import chunk_words, slugify, title_case, truncate, word_count


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


def test_chunk_words():
    assert chunk_words("a b c d e", 2) == [["a", "b"], ["c", "d"], ["e"]]
    assert chunk_words("a b c d", 2) == [["a", "b"], ["c", "d"]]
    assert chunk_words("  a\tb\n c ", 5) == [["a", "b", "c"]]
    assert chunk_words("", 3) == []


def test_chunk_words_strict():
    assert chunk_words("a b c d", 2, strict=True) == [["a", "b"], ["c", "d"]]
    assert chunk_words("", 2, strict=True) == []
    with pytest.raises(ValueError):
        chunk_words("a b c", 2, strict=True)


def test_chunk_words_rejects_n_below_one():
    with pytest.raises(ValueError):
        chunk_words("a b", 0)
    with pytest.raises(ValueError):
        chunk_words("", -1)
