# Capability-Limited Restrictions

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`
- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`
- `doc/project/50-requirements/requirements-015-newcomer-surface-limits.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`

Related schemas:

- `participant-capability-limits.v1`
- `participant-effective-limits.v1`
- `surface-access-policy.v1`
- `participant-restriction-source.v1`
- `participant-restriction-sources.v1`
- `responsibility-effect-request.v1`
- `responsibility-effect-receipt.v1`

## Status

Implemented solution.

This solution captures the implemented `participant-capability-limits.v1`
runtime slice. Newcomer and membership/sponsorship policies may project into
the same effective-limits vocabulary, but their social-policy source artifacts
remain outside this solution.

The source-aware social-correction adapter is implemented and requalified on
2026-10-10 for the explicit one-host test-subject profile. The reviewed evidence
proves targeted A correction while the profile is disabled, independent
B/operator restrictions, protected access, replay and expiry during service outage.
This extension is outside hard MVP and does not qualify sanctions against real
participants, complete entry-policy integration or the full social appeal process.

## Date

2026-07-03

Integration review: 2026-10-10.

## Executive Summary

Capability-Limited Restrictions are the host-owned enforcement layer for
temporarily reducing a participant's operational influence on specific
surfaces. The model is layered: protected floors remain available, hard blocks
deny selected privileged operations, and soft factors alter ranking or cooldown
without silently becoming bans.

The solution is intentionally auditable rather than folkloric. Imports are
schema-gated, stale or already-dead records are rejected, clear operations can
carry `reason/ref`, and replay reconstructs the current participant restriction
state from durable facts.

## Context and Problem Statement

Orbiplex needs practical ways to reduce harm without turning every incident into
a global identity ban. Newcomer limits, probation, sponsor liability, fraud
holds, and operator sanctions all need a common lower layer that can say:

```text
participant X may not use operation Y until time T
participant X is ranked lower for operation family Z
participant X has slower cooldown for operation family W
```

Before this solution, such restrictions risked becoming scattered across
procurement, messaging, governance, and UI-specific checks.

## Proposed Model / Decision

The participant capability-limits layer is a local host enforcement read model.
It consumes operator-imported restriction records and clear tombstones, then
exposes deterministic decisions to operation gates. The v1 record has no signature
field; schema validation and its `decision/author` field are not verification of a
social verdict. The signed-decision adapter verifies issuer, mandate,
target, scope, validity and revocation before admitting a case restriction.

Rules:

- protected floor operations cannot be hard-blocked by this layer;
- hard blocks fail closed for configured privileged operation families;
- soft priority factors affect ranking/scoring;
- soft rate-limit factors affect cooldown;
- stale imports do not overwrite newer facts or clear tombstones;
- already-expired hard blocks are rejected before mutating state;
- operator-visible refresh events are metadata-only.

### Social Correction Boundary

