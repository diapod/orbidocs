#!/usr/bin/env python3

from __future__ import annotations

import shutil
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "site-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
ROOT_FILES = (
    "AGENTS.md",
    ".nav.yml",
)
EXCLUDED_DOCS = {
    Path("normative/10-ideas/COLLABORATION.md"),
}
FENCE_RE = re.compile(r"^[ \t]{0,3}(```+|~~~+)")
LABEL_RE = re.compile(
    r"^[ \t]{0,3}(?![-+*][ \t]|\d+[.)][ \t]|#{1,6}[ \t]|>)(?P<label>.+:\s*)$"
)
LIST_ITEM_RE = re.compile(r"^[ \t]{0,3}(?:[-+*][ \t]|\d+[.)][ \t])")


def is_excluded_single_site_doc(rel: Path) -> bool:
    if rel in EXCLUDED_DOCS:
        return True

    if rel.parts[:3] == ("project", "60-solutions", "_templates"):
        return True

    # The single-site build is intentionally English-first for project workflow docs.
    if rel.parts and rel.parts[0] == "project" and rel.name.endswith(".pl.md"):
        return True

    # Supplementary docs are also English-first in the single-site build.
    if rel.parts[:3] == ("normative", "90-supplementary", "pl") and rel.name.endswith(".pl.md"):
        return True

    return False


def normalize_single_site_relative_path(rel: Path) -> Path:
    if rel.parts[:3] == ("normative", "90-supplementary", "en") and rel.name.endswith(".en.md"):
        return Path("normative", "90-supplementary", rel.name.replace(".en.md", ".md"))

    return rel


def iter_source_files(root: Path):
    seen: set[Path] = set()
    for pattern in ("*", ".*"):
        for path in root.rglob(pattern):
            if path in seen:
                continue
            seen.add(path)
            yield path


def rewrite_asset_links(text: str) -> str:
    replacements = {
        'src="styles/': 'src="/styles/',
        "src='styles/": "src='/styles/",
        'href="styles/': 'href="/styles/',
        "href='styles/": "href='/styles/",
        '](styles/': '](/styles/',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def normalize_label_led_lists(text: str) -> str:
    """Add virtual source spacing needed by Python-Markdown before label-led lists."""
    result: list[str] = []
    previous_was_label = False
    in_fence = False

    for line in text.splitlines(keepends=True):
        stripped_line = line.rstrip("\r\n")
        newline = line[len(stripped_line) :]

        if FENCE_RE.match(stripped_line):
            in_fence = not in_fence

        if not in_fence and previous_was_label and LIST_ITEM_RE.match(stripped_line):
            result.append(newline or "\n")

        result.append(line)
        previous_was_label = not in_fence and bool(LABEL_RE.match(stripped_line))

    return "".join(result)


def write_transformed_markdown(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    target.write_text(normalize_label_led_lists(rewrite_asset_links(text)), encoding="utf-8")


def copy_root_files() -> None:
    for rel in ROOT_FILES:
        source = ROOT / rel
        if not source.exists():
            continue
        target = BUILD_DIR / rel
        if source.suffix == ".md":
            write_transformed_markdown(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def copy_doc_tree() -> None:
    for source in sorted(iter_source_files(SOURCE_DOC_DIR)):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        rel = source.relative_to(SOURCE_DOC_DIR)
        if is_excluded_single_site_doc(rel):
            continue

        target = BUILD_DIR / "doc" / normalize_single_site_relative_path(rel)
        if source.suffix == ".md":
            write_transformed_markdown(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def copy_styles() -> None:
    shutil.copytree(STYLES_DIR, BUILD_DIR / "styles", dirs_exist_ok=True)


def main() -> int:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    copy_root_files()
    copy_doc_tree()
    copy_styles()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
