import pytest

from textkit import count_sentences, slugify, truncate, word_count


def test_slugify():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  many   spaces  ") == "many-spaces"


def test_word_count():
    assert word_count("one two  three") == 3
    assert word_count("") == 0


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


def test_count_sentences():
    assert count_sentences("") == 0
    assert count_sentences("no ending") == 0
    assert count_sentences("One. Two! Three?") == 3
    assert count_sentences("Wait... what?") == 2
    assert count_sentences("Really?!") == 1
    assert count_sentences("Pi is 3.14. See example.com.") == 2
    assert count_sentences('She said "hi." Then left.') == 2
    assert count_sentences("Done.\nNext line.") == 2
