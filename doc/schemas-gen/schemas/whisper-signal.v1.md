# Whisper Signal v1

Source schema: [`doc/schemas/whisper-signal.v1.schema.json`](../../schemas/whisper-signal.v1.schema.json)

Machine-readable schema for bounded rumor-style social-signal exchange.

## Governing Basis

- [`doc/project/20-memos/orbiplex-whisper.md`](../../project/20-memos/orbiplex-whisper.md)
- [`doc/project/20-memos/orbiplex-anon.md`](../../project/20-memos/orbiplex-anon.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`signal/id`](#field-signal-id) | `yes` | string | Stable identifier of the published rumor-style signal. |
| [`created-at`](#field-created-at) | `yes` | string | Publication timestamp of the outgoing signal. |
| [`sender/node-id`](#field-sender-node-id) | `yes` | string | Node that emitted the outgoing signal. |
| [`sender/federation-id`](#field-sender-federation-id) | `no` | string | Federation scope of the sender when relevant to routing or threshold policy. |
| [`rumor/nym`](#field-rumor-nym) | `yes` | string | Bounded outgoing pseudonym that is not a stable long-lived author identity. |
| [`epistemic/class`](#field-epistemic-class) | `yes` | enum: `rumor`, `weak-signal` | Explicit epistemic class that prevents the artifact from being treated as evidence. |
| [`signal/text`](#field-signal-text) | `yes` | string | Sanitized text accepted by the local user before publication. |
| [`topic/class`](#field-topic-class) | `yes` | string | Normalized issue class used for bounded correlation. |
| [`context/facets`](#field-context-facets) | `yes` | array | Normalized, low-resolution facets that help correlation without forcing raw disclosure. |
| [`confidence`](#field-confidence) | `yes` | number | Local confidence in the quality and relevance of the prepared signal. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `private-correlation`, `federation-scoped`, `cross-federation`, `public-aggregate-only` | Maximum disclosure posture allowed for this signal. |
| [`source/class`](#field-source-class) | `no` | enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived` | High-level origin class of the signal. `monus-derived` is used when a local Monus-like wellbeing module prepared the draft before Whisper publication. |
| [`risk/grade`](#field-risk-grade) | `yes` | enum: `low`, `moderate`, `high`, `critical` | Risk grade used to constrain later routing and disclosure. |
| [`routing/profile`](#field-routing-profile) | `yes` | enum: `direct`, `relayed`, `onion-relayed` | Requested outbound transport posture. |
| [`routing/failure-mode`](#field-routing-failure-mode) | `yes` | enum: `soft-fail`, `hard-fail` | Whether the sender allows downgrade if the requested transport posture cannot be satisfied. |
| [`relay/acceptable-classes`](#field-relay-acceptable-classes) | `no` | array | Optional relay classes acceptable for outbound privacy realization. |
| [`forwarding/max-hops`](#field-forwarding-max-hops) | `yes` | integer | Maximum number of relay hops allowed for the signal. |
| [`forwarding/budget`](#field-forwarding-budget) | `no` | integer | Maximum number of bounded forwards allowed under local policy. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation- or federation-local annotations that do not change the core semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "routing/profile": {
      "const": "direct"
    }
  },
  "required": [
    "routing/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "forwarding/max-hops": {
      "const": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "routing/failure-mode": {
      "const": "hard-fail"
    }
  },
  "required": [
    "routing/failure-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "routing/profile": {
      "enum": [
        "relayed",
        "onion-relayed"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-signal-id"></a>
## `signal/id`

- Required: `yes`
- Shape: string

Stable identifier of the published rumor-style signal.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Publication timestamp of the outgoing signal.

<a id="field-sender-node-id"></a>
## `sender/node-id`

- Required: `yes`
- Shape: string

Node that emitted the outgoing signal.

<a id="field-sender-federation-id"></a>
## `sender/federation-id`

- Required: `no`
- Shape: string

Federation scope of the sender when relevant to routing or threshold policy.

<a id="field-rumor-nym"></a>
## `rumor/nym`

- Required: `yes`
- Shape: string

Bounded outgoing pseudonym that is not a stable long-lived author identity.

<a id="field-epistemic-class"></a>
## `epistemic/class`

- Required: `yes`
- Shape: enum: `rumor`, `weak-signal`

Explicit epistemic class that prevents the artifact from being treated as evidence.

<a id="field-signal-text"></a>
## `signal/text`

- Required: `yes`
- Shape: string

Sanitized text accepted by the local user before publication.

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

Normalized issue class used for bounded correlation.

<a id="field-context-facets"></a>
## `context/facets`

- Required: `yes`
- Shape: array

Normalized, low-resolution facets that help correlation without forcing raw disclosure.

<a id="field-confidence"></a>
## `confidence`

- Required: `yes`
- Shape: number

Local confidence in the quality and relevance of the prepared signal.

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: enum: `private-correlation`, `federation-scoped`, `cross-federation`, `public-aggregate-only`

Maximum disclosure posture allowed for this signal.

<a id="field-source-class"></a>
## `source/class`

- Required: `no`
- Shape: enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`

High-level origin class of the signal. `monus-derived` is used when a local Monus-like wellbeing module prepared the draft before Whisper publication.

<a id="field-risk-grade"></a>
## `risk/grade`

- Required: `yes`
- Shape: enum: `low`, `moderate`, `high`, `critical`

Risk grade used to constrain later routing and disclosure.

<a id="field-routing-profile"></a>
## `routing/profile`

- Required: `yes`
- Shape: enum: `direct`, `relayed`, `onion-relayed`

Requested outbound transport posture.

<a id="field-routing-failure-mode"></a>
## `routing/failure-mode`

- Required: `yes`
- Shape: enum: `soft-fail`, `hard-fail`

Whether the sender allows downgrade if the requested transport posture cannot be satisfied.

<a id="field-relay-acceptable-classes"></a>
## `relay/acceptable-classes`

- Required: `no`
- Shape: array

Optional relay classes acceptable for outbound privacy realization.

<a id="field-forwarding-max-hops"></a>
## `forwarding/max-hops`

- Required: `yes`
- Shape: integer

Maximum number of relay hops allowed for the signal.

<a id="field-forwarding-budget"></a>
## `forwarding/budget`

- Required: `no`
- Shape: integer

Maximum number of bounded forwards allowed under local policy.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation- or federation-local annotations that do not change the core semantics.
