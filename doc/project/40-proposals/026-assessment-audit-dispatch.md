# P026-012c-02/03: audit-unit and private-dispatch contract

Status: frozen implementation contract, 2026-10-29; narrow dispatch prerequisite qualified; whole-unit retention and the joint stage gate remain incomplete.
Based on: [accepted staged plan](026-assessment-dependent-context.md), P066, P073,
S028, S029 and P036. This refines stages 02/03; it does not enable later profiles.

## Executive Summary

An admission reserves an entire auditable attempt before Agora. A durable fence
then binds the exact prepared transport bytes before a fresh final authority gate.
A crash after the fence is ambiguous until reconciled; it never permits dispatch
replay. Retirement acts on whole units through owner receipts, never by deleting
isolated Agent facts from a shared journal.

## Context and Problem Statement

Stage 01 isolates general Agent facts from Personal but does not bound the lifetime
of closed-consumer facts. P066 keeps consent and consumption rows; operator questions
and notifications also retain copies. Notification audit JSONL is a shared stream.
Deleting queue rows cannot qualify retirement of that copy. Historical shared
populations remain protected; a complete inventory or a new isolated destination is
required before an aggregate retirement can complete.

## Proposed Model / Decision

### Values and owners

The reference profile remains `assessment-audit/v1` with all numeric floors and
ceilings in the accepted plan. Timestamps are explicit signed UTC milliseconds;
checked arithmetic refuses overflow. Retention time is distinct from authority time.
A backwards observation cannot move a terminal timestamp or a retired horizon back.
No receipt or checkpoint restores authority.

An inventory is immutable and binds `unit/ref`, `unit/kind` (source or consumer),
`allocation/ordinal`, activation, boot and launch, policy, terminal time, and exact
members. Each member binds owner, opaque locator, content commitment, encoded bytes,
record count, dependency refs, copies and applicable holds. Missing coverage is
unknown and refuses retirement. References grant no authority to delete.

The owner's mutable admission projection holds actual bytes/records and outstanding
reservations separately. All additions use checked arithmetic. Source maximum is
192 KiB/64 records. Consumer maximum is 1 MiB/256 records: 192 KiB base, eight
96 KiB attempts and 64 KiB terminal capacity. The record partition is 48 base,
eight attempts of 24 records, and 16 terminal records. Each claim includes all owner
copies and envelope overhead. A failed/ambiguous write keeps its reservation.
Settlement is idempotent, releasing only unused reservation after actual usage is
known durably. Capacity refusal precedes Agora and is distinct from storage failure.

### Retirement operation

S029 owns the bounded operation protocol. A plan contains `operation/ref`,
`inventory/digest`, `replacement/ref`, exact owner decisions, and a dependency DAG
of steps. A referring member's receipt is required before executing a referenced
member's step. Duplicate steps, missing dependencies and cycles refuse; a joint
cyclic set requires an explicit owner operation, not an implicit ordering exception.

A receipt binds the plan digest, step and owner, input commitment and physical result.
Allowed physical results distinguish files unlinked, SQLite rows removed with bytes
possibly remaining, and explicitly retained copies. A retained copy blocks whole-unit
completion; it cannot be silently reclassified as a completed deletion. SQLite DELETE
is never a claim of filesystem reclamation or sanitization. Receipts are immutable;
retry of the same step recovers its receipt, and conflicting receipts refuse.

A unit stays retiring until every required step has a verified successful receipt.
An unknown owner, hold, copy, or failed receipt preserves a resumable partial operation.
The source cannot retire while a retained consumer refers to it. Holds include owner
and deadline; expiry is not itself permission to forget a hold. The current plan's
16-exception bound and horizon rules apply.

Capsules are metadata-only, at most 4 KiB, retained to max(terminal+180 days,
first-compacted+7 days). Detail has a 30-day minimum. Capsule buckets rotate at a
UTC day, 256 entries or 1 MiB and retire as whole streams. The checkpoint is at most
64 KiB and contains only horizon, pointers and digests, never copied capsule bodies.
Two checkpoint generations and at most 256 capsule buckets are admitted. Recovery
loads bounded current buckets/deltas, never all retired unit histories. Lost allocator
or checkpoint refuses; neither an empty projection nor an archive import repairs it.

