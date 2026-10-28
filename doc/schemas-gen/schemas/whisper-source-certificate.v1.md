# Whisper Source Certificate Profile of Nym Certificate v1

Source schema: [`doc/schemas/whisper-source-certificate.v1.schema.json`](../../schemas/whisper-source-certificate.v1.schema.json)

Strict NFC-only contextual profile of the existing nym-certificate.v1 signing format; no extra signature framing.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`nym/id`](#field-nym-id) | `yes` | string | Certified nym identity. |
| [`epoch`](#field-epoch) | `yes` | integer | Epoch number of this pseudonym line. |
| [`issued-at`](#field-issued-at) | `yes` | string | Issue timestamp of the certificate. |
| [`expires-at`](#field-expires-at) | `yes` | string | End of ordinary validity for application-message signing. |
| [`leniency-until`](#field-leniency-until) | `no` | string | End of grace semantics for continuity work. After this moment the old line is dead. |
| [`issuer/id`](#field-issuer-id) | `yes` | string | Issuing council identity in canonical `council:did:key:z...` form. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`whisper/source`](#field-whisper-source) | `yes` | ref: `whisper-source-descriptor.v1.schema.json` |  |
| [`privacy/linkability`](#field-privacy-linkability) | `yes` | const: `context-scoped` |  |
| [`privacy/context-domain`](#field-privacy-context-domain) | `yes` | string |  |
| [`scope/audiences`](#field-scope-audiences) | `yes` | array |  |
| [`scope/context-domains`](#field-scope-context-domains) | `yes` | array |  |
| [`scope/federation-id`](#field-scope-federation-id) | `yes` | string |  |
| [`scope/topic-patterns`](#field-scope-topic-patterns) | `yes` | array |  |
| [`scope/record-kinds`](#field-scope-record-kinds) | `yes` | const: `['whisper-signal']` |  |
| [`scope/content-schemas`](#field-scope-content-schemas) | `yes` | const: `['whisper-signal.v2']` |  |
| [`scope/disclosure-scopes`](#field-scope-disclosure-scopes) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

Certified nym identity.

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

Epoch number of this pseudonym line.

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

Issue timestamp of the certificate.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

End of ordinary validity for application-message signing.

<a id="field-leniency-until"></a>
## `leniency-until`

- Required: `no`
- Shape: string

End of grace semantics for continuity work. After this moment the old line is dead.

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

Issuing council identity in canonical `council:did:key:z...` form.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-whisper-source"></a>
## `whisper/source`

- Required: `yes`
- Shape: ref: `whisper-source-descriptor.v1.schema.json`

<a id="field-privacy-linkability"></a>
## `privacy/linkability`

- Required: `yes`
- Shape: const: `context-scoped`

<a id="field-privacy-context-domain"></a>
## `privacy/context-domain`

- Required: `yes`
- Shape: string

<a id="field-scope-audiences"></a>
## `scope/audiences`

- Required: `yes`
- Shape: array

<a id="field-scope-context-domains"></a>
## `scope/context-domains`

- Required: `yes`
- Shape: array

<a id="field-scope-federation-id"></a>
## `scope/federation-id`

- Required: `yes`
- Shape: string

<a id="field-scope-topic-patterns"></a>
## `scope/topic-patterns`

- Required: `yes`
- Shape: array

<a id="field-scope-record-kinds"></a>
## `scope/record-kinds`

- Required: `yes`
- Shape: const: `['whisper-signal']`

<a id="field-scope-content-schemas"></a>
## `scope/content-schemas`

- Required: `yes`
- Shape: const: `['whisper-signal.v2']`

<a id="field-scope-disclosure-scopes"></a>
## `scope/disclosure-scopes`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
