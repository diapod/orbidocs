# Proposal 040: Custodial Redelivery and Tombstones for Agora Records

Based on:
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/50-requirements/requirements-014.md`

## Status

Draft

## Date

2026-04-17

## Executive Summary

Agora records are byte-identical, content-addressed, and self-verifying
(proposal 035, requirements-014 FR-009/FR-010/NFR-004). Memarium (proposal
036) is the local organ that preserves what should not disappear, including
the participant's own published artifacts in their original envelope form.
Together they make a simple redelivery pattern possible: if a remote Agora
loses a record, any custodian that still holds the byte-identical envelope
can re-ship it without re-signing, and a content-addressed dedup drops it
into place under the same `record/id`.

What is missing is the **contract** around that pattern:

1. the sovereign right of a remote relay operator to refuse old artifacts
   under current policy, independent of the fact that they were once
   accepted,
2. a protocol-level distinction between "lost" and "removed by policy" on
   readback, so custodians do not hammer a relay that has deliberately
   forgotten,
3. an explicit custody request/response flow so that participants can place
   copies of their own artifacts with other nodes under mutually agreed
   limits, backed by a capability passport,
4. sensible defaults (indefinite self-custody of one's own opinions by the
   local memarium) that do not require operator configuration for the MVP
   path,
5. anti-storm protections on the sondage side: backoff, authenticated batch
   listings, and cheap digests for "do you still hold my stuff" probes,
6. a clear statement that republication is publicly observable via
   `relay/received-at` divergence and that this is a feature, not a leak.

This proposal freezes those six pieces as one contract family so that the
Agora substrate and Memarium organ compose into a resilient, sovereign,
and non-abusive redelivery fabric.

## Context and Problem Statement

Proposal 035 already gives Agora records the cryptographic properties that
make redelivery safe:

- the envelope is signed in the `agora.record.v1` domain over canonical JCS
  bytes that include `content`; no relay can silently rewrite a stored
  record without breaking verification,
- `record/id = sha256(canonical-bytes)` is globally stable, so the same
  artifact arriving at the same relay twice is idempotent (requirements-014
  FR-010),
- `relay/received-at` and `relay/id` are explicitly pruned from the signed
  bytes so that hop-local metadata does not invalidate the author's
  signature.

Proposal 036 gives Memarium the role of the participant's local authoritative
archive, including a first-class relationship to Agora ("an Agora client may
record outbound submissions and their synchronization status as local
Memarium facts").

What the current contracts do not say:

- what a remote relay returns on `GET /v1/agora/records/{id}` when it once
  had the record and no longer does, beyond a generic `404`,
- under what authority a participant's node may push old artifacts to a
  third-party relay,
- how custodian relationships are negotiated and proven,
- how a custodian checks liveness at scale without flooding,
- how much of this is automatic and how much is operator-configured.

The absence of those answers invites two failure modes:

- **custody by accident**: nodes silently reshipping forever, with no
  consent from the receiving operator,
- **opportunistic cenzura laundering**: nodes unable to distinguish "I lost
  your data, please resend" from "I removed it by policy, stop pushing",
  and therefore unable to react correctly to either.

This proposal closes both by making the contract explicit.

## Goals

- Affirm operator sovereignty over acceptance decisions, including over
  artifacts previously accepted.
- Freeze a tombstone vocabulary on the Agora readback surface.
- Define a custody negotiation flow anchored in `capability-passport.v1`.
- State sensible defaults for self-custody of the participant's own
  artifacts in their local Memarium.
- Freeze anti-storm primitives (backoff, authenticated listing, count,
  checksum) to bound the load of redelivery sondage.
- State explicitly that hop-local `relay/received-at` divergence is an
  observable, intentional feature.

## Non-Goals

- This proposal does not define cross-relay gossip or automatic
  anti-entropy between relays. Custody is a participant-driven pattern;
  relay-to-relay replication is out of scope.
- This proposal does not define new content schemas for opinions or other
  record kinds. It operates at the Agora substrate layer only.
- This proposal does not freeze quotas, billing, or economic settlement for
  custody. It only freezes the *consent* surface; economic terms are the
  operator's business.
- This proposal does not define search, ranking, or discovery over
  custodied archives.

## Decision

### 1. Operator Sovereignty over Acceptance

A remote Agora MUST treat every ingest — including an ingest of an
envelope it once held and lost — as a fresh policy decision against its
**current** configuration. Past acceptance does not bind future acceptance.

Concretely:

- an operator MAY refuse redelivery because the relay is at capacity,
  because retention for the topic has been shortened, because the author
  is no longer in scope, or for any other reason consistent with its
  public policy,
- refusal MUST surface through the already-defined ingest error channel
  with a machine-readable reason (see §2 for the readback-side
  counterpart),
- a refusing relay MUST NOT be considered "faulty" by custodians; refusal
  is a first-class valid outcome. A custodian that refuses to accept
  refusal is the abuser in this relationship, not the refusing relay.

This is the substrate counterpart of the node sovereignty principle:
a node cannot be compelled to hold what its operator no longer wishes to
hold, even if it once did.

### 2. Tombstones on Readback

On `GET /v1/agora/records/{record/id}` a relay MUST distinguish four
cases:

| Case | HTTP | Body |
|---|---|---|
| record is present and unchanged | `200 OK` | byte-identical envelope |
| relay has no knowledge of this `record/id` (never held it) | `404 Not Found` | `{"error":"record_unknown"}` |
| relay held this `record/id` and no longer does | `410 Gone` | tombstone JSON (below) |
| relay cannot answer right now (transient) | `5xx` | operator-defined |

Tombstone body (on `410 Gone`):

```json
{
  "error": "record_gone",
  "record/id": "sha256:...",
  "reason": "retention_expired",
  "policy_ref": "...optional..."
}
```

The `reason` field MUST be one of the following stable values:

- `retention_expired` — the record aged out under the topic's retention
  policy,
- `removed_by_policy` — the operator removed it under a moderation,
  legal, or compliance rule,
- `storage_lost` — the relay suffered data loss and acknowledges the gap,
- `superseded` — the record was withdrawn by a higher-layer semantic
  (reserved for future use; not required by MVP).

Custodian reaction matrix:

| Reason | Custodian SHOULD |
|---|---|
| `storage_lost` | re-ship (unless refused under §1) |
| `retention_expired` | do not re-ship; the operator declared the artifact out of scope |
| `removed_by_policy` | do not re-ship; treat as operator decision |
| `superseded` | do not re-ship raw; higher-layer semantics apply |
| `record_unknown` (404) | re-ship if this relay is still an intended destination |
| transient 5xx | retry with backoff; do not treat as gone |

A relay MAY choose not to distinguish `storage_lost` from
`retention_expired` if it considers that privacy-sensitive; in that case it
MUST return `removed_by_policy` as the catch-all, which correctly suppresses
redelivery. The absence of `storage_lost` is always safe for the operator.

### 3. Custody Protocol

A participant's node MAY request that another node hold a copy of some
subset of its memarium artifacts. The flow is:

1. **CustodyRequest** — the requesting node sends, on behalf of its
   participant, a signed request containing:
   - `participant_id` (the author / subject of custody),
   - `scope` (e.g. `"own-agora-records"`, or a topic/author filter),
   - optional `max_bytes` the requester is asking for,
   - optional `max_records`,
   - optional `duration` (ask-for-how-long).
2. **CustodyResponse** — the receiving node answers with `accept` or
   `decline`. An `accept` MUST include a `capability-passport.v1` (proposal
   024) bearing a dedicated `capability_id = "memarium.custody"` whose
   scope encodes the **actually granted** limits (which MAY be lower than
   asked), the counterparty node id, and expiry. The passport is the
   receiver's signed, verifiable consent — the receiver cannot later claim
   "I never agreed" without repudiating their own key.
3. **Transfer** — the requester ships envelopes addressed by their
   `record/id`, either directly to the custodian's ingest surface (for
   Agora-native records) or via a memarium-to-memarium transfer endpoint
   (for memarium-native blobs). Transfers beyond the granted limits MUST
   be refused by the custodian.
4. **Renewal / Revocation** — either side MAY terminate: the custodian
   by letting the passport expire or revoking it through the passport
   revocation channel, the requester by simply stopping to rely on the
   custodian (no artifact push is required to "leave").

Encryption rule:

- content that was encrypted in memarium MUST be transferred in its
  encrypted form and stored as such; the custodian is a byte custodian,
  not a reader,
- content that was plaintext in memarium MAY be transferred in plaintext
  and stored as such,
- the custody passport does not grant read access to encrypted payloads;
  read rights are a separate capability on a separate key path.

Multiple-custody is explicit:

- a participant MAY hold many custody passports from many custodians over
  overlapping scopes,
- each custodian acts independently; there is no coordination requirement
  between them,
- content-addressing (`record/id`) ensures that overlap produces no
  divergence — multiple custodians converge on the same authoritative
  bytes.

### 4. Default: Indefinite Self-Custody

A node's default Memarium policy for its own participant's own
Agora-published artifacts MUST be: **keep indefinitely**. The operator
MAY shorten this, but the MVP default is "forever".

Rationale:

- the node is the natural authoritative custodian of its participant's
  own published facts,
- disk is cheaper than re-publishing lost identity over federated trust,
- if the node operator later disagrees, that is a conscious configuration
  change, not a silent default.

This default MUST NOT extend to:

- artifacts authored by other participants (those follow normal Memarium
  space policies),
- artifacts the participant explicitly chose to expire (via a higher-layer
  right-to-forget flow),
- crisis-space artifacts whose retention is governed by separate
  constitutional rules.

### 5. Anti-Storm Protections

Custodians performing liveness sondage ("is my stuff still there?") MUST
follow these rules; target relays MAY enforce them.

**Backoff.** Per-endpoint exponential backoff on transient errors and on
any `Retry-After` header. A custodian MUST NOT hammer a 5xx relay faster
than the relay's advertised cadence. If no `Retry-After` is sent,
default to a capped exponential (e.g. 1s → 2s → 4s → … → 1h ceiling).

**Proof of authorship for bulk queries.** To read back anything
author-scoped (count, listing, digest), the requester MUST present a
short-lived, signed proof-of-authorship token:

```json
{
  "schema": "agora-author-proof.v1",
  "author/participant-id": "participant:did:key:...",
  "relay/id": "relay.example.org",
  "issued_at": "2026-04-17T10:00:00Z",
  "expires_at": "2026-04-17T10:05:00Z",
  "nonce": "..."
}
```

signed in a dedicated `agora.author.proof.v1` domain by the participant's
key. The relay MUST verify that the signer matches the claimed
`author/participant-id` and that `relay/id` matches its own identity
(preventing cross-relay replay), before returning any author-scoped
aggregate data.

**Batch listing endpoint.** `GET /v1/agora/authors/{author-id}/records`
with the proof token as a header MUST return:

- an array of `record/id` values held for that author,
- ordered by `authored/at` ascending (stable),
- paginated by an opaque cursor,
- with no envelope bodies (identifier-only).

**Count endpoint.** `GET /v1/agora/authors/{author-id}/count` with the
proof token returns `{"count": N}`. This is a cheap liveness check
against expected totals.

**Digest endpoint.** `GET /v1/agora/authors/{author-id}/digest` with the
proof token returns:

```json
{
  "algo": "sha256",
  "value": "sha256:...",
  "record_count": N,
  "as_of": "..."
}
```

The digest is defined as `sha256(concat(record_id_i for i in records
sorted by (authored_at, record_id)))`. Two custodians computing this over
the same set get the same value; divergence is detectable in one byte
comparison. The ordering key is fixed to make the digest deterministic
across relays.

Together these three endpoints let a custodian detect most redelivery
needs with one HTTP call (digest mismatch → fall back to listing → diff
against local memarium → reship only the missing `record/id`s).

**Topic-scoped digests.** Beside the author-scoped trio above, the relay
MUST also expose topic-scoped reconciliation endpoints:

- `GET /v1/agora/topics/{key}/records` — ordered listing of `record/id`
  values under the topic, paginated by opaque cursor, identifier-only
  (this overlaps with the existing topic-records surface from
  proposal 035 and MAY reuse it with an `ids_only=true` query
  parameter),
- `GET /v1/agora/topics/{key}/count` — `{"count": N}` for the topic,
- `GET /v1/agora/topics/{key}/digest` — the same digest construction as
  above, applied to the set of `record/id` values present under the
  topic:
  `sha256(concat(record_id_i for i in records sorted by (authored_at, record_id)))`.

Topic-scoped endpoints do NOT require `agora-author-proof.v1`: topic
contents are already publicly enumerable under the existing readback
surface (requirements-014 FR-011), so adding a digest over the same
set does not expose any additional information. A relay MAY still
apply rate limits and `Retry-After` to these endpoints.

Topic-scoped digests serve two distinct consumers:

- **custodians** performing reconciliation across a topic where they
  hold an expected subset (e.g. all records their participant has
  authored under `opinions/url`),
- **future cross-relay mesh replication** (signaled in proposal 035
  Follow-Up): two relays carrying the same topic can detect divergence
  with one digest comparison before falling back to listing + diff.
  Bringing the digest primitive into the substrate now keeps the
  future mesh protocol content-addressed and zero-trust across relays
  rather than inventing a bespoke gossip channel.

The digest ordering key (`(authored_at, record_id)`) MUST be identical
across author-scoped and topic-scoped variants, so that a record
contributes the same byte to every digest it appears in — this makes
cross-scope reasoning (e.g. "is the author-digest subset of the
topic-digest consistent with what I see?") mechanical rather than
schema-dependent.

Optional range-digest (`?from=…&to=…` on `authored_at`) is deferred to
a follow-up; the unbounded digest above is the MVP contract.

### 6. Public Observability of Redelivery

Redelivery is publicly observable through `relay/received-at` divergence:
a reader pulling the same `record/id` from two relays will see two
different reception timestamps, even though the signed `authored/at` is
identical. This is a feature:

- `authored/at` is the participant's signed claim about when the fact was
  made,
- `relay/received-at` is each relay's own claim about when it accepted
  the fact,
- divergence between relays is expected and meaningful; it is the visible
  record of federation topology over time.

Readers MUST NOT conflate `relay/received-at` with authorship time.
Aggregators MAY use the minimum observed `relay/received-at` across
relays as an "earliest known public appearance" metric, but that is a
read-model convention, not a contract.

Relays MUST NOT rewrite `relay/received-at` on a later reship to pretend
the record arrived earlier; the field is "when did *this* acceptance
happen", and redelivery is a new acceptance.

## Consequences

Positive:

- redelivery becomes a well-defined protocol instead of an accidental
  behavior,
- operators can refuse without being perceived as broken,
- custodians can detect the difference between "please resend" and "stop
  asking" and behave accordingly,
- multi-custody gives participants natural redundancy without
  cross-relay replication machinery,
- sondage at scale stays cheap through count/digest primitives backed by
  proof-of-authorship,
- the default "forever" self-custody policy removes the most common
  footgun (author loses their own publication history because nobody
  configured retention).

Tradeoffs:

- relays must implement `410 Gone` with reason codes and a minimal
  author-scoped query surface; this is new ingest-side work,
- proof-of-authorship tokens add a signing operation to author-scoped
  queries, though the cost is negligible versus the federation it
  protects,
- `storage_lost` is socially uncomfortable — operators may prefer the
  catch-all `removed_by_policy`, which is explicitly allowed but
  suppresses useful redelivery,
- indefinite self-custody assumes the operator accepts the disk cost; for
  pathological volumes the operator must opt out consciously.

## Open Questions

- Should the custody passport's `scope` grammar be frozen here, or
  delegated to a separate custody-scope proposal alongside other
  capability scopes?
- Should `agora-author-proof.v1` be generalized to a reusable
  "short-lived self-proof" artifact family, since the same pattern
  appears in several probes (sondage, recovery, attestation)?
- Should `digest` cover `authored/at`-range windows by default, for
  efficient incremental reconciliation, or should range-digest be a
  later addition?
- Should custody acceptance be allowed to be anonymous (a passport
  bearing only a custodian pseudonym), or must the custodian's node
  identity always be resolvable?
- How should custodian-held copies be evicted on author-initiated
  right-to-forget without violating the author-sovereign intent when
  the custodian is itself offline?

## Follow-Up

If adopted, the next artifacts should be:

1. a schema file for `agora-author-proof.v1`,
2. a schema / scope definition for the `memarium.custody` capability
   within `capability-passport.v1`,
3. a requirements note tying §2 (tombstones) into the Agora readback
   surface alongside requirements-014,
4. a requirements note tying §4 (default self-custody) into Memarium
   space policies alongside proposal 036,
5. an operational playbook for custodians on sondage cadence, digest
   usage, and behavior across the tombstone reason matrix,
6. proposal 041 (Agora ingest attestation) defines the ingest-side gate
   that reshipment traverses; its reason-code vocabulary is symmetric
   with the tombstone matrix here, and custody acceptance (§3) is
   itself one of the consumers of the shared `attestation-gate`
   primitive (a custodian verifies that the requesting participant is
   attested under a passport the custodian's operator currently
   accepts, before admitting the custody relationship).
