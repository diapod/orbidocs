#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "doc" / "schemas"
EXAMPLES_DIR = SCHEMAS_DIR / "examples"
INVALID_EXAMPLES_DIR = EXAMPLES_DIR / "invalid"
GOLDEN_DIR = SCHEMAS_DIR / "golden"

SCHEMA_WHITELIST = (
    "node-identity.v1.schema.json",
    "node-advertisement.v1.schema.json",
    "peer-handshake.v1.schema.json",
    "capability-advertisement.v1.schema.json",
    "capability-passport-present.v1.schema.json",
    "capability-passport-revocation.v1.schema.json",
    "capability-passport.v1.schema.json",
    "seed-capability-registration.v1.schema.json",
    "seed-directory-query-attestation.v1.schema.json",
    "capability-schema-present.v1.schema.json",
    "capability-schema.v1.schema.json",
    "signal-marker-envelope.v1.schema.json",
    "signal-marker.v1.schema.json",
    "coi-declaration.v1.schema.json",
    "exception-record.v1.schema.json",
    "emergency-signal.v1.schema.json",
    "reputation-signal.v1.schema.json",
    "agora-authority-policy.v1.schema.json",
    "agora-public-rejection.v1.schema.json",
    "reputation-snapshot.v1.schema.json",
    "nym-certificate.v1.schema.json",
    "nym-authorship-proof.v1.schema.json",
    "nym-succession.v1.schema.json",
    "association-room-proposal.v1.schema.json",
    "room.v1.schema.json",
    "room-membership.v1.schema.json",
    "room-event.v1.schema.json",
    "room-policy.v1.schema.json",
    "room-live-message.v1.schema.json",
    "room-membership-attestation.v1.schema.json",
    "room-membership-attestation-request.v1.schema.json",
    "room-attestation-audit.v1.schema.json",
    "whisper-interest.v1.schema.json",
    "whisper-signal.v1.schema.json",
    "whisper-threshold-reached.v1.schema.json",
    "whisper-redaction-prepare-request.v1.schema.json",
    "whisper-redaction-prepare-response.v1.schema.json",
    "procurement-offer.v1.schema.json",
    "procurement-contract.v1.schema.json",
    "procurement-receipt.v1.schema.json",
    "gateway-policy.v1.schema.json",
    "escrow-policy.v1.schema.json",
    "settlement-policy-disclosure.v1.schema.json",
    "ledger-account.v1.schema.json",
    "gateway-receipt.v1.schema.json",
    "community-pool-disbursement.v1.schema.json",
    "participant-bind.v1.schema.json",
    "participant-capability-limits.v1.schema.json",
    "node-operator-binding.v1.schema.json",
    "client-instance-attachment.v1.schema.json",
    "client-instance-detachment.v1.schema.json",
    "client-instance-recovery.v1.schema.json",
    "question-envelope.v1.schema.json",
    "response-envelope.v1.schema.json",
    "service-offer.v1.schema.json",
    "service-offer-relay.v1.schema.json",
    "service-order.v1.schema.json",
    "offer-catalog-fetch-request.schema.json",
    "offer-catalog-fetch-response.schema.json",
    "classification.v1.schema.json",
    "memarium-host-api.v1.schema.json",
    "memarium-blob.v1.schema.json",
    "artifact-delivery-envelope.v1.schema.json",
    "artifact-delivery-result.v1.schema.json",
    "artifact-delivery-status.v1.schema.json",
    "artifact-object-pointer.v1.schema.json",
    "deferred-operation.v1.schema.json",
    "deferred-operation-status.v1.schema.json",
    "inac-control.v1.schema.json",
    "notification.v1.schema.json",
    "notification-create.v1.schema.json",
    "notification-action.v1.schema.json",
    "notification-action-result.v1.schema.json",
    "notification-state-changed.v1.schema.json",
    "notification-allow.v1.schema.json",
    "notification-delivery-policy.v1.schema.json",
    "local-contact.v1.schema.json",
    "contact-claim.v1.schema.json",
    "contact-lookup-result.v1.schema.json",
    "contact-request.v1.schema.json",
    "contact-attestation-request.v1.schema.json",
    "contact-attestation-result.v1.schema.json",
    "membership-invitation.v1.schema.json",
    "membership-sponsorship.v1.schema.json",
    "membership-acceptance.v1.schema.json",
    "participant-entry-profile.v1.schema.json",
    "participant-effective-limits.v1.schema.json",
    "surface-access-policy.v1.schema.json",
    "message-envelope.v1.schema.json",
    "messaging.passport-issued.v1.schema.json",
    "messaging.passport-revoked.v1.schema.json",
    "messaging.retention-decided.v1.schema.json",
    "messaging.crisis-marked.v1.schema.json",
    "capability-passport-lookup.v1.schema.json",
    "local-recipient-mailbox-resolve.v1.schema.json",
    "service-ca-material.v1.schema.json",
    "service-ca-revocation.v1.schema.json",
)

