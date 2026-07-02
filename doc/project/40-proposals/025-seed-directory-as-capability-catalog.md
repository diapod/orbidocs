# Proposal 025: Seed Directory as Capability Catalog

Based on:
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/20-memos/seed-directory-http-examples.md`
- `doc/schemas/capability-advertisement.v1.schema.json`
- `doc/schemas/node-advertisement.v1.schema.json`

## Status

Accepted

## Date

2026-04-01

Promoted to:
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`

## Executive Summary

The Seed Directory defined in Proposal 014 is a signed cache for
`node-advertisement.v1` artifacts. It answers the question: given a
`node:did:key:...`, what are its current endpoints?

This proposal extends the Seed Directory to also answer: which Nodes currently
hold a given infrastructure capability — backed by a `capability-passport.v1`
(capability *scope*) plus, for federation-official services, a
`federation-service-endorsement.v1` (the federation's vouch, Proposal 076 §6)?

The extension adds two complementary surfaces to the Seed Directory:

1. a **capability registration surface** — Nodes register per-capability with a
   passport-backed scope claim and an optional federation-service endorsement,
   and the directory verifies each artifact before storing it,
2. a **federated revocation surface** — sovereign operators publish revocations
   for artifacts whose validity may be relied on by other Nodes; consumers poll
   for them.

This revocation surface is not the universal home for every revocation in a
Node. Revocations that affect only local dispatch, local modules, local
operator UI, or local host capabilities remain node-local policy projections.
They may be represented by the same signed revocation artifact shape, but they
do not need Seed Directory publication unless another Node is expected to rely
on the artifact being revoked.

The Seed Directory itself is modeled as a capability (`seed-directory`), with
its own passports shipped in the software distribution. This closes the
bootstrap chain: to find Nodes with any capability, you first find the Seed
Directory via passports pinned in your local distribution.

## Context and Problem Statement

Proposal 024 introduced `capability-passport.v1` as the signed delegation
artifact for infrastructure capabilities and defined static-config discovery
for hard-MVP. Static config is sufficient for a single closed deployment, but
it scales poorly:

- each operator must manually maintain config for every capability node,
- there is no network-level query surface for "who currently runs capability X",
- revocation has no propagation channel.

The Seed Directory already solves the analogous problem for Node endpoints: it
is a shared, signed cache rather than a per-operator config problem. Extending
it to capabilities applies the same solution to the capability discovery problem.

A self-referential element is necessary for bootstrap: the Seed Directory itself
must be discoverable without prior knowledge of any running node. Modeling
`seed-directory` as a capability and shipping its passports with the distribution
solves this without introducing a separate hard-coded lookup mechanism.

## Goals

- Extend the Seed Directory with capability registration and query surfaces.
- Require a valid capability passport for every capability registration.
- Define the consumer verification flow: independent passport check, local cache,
  revocation polling.
- Define `seed-directory` as the self-referential capability whose passports are
  shipped in the software distribution.
- Establish the naming convention between `CapabilityAdvertisementV1` capability
  strings and capability passport `capability_id` values.
- Support multiple capabilities per Node, each with its own passport.
- Support sovereign capability ids plus sovereign-aware lookup filters without
  collapsing them into the global bare-name namespace.

## Non-Goals

- This proposal does not define gossip-based capability propagation.
- This proposal does not define capability marketplace or auction mechanisms.
- This proposal does not define per-capability wire protocols. Those are defined
  per capability (e.g. `network-ledger` wire protocol is out of scope here).
- This proposal does not define OpenAPI, ETag headers, or rate-limiting headers
  for the extended Seed Directory. Those may be added without a new proposal.
- This proposal does not define multi-federation capability directories.
- This proposal does not define federation-extension governance for the formal
  capability namespace: who may register new federation-scoped capability ids,
  how public namespace allocation works, or how a namespace-level registration
  authority is revoked. P025 supplies the registration/revocation transport
  mechanics; the governance decision remains the deferred P072 Phase 5 track.

## Decision

### 1. One Registration Per (Node, Capability) Pair

A Node with multiple capabilities registers each separately. One call to
`PUT /cap/{node-id}/{capability-id}` registers one capability entry backed by
one passport.

A Node with three capabilities makes three separate PUT requests. The Seed
Directory stores, verifies, and serves each entry independently. Per-entry
independence allows:

- different expiry per capability,
- independent revocation per capability,
- partial updates without re-registering all capabilities.

### 2. Registration Requires a Valid Passport

The `PUT /cap/{node-id}/{capability-id}` request body MUST carry:

- a signed `capability-advertisement.v1` artifact for the Node,
- a `capability-passport.v1` artifact for the specific `capability_id` (capability
  *scope*),
- optionally, a `federation-service-endorsement.v1` when registering the entry as
  **federation-official** (Proposal 076 §6).

The Seed Directory MUST verify before storing:

1. the passport `signature` — direct passports verify against the issuer
   participant public key recovered from `issuer/participant_id`; passports
   with `issuer_delegation` first verify that inline proof against the issuer
   participant, then verify the passport with `issuer_delegation.proxy_key`,
2. `issuer/participant_id` is a valid, self-consistent issuer for the passport
   (for `sovereign/...`-namespaced custom capabilities, an issuer recognized
   under local policy). **The passport proves capability *scope*, not official
   status** — federation-official / federation-endorsed status is never conferred
   by the passport issuer; it comes solely from a `federation-service-endorsement.v1`
   (see below and Proposal 076 §6),
3. `passport.node_id == {node-id}` in the URL path,
4. `passport.capability_id == {capability-id}` in the URL path,
5. `passport.expires_at` is either absent or in the future,
6. `passport_id` is not present in the directory's revocation log.
7. the **advertisement `signature`** cryptographically verifies against the
   public key recovered from `advertisement.node_id` (not merely the structural
   `validate()`), and the advertisement is fresh (a recent `published_at`/sequence,
   not a replayed stale one the node has since retracted). This makes registration
   a **joint act** — the node itself signed a claim to the capability (its
   `capabilities_core` must include the capability's wire-name, per the naming
   convention in §7) and a
   sovereign separately endorses it — so a sovereign operator (or, since `PUT /cap`
   is unauthenticated, anyone) cannot register or flood the catalog with services
   on nodes that never advertised them.

When a `federation-service-endorsement.v1` is present, the directory MUST verify
it per Proposal 076 §6 (resolve `endorser_subject_ref` in the active
`sovereign_subject_refs[]`; participant = its key, org = custody met) before
marking the entry **federation-official**. A registration without a valid
endorsement is stored as an ordinary scope-only entry, never as official.

Endorsement delivery is **two-phase**: the endorsement does not have to arrive
in the same request as the registration. A sovereign (typically from a separate
high-attestation node, per Proposal 076 P076-013) MAY later submit a standalone
`federation-service-endorsement.v1` for `(node_id, capability_id)`. The
directory MUST accept such an endorsement-attach **only when a scope entry with
a node-signed advertisement covering that capability already exists** (§2 step
7) — an endorsement for a node that never advertised the capability is refused,
so a sovereign cannot conjure official services onto unwilling or unaware nodes.

That refusal MUST be classified as **retryable**, not terminal: the directory
returns a machine-readable reason (e.g. `scope-entry-missing`) distinct from
signature/custody failures, because the endorsement may simply have raced ahead
of the node's own registration. A submitter SHOULD retry with a bounded backoff
schedule (e.g. `5s → 30s → 120s → 360s`) before concluding the target node has
not (yet) claimed the capability and giving up. Cryptographic failures
(signature, custody, expiry, revocation) remain terminal and MUST NOT be
retried on an unchanged artifact.

On successful verification the existing entry is upgraded to
federation-official; the stored endorsement replaces an older one only under the
directory's normal replacement semantics. Capability registrations use
`sequence/no`, aligned with `/adv`, as the primary replacement-ordering
authority. `expires_at` remains a validity boundary, not the update-ordering
mechanism.

If any *terminal* check fails (signature, custody, expiry, revocation, URL
mismatch), the directory MUST return `403 Forbidden` with a machine-readable
reason string. The one deliberate exception is the endorsement-attach
`scope-entry-missing` case above, which returns a **retryable** `409 Conflict`
(§3) — it reflects ordering, not a refusal of authority. Self-reported
capability advertisements without a passport are accepted only for non-critical
capabilities (see Section 7).

The directory stores the passport alongside the capability entry so that
consumers can retrieve it directly.

### 3. Extended HTTP Surface

The existing `/adv` surface is unchanged. The new capability surfaces are:

The Seed Directory does not rely on bearer-token authentication for capability
catalog operations. Discovery reads are open, and write authorization is derived
solely from signed artifacts:

- `PUT /cap` is accepted only when the node-signed advertisement and the
  embedded `capability-passport.v1` (scope) verify; an embedded or
  later-attached `federation-service-endorsement.v1` is additionally verified
  per Proposal 076 §6 before the entry is marked official.
- `POST /revoke` is accepted only when the
  `capability-passport-revocation.v1` verifies under either the `issuer` or
  `subject` authority path.
- `GET /cap*` and `GET /revocations` are intentionally public discovery
  surfaces so Nodes can bootstrap without pre-shared HTTP credentials.

```
# Capability registration (one per node+capability pair)
PUT  /cap/{node-id}/{capability-id}
     Body: { "advertisement": capability-advertisement.v1,
             "passport":      capability-passport.v1,
             "endorsement":   federation-service-endorsement.v1 (optional) }
     → 201 Created | 200 OK (replace) | 403 Forbidden | 409 Conflict (stale)

# Two-phase endorsement attach (scope entry must already exist)
PUT  /cap/{node-id}/{capability-id}/endorsement
     Body: federation-service-endorsement.v1
     → 200 OK (entry upgraded to federation-official)
     | 409 Conflict + { "reason": "scope-entry-missing", "retryable": true }
       (no node-signed scope entry yet; submitter SHOULD back off and retry)
     | 403 Forbidden (terminal: signature/custody/expiry/revocation failure;
       MUST NOT be retried on an unchanged artifact)

# Query: all capabilities of one node
GET  /cap/{node-id}
     → { node_id, endpoints[], capabilities: [ { capability_id, passport,
             official, endorsement,       # endorsement artifact when official
             published_at, expires_at } ] }
     → 404 if node not found

# Query: all nodes with a given capability
GET  /cap?capability={capability-id-or-wire-name}
        [&anchor={anchor-id}]
        [&include_formal=true|false]
        [&include_sovereign_formal=true|false]
        [&include_sovereign_informal=true|false]
        [&include_sovereign=true|false]
        [&official=true|false]
     → { items: [ { node_id, endpoints[], capability_id, passport,
                    official, endorsement,
                    published_at, expires_at, anchor_identity, informal } ],
          next, max-items }

# Revocation log (passports)
POST /revoke
     Body: capability-passport-revocation.v1
     → 200 OK | 403 Forbidden (bad revocation signature)

# Endorsement revocation (current split surface; converges per §5 / P025-004)
POST /revoke/endorsement
     Body: federation-service-endorsement-revocation.v1
     → 200 OK | 403 Forbidden (bad signature / unauthorized revoker)
GET  /revocations/endorsement?since={cursor}
     → paged endorsement-revocation feed (poll alongside /revocations until
       the shared artifact_family log lands)

GET  /revocations?since={cursor}
     → { items: [ { passport_id, node_id, capability_id, revoked_at } ],
         next, max-items }

# Node address attestation
GET  /attest/node-address/{node-id}
     → node-address-attestation.v1
     → 503 if directory signing is missing, or if a configured active probe fails
```

`GET /cap?capability` joins capability entries with the `/adv` table to return
current endpoints alongside each passport. A Node missing a current advertisement
is returned without endpoints (`endpoints: []`) rather than being omitted; the
consumer may still use the passport for out-of-band contact.

Runtime capability queries omit expired registrations by default. A later
operator/debug surface MAY expose an explicit include-expired mode for
historical inspection, but discovery clients MUST NOT receive expired entries
unless they explicitly ask for a diagnostic view.

The Seed Directory SHOULD enforce a policy-tunable maximum number of active
capability registrations per Node. The safe default is **64 active
registrations per Node**. Federations MAY lower this for public low-trust
directories or raise it for governed infrastructure nodes, but unbounded active
registrations are not a safe public-directory default.

Flag defaults:

- `include_formal = true`
- `include_sovereign_formal = true`
- `include_sovereign_informal = false`
- `include_sovereign` is a shortcut for both sovereign flags

This keeps old `GET /cap?capability=...` callers backward-compatible while
still suppressing custom `~...@...` sovereign capabilities unless the consumer
asks for them explicitly.

### 3a. Capability Query Predicate/Filter

Capability discovery consumers may need to ask for "Nodes with capability X
that also satisfy local trust policy Y" without first downloading an arbitrary
page of unrelated entries and filtering it locally.  The Seed Directory query
surface therefore accepts an optional predicate/filter object for capability
discovery. Callers should still keep local post-filtering as a compatibility and
defense-in-depth layer because older Seed Directory endpoints may ignore unknown
query parameters.

The first predicate set stays deliberately small and index-friendly:

- `node_id` / `node_ids` — restrict results to one or more known Nodes,
- `issuer` / `issuers` — restrict results to passports issued by
  a known participant or sovereign operator,
- `capability_id` — keep the primary capability selector explicit inside the
  predicate form when clients use a structured query body,
- `endorsement` — restrict results to entries carrying a recognized federation
  or policy endorsement,
- `passport_profile` — filter by projected passport profile markers. This starts
  as a shallow marker match and can become index-backed when profile projection
  stabilizes.

The predicate is a discovery optimization and policy expression, not an
authorization decision.  Consumers MUST still verify the served Node's passport
after connecting, and local policy MAY reject a result even if the Seed
Directory predicate matched it.

Until this contract is implemented, clients that apply local trust filters
SHOULD avoid passing a page-size `limit` to the Seed Directory before applying
their own filter.  They should filter the returned entries locally and then
apply their acceptance limit.  This prevents untrusted first-page entries from
starving trusted peers.

### 4. Consumer Verification Flow

A Node consuming a passport-backed service MUST:

1. Query the Seed Directory: `GET /cap?capability={capability-id}`.
2. Select a candidate Node from the response.
3. Connect to the candidate Node via the standard inter-node transport.
4. Read the passport — and any endorsement — from the capability advertisement
   already exchanged during session establishment (Proposal 014 §4):
   `capabilities_presented[].{passport, endorsements[]}` arrive in one message.
   Request `capability-passport-present.v1` only as a fallback or refresh when
   the advertisement did not carry them; the normal path adds **no extra
   round-trips** beyond the P014 session baseline. The minimal
   `capability-passport-present.v1` wrapper is owned by this proposal because it
   exists to present or refresh the capability passport used by this capability
   catalog contract.
5. Verify the passport independently:
   - valid Ed25519 signature; for delegated passports, first verify inline
     `issuer_delegation`, then verify the passport with the proof's `proxy_key`;
     for direct passports, verify with the issuer participant key,
   - `passport.node_id` matches the `node:did:key:...` of the peer session,
   - `passport.capability_id` matches the capability being consumed,
   - `expires_at` is absent or in the future.
6. If the consumer requires a **federation-official** service: obtain the
   `federation-service-endorsement.v1` from **any** available source — a local
   cache (still unexpired), the directory response's `endorsement` field, or
   the serving Node itself (the `capability-advertisement.v1`
   `capabilities_presented[].endorsements[]` slot carries it over the
   post-handshake capability exchange). The artifact is self-verifying, so the
   source carries no authority; verify it identically
   per Proposal 076 §6 — resolve `endorser_subject_ref` in the *active*
   `identity.sovereign_subject_refs[]` (participant subject = its key is the
   sole signer; org subject = signer set satisfies that org's custody policy),
   apply the local `endorsement-multiplicity` policy, and check `expires_at`
   plus that `endorsement_id` is not revoked. Passport verification alone
   (step 5) MUST NOT be treated as official status; without a verifying
   endorsement the service is at most community/scope-only.
7. Cache the passport (and endorsement, when present) locally with TTL equal
   to `expires_at` (or a configured maximum if `expires_at` is absent).
   Endorsement acceptance is re-checked against the active federation root on
   every use — sovereign rotation lapses it without any cache invalidation.
8. Reject the connection if any scope verification step fails. A failed
   *endorsement* check downgrades the service to community/scope-only instead
   of terminating an otherwise valid scope connection — unless the consumer's
   policy requires official, in which case it rejects.

Steps 5–6 are the critical independence guarantee: the consumer does not trust
the Seed Directory's copy of either artifact. It trusts only what it verifies
against the peer session and the locally loaded federation root.

### 5. Revocation Artifact and Polling

Passport revocation is expressed as a `capability-passport-revocation.v1`
artifact. Endorsement revocation is expressed as a
`federation-service-endorsement-revocation.v1` artifact targeting
`endorsement_id`. Revocation authority for an endorsement is deliberately
asymmetric to issuance: a participant endorsing subject revokes with its own
key, and for an org subject **any single authorized custodian key** of that
org's custody policy may revoke — revocation narrows trust, so unilateral
withdrawal is fail-safe even though issuance requires the threshold.
(Independently, dropping the endorsing subject from the active federation root
lapses its endorsements without any revocation entry.)

> **Current state vs convergence target (P025-004).** The implementation ships
> endorsement revocation as a *separate* surface: `POST /revoke/endorsement`
> plus a paged `GET /revocations/endorsement` feed and its own storage. The
> convergence target is one federated log shape with an `artifact_family`
> discriminator (`capability-passport` | `federation-service-endorsement`)
> polled through a single `GET /revocations` feed, plus a frozen shared
> schema/fixtures for the revocation artifact. Until convergence, endorsement
> consumers MUST poll the endorsement feed as well — polling only
> `/revocations` does not cover endorsement withdrawals.

For `capability-passport-revocation.v1`, two signing authorities are
recognised, discriminated by the `signed_by` field:

**`signed_by: "issuer"`** — sovereign operator revocation. The same participant
who issued the original passport declares it void. Semantics: *"I withdraw the
delegation I granted."* The `issuer/participant_id` field is required and MUST
match the issuer of the original passport.

```json
{
  "schema":        "capability-passport-revocation.v1",
  "revocation_id": "passport-revocation:...",
  "passport_id":   "passport:capability:...",
  "node_id":       "node:did:key:...",
  "capability_id": "network-ledger",
  "revoked_at":    "2026-04-01T12:00:00Z",
  "signed_by":     "issuer",
  "reason":        "operator key rotation",
  "issuer/participant_id": "participant:did:key:...",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

**`signed_by: "subject"`** — self-revocation by the node. The node whose
capability is being revoked signs the revocation using its own node key (the
private key corresponding to `node_id`). Semantics: *"I no longer offer this
capability."* The `issuer/participant_id` field MUST NOT be present; the Seed
Directory recovers the signer public key from `node_id` directly.

```json
{
  "schema":        "capability-passport-revocation.v1",
  "revocation_id": "passport-revocation:...",
  "passport_id":   "passport:capability:...",
  "node_id":       "node:did:key:...",
  "capability_id": "network-ledger",
  "revoked_at":    "2026-04-01T12:00:00Z",
  "signed_by":     "subject",
  "reason":        "node decommissioned",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

Self-revocation covers the common operational case where a node is being
decommissioned while the sovereign operator is offline. It is not a security
escalation: a node can only withdraw its own passport, never grant capabilities.
The worst-case effect of a compromised node key performing self-revocation is
availability loss, not privilege escalation.

The Seed Directory verifies the revocation signature before storing:

- `signed_by == "issuer"`: verify Ed25519 against `issuer/participant_id` public
  key, check that issuer is sovereign under the directory's policy, check that
  `issuer/participant_id` matches the original passport's issuer.
- `signed_by == "subject"`: verify Ed25519 against the public key derived from
  `node_id`, check that `node_id` matches the original passport's `node_id`. No
  sovereignty check required.

The revocation log is append-only. Both `signed_by` values and the signer
reference are stored for audit.

Consumers MUST poll `GET /revocations?since={cursor}` at an interval no greater
than half the minimum expected passport TTL for capabilities they are actively
consuming. On finding a revocation entry for a cached passport, the consumer
MUST immediately invalidate its local cache and re-verify before continuing
operations.

This polling requirement applies to consumers of Seed Directory-published,
federated capability or delegation artifacts. A Node may also maintain a
separate local `RevocationView` for node-local dispatch decisions; that local
view may include revocations that were never published to the Seed Directory.

Nodes SHOULD also proactively re-verify passports for long-running sessions when
they detect that a cached passport is approaching expiry.

### 6. `seed-directory` as a Self-Referential Capability

The Seed Directory is itself modeled as a capability to unify the bootstrap
chain. A Node acting as a Seed Directory holds a `capability-passport.v1` with
`capability_id = "seed-directory"` for capability *scope*, and — to be trusted as
a **federation-official** directory — a corresponding
`federation-service-endorsement.v1` (Proposal 076 §6). The passport alone
establishes only that the node offers the capability, never that the federation
vouches for it.

These passports are shipped with the software distribution, equivalent to TLS
root trust anchors:

```toml
# Shipped in the default node configuration

[[network.seed_directory]]
node_id     = "node:did:key:z6Mk..."
endpoint    = "https://seed-01.orbiplex.example"
passport    = """{ ... capability-passport.v1 for seed-directory (scope) ... }"""
endorsement = """{ ... federation-service-endorsement.v1 (official) ... }"""

[[network.seed_directory]]
node_id     = "node:did:key:z6Mk..."
endpoint    = "https://seed-02.orbiplex.example"
passport    = """{ ... }"""
endorsement = """{ ... }"""
```

At daemon startup, each seed directory entry MUST be verified:

1. the `capability-passport.v1` signature is valid, `capability_id ==
   "seed-directory"`, and `node_id` matches the configured endpoint's Node — this
   establishes *scope* only;
2. to treat the directory as **federation-official**, a corresponding
   `federation-service-endorsement.v1` MUST be present and verify per Proposal
   076 §6 (resolve `endorser_subject_ref` in the active `sovereign_subject_refs[]`;
   participant = its key, org = custody met). Without it the entry is at most a
   local/community directory, never federation-official.

A seed directory entry whose passport fails verification MUST be skipped with
a logged warning. If no valid seed directory entry remains, the Node starts in
isolated mode and logs a startup warning.

The Seed Directory does not register itself in its own catalog. Its endpoints
are known from the shipped passports only.

### 7. Capability Naming Convention

Capability naming now has three related layers:

| Context | Pattern | Example |
| :--- | :--- | :--- |
| Formal wire capability name | `core/...`, `role/...`, `plugin/...`, or bare formal name | `role/seed-directory` |
| Sovereign wire capability name | `sovereign/...` | `sovereign/audio-transcription` |
| Capability passport `capability_id` | formal bare id or sovereign id with anchor | `seed-directory`, `audio-transcription@participant:did:key:z...` |

Formal mappings stay stable:

```
role/seed-directory   →  seed-directory
core/network-ledger   →  network-ledger
role/escrow           →  escrow
plugin/oracle-basic   →  oracle-basic
```

Unknown formal capabilities may also appear as bare formal wire names and map
to themselves on local, private, or explicitly experimental surfaces. Public
Seed Directory publication SHOULD NOT use unknown bare formal names for custom
services. Public custom capabilities should be identity-anchored sovereign
capabilities, or should first be added to the shared registry as formal
`core/...`, `role/...`, or `plugin/...` mappings.

Sovereign capabilities intentionally do not have a pure-name reverse mapping.
Instead:

```
sovereign/audio-transcription + anchor_identities["audio-transcription"]
  → audio-transcription@participant:did:key:z...
```

Custom sovereign capabilities use the same anchor rule and carry the leading
`~` in the passport capability id:

```
sovereign/article-review + anchor_identities["article-review"]
  → ~article-review@participant:did:key:z...
```

The `~` marker is deliberately part of the canonical `capability_id`, not the
wire projection. The wire name is a routing/discovery projection; the passport
capability id, its anchor, and its signed `capability_profile` are the semantic
source of truth.

Publicly indexed capability passports therefore divide into:

| Public class | Passport `capability_id` | Query / wire name | Acceptance rule |
| :--- | :--- | :--- | :--- |
| Official / community-recognized | registered formal id, e.g. `seed-directory`, `network-ledger`, `offer-catalog` | stable mapped name, e.g. `role/seed-directory`, `core/network-ledger`, `role/offer-catalog` | directory policy requires the configured high-assurance issuer or federation endorsement |
| Compatible sovereign implementation | sovereign id without `~`, e.g. `offer-catalog@participant:did:key:z...` | `sovereign/offer-catalog` plus anchor filter | directory policy verifies the anchor, signature, revocation state, `capability_profile.compatible_with`, schema/profile evidence, and local endorsement predicate |
| Custom / operator-authored | sovereign id with `~` and anchor, e.g. `~article-review@participant:did:key:z...` | `sovereign/article-review` plus anchor filter | directory policy verifies the anchor, signature, revocation state, and any local endorsement predicate; `schema/ref` describes the custom protocol |

Sovereign ids without `~`, such as
`offer-catalog@participant:did:key:z...`, are compatibility claims. They SHOULD
carry `capability_profile.compatible_with = "offer-catalog"` and a
content-addressed `schema/ref` for the profile being implemented. Consumers
MUST still verify this claim against local policy and schema evidence; the name
alone is not sufficient authority.

This keeps public discovery open to community-built services without allowing
unanchored custom strings to look like globally recognized capabilities.

Closed, operator-owned deployments MAY deliberately relax this rule for a
known set of formal capabilities. In that mode the Seed Directory is not a
public recommendation surface; it is a local/deployment catalog whose trust
boundary is the operator's explicit configuration, allowlisted node ids, and
established peer sessions. Story-009 uses this deployment-shaped exception:
`offer-catalog` is a registered formal capability, but its node B/C passports
are accepted inside a closed editorial harness and are not presented as
community-wide endorsement of those providers.

### 8. Directory-Indexed vs. Node-Presented Capabilities

Capability advertisements are no longer raw self-reported strings. They are
Node-signed presentations of passport-form capability assertions.

The Seed Directory still distinguishes two discovery paths:

| Path | Seed Directory publication | Examples |
| :--- | :--- | :--- |
| Directory-indexed (`PUT /cap`) | Yes, accepted only after directory policy verifies the passport | `seed-directory`, `network-ledger`, `escrow`, `oracle` |
| Node-presented (`capability-advertisement.v1`) | No directory required; the peer evaluates the presented passport under local policy | `core/messaging`, `core/discovery`, custom sovereign capability |

`capability-advertisement.v1` may be sent directly after handshake, returned in
response to a capability query, or broadcast where the transport profile admits
datagram-style publication. It carries the presented capability assertions and
the credentials needed for local verification.

`GET /cap?capability=` remains the passport-backed directory lookup surface. It
returns capabilities that the Seed Directory has accepted for indexing. A peer
MAY still accept a directly presented capability that is absent from the Seed
Directory if local policy allows that assertion kind and passport profile.

This separation prevents conflation of directory availability with capability
truth. The directory helps peers find and cache capabilities; it is not the only
way a Node may communicate a signed capability assertion.

Operator-binding availability uses the same passport-backed availability pattern
but adds one extra rule. A `node-primary-operator` passport is only the
participant-side consent half of a `node-operator-binding.v1` bundle. A Seed
Directory MUST NOT accept or serve it as an operator binding unless the payload
also carries the Node's signed acceptance, or an equivalent
`node-operator-binding.v1` bundle, proving that the target Node accepted that
participant as its primary operator. Publishing such a bundle is an explicit
privacy/disclosure decision by the Node, not a default capability-gossip step.

Participant-to-node lookup is therefore not a default directory fact. It is a
public/operator discovery projection derived from accepted
`node-operator-binding.v1` bundles and should be treated as opt-in disclosure.
Directory implementations that expose this projection SHOULD sort candidate
nodes by the local acceptance/receipt time descending, then by `node_id`
ascending as a deterministic tie-break. The local projection timestamp is the
ranking input; remote-declared timestamps are evidence, not authority.

Privacy-preserving contact or delivery discovery should use a scoped
`routing-subject` rather than the root `participant:did:key`. A routing subject
is an application/discovery identity that may be indexed as
`routing-subject-id -> node candidates` without publishing the hidden root
participant relation. Transport still targets the selected `node-id`.

The implemented Seed Directory HTTP surface for these projections is:

```text
GET /participant/{participant-id}
PUT /routing-subject/{routing-subject-id}/{binding-id}
GET /routing-subject/{routing-subject-id}
```

`GET /participant/{participant-id}` is derived from accepted
`node-operator-binding.v1` entries and is therefore an explicit public/operator
disclosure path. `PUT /routing-subject/{routing-subject-id}/{binding-id}` accepts
`routing-subject-binding.v1`: the routing subject signs the binding, the node
signs acceptance over the same canonical binding input, and the directory stores
only bindings that pass shape, path-id, expiry, and signature checks. Both read
projections sort candidates by local acceptance/receipt time descending and then
by `node_id` ascending.

`GET /routing-subject/{routing-subject-id}` is intentionally the public routing
projection. It returns only `routing-subject-binding.v1` entries whose effective
`disclosure/mode` is `public-unlinked`. Bindings marked `participant-disclosed`,
`org-disclosed`, or `present-on-demand` may still be stored as verified facts, but
they are not enumerable through this public resolver without a later
authorization/presentation flow.

This also covers private replies to nym-authored public posts. A public Matrix
or Agora post may expose an optional contact reference for its nym. Seed
Directory should resolve that contact reference to a routing subject and node
candidates, not to the root participant. The reply payload should be encrypted
to the contact/routing public key and delivered to the selected node; the
receiver's local policy decides which participant, operator, or inbox may
decrypt it.

## Artifact Shapes

### `capability-passport.v1` (normative reference to Proposal 024)

Full field list in `doc/schemas/capability-passport.v1.schema.json`.

Capability passports may carry optional `capability_profile` metadata:

```json
{
  "capability_profile": {
    "display/name": "Audio transcription",
    "description": "Transcribes audio input into timestamped text segments.",
    "lang": "en",
    "doc/ref": "orbiplex:blob:sha256:...",
    "doc/url": "https://example.org/capabilities/audio-transcription",
    "schema/id": "urn:orbiplex:capability-profile:audio-transcription:v1",
    "schema/ref": "orbiplex:blob:sha256:...",
    "schema/media-type": "application/schema+json"
  }
}
```

These fields help humans and programs understand the capability profile, but do
not create trust by themselves. The passport signature, issuer policy,
revocation state, and receiver-local policy remain authoritative.

`doc/url` is only a convenience mirror. Runtime behavior MUST NOT depend on
dereferencing it.

### `capability-schema.v1`

Full field list in `doc/schemas/capability-schema.v1.schema.json`.

`capability-schema.v1` is the portable machine-readable description of a
capability profile. It may describe:

- accepted `scope` fields,
- request input shape,
- response output shape,
- error classes,
- retry and idempotency semantics,
- artifact or resource references used by that capability.

The artifact uses:

- `schema/id` as the stable logical contract name,
- `schema/ref` as the content-addressed Orbiplex reference,
- `schema/media-type` to identify the schema language,
- `content` for the actual machine-readable schema,
- a signature for portable provenance when the artifact is cached or relayed.

Nodes may expose schema artifacts through the peer-message kind
`capability.schema.present.request` / `capability.schema.present.response`.
Seed Directory may index or cache them later, but it is not the mandatory
runtime transport for schema retrieval.

The response payload for that peer-message exchange is
`capability-schema-present.v1`, a thin wrapper carrying either:

- `status = "ok"` plus `artifact = { ... capability-schema.v1 ... }`,
- or `status = "error"` plus an error object.

### `capability-passport-revocation.v1`

Full field list in `doc/schemas/capability-passport-revocation.v1.schema.json`.

Fields always required:

- `schema` = `"capability-passport-revocation.v1"`
- `revocation_id` with prefix `"passport-revocation:"`
- `passport_id` — the passport being revoked
- `node_id` — the Node whose capability is revoked
- `capability_id` — the capability being revoked
- `revoked_at` — RFC 3339
- `signed_by` — `"issuer"` or `"subject"` (see Section 5)
- `signature` — Ed25519 over canonical JSON without `signature` field

Conditional fields:

- `issuer/participant_id` — required when `signed_by == "issuer"`, MUST match
  the issuer of the original passport; MUST NOT be present when
  `signed_by == "subject"`
- `reason` — optional human-readable note (both paths)

### Seed Directory Registration Request

```json
{
  "advertisement": { /* capability-advertisement.v1 */ },
  "passport":      { /* capability-passport.v1 */ }
}
```

### `GET /cap?capability=network-ledger` Response

```json
{
  "items": [
    {
      "node_id": "node:did:key:z6MkLedger",
      "endpoints": [
        { "endpoint/url": "wss://ledger.example/peer",
          "endpoint/transport": "wss",
          "endpoint/role": "listener",
          "endpoint/priority": 0 }
      ],
      "capability_id": "network-ledger",
      "passport": { /* capability-passport.v1 */ },
      "published_at": "2026-04-01T10:00:00Z",
      "expires_at":   "2027-04-01T10:00:00Z",
      "anchor_identity": null,
      "informal": false
    }
  ],
  "next": "cur:01JQCAPCUR002",
  "max-items": 100
}
```

### `GET /cap?capability=audio-transcription&include_sovereign=true` Response

```json
{
  "items": [
    {
      "node_id": "node:did:key:z6MkAudio",
      "endpoints": [
        { "endpoint/url": "wss://audio.example/peer",
          "endpoint/transport": "wss",
          "endpoint/role": "listener",
          "endpoint/priority": 0 }
      ],
      "capability_id": "audio-transcription@participant:did:key:z6MkAnchor",
      "passport": { /* capability-passport.v1 */ },
      "published_at": "2026-04-01T10:00:00Z",
      "expires_at":   "2027-04-01T10:00:00Z",
      "anchor_identity": "participant:did:key:z6MkAnchor",
      "informal": false
    }
  ],
  "next": "cur:01JQCAPCUR002",
  "max-items": 100
}
```

### `GET /revocations?since=cur:...` Response

```json
{
  "items": [
    {
      "revocation_id": "passport-revocation:01JQREV001",
      "passport_id":   "passport:capability:network-ledger:01hznx",
      "node_id":       "node:did:key:z6MkOldLedger",
      "capability_id": "network-ledger",
      "revoked_at":    "2026-04-01T12:00:00Z",
      "signed_by":     "issuer"
    },
    {
      "revocation_id": "passport-revocation:01JQREV002",
      "passport_id":   "passport:capability:seed-directory:02abcd",
      "node_id":       "node:did:key:z6MkDecommissioned",
      "capability_id": "seed-directory",
      "revoked_at":    "2026-04-01T14:30:00Z",
      "signed_by":     "subject"
    }
  ],
  "next": "cur:01JQREVCUR003",
  "max-items": 100
}
```

## Implementation Notes

- The reference Node runtime now ships an embedded Seed Directory service
  inside the daemon process. It keeps the same HTTP surface and SQLite schema as
  the earlier sidecar design so deployments can still treat it as the same
  logical service.
- Node-side Seed Directory consumption is split from the daemon host into a
  `seed-directory-client` host-service crate. That crate owns source
  eligibility, bounded capability/revocation fetch, multi-directory
  reconciliation, and monotonic revocation suppression; the daemon maps local
  config into it and keeps HTTP routing, lifecycle, and operator surfaces.
- The Seed Directory persistence layer gains capability and subject-specific
  tables: `capability_registrations`, `capability_passports`,
  `federation_service_endorsements`, `revocations`, and
  `routing_subject_bindings`.
- `capability_registrations` indexes `(node_id, capability_id)` as primary key
  with `published_at`, `expires_at`, and a foreign key to the passport record.
- `federation_service_endorsements` stores the verified endorsement artifact
  keyed by `endorsement_id`, with `(node_id, capability_id)` as a foreign key
  into `capability_registrations`; at most one **active** endorsement per
  `(node_id, capability_id)` (a newer valid endorsement replaces an older one
  under the normal freshness semantics). The read-model `official` flag is a
  projection of this relation, never an independently settable column.
- `revocations` stores `revocation_id`, `artifact_family`
  (`capability-passport` | `federation-service-endorsement`), the per-family
  target (`passport_id` or `endorsement_id`), `node_id`,
  `capability_id`, `revoked_at`, and `signed_by`. The signer identity
  (`issuer/participant_id` or `node_id`) is recoverable from the stored
  `passport_id` and `signed_by` columns; it need not be duplicated.
  *Current implementation state:* endorsement revocations live in a separate
  `federation_service_endorsement_revocations` table; merging into the
  `artifact_family` shape above is P025-004 convergence work.
- The `revocations` table is the Seed Directory's federated publication log. It
  is not a required storage backend for node-local revocations whose effect is
  limited to one Node's dispatch gate.
- The embedded Seed Directory persistence layer now follows the Temporal
  Storage Convention for accepted facts. Local
  `seed_directory_transactions` / `seed_directory_events` are the recovery and
  audit source of truth for accepted advertisements, capability registrations,
  node-operator bindings, routing-subject bindings, revocations, key
  delegations, and local operator retractions. The established HTTP/API
  surfaces still read projection tables. `advertisement_events` remains only a
  compatibility feed/projection during this transition.
- Public reads filter projection rows by domain validity (`expires_at`,
  `valid_until`) and do not perform hidden destructive cleanup. Maintenance and
  compaction must be explicit, operator-visible, and must not silently change
  the meaning of the accepted fact log.
- `GET /cap?capability` joins `capability_registrations` with
  `node_advertisements` to return current endpoints, and with
  `federation_service_endorsements` to project `official` plus the stored
  endorsement artifact.
- `GET /participant/{participant-id}` projects accepted
  `node-operator-binding.v1` entries into node candidates.
- `PUT /routing-subject/{routing-subject-id}/{binding-id}` stores verified
  `routing-subject-binding.v1` entries and `GET /routing-subject/{routing-subject-id}`
  projects only `public-unlinked` entries into node candidates.
- `GET /attest/node-address/{node-id}` assembles
  `node-address-attestation.v1` from the current signed advertisement. In the
  embedded daemon implementation both `PUT /adv/{node-id}` and
  `GET /attest/node-address/{node-id}` use an active WSS
  `peer-handshake.v1` probe when a probe is configured. `GET /attest` issues
  `directory-confirmed` evidence only after a fresh successful probe; if a
  deployment has no probe configured, the same surface can still emit
  `directory-accepted` evidence.
- The two probes have different purposes: the PUT-time probe protects the
  directory write gate, while the attestation-time probe produces fresh
  third-party evidence. A PUT followed immediately by GET may therefore dial
  twice in the MVP. Add a short TTL cache for `ReachabilityProof` keyed by
  `(node_id, endpoint_url)` once traces show this is noisy.
- Active probes are synchronous in the embedded MVP server. Before operating at
  larger registration volume, bound probe concurrency with a semaphore or move
  probing into a small async worker pool with limited fan-out.
- capability registration rows should also project `anchor_identity` and
  `informal` as derived columns from the stored passport capability id so query
  filtering does not need to re-parse every passport blob on the hot path.
- `POST /revoke` branches on `signed_by`:
  - `"issuer"`: verify Ed25519 against `issuer/participant_id`; check issuer is
    sovereign; check issuer matches original passport's `issuer/participant_id`.
  - `"subject"`: verify Ed25519 against the public key decoded from `node_id`;
    check `node_id` matches original passport's `node_id`. No sovereignty check.
  Both paths: reject if `passport_id` is already in the revocation log (idempotent
  reject, not an error) or if the referenced passport is unknown.
- HTTP bearer tokens are deliberately out of scope for this surface. Operators
  may still place the service behind generic rate limiting or network policy,
  but such controls are operational hardening, not part of the capability trust
  model.
- The sovereign key set used by the Seed Directory for passport verification is
  loaded at startup from configuration, following the same pattern as the Node
  daemon's sovereign operator list.
- The `capability-passport-present.v1` post-handshake artifact (for direct
  Node-to-Node passport exchange, step 4 of the consumer flow) is a thin
  wrapper: `{ "schema": "capability-passport-present.v1", "passport": { ... } }`.
  Its full schema may be defined without a new proposal.
- The `capability-schema.v1` artifact is fetched over the existing peer-message
  channel with `capability.schema.present.request` and
  `capability.schema.present.response`. A URL may be carried as a documentation
  hint, but the protocol dependency is the content-addressed `schema/ref`, not
  the URL.
- Revocation cursor format follows the same opaque string pattern as `/adv?since`.

## Consequences

### Positive

- Single service answers both endpoint and capability queries.
- Passport verification at registration prevents unsigned capability claims.
- Consumer-side independent verification prevents directory-compromise attacks.
- `seed-directory` as a capability unifies the bootstrap mechanism.
- Multiple capabilities per Node are first-class, not an afterthought.
- Self-revocation (`signed_by: "subject"`) allows clean node decommissioning
  without requiring the sovereign operator to be online.
- P072 continuation is explicit: when a separate federation-extension governance
  proposal defines public capability namespace allocation, registration
  authority, and namespace-level revocation, it should state how its authority
  records flow into this Seed Directory capability-registration surface and then
  update P072 Phase 5 from deferred to landed.

### Negative

- The embedded Seed Directory service grows in scope and maintenance surface.
- Consumers must implement revocation polling, adding operational complexity.
- Self-referential bootstrap (directory passports in distribution) requires
  governance discipline for key rotation.
- Adding scoped `config-install` as an endorsement delivery surface increases
  the authority of local configuration import. It must therefore remain
  explicit, scoped, and auditable. Peer-presentation delivery remains deferred.

## Alternatives Considered

### Accept raw self-reported capabilities without passport-form assertions

Rejected. Raw capability strings create taxonomy drift and cannot be audited as
governance or operator decisions. A Node may self-issue and directly present a
passport-form assertion, but receivers still evaluate that assertion under local
policy. Critical capabilities such as `network-ledger` require a suitable issuer
or federation policy before they are trusted.

### Separate capability directory service

Rejected. A second service multiplies bootstrap complexity. The existing Seed
Directory already has the persistence layer, inter-node trust model, and
deployment footprint needed.

### Gossip-based capability propagation

Deferred. Gossip is appropriate for eventual consistency at scale; for hard-MVP
with a small known set of infrastructure nodes, a single trusted directory with
polling is simpler and easier to audit.

## Implementation Tracker

| ID | Task | Status | Notes |
|---|---|---|---|
| P025-001 | ~~Resolve issuer sovereignty against the active federation root~~ | superseded | Written before the scope/official split. It grounded *passport issuer* sovereignty as the official-status check in §2/§4/§6; after the model change the passport is scope-only and never confers official status, so resolving its issuer against `sovereign_subject_refs[]` is no longer the official-status mechanism. The intent (federation-grounded verification in §2 registration, §4 consumption, §6 startup) is carried entirely by **P025-002** (endorsement as the sole official-status proof, incl. two-phase attach) on top of **P076-016/P076-017**. |
| P025-002 | Consume `federation-service-endorsement.v1` as the sole official-status proof | partial | Node now wires the verifier core into Seed Directory attach/read: `PUT /cap/{node-id}/{capability-id}` requires a cryptographically valid node-signed `capability-advertisement.v1`; `PUT /cap/{node-id}/{capability-id}/endorsement` requires an existing active scope entry, an active federation authority snapshot derived from `federation-root.v1`, and a valid `federation-service-endorsement.v1` for the expected node/capability before storing it. The Seed Directory stores `federation_service_endorsements` as an at-most-one-active relation and `GET /cap*` projects `official` plus the stored endorsement artifact. Attach responses now include a typed `official_status` decision (`official` or retryable `scope-only` for `scope-entry-missing`). Re-issue is intentionally per endorsement artifact: revoking one `endorsement_id` does not automatically block a later separately signed endorsement for the same `(node_id, capability_id)`. The Seed Directory client carries `official`/`endorsement` through the discovery cache and can build a `PresentedCapability` with `capabilities_presented[].endorsements[]` via the shared presentation builder. Remaining work: consumer-side independent re-verification on every official-status use, exact retry class/backoff surface for `scope-entry-missing`, and broader operator issuance UX. |
| P025-003 | Cryptographically verify the node advertisement signature at `PUT /cap` | done | Seed Directory `validate_capability_advertisement` now calls the network verifier for `capability-advertisement.v1`, verifying the Ed25519 signature against the key recovered from `advertisement.node_id` before accepting the scope registration. A focused regression test mutates a signed field after signing and expects rejection. |
| P025-004 | Extend the federated revocation log to `federation-service-endorsement.v1` | partial | Node now has signed endorsement revocation storage and projection: `POST /revoke/endorsement` accepts `federation-service-endorsement-revocation.v1`, verifies the revoker against the active federation authority snapshot through the shared sovereign-subject signature verifier, treats org revocation as fail-safe unilateral withdrawal by any authorized custodian regardless of issuance threshold, stores `federation_service_endorsement_revocations`, hides revoked endorsements from `official` projections, exposes a paged `GET /revocations/endorsement` feed, and provides best-effort publisher hooks for endorsement and endorsement-revocation facts. Remaining work: converge this with the common `/revocations` feed shape and freeze a shared schema/fixtures for the revocation artifact. |
| P025-005 | Use `sequence/no` as capability-registration replacement ordering | todo | `PUT /cap/{node-id}/{capability-id}` must order replacements by monotonic `sequence/no`, matching `/adv`; `expires_at` only controls validity. |
| P025-006 | Filter expired capability registrations from runtime reads | todo | `GET /cap/{node-id}` and capability queries should omit expired registrations by default. A future operator/debug include-expired mode may exist, but runtime discovery receives active entries only. |
| P025-007 | Enforce a policy-tunable max active registrations per Node | todo | Default limit: 64 active capability registrations per Node. Federation policy may tune it, but public directories must not be unbounded. |
| P025-008 | Define `capability-passport-present.v1` in the Seed Directory capability-catalog contract | todo | Keep the minimal post-handshake/fallback wrapper here rather than in a separate transport memo, because it exists to refresh or present the capability passport used by this catalog. |
| P025-009 | Add scoped `config-install` delivery for `federation-service-endorsement.v1` | todo | In addition to Seed Directory registration, support explicit scoped config-install for endorsement artifacts. Peer-presentation delivery remains deferred until a concrete offline/disconnected use case requires it. |

## Open Questions

None for the current proposal revision.

Resolved 2026-07-02:

1. `PUT /cap/{node-id}/{capability-id}` uses `sequence/no` as its replacement
   ordering authority, aligned with `/adv`; `expires_at` controls validity only.
2. Runtime `GET /cap*` projections omit expired entries by default.
3. Seed Directory enforces a policy-tunable maximum number of active capability
   registrations per Node. The safe default is 64.
4. `capability-passport-present.v1` is defined by this proposal as the minimal
   capability-catalog presentation/refresh wrapper.
5. `federation-service-endorsement.v1` gains Seed Directory registration and
   explicit scoped `config-install` delivery surfaces. Peer-presentation
   delivery remains deferred.
