# Local Relationship Layer

The Local Relationship Layer is the host-owned, vault-backed source of
truth for the user's private relationship state: relationship classes,
membership facts, pairwise nym continuity, and relationship-derived
policy predicates that turn participant-level trust into bounded,
explicit node-level decisions.

Status: `accepted`

Date: `2026-05-19`

Based on: `doc/project/40-proposals/065-local-relationship-layer.md`

## Executive Summary

Messaging, Artifact Delivery, and Contact Catalog stop owning partial
models of "who this person is to me". One layer holds the canonical
private relationship state. Schema shape:

```text
append relationship-class, relationship-membership-fact,
   pairwise-nym-binding-fact events
  -> derive current projection (class definition, membership, nym binding)
  -> evaluate relationship-policy-predicates on demand
  -> return relationship-policy-decision to middleware/host
  -> verify replay equivalence in tests
```

Sealed vault event log is the recovery source of truth. SQLite projection
under `<data-dir>/storage/local-relationships.sqlite` is a rebuildable
performance cache per Solution 028. Middleware never reads sealed state;
it declares trust requirements and receives bound decisions.

## Context and Problem Statement

Three subsystems currently co-own personal relationship state:

- Messaging defines what a `contact` is; `contacts.membership-changed.v1`
  is messaging-owned.
- Artifact Delivery references `friends` without owning its definition;
  the leak rests on Messaging conventions.
- Contact Catalog accreted local annotation onto its public-discovery
  surface.

Concrete consequences: a custom class (`book-club`) has no home; "block"
exists at two layers and drifts; pairwise nym continuity is reasoned
about ad-hoc; and personal data about peers lives outside the Pseudonym
Vault recovery model. Cross-cutting changes (privacy class, retention,
operator UI) are not possible in any one place.

## Load-Bearing Invariants

The solution exists to enforce these. Implementations that violate any
one are non-conformant.

1. **Label is not authority.** Class membership is never, by itself, a
   capability grant. It may be policy input; capabilities flow through
   passports and admission.

2. **Classes and memberships are separate entities.** Class is an
   operator-defined policy bundle (mutable projection, every change
   emits a fact). Membership is an append-only fact.

3. **Membership facts are strictly local-emitted.** No wire-shape
   inbound. Other subsystems may *trigger* local emission; the fact is
   always produced locally with `actor/ref` of a host-issued operator
   binding.

4. **Canonical state lives in the Pseudonym Vault.** Vault-sealed event
   log + latest sealed snapshot is the recovery source of truth. SQLite
   projection is a rebuildable cache, never authority.

5. **Reserved IDs + mandatory namespace.** `contacts` and `friends` are
   reserved as well-known classes with seeded default policy. All other
   classes MUST be namespaced (`vendor.example/...`, `operator-local/...`).
   `blocked` is intentionally NOT a class — it is a *status* on
   memberships, never a class equivalent to `contacts`/`friends`.

6. **Classes are archived, never deleted.** Archive transitions the class
   out of active resolver results; facts remain in the event log.

7. **Class definitions are mutable projection; every change emits a
   fact.** Current class is mutable; `relationship-class-changed.v1`
   captures every transition for audit.

8. **Relationship membership informs autonomous host policy but never
   becomes node-node authority by itself.** Relationship-derived node
   trust requires all of: (a) local membership, (b) verified
   subject-to-node evidence, (c) explicit local policy predicate, (d)
   normal capability/passport/admission, (e) bounded effects. This is
   local political projection, never trust propagation.

## Storage Architecture

Three layers with explicit authority order:

| Layer | Role | Authority |
| --- | --- | --- |
| Sealed event log + latest sealed snapshot | Vault-backed inner entries (kind `local-relationship`) | **Canonical truth** |
| Sealed snapshot alone | Checkpoint accelerator (skip replay before `tx/id`) | Recovery accelerator, never alternate authority |
| SQLite projection | `<data-dir>/storage/local-relationships.sqlite` per Solution 028 | Rebuildable cache, deletable, never authority |

