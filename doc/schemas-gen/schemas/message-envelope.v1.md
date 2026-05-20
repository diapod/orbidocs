# Message Envelope v1

Source schema: [`doc/schemas/message-envelope.v1.schema.json`](../../schemas/message-envelope.v1.schema.json)

Private personal-message artifact carried by Artifact Delivery and admitted by the messaging middleware.

## Governing Basis

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)
- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `message-envelope.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`envelope/id`](#field-envelope-id) | `yes` | string |  |
| [`message/id`](#field-message-id) | `no` | string |  |
| [`thread/id`](#field-thread-id) | `no` | string |  |
| [`parent/message-id`](#field-parent-message-id) | `no` | string | Optional parent message id used by replies and forwards. It is independent from recording metadata so a receiver can reject a reply that drops a required recording flag. |
| [`recording`](#field-recording) | `no` | object |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`receiver/route`](#field-receiver-route) | `yes` | ref: `#/$defs/subject` |  |
| [`receiver/public-handle`](#field-receiver-public-handle) | `no` | ref: `#/$defs/public_handle` |  |
| [`authorization`](#field-authorization) | `yes` | object |  |
| [`body`](#field-body) | `yes` | object |  |
| [`meta`](#field-meta) | `yes` | object |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
| [`public_handle`](#def-public-handle) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `message-envelope.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-envelope-id"></a>
## `envelope/id`

- Required: `yes`
- Shape: string

<a id="field-message-id"></a>
## `message/id`

- Required: `no`
- Shape: string

<a id="field-thread-id"></a>
## `thread/id`

- Required: `no`
- Shape: string

<a id="field-parent-message-id"></a>
## `parent/message-id`

- Required: `no`
- Shape: string

Optional parent message id used by replies and forwards. It is independent from recording metadata so a receiver can reject a reply that drops a required recording flag.

<a id="field-recording"></a>
## `recording`

- Required: `no`
- Shape: object

<a id="field-sender-subject"></a>
## `sender/subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-receiver-route"></a>
## `receiver/route`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-receiver-public-handle"></a>
## `receiver/public-handle`

- Required: `no`
- Shape: ref: `#/$defs/public_handle`

<a id="field-authorization"></a>
## `authorization`

- Required: `yes`
- Shape: object

<a id="field-body"></a>
## `body`

- Required: `yes`
- Shape: object

<a id="field-meta"></a>
## `meta`

- Required: `yes`
- Shape: object

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object

<a id="def-public-handle"></a>
## `$defs.public_handle`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
