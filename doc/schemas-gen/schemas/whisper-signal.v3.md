# Whisper-signal.v3

Source schema: [`doc/schemas/whisper-signal.v3.schema.json`](../../schemas/whisper-signal.v3.schema.json)

Contextual authored signal with reviewed material origin; origin grants no source independence or credibility.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/084-sensorium-web-observation-connector.md`](../../project/40-proposals/084-sensorium-web-observation-connector.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-signal.v3` |  |
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
| [`source/class`](#field-source-class) | `yes` | enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, `monus-sensorium-derived` | Authorship and preparation posture of the signal; material origin is declared independently by origin/source-kinds. Existing Monus and Sensorium evidence requirements remain in force. This axis alone cannot supply or replace a material-origin declaration. |
| [`source/signal-kinds`](#field-source-signal-kinds) | `no` | array | Optional high-level local signal classes that materially informed a derived or sensorium-assisted rumor draft. |
| [`signal/grade`](#field-signal-grade) | `yes` | enum: `low`, `moderate`, `high`, `critical` | Signal salience grade. For `problem` signals this grades protective risk and urgency. For `idea` signals this grades convergence strength, co-creation potential, or urgency of matching interested participants. Routing and disclosure policy MAY interpret the same scale differently by `signal/polarity`. |
| [`routing/profile`](#field-routing-profile) | `yes` | enum: `direct`, `relayed`, `onion-relayed` | Requested outbound transport posture. |
| [`routing/failure-mode`](#field-routing-failure-mode) | `yes` | enum: `soft-fail`, `hard-fail` | Whether the sender allows downgrade if the requested transport posture cannot be satisfied. |
| [`relay/acceptable-classes`](#field-relay-acceptable-classes) | `no` | array | Optional relay classes acceptable for outbound privacy realization. |
| [`forwarding/max-hops`](#field-forwarding-max-hops) | `yes` | integer | Maximum number of relay hops allowed for the signal. |
| [`forwarding/budget`](#field-forwarding-budget) | `no` | integer | Maximum number of bounded forwards allowed under local policy. |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`embargo/manifest-digest`](#field-embargo-manifest-digest) | `no` | string |  |
| [`case/continuity-key-digest`](#field-case-continuity-key-digest) | `no` | string |  |
| [`case/status-authority`](#field-case-status-authority) | `no` | string |  |
| [`case/not-after`](#field-case-not-after) | `no` | string |  |
| [`origin/source-kinds`](#field-origin-source-kinds) | `yes` | ref: `whisper-origin.v1.schema.json#/properties/origin~1source-kinds` |  |
| [`origin/collection-method`](#field-origin-collection-method) | `yes` | ref: `whisper-origin.v1.schema.json#/properties/origin~1collection-method` |  |
| [`origin/processing`](#field-origin-processing) | `yes` | ref: `whisper-origin.v1.schema.json#/properties/origin~1processing` |  |
| [`origin/coverage`](#field-origin-coverage) | `yes` | ref: `whisper-origin.v1.schema.json#/properties/origin~1coverage` |  |

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
- Shape: const: `whisper-signal.v3`

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

- Required: `yes`
- Shape: enum: `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, `monus-sensorium-derived`

Authorship and preparation posture of the signal; material origin is declared independently by origin/source-kinds. Existing Monus and Sensorium evidence requirements remain in force. This axis alone cannot supply or replace a material-origin declaration.

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

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-epoch-end"></a>
## `epoch/end`

- Required: `yes`
- Shape: string

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-embargo-manifest-digest"></a>
## `embargo/manifest-digest`

- Required: `no`
- Shape: string

<a id="field-case-continuity-key-digest"></a>
## `case/continuity-key-digest`

- Required: `no`
- Shape: string

<a id="field-case-status-authority"></a>
## `case/status-authority`

- Required: `no`
- Shape: string

<a id="field-case-not-after"></a>
## `case/not-after`

- Required: `no`
- Shape: string

<a id="field-origin-source-kinds"></a>
## `origin/source-kinds`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json#/properties/origin~1source-kinds`

<a id="field-origin-collection-method"></a>
## `origin/collection-method`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json#/properties/origin~1collection-method`

<a id="field-origin-processing"></a>
## `origin/processing`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json#/properties/origin~1processing`

<a id="field-origin-coverage"></a>
## `origin/coverage`

- Required: `yes`
- Shape: ref: `whisper-origin.v1.schema.json#/properties/origin~1coverage`
