# Proposal 047: Classification Label Propagation for Memarium-Touching Data

Based on:
- `doc/normative/20-vision/en/VISION.en.md` (Memarium spaces; constitutional dignity of data)
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. II.4, V.7 — Memarium as constitutional organ)
- `doc/project/40-proposals/036-memarium.md` (four memory spaces and space policies)
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md` (`disclosure/scope` as a partial classification axis)
- `doc/project/40-proposals/032-key-delegation-passports.md` (passport as gate-level authority)
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md` (Agora egress surface)
- `doc/project/40-proposals/042-inter-node-artifact-channel.md` (INAC direct exchange surface)
- `doc/schemas/whisper-signal.v1.schema.json` (current partial disclosure-scope handling)

## Status

Draft

## Date

2026-04-19

## Executive Summary

Today, Memarium classification (Personal / Community / Public / Crisis) is a
**property of the place of writing**: a fact is "private" because it sits in the
Personal space. Once read, the data loses its classification — downstream
components (Monus, Sensorium, Agora publishers, Whisper senders, INAC
forwarders) receive plain values and must reconstruct, heuristically, what
policy originally applied to them.

This proposal shifts classification from a **location property** to a **data
property**. Every fact produced or consumed by a Memarium-touching component
carries a `classification` label. Every protocol envelope that crosses a
component boundary carries it too. Egress components (Agora, Whisper, INAC,
bus) refuse publication when the label is incompatible with the destination.
Lowering the classification (declassification) becomes an **explicit,
passport-gated, audit-logged operation** with one-shot or persistent exception
modes.

The pattern is well-known under several names: **taint tracking** (Perl, PLD
Linux tooling, static analyzers), **information-flow control / IFC** (Jif,
HiStar, Asbestos, LIO, FlowCaml), **mandatory access control with sensitivity
labels** (Bell-LaPadula, MLS databases), and — in rendering pipelines —
"**never interpret data as code without an explicit parser boundary**" (CSP,
Trusted Types). This proposal adopts the pragmatic 80/20 of that family: label
as data, enforcement at edges, declassification as a privileged operation.

The key decisions are:

1. `Classification` is defined as a first-class data type with a **small, boring
   lattice** (`Public < Community < Personal`) — no `Internal`/`Secret`/
   `Restricted` sub-tiers until there is concrete edge enforcement for them.
2. `source_tier` (immutable, assigned at first stamping) is **separate** from
   `effective_tier` (derived from `source_tier` and the `declassify_trail`).
   Declassification never rewrites the source.
3. All Memarium-touching envelopes carry a **required** `classification` field.
4. Join semantics on merge are **most-restrictive-wins** (`Personal ⊔ Public =
   Personal`). Aggregation, summarization, k-anon, embedding — none of these
   auto-declassify; each produces a new artefact with its own transformation
   record or an explicit `DeclassifyFact`.
5. Declassification is a **passport-gated host capability**
   (`memarium.declassify`) whose grant is **narrow by construction**: it binds
   `from → to`, surface, `topic_class`, TTL, mode (one-shot / persistent),
   rationale, caller, and `correlation_id`. A bare `memarium.declassify` scope
   without those bindings is invalid.
6. `bound_subjects` is a **projection-aware field**: full set for
   Personal/Community, hashed/counted/redacted for Public, to avoid the
   protection field itself becoming a leak.
7. Ingress without a label defaults to **highest restriction** (`Personal`) +
   **visible quarantine** with operator UX (accept-as-X / reject / declassify).
8. Enforcement is **edge-first**: egress guards at Agora / Whisper / INAC /
   bus publishers / export-backup refuse non-conformant publication. The
   interior of Memarium can remain *label-aware* long before it is
   *taint-complete*.
9. The existing `disclosure/scope` in Whisper v1 is re-expressed as a
   **projection** of `effective_tier` onto the distribution axis, not a
   parallel concept.
