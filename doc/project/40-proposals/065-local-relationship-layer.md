# Proposal 065: Local Relationship Layer

Based on:
- `doc/project/20-memos/operator-participation-in-answer-channel.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/043-node-address-attestation-fallback.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/40-proposals/061-contact-attestation-service.md`
- `doc/project/40-proposals/062-temporal-storage-convention.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`
- `doc/project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md`
- `doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`

## Status

Accepted

## Date

2026-05-19

## Promoted to

`doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

This proposal records rationale and decision history. The canonical
implementation guidance now lives in the promoted solution document.

## Executive Summary

Today the concept "who is this person to me" is implicitly co-owned by three
subsystems: Messaging defines what a `contact` is, Artifact Delivery has
opinions about `friends` as a privileged delivery group, and Contact Catalog
holds both public route discovery and some local annotation. This is
splątanie: each subsystem grew a partial model of personal relationship state,
and changes in one ripple into the others through implicit shared assumptions.

This proposal introduces **Local Relationship Layer** as a host-owned,
vault-backed source of truth for the user's private relationship state:
relationship classes (`contacts`, `friends`, namespaced custom classes),
membership facts, status transitions, and pairwise nym continuity per
context. Messaging, Artifact Delivery, and Contact Catalog become
**consumers** of this layer; none of them owns the concept anymore.

The architectural rule is:

> A relationship class label classifies a peer. It is never, by itself, a
> grant of authority. Capability grants are issued through capabilities and
> passports; membership may inform policy that decides to issue them, but
> membership alone authorizes nothing.

The first iteration introduces the layer as a local host-owned component
behind daemon-internal API (no new public host capability), with vault
snapshot as recovery source of truth and a per-store SQLite projection per
Proposal 028 convention.

## Context and Problem Statement

The current state has three overlapping models of personal relationship:

1. **Messaging** previously owned the `contact` concept end to end. Before
   first release this legacy ownership was removed: membership in the
   `contacts` set is now represented only by Local Relationship membership
   facts.
2. **Artifact Delivery** documents `friends` as one of the recipient
   selector resolver targets. AD does not define what `friends` is, but it
   expects somebody to define it; in practice this leaked back into
   Messaging conventions.
3. **Contact Catalog** publishes route-sets and discovery handles; some
   local annotation (label, last-seen, trust) accreted onto it.

Several concrete consequences follow:

- Adding a custom relationship class (e.g. `book-club`) has no single home.
  Messaging would have to extend its contact concept; AD would have to know
  the new label; Contact Catalog might also need a copy.
- "Block this person" has two implementations: a Messaging-level block and
  an AD-level group exclusion. They drift.
- `pairwise nym continuity` (the fact that "Alice in this conversation" is
  the same Alice over time, even across nym rotation) has no canonical
  home. Each consumer reasons about it locally.
- The Pseudonym Vault (Proposal 026) holds nym seeds and routing-subject
  seeds, but the personal data *about* peers (annotations, membership,
  relationship state) is currently outside the vault, scattered across
  subsystem-specific stores.

Cross-cutting changes (privacy class taxonomy, retention horizon per
relationship class, operator UI for relationship management) cannot be
made coherently because there is no layer to make them in.

## Proposed Model / Decision

Introduce a **Local Relationship Layer** as a node-local, host-owned
component with the following responsibilities:

- own the canonical schema set for relationship classes, membership facts,
  and pairwise nym bindings;
- persist the canonical state inside the Pseudonym Vault as a sealed
  inner-entry kind (`local-relationship`);
- expose a daemon-internal API for class management, membership append,
  membership query, group resolution, and pairwise nym binding management;
- emit canonical Layer 3 facts (`relationship-membership-fact.v1`,
  `pairwise-nym-binding.v1`) for downstream consumers;
- remove legacy Messaging-owned relationship state before first release, so
  no compatibility bridge becomes part of the public contract.

Local Relationship Layer is **not**:

- a public host capability surface (first iteration);
- a peer-to-peer protocol;
- a discovery / lookup catalog (that remains Contact Catalog);
- an authority issuer (capabilities and passports remain authoritative);
- a federated relationship store (relationships are local-only).

### Load-Bearing Invariants

These are non-negotiable. The proposal exists primarily to enforce them.

1. **Label is not authority.** Relationship class membership is never, by
   itself, a grant of capability. Membership may be:
   - an INPUT to a host policy that decides whether to issue a grant;
   - an INPUT to a policy that filters delivery candidates;
   - an INPUT to UI to surface or rank contacts.
   Membership MUST NOT be:
   - a standalone authority to deliver to that contact;
   - a standalone authority to read/write a memarium scope;
   - a bypass of any capability/passport check.

2. **Classes and memberships are separate entities.** A relationship class
   is an operator-defined policy bundle (definition). A membership is an
   append-only fact saying "contact X is in class Y with status Z as of
   transaction T". Conflating them produces undefined semantics when a
   class is archived or modified.

3. **Membership facts are strictly local-emitted.** There is no
   wire-shape inbound for `relationship-membership-fact.v1`. A peer cannot
   push a membership into my relationship layer. Other subsystems
   (Messaging accept, AD authorize) may *trigger* local emission, but the
   fact is always produced locally with an `actor/ref` of a host-issued
   operator binding.

4. **Canonical state lives in the Pseudonym Vault.** No relationship
   state escapes the vault as plaintext on disk. The SQLite projection is
   a recoverable cache, never authority.

5. **Reserved class IDs and mandatory namespace.** Four reserved
   well-known IDs form a PGP-style trust gradation: `untrusted`,
   `contacts`, `friends`, `trusted`. Each ships with seeded default
   policy semantics. All other classes MUST be namespaced
   (`vendor.example/...`, `operator-local/...`, etc.). A definition
   collision on a reserved or namespaced ID fails the readiness gate at
   daemon start; classes are not silently merged.

   Custom namespaced classes that visually shadow a reserved name (e.g.
   `vendor.x/trusted`) are allowed — namespace makes the distinction
   explicit; `is_reserved_class_id` returns `false` for namespaced
   variants. UI displays the full `class/id` to avoid confusion.

   **`blocked` is intentionally NOT a reserved class.** Block semantics
   are a *status* on existing memberships (`status = blocked` on a
   membership fact in any class) or a separate `operator-local/blocklist`
   policy input — never a relationship class equivalent in standing to
   the four tiers. Mixing block as both class and status would recreate
   the relationship-state ≠ relationship-class confusion this layer was
   built to eliminate.

   **Reserved classes cannot be archived.** Operator may promote/demote
   memberships across the four reserved tiers, but
   `archive_class(<reserved>)` returns `cannot-archive-reserved-class`.
   This guarantees recovery from any vault snapshot lands in a
   consistent state where all four reserved classes exist with their
   seeded definitions.

6. **Classes are archived, never deleted.** When a non-reserved class is
   retired, its membership facts remain in the event log per Proposal
   062 retention. The class transitions to `archived` and is excluded
   from active resolver results. Reserved classes are exempt per
   invariant 5.

7. **Class definitions are mutable projection; every change emits a
   fact.** The `current class definition` is a mutable projection
   (operator UI shows the current set of policies and labels), but every
   class create / update / archive transition emits a
   `relationship-class-changed.v1` fact into the sealed event log. UX has
   the current view; audit has the full history. This avoids choosing
   between mutable-without-audit (loses history) and append-only-only
   (forces UI to fold over fact log on every read).

8. **Relationship membership may inform autonomous host policy, but
   never becomes node-node authority by itself.** This is the strongest
   boundary in this proposal. Participant-participant relationship trust
   is not automatically inherited by nodes claiming to act on behalf of
   those participants. A claim "I am Alice's node" is data, not
   authority; participant-to-node binding requires explicit, verifiable
   evidence (Seed Directory entries, node-operator-binding passports,
   node-address attestations, capability advertisements). Only after
   such evidence is present, may relationship membership be used as one
   input among several to a *local policy decision* for a *specific
   action kind*, with *bounded effects*.

   Relationship-derived node trust requires all of:
   1. local relationship membership (e.g. `participant:Alice ∈ friends`);
   2. subject-to-node evidence (e.g. verified `node-operator-binding.v1`
      stating `node:B` is operated by `participant:Alice`);
   3. explicit local policy declaration for the action kind
      (`relationship-policy-predicate.v1`);
   4. normal capability / passport / admission checks;
   5. bounded effects: quota, TTL, target space, artifact schema, crisis
      mode.

   This is **local political projection**, never **trust propagation**.
   The host autonomously interprets a participant-level relationship as
   permission for a specific node-level action; this interpretation is
   never automatic, never transitive, and never replaces capability
   checks.

### Schemas

Four new contracts plus one revised:

#### `relationship-class.v1` (new)

Definition of a relationship class. Operator config, not a fact.

```text
relationship-class.v1
  schema = "relationship-class.v1"
  class/id                # "contacts" | "friends" | namespaced "vendor.example/book-club"
  class/state             # "active" | "archived"
  display/label           # operator-facing label
  description?
  default-status          # default status when membership is appended without explicit status, typically "active"
  grant-policy/default-allowlist[]?    # capabilities the host policy MAY grant to members; never automatic
  grant-policy/suggested-defaults[]?   # capabilities the host policy SUGGESTS but operator must confirm
  grant-allowlist[]?      # capabilities the operator may grant to members of this class (operator action required)
  verification/required?  # what proof is required before membership transitions to active
  privacy/profile         # "sealed-only" | "operator-visible-summary" | "public-aggregate" (defaults to sealed-only)
  retention/profile-ref?  # reference to retention profile from Proposal 028 (defaults to host default)
  policy/refs[]?          # additional policy references this class participates in
