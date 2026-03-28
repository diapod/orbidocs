#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "doc" / "schemas"
EXAMPLES_DIR = SCHEMAS_DIR / "examples"
INVALID_EXAMPLES_DIR = EXAMPLES_DIR / "invalid"

SCHEMA_WHITELIST = (
    "node-identity.v1.schema.json",
    "node-advertisement.v1.schema.json",
    "peer-handshake.v1.schema.json",
    "capability-advertisement.v1.schema.json",
    "signal-marker.v1.schema.json",
    "coi-declaration.v1.schema.json",
    "participant-bind.v1.schema.json",
    "client-instance-attachment.v1.schema.json",
    "client-instance-detachment.v1.schema.json",
    "client-instance-recovery.v1.schema.json",
)

EXAMPLE_WHITELIST = (
    "bootstrap.node-identity.json",
    "seed-wss.node-advertisement.json",
    "vector-signed.node-advertisement.json",
    "bootstrap.hello.peer-handshake.json",
    "bootstrap.ack.peer-handshake.json",
    "base-node.capability-advertisement.json",
    "privacy-redacted.signal-marker.json",
    "no-conflict.coi-declaration.json",
    "bound-over-live-session.participant-bind.json",
    "operator-remote-screen.client-instance-attachment.json",
    "user-requested.client-instance-detachment.json",
    "replace-device.client-instance-recovery.json",
)

INVALID_EXAMPLE_WHITELIST = (
    "missing-storage-ref.node-identity.json",
    "inline-secret.node-identity.json",
    "no-endpoints.node-advertisement.json",
    "ack-without-reference.peer-handshake.json",
    "no-core-caps.capability-advertisement.json",
    "raw-with-operations.signal-marker.json",
    "conflict-without-category.coi-declaration.json",
    "missing-via-node.participant-bind.json",
    "missing-participant-bind.client-instance-attachment.json",
    "missing-participant-bind.client-instance-detachment.json",
    "missing-detachment-ref.client-instance-recovery.json",
)


def copy_files(files: tuple[str, ...], source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        shutil.copy2(source_dir / name, target_dir / name)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--node-src", default="../node")
    args = parser.parse_args()

    node_root = (ROOT / args.node_src).resolve()
    contracts_root = node_root / "protocol" / "contracts"
    schema_target = contracts_root / "schemas"
    example_target = contracts_root / "examples"
    invalid_target = example_target / "invalid"

    copy_files(SCHEMA_WHITELIST, SCHEMAS_DIR, schema_target)
    copy_files(EXAMPLE_WHITELIST, EXAMPLES_DIR, example_target)
    copy_files(INVALID_EXAMPLE_WHITELIST, INVALID_EXAMPLES_DIR, invalid_target)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
