#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'doc'
OUTPUT = DOC / 'COVERAGE.md'

NORMATIVE_STEPS = [
    ('10-ideas', 'Ideas'),
    ('20-vision', 'Vision'),
    ('30-core-values', 'Core Values'),
    ('40-constitution', 'Constitution'),
    ('50-constitutional-ops', 'Constitutional Ops'),
]

PROJECT_STEPS = [
    ('10-challenges', 'Challenges'),
    ('20-memos', 'Memos'),
    ('30-stories', 'Stories'),
    ('40-proposals', 'Proposals'),
    ('50-requirements', 'Requirements'),
    ('60-solutions', 'Solutions'),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def localized_counts(paths: Iterable[Path]) -> tuple[int, int, int]:
    pl = en = shared = 0
    for path in paths:
        s = rel(path)
        if '/pl/' in s or s.endswith('.pl.md'):
            pl += 1
        elif '/en/' in s or s.endswith('.en.md'):
            en += 1
        else:
            shared += 1
    return pl, en, shared


def md_files(dir_path: Path) -> list[Path]:
    return sorted(p for p in dir_path.rglob('*.md') if p.is_file())


def edge_count(files: Iterable[Path], marker: str) -> int:
    count = 0
    for path in files:
        text = path.read_text(encoding='utf-8')
        if marker in text:
            count += 1
    return count


def schema_example_count(examples_dir: Path, suffix: str) -> int:
    return sum(1 for p in examples_dir.glob(f'*.{suffix}.json'))


def schema_doc_name(schema_path: Path) -> Path:
    return DOC / 'schemas-gen' / 'schemas' / f"{schema_path.name.removesuffix('.schema.json')}.md"


def rel_from_output(path: Path) -> str:
    return path.relative_to(OUTPUT.parent).as_posix()


def schema_row(schema_path: Path) -> str:
    data = json.loads(schema_path.read_text(encoding='utf-8'))
    props = data.get('properties', {})
    described = sum(1 for spec in props.values() if isinstance(spec, dict) and spec.get('description'))
    basis = 'yes' if data.get('x-dia-basis') else 'no'
    generated_doc = schema_doc_name(schema_path)
    generated = 'yes' if generated_doc.exists() else 'no'
    stem = schema_path.name.removesuffix('.schema.json')
    valid_examples = schema_example_count(DOC / 'schemas' / 'examples', stem.split('.v1')[0])
    invalid_examples = schema_example_count(DOC / 'schemas' / 'examples' / 'invalid', stem.split('.v1')[0])
    # fallback to suffix-based examples if direct stem match is zero
    if valid_examples == 0 and invalid_examples == 0:
        suffix_map = {
            'proof-of-personhood-attestation.v1': 'proof-of-personhood-attestation',
            'ubc-allocation.v1': 'ubc-allocation',
            'ubc-settlement.v1': 'ubc-settlement',
            'answer-room-metadata.v1': 'room-metadata',
            'transcript-segment.v1': 'segment',
            'transcript-bundle.v1': 'bundle',
        }
        suffix = suffix_map.get(stem, stem)
        valid_examples = schema_example_count(DOC / 'schemas' / 'examples', suffix)
        invalid_examples = schema_example_count(DOC / 'schemas' / 'examples' / 'invalid', suffix)
    return (
        f"| [`{schema_path.name}`]({rel_from_output(generated_doc)}) | `{len(props)}` | `{described}` | `{basis}` | `{generated}` | `{valid_examples}` | `{invalid_examples}` |"
    )


def schema_basis_index(schema_paths: list[Path]) -> dict[str, list[tuple[str, Path]]]:
    index: dict[str, list[tuple[str, Path]]] = {}
    for schema_path in schema_paths:
        data = json.loads(schema_path.read_text(encoding='utf-8'))
        generated_doc = schema_doc_name(schema_path)
        for basis in data.get('x-dia-basis', []):
            index.setdefault(basis, []).append((schema_path.name, generated_doc))
    return index


BASED_ON_RE = re.compile(r"^- `([^`]+)`\s*$")


def project_doc_group(path: Path) -> str | None:
    rel_path = rel(path)
    if not rel_path.startswith('doc/project/'):
        return None
    for step_dir, label in PROJECT_STEPS:
        if f'/project/{step_dir}/' in rel_path:
            return label
    return None


def parse_based_on(path: Path) -> list[Path]:
    refs: list[Path] = []
    in_block = False
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip() == 'Based on:':
            in_block = True
            continue
        if in_block and not line.strip():
            break
        if in_block:
            match = BASED_ON_RE.match(line)
            if match:
                refs.append(ROOT / match.group(1))
    return refs


def project_lineage(seeds: Iterable[Path]) -> dict[str, list[Path]]:
    grouped: dict[str, set[Path]] = {label: set() for _, label in PROJECT_STEPS}
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


def schema_project_lineage(schema_path: Path) -> dict[str, list[Path]]:
    data = json.loads(schema_path.read_text(encoding='utf-8'))
    seeds = [ROOT / item for item in data.get('x-dia-basis', [])]
    return project_lineage(seeds)


normative_files = md_files(DOC / 'normative')
project_files = md_files(DOC / 'project')
schema_files = sorted((DOC / 'schemas').glob('*.schema.json'))

lines: list[str] = [
    '# Workflow Coverage',
    '',
    'Generated coverage snapshot for the current `doc/` structure.',
    '',
    '## Normative Workflow',
    '',
    '| Step | Markdown Files | PL | EN | Shared |',
    '|---|---:|---:|---:|---:|',
]

for step_dir, label in NORMATIVE_STEPS:
    files = md_files(DOC / 'normative' / step_dir)
    pl, en, shared = localized_counts(files)
    lines.append(f'| `{step_dir}` ({label}) | `{len(files)}` | `{pl}` | `{en}` | `{shared}` |')

lines.extend([
    '',
    f'- Total normative markdown files: `{len(normative_files)}`',
    '',
    '## Project Workflow',
    '',
    '| Step | Markdown Files | With `Based on:` |',
    '|---|---:|---:|',
])

for step_dir, label in PROJECT_STEPS:
    files = md_files(DOC / 'project' / step_dir)
    lines.append(f'| `{step_dir}` ({label}) | `{len(files)}` | `{edge_count(files, "Based on:")}` |')

lines.extend([
    '',
    f'- Total project markdown files: `{len(project_files)}`',
    f'- Proposals referencing source material: `{edge_count(md_files(DOC / "project" / "40-proposals"), "Based on:")}` / `{len(md_files(DOC / "project" / "40-proposals"))}`',
    f'- Requirements referencing source material: `{edge_count(md_files(DOC / "project" / "50-requirements"), "Based on:")}` / `{len(md_files(DOC / "project" / "50-requirements"))}`',
    '',
    '## Schema Workflow',
    '',
    '| Schema | Properties | Described Fields | `x-dia-basis` | Generated Doc | Valid Examples | Invalid Examples |',
    '|---|---:|---:|---|---|---:|---:|',
])

for schema_path in schema_files:
    lines.append(schema_row(schema_path))

lines.extend([
    '',
    '## Schema Project Lineage',
    '',
    '| Schema | Requirements | Stories |',
    '|---|---|---|',
])

for schema_path in schema_files:
    lineage = schema_project_lineage(schema_path)

    def format_group(group: str) -> str:
        docs = lineage.get(group, [])
        if not docs:
            return ''
        return ', '.join(f'[`{p.name}`]({rel_from_output(p)})' for p in docs)

    generated_doc = schema_doc_name(schema_path)
    lines.append(
        f"| [`{schema_path.name}`]({rel_from_output(generated_doc)}) | "
        f"{format_group('Requirements')} | "
        f"{format_group('Stories')} |"
    )

basis_index = schema_basis_index(schema_files)
if basis_index:
    lines.extend([
        '',
        '## Schema Traceability',
        '',
        '| Governing Doc | Schemas |',
        '|---|---|',
    ])
    for basis in sorted(basis_index):
        schema_links = ', '.join(
            f'[`{schema_name}`]({rel_from_output(generated_doc)})'
            for schema_name, generated_doc in sorted(basis_index[basis])
        )
        lines.append(
            f"| [`{basis}`]({rel_from_output(ROOT / basis)}) | {schema_links} |"
        )

lines.extend([
    '',
    f'- Canonical schemas: `{len(schema_files)}`',
    f'- Generated schema docs: `{len(list((DOC / "schemas-gen" / "schemas").glob("*.md")))}`',
    f'- Positive examples: `{len(list((DOC / "schemas" / "examples").glob("*.json")))}`',
    f'- Negative examples: `{len(list((DOC / "schemas" / "examples" / "invalid").glob("*.json")))}`',
])

OUTPUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