```

#### `relationship-class-changed.v1` (new — append-only event)

Records every transition of a class definition: create, update, archive,
and unarchive. Archive/unarchive are reversible operational lifecycle
transitions, not deletion. Both require an explicit `reason/code`; archive
captures only `prior/definition`, while unarchive captures both prior and
next definition snapshots.
The current `relationship-class.v1` is the mutable projection over this
event log.

```text
relationship-class-changed.v1
  schema = "relationship-class-changed.v1"
  fact/id
  class/id
  transition              # "created" | "updated" | "archived" | "unarchived"
  prior/definition?       # full prior class definition snapshot (for updates/archives/unarchives)
  next/definition?        # full next class definition snapshot (for creates/updates/unarchives; absent for archives)
  actor/ref               # operator binding id
  event/at                # RFC3339
  reason/code?            # required for archived/unarchived
  reason/note?
  tx/id                   # transaction id per Proposal 028
```

#### `relationship-membership-fact.v1` (new)

Append-only fact: a membership state transition.

```text
relationship-membership-fact.v1
  schema = "relationship-membership-fact.v1"
  fact/id                 # ULID, monotonic per store
  owner/ref               # operator binding or local participant whose private
                          #   relationship space this fact belongs to; default for
                          #   single-operator nodes is the node primary operator binding
  contact/ref             # reference to local-contact.v1 record
  class/id                # class membership applies to
  status                  # "active" | "pending-outgoing" | "pending-incoming" | "blocked" | "revoked"
  actor/ref               # operator binding id that performed this transition
  event/at                # RFC3339, wall-clock at commit; consistent naming across all facts in this layer
  tx/id                   # transaction id per Proposal 028
  supersedes/fact-id?     # projection hint: the prior membership fact this one supersedes for (owner, contact, class) tuple.
                          #   Hint only — the prior fact is NEVER deleted; both remain in the event log forever.
  reason/code?            # closed enum; "user-action" | "messaging-accept" | "messaging-block" | "ad-authorize" | "migration-bootstrap" | "operator-import" | …
  reason/note?            # free-form, sealed-only
  context/ref?            # which subsystem triggered the change (messaging/ad/operator-ui)
