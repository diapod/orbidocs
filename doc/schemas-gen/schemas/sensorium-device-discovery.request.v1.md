# Sensorium-device-discovery.request.v1

Source schema: [`doc/schemas/sensorium-device-discovery.request.v1.schema.json`](../../schemas/sensorium-device-discovery.request.v1.schema.json)

Private bounded discovery intent. The host derives authority and resolves scope; caller parameters never grant permission. Finite limits are hard ceilings, narrowed by admitted profiles and policy. Exact deadlines require host cleanup margin. No acquisition, probing, automatic observation or retention of identifiers.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-device-discovery.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`discovery/mode`](#field-discovery-mode) | `yes` | enum: `passive`, `active` |  |
| [`transport/kind`](#field-transport-kind) | `yes` | enum: `ble`, `usb-serial`, `mdns` |  |
| [`transport/scope`](#field-transport-scope) | `yes` | object |  |
| [`filters`](#field-filters) | `yes` | object |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`budgets`](#field-budgets) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`profile`](#def-profile) | object |  |
| [`scope`](#def-scope) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "transport/kind": {
      "const": "ble"
    }
  },
  "required": [
    "transport/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "filters": {
      "not": {
        "anyOf": [
          {
            "required": [
              "usb/vendor-id"
            ]
          },
          {
            "required": [
              "usb/product-id"
            ]
          },
          {
            "required": [
              "mdns/service-type"
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
    "transport/kind": {
      "const": "usb-serial"
    }
  },
  "required": [
    "transport/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "filters": {
      "not": {
        "anyOf": [
          {
            "required": [
              "advertised-name/prefix"
            ]
          },
          {
            "required": [
              "advertised-name/exact"
            ]
          },
          {
            "required": [
              "service/uuid"
            ]
          },
          {
            "required": [
              "mdns/service-type"
            ]
          }
        ]
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
    "transport/kind": {
      "const": "mdns"
    }
  },
  "required": [
    "transport/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "filters": {
      "not": {
        "anyOf": [
          {
            "required": [
              "advertised-name/prefix"
            ]
          },
          {
            "required": [
              "advertised-name/exact"
            ]
          },
          {
            "required": [
              "service/uuid"
            ]
          },
          {
            "required": [
              "usb/vendor-id"
            ]
          },
          {
            "required": [
              "usb/product-id"
            ]
          }
        ]
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-device-discovery.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-discovery-mode"></a>
## `discovery/mode`

- Required: `yes`
- Shape: enum: `passive`, `active`

<a id="field-transport-kind"></a>
## `transport/kind`

- Required: `yes`
- Shape: enum: `ble`, `usb-serial`, `mdns`

<a id="field-transport-scope"></a>
## `transport/scope`

- Required: `yes`
- Shape: object

<a id="field-filters"></a>
## `filters`

- Required: `yes`
- Shape: object

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-profile"></a>
## `$defs.profile`

- Shape: object

<a id="def-scope"></a>
## `$defs.scope`

- Shape: object
