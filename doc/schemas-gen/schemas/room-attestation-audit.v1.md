# Room Attestation Audit v1

Source schema: [`doc/schemas/room-attestation-audit.v1.schema.json`](../../schemas/room-attestation-audit.v1.schema.json)

Operator-visible metadata-only audit event emitted when a room membership attestation request is issued, refused, deduplicated, or rate-limited.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`audit/id`](#field-audit-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`request/mode`](#field-request-mode) | `yes` | enum: `invitee-first-join`, `member-self`, `authority-roster` |  |
| [`requester/subject`](#field-requester-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | string | Digest or stable redacted reference for the requested subject; the audit event must not disclose closed-room roster contents to unauthorized viewers. |
| [`decision`](#field-decision) | `yes` | enum: `issued`, `refused`, `deduplicated`, `rate-limited` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`exposure`](#field-exposure) | `no` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` | Effective room exposure used for attestation policy evaluation. If the room policy is unavailable, producers may emit the conservative private-to-swarm fallback. |
| [`ttl/requested`](#field-ttl-requested) | `no` | integer | TTL requested by the caller before endpoint caps are applied. |
| [`ttl/granted`](#field-ttl-granted) | `no` | integer | TTL granted by the endpoint after exposure-specific caps are applied. |
| [`high-water/seq-no`](#field-high-water-seq-no) | `no` | integer |  |
| [`attestation/ref`](#field-attestation-ref) | `no` | string |  |
| [`dedup/key`](#field-dedup-key) | `no` | string |  |
| [`rate-limit/key`](#field-rate-limit-key) | `no` | string |  |
| [`observed-at`](#field-observed-at) | `yes` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-audit-id"></a>
## `audit/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-request-mode"></a>
## `request/mode`

- Required: `yes`
- Shape: enum: `invitee-first-join`, `member-self`, `authority-roster`

<a id="field-requester-subject"></a>
## `requester/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: string

Digest or stable redacted reference for the requested subject; the audit event must not disclose closed-room roster contents to unauthorized viewers.

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `issued`, `refused`, `deduplicated`, `rate-limited`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-exposure"></a>
## `exposure`

- Required: `no`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

Effective room exposure used for attestation policy evaluation. If the room policy is unavailable, producers may emit the conservative private-to-swarm fallback.

<a id="field-ttl-requested"></a>
## `ttl/requested`

- Required: `no`
- Shape: integer

TTL requested by the caller before endpoint caps are applied.

<a id="field-ttl-granted"></a>
## `ttl/granted`

- Required: `no`
- Shape: integer

TTL granted by the endpoint after exposure-specific caps are applied.

<a id="field-high-water-seq-no"></a>
## `high-water/seq-no`

- Required: `no`
- Shape: integer

<a id="field-attestation-ref"></a>
## `attestation/ref`

- Required: `no`
- Shape: string

<a id="field-dedup-key"></a>
## `dedup/key`

- Required: `no`
- Shape: string

<a id="field-rate-limit-key"></a>
## `rate-limit/key`

- Required: `no`
- Shape: string

<a id="field-observed-at"></a>
## `observed-at`

- Required: `yes`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