**Authority ordering rule (non-negotiable):** discarding the snapshot but
keeping the event log is recoverable. The inverse is not.

### Privacy Boundary in the SQLite Projection

No plaintext relationship state on disk outside the vault. Three
acceptable shapes:

| Mode | Content | Status |
| --- | --- | --- |
| Encrypted-at-rest | Cell-level AEAD with per-store key derived from vault | First-iteration target |
| Opaque references only | Vault-internal opaque refs + `tx/id`; lookups resolve via vault | Acceptable if cell-level AEAD deferred |
| Plaintext | Forbidden in target state | Transitional only during Phase 2 bridge; explicit `legacy_plaintext_cache` flag; operator warning at startup |

The existing `local-contacts.sqlite` daemon-side plaintext store is
labelled transitional. Phase 4 retires it.

### Write Path

```text
1. validate request, resolve class/contact refs, check owner space
2. append membership event to sealed event log (single fsync)
3. update SQLite projection in same SQL transaction (Solution 028)
4. emit relationship-membership-fact.v1 to subscribers
5. schedule vault snapshot recheckpoint if threshold reached
```

### Snapshot Recheckpoint Cadence (Performance Profile from Solution 028)

| Profile | After N events | Or idle T seconds |
| --- | --- | --- |
| `minimal` | 50 | 30 |
| `balanced` | 100 | 60 |
| `full-audit` | 25 | 15 |

Crash recovery: replay sealed event log forward from last good snapshot.
Snapshot is correctness checkpoint, not latency checkpoint.

## Schemas

All schemas land in `orbidocs/doc/schemas` with mirror under
`node/protocol/contracts`. New schemas drop the `local-` prefix;
`local-contact.v1` is preserved unchanged for backward compatibility.

### Class definitions (mutable projection)

- `relationship-class.v1` — class definition with policy fields
  (`grant-policy/default-allowlist`, `grant-policy/suggested-defaults`,
  `grant-allowlist`, `verification/required`, `privacy/profile`,
  `retention/profile-ref`). `grant-allowlist` requires operator action;
  `grant-policy/*` never grants automatically.

- `relationship-class-changed.v1` — append-only event for every class
  create/update/archive/unarchive transition. Create/update/unarchive
  carry the next class snapshot; update/archive/unarchive carry the prior
  snapshot. Archive and unarchive require `reason/code`, and archive
  forbids `next/definition` so the audit event is an explicit lifecycle
  transition rather than an implicit definition rewrite. UI reads class
  projection; audit reads this fact stream.

### Membership facts (append-only)

- `relationship-membership-fact.v1` — append-only fact with `owner/ref`
  (whose relationship space), `contact/ref`, `class/id`, `status` ∈
  {`active`, `pending-outgoing`, `pending-incoming`, `blocked`,
  `revoked`}, `actor/ref`, `event/at`, `tx/id`, `supersedes/fact-id?`
  (projection hint only — prior fact never deleted),
  `reason/code?`/`reason/note?`/`context/ref?`.

  `owner/ref` answers "whose relationship is this?" — essential on
  multi-operator nodes. Single-operator defaults to node primary
  operator binding.

### Pairwise nym continuity

- `pairwise-nym-binding-fact.v1` — append-only event:
  `event/kind` ∈ {`observed`, `rotated-into`, `retired`},
  `nym/value`, `prior/nym?`, `context/kind`, `context/ref?`,
  `detected/by`, `evidence/ref?`, `tx/id`.

- `pairwise-nym-binding.v1` — sealed projection reducing
  `pairwise-nym-binding-fact.v1` to current state per (contact, context).
  History is derived from facts, never mutated in place.

### Relationship-derived policy

