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
    *.training-job.json)
      echo "$SCHEMAS_DIR/training-job.v1.schema.json"
      ;;
    *.eval-report.json)
      echo "$SCHEMAS_DIR/eval-report.v1.schema.json"
      ;;
    *.adapter-artifact.json)
      echo "$SCHEMAS_DIR/adapter-artifact.v1.schema.json"
      ;;
    *.node-identity.json)
      echo "$SCHEMAS_DIR/node-identity.v1.schema.json"
      ;;
    *.node-advertisement.json)
      echo "$SCHEMAS_DIR/node-advertisement.v1.schema.json"
      ;;
    *.service-offer.json)
      echo "$SCHEMAS_DIR/service-offer.v1.schema.json"
      ;;
    *.service-order.json)
      echo "$SCHEMAS_DIR/service-order.v1.schema.json"
      ;;
    *.peer-handshake.json)
      echo "$SCHEMAS_DIR/peer-handshake.v1.schema.json"
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
    *.capability-advertisement.json)
      echo "$SCHEMAS_DIR/capability-advertisement.v1.schema.json"
      ;;
    *.signal-marker-envelope.json)
      echo "$SCHEMAS_DIR/signal-marker-envelope.v1.schema.json"
      ;;
    *.signal-marker.json)
      echo "$SCHEMAS_DIR/signal-marker.v1.schema.json"
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
    *.association-room-proposal.json)
      echo "$SCHEMAS_DIR/association-room-proposal.v1.schema.json"
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
