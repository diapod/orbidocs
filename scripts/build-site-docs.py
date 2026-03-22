#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "site-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
ROOT_MARKDOWN = (
    "README.md",
    "DOCS-I18N.md",
    "TRACEABILITY.md",
    "AGENTS.md",
)


def rewrite_asset_links(text: str, target: Path, site_root: Path) -> str:
    styles_prefix = os.path.relpath(site_root / "styles", target.parent).replace(os.sep, "/")
    replacements = {
        'src="styles/': f'src="{styles_prefix}/',
        "src='styles/": f"src='{styles_prefix}/",
        'href="styles/': f'href="{styles_prefix}/',
        "href='styles/": f"href='{styles_prefix}/",
        '](styles/': f']({styles_prefix}/',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def write_transformed_markdown(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    target.write_text(rewrite_asset_links(text, target, BUILD_DIR), encoding="utf-8")


def copy_root_markdown() -> None:
    for rel in ROOT_MARKDOWN:
        source = ROOT / rel
        target = BUILD_DIR / rel
        write_transformed_markdown(source, target)


def copy_doc_tree() -> None:
    for source in sorted(SOURCE_DOC_DIR.rglob("*")):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        target = BUILD_DIR / source.relative_to(ROOT)
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