- `relationship-policy-predicate.v1` — declarative condition (middleware
  or operator-defined). Fields: `predicate/kind`,
  `local/operator-ref?`, `remote/operator-binding-ref`,
  `required/class-id`, `required/status`, `action/kind`, `effect/scope`,
  `ttl?`, `failure/mode` ∈ {`deny`, `require-operator`, `quarantine`},
  `declared/by`. `effect/scope` is mandatory; predicates never bind
  general authority.

- `relationship-policy-candidate.v1` — host-internal read model for
  diagnostic / audit / candidate ranking. `candidate/effects[]` (not
  `allowed/effects[]`) signals possible permissibility, never grant.

- `relationship-policy-decision.v1` — host-bound outcome:
  `decision` ∈ {`allow`, `deny`, `quarantine`, `require-operator`},
  `reason/code` (closed enum), `evidence/ref[]` (redacted),
  `effect/scope`, `valid/until`, `decided/by`/`decided/at`, `tx/id`.
  This is the only shape middleware sees.

### Vault schema extension (additive)

- `pseudonym-vault.v1` (existing) — additively accept `local-relationship`
  as inner-entry kind. Forward-compat: readers MAY ignore unknown kinds;
  importers/resealers MUST preserve unknown kinds verbatim;
  `critical=true` entries fail closed on unknown kind; integrity
  violations always fail closed.

### Existing schemas with documentation-only changes

- `local-contact.v1` — schema unchanged. Documentation now states the
  boundary explicitly: Local Contact Store owns private contact records
  (raw handles, labels, UX metadata); Local Relationship Layer owns
  classes, memberships, policy predicates, and pairwise relationship
  facts.

## Read Models and Redaction Levels

Three named read projections; consumers declare needed level; layer
refuses higher detail than the class `privacy/profile` allows.

| Level | Content | Consumers |
| --- | --- | --- |
| `sealed-only` | Full record incl. notes, reasons, history | Recovery, audit, operator forensics under explicit grant |
| `operator-visible-summary` | Display name, active class memberships, last-event timestamp | Operator UI inbox, dashboard |
| `ui-row` | Display name + opaque contact-ref | Contact list sidebar, AD candidate diagnostic |

`privacy/profile` on class definition sets upper bound for that class.
Default `sealed-only`.

## Default Class Seeds

Reserved classes ship with seeded definitions written via
`relationship-class-changed.v1` at first daemon start (so seed is
auditable, not magic).

The two reserved classes form an intentional gradation: `contacts` is
the soft class (*known, may correspond, no routine action authority*);
`friends` is the firmer class (*known, may correspond, plus routine
opt-in actions*).

```text
contacts:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: [messaging-receive@v1]
  grant-allowlist: [messaging-receive@v1]
  verification/required: peer-mutual-accept
  privacy/profile: operator-visible-summary

friends:
  default-status: active
  grant-policy/default-allowlist: []
  grant-policy/suggested-defaults: [messaging-receive@v1, ad.direct-target]
  grant-allowlist: [messaging-receive@v1, ad.direct-target, agora.private-topic]
  verification/required: operator-explicit
  privacy/profile: sealed-only
```

Seed grants nothing automatically. Operator confirmation at install /
membership append is the gate.

### Gradation: `contacts` → `friends` → custom → predicate

The `contacts` seed is intentionally narrow: routine `grant-allowlist`
covers correspondence only. A `contact` becoming an AD direct-target or
a private-topic participant is not a routine operation — it requires one
of:

| Path | When to use |
| --- | --- |
| Promote to `friends` | The contact has crossed a personal threshold and the operator wants routine access. One-click operator action, audited via `relationship-class-changed.v1` (membership) + `relationship-membership-fact.v1`. |
| Custom namespaced class (e.g. `operator-local/inner-circle`) | The operator wants a class semantically distinct from `friends` (different verification, different `privacy/profile`, narrower grants) without touching reserved-class seeds. |
| Per-person grant via existing capability/passport mechanism | A single peer needs one specific capability without class semantics. Heavier process by design; relationship layer is not the only path. |
| Relationship-policy predicate with bounded `effect/scope` | Situational, bounded autonomy. E.g. `crisis.assist` predicate accepting `contacts` as input under `effect/scope = crisis:assist-bounded`. Class is the *input*; predicate scope is the *bound*. |

