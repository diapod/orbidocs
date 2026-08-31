# Corpus Reasoning Experiment Review v3

Source schema: [`doc/schemas/corpus-reasoning-experiment-review.v3.schema.json`](../../schemas/corpus-reasoning-experiment-review.v3.schema.json)

Story 012 technical experiment-review revision and first thematic structured-review profile above the general Corpus prose exchange. It embeds a profile-bound structural claim artifact for this review boundary; it does not make that artifact a universal Corpus deliberation contract, require claim envelopes for ordinary plain-text or Markdown deliberation, or install PowerDNS semantics in the generic claim envelope. Schema validity does not establish readiness of the referenced review profile, which must be versioned and separately admitted by the receiving host; federation endorsement cannot compel admission.

## Governing Basis

- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)
- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`](../../project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md)
- [`doc/project/60-solutions/038-corpus/038-corpus.md`](../../project/60-solutions/038-corpus/038-corpus.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)

## Fixtures

### Valid Fixtures

- [`doc/schemas/examples/accepted.corpus-reasoning-experiment-review.v3.json`](../../schemas/examples/accepted.corpus-reasoning-experiment-review.v3.json)

### Invalid Fixtures

- [`doc/schemas/examples/invalid/missing-claim-envelope.corpus-reasoning-experiment-review.v3.json`](../../schemas/examples/invalid/missing-claim-envelope.corpus-reasoning-experiment-review.v3.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `3` |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`proposal/digest`](#field-proposal-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`candidate-plan/ref`](#field-candidate-plan-ref) | `yes` | string |  |
| [`candidate-plan/artifact-ref`](#field-candidate-plan-artifact-ref) | `yes` | ref: `#/$defs/artifact-ref` |  |
| [`candidate-plan/digest`](#field-candidate-plan-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`reviewer`](#field-reviewer) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`reviewer/node-id`](#field-reviewer-node-id) | `yes` | string |  |
| [`reviewer-turn/id`](#field-reviewer-turn-id) | `yes` | string |  |
| [`terminal-state/digest`](#field-terminal-state-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`correction-state/digest`](#field-correction-state-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`verdict`](#field-verdict) | `yes` | enum: `accept`, `revise`, `reject`, `request-regeneration` |  |
| [`claim-envelope`](#field-claim-envelope) | `yes` | ref: `corpus-deliberation-review-claims.v1.schema.json` | Structural review artifact interpreted only through a separately admitted, versioned Story 012 domain profile. Its use here does not require other Corpus deliberation profiles to use claim envelopes. |
| [`replacement`](#field-replacement) | `no` | ref: `#/$defs/candidate-plan-binding` |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`reviewed-at`](#field-reviewed-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`artifact-ref`](#def-artifact-ref) | string |  |
| [`candidate-plan-binding`](#def-candidate-plan-binding) | object |  |
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "verdict": {
      "const": "revise"
    }
  },
  "required": [
    "verdict"
  ]
}
```

Then:

```json
{
  "required": [
    "replacement"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `3`

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-proposal-digest"></a>
## `proposal/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-candidate-plan-ref"></a>
## `candidate-plan/ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-plan-artifact-ref"></a>
## `candidate-plan/artifact-ref`

- Required: `yes`
- Shape: ref: `#/$defs/artifact-ref`

<a id="field-candidate-plan-digest"></a>
## `candidate-plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-reviewer"></a>
## `reviewer`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-reviewer-node-id"></a>
## `reviewer/node-id`

- Required: `yes`
- Shape: string

<a id="field-reviewer-turn-id"></a>
## `reviewer-turn/id`

- Required: `yes`
- Shape: string

<a id="field-terminal-state-digest"></a>
## `terminal-state/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-correction-state-digest"></a>
## `correction-state/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-verdict"></a>
## `verdict`

- Required: `yes`
- Shape: enum: `accept`, `revise`, `reject`, `request-regeneration`

<a id="field-claim-envelope"></a>
## `claim-envelope`

- Required: `yes`
- Shape: ref: `corpus-deliberation-review-claims.v1.schema.json`

Structural review artifact interpreted only through a separately admitted, versioned Story 012 domain profile. Its use here does not require other Corpus deliberation profiles to use claim envelopes.

<a id="field-replacement"></a>
## `replacement`

- Required: `no`
- Shape: ref: `#/$defs/candidate-plan-binding`

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-reviewed-at"></a>
## `reviewed-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-artifact-ref"></a>
## `$defs.artifact-ref`

- Shape: string

<a id="def-candidate-plan-binding"></a>
## `$defs.candidate-plan-binding`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
