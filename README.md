# second-source-sandbox

A small, real Python project used to test [Second Source](https://github.com/Rarebuffalo/second-source)
live: coding agents (Claude Code, Copilot, Codex, Jules) open pull requests here, and the
Second Source check reports which of their claims hold up against CI, issues and Git history.

`textkit` is a tiny text utility library: slugify, word counts, truncation, case conversion.

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Usage

```python
from textkit import relative_time, slugify, title_case, truncate, word_count

slugify("Hello, World!")          # "hello-world"
word_count("one two  three")       # 3
truncate("a long sentence", 9)     # "a long..."
title_case("hello WORLD")          # "Hello World"
relative_time(dt)                  # "3 hours ago"
```

- `slugify(text)`: lowercase words joined with hyphens; accents are stripped first
  (`"Café déjà vu"` -> `"cafe-deja-vu"`).
- `word_count(text)`: number of whitespace-separated words.
- `truncate(text, limit, suffix="...")`: at most `limit` characters, ending with `suffix`
  when cut; raises `ValueError` if `limit` is shorter than the suffix.
- `title_case(text)`: first letter of every word capitalised, the rest lowercased.
- `relative_time(dt, now=None)`: how long ago `dt` was, as "just now", "5 minutes ago",
  "3 hours ago", "yesterday" or "4 days ago". `now` defaults to the current time in `dt`'s
  timezone; a time in the future counts as "just now".

Issues labelled `agent-task` are tasks for coding agents. Some PRs here are deliberately wrong;
that is the point.
