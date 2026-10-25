# Capability-issuance-request.v1

Source schema: [`doc/schemas/capability-issuance-request.v1.schema.json`](../../schemas/capability-issuance-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-issuance-request.v1` |  |
| [`request_id`](#field-request-id) | `yes` | string |  |
| [`federation_id`](#field-federation-id) | `yes` | string |  |
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`node_id`](#field-node-id) | `yes` | string |  |
| [`delegate_key`](#field-delegate-key) | `yes` | string |  |
| [`issued_at`](#field-issued-at) | `yes` | string |  |
| [`expires_at`](#field-expires-at) | `yes` | string |  |
| [`templates`](#field-templates) | `yes` | array |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`root_digest`](#field-root-digest) | `yes` | string |  |
| [`root_version`](#field-root-version) | `yes` | integer |  |
| [`signatures`](#field-signatures) | `yes` | array |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "templates": {
      "contains": {
        "properties": {
          "template": {
            "const": "nym-bootstrap-consent"
          }
        },
        "required": [
          "template"
        ]
      }
    }
  },
  "required": [
    "templates"
  ]
}
```

Then:

```json
{
  "properties": {
    "templates": {
      "maxItems": 1,
      "items": {
        "properties": {
          "template": {
            "const": "nym-bootstrap-consent"
          },
          "issuance_caller": {
            "const": "host:nym-bootstrap.accept"
          },
          "max_passport_ttl_seconds": {
            "maximum": 900
          }
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
- Shape: const: `capability-issuance-request.v1`

<a id="field-request-id"></a>
## `request_id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

<a id="field-delegate-key"></a>
## `delegate_key`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

<a id="field-templates"></a>
## `templates`

- Required: `yes`
- Shape: array

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

<a id="field-root-digest"></a>
## `root_digest`

- Required: `yes`
- Shape: string

<a id="field-root-version"></a>
## `root_version`

- Required: `yes`
- Shape: integer

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array
