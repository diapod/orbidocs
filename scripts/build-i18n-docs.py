#!/usr/bin/env python3

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "i18n-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
LOCALES = ("pl", "en")
LOCALE_SUFFIX_RE = re.compile(r"\.(pl|en)\.md$")
SHARED_ROOT_MARKDOWN: tuple[str, ...] = ()
EXCLUDED_DOCS = {
    Path("normative/10-ideas/COLLABORATION.md"),
}
LOCALE_INDEX = {
    "pl": """# Dokumentacja Orbiplex\n\nTo jest polska strona startowa dokumentacji Orbiplex.\n\nJęzyk: [English](/)\n\n## Sekcje\n\n- [Wizja](doc/normative/20-vision/VISION.md)\n- [Wartości podstawowe](doc/normative/30-core-values/CORE-VALUES.md)\n- [Konstytucja](doc/normative/40-constitution/CONSTITUTION.md)\n- [Akty wykonawcze](doc/normative/50-constitutional-ops/README.md)\n- [Workflow projektowy](doc/project/PROJECTS.md)\n- [Pokrycie workflowów](doc/COVERAGE.md)\n""",
    "en": """# Orbiplex Documentation\n\nThis is the English start page for Orbiplex documentation.\n\nLanguage: [Polski](/pl/)\n\n## Sections\n\n- [Vision](doc/normative/20-vision/VISION.md)\n- [Core Values](doc/normative/30-core-values/CORE-VALUES.md)\n- [Constitution](doc/normative/40-constitution/CONSTITUTION.md)\n- [Constitutional Ops](doc/normative/50-constitutional-ops/README.md)\n- [Project Workflow](doc/project/PROJECTS.md)\n- [Workflow Coverage](doc/COVERAGE.md)\n""",
}


def rewrite_markdown_links(text: str) -> str:
    text = re.sub(r"([A-Za-z0-9_./-]+)/(pl|en)/([^/]+)\.(pl|en)\.md\b", r"\1/\3.md", text)
    text = re.sub(r"([A-Za-z0-9_./-]+)\.(pl|en)\.md\b", r"\1.md", text)
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


def locale_from_suffix(path: Path) -> str | None:
    match = LOCALE_SUFFIX_RE.search(path.name)
    return match.group(1) if match else None


def locale_from_directory(path: Path) -> str | None:
    rel = path.relative_to(SOURCE_DOC_DIR)
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
    rel = path.relative_to(SOURCE_DOC_DIR)
    parts = [part for part in rel.parts if part not in LOCALES]
    normalized = Path(*parts)
    if normalized.suffix == ".md":
        normalized = normalized.with_name(canonical_name(normalized))
    return Path("doc") / normalized


def write_transformed_markdown(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    target.write_text(rewrite_markdown_links(text), encoding="utf-8")


def write_locale_index(locale: str) -> None:
    target = BUILD_DIR / locale / "index.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(LOCALE_INDEX[locale], encoding="utf-8")


def copy_root_markdown(locale: str) -> None:
    locale_root = BUILD_DIR / locale
    for rel in SHARED_ROOT_MARKDOWN:
        source = ROOT / rel
        if not source.exists():
            continue
        target = locale_root / rel
        write_transformed_markdown(source, target)


def copy_doc_tree(locale: str) -> None:
    locale_root = BUILD_DIR / locale
    for source in sorted(SOURCE_DOC_DIR.rglob("*")):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        rel = source.relative_to(SOURCE_DOC_DIR)
        if rel in EXCLUDED_DOCS:
            continue

        detected = detect_locale(source)
        if detected and detected != locale:
            continue

        target = locale_root / normalized_relative_path(source)
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

    for locale in LOCALES:
        write_locale_index(locale)
        copy_root_markdown(locale)
        copy_doc_tree(locale)

    copy_styles()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
