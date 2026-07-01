#!/bin/sh

set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SCHEMAS_DIR="$ROOT/doc/schemas"
VALID_EXAMPLES_DIR="$SCHEMAS_DIR/examples"
INVALID_EXAMPLES_DIR="$VALID_EXAMPLES_DIR/invalid"
MODE=${1:-all}

if [ "$MODE" != "all" ] && [ "$MODE" != "--syntax-only" ]; then
  echo "Usage: $0 [--syntax-only]" >&2
  exit 1
fi

choose_validator() {
  if command -v check-jsonschema >/dev/null 2>&1; then
    echo "check-jsonschema"
    return 0
  fi

  if command -v ajv >/dev/null 2>&1; then
    echo "ajv"
    return 0
  fi

  echo ""
}

schema_for_file() {
  case "$1" in
    *.learning-outcome.json)
      echo "$SCHEMAS_DIR/learning-outcome.v1.schema.json"
      ;;
    *.curation-decision.json)
      echo "$SCHEMAS_DIR/curation-decision.v1.schema.json"
      ;;
    *.corpus-entry.json)
      echo "$SCHEMAS_DIR/corpus-entry.v1.schema.json"
      ;;
    *.classification.json)
      echo "$SCHEMAS_DIR/classification.v1.schema.json"
      ;;
    *.memarium-host-api.json)
      echo "$SCHEMAS_DIR/memarium-host-api.v1.schema.json"
      ;;
    *.memarium-blob.json)
      echo "$SCHEMAS_DIR/memarium-blob.v1.schema.json"
      ;;
    *.artifact-delivery-envelope.json)
      echo "$SCHEMAS_DIR/artifact-delivery-envelope.v1.schema.json"
      ;;
    *.artifact-delivery-result.json)
      echo "$SCHEMAS_DIR/artifact-delivery-result.v1.schema.json"
      ;;
    *.artifact-delivery-status.json)
      echo "$SCHEMAS_DIR/artifact-delivery-status.v1.schema.json"
      ;;
    *.artifact-object-pointer.json)
      echo "$SCHEMAS_DIR/artifact-object-pointer.v1.schema.json"
      ;;
    *.deferred-operation.json)
      echo "$SCHEMAS_DIR/deferred-operation.v1.schema.json"
      ;;
    *.deferred-operation-status.json)
      echo "$SCHEMAS_DIR/deferred-operation-status.v1.schema.json"
      ;;
    *.interaction-broker-watch.json)
      echo "$SCHEMAS_DIR/interaction-broker-watch.v1.schema.json"
      ;;
    *.interaction-broker-wait.request.json)
      echo "$SCHEMAS_DIR/interaction-broker-wait.request.v1.schema.json"
      ;;
    *.interaction-broker-wait.outcome.json)
      echo "$SCHEMAS_DIR/interaction-broker-wait.outcome.v1.schema.json"
      ;;
    *.interaction-broker-probe.json)
      echo "$SCHEMAS_DIR/interaction-broker-probe.v1.schema.json"
      ;;
    *.sensorium-relative-path-address.json)
      echo "$SCHEMAS_DIR/sensorium-relative-path-address.v1.schema.json"
      ;;
    *.sensorium-command-profile.json)
      echo "$SCHEMAS_DIR/sensorium-command-profile.v1.schema.json"
      ;;
    *.sensorium-command-intent.json)
      echo "$SCHEMAS_DIR/sensorium-command-intent.v1.schema.json"
      ;;
    *.sensorium-pty-resource-caps.json)
      echo "$SCHEMAS_DIR/sensorium-pty-resource-caps.v1.schema.json"
      ;;
    *.sensorium-workbench-environment.json)
      echo "$SCHEMAS_DIR/sensorium-workbench-environment.v1.schema.json"
      ;;
    *.sensorium-terminal-session.json)
      echo "$SCHEMAS_DIR/sensorium-terminal-session.v1.schema.json"
      ;;
    *.sensorium-terminal-command.json)
      echo "$SCHEMAS_DIR/sensorium-terminal-command.v1.schema.json"
      ;;
    *.sensorium-terminal-input.json)
      echo "$SCHEMAS_DIR/sensorium-terminal-input.v1.schema.json"
      ;;
    *.sensorium-terminal-event.json)
      echo "$SCHEMAS_DIR/sensorium-terminal-event.v1.schema.json"
      ;;
    *.sensorium-terminal-screen-snapshot.json)
      echo "$SCHEMAS_DIR/sensorium-terminal-screen-snapshot.v1.schema.json"
      ;;
    *.sensorium-file-snapshot.json)
      echo "$SCHEMAS_DIR/sensorium-file-snapshot.v1.schema.json"
      ;;
    *.sensorium-file-read-result.json)
      echo "$SCHEMAS_DIR/sensorium-file-read-result.v1.schema.json"
      ;;
    *.sensorium-workbench-patch.json)
      echo "$SCHEMAS_DIR/sensorium-workbench-patch.v1.schema.json"
      ;;
    *.sensorium-workbench-patch-apply-result.json)
      echo "$SCHEMAS_DIR/sensorium-workbench-patch-apply-result.v1.schema.json"
      ;;
    *.sensorium-workbench-outcome.json)
      echo "$SCHEMAS_DIR/sensorium-workbench-outcome.v1.schema.json"
      ;;
    *.inac-control.json)
      echo "$SCHEMAS_DIR/inac-control.v1.schema.json"
      ;;
    *.training-job.json)
      echo "$SCHEMAS_DIR/training-job.v1.schema.json"
      ;;
    *.eval-report.json)
      echo "$SCHEMAS_DIR/eval-report.v1.schema.json"
      ;;
    *.adapter-artifact.json)
      echo "$SCHEMAS_DIR/adapter-artifact.v1.schema.json"
      ;;
    *.agora-record.json)
      echo "$SCHEMAS_DIR/agora-record.v1.schema.json"
      ;;
    *.agora-query-attestation.json)
      echo "$SCHEMAS_DIR/agora-query-attestation.v1.schema.json"
      ;;
    *.agora-authority-policy.json)
      echo "$SCHEMAS_DIR/agora-authority-policy.v1.schema.json"
      ;;
    *.agora-public-rejection.json)
      echo "$SCHEMAS_DIR/agora-public-rejection.v1.schema.json"
      ;;
    *.reputation-snapshot.json)
      echo "$SCHEMAS_DIR/reputation-snapshot.v1.schema.json"
      ;;
    *.org-custody-policy.json)
      echo "$SCHEMAS_DIR/org-custody-policy.v1.schema.json"
      ;;
    *.org-custody-decision.json)
      echo "$SCHEMAS_DIR/org-custody-decision.v1.schema.json"
      ;;
    *.resource-opinion.json)
      echo "$SCHEMAS_DIR/resource-opinion.v1.schema.json"
      ;;
    *.public-gossip.json)
      echo "$SCHEMAS_DIR/public-gossip.v1.schema.json"
      ;;
    *.moderation-marker.json)
      echo "$SCHEMAS_DIR/moderation-marker.v1.schema.json"
      ;;
    *.comment-thread-policy.json)
      echo "$SCHEMAS_DIR/comment-thread-policy.v1.schema.json"
      ;;
    *.contact-claim.json)
      echo "$SCHEMAS_DIR/contact-claim.v1.schema.json"
      ;;
    *.contact-lookup-result.json)
      echo "$SCHEMAS_DIR/contact-lookup-result.v1.schema.json"
      ;;
    *.contact-request.json)
      echo "$SCHEMAS_DIR/contact-request.v1.schema.json"
      ;;
    *.message-envelope.json)
      echo "$SCHEMAS_DIR/message-envelope.v1.schema.json"
      ;;
    *.agora-vault-entry.json)
      echo "$SCHEMAS_DIR/agora-vault-entry.v1.schema.json"
      ;;
    *.agora-vault-ref.json)
      echo "$SCHEMAS_DIR/agora-vault-ref.v1.schema.json"
      ;;
    *.messaging.passport-issued.json)
      echo "$SCHEMAS_DIR/messaging.passport-issued.v1.schema.json"
      ;;
    *.messaging.passport-revoked.json)
      echo "$SCHEMAS_DIR/messaging.passport-revoked.v1.schema.json"
      ;;
    *.messaging.retention-decided.json)
      echo "$SCHEMAS_DIR/messaging.retention-decided.v1.schema.json"
      ;;
    *.messaging.crisis-marked.json)
      echo "$SCHEMAS_DIR/messaging.crisis-marked.v1.schema.json"
      ;;
    *.local-contact.json)
      echo "$SCHEMAS_DIR/local-contact.v1.schema.json"
      ;;
    *.contact-attestation-request.json)
      echo "$SCHEMAS_DIR/contact-attestation-request.v1.schema.json"
      ;;
    *.contact-attestation-result.json)
      echo "$SCHEMAS_DIR/contact-attestation-result.v1.schema.json"
      ;;
    *.node-identity.json)
      echo "$SCHEMAS_DIR/node-identity.v1.schema.json"
      ;;
    *.node-operator-binding.json)
      echo "$SCHEMAS_DIR/node-operator-binding.v1.schema.json"
      ;;
    *.routing-subject-binding.json)
      echo "$SCHEMAS_DIR/routing-subject-binding.v1.schema.json"
      ;;
    *.pseudonym-vault.json)
      echo "$SCHEMAS_DIR/pseudonym-vault.v1.schema.json"
      ;;
    *.relationship-class.json)
      echo "$SCHEMAS_DIR/relationship-class.v1.schema.json"
      ;;
    *.relationship-class-changed.json)
      echo "$SCHEMAS_DIR/relationship-class-changed.v1.schema.json"
      ;;
    *.relationship-membership-fact.json)
      echo "$SCHEMAS_DIR/relationship-membership-fact.v1.schema.json"
      ;;
    *.pairwise-nym-binding-fact.json)
      echo "$SCHEMAS_DIR/pairwise-nym-binding-fact.v1.schema.json"
      ;;
    *.pairwise-nym-binding.json)
      echo "$SCHEMAS_DIR/pairwise-nym-binding.v1.schema.json"
      ;;
    *.relationship-policy-predicate.json)
      echo "$SCHEMAS_DIR/relationship-policy-predicate.v1.schema.json"
      ;;
    *.relationship-policy-candidate.json)
      echo "$SCHEMAS_DIR/relationship-policy-candidate.v1.schema.json"
      ;;
    *.relationship-policy-decision.json)
      echo "$SCHEMAS_DIR/relationship-policy-decision.v1.schema.json"
      ;;
    *.node-advertisement.json)
      echo "$SCHEMAS_DIR/node-advertisement.v1.schema.json"
      ;;
    *.node-succession.json)
      echo "$SCHEMAS_DIR/node-succession.v1.schema.json"
      ;;
    *.node-address-attestation.json)
      echo "$SCHEMAS_DIR/node-address-attestation.v1.schema.json"
      ;;
    *.service-ca-material.json)
      echo "$SCHEMAS_DIR/service-ca-material.v1.schema.json"
      ;;
    *.service-ca-revocation.json)
      echo "$SCHEMAS_DIR/service-ca-revocation.v1.schema.json"
      ;;
    *.service-offer.json)
      echo "$SCHEMAS_DIR/service-offer.v1.schema.json"
      ;;
    *.topic-taxonomy.json)
      echo "$SCHEMAS_DIR/topic-taxonomy.v1.schema.json"
      ;;
    *.topic-resolution.json)
      echo "$SCHEMAS_DIR/topic-resolution.v1.schema.json"
      ;;
    *.corpus-reasoning-query.json)
      echo "$SCHEMAS_DIR/corpus-reasoning-query.v1.schema.json"
      ;;
    *.corpus-reasoning-bid.json)
      echo "$SCHEMAS_DIR/corpus-reasoning-bid.v1.schema.json"
      ;;
    *.corpus-reasoning-answer.json)
      echo "$SCHEMAS_DIR/corpus-reasoning-answer.v1.schema.json"
      ;;
    *.corpus-reasoning-bid-state.json)
      echo "$SCHEMAS_DIR/corpus-reasoning-bid-state.v1.schema.json"
      ;;
    *.service-offer-relay.json)
      echo "$SCHEMAS_DIR/service-offer-relay.v1.schema.json"
      ;;
    *.seed-capability-registration.json)
      echo "$SCHEMAS_DIR/seed-capability-registration.v1.schema.json"
      ;;
    *.seed-directory-trust.json)
      echo "$SCHEMAS_DIR/seed-directory-trust.v1.schema.json"
      ;;
    *.federation-root.json)
      echo "$SCHEMAS_DIR/federation-root.v1.schema.json"
      ;;
    *.seed-directory-query-attestation.json)
      echo "$SCHEMAS_DIR/seed-directory-query-attestation.v1.schema.json"
      ;;
    *.offer-catalog-fetch-request.json)
      echo "$SCHEMAS_DIR/offer-catalog-fetch-request.schema.json"
      ;;
    *.offer-catalog-fetch-response.json)
      echo "$SCHEMAS_DIR/offer-catalog-fetch-response.schema.json"
      ;;
    *.service-order.json)
      echo "$SCHEMAS_DIR/service-order.v1.schema.json"
      ;;
    *.service-order-dispatch-request.json)
      echo "$SCHEMAS_DIR/service-order-dispatch-request.v1.schema.json"
      ;;
    *.service-order-result.json)
      echo "$SCHEMAS_DIR/service-order-result.v1.schema.json"
      ;;
    *.peer-handshake.json)
      echo "$SCHEMAS_DIR/peer-handshake.v1.schema.json"
      ;;
    *.peer-status.json)
      echo "$SCHEMAS_DIR/peer-status.v1.schema.json"
      ;;
    *.nym-issue-request.json)
      echo "$SCHEMAS_DIR/nym-issue-request.v1.schema.json"
      ;;
    *.nym-succession.json)
      echo "$SCHEMAS_DIR/nym-succession.v1.schema.json"
      ;;
    *.nym-certificate.json)
      echo "$SCHEMAS_DIR/nym-certificate.v1.schema.json"
      ;;
    *.nym-renew-request.json)
      echo "$SCHEMAS_DIR/nym-renew-request.v1.schema.json"
      ;;
    *.nym-renew-rejected.json)
      echo "$SCHEMAS_DIR/nym-renew-rejected.v1.schema.json"
      ;;
    *.participant-bind.json)
      echo "$SCHEMAS_DIR/participant-bind.v1.schema.json"
      ;;
    *.participant-capability-limits.json)
      echo "$SCHEMAS_DIR/participant-capability-limits.v1.schema.json"
      ;;
    *.membership-invitation.json)
      echo "$SCHEMAS_DIR/membership-invitation.v1.schema.json"
      ;;
    *.membership-sponsorship.json)
      echo "$SCHEMAS_DIR/membership-sponsorship.v1.schema.json"
      ;;
    *.membership-acceptance.json)
      echo "$SCHEMAS_DIR/membership-acceptance.v1.schema.json"
      ;;
    *.participant-entry-profile.json)
      echo "$SCHEMAS_DIR/participant-entry-profile.v1.schema.json"
      ;;
    *.participant-effective-limits.json)
      echo "$SCHEMAS_DIR/participant-effective-limits.v1.schema.json"
      ;;
    *.surface-access-policy.json)
      echo "$SCHEMAS_DIR/surface-access-policy.v1.schema.json"
      ;;
    *.coi-declaration.json)
      echo "$SCHEMAS_DIR/coi-declaration.v1.schema.json"
      ;;
    *.exception-record.json)
      echo "$SCHEMAS_DIR/exception-record.v1.schema.json"
      ;;
    *.emergency-signal.json)
      echo "$SCHEMAS_DIR/emergency-signal.v1.schema.json"
      ;;
    *.emergency-activation.json)
      echo "$SCHEMAS_DIR/emergency-activation.v1.schema.json"
      ;;
    *.reputation-signal.json)
      echo "$SCHEMAS_DIR/reputation-signal.v1.schema.json"
      ;;
    *.client-instance-attachment.json)
      echo "$SCHEMAS_DIR/client-instance-attachment.v1.schema.json"
      ;;
    *.client-instance-detachment.json)
      echo "$SCHEMAS_DIR/client-instance-detachment.v1.schema.json"
      ;;
    *.client-instance-recovery.json)
      echo "$SCHEMAS_DIR/client-instance-recovery.v1.schema.json"
      ;;
    *.capability-registry.json)
      echo "$SCHEMAS_DIR/capability-registry.v1.schema.json"
      ;;
    *.capability-authorization-policy.json)
      echo "$SCHEMAS_DIR/capability-authorization-policy.v1.schema.json"
      ;;
    *.capability-advertisement.json)
      echo "$SCHEMAS_DIR/capability-advertisement.v1.schema.json"
      ;;
    *.capability-passport-present.json)
      echo "$SCHEMAS_DIR/capability-passport-present.v1.schema.json"
      ;;
    *.capability-passport.json)
      echo "$SCHEMAS_DIR/capability-passport.v1.schema.json"
      ;;
    *.capability-schema-present.json)
      echo "$SCHEMAS_DIR/capability-schema-present.v1.schema.json"
      ;;
    *.capability-schema.json)
      echo "$SCHEMAS_DIR/capability-schema.v1.schema.json"
      ;;
    *.signal-marker-envelope.json)
      echo "$SCHEMAS_DIR/signal-marker-envelope.v1.schema.json"
      ;;
    *.signal-marker.json)
      echo "$SCHEMAS_DIR/signal-marker.v1.schema.json"
      ;;
    *.orbiplex.api-descriptor.json)
      echo "$SCHEMAS_DIR/orbiplex.api-descriptor.v1.schema.json"
      ;;
    *.model-card.json)
      echo "$SCHEMAS_DIR/model-card.v1.schema.json"
      ;;
    *.knowledge-artifact.json)
      echo "$SCHEMAS_DIR/knowledge-artifact.v1.schema.json"
      ;;
    *.archival-package.json)
      echo "$SCHEMAS_DIR/archival-package.v1.schema.json"
      ;;
    *.archivist-advertisement.json)
      echo "$SCHEMAS_DIR/archivist-advertisement.v1.schema.json"
      ;;
    *.retrieval-request.json)
      echo "$SCHEMAS_DIR/retrieval-request.v1.schema.json"
      ;;
    *.retrieval-response.json)
      echo "$SCHEMAS_DIR/retrieval-response.v1.schema.json"
      ;;
    *.question-envelope.json)
      echo "$SCHEMAS_DIR/question-envelope.v1.schema.json"
      ;;
    *.procurement-offer.json)
      echo "$SCHEMAS_DIR/procurement-offer.v1.schema.json"
      ;;
    *.procurement-contract.json)
      echo "$SCHEMAS_DIR/procurement-contract.v1.schema.json"
      ;;
    *.procurement-receipt.json)
      echo "$SCHEMAS_DIR/procurement-receipt.v1.schema.json"
      ;;
    *.ledger-account.json)
      echo "$SCHEMAS_DIR/ledger-account.v1.schema.json"
      ;;
    *.ledger-hold.json)
      echo "$SCHEMAS_DIR/ledger-hold.v1.schema.json"
      ;;
    *.ledger-transfer.json)
      echo "$SCHEMAS_DIR/ledger-transfer.v1.schema.json"
      ;;
    *.community-pool-disbursement.json)
      echo "$SCHEMAS_DIR/community-pool-disbursement.v1.schema.json"
      ;;
    *.gateway-receipt.json)
      echo "$SCHEMAS_DIR/gateway-receipt.v1.schema.json"
      ;;
    *.gateway-policy.json)
      echo "$SCHEMAS_DIR/gateway-policy.v1.schema.json"
      ;;
    *.escrow-policy.json)
      echo "$SCHEMAS_DIR/escrow-policy.v1.schema.json"
      ;;
    *.settlement-policy-disclosure.json)
      echo "$SCHEMAS_DIR/settlement-policy-disclosure.v1.schema.json"
      ;;
    *.organization-subject.json)
      echo "$SCHEMAS_DIR/organization-subject.v1.schema.json"
      ;;
    *.response-envelope.json)
      echo "$SCHEMAS_DIR/response-envelope.v1.schema.json"
      ;;
    *.whisper-signal.json)
      echo "$SCHEMAS_DIR/whisper-signal.v1.schema.json"
      ;;
    *.whisper-interest.json)
      echo "$SCHEMAS_DIR/whisper-interest.v1.schema.json"
      ;;
    *.whisper-threshold-reached.json)
      echo "$SCHEMAS_DIR/whisper-threshold-reached.v1.schema.json"
      ;;
    *.whisper-redaction-prepare-request.json)
      echo "$SCHEMAS_DIR/whisper-redaction-prepare-request.v1.schema.json"
      ;;
    *.whisper-redaction-prepare-response.json)
      echo "$SCHEMAS_DIR/whisper-redaction-prepare-response.v1.schema.json"
      ;;
    *.association-room-proposal.json)
      echo "$SCHEMAS_DIR/association-room-proposal.v1.schema.json"
      ;;
    *.room-membership-attestation.json)
      echo "$SCHEMAS_DIR/room-membership-attestation.v1.schema.json"
      ;;
    *.room-membership-attestation-request.json)
      echo "$SCHEMAS_DIR/room-membership-attestation-request.v1.schema.json"
      ;;
    *.room-attestation-audit.json)
      echo "$SCHEMAS_DIR/room-attestation-audit.v1.schema.json"
      ;;
    *.room-live-message.json)
      echo "$SCHEMAS_DIR/room-live-message.v1.schema.json"
      ;;
    *.room-membership.json)
      echo "$SCHEMAS_DIR/room-membership.v1.schema.json"
      ;;
    *.room-event.json)
      echo "$SCHEMAS_DIR/room-event.v1.schema.json"
      ;;
    *.room-policy.json)
      echo "$SCHEMAS_DIR/room-policy.v1.schema.json"
      ;;
    *.room.json)
      echo "$SCHEMAS_DIR/room.v1.schema.json"
      ;;
    *.proof-of-personhood-attestation.json)
      echo "$SCHEMAS_DIR/proof-of-personhood-attestation.v1.schema.json"
      ;;
    *.ubc-allocation.json)
      echo "$SCHEMAS_DIR/ubc-allocation.v1.schema.json"
      ;;
    *.ubc-settlement.json)
      echo "$SCHEMAS_DIR/ubc-settlement.v1.schema.json"
      ;;
    *.room-metadata.json)
      echo "$SCHEMAS_DIR/answer-room-metadata.v1.schema.json"
      ;;
    *.segment.json)
      echo "$SCHEMAS_DIR/transcript-segment.v1.schema.json"
      ;;
    *.bundle.json)
      echo "$SCHEMAS_DIR/transcript-bundle.v1.schema.json"
      ;;
    *)
      echo ""
      ;;
  esac
}

