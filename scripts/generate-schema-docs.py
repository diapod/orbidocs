#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - keeps scripts usable on Python 3.10.
    tomllib = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "doc" / "schemas"
GENERATED_DIR = ROOT / "doc" / "schemas-gen"
GENERATED_SCHEMAS_DIR = GENERATED_DIR / "schemas"
REFS_PATH = ROOT / "doc" / "_refs.toml"


def load_refs() -> dict[str, dict[str, str]]:
    if not REFS_PATH.exists():
        return {}
    if tomllib is not None:
        with REFS_PATH.open("rb") as fh:
            data = tomllib.load(fh)
        return {key: value for key, value in data.items() if isinstance(value, dict)}
    data: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for raw_line in REFS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = {}
            data[line[1:-1]] = current
            continue
        if current is not None and "=" in line:
            key, value = line.split("=", 1)
            current[key.strip()] = value.strip().strip('"')
    return {key: value for key, value in data.items() if isinstance(value, dict)}


REFS = load_refs()


def resolve_doc_ref(ref: str) -> Path:
    entry = REFS.get(ref)
    if entry and entry.get("path"):
        return ROOT / entry["path"]
    return ROOT / ref


def display_doc_ref(ref: str) -> str:
    entry = REFS.get(ref)
    if entry:
        return entry.get("short") or ref
    return ref


def slugify(value: str) -> str:
    out = []
    prev_dash = False
    for ch in value:
        if ch.isalnum():
            out.append(ch.lower())
            prev_dash = False
        else:
            if not prev_dash:
                out.append("-")
                prev_dash = True
    slug = "".join(out).strip("-")
    return slug or "item"



def rel_link(from_dir: Path, target: Path) -> str:
    return os.path.relpath(target, from_dir).replace(os.sep, "/")



def json_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return f"ref: `{schema['$ref']}`"
    if "const" in schema:
        return f"const: `{schema['const']}`"
    if "enum" in schema:
        enum_vals = ", ".join(f"`{v}`" for v in schema["enum"])
        return f"enum: {enum_vals}"
    t = schema.get("type")
    if isinstance(t, list):
        return " | ".join(str(x) for x in t)
    if t:
        return str(t)
    return "unspecified"



def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def humanize_compound_token(token: str) -> str:
    token = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", token)
    token = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", token)
    return token