[P051](../../40-proposals/051-swarm-membership-and-reputation-bootstrap.md#25-close-the-correction-loop-without-creating-another-authority-plane)
owns case procedure, reviewer independence, appeal and reputation consequences.
S040 neither selects judges nor evaluates the truth of allegations. A valid
review result is input to a separately authorized application step, not an
automatic command. Room moderation and Corpus deliberation roles do not confer
restriction authority.

The implemented local adapter composes case-scoped effects into the existing
enforcement path and preserves these boundaries:

1. **Targeted correction.** Retract only effects derived from the challenged
   decision. Recompute remaining sanctions and entry defaults; do not translate
   one successful appeal into participant-wide `clear` or an unrestricted `allow`.
2. **All writers accounted for.** Existing operator imports remain independent
   sources. Serialize/fence their changes with case projections and expose
   unresolved legacy attribution; no adapter may overwrite unseen restrictions.
   Before enabling the adapter, inventory records and clear tombstones into a
   pinned baseline, preserve them as `legacy-operator-source` without inventing
   authorship, and verify effective-value equivalence for valid sources at the same
   evaluation time. Invalid/ambiguous sources retain evidence and a typed refusal;
   compatibility must not preserve a legacy fail-open result. Restart must resume
   this cutover before accepting case effects or corrections.
3. **Bound authority.** Pin the decision and source-set revision, then recheck
   current authority, revocation and time before applying a new restriction.
   An exactly accepted narrowing withdrawal retains its admission proof after
   mandate, policy or profile revocation; it grants no new authority. A fresh
   correction still requires an eligible current mandate. Historical replay is
   evidence, not permission to repeat an expired effect.
4. **Separate validity.** Each case effect, including soft penalties, has its own
   expiry. Admission must stop expired effects even if reconciliation is down.
   Removing one source must not renew another source's lifetime.
   Malformed or indeterminate validity is a typed recovery/admission failure, not
   evidence of expiry: refuse affected privileged admission with diagnostics while
   preserving the protected floor. A blocked appeal retains its prior finding as
   history; effects follow P051's explicit stay/validity policy, not an automatic
   participant clear or extension.
5. **Truthful recovery.** Persist the admitted transition before idempotent
   enforcement and record its outcome. Pending correction is visible; replay
   converges without duplicate effects. External harm requires compensation or
   corrective publication, not deletion of history.
6. **Usable protected access.** Reasons and bounded appeal remain accessible
   despite the affected restriction, Room removal or muted notifications. Soft
   cooldowns must not make the protected floor unusable; ordinary bounded
   anti-abuse protections remain in force.

### Implementation Seams and Compatibility Gate

The 2026-10-10 inspection found reusable code in
`node:daemon/src/execution_host.rs` (import/clear and operation admission),
`node:daemon/src/lib.rs` (validation, commit records and policy snapshots), and
`node:daemon/src/tests/participant_policy.rs` (protected floors and operator
routes). Reuse these hooks and their replay stream; do not introduce another
restriction engine in UI, Room, Corpus or a case service.

The adapter uses `node:daemon/src/responsibility_host.rs` for admitted policies,
mandates, mirrored procedural facts, source-set CAS and durable receipts.
`participant-restriction-source.v1` is the authoritative source fact; the source
set is an independently rebuildable projection. Every operator/case/admission
writer participates in the same host gate. Effect outboxes serialize changes per
source and retained retraction revisions fence late original effects.

v1 remains the operator-input format. Migration pins original records and clear
tombstones to a digest-bound baseline, preserves unknown authorship as
`legacy-operator-source`, and separates indefinite legacy soft factors from hard
expiry. Host replay resumes interrupted migration before case admission. Invalid
records or tombstones retain diagnostics and refuse affected privileged admission;
they no longer disappear through the former expiry parser's `.ok()?` path.
Protected case inspection and appeal survive this refusal.

| Boundary | Local behavior |
| --- | --- |
| Composition | Active hard blocks union; active per-operation soft factors take the minimum. Evaluation uses host observation time. |
| Correction | Retract only named effects of the bound decision. Other cases, operator sources and independent authorization remain intact. |
| v1 import | Write the operator source through the common gate, retaining raw evidence and timestamp conflicts. |
| v1 export | Refuse source compositions or targeted retractions that cannot be faithfully represented. |
| Legacy wide DELETE | Refuse active or unresolved case sources; use revision-bound operator-source retraction. |
| Expiry / outage | Independently expired soft/hard effects cease at admission without a live case service or Scheduler. |
| Failure | Pending, refusal and applied/retracted receipts remain distinct; timeout never means success. |

Canonical schemas and Node mirrors are registered in Schema Gate. The contract
and ownership guide is `node:docs/development/LOCAL-ACCOUNTABILITY-CONTRACT.md`;
the original historical report and conformance are retained under
`node:docs/evidence/local-accountability/2026-10-10-qualified-local/` (18 runtime
cases and two conformance bindings). The corrected-source review-v2 execution
passed 18 runtime cases and two conformance bindings, with 713 conformance checks
across 15 suites and 27 qualifier tests (one positive and 26 negative).
Its report is `node:docs/evidence/local-accountability/2026-10-10-review/passage-3/report.json`,
with SHA-256 `4c16aa570954c29bb2cb1c45317f837c9dad563e9d8b2871ad2dbaea96d91b72`.
The qualification and review findings remain beside that report and in the
parent review README; historical and failed-attempt bytes remain unchanged.

Host observation time now governs current operation admission, including old
envelopes whose `created_at` precedes a restriction. Envelope time remains
historical metadata; it is not authority to bypass current restrictions. A
checkpoint containing only legacy limits cannot restore source corrections.
New responsibility-bearing checkpoints require the matching SQLite source store;
consistent full data-directory backup is required, and portable backup/restore
is not qualified by the local profile.

The pure `node:membership-policy-core/src/lib.rs` projectors already retain source
references and accept sanction/appeal overlays, but later overlays replace earlier
values for the same operation. The case adapter composes admitted source facts independently; it does not
activate this pure entry-policy projector or make overlay order authoritative. P051 owns policy admission; S040's
existing protected floor and independent operation authorization still apply.

Use S028 temporal facts/projections for source tracking and a replayable outbox
for cross-store application; S020 Scheduler for bounded reconciliation; S043
causal/receipt primitives for effect evidence; and S039 for recipient-bound notices.
Their receipt, queue or delivery success is not the case's social outcome.
Case-owned deadlines survive scheduler loss; admission-time validity checks do not
depend on a cleanup launch. Without Scheduler or another declared trigger there is
no baseline promise of proactive timeout notification. Read-only inspection may
show overdue state; durable correction resumes only on an authorized execution
path. Do not add a private timing engine to S040.

## Must Implement

### Capability Limits Contract

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- define the canonical restriction artifact;
- reject unsafe or unknown hard-block targets;
- keep protected floor operations unblocked;
- validate participant ids, reason refs, expiry windows, and soft factors.

Status:

- `done`

### Schema-Gated Import and Clear

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- reject invalid, oversized, stale, already-dead, or already-expired imports;
- preserve monotonic `recorded-at` and `last_cleared_at` semantics;
- accept optional bounded `reason/ref` when clearing restrictions;
- emit clear tombstones instead of deleting history.

Status:

- `done`

### Operation Enforcement Hooks

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- enforce hard blocks on the first privileged operation set;
- apply priority-factor penalties in procurement ranking;
- apply rate-limit-factor cooldowns at admitted operation gates;
- keep participant-side accept/dispute/reject controls separate from operator
  execution controls.

Status:

- `done`

### Durable Replay and Operator Visibility

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- append imports and clear tombstones to the daemon commit log;
- replay the current read model deterministically;
- expose import, list, detail/export, and clear routes;
- emit metadata-only refresh events for operator surfaces.

Status:

- `done`

## May Implement

### Newcomer Effective-Limits Projection

Based on:

- `doc/project/50-requirements/requirements-015-newcomer-surface-limits.md`
- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`

Related schemas:

- `participant-effective-limits.v1`
- `surface-access-policy.v1`

Responsibilities:

- project entry profile, surface access policy, sanctions, and appeals into one
  effective-limits read model;
- keep social membership policy outside the enforcement primitive;
- allow newcomer defaults and sanctions to share operation vocabulary without
  sharing authority.

Status:

- `post-MVP`

### Source-Aware Social-Correction Adapter

Based on:

- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`
- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Responsibilities:

- map admitted case effects into existing restriction enforcement without losing
  source, operation scope or per-effect validity;
- reconcile independent operator imports, targeted appeal corrections and expiry;
- preserve protected access and emit replayable application outcomes.

Status:

- `done` for the corrected-source `review-v2` local test-subject passage
  (P018-12/13/14); outside hard MVP.
  P051-004 and P051-008 remain partial for their broader scope.

Implementation tracker ownership:

- **P018-12:** source composition, compatibility and writer-fencing contract;
- **P018-13:** host application, expiry and replay integration;
- **P018-14:** two-case isolation, protected-access and failure evidence;
- **P051-004 / P051-008:** domain integration and cross-component acceptance.

These are single-source tracker references, not a second copy of their statuses.
See [P018 implementation tracker](../../40-proposals/018-layered-capability-limited-participant-restrictions.md#implementation-status)
and [P051 acceptance](../../40-proposals/051-swarm-membership-and-reputation-bootstrap.md#cross-component-acceptance-local-accountability).

## Out of Scope

- moral classification of participants;
- global federation ban semantics;
- deciding membership or sponsorship status;
- replacing capability passports or operation-specific authorization;
- blocking protected floor operations.

## Consumes

- operator participant capability-limits records and admitted source facts;
- clear tombstones;
- operation admission context;
- procurement ranking inputs.

## Produces

- hard-block decisions;
- soft ranking/cooldown modifiers;
- durable replay state and exact effect receipts;
- metadata-only operator refresh events.

## Related Capability Data

- `040-capability-limited-restrictions-caps.edn`
