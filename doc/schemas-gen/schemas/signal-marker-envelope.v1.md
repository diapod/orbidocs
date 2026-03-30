# Signal Marker Envelope v1

Source schema: [`doc/schemas/signal-marker-envelope.v1.schema.json`](../../schemas/signal-marker-envelope.v1.schema.json)

Machine-readable schema for the participant-scoped signed wire envelope that publishes a signal marker reference over an established peer session.

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
| [`message/id`](#field-message-id) | `yes` | string | Stable identifier of this signed application envelope. |
| [`protocol/version`](#field-protocol-version) | `yes` | string | Protocol version understood by the sender for this envelope family. |
| [`message/kind`](#field-message-kind) | `yes` | const: `signal-marker-envelope.v1` | Canonical message family identifier for this participant-scoped wire envelope. |
| [`sender/participant-id`](#field-sender-participant-id) | `yes` | string | Participant identity that signs and emits this message. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp carried inside the signed envelope. |
| [`marker/ref`](#field-marker-ref) | `yes` | string | Stable reference to the signal-marker artifact or stream record pointed to by this envelope. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation-local annotations outside the minimal semantic core. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-message-id"></a>
## `message/id`

- Required: `yes`
- Shape: string

Stable identifier of this signed application envelope.

<a id="field-protocol-version"></a>
## `protocol/version`

- Required: `yes`
- Shape: string

Protocol version understood by the sender for this envelope family.

<a id="field-message-kind"></a>
## `message/kind`

- Required: `yes`
- Shape: const: `signal-marker-envelope.v1`

Canonical message family identifier for this participant-scoped wire envelope.

<a id="field-sender-participant-id"></a>
## `sender/participant-id`

- Required: `yes`
- Shape: string

Participant identity that signs and emits this message.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Creation timestamp carried inside the signed envelope.

<a id="field-marker-ref"></a>
## `marker/ref`

- Required: `yes`
- Shape: string

Stable reference to the signal-marker artifact or stream record pointed to by this envelope.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation-local annotations outside the minimal semantic core.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