```

`owner/ref` answers "whose relationship is this?" — essential on
multi-operator nodes where Paweł's `friends` and Alicja's `friends` are
distinct relationship spaces. Membership lookups are scoped by
`(owner/ref, contact/ref, class/id)`. Single-operator nodes default
`owner/ref` to the node primary operator binding, so the field is set
even when not visibly distinguishing.

#### `pairwise-nym-binding-fact.v1` (new — append-only event)

Per-contact, per-context observed event: a nym was first observed, rotated
into, or retired from a context. Append-only, never mutated.

```text
pairwise-nym-binding-fact.v1
  schema = "pairwise-nym-binding-fact.v1"
  fact/id
  contact/ref             # which contact this fact is about
  context/kind            # "messaging" | "ad-direct" | "agora-topic" | "inquirium-session" | …
  context/ref?            # optional finer context (session id, topic id)
  event/kind              # "observed" | "rotated-into" | "retired"
  nym/value               # the nym observed/rotated-into/retired in this event
  prior/nym?              # for "rotated-into", the prior nym now retired
  event/at                # RFC3339 wall-clock observation timestamp
  detected/by             # subsystem that emitted this fact (messaging/ad/operator)
  evidence/ref?           # optional reference to evidence proving continuity (e.g. session transcript hash)
  tx/id                   # transaction id per Proposal 028
```

#### `pairwise-nym-binding.v1` (new — current projection)

Sealed projection of the latest known nym binding state for a contact in
a context. Reducer over `pairwise-nym-binding-fact.v1` events.

```text
pairwise-nym-binding.v1
  schema = "pairwise-nym-binding.v1"
  contact/ref
  context/kind
  context/ref?
  nym/current             # the active nym; null if context is currently dormant
  nym/history[]           # ordered list of prior bindings, derived from facts
    {nym, observed-at, retired-at?, retired-by-fact-id?}
  as-of-tx/id             # transaction id of the latest fact applied
```

The split mirrors Solution 028: facts are append-only and authoritative;
the projection is the rebuilt-from-facts read model. Operator UI shows
the projection; audit and forensics read facts. History never mutates
in-place.

#### `relationship-policy-predicate.v1` (new — declarative policy requirement)

Declarative requirement attached to an action kind. Middleware packages,
acceptors, and operator-defined policies declare predicates; the host
evaluates them at decision time. Predicates are *not* facts — they are
*conditions* the host evaluates against current state.

```text
relationship-policy-predicate.v1
  schema = "relationship-policy-predicate.v1"
  predicate/id
  predicate/kind            # "operator-relationship-class" | future kinds
  local/operator-ref?       # whose relationship space to evaluate; defaults to current node primary operator
  remote/operator-binding-ref  # how to identify the remote operator (verified node-operator-binding.v1)
  required/class-ids        # non-empty set: "contacts" | "friends" | "trusted" | namespaced classes
  required/status           # "active" by default
  action/kind               # "artifact.custody.accept" | "crisis.assist" | "gossip.accept" | …
  effect/scope              # bounded scope identifier; never "any"
  ttl?                      # optional bound on decision validity
  failure/mode              # "deny" | "require-operator" | "quarantine"
  declared/by               # middleware package id or "operator-local"
```

`effect/scope` is mandatory. A predicate must always be paired with a
*specific bounded effect*, never with general authority. "Friends may
accept custody" is incomplete; "friends may accept custody under scope
`artifact.custody:short-ttl`" is a complete predicate.

#### `relationship-policy-candidate.v1` (new — host-internal read model)

Outcome shape produced by the host policy evaluator when scanning for
matches to a predicate. Used for diagnostics, audit trail, AD candidate
ranking, operator UI explanation. A candidate is *eligibility input*,
never *authority*.

```text
relationship-policy-candidate.v1
  schema = "relationship-policy-candidate.v1"
  candidate/id
  predicate/ref
  contact/ref
  class/id
  relationship/fact-id      # the specific membership fact backing this candidate
  local/operator-ref
  remote/operator-ref?
  participant/ref?
  node/ref?
  node-operator-binding/ref?  # the verified binding tying remote operator to remote node
  evidence/ref[]            # additional evidence (passports, attestations) considered
  action/kind
  policy/ref
  candidate/effects[]       # what effects would be permissible under this candidate; NEVER "granted"
  limits                    # quota, ttl, target space, artifact schema bounds
  valid/until
  decision/hint             # "eligible" | "quarantine" | "deny" — non-binding hint
  as-of-tx/id
```

Naming choice: `candidate/effects[]` (not `allowed/effects[]`) makes
clear this is a description of *what would be permissible*, not a
grant. Only a `relationship-policy-decision.v1` (below) finalizes a
specific allow/deny.

#### `relationship-policy-decision.v1` (new — host decision outcome)

The host's bound decision for a concrete action. Recorded for audit;
returned to middleware as the answer to its declared
`trust_requirements`.

```text
relationship-policy-decision.v1
  schema = "relationship-policy-decision.v1"
  decision/id
  predicate/ref
  candidate/ref?            # candidate the decision is based on; null when no candidate matched
  decision                  # "allow" | "deny" | "quarantine" | "require-operator"
  reason/code               # closed enum
  action/kind
  effect/scope
  evidence/ref[]            # redacted refs sufficient for audit
  valid/until
  decided/by                # daemon component that evaluated the predicate
  decided/at
  tx/id