10. An explicit **denial-code vocabulary** is published for classification
    failures (see §9), reusing the reason-dictionary discipline already
    adopted for Memarium dispatch.

## Context and Problem Statement

Memarium proposal 036 establishes four spaces with distinct encryption,
retention, and forget policies. Proposal 013 defines `disclosure/scope`
(`private-correlation`, `federation-scoped`, `cross-federation`,
`public-aggregate-only`) as a **per-message** disclosure posture carried inside
Whisper bodies. Proposal 036 treats space as an organizational structure
inside Memarium.

Neither proposal binds the classification to the **data itself** as it flows
across components. In practice this leaves three gaps:

- **Composition leakage.** When Monus reads a fact from Personal and hands a
  derived summary to Sensorium, Sensorium has no machine-readable way to know
  that the derivative is Personal-origin. Subsequent enaction may publish it.
- **Forensic-only accountability.** Answering "how did this Personal-origin
  fragment appear in a Public artefact?" requires reconstruction from traces,
  not a query over data.
- **Inconsistent axes.** `disclosure/scope` in Whisper overlaps with space
  classification but is neither derived from nor synchronized with it. A
  `private-correlation` Whisper built from Personal Memarium data and a
  `private-correlation` Whisper built from Community data carry the same
  wire-level posture with very different source postures.

Additionally, proposals around crisis (039), ingest (041), inter-node channel
(042), and Agora relay (035) all describe egress surfaces whose acceptance
policy would benefit from a uniform, data-carried classification — instead of
per-surface bespoke checks.

## Goals

- Define `Classification` as a data type with a tier lattice and a preserved
  declassification history.
- Make classification **a required field** on every Memarium-touching envelope
  (reads, writes, bus events, outbound Agora/Whisper/INAC bodies).
- Specify **propagation semantics** (join on merge, inheritance on derivation).
- Specify **declassification** as a passport-gated host capability with
  one-shot and persistent-exception modes, both recorded as facts.
- Specify **egress guards** at Agora, Whisper, INAC, and bus surfaces.
- Unify `disclosure/scope` (Whisper v1) with `classification` as a projection,
  eliminating the dual-axis ambiguity.

## Non-Goals

- Full information-flow control with runtime propagation inside arbitrary
  computation (Jif-class completeness). This proposal adopts envelope-level
  propagation + edge enforcement, not whole-program IFC.
- Per-field labels. Granularity in v1 is **per fact**; the text/body field
  always inherits the fact's tier. Per-field labels are deferred.
- Covert-channel analysis. Metadata about queries (who asked for what) is out
  of scope for v1; this proposal protects data, not flow metadata.
- Cryptographic enforcement of labels (sealed computation, confidential
  enclaves). This proposal is a process-of-record construct, not a TEE.
- Retroactive re-labeling of pre-existing Memarium facts. Migration guidance is
  sketched but full backfill is a separate workflow.

## Decision

### 1. `Classification` as a First-Class Data Type

```
Classification {
    source_tier:        Tier,                // required, IMMUTABLE after first stamp
    effective_tier:     Tier,                // derived = source_tier unless a
                                             //   currently-valid DeclassifyFact
                                             //   in declassify_trail lowers it
    provenance:         SpaceOrigin,         // where the data first entered the system
    bound_subjects:     BoundSubjects,       // projection-aware (see §5)
    declassify_trail:   Vec<DeclassifyFact>, // append-only, possibly empty
}

Tier = Personal | Community | Public
// Crisis is orthogonal — a flag on the bearer, not a tier — because Crisis
// governs "who may operate at all", not "what may be disclosed".
//
// This tier set is intentionally small. Sub-tiers (Internal, Secret,
// Restricted, ...) are NOT introduced in v1 — added only when a concrete
// edge guard exists that would enforce them. Decorative taxonomy is a
// non-goal.
```

The tier forms a **small boring lattice**:

