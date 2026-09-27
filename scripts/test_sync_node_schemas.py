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
