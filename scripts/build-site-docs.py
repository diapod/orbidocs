#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "site-docs"
SOURCE_DOC_DIR = ROOT / "doc"
ROOT_MARKDOWN = (
    "README.md",
    "DOCS-I18N.md",
    "TRACEABILITY.md",
    "AGENTS.md",
)


def copy_root_markdown() -> None:
    for rel in ROOT_MARKDOWN:
        source = ROOT / rel
        target = BUILD_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_doc_tree() -> None:
    target = BUILD_DIR / "doc"
    shutil.copytree(SOURCE_DOC_DIR, target, dirs_exist_ok=True)


def main() -> int:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    copy_root_markdown()
    copy_doc_tree()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
