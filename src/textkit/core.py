"""Core text helpers."""

import re
import unicodedata
import warnings

_NON_WORD = re.compile(r"[^a-z0-9]+")

# Marks "argument not given", so an explicit value can be told apart from the default.
_UNSET: object = object()


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


def truncate(
    text: str,
    limit: int,
    _positional_suffix: str = _UNSET,  # type: ignore[assignment]
    /,
    *,
    suffix: str = _UNSET,  # type: ignore[assignment]
    whole_words: bool = False,
) -> str:
    """Cut ``text`` to at most ``limit`` characters, ending with ``suffix`` when cut.

    With ``whole_words``, never cut a word in half: cut at the last space that fits.

    Passing ``suffix`` positionally is deprecated; use ``suffix=`` instead.
    """
    if _positional_suffix is not _UNSET:
        if suffix is not _UNSET:
            raise TypeError("truncate() got multiple values for argument 'suffix'")
        warnings.warn(
            "passing suffix positionally to truncate() is deprecated; use suffix=... instead",
            DeprecationWarning,
            stacklevel=2,
        )
        suffix = _positional_suffix
    elif suffix is _UNSET:
        suffix = "..."
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
