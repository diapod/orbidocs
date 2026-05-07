# Whisper Redaction Prepare Request v1

Source schema: [`doc/schemas/whisper-redaction-prepare-request.v1.schema.json`](../../schemas/whisper-redaction-prepare-request.v1.schema.json)

Host-capability request for preparing a local redaction draft from raw Whisper intake material. This is a private workflow contract, not an Agora content schema; the provider returns a draft and never publishes to Agora or approves publication.

## Governing Basis

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-redaction-prepare-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`intake/id`](#field-intake-id) | `yes` | string | Local whisper-intake identifier. Used for correlation and idempotent retry, not for public publication. |
| [`raw/private-material`](#field-raw-private-material) | `yes` | object \| array \| string \| number \| boolean \| null | Raw local/private material supplied to the configured redaction provider. The request must remain on loopback/host-capability transport and must not be published to Agora. |
| [`redaction/profile`](#field-redaction-profile) | `yes` | string | Provider-local redaction profile or policy preset. `default` is the safe baseline. |
| [`operator/instructions`](#field-operator-instructions) | `no` | string \| null | Optional local-only operator instructions for the provider. |
| [`policy/constraints`](#field-policy-constraints) | `yes` | object | Machine-readable policy constraints such as maximum length, forbidden categories, local-only model policy, or disclosure target. |
| [`retention/policy-ref`](#field-retention-policy-ref) | `no` | string |  |
| [`disclosure/target`](#field-disclosure-target) | `yes` | enum: `public-whisper-candidate`, `private-summary`, `operator-review-only` | Intended use of the draft. M4 uses `public-whisper-candidate`; operator approval is still required before publication. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-redaction-prepare-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-intake-id"></a>
## `intake/id`

- Required: `yes`
- Shape: string

Local whisper-intake identifier. Used for correlation and idempotent retry, not for public publication.

<a id="field-raw-private-material"></a>
## `raw/private-material`

- Required: `yes`
- Shape: object | array | string | number | boolean | null

Raw local/private material supplied to the configured redaction provider. The request must remain on loopback/host-capability transport and must not be published to Agora.

<a id="field-redaction-profile"></a>
## `redaction/profile`

- Required: `yes`
- Shape: string

Provider-local redaction profile or policy preset. `default` is the safe baseline.

<a id="field-operator-instructions"></a>
## `operator/instructions`

- Required: `no`
- Shape: string | null

Optional local-only operator instructions for the provider.

<a id="field-policy-constraints"></a>
## `policy/constraints`

- Required: `yes`
- Shape: object

Machine-readable policy constraints such as maximum length, forbidden categories, local-only model policy, or disclosure target.

<a id="field-retention-policy-ref"></a>
## `retention/policy-ref`

- Required: `no`
- Shape: string

<a id="field-disclosure-target"></a>
## `disclosure/target`

- Required: `yes`
- Shape: enum: `public-whisper-candidate`, `private-summary`, `operator-review-only`

Intended use of the draft. M4 uses `public-whisper-candidate`; operator approval is still required before publication.
