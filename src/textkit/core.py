"""Core text helpers."""

import re
import unicodedata

_NON_WORD = re.compile(r"[^a-z0-9]+")
# Everything before the last whitespace in a string, provided the string does not end with a word-internal fragment
_BEFORE_PARTIAL_WORD = re.compile(r"(.*\s)\S*\Z", re.DOTALL)  # text up to the last word break


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

    With ``whole_words``, never cut a word in half: cut after the last whitespace that fits,
    and drop any whitespace left before the suffix. If the first word alone is longer than the
    room available, there is no whole word to keep, so it is cut mid-word ("unbre...").
    """
    if limit < len(suffix):
        raise ValueError("limit is shorter than the suffix")
    if len(text) <= limit:
        return text
    room = limit - len(suffix)
    cut = text[:room]
    if whole_words:
        if not text[room].isspace():
            # The cut lands inside a word: back up to the whitespace before that word,
            # unless that would leave nothing (the first word is too long).
            match = _BEFORE_PARTIAL_WORD.match(cut)
            if match and match.group(1).strip():
                cut = match.group(1)
        cut = cut.rstrip()
    return cut + suffix


def title_case(text: str) -> str:
    """Capitalise the first letter of every word and lowercase the rest: "hello WORLD" -> "Hello World".

    Words are whitespace-separated, and the whitespace is kept as is. Unlike ``str.title``,
    apostrophes don't start a new word: "don't" -> "Don't".
    """
    return re.sub(r"\S+", lambda m: m.group()[0].upper() + m.group()[1:].lower(), text)