EXAMPLE_WHITELIST = (
    "bootstrap.node-identity.json",
    "seed-wss.node-advertisement.json",
    "vector-signed.node-advertisement.json",
    "bootstrap.hello.peer-handshake.json",
    "bootstrap.ack.peer-handshake.json",
    "base-node.capability-advertisement.json",
    "network-ledger.capability-passport-present.json",
    "sealer-access.capability-passport-present.json",
    "memarium-space-access.capability-passport-present.json",
    "offer-catalog.seed-capability-registration.json",
    "capability.seed-directory-query-attestation.json",
    "memarium-declassify.capability-passport-present.json",
    "community-key-access.capability-passport-present.json",
    "audio-transcription.capability-schema-present.json",
    "audio-transcription.capability-schema.json",
    "participant-broadcast.signal-marker-envelope.json",
    "privacy-redacted.signal-marker.json",
    "no-conflict.coi-declaration.json",
    "temporary-routing-override.exception-record.json",
    "blackout-failover.exception-record.json",
    "blackout-correlated.emergency-signal.json",
    "degraded-trust-peer-corroborated.emergency-signal.json",
    "participant-governance-inaction.reputation-signal.json",
    "node-relay-unreliable.reputation-signal.json",
    "nym-helpful-participation.reputation-signal.json",
    "default.agora-authority-policy.json",
    "public-policy-denial.agora-public-rejection.json",
    "community-trusted.reputation-snapshot.json",
    "selected-responder.question-envelope.json",
    "single-responder.procurement-offer.json",
    "contract-without-receipt.response-envelope.json",
    "host-ledger-escrow.procurement-contract.json",
    "arbiter-confirmed.procurement-contract.json",
    "host-ledger-settled.procurement-receipt.json",
    "arbiter-confirmed.procurement-receipt.json",
    "pl-main.gateway-policy.json",
    "pl-main.escrow-policy.json",
    "gateway-payout-freeze.settlement-policy-disclosure.json",
    "access-condition-violation.settlement-policy-disclosure.json",
    "prepaid-participant.ledger-account.json",
    "community-pool.ledger-account.json",
    "inbound-topup.gateway-receipt.json",
    "ubc-subsidy.community-pool-disbursement.json",
    "bound-over-live-session.participant-bind.json",
    "limited-procurement-offer.participant-capability-limits.json",
    "primary-operator.node-operator-binding.json",
    "operator-remote-screen.client-instance-attachment.json",
    "user-requested.client-instance-detachment.json",
    "replace-device.client-instance-recovery.json",
    "federation-local-procurement.question-envelope.json",
    "federation-local-pseudonymous.question-envelope.json",
    "human-mediated.response-envelope.json",
    "ola-redaction.service-offer.json",
    "basic.service-offer-relay.json",
    "casualfeeders-breakfast-research.service-order.json",
    "basic.offer-catalog-fetch-request.json",
    "basic.offer-catalog-fetch-response.json",
    "personal-local.classification.json",
    "quarantined-ingress.classification.json",
    "personal-to-community-one-shot.classification.json",
    "community-to-public-persistent.classification.json",
    "write-entry.memarium-host-api.json",
    "inline-note.memarium-blob.json",
    "basic.whisper-redaction-prepare-request.json",
    "draft-ready.whisper-redaction-prepare-response.json",
    "declassify.memarium-host-api.json",
    "revoked.memarium-host-api.json",
    "private-whisper.artifact-delivery-envelope.json",
    "contact-request-via-contact-lookup.artifact-delivery-envelope.json",
    "basic.artifact-object-pointer.json",
    "accepted.artifact-delivery-result.json",
    "running.artifact-delivery-status.json",
    "push-inline.inac-control.json",
    "refused.inac-control.json",
    "invite-only.contact-claim.json",
    "invitation-required.contact-lookup-result.json",
    "no-match.contact-lookup-result.json",
    "basic.local-contact.json",
    "basic.contact-attestation-request.json",
    "issued.contact-attestation-result.json",
    "community-basic.membership-invitation.json",
    "community-basic.membership-sponsorship.json",
    "probationary.membership-acceptance.json",
    "newcomer.participant-entry-profile.json",
    "newcomer.participant-effective-limits.json",
    "default.surface-access-policy.json",
    "basic.room.json",
    "grant-member.room-membership.json",
    "close.room-event.json",
    "closed-private.room-policy.json",
    "basic.room-live-message.json",
    "member.room-membership-attestation.json",
    "member-self.room-membership-attestation-request.json",
    "issued.room-attestation-audit.json",
    "refused.room-attestation-audit.json",
    "messaging.contact-request.json",
    "basic.message-envelope.json",
    "issued.messaging.passport-issued.json",
    "public-seed-directory.service-ca-material.json",
    "public-seed-directory.service-ca-revocation.json",
)

