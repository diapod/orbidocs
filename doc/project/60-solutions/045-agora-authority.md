# Solution 045: Agora Authority

Date: `2026-05-01`
Status: Draft

Based on:
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`
- `doc/project/50-requirements/requirements-008-org-subject-rollout.md`
- `doc/project/60-solutions/008-agora/008-agora.md`
- `doc/project/60-solutions/014-key-delegation-passports/014-key-delegation-passports.md`

## Executive Summary

Agora Authority defines who may publish or subscribe to topic namespaces when a
relay needs more than local development authentication.

The design separates three layers:

1. **Authority roots**: locally configured high-assurance subjects that may
   establish authority for a namespace.
2. **Operational delegation**: short-lived proxy or derived keys that may act for
   an authority root under a scoped proof.
3. **Capability profiles**: `agora-publish@v1` and `agora-subscribe@v1`, which
   bind a caller to allowed topic prefixes, record kinds, content schemas, and
   read/write operations.

For the initial Orbiplex namespace, deployments SHOULD protect authoritative
records such as announcements and proposals with highest-attestation authority
roots. Social participation records such as comments and resource opinions are a
different tier: any author with at least phone-confirmed attestation SHOULD be
able to comment and publish an opinion about a resource, subject to rate limits,
abuse controls, and local moderation.

## Context and Problem Statement

Agora v1 already verifies `agora-record.v1` envelope shape, content address,
signature bytes, and topic ACLs. That is not enough for decentralized
responsibility.

A public namespace such as `ai.orbiplex.*` needs two different questions:

```text
For authoritative records:
Which accountable subject has authority to publish here, and through which
operational key did that authority act?

For participation records:
Is this author sufficiently attested to participate here, and under which
rate/moderation policy?
```

Hard-coding public keys in source code is the wrong boundary:

- the code is open and can be recompiled,
- federated test environments need their own trust roots,
- root key rotation should not require rebuilding binaries,
- long-lived high-assurance keys should not be used for day-to-day signing.

The authority model must therefore be configuration-driven and delegation-aware.

## Proposed Model / Decision

### 1. Authority Roots

An authority root is a locally configured subject that the deployment accepts as
a high-assurance source of namespace authority.

Authority roots are not merely keys that may publish. They are subjects that may
establish or delegate the right to publish or subscribe.

Core invariant:

```text
authority root config is not a list of keys that may publish;
it is a list of identities that may establish publishing authority.
```

The concrete key that signs an `agora-record.v1` may be the root key, a proxy
key, or a derived operational key. The authority decision is about whether that
signing path resolves to a configured root subject for the target namespace.

Minimal shape:

```json
{
  "agora": {
    "authority_roots": [
      {
        "id": "participant:did:key:z...",
        "kind": "participant",
        "assurance": "highest",
        "purposes": ["agora.namespace.root"],
        "namespaces": ["ai.orbiplex/**"],
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_until": null
      },
      {
        "id": "org:did:key:z...",
        "kind": "org",
        "assurance": "highest",
        "purposes": ["agora.namespace.root"],
        "namespaces": ["ai.orbiplex/**"],
        "custody_policy_ref": "org-custody:orbiplex-foundation:v1"
      }
    ]
  }
}
```

Rules:

- `id` MUST be a canonical subject identifier.
- `kind` MUST match the identifier family.
- `assurance` SHOULD support at least `highest`, `delegated-highest`, and
  deployment-local lower tiers.
- `namespaces` are topic-prefix patterns, not schema identifiers.
- absence of an authority root for a protected namespace means no one is
  locally authoritative for that namespace.

### 2. Participants and Organizations

`participant:did:key` roots are direct high-assurance human or operator anchors.

`org:did:key` roots are accountable institutional anchors. In the current MVP,
organization custody is resolved through one custodian participant. Later
resolvers may support threshold, board, council, or multisig policies without
changing the Agora record envelope.

Authority resolution therefore has this conceptual interface:

```rust
trait AgoraAuthorityResolver {
    fn resolve_authority(&self, record: &AgoraRecord) -> Result<ResolvedAuthority>;
    fn authorize_namespace(&self, authority: &ResolvedAuthority, topic: &str) -> Result<()>;
}
```

`ResolvedAuthority` should preserve:

- the root subject id (`participant:did:key` or `org:did:key`),
- the concrete signing key,
- the delegation or custody proof path,
- the matched namespace rule,
- the effective assurance level,
- validity and revocation status at `record.authored/at`.

### 3. Operational Delegation and Derived Keys

Authority roots SHOULD be long-lived anchors. They SHOULD NOT be used as ordinary
online signing keys.

Operational signing should use short-lived delegated keys:

```text
authority root
  -> key-delegation.v1 / custody proof / derived-key proof
  -> proxy or derived operational key
  -> agora-record.v1 signature
