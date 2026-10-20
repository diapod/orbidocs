# S040: inactive maintenance and shadow composition contracts

Status: accepted local design, draft contracts; M0 offline and M1/M2 internal-owner
conformance only, without operator/runtime qualification.
Date: 2026-10-20.
Based on: P051 sections 25–27 and its early P051-010 alignment, P018, P072/S037,
S028 and S039. This page does not amend normative rights or grant operator power.

## Executive summary

Freeze a bounded maintenance protocol before implementing abandonment, archival
recovery, operator APIs or shadow composition. v1 remains authoritative for
admission, scoring, diagnostics, writers, CAS and receipts. D7 stays closed in
every component. M0 provides contracts and offline validation, no new runtime
qualification. M2 covers the internal F-04 boundary only; P051-010, F-04 operator
qualification, F-05 and the wider P051-015/016 work remain open.

## Context and problem statement

At the planning baseline, the F-02 worker removed replay/conversion from admission
but continuous v1 writes could invalidate its coarse CAS. The M1 checkpoint below
addresses that internal progress defect. M2 separates foreign generations from
current-incarnation preparation; exhausted budgets still lack capacity escape
paths. A maintenance protocol must preserve
source-local consequences and participant rights while leaving room for later
repair reviews. Incidental SQLite/storage behavior must not become procedural
authority or a finding of participant guilt.

The interpretive path is proportionality, agency and auditability → P051/P018
source correction and separate protection/return/repair → existing S028/S039/
P072 owners → bounded schemas → later host implementation. M0 compresses these
invariants into data and ownership; it newly determines exact budgets, local
operator command references and compatibility, not merits or runtime readiness.

## Proposed model and decisions

### Early P051-010 alignment

| Domain | Owner | Preservation / next evidence gate |
| --- | --- | --- |
| Migration generation and preparation | Existing Responsibility host/S028 | Immutable baseline, retained history epoch, bounded CAS; M1 proves progress without replay under admission |
| Repair review and ownership | Existing responsibility-core/service | Explicit review identity, revision, deadlines and accepted handoff; maintenance cannot create or complete a review |
| Correction and protection | Existing signed procedure/host effect adapter | Exact source/CAS/receipt; correction cannot clear other sources or imply applied suspension |
| Incarnation/current receipts | Membership host supplies incarnation; execution owner issues receipts | Old facts/receipts stay historical, fresh commands require current authority; M2 is not restore qualification |
| Operator authority | P072/S037 registry plus host local-control owner | Current per-operation grant/admission and exact plan approval; descriptions and references never prove authority |
| Notices and alert actions | Domain outbox producer plus S039 delivery owner | Recipient binding, separate queue/delivery/open/ack, inspection-only action, no repair by acknowledgment |
| Retention/sealing | Host storage/sealer owners | Only inactive migration copies; preserve live appeals/reviews, authority evidence, pending work, idempotency and terminal fences |
| Qualification | Node profile owner | Separate conformance/performance/runtime/clock/fixture classes; no schema or aggregate signal grants individual power |

The alignment is recorded against Node `a176fdd2` / Orbidocs `275af430` plus this
M0 draft. It does not complete P051-010, extend historical runtime reports or
start a competing repair, enforcement, workflow or backup subsystem.

### Contracts and compatibility

Canonical `responsibility-maintenance-common.local.v1` plus nine document schemas
freeze request, result, generation, abandonment, alert, archive, bounded index,
bindings and report. All carry v1-authority/all-false-D7 boundaries. Node mirrors
and Schema Gate validate them at offline Import/Export, never public transport.
The [Node M0 contract](node:docs/development/RESPONSIBILITY-MAINTENANCE-M0-CONTRACT.md)
specifies exact budgets, metadata hashing, archive package/AAD/index and retry
obligations. Existing signed case/lifecycle contracts are not reinterpreted.

