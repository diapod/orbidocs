# Proposal 054: User-Maintained Federated Seed Directory

Based on:

- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/046-agora-topic-key-namespace-conventions.md`
- `doc/project/60-solutions/021-agora-authority/021-agora-authority.md`

## Status

Accepted

## Date

2026-05-02

Promoted to:
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`

## Executive Summary

Seed Directory can be operated by users, communities, and federations, but it
must not become one global source of truth.

The proposed model is a network of local and community-maintained directories
that:

- accept only verified domain artifacts,
- publish accepted facts as Agora records,
- build local discovery projections,
- are evaluated by clients through local trust policy.

A user-maintained Seed Directory may therefore operate as one of three tiers:

1. **personal mirror / local cache**,
2. **community directory**,
3. **federation-endorsed directory**.

All three tiers use the same domain protocol. They differ by the trust a client
or community assigns to the directory operator and to its admission policy.

The core invariant is:

```text
Seed Directory may be user-maintained.
Seed Directory results must remain independently verifiable.
Seed Directory trust is local, weighted, and revocable.
```

## Context and Problem Statement

Proposal 025 defines Seed Directory as a signed cache for
`node-advertisement.v1` and as a capability catalog for passport-backed
capability registrations. Proposal 032 adds delegated operational keys. Agora
Authority defines authority roots and the `agora-publish@v1` /
`agora-subscribe@v1` capability profiles.

The recent directory simplification work establishes a boundary that is
important for federation:

```text
Agora stores and federates accepted public records.
Seed Directory interprets a subset of those records as discovery state.
```

This proposal answers the follow-up question: to what extent can Seed Directory
be maintained by users rather than a central operator?

The answer is: yes, provided clients do not confuse directory availability with
cryptographic truth about a capability. A directory helps clients discover
artifacts and endpoints. Final trust still comes from independent verification
of passports, revocations, node identity, and local policy.

## Goals

- Allow users and communities to run Seed Directory instances.
- Preserve the existing Seed Directory API as a domain-shaped discovery facade.
- Keep capability passports and node advertisements independently verifiable.
- Use Agora as the public/federated accepted-fact substrate, not as the Seed
  Directory policy engine.
- Define trust tiers for directory operators.
- Define a local trust registry for directory endpoints.
- Define the need for optional query attestations for critical responses.
- Define reconciliation rules for multiple directories.

## Non-Goals

- This proposal does not define a single global registry of true Seed
  Directories.
- This proposal does not make raw Agora queries a replacement for Seed Directory
  discovery.
- This proposal does not require every `GET /cap` or `GET /adv` response to be
  signed.
- This proposal does not define a complete reputation algorithm for directory
  operators.
- This proposal does not remove local operator policy from Seed Directory.
- This proposal does not require identical projections across all directories.

## Decision

### 1. Seed Directory Remains a Semantic Facade

Seed Directory remains the domain facade and policy surface for discovery.

It owns:

- node advertisement acceptance,
- passport signature verification,
- sovereign issuer policy,
- `node_id` and `capability_id` consistency,
- expiry checks,
- revocation checks,
- stale sequence checks,
- endpoint joins,
- node-address attestations,
- capability query shape.

Agora MUST NOT learn these domain meanings. Agora verifies envelopes and stores
records. Seed Directory interprets accepted records as discovery state.

### 2. User-Maintained Directory Tiers

A Seed Directory instance SHOULD declare or be configured under one of three
trust tiers.

#### 2.1 Personal Mirror / Local Cache

A personal mirror is the lowest-trust tier.

A user runs Seed Directory for themselves or for a small group. The directory
may:

- replay accepted facts from Agora,
- keep a local SQLite projection,
- filter entries through private allowlists or preferences,
- answer local clients through the standard Seed Directory API.

A personal mirror does not require community recognition. A client treats it as
a local index, not as an authority.

#### 2.2 Community Directory

A community directory is a medium-trust tier.

A user or group operates the directory for a community. The directory still does
not become the source of truth for passports, but its admission policy has
practical meaning:

- which sovereign issuers it recognizes,
- which capabilities it indexes,
- which entries it rejects as spam or abuse,
- how quickly it replays revocations,
- which rate limits and anti-abuse policies it applies.

Clients may configure a community directory as a trusted peer discovery source.
That trust is local and revocable.

#### 2.3 Federation-Endorsed Directory

A federation-endorsed directory is the highest trust tier in the open model.

