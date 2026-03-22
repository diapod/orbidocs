#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


ROOT = Path("/Users/siefca/kody/FREE/AI/orbiplex/orbidocs")
SCHEMAS_DIR = ROOT / "doc" / "schemas"
GENERATED_DIR = ROOT / "doc" / "schemas-gen"
GENERATED_SCHEMAS_DIR = GENERATED_DIR / "schemas"


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



def basis_lines(basis: Any, from_dir: Path) -> str:
    if not basis:
        return ""
    links = []
    for item in basis:
        target = ROOT / item
        href = rel_link(from_dir, target)
        links.append(f"- [`{item}`]({href})")
    return "\n".join(links)



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
    doc_stem = schema_path.name.removesuffix(".schema.json")
    out_path = GENERATED_SCHEMAS_DIR / f"{doc_stem}.md"
    from_dir = out_path.parent

    title = data.get("title", schema_path.name)
    description = data.get("description", "")
    schema_rel = rel_link(from_dir, schema_path)
    required = set(data.get("required", []))
    properties = data.get("properties", {})
    defs = data.get("$defs", {})
    all_of = data.get("allOf", [])
    basis = data.get("x-dia-basis", [])

    lines = [
        f"# {title}",
        "",
        f"Source schema: [`doc/schemas/{schema_path.name}`]({schema_rel})",
        "",
    ]
    if description:
        lines.extend([description, ""])
    if basis:
        lines.extend(["## Governing Basis", "", basis_lines(basis, from_dir), ""])

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
    return schema_path.name, out_path.name



def generate_index(rows: list[tuple[str, str]]) -> None:
    out_path = GENERATED_DIR / "schema-index.md"
    lines = [
        "# Schema Index",
        "",
        "This page is generated from canonical JSON Schema files under `/doc/schemas`.",
        "",
        "| Schema | Generated Doc |",
        "|---|---|",
    ]
    for schema_name, doc_name in sorted(rows):
        lines.append(
            f"| [`{schema_name}`](../schemas/{schema_name}) | [`{doc_name}`](schemas/{doc_name}) |"
        )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def main() -> int:
    GENERATED_SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str]] = []
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        rows.append(generate_schema_doc(schema_path))
    generate_index(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