def humanize_title(title: str) -> str:
    stopwords = {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to"}
    words: list[str] = []
    for part in title.split():
        for idx, word in enumerate(humanize_compound_token(part).split()):
            overall_idx = len(words)
            if word.isupper():
                words.append(word)
            elif re.fullmatch(r"v\d+", word, re.IGNORECASE):
                words.append(word.lower())
            elif overall_idx > 0 and word.lower() in stopwords:
                words.append(word.lower())
            else:
                words.append(word[:1].upper() + word[1:].lower())
    return " ".join(words)



def basis_lines(basis: Any, from_dir: Path) -> str:
    if not basis:
        return ""
    links = []
    for item in basis:
        target = resolve_doc_ref(item)
        href = rel_link(from_dir, target)
        links.append(f"- [`{display_doc_ref(item)}`]({href})")
    return "\n".join(links)


BASED_ON_RE = re.compile(r"^- `([^`]+)`\s*$")


PROJECT_GROUPS = [
    ("50-requirements", "Requirements"),
    ("40-proposals", "Proposals"),
    ("30-stories", "Stories"),
    ("20-memos", "Memos"),
    ("10-challenges", "Challenges"),
    ("60-solutions", "Solutions"),
]

DISPLAY_PROJECT_GROUPS = ["Requirements", "Stories"]


def parse_based_on(path: Path) -> list[Path]:
    refs: list[Path] = []
    in_block = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "Based on:":
            in_block = True
            continue
        if in_block and not line.strip():
            break
        if in_block:
            match = BASED_ON_RE.match(line)
            if match:
                refs.append(ROOT / match.group(1))
    return refs


def project_doc_group(path: Path) -> str | None:
    rel_path = path.relative_to(ROOT).as_posix()
    if not rel_path.startswith("doc/project/"):
        return None
    for step_dir, label in PROJECT_GROUPS:
        if f"/project/{step_dir}/" in rel_path:
            return label
    return None


def project_lineage(seeds: list[Path]) -> dict[str, list[Path]]:
    grouped: dict[str, set[Path]] = {label: set() for _, label in PROJECT_GROUPS}
    stack = [seed for seed in seeds if project_doc_group(seed)]
    visited: set[Path] = set()

    while stack:
        current = stack.pop()
        if current in visited or not current.exists():
            continue
        visited.add(current)
        group = project_doc_group(current)
        if group:
            grouped[group].add(current)
        for ref in parse_based_on(current):
            if project_doc_group(ref):
                stack.append(ref)

    return {group: sorted(paths) for group, paths in grouped.items() if paths}


def project_lineage_lines(seeds: list[Path], from_dir: Path) -> str:
    lineage = project_lineage(seeds)
    if not lineage:
        return ""
    lines = ["## Project Lineage", ""]
    for label in DISPLAY_PROJECT_GROUPS:
        docs = lineage.get(label, [])
        if not docs:
            continue
        lines.append(f"### {label}")
        lines.append("")
        for doc in docs:
            href = rel_link(from_dir, doc)
            lines.append(f"- [`{doc.relative_to(ROOT).as_posix()}`]({href})")
        lines.append("")
    return "\n".join(lines).rstrip()



def render_field_section(name: str, spec: dict[str, Any], required: bool, from_dir: Path) -> str:
    anchor = slugify(name)
    lines = [
        f'<a id="field-{anchor}"></a>',
        f"## `{name}`",
        "",
        f"- Required: `{'yes' if required else 'no'}`",
        f"- Shape: {json_type(spec)}",
    ]
    desc = spec.get("description")
    if desc:
        lines.extend(["", desc])
    basis = spec.get("x-dia-basis")
    if basis:
        lines.extend(["", "Governing basis:", basis_lines(basis, from_dir)])
    comment = spec.get("$comment")
    if comment:
        lines.extend(["", f"Maintainer note: {comment}"])
    return "\n".join(lines)



def render_def_section(name: str, spec: dict[str, Any], from_dir: Path) -> str:
    anchor = slugify(name)
    lines = [
        f'<a id="def-{anchor}"></a>',
        f"## `$defs.{name}`",
        "",
        f"- Shape: {json_type(spec)}",
    ]
    desc = spec.get("description")
    if desc:
        lines.extend(["", desc])
    basis = spec.get("x-dia-basis")
    if basis:
        lines.extend(["", "Governing basis:", basis_lines(basis, from_dir)])
    return "\n".join(lines)



def summarize_condition(index: int, condition: dict[str, Any]) -> str:
    parts = [f"### Rule {index}"]
    if_block = condition.get("if")
    then_block = condition.get("then")
    if if_block:
        parts.extend(["", "When:", "", "```json", json.dumps(if_block, indent=2, ensure_ascii=False), "```"])
    if then_block:
        parts.extend(["", "Then:", "", "```json", json.dumps(then_block, indent=2, ensure_ascii=False), "```"])
    if not if_block and not then_block:
        parts.extend(["", "Constraint:", "", "```json", json.dumps(condition, indent=2, ensure_ascii=False), "```"])
    return "\n".join(parts)



def generate_schema_doc(schema_path: Path) -> tuple[str, str]:
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    schema_rel_to_dir = schema_path.relative_to(SCHEMAS_DIR).as_posix()
    doc_stem = schema_path.name.removesuffix(".schema.json")
    out_path = GENERATED_SCHEMAS_DIR / f"{doc_stem}.md"
    from_dir = out_path.parent

    title = humanize_title(data.get("title", schema_path.name))
    description = data.get("description", "")
    schema_rel = rel_link(from_dir, schema_path)
    required = set(data.get("required", []))
    properties = data.get("properties", {})
    defs = data.get("$defs", {})
    all_of = data.get("allOf", [])
    basis = data.get("x-dia-basis", [])
    lineage = project_lineage_lines([resolve_doc_ref(item) for item in basis], from_dir)

    lines = [
        f"# {title}",
        "",
        f"Source schema: [`doc/schemas/{schema_rel_to_dir}`]({schema_rel})",
        "",
    ]
    if description:
        lines.extend([description, ""])
    if basis:
        lines.extend(["## Governing Basis", "", basis_lines(basis, from_dir), ""])
    if lineage:
        lines.extend([lineage, ""])

    lines.extend(["## Fields", "", "| Field | Required | Shape | Description |", "|---|---|---|---|"])
    for name, spec in properties.items():
        anchor = slugify(name)
        desc = md_escape(spec.get("description", ""))
        lines.append(
            f"| [`{name}`](#field-{anchor}) | `{'yes' if name in required else 'no'}` | {md_escape(json_type(spec))} | {desc} |"
        )

    if defs:
        lines.extend(["", "## Definitions", "", "| Definition | Shape | Description |", "|---|---|---|"])
        for name, spec in defs.items():
            anchor = slugify(name)
            desc = md_escape(spec.get("description", ""))
            lines.append(f"| [`{name}`](#def-{anchor}) | {md_escape(json_type(spec))} | {desc} |")

    if all_of:
        lines.extend(["", "## Conditional Rules", ""])
        for idx, cond in enumerate(all_of, start=1):
            lines.extend([summarize_condition(idx, cond), ""])

    lines.extend(["## Field Semantics", ""])
    for name, spec in properties.items():
        lines.extend([render_field_section(name, spec, name in required, from_dir), ""])

    if defs:
        lines.extend(["## Definition Semantics", ""])
        for name, spec in defs.items():
            lines.extend([render_def_section(name, spec, from_dir), ""])

    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return schema_rel_to_dir, out_path.name



def generate_index(rows: list[tuple[str, str]]) -> None:
    out_path = GENERATED_DIR / "schema-index.md"
    lines = [
        "# Schema Index",
        "",
        "This page is generated from canonical JSON Schema files under `/doc/schemas`.",
        "",
        "| Schema | Generated Doc | Governing Basis |",
        "|---|---|---|",
    ]
    for schema_name, doc_name in sorted(rows):
        schema_path = SCHEMAS_DIR / schema_name
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        basis = data.get("x-dia-basis", [])
        if basis:
          basis_links = ", ".join(
              f"[`{display_doc_ref(item)}`]({rel_link(out_path.parent, resolve_doc_ref(item))})" for item in basis
          )
        else:
          basis_links = ""
        lines.append(
            f"| [`{schema_name}`](../schemas/{schema_name}) | [`{doc_name}`](schemas/{doc_name}) | {basis_links} |"
        )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def main() -> int:
    GENERATED_SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str]] = []
    for schema_path in sorted(SCHEMAS_DIR.rglob("*.schema.json")):
        rows.append(generate_schema_doc(schema_path))
    generate_index(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
