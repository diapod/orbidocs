# Corpus Provenance-bearing Signed Outcome v2

Source schema: [`doc/schemas/corpus-reasoning-answer.v2.schema.json`](../../schemas/corpus-reasoning-answer.v2.schema.json)

An unchanged V1 answer and content-bound execution evidence, jointly authenticated with corpus-reasoning-answer-signature.v2 over RFC 8785 JSON after removing only the outer signature. Receiving hosts independently admit the responder, evidence and publication policy. Source sessions are not exported.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-reasoning-answer.v2` |  |
| [`answer`](#field-answer) | `yes` | ref: `corpus-reasoning-answer.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
| [`publication/assessment`](#field-publication-assessment) | `no` | object | Non-compelling publisher decision. A policy digest avoids disclosing private provider allow/deny sets; the publisher retains the exact policy for audit. |
| [`signature`](#field-signature) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-reasoning-answer.v2`

<a id="field-answer"></a>
## `answer`

- Required: `yes`
- Shape: ref: `corpus-reasoning-answer.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`

<a id="field-publication-assessment"></a>
## `publication/assessment`

- Required: `no`
- Shape: object

Non-compelling publisher decision. A policy digest avoids disclosing private provider allow/deny sets; the publisher retains the exact policy for audit.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: unspecified
