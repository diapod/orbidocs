# Local Contact v1

Source schema: [`doc/schemas/local-contact.v1.schema.json`](../../schemas/local-contact.v1.schema.json)

Daemon-local address-book and contact continuity record. It is never published as a Contact Catalog claim and may contain raw handles, labels, UX metadata, and pairwise routing continuity state. Ownership note: Local Contact Store owns private contact records; Local Relationship Layer owns classes, memberships, relationship policy predicates, and pairwise relationship facts.

## Governing Basis

- [`doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`](../../project/60-solutions/025-contact-catalog/025-contact-catalog.md)
- [`doc/project/40-proposals/058-contact-catalog.md`](../../project/40-proposals/058-contact-catalog.md)
- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `local-contact.v1` |  |
| [`contact/id`](#field-contact-id) | `yes` | string |  |
| [`handle/kind`](#field-handle-kind) | `yes` | enum: `email`, `phone`, `other` |  |
| [`handle/raw`](#field-handle-raw) | `yes` | string | Raw user-entered handle. This stays daemon-local. |
| [`handle/normalized`](#field-handle-normalized) | `yes` | string |  |
| [`handle/digest`](#field-handle-digest) | `yes` | string |  |
| [`label`](#field-label) | `no` | string | Compatibility single display label. |
| [`labels`](#field-labels) | `no` | array | User-managed labels for grouping and search. |
| [`metadata`](#field-metadata) | `no` | object | Daemon-local UX/provenance metadata. It is not network evidence. |
| [`state`](#field-state) | `yes` | enum: `pending`, `active`, `rejected`, `blocked`, `archived` |  |
| [`pairwise/contact-nym-id`](#field-pairwise-contact-nym-id) | `no` | string | Compatibility pointer to the current active pairwise mapping. |
| [`routing-subject/id`](#field-routing-subject-id) | `no` | string |  |
| [`remote/subject`](#field-remote-subject) | `no` | ref: `#/$defs/subject` |  |
| [`source/ref`](#field-source-ref) | `no` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`updated/at`](#field-updated-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `local-contact.v1`

<a id="field-contact-id"></a>
## `contact/id`

- Required: `yes`
- Shape: string

<a id="field-handle-kind"></a>
## `handle/kind`

- Required: `yes`
- Shape: enum: `email`, `phone`, `other`

<a id="field-handle-raw"></a>
## `handle/raw`

- Required: `yes`
- Shape: string

Raw user-entered handle. This stays daemon-local.

<a id="field-handle-normalized"></a>
## `handle/normalized`

- Required: `yes`
- Shape: string

<a id="field-handle-digest"></a>
## `handle/digest`

- Required: `yes`
- Shape: string

<a id="field-label"></a>
## `label`

- Required: `no`
- Shape: string

Compatibility single display label.

<a id="field-labels"></a>
## `labels`

- Required: `no`
- Shape: array

User-managed labels for grouping and search.

<a id="field-metadata"></a>
## `metadata`

- Required: `no`
- Shape: object

Daemon-local UX/provenance metadata. It is not network evidence.

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `pending`, `active`, `rejected`, `blocked`, `archived`

<a id="field-pairwise-contact-nym-id"></a>
## `pairwise/contact-nym-id`

- Required: `no`
- Shape: string

Compatibility pointer to the current active pairwise mapping.

<a id="field-routing-subject-id"></a>
## `routing-subject/id`

- Required: `no`
- Shape: string

<a id="field-remote-subject"></a>
## `remote/subject`

- Required: `no`
- Shape: ref: `#/$defs/subject`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `no`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-updated-at"></a>
## `updated/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object