- `Personal` as the top (most restrictive),
- `Public` as the bottom (least restrictive),
- `Community` strictly between them,
- join `⊔` = *most restrictive wins* (`Personal ⊔ Public = Personal`),
- meet `⊓` = *least restrictive wins* (used only for declassification reasoning,
  never for merge).

**`source_tier` is immutable.** It is stamped once (at write into Memarium,
at ingress from outside, or by explicit operator stamping out of quarantine)
and is never rewritten. This preserves the original dignity claim as a fact.

**`effective_tier` is derived**, not stored as mutable state. At read time it
is computed as:

```
effective_tier(c) = min_in_lattice(
    c.source_tier,
    latest_active(c.declassify_trail).to   // if any DeclassifyFact is still valid
)
```

A `DeclassifyFact` is *active* when: (a) its TTL has not expired, (b) its
scope constraints (surface, topic_class) match the current request, (c) it
has not been revoked via the shared revocation feed, and (d) for one-shot
mode, it has not yet been consumed.

Declassification **never rewrites** `source_tier` or prior trail entries.
This is the "facts, not overwriting state" discipline applied to
classification.

### 2. Required Field on All Memarium-Touching Envelopes

Classification is added as a **required** field to:

- `MemariumReadResult`, `MemariumWriteRequest`, `MemariumIndexEntry`,
  `MemariumBundleDigest`,
- `LifecycleEvent` variants that carry fact-derived payloads,
- outbound `agora-record.v1` envelopes containing Memarium-derived bodies,
- `whisper-signal.v1` bodies (see §8 for the projection unification),
- INAC artefact envelopes (per proposal 042).

"Required" is the stable v1 target: no schema `default` and no silent
classification loss at protocol boundaries. During the migration window,
Memarium may accept missing labels under an explicit `LegacyStampThenWarn`
mode: absence is stamped as `Personal` plus ingress quarantine, a warning is
emitted, and the fallback is counted. `StrictRequired` may be enabled only
after the configured date and an observed zero-fallback window (§10).

### 3. Propagation by Join on Merge — No Auto-Declassification

Whenever two classified values are combined into a derived value, the
derivative carries `source_tier = join(source_tier_a, source_tier_b)`. This
rule is:

- **monotonic upward** (a derivative is at least as restrictive as any input),
- **local** (no global dataflow analysis needed),
- **cheap** (a single enum comparison).

`bound_subjects` is unioned then re-projected per §5. `provenance` becomes a
two-parent reference. `declassify_trail` is unioned and time-ordered.

**Aggregation does not auto-declassify.** Histograms, summaries, k-anonymized
views, redactions, and embeddings are **not** privileged with respect to
classification. Each such transformation produces a new artefact whose
classification is, by default, the join of its inputs. Lowering it requires an
explicit `DeclassifyFact` attached to the output (§4).

`classification.v1` carries the label and the `declassify_trail`; it does not
embed `TransformationFact`. A `TransformationFact` may be stored as separate
Memarium provenance and referenced from `DeclassifyFact.evidence_ref`, but it
is evidence only in v1: it never lowers `effective_tier` without the explicit
declassification act.

Without that explicit act, a "summary" of Personal data is Personal. "Summary"
is not a magic bypass.

**Rust shape — staged, not all-at-once.** To avoid prematurely coloring the
entire codebase:

1. **First**: `Classified<T>` as an **envelope type at protocol boundaries**
   only (write, read, index, cache, observe, egress). Schema-level propagation
   is sufficient for label-awareness.
2. **Later, where it pays**: `Tainted<T>` as a newtype with no direct `Deref`
   and an audited `declassify()` method, introduced incrementally in modules
   whose internal composition is risky.
3. A `Join` trait implementation composes classifications without touching
   the payload.

Introducing `Tainted<T>` across the entire Rust codebase before egress guards
are in place would slow iteration without adding enforcement. Edge-first.

### 4. Declassification as a Narrow, Passport-Gated Host Capability

