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

## Status

Implemented solution.

This solution captures the implemented `participant-capability-limits.v1`
runtime slice. Newcomer and membership/sponsorship policies may project into
the same effective-limits vocabulary, but their social-policy source artifacts
remain outside this solution.

The source-aware social-correction adapter described below is planned. The
existing enforcement slice stays implemented; it does not yet prove safe
composition or independent undo of multiple social cases.

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
social verdict. A future signed-decision adapter must verify issuer, mandate,
target, scope, validity and revocation before producing an admitted restriction.

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

The planned adapter composes case-scoped effects into the existing enforcement
path. It must preserve the following boundaries:

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
3. **Current authority.** Pin the decision and source-set revision, then recheck
   authority, revocation and time at application. Historical replay is evidence,
   not permission to repeat an expired effect.
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

Recovery also passes through `node:daemon/src/state_checkpoint.rs`. The current
policy snapshot uses `.ok()?` when parsing `hard.expires-at`, so malformed data
reaching it silently loses the hard block. Import validates expiry, but replay's
typed decode and timestamp ordering are not equivalent to that validity check.
P018-13/P018-14 own the missing recovery/admission refusal and corrupted-expiry
fixture; this design requirement is not a claim that the baseline already handles it.

There are explicit limits to v1:

- the current map stores one record per participant and `clear` removes that
  participant's state, not a case contribution;
- `recorded-at`/clear tombstones order imports but do not provide a source-set CAS;
- one `hard.expires-at` applies to the whole hard set; soft factors persist
  independently of that expiry;
- the two soft factors are participant-wide, not arbitrary per-surface limits.

P018-12 must choose and test a non-lossy mapping before enabling case effects.
Keep per-source facts and their authoritative projection in the owning layer;
reuse v1 only where it can represent the exact scope and lifetimes. Otherwise
introduce a narrowly versioned contract at that boundary, or refuse the unsupported
shape. Never broaden a case's surface or lengthen its lifetime to fit v1.

The pure `node:membership-policy-core/src/lib.rs` projectors already retain source
references and accept sanction/appeal overlays, but later overlays replace earlier
values for the same operation. The adapter must resolve authority and targeted
retractions before invoking that mechanism. P051 owns policy admission; S040's
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

- `planned`, outside the implemented slice and current hard-MVP claim.

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

- participant capability-limits records;
- clear tombstones;
- operation admission context;
- procurement ranking inputs.

## Produces

- hard-block decisions;
- soft ranking/cooldown modifiers;
- durable replay state;
- metadata-only operator refresh events.

## Related Capability Data

- `040-capability-limited-restrictions-caps.edn`
