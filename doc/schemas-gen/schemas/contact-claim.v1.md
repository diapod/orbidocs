# Contact Claim v1

Source schema: [`doc/schemas/contact-claim.v1.schema.json`](../../schemas/contact-claim.v1.schema.json)

Opt-in Contact Catalog claim using an ordered lookup-safe owner route set. Raw handles are not stored in this artifact.

## Governing Basis

- [`doc/project/40-proposals/058-contact-catalog.md`](../../project/40-proposals/058-contact-catalog.md)
- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)
- [`doc/schemas/routing-subject-binding.v1.schema.json`](../../schemas/routing-subject-binding.v1.schema.json)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contact-claim.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`claim/id`](#field-claim-id) | `yes` | string |  |
| [`contact/kind`](#field-contact-kind) | `yes` | enum: `phone`, `email`, `other` |  |
| [`contact/index`](#field-contact-index) | `yes` | ref: `#/$defs/contactIndex` |  |
| [`contact/attestation-ref`](#field-contact-attestation-ref) | `yes` | string |  |
| [`contact/attested-at`](#field-contact-attested-at) | `yes` | string |  |
| [`contact/attestation-expires-at`](#field-contact-attestation-expires-at) | `yes` | string |  |
| [`owner/routes`](#field-owner-routes) | `yes` | array |  |
| [`owner/participant-id`](#field-owner-participant-id) | `no` | string | Disclosure-gated root participant id. It MUST NOT be returned by default Contact Catalog lookup profiles. |
| [`disclosure/mode`](#field-disclosure-mode) | `yes` | enum: `private-lookup`, `invite-only`, `public-handle`, `present-on-demand` |  |
| [`purposes`](#field-purposes) | `yes` | array |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`sequence/no`](#field-sequence-no) | `yes` | integer |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | string \| null |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`proof/signature`](#field-proof-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`contactIndex`](#def-contactindex) | object |  |
| [`ownerRoute`](#def-ownerroute) | object |  |
| [`invitationRoute`](#def-invitationroute) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contact-claim.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-claim-id"></a>
## `claim/id`

- Required: `yes`
- Shape: string

<a id="field-contact-kind"></a>
## `contact/kind`

- Required: `yes`
- Shape: enum: `phone`, `email`, `other`

<a id="field-contact-index"></a>
## `contact/index`

- Required: `yes`
- Shape: ref: `#/$defs/contactIndex`

<a id="field-contact-attestation-ref"></a>
## `contact/attestation-ref`

- Required: `yes`
- Shape: string

<a id="field-contact-attested-at"></a>
## `contact/attested-at`

- Required: `yes`
- Shape: string

<a id="field-contact-attestation-expires-at"></a>
## `contact/attestation-expires-at`

- Required: `yes`
- Shape: string

<a id="field-owner-routes"></a>
## `owner/routes`

- Required: `yes`
- Shape: array

<a id="field-owner-participant-id"></a>
## `owner/participant-id`

- Required: `no`
- Shape: string

Disclosure-gated root participant id. It MUST NOT be returned by default Contact Catalog lookup profiles.

<a id="field-disclosure-mode"></a>
## `disclosure/mode`

- Required: `yes`
- Shape: enum: `private-lookup`, `invite-only`, `public-handle`, `present-on-demand`

<a id="field-purposes"></a>
## `purposes`

- Required: `yes`
- Shape: array

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-sequence-no"></a>
## `sequence/no`

- Required: `yes`
- Shape: integer

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: string | null

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-proof-signature"></a>
## `proof/signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-contactindex"></a>
## `$defs.contactIndex`

- Shape: object

<a id="def-ownerroute"></a>
## `$defs.ownerRoute`

- Shape: object

<a id="def-invitationroute"></a>
## `$defs.invitationRoute`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