### Owner integration and recovery refinement (2026-10-29)

New source and consumer proposals reserve their unit before creating P066 data.
A host-authored `assessment/audit-unit` metadata reference follows the consent,
question and notification projection. It is a locator, never deletion authority.
Historical records without this routing witness remain protected. New closed Agent
facts use their consumer's isolated stream, not the general Agent stream.

The closed inventory includes P066 request/decision/consumption/revoke rows,
operator-question rows, notification queue/idempotency/events/transaction/audit
copies, attention-group membership and any referring group copy, Agent facts,
dispatch facts, reservations and owner receipts. A shared attention group or other
unresolved copy blocks retirement rather than deleting another unit's data.
Exposure-store facts are explicitly outside the unit and never retired with it.

SQLite owners compare a bounded canonical row inventory inside an immediate
transaction before removing rows and recording the receipt atomically. They report
`rows-removed-bytes-may-remain`; no VACUUM or sanitization is inferred. New private
notification audit copies are isolated by unit, so the historical mixed JSONL
journal is never rewritten to retire a unit. Owner receipts remain available for
crash reconciliation until their covering capsule can itself retire.

S029 persists plan before any owner step, recovers the exact owner receipt after
an interrupted acknowledgement, and records each receipt before the next dependent
step. Capsule publication precedes detail retirement. A bounded checkpoint binds
current detail exceptions, capsule buckets and operation deltas; its metadata never
materializes authority. Source retirement also requires every referring consumer
to have retired. Unknown inventory, copies, holds or owner state refuse.

New S039 owner tables use local SQLite format 7. Migration precedes accepting
new routed work; a format-6 executable must refuse that database at startup.
This prevents a previous writer from bypassing unit routing and mixing new audit
copies back into the historical JSONL file. It changes local storage compatibility,
not the public notification wire contract. Current readers verify the required
owner tables instead of silently recreating lost routed data.

### Dispatch values and protocol

`private-dispatch-reservation.v1` binds:

- `attempt/ref`, unit, activation, Agent, binding, request and passage;
- unkeyed `manifest/ref` and private canonical-request and exact-wire commitments;
- boot, launch, captured session and epoch, lifecycle and runtime generation;
- frozen deadline and the exact budget/capacity reservation.

An attempt's identity includes the activation and request, not just a step number.
The manifest reference survives restart; HMAC commitments are comparable only inside
their originating launch. Full requests, observations and results are never persisted
by this profile. Existing external-runtime facts keep their historical interpretation.

Preparation freezes mapped transport bytes once, after queueing. Durable reservation
and its manifest are acknowledged before a fresh memory-only gate. The time spent
writing and synchronizing is included in this fresh check. No owner I/O, remapping,
serialization, fallback or automatic retry occurs between that gate and send.

`PreparedPrivateDispatch` has a private constructor, redacted Debug, no Clone or
serialization, and consuming `send(self)` / `abandon(self)`. Abandon records
not-dispatched before the refusal returns. An interrupted or failed marker leaves
the reservation `dispatch-outcome-unknown` (producer Ambiguous). Settlement states
are not-dispatched, completed, failed-after-dispatch, or dispatch-outcome-unknown.
Only not-dispatched attests that no send was attempted. A failure after send retains
possible disclosure even if HTTP or response decoding fails. No settlement retry
sends bytes again. Tests detect silently dropped prepared values.

## Trade-offs

Worst-case reservations deliberately reject load before effects. The reference
three-pairs/day all-owner reference workload (144 KiB / 65 records per pair) is conditional arithmetic, not a benchmark. Stronger owner
floors and holds can reduce throughput. Shared historical copies block retirement;
these stages do not authorize deleting historical evidence or mixed Personal logs.

## Failure Modes and Mitigations

Qualification must cover saturation, duplicate settlement, partial owner receipts,
compaction versus commit, each failed write, restart after reservation and after
not-dispatched, exact transmitted bytes, final-gate expiry, no retry, bounded recovery,
and no snapshot activation. Physical failures and deterministic component faults
remain separate evidence classes. Ordinary daemon/ChannelJson/browser acceptance
uses deterministic inference, no models, with pinned binaries and features.

