# Nym-case-recovery-result.local.v1

Source schema: [`doc/schemas/nym-case-recovery-result.local.v1.schema.json`](../../schemas/nym-case-recovery-result.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md`](../../project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-case-recovery-result.local.v1` |  |
| [`policy`](#field-policy) | `yes` | enum: `account`, `require` |  |
| [`state`](#field-state) | `yes` | enum: `applied`, `refused`, `unavailable` |  |
| [`entries`](#field-entries) | `yes` | array |  |
| [`reason`](#field-reason) | `yes` | enum: `None`, `case-key-required`, `case-key-input-invalid`, `case-key-state-corrupt`, `case-key-owner-busy`, `case-key-unavailable`, `case-key-expired`, `case-key-erased`, `case-key-conflict`, `case-key-capacity`, `case-key-recovery-not-enabled`, `case-key-entropy-unavailable`, `case-key-storage-unavailable`, `case-key-clock-regressed`, `case-key-fence-unavailable`, `case-key-journal-unavailable`, `use-not-enabled`, `case-key-succession-refused` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-case-recovery-result.local.v1`

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: enum: `account`, `require`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `applied`, `refused`, `unavailable`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: enum: `None`, `case-key-required`, `case-key-input-invalid`, `case-key-state-corrupt`, `case-key-owner-busy`, `case-key-unavailable`, `case-key-expired`, `case-key-erased`, `case-key-conflict`, `case-key-capacity`, `case-key-recovery-not-enabled`, `case-key-entropy-unavailable`, `case-key-storage-unavailable`, `case-key-clock-regressed`, `case-key-fence-unavailable`, `case-key-journal-unavailable`, `use-not-enabled`, `case-key-succession-refused`
