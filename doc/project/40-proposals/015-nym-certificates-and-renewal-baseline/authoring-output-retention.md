# Finite protected authoring output retention

## Executive Summary

P015-011 closed on 2026-11-17 for the accepted full-record scope. The bounded
qualification and identity-bound replica exception are recorded below.
The authoring journal is a finite retry buffer;
Memarium/P036 owns retained full-record material after a verified handoff.
Both case and non-case authoring are included. Private detached readback and
idempotent disclosure audit are deferred until an actual consumer requires them.

## Context and Problem Statement

Before P015-011, the recoverably sealed authoring journal retained every preview
and signed revision indefinitely. A case-key binding or custody reservation does not
prove capture. Restoring an old domain DB must not revive a buffer removed after
handoff or erasure, even before its original time limit.

## Adopted Model

### Identity and configuration

An AuthorshipScope is a domain-separated digest of the canonical tuple
(participant, certification, operation-id). Construct it once at the authoring
boundary. S026 preparation, P036 reserve/abandon and review binding consume the
same opaque value. Lower owners do not depend on the authoring type.

P091 explicitly selects custody disabled or enabled before preparation effects.
Disabled means buffer-only. Enabled requires a ready, contract-compatible,
exactly pinned owner/provider; absence or failure refuses with
retry=dependency-recovery. No lookup failure downgrades an operation.
Non-case authoring defaults to disabled. Case opening still requires its P036
promise; disabled cannot bypass that independent requirement. Later configuration
or ReplaceProvider cannot repin an existing operation. Authoring never Capture's.

### Horizons

    initial_until = min(first_prepared_at + retry_window,
                        applicable_case_not_after,
                        applicable_material_deadline)
    until = initial_until
    tombstone_until = max(initial_until, certificate.expires-at) + 604800 seconds

The default retry window is 86400 seconds; operators may shorten it for new
operations. Only applicable ceilings are omitted. Missing required promises
refuse. until only decreases through reasoned facts. initial_until and
tombstone_until never change. Reads, retries, imports and restarts do not renew.
The separate preview deadline still limits signing. Clock observations use the
shared monotonic fence. Sign checks before and after private work, before commit
and before release. No result is released until the DB and final fence commit.

A handoff must commit before until. Its sealed reference may serve until
min(Memarium payload_until, tombstone_until), further constrained by current
proof/material availability and disclosure policy. This does not revive a local
buffer. Afterwards only P036 surfaces may serve retained material.

### Custody and local reads

Capture already verifies payload SHA-256 against the receipt author digest.
Readback checks the original owner through material_availability, requiring
FullRecord, reachable payload/key, original horizons and exact material witness.
A closed owner observation distinguishes not-captured, detached, full and failure;
an InvalidInput error is never guessed to mean detached.

Handoff atomically replaces all local payload revisions with a sealed reference.
After handed-off there is no local fallback. A detached capture records its
observed profile but leaves the local buffer to end with expired.

Use custody-local-material for exact full-record readback. A closed local
consumer enum distinguishes CaseKnowledge and AuthorshipReadback in the current
egress policy. Both pre/post handoff use the same current operator/Vault checks
and audit class. Compare the author digest and verify_signed_record before
release; never expose local first-seen observation authority in the response.

The payload digest, commitment and retained reference remain sealed. Locked
Vault maintenance performs only time expiry/compaction, never custody queries.
Readback is the handoff trigger. Background maintenance gets no decryption grant.

Full-record local inspection does not append PayloadRead facts. Public
read-private keeps its per-call audit. Its audit cannot be claimed as a
confidentiality barrier against an authorized local operator who can inspect the
same full-record bytes. Detached private bytes remain exclusively behind that
separate audited disclosure boundary. The earlier deduplicated-read design is
superseded for P015-011; retain it only as the deferred P015/P036 extension design.

### Transition table

State dimensions remain distinct: authoring phase, storage mode, observed
custody profile and dependency availability. A pure transition returns state and
an effect description, or a typed refusal. The host performs effects.

