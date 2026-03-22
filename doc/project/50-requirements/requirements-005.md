# Requirements 005: Transcript Segment and Bundle Schemas v1

Based on:
- `doc/project/50-requirements/requirements-002.md`
- `doc/project/50-requirements/requirements-003.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`
- `doc/project/40-proposals/005-operator-participation-room-policy-profiles.md`

Date: `2026-03-17`
Status: Draft

## Executive Summary

This document freezes v1 schema shape for `TranscriptSegment` and `TranscriptBundle`.

The goal is not maximal richness. The goal is a small, interoperable, audit-friendly contract that preserves:

- question and room identity,
- message provenance,
- human-origin semantics,
- visibility and consent basis,
- transcript integrity and redaction state.

## Context and Problem Statement

`requirements-004.md` defines what the transcript and training pipeline must preserve, but it does not yet freeze the exact data shape.

Without a concrete v1 schema:

- transcript monitors may export incompatible payloads,
- archivists may lose provenance on ingest,
- curators may flatten `human-live` and `node-mediated-human`,
- training nodes may receive under-specified corpus metadata.

These schema contracts also sit in the middle of two upstream flows:

- `requirements-002.md` defines how correction and accepted learning outcomes arise
  in answer rooms,
- `requirements-003.md` defines how approved artifacts later move into archivist and
  vault storage.

The transcript schemas therefore need to be compatible both with correction outcomes
and with later archival packaging.

## Design Principles

1. Data first:
   - schemas should be plain, portable, and easy to validate in `EDN` or `JSON`.
2. Append-only provenance:
   - transcript records describe observed events, not mutable object state.
3. Minimal trusted core:
   - the schema should preserve what later layers need, but not pull in room implementation details unnecessarily.
4. Open model:
   - extra fields MAY exist, but required fields and core enums must remain stable.

## Enumerations

### `origin_class`

Allowed values:

- `node-generated`
- `node-mediated-human`
- `human-live`

### `operator_presence_mode`

Allowed values:

- `none`
- `mediated`
- `direct-live`

### `visibility_scope`

Allowed values:

- `private-to-swarm`
- `federation-local`
- `cross-federation`
- `global`

### `consent_basis`

Allowed v1 values:

- `not-required`
- `operator-consultation`
- `explicit-consent`
- `federation-policy`
- `public-scope`
- `emergency-exception`

### `redaction_status`

Allowed values:

- `none`
- `partial`
- `full-derived`

### `room_policy_profile`

Allowed values:

- `none`
- `mediated-only`
- `direct-live-allowed`

## `TranscriptSegment` v1

### Required fields

- `schema/v`
- `segment_id`
- `question_id`
- `channel_id`
- `message_id`
- `speaker_ref`
- `gateway_node_ref`
- `origin_class`
- `operator_presence_mode`
- `human_origin`
- `ts`
- `content`
- `visibility_scope`
- `consent_basis`
- `provenance_refs`

### Optional fields

- `redaction_markers`
- `content_hash`
- `language`
- `reply_to`
- `attachments`
- `policy_annotations`

### Field constraints

- `schema/v` MUST equal `1`.
- `segment_id`, `question_id`, `channel_id`, and `message_id` MUST be stable strings.
- `speaker_ref` MUST identify the semantic speaker at the room boundary.
- `gateway_node_ref` MUST identify the node that injected the message into the room or relay path.
- `human_origin` MUST be:
  - `false` when `origin_class = node-generated`
  - `true` when `origin_class = node-mediated-human`
  - `true` when `origin_class = human-live`
- `operator_presence_mode` MUST be:
  - `none` when `origin_class = node-generated`
  - `mediated` when `origin_class = node-mediated-human`
  - `direct-live` when `origin_class = human-live`
- `ts` MUST be an ISO-8601 UTC timestamp.
- `content` MUST be a string or a structured content object with a stable textual projection.
- `provenance_refs` MUST be an array, even when empty.
- `redaction_markers` MUST describe removals or transformations rather than silently rewriting content history.

