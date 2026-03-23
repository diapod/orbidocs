# Capability Advertisement v1

Source schema: [`doc/schemas/capability-advertisement.v1.schema.json`](../../schemas/capability-advertisement.v1.schema.json)

Machine-readable schema for baseline capability exchange after peer session establishment.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/60-solutions/node.md`](../../project/60-solutions/node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`advertisement/id`](#field-advertisement-id) | `yes` | string | Stable identifier of this capability advertisement. |
| [`node/id`](#field-node-id) | `yes` | string | Node advertising its baseline capability surface. |
| [`published-at`](#field-published-at) | `yes` | string | Timestamp when the capability set was published. |
| [`protocol/version`](#field-protocol-version) | `yes` | string | Protocol version for which the capability advertisement is valid. |
| [`transport/profiles`](#field-transport-profiles) | `yes` | array | Transport profiles currently exposed by the Node. |
| [`capabilities/core`](#field-capabilities-core) | `yes` | array | Schematic capability identifiers supported by the Node. MVP capability advertisement is intentionally limited to a narrow core and MUST at least include `core/node-participant`. |
| [`roles/attached`](#field-roles-attached) | `no` | array | Optional attached roles or plugin-process capabilities visible at the Node boundary. Not required in MVP. |
| [`surfaces/exposed`](#field-surfaces-exposed) | `no` | array | Exposed APIs, channels, or queues that can be used by peers or attached roles. |
| [`messages/supported`](#field-messages-supported) | `yes` | array | Protocol message families currently supported by the Node. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional annotations that do not change the core advertised capability semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "properties": {
    "capabilities/core": {
      "contains": {
        "const": "core/node-participant"
      }
    }
  },
  "required": [
    "capabilities/core"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-advertisement-id"></a>
## `advertisement/id`

- Required: `yes`
- Shape: string

Stable identifier of this capability advertisement.

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

Node advertising its baseline capability surface.

<a id="field-published-at"></a>
## `published-at`

- Required: `yes`
- Shape: string

Timestamp when the capability set was published.

<a id="field-protocol-version"></a>
## `protocol/version`

- Required: `yes`
- Shape: string

Protocol version for which the capability advertisement is valid.

<a id="field-transport-profiles"></a>
## `transport/profiles`

- Required: `yes`
- Shape: array

Transport profiles currently exposed by the Node.

<a id="field-capabilities-core"></a>
## `capabilities/core`

- Required: `yes`
- Shape: array

Schematic capability identifiers supported by the Node. MVP capability advertisement is intentionally limited to a narrow core and MUST at least include `core/node-participant`.

<a id="field-roles-attached"></a>
## `roles/attached`

- Required: `no`
- Shape: array

Optional attached roles or plugin-process capabilities visible at the Node boundary. Not required in MVP.

<a id="field-surfaces-exposed"></a>
## `surfaces/exposed`

- Required: `no`
- Shape: array

Exposed APIs, channels, or queues that can be used by peers or attached roles.

<a id="field-messages-supported"></a>
## `messages/supported`

- Required: `yes`
- Shape: array

Protocol message families currently supported by the Node.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional annotations that do not change the core advertised capability semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