| State/event | Outcome |
|---|---|
| absent/prepare | Validate certificate, scope, explicit policy and capacity; prepare. |
| existing/same prepare | Exact saved result; changed input conflicts. |
| reviewed/sign | Withheld result until durable commit and final fence before deadlines. |
| buffer-only/read | Local result; no custody dependency. |
| handoff-available/not captured | Local result before until. |
| handoff-available/detached | Protected profile fact; buffer expires normally. |
| handoff-available/full available | CAS sealed reference and remove all local payloads. |
| handed-off/read | Exact local_material only, before reference horizon. |
| erased or terminal missing full bytes | material-unavailable, retry=never. |
| dependency failure/ReplaceProvider | dependency-recovery; do not repin or fall back. |
| buffer/until | Delete revisions and keep small tombstone. |
| reference/reference deadline | Delete reference; retain terminal knowledge until original tombstone end. |
| tombstone/tombstone_until | Absent; read/sign cannot create anything. |
| restored DB or inconsistent fence | reconciliation-required; suspend authoring only. |
| legacy | Existing read behavior; retention unknown, no automatic migration. |

Disallowed combinations refuse. Expired is a terminal reason; tombstone is its
retained representation. The v4 readback exposes separate buffer/reference
horizons and typed availability. Reasons: preview-expired, expired,
expired-before-handoff, material-unavailable, legacy-unknown. Detached uses
expired, never expired-before-handoff. Retry reuses the complete existing
protocol vocabulary, including dependency-recovery; it is not a new enum copy.
Closed v1-v3 schema bytes remain unchanged.

### Persistence, capacity and recovery

The independent fence binds the revision and actual state digest, including
clear maintenance metadata. Horizons are also bound to sealed state/AAD. A
mismatch is Corrupt. Pending/committed recovery must resolve exact DB outcomes;
missing established fencing cannot be initialized as a fresh owner. This blocks
DB-only rollback, not simultaneous restore of DB and fence/filesystem.

Each blob belongs to exactly one (operation, revision); sharing is corruption.
Retire all revisions and their event capacity, not only the current projection.
Keep 256 live operations, 16 revisions and 4096 events, plus 2048 reserved or actual
tombstone slots. Reserve terminal capacity at admission, including live references.
Full capacity blocks new preparations, never retirement of admitted work.
S020 runs every 60 seconds, at most 64 operations with bounded nonoverlapping
execution. Access-time checks are authoritative even without the sweeper.

Legacy blocks colliding IDs across all participating owners and remains untouched.
Capacity refusal caused by protected legacy is legacy-capacity. Do not create a
parallel DB to evade it. Read-only inventory of recognized workstream fixtures:
45 databases, 347 operations, 795 events; maximum 94 operations in one DB. No
unsettled WAL or unknown DB was observed. These are fixture counts, not an
inventory of user data or proof of deployment. No payload was decrypted.

| Effect | Owner/key | Recovery semantics |
|---|---|---|
| Signature output | authoring scope/revision | transactional-withheld; DB plus final fence before release; exact replay only. |
| Handoff reference | authoring scope/revision/material witness | transactional-withheld CAS plus fence; reconcile exact commit. |
| Expiry/removal | authoring scope/original horizons | Journaled tombstone; no undo claim after commit. |
| Time observation | fence owner | Durable monotonic fact; never reset to request time. |
| Capture/private audit | P036 | Foreign effects; authoring never executes or replays them. |

## Trade-offs and Boundaries

Clear deadlines reveal approximate activity locally, but never author commitments.
This is logical active-store removal, not cryptographic erasure of DB/WAL/free
pages, filesystem snapshots or backups. A recoverable operational key proves no
such erasure. Shortening a buffer does not promise higher sustained throughput:
tombstone/certificate horizons still consume capacity. Issuance and renewal keep
their own separate lifecycle.

## Failure Modes and Qualification