The six frozen future operations are `responsibility.maintenance.inspect`,
`.prepare`, `.abandon`, `.verify`, `.reconcile` and `.compact`. Each has a separate
`grant/responsibility.maintenance.<suffix>` and is host-local, non-advertisable,
passport-ineligible and unavailable to generic module dispatch. M0 adds no live
registry/policy entry or route. Current local-control operator admission and
explicit approval are M4 obligations; absence refuses rather than selecting a
default actor. Case mandates, module registration and passport possession do not
provide maintenance authority.

Decision, 2026-10-20: the **first future new-protocol write** atomically fences
storage v2/v3 to **v4**, after explicit current-operator acknowledgment of the
binary, one-way transition and verified recovery procedure. This replaces the
plan's prospective v3-only pin wording, without rewriting historical v3 facts.
M0 does not change a database/version. Inspection cannot trigger the transition.
A first abandonment of an already-full historical generation is allowed; a new
ordinary generation is not a prerequisite for establishing its escape record.
Every future v4 writer must respect terminal/archive fences even before it can
produce them; otherwise it must refuse. Storage v4 is not implementation V4.

Options considered: reuse storage v3 (older writers can ignore terminal state),
delay fencing until enforcement cutover (too late for maintenance-only writes),
or explicit v4 at first new write. The last preserves the semantics before any
older writer can reinterpret them. It requires an acknowledged irreversible
operator step and compatible recovery tooling. These are future implementation
and qualification gates, not permissions granted by the schema.

### Capacity, archive and missing recipient

Reserve one 8 KiB terminal slot for each of 16 resident generations separately
from 1024 ordinary steps. Pin/copy/verify batches remain at most 100 sources,
8192 per generation. Resident baseline/prepared limits remain 32 MiB each.
Commands, receipts, alerts, archive/index and public report bytes have exact
finite constants in the common schema and Node profile; no runtime limit is
raised by publishing them. Already-full stores need an explicitly approved
control-reserve bootstrap before new ordinary work. Physical disk failure can
still refuse writes and must never fabricate success.

Private archival uses existing host sealer custody, XChaCha20-Poly1305, fresh
nonce, `0600` files/`0700` directories, exact retained members and verified
durable publication before deletion. Context is authenticated before encryption;
ciphertext digest lies outside context to avoid a circular hash. Index pages
have 64-entry/64-KiB bounds, chained roots and verified sealing before rotation.
Only inactive migration material is eligible. Portable backup, keys/unlocking
and restoring another incarnation remain P051-016/D. No archive is made in M0.

Missing current admitted operator recipient yields durable `pending-recipient`;
S039 cannot infer a recipient from a raw name. Pending/queued/delivered/opened/
acknowledged states differ. Notices/actions expose minimal digest references and
authenticated inspection; acknowledgment grants no authority or corruption repair.

### M1 internal progress checkpoint (2026-10-20)

Node's existing inactive worker now separates ordinary v1 appends from scoped
history, migration-lane and prepared-input epochs. SQL bookkeeping observes
legacy v3 writers without changing retained JSON bytes or executing the M0
request protocol. Exact epoch deltas and generation/head CAS precede commit;
the host/incarnation of a request cannot be rebound by retry. The current hint
binds the observed Responsibility history sequence; it is not composition parity.
Automatic checkpoints are disabled on the private writer and passive WAL cleanup
runs outside admission, preserving v1's connection and enforcement policy.

Owner tests exercise every-plan v1 writes, 0/1/500/1000/8192 sources, recovery,
bounded conflicts/busy and the unchanged D7 floor. This is internal conformance
and performance, not Q runtime qualification, M4 grant admission or M5 delivery.
Three conflicts expose a process-local deduplicated signal; no durable operator
notification is claimed. F-04/F-05, V3 and wider P051 remain open. See
`node:docs/development/RESPONSIBILITY-MIGRATION-PROGRESS-M1.md` and
`node:docs/audits/RESPONSIBILITY-MAINTENANCE-M1-2026-10-20.md`.

