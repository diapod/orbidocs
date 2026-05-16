# Contact Claim v1

Source schema: [`doc/schemas/contact-claim.v1.schema.json`](../../schemas/contact-claim.v1.schema.json)

Opt-in claim that a controller of a phone number, email address, or comparable human contact handle wants a Contact Catalog to expose a privacy-preserving route candidate for selected purposes. Raw contact handles are not stored in this artifact by default.

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
| [`claim/id`](#field-claim-id) | `yes` | string | Stable catalog record id. Sequence-aware stores replace only with newer `sequence/no` values for the same id. |
| [`contact/kind`](#field-contact-kind) | `yes` | enum: `phone`, `email`, `other` | Kind of external contact handle proved by the attestation. |
| [`contact/index`](#field-contact-index) | `yes` | ref: `#/$defs/contactIndex` |  |
| [`contact/attestation-ref`](#field-contact-attestation-ref) | `yes` | string | Reference to a fresh contact-control proof, normally a `capability-passport.v1` under `email-control` or `phone-control`. The Contact Catalog stores this reference, not the OTP transcript. |
| [`contact/attested-at`](#field-contact-attested-at) | `yes` | string |  |
| [`contact/attestation-expires-at`](#field-contact-attestation-expires-at) | `yes` | string | Time after which the contact-control proof is no longer fresh enough for admission or lookup. |
| [`owner/routing-subject-id`](#field-owner-routing-subject-id) | `no` | string | Preferred MVP route target. It is contactable without revealing the root participant. |
| [`owner/contact-nym-id`](#field-owner-contact-nym-id) | `no` | string | Optional relationship or context pseudonym exposed for contact discovery. |
| [`owner/invitation-route`](#field-owner-invitation-route) | `no` | ref: `#/$defs/invitationRoute` |  |
| [`owner/participant-id`](#field-owner-participant-id) | `no` | string | Disclosure-gated participant id. It MUST NOT be returned by default contact lookup profiles. |
| [`disclosure/mode`](#field-disclosure-mode) | `yes` | enum: `private-lookup`, `invite-only`, `public-handle`, `present-on-demand` | MVP Contact Catalog admission MUST support `invite-only`; other modes are profile extensions. |
| [`purposes`](#field-purposes) | `yes` | array |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`sequence/no`](#field-sequence-no) | `yes` | integer | Monotonic sequence for idempotent replacement in `CatalogStore<T>`. |
| [`revocation/ref`](#field-revocation-ref) | `no` | string \| null |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`proof/signature`](#field-proof-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`contactIndex`](#def-contactindex) | object |  |
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

Stable catalog record id. Sequence-aware stores replace only with newer `sequence/no` values for the same id.

<a id="field-contact-kind"></a>
## `contact/kind`

- Required: `yes`
- Shape: enum: `phone`, `email`, `other`

Kind of external contact handle proved by the attestation.

<a id="field-contact-index"></a>
## `contact/index`

- Required: `yes`
- Shape: ref: `#/$defs/contactIndex`

<a id="field-contact-attestation-ref"></a>
## `contact/attestation-ref`

- Required: `yes`
- Shape: string

Reference to a fresh contact-control proof, normally a `capability-passport.v1` under `email-control` or `phone-control`. The Contact Catalog stores this reference, not the OTP transcript.

<a id="field-contact-attested-at"></a>
## `contact/attested-at`

- Required: `yes`
- Shape: string

<a id="field-contact-attestation-expires-at"></a>
## `contact/attestation-expires-at`

- Required: `yes`
- Shape: string

Time after which the contact-control proof is no longer fresh enough for admission or lookup.

<a id="field-owner-routing-subject-id"></a>
## `owner/routing-subject-id`

- Required: `no`
- Shape: string

Preferred MVP route target. It is contactable without revealing the root participant.

<a id="field-owner-contact-nym-id"></a>
## `owner/contact-nym-id`

- Required: `no`
- Shape: string

Optional relationship or context pseudonym exposed for contact discovery.

<a id="field-owner-invitation-route"></a>
## `owner/invitation-route`

- Required: `no`
- Shape: ref: `#/$defs/invitationRoute`

<a id="field-owner-participant-id"></a>
## `owner/participant-id`

- Required: `no`
- Shape: string

Disclosure-gated participant id. It MUST NOT be returned by default contact lookup profiles.

<a id="field-disclosure-mode"></a>
## `disclosure/mode`

- Required: `yes`
- Shape: enum: `private-lookup`, `invite-only`, `public-handle`, `present-on-demand`

MVP Contact Catalog admission MUST support `invite-only`; other modes are profile extensions.

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

Monotonic sequence for idempotent replacement in `CatalogStore<T>`.

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

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-contactindex"></a>
## `$defs.contactIndex`

- Shape: object

<a id="def-invitationroute"></a>
## `$defs.invitationRoute`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