A new host capability is introduced. **The grant is narrow by construction**:
a bare `memarium.declassify` scope without binding constraints is rejected by
the gate. Every declassification request must fully specify:

```
memarium.declassify {
    fact_id:           FactId,          // exact subject
    from:              Tier,            // must equal current effective_tier
    to:                Tier,            // must satisfy to < from in the lattice
    surface:           Surface,         // "agora" | "whisper" | "inac" | "export" | "bus"
    topic_class:       String,          // the semantic class this declassification applies to
    mode:              OneShot
                       | PersistentForTopicClass { ttl: Duration },
    rationale:         String,          // operator-accepted, stored verbatim
    caller:            PassportRef,     // whose passport presented the grant
    correlation_id:    CorrelationId,   // ties request ↔ DeclassifyFact ↔ ledger
}
```

A `DeclassifyFact` appended to the trail mirrors this shape plus issuance
time, expiry, revocation anchor, optional `evidence_ref`, and a `consumed_at`
marker for one-shot mode.

Authorization:

- **one-shot** declassification within one tier step (`Personal → Community`
  or `Community → Public`) requires a passport with scope
  `memarium.declassify:one-shot` bound to the specific `surface` and
  `topic_class` — typically A0 (operator), rarely A1 with a narrow per-topic
  binding,
- **two-step** declassification (`Personal → Public` directly) is **not**
  permitted; it must proceed via two explicit acts, each separately audited,
- **persistent exceptions** are recorded as `policy facts` in the Memarium
  ledger, subject to the same revocation feed composite (local + static +
  seed-directory) already used for nym revocation.

The surface + topic_class binding means a declassification authorized for
"Whisper publication of `workplace-retaliation-pattern`" does **not** permit
Agora publication of the same fact — a separate declassification act is
required.

Every declassification appends a `DeclassifyFact` to the subject's
`declassify_trail` and emits an audit entry with the same `correlation_id`
discipline as other passport-gated calls.

### 5. `bound_subjects` as a Projection-Aware Field

The `bound_subjects` set names the subjects whose dignity interests attach to
the fact. Carried verbatim into a `Public` artefact, it can itself become a
leak (publishing a redacted summary while naming the subjects it redacts).

`bound_subjects` is therefore defined as a **tier-dependent projection**:

```
BoundSubjects = {
    personal_or_community: Option<Vec<SubjectRef>>,   // full, only when effective_tier >= Community
    public_projection:     Option<PublicProjection>,  // used when effective_tier == Public
}

PublicProjection = {
    subject_set_hash:   Bytes32,         // stable hash of the full set, salted per fact
    count:              u32,             // cardinality only
    redacted_refs:      Option<Vec<RedactedSubjectRef>>,  // explicit, if operator-approved
}
```

Egress to Public surfaces **must** carry `public_projection`, never the full
set. Computing the projection is part of the declassification act (§4) or of
an explicit aggregation producing a Public artefact. The full set is never
reconstructable from the projection alone.

### 6. Ingress Defaults to Highest Restriction + Visible Quarantine

Data entering the node without a legible label is stamped `source_tier =
Personal` and placed in an ingress **quarantine**. Promotion out of
quarantine requires an operator act (accept-as-tier, reject, or declassify
via §4). "No label" never defaults to `Public`.

This rule applies at:

- federation ingress when peers send schemas older than v-with-classification,
- local module enqueueing when A1 code has not yet migrated,
- import / restore flows where provenance is unclear.

**Operator UX is a first-class requirement**, not an afterthought. Without
it, a safe system is an unusable system. The quarantine surface must expose:

- a queue view (count, oldest, breakdown by provenance),
- per-item actions: **accept-as Personal / Community / Public**, **reject**,
  **declassify** (which opens the §4 flow),
- batch actions for obvious cases (e.g. all from federation peer X as
  Community),
- an audit record of every operator action with `correlation_id`.

A CLI surface (`orbictl memarium quarantine ...`) is the minimum; a TUI/web
surface is recommended but not required for v1.

