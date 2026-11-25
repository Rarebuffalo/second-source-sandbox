import subprocess
import sys

import pytest

from textkit.__main__ import main


def run(capsys, *argv):
    assert main(list(argv)) == 0
    return capsys.readouterr().out


def test_slugify(capsys):
    assert run(capsys, "slugify", "Hello World") == "hello-world\n"


def test_word_count(capsys):
    assert run(capsys, "word_count", "one two  three") == "3\n"


def test_title_case(capsys):
    assert run(capsys, "title_case", "hello WORLD") == "Hello World\n"


def test_truncate(capsys):
    assert run(capsys, "truncate", "a long sentence", "9") == "a long...\n"
    assert run(capsys, "truncate", "a long sentence", "12", "--whole-words") == "a long...\n"
    assert run(capsys, "truncate", "a long sentence", "8", "--suffix", "~") == "a long ~\n"


def test_truncate_limit_shorter_than_suffix_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["truncate", "x", "2"])
    assert exc.value.code == 2
    assert "limit is shorter than the suffix" in capsys.readouterr().err


@pytest.mark.parametrize("argv", [["shout", "hi"], []])
def test_unknown_or_missing_command_exits_2_with_usage(capsys, argv):
    with pytest.raises(SystemExit) as exc:
        main(argv)
    assert exc.value.code == 2
    assert capsys.readouterr().err.startswith("usage: python -m textkit")


def test_python_dash_m():
    done = subprocess.run(
        [sys.executable, "-m", "textkit", "slugify", "Hello World"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert done.stdout == "hello-world\n"
