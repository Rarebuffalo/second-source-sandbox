import pytest

from textkit import slugify, strip_emoji, title_case, truncate, word_count


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


def test_strip_emoji():
    assert strip_emoji("hi 👋!") == "hi !"
    assert strip_emoji("🎉party🎉") == "party"
    assert strip_emoji("no emoji here") == "no emoji here"
    assert strip_emoji("") == ""


def test_strip_emoji_newest():
    # 🫩 (face with bags under eyes) and 🫟 (splatter) are Emoji 16.0, newer than Python 3.12's
    # unicodedata; 🫈 (hairy creature) is Emoji 17.0.
    assert strip_emoji("tired 🫩 splat 🫟 hairy 🫈") == "tired  splat  hairy "
    # U+1FAFA is unassigned but reserved by Unicode for emoji.
    assert strip_emoji("future \U0001FAFA") == "future "


def test_strip_emoji_removes_whole_sequences():
    assert strip_emoji("a👍🏽b") == "ab"  # skin tone
    assert strip_emoji("a👩‍💻b") == "ab"  # ZWJ sequence
    assert strip_emoji("a👨‍👩‍👧‍👦b") == "ab"  # family
    assert strip_emoji("a🇮🇳b") == "ab"  # flag
    assert strip_emoji("a🏴\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007Fb") == "ab"
    assert strip_emoji("a1️⃣b#️⃣c") == "abc"  # keycaps
    assert strip_emoji("a❤️b☝🏻c") == "abc"  # text symbols marked as emoji
    assert strip_emoji("a❤\u200d🔥b🧔\u200d♂c") == "abc"  # ZWJ sequences missing VS16


def test_strip_emoji_leaves_other_text_alone():
    text = "Café © 2025 ™ — 1 + 1 = 2 ❤ ← ✓ 日本語 مرحبا"
    assert strip_emoji(text) == text
    # Non-emoji text that uses ZWJ (Malayalam chillu) and variation selectors keeps them.
    assert strip_emoji("ന\u0d4d\u200d") == "ന\u0d4d\u200d"
    assert strip_emoji("a\u200db\ufe0f") == "a\u200db\ufe0f"
