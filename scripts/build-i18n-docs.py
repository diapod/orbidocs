#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from fnmatch import fnmatch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "i18n-docs"
SOURCE_DOC_DIR = ROOT / "doc"
STYLES_DIR = ROOT / "styles"
I18N_TEMPLATE_CONFIG = ROOT / "mkdocs.i18n.yml"
I18N_GENERATED_CONFIG = ROOT / "mkdocs.i18n.generated.yml"
LOCALES = ("pl", "en")
LOCALE_SUFFIX_RE = re.compile(r"\.(pl|en)\.md$")
SHARED_ROOT_MARKDOWN: tuple[str, ...] = ()
EXCLUDED_DOCS = {
    Path("normative/10-ideas/COLLABORATION.md"),
}
PROJECT_NAV_MARKERS = {
    "en": (
        "          # BEGIN GENERATED PROJECT NAV EN",
        "          # END GENERATED PROJECT NAV EN",
    ),
    "pl": (
        "          # BEGIN GENERATED PROJECT NAV PL",
        "          # END GENERATED PROJECT NAV PL",
    ),
}
PROJECT_LABELS = {
    "en": {
        "root": "Project",
        "sections": {
            "10-challenges": "Challenges",
            "20-memos": "Memos",
            "30-stories": "Stories",
            "40-proposals": "Proposals",
            "50-requirements": "Requirements",
            "60-solutions": "Solutions",
        },
        "supplementary": "Supplementary",
        "supplementary_children": {
            "ai_manifesto": "AI Manifesto",
        },
    },
    "pl": {
        "root": "Projektowe",
        "sections": {
            "10-challenges": "Wyzwania",
            "20-memos": "Mema i notatki",
            "30-stories": "Stories",
            "40-proposals": "Propozycje",
            "50-requirements": "Wymagania",
            "60-solutions": "Rozwiązania",
        },
        "supplementary": "Dodatkowe",
        "supplementary_children": {
            "ai_manifesto": "Manifest AI",
        },
    },
}
PROJECT_SECTION_ORDER = (
    "10-challenges",
    "20-memos",
    "30-stories",
    "40-proposals",
    "50-requirements",
    "60-solutions",
)
LOCALE_INDEX = {
    "pl": """# Dokumentacja Orbiplex\n\nTo jest polska strona startowa dokumentacji Orbiplex.\n\nJęzyk: [English](/)\n\n## Sekcje\n\n- [Wizja](doc/normative/20-vision/VISION.md)\n- [Wartości podstawowe](doc/normative/30-core-values/CORE-VALUES.md)\n- [Konstytucja](doc/normative/40-constitution/CONSTITUTION.md)\n- [Akty wykonawcze](doc/normative/50-constitutional-ops/README.md)\n- [Workflow projektowy](doc/project/PROJECTS.md)\n- [Pokrycie workflowów](doc/COVERAGE.md)\n""",
    "en": """# Orbiplex Documentation\n\nThis is the English start page for Orbiplex documentation.\n\nLanguage: [Polski](/pl/)\n\n## Sections\n\n- [Vision](doc/normative/20-vision/VISION.md)\n- [Core Values](doc/normative/30-core-values/CORE-VALUES.md)\n- [Constitution](doc/normative/40-constitution/CONSTITUTION.md)\n- [Constitutional Ops](doc/normative/50-constitutional-ops/README.md)\n- [Project Workflow](doc/project/PROJECTS.md)\n- [Workflow Coverage](doc/COVERAGE.md)\n""",
}


def iter_source_files(root: Path):
    seen: set[Path] = set()
    for pattern in ("*", ".*"):
        for path in root.rglob(pattern):
            if path in seen:
                continue
            seen.add(path)
            yield path


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
    for source in sorted(iter_source_files(SOURCE_DOC_DIR)):
        if source.is_dir() or source.name == ".DS_Store":
            continue

        rel = source.relative_to(SOURCE_DOC_DIR)
        if rel in EXCLUDED_DOCS:
            continue

        if rel.parts[:3] == ("project", "60-solutions", "_templates"):
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