**Crisis flows are explicitly the predicate path, not a hardcoded class
power.** A predicate may declare that `contacts` qualifies for
`crisis.assist` while `friends` qualifies for a wider crisis scope — the
classes provide eligibility input, the predicate scope provides the
bound. This is orthogonal to `grant-allowlist`: the class never gives
*routine* crisis authority; the predicate gates a *specific bounded*
crisis scope through normal capability/passport checks.

Operator UI labels SHOULD make the gradation visible:

- **contacts** — known peers; correspondence
- **friends** — close peers; correspondence + routine opt-in actions

This wording is part of the operator-visible vocabulary, not the
machine-readable schema. The schema enforces the policy difference
through `grant-allowlist` and `verification/required`.

## Daemon API (Local Host-Owned)

No public protocol capability in this iteration. Local-authenticated
host capabilities for in-process and supervised middleware consumers:

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

Each capability declares allowed callers in effective host config. A
caller without explicit grant fails closed with `caller-not-authorized`,
even from within the daemon process.

### API surface

```text
list_classes(filter?) -> [RelationshipClassV1]
upsert_class(class) -> RelationshipClassV1
archive_class(class_id, reason) -> ClassArchiveResult

append_membership(owner_ref, contact_ref, class_id, status, actor_ref, reason_code, context_ref?)
  -> MembershipFactV1
list_memberships(filter?) -> [MembershipFactV1]
latest_membership(owner_ref, contact_ref, class_id) -> Option<MembershipFactV1>
list_class_members(owner_ref, class_id, status_filter?)
  -> [(ContactRef, latest_status, latest_fact_id)]

upsert_nym_binding(contact_ref, context_kind, context_ref?, nym, detected_by)
  -> PairwiseNymBindingV1
list_nym_bindings(contact_ref?, context_kind?) -> [PairwiseNymBindingV1]

resolve_group(group_id) -> [ResolvedRelationshipCandidate]

list_predicates(filter?) -> [RelationshipPolicyPredicateV1]
register_predicate(predicate, declared_by, operator_acknowledgement)
  -> PredicateRegistration
evaluate_predicate(predicate_ref, action_context) -> RelationshipPolicyDecisionV1
list_decisions(filter?) -> [RelationshipPolicyDecisionV1]
```

`ResolvedRelationshipCandidate` carries `contact/ref`, `class/id`,
`relationship/fact-id`, `candidate/status`, `resolved-at-tx/id`,
optional `route-hints[]`. AD performs its own passport/capability checks
against each candidate.

## Relationship-Derived Policy Predicates

The canonical mechanism for autonomous host decisions that need local
relationship context. Replaces any "node trust projection" layer.

### Architecture

```text
participant-participant relationship  (local relationship layer)
  + subject-to-node evidence          (node-operator-binding.v1, P043 attestations, …)
  + local policy for action kind      (relationship-policy-predicate.v1)
  + capability/passport/admission     (existing mechanisms — unchanged)
  -> bounded host action (allow/deny/quarantine + scoped effects)
```

### Three-tier separation

| Concept | Role |
| --- | --- |
| **Predicate** | Declarative condition: "for action X, require relationship class Y in owner's space". |
| **Candidate** | Host-internal eligibility input: "this remote operator matches the predicate with this evidence and these bounds". Diagnostic / audit / ranking surface. |
| **Decision** | Host-bound outcome: "allow/deny/quarantine for this concrete action with this scope". Only shape middleware sees. |

### Autonomous host decisions (use cases)

| Action kind | Required class (example) | Bounded effect scope |
| --- | --- | --- |
| `artifact.custody.accept` | `friends` | `artifact.custody:short-ttl` |
| `crisis.assist` | `guardians` or `friends` | `crisis:assist-bounded` |
| `gossip.accept` | `contacts` | `gossip:quarantine-only` |
| `attestation.accept-routing-hint` | `friends` | `routing:hint-only` |

