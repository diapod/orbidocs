#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOLUTIONS_DIR = ROOT / "doc" / "project" / "60-solutions"
SCHEMA_DOCS_DIR = ROOT / "doc" / "schemas-gen" / "schemas"


@dataclass
class Token:
    kind: str
    value: str


class EdnParser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def parse(self) -> Any:
        value = self._parse_value()
        self._skip_ws()
        if self.pos != len(self.text):
            raise ValueError(f"Unexpected trailing EDN at position {self.pos}")
        return value

    def _skip_ws(self) -> None:
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch in " \t\r\n,":
                self.pos += 1
                continue
            if ch == ";":
                while self.pos < len(self.text) and self.text[self.pos] != "\n":
                    self.pos += 1
                continue
            break

    def _peek(self) -> str:
        self._skip_ws()
        if self.pos >= len(self.text):
            raise ValueError("Unexpected end of EDN")
        return self.text[self.pos]

    def _consume(self, expected: str) -> None:
        self._skip_ws()
        if self.pos >= len(self.text) or self.text[self.pos] != expected:
            raise ValueError(f"Expected '{expected}' at position {self.pos}")
        self.pos += 1

    def _parse_value(self) -> Any:
        ch = self._peek()
        if ch == "{":
            return self._parse_map()
        if ch == "[":
            return self._parse_vector()
        if ch == '"':
            return self._parse_string()
        if ch == ":":
            return self._parse_keyword()
        return self._parse_symbol()

    def _parse_map(self) -> dict[str, Any]:
        self._consume("{")
        out: dict[str, Any] = {}
        while True:
            self._skip_ws()
            if self._peek() == "}":
                self.pos += 1
                return out
            key = self._parse_value()
            value = self._parse_value()
            out[str(key)] = value

    def _parse_vector(self) -> list[Any]:
        self._consume("[")
        out: list[Any] = []
        while True:
            self._skip_ws()
            if self._peek() == "]":
                self.pos += 1
                return out
            out.append(self._parse_value())

    def _parse_string(self) -> str:
        self.pos += 1
        out: list[str] = []
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch == '"':
                self.pos += 1
                return "".join(out)
            if ch == "\\":
                self.pos += 1
                if self.pos >= len(self.text):
                    raise ValueError("Unterminated EDN escape sequence")
                escaped = self.text[self.pos]
                out.append(
                    {
                        "n": "\n",
                        "r": "\r",
                        "t": "\t",
                        '"': '"',
                        "\\": "\\",
                    }.get(escaped, escaped)
                )
                self.pos += 1
                continue
            out.append(ch)
            self.pos += 1
        raise ValueError("Unterminated EDN string")

    def _parse_keyword(self) -> str:
        self.pos += 1
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] not in " \t\r\n,[]{}":
            self.pos += 1
        return self.text[start:self.pos]

    def _parse_symbol(self) -> Any:
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] not in " \t\r\n,[]{}":
            self.pos += 1
        token = self.text[start:self.pos]
        if token == "true":
            return True
        if token == "false":
            return False
        if token == "nil":
            return None
        return token


def parse_edn(path: Path) -> dict[str, Any]:
    return EdnParser(path.read_text(encoding="utf-8")).parse()


def rel_link(from_path: Path, target: Path) -> str:
    return target.relative_to(from_path.parent).as_posix() if target.is_relative_to(from_path.parent) else str(target.relative_to(from_path.parent))


def rel_link_safe(from_path: Path, target: Path) -> str:
    return Path(
        __import__("os").path.relpath(target, from_path.parent)
    ).as_posix()


def schema_doc_link(from_path: Path, schema_name: str) -> str:
    schema_path = SCHEMA_DOCS_DIR / f"{schema_name}.md"
    return f"[`{schema_name}`]({rel_link_safe(from_path, schema_path)})"


def doc_link(from_path: Path, rel_doc: str) -> str:
    target = ROOT / rel_doc
    return f"[`{Path(rel_doc).name}`]({rel_link_safe(from_path, target)})"


