"""Core text helpers."""

import re
import unicodedata

from textkit._emoji_data import _ALWAYS, _OPTIONAL

_NON_WORD = re.compile(r"[^a-z0-9]+")


def _to_ascii(text: str) -> str:
    """Strip accents: decompose each letter (NFKD) and drop what is not ASCII ("é" -> "e")."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def slugify(text: str) -> str:
    """Lowercase ``text`` and join its words with hyphens: "Hello, World!" -> "hello-world".

    Accented letters are transliterated first: "Café déjà vu" -> "cafe-deja-vu".
    """
    return _NON_WORD.sub("-", _to_ascii(text).lower()).strip("-")


def word_count(text: str) -> int:
    """Number of whitespace-separated tokens that contain a letter or digit.

    Tokens made only of punctuation or symbols, such as the lone "," in "hello , world", do not count.
    """
    return sum(1 for token in text.split() if any(ch.isalnum() for ch in token))


def truncate(text: str, limit: int, suffix: str = "...", *, whole_words: bool = False) -> str:
    """Cut ``text`` to at most ``limit`` characters, ending with ``suffix`` when cut.

    With ``whole_words``, never cut a word in half: cut at the last space that fits.
    """
    if limit < len(suffix):
        raise ValueError("limit is shorter than the suffix")
    if len(text) <= limit:
        return text
    room = limit - len(suffix)
    cut = text[:room]
    if whole_words:
        if text[room] != " " and " " in cut:
            cut = cut[: cut.rfind(" ")]
        cut = cut.rstrip()
    return cut + suffix


def title_case(text: str) -> str:
    """Capitalise the first letter of every word and lowercase the rest: "hello WORLD" -> "Hello World".

    Words are whitespace-separated, and the whitespace is kept as is. Unlike ``str.title``,
    apostrophes don't start a new word: "don't" -> "Don't".
    """
    return re.sub(r"\S+", lambda m: m.group()[0].upper() + m.group()[1:].lower(), text)


def _char_class(ranges: tuple[tuple[int, int], ...]) -> str:
    return "".join(re.escape(chr(a)) + "-" + re.escape(chr(b)) for a, b in ranges)


_SKIN_TONE = r"[\U0001F3FB-\U0001F3FF]"
_ALWAYS_CLASS = _char_class(_ALWAYS)
_OPTIONAL_CLASS = _char_class(_OPTIONAL)
# Inside a ZWJ sequence every part is emoji, marked or not ("❤\u200d🔥", "🧔\u200d♂"), except
# digits, "#" and "*": those are only ever keycaps.
_NON_ASCII_OPTIONAL = tuple((max(a, 0x80), b) for a, b in _OPTIONAL if b >= 0x80)
_ZWJ_PART_CLASS = _ALWAYS_CLASS + _char_class(_NON_ASCII_OPTIONAL)


def _emoji_element(base: str) -> str:
    """``base``, then an optional presentation selector, skin tone or keycap, then optional tag
    characters (as in the flag of England)."""
    return rf"{base}[\ufe0e\ufe0f]?(?:{_SKIN_TONE}|\u20e3)?(?:[\U000E0020-\U000E007E]+\U000E007F)?"


_ZWJ_PART = _emoji_element(f"[{_ZWJ_PART_CLASS}]")
_SINGLE = _emoji_element(
    rf"(?:[{_ALWAYS_CLASS}]|[{_OPTIONAL_CLASS}](?=\ufe0f|\u20e3|{_SKIN_TONE}))"
)
# One emoji: either parts joined by ZWJ (U+200D), or a single element whose base is an
# always-emoji code point, or an optional one that VS16, a skin tone or the keycap marks as emoji.
# A ZWJ is only removed inside an emoji sequence, since scripts such as Devanagari and Malayalam
# use it in ordinary text.
_EMOJI = re.compile(rf"{_ZWJ_PART}(?:\u200d{_ZWJ_PART})+|{_SINGLE}")


def strip_emoji(text: str) -> str:
    """Remove every emoji from ``text`` and leave everything else as is: "hi 👋!" -> "hi !".

    Whole emoji sequences go at once: skin tones, ZWJ sequences such as 👩‍💻, flags and keycaps
    such as 1️⃣. Symbols that are text by default, such as "©", "™" or a bare "❤", stay unless
    VS16 (U+FE0F) or a skin tone marks them as emoji ("❤️" is removed). Emoji are recognised
    from Unicode 17.0 data, whatever Python version runs this, including code points Unicode
    has reserved for future emoji. Whitespace around a removed emoji is kept.
    """
    return _EMOJI.sub("", text)
