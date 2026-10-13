# Sensorium-device-discovery-candidate.v1

Source schema: [`doc/schemas/sensorium-device-discovery-candidate.v1.schema.json`](../../schemas/sensorium-device-discovery-candidate.v1.schema.json)

Ephemeral caller-private candidate. Label and selector are untrusted UTF-8 (256 encoded bytes enforced by host). Never put candidate or selector material or their digests into durable metadata, logs, receipts, outcomes or publications. Identity names a verification method, source and time/scope; selector kinds are not a trust ladder. Candidate validity is at most 120 seconds and cannot exceed identity validity. Restart/revoke invalidation remains host-owned.

## Governing Basis

- [`doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`](../../project/40-proposals/045-sensorium-local-enaction-stratum.md)
- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-device-discovery-candidate.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`candidate/ref`](#field-candidate-ref) | `yes` | string |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`caller/ref`](#field-caller-ref) | `yes` | string |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `sensorium-device-discovery.request.v1.schema.json#/$defs/profile` |  |
| [`transport/kind`](#field-transport-kind) | `yes` | enum: `ble`, `usb-serial`, `mdns` |  |
| [`transport/scope`](#field-transport-scope) | `yes` | ref: `sensorium-device-discovery.request.v1.schema.json#/$defs/scope` |  |
| [`label`](#field-label) | `yes` | string |  |
| [`selector`](#field-selector) | `yes` | object |  |
| [`identity`](#field-identity) | `yes` | object |  |
| [`expires/at-unix-ms`](#field-expires-at-unix-ms) | `yes` | integer |  |
| [`classification`](#field-classification) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "selector": {
      "properties": {
        "kind": {
          "const": "advertised-name"
        }
      },
      "required": [
        "kind"
      ]
    }
  },
  "required": [
    "selector"
  ]
}
```

Then:

```json
{
  "properties": {
    "identity": {
      "properties": {
        "method": {
          "const": "advertisement"
        },
        "source": {
          "const": "provider"
        }
      }
    },
    "transport/kind": {
      "const": "ble"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "selector": {
      "properties": {
        "kind": {
          "const": "transport-address"
        }
      },
      "required": [
        "kind"
      ]
    }
  },
  "required": [
    "selector"
  ]
}
```

Then:

```json
{
  "properties": {
    "identity": {
      "properties": {
        "method": {
          "const": "transport-observation"
        },
        "source": {
          "const": "provider"
        }
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
    "selector": {
      "properties": {
        "kind": {
          "const": "verified-serial"
        }
      },
      "required": [
        "kind"
      ]
    }
  },
  "required": [
    "selector"
  ]
}
```

Then:

```json
{
  "properties": {
    "identity": {
      "properties": {
        "method": {
          "const": "operator-verification"
        },
        "source": {
          "const": "operator"
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-device-discovery-candidate.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-candidate-ref"></a>
## `candidate/ref`

- Required: `yes`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-caller-ref"></a>
## `caller/ref`

- Required: `yes`
- Shape: string

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `sensorium-device-discovery.request.v1.schema.json#/$defs/profile`

<a id="field-transport-kind"></a>
## `transport/kind`

- Required: `yes`
- Shape: enum: `ble`, `usb-serial`, `mdns`

<a id="field-transport-scope"></a>
## `transport/scope`

- Required: `yes`
- Shape: ref: `sensorium-device-discovery.request.v1.schema.json#/$defs/scope`

<a id="field-label"></a>
## `label`

- Required: `yes`
- Shape: string

<a id="field-selector"></a>
## `selector`

- Required: `yes`
- Shape: object

<a id="field-identity"></a>
## `identity`

- Required: `yes`
- Shape: object

<a id="field-expires-at-unix-ms"></a>
## `expires/at-unix-ms`

- Required: `yes`
- Shape: integer

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: object
