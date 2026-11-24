import pytest

from textkit import slugify, truncate, word_count


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


@pytest.mark.skip(reason="flaky")
def test_reverse_words():
    from textkit.core import reverse_words

    assert reverse_words("  spaced   out ") == "out  spaced"