## Open Questions

No numeric policy change is authorized by this contract. Owner integration and
runtime acceptance remain pending until their exact receipts and evidence exist.

## Next Actions

Implement owner values and ports, route new unit populations, then qualify the
02/03 vertical. Keep both trackers open until all owners, scheduling, bounded
recovery, dispatch and acceptance requirements are met.

### Owner allocation inside the existing base reservation

The consumer base (192 KiB / 48 records) reserves 80 KiB / 16 records for
unit-local Agent metadata and 112 KiB / 32 rows for SQLite owners. The latter
is partitioned as P066 16 KiB / 2, question 16 KiB / 1, notifications 64 KiB /
20 and attention 16 KiB / 9. Source owners use P066 32 KiB / 2 and question
32 KiB / 1, with the same notification and attention allocations (144 KiB /
32 total), inside the existing 192 KiB / 64 source reservation. These are
logical typed-row bytes, including escaping and UTF-8, not SQLite page sizes.
Owners enforce their allocation in the writer transaction. Temporary space
reserved for subsequent rows is conservative; admission may refuse before a
partition is completely occupied. No allocation is borrowed from another
owner or from the eight attempt reservations. This partition changes no
retention floor or authority. Missing owner coverage still protects the unit.

### Local encoding and recovery profile

The owner-bound envelope `assessment.audit-fact.v1` adds `open-routed`, `agent-fact`
and `copies-settled`; old `open` populations are retained as uncovered migration
holds. The four owner copies contain owner, exact locator and typed-row inventory
(digest, bytes, records). The S029 operation carries that inventory, immutable plan
and individually acknowledged receipts. Receipt recovery precedes re-reading
removed rows; the same plan cannot retire a substituted population.

The bounded checkpoint holds stream ordinals, positive completed-operation and
detail horizons, a scan cursor and at most sixteen explicit hold exceptions.
It has a 64 KiB encoding ceiling and two stream generations. Both published and
prepared references protect controls during publication. A capsule's compact
encoding stores unit/activation/inventory/plan/receipt commitments and its
operation ordinal. Completion requires a positive horizon, not absence from the
pending list. The 4 KiB allocation includes the SQLite receipts and fences;
open-bucket preallocation counts in the 16 MiB pool. There are at most 256 whole
capsule buckets, 256 entries per bucket and sixteen pending operations.

S020 processes bounded work with 900-second cadence and at most 60 seconds of
jitter. Its 250 ms bound stops new work rather than interrupting an active fsync.
A persistent cursor makes partial capsule receipt cleanup replayable. A deleted
namespace, lost allocator or populated unreferenced capsule stream refuses
recovery. No checkpoint restores an activation. SQLite removal is explicitly
logical; free pages, WAL and snapshots may retain bytes.

The four terminal SQLite write fences are control rows: their exact typed bytes
and four records consume the existing terminal reservation (or the source's
remaining reservation), in addition to owner data rows. They remain with the
owner receipts until capsule expiry and also count in the capsule's 4 KiB
allocation. They are never omitted from settled whole-unit accounting.

### Owner metadata encoding and decoder bounds

The first ordinary all-owner trial retained possible disclosure but refused the
completed P073 commit: repeated metadata copies in array-encoded JSONL exhausted
the 96 KiB attempt allocation. The allocation and the facts are retained. The
owner may encode an Agent metadata payload as
`assessment.agent-metadata.deflate.v1`: `codec: zlib`, `decoded/bytes`,
`decoded/digest` (SHA-256 of exact JCS bytes), and unpadded base64url `data`.
Plain historical Agent payloads remain readable. The envelope hash and fact
identity cover the encoded value; decoding must reproduce exactly the committed
canonical JSON value. No prompt, observation content or product is added.

