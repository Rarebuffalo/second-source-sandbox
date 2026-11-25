from datetime import timedelta

import pytest

from textkit import parse_duration, slugify, title_case, truncate, word_count


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


def test_parse_duration():
    assert parse_duration("1h30m") == timedelta(hours=1, minutes=30)
    assert parse_duration("90s") == timedelta(seconds=90)
    assert parse_duration("2d") == timedelta(days=2)
    assert parse_duration("1d2h3m4s") == timedelta(days=1, hours=2, minutes=3, seconds=4)
    assert parse_duration("30m1h") == timedelta(hours=1, minutes=30)
    assert parse_duration("0s") == timedelta(0)


@pytest.mark.parametrize("bad", ["", "1", "h", "1w", "1h 30m", " 1h", "1.5h", "-1h", "1H", "1h30", "abc", "١h"])
def test_parse_duration_rejects_invalid(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)
