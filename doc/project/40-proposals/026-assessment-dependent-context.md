# P026-012c: retained audit units and dependent assessment context

Status: accepted staged design; implementation and qualification are tracked separately.
Date: 2026-10-29
Based on: P026-012b/r1, P036, P066, P073, P090; S002, S028 and S029.

## Executive Summary

Implement the substrate before broadening context: owned fact streams and a startup
legacy barrier; whole-unit retention and durable dispatch; explicit provenance;
operator delivery; RAM continuation; then memory, summaries and one inherited child.
Each stage freezes its contracts, implements them, and qualifies its own claims.
Retention and dispatch freeze together because the reservation is retained history.
Accepted semantics and the separately recorded implementation checkpoints below
are distinct from each stage's measured runtime qualification.

Current local status (2026-11-01): stages 01 and joint 02/03 are qualified within
their separately pinned scopes. Stage 04 and later remain todo; parent 012c/P073
remain partial. The review qualification below covers current 02/03 corrections; earlier checkpoints are historical.

## Context and Problem Statement

Memarium forget addresses entries and appends a decision. Its `Erased` outcome
currently hides the entry in read projections; it does not physically erase the
source or Agent facts. JSONL segment compaction preserves every record. Before this stage, Agent
recovery scanned Personal before tag selection and shared the 100,000-fact/256 MiB
refusal budget across Agent fact kinds. The formerly suggested administrative compaction/snapshot remedy is not implemented;
the Node refusal now explicitly reports that absence. These are lower-layer gaps, not
permission to delete a mixed Personal stream.

## Proposed Model / Decision

### Ownership and implementation order

| ID | Stage | Status | Dependency and completion boundary |
| --- | --- | --- | --- |
| P026-012c-01 | Owned Memarium streams and startup cutover | done | S028-OS-001/002/003; P036-009/010/011. Reviewed v3 profile at clean Node `0ec8dbac` / Orbidocs `1b870593`: 11 native failure/restart/catalog cases plus byte-anchor migration, reclaim and append-cost checks; renewed ordinary previous/current-daemon cutover. Normal/-O loose/extracted agreement, 332 mutation refusals. Protected legacy and later audit-unit/dispatch/context scope remain separate. |
| P026-012c-02 | Whole audit-unit retention | done | Reviewed local profile at Node `1e264cab` / Orbidocs `bc62fab1`: complete owner copies/fences, durable S029, observed-time retention, capsule/checkpoint expiry and S020. Six ordinary cases, 234 component checks, 81 controls per normal/-O loose/extracted variant; physical age/erasure and unknown legacy remain excluded. |
| P026-012c-03 | Durable private dispatch reservation | done | Frozen with 02 and qualified as one vertical; exact-byte preparation, durable fence, final witness gate and settlement. |
| P026-012c-04 | Context provenance | todo | 02/03; authority carrier, exact parent refs, bounded DAG and P090 composition. |
| P026-012c-09 | Same-viewer operator delivery | todo | 04; separate P066 consent and Node UI admission/render; before continuation and memory, so it can display continuation acceptance. |
| P026-012c-05 | RAM continuation | todo | 04; exact latest committed predecessor, no silent fallback or regeneration. |
| P026-012c-06 | Bounded memory/recall | todo | 05; original activation only; one RAM slot store, no durable memory content. |
| P026-012c-07 | Non-Agent summaries | todo | 06; positively admitted producer, private metadata-only execution and inherited dependencies. |
| P026-012c-08 | One inherited child | todo | 04/05; exact family consent, atomic binding/budget admission, one child and no grandchildren. |
| P026-012c-10 | Integrated qualification | todo | All adopted profiles; normal/-O, loose/extracted, explicit exclusions and retained failures. |

Identifiers remain stable when execution order changes. Each stage's qualification
is a prerequisite, not a claim inferred from the table.

### Dedicated and legacy populations