`effect/scope` is mandatory and unique per action-kind family. Scopes do
not compose; "friend" for custody is not "friend" for crisis.

### Middleware trust requirements declaration

Middleware declares requirements, not decisions. Package manifest:

```json
{
  "trust_requirements": [
    {
      "id": "accept-friend-custody",
      "predicate/kind": "operator-relationship-class",
      "required/class-id": "friends",
      "required/status": "active",
      "action/kind": "artifact.custody.accept",
      "effect/scope": "artifact.custody:short-ttl",
      "failure/mode": "quarantine"
    }
  ]
}
```

Operator approval at install time is required. Readiness gate refuses
to enable a package whose trust requirements have not been explicitly
acknowledged.

### Middleware boundary (INVARIANT)

```text
Middleware MAY declare relationship-derived policy requirements.
Middleware MUST NOT directly read sealed relationship state.
Middleware MUST NOT turn relationship membership into authority.
The host evaluates predicates and returns relationship-policy-decision.v1
with redacted evidence refs.
```

Middleware sees decision objects only:

```json
{
  "schema": "relationship-policy-decision.v1",
  "decision": "allow",
  "predicate/ref": "accept-friend-custody",
  "action/kind": "artifact.custody.accept",
  "effect/scope": "artifact.custody:short-ttl",
  "evidence/ref": ["...redacted..."]
}
```

Never the candidate, the membership fact, or any sealed state.

### Evaluation flow

```text
remote-action arrives
  -> verify node-operator-binding.v1 (P043 / capability layer)
  -> resolve remote operator participant
  -> look up matching predicate(s) for action/kind
  -> build candidate(s):
       fetch membership in owner's relationship space
       gather evidence refs (binding, attestations, passports)
       check status, valid/until, limits
  -> capability/passport/admission checks (existing layers)
  -> emit relationship-policy-decision.v1
  -> return decision to middleware / autonomous handler
  -> if allow: execute bounded effect within declared scope
  -> if quarantine: deferred operator review
  -> if deny: terminate with reason/code
```

None of the stages alone is sufficient; all must pass.

## Phased Migration

Phase 1 + Phase 2 commit in first iteration; Phase 3 + Phase 4 deferred.

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Layer exists; no consumer migration | first iteration |
| 2 | Bridge: read new layer, write new + legacy; one-shot migration at first start after deploy | first iteration |
| 3 | Messaging stops writing to legacy table; emits legacy projection from event log | deferred |
| 4 | Legacy table and fact deprecated; Solution 028 retention applies | deferred |

### One-shot migration at first start (Phase 2)

```text
1. open existing Messaging contacts_membership table
2. for each row, emit relationship-membership-fact.v1 with reason/code = "migration-bootstrap"
3. seal initial vault snapshot
4. mark daemon as migrated_at = <RFC3339>
5. emit operator notification on completion (Solution 057)
```

Migration is idempotent. Re-running emits no new facts for already-migrated
rows. Daemon stays in `migration-pending` until success.

### Write order during Phase 2

```text
1. append event to sealed event log; failure aborts
2. update SQLite projection in same transaction
3. write to legacy contacts_membership (best-effort, non-blocking, retry record on failure)
4. emit relationship-membership-fact.v1 subscriber notify
5. emit legacy contacts.membership-changed.v1
```

Steps 1–2 atomic. Step 3 has retry record so legacy consumers eventually
catch up.

## Relationship to Other Solutions

- **023 Artifact Delivery** — AD `selector/kind = "group"` calls
  `resolve_group(...)`; AD never knows what `friends` is. AD inbound
  acceptors may require relationship-policy predicates for autonomous
  decisions. Passport/capability checks remain unchanged.