### 7. Edge-First Enforcement

Enforcement lives at **egress surfaces**, not inside engines. The interior
of Memarium can remain *label-aware* (schema carries the field, reads expose
it) for a long time before it is *taint-complete* (every internal
computation propagates labels through typed channels). Edge enforcement is
the cheap high-value layer; interior propagation is the expensive one and
can be staged.

| Surface                 | Guard rule                                                                            |
|-------------------------|---------------------------------------------------------------------------------------|
| Agora publish           | `effective_tier` must be `Public`; `bound_subjects` must be `public_projection` only. |
| Whisper send            | `effective_tier` must project onto a `disclosure/scope` compatible with the posture.  |
| INAC direct exchange    | `effective_tier` ≤ agreed peer tier (by trust class).                                 |
| Bus publisher           | Consumers see `classification`; consumers self-filter by their own scope.             |
| Export / backup         | Classification is preserved verbatim in the exported bundle.                          |

This mirrors the **dispatch-gate** pattern already used for authorization:
thin, stable guards at boundaries, engines trust their inputs.

### 8. Unification with `disclosure/scope`

Whisper v1's `disclosure/scope` is redefined in v1.1 (non-breaking superset)
as a **projection** of `effective_tier` onto the distribution axis:

| `effective_tier` | Permissible `disclosure/scope`                         |
|------------------|--------------------------------------------------------|
| Personal         | `private-correlation`                                  |
| Community        | `private-correlation`, `federation-scoped`             |
| Public           | any of the four                                        |

Whisper senders compute the projection at construction time; ingress-side
validators reject envelopes whose declared `disclosure/scope` is not permitted
by the `effective_tier`.

### 9. Denial-Code Vocabulary

Classification failures reuse the Memarium reason-dictionary discipline. The
v1 vocabulary publishes at minimum:

| Wire `reason`                   | When                                                                                        | HTTP  |
|---------------------------------|---------------------------------------------------------------------------------------------|-------|
| `classification_missing`        | Envelope lacks a required `classification` field at a guarded surface.                      | 400   |
| `classification_mismatch`       | `effective_tier` incompatible with destination (e.g. Personal → Agora publish).             | 403   |
| `declassification_required`     | Destination would be reachable only after a valid `DeclassifyFact`; none present.           | 403   |
| `declassification_scope_expired`| A `DeclassifyFact` exists but its TTL elapsed, it was revoked, or its `surface`/`topic_class` does not bind. | 403 |
| `bound_subjects_not_public`     | Public-bound egress carries full `bound_subjects` instead of `public_projection`.           | 400   |
| `quarantined`                   | Read/publish touches a quarantined fact that has not been accepted by the operator.         | 409   |
| `source_tier_immutable`         | A request attempted to rewrite `source_tier` rather than append a `DeclassifyFact`.         | 400   |

Each denial carries `correlation_id` and an audit entry `denied:<kebab>` per
the existing Memarium audit-decision discipline.

### 10. Migration

- Phase M1: add `classification` as *optional* to envelopes; Memarium stamps
  reads with the space's tier; no enforcement yet. **Label-first.**
- Phase M2: run Memarium HTTP writes in `LegacyStampThenWarn`; old-schema
  ingress and missing labels map to `Personal` + quarantine per §6, emit
  warning diagnostics, and increment
  `fallback_stamped_facts_per_space_per_day`.
- Phase M2.5: flip to `StrictRequired` only after `strict_not_before` and after
  the fallback metric is zero for the configured observation window. The
  reference daemon default is no earlier than 2026-06-30 plus seven zero days.
- Phase M3: activate egress guards on Agora / Whisper / INAC.
- Phase M4: introduce `memarium.declassify` and wire the passport scope.
- Phase M5: projection rule enforced at Whisper validator.
- Phase M6: `Tainted<T>` rolled through Memarium-touching Rust code.

Each phase is independently releasable.

