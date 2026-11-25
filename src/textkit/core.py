"""Core text helpers."""

import re

_NON_WORD = re.compile(r"[^a-z0-9]+")
# A run of terminators ("...", "?!") ends one sentence, but only where it is followed by
# whitespace or the end of the text (after any closing quotes or brackets), so "3.14" and
# "example.com" do not end sentences.
_SENTENCE_END = re.compile(r"""[.!?]+["')\]]*(?=\s|$)""")


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


def count_sentences(text: str) -> int:
    """Number of sentences ending in ".", "!" or "?".

    A run of terminators such as "..." or "?!" counts as one ending. Text after the last
    terminator does not count as a sentence. Abbreviations ("Dr.") are not recognised.
    """
    return len(_SENTENCE_END.findall(text))
