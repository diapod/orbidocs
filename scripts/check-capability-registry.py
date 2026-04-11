#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NODE_CAPABILITY = ROOT.parent / "node" / "capability" / "src" / "lib.rs"
REGISTRY_EN = ROOT / "doc" / "project" / "60-solutions" / "CAPABILITY-REGISTRY.en.md"
REGISTRY_PL = ROOT / "doc" / "project" / "60-solutions" / "CAPABILITY-REGISTRY.pl.md"


CONST_RE = re.compile(r'pub const ([A-Z0-9_]+): &str = "([^"]+)";')
MAP_RE = re.compile(
    r"pub static CAPABILITY_ADVERTISEMENT_MAP: &\[\(&str, &str\)\] = &\[(.*?)\];",
    re.S,
)
ENTRY_RE = re.compile(r'\(\s*([A-Z0-9_]+|"[^"]+")\s*,\s*"([^"]+)"\s*\)')


def load_runtime_capabilities(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    consts = {name: value for name, value in CONST_RE.findall(text)}
    match = MAP_RE.search(text)
    if not match:
        raise ValueError(f"Could not find CAPABILITY_ADVERTISEMENT_MAP in {path}")
    mapping: dict[str, str] = {}
    for raw_key, wire_name in ENTRY_RE.findall(match.group(1)):
        if raw_key.startswith('"'):
            capability_id = raw_key.strip('"')
        else:
            capability_id = consts.get(raw_key)
            if capability_id is None:
                raise ValueError(
                    f"Map entry key {raw_key!r} is not a string literal and not a known const"
                )
        mapping[capability_id] = wire_name
    return mapping


def parse_registry_table(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    marker = "## Capability Registry"
    if marker not in text:
        raise ValueError(f"Could not find {marker!r} in {path}")
    section = text.split(marker, 1)[1]
    lines = section.splitlines()
    rows: dict[str, str] = {}
    in_table = False
    for line in lines:
        if line.startswith("| capability_id |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        capability = cells[0].strip("`")
        wire_name = cells[1].strip("`")
        rows[capability] = wire_name
    if not rows:
        raise ValueError(f"No registry rows found in {path}")
    return rows


def compare_registry(runtime: dict[str, str], registry: dict[str, str], path: Path) -> list[str]:
    errors: list[str] = []
    runtime_keys = set(runtime)
    registry_keys = set(registry)

    missing = sorted(runtime_keys - registry_keys)
    extra = sorted(registry_keys - runtime_keys)

    if missing:
        errors.append(
            f"{path.name}: missing capability ids: {', '.join(missing)}"
        )
    if extra:
        errors.append(
            f"{path.name}: extra capability ids not present in node runtime: {', '.join(extra)}"
        )

    for capability_id in sorted(runtime_keys & registry_keys):
        expected = runtime[capability_id]
        actual = registry[capability_id]
        if expected != actual:
            errors.append(
                f"{path.name}: wire name mismatch for {capability_id!r}: expected {expected!r}, got {actual!r}"
            )
    return errors


def main() -> int:
    runtime = load_runtime_capabilities(NODE_CAPABILITY)
    errors: list[str] = []
    for registry_path in (REGISTRY_EN, REGISTRY_PL):
        registry = parse_registry_table(registry_path)
        errors.extend(compare_registry(runtime, registry, registry_path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("ok capability registry is in sync with node runtime capability map")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