Named tests cover refusal/replay/restore before positive paths: explicit disabled
and failed enabled providers; deadline boundaries and fractional sweeps; clock
rollback; lost response and expiry during signing; all revisions/capacity;
DB restore before/after handoff and erase; missing/tampered fence and metadata;
locked Vault never queries custody; exact/full/detached distinctions; unchanged
operator and audit class; scope equality across reserve/abandon; legacy refusal;
regressions for issuer, renewal and case owner consumers.

A single development driver must pass both full-record variants, detached expiry,
restart, handoff, erase before until, reference read after buffer expiry, restore
and buffer-only under missing Memarium. Use short fixture deadlines. During this
stage create no formal campaign ID, manifests, evidence indexes, archives or store
publications. Keep only producer-owned current scratch diagnostics.

Only after all functional paths pass and fixes are reviewed/committed may the
same driver run with a formal evidence layer. Pin the source and qualifier before
capture. qualified iff contract/complete iff exit 0; unsupported families refuse.
The real daemon/Vault/SQLite relay/Memarium gate uses the relay receipt for Capture;
it does not repeat LLR-012 or Synapse. Fixture times prove mechanism; controlled
clock tests cover production horizons. Rust/Python named witnesses must execute,
not remain ignored or merely compiled.

The formal phase first reads current retention rules and measures capacity.
Campaign P015-011 preserves every formal failure in an attempt register and
returns to the development gate before another attempt. Existing 16/1/4 MiB and
aggregate limits stay fixed; new Git controls target at most 64 KiB including
superseded blobs. Loose, extracted and both-store fresh qualifications must agree.
Record owner, classification, inventory, dependencies/holds and minimum retention;
unknown stays unknown. Prior operator-only/recovery-export grants do not extend.

### Qualified scope and replica exception — 2026-11-17

The ordinary development walk preceded a fresh formal capture of the same driver
at Node `c15ec3e13` / Orbidocs `b3d63b30`. All full-record runtime/conformance
requirements passed, with identical loose, extracted and fresh two-store results.
The complete retained positive set is 96439 bytes. The first formal refusal
remains unchanged. Final review, full workspace gate and artifact cleanup passed;
fresh qualification also succeeded after removing the owned Cargo dev cache.
Evidence and exact scope:
`node:docs/evidence/matrix-opaque-envelope/2026-11-16-authoring-retention/README.md`.

The retention owner accepted one identity-bound isolation exception on
2026-11-16, recorded as closed policy/adoption data at
`node:docs/release/evidence-p015011-adoption.json` and explained in
`node:docs/audits/P015-011-ISOLATION-EXCEPTION.md`. All twelve inventory entries
passed fresh ordinary verification in both stores. Under OS-enforced denial of
primary and prior scratch, the other ten historical entries and the new
cause-only capsule retain full verification in their own scopes. Only the exact
P015-011 bundle and pinned qualifier have class `integrity-extraction-only`,
reason `platform-sandbox-nesting`; the isolated observation performs no domain
qualification. Qualifier filesystem hermeticity remains unproved.

The primary copy cannot be retired while that exception is open. Code enforces
the hold independently of artifact labels. Closure requires a new additive full
isolated adoption, preserving the original failed attempt and cause capsule.
The cheap nonnested alternatives required administrator authentication or
interrupting other work; no such environment changes were made. P035-020 owns
host-composed isolation as separate work. Exception/capsule/control bytes consume
the unchanged budgets. Final repository gates and the owned-cache cleanup passed
before closure. Global Whisper, private detached readback and P015-005 remain
separate. No merge or push was part of this closeout.

## Open Questions

None for the accepted full-record scope. The deferred detached reader activates
only with its first explicit consumer and needs its own contract and qualification.

## Next Actions

- P035-020: qualify host-composed isolation and close the exact exception through
  additive full isolated adoption; preserve primary until then.
- Activate private detached authoring readback/audit only for its first explicit
  consumer, with a separate P015/P036 contract and qualification.
- Keep P015-005, global Whisper and release readiness under their own gates.
