# Agora Record v1

Source schema: [`doc/schemas/agora-record.v1.schema.json`](../../schemas/agora-record.v1.schema.json)

Machine-readable schema for a signed, content-addressed, topic-addressed record ingested by an Agora topic relay. The envelope is backend-neutral and intentionally opaque about topic-key shape: the substrate does not type, parse, or split `topic/key`. Resource identity (proposal 026) is reachable through the optional `record/about` field and is never used as the primary key.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/032-key-delegation-passports.md`](../../project/40-proposals/032-key-delegation-passports.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-record.v1` | Schema discriminator. MUST be the literal string `agora-record.v1`. |
| [`record/id`](#field-record-id) | `yes` | string | Content-addressed identifier of this record. Computed by the Orbiplex canonical `sha256_base64url` helper: `sha256:` followed by the unpadded base64url (RFC 4648 section 5) encoding of `sha256(canonicalize(payload))`, where `payload` is the record with `record/id`, `signature`, `relay/received-at`, and `relay/id` removed. Two records with the same canonical payload MUST yield the same `record/id` on every relay. |
| [`record/kind`](#field-record-kind) | `yes` | string | Role label of this record. Application-visible discriminator used by query APIs and kind contracts. Examples: `opinion`, `comment`, `annotation`, `public-log`, `whisper-durable`. The substrate accepts any well-formed kind; it MAY mark unknown kinds as non-indexable until a kind contract is registered. |
| [`topic/key`](#field-topic-key) | `yes` | string | Opaque topic identifier. The substrate MUST NOT parse, split, or type this value. Canonicalization rules: Unicode NFC, no control characters (C0/C1/DEL), no leading or trailing whitespace, non-empty, at most 512 bytes after UTF-8 encoding. Applications choose their own naming conventions (namespace-prefixed paths, content-derived identifiers, human-readable channel names). Topic keys derived from external resource identity are a convention of the record-kind contract, not a rule of the substrate. |
| [`author/participant-id`](#field-author-participant-id) | `yes` | string | Participant identity of the record author. The signature MUST verify against the participant's current capability passport chain, honoring any delegation from proposal 032. |
| [`authored/at`](#field-authored-at) | `yes` | string | Wall-clock timestamp asserted by the author at the moment of record creation. Relays enforce a clock skew window (default ±10 minutes) at ingest; out-of-window records are flagged and temporarily excluded from live query results. |
| [`content/schema`](#field-content-schema) | `yes` | string | Identifier of the schema that describes the inner `content` payload. MUST follow the `{slug}.v{n}` shape. Examples: `plain-comment.v1`, `public-log-entry.v1`, `resource-opinion.v1`. The substrate does not require `content/schema` to be pre-registered; unknown schemas are stored and served but MAY be treated as opaque by indexers. |
| [`content`](#field-content) | `yes` | object | Payload object conforming to the schema named by `content/schema`. Kind contracts define field-level validation; the substrate performs envelope-level validation only. |
| [`record/about`](#field-record-about) | `no` | array | Optional secondary-index references to external subjects this record is about. Each entry follows the resource identity model from proposal 026. MUST NOT be used by the substrate to derive `topic/key`. A kind contract MAY require one or more entries for specific record kinds. |
| [`record/parent`](#field-record-parent) | `no` | string | Optional parent record reference (reply, annotation, successor). MUST resolve to a record under the same `topic/key`. A record that references an as-yet-unknown parent is flagged `dangling` until the parent appears. |
| [`record/supersedes`](#field-record-supersedes) | `no` | string | Optional prior record reference that this record revises or replaces. MUST resolve to a record under the same `topic/key` authored by the same `author/participant-id`, unless a kind contract explicitly relaxes the author constraint. |
| [`record/tags`](#field-record-tags) | `no` | array | Optional short free-form tags for application-level grouping. The substrate does not interpret tag semantics. |
| [`record/lang`](#field-record-lang) | `no` | string | Optional BCP 47 language tag describing the natural-language contents of the record. Informational only. |
| [`relay/received-at`](#field-relay-received-at) | `no` | string | Wall-clock timestamp stamped by the relay that first ingested the record. MUST NOT appear in the payload the author signs. Stripped before `record/id` computation and signature verification. |
| [`relay/id`](#field-relay-id) | `no` | string | Identifier of the relay that first ingested the record. MUST NOT appear in the payload the author signs. Stripped before `record/id` computation and signature verification. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` | Ed25519 signature by the participant key of `author/participant-id` over the canonical payload of this record with `signature`, `relay/received-at`, and `relay/id` removed. Note that `record/id` is INCLUDED in the signed payload: the signature explicitly binds the content-address. `record/id` itself is a separate hash computed over a different canonical payload that additionally excludes `record/id`. Verification uses the participant's capability passport chain (proposals 024 and 032); delegated signing via proposal 032 is permitted. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-record.v1`

Schema discriminator. MUST be the literal string `agora-record.v1`.

<a id="field-record-id"></a>
## `record/id`

- Required: `yes`
- Shape: string

Content-addressed identifier of this record. Computed by the Orbiplex canonical `sha256_base64url` helper: `sha256:` followed by the unpadded base64url (RFC 4648 section 5) encoding of `sha256(canonicalize(payload))`, where `payload` is the record with `record/id`, `signature`, `relay/received-at`, and `relay/id` removed. Two records with the same canonical payload MUST yield the same `record/id` on every relay.

Maintainer note: Canonicalization rules (key sorting, number normalization, Unicode NFC) are defined by the orbiplex-agora-core library and MUST match across implementations. The `sha256:<base64url-no-pad>` shape matches the convention already used by `node/capability/src/lib.rs::sha256_base64url` for signed artifacts and passport hashes.

<a id="field-record-kind"></a>
## `record/kind`

- Required: `yes`
- Shape: string

Role label of this record. Application-visible discriminator used by query APIs and kind contracts. Examples: `opinion`, `comment`, `annotation`, `public-log`, `whisper-durable`. The substrate accepts any well-formed kind; it MAY mark unknown kinds as non-indexable until a kind contract is registered.

<a id="field-topic-key"></a>
## `topic/key`

- Required: `yes`
- Shape: string

Opaque topic identifier. The substrate MUST NOT parse, split, or type this value. Canonicalization rules: Unicode NFC, no control characters (C0/C1/DEL), no leading or trailing whitespace, non-empty, at most 512 bytes after UTF-8 encoding. Applications choose their own naming conventions (namespace-prefixed paths, content-derived identifiers, human-readable channel names). Topic keys derived from external resource identity are a convention of the record-kind contract, not a rule of the substrate.

Maintainer note: The `^\S(.*\S)?$` pattern rejects leading and trailing whitespace. Unicode NFC normalization and the byte-length bound are enforced by orbiplex-agora-core since JSON Schema cannot express them directly.

<a id="field-author-participant-id"></a>
## `author/participant-id`

- Required: `yes`
- Shape: string

Participant identity of the record author. The signature MUST verify against the participant's current capability passport chain, honoring any delegation from proposal 032.

<a id="field-authored-at"></a>
## `authored/at`

- Required: `yes`
- Shape: string

Wall-clock timestamp asserted by the author at the moment of record creation. Relays enforce a clock skew window (default ±10 minutes) at ingest; out-of-window records are flagged and temporarily excluded from live query results.

<a id="field-content-schema"></a>
## `content/schema`

- Required: `yes`
- Shape: string

Identifier of the schema that describes the inner `content` payload. MUST follow the `{slug}.v{n}` shape. Examples: `plain-comment.v1`, `public-log-entry.v1`, `resource-opinion.v1`. The substrate does not require `content/schema` to be pre-registered; unknown schemas are stored and served but MAY be treated as opaque by indexers.

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: object

Payload object conforming to the schema named by `content/schema`. Kind contracts define field-level validation; the substrate performs envelope-level validation only.

<a id="field-record-about"></a>
## `record/about`

- Required: `no`
- Shape: array

Optional secondary-index references to external subjects this record is about. Each entry follows the resource identity model from proposal 026. MUST NOT be used by the substrate to derive `topic/key`. A kind contract MAY require one or more entries for specific record kinds.

<a id="field-record-parent"></a>
## `record/parent`

- Required: `no`
- Shape: string

Optional parent record reference (reply, annotation, successor). MUST resolve to a record under the same `topic/key`. A record that references an as-yet-unknown parent is flagged `dangling` until the parent appears.

<a id="field-record-supersedes"></a>
## `record/supersedes`

- Required: `no`
- Shape: string

Optional prior record reference that this record revises or replaces. MUST resolve to a record under the same `topic/key` authored by the same `author/participant-id`, unless a kind contract explicitly relaxes the author constraint.

<a id="field-record-tags"></a>
## `record/tags`

- Required: `no`
- Shape: array

Optional short free-form tags for application-level grouping. The substrate does not interpret tag semantics.

<a id="field-record-lang"></a>
## `record/lang`

- Required: `no`
- Shape: string

Optional BCP 47 language tag describing the natural-language contents of the record. Informational only.

<a id="field-relay-received-at"></a>
## `relay/received-at`

- Required: `no`
- Shape: string

Wall-clock timestamp stamped by the relay that first ingested the record. MUST NOT appear in the payload the author signs. Stripped before `record/id` computation and signature verification.

<a id="field-relay-id"></a>
## `relay/id`

- Required: `no`
- Shape: string

Identifier of the relay that first ingested the record. MUST NOT appear in the payload the author signs. Stripped before `record/id` computation and signature verification.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

Ed25519 signature by the participant key of `author/participant-id` over the canonical payload of this record with `signature`, `relay/received-at`, and `relay/id` removed. Note that `record/id` is INCLUDED in the signed payload: the signature explicitly binds the content-address. `record/id` itself is a separate hash computed over a different canonical payload that additionally excludes `record/id`. Verification uses the participant's capability passport chain (proposals 024 and 032); delegated signing via proposal 032 is permitted.

Maintainer note: Two distinct canonical payloads are used in this schema: (1) the `record/id` payload excludes record/id + signature + relay fields; (2) the signature payload excludes only signature + relay fields and keeps record/id. This matches the Matrix event-signing pattern where event_id is embedded in the signed content and gives wider cross-transport compatibility.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
