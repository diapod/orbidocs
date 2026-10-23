#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("sync-node-schemas.py")
SPEC = importlib.util.spec_from_file_location("sync_node_schemas", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class ResolveNodeRootTests(unittest.TestCase):
    def test_maintenance_m0_mirrors_are_explicit_complete_and_byte_identical(self) -> None:
        groups = (
            (SYNC.SCHEMA_WHITELIST, SYNC.SCHEMAS_DIR, "responsibility-maintenance-*.schema.json", 10),
            (SYNC.EXAMPLE_WHITELIST, SYNC.EXAMPLES_DIR, "*.responsibility-maintenance-*.json", 10),
            (SYNC.INVALID_EXAMPLE_WHITELIST, SYNC.INVALID_EXAMPLES_DIR, "*.responsibility-maintenance-*.json", 13),
        )
        for whitelist, source, pattern, count in groups:
            names = tuple(sorted(path.name for path in source.glob(pattern)))
            self.assertEqual(len(names), count)
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary)
                for name in names:
                    self.assertIn(name, whitelist)
                SYNC.copy_files(names, source, target)
                for name in names:
                    self.assertEqual((target / name).read_bytes(), (source / name).read_bytes())

    def test_local_catalog_contracts_are_reproducible_node_mirrors(self) -> None:
        families = (
            "capability-catalog-request.v1.schema.json",
            "capability-catalog-result.v1.schema.json",
            "capability-catalog-refusal.v1.schema.json",
            "capability-guidance.v1.schema.json",
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            for name in families:
                self.assertIn(name, SYNC.SCHEMA_WHITELIST)
            SYNC.copy_files(families, SYNC.SCHEMAS_DIR, target)
            for name in families:
                self.assertEqual((target / name).read_bytes(), (SYNC.SCHEMAS_DIR / name).read_bytes())

    def test_panel_and_lifecycle_contracts_and_examples_are_reproducible_mirrors(self) -> None:
        families = tuple(sorted(
            path.name for path in SYNC.SCHEMAS_DIR.glob("*.schema.json")
            if (path.name.startswith("panel-") and ".local." in path.name)
            or path.name.startswith("participant-restriction-lifecycle")
            or path.name in {
                "responsibility-effect-receipt.v2.schema.json",
                "responsibility-lifecycle-readiness.local.v1.schema.json",
            }
        ))
        self.assertEqual(len(families), 15)
        for whitelist, source, names in (
            (SYNC.SCHEMA_WHITELIST, SYNC.SCHEMAS_DIR, families),
            (SYNC.EXAMPLE_WHITELIST, SYNC.EXAMPLES_DIR, tuple(
                path.name for path in SYNC.EXAMPLES_DIR.glob("*.json")
                if ".panel-" in path.name
            )),
            (SYNC.INVALID_EXAMPLE_WHITELIST, SYNC.INVALID_EXAMPLES_DIR, tuple(
                path.name for path in SYNC.INVALID_EXAMPLES_DIR.glob("*.json")
                if ".panel-" in path.name
            )),
        ):
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary)
                for name in names:
                    self.assertIn(name, whitelist)
                SYNC.copy_files(names, source, target)
                for name in names:
                    self.assertEqual((target / name).read_bytes(), (source / name).read_bytes())

    def test_discovery_contracts_are_synced_to_both_runtime_targets(self) -> None:
        families = (
            "sensorium-device-discovery.request.v1.schema.json",
            "sensorium-device-discovery-candidate.v1.schema.json",
            "sensorium-device-discovery-result.v1.schema.json",
            "deferred-operation-status.v2.schema.json",
        )
        for whitelist in (SYNC.SCHEMA_WHITELIST, SYNC.MIDDLEWARE_SCHEMA_WHITELIST):
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary)
                for family in families:
                    self.assertIn(family, whitelist)
                SYNC.copy_files(families, SYNC.SCHEMAS_DIR, target)
                for family in families:
                    self.assertEqual((target / family).read_bytes(),
                                     (SYNC.SCHEMAS_DIR / family).read_bytes())

    def test_sensorium_os_schema_is_synced_to_its_existing_node_filename(self) -> None:
        canonical = "sensorium-os-error-codes.v1.schema.json"
        self.assertIn(canonical, SYNC.SCHEMA_WHITELIST)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            SYNC.copy_files(
                (canonical,), SYNC.SCHEMAS_DIR, target, SYNC.NODE_SCHEMA_FILENAMES
            )
            self.assertEqual(
                (target / "sensorium-os-error-codes.v1.json").read_bytes(),
                (SYNC.SCHEMAS_DIR / canonical).read_bytes(),
            )
            self.assertFalse((target / canonical).exists())

    def test_accepts_a_node_workspace_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "node"
            for relative in SYNC.NODE_WORKSPACE_SENTINELS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()

            self.assertEqual(SYNC.resolve_node_root(str(root)), root.resolve())

    def test_rejects_protocol_contracts_as_node_workspace_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            contracts = Path(temporary) / "node" / "protocol" / "contracts"
            contracts.mkdir(parents=True)

            with self.assertRaisesRegex(ValueError, "not its protocol/contracts directory"):
                SYNC.resolve_node_root(str(contracts))


if __name__ == "__main__":
    unittest.main()