- **025 Contact Catalog** — public discovery / route-set lookup only.
  Local annotations and membership state removed from Catalog. Flow:
  `Catalog lookup → Relationship annotation → consumer policy`.
- **026 Pseudonym Vault** — relationship state lives as sealed inner
  entries (kind `local-relationship`). Recovery bundle automatically
  includes relationship state. Schema extends `pseudonym-vault.v1`
  additively.
- **027 Messaging Middleware** — consumer:
  - reads active `contacts` membership for inbound/outbound policy;
  - on `contact-request.accept`, triggers membership append;
  - emits `messaging-receive@v1` based on relationship state;
  - may declare `trust_requirements` in package manifest;
  - stops being canonical owner of `contacts`.
- **028 Temporal Storage Convention** — full convention applies:
  transactions, events, current projection, replay equivalence,
  performance profile drives snapshot recheckpoint cadence.
- **043 Node Address Attestation Fallback** — predicate evaluation
  consumes `node-address-attestation.v1` as subject-to-node evidence.
  Receiver still makes local policy decision per P043.
- **057 Notifications** — operator notifications for class management
  events and migration completion; contact-specific notification
  preferences live in Relationship Layer.
- **063 Inquirium** — `context_refs` resolver may read redacted views
  per request retention policy.

## Trade-offs

### Benefits

- Single source of truth for "who is this person to me".
- Class extensibility without touching Messaging, AD, or Catalog.
- Pairwise nym continuity has a home.
- Privacy boundary clear: relationship state never escapes vault as
  plaintext.
- AD generic via `resolve_group`; no `friends`-specific paths.
- Concrete migration path, not aspirational.
- Autonomous host decisions become explicit and bounded.

### Costs

- New layer to learn for operators.
- Two-source-of-truth window during Phase 2 bridge.
- Vault snapshot recheckpoint adds background I/O.
- Migration must complete at first start after Phase 2 deploy.
- Schema additively changes `pseudonym-vault.v1`.

### Constraints

- SQLite still serializes writers; per-fact UI latency depends on event
  log append speed, not snapshot recheckpoint cadence.
- Phase 2 bridge depends on Messaging cooperation.
- Predicate evaluation depends on node-operator-binding evidence —
  binding absence ≠ binding deny.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Vault seal fails during recheckpoint | Event log remains source of truth; recheckpoint retries with exponential backoff; operator notification on persistent failure. |
| Migration step fails partway through at first Phase 2 start | Bootstrap migration is idempotent; daemon stays in `migration-pending` until successful completion. |
| Class collision at startup | Readiness gate fails with `relationship-class-conflict` naming both producers. |
| SQLite projection diverges from event log | Replay equivalence checksum compare at startup; divergence triggers projection rebuild from log. |
| Peer-emitted fact attempts to enter layer | Inbound path does not exist by design; subsystem adapter translates peer-triggered events into local emissions with operator binding `actor/ref`. |
| Relationship state leaks to logs/traces | `privacy/profile` enforced per class; default `sealed-only`; redaction tests per Solution 028 anti-secret-leak pattern. |
| Operator archives class with active members | Allowed; members remain in event log; resolver excludes archived class from active queries; UI shows "X members of archived class". |
| Pairwise nym binding records grow unbounded | Per-context retention from performance profile; old bindings compacted past horizon. |
| Predicate evaluation runs with no node-operator-binding evidence | Returns `decision = deny` with `reason/code = "operator-binding-missing"`. No string-match fallback on participant id. |
| Middleware attempts to read sealed relationship state | Local capabilities do not expose membership lists to middleware; only `evaluate_predicate` returns a decision; direct list access fails closed. |
| Package declares predicate but operator never approved | Readiness gate refuses to enable package; predicate sits in `registered/pending-operator-approval`. |
| Predicate scope grows by accretion | `effect/scope` mandatory and unique per `(action/kind, effect/scope)`; readiness gate refuses duplicate scope from different packages without operator-acknowledged precedence. |

## Open Questions

