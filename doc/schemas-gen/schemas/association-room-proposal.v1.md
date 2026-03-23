# Association Room Proposal v1

Source schema: [`doc/schemas/association-room-proposal.v1.schema.json`](../../schemas/association-room-proposal.v1.schema.json)

Machine-readable schema for a deterministic bootstrap proposal of an opt-in association room.

## Governing Basis

- [`doc/project/20-memos/orbiplex-whisper.md`](../../project/20-memos/orbiplex-whisper.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`proposal/id`](#field-proposal-id) | `yes` | string | Stable identifier of the room bootstrap proposal. |
| [`cluster/id`](#field-cluster-id) | `yes` | string | Correlation cluster identifier that justified the proposal. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp of proposal publication. |
| [`proposal/node-id`](#field-proposal-node-id) | `yes` | string | Node that published the proposal artifact. |
| [`room/id`](#field-room-id) | `yes` | string | Identifier of the proposed association room or process. |
| [`room-policy/profile`](#field-room-policy-profile) | `yes` | enum: `mediated-only`, `witness-mediated`, `direct-live-allowed` | Initial room policy profile for the next-stage space. |
| [`disclosure/profile`](#field-disclosure-profile) | `yes` | enum: `minimal-disclosure`, `room-opt-in`, `witness-reviewed` | Disclosure posture to be applied before and during enrollment. |
| [`bootstrap/node-ids`](#field-bootstrap-node-ids) | `yes` | array | Nodes that form the bootstrap witness or proposal set. |
| [`bootstrap/expires-at`](#field-bootstrap-expires-at) | `yes` | string | Time after which the proposal must be reconsidered or discarded. |
| [`human-opt-in/required`](#field-human-opt-in-required) | `yes` | const: `True` | Human enrollment must remain opt-in. |
| [`moderation/mode`](#field-moderation-mode) | `yes` | enum: `bootstrap-witness-set`, `mediated`, `federated-review` | Initial moderation or witness posture of the proposed room. |
| [`participants/min-opt-in-count`](#field-participants-min-opt-in-count) | `yes` | integer | Minimum number of human opt-ins required before the room is considered active. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-proposal-id"></a>
## `proposal/id`

- Required: `yes`
- Shape: string

Stable identifier of the room bootstrap proposal.

<a id="field-cluster-id"></a>
## `cluster/id`

- Required: `yes`
- Shape: string

Correlation cluster identifier that justified the proposal.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp of proposal publication.

<a id="field-proposal-node-id"></a>
## `proposal/node-id`

- Required: `yes`
- Shape: string

Node that published the proposal artifact.

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

Identifier of the proposed association room or process.

<a id="field-room-policy-profile"></a>
## `room-policy/profile`

- Required: `yes`
- Shape: enum: `mediated-only`, `witness-mediated`, `direct-live-allowed`

Initial room policy profile for the next-stage space.

<a id="field-disclosure-profile"></a>
## `disclosure/profile`

- Required: `yes`
- Shape: enum: `minimal-disclosure`, `room-opt-in`, `witness-reviewed`

Disclosure posture to be applied before and during enrollment.

<a id="field-bootstrap-node-ids"></a>
## `bootstrap/node-ids`

- Required: `yes`
- Shape: array

Nodes that form the bootstrap witness or proposal set.

<a id="field-bootstrap-expires-at"></a>
## `bootstrap/expires-at`

- Required: `yes`
- Shape: string

Time after which the proposal must be reconsidered or discarded.

<a id="field-human-opt-in-required"></a>
## `human-opt-in/required`

- Required: `yes`
- Shape: const: `True`

Human enrollment must remain opt-in.

<a id="field-moderation-mode"></a>
## `moderation/mode`

- Required: `yes`
- Shape: enum: `bootstrap-witness-set`, `mediated`, `federated-review`

Initial moderation or witness posture of the proposed room.

<a id="field-participants-min-opt-in-count"></a>
## `participants/min-opt-in-count`

- Required: `yes`
- Shape: integer

Minimum number of human opt-ins required before the room is considered active.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
