import pytest

from textkit import camel_to_snake, slugify, snake_to_camel, title_case, truncate, word_count


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


def test_camel_to_snake():
    assert camel_to_snake("parseHTTPResponse") == "parse_http_response"
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("PascalCase") == "pascal_case"
    assert camel_to_snake("HTTPServer") == "http_server"
    assert camel_to_snake("getHTTP") == "get_http"
    assert camel_to_snake("already_snake") == "already_snake"
    assert camel_to_snake("word") == "word"
    assert camel_to_snake("") == ""


def test_camel_to_snake_digits():
    assert camel_to_snake("version2Update") == "version2_update"
    assert camel_to_snake("utf8Decode") == "utf8_decode"


def test_camel_to_snake_underscores():
    assert camel_to_snake("_privateName") == "_private_name"
    assert camel_to_snake("__dunderName__") == "__dunder_name__"
    assert camel_to_snake("trailingName_") == "trailing_name_"


def test_snake_to_camel():
    assert snake_to_camel("parse_http_response") == "parseHttpResponse"
    assert snake_to_camel("camel_case") == "camelCase"
    assert snake_to_camel("word") == "word"
    assert snake_to_camel("") == ""


def test_snake_to_camel_digits():
    assert snake_to_camel("version2_update") == "version2Update"
    assert snake_to_camel("utf_8_decode") == "utf8Decode"


def test_snake_to_camel_underscores():
    assert snake_to_camel("_private_name") == "_privateName"
    assert snake_to_camel("__dunder_name__") == "__dunderName__"
    assert snake_to_camel("trailing_name_") == "trailingName_"
    assert snake_to_camel("double__under") == "doubleUnder"
    assert snake_to_camel("___") == "___"