1. Should `relationship-class.v1` allow per-class operator override of
   retention horizon (currently inherits from host default via
   `retention/profile-ref`)?
2. Does `pairwise-nym-binding-fact.v1` need context kinds beyond initial
   set (`messaging`, `ad-direct`, `agora-topic`, `inquirium-session`)?
3. When does pairwise nym continuity evidence get strong enough to be a
   policy input (deferred to a later proposal)?

## Next Actions

1. Add schemas in `orbidocs/doc/schemas`; mirror to
   `node/protocol/contracts`; extend `pseudonym-vault.v1` additively;
   update `local-contact.v1` documentation note.
2. Implement `node/local-relationship-core` (pure types, validators,
   projection reducer, group resolver, predicate evaluator).
3. Implement `LocalRelationshipStore` in daemon with vault-backed event
   log + SQLite projection per Solution 028.
4. Implement local-authenticated host capabilities and API surface.
5. Implement Phase 2 bridge in Messaging (read new, write new + legacy).
6. Implement AD `resolve_group` resolver.
7. Implement bootstrap migration step (one-shot at first start after
   deploy).
8. Clean up Contact Catalog (remove `friends`, raw handles, local
   membership).
9. Implement relationship-policy predicate evaluator and middleware
   `trust_requirements` declaration mechanism.
10. Add operator approval flow for predicate registration via package
    install path.
11. Add operator UI for class management, membership inspection,
    predicate registration, and decision audit.
12. Replay equivalence tests + privacy regression tests per Solution 028.

## Tracking

### MVP Milestones

| ID | Milestone | Status | Notes |
| --- | --- | --- | --- |
| S032-M1 | Contracts | done | Schemas are present in `orbidocs/doc/schemas`, mirrored into `node/protocol/contracts`, schema-gated with positive/negative fixtures, and include the additive `pseudonym-vault.v1` `local-relationship` kind plus unknown-kind preserve/fail-closed rules. |
| S032-M2 | Pure core | done | `node/local-relationship-core` provides schema-shaped types, validators, reducers, active group resolution, relationship-derived predicate evaluation, owner-scoped membership keys, and read-model filters without I/O or daemon coupling. |
| S032-M3 | Storage + daemon API | planned | Daemon-owned sealed `LocalRelationshipStore`, SQLite projection, local host capabilities, caller binding gate, seed classes, and restart replay/rebuild checks. |
| S032-M4 | Operator UI + trust requirements | planned | Class editor, membership inspector, predicate approval, decision audit, `trust_requirements[]` manifest parser, and readiness gate for unapproved requirements. |
| S032-M5 | Messaging bridge + bootstrap migration | planned | Idempotent migration from legacy contact membership, messaging read bridge, dual-write compatibility cache, canonical relationship facts, and multi-operator owner scoping. |
| S032-M6 | AD integration + Contact Catalog cleanup + hardening | planned | AD group resolver, Contact Catalog private-state cleanup, privacy/performance hardening, encrypted projection enforcement, and cross-component acceptance coverage. |
| S032-D1 | Phase 3 writes fully migrated | deferred | Post-MVP: messaging stops writing legacy tables directly. |
| S032-D2 | Phase 4 legacy deprecation | deferred | Post-MVP: legacy table and fact deprecation after consumer audit. |
| S032-D3 | Public protocol capability | deferred | Post-MVP only; the MVP boundary remains local-authenticated host API. |

### Capability Tracker