```

Middleware receives the decision shape directly. It never receives the
candidate object, the membership fact, or any other sealed relationship
state.

Three-tier separation:

| Concept | Role |
| --- | --- |
| **Predicate** | Declarative *condition* requested by middleware/policy. |
| **Candidate** | Host-internal *eligibility input* assembled from membership + binding + evidence. |
| **Decision** | Host-bound *outcome* (allow/deny/quarantine) returned to middleware. |

This matches the `label != authority` invariant: candidate means "may be
basis for decision"; decision means "host has bound a specific effect";
real authority still flows through capability/passport/admission.

#### `local-contact.v1` (revised — ownership note only)

The existing schema is preserved for backward compatibility. Its
documentation is updated to make the split explicit:

> Local Contact Store owns private contact records: raw handles, labels,
> UX metadata, and contact-continuity annotations.
> Local Relationship Layer owns relationship classes, membership facts,
> relationship policy predicates, and pairwise relationship facts.

That split keeps address-book material and relationship-policy material
adjacent but not conflated.

#### `pseudonym-vault.v1` (extended additively)

Add `local-relationship` to the accepted plaintext inner-entry kinds.
Outer artifact remains ciphertext-only per Proposal 026.

Forward-compat contract for unknown inner-entry kinds:

- **Reader** MAY ignore the semantics of an unknown entry kind. It does
  not need to know what the entry means.
- **Importer / resealer** MUST preserve unknown entries verbatim when
  resealing the vault. Silent dropping of unknown entries during reseal
  is data loss; this is forbidden.
- **Critical-flag escape hatch.** An entry may carry `critical = true`
  (default false). A reader that cannot interpret a `critical = true`
  entry MUST fail closed rather than proceed with partial understanding.
- **Integrity violations** (broken AEAD, tampered envelope) always fail
  closed regardless of `critical` flag.

"Ignore" without "preserve" is a silent data-loss mechanism at recovery
time. This contract makes "ignore" safe by guaranteeing roundtrip
preservation.

### Storage Architecture

Three layers with explicit authority order:

1. **Canonical truth: sealed event log + latest sealed snapshot.** The
   append-only sealed event log carries every relationship transition
   since the previous checkpoint. The latest sealed snapshot captures
   the projection state at a known transaction. Together, log + most
   recent snapshot are the authoritative reconstruction source. Both
   live as inner entries of a Pseudonym Vault sealed blob.

2. **Checkpoint accelerator: sealed snapshot alone.** A fresh snapshot
   lets recovery skip log replay before its `tx/id` cutoff. Snapshot is
   *not* an alternate authority — discarding the snapshot but keeping
   the event log is recoverable; the inverse is not. This ordering is
   non-negotiable.

3. **Rebuildable projection: SQLite under
   `<data-dir>/storage/local-relationships.sqlite`** per Solution 028
   three-table shape (`relationship_transactions`,
   `relationship_events`, `relationship_current`). The projection is
   never an authority and may be deleted at any time; daemon restart
   rebuilds it from snapshot + event log.

#### Privacy boundary in the SQLite projection

The invariant *no relationship state escapes the vault as plaintext on
disk* applies in full. The SQLite projection MUST NOT store plaintext
relationship data. Three permitted shapes:

| Mode | Content | When |
| --- | --- | --- |
| Encrypted-at-rest | Cell-level AEAD with per-store key derived from vault | First-iteration target |
| Opaque references only | Column data = vault-internal opaque ref + `tx/id`; lookups resolve via vault | Acceptable if cell-level AEAD is deferred |
| Plaintext | Forbidden in target state | Not an accepted Local Relationship projection mode |

The current `local-contacts.sqlite` daemon-side store is **plaintext** and
is treated as a labelled transitional state outside the Local
Relationship projection boundary. The new projection must use encrypted
cells or opaque vault references; there is no legacy plaintext cache mode.

Replay equivalence between event log and projection remains a test gate
per Solution 028. The replay must reproduce projection rows *bit-for-bit*
under same key material; this is part of correctness, not optional.

#### Per-fact write granularity: event log + checkpoint

Each membership transition appends a small sealed event record (single
append + fsync, fast). The vault snapshot is recheckpointed periodically
(every N facts since last snapshot, or T seconds idle, whichever fires
first). This decouples per-fact UI latency from vault seal cost.

Concretely:

```text
write path:
  1. validate request, resolve class/contact refs
  2. append membership event to sealed event log (cheap, single fsync)
  3. update SQLite projection in same transaction (per 028)
  4. emit relationship-membership-fact.v1 to subscribers
  5. schedule vault snapshot recheckpoint if threshold reached

snapshot path (background, throttled):
  1. take consistent read of current projection state
  2. seal as pseudonym-vault.v1 with contents/kinds = "local-relationship"
  3. commit atomically; mark prior snapshot as superseded
```

Snapshot intervals follow performance profile (Solution 028):

| Profile | Recheckpoint after | Recheckpoint idle |
| --- | --- | --- |
| `minimal` | 50 events | 30 s |
| `balanced` | 100 events | 60 s |
| `full-audit` | 25 events | 15 s |

Crash recovery: replay sealed event log forward from last good snapshot
to rebuild projection. Snapshot is correctness checkpoint, not latency
checkpoint.

### Read Models and Redaction Levels

The relationship layer exposes three named read projections, each with a
distinct privacy contract. Consumers must declare which level they need;
the layer refuses to return data above the requested level.

| Level | Content | Consumers |
| --- | --- | --- |
| `sealed-only` | Full record incl. notes, reasons, history | Recovery, audit, operator forensics under explicit grant |
| `operator-visible-summary` | Contact display name, class memberships (active), last-event timestamp; no notes/reasons/history | Operator UI inbox, dashboard |
| `ui-row` | Display name only + opaque contact-ref | Contact list in UI sidebars, AD candidate diagnostic |

The `privacy/profile` field on `relationship-class.v1` (default
`sealed-only`) sets the upper bound for that class. A class with
`privacy/profile = ui-row` cannot expose memberships at higher detail
even to an authorized operator UI without a separate explicit grant.

### Default Class Seeds

The four reserved class IDs ship with default class definitions seeded
at first daemon start. These are **operator-editable defaults**, not
magic constants.

The four reserved classes form a PGP-style trust gradation
(`untrusted < contacts < friends < trusted`), inspired by PGP trust
levels (`unknown < marginal < full < ultimate`). The gradation is
**convention**, not enforced linear ordering: the schema does not
implement "level ≥ X" comparisons. Each predicate explicitly lists the
required class IDs in `required/class-ids[]`. Custom namespaced classes
live alongside the hierarchy.

| Tier | Operator meaning | Verification | Routine actions |
| --- | --- | --- | --- |
| `untrusted` | Known but explicitly distrusted | none | none |
| `contacts` | Known, partial trust | `peer-mutual-accept` | correspondence |
| `friends` | Known, full routine trust | `operator-explicit` | correspondence + routine opt-in |
| `trusted` | Known, ultimate trust | `operator-explicit + secondary-confirmation` | broader scope incl. custody, delegation, governance |

```text
untrusted:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: []                       # nothing auto
  grant-allowlist: []                                       # nothing routine
  verification/required: []                                 # "known and intentionally distrusted"
  privacy/profile: operator-visible-summary

