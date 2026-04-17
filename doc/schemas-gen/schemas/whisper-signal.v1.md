# Whisper Signal v1

Source schema: [`doc/schemas/whisper-signal.v1.schema.json`](../../schemas/whisper-signal.v1.schema.json)

Machine-readable schema for the content body of an Agora record (or INAC artefact) expressing a bounded rumor-style social signal. The enclosing `agora-record.v1` envelope carries identity, authorship (including pseudonymous `nym:did:key:…` authorship and the attached nym-certificate reference), authorship signature, timestamping, and topic routing; this schema validates only the content body. Sender transport identifiers (node id, federation id) are peer-session concerns and are not part of the signed content body.

## Governing Basis

- [`doc/project/20-memos/orbiplex-whisper.md`](../../project/20-memos/orbiplex-whisper.md)
- [`doc/project/20-memos/orbiplex-anon.md`](../../project/20-memos/orbiplex-anon.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline.md)
- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/041-agora-ingest-attestation.md`](../../project/40-proposals/041-agora-ingest-attestation.md)
- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)
- [`doc/project/50-requirements/requirements-014.md`](../../project/50-requirements/requirements-014.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-signal.v1` | Content-level discriminator for consumers that inspect the payload outside its Agora or INAC envelope. |
| [`epistemic/class`](#field-epistemic-class) | `yes` | enum: `rumor`, `weak-signal` | Explicit epistemic class that prevents the artifact from being treated as evidence. |
| [`signal/text`](#field-signal-text) | `yes` | string | Sanitized text accepted by the local user before publication. |
| [`topic/class`](#field-topic-class) | `yes` | string | Normalized issue class used for bounded correlation. Distinct from the enclosing envelope's `topic/key`, which is an Agora routing key; `topic/class` is the semantic correlation class carried inside the rumor body. |
| [`context/facets`](#field-context-facets) | `yes` | array | Normalized, low-resolution facets that help correlation without forcing raw disclosure. |
| [`confidence`](#field-confidence) | `yes` | number | Local confidence in the quality and relevance of the prepared signal. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `private-correlation`, `federation-scoped`, `cross-federation`, `public-aggregate-only` | Maximum disclosure posture allowed for this signal. Distribution-surface selection honours this: `private-correlation` SHOULD travel via INAC direct exchange (proposal 042); wider scopes MAY use Agora. The `SHOULD` is intentional — public Agora deployments SHOULD refuse `private-correlation` at ingest (its publication properties conflict with the disclosure intent), while closed / intra-organization Agora federations MAY carry these whispers internally under their own ingest policy. |
| [`source/class`](#field-source-class) | `no` | enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, `monus-sensorium-derived` | High-level origin class of the signal. `monus-derived` is used when a local Monus-like wellbeing module prepared the draft before Whisper publication. `monus-sensorium-derived` is used when Monus relied materially on Sensorium-originated local signals. |
| [`source/signal-kinds`](#field-source-signal-kinds) | `no` | array | Optional high-level local signal classes that materially informed a derived or sensorium-assisted rumor draft. |
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

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-signal.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora or INAC envelope.

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

Normalized issue class used for bounded correlation. Distinct from the enclosing envelope's `topic/key`, which is an Agora routing key; `topic/class` is the semantic correlation class carried inside the rumor body.

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

Maximum disclosure posture allowed for this signal. Distribution-surface selection honours this: `private-correlation` SHOULD travel via INAC direct exchange (proposal 042); wider scopes MAY use Agora. The `SHOULD` is intentional — public Agora deployments SHOULD refuse `private-correlation` at ingest (its publication properties conflict with the disclosure intent), while closed / intra-organization Agora federations MAY carry these whispers internally under their own ingest policy.

<a id="field-source-class"></a>
## `source/class`

- Required: `no`
- Shape: enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, `monus-sensorium-derived`

High-level origin class of the signal. `monus-derived` is used when a local Monus-like wellbeing module prepared the draft before Whisper publication. `monus-sensorium-derived` is used when Monus relied materially on Sensorium-originated local signals.

<a id="field-source-signal-kinds"></a>
## `source/signal-kinds`

- Required: `no`
- Shape: array

Optional high-level local signal classes that materially informed a derived or sensorium-assisted rumor draft.

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
