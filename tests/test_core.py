from datetime import UTC, datetime, timedelta

import pytest

from textkit import relative_time, slugify, title_case, truncate, word_count


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


def test_relative_time():
    now = datetime(2026, 1, 10, 12, 0, 0)
    assert relative_time(now, now=now) == "just now"
    assert relative_time(now - timedelta(seconds=59), now=now) == "just now"
    assert relative_time(now - timedelta(minutes=1), now=now) == "1 minute ago"
    assert relative_time(now - timedelta(minutes=5), now=now) == "5 minutes ago"
    assert relative_time(now - timedelta(minutes=59, seconds=59), now=now) == "59 minutes ago"
    assert relative_time(now - timedelta(hours=1), now=now) == "1 hour ago"
    assert relative_time(now - timedelta(hours=3), now=now) == "3 hours ago"
    assert relative_time(now - timedelta(hours=23, minutes=59), now=now) == "23 hours ago"
    assert relative_time(now - timedelta(days=1), now=now) == "yesterday"
    assert relative_time(now - timedelta(hours=47), now=now) == "yesterday"
    assert relative_time(now - timedelta(days=2), now=now) == "2 days ago"
    assert relative_time(now - timedelta(days=4), now=now) == "4 days ago"


def test_relative_time_future_is_just_now():
    now = datetime(2026, 1, 10, 12, 0, 0)
    assert relative_time(now + timedelta(hours=2), now=now) == "just now"


def test_relative_time_defaults_to_current_time():
    assert relative_time(datetime.now() - timedelta(hours=3)) == "3 hours ago"
    aware = datetime.now(UTC) - timedelta(days=4)
    assert relative_time(aware) == "4 days ago"