The directory is still operated by a user, organization, or community, but it
has a public passport for capability `seed-directory`, a federation endorsement,
or another verifiable proof that its operator satisfies the federation's
requirements.

A federation-endorsed directory may be a default bootstrap endpoint for clients,
but it MUST NOT be a monopoly. Clients should be able to query multiple
directories and apply local policy:

```text
accept discovery result if:
  enough trusted directories agree
  OR one configured directory plus independently verified passport passes
  OR the operator manually accepts the result
```

### 3. Directory Trust Registry

There is no need for a global protocol that decides which Seed Directories are
"real". Each client or deployment needs an explicit local trust registry.

Conceptual shape:

```json
{
  "schema": "seed-directory-trust.v1",
  "directories": [
    {
      "node_id": "node:did:key:z...",
      "endpoint": "https://seed.example",
      "trust_level": "personal",
      "passport_ref": "passport:capability:...",
      "federation_id": "orbiplex-main",
      "weight": 1,
      "endorsement_refs": ["endorsement:seed-directory:orbiplex-main"],
      "reputation_ref": "reputation:seed-directory:orbiplex-main"
    }
  ]
}
```

`trust_level` SHOULD initially support:

- `personal`,
- `community`,
- `federation-endorsed`.

The trust registry may be bootstrapped from distribution defaults, manual
configuration, a local community pack, or later from public reputation records.
For the hard-MVP runtime, `endorsement_refs` and `reputation_ref` are local
policy inputs only. They help the daemon decide which trusted directories may
participate in discovery, but they do not replace passport verification,
revocation checks, peer `node_id` verification, or future `ReputationProjection`
logic.

The daemon-owned query policy is configured separately:

```json
{
  "network": {
    "seed_directory_query_policy": {
      "mode": "preferred-directory",
      "preferred_node_id": "node:did:key:z...",
      "required_directory_endorsements": [],
      "include_embedded": false
    }
  }
}
```

`mode` supports:

- `preferred-directory`, the compatibility default. The daemon queries the
  preferred configured directory first and falls back to later configured
  sources, including the embedded local directory as a fallback, only after
  fetch or verification failure. A successful empty response means "the
  preferred source does not currently know this capability" and is reported in
  last-query diagnostics rather than silently falling through.
- `quorum`, which requires `min_success` matching observations for the same
  result.
- `weighted-trust`, which requires `min_weight` total local trust weight for
  the same result.

For `quorum` and `weighted-trust`, the embedded local directory is not counted
as a vote unless the operator explicitly opts in with `include_embedded = true`
or represents it as an explicit trusted source. This avoids accidental
self-voting in multi-directory policy.

All modes consult the bounded revocation feed from eligible sources before
returning merged capability observations. A verified revocation for a passport
id is monotonic for that query: a capability passport revoked by one eligible
directory is filtered out even when another eligible directory still advertises
it. Revocation feed fetch failures are operator diagnostics; they do not make
Matrix, Agora, or any directory an authority substitute for passport and
revocation verification at the consumer boundary.

### 4. Sovereign Issuer Policy Uses Authority Roots

A local list such as `sovereign_participant_ids` is correct for closed or small
deployments. Public federation needs a richer policy surface:

- authority roots from Agora Authority,
- organization roots with custody policy,
- short-lived delegation through `key-delegation.v1`,
- future `community-trusted` / `community-entrusted` attestation,
- local operator override.

The invariant from Agora Authority applies here:

```text
authority root config is not a list of keys that may publish;
it is a list of identities that may establish publishing authority.
```

### 5. Query Attestations Are Optional and Purpose-Built

Ordinary `GET /cap` or `GET /adv` responses do not need to be signed as a
baseline requirement. They contain, or point at, signed domain artifacts that the
client must verify independently.

The missing capability is not a generic signature on every JSON response. The
missing capability is **view integrity evidence**: a way for a directory to say,
"this is the projection slice I served at this time, under this policy and
cursor".

Therefore, the extension is a purpose-built
`seed-directory-query-attestation.v1`, not ad-hoc signing of every response.

A query attestation should be optional and used by critical clients or
multi-directory comparison flows. The first implementation is requested with
`attest=seed-directory-query.v1` on Seed Directory reads and leaves response
shapes unchanged when the parameter is absent. The attestation includes:

- directory `node_id`,
- query mode and normalized query filter,
- digest of the canonical response body without the attestation field,
- projection cursor / high-water mark,
- issued time and expiry,
- signer id,
- signature by the directory node or delegated signing key.