P036 owns the Memarium stream contract and startup-only cutover; S028 owns storage
mechanics. Dedicated owner streams are excluded from generic Personal views,
search, export, backup and read sidecars by default. An exact owner port is needed.
Streams are opened lazily and catalog directories are sharded by allocation ordinal.
A durable allocator outside retired streams owns generation/ordinal monotonicity;
loss refuses recovery, never resets the counter or reuses an identity.

Before Agent load/admission, create the new streams, append the final tagged Agent
cutover fact to Personal with expected head S, then select the new writer. The
barrier binds S, the range digest and exact new namespace/stream descriptors. Before
the barrier commit old mode applies; afterward only dedicated writes are admitted.
The namespace locator is checked against the barrier digest. Lost-locator discovery
is an explicit budgeted one-time scan, not a silent empty state or an every-start
scan. Existing unrelated Personal writers are handled by the expected-head CAS.

Legacy remains immutable and protected, with no copy, migration or deletion. Replay
reads its prefix through S with historical readers, then new owner facts. A streaming
range reader verifies hash linkage while stopping at S; output pagination alone is
not an I/O bound. Fresh S=0 and previous-binary legacy use the same protocol. The
previous daemon must refuse the unknown tagged barrier. This is not a claim about
arbitrary malicious binaries. Agent append, recovery repair and imports reject the
old destination after cutover, before an idempotency hit can hide a write attempt.
A per-schema identity table defines domain fact keys; retired targets return
`stream-retired`. Old general Agent continuity is preserved.

### Stage 01 implementation boundary (2026-10-29)

Node implements the startup-only barrier and owner routing before Agent load and
admission, with no copy/deletion of legacy. The descriptor freezes exact anchored
source extents, expected head and destination generation; generic owner-tag writes
refuse before idempotency. Lost-locator discovery is explicitly enabled and bounded;
allocator loss, corrupt locators and missing committed data refuse. Source protection
conservatively blocks relocation/compaction of the whole Personal fact stream.
There is no release operation yet. General Personal/sidecar startup can still scan
Personal, so the bound is on Agent recovery rather than total Node startup.

