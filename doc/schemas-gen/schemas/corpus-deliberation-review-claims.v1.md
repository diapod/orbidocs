# Corpus Deliberation Review Claims v1

Source schema: [`doc/schemas/corpus-deliberation-review-claims.v1.schema.json`](../../schemas/corpus-deliberation-review-claims.v1.schema.json)

Optional profile-bound structural artifact for thematic review profiles only. The general/default Corpus profile remains prose exchange on an arbitrary topic through plain-text or Markdown, including inert code fragments, and does not require a claim envelope. This artifact is used only by a review boundary that explicitly adopts it; it is not a domain ontology, a global profile registry, or a mandatory claim format for every technical, scientific, social, or creative workflow. Operators and communities may propose versioned profiles, while each receiving host admits them under local policy; federation endorsement may provide evidence but cannot compel local admission. The admitted profile owns vocabulary, admissibility, evidence or evaluation semantics, success criteria, disposition mapping, and legal next moves; their opaque namespaced refs remain open and are not centrally enumerated by this schema. Schema-valid references alone do not prove profile support or readiness: automatic machine consumption requires a separately admitted versioned profile.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`](../../project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md)

## Project Lineage

## Fixtures

### Valid Fixtures

- [`doc/schemas/examples/accepted.corpus-deliberation-review-claims.v1.json`](../../schemas/examples/accepted.corpus-deliberation-review-claims.v1.json)

### Invalid Fixtures

- [`doc/schemas/examples/invalid/unknown-field.corpus-deliberation-review-claims.v1.json`](../../schemas/examples/invalid/unknown-field.corpus-deliberation-review-claims.v1.json)
- [`doc/schemas/examples/invalid/unnamespaced-profile.corpus-deliberation-review-claims.v1.json`](../../schemas/examples/invalid/unnamespaced-profile.corpus-deliberation-review-claims.v1.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-deliberation-review-claims.v1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `#/$defs/ref` | Opaque namespaced reference to semantics proposed and owned outside this envelope. Automatic machine consumption requires the receiving host to have separately admitted that exact versioned operator- or community-defined profile, which then owns the meaning and validation of every other opaque reference in this artifact. Federation endorsement may inform local policy but cannot compel admission. |
| [`disposition/ref`](#field-disposition-ref) | `yes` | ref: `#/$defs/ref` | Opaque namespaced profile-owned review disposition. The generic envelope neither enumerates it nor maps it to a verdict or outcome. |
| [`claims`](#field-claims) | `yes` | array | Profile-interpreted structural claims. An empty set is valid at the generic layer when the selected profile permits it. |
| [`next-move`](#field-next-move) | `yes` | unspecified | Optional profile-owned structural suggestion using opaque namespaced refs. It carries no execution, publication, or adjudication authority. |
| [`commentary`](#field-commentary) | `yes` | array | Bounded inert provenance commentary. A profile MUST NOT derive its disposition, verdict, next move, or effect authority from this text. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`claim`](#def-claim) | object | Closed structural claim tuple whose reference vocabulary and admissibility remain owned by the selected profile. |
| [`next-move`](#def-next-move) | object | Closed, inert prospective move interpreted and authorized only by the selected profile and its downstream owner. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-deliberation-review-claims.v1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

Opaque namespaced reference to semantics proposed and owned outside this envelope. Automatic machine consumption requires the receiving host to have separately admitted that exact versioned operator- or community-defined profile, which then owns the meaning and validation of every other opaque reference in this artifact. Federation endorsement may inform local policy but cannot compel admission.

<a id="field-disposition-ref"></a>
## `disposition/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

Opaque namespaced profile-owned review disposition. The generic envelope neither enumerates it nor maps it to a verdict or outcome.

<a id="field-claims"></a>
## `claims`

- Required: `yes`
- Shape: array

Profile-interpreted structural claims. An empty set is valid at the generic layer when the selected profile permits it.

<a id="field-next-move"></a>
## `next-move`

- Required: `yes`
- Shape: unspecified

Optional profile-owned structural suggestion using opaque namespaced refs. It carries no execution, publication, or adjudication authority.

<a id="field-commentary"></a>
## `commentary`

- Required: `yes`
- Shape: array

Bounded inert provenance commentary. A profile MUST NOT derive its disposition, verdict, next move, or effect authority from this text.

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-claim"></a>
## `$defs.claim`

- Shape: object

Closed structural claim tuple whose reference vocabulary and admissibility remain owned by the selected profile.

<a id="def-next-move"></a>
## `$defs.next-move`

- Shape: object

Closed, inert prospective move interpreted and authorized only by the selected profile and its downstream owner.
