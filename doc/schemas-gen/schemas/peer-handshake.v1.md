# Peer Handshake v1

Source schema: [`doc/schemas/peer-handshake.v1.schema.json`](../../schemas/peer-handshake.v1.schema.json)

Machine-readable schema for signed peer session establishment over the Node networking baseline.

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
| [`handshake/id`](#field-handshake-id) | `yes` | string | Stable identifier of this handshake attempt. |
| [`handshake/mode`](#field-handshake-mode) | `yes` | enum: `hello`, `ack` | Whether this artifact initiates or acknowledges a session attempt. |
| [`ack/of-handshake-id`](#field-ack-of-handshake-id) | `no` | string | Reference to the original handshake when `handshake/mode = ack`. |
| [`ts`](#field-ts) | `yes` | string | Timestamp of the handshake artifact. |
| [`sender/node-id`](#field-sender-node-id) | `yes` | string | Node sending this handshake artifact. |
| [`key/alg`](#field-key-alg) | `yes` | enum: `ed25519` | Algorithm of the sender key. |
| [`key/public`](#field-key-public) | `yes` | string | Public key corresponding to `sender/node-id`. |
| [`protocol/version`](#field-protocol-version) | `yes` | string | Protocol version requested or accepted for this session. |
| [`transport/profile`](#field-transport-profile) | `yes` | enum: `wss` | Baseline transport profile of the current session. |
| [`session/intent`](#field-session-intent) | `no` | enum: `bootstrap`, `peer-connect`, `reconnect` | High-level intent of this session attempt. |
| [`nonce`](#field-nonce) | `yes` | string | Fresh nonce used to bind this session attempt and reduce replay risk. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation-local annotations that do not change core session semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "handshake/mode": {
      "const": "ack"
    }
  },
  "required": [
    "handshake/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "ack/of-handshake-id"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-handshake-id"></a>
## `handshake/id`

- Required: `yes`
- Shape: string

Stable identifier of this handshake attempt.

<a id="field-handshake-mode"></a>
## `handshake/mode`

- Required: `yes`
- Shape: enum: `hello`, `ack`

Whether this artifact initiates or acknowledges a session attempt.

<a id="field-ack-of-handshake-id"></a>
## `ack/of-handshake-id`

- Required: `no`
- Shape: string

Reference to the original handshake when `handshake/mode = ack`.

<a id="field-ts"></a>
## `ts`

- Required: `yes`
- Shape: string

Timestamp of the handshake artifact.

<a id="field-sender-node-id"></a>
## `sender/node-id`

- Required: `yes`
- Shape: string

Node sending this handshake artifact.

<a id="field-key-alg"></a>
## `key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Algorithm of the sender key.

<a id="field-key-public"></a>
## `key/public`

- Required: `yes`
- Shape: string

Public key corresponding to `sender/node-id`.

<a id="field-protocol-version"></a>
## `protocol/version`

- Required: `yes`
- Shape: string

Protocol version requested or accepted for this session.

<a id="field-transport-profile"></a>
## `transport/profile`

- Required: `yes`
- Shape: enum: `wss`

Baseline transport profile of the current session.

<a id="field-session-intent"></a>
## `session/intent`

- Required: `no`
- Shape: enum: `bootstrap`, `peer-connect`, `reconnect`

High-level intent of this session attempt.

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

Fresh nonce used to bind this session attempt and reduce replay risk.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation-local annotations that do not change core session semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
