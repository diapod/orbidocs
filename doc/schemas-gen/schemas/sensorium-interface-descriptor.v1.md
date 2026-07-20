# Sensorium Interface Descriptor v1

Source schema: [`doc/schemas/sensorium-interface-descriptor.v1.schema.json`](../../schemas/sensorium-interface-descriptor.v1.schema.json)

Immutable publication contract for one deliberately exposed Sensorium or Workbench projection.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-descriptor.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`interface/id`](#field-interface-id) | `yes` | string | Stable resource identifier for this interface publication. |
| [`interface/kind`](#field-interface-kind) | `yes` | const: `observation` | Directional resource kind. |
| [`interface/name`](#field-interface-name) | `yes` | string | Short operator-facing name; not an authority identifier. |
| [`publisher/node-ref`](#field-publisher-node-ref) | `yes` | string | Node that owns publication and source-side policy. |
| [`output/schema-ref`](#field-output-schema-ref) | `yes` | string | Schema required for each data frame payload. |
| [`delivery/semantics`](#field-delivery-semantics) | `yes` | enum: `latest-state`, `ordered-events` | Whether the interface exposes one current snapshot or a bounded ordered event window. |
| [`access/modes`](#field-access-modes) | `yes` | array | Operations that may be granted for this interface. |
| [`classification/max-tier`](#field-classification-max-tier) | `yes` | enum: `Public`, `Community`, `Personal` | Most restrictive effective tier this interface accepts at egress. |
| [`classification/topic-class`](#field-classification-topic-class) | `yes` | string | Exact topic-class binding required for Interface declassification facts. |
| [`redaction/profile-ref`](#field-redaction-profile-ref) | `no` | string | Optional source-owned redaction profile applied before frame creation. |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | string | Opaque host-derived identity of the concrete source generation. |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`supersedes/interface-id`](#field-supersedes-interface-id) | `no` | string | Prior publication atomically replaced by this publication. |
| [`limits`](#field-limits) | `yes` | object | Hard publication ceilings further narrowed by callers and host policy. |
| [`overflow/policy`](#field-overflow-policy) | `yes` | enum: `coalesce-latest`, `emit-gap`, `close-subscription` | Explicit behavior when source state exceeds its delivery window. |
| [`published/at`](#field-published-at) | `yes` | string | Publication creation time. |
| [`expires/at`](#field-expires-at) | `yes` | string | Hard end of the publication lifetime. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "delivery/semantics": {
      "const": "latest-state"
    }
  },
  "required": [
    "delivery/semantics"
  ]
}
```

Then:

```json
{
  "properties": {
    "overflow/policy": {
      "const": "coalesce-latest"
    },
    "limits": {
      "not": {
        "anyOf": [
          {
            "required": [
              "replay/max-frames"
            ]
          },
          {
            "required": [
              "replay/max-seconds"
            ]
          }
        ]
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "delivery/semantics": {
      "const": "ordered-events"
    }
  },
  "required": [
    "delivery/semantics"
  ]
}
```

Then:

```json
{
  "properties": {
    "overflow/policy": {
      "enum": [
        "emit-gap",
        "close-subscription"
      ]
    },
    "limits": {
      "required": [
        "replay/max-frames",
        "replay/max-seconds"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-descriptor.v1`

Contract discriminator.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Contract version.

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

Stable resource identifier for this interface publication.

<a id="field-interface-kind"></a>
## `interface/kind`

- Required: `yes`
- Shape: const: `observation`

Directional resource kind.

<a id="field-interface-name"></a>
## `interface/name`

- Required: `yes`
- Shape: string

Short operator-facing name; not an authority identifier.

<a id="field-publisher-node-ref"></a>
## `publisher/node-ref`

- Required: `yes`
- Shape: string

Node that owns publication and source-side policy.

<a id="field-output-schema-ref"></a>
## `output/schema-ref`

- Required: `yes`
- Shape: string

Schema required for each data frame payload.

<a id="field-delivery-semantics"></a>
## `delivery/semantics`

- Required: `yes`
- Shape: enum: `latest-state`, `ordered-events`

Whether the interface exposes one current snapshot or a bounded ordered event window.

<a id="field-access-modes"></a>
## `access/modes`

- Required: `yes`
- Shape: array

Operations that may be granted for this interface.

<a id="field-classification-max-tier"></a>
## `classification/max-tier`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

Most restrictive effective tier this interface accepts at egress.

<a id="field-classification-topic-class"></a>
## `classification/topic-class`

- Required: `yes`
- Shape: string

Exact topic-class binding required for Interface declassification facts.

<a id="field-redaction-profile-ref"></a>
## `redaction/profile-ref`

- Required: `no`
- Shape: string

Optional source-owned redaction profile applied before frame creation.

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: string

Opaque host-derived identity of the concrete source generation.

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-supersedes-interface-id"></a>
## `supersedes/interface-id`

- Required: `no`
- Shape: string

Prior publication atomically replaced by this publication.

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

Hard publication ceilings further narrowed by callers and host policy.

<a id="field-overflow-policy"></a>
## `overflow/policy`

- Required: `yes`
- Shape: enum: `coalesce-latest`, `emit-gap`, `close-subscription`

Explicit behavior when source state exceeds its delivery window.

<a id="field-published-at"></a>
## `published/at`

- Required: `yes`
- Shape: string

Publication creation time.

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

Hard end of the publication lifetime.