contacts:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: [messaging-receive@v1]
  grant-allowlist: [messaging-receive@v1]                   # correspondence only — intentionally narrow
  verification/required: [peer-mutual-accept]
  privacy/profile: operator-visible-summary

friends:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: [messaging-receive@v1, ad.direct-target]
  grant-allowlist: [messaging-receive@v1, ad.direct-target, agora.private-topic]
  verification/required: [operator-explicit]
  privacy/profile: sealed-only

trusted:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: [messaging-receive@v1, ad.direct-target, agora.private-topic]
  grant-allowlist: [messaging-receive@v1, ad.direct-target, agora.private-topic,
                    memarium.custody-accept, delegation.receive]
  verification/required: [operator-explicit, secondary-confirmation]
  privacy/profile: sealed-only
```

The seed for `untrusted` is the strictest in the gradation: every
action, including `messaging-receive`, requires explicit per-contact
operator grant. This prevents "known and intentionally distrusted" from
functionally collapsing into `contacts`.

The seed for `trusted` requires **two-step verification**:
`operator-explicit + secondary-confirmation`. Concrete realisation of
secondary-confirmation (time-delayed 2-step UI dialog, separate session,
or stronger flow such as cross-signed passport) is an implementation
detail — the contract is that two distinct verification steps must
succeed before a membership transition into `trusted` is committed.

The seed for `contacts` does not grant `messaging-receive@v1` — it
suggests it as default for the operator to confirm. Actual reception
still passes through standard `messaging-receive@v1` capability check.
Seeds are written via the same `relationship-class-changed.v1` event as
operator-driven changes, so audit is uniform. Reserved classes cannot
be archived (invariant 5).

**Crisis flows are intentionally the predicate path, not a hardcoded
class power.** A `contacts` member may qualify as input to a
`crisis.assist` predicate with bounded `effect/scope`; `friends` and
`trusted` may qualify for wider scopes. The class is the eligibility
input; the predicate scope is the bound. This is orthogonal to
`grant-allowlist`:
the class never grants *routine* crisis authority; the predicate gates
a *specific bounded* crisis scope through normal capability/passport
checks.

### Relationship-Derived Policy Predicates

Relationship-derived policy predicates are the **canonical mechanism**
for autonomous host decisions that need local relationship context. They
replace any separate "node trust projection" layer. Implementations may
maintain redacted read models (candidates) for performance, but those
read models are caches of predicate evaluation inputs — they are not
authority, and they are not a new source of trust.

The architectural shape:

```text
participant-participant relationship  (local relationship layer)
  + subject-to-node evidence          (node-operator-binding.v1, P043 attestations, …)
  + local policy for action kind      (relationship-policy-predicate.v1)
  + capability/passport/admission     (existing mechanisms — unchanged)
  -> bounded host action (allow/deny/quarantine + scoped effects)
```

#### Autonomous Host Decisions

The host autonomously evaluates predicates when an action arrives that
the daemon may handle without operator-in-the-loop:

- **Custody acceptance**: AD inbound acceptor for memarium-custody@v1
  requires a predicate match (e.g. remote operator ∈ `friends` of local
  operator, scoped to `artifact.custody:short-ttl`).
- **Crisis assist**: a dedicated `crisis.assist` action kind may use
  `friends`, `guardians`, or `trusted-anchor` as required class. The
  decision is made by a *specific crisis policy*, not by general
  friendship.
- **Gossip / whisper admission**: inbound gossip from a remote node may
  be admitted into a quarantine queue when the operator relationship is
  present. The gossip *content* remains evidence, never truth.
- **Address fallback**: per Proposal 043, trusted peers may serve
  `node-address-attestation.v1`. A predicate may declare the trust class
  required for the receiver to accept the attestation as a routing hint.

Each use case is paired with a specific `effect/scope` — a "friend" for
custody is not automatically a "friend" for crisis or for address
fallback. Scopes do not compose; each predicate is a single tightly
bounded grant.

#### Middleware Trust Requirements Declaration

Middleware packages declare *trust requirements*, not trust decisions.
A package manifest may include:

```json
{
  "trust_requirements": [
    {
      "id": "accept-friend-custody",
      "predicate/kind": "operator-relationship-class",
      "required/class-ids": ["friends", "trusted"],
      "required/status": "active",
      "action/kind": "artifact.custody.accept",
      "effect/scope": "artifact.custody:short-ttl",
      "failure/mode": "quarantine"
    }
  ]
}
```

The host materializes such declarations into
`relationship-policy-predicate.v1` records during package install /
effective-config merge. Operator approval at install time is required;
the readiness gate refuses to load a package whose trust requirements
have not been explicitly accepted.

#### Boundary: Middleware Cannot Read Sealed State

This is enforced as a strong invariant:

```text
INVARIANT (middleware boundary):
  Middleware MAY declare relationship-derived policy requirements.
  Middleware MUST NOT directly read sealed relationship state.
  Middleware MUST NOT turn relationship membership into authority.
  The host evaluates predicates and returns
    `relationship-policy-decision.v1` with redacted evidence refs.
```

Concretely, middleware receives:

```json
{
  "schema": "relationship-policy-decision.v1",
  "decision/id": "...",
  "predicate/ref": "accept-friend-custody",
  "decision": "allow",
  "action/kind": "artifact.custody.accept",
  "effect/scope": "artifact.custody:short-ttl",
  "evidence/ref": ["...redacted..."]
}
```

or:

```json
{
  "schema": "relationship-policy-decision.v1",
  "predicate/ref": "accept-friend-custody",
  "decision": "quarantine",
  "reason/code": "operator-relationship-not-established"
}
```

Middleware never receives the list of friends, notes, history, or raw
membership facts. Even the `candidate/ref` is not exposed by default;
it is operator-visible diagnostic surface, not middleware-consumable.

#### Evaluation Flow

```text
remote-action arrives
  -> verify node-operator-binding.v1 (P043 / capability layer)
  -> resolve remote operator participant
  -> look up matching predicate(s) for action/kind
  -> build candidate(s):
       fetch membership fact in owner's relationship space
       gather evidence refs (binding, attestations, passports)
       check status, valid/until, limits
  -> capability/passport/admission checks (existing layers)
  -> emit relationship-policy-decision.v1
  -> return decision to middleware / autonomous handler
  -> if allow: execute bounded effect within declared scope
  -> if quarantine: deferred operator review
  -> if deny: terminate with reason/code
