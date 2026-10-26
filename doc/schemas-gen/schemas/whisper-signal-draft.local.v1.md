# Whisper-signal-draft.local.v1

Source schema: [`doc/schemas/whisper-signal-draft.local.v1.schema.json`](../../schemas/whisper-signal-draft.local.v1.schema.json)

Reviewed local body before host-derived profile, context, epoch and source fields. This draft has no admission or publication authority.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `no` | const: `whisper-signal.v2` |  |
| [`signal/polarity`](#field-signal-polarity) | `yes` | enum: `problem`, `idea` | Fundamental polarity of the whisper signal. `problem` describes a distributed harm, failure, or dignity risk that may require correlation and protective response. `idea` describes a convergent idea, creative discovery, or emerging approach that may justify co-creation. Emergency handling MUST NOT be triggered solely by an `idea` signal. |
| [`epistemic/class`](#field-epistemic-class) | `yes` | enum: `rumor`, `weak-signal` | Explicit epistemic class that prevents the artifact from being treated as evidence. |
| [`signal/text`](#field-signal-text) | `yes` | string | Sanitized text accepted by the local user before publication. |
| [`signal/text-native`](#field-signal-text-native) | `no` | string | Optional sanitized text in the original non-English language. Use this only when the original accepted user-facing wording is not English; English text stays solely in `signal/text`. |
| [`signal/text-native-lang`](#field-signal-text-native-lang) | `no` | string | BCP 47-like language tag for `signal/text-native`. This field is intentionally non-English; English originals MUST omit both native-text fields and use only `signal/text`. |
| [`topic/class`](#field-topic-class) | `yes` | string | Normalized issue class used for bounded correlation. Distinct from the enclosing envelope's `topic/key`, which is an Agora routing key; `topic/class` is the semantic correlation class carried inside the rumor body. |
| [`signal/similarity-key`](#field-signal-similarity-key) | `yes` | string | Exact contextual correlation key. This required value is bound by the certificate profile/context; semantic similarity remains separate policy. |
| [`context/facets`](#field-context-facets) | `yes` | array | Normalized, low-resolution facets that help correlation without forcing raw disclosure. |
| [`confidence`](#field-confidence) | `yes` | number | Local confidence in the quality and relevance of the prepared signal. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `federation-scoped`, `cross-federation`, `public-aggregate-only` | Maximum disclosure posture for the contextual signal. Public Agora ingress does not admit private-correlation; this value grants no dissemination authority. |
| [`source/class`](#field-source-class) | `no` | enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, `monus-sensorium-derived` | High-level origin class of the signal. `monus-derived` is used when a local Monus-like wellbeing module prepared the draft before Whisper publication. `monus-sensorium-derived` is used when Monus relied materially on Sensorium-originated local signals. |
| [`source/signal-kinds`](#field-source-signal-kinds) | `no` | array | Optional high-level local signal classes that materially informed a derived or sensorium-assisted rumor draft. |
| [`signal/grade`](#field-signal-grade) | `yes` | enum: `low`, `moderate`, `high`, `critical` | Signal salience grade. For `problem` signals this grades protective risk and urgency. For `idea` signals this grades convergence strength, co-creation potential, or urgency of matching interested participants. Routing and disclosure policy MAY interpret the same scale differently by `signal/polarity`. |
| [`routing/profile`](#field-routing-profile) | `yes` | enum: `direct`, `relayed`, `onion-relayed` | Requested outbound transport posture. |
| [`routing/failure-mode`](#field-routing-failure-mode) | `yes` | enum: `soft-fail`, `hard-fail` | Whether the sender allows downgrade if the requested transport posture cannot be satisfied. |
| [`relay/acceptable-classes`](#field-relay-acceptable-classes) | `no` | array | Optional relay classes acceptable for outbound privacy realization. |
| [`forwarding/max-hops`](#field-forwarding-max-hops) | `yes` | integer | Maximum number of relay hops allowed for the signal. |
| [`forwarding/budget`](#field-forwarding-budget) | `no` | integer | Maximum number of bounded forwards allowed under local policy. |

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

- Required: `no`
- Shape: const: `whisper-signal.v2`

<a id="field-signal-polarity"></a>
## `signal/polarity`

- Required: `yes`
- Shape: enum: `problem`, `idea`

Fundamental polarity of the whisper signal. `problem` describes a distributed harm, failure, or dignity risk that may require correlation and protective response. `idea` describes a convergent idea, creative discovery, or emerging approach that may justify co-creation. Emergency handling MUST NOT be triggered solely by an `idea` signal.

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

<a id="field-signal-text-native"></a>
## `signal/text-native`

- Required: `no`
- Shape: string

Optional sanitized text in the original non-English language. Use this only when the original accepted user-facing wording is not English; English text stays solely in `signal/text`.

<a id="field-signal-text-native-lang"></a>
## `signal/text-native-lang`

- Required: `no`
- Shape: string

BCP 47-like language tag for `signal/text-native`. This field is intentionally non-English; English originals MUST omit both native-text fields and use only `signal/text`.

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

Normalized issue class used for bounded correlation. Distinct from the enclosing envelope's `topic/key`, which is an Agora routing key; `topic/class` is the semantic correlation class carried inside the rumor body.

<a id="field-signal-similarity-key"></a>
## `signal/similarity-key`

- Required: `yes`
- Shape: string

Exact contextual correlation key. This required value is bound by the certificate profile/context; semantic similarity remains separate policy.

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
- Shape: enum: `federation-scoped`, `cross-federation`, `public-aggregate-only`

Maximum disclosure posture for the contextual signal. Public Agora ingress does not admit private-correlation; this value grants no dissemination authority.

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

<a id="field-signal-grade"></a>
## `signal/grade`

- Required: `yes`
- Shape: enum: `low`, `moderate`, `high`, `critical`

Signal salience grade. For `problem` signals this grades protective risk and urgency. For `idea` signals this grades convergence strength, co-creation potential, or urgency of matching interested participants. Routing and disclosure policy MAY interpret the same scale differently by `signal/polarity`.

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