The separate daemon regression follow-up,
`node:docs/audits/DAEMON-SENSORIUM-S020-REGRESSION-2026-10-20.md`, records Messaging
startup atomicity and Sensorium fixture clock separation, with unchanged live
authority/cleanup deadlines. It preserves M1's original failed measurements and
historical reports. This is not progress on M2–M5/V3/Q, maintenance authorization
or D7; v1 remains the sole enforcement authority.

## M2 internal incarnation checkpoint (2026-10-20)

The Node owner now treats foreign-incarnation generations as immutable history.
A fresh internal prepare can pin the next current-incarnation generation even
when the previous one was unfinished. Membership supplies identity; callers
cannot assert it. The original baseline/history binding still verifies. Old
baseline and checkpoint bytes are never repaired or rewritten, and the single
disposable prepared table is reused only through bounded clear/copy/verify.

Addressed internal inspection distinguishes current, stale, historical and
corrupt generations. Historical inspection checks original history/checkpoints,
not today's prepared rows, and cannot replace the current worker cache. An
in-flight old-incarnation attempt refuses before any write to either generation.
A corrupt foreign checkpoint chain is isolated to that address; an untrusted
baseline identity/digest or changed retained v1 history still refuses new pinning.
M2 does not infer a trusted identity, abandon current work or bypass the 16-generation
and byte budgets. No observation is an execution receipt; existing receipt,
signature and source bytes are unchanged.

This is synthetic owner conformance with restart/interruption and concurrency
checks, not a restore producer, operator grant or runtime qualification. All
existing v1 consumers and D7 remain unchanged. Legacy-v3 durable row shapes are
preserved; the acknowledged future new-protocol v4 fence remains pending.
M3 capacity recovery, M4 P072 admission, M5 S039 delivery, V3/Q and P051-016 remain
open. See `node:docs/development/RESPONSIBILITY-MIGRATION-INCARNATION-M2.md` and
`node:docs/audits/RESPONSIBILITY-MAINTENANCE-M2-2026-10-20.md`.

## Trade-offs

Bounded closed contracts make ownership and refusal auditable but do not prove
the operator grant producer, archive availability, fairness or delivery. A v4
fence protects maintenance history at the cost of old-writer incompatibility.
No generic superset relation can replace exact v1/v2 composition comparison.

## Failure modes and mitigations

- Continuous writes: pinned historical input and generation/epoch/prefix CAS,
  bounded retries and conflict alerts (M1).
- Incarnation/capacity exhaustion: historical isolation, reserved abandonment and
  verified archive/index recovery (M2/M3).
- Missing/revoked authority: no mutation on refusal; live operator admission (M4).
- Missing recipient/queue/archive: explicit pending/unavailable, no invented
  delivery or deletion (M3/M5).
- False runtime claims: the M0 report checker always returns runtime-qualified
  false; Q must implement owner-specific proof predicates before any runner.
- Shadow mismatch: exact equality outside `invalid-subject` and
  `source-key-mismatch`, individually reported with qualified alerts; no cutover.

## Open questions

M0 design choices are frozen as draft. M1's internal owner mechanics have scoped
conformance/performance, and M2 has internal incarnation/history conformance.
M3–M5, V3 and Q implementation/runtime qualification remain open. General repair
contracts under P051-010 and portable
backup/restore remain separate. A private `PRIMARY_EVIDENCE_STORE` configuration
may select future capture storage but is neither a public path nor accountable
external retention without the owner/retrieval/commitment policy in
`node:docs/evidence/RETENTION.md`.

## Next actions

Implement and review M3 next. Register no maintenance capability or route before
capacity recovery and M4 authorization gates; qualify delivery under M5 and shadow
composition under V3/Q. The Node report profile freezes 37 **future** cases in
six evidence classes; fixtures and offline checks are not completed runtime cases.
Keep P051-006/007/008/015/016 incomplete, P051-009 deferred and hard-MVP unchanged.