## Rationale

### Why data-level, not place-level

Place-level classification is correct only as long as data does not move. The
moment a fact is read, summarized, re-encoded, or forwarded, its "place" is
lost but its dignity is not. Data-level labels preserve the dignity across
composition — exactly the property needed for a constitutional organ whose
mandate is "preserve what should not disappear" together with "do not leak
what should not appear."

### Why join-on-merge and not a smarter policy

Join-on-merge is monotonic, local, and predictable. Smarter policies (e.g.,
"average" or "drop if proportion is small") are heuristic and fragile, and
they destroy audit value. Label creep is acknowledged (§Trade-offs) and
addressed via explicit declassification, not implicit relaxation.

### Why declassification is passport-gated

Declassification is a *political act*: someone claims the right to weaken a
protection that was established for a reason. The node already has a gate for
political acts — capability passports. Using the same gate preserves
stratification (gate authorizes, engine performs) and reuses the audit /
revocation machinery we already built.

### Why edge-first enforcement

Inside the engine, treating every merge as an enforcement point is both
expensive and unnecessary — most merges are interior computation that will
never leave the process. Enforcing at egress surfaces catches leakage *at the
moment of disclosure*, which is the only moment that matters constitutionally.

### Why align with `disclosure/scope`

Two axes for the same concept invite drift and misconfiguration. The Whisper
axis was a local expression of what is fundamentally the same classification
question. Expressing one as a projection of the other removes duplication
without breaking existing senders.

## Trade-offs and Open Questions

- **Label creep.** Everything composed from Personal inputs becomes Personal.
  Mitigation: projection-producing capabilities (k-anonymization, counts,
  histograms) that yield `Public` outputs **only through explicit declassify
  with a `PersistentForTopicClass` exception**. Never implicitly.
- **Covert channels via metadata.** Query patterns themselves can leak
  classification. v1 does not address this; v2 may extend classification to
  queries.
- **Granularity.** Per-fact labels may be too coarse for rich facts. v1 accepts
  this; per-field is a v2 concern.
- **Interop with older federations.** Handled via §6 quarantine rule;
  federations that never upgrade will see all Memarium-touching content as
  `Personal` at their ingress.
- **Crisis orthogonality.** Crisis is a flag, not a tier, to avoid conflating
  "who may act" with "what may be disclosed." This may need revisiting if a
  crisis-only disclosure scope emerges (currently not required).
- **Backfill.** Existing Memarium facts pre-dating §2 need a one-time migration
  pass assigning `classification` from their host space. This is a separate
  workflow, not part of normal operation.

## Relationship to Other Proposals

- **036 (Memarium).** Classification becomes the data-level expression of
  space policies; spaces remain the organizational home, classifications
  travel.
- **013 (Whisper).** `disclosure/scope` becomes a projection (§8); unchanged
  for senders at v1.0, enforced at v1.1.
- **032 (Key delegation passports).** The declassification capability reuses
  the passport + scope + revocation machinery; no new authorization primitive.
- **035 (Agora relay).** Egress guard §7 is added to the Agora publish path.
- **041 (Agora ingest attestation).** Ingress stamping §6 integrates with
  attestation.
- **042 (INAC).** Egress guard §7 is added to INAC direct exchange; INAC is
  the natural surface for `private-correlation` traffic.
- **039 (Crisis seed).** Crisis remains orthogonal per §1.

## Implementation Sketch

1. New schema `orbidocs/doc/schemas/classification.v1.schema.json` defining
   `Classification`, `Tier`, `DeclassifyFact`, `BoundSubjects`,
   `PublicProjection`.
2. Rust crate `classification` (or inline in `memarium`) exposing
   `Classified<T>` at boundaries, `Join`, `DeclassifyFact`, and
   `effective_tier()` as a derived function. `Tainted<T>` is deferred and
   introduced per-module later (see §3 staging).
3. Memarium envelope types extended with required `classification` field
   carrying both `source_tier` and `effective_tier`.
