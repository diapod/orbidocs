# Nym-issuance-readback.local.v1

Source schema: [`doc/schemas/nym-issuance-readback.local.v1.schema.json`](../../schemas/nym-issuance-readback.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-readback.local.v1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`issuer/peer`](#field-issuer-peer) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`reply/key-offer`](#field-reply-key-offer) | `yes` | unspecified |  |
| [`reply/decision`](#field-reply-decision) | `yes` | unspecified |  |
| [`request/ref`](#field-request-ref) | `yes` | unspecified | Digest of the exact privately signed issuance request; never a transport handle or public AD identifier. |
| [`state`](#field-state) | `yes` | enum: `preparing`, `reconciliation-required`, `preview-expired`, `awaiting-recovery`, `document-prepared`, `key-request-prepared`, `key-request-delivered`, `request-prepared`, `request-delivered`, `decision-received` |  |
| [`nym/id`](#field-nym-id) | `yes` | unspecified |  |
| [`key-request/delivery`](#field-key-request-delivery) | `yes` | enum: `not-requested`, `prepared`, `delivered` |  |
| [`request/delivery`](#field-request-delivery) | `yes` | enum: `not-requested`, `prepared`, `delivered` |  |
| [`decision`](#field-decision) | `yes` | enum: `None`, `issued`, `refused`, `reset-required` |  |
| [`decision/reason`](#field-decision-reason) | `yes` | enum: `None`, `policy-denied`, `request-expired`, `binding-unavailable`, `context-unavailable`, `capacity-exceeded`, `reset-required` |  |
| [`certificate`](#field-certificate) | `yes` | unspecified |  |
| [`certificate/state`](#field-certificate-state) | `yes` | enum: `None`, `present`, `expired` |  |
| [`status/freshness`](#field-status-freshness) | `yes` | enum: `fresh`, `unknown` |  |
| [`recovery/current`](#field-recovery-current) | `yes` | boolean |  |
| [`status/collection-freshness`](#field-status-collection-freshness) | `yes` | enum: `fresh`, `unknown` |  |
| [`status/emission-freshness`](#field-status-emission-freshness) | `yes` | enum: `fresh`, `unknown` |  |
| [`certificate/eligibility`](#field-certificate-eligibility) | `yes` | enum: `accepted`, `revoked`, `activation-pending`, `unknown` |  |
| [`status/minimum-revision`](#field-status-minimum-revision) | `no` | integer |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
| [`source/activation-not-before`](#field-source-activation-not-before) | `no` | string |  |
| [`reply/decision-consent-until`](#field-reply-decision-consent-until) | `yes` | string | Maximum original result-reception policy horizon (target epoch end plus tombstone retention), not evidence of current issuer availability. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "decision": {
      "const": "issued"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "certificate": {
      "type": "object"
    },
    "certificate/state": {
      "enum": [
        "present",
        "expired"
      ]
    },
    "decision/reason": {
      "type": "null"
    },
    "state": {
      "const": "decision-received"
    }
  },
  "required": [
    "status/minimum-revision",
    "source/activation-not-before"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "decision": {
      "type": "null"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "decision/reason": {
      "type": "null"
    },
    "state": {
      "not": {
        "const": "decision-received"
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "certificate/eligibility": {
      "enum": [
        "accepted",
        "revoked",
        "activation-pending"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "decision": {
      "const": "issued"
    },
    "certificate": {
      "type": "object"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-readback.local.v1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-issuer-peer"></a>
## `issuer/peer`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-reply-key-offer"></a>
## `reply/key-offer`

- Required: `yes`
- Shape: unspecified

<a id="field-reply-decision"></a>
## `reply/decision`

- Required: `yes`
- Shape: unspecified

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: unspecified

Digest of the exact privately signed issuance request; never a transport handle or public AD identifier.

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `preparing`, `reconciliation-required`, `preview-expired`, `awaiting-recovery`, `document-prepared`, `key-request-prepared`, `key-request-delivered`, `request-prepared`, `request-delivered`, `decision-received`

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: unspecified

<a id="field-key-request-delivery"></a>
## `key-request/delivery`

- Required: `yes`
- Shape: enum: `not-requested`, `prepared`, `delivered`

<a id="field-request-delivery"></a>
## `request/delivery`

- Required: `yes`
- Shape: enum: `not-requested`, `prepared`, `delivered`

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `None`, `issued`, `refused`, `reset-required`

<a id="field-decision-reason"></a>
## `decision/reason`

- Required: `yes`
- Shape: enum: `None`, `policy-denied`, `request-expired`, `binding-unavailable`, `context-unavailable`, `capacity-exceeded`, `reset-required`

<a id="field-certificate"></a>
## `certificate`

- Required: `yes`
- Shape: unspecified

<a id="field-certificate-state"></a>
## `certificate/state`

- Required: `yes`
- Shape: enum: `None`, `present`, `expired`

<a id="field-status-freshness"></a>
## `status/freshness`

- Required: `yes`
- Shape: enum: `fresh`, `unknown`

<a id="field-recovery-current"></a>
## `recovery/current`

- Required: `yes`
- Shape: boolean

<a id="field-status-collection-freshness"></a>
## `status/collection-freshness`

- Required: `yes`
- Shape: enum: `fresh`, `unknown`

<a id="field-status-emission-freshness"></a>
## `status/emission-freshness`

- Required: `yes`
- Shape: enum: `fresh`, `unknown`

<a id="field-certificate-eligibility"></a>
## `certificate/eligibility`

- Required: `yes`
- Shape: enum: `accepted`, `revoked`, `activation-pending`, `unknown`

<a id="field-status-minimum-revision"></a>
## `status/minimum-revision`

- Required: `no`
- Shape: integer

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

<a id="field-source-activation-not-before"></a>
## `source/activation-not-before`

- Required: `no`
- Shape: string

<a id="field-reply-decision-consent-until"></a>
## `reply/decision-consent-until`

- Required: `yes`
- Shape: string

Maximum original result-reception policy horizon (target epoch end plus tombstone retention), not evidence of current issuer availability.