```

This keeps root keys offline or rarely used while allowing practical federation.

Existing `key-delegation.v1` already provides the correct direction for
participant roots:

```json
{
  "grants": {
    "signing/agora-record": ["topic:ai.orbiplex.proposals/035"]
  },
  "expires_at": "2026-06-01T00:00:00Z"
}
```

For `ai.orbiplex/**`, deployments SHOULD prefer explicit namespace grants over
the wildcard `*`.

Derived keys MAY be used as operational keys, but the configuration SHOULD
anchor authority in the long-lived root subject. A derived key should be trusted
because it carries a proof path to a configured authority root, not because it is
listed as a root by itself. Test deployments MAY list short-lived delegated keys
directly, but that should be treated as a deployment-local shortcut.

### 4. `agora-publish@v1`

`agora-publish@v1` is the capability profile for publishing final records into
Agora topics.

The profile has two intended uses:

- **authority publish**: announcements, proposals, policy records, namespace
  roots, or other records that speak *for* a project, organization, or
  federation,
- **participation publish**: comments, resource opinions, and similar records
  that speak *as* an attested author.

These two uses SHOULD NOT share one undifferentiated rule. The record kind and
content schema matter.

Example authority-publish profile:

```json
{
  "profile": "agora-publish@v1",
  "grants": {
    "agora/publish": ["topic:ai.orbiplex/**"]
  },
  "topics": ["topic:ai.orbiplex/**"],
  "record_kinds": ["announcement", "proposal"],
  "content_schemas": ["plain-comment.v1", "public-log-entry.v1"],
  "max_revocation_staleness_seconds": 300
}
```

`proposal` is intentionally listed as a record kind even though its dedicated
content schema may be introduced later. Until then, a deployment may carry
proposal-like text as `plain-comment.v1` or use another explicitly configured
schema such as `public-log-entry.v1`. The authority decision is keyed by record
kind, topic, and local policy; the content schema list is the concrete wire
allowlist for a given deployment.

Example participation-publish profile:

```json
{
  "profile": "agora-publish@v1",
  "grants": {
    "agora/publish": [
      "topic:ai.orbiplex.comments/**",
      "topic:ai.orbiplex.opinions/**"
    ]
  },
  "topics": [
    "topic:ai.orbiplex.comments/**",
    "topic:ai.orbiplex.opinions/**"
  ],
  "record_kinds": ["comment", "opinion"],
  "content_schemas": ["plain-comment.v1", "resource-opinion.v1"],
  "max_revocation_staleness_seconds": 300
}
```

For comment threads, the minimum participation threshold MAY be tightened by a
separate `thread-policy` record:

```text
record/kind    = "thread-policy"
content/schema = "comment-thread-policy.v1"
```

A root comment or descendant comment can reference that policy through
`record/policy`. The effective policy is inherited by descendants. A descendant
MAY attach a stricter policy for its own subtree, but MUST NOT loosen the
inherited policy. This keeps speech content (`plain-comment.v1`) separate from
participation control, while still letting the thread initiator set a minimum
attestation level such as `phone-confirmed`.

Authority-publish authorization succeeds only if:

1. the `agora-record.v1` envelope verifies,
2. the topic matches an `agora/publish` grant,
3. the record kind and content schema satisfy profile constraints,
4. the signing key resolves to an accepted authority root,
5. the authority root is authorized for the topic namespace,
6. the delegation, custody proof, or derived-key proof is current and not
   revoked,
7. the effective assurance satisfies the profile.

For `ai.orbiplex/**`, the recommended local policy is:

```text
announcement/proposal publish allowed iff effective authority assurance == highest
comment/opinion publish allowed iff author attestation >= phone-confirmed
```

For a policy-bound comment thread, `phone-confirmed` above is the default
participation floor. The effective floor is the stricter of the topic policy
and the inherited `comment-thread-policy.v1` records that apply to the comment.

This distinction preserves an important civic boundary: ordinary participants
should be able to speak, comment, and attach opinions to resources without
holding project authority. Project authority is required only for records that
claim to speak for a namespace, organization, council, or federation.

### 4a. Relationship to Ingest Attestation

Participation publishing SHOULD reuse the Proposal 041 attestation-gate rather
than authority roots.

For comments and opinions, the relay asks:

```text
Does the author present an accepted attestation at or above the configured
participation threshold?
```

For announcements and proposals, the relay asks:

```text
Does the signing path resolve to a configured authority root for this namespace?
```

These are complementary gates:

- attestation gate answers whether an author may participate,
- authority resolver answers whether an author may speak with namespace
  authority.

The same `agora-publish@v1` profile can describe both gates, but the evaluator
must keep their semantics separate. `required_author_attestation` MUST NOT be
treated as authority to publish announcements, and
`required_authority_assurance` MUST NOT be required for ordinary comments or
resource opinions unless local policy deliberately creates a closed topic.

### 5. `agora-subscribe@v1`

`agora-subscribe@v1` is the capability profile for reading, replaying, or
streaming topic records when a relay is not public-open.

Example passport scope profile:

```json
{
  "profile": "agora-subscribe@v1",
  "grants": {
    "agora/subscribe": ["topic:ai.orbiplex/**"]
  },
  "topics": ["topic:ai.orbiplex/**"],
  "modes": ["history", "live"],
  "max_revocation_staleness_seconds": 300
}
```

Subscribe authorization is intentionally separate from publish authority:

- public topics may allow anonymous or token-authenticated subscribe,
- protected topics may require a passport-backed `agora-subscribe@v1` grant,
- reading a topic does not imply any right to publish to it,
- publishing to a topic does not imply any right to subscribe to unrelated
  topics.

The profile should gate:

- `GET /v1/agora/topics/{topic}/records`,
- `GET /v1/agora/topics/{topic}/subscribe`,
- `GET /v1/agora/about/{kind}/{id}/records` when the subject query would reveal
  protected topics.

Reference implementation note: `agora-service` keeps `open`,
`authenticated`, and `deny` as local transport ACL modes, and adds
`capability` as the passport-backed mode. In `capability` mode the service
first requires the normal Agora client token, then asks the daemon host
capability API to authorize either `agora.publish.authorize` or
`agora.subscribe.authorize`. The daemon evaluates the local
`capability-passport.v1` against the built-in `agora-publish@v1` and
`agora-subscribe@v1` profile evaluators. Subject-index results are filtered by
the same subscribe gate so they cannot reveal records from protected topics.

### 6. Relationship to Topic ACLs

Topic ACLs remain a local relay policy. They are the fast local gate.

Authority roots and capability profiles are the accountable authorization layer.

The intended order is:

```text
HTTP/client auth
  -> topic ACL coarse gate
  -> envelope verification
  -> capability profile evaluation
  -> authority root / delegation resolution
  -> ingest or subscribe
```

A development relay MAY run with permissive topic ACLs and no authority roots.
A federated relay for protected namespaces SHOULD require both topic ACL match
and authority resolution.

## Trade-offs

### Benefits

- Removes high-assurance public keys from source code.
- Allows federated test networks to define their own trust roots.
- Keeps long-lived authority roots separate from operational signing keys.
- Lets participant and organization roots share one resolver interface.
- Preserves Agora's role as record substrate while moving namespace
  responsibility into a dedicated policy layer.

### Risks

- More moving parts than a static public-key allowlist.
- Organization authority remains weak until custody policies are implemented
  beyond the MVP single-custodian model.
- Misconfigured roots can create local forks of namespace authority.
- Wildcard delegation can accidentally grant more power than intended.

### Constraints

- The `agora-record.v1` envelope should not grow org-custody semantics.
- `agora-core` should remain a signature and content-address verifier, not an
  authority policy engine.
- Authority resolution must be deterministic for a given config, record, and
  revocation snapshot.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Public keys remain hard-coded in code | Rebuild required for federation/test roots; false sense of security | Move roots into config and keep code as policy interpreter only. |
| Root key signs day-to-day records directly | Higher compromise blast radius | Prefer short-lived proxy or derived operational keys with proof paths. |
| Derived key is configured as an opaque root | Accountability chain is lost | Treat direct delegated-key roots as test-only or require `parent` metadata and expiry. |
| Org root has no custody resolver | Relay cannot know who may act for the org | MVP resolver uses `org/custodian-ref`; future resolver supports threshold policies. |
| Wildcard `signing/agora-record = "*"` is overused | Broad accidental publish authority | UI and policy SHOULD prefer explicit topic targets and warn on wildcard use. |
| Comments and opinions require highest authority | Ordinary attested participants cannot participate | Split authority publish from participation publish; use phone-confirmed or equivalent attestation for `comment` and `opinion`. |
| Phone-confirmed participants can publish announcements | Namespace authority is diluted into weak attestation | Keep `required_author_attestation` separate from `required_authority_assurance`; announcements/proposals require authority roots. |
| Subscribe gate is coupled to publish gate | Readers accidentally become writers or vice versa | Keep `agora-publish@v1` and `agora-subscribe@v1` separate profiles. |
| Topic ACL says yes but authority resolver says no | Confusing operator behavior | Expose both decisions in diagnostics: `topic_acl=allow`, `authority=deny`. |

## Open Questions

1. What is the canonical schema name for authority root configuration:
   `agora-authority-roots.v1`, `agora-authority-policy.v1`, or a wider
   node policy schema section?
2. What is the first non-MVP organization custody policy:
   threshold signatures, multiple custodian signatures, council attestation, or
   an external org policy artifact?
3. Which record kinds are authoritative in `ai.orbiplex/**` by default:
   `announcement`, `proposal`, namespace-policy records, and what else?
4. Should subscribe grants be required for public query APIs, or only for
   non-public topics and high-volume replay/SSE?
5. What is the exact minimum participation threshold name: `phone-confirmed`,
   `phone-verified`, `IAL1`, or a capability-passport profile over
   Proposal 041's attestation-gate?

Resolved for the reference implementation:

- `agora-publish@v1` and `agora-subscribe@v1` live in the
  `capability-binding` built-in registry so every host dispatch gate uses the
  same profile engine.

## Next Actions

1. Define `agora-authority-roots.v1` or an equivalent config section schema.
2. Add an authority resolver that supports direct participant roots and MVP
   `org/custodian-ref`.
3. Extend the Agora HTTP authorization path to report topic ACL, profile, and
   authority decisions separately.
4. Add a test profile where `ai.orbiplex/**` accepts only a configured
   highest-attestation authority root or its scoped delegated operational key
   for `announcement` and `proposal`.
5. Add a participation test profile where `comment` and `opinion` accept
   authors with at least phone-confirmed attestation.