| ID | Work item | Status | Notes |
| --- | --- | --- | --- |
| S032-01 | Schema set: `relationship-class.v1` + `relationship-class-changed.v1` + `relationship-membership-fact.v1` + `pairwise-nym-binding-fact.v1` + `pairwise-nym-binding.v1` | done | Mutable class projection + append-only class change events + append-only membership + nym binding split into fact + projection. |
| S032-02 | Schema set: `relationship-policy-predicate.v1` + `relationship-policy-candidate.v1` + `relationship-policy-decision.v1` | done | Three-tier separation: declarative condition, host-internal read model, host-bound decision. |
| S032-03 | Extend `pseudonym-vault.v1` additively with `local-relationship` inner-entry kind; forward-compat ignore-but-preserve unknown kinds | done | Additive kind is schema-gated and implemented in `node/pseudonym-vault`; non-critical unknown entries preserve across reseal, while `critical=true` unknown entries fail closed. |
| S032-04 | Implement `node/local-relationship-core` (pure) | done | Types, validation, projection reducer, active group resolver, predicate evaluator, read-model filters. No I/O. |
| S032-05 | Implement `LocalRelationshipStore` in daemon | todo | Vault-backed event log + SQLite projection per Solution 028; encrypted-at-rest target. |
| S032-06 | Local-authenticated host capabilities + API surface | todo | All `local-relationship.*` capabilities; caller binding required. |
| S032-07 | Phase 2 bridge in Messaging | todo | Read new, write new + legacy; emit canonical + legacy facts. |
| S032-08 | One-shot bootstrap migration | todo | Idempotent; daemon stays in `migration-pending` until success; operator notification on completion. |
| S032-09 | AD `resolve_group` resolver | todo | Returns `ResolvedRelationshipCandidate[]`; AD performs own passport/capability checks. |
| S032-10 | Contact Catalog cleanup | todo | Remove `friends`, raw handles, local annotation. |
| S032-11 | Operator UI: class management + membership inspection | todo | Three read-model levels; default `operator-visible-summary` for inbox. |
| S032-12 | Replay equivalence + privacy regression tests | partial | Pure reducer replay/property coverage and vault unknown-kind roundtrip coverage exist; daemon projection rebuild and full privacy regex pass remain M3/M6 work. |
| S032-13 | Default class seeds for `contacts` and `friends` | todo | Written via `relationship-class-changed.v1` at first start. |
| S032-14 | SQLite projection encrypted-at-rest | todo | Cell-level AEAD with per-store key derived from vault. Phase 2 may temporarily allow `legacy_plaintext_cache` flag with operator warning. |
| S032-15 | Read-model level enforcement | partial | Pure read-model filters exist; daemon/UI/AD enforcement remains M3/M4/M6 work. |
| S032-16 | Host policy evaluator for predicates | partial | Pure evaluator composes predicate + membership + node-operator-binding evidence into candidate/decision; daemon dispatch integration remains M3/M4 work. |
| S032-17 | Middleware package manifest `trust_requirements` declaration mechanism | todo | Parser, operator approval flow, readiness gate enforcement, package install audit event. |
| S032-18 | Node-operator-binding evidence integration | partial | Pure evaluator requires a node-operator-binding evidence ref and rejects mismatches; verification against the daemon binding store remains M3/M4 work. |
| S032-19 | `owner/ref` multi-operator query scoping | partial | Pure membership keys and group resolution are owner-scoped; daemon defaults and multi-operator query surfaces remain M3/M5 work. |
| S032-20 | Phase 3 (writes fully migrated) | deferred | Future iteration. |
| S032-21 | Phase 4 (legacy deprecation + retention) | deferred | Future iteration. |
| S032-22 | Public protocol capability for federated consumers | deferred | Not in this iteration; local-authenticated host API only. |

## Notes

- Local Relationship Layer is the first Pseudonym Vault-backed
  application of relationship state. Messaging, AD, and Contact Catalog
  cease to own partial models.
- The three-tier predicate/candidate/decision split matches the
  `label != authority` invariant: candidate means "may be basis"; decision
  means "host bound a specific bounded effect"; real authority still flows
  through capability/passport/admission.
- Default class seeds are operator-editable defaults, not magic
  constants. They are written via the same `relationship-class-changed.v1`
  event as any operator-driven change; audit is uniform.
- The middleware boundary (no direct read of sealed state) is the
  single biggest implementation invariant. Any future capability that
  would let middleware see membership directly must be rejected at design
  review.