The attestation is proof of the directory response, not proof that the response
is the whole truth about the network. Truth still comes from the accepted fact
log, replayed or locally admitted records, independent verification of the
embedded domain artifacts, and local trust policy. In other words, the
attestation answers "what did this directory serve for this query at this
projection high-water mark?", not "what must every client believe?".

Existing `node-address-attestation.v1` is the right precedent: signed
attestations should have a clear evidence class and purpose rather than turning
transport responses into an implicit authority layer.

### 6. Directory Identity Chain

The claim that Seed Directory has no identity is too strong. The target model
already treats Seed Directory as capability `seed-directory` attached to a Node.

What is missing for the public user-maintained model is the complete identity
and accountability chain:

```text
directory node_id
  -> node advertisement
  -> capability passport: seed-directory
  -> operator binding / authority root / endorsement
  -> local client trust policy
```

In embedded laptop deployments this chain may be simplified. In public
federation it should be explicit.

### 7. Cross-Directory Reconciliation Is Local Policy

Different directories may have different projections and still be correct. This
is not a contradiction. It is a consequence of local policy and partial
federation.

Clients and replaying directories need deterministic reconciliation rules:

- a domain artifact signature wins over a directory's unsupported claim,
- revocation is monotonic and should remove or mark an entry regardless of which
  directory observed it first,
- a newer node advertisement sequence replaces an older one,
- absence from one directory does not invalidate presence in another,
- policy conflict is resolved locally through quorum, preferred directory,
  operator reputation, or manual operator decision.

Important invariant:

```text
SeedDirectoryHTTP(ProjectionFromLocalStore)
==
SeedDirectoryHTTP(ProjectionFromTrustedAgoraReplay)
```

This does not mean all directories have identical state. It means the same
policy applied to the same accepted-fact stream yields the same projection.

## Protocol Model

### Write Path

```text
client request
  -> SeedDirectoryEngine validates domain artifact
  -> local projection/store commit
  -> publish accepted fact to Agora
  -> return Seed Directory response
```

Seed Directory publishes accepted facts, not raw requests:

```text
record/kind    = "seed.node-advertisement.accepted"
content/schema = "node-advertisement.v1"

record/kind    = "seed.capability-registration.accepted"
content/schema = "seed-capability-registration.v1"

record/kind    = "seed.capability-revocation.accepted"
content/schema = "capability-passport-revocation.v1"
```

Future subject-discovery facts should keep the same rule: publish accepted
semantic facts, not raw requests. In particular:

```text
record/kind    = "seed.node-operator-binding.accepted"
content/schema = "node-operator-binding.v1"
```

is a public/operator disclosure fact. It lets Seed Directory project
`participant-id -> node candidates` only for participants that explicitly chose
that disclosure path through a verified `node-operator-binding.v1` bundle.

Privacy-preserving delivery does not require publishing root
`participant-id -> node-id`. `routing-subject-binding.v1` publishes a scoped
`routing-subject-id -> node candidates` projection. Such a routing subject is an
application/discovery identity; transport still connects to the selected
`node-id`, and nym/root participant linkage remains private unless a workflow
explicitly discloses it. The binding is accepted through
`PUT /routing-subject/{routing-subject-id}/{binding-id}` and queried through
`GET /routing-subject/{routing-subject-id}`.

Nym contact discovery follows this same pattern. A nym-authored Matrix or Agora
post may carry a contact reference, but that reference should resolve to a
routing subject or mailbox/contact surface, not to the root participant. The
Seed Directory projection may help locate candidate nodes for that routing
subject; it should not become a public oracle for `nym -> participant`.

### Read Path

```text
client query
  -> local materialized projection
  -> domain-shaped Seed Directory response
  -> optional query attestation for critical clients
```

Clients SHOULD NOT use raw Agora query as the ordinary discovery path. That
would force every client to understand topic naming, record kinds, content
schemas, revocation rules, endpoint joins, passport validation, and local trust
policy.

### Sync Path

```text
Agora replay/subscription
  -> verify Agora envelope
  -> verify accepted fact content schema
  -> verify inner domain artifact where applicable
  -> apply Seed Directory policy
  -> upsert local projection
```

Replay of historical accepted facts is not the same operation as live write
admission. A directory may trust replayed accepted facts only when it trusts the
publisher, federation topic, or a local threshold policy.

## What Is Already Available