### JSON example

```json
{
  "schema/v": 1,
  "segment_id": "segment:01JNZ8V8EK7M94N8WQ4Q70WJ5V",
  "question_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "channel_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "message_id": "matrix:$Qaf3M9d0event",
  "speaker_ref": "nym:fed-pl:operator-7f3c",
  "gateway_node_ref": "node:pl-wro-7f3c",
  "origin_class": "human-live",
  "operator_presence_mode": "direct-live",
  "human_origin": true,
  "ts": "2026-03-17T21:14:08Z",
  "content": "I have seen this migration fail when the overlap window was too short.",
  "visibility_scope": "federation-local",
  "consent_basis": "federation-policy",
  "provenance_refs": [
    "room:fed-pl:question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
    "event:matrix:$Qaf3M9d0event"
  ],
  "language": "en",
  "content_hash": "sha256:98f6bcd4621d373cade4e832627b4f6..."
}
```

### EDN example

```clojure
{:schema/v 1
 :segment_id "segment:01JNZ8V8EK7M94N8WQ4Q70WJ5V"
 :question_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
 :channel_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
 :message_id "matrix:$Qaf3M9d0event"
 :speaker_ref "nym:fed-pl:operator-7f3c"
 :gateway_node_ref "node:pl-wro-7f3c"
 :origin_class "human-live"
 :operator_presence_mode "direct-live"
 :human_origin true
 :ts "2026-03-17T21:14:08Z"
 :content "I have seen this migration fail when the overlap window was too short."
 :visibility_scope "federation-local"
 :consent_basis "federation-policy"
 :provenance_refs ["room:fed-pl:question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
                   "event:matrix:$Qaf3M9d0event"]
 :language "en"
 :content_hash "sha256:98f6bcd4621d373cade4e832627b4f6..."}
```

## `TranscriptBundle` v1

### Required fields

- `schema/v`
- `bundle_id`
- `question_id`
- `channel_id`
- `source_scope`
- `created_at`
- `source_nodes`
- `segments`
- `contains_human_origin`
- `contains_direct_human_live`
- `consent_basis`
- `redaction_status`
- `integrity_proof`

### Optional fields

- `room_policy_profile`
- `summary_refs`
- `source_transport`
- `retention_profile`
- `policy_annotations`

### Field constraints

- `schema/v` MUST equal `1`.
- `segments` MUST be an array of `TranscriptSegment` records or content-addressed references to such records.
- `contains_human_origin` MUST be `true` if any segment has `human_origin = true`.
- `contains_direct_human_live` MUST be `true` if any segment has `origin_class = human-live`.
- `source_nodes` MUST include every node that acted as a gateway for included segments, if known.
- `consent_basis` at bundle level MUST represent the archival/publication basis for the bundle as a whole, not just one segment.
- `redaction_status` MUST reflect the exported bundle form, not the original room state.
- `integrity_proof` MUST carry enough information to verify bundle integrity or locate the verification artifact.

### JSON example

```json
{
  "schema/v": 1,
  "bundle_id": "bundle:01JNZ94NQ90KJ0H2VTW6J8Q0D9",
  "question_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "channel_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "source_scope": "federation-local",
  "created_at": "2026-03-17T21:32:44Z",
  "source_nodes": [
    "node:pl-wro-7f3c",
    "node:pl-wro-secretary-2"
  ],
  "segments": [
    {
      "schema/v": 1,
      "segment_id": "segment:01JNZ8V8EK7M94N8WQ4Q70WJ5V",
      "question_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
      "channel_id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
      "message_id": "matrix:$Qaf3M9d0event",
      "speaker_ref": "nym:fed-pl:operator-7f3c",
      "gateway_node_ref": "node:pl-wro-7f3c",
      "origin_class": "human-live",
      "operator_presence_mode": "direct-live",
      "human_origin": true,
      "ts": "2026-03-17T21:14:08Z",
      "content": "I have seen this migration fail when the overlap window was too short.",
      "visibility_scope": "federation-local",
      "consent_basis": "federation-policy",
      "provenance_refs": [
        "room:fed-pl:question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
        "event:matrix:$Qaf3M9d0event"
      ]
    }
  ],
  "contains_human_origin": true,
  "contains_direct_human_live": true,
  "consent_basis": "federation-policy",
  "redaction_status": "partial",
  "room_policy_profile": "direct-live-allowed",
  "integrity_proof": {
    "alg": "sha256+ed25519",
    "manifest_hash": "sha256:3f786850e387550fdab836ed7e6dc881...",
    "signer": "node:pl-wro-secretary-2",
    "signature": "base64url:MEQCIG..."
  }
}
```

