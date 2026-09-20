from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import capability_registry_docs as docs


def entry(name: str, owner: str = "test-owner", **flags: bool) -> dict:
    values = dict.fromkeys((*docs.OTHER_FLAGS, "dispatchable", "host-route"), False)
    values.update({"dispatchable": True, **flags})
    surfaces = ["host-local"] if values["dispatchable"] or values["host-route"] else []
    if any(
        values[key]
        for key in ("advertisable", "passport/eligible", "federated-discovery")
    ):
        surfaces.append("federated")
    return {
        "capability/id": name,
        "wire/name": f"host/{name}",
        "owner": owner,
        "status": "active",
        "surfaces": surfaces,
        "flags": values,
        "docs": {"human-registry": False},
    }


def document() -> str:
    return (
        f"# Manual title\n\n{docs.BEGIN}\nold contents\n{docs.END}\n\nManual ending.\n"
    )


class RenderingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = {name: entry(name) for name in ("beta.read", "alpha.read")}

    def test_includes_all_host_entries_and_preserves_lifecycle_status(self) -> None:
        self.registry["alpha.read"]["status"] = "reserved"
        remote = entry("remote.read")
        remote["surfaces"] = ["federated"]
        self.registry["remote.read"] = remote
        for language in docs.LABELS:
            rendered = docs.render_host_catalogue(self.registry, language)
            self.assertIn("**2** host-local / **3**", rendered)
            self.assertIn("<code>reserved</code>", rendered)
            self.assertIn("<code>alpha.read</code>", rendered)
            self.assertNotIn("<code>remote.read</code>", rendered)

    def test_stable_owner_and_id_sorting_independent_of_input_order(self) -> None:
        self.registry["beta.read"]["owner"] = "a-owner"
        rendered = docs.render_host_catalogue(self.registry, "en")
        self.assertEqual(
            rendered,
            docs.render_host_catalogue(
                dict(reversed(list(self.registry.items()))), "en"
            ),
        )
        self.assertLess(
            rendered.index("### <code>a-owner"), rendered.index("### <code>test-owner")
        )
        self.registry["beta.read"]["owner"] = "test-owner"
        rendered = docs.render_host_catalogue(self.registry, "en")
        self.assertLess(
            rendered.index("<code>alpha.read"), rendered.index("<code>beta.read")
        )

    def test_languages_have_identical_data_rows(self) -> None:
        rows = lambda language: [
            line
            for line in docs.render_host_catalogue(self.registry, language).splitlines()
            if line.startswith("| <code>")
        ]
        self.assertEqual(rows("pl"), rows("en"))

    def test_both_languages_expose_a_stable_anchor(self) -> None:
        for language in docs.LABELS:
            self.assertEqual(
                1,
                docs.render_host_catalogue(self.registry, language).count(
                    '<a id="host-local-capabilities"></a>'
                ),
            )

    def test_all_flags_and_both_surfaces_are_visible(self) -> None:
        item = self.registry["alpha.read"]
        item["flags"] = dict.fromkeys(item["flags"], True)
        item["flags"]["dispatchable"] = False
        item["surfaces"] = ["host-local", "federated"]
        rendered = docs.render_host_catalogue(self.registry, "en")
        row = next(
            line
            for line in rendered.splitlines()
            if line.startswith("| <code>alpha.read")
        )
        self.assertIn("| false | true |", row)
        for value in (*docs.OTHER_FLAGS, "host-local", "federated"):
            self.assertIn(docs.literal(value), row)

    def test_escaping_cannot_inject_table_heading_or_html(self) -> None:
        self.registry["alpha.read"]["owner"] = "<script>|`_*\n## injected"
        rendered = docs.render_host_catalogue(self.registry, "en")
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("\n## injected", rendered)
        self.assertIn("&lt;script&gt;&#124;&#96;&#95;&#42;&#10;", rendered)

    def test_empty_host_subset_is_explicit(self) -> None:
        self.assertIn("**0** host-local / **0**", docs.render_host_catalogue({}, "en"))

    def test_idempotent_and_preserves_manual_bytes_including_crlf(self) -> None:
        original = document().replace("\n", "\r\n")
        rendered = docs.update_document(original, self.registry, "pl")
        self.assertEqual(rendered, docs.update_document(rendered, self.registry, "pl"))
        self.assertEqual(original.split(docs.BEGIN)[0], rendered.split(docs.BEGIN)[0])
        self.assertEqual(original.split(docs.END)[1], rendered.split(docs.END)[1])

    def test_rejects_ambiguous_missing_reversed_or_inline_markers(self) -> None:
        for text in (
            "",
            docs.BEGIN,
            docs.END,
            document() + docs.BEGIN,
            document() + docs.END,
            f"{docs.END}\n{docs.BEGIN}",
            "prefix " + document().split("\n\n", 1)[1],
            document().replace(docs.END, docs.END + " suffix"),
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                docs.update_document(text, self.registry, "en")

    def test_changes_in_owner_flags_status_or_wire_produce_drift(self) -> None:
        original = docs.update_document(document(), self.registry, "en")
        for key, value in (
            ("owner", "new-owner"),
            ("status", "deprecated"),
            ("wire/name", "host/new-name"),
        ):
            changed = copy.deepcopy(self.registry)
            changed["alpha.read"][key] = value
            self.assertNotEqual(original, docs.update_document(original, changed, "en"))
        changed = copy.deepcopy(self.registry)
        changed["alpha.read"]["flags"]["host-route"] = True
        self.assertNotEqual(original, docs.update_document(original, changed, "en"))


class CommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "node/capability/capability-registry.v1.json"
        self.source.parent.mkdir(parents=True)
        self.source.write_text(
            json.dumps(
                {"schema/v": "capability-registry.v1", "entries": [entry("alpha.read")]}
            )
        )
        self.paths = [
            self.root / "doc/project/60-solutions" / f"CAPABILITY-REGISTRY.{lang}.md"
            for lang in ("pl", "en")
        ]
        self.paths[0].parent.mkdir(parents=True)
        for path in self.paths:
            path.write_text(document())
        spec = importlib.util.spec_from_file_location(
            "generator",
            Path(__file__).with_name("generate-capability-registry-docs.py"),
        )
        self.generator = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, capability_registry_docs=docs):
            spec.loader.exec_module(self.generator)
        self.generator.ROOT = self.root

    def run_command(self, *args: str) -> int:
        with (
            patch.dict(sys.modules, capability_registry_docs=docs),
            patch.object(
                sys, "argv", ["generator", "--node-src", str(self.root / "node"), *args]
            ),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return self.generator.main()

    def test_check_is_read_only_and_detects_drift(self) -> None:
        before = [path.read_bytes() for path in self.paths]
        self.assertEqual(1, self.run_command("--check"))
        self.assertEqual(before, [path.read_bytes() for path in self.paths])
        self.assertEqual(0, self.run_command())
        self.assertEqual(0, self.run_command("--check"))
        before = [path.stat().st_mtime_ns for path in self.paths]
        self.assertEqual(0, self.run_command())
        self.assertEqual(before, [path.stat().st_mtime_ns for path in self.paths])

    def test_invalid_second_destination_leaves_first_untouched(self) -> None:
        self.paths[1].write_text("Manual document without markers")
        before = [path.read_bytes() for path in self.paths]
        self.assertEqual(1, self.run_command())
        self.assertEqual(before, [path.read_bytes() for path in self.paths])

    def test_missing_or_invalid_registry_leaves_documents_untouched(self) -> None:
        before = [path.read_bytes() for path in self.paths]
        for contents in (
            "{",
            '{"schema/v":"wrong","entries":[]}',
            json.dumps(
                {"schema/v": "capability-registry.v1", "entries": [entry("UPPERCASE")]}
            ),
        ):
            self.source.write_text(contents)
            self.assertEqual(1, self.run_command())
            self.assertEqual(before, [path.read_bytes() for path in self.paths])
        self.source.unlink()
        self.assertEqual(1, self.run_command())
        self.assertEqual(before, [path.read_bytes() for path in self.paths])


if __name__ == "__main__":
    unittest.main()
