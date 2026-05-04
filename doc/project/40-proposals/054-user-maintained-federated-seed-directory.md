# Proposal 054: User-Maintained Federated Seed Directory

Based on:

- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/046-agora-topic-key-namespace-conventions.md`
- `doc/project/60-solutions/021-agora-authority/021-agora-authority.md`

## Status

Draft

## Date

2026-05-02

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
      "weight": 1
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

Therefore, the future extension should be a purpose-built
`seed-directory-query-attestation.v1`, not ad-hoc signing of every response.

A query attestation should be optional and used by critical clients or
multi-directory comparison flows. It should include at least:

- directory `node_id`,
- endpoint or directory identity reference,
- query parameters or canonical query digest,
- response digest or Merkle-style page digest,
- projection cursor / high-water mark,
- policy id or policy digest,
- issued time and expiry,
- signature by the directory node or delegated signing key.

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
2. What is the minimal `seed-directory-query-attestation.v1` shape that is useful
   without becoming a Merkle-tree protocol too early?
3. Which directory trust policy should be the default for a new open-network
   node: one preferred directory, two-of-N quorum, weighted trust, or manual
   bootstrap?
4. How should `community-trusted` / `community-entrusted` attestation feed into
   directory operator trust?
5. Which accepted-fact lanes should be replayed by default for personal mirrors?

## Next Actions

1. Define `seed-directory-trust.v1` as a local configuration schema for trusted
   directories, their weights, and trust tiers.
2. Define `seed-directory-query-attestation.v1` for critical signed discovery
   responses.
3. Complete Agora replay of accepted Seed Directory facts into a materialized
   projection.
4. Add an equivalence test:

   ```text
   SeedDirectoryHTTP(ProjectionFromLocalStore)
   ==
   SeedDirectoryHTTP(ProjectionFromTrustedAgoraReplay)
   ```

5. Add client-side multi-directory query policy: preferred directory, quorum, or
   weighted trust.
6. Connect directory operator trust to future `ai.orbiplex.reputation/**`
   records and `ReputationProjection`.

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
| P054-02 | Add Node runtime config for trusted directories | done | Node config can load trusted directory entries with `node_id`, `endpoint`, `trust_level`, `weight`, optional `passport_ref`, and rejects invalid entries at config check. |
| P054-03 | Expose trusted directory status in operator surfaces | todo | UI/API can show configured trusted Seed Directories, their trust tier, and why each is trusted or rejected. |
| P054-04 | Define `seed-directory-query-attestation.v1` | todo | Schema and proposal text define query digest, response digest, projection cursor/high-water mark, policy id/digest, issued time, expiry, signer, and signature. |
| P054-05 | Add optional query attestation support | todo | Seed Directory can return a signed query attestation for critical `GET /adv`, `GET /cap`, and `GET /revocations` responses when requested. |
| P054-06 | Replay accepted Seed Directory facts from Agora | in-progress | A Seed Directory projection can rebuild from trusted Agora `seed.*.accepted` records after envelope, schema, and domain validation. |
| P054-07 | Add projection equivalence tests | in-progress | Tests prove `SeedDirectoryHTTP(ProjectionFromLocalStore) == SeedDirectoryHTTP(ProjectionFromTrustedAgoraReplay)` for advertisements, capabilities, and revocations under the same policy. |
| P054-08 | Add multi-directory client query policy | todo | Client-side discovery can query multiple trusted directories and merge results using preferred directory, quorum, or weighted trust policy. |
| P054-09 | Implement reconciliation rules | todo | Revocations are monotonic, newer advertisements replace older ones, absence in one directory does not delete another directory's positive result, and duplicate capabilities dedupe deterministically. |
| P054-10 | Connect directory operator trust to reputation/endorsement | deferred | `community-trusted` / `community-entrusted` and `ai.orbiplex.reputation/**` can influence directory trust without replacing local override. |
| P054-11 | Document operational runbook for user-maintained directories | todo | Operator docs explain personal mirror, community directory, and federation-endorsed deployment modes, including failure and revocation handling. |