The concrete contract and per-schema identities are in
`node:memarium-runtime/docs/OWNER-JOURNALS.md`. An ordinary previous/current daemon
pack is in `node:tools/acceptance/memarium-owner-cutover/README.md`. The
[Node checkpoint](https://github.com/diapod/node/blob/main/docs/evidence/agent-runtime/2026-10-29-p026-012c-01/README.md)
qualifies exact legacy bytes, owner routing, current restart and refusal by the
pinned previous executable at Node `d5ad1392` / Orbidocs `365a3796`. Four qualification
variants agree (normal/-O, loose/extracted), with 80 manipulation refusals. Component
faults are explicitly separate from the ordinary-process witness. At that historical checkpoint, S028-OS-003 remained partial for independent
physical failure/cost qualification. Later audit-unit/dispatch and context stages
remain open, including P066/notification retirement receipts.

The subsequent stage-01 review separates the frozen v1 runtime witness from its
verifier's missing Agent/command bindings. Current repairs enforce non-repairing
owned reads across lifecycle operations, exact discovery boundaries, and domain
wrapper identities before recovery admission. The reviewed qualifier is a versioned
successor that reuses the pinned v1 codec, adds complete fact/session/command and
anchor links, ordinary fresh S=0 restart, and observed runtime-root cleanup.
Independent S028 failure/cost qualification remains partial; the later stages below
are unchanged. New measured results must be retained separately from the original
checkpoint.

The concrete 02/03 data and failure contract is frozen in
[Audit units and private dispatch](026-assessment-audit-dispatch.md). Its freeze
is not implementation or runtime acceptance.

### Historical stages 02/03 dispatch checkpoint (2026-10-29)

The joint contract is frozen. Node now has pure capacity/retention values and an
S029 receipt-DAG projection, an isolated dispatch metadata stream, exact-byte
preparation and a durable fence before the final witness gate. Possible disclosure
survives adapter failure; replay after restart never reactivates or dispatches.
The selected runtime configuration is committed, without claiming attestation of
a provider process generation. Component checks and the ordinary dispatch witness
are separate from the full stage gate.

A narrow ordinary-process witness at Node `b1a51400` / Orbidocs `755f50fc` now
passes three dispatch/failed-outcome/restart cases; normal/-O loose/extracted
qualification agrees with 144 mutation refusals. See
`node:docs/evidence/agent-runtime/2026-10-29-p026-012c-dispatch/README.md`.
This does not qualify physical retention or the full joint stage gate.

At that checkpoint both stages remained in progress. All-copy source/consumer accounting and routing,
P066/question/notification/Agent owner receipts, persistent saga execution,
capsules/checkpoints and scheduled maintenance are not yet complete. The partial
journal ceiling applies to that journal, not all copies. Existing shared owner
journals remain protected and no aggregate retirement is enabled. Historical
qualification remains unchanged; this checkpoint is not the 02/03 acceptance.

### Audit units and capacity

An audit unit is a closed graph of owner facts. Source and consumer units have
separate ownership. Question identity, frozen intent, consent/consumption/revoke,
binding, attempts, manifests, outcomes, traces, accounting, notification metadata,
references and all retained copies belong in the inventory. Exposure facts do not.
Terminality requires closed admission and settled or explicitly ambiguous attempts;
suspend/reconnect alone are not terminal.

The `assessment-audit/v1` profile retains full metadata for at least 30 days after
observed terminality. Capsules remain until max(terminal+180 days, first-compacted+7
days). Reads/retries do not reset dates; stronger floors and unresolved holds win.
Limits: 1024 detailed units; 16,384 detailed records/64 MiB; 4096 capsules of at most
4 KiB/16 MiB; 32 active bindings; 128 retained detailed closed bindings per launch.
Source ceiling: 192 KiB/64 records. Consumer ceiling: 1 MiB/256 records, partitioned
into 192 KiB base, eight 96 KiB attempts and a protected 64 KiB terminal reserve.
Pending P066 keeps its existing 32 limit and also needs audit capacity.

Reservation accounting is `actual retained + outstanding worst-case reservations`,
not lifetime maxima. Settlement releases unused attempt bytes/records; terminality
releases unused base, future attempts and terminal reserve after recording actual
terminal metadata. Repeated settlement cannot release twice. The admission snapshot
and release are atomic owner transitions. No reserve is released for ambiguous writes
until durable reconciliation determines its usage. Shared owner copies count.

Reference steady-state workload: three completed source/consumer pairs per day
for one launch, at most 144 KiB and 65 actual records per closed pair (all owner
rows and fences included), 30-day full retention, no holds, and room for 32
worst-case live pairs. Ninety closed pairs plus live headroom use 50.65625 MiB and
16,090 records; 90 closed bindings fit the 128 launch cap. At 180 days the capsule
workload is 1,080 units. This is conditional capacity arithmetic, not measured
throughput; the ordinary fixture is checked separately. The earlier four-pairs/day
illustration assumed only 32 records per pair and does not describe all-owner
routing. With 32 live pairs, 94 closed pairs of this reference size fit, while the
95th refuses on records. Maximal retained pairs still fit only about 51 times in
the detail pool and support about 1.7 pairs/day without live headroom. Admission
must refuse heavier steady-state loads truthfully. Tests cover the reference,
record-bound saturation and worst-case reservations; no ceiling is raised.

At admission attempt capacity is reserved before Agora. Physical preallocation is
attempted for the dedicated writable segment: supported native allocation must
confirm reserved blocks; an unsupported-platform fallback reports logical-only
reservation. Preallocation reduces ENOSPC exposure but cannot guarantee later writes
against quota changes, metadata exhaustion, I/O failure or unrelated storage users.
It is never advertised as a successful physical reservation when only sparse length
was set. Provisioned unused extents are reclaimed at sealing.

### Retirement saga and honest physical receipts

S029 owns a bounded retirement operation, not a new daemon loop. Its exact immutable
plan binds inventory, owner decisions, dependency dispositions, holds and replacement
capsule. Retire referring records before referenced records. Each owner commits an
idempotent receipt; the aggregate unit is retired only when every required receipt
is verified. Cycles require an explicitly jointly planned set, not arbitrary order.
Failure retains a resumable partial operation. S020 schedules bounded work every
15 minutes with at most 60-second jitter, no overlap, and 16 units/4 MiB per pass;
250 ms limits starting more work, not fsync latency.

SQLite receipts distinguish `rows-removed` from file reclamation and physical
sanitization. DELETE can leave free-page/WAL bytes. secure_delete, checkpoint and
VACUUM may be separately reported only when configured, executed and verified;
none proves erasure of filesystem snapshots/backups. JSONL receipts identify exact
unlinked files and remaining copies. No receipt claims undoing prior disclosure.

Retire whole streams only; never excise a prefix of one hash chain. Audit detail,
time-bucketed capsule streams, checkpoint generations and bounded delta streams form
a chain linked by sealed predecessors. A small checkpoint carries horizon, digests
and locators, not copies of all capsules. Bound it to 64 KiB, at most 16 hold
exceptions, and two checkpoint generations. Rotate capsule buckets daily or at
256 capsules/1 MiB; retain a maximum 256 bucket streams within the capsule pool.
Holds carry an owner and deadline. Exceptions retain their exact streams and remain
visible; more than 16 exceptions refuses further horizon advancement rather than
losing a hold. Expired/unknown owner state is resolved under the hold contract, never
inferred from a missing response. Held source relationships remain protected.

Replay below the retired horizon returns `history-unavailable`; retained exceptions
are looked up explicitly. No per-request lifetime tombstone table is introduced.
Archive import cannot allocate old identities or reactivate old authority.

### Dispatch and provenance

Reuse common dispatch identity/header laws from the controller and external-runtime
journals, with owner-specific bodies and historical readers. The private variant
contains commitments, not the external runtime's complete request. The attempt key
is (unit, activation, Agent, binding, request), never step alone. Bind manifest/ref
(the unkeyed canonical metadata hash), canonical-request HMAC and exact-wire HMAC,
boot/launch/captured session/epoch, lifecycle, runtime generation, deadline and
budget/capacity reservation. HMAC equality is verifiable only within the launch;
after restart metadata hashes still verify but private bytes are unavailable.

`PreparedPrivateDispatch` has a private constructor, no Clone/Serialize/Deserialize,
redacted Debug, consuming send(self), and explicit abandon(self). Tests detect silent
abandonment. Preparation freezes exact bytes after queueing and mapping. Durable
reservation precedes a fresh memory-only witness/time gate; fsync time counts.
There is no owner I/O, remapping, fallback or second dispatch between gate and send.
Abandon persists not-dispatched before returning. If it cannot, the durable fence
remains ambiguous. Settlement is atomic metadata and preserves possible disclosure.

States: reserved; not-dispatched; completed; failed-after-dispatch; and the existing
`dispatch-outcome-unknown` (producer Ambiguous). Only not-dispatched proves no send.
No automatic retry after a durable fence with missing/ambiguous settlement. A
not-dispatched attempt does not hide the last usable committed predecessor; a later
in-flight, ambiguous or dispatched-but-unusable attempt does. Pre-dispatch 429 does
not poison the continuation chain. Private summaries use this metadata-only journal,
not a producer result pointer into the general object store.

Freeze all origin variants in the successor supplied-input manifest: host-template,
observation, product, memory and summary. Unqualified memory/summary origins refuse
with a typed profile-not-enabled result. Parents are manifest refs, not nested copies.
Bound depth to eight and distinct ancestors to 64; memoize traversal and reject
cycles, missing parents and overflow. Missing authority carrier is distinct from a
known empty set. Products are constructed only from a sealed parent manifest.
Authority union laws and P090 execution provenance stay separate. A predecessor
occupies one of eight inputs and is selected by commit ordinal, never wall time.

### Later profiles and recipient

The accepted memory profile is RAM-only: Orbiplex persists no memory content.
This does not prevent OS swap, core dumps or allocator copies. The daemon currently
neither locks these pages nor disables dumps; process hardening is a separate option.
Only artifact identity, HMAC commitment, byte size, parent manifest and dependencies
enter the durable audit inventory. One bounded typed slot store holds both the latest
012b result and memory artifacts, with shared lifecycle/accounting operations and
explicit per-kind rules. Memory slots are not silently evicted. The latest-result
slot retains 012b's explicit replacement semantics.

All dependent context stays tied to its original live activation. A new consent is
a new activation, not an in-place scope extension. Memory has a separate 2 MiB/unit,
64 MiB/node RAM budget outside the metadata pool; existing result-slot bounds remain
explicit additional charges in the same store. A P091 node ceiling may be narrowed
by later layers, never silently raised. Reserve required bytes before Agora; the
parent and child share the unit budget. Over-capacity writes refuse without eviction. Eight artifacts/unit, up to 256 KiB each, and up to four memory inputs are
further limited by total eight inputs and token budgets. Revoke, expiry, activation loss and launch closure clear slots using best-effort
zeroize; temporary/allocator/provider copies are not claimed erased. Encrypted spill
is excluded from this profile. A future distinct profile requires explicit consent,
Sealer/key custody, crypto-shredding and ciphertext retirement; configuration cannot
switch an existing RAM-only activation into spill.

A family has one exact parent and one child; binding admission and family budget
split are atomic and both count against 32 bindings. Reuse monotone fork/lineage
quarantine. Shared eight attempts include summaries and child work.

Operator delivery is a new named recipient, with separate exact-product P066 consent.
Required recipient proof kind is same-viewer; Room/Corpus/export refuse with
recipient-exposure-unverifiable pending their round/recipient contracts. Bind viewer,
subject and normalized admitted record set/exposure states, excluding presentation
countdowns. Window release remains a meaningful change. Current admission and all
parent dependencies are checked before issuing the RAM result; source changes can
refuse the entire old product, never attempt textual redaction. Hidden-peer changes
must not change that projection. Node UI uses no-store, no product handle in URLs,
no prefetch/history persistence/SSE, a no-JavaScript path and P057-014 attention guards.

## Trade-offs

Legacy remains physically present and whole-space Memarium scans still read it.
Dedicated recovery is bounded independently; other Agent kinds retain their own
startup/history constraints. A hold can still cause admission refusal when bounded
exceptions or pools fill. Native preallocation is best effort with an explicit mode.
Restart invalidates context authority by design; snapshots never revive it.

## Failure Modes and Mitigations

Qualify cutover crashes, old-binary refusal, allocator loss, stale generation, retired
imports, delayed writes, corrupt range chains, partial owner receipts, compaction
versus commit, ENOSPC at each write, exact reservation release, ambiguous dispatch,
manifest/DAG substitution and no source/object-store leakage. Expired authority blocks
issuance independently of retirement progress. Do not infer secure physical erasure
from SQLite DELETE or from removal of one local copy.

## Open Questions

RAM-only memory was selected explicitly on 2026-10-29; encrypted spill is a separate
future profile. Numeric capacity is a frozen reference profile to be tested, not a
throughput benchmark or release-readiness statement.

## Historical qualification checkpoints

These checkpoints describe their pinned gates. Run05 is not evidence for its
previously unmeasured short-write, sealing-allocation and append-cost properties.
The [v3 review renewal](https://github.com/diapod/node/blob/main/docs/evidence/agent-runtime/2026-10-29-p026-012c-01-storage-v3/README.md)
qualifies the corrected local gate at Node `0ec8dbac` / Orbidocs `1b870593`, including
native recovery without restart, byte-preserving reclamation, actual v2-reader refusal
and ordinary daemon cutover. Historical bytes and tool pins stay frozen.

### Stage 01 reviewed checkpoint (2026-10-29)

The [Node review](https://github.com/diapod/node/blob/main/docs/evidence/agent-runtime/2026-10-29-p026-012c-01-review/README.md)
records the corrected non-repairing lifecycle reads, discovery limits, domain
wrapper identity and independent semantic witness links. Clean ordinary run 02 at
Node `5d62641f` / Orbidocs `9690ac42` qualifies legacy and fresh S=0 restart plus the
pinned previous reader's refusal, with normal/-O loose/extracted agreement and 164
manipulation refusals. This is a new scoped checkpoint; original evidence and its
v1 verifier stay frozen. It does not close independent S028-OS-003 failure/cost
qualification or later audit-unit, dispatch, provenance and context stages.

### Stage 01 native/cost checkpoint (2026-10-29)

Clean Node `6fc81f7d` / Orbidocs `050d8d58` executes nine ordinary public-API
worker cases and renews the ordinary previous/current-daemon cutover witness.
The [Node storage report](https://github.com/diapod/node/blob/main/docs/evidence/agent-runtime/2026-10-29-p026-012c-01-storage/README.md)
records actual permission failure, process interruption, exact-plan recovery and
32/1024/4096 materialized catalogs with five fresh-process warm-cache reopens.
The mapped 137 component tests and six Agent adapter tests remain separate.

The full storage qualifier refuses with `native-enospc-unqualified` normally and
under `-O`, before/after extraction. Twenty-seven mutations reject in each mode
and location (108), without promoting the refused baseline. The host denied the
producer-created APFS image mount. Actual ENOSPC and native cleanup are pending;
At that historical checkpoint, S028-OS-003 remained partial and P026-012c-01 remains in-progress. No later stage,
release, physical erasure, power-loss or whole-node startup claim follows.

### Stage 01 qualified local closeout (2026-10-29, run 05)

The [retained Node closeout](https://github.com/diapod/node/blob/main/docs/evidence/agent-runtime/2026-10-29-p026-012c-01-storage/README.md)
at clean Node `4f8369ff` / Orbidocs `c85d213f` qualifies the entire frozen local
S028 profile plus renewed ordinary-daemon legacy/fresh restart and previous-binary
refusal. Eleven public-API cases include actual ENOSPC 28 on append, failed native
preallocation, acknowledged-prefix recovery, permissions, process interruption,
seal/append races and bounded catalogs. The exact new 128 MiB APFS image mounts
from an allowed temporary location and detaches after worker exit. Earlier mount
refusals remain observed facts; no security setting changed.

Run 04 is separately retained and correctly refused: its numeric payload encoded
past the generic record limit before append I/O. A versioned collector corrects
that fixture. The owner append adapter preserves concrete JSONL errors and typed
native codes; the frozen v1 tools and partial run 03 remain unchanged. No threshold
was weakened. All 138 mapped component tests, six Agent adapter tests and scoped
Clippy pass. Normal/-O loose/extracted qualification agrees; 33 storage and 41
cutover mutations per variant yield 296 refusals.

S028-OS-003 and P026-012c-01 are done for this local profile. Later 02/03 remain
jointly frozen before context extension; S029 owner receipts, P066/notification
retention, provenance, context and parent P026/P073 remain open. This is neither
power-loss, media sanitization, Linux, whole-node startup, production retirement
authority nor model/release qualification. New initial retain converts only
verified producer-owned loose copies; historical evidence and legacy facts remain.

## Next Actions

Stages 01 and 02/03 have local qualification, including the separately pinned
retention review below. Proceed to stage 04 context provenance while preserving
the accepted ownership boundaries and the explicit limits of each proof.
Use ordinary-daemon/ChannelJson/browser acceptance with deterministic inference,
separately classified native fault/clock evidence, source/binary/feature pins and
normal/-O loose/extracted qualifier mutations. Retained evidence follows Node
RETENTION/RETIREMENT/EXTERNAL-RETENTION; runtime policies authorize no historical
acceptance cleanup. Reconcile owner docs, schemas, trackers, Node ledger/MVP and
convergence/cleanup reviews per completed stage. Preserve 012b historical evidence.

### Historical stages 02/03 integration before qualification (2026-10-30)

The preceding 2026-10-29 checkpoints are historical. Node now composes isolated
source and consumer units with P066, operator questions, S039, attention and P073
metadata; a durable S029 receipt graph; time-bucketed capsules; pointer-only
checkpoints and bounded S020 maintenance. Writer quotas share the existing base
reservation. Legacy unrouted populations, unknown coverage and stronger owner
floors stay protected. This is implementation status pending the new exact-source
qualification, not closure of the tracker or renewal of historical evidence.
Later context, continuation, RAM-only memory, forks and recipients remain outside
this vertical. See the [joint contract](026-assessment-audit-dispatch.md).


### Local stages 02/03 closeout (2026-10-30)

At clean Node `da1d14a7` / Orbidocs `127843fb`, five ordinary-process cases pass with
production P066/browser consent, a ChannelJson holder, real Agora and a deterministic
loopback adapter. Seven pinned ordinary test images supply 172 component checks in
nine exact raw-log groups. Seventy rehashed controls refuse in each normal/optimized
loose/extracted variant (280); both qualification modes and extracted results agree.
The retained proof is `node:docs/evidence/agent-runtime/2026-10-30-p026-012c-retention/README.md`.

S029 durably resumes all five owner receipts; S020 settles terminal owner copies
without early deletion. Explicit-time tests cover full detail/capsule expiry,
mid-bucket restart, bounded working-set recovery, capacity and 21 before/21 after
control-write faults. The old selected daemon refuses notification schema v7 without
changing retained populations. The originally overflowing chained capsule remains a
failure; complete v2 encoding and S028 exact-line admission fix it within 4 KiB.
The fixture pair uses 141,608 B / 65 records; the component capsules including owner
controls use 3,737 B and 3,671 B. No unit, pool or floor ceiling was raised.

This closes only the joint local 02/03 profile. The physical-clock/power-loss/erasure,
actual-model, provider-process, federation and release claims remain excluded.
SQLite free pages/WAL/backups may retain bytes. Historical/unrouted and unknown
coverage stays protected. Initial retain replaced only new own staging duplicates
after readback, all-mode qualification and conservative global-budget admission;
it did not retire history or adopted replicas. Stage 04 context provenance and
all later profiles keep their separate gates; parent P026-012/P073 remain partial.

### P026-012c-02/03 review qualification (2026-11-01)

Node `1e264cab` / Orbidocs `bc62fab1` qualify the repaired local profile: six ordinary browser/ChannelJson cases, 234 component checks in 11 byte-bound groups and 81 rejecting controls per normal/`-O`, loose/extracted variant (324). The ordinary pending-consent restart reaches owner timeout before freeze and releases both pending slots. The prior daemon refuses the question-owner version barrier without changing owner populations. The retained proof is `node:docs/evidence/agent-runtime/2026-11-01-p026-012c-retention-review/README.md`.

Orphan reclamation, same-process replay, owner barriers and terminal-only freeze are repaired. Retention advances only observed monotonic credit capped by UTC, with no offline age; clock divergence requires review and does not clear on restart. S020 publishes once per pass, with durable plan/bucket pointers before effects. The 347/545 ms lock observations are not a hard 250 ms latency guarantee. SQLite receipts still permit residual bytes. Lossless metadata compression remains; replacing it with a shared-reference graph is separate design work. Historical proofs are unchanged; context provenance and later 012c stages, parent P073 and release qualification remain partial.