def read_markdown_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        _, _, remainder = text.partition("\n---\n")
        if remainder:
            text = remainder

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    return path.stem.replace("-", " ").replace("_", " ").title()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_simple_nav_yaml(path: Path) -> dict[str, list[str]]:
    data: dict[str, list[str]] = {"ignore": [], "nav": []}
    current_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not line.startswith("  ") and stripped.endswith(":"):
            key = stripped[:-1]
            if key in data:
                current_key = key
            else:
                current_key = None
            continue

        if current_key and stripped.startswith("- "):
            value = stripped[2:].strip()
            if value[:1] == value[-1:] and value[:1] in {"'", '"'}:
                value = value[1:-1]
            data[current_key].append(value)

    return data


def load_project_nav_patterns(section_dir: str) -> list[str]:
    nav_file = SOURCE_DOC_DIR / "project" / section_dir / ".nav.yml"
    data = parse_simple_nav_yaml(nav_file)
    patterns = data.get("nav", [])
    return [pattern for pattern in patterns if isinstance(pattern, str)]


def collect_project_section_files(locale: str, section_dir: str) -> list[Path]:
    section_root = BUILD_DIR / locale / "doc" / "project" / section_dir
    patterns = load_project_nav_patterns(section_dir)
    files: list[Path] = []
    seen: set[Path] = set()

    for pattern in patterns:
        matched = sorted(
            path
            for path in section_root.iterdir()
            if path.is_file() and fnmatch(path.name, pattern)
        )
        for path in matched:
            if path not in seen:
                seen.add(path)
                files.append(path)

    return files


def render_project_nav(locale: str) -> str:
    labels = PROJECT_LABELS[locale]
    root_indent = " " * 12
    section_indent = " " * 16
    item_indent = " " * 20

    lines = [
        f"{root_indent}- {labels['root']}:",
        f"{section_indent}- doc/project/PROJECTS.md",
    ]

    for section_dir in PROJECT_SECTION_ORDER:
        section_label = labels["sections"][section_dir]
        files = collect_project_section_files(locale, section_dir)
        lines.append(f"{section_indent}- {section_label}:")
        for index, path in enumerate(files):
            rel = path.relative_to(BUILD_DIR / locale).as_posix()
            if index == 0:
                lines.append(f"{item_indent}- {rel}")
                continue

            title = read_markdown_title(path)
            lines.append(f"{item_indent}- {yaml_string(title)}: {rel}")

    lines.extend(
        [
            f"{section_indent}- {labels['supplementary']}:",
            f"{item_indent}- doc/normative/90-supplementary/SUPPLEMENTARY.md",
            (
                f"{item_indent}- {yaml_string(labels['supplementary_children']['ai_manifesto'])}: "
                "doc/normative/90-supplementary/AI-MANIFESTO.md"
            ),
        ]
    )

    return "\n".join(lines)


def replace_marked_block(text: str, begin_marker: str, end_marker: str, content: str) -> str:
    pattern = re.compile(
        rf"{re.escape(begin_marker)}\n.*?\n{re.escape(end_marker)}",
        flags=re.DOTALL,
    )
    replacement = f"{begin_marker}\n{content}\n{end_marker}"
    return pattern.sub(replacement, text, count=1)


def write_generated_i18n_config() -> None:
    template = I18N_TEMPLATE_CONFIG.read_text(encoding="utf-8")
    rendered = template

    for locale in LOCALES:
        begin_marker, end_marker = PROJECT_NAV_MARKERS[locale]
        rendered = replace_marked_block(
            rendered,
            begin_marker,
            end_marker,
            render_project_nav(locale),
        )

    I18N_GENERATED_CONFIG.write_text(rendered, encoding="utf-8")


def main() -> int:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    for locale in LOCALES:
        write_locale_index(locale)
        copy_root_markdown(locale)
        copy_doc_tree(locale)

    copy_styles()
    write_generated_i18n_config()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
