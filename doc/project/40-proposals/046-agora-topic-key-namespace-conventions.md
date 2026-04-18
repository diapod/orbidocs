# Proposal 046: Agora Topic-Key Namespace Conventions

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/032-key-delegation-and-capability-chain.md`
- `doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/50-requirements/requirements-014.md`

## Status

Accepted

## Date

2026-04-18

## Executive Summary

Agora substrate (proposal 035) treats `topic/key` as an **opaque**
UTF-8 string on purpose: the substrate MUST NOT parse it, split it,
or attach semantics to any prefix or suffix. That invariant stays.

However, the absence of any agreed convention above the substrate
has produced three concrete hazards:

1. **Collision** — two independent applications that both pick
   `announcements` or `status-feed` silently share a topic.
2. **Squatting** — on a shared (multi-tenant) relay, anyone can
   post to `orbiplex/proposals/035` or to another participant's
   informal topic, because no mechanism binds a topic to an owner.
3. **Leakage** — a node that runs an Agora relay for other nodes
   has no syntactic way to separate *topics meant to federate* from
   *topics that must stay local* or *topics that must never go
   through Agora at all* (e.g. `private-correlation` whispers).

This proposal freezes a **conventional** topic-key namespace scheme
that higher layers (relay operators, authoring clients, node outbound
policy, UIs, analytics) MAY and SHOULD enforce. The substrate
contract from 035 is unchanged; all enforcement lives in relay
policy and author-side hygiene.

The scheme has six named classes (plus an "ad-hoc / unscoped"
residue), a one-compare discriminator for the Orbiplex core
namespace (`ai.orbiplex.`), and five cheap relay ingest checks that
turn prefix shapes into cryptographic ownership without touching the
substrate.

## Context and Problem Statement

### What the substrate gives us

Proposal 035 §1.1 states that `topic/key`:

- is opaque,
- is canonicalized (NFC, printable, length bound, no leading/trailing
  whitespace, non-empty),
- carries no substrate-level ownership,
- MAY be constrained by *kind contracts* but never by the substrate
  itself.

That is the right invariant for the substrate — topics are an
application concept, not a substrate primitive.

### What is scattered across proposals today

Different proposals already assume conventions and none of them
cross-reference each other:

| Proposal | Convention used | Shape |
|---|---|---|
| 013 (Whisper) | `whispers/<topic-class>` | flat |
| 026 (Resource opinions) | `opinions/<resource-kind>[/<resource-hash>]` | two-level |
| 035 (examples) | `orbiplex/proposals/<id>`, `orbiplex/announcements`, `orbiplex/workflow-runs/<id>` | project-scoped |
| 041 (Ingest attestation) | `opinions/*` glob matcher in policy | — |
| 042 (INAC) | topic identity is envelope-internal | — |

None of these conventions carry an ownership signal. None of them
syntactically distinguishes "Orbiplex-defined" from "this node's
private feed" from "a topic an external participant posted under
their own identity".

### What breaks without a standard

- A node that runs a **public** Agora relay cannot mechanically
  reject local-only topics at ingress — the only defense is
  manually-curated ACLs per topic.
- A participant has no way to stake a cryptographic claim on "this
  topic is mine"; first-post-wins is policy, not protocol.
- `disclosure/scope: private-correlation` whispers (proposal 013,
  hardened by proposal 042) have no syntactic marker on the topic
  key that would let a relay reject them wholesale.
- Client code that wants to show "this is a substrate announcement"
  vs "this is user content" has to match many ad-hoc prefixes.

## Goals

1. Provide a **stratified** topic-key namespace convention that
   covers all four axes we actually care about: core-vs-app,
   owner-vs-shared, federation-public-vs-local, Agora-eligible-vs-not.
2. Keep the substrate (035 §1.1) opaque and unchanged.
3. Turn prefix shapes into cryptographic ownership by way of
   relay-policy checks grounded in proposals 024, 032 and 034.
4. Provide a **one-compare** test for "is this a built-in Orbiplex
   topic" that does not require parsing.
5. Define a migration path for the informal conventions already in
   use (013, 026, 035 examples, 041 glob).

## Non-Goals

- Changing the substrate contract from 035 §1.1. `topic/key`
  remains opaque.
- Defining content-body schemas for the topics themselves. Each
  topic class is still free to carry any `record/kind` +
  `content/schema` combination that kind contracts allow.
- Enforcing a global uniqueness registry. Even under the scheme,
  two nodes can legitimately both publish to their own
  `participant:<pid>/<app>/announcements`; no central authority
  adjudicates.
- Specifying Agora-to-non-Agora bridging rules. Keys that live in
  `private/…` are by definition not Agora's concern (proposal 042).

## Decision

### 1. Topic-Key Classes

All recommended topic keys match one of the following six prefix
shapes. Anything that does not match is **unscoped / ad-hoc** and
carries no ownership, no collision protection, and no routing
guarantee.

#### 1.1. `ai.orbiplex.<subsystem>/<name>` — Orbiplex core

Reserved for topics whose definition belongs to the Orbiplex
project (proposals, substrate-wide announcements, shared kind
contracts such as `opinions` and `whispers`, workflow run feeds,
threshold notifications).

- The prefix is reverse-DNS under the project identity
  `orbiplex.ai`, using dot-joined segments to keep the prefix a
  single non-slashed token that the one-compare discriminator can
  match in constant time.
- `<subsystem>` names the Orbiplex subsystem (`proposals`,
  `announcements`, `workflow-runs`, `whispers`, `opinions`,
  `threshold`, …). Subsystem names are introduced by the proposal
  that defines them; this document does not enumerate them.
- `<name>` is the topic name inside the subsystem, and MAY contain
  further `/` segments at the subsystem contract's discretion (for
  example `ai.orbiplex.proposals/035`,
  `ai.orbiplex.workflow-runs/<run-id>`,
  `ai.orbiplex.opinions/url/sha256:4b7c…`).

Relay enforcement (optional, deployment-dependent):

- default: honor-convention only (no enforcement),
- hardened deployments MAY require that ingest into
  `ai.orbiplex.…` carries a delegation proof anchored in the
  Orbiplex project identity (proposal 032). This is *future work*;
  no such delegation chain exists today.

#### 1.2. `participant:<participant-id>/<app>/<name>` — Participant-owned

A topic that a single participant stakes as theirs.

- `<participant-id>` MUST be the full participant identity string
  (`participant:did:key:…`), percent-encoded where needed.
- `<app>` is an author-chosen application label
  (`journal`, `status`, `diary`, `announcements`, …).
- `<name>` is the topic name inside that app; MAY contain further
  `/` segments.

Relay enforcement (REQUIRED for conformance to this convention):

- ingest MUST reject the record unless
  `record.author/participant-id` equals `<participant-id>` decoded
  from the prefix, OR the record carries a valid
  `key/delegation` chain (proposal 032) whose root resolves to
  `<participant-id>`.

This is the primary mechanism for squat-resistance without a
central registry: the topic namespace bakes in the owner's DID,
and the relay turns that into a cryptographic check at ingest.

#### 1.3. `node:<node-id>/<name>` — Node-owned

A topic owned by a specific node (node status feeds, capability
catalog snapshots, node-operator announcements).

- `<node-id>` MUST be the canonical node identity string.
- `<name>` as above.

Relay enforcement (REQUIRED):

- ingest MUST reject the record unless the signing key chain
  resolves to `<node-id>` through proposal 034 node-operator
  binding (node key, or key delegated by node operator).

#### 1.4. `federation:<federation-id>/<name>` — Federation-scoped

A topic shared within a named federation (a cooperative, a
project's working group, an intranet).

- `<federation-id>` MUST be a stable identifier minted by the
  federation and resolvable to a federation identity document.
- Relay enforcement is **federation policy**: the federation's
  own ingest attestation ruleset (proposal 041) decides who can
  post. The substrate does not adjudicate.

#### 1.5. `local/<name>` — Node-local, never-federated

A topic that MUST NOT leave the authoring node.

- Used for in-node buffers, debug feeds, local dashboards, and any
  material whose disclosure scope is strictly local.

Enforcement (REQUIRED on both ends):

- Author-side: the node's outbound policy MUST refuse to publish
  any record with a `local/…` topic key to any relay that is not
  the node's own in-process Agora instance.
- Relay-side: a multi-tenant / public Agora relay MUST reject
  ingest of any record whose topic key starts with `local/`.
- A relay running strictly intra-node (single-tenant, not
  federated) MAY accept `local/…` keys; this is the only case
  where they are legitimate.

#### 1.6. `private/<name>` — Direct-only (INAC), never via Agora

A topic whose envelope is routed strictly through the Inter-Node
Artifact Channel (proposal 042). Agora is not a carrier for this
namespace at all.

- Used for `disclosure/scope: private-correlation` whispers and
  any other artifact whose distribution model is direct
  node-to-node only.
- The prefix exists so that an envelope accidentally routed to
  Agora can be rejected by a single syntactic check.

Enforcement (REQUIRED):

- Any Agora relay (intra-node or federated) MUST reject ingest of
  any record whose topic key starts with `private/`.
- INAC implementations do not need the prefix for routing (the
  envelope is addressed by `record/about` and peer-message kind,
  not by `topic/key`), but carrying the `private/…` topic key in
  the envelope lets any accidental Agora path fail fast.

#### 1.7. Unscoped / ad-hoc

Anything that does not match §1.1–§1.6.

- No ownership. No squat resistance. No disclosure guarantee. Two
  nodes both picking `hello` share a topic.
- Legitimate for throwaway experiments, local demos, and topics
  whose disclosure model is explicitly "public free-for-all".
- SHOULD NOT be used for any production-facing surface.

### 2. One-Compare Core Discriminator

A higher layer MAY determine that a topic key belongs to the
Orbiplex core namespace by a single prefix test:

```
is_orbiplex_core(k) := starts_with(k, "ai.orbiplex.")
```

No parsing, no splitting, no structural inspection. This is
deliberately cheap and is the only parsing-like operation this
proposal requires anyone to perform on a topic key. The substrate
still does not perform it; application layers do.

### 3. Relay Ingest Policy — Five Cheap Checks

These checks are a **single pure module** living in
`node/agora-relay-trait` (the layer that owns the relay-facing
contracts and knows nothing about storage or transport). They are
exposed as one function
`(topic_key, author_identity, relay_posture) → Decision` — no I/O,
no backend assumptions. Concrete relays (`agora-relay-sqlite`,
`agora-relay-matrix`, any future backend) and the `agora-service`
binary MUST call into that module and MUST NOT reimplement the
checks locally; duplicating them per backend would re-introduce
exactly the divergence this proposal eliminates. `agora-core`
continues to treat `topic/key` as opaque per proposal 035 §1.1 and
does not import the namespace policy at all.

A relay implementing this convention runs the following checks on
every ingest, in order; the first matching rule decides:

1. If `topic/key` starts with `private/` → **reject** (code
   `topic-namespace/private-not-on-agora`).
2. If `topic/key` starts with `local/` and the relay is multi-
   tenant or federated → **reject** (code
   `topic-namespace/local-not-federated`).
3. If `topic/key` starts with `participant:<X>/` →
   **reject unless** the signing chain resolves to `<X>`
   (proposals 024/032); on mismatch code
   `topic-namespace/owner-mismatch`.
4. If `topic/key` starts with `node:<X>/` →
   **reject unless** the signing chain resolves to `<X>` via
   proposal 034; on mismatch same code as above.
   The current reference relay is intentionally fail-closed for
   `node:<X>/...` until the proposal 034 node-binding verifier is
   wired into this policy.
5. If `topic/key` starts with `ai.orbiplex.` → apply the
   deployment's Orbiplex-core policy (default: accept; hardened:
   require Orbiplex-project delegation once that chain exists).

All five checks read `topic/key` as a byte-prefix; none of them
parse the key into structured fields beyond the leading token.
Proposal 041's attestation policy matchers (`topic_match`) are
orthogonal and run on top of these namespace checks.

### 4. Relationship to Proposal 041 (Ingest Attestation)

041 matches topics with globs (`opinions/*`) to decide which
attestation tier an ingest requires. After this proposal lands,
041 policies SHOULD be rewritten against the `ai.orbiplex.`
namespace (e.g. `ai.orbiplex.opinions/*`), and 041 globs MAY
additionally match the ownership prefixes (`participant:*/*`,
`node:*/*`, `federation:*/*`) to apply tier policy per class.

The §3 namespace checks run **before** 041's attestation tiering.
A record that fails a §3 check is rejected before any attestation
proof is consulted.

### 5. Authoring-Side Hygiene

Clients constructing `agora-record.v1` envelopes SHOULD:

1. Pick the narrowest namespace class that fits their use case.
2. Never hand-write `participant:<pid>/…` or `node:<node-id>/…`
   prefixes — the node's outbound path should synthesize them
   from the active participant or node identity, so that the
   signing chain and the prefix cannot drift.
3. Refuse to publish any record whose topic key starts with
   `local/` or `private/` to any outbound surface other than the
   one that class permits (intra-node relay for `local/`, INAC
   for `private/`).
4. When a record's `disclosure/scope` is `private-correlation`,
   enforce the `private/…` prefix at construction time. This
   converts a policy error into a schema-level error.

## Migration of Existing Conventions

| Today | After migration |
|---|---|
| `orbiplex/proposals/<id>` | `ai.orbiplex.proposals/<id>` |
| `orbiplex/announcements` | `ai.orbiplex.announcements/default` |
| `orbiplex/workflow-runs/<id>` | `ai.orbiplex.workflow-runs/<id>` |
| `opinions/<resource-kind>` | `ai.orbiplex.opinions/<resource-kind>` |
| `opinions/url/sha256:…` | `ai.orbiplex.opinions/url/sha256:…` |
| `whispers/<topic-class>` | `ai.orbiplex.whispers/<topic-class>` |

Updates needed:

- Proposal 013 §Distribution and Next Actions — swap
  `whispers/<topic-class>` for `ai.orbiplex.whispers/<topic-class>`
  and add `private/…` prefix requirement for
  `disclosure/scope: private-correlation` whispers.
- Proposal 026 — swap `opinions/<…>` examples for
  `ai.orbiplex.opinions/<…>`.
- Proposal 035 §1.1 — add a one-paragraph non-normative pointer
  to this proposal under "applications choose their own topic-key
  conventions"; the opaque substrate invariant remains unchanged.
- Proposal 041 — note that `topic_match` globs SHOULD target the
  new `ai.orbiplex.*` shape and MAY additionally key off ownership
  prefixes.

Authors who have already published records under the legacy
informal prefixes continue to be verifiable (the envelope bytes are
unchanged); only new publications adopt the new shape. A migration
period where both shapes coexist is acceptable; relays MAY alias
legacy keys to their new counterparts at the query layer, but MUST
NOT rewrite stored envelopes (that would break `record/id`).

## Trade-offs

- **Cryptographic ownership without central registry**: the
  `participant:<pid>/…` and `node:<node-id>/…` classes bake the
  owner's identity into the key, so a relay can adjudicate by
  signature alone. Cost: long, unwieldy topic keys. Benefit:
  zero-coordination squat resistance.
- **Opaque substrate preserved**: the substrate still does not
  parse topic keys. All structure lives in policy. Cost: compliance
  is a relay-deployment property, not a protocol property. Benefit:
  the substrate keeps its minimum-trusted-core posture from 035.
- **One-compare discriminator**: `ai.orbiplex.` is cheap to match
  and hard to collide with. Cost: the Orbiplex project commits to
  not introducing Orbiplex-defined topics outside this prefix.
- **Six classes is more than strictly needed**: we could collapse
  `participant:` and `node:` into one class, but they have
  different signing-chain resolution rules (024/032 vs 034), so
  keeping them apart matches the enforcement primitive.

## Open Questions

1. Should `federation:<federation-id>/…` require that
   `<federation-id>` be content-addressed (e.g. a hash over the
   federation identity document) to prevent rebinding, or is a
   human-readable identifier + a separate ledger entry enough?
2. When a participant rotates keys (proposal 032), does their
   existing `participant:<old-pid>/…` topic remain owned, or does
   rotation produce a new namespace? Likely answer: the old
   namespace remains owned by the rotation chain, and the relay
   follows the chain at ingest — but this should be stated
   normatively once 032 lands.
3. Should `local/` and `private/` be accompanied by a machine-
   readable discovery document (e.g. a capability at the node
   level) that declares *which* `local/` and `private/` topics
   exist, so that UI can list them? Out of scope for this
   proposal; tracked as a future extension.
4. Is there value in a further `anonymous:<nym>/…` class for
   pseudonymous identities whose rotation is faster than regular
   participant identities (proposals 013, 015)? Current thinking:
   no — pseudonymous identities still fit under
   `participant:<nym-pid>/…` because `nym:did:key:…` is itself a
   valid participant id form.
5. Should the Orbiplex-core policy ever require a delegation
   chain (see §1.1), or is honor-convention always sufficient
   given that the namespace is visible to all participants and
   misuse can be publicly opined-upon via proposals 013/026?

## Next Actions

1. [done] Land this proposal.
2. [done] Add a one-paragraph non-normative pointer from proposal 035
   §1.1 to this proposal.
3. [done] Update proposals 013, 026, 041 per the Migration table.
4. [done] Update the topic-key examples in
   `doc/schemas/examples/*.agora-record.json` to use
   `ai.orbiplex.*` prefixes.
5. [done] Implement the §3 five-check ingest policy as a **pure module
   in `node/agora-relay-trait`** — a function of
   `(topic_key, author_identity, relay_posture) → Decision` with
   no dependency on storage, transport, or HTTP. Concrete relays
   (`agora-relay-sqlite`, `agora-relay-matrix`) and the
   `agora-service` binary consume it without reaching upward;
   `agora-core` continues to treat `topic/key` as opaque per
   proposal 035 §1.1. Gate enforcement behind a per-relay config
   flag `enforce_topic_namespace` that defaults to `true` for
   multi-tenant deployments and `false` for strictly intra-node
   relays.
6. [done] Add a small authoring helper to the node's outbound path that
   synthesizes `participant:<pid>/…` and `node:<node-id>/…`
   prefixes from the active identity, so client code never types
   them by hand.
7. [done] Document the `private/…` prefix requirement in proposal 042
   §Artifact shapes and in the whisper-signal envelope builder
   (proposal 013 impl doc) so that `disclosure/scope:
   private-correlation` always materializes with the prefix.
