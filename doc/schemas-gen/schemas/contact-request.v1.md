# Contact Request v1

Source schema: [`doc/schemas/contact-request.v1.schema.json`](../../schemas/contact-request.v1.schema.json)

Private artifact sent to a route candidate returned by Contact Catalog to request a narrow messaging/contact relationship. It carries a sender subject and optional sender-handle proof; it is not the private message body.

## Governing Basis

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)
- [`doc/project/40-proposals/058-contact-catalog.md`](../../project/40-proposals/058-contact-catalog.md)
- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contact-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`request/kind`](#field-request-kind) | `yes` | enum: `messaging-contact` |  |
| [`sender/display-name`](#field-sender-display-name) | `no` | string |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`sender/handle-proof-ref`](#field-sender-handle-proof-ref) | `no` | string | Optional `email-control` or `phone-control` passport reference proving that the sender controls the displayed contact handle. |
| [`sender/reply-route`](#field-sender-reply-route) | `no` | ref: `#/$defs/subject` |  |
| [`recipient/route`](#field-recipient-route) | `yes` | ref: `#/$defs/subject` |  |
| [`recipient/public-handle-ref`](#field-recipient-public-handle-ref) | `no` | string | Opaque reference to the external handle used for lookup. Raw email or phone MAY be stored locally, but network artifacts SHOULD prefer a redacted or digest-bound reference. |
| [`requested/capability-id`](#field-requested-capability-id) | `yes` | enum: `messaging-receive` | Capability passport profile requested from the recipient if the user accepts. |
| [`requested/purposes`](#field-requested-purposes) | `yes` | array |  |
| [`greeting`](#field-greeting) | `no` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`proof/signature`](#field-proof-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contact-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-request-kind"></a>
## `request/kind`

- Required: `yes`
- Shape: enum: `messaging-contact`

<a id="field-sender-display-name"></a>
## `sender/display-name`

- Required: `no`
- Shape: string

<a id="field-sender-subject"></a>
## `sender/subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-sender-handle-proof-ref"></a>
## `sender/handle-proof-ref`

- Required: `no`
- Shape: string

Optional `email-control` or `phone-control` passport reference proving that the sender controls the displayed contact handle.

<a id="field-sender-reply-route"></a>
## `sender/reply-route`

- Required: `no`
- Shape: ref: `#/$defs/subject`

<a id="field-recipient-route"></a>
## `recipient/route`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-recipient-public-handle-ref"></a>
## `recipient/public-handle-ref`

- Required: `no`
- Shape: string

Opaque reference to the external handle used for lookup. Raw email or phone MAY be stored locally, but network artifacts SHOULD prefer a redacted or digest-bound reference.

<a id="field-requested-capability-id"></a>
## `requested/capability-id`

- Required: `yes`
- Shape: enum: `messaging-receive`

Capability passport profile requested from the recipient if the user accepts.

<a id="field-requested-purposes"></a>
## `requested/purposes`

- Required: `yes`
- Shape: array

<a id="field-greeting"></a>
## `greeting`

- Required: `no`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

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

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