```

The flow has explicit stages, each with typed input/output. None of the
stages alone is sufficient to authorize the action; all must pass.

### Daemon API (Local Host-Owned)

Two distinct concepts that must not be conflated:

- **No new public protocol capability** in this iteration. Local
  Relationship Layer is not exposed as a network-visible host capability;
  no peer can invoke it, no federated discovery references it.
- **Yes, a local authenticated host API for in-process and supervised
  middleware consumers.** Messaging is a supervised process and AD resolver
  runs in daemon. Both call into the layer through an authenticated,
  capability-gated host surface instead of sharing storage or hidden
  in-process state.

The local host capabilities are gated through the existing daemon caller
binding mechanism. Capability ids (host-internal, not protocol-visible):

```text
local-relationship.class.list
local-relationship.class.upsert
local-relationship.class.archive

local-relationship.membership.append
local-relationship.membership.list
local-relationship.membership.latest
local-relationship.class-members.list

local-relationship.nym-binding.upsert
local-relationship.nym-binding.list

local-relationship.group.resolve

local-relationship.predicate.list
local-relationship.predicate.register
local-relationship.predicate.evaluate
local-relationship.decision.list
```

Each capability declares allowed callers (Messaging adapter, AD
resolver, Operator UI, migration tool) in effective host config. A caller
without an explicit grant cannot reach the API even from within the
daemon process; this prevents accidental coupling from unrelated
subsystems. The capabilities are *local-authenticated* — they require a
caller binding but never a peer signature, and they never appear in
public capability matrices.

The API surface:

```text
list_classes(filter?) -> [RelationshipClassV1]
upsert_class(class) -> RelationshipClassV1
archive_class(class_id, reason) -> ClassArchiveResult

append_membership(contact_ref, class_id, status, actor_ref, reason_code, context_ref?) -> MembershipFactV1
list_memberships(filter?) -> [MembershipFactV1]
latest_membership(contact_ref, class_id) -> Option<MembershipFactV1>
list_class_members(class_id, status_filter?) -> [(ContactRef, latest_status, latest_fact_id)]

upsert_nym_binding(contact_ref, context_kind, context_ref?, nym, detected_by) -> PairwiseNymBindingV1
list_nym_bindings(contact_ref?, context_kind?) -> [PairwiseNymBindingV1]

resolve_group(group_id) -> [ResolvedRelationshipCandidate]