def capability_rows(component_doc: str, caps: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for level_key, level_label in (("must-implement", "must"), ("may-implement", "may")):
        for cap in caps.get(level_key, []):
            rows.append(
                {
                    "component_title": caps.get("component/title", component_doc),
                    "component_doc": component_doc,
                    "component_type": caps.get("component/type", ""),
                    "component_status": caps.get("component/status", ""),
                    "summary": caps.get("summary", ""),
                    "level": level_label,
                    "cap_title": cap.get("title", ""),
                    "kind": cap.get("kind", ""),
                    "status": cap.get("status", ""),
                    "based_on": cap.get("based-on", []),
                    "schemas": cap.get("schemas", []),
                    "depends_on": cap.get("depends-on", []),
                }
            )
    return rows


def humanize_keyword(value: str) -> str:
    return value.replace("-", " ").strip()


def keyword_ref(value: Any) -> str:
    text = str(value)
    if text.startswith(":"):
        text = text[1:]
    return f"`:{text}`"


def load_components() -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []
    for path in sorted(SOLUTIONS_DIR.glob("*-caps.edn")):
        caps = parse_edn(path)
        component_doc = path.name.removesuffix("-caps.edn") + ".md"
        components.append(
            {
                "caps_path": path,
                "component_doc": component_doc,
                "data": caps,
                "rows": capability_rows(component_doc, caps),
            }
        )
    return components


def render_matrix(output_path: Path, title: str, intro: str, labels: dict[str, str], components: list[dict[str, Any]]) -> None:
    lines = [
        "# " + title,
        "",
        intro,
        "",
        "## " + labels["components_heading"],
        "",
        f"| {labels['component']} | {labels['type']} | {labels['status']} | {labels['summary']} |",
        "|---|---|---|---|",
    ]

    for component in components:
        data = component["data"]
        doc_target = SOLUTIONS_DIR / component["component_doc"]
        lines.append(
            f"| [`{data.get('component/title', component['component_doc'])}`]({rel_link_safe(output_path, doc_target)}) | "
            f"`{data.get('component/type', '')}` | "
            f"`{data.get('component/status', '')}` | "
            f"{data.get('summary', '')} |"
        )

    lines.extend(
        [
            "",
            "## " + labels["matrix_heading"],
            "",
            f"| {labels['component']} | {labels['level']} | {labels['capability']} | {labels['kind']} | {labels['based_on']} | {labels['schemas']} | {labels['depends_on']} | {labels['status']} |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )

    all_rows = [row for component in components for row in component["rows"]]
    all_rows.sort(key=lambda row: (row["component_title"], row["level"], row["cap_title"]))

    for row in all_rows:
        component_doc = SOLUTIONS_DIR / row["component_doc"]
        based_on = ", ".join(doc_link(output_path, item) for item in row["based_on"])
        schemas = ", ".join(schema_doc_link(output_path, item) for item in row["schemas"])
        depends_on = ", ".join(keyword_ref(item) for item in row["depends_on"])
        lines.append(
            f"| [`{row['component_title']}`]({rel_link_safe(output_path, component_doc)}) | "
            f"`{labels['must'] if row['level'] == 'must' else labels['may']}` | "
            f"{row['cap_title']} | "
            f"`{row['kind']}` | "
            f"{based_on} | "
            f"{schemas} | "
            f"{depends_on} | "
            f"`{row['status']}` |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    components = load_components()

    render_matrix(
        SOLUTIONS_DIR / "CAPABILITY-MATRIX.en.md",
        title="Solution Capability Matrix",
        intro="Generated from `*-caps.edn` sidecars under `doc/project/60-solutions/`. This matrix is the compact architecture-level view of solution components, their capabilities, protocol/data dependencies, and coarse status.",
        labels={
            "components_heading": "Component Summary",
            "matrix_heading": "Capability Matrix",
            "component": "Component",
            "type": "Type",
            "status": "Status",
            "summary": "Summary",
            "level": "Level",
            "capability": "Capability",
            "kind": "Kind",
            "based_on": "Based On",
            "schemas": "Schemas",
            "depends_on": "Depends On",
            "must": "must",
            "may": "may",
        },
        components=components,
    )

    render_matrix(
        SOLUTIONS_DIR / "CAPABILITY-MATRIX.pl.md",
        title="Macierz zdolności rozwiązań",
        intro="Wygenerowane z sidecarów `*-caps.edn` w `doc/project/60-solutions/`. Ta macierz jest zwartym widokiem architektonicznym komponentów rozwiązania, ich zdolności, zależności protokołowo-danych oraz zgrubnego statusu.",
        labels={
            "components_heading": "Przegląd komponentów",
            "matrix_heading": "Macierz zdolności",
            "component": "Komponent",
            "type": "Typ",
            "status": "Status",
            "summary": "Opis",
            "level": "Poziom",
            "capability": "Zdolność",
            "kind": "Rodzaj",
            "based_on": "Wynika z",
            "schemas": "Schematy",
            "depends_on": "Zależy od",
            "must": "must",
            "may": "may",
        },
        components=components,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
