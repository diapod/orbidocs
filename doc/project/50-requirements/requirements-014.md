# Requirements 014: Resource Opinions over Local Agora Relay

Based on:
- `doc/project/20-memos/resource-opinions-and-discussion.md`
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/60-solutions/agora.md`
- `doc/project/60-solutions/agora-caps.edn`
- `doc/project/60-solutions/035-agora-topic-addressed-relay-impl.md`
- `doc/project/50-requirements/requirements-010.md`

Date: `2026-04-16`

Status: Draft

## Executive Summary

Requirements 001–013 cover Node onboarding, federated answer procurement,
learning, archival, transcript curation, networking baseline, settlement,
organization subjects, `capability_limited` participants, middleware
execution, bundled exchange modules, service offers, and Monus. None of them
cover the MVP path for **a participant publishing a signed opinion about an
external URL through the local Agora relay, discovered via the node's
capability-routing surface**.

Story-008 exercises exactly that path end-to-end in the smallest possible
shape:

- one author (operator's primary participant key),
- one URL resource (`resource/kind = "url"`),
- one content schema (`resource-opinion.v1`),
- one `agora-record.v1` envelope,
- one local relay discovered under capability id `agora.relay`,
- zero federation, zero delegation.

This requirements document fixes the contract of that path so that the
smallest coherent Agora slice cannot regress even before the federated
profile lands.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST support publishing a `resource-opinion.v1` content payload as an `agora-record.v1` envelope with `record/kind = "opinion"` and `content/schema = "resource-opinion.v1"`. | Fact | Proposal 035 §3 + Proposal 026 |
| FR-002 | The envelope MUST carry the resource reference in `record/about` as an array containing at least one `{ "resource/kind": "...", "resource/id": "..." }` entry. | Fact | Proposal 026 + Proposal 035 |
| FR-003 | For URL-scoped opinions the `resource/kind` MUST be the literal string `"url"` and `resource/id` MUST be the URL without any implementation-side normalization. | Fact | Proposal 026 + Story-008 AC-4 |
| FR-004 | The MVP deployment MUST accept a `topic/key` of `"ai.orbiplex.opinions/url"` as a default catch-all bucket for URL opinions without requiring a per-domain or per-community split. | Fact | Story-008 Step 3 notes + Proposal 046 |
| FR-005 | A Node UI flow that composes a resource opinion MUST NOT hold a hardcoded Agora endpoint. It MUST resolve the relay endpoint through the daemon's host capability API under capability id `agora.relay`. | Fact | Story-008 AC-1 + Proposal 024 |
| FR-006 | When no `agora.relay` provider is registered locally, the UI MUST surface a clear "no local relay available" state and MUST NOT silently fall back to any non-local relay. | Fact | Story-008 AC-2 |
| FR-007 | Signing MUST use `KeyRef::PrimaryParticipant` as the MVP default, with the signer returning an Ed25519 signature in the `agora.record.v1` domain. | Fact | Proposal 035 + signer-core contract |
| FR-008 | The signing path MUST verify that the public key returned by the host signer matches the author's `participant:did:key` fingerprint and MUST reject the record on mismatch before returning it to the caller. | Fact | Proposal 035 + agora-core sign adapter |
| FR-009 | The envelope MUST self-verify (canonicalize → recompute `record/id` → verify `signature.value` in the `agora.record.v1` domain) before it is persisted or federated. | Fact | Proposal 035 §4 |
| FR-010 | Local ingest MUST be idempotent on `record/id`: a duplicate POST of the same signed envelope MUST return `200 OK` rather than `409` or `201`, without creating duplicate storage rows. | Fact | Proposal 035 §5 + Story-008 AC-6 |
| FR-011 | The relay MUST serve the record back by `record/id` and MUST expose the subject-indexed listing keyed by `{resource/kind, resource/id}` so that later readers can retrieve all opinions attached to a given URL without scanning full topics. | Fact | Proposal 026 + Proposal 035 |
| FR-012 | The MVP local deployment MUST be operable without any `agora.relay` capability passport. A node that never mints an `agora.relay` passport MUST still be able to sign, ingest, query, and subscribe on its own relay. | Fact | Proposal 035 §5.7 + Story-008 AC-8 |
| FR-013 | The relay MUST record a full action trace for each accepted record covering: capability lookup, sign request, ingest, readback. This trace MUST be inspectable without re-running the flow. | Fact | Story-008 AC-7 |
| FR-014 | The relay MUST NOT interpret `content` beyond `content/schema` for ACL or retention purposes. Per-kind content semantics (opinion meaning, ranking, moderation) remain outside the relay contract. | Fact | Solution doc (agora.md) + Proposal 035 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | The smallest useful deployment (one node, one participant, one topic, no passport) MUST remain a first-class configuration rather than a degraded fallback. Local-only behavior SHALL NOT be gated on federation features. | Fact | Proposal 035 §5.7 |
| NFR-002 | The capability-lookup surface (`GET /v1/host/capabilities/agora.relay`) SHOULD return local providers with `transport: "http-local"`, `scope: "local"`, and `passport: null`; it SHOULD distinguish a known-but-unready capability (`200` with empty `providers`) from an unknown capability (`404 capability_unknown`) and SHOULD NOT require a passport to be minted for a local response to be valid. | Fact | Proposal 024 + Story-008 Step 2 |
| NFR-003 | The signing/ingest/query surfaces SHOULD be reachable exclusively on loopback in the MVP local-only profile; remote addresses MUST require explicit operator opt-in at the daemon config layer. | Inference | Operator safety + Proposal 035 |
| NFR-004 | The envelope used in local-only mode MUST be byte-identical to the envelope used in a federated, passport-gated, multi-relay deployment. No local shortcuts, no dialects. | Fact | Proposal 035 + Story-008 architectural significance |
| NFR-005 | The local trace for a published opinion SHOULD be available under a single trace namespace (e.g. `trace/agora`) and SHOULD correlate capability lookup, sign request, ingest, and readback by a common correlation identifier. | Inference | Operability |
| NFR-006 | A deployment that later adds `key-delegation.v1`-backed proxy signing MUST NOT be required to change the envelope wire shape beyond the optional proof fields documented for the delegated-signing layer; archival readers that ignore delegation proofs MUST still be able to verify direct-signed records. | Fact | Proposal 032 |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Node UI hardcodes an Agora endpoint | Breakage when the relay moves ports; no fallback discovery; hidden coupling | FR-005: discovery must go through capability-routing; reject code that imports a hardcoded URL. |
| Signer returns a public key that disagrees with the author's participant id | Record whose signature verifies but whose author claim is a lie | FR-008: hard block in the sign adapter; `SignAdapterError::PublicKeyMismatch`. |
| Duplicate POST creates two storage rows with the same `record/id` | Subject-index and topic pagination become non-deterministic | FR-010: idempotent ingest keyed on `record/id`. |
| URL resource id is silently normalized (trailing slash, case, punycode) before hashing | Two users opining about the same URL end up on different subject-index buckets | FR-003: no normalization drift; byte-identical `resource/id`. |
| Local UI silently falls back to a public relay when no local provider is registered | Operator believes they are posting locally but is in fact publishing to the open web | FR-006: explicit "no local relay available" state, no silent fallback. |
| Operator attempts federation-only workflows on a node that never minted an `agora.relay` passport | Local publication blocked for no architectural reason | FR-012 + NFR-001: local-only mode is first-class. |
| Relay starts interpreting `content` for ACL or moderation | Layer violation; per-kind semantics leak into the substrate | FR-014: relay never reads beyond `content/schema`. |

## Out of Scope

- federation topology, Seed Directory registration of `agora.relay`
  providers, cross-relay replication behavior,
- delegated / proxy-key signing (see proposal 032),
- content moderation, reputation weighting, listener-side filtering,
- multi-subject opinions (`record/about` as an array with more than one
  entry) and richer opinion metadata (`rating`, `tags`),
- any opinion substrate keyed on non-URL resource kinds
  (`resource/kind = "ean"`, `"node"`, `"org"`, `"gps"`, ...); those are
  covered by proposal 026 but not tested by story-008.

## Notes

This requirements document is the "contract" side of the story-008 flow. It
deliberately mirrors story-008's acceptance criteria rather than restating
them, so that implementation work done against the capability catalog
(`agora-caps.edn`) has a checkable requirements trail even if story-008
itself evolves.

The substrate layer (ingest, query, subject-index, topic routing, relay
ACL) MUST remain **open on `resource/kind`** — it accepts any value
conforming to the `resource-ref.v1` shape (`^[a-z][a-z0-9-]*$`, 1..64
chars), not only the literal `"url"`. The URL-only scope present in
FR-003, FR-004, and the "Out of Scope" list above applies solely to the
**MVP UI flow and the story-008 end-to-end test surface**; it is a
product-scope decision, not a contract closure. Implementations MUST NOT
hardcode `"url"` below the UI layer, and a later requirements document
covering non-URL kinds will exercise the same substrate without
requiring schema, gate, or relay changes.

Future requirements documents may extend this one horizontally
(requirements-015 for non-URL resource kinds, requirements-016 for
delegated signing) rather than widening FR/NFR counts in place.

Redelivery semantics — what a relay returns on `GET
/v1/agora/records/{id}` when it once held a record and no longer does,
how a participant's node may re-ship from its local Memarium archive,
how custody between nodes is negotiated and proven, and how sondage
protects relays from flood — are out of scope for the MVP contract
frozen here and are covered by proposal 040 (custodial redelivery and
tombstones). The MVP path (local-only, one node, no federation) does
not exercise those semantics; a federated requirements document will
translate proposal 040 into FR/NFR form.