### EDN example

```clojure
{:schema/v 1
 :bundle_id "bundle:01JNZ94NQ90KJ0H2VTW6J8Q0D9"
 :question_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
 :channel_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
 :source_scope "federation-local"
 :created_at "2026-03-17T21:32:44Z"
 :source_nodes ["node:pl-wro-7f3c"
                "node:pl-wro-secretary-2"]
 :segments [{:schema/v 1
             :segment_id "segment:01JNZ8V8EK7M94N8WQ4Q70WJ5V"
             :question_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
             :channel_id "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
             :message_id "matrix:$Qaf3M9d0event"
             :speaker_ref "nym:fed-pl:operator-7f3c"
             :gateway_node_ref "node:pl-wro-7f3c"
             :origin_class "human-live"
             :operator_presence_mode "direct-live"
             :human_origin true
             :ts "2026-03-17T21:14:08Z"
             :content "I have seen this migration fail when the overlap window was too short."
             :visibility_scope "federation-local"
             :consent_basis "federation-policy"
             :provenance_refs ["room:fed-pl:question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9"
                               "event:matrix:$Qaf3M9d0event"]}]
 :contains_human_origin true
 :contains_direct_human_live true
 :consent_basis "federation-policy"
 :redaction_status "partial"
 :room_policy_profile "direct-live-allowed"
 :integrity_proof {:alg "sha256+ed25519"
                   :manifest_hash "sha256:3f786850e387550fdab836ed7e6dc881..."
                   :signer "node:pl-wro-secretary-2"
                   :signature "base64url:MEQCIG..."}}
```

## Validation Rules

1. A segment with `origin_class = human-live` MUST fail validation if `human_origin = false`.
2. A segment with `origin_class = node-generated` MUST fail validation if `operator_presence_mode != none`.
3. A bundle with `contains_direct_human_live = true` MUST fail validation if no included segment has `origin_class = human-live`.
4. A bundle with `contains_human_origin = false` MUST fail validation if any included segment has `human_origin = true`.
5. A bundle declaring `room_policy_profile = none` MUST fail validation if any included segment has `human_origin = true`.
6. Unknown enum values MUST be rejected in strict mode and quarantined in ingest pipelines that operate in compatibility mode.

## Compatibility Rules

1. Producers MAY add extra fields.
2. Consumers MUST ignore unknown fields unless strict federation policy forbids it.
3. Producers MUST NOT repurpose existing field meanings in v1.
4. Breaking semantic changes require `schema/v = 2`.

## Open Questions

1. Should `content` be normalized to a single textual field in archival bundles, with multimodal payloads referenced externally?
2. Should `speaker_ref` support an explicit composite form for `node + operator nym`?
3. Should bundle integrity be Merkle-based in v1, or is manifest-hash plus signature enough?

## Next Actions

1. Define machine-readable JSON Schema and EDN/spec or Malli forms for these contracts.
2. Add conformance test vectors for all three `origin_class` variants.
3. Bind ingest validation to room-policy profile checks from `proposal 005`.
4. Extend `CurationDecision` and `CorpusEntry` schemas with human-origin eligibility markers.