validate_with_check_jsonschema() {
  schema_file=$1
  data_file=$2
  check-jsonschema \
    --schemafile "$schema_file" \
    --base-uri "file://$SCHEMAS_DIR/" \
    "$data_file" >/dev/null
}

validate_with_ajv() {
  schema_file=$1
  data_file=$2

  case "$schema_file" in
    *membership-invitation.v1.schema.json|*membership-sponsorship.v1.schema.json|*membership-acceptance.v1.schema.json|*participant-entry-profile.v1.schema.json|*participant-effective-limits.v1.schema.json|*surface-access-policy.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/_shared/membership-enums.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *transcript-bundle.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/transcript-segment.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *nym-certificate.v1.schema.json|*nym-renew-request.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/nym-succession.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *client-instance-attachment.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/participant-bind.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *client-instance-detachment.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/participant-bind.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *client-instance-recovery.v1.schema.json)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -r "$SCHEMAS_DIR/participant-bind.v1.schema.json" \
        -d "$data_file" >/dev/null
      ;;
    *)
      ajv validate \
        --spec=draft2020 \
        --strict=false \
        -s "$schema_file" \
        -d "$data_file" >/dev/null
      ;;
  esac
}

validate_file() {
  validator=$1
  data_file=$2
  expected=$3
  schema_file=$(schema_for_file "$data_file")

  if [ -z "$schema_file" ]; then
    echo "Cannot determine schema for file: $data_file" >&2
    return 1
  fi

  if [ "$validator" = "check-jsonschema" ]; then
    if validate_with_check_jsonschema "$schema_file" "$data_file"; then
      status=pass
    else
      status=fail
    fi
  else
    if validate_with_ajv "$schema_file" "$data_file"; then
      status=pass
    else
      status=fail
    fi
  fi

  if [ "$status" = "$expected" ]; then
    printf '%s %s\n' "$expected" "$data_file"
    return 0
  fi

  printf 'unexpected-%s %s\n' "$status" "$data_file" >&2
  return 1
}

echo "Checking JSON syntax..."
find "$SCHEMAS_DIR" -type f -name '*.json' -print | sort | while IFS= read -r file; do
  jq empty "$file"
done
echo "JSON syntax OK"

if [ "$MODE" = "--syntax-only" ]; then
  exit 0
fi

VALIDATOR=$(choose_validator)

if [ -z "$VALIDATOR" ]; then
  echo "No supported JSON Schema validator found." >&2
  echo "Install one of: check-jsonschema, ajv-cli" >&2
  exit 2
fi

echo "Using validator: $VALIDATOR"

echo "Validating positive examples..."
find "$VALID_EXAMPLES_DIR" -maxdepth 1 -type f -name '*.json' -print | sort | while IFS= read -r file; do
  validate_file "$VALIDATOR" "$file" pass
done

echo "Validating negative examples..."
find "$INVALID_EXAMPLES_DIR" -maxdepth 1 -type f -name '*.json' -print | sort | while IFS= read -r file; do
  validate_file "$VALIDATOR" "$file" fail
done

echo "Schema validation finished successfully."
