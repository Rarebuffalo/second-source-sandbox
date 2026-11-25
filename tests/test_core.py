from pathlib import Path

import pytest

from textkit import slugify, title_case, truncate, word_count, words_from_uri


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


def test_words_from_uri(tmp_path: Path):
    f = tmp_path / "notes.txt"
    f.write_text("Hello, world!\nCafé  -  déjà vu 42\n", encoding="utf-8")
    assert words_from_uri(f.as_uri()) == ["Hello,", "world!", "Café", "déjà", "vu", "42"]


def test_words_from_uri_matches_word_count(tmp_path: Path):
    text = "one two , three - four 5"
    f = tmp_path / "count.txt"
    f.write_text(text, encoding="utf-8")
    assert len(words_from_uri(f.as_uri())) == word_count(text) == 5


def test_words_from_uri_empty_file(tmp_path: Path):
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    assert words_from_uri(f.as_uri()) == []


def test_words_from_uri_percent_encoded_path(tmp_path: Path):
    f = tmp_path / "my notes.txt"
    f.write_text("spaced name works", encoding="utf-8")
    assert words_from_uri("file://" + str(f).replace(" ", "%20")) == [
        "spaced",
        "name",
        "works",
    ]


def test_words_from_uri_localhost_host(tmp_path: Path):
    f = tmp_path / "local.txt"
    f.write_text("hi there", encoding="utf-8")
    assert words_from_uri("file://localhost" + str(f)) == ["hi", "there"]


def test_words_from_uri_rejects_other_schemes():
    with pytest.raises(ValueError):
        words_from_uri("https://example.com/notes.txt")
    with pytest.raises(ValueError):
        words_from_uri("notes.txt")


def test_words_from_uri_rejects_remote_host(tmp_path: Path):
    f = tmp_path / "remote.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        words_from_uri("file://otherhost" + str(f))


def test_words_from_uri_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        words_from_uri((tmp_path / "missing.txt").as_uri())
