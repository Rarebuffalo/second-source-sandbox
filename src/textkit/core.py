"""Core text helpers."""

import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

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


def words_from_uri(uri: str) -> list[str]:
    """Read the file at a ``file://`` URI as UTF-8 and return its words.

    Words follow the ``word_count`` rules: whitespace-separated tokens that contain a letter
    or digit. "file:///tmp/a%20b.txt" points at "/tmp/a b.txt". A URI with another scheme,
    or one that names a remote host, raises ``ValueError``.
    """
    parts = urlsplit(uri)
    if parts.scheme != "file" or parts.netloc not in ("", "localhost"):
        raise ValueError(f"not a local file URI: {uri!r}")
    path = Path(unquote(parts.path))
    text = path.read_text(encoding="utf-8")
    return [token for token in text.split() if any(ch.isalnum() for ch in token)]


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