The decoder accepts at most 64 KiB per fact, refuses trailing compressed input,
wrong size/digest, unknown fields and noncanonical JSON, and never truncates.
Decoded Agent payloads also fit the existing 96 KiB attempt, 80 KiB private base,
1 MiB consumer and 64 MiB node ceilings. The decoded node pool conservatively
reserves the full unit ceiling until terminality, then charges retained decoded
payload bytes; encoded settlement still refunds actual encoded usage. These are
separate resource checks with the same ceilings, not a promise about allocator
or physical RAM overhead. Capacity refuses before unit admission; oversized
provider metadata after dispatch retains possible disclosure and cannot create
a completed outcome or trigger redispatch. No numeric ceiling, authority,
consent, dispatch, retention floor or content-retention policy is widened.

### Component and runtime source identity

The qualifier requires the same exact clean Node source pin for component and
ordinary-runtime evidence. A Rust, schema, test or runtime change requires fresh
component execution. Ordinary processes, browser consent, channels, S020 and cleanup
also run freshly under their own paired Node/Orbidocs source pins. Earlier component
recordings keep their original revisions; no semantic compatibility adapter or
source-reuse optimization is implemented.

Missing or changed terminal owner coverage creates an explicit coordinator-owned
review hold (`assessment-audit`, `owner-copy-coverage-incomplete`, one-day review
deadline), within the sixteen unit exceptions. This permits later positively retired
catalog rows to pass the horizon without retiring the protected unit. Expiry is a
review signal only; positive owner reconciliation resolves this exact hold, never
another owner's hold. Exhausting exception capacity safely stops the horizon.
The final handoff repeats admission after the blocking durable settlement write.

### All-owner reference capacity correction (2026-10-30)

The first complete owner-routing diagnostic measured 141,535 bytes / 65 records
for a source and consumer pair with one completed and one failed-after-dispatch
attempt. This diagnostic is not the final qualification. It invalidates applying
the earlier 32-record illustration to this real flow. The staged plan now uses
three pairs/day at at most 144 KiB / 65 records, 30 days of detail and 32 live-pair
reservations. All numeric pool, unit, floor and launch ceilings remain unchanged.
Measured final fixture costs and scope must be retained separately; this arithmetic
is not a performance, disk-use or generic workload guarantee.

### Exact capsule record admission and lossless v2 encoding (2026-10-30)

A component refusal exposed the extra previous-record hash in a chained JSONL
record: a first-position capsule could fit 4 KiB while a later one did not. The
4 KiB ceiling continues to include the actual complete JSONL line, all four owner
receipts and their fences. S028 accepts an optional exact encoded-record ceiling;
it prepares the envelope and checks its complete line length before recording the
pending append. A bounded idempotent retry checks the retained line's actual size.
The existing stream, state and idempotency rules do not change.

The local `assessment.audit-capsule.v2` payload is a canonical JSON tuple of ten
positions: `[unit, generation, terminal_ms, compacted_ms, inventory_digest,
plan_digest, activation_digest, source_activation_digest_or_null,
receipt_set_digests, operation_generation]`. Digest positions are canonical unpadded
base64url encodings of exactly 32 SHA-256 bytes; the v2 schema supplies the algorithm.
Decoding restores the ordinary `sha256:` references and every Capsule field.
There is no field removal or authority/retention change. V1 tagged JSON remains
readable; it is not rewritten. Unknown schemas, tuple arity, noncanonical or wrong
length digests refuse. New capsules reserve the remaining exact line budget before
append; an oversized capsule leaves the detail and owners protected and undispatched
retirement steps unexecuted. No ceiling increase or successful-result inference follows.


### Measured local closeout (2026-10-30)

The local 02/03 profile is qualified at Node `da1d14a7` / Orbidocs `127843fb`:
five ordinary consent/channel/fence/restart/S020/previous-writer cases, 172 separately
classified component checks and 70 controls per normal/-O loose/extracted variant
(280). See `node:docs/evidence/agent-runtime/2026-10-30-p026-012c-retention/README.md`.
The exact archive preserves all mode outcomes, source/feature pins and prior failure
boundaries. The final fixture pair is 141,608 B / 65 records; chained v2 capsules
including all SQLite owner controls are 3,737 B and 3,671 B. Source/consumer owner
inventories, durable S029, bounded capsule/checkpoint lifecycle and S020 are now
implemented and qualified within that scope. Earlier narrow dispatch and failed
whole-unit attempts are not relabelled. Physical erasure/age, actual models,
unknown legacy adoption, broader context and release remain unqualified.