4. `memarium.declassify` added to `memarium_integration.rs` dispatch table
   alongside existing host capabilities; wired to passport gate with a new
   scope constant and binding validation (§4).
5. Egress guards added as middleware layers at Agora publish, Whisper send,
   INAC forward, and export/backup paths; each emits denial codes from §9.
6. Whisper v1.1 schema adds the projection rule as an `allOf` conditional
   tying `disclosure/scope` to `effective_tier`.
7. Ledger entries for `declassify` use the same `correlation_id` and
   `denied:*` / `allowed:*` discipline as other gate-audited ops.
8. **Hook-point inventory in Memarium docs.** Proposal 036 and
   `doc/project/60-solutions/memarium.md` are updated with an explicit
   subsection "Where labels live" enumerating the exact hook points:
   - `memarium.write` — stamps `source_tier` from the target space,
     initializes empty `declassify_trail`.
   - `memarium.read` — computes `effective_tier` at response time, attaches
     full `Classification` to the read envelope.
   - `memarium.index` — carries `effective_tier` for index-time filtering;
     index entries that would leak across tiers are partitioned per tier.
   - `memarium.cache` — cache key includes `effective_tier`; cross-tier cache
     hits are disallowed.
   - Observe (`PeerMessageHandler` middleware slot) — the observed payload
     carries `classification`; observers that re-emit must preserve it.
   - `memarium.crisis_status` / `memarium.crisis_resolve` — Crisis is
     orthogonal (§1), so classification is passed through unchanged.
9. CLI `orbictl memarium quarantine {list,accept,reject,declassify}` for
   operator UX (§6).
10. Property-test suite per Acceptance Criteria, runnable in CI.

## Acceptance Criteria

- `Classification` schema published and referenced by Memarium envelopes.
- All Memarium host-cap responses carry `classification` with distinct
  `source_tier` and `effective_tier`.
- Agora publish, Whisper send, INAC forward, and export/backup each reject
  at least one regression test demonstrating classification-mismatch denial,
  with the specific denial code from §9.
- `memarium.declassify` host capability implemented with narrow grant binding
  (surface + topic_class + TTL + mode + caller + correlation_id), both
  one-shot and persistent-exception modes, audited, and subject to revocation.
- A `memarium.declassify` request lacking any of the required bindings is
  rejected with `reason: declassification_scope_expired` or
  `classification_mismatch` as appropriate.
- **Property tests** for classification semantics published and green:
  - `join` is idempotent: `a ⊔ a = a`,
  - `join` is commutative: `a ⊔ b = b ⊔ a`,
  - `join` is associative: `(a ⊔ b) ⊔ c = a ⊔ (b ⊔ c)`,
  - merge never lowers `source_tier` of any input,
  - `effective_tier ≤ source_tier` always (in the lattice order where
    Personal is top),
  - Agora egress rejects every non-`Public` `effective_tier`,
  - Whisper `disclosure/scope` never exceeds the projection of
    `effective_tier`,
  - Public-surface egress rejects every envelope carrying full
    `bound_subjects.personal_or_community`.
- Operator UX: CLI `orbictl memarium quarantine {list,accept,reject,declassify}`
  implemented and covered by integration tests.
- Operator documentation (`orbidocs/doc/ops/`) includes a runbook for
  declassification and for handling ingress quarantine.
- Proposal 036 and `orbidocs/doc/project/60-solutions/memarium.md` updated
  with an explicit "where labels live" section covering read / write / index
  / cache / observe paths (see §Implementation Sketch step 8).

## Future Work

- Per-field classification (v2).
- Query-metadata classification for covert-channel mitigation.
- Federation-level label negotiation (what a peer accepts) replacing the
  current static trust-class mapping.
- Cryptographic enforcement via sealed computation for high-assurance
  deployments.
- Automated label-creep detection (monitoring the proportion of facts at each
  tier over time).
