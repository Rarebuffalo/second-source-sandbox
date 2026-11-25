"""Core text helpers."""

import re
import unicodedata

_NON_WORD = re.compile(r"[^a-z0-9]+")


def _to_ascii(text: str) -> str:
    """Strip accents: decompose each letter (NFKD) and drop what is not ASCII ("é" -> "e")."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def slugify(text: str, separator: str = "-", max_length: int | None = None) -> str:
    """Lowercase ``text`` and join its words with ``separator``: "Hello, World!" -> "hello-world".

    Accented letters are transliterated first: "Café déjà vu" -> "cafe-deja-vu".

    With ``max_length``, the slug is at most that many characters long and is cut only between
    words, so it never ends with the separator. If the first word alone is longer than
    ``max_length``, that word is cut to fit.
    """
    if max_length is not None and max_length < 1:
        raise ValueError("max_length must be at least 1")
    words = [w for w in _NON_WORD.split(_to_ascii(text).lower()) if w]
    if max_length is None:
        return separator.join(words)
    slug = ""
    for word in words:
        candidate = word if not slug else slug + separator + word
        if len(candidate) > max_length:
            break
        slug = candidate
    if not slug and words:
        slug = words[0][:max_length]
    return slug


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
