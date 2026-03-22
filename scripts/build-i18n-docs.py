#!/usr/bin/env python3

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "i18n-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
LOCALES = ("pl", "en")
LOCALE_SUFFIX_RE = re.compile(r"\.(pl|en)\.md$")

SHARED_ROOT_MARKDOWN = (
    "README.md",
    "DOCS-I18N.md",
    "TRACEABILITY.md",
)


def rewrite_markdown_links(text: str, target: Path, locale_root: Path) -> str:
    text = re.sub(r"([A-Za-z0-9_./-]+)/(pl|en)/([^/]+)\.(pl|en)\.md\b", r"\1/\3.md", text)
    text = re.sub(r"([A-Za-z0-9_./-]+)\.(pl|en)\.md\b", r"\1.md", text)
    styles_prefix = os.path.relpath(locale_root / "styles", target.parent).replace(os.sep, "/")
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


def locale_from_suffix(path: Path) -> str | None:
    match = LOCALE_SUFFIX_RE.search(path.name)
    return match.group(1) if match else None


def locale_from_directory(path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    for part in rel.parts:
        if part in LOCALES:
            return part
    return None


def detect_locale(path: Path) -> str | None:
    suffix_locale = locale_from_suffix(path)
    dir_locale = locale_from_directory(path)
    if suffix_locale and dir_locale and suffix_locale != dir_locale:
        raise ValueError(
            f"Locale mismatch for {path.relative_to(ROOT)}: suffix={suffix_locale}, directory={dir_locale}"
        )
    return suffix_locale or dir_locale


def canonical_name(path: Path) -> str:
    return LOCALE_SUFFIX_RE.sub(".md", path.name)


def normalized_relative_path(path: Path) -> Path:
    rel = path.relative_to(ROOT)
    parts = [part for part in rel.parts if part not in LOCALES]
    normalized = Path(*parts)
    if normalized.suffix == ".md":
        normalized = normalized.with_name(canonical_name(normalized))
    return normalized


def write_transformed_markdown(source: Path, target: Path, locale_root: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    target.write_text(rewrite_markdown_links(text, target, locale_root), encoding="utf-8")


def copy_root_markdown(locale: str) -> None:
    locale_root = BUILD_DIR / locale
    for rel in SHARED_ROOT_MARKDOWN:
        source = ROOT / rel
        target = locale_root / rel
        write_transformed_markdown(source, target, locale_root)


def copy_doc_tree(locale: str) -> None:
    locale_root = BUILD_DIR / locale
    for source in sorted(SOURCE_DOC_DIR.rglob("*")):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        detected = detect_locale(source)
        if detected and detected != locale:
            continue

        target = locale_root / normalized_relative_path(source)
        if source.suffix == ".md":
            write_transformed_markdown(source, target, locale_root)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def copy_styles(locale: str) -> None:
    shutil.copytree(STYLES_DIR, BUILD_DIR / locale / "styles", dirs_exist_ok=True)


def main() -> int:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    for locale in LOCALES:
        copy_root_markdown(locale)
        copy_doc_tree(locale)
        copy_styles(locale)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
