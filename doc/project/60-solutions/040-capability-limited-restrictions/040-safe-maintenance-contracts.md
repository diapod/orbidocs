# S040: inactive maintenance and shadow composition contracts

Status: accepted local design, draft contracts; M0 offline and M1/M2/M3 internal-owner
conformance only, without operator/runtime qualification.
Date: 2026-10-21.
Based on: P051 sections 25–27 and its early P051-010 alignment, P018, P072/S037,
S028 and S039. This page does not amend normative rights or grant operator power.

## Executive summary

The bounded maintenance protocol now has M3 internal abandonment and archival
recovery mechanics; operator APIs and shadow composition remain later stages. v1 remains authoritative for
admission, scoring, diagnostics, writers, CAS and receipts. D7 stays closed in
every component. M0 provides contracts and offline validation, no new runtime
qualification. M2/M3 cover internal incarnation/capacity boundaries only;
P051-010, F-04/F-05 operator qualification and the wider P051-015/016 remain open.

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

## M3 internal capacity checkpoint (2026-10-21)

The internal storage owner now separates monotonic generation identifiers from
sixteen resident baselines. One 8 KiB append-only abandonment slot per resident
generation remains available beyond the 1024-step and ordinary-receipt budgets.
A terminal enables an explicit successor; it never retracts a participant source.
The first approved new-protocol write atomically installs the acknowledged v4
fence. Startup and inspection do not install it, and v1 remains authoritative.

The private archive uses existing host sealer custody, exact M0 context/AAD,
0700/0600 modes, durable publication, decryption/member verification and manifest
commit before bounded deletion. A resident 64-entry/64-KiB index rotates only after
its old page has been sealed and verified. The manifest binds the original
projector fingerprint; historical absence is explicitly unbound and cannot
qualify a projector for V3. Archives keep consuming the 256 MiB
area; encoding, metadata links and crash stages count too. Crash-left compact
work resumes under current authority. A fresh exact plan can explicitly supersede
an old pending compact command without reviving its grant or reporting it as
completed. Raw v1 facts, sources, receipts and live case obligations are outside
the deletion set. General backup/restore remains P051-016/D.

M3's additional internal command-address profile is
`maintenance:g<generation>:<opaque-suffix>`, within the existing Id limit. This
binds a request to its never-reused generation and keeps a resident terminal
escape independent of archived key availability. Canonical M0 fixtures still
prove shape only. The admitted exact plan includes the optional superseded
command/digest binding; raw actor strings still confer no authority.

The M1 review also shares refusal decoding, reports nonauthoritative remaining
resident capacity and pairs gate/checkpoint timings. Manually dropping the epoch
table while leaving v1-fact triggers can stop v1 writes until startup recreation;
that is an unsupported live schema edit, not a claimed isolation guarantee.
Loss/change of history invalidation metadata fences further preparation after
archival rather than laundering a rewritten prefix. Tracing is not operator
delivery, and timing correlation is not proof of a syscall cause.

The Node Schema Gate corrects object-constant key-order comparison for the M0
family in its private compiled schemas. Canonical schemas, original command bytes,
digest preimages and all-false-D7 constraints remain unchanged.

See `node:docs/development/RESPONSIBILITY-MIGRATION-CAPACITY-M3.md` and
`node:docs/audits/RESPONSIBILITY-MAINTENANCE-M3-2026-10-21.md`. These are internal-owner
conformance/performance results with synthetic authority, not current P072 grant
admission, durable S039 alerts or Q runtime qualification. F-04/F-05 operator
exposure, M4/M5/V3/Q and the wider P051-015/016 remain open. No live capability,
source writer, suspension protection or D7 state is promoted.

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
M3 has internal capacity-owner conformance; M4/M5, V3 and Q implementation/runtime qualification remain open. General repair
contracts under P051-010 and portable
backup/restore remain separate. A private `PRIMARY_EVIDENCE_STORE` configuration
may select future capture storage but is neither a public path nor accountable
external retention without the owner/retrieval/commitment policy in
`node:docs/evidence/RETENTION.md`.

## Next actions

Implement M4 next. Register no maintenance capability or route before
capacity recovery and M4 authorization gates; qualify delivery under M5 and shadow
composition under V3/Q. The Node report profile freezes 37 **future** cases in
six evidence classes; fixtures and offline checks are not completed runtime cases.
Keep P051-006/007/008/015/016 incomplete, P051-009 deferred and hard-MVP unchanged.

## M4/M5/V3/Q contract checkpoint — 2026-10-23

The accepted Node execution revision 2 is
node:docs/development/RESPONSIBILITY-MAINTENANCE-SHADOW-EXECUTION-2026-10-23.md.
CP0 reserves six host-local capability identifiers; it adds no active policy,
route, operator authority or runtime qualification. P066 owns exact-descriptor
grants and recoverable allow-once plan reservations; the maintenance ledger
owns work and S029 projects it. Scoped memory epochs replace registry I/O under
admission. Shared operator:default inbox delivery/access binds a verified operator,
not a guessed default identity. Maintenance-only retention holds can be satisfied
by verified archives without notification acknowledgment.

Five draft canonical/mirrored contracts add grant, closed-run plan, hold and v2
bindings/report shapes. The new fifty-case profile preserves historical M0's
37-case conformance scope. A new full-wall limit of less than ten seconds is
conditional on host authorization below twelve and full v1 commands below fourteen
seconds within the existing fifteen-second route. CPU/non-COMMIT guards stay below
one second. These are new qualification gates, not passing measurements.
Historical one-second reports are immutable. v1 remains authoritative and all D7
components stay false; wider P051 and operator/runtime/release gates remain open.

### Pure V3a checkpoint — 2026-10-23

Node now provides read-only exact-instant lifecycle/quarantine composition, after
a separate semantics-preserving v1 kernel extraction. Frozen-v1 differential and
independent lifecycle arithmetic tests cover suspension, original expiry,
terminal withdrawal and scoped quarantine. This is core conformance: daemon
admission, scoring, writers and receipts still use v1. D7 remains closed; host
shadow reads, operator delivery and Q qualification are not complete.

### Preliminary I/O preparation — 2026-10-23

Node adds FIFO admission around the existing host mutex, preserving queued v1
service and maintenance progress. Live authority/governor time is read after the
wait; explicit as-of diagnostics remain separate. The existing channel deadline
reaches the Responsibility handler and clamps its authorization call to twelve
seconds with a three-second route reserve. SQLite durability and v1 writers are
unchanged. The new preliminary profile passes twelve fixed internal-owner cost
matrices (fsync/F_FULLFSYNC); historical one-second results remain immutable.
Actual end-to-end v1 availability, M4/M5 delivery and final Q remain unqualified.
See `node:docs/evidence/local-accountability/2026-10-23-maintenance-io-pre/README.md`.

### Inactive M4a authority owner — 2026-10-23

Node adds P066's narrow `remember-exact-descriptor` scope, exact allow-once
reservation recovery and typed operator/binding/grant witnesses. Scoped epochs
cover revocation and binding changes without owner I/O under admission. Agent
spawn/bind/proposal/dispatch refuses maintenance even with a mistaken grant;
its catalog hides those identifiers. This is inactive owner conformance, not
public grant admission, M5 delivery or Q runtime qualification. Existing consent
preimages remain unchanged; unsupported scope readers refuse the new enum.
v1 remains authoritative and all D7 components stay false. See
`node:docs/audits/RESPONSIBILITY-MAINTENANCE-M4A-2026-10-23.md`.
