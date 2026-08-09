# Daemon NSE Offer Resolution Trace v1

Source schema: [`doc/schemas/daemon.nse-offer-resolution-trace.v1.schema.json`](../../schemas/daemon.nse-offer-resolution-trace.v1.schema.json)

Prompt-free host trace for one opaque NSE offer resolution attempt.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `daemon.nse-offer-resolution-trace.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
| [`offer/ref`](#field-offer-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | unspecified | Exact invocation reference only after the registry found an entry and authorized its caller; null for pre-registry, unknown-offer, foreign-caller, or unavailable-registry refusals. |
| [`offer/digest`](#field-offer-digest) | `yes` | unspecified | Exact offer digest only after the registry found an entry and authorized its caller; null for pre-registry, unknown-offer, foreign-caller, or unavailable-registry refusals. |
| [`hook/id`](#field-hook-id) | `yes` | string |  |
| [`caller/ref`](#field-caller-ref) | `yes` | string |  |
| [`lookup/status`](#field-lookup-status) | `yes` | enum: `not-inspected`, `registry-unavailable`, `unknown-offer`, `foreign-caller`, `matched` | Host-operator diagnostic that is never included in the caller decision projection. matched permits bound entry metadata; foreign-caller remains caller-visible only as identifier/invalid; not-inspected means a pre-registry hook allowlist refusal. |
| [`step/id`](#field-step-id) | `yes` | unspecified |  |
| [`producer/refs`](#field-producer-refs) | `yes` | array |  |
| [`evidence/count`](#field-evidence-count) | `yes` | integer |  |
| [`status`](#field-status) | `yes` | enum: `admitted`, `refused` |  |
| [`refusal/code`](#field-refusal-code) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "admitted"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "invocation/ref": {
      "type": "string"
    },
    "offer/digest": {
      "$ref": "#/$defs/digest"
    },
    "refusal/code": {
      "type": "null"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "refused"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "refusal/code": {
      "$ref": "operator-extension-refusal-code.v1.schema.json"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `daemon.nse-offer-resolution-trace.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

<a id="field-offer-ref"></a>
## `offer/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-invocation-ref"></a>
## `invocation/ref`

- Required: `yes`
- Shape: unspecified

Exact invocation reference only after the registry found an entry and authorized its caller; null for pre-registry, unknown-offer, foreign-caller, or unavailable-registry refusals.

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: unspecified

Exact offer digest only after the registry found an entry and authorized its caller; null for pre-registry, unknown-offer, foreign-caller, or unavailable-registry refusals.

<a id="field-hook-id"></a>
## `hook/id`

- Required: `yes`
- Shape: string

<a id="field-caller-ref"></a>
## `caller/ref`

- Required: `yes`
- Shape: string

<a id="field-lookup-status"></a>
## `lookup/status`

- Required: `yes`
- Shape: enum: `not-inspected`, `registry-unavailable`, `unknown-offer`, `foreign-caller`, `matched`

Host-operator diagnostic that is never included in the caller decision projection. matched permits bound entry metadata; foreign-caller remains caller-visible only as identifier/invalid; not-inspected means a pre-registry hook allowlist refusal.

<a id="field-step-id"></a>
## `step/id`

- Required: `yes`
- Shape: unspecified

<a id="field-producer-refs"></a>
## `producer/refs`

- Required: `yes`
- Shape: array

<a id="field-evidence-count"></a>
## `evidence/count`

- Required: `yes`
- Shape: integer

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `admitted`, `refused`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `yes`
- Shape: unspecified

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