list_predicates(filter?) -> [RelationshipPolicyPredicateV1]
register_predicate(predicate, declared_by, operator_acknowledgement) -> PredicateRegistration
evaluate_predicate(predicate_ref, action_context) -> RelationshipPolicyDecisionV1
list_decisions(filter?) -> [RelationshipPolicyDecisionV1]
```

`resolve_group` is the bridge to Artifact Delivery. Returning a list of
raw `ContactRef` is too thin: AD needs enough metadata to decide candidate
ordering, surface in operator diagnostics, and apply its own policy
without knowing relationship semantics.

```text
ResolvedRelationshipCandidate {
  contact/ref               # opaque contact identifier
  class/id                  # which class this candidate comes from (e.g. "friends")
  relationship/fact-id      # the membership fact this resolution is based on
  candidate/status          # "active" — only active memberships resolve into candidates
  resolved-at-tx/id         # transaction id at resolution time
  route-hints[]?            # optional Catalog-derived route hints, opaque to AD
                            #   — never authority, just routing helpers
}
```

AD's `selector/kind = "group"` resolver calls `resolve_group(group_id)`
and gets a typed candidate list. The `group_id` may be a reserved class
id (`friends`) or a namespaced group reference. AD then performs its own
passport/capability checks against each candidate before delivery —
`ResolvedRelationshipCandidate` is *selection metadata*, never authority.

### Pre-Release Migration Decision

Because the system is still before its first release, Local Relationship
Layer is completed as a **breaking pre-release change** rather than a
compatibility bridge.

#### Phase 1: layer exists

- schemas land;
- `node/local-relationship-core` crate (pure, no I/O);
- daemon `LocalRelationshipStore`;
- vault snapshot integration;
- SQLite projection;
- replay equivalence tests;
- daemon-internal API;
- operator UI for class management (basic);
- no public Local Relationship protocol.

#### Phase 2: canonical consumers, no legacy bridge

- Messaging accept/block produces relationship membership facts only
  through Local Relationship host capabilities.
- `relationship-membership-fact.v1` is the new canonical fact.
- AD `selector/kind = "group"` calls `resolve_group(...)` against the
  Local Relationship Layer.
- Contact Catalog cleanup: remove any local relationship annotation
  (label, last-interaction, trust scoring, membership state) from
  Catalog; Catalog retains only public discovery / route-set lookup
  state. Raw handles or private address-book-like data must not migrate
  *into* Catalog from Local Relationship Layer — those belong in the
  vault-backed layer. The expected flow becomes:
  `Catalog lookup (public discovery) → Local Relationship annotation
  (private) → consumer policy (passport-gated)`.

Order of writes inside `LocalRelationshipStore`:

1. Append event to vault event log (sealed). Failure here aborts.
2. Update SQLite projection in same SQL transaction as commit of event
   log offset.
3. Emit `relationship-membership-fact.v1` to subscribers.

There is no `contacts_membership` compatibility cache and no
`contacts.membership-changed.v1` compatibility fact in the target state.

### Relationship to Other Proposals

- **023 Artifact Delivery** — AD `selector/kind = "group"` resolver calls
  `resolve_group(group_id)` against Local Relationship Layer. AD never
  knows what `friends` is; it sees only resolved contact refs. Delivery
  still requires standard passport/capability checks; group resolution is
  candidate selection, not authorization. AD inbound acceptors may
  additionally require relationship-policy predicates for autonomous
  custody / acceptance decisions.
- **043 Node Address Attestation Fallback** — predicate evaluation
  consumes `node-address-attestation.v1` as one form of subject-to-node
  evidence. A predicate may declare that the receiver requires a trusted
  relationship class for accepting attestations as routing hints.
  Receiver still makes its own local policy decision per P043 §43.
- **025 Contact Catalog** — Contact Catalog remains public route-set
  lookup. After Phase 2, Contact Catalog removes `friends`, raw handles,
  and any local annotation. Flow: Catalog lookup → local annotation in
  Relationship Layer → consumer policy.
- **026 Pseudonym Vault** — Local Relationship Layer state lives as
  sealed inner entries of kind `local-relationship`. Recovery bundle
  (P026) automatically includes relationship state. Schema additively
  extends `pseudonym-vault.v1`.
- **027 Messaging Middleware** — Messaging becomes a consumer:
  - reads active `contacts` class membership for inbound/outbound policy;
  - on `contact-request.accept`, triggers relationship membership append;
  - emits `messaging-receive@v1` based on relationship state;
  - stops being canonical owner of `contacts` concept;
  - may declare `trust_requirements` (relationship-policy predicates) in
    its package manifest for autonomous decisions outside operator loop.
- **028 Temporal Storage Convention** — Relationship store uses the
  full 028 shape: transactions, events, current projection, replay
  equivalence, performance profile drives snapshot recheckpoint cadence.
- **057 Notifications** — Operator notifications for class management
  events (class added/archived, membership migration completed) use
  notification kinds; contact-specific notification preferences live
  in Relationship Layer, not Notifications.
- **062 Temporal Storage Convention (proposal)** — Same as 028
  reference. Retention horizon, compaction, excision rules apply.
- **063 Inquirium** — Inquirium `context_refs` resolver may read from
  Local Relationship Layer for inquiries about peers. Relationship Layer
  exposes redacted context views per Inquirium retention policy.

## Trade-offs

### Benefits

- single source of truth for "who is this person to me";
- relationship class extensibility without touching Messaging, AD, or
  Catalog;
- pairwise nym continuity has a home;
- privacy boundary is clear: relationship state never escapes vault as
  plaintext;
- AD becomes generic via `resolve_group`; no more `friends`-specific
  code paths;
- migration path is concrete, not aspirational.

### Costs

- new layer to learn for operators;
- vault snapshot recheckpoint adds background I/O;
- pre-release data stores may be destructively cleaned when legacy
  relationship tables are present;
- schema changes to `pseudonym-vault.v1` (additive, forward-compat) but
  still a contract surface.

### Constraints

- SQLite still serializes writers; performance benefit comes from short
  per-fact event append, not concurrent writes;
- vault seal cost is real; per-fact UI latency depends on event log
  append speed, not vault seal cadence.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Vault seal fails during recheckpoint | Event log remains source of truth; recheckpoint retries with exponential backoff; operator notification on persistent failure. |
| Legacy messaging relationship state exists on disk | Pre-release startup migration drops obsolete tables/facts; runtime uses only canonical Local Relationship facts and never enters a bridge `migration-pending` state. |
| Class collision at startup (two definitions of same class id) | Readiness gate fails; daemon refuses to start with explicit `relationship-class-conflict` error naming both producers. |
| SQLite projection diverges from event log | Replay equivalence test fires at startup (checksum compare); divergence triggers projection rebuild from event log. |
| Peer-emitted fact tries to enter relationship layer | Inbound path does not exist by design; subsystem adapter (messaging, AD) translates peer-triggered events into local emissions with `actor/ref` of the operator's binding, not the peer. |
| Relationship state leaks to logs or traces | Per `privacy/profile` field on each class; default `sealed-only` blocks any non-sealed export; redaction tests in CI per Solution 028 anti-secret-leak pattern. |
| Operator archives a class with active members | Archive is allowed; members remain in event log; resolver excludes archived class from active queries; operator UI shows "X members of archived class". |
| Pairwise nym binding records grow unbounded | Per-context retention horizon from performance profile (Solution 028); old bindings compacted to `compacted_snapshot` event past horizon. |
| Predicate evaluation runs with no node-operator-binding evidence | Evaluator returns `decision = deny` with `reason/code = "operator-binding-missing"`. No fallback to "trust by participant id string match"; binding must be verified evidence, not claim. |
| Middleware attempts to read sealed relationship state directly | Local host capabilities do not expose membership lists to middleware; only `evaluate_predicate` returns `relationship-policy-decision.v1`. Attempting to list memberships from a middleware caller binding fails closed with `caller-not-authorized`. |
| Package declares predicate but operator never approved | Readiness gate refuses to enable the package; predicate sits in `registered/pending-operator-approval` state and never evaluates. Operator approval emits `relationship-policy-predicate-acknowledged` audit event. |
| Predicate scope grows by accretion (one scope used for many actions) | `effect/scope` is mandatory and must be unique per action-kind family. Readiness gate refuses two predicates declaring the same `(action/kind, effect/scope)` from different packages without explicit operator-acknowledged precedence. |

## Open Questions

1. Should `relationship-class.v1` allow per-class operator override of
   retention horizon (currently inherits from host default via profile-ref),
   or is the inherited horizon sufficient for first iteration?
2. Does `pairwise-nym-binding.v1` need additional context kinds beyond
   the initial set (`messaging`, `ad-direct`, `agora-topic`,
   `inquirium-session`)? Adding kinds later is forward-compatible, but a
   complete-enough initial set reduces churn.
3. When does `pairwise nym continuity` evidence get strong enough to be a
   policy input vs purely informational? This is a follow-up concern about
   how confidence in continuity flows into trust decisions, deferred to a
   later proposal.

## Next Actions

1. Promote this proposal to `Solution 032: Local Relationship Layer` with
   the implementation guidance and storage contract.
2. Add schemas (`relationship-class.v1`, `relationship-membership-fact.v1`,
   `pairwise-nym-binding.v1`) to `orbidocs/doc/schemas` and mirror to
   `node/protocol/contracts`. Extend `pseudonym-vault.v1` additively.
3. Update `local-contact.v1` schema documentation (ownership note only).
4. Implement `node/local-relationship-core` crate (pure types,
   validators, projection reducer).
5. Implement `LocalRelationshipStore` in daemon with vault-backed event
   log + SQLite projection per Solution 028.
6. Switch Messaging to canonical-only Local Relationship membership reads
   and writes; remove legacy contact-membership storage and fact emission.
7. Implement AD group resolver (`selector/kind = "group"` →
   `resolve_group`).
8. Clean up Contact Catalog: remove `friends`, raw handles, local
   membership state.
9. Add operator UI for class management and membership inspection.
10. Update cross-referenced docs (023, 025, 026, 027, 028, 043, 057, 060,
    062, 063) at ownership/cross-reference points only.
11. Implement relationship-policy predicate schemas, host policy
    evaluator, and middleware `trust_requirements` declaration mechanism.
12. Add operator approval flow for predicate registration via package
    install path.

## Tracking

This tracker is milestone-shaped. M1-M6 are the MVP implementation
slice for Solution 032. Legacy Messaging relationship storage was removed
before first release instead of being promoted to a deferred compatibility
track.

| ID | Milestone | MVP scope | Status | Notes |
|---|---|---:|---|---|
| P065-M1 | Contracts | `true` | done | Added relationship class, class-change, membership, pairwise nym, predicate, candidate, and decision schemas; mirrored them to `node/protocol/contracts`; extended `pseudonym-vault.v1` with `local-relationship`; added positive/negative fixtures, including forbidden wildcard scopes and bare `blocked` as a class id. |
| P065-M2 | Pure core | `true` | done | Added `node/local-relationship-core` with schema-shaped types, validators, replay reducers, active group resolver, predicate evaluator, node-operator-binding evidence checks, owner-scoped membership keys, shared `route_key` canonicalization for relationship/contact route matching, and read-model filters. No I/O, daemon, SQLite, or async runtime dependency. |
| P065-M3 | Storage + daemon API | `true` | partial | Implemented daemon-owned `LocalRelationshipStore`, `<data-dir>/storage/local-relationships.sqlite` projection with `transactions`, `events`, `current_*`, predicates, `predicate_class_ids`, and decisions, startup replay from Pseudonym Vault `local-relationship` records, default `untrusted`/`contacts`/`friends`/`trusted` seed when the vault is writable, runtime rejection of reserved-class archival with `cannot-archive-reserved-class`, explicit support for operator metadata edits on reserved classes, control API, and guarded host capabilities. Projection cells are sealed with the daemon sealer AEAD backend under `local-relationship-projection:v1`, lookup columns use sealer-derived keyed HMAC indexes rather than raw refs, and control writes now follow `prepare record -> append sealed vault entry -> apply projection`; projection failure after vault commit marks `pending-vault-rebuild` rather than treating SQLite as canonical. Production projection-only mutation helpers have been removed from the non-test API. Remaining hardening: broader restart/rebuild and performance smoke gates. |
| P065-M4 | Operator UI + trust requirements | `true` | partial | Added a minimal operator UI at `/admin/local-relationships` for class upsert, membership append, predicate registration/evaluation, and decision audit. The UI renders the four reserved tiers distinctly, submits predicate requirements as `required/class-ids[]`, validates that at least one class is selected before daemon submission, requires typed secondary confirmation with a bounded modal lifetime before approving predicates that include `trusted`, and now records predicate approval as `pending`, `approved`, or `rejected`. Rejection requires a reason and is stored as vaulted `local-relationship-predicate-approval.local.v1` audit state. Middleware package manifests can declare `trust_requirements[]`; signed package readiness blocks startup until approval and reports `predicate-rejected` after rejection. Remaining work: a richer dedicated pending/rejected package queue and package-install audit navigation. |
| P065-M5 | Messaging canonical integration | `true` | partial | `contact-request.accept` now creates/updates local contact state and appends canonical `contacts` membership plus pairwise messaging nym binding through the Local Relationship Layer. `messaging-service` has owner-scoped Local Relationship integration: active-membership reads call `local-relationship.membership.latest`, membership writes append canonical `relationship-membership-fact.v1` through `local-relationship.membership.append`, and missing host/owner configuration fails closed instead of falling back to local legacy state. Daemon tests prove owner A membership does not satisfy owner B group resolution, and Story-010 acceptance tooling now has `--multi-operator-scope` coverage for contradictory owner-scoped memberships. `status = blocked` now feeds the schema-scoped `contact-request.v1` AD/INAC preflight as the canonical local deny signal for public contact-request delivery. The pre-release `contacts_membership` cache, bootstrap migration endpoint, and `contacts.membership-changed.v1` compatibility fact have been removed. Story-010 strict `ad-smoke` passes over this canonical-only path. |
| P065-M6 | AD integration + Contact Catalog cleanup + hardening | `true` | partial | AD has a dynamic group selector hook and daemon wiring to resolve Local Relationship classes for the primary local operator into ordinary recipient selectors when relationship candidates carry AD-routable `contact/ref` values (`node:`, `participant:`, `routing:`), or `local-contact:` records that carry a local `routing-subject/id` or participant `remote/subject`. The relationship membership contract permits directly routable `node:`, `participant:`, and `routing:` refs while keeping pairwise nym bindings local-contact scoped; tests assert empty groups fail closed and relationship candidates do not bypass AD outbound allow/passport authority. Host predicate evaluation verifies available node-operator-binding evidence from the daemon binding store and redacts candidate/evidence detail before returning to middleware. Contact Catalog public-discovery-only cleanup is documented, and Story-010 acceptance tooling now has `--relationship-group-delivery` coverage that promotes the accepted contact to `friends` and verifies Local Relationship group resolution; the new Story-010 group/multi-operator variants pass locally. AD config validation permits late-bound group references, so Local Relationship groups do not need static placeholder groups. Remaining planned work: wire the new Story-010 variants into CI, broaden privacy regression tests, add performance smoke, and add a remote-disclosed binding import path beyond the current local verified binding store. |
| P065-D1 | Legacy bridge removal | `true` | done | Completed before first release as a breaking change: no `contacts_membership` cache, no bootstrap migration endpoint, and no `contacts.membership-changed.v1` contract remain. |
| P065-D3 | Public protocol capability | `false` | deferred | Local-authenticated host API remains the MVP boundary. A public/federated capability would need a separate threat model. |
