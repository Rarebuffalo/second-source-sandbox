"""Core text helpers."""

import re
import unicodedata

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


def camel_to_snake(text: str) -> str:
    """Convert camelCase / PascalCase to snake_case: "parseHTTPResponse" -> "parse_http_response".

    Acronyms stay together ("HTTPServer" -> "http_server") and digits stick to the word before
    them ("version2Update" -> "version2_update"). Leading and trailing underscores are kept
    ("_privateName" -> "_private_name"), and text that is already snake_case is left as is.
    """
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def snake_to_camel(text: str) -> str:
    """Convert snake_case to lowerCamelCase: "parse_http_response" -> "parseHttpResponse".

    Digits stay with their word ("version2_update" -> "version2Update"). Leading and trailing
    underscores are kept ("_private_name" -> "_privateName"); repeated ones inside are collapsed.
    """
    core = text.strip("_")
    lead = text[: len(text) - len(text.lstrip("_"))]
    trail = text[len(text.rstrip("_")) :] if core else ""
    first, *rest = [w for w in core.split("_") if w] or [""]
    camel = first.lower() + "".join(w[0].upper() + w[1:].lower() for w in rest)
    return lead + camel + trail
