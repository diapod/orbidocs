# Whisper-origin.v1

Source schema: [`doc/schemas/whisper-origin.v1.schema.json`](../../schemas/whisper-origin.v1.schema.json)

Minimized declared material origin. Authorship posture and distinct-source counting remain independent. Private evidence references and retention horizons are excluded.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`origin/source-kinds`](#field-origin-source-kinds) | `yes` | array |  |
| [`origin/collection-method`](#field-origin-collection-method) | `yes` | enum: `manual-selection`, `configured-monitoring`, `media-monitoring`, `mixed`, `unknown` |  |
| [`origin/processing`](#field-origin-processing) | `yes` | array |  |
| [`origin/coverage`](#field-origin-coverage) | `yes` | enum: `complete`, `partial` | Declared coverage of the material lineage presented for this review, not a claim of independent corroboration or global source completeness. |
## Field Semantics

<a id="field-origin-source-kinds"></a>
## `origin/source-kinds`

- Required: `yes`
- Shape: array

<a id="field-origin-collection-method"></a>
## `origin/collection-method`

- Required: `yes`
- Shape: enum: `manual-selection`, `configured-monitoring`, `media-monitoring`, `mixed`, `unknown`

<a id="field-origin-processing"></a>
## `origin/processing`

- Required: `yes`
- Shape: array

<a id="field-origin-coverage"></a>
## `origin/coverage`

- Required: `yes`
- Shape: enum: `complete`, `partial`

Declared coverage of the material lineage presented for this review, not a claim of independent corroboration or global source completeness.
