# Capability Advertisement v1

Source schema: [`doc/schemas/capability-advertisement.v1.schema.json`](../../schemas/capability-advertisement.v1.schema.json)

Machine-readable schema for baseline capability exchange after peer session establishment. The advertisement is a node-signed presentation of capability assertions in passport form. Seed Directory publication is optional: a Node may broadcast or directly answer with this artifact and include the credentials needed by the receiver to evaluate each presented capability under local policy.

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
| [`node/id`](#field-node-id) | `yes` | string | Node advertising its baseline capability surface. In v1 this MUST use the canonical `node:did:key:z...` format. |
| [`published-at`](#field-published-at) | `yes` | string | Timestamp when the capability set was published. |
| [`protocol/version`](#field-protocol-version) | `yes` | string | Protocol version for which the capability advertisement is valid. |
| [`transport/profiles`](#field-transport-profiles) | `yes` | array | Transport profiles currently exposed by the Node. |
| [`capabilities/core`](#field-capabilities-core) | `yes` | array | Compatibility and routing projection of the wire-visible capability identifiers supported by the Node. Values SHOULD be derived from `capabilities/presented[*].wire/name`. Known formal capabilities use stable `core/` or `role/` names, sovereign capabilities use `sovereign/`; `sovereign-informal/` remains accepted for legacy advertisements but new `~...@...` capability ids project to `sovereign/...`. Unknown formal capabilities may be advertised as bare names. |
| [`capabilities/presented`](#field-capabilities-presented) | `yes` | array | Passport-form capability assertions presented directly by this Node. Each item carries the canonical capability id, the wire-visible projection, an assertion kind, and the passport or passport-compatible credential needed to evaluate the claim without querying a Seed Directory. |
| [`anchor_identities`](#field-anchor-identities) | `no` | object | Optional sovereign capability anchor map keyed by the sovereign short name. Empty or absent for formal capabilities. |
| [`roles/attached`](#field-roles-attached) | `no` | array | Optional attached roles or plugin-process capabilities visible at the Node boundary. Not required in MVP. |
| [`surfaces/exposed`](#field-surfaces-exposed) | `no` | array | Exposed APIs, channels, or queues that can be used by peers or attached roles. |
| [`messages/supported`](#field-messages-supported) | `yes` | array | Protocol message families currently supported by the Node. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional annotations that do not change the core advertised capability semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capabilityPresentation`](#def-capabilitypresentation) | object |  |
| [`capabilityProfile`](#def-capabilityprofile) | object |  |
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "properties": {
    "capabilities/core": {
      "contains": {
        "const": "core/messaging"
      }
    }
  },
  "required": [
    "capabilities/core"
  ]
}
```

### Rule 2

Constraint:

```json
{
  "properties": {
    "capabilities/presented": {
      "contains": {
        "type": "object",
        "properties": {
          "wire/name": {
            "const": "core/messaging"
          }
        },
        "required": [
          "wire/name"
        ]
      }
    }
  },
  "required": [
    "capabilities/presented"
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

Node advertising its baseline capability surface. In v1 this MUST use the canonical `node:did:key:z...` format.

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

Compatibility and routing projection of the wire-visible capability identifiers supported by the Node. Values SHOULD be derived from `capabilities/presented[*].wire/name`. Known formal capabilities use stable `core/` or `role/` names, sovereign capabilities use `sovereign/`; `sovereign-informal/` remains accepted for legacy advertisements but new `~...@...` capability ids project to `sovereign/...`. Unknown formal capabilities may be advertised as bare names.

<a id="field-capabilities-presented"></a>
## `capabilities/presented`

- Required: `yes`
- Shape: array

Passport-form capability assertions presented directly by this Node. Each item carries the canonical capability id, the wire-visible projection, an assertion kind, and the passport or passport-compatible credential needed to evaluate the claim without querying a Seed Directory.

<a id="field-anchor-identities"></a>
## `anchor_identities`

- Required: `no`
- Shape: object

Optional sovereign capability anchor map keyed by the sovereign short name. Empty or absent for formal capabilities.

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

<a id="def-capabilitypresentation"></a>
## `$defs.capabilityPresentation`

- Shape: object

<a id="def-capabilityprofile"></a>
## `$defs.capabilityProfile`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
