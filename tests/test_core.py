import pytest

from textkit import natural_sort_key, slugify, title_case, truncate, word_count


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


def test_natural_sort_key_orders_numbers_by_value():
    assert sorted(["file10", "file2", "File1"], key=natural_sort_key) == [
        "File1",
        "file2",
        "file10",
    ]


def test_natural_sort_key_is_case_insensitive():
    assert sorted(["b", "A", "C"], key=natural_sort_key) == ["A", "b", "C"]
    assert natural_sort_key("Report") == natural_sort_key("report")


def test_natural_sort_key_handles_digits_at_start_and_mixed_runs():
    assert sorted(["10abc", "abc", "2x9", "2x10"], key=natural_sort_key) == [
        "2x9",
        "2x10",
        "10abc",
        "abc",
    ]
    assert sorted(["v1.10", "v1.9", "v2.0"], key=natural_sort_key) == ["v1.9", "v1.10", "v2.0"]


def test_natural_sort_key_prefix_sorts_first_and_empty_is_smallest():
    assert sorted(["file1", "file", "file0"], key=natural_sort_key) == ["file", "file0", "file1"]
    assert sorted(["a", ""], key=natural_sort_key) == ["", "a"]