| Element | Status | Meaning for user-maintained Seed Directory |
| :--- | :--- | :--- |
| Signed `node-advertisement.v1` | Available | Directory does not have to author the Node advertisement. |
| Signed `capability-passport.v1` | Available | Directory indexes the grant but does not replace it. |
| Passport signature / expiry / revocation verification | Available in the domain model | User-operated directory can enforce local admission policy. |
| `seed-directory` as capability | Defined in Proposal 025 | Directory can itself be a discovery target. |
| Proxy key delegation | Defined in Proposal 032 | Directory operator does not need to use a hot root key for routine signing. |
| Accepted facts via Agora | Direction established and partly implemented | Directories can exchange accepted facts without raw request gossip. |
| Consumer-side independent verification | Defined | Client does not need to trust the directory in order to trust a passport. |

## Trade-offs

### Benefits

- Users can run discovery infrastructure without asking a central operator.
- Discovery remains resilient under partial outages and community forks.
- Seed Directory keeps a stable domain API while Agora carries public accepted
  facts.
- Clients can combine multiple discovery sources with local trust policy.
- Passport verification remains independent of directory trust.

### Costs

- Clients need a directory trust registry instead of one hard-coded endpoint.
- Multiple directories can disagree, so clients need reconciliation policy.
- Public federation needs operator reputation or endorsement over time.
- Optional query attestations add another artifact type and verification path.
- Operators must understand the difference between indexing, endorsement, and
  cryptographic authority.

## Failure Modes and Mitigations

| Failure mode | Effect | Mitigation |
| :--- | :--- | :--- |
| Spam capability registrations | Directory becomes noisy or unusable | Rate limits, required passports, attestation thresholds, local filters. |
| Malicious directory hides entries | Client misses part of the network | Multi-directory query, Agora replay, operator override, directory reputation. |
| Malicious directory injects false entry | Client attempts to connect to unauthorized Node | Consumer-side passport verification and peer-session `node_id` check. |
| Divergent sovereign policies | Directories return different results | Explicit `trust_level`, `federation_id`, authority roots, and client-local policy. |
| Delayed revocation propagation | Client temporarily trusts revoked passport | Revocation polling, `max_revocation_staleness_seconds`, Agora replay, shorter TTL. |
| Compromised directory operator | Directory publishes bad accepted facts | Short-lived delegation, revocation, multi-directory quorum, operator reputation. |

## Open Questions

1. Should `seed-directory-trust.v1` live in node runtime config, in a federation
   pack, or in both?
2. Should the first `seed-directory-query-attestation.v1` later grow Merkle page
   proofs, or is canonical response-body digest enough until multi-directory
   comparison needs partial proofs?
3. Which directory trust policy should be the default for a new open-network
   node: one preferred directory, two-of-N quorum, weighted trust, or manual
   bootstrap?
4. How should `community-trusted` / `community-entrusted` attestation feed into
   directory operator trust?
5. Should personal mirrors enable trusted Agora replay by default once a trusted
   federation pack is installed, or should replay remain an explicit local
   operator choice?

## Next Actions

1. Keep the equivalence invariant for future merge policy:

   ```text
   SeedDirectoryHTTP(ProjectionFromLocalStore)
   ==
   SeedDirectoryHTTP(ProjectionFromTrustedAgoraReplay)
   ```

2. Connect the hard-MVP local `endorsement_refs` / `reputation_ref` input to
   future `ai.orbiplex.reputation/**` records and `ReputationProjection`.
3. Consider Merkle/page proof extensions for `seed-directory-query-attestation.v1`
   only if partial proof verification becomes necessary for large
   multi-directory comparisons.

## Operational Runbook

### Personal Mirror

- Configure one trusted directory entry with `trust_level = "personal"` and a
  low local `weight`, or rely on the embedded local directory in
  `preferred-directory` mode.
- Keep `include_embedded = false` for quorum/weighted modes unless the operator
  explicitly wants the local mirror to count as a vote.
- Enable trusted Agora replay only when a trusted federation pack or explicit
  operator policy defines the relevant federation lanes.

### Community Directory

- Configure the community directory under `seed_directory_trust` with
  `trust_level = "community"`, a bounded local `weight`, and any local
  `endorsement_refs` supplied by the community pack.
- Use `quorum` when multiple community directories should independently observe
  the same discovery result.
- Treat missing results as absence, not deletion. A community directory that
  omits an entry must not remove another directory's positive result.

### Federation-Endorsed Directory

- Configure `trust_level = "federation-endorsed"`, `federation_id`,
  `policy_ref`, and local endorsement references from the federation pack.
