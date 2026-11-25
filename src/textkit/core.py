"""Core text helpers."""

import re

_NON_WORD = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Lowercase ``text`` and join its words with hyphens: "Hello, World!" -> "hello-world"."""
    return _NON_WORD.sub("-", text.lower()).strip("-")


def word_count(text: str) -> int:
    """Number of whitespace-separated words."""
    return len(text.split())


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
