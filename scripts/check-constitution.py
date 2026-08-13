#!/usr/bin/env python3
"""Validate multilingual DIA Constitution structure and generate its stable-ID index."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION_DIR = ROOT / "doc" / "normative" / "40-constitution"
INDEX_PATH = CONSTITUTION_DIR / "constitution-index.v1.json"
SOURCES = {
    "pl": CONSTITUTION_DIR / "pl" / "CONSTITUTION.pl.md",
    "en": CONSTITUTION_DIR / "en" / "CONSTITUTION.en.md",
}

# Workflow metadata only. This default is used only before the first index exists;
# later runs preserve the designation recorded in the index unless explicitly
# changed with --working-language. It has no normative or interpretive force.
DEFAULT_WORKING_LANGUAGE = "pl"

HEADING_KEYS = {
    "pl": {
        "Moc normatywna i wykładnia": "norm",
        "Główne definicje": "def",
        "Rdzeń nienegocjowalny": "core",
    },
    "en": {
        "Normative Force and Interpretation": "norm",
        "Main Definitions": "def",
        "Non-Negotiable Core": "core",
    },
}

ARTICLE_RE = {
    "pl": re.compile(r"^Artykuł ([IVX]+(?:\.A)?)\. "),
    "en": re.compile(r"^Article ([IVX]+(?:\.A)?)\. "),
}

ROMAN_TO_KEY = {
    "I": "1",
    "II": "2",
    "III": "3",
    "IV": "4",
    "V": "5",
    "VI": "6",
    "VII": "7",
    "VIII": "8",
    "IX": "9",
    "X": "10",
    "X.A": "10a",
    "XI": "11",
    "XII": "12",
    "XIII": "13",
    "XIV": "14",
    "XV": "15",
    "XVI": "16",
}

CLAUSE_RE = re.compile(
    r'^(?P<number>\d+)\. (?:<span id="(?P<id>const:[^"]+)"></span>)?(?P<body>.*)$'
)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
CORE_REF_RE = re.compile(r"`(const:[a-z0-9.-]+)`")
STABLE_REF_RE = re.compile(r"const:[a-z0-9.-]+")

KEYWORDS = {
    "pl": {
        "requirement": re.compile(r"\b(?:MUSI|MUSZĄ)\b"),
        "prohibition": re.compile(r"\bNIE (?:MOŻE|MOGĄ)\b"),
        "strong-requirement": re.compile(r"\b(?:POWINIEN|POWINNA|POWINNO|POWINNY)\b"),
        "permission": re.compile(r"(?<!NIE )\b(?:MOŻE|MOGĄ)\b"),
    },
    "en": {
        "requirement": re.compile(r"\bMUST\b(?! NOT)"),
        "prohibition": re.compile(r"\bMUST NOT\b"),
        "strong-requirement": re.compile(r"\bSHOULD\b"),
        "permission": re.compile(r"\bMAY\b"),
    },
}

LOWERCASE_MODAL = {
    "pl": re.compile(
        r"\b(?:musi|muszą|powinien|powinna|powinno|powinny|może|mogą)\b"
    ),
    "en": re.compile(r"\b(?:must|should|may)\b"),
}


@dataclass(frozen=True)
class Clause:
    stable_id: str
    section: str
    paragraph: str
    heading: str
    text: str
    line: int


def section_key(locale: str, heading: str) -> str | None:
    fixed = HEADING_KEYS[locale].get(heading)
    if fixed:
        return fixed
    match = ARTICLE_RE[locale].match(heading)
    if not match:
        return None
    return f"art-{ROMAN_TO_KEY[match.group(1)]}"


def expected_id(section: str, paragraph: str) -> str:
    return f"const:{section}.{paragraph}"


def add_missing_ids(locale: str, path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    current_section: str | None = None
    changed = False

    for index, line in enumerate(lines):
        if line.startswith("## "):
            heading = line[3:].strip()
            current_section = section_key(locale, heading)
            continue
        if not current_section:
            continue
        match = CLAUSE_RE.match(line.rstrip("\n"))
        if not match or match.group("id"):
            continue
        stable_id = expected_id(current_section, match.group("number"))
        newline = "\n" if line.endswith("\n") else ""
        lines[index] = (
            f'{match.group("number")}. <span id="{stable_id}"></span>'
            f'{match.group("body")}{newline}'
        )
        changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def parse_clauses(locale: str, path: Path) -> tuple[list[Clause], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    clauses: list[Clause] = []
    errors: list[str] = []
    current_section: str | None = None
    current_heading = ""
    active: dict[str, object] | None = None

    def flush() -> None:
        nonlocal active
        if not active:
            return
        clauses.append(
            Clause(
                stable_id=str(active["stable_id"]),
                section=str(active["section"]),
                paragraph=str(active["paragraph"]),
                heading=str(active["heading"]),
                text="\n".join(active["text"]),
                line=int(active["line"]),
            )
        )
        active = None

    for line_number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_section = section_key(locale, current_heading)
            continue

        match = CLAUSE_RE.match(line) if current_section else None
        if match:
            flush()
            stable_id = match.group("id")
            if not stable_id:
                errors.append(f"{path}:{line_number}: missing stable clause id")
                stable_id = expected_id(current_section, match.group("number"))
            active = {
                "stable_id": stable_id,
                "section": current_section,
                "paragraph": match.group("number"),
                "heading": current_heading,
                "text": [match.group("body")],
                "line": line_number,
            }
            continue

        if active is not None:
            active["text"].append(line)

    flush()
    return clauses, errors


def without_inline_code(text: str) -> str:
    return INLINE_CODE_RE.sub("", text)


def keyword_families(locale: str, text: str) -> list[str]:
    visible = without_inline_code(text)
    return sorted(
        family for family, pattern in KEYWORDS[locale].items() if pattern.search(visible)
    )


def machine_identifier(token: str) -> bool:
    return bool(
        token.startswith("const:")
        or re.search(r"\.v\d+$", token)
        or "_" in token
        or re.search(r"-(?:id|identity|ref)$", token)
    )


def schema_exists(token: str) -> bool:
    return (ROOT / "doc" / "schemas" / f"{token}.schema.json").is_file()


def validate_locale(
    locale: str, path: Path, clauses: list[Clause]
) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    ids = [clause.stable_id for clause in clauses]

    duplicates = sorted({stable_id for stable_id in ids if ids.count(stable_id) > 1})
    for stable_id in duplicates:
        errors.append(f"{path}: duplicate stable id {stable_id}")

    for clause in clauses:
        if not clause.stable_id.startswith(f"const:{clause.section}."):
            errors.append(
                f"{path}:{clause.line}: {clause.stable_id} belongs to "
                f"{clause.section}, expected prefix const:{clause.section}."
            )

    for line_number, line in enumerate(text.splitlines(), start=1):
        visible = without_inline_code(line)
        match = LOWERCASE_MODAL[locale].search(visible)
        if match:
            errors.append(
                f"{path}:{line_number}: lowercase modal '{match.group(0)}' has no "
                "declared normative force"
            )

    defined_tokens: set[str] = set()
    for clause in clauses:
        if clause.section == "def":
            defined_tokens.update(INLINE_CODE_RE.findall(clause.text))

    for token in INLINE_CODE_RE.findall(text):
        if not machine_identifier(token):
            continue
        if token.startswith("const:"):
            if token not in ids:
                errors.append(f"{path}: unknown stable clause reference {token}")
            continue
        if token in defined_tokens or schema_exists(token):
            continue
        errors.append(
            f"{path}: machine identifier `{token}` is neither defined in Main "
            "Definitions nor incorporated by an existing canonical schema"
        )

    return errors


def core_refs(clauses: list[Clause]) -> set[str]:
    refs: set[str] = {clause.stable_id for clause in clauses if clause.section == "core"}
    for clause in clauses:
        if clause.section == "core":
            refs.update(CORE_REF_RE.findall(clause.text))
    return refs


def compare_locales(parsed: dict[str, list[Clause]]) -> list[str]:
    errors: list[str] = []
    for left_locale, right_locale in combinations(parsed, 2):
        left = parsed[left_locale]
        right = parsed[right_locale]
        left_ids = [clause.stable_id for clause in left]
        right_ids = [clause.stable_id for clause in right]

        if left_ids != right_ids:
            missing_right = [
                stable_id for stable_id in left_ids if stable_id not in right_ids
            ]
            missing_left = [
                stable_id for stable_id in right_ids if stable_id not in left_ids
            ]
            errors.append(
                f"{left_locale}/{right_locale} stable-id sequence differs; "
                f"missing in {right_locale}={missing_right}, "
                f"missing in {left_locale}={missing_left}"
            )
            continue

        for left_clause, right_clause in zip(left, right, strict=True):
            if (left_clause.section, left_clause.paragraph) != (
                right_clause.section,
                right_clause.paragraph,
            ):
                errors.append(
                    f"{left_clause.stable_id}: {left_locale} location "
                    f"{left_clause.section}.{left_clause.paragraph} differs from "
                    f"{right_locale} {right_clause.section}.{right_clause.paragraph}"
                )
            left_keywords = keyword_families(left_locale, left_clause.text)
            right_keywords = keyword_families(right_locale, right_clause.text)
            if left_keywords != right_keywords:
                errors.append(
                    f"{left_clause.stable_id}: normative keyword families differ: "
                    f"{left_locale}={left_keywords}, {right_locale}={right_keywords}"
                )

        left_core = core_refs(left)
        right_core = core_refs(right)
        if left_core != right_core:
            errors.append(
                f"{left_locale}/{right_locale} non-negotiable core differs: "
                f"only {left_locale}={sorted(left_core - right_core)}, "
                f"only {right_locale}={sorted(right_core - left_core)}"
            )
    return errors


def validate_stable_references(valid_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for path in sorted((ROOT / "doc").rglob("*")):
        if not path.is_file() or path.suffix not in {".json", ".md"}:
            continue
        if path == INDEX_PATH:
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for stable_id in STABLE_REF_RE.findall(line):
                if stable_id not in valid_ids:
                    errors.append(
                        f"{path}:{line_number}: unknown Constitution clause "
                        f"reference {stable_id}"
                    )
    return errors


def text_digest(clause: Clause) -> str:
    return "sha256:" + hashlib.sha256(clause.text.encode("utf-8")).hexdigest()


def resolve_working_language(requested: str | None) -> str:
    if requested is not None:
        return requested
    if not INDEX_PATH.is_file():
        return DEFAULT_WORKING_LANGUAGE
    try:
        existing = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_WORKING_LANGUAGE
    recorded = existing.get("editorial/current-working-language")
    if isinstance(recorded, str) and recorded in SOURCES:
        return recorded
    return DEFAULT_WORKING_LANGUAGE


def make_index(
    parsed: dict[str, list[Clause]], working_language: str
) -> dict[str, object]:
    ordering_clauses = parsed[working_language]
    clauses_by_locale = {
        locale: {clause.stable_id: clause for clause in clauses}
        for locale, clauses in parsed.items()
    }
    core = core_refs(ordering_clauses)
    entries: list[dict[str, object]] = []
    for ordering_clause in ordering_clauses:
        entries.append(
            {
                "id": ordering_clause.stable_id,
                "section": ordering_clause.section,
                "paragraph": ordering_clause.paragraph,
                "normative/keywords": keyword_families(
                    working_language, ordering_clause.text
                ),
                "core": ordering_clause.stable_id in core,
                "language/locations": {
                    locale: {
                        "path": str(SOURCES[locale].relative_to(ROOT)),
                        "heading": clauses_by_locale[locale][
                            ordering_clause.stable_id
                        ].heading,
                        "line": clauses_by_locale[locale][
                            ordering_clause.stable_id
                        ].line,
                        "text/digest": text_digest(
                            clauses_by_locale[locale][ordering_clause.stable_id]
                        ),
                    }
                    for locale in SOURCES
                },
            }
        )

    return {
        "schema/v": 1,
        "editorial/current-working-language": working_language,
        "editorial/working-language-has-interpretive-priority": False,
        "editorial/working-language-may-change": True,
        "language/variants": list(SOURCES),
        "language/normative-force": "equal",
        "language/semantically-self-contained": True,
        "language/semantic-equivalence-validation": "human-review-required",
        "metrics": {
            "clauses": len(entries),
            "core/clauses": len(core),
            "language/structural-divergences": 0,
            "undefined-modal-clauses": 0,
        },
        "clauses": entries,
    }


def serialized_index(index: dict[str, object]) -> str:
    return json.dumps(index, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-ids",
        action="store_true",
        help="insert missing stable ids derived from current visible clause numbers",
    )
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="write the canonical constitution-index.v1.json after validation",
    )
    parser.add_argument(
        "--working-language",
        choices=tuple(SOURCES),
        help=(
            "set revision workflow metadata while writing or checking the index; "
            "this does not grant interpretive priority"
        ),
    )
    args = parser.parse_args()

    if args.write_ids:
        for locale, path in SOURCES.items():
            add_missing_ids(locale, path)

    parsed: dict[str, list[Clause]] = {}
    errors: list[str] = []
    for locale, path in SOURCES.items():
        clauses, parse_errors = parse_clauses(locale, path)
        parsed[locale] = clauses
        errors.extend(parse_errors)
        errors.extend(validate_locale(locale, path, clauses))
    errors.extend(compare_locales(parsed))
    valid_ids = set.intersection(
        *({clause.stable_id for clause in clauses} for clauses in parsed.values())
    )
    errors.extend(validate_stable_references(valid_ids))

    if errors:
        for error in errors:
            print(f"constitution-check: {error}", file=sys.stderr)
        return 1

    working_language = resolve_working_language(args.working_language)
    index = make_index(parsed, working_language)
    rendered = serialized_index(index)
    if args.write_index:
        INDEX_PATH.write_text(rendered, encoding="utf-8")
    elif not INDEX_PATH.is_file():
        print(f"constitution-check: missing generated index {INDEX_PATH}", file=sys.stderr)
        return 1
    elif INDEX_PATH.read_text(encoding="utf-8") != rendered:
        print(
            "constitution-check: generated index is stale; run "
            "scripts/check-constitution.py --write-index",
            file=sys.stderr,
        )
        return 1

    print(
        f"constitution-check: ok ({len(parsed[working_language])} clauses, "
        f"{len(core_refs(parsed[working_language]))} core clauses)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
