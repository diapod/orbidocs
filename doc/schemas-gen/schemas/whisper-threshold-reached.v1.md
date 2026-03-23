# Whisper Threshold Reached v1

Source schema: [`doc/schemas/whisper-threshold-reached.v1.schema.json`](../../schemas/whisper-threshold-reached.v1.schema.json)

Machine-readable schema for a threshold event indicating sufficient aligned whisper interest for association bootstrap.

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
| [`threshold/id`](#field-threshold-id) | `yes` | string | Stable identifier of the recognized threshold event. |
| [`cluster/id`](#field-cluster-id) | `yes` | string | Correlation cluster identifier shared with later association proposals. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp of threshold recognition. |
| [`detector/node-id`](#field-detector-node-id) | `yes` | string | Node that emitted the threshold event. |
| [`topic/class`](#field-topic-class) | `yes` | string | Issue class for which critical mass was detected. |
| [`threshold/policy-ref`](#field-threshold-policy-ref) | `yes` | string | Reference to the threshold policy used for recognition. |
| [`participants/distinct-node-count`](#field-participants-distinct-node-count) | `yes` | integer | Number of distinct nodes that contributed sufficient aligned signals or interest. |
| [`participants/interest-count`](#field-participants-interest-count) | `yes` | integer | Number of counted interest registrations in the cluster. |
| [`participants/trust-summary`](#field-participants-trust-summary) | `no` | object | Optional aggregate trust-tier or diversity summary. |
| [`bootstrap/candidate-node-ids`](#field-bootstrap-candidate-node-ids) | `yes` | array | Candidate nodes from which a deterministic bootstrap subset may be derived. |
| [`disclosure/profile`](#field-disclosure-profile) | `yes` | enum: `aggregate-notice-only`, `room-opt-in`, `witness-reviewed` | Disclosure posture allowed at threshold crossing. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-threshold-id"></a>
## `threshold/id`

- Required: `yes`
- Shape: string

Stable identifier of the recognized threshold event.

<a id="field-cluster-id"></a>
## `cluster/id`

- Required: `yes`
- Shape: string

Correlation cluster identifier shared with later association proposals.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp of threshold recognition.

<a id="field-detector-node-id"></a>
## `detector/node-id`

- Required: `yes`
- Shape: string

Node that emitted the threshold event.

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

Issue class for which critical mass was detected.

<a id="field-threshold-policy-ref"></a>
## `threshold/policy-ref`

- Required: `yes`
- Shape: string

Reference to the threshold policy used for recognition.

<a id="field-participants-distinct-node-count"></a>
## `participants/distinct-node-count`

- Required: `yes`
- Shape: integer

Number of distinct nodes that contributed sufficient aligned signals or interest.

<a id="field-participants-interest-count"></a>
## `participants/interest-count`

- Required: `yes`
- Shape: integer

Number of counted interest registrations in the cluster.

<a id="field-participants-trust-summary"></a>
## `participants/trust-summary`

- Required: `no`
- Shape: object

Optional aggregate trust-tier or diversity summary.

<a id="field-bootstrap-candidate-node-ids"></a>
## `bootstrap/candidate-node-ids`

- Required: `yes`
- Shape: array

Candidate nodes from which a deterministic bootstrap subset may be derived.

<a id="field-disclosure-profile"></a>
## `disclosure/profile`

- Required: `yes`
- Shape: enum: `aggregate-notice-only`, `room-opt-in`, `witness-reviewed`

Disclosure posture allowed at threshold crossing.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
