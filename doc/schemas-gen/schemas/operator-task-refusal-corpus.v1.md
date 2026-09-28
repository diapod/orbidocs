# Operator Task Refusal Corpus v1

Source schema: [`doc/schemas/operator-task-refusal-corpus.v1.schema.json`](../../schemas/operator-task-refusal-corpus.v1.schema.json)

A task pack's refusal corpus: cases that must be refused, each with the tabled refusal code it expects. A case with a candidate is executable: conformance compiles it against the profile under the most favourable admissible environment (contained, declared observations enforced), so the refusal it proves comes from the candidate itself, and a case refused with another code, or not refused, fails the pack facts evidence. A case without a candidate declares a refusal another layer proves (readiness, HIL, the run driver, the verifier) and counts towards coverage only. Coverage of the registered codes is recorded, never required.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-refusal-corpus.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`corpus/ref`](#field-corpus-ref) | `yes` | unspecified |  |
| [`cases`](#field-cases) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`case`](#def-case) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-refusal-corpus.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-corpus-ref"></a>
## `corpus/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-cases"></a>
## `cases`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-case"></a>
## `$defs.case`

- Shape: object
