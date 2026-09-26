"""Drift check between the P094 refusal table and the operator-task schema enums.

The proposal's refusal table is the source of truth. Every code, stage, retry
class and next action it names must appear in the closed schema vocabularies,
and the schema must not carry a code the table does not name.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = (
    ROOT
    / "doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md"
)
COMMON = ROOT / "doc/schemas/operator-task-common.v1.schema.json"
HEADER = "| Code | Stage | Retry class | Next action |"
CELL = re.compile(r"^`([^`]+)`$")


def refusal_table() -> list[tuple[str, str, str, str]]:
    lines = PROPOSAL.read_text(encoding="utf-8").splitlines()
    start = lines.index(HEADER) + 2
    rows = []
    for line in lines[start:]:
        if not line.startswith("| `"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        code = CELL.match(cells[0])
        action = CELL.match(cells[3])
        if code is None or action is None:
            raise AssertionError(f"malformed refusal row: {line}")
        rows.append((code[1], cells[1], cells[2], action[1]))
    return rows


class RefusalTableDrift(unittest.TestCase):
    def setUp(self) -> None:
        self.defs = json.loads(COMMON.read_text(encoding="utf-8"))["$defs"]
        self.rows = refusal_table()

    def test_codes_match_exactly_and_are_unique(self) -> None:
        codes = [row[0] for row in self.rows]
        self.assertEqual(len(codes), len(set(codes)), "duplicate code in the table")
        self.assertEqual(codes, self.defs["refusalCode"]["enum"])

    def test_stages_retry_classes_and_actions_are_closed_vocabulary(self) -> None:
        for code, stage, retry, action in self.rows:
            with self.subTest(code=code):
                self.assertIn(stage, self.defs["refusalStage"]["enum"])
                self.assertIn(retry, self.defs["retryClass"]["enum"])
                self.assertIn(action, self.defs["nextAction"]["enum"])

    def test_every_next_action_is_used(self) -> None:
        used = {row[3] for row in self.rows}
        self.assertEqual(used, set(self.defs["nextAction"]["enum"]))


if __name__ == "__main__":
    unittest.main()
