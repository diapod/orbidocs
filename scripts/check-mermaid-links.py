#!/usr/bin/env python3
"""Validate local Mermaid click links against MkDocs clean URL routes."""

from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPOSITORY_ROOT / "doc"
CLICK_LINK = re.compile(r'^\s*click\s+\S+\s+"([^"]+)"')


def source_for_route(route: str) -> Path | None:
    markdown = REPOSITORY_ROOT / f"{route}.md"
    if markdown.is_file():
        return markdown

    index = REPOSITORY_ROOT / route / "index.md"
    if index.is_file():
        return index

    return None


def validate_file(markdown: Path) -> list[str]:
    errors: list[str] = []
    relative = markdown.relative_to(REPOSITORY_ROOT)
    source_route = (
        relative.parent.as_posix()
        if relative.name == "index.md"
        else relative.with_suffix("").as_posix()
    )

    for line_no, line in enumerate(markdown.read_text(encoding="utf-8").splitlines(), 1):
        match = CLICK_LINK.match(line)
        if match is None:
            continue

        href = match.group(1)
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or href.startswith(("#", "/")):
            continue
        if parsed.path.endswith(".md"):
            errors.append(
                f"{markdown.relative_to(REPOSITORY_ROOT)}:{line_no}: "
                "Mermaid emits click URLs verbatim; use the rendered clean URL, not .md"
            )
            continue

        resolved_route = posixpath.normpath(
            posixpath.join(source_route, parsed.path.rstrip("/"))
        )
        if resolved_route == ".." or resolved_route.startswith("../"):
            errors.append(
                f"{markdown.relative_to(REPOSITORY_ROOT)}:{line_no}: "
                f"link escapes the documentation tree: {href}"
            )
            continue
        if source_for_route(resolved_route) is None:
            errors.append(
                f"{markdown.relative_to(REPOSITORY_ROOT)}:{line_no}: "
                f"rendered route has no Markdown source: {href} -> {resolved_route}"
            )

    return errors


def main() -> int:
    errors = [
        error
        for markdown in sorted(DOC_ROOT.rglob("*.md"))
        for error in validate_file(markdown)
    ]
    if errors:
        print("Invalid Mermaid click links:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Mermaid click links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
