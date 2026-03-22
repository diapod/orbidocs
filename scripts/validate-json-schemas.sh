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