INVALID_EXAMPLE_WHITELIST = (
    "missing-storage-ref.node-identity.json",
    "inline-secret.node-identity.json",
    "no-endpoints.node-advertisement.json",
    "ack-without-reference.peer-handshake.json",
    "no-core-caps.capability-advertisement.json",
    "wrong-kind.signal-marker-envelope.json",
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
    "org-root-without-custody.agora-authority-policy.json",
    "detailed-public-rejection.agora-public-rejection.json",
    "runtime-authority.reputation-snapshot.json",
    "negative-price.procurement-offer.json",
    "no-confirmation-paid.procurement-contract.json",
    "settled-without-payee.procurement-receipt.json",
    "gateway-policy-with-participant-operator.gateway-policy.json",
    "escrow-policy-without-operator.escrow-policy.json",
    "incident-without-basis.settlement-policy-disclosure.json",
    "manual-review-without-decision-basis.settlement-policy-disclosure.json",
    "community-pool-without-council-controller.ledger-account.json",
    "inbound-topup-without-fee-breakdown.gateway-receipt.json",
    "without-basis.community-pool-disbursement.json",
    "missing-via-node.participant-bind.json",
    "mixed-participant-and-nym.question-envelope.json",
    "private-scope-public-delivery.question-envelope.json",
    "selected-responder-missing-federation.question-envelope.json",
    "human-flag-without-human-origin.response-envelope.json",
    "blocked-core-messaging.participant-capability-limits.json",
    "missing-scopes.membership-sponsorship.json",
    "guest-with-broadcast.participant-entry-profile.json",
    "unknown-surface.surface-access-policy.json",
    "missing-participant-bind.client-instance-attachment.json",
    "missing-participant-bind.client-instance-detachment.json",
    "missing-detachment-ref.client-instance-recovery.json",
    "direct-personal-to-public.classification.json",
    "one-shot-with-expires.classification.json",
    "persistent-without-expires.classification.json",
    "public-with-full-subjects.classification.json",
    "success-without-draft.whisper-redaction-prepare-response.json",
    "grant-without-grants.room-membership.json",
    "mediated-policy-with-live.room-policy.json",
    "live-message-without-session.room-live-message.json",
    "inac-push-missing-artifact.inac-control.json",
    "raw-handle.contact-lookup.artifact-delivery-envelope.json",
    "unsupported-mode.contact-lookup.artifact-delivery-envelope.json",
    "missing-store-ref.artifact-object-pointer.json",
    "invitation-without-route.contact-lookup-result.json",
    "missing-signature.message-envelope.json",
    "memarium-blob-without-signature.memarium-blob.json",
    "no-scope.service-ca-material.json",
    "missing-signature.seed-directory-query-attestation.json",
)

GOLDEN_WHITELIST = (
    "golden-room-projection-input.json",
    "golden-room-projection-output.json",
)

SCHEMA_GATE_AGORA_SCHEMA_WHITELIST = (
    "room.v1.schema.json",
    "room-membership.v1.schema.json",
    "room-event.v1.schema.json",
    "room-policy.v1.schema.json",
    "room-live-message.v1.schema.json",
    "room-membership-attestation.v1.schema.json",
    "room-membership-attestation-request.v1.schema.json",
    "room-attestation-audit.v1.schema.json",
)


def copy_files(files: tuple[str, ...], source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        source = source_dir / name
        target = target_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_shared_schemas(schema_target: Path) -> None:
    shared_source = SCHEMAS_DIR / "_shared"
    if not shared_source.exists():
        return
    shared_target = schema_target / "_shared"
    shared_target.mkdir(parents=True, exist_ok=True)
    for source in shared_source.rglob("*.json"):
        relative = source.relative_to(shared_source)
        target = shared_target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


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
    golden_target = contracts_root / "golden"
    schema_gate_agora_target = node_root / "schema-gate" / "contracts" / "schemas" / "agora"

    copy_files(SCHEMA_WHITELIST, SCHEMAS_DIR, schema_target)
    copy_shared_schemas(schema_target)
    copy_files(SCHEMA_GATE_AGORA_SCHEMA_WHITELIST, SCHEMAS_DIR, schema_gate_agora_target)
    copy_files(EXAMPLE_WHITELIST, EXAMPLES_DIR, example_target)
    copy_files(INVALID_EXAMPLE_WHITELIST, INVALID_EXAMPLES_DIR, invalid_target)
    copy_files(GOLDEN_WHITELIST, GOLDEN_DIR, golden_target)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
