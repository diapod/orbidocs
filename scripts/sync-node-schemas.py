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
    "exception-record.v1.schema.json",
    "emergency-signal.v1.schema.json",
    "reputation-signal.v1.schema.json",
    "gateway-policy.v1.schema.json",
    "escrow-policy.v1.schema.json",
    "settlement-policy-disclosure.v1.schema.json",
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
    "temporary-routing-override.exception-record.json",
    "blackout-failover.exception-record.json",
    "blackout-correlated.emergency-signal.json",
    "degraded-trust-peer-corroborated.emergency-signal.json",
    "participant-governance-inaction.reputation-signal.json",
    "node-relay-unreliable.reputation-signal.json",
    "nym-helpful-participation.reputation-signal.json",
    "pl-main.gateway-policy.json",
    "pl-main.escrow-policy.json",
    "gateway-payout-freeze.settlement-policy-disclosure.json",
    "access-condition-violation.settlement-policy-disclosure.json",
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
    "high-risk-without-approvals.exception-record.json",
    "critical-without-monitoring-metrics.exception-record.json",
    "system-requester-with-non-system-id.exception-record.json",
    "wrong-policy-id.exception-record.json",
    "bad-source-node-id.emergency-signal.json",
    "unknown-trigger-class.emergency-signal.json",
    "tc5-without-flag.emergency-signal.json",
    "tc5-flag-on-non-tc5.emergency-signal.json",
    "nym-procedural-governance-inaction.reputation-signal.json",
    "zero-weight.reputation-signal.json",
    "neutral-polarity.reputation-signal.json",
    "participant-kind-with-node-id.reputation-signal.json",
    "council-emitter-without-council-id.reputation-signal.json",
    "gateway-policy-with-participant-operator.gateway-policy.json",
    "escrow-policy-without-operator.escrow-policy.json",
    "incident-without-basis.settlement-policy-disclosure.json",
    "manual-review-without-decision-basis.settlement-policy-disclosure.json",
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