- Use `weighted-trust` when federation packs assign different local weights to
  personal, community, and federation-endorsed directories.
- Keep public query attestation optional for normal reads, but require it for
  audit/export workflows that need a signed response digest.

### Failure Handling

- Fetch, parse, verification, policy, and endorsement failures must appear as
  skipped/rejected diagnostics in `/v1/seed-directory` and the operator UI.
- A failed directory source does not reset replay cursors and does not silently
  rewrite query policy.
- Revocations are monotonic: a revoked passport or target cannot be restored by
  a positive observation from a different directory.
- Directory trust chooses discovery sources only. Consumers still verify
  passports, revocation freshness, peer-session identity, and domain admission.

## Implementation Tracking

This section is a lightweight, manually maintained tracker for implementation
work derived from this proposal. Status values:

- `todo` — not started,
- `in-progress` — design or implementation has started,
- `done` — implemented and covered by tests or schema validation,
- `deferred` — intentionally postponed.

| ID | Work item | Status | Done criteria |
| :--- | :--- | :--- | :--- |
| P054-01 | Define `seed-directory-trust.v1` schema | done | Canonical schema exists, has positive/negative fixtures, and documents `personal`, `community`, and `federation-endorsed` trust tiers. |
| P054-02 | Add Node runtime config for trusted directories | done | Node config can load trusted directory entries with `node_id`, `endpoint`, `trust_level`, `weight`, optional `passport_ref`, optional `endorsement_refs`, optional `reputation_ref`, and rejects invalid entries at config check. |
| P054-03 | Expose trusted directory status in operator surfaces | done | `/v1/seed-directory` and Node UI expose query policy, configured/effective trusted directories, trust tiers, weights, enabled state, federation/policy refs, endorsement/reputation refs, replay state, last query diagnostic, and skip reasons without exposing secrets or raw fetch bodies. |
| P054-04 | Define `seed-directory-query-attestation.v1` | done | Canonical schema, positive/negative fixtures, schema-gate validation, and proposal text define query mode/filter, canonical response digest, projection high-water mark, issued time, expiry, signer, and signature. |
| P054-05 | Add optional query attestation support | done | Seed Directory returns a signed query attestation for `GET /adv`, `GET /adv/{node_id}`, `GET /cap`, `GET /cap/{node_id}`, and `GET /revocations` when requested with `attest=seed-directory-query.v1`; unavailable signer returns `503 attestation_unavailable`; default responses remain unchanged. |
| P054-06 | Replay accepted Seed Directory facts from Agora | done | Daemon has opt-in `seed_directory_agora_replay` runtime that replays trusted `adv`, `cap`, and `revocations` lanes from Agora through the Seed Directory Agora adapter, follows paginated result pages until `next_cursor` is absent, persists per-federation lane cursors/status, and applies validated records to the embedded store. |
| P054-07 | Add projection equivalence tests | done | Tests prove direct-write and trusted-Agora replay projection equivalence for advertisements, capability registrations, and revocations, including the effect of revocation on capability lookup. |
| P054-08 | Add multi-directory client query policy | done | Daemon-owned Seed Directory consumers use `preferred-directory`, `quorum`, or `weighted-trust` policy through one source eligibility and merge layer; embedded local directory counts in quorum/weighted only by explicit opt-in. |
| P054-09 | Implement reconciliation rules | done | Capability observations group by `passport_id` with a stable fallback key, duplicate observations from one source cannot satisfy quorum/weight, verified cross-directory revocations monotonically suppress revoked passports, absence in one directory does not delete another directory's positive result, duplicates dedupe deterministically, and subject/capability discovery share the same source eligibility policy. |
| P054-10 | Connect directory operator trust to reputation/endorsement | done | Hard-MVP implements local `endorsement_refs`, `reputation_ref`, and `required_directory_endorsements` as policy inputs; full `ai.orbiplex.reputation/**` to `ReputationProjection` remains post-MVP. |
| P054-11 | Document operational runbook for user-maintained directories | done | Operator docs explain personal mirror, community directory, federation-endorsed directory, multi-directory policy, replay/query failure handling, revocation handling, query attestation, and troubleshooting boundaries. |
| P054-12 | Adopt Temporal Storage Convention for local accepted facts | done | Embedded Seed Directory writes accepted facts and operator retractions into `seed_directory_transactions` / `seed_directory_events`, keeps HTTP/API tables as projections, filters expiry on read, exposes operator temporal status/events/replay-check, and covers replay equivalence for accepted/retracted local facts. |
