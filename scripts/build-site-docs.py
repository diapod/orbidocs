#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "site-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
ROOT_MARKDOWN = (
    "AGENTS.md",
)
EXCLUDED_DOCS = {
    Path("normative/10-ideas/COLLABORATION.md"),
}


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


def write_transformed_markdown(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    target.write_text(rewrite_asset_links(text), encoding="utf-8")


def copy_root_markdown() -> None:
    for rel in ROOT_MARKDOWN:
        source = ROOT / rel
        if not source.exists():
            continue
        target = BUILD_DIR / rel
        write_transformed_markdown(source, target)


def copy_doc_tree() -> None:
    for source in sorted(SOURCE_DOC_DIR.rglob("*")):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        rel = source.relative_to(SOURCE_DOC_DIR)
        if rel in EXCLUDED_DOCS:
            continue

        target = BUILD_DIR / "doc" / rel
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

    copy_root_markdown()
    copy_doc_tree()
    copy_styles()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
