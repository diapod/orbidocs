# P096 implementation and qualification history

## Executive Summary

This companion preserves dated P096 implementation, campaign and qualification
checkpoints extracted on 2026-11-01. The [proposal](096-sensorium-brainflow-connector.md)
owns current semantics, invariants and its tracker. An accepted decision below
retains its original status; moving it does not rescind it or renew qualification.

## Context and decision

Separate the growing campaign chronology from the proposal's design. Checkpoint
prose and ordering within each extracted series are preserved; same-document
links are rebased where their targets stayed in the proposal. Original proposal
anchors remain as links; Node evidence, pins and qualifiers are not modified.

## Trade-offs and failure modes

Navigation gains an extra link. Stable anchor stubs preserve incoming references.
Historical observations must be read with their original candidate, authority and
scope; a successful old run is not acceptance of current code.

## Open Questions and Next Actions

No new implementation or qualification claim is made by this extraction. Continue
current work through the proposal tracker and Node-owned evidence. When a dated
decision changes current semantics, update the owning model explicitly.

## Synthetic implementation and acceptance checkpoint (2026-10-16)

P096-006a/007a/008/010a are complete for a **synthetic-only same-process local
P082 host-API profile**: two synthetic instances in one supervisor, two
separately authorized consumers and zero devices. A signed Synthetic Board
feeds one serialized drain, exact independent preset metadata, typed buffers,
host-computed content digests and normal P082 publication/grant/read ownership.
Publication and reads resolve an existing exact operation and cannot start
acquisition or extend its authority.

Retained data is capped at 64 blocks, 512 KiB and two monotonic seconds. Ordered
cursors have explicit gaps; latest windows preserve source identity, descriptors,
receipt intervals and min/max/health, including empty replacement after age-only
eviction. Carrier caps include envelopes/cursors. Stop fences retained samples.
Read-grant revocation does not stop independently admitted acquisition or another
reader. Final P082 output freezes/rechecks the exact grant and current
subscription in the delivery transaction serialized with local revocation;
regrant cannot revive an old read, closed state cannot be restored by late output,
and valid lease renewal remains preserved.

The pinned release at Node code checkpoint `a983167d` passed the unchanged
predeclared four-case independent P096-010a qualifier. Baseline p95/p99/max was
93/116/129 ms, loaded healthy-reader 110/148/155 ms, and full local revoke propagation
including a concurrent healthy read 54 ms, with zero admitted blocks after fence.
SDK pressure recovered in 2535 ms. Protected stop disposed a deliberately blocked
child in 1045 ms, preserving quarantine when SDK release was unacknowledged.
Clock-witness discontinuity, oversized ingress, per-layer loss/pressure,
shared-supervisor isolation, durable revocation/reopen and privacy boundaries
were exercised through actual signed synthetic processes and the normal P082
owner. The OS clock was not changed and no recovery was executed.

Node retains unchanged report/facts/qualification bytes in
`docs/evidence/sensorium-synthetic-local/`, with exact image/source/runtime/package
and profile bindings, separately bounded metadata storage, review corrections
and a source-checkpoint record. This scope grants no real-device, radio,
contact-quality, heart-rate, capture, remote-carrier, HTTP/SSE, production-signing
or background-daemon qualification. P096-005/006b/007b/009/010/011a/011b/014 and
later opt-in features retain their own remaining criteria.

### Delivery review decisions (2026-10-16)

Status: accepted implementation contract; the historical qualified image and
its original fact/qualifier digests remain unchanged.

Context: the first synthetic qualification measured valid baseline and loaded
latencies, but its loaded-reader gate checked only maximum latency and its
zero-gap assertion was not exported as a numeric fact. Review also exposed
partial batch application, session-baseline clock comparison and ambiguous
source-overload reporting.

Options considered: retain only max/coverage gates or gate p95/p99/max plus an
observed gap counter; equate local/global revoke propagation or scope them
separately; use source-unavailable or the existing P082 overload code; treat
SHA-256 as attestation or content consistency.

Decisions:

- Future `live-slow-consumer` qualification enforces the same nearest-rank
  p95/p99/max gates as `live-latency` and measured integer
  `healthy-reader/gap-frames: 0`. No old fact is backfilled; reevaluation of the
  historical report uses its pinned original qualifier.
- Operator/report prose names the metric **host-path latency** (SDK drain to
  local receipt). SDK sample-to-drain delay and source-clock uncertainty remain
  unknown; these numbers are not sample-to-receipt latency.
- The measured 54 ms and 100 ms limit apply to **local read-grant revocation**.
  Global revocation also depends on its configured view freshness/propagation
  budget. Stale views refuse; P096-014 must measure global/remote propagation
  separately. An external revocation service is not serialized by the local
  delivery transaction.
- Concurrent-reader exhaustion uses existing `interface/overloaded`, retryable
  while authority remains current, with HTTP 429 at the host adapter. Source,
  generation and subscription remain intact. It neither starts acquisition nor
  authorizes automatic retries. Remote/SSE biosignal behavior remains gated.
- `host/digest` is an unkeyed **host-computed content digest** proving
  consistency, not authenticity or cryptographic host attestation.
- Batch append validates fully before applying any visible state. Clock-step
  detection compares consecutive available wall/monotonic witnesses (at least
  100 ms), without accumulating gradual drift against session start.

Consequences: evidence tables distinguish predeclared source budgets
(1 MiB/256 blocks/5000 ms) from hard caps (512 KiB/64 blocks/2000 ms).
These corrections do not retroactively qualify a changed image, enable native
acquisition or close additional hardware/remote gates. The four synthetic-only
tracker completions retain their original evidence scope. Node records review
and conformance in `docs/audits/REVIEW-SENSORIUM-SYNTHETIC-FOLLOWUPS-2026-10-16.md`.


### Stronger-gate synthetic requalification (2026-10-19)

Node's separate Sensorium branch retained a new release at code checkpoint
`45454121`, independently matched source `ecbaf810` and image `532d20ed`.
The unchanged-budget independent qualifier accepted P096-010a for profile
revision 3, two synthetic instances and zero physical devices. Baseline
host-path p95/p99/max measured 138/167/197 ms; the healthy reader under pressure
measured 120/157/164 ms. Both enforce 250/500/1000 ms and measured integer zero
healthy-reader gap frames. Local read-grant revoke measured 61 ms; no global
revocation, native exposure or additional carrier qualification follows.

The profile predeclared fixed fifteen-second windows, at least 100 observed
blocks per preset and a test-only enclosing session of 45 seconds. Preset counts
were 136, 150 and 193 across the cases. Earlier runtime/schema/count refusals and
separate diagnostics remain explicit; unresolved original runtime causes were
not inferred from later passing runs. A correctly refused 99-observation result
led to the longer predeclared window without relaxing any performance gate.
The controlled paused-child fault is named `worker-rpc-stall`; native acquisition
queue overflow remains separate.

The immutable first report remains in Node's original metadata area. The new
report, independent decision, build/source observations, profile and all attempt
history are retained in `node:docs/evidence/sensorium-synthetic-local-20261019/`,
under the unchanged 1 MiB per-area/64 KiB per-file storage contract. Independent
source/evidence review found no remaining issue in this run. This report binds
its exact checkpoint; later P096-005 lifecycle code has separate evidence.
P096-005/006b/007b/010/011a/011b/014 remain unpromoted.


A second exact release `578abe5d` includes the protected-control implementation
and repeats the unchanged profile3 qualification: baseline p95/p99/max
100/126/141 ms, loaded 112/153/156 ms, measured healthy-reader gaps zero and local
read-grant revocation 58 ms. The report binds source `ec5ab693` and image
`f2482e5a`; subsequent protected-writer and test changes have their own
conformance checkpoint.
`node:docs/evidence/sensorium-host-control-20261019/` retains the independent
rerun and an explicit compiler-log-reference correction for the earlier release
metadata. Original report, source/image binding and historical bytes are preserved.
This remains P096-010a host-path qualification only.

### Device-free protected-control checkpoint (2026-10-19)

P096-005 remains **partial**. The separate Sensorium implementation now closes
the missing durable stop/withdrawal state: a pre-effect marker and bounded,
write-once lifecycle facts accompany the existing private confirmation envelope.
All writers share nonblocking cross-process coordination and reserve terminal
capacity before effects. The protected lane fences immediately, disposal precedes
audit I/O, current durable revisions authorize release, and late terminal
withdrawal has separate audit status. Normal release additionally requires the
exact still-held resource/owner row. Duplicate completed cleanup is idempotent.

Final separate release `753911aa` (source `b6d2dbfb`, image `26605f62`) passes
462 standard Sensorium cases and four explicitly selected actual-owned-synthetic
control cases. The latter exercise bearer HTTP withdrawal after policy revoke
with an occupied independent ordinary server fixture, actual control-listener
loss, injected retained-monotonic expiry/reopen, and disposal despite unavailable
audit storage. Explicit-unlock writer ownership also has two deterministic
surviving-descriptor regressions, including error return. The independent pool
is not a full management-graph qualification and injected expiry is not a clock-
mutation measurement. These software facts do not create native consent.

These are host implementation and device-free conformance claims, not adoption
or physical qualification. Existing native source observations, expired grants,
registration history and recovery decisions are not rewritten or renewed. The
generic Deferred Registry remains a pending seed, not a consent/terminal ledger.
Node records the contract and execution in
`daemon/docs/SENSORIUM-ACQUISITION-CONTROL.md` and
`docs/audits/REVIEW-SENSORIUM-DURABLE-CONTROL-2026-10-19.md`.

The accepted prerequisite matrix is unchanged: six `physical-native`, two
`controlled-native-fault` and two exact-candidate `host-software` cases.
Synthetic fixture/software tests cannot substitute for that matrix. Current
OS/TCC, mode consent, protected wearer stop after operator logout and saturation,
live authority loss, control-provider loss, hung native cleanup and the complete
launch context still require separately approved native evidence. The normal
native gate stays closed until its prerequisite is actually qualified.

### P096-005 candidate preparation checkpoint (2026-10-19)

A new clean production release `af692fed` is frozen on host-B.local with source
`4fc1405e` (4948 tracked files), release image `56fa8251` and distinct post-sign
GUI image `e8989103`/handoff `8c00d7d4`. The private reader now accepts optional
closed audit durability metadata and `audit-unconfirmed` while preserving
historical absence and the separation of audit, cleanup and authority.
All 51 frozen-client tests pass on target Python 3.13.15. Exact closure/signatures
and actual GUI LaunchServices `launchd` preflight pass without opening the root
or controller. Signing is ad hoc with an image-cdhash requirement; current
Bluetooth permission and background-daemon access remain unobserved.

Before/after protected-root comparison preserves 238 prior files (non-key hashes
and metadata; signing-key files metadata only) and directory identities, the controller namespace, journal revision 81/twelve Cases and zero
claims. Only eight files in one new capsule were added; expired owner authority,
grants, consent and historical observations were not renewed or reused. No
manager, permission probe, scan, acquisition, recovery or Case ran. This is
software preparation for the unchanged six/two/two native-origin prerequisite
matrix, not P096-005 qualification or adoption. Earlier synthetic reports retain
their exact candidate. Bounded records and review are in
`node:docs/evidence/sensorium-host-control-20261019/` and
`node:docs/audits/REVIEW-SENSORIUM-NATIVE-CANDIDATE-2026-10-19.md`.

### Explicit delegated authority renewal (2026-10-19)

The private acceptance operator may explicitly select delegated SSH control for
the metadata-only controller/discovery renewal review and its separate exact
commit/resume. The
review binds this declared control mode. It is not an SSH identity or OS/TCC
attestation; ordinary account/root custody, candidate/source/boot binding,
current source checks, admitted-process absence, idle claims and partial-write
fencing remain mandatory. The default nearby-terminal route retains its local
TTY guard and legacy canonical review/output shape.

A unique discovery grant can coexist with disabled same-owner registrations.
Their plans and declaration digests must match, and an occupied p21 revision
must equal the complete contiguous retirement-history head. The fresh-Case
occupied-declaration guard remains separate. Expired registered p21 authority
is preserved without re-admission, renewal, retirement or consent reuse. Only the
two discovery expiry fields and controller expiry/generation may change. This
metadata operation supplies no native permission, release/reset proof or P096-005
qualification. The focused implementation and runtime checkpoint are tracked in
`node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-RENEWAL-2026-10-19.md`.

The 2026-10-19 runtime checkpoint completed exact review `4cdd860b` with admin
source `b7553f0f`/image `171b658b` and pinned process-only observer. Same-scope
controller/discovery authority expires at 2026-10-20 00:59:45 CEST. Independent
remote before/after comparisons preserve twelve protected sources, journal 81/
twelve Cases, expired stopped p21 revision 5 and zero claims/pending transition.
Two pure and three representative normal-owner/fault cases pass. Separately
approved identity-checked SIGTERM of twelve orphaned host helpers unblocked the
unchanged executable-inspection guard; it supplies no native-stop/reset proof.
No manager, Case, recovery, headband test or native qualification ran. Frozen GUI
closure and unobserved TCC remain separate. See
`node:docs/evidence/sensorium-host-control-20261019/authority-renewal-runtime.json`.

### Consent capacity follow-up (2026-10-19)

The private owner reserves maximum confirmation and terminal audit capacity for
all native enrollment before its transport claim and wearer-control publication,
including never-WEAR. Capacity is distinct from consent; exhaustion refuses with
a typed code before effects. Audit writer contention may wait at most 250 ms,
capped by the original cleanup deadline, after fencing and disposal. Late terminal
withdrawal has its own bounded audit wait without reopening cleanup. The source
checkpoint passes 55 acquisition tests; closed-session digest-linked compaction
remains the following checkpoint. Strict older readers may refuse new lifecycle
fields: selecting a binary for an updated root requires actual format compatibility.
No nearby root, frozen GUI image, hardware evidence or P096-005 status changes.
See `node:docs/audits/REVIEW-SENSORIUM-RETENTION-CAPACITY-2026-10-19.md`.

### Retention and private control follow-up (2026-10-19)

Every native enrollment reserves confirmation and terminal capacity before its
claim, including never-WEAR. Exhaustion refuses with a typed capacity code before
acquisition effects. Audit lock contention waits at most 250 ms within the
original cleanup deadline, independently of fence/disposal. Only durable closed
sessions with verified released-claim eligibility compact into immutable 64-KiB
segments chained by digest; the active head remains 64 KiB and the archive has
at most 128 segment files. Interrupted publication preserves the old head;
late withdrawal adds an amendment without rewriting segments or reusing consent.
No unproven or quarantined cleanup is promoted into released history.

Strict old readers cannot operate on roots after unsupported lifecycle fields
are persisted. Source `4fc1405e` knows base lifecycle but not these new fields;
immutable candidate/TCC history never establishes format compatibility. This is
one-way adoption, with no nearby migration in this checkpoint.

Delegated metadata renewal has a four-hour per-review ceiling in both input and
review validation; nearby-terminal approval retains its own TTY and 24-hour
bound. The trusted OS account and review remain authority for delegated metadata;
this ceiling supplies no proof of human presence or cumulative renewal budget.
Explicit idle-root status checks canonical completed review/marker history with
`authority/granted:false`; new public receipts use `operator/control`, while
private review bytes and prior public evidence stay unchanged. The Node source checkpoints are `c6a24619` (archival) and `55dc91eb` (delegated
control/diagnostics). All 475 standard and 52 console checks pass, plus three
normal-owner/fault cases and one real-owned-synthetic disposal case; these are
software conformance. Software checks and runtime prerequisites remain distinct;
P096-005 stays partial. See
`node:docs/audits/REVIEW-SENSORIUM-RETENTION-CAPACITY-2026-10-19.md`.

Pinned branch history is retained under
`refs/acceptance/sensorium-p096-20261019/` in both repositories. The future
integration choice is a merge commit, preserving master's current-source runtime
fixture and regenerating the combined ledger. No integration occurs in this work.


### Corrected nearby preparation (2026-10-19)

Node clean `3775bf56` freezes the reviewed source `cbb85050` as production release
`dfcf60f5` and a separate signed GUI `d153b457`/handoff `5205c163` on host-B.local.
Exact closure/signature checks, 52 frozen-client tests and rootless actual
`launchd` preflight pass. All 248 previous root files, controller namespace,
journal 81/twelve Cases and zero claims are preserved; only the new capsule's
eight files are added. No new consent fields or root migration, grant renewal,
manager, hardware or recovery runs. New ad-hoc TCC remains unobserved. Preparation
does not reuse earlier native evidence or close P096-005's origin matrix. Both
branches remain separate. See
`node:docs/audits/REVIEW-SENSORIUM-CORRECTED-CANDIDATE-2026-10-19.md` and
`node:docs/evidence/sensorium-host-control-20261019/corrected-candidate-preparation.json`.


### Merged-source preparation (2026-10-20)

Node clean merged `a176fdd2` freezes source `7a500816` as final signed deployment
`92f7ba9b` and GUI `0baa4846`/handoff `83f75e0d` on host-B.local. The oversized
compiler image was refused; explicit signing-container normalization preserves
the original and independently verifies payload equivalence within the unchanged
128-MiB deployment bound. All 52 frozen-client checks, signatures and rootless
actual GUI `launchd` preflight pass. All 256 previous root files, directory and
controller state, journal 81/twelve Cases and zero claims remain exact; eight new
capsule files are added. Expired authority and unobserved TCC are preserved.
No manager, hardware, root migration, renewal or further merge occurs. This
preparation leaves P096-005 and its native-origin matrix partial. Both temporary
branches continue separately after the earlier merge. See
`node:docs/audits/REVIEW-SENSORIUM-MERGED-CANDIDATE-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/merged-candidate-preparation.json`.

### Merged-source authority renewal (2026-10-20)

Exact delegated review `60ea3f0d` completed on host-B.local using merged commit
`a176fdd2`, source `7a500816` and deployment image `92f7ba9b`. The declared
`operator/control` is `delegated-ssh`; its 14400-second TTL was fixed at prepare,
with absolute controller/discovery expiry **2026-10-20 05:27:23 CEST**
(`1792466843000` Unix ms). The authority projection changes only the same-scope
discovery expiry fields and controller expiry/generation. Twelve protected sources, journal revision
81/twelve Cases and expired registered p21 revision 5 remain exact, with zero
claims and no pending transition.

Of 264 previous root files, two reviewed policies change content; the remaining
262 file observations preserve non-key content hashes and signing-key metadata.
`read-store.sqlite` changes only ctime through a `0600` permission refresh, with
unchanged content, inode, mode and mtime. Two create-only review/consumption files
are added. The explicit status projection records this completed review with
`authority/granted:false`; historical completion does not authorize a new action.
No Bluetooth manager, hardware, root migration, recovery, new consent, consent
reuse or merge ran. P096-005 stays **partial** under the unchanged six `physical-native`, two
`controlled-native-fault` and two exact-candidate `host-software` prerequisites.
See `node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-RENEWAL-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/authority-renewal-20261020-runtime.json`.

### Native qualification preflight and immutable package correction (2026-10-20)

The operator authorized SSH qualification while wearing Muse 2. The exact signed
GUI `0baa4846`/source `7a500816` observed Bluetooth allowed with confirmed no-scan
cleanup; TCC responsibility remains unverified. Current controller/discovery
authority expires at **2026-10-20 05:27:23 CEST**. Normal released retirement
`02af8be7`, based on Case `1921aad7`, completed revision 5-to-6 with the four
reviewed sources matching and history, consent and the discovery sibling
preserved. Revision 6 is reserved but unregistered; journal 81/twelve Cases and
zero claims remain unchanged.

The intended Case refused before SCAN, stage decisions or journal allocation.
A separate console diagnostic supplied no SCAN approval and recovered the closed
`sensorium-private-case-refused` result. Offline comparison proves a separate
blocker: immutable `sensorium.acceptance.muse-2-p21.runtime-layout` retains worker
`616fd76e` from `047d9430`, while the compiled closure requires `1fa413b5` after
`3346a4cd`/`b6869f31`. Exact-asset refusal is correct; the original first failing
guard remains unobserved. The source correction selects new revision-1 package
`sensorium.acceptance.muse-2-p21.sdk-health`, requiring fresh normal Author and
separate Sign while preserving legacy packages. Sixteen closed preflight stages
and the relay's first bounded closed stderr projection improve diagnostics
without weakening guards or adding an effect route. Four focused Rust tests and
one normal-key Init/Author/Sign coexistence test pass; no corrected candidate is
yet frozen at this checkpoint.

No new consent/lifecycle format is adopted and no completed P096-005 case is
produced. The six physical-native, two controlled-native-fault and two
exact-candidate host-software prerequisites remain open. A private durability
mirror selected by `PRIMARY_EVIDENCE_STORE` does not adopt public external
retention. See
`node:docs/audits/REVIEW-SENSORIUM-NATIVE-PREFLIGHT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/native-preflight-20261020-runtime.json`.

### Corrected native package preparation (2026-10-20)

Node `88542281` freezes source `280b188c` as admin image `51deff86` and signed GUI
`2b19ea81`/handoff `eeec3bc9`. The exact seven-file target closure, code signatures,
rootless actual `launchd` metadata and 58 target-frozen client checks pass. Normal
Author and separate Sign create package `47dccc41` under the new
`sensorium.acceptance.muse-2-p21.sdk-health` identity, review `ba9db538` and
signature sidecar `d37dfb8d`. Independent OpenSSL verification accepts the exact
payload and refuses its modified copy; legacy package bytes remain unchanged.

At the signing checkpoint, 274 previous non-key files preserve content hashes
and metadata except the normal `read-store.sqlite` ctime refresh; two signing-key
files are checked by metadata only, without reading their contents. Exactly
thirteen files are added: ten assets, review, artifact and signature sidecar. The
controller is unchanged, claims are zero and journal 81/twelve Cases is preserved. A later
explicit no-SCAN diagnostic using the frozen relay reaches one SCAN prompt, then
sends only STOP with zero stage approvals. Its new Case `67c78496` is released
through client withdrawal with no target instance; journal 84/thirteen Cases is
the only content change, while consent, control and grants remain unchanged.
Revision 6 remains unregistered. No scan, acquisition, recovery or merge runs.

The new GUI's TCC permission is unobserved; the older `0baa4846` permission
observation is a separate image-bound fact. Fresh physical readiness is still
required before a new approved trial. This is preparation, with no completed
P096-005 case, qualifier decision or adoption; the six/two/two origin matrix
remains partial. Private durability copies selected through
`PRIMARY_EVIDENCE_STORE` do not adopt public external retention. See
`node:docs/audits/REVIEW-SENSORIUM-NATIVE-PREFLIGHT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/native-corrected-20261020-runtime.json`.

**Later fresh native observation (2026-10-20).** After renewed physical readiness,
the same `88542281`/source `280b188c`, GUI `2b19ea81` and package `47dccc41`
complete one separately approved SCAN/BIND/REGISTER revision 6/WEAR p21 sequence.
A separate state-only permission probe first observes allowed for this new GUI,
with confirmed manager cleanup; TCC responsibility remains unverified. The Case
reports `observed-released` with `run-completed`, confirmed cooperative native
cleanup, executor exit, durable audit revision 2 and controller release. Host
snapshots show journal 93/fourteen Cases, zero claims and unchanged controller
namespace. Revision 6 stays stopped and registered at its original new
five-minute p21 grant, with its fresh binding. Actual native persistence adopts
the lifecycle fields, so older strict readers must not open this updated root.
This source observation retains `qualification:false` and `adoption:false`;
it closes no formal case in the unchanged six/two/two matrix. Current firmware
was not freshly observed. No additional hardware trial, reset, retry or merge
follows. See
`node:docs/evidence/sensorium-host-control-20261019/native-p21-r6-20261020-runtime.json`
and the existing native-preflight review.

### Bounded acquisition-owner observations (2026-10-20)

A device-free implementation follow-up records write-once raw monotonic control
events and bounded counters in the same production acquisition owner. Protected
HTTP ingress is captured before waiting for the session lock and published only
after authentication; provider withdrawal refuses unfinished siblings before
removing their shared endpoint. Authority, consent, permits, validated presets,
fence, receipt, disposal, audit and claim release remain distinct observations.
Missing exact-launch and native-call witnesses stay null. The source snapshot
names its host-before-return fence boundary and independent atomic consistency;
it does not attest a post-return race or physical execution. The 491 passing
software checks (55 opt-in cases ignored) do not close any new native safety
case. P096-005 remains `partial`; historical device evidence is unchanged.

### Finite private campaign preparation (2026-10-20)

The same closed normal-owner runner now has finite baseline, protected wearer
HTTP-stop, Case-deadline and actual control-provider-loss episodes. The first
uses SCAN/BIND/REGISTER/WEAR; later episodes can reuse only the exact current
registration of an earlier ordinary released baseline, bound by its canonical
record digest. They create fresh Cases, enrollment, operation, consent and
permits. No grant/consent, scan observation or process ancestry is carried forward
as authority. The current process verifies its own ancestry, all other
owner/boot/candidate/runtime/target pins stay exact, and unresolved history
refuses. The explicit private-journal basis is one-way strict-reader evolution;
this implementation checkpoint migrates no root.

The fixed 900-second campaign ceiling cannot extend any original grant or
per-session clock. Refusal, uncertain disposal, wrong target/basis, EOF, STOP or
deadline prevents later executable episodes. Seven unavailable hooks are explicit
blocked rows: expired-authority probe, operator logout, ordinary-control pool
saturation, live revocation, native-call hang, uncertain retained claim and real
restart. None is simulated or silently replaced by another event. The deadline
operational episode is the Case clock, not automatically the qualifier's native
activation-deadline measurement.

Automatic private plans/events/validated observations/partial reports remain
bounded and create-only, with qualification/adoption false. The separate offline
collector validates existing v1 case records through the same Schema Gate and
semantic qualifier. It groups by the entire exact qualification tuple, retains
unbound episodes explicitly and never promotes synthetic origin. Only all sixteen
native-p21 and ten host-boundary records of one exact tuple permit source export;
the independent qualifier still decides afterward. Reused registration identity
is not equality of every full-tuple field, especially fresh process launch chains.
Missing exact-launch and native-call witnesses remain missing. No new native case
is claimed closed, and P096-005 stays `partial`. The closing software checks pass
493 standard Rust cases sequentially (55 opt-in cases ignored), 97 Python cases
and library/binary Clippy. One intermediate parallel process-stop refusal remains
retained with its passing isolated and sequential reruns; no timing limit changed. See the Node-owned
`daemon/docs/SENSORIUM-P096-CAMPAIGN.md` and dated campaign audit for mechanics,
review corrections and software checks. No SSH, hardware trial, root migration,
recovery or branch integration occurred in this checkpoint.


### Campaign owner integration checkpoint (2026-10-20)

A later device-free implementation connects the seven operational hooks left
blocked at the preceding checkpoint. The common prefix contains six episodes:
baseline, protected HTTP stop, Case deadline, provider loss, logout of the private
application operator session, and saturation of that application's ordinary
control pool. Logout and pool occupancy are observations of those actual private
owners; they do not establish Node UI logout, OS logout or saturation of the
whole Node management graph. Each acquisition still has fresh current admission,
enrollment, WEAR, consent and permit. The Case-deadline episode remains distinct
from the qualifier's native activation-deadline case.

Two explicit terminal branches preserve the authority and disposal boundaries:

- **Authority loss:** a fresh REVOKE approval reduces only the exact current
  acquisition grant's expiry to the observed real wall clock, with durable
  before/intent/receipt history and preserved sibling grants. The acquisition
  monitor must observe authority loss. After confirmed disposal, the same episode
  probes normal enrollment against that exact retained expired grant and requires
  refusal without a new session, listener, claim or deferred-operation identity.
  The grant is never restored or extended.
- **Native fault:** a fresh FAULT approval selects a fixed, separately signed C
  call after required EEG/motion blocks. The native body publishes its own entry
  clock before a nonreturning wait. This is an `injected-native-call`, not evidence
  of an SDK deadlock. The software caps this armed path's cleanup at five seconds
  and shortens its cooperative dispatch window; that cap is not a measured
  hardware shutdown qualification. Unconfirmed release retains the exact claim,
  and a normal conflicting enrollment probe must actually refuse through that
  claim owner. A create-only checkpoint can then await a separately approved host
  restart. The later read-only observer checks exact source/image, OS and launch
  context, changed boot, original journal, protected sources, controller and
  resources; ordinary Case reopening must still refuse. It resets or recovers
  nothing and starts no middleware.

The terminal branches are alternatives for one registered target. Expired
authority or retained quarantine cannot be bypassed to execute the other branch:
new registration or recovery remains a separate decision. Derived expired-grant
and retained-claim observations do not start another acquisition; restart remains
an explicit pending stage until its separately performed restart is observed.
Partial owner facts and interrupted reports stay partial, with no automatic
retry, authority renewal, reset or recovery.

The new immutable `sensorium.acceptance.muse-2-p21.campaign-native-fault` package
needs normal Author/Sign and a fresh pinned build/signed client before target use.
Old signed packages and observations remain unchanged; no target package or root
was migrated, and no SSH, hardware trial or branch integration occurred here.
The unchanged qualifier still requires its exact native-origin matrix, original
case taxonomy and complete qualification tuple. Reusing a registration does not
merge fresh process ancestry into the same qualification tuple. These are owner
implementation and software-conformance claims, not closure of any formal native
case: **P096-005 remains partial**. Operational details and current checks belong
to `node:daemon/docs/SENSORIUM-P096-CAMPAIGN.md`.

### Campaign target preparation checkpoint (2026-10-20)

The isolated workstream now prepares the campaign on the nearby host from merged
Node `64e92854`, source pin `2694f0aa`, admin image `cce00f57` and ad-hoc signed
GUI `e8ce6d5f`/handoff `6821f1d4`. Normal Author/Sign produces the distinct
campaign package `98dda828`, review `6bd78dd6` and sidecar `ffea479f`: thirteen
package files, a separate signature and nine frozen GUI closure files remain
exact. The oversized release is separately stripped of local symbols and signed;
eighteen loaded sections, globals, imports and fixups remain exact, while local
debug symbolization differs. This is an image-preparation proof, not native
qualification or a new image-size allowance.

The actual target passes 156 program checks after correcting an omitted C source
and Rust parity fixture in the validation kit; the initial failure remains
retained without product changes. Inert target loading of the fixed C library
observes no body entry or SDK import. Local checks pass 517 Rust, 156 Python,
22 ledger and thirteen registry-document tests. No Case, permission probe,
Bluetooth manager, renewal, migration, recovery or hardware trial runs.

Root comparison preserves 299 prior non-key content hashes, two signing-key
metadata observations, all 103 recorded directory identities, both parent
directories and the controller namespace. Three hundred of 301 previous files
also retain all metadata; the read-store SQLite file changes only ctime,
consistent with normal root opening's unconditional mode-0600 refresh. The strict
refusal is retained alongside a separate closed metadata-exception review.
Exactly 26 new files and eight directories are admitted. Journal 93/fourteen
Cases, zero claims, expired controller ownership and stopped registered p21
revision 6 remain unchanged.

P096-005 remains **partial** under the unchanged qualifier and origin matrix.
Fresh authority handling and any revision-6 retirement remain separate from this
preparation; new-image TCC and physical evidence are unobserved. This checkpoint
does not claim final integration into the primary branches. See
`node:docs/audits/REVIEW-SENSORIUM-CAMPAIGN-PREPARATION-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/campaign-preparation-20261020-runtime.json`.

### Revision-6 authority renewal checkpoint (2026-10-20)

The paired workstream fast-forwards to Node `82f9c535` and Orbidocs `7044cbe2`,
without a merge commit or changes to the primary branches. The existing immutable
administrator remains Node `64e92854` / source `2694f0aa` / signed image `cce00f57`;
this operation neither rebuilds it from the synchronized source nor transfers
new source/header or native-startup claims to that image.

Explicit delegated SSH prepare and commit approve review `5e89ee68`. The
14400-second lifetime is fixed at preparation, ending at **2026-10-21 00:19:27
CEST** (`1792534767000` Unix ms). Only the sole-owner controller policy's finite
expiry/generation and the existing stopped discovery revision 3's matching
host/caller grant expiries change. Twelve protected source digests, journal
revision 93/fourteen Cases and zero claims remain exact. Both immutable
SDK-health and campaign packages are preserved; the stopped registered p21
revision 6 retains its original expired grant, binding, consent and history.

This is metadata authority renewal, with no Bluetooth manager, permission probe,
SCAN, acquisition, recovery, root migration or new wearer consent. P096-005
remains **partial** under the unchanged native-origin and exact-tuple gates.
Separately reviewed retirement **6 → 7 is the next step**, not a result of this
renewal; no retirement completion is claimed here. See
`node:docs/audits/REVIEW-SENSORIUM-R6-AUTHORITY-RETIREMENT-2026-10-20.md` and
`node:docs/evidence/sensorium-host-control-20261019/authority-r6-20261020-runtime.json`.

### Released revision-6 retirement checkpoint (2026-10-20)

The separately reviewed metadata retirement now completes **6 → 7** on the
retained administrator `64e92854` / source `2694f0aa`. Review `fe930943` binds
Case `487b1e94` and its `confirmed-case-release` basis; no recovery fact is
substituted. Its four reviewed metadata sources remove only the expired revision-6
host grant/plan, acquisition grant, discovered binding and active candidate
receipt. The completed contiguous history reserves revision 7; it does not
register that revision or create/extend a grant.

Journal revision 93/fourteen Cases, consent and logical resource state remain unchanged;
the controller is free. Both immutable SDK-health and campaign packages remain
exact, and the prepared campaign package is still unregistered. Controller and
discovery authority retain their reviewed **2026-10-21 00:19:27 CEST** expiry
(`1792534767000` Unix ms). A local verifier correction accounts for typed serde's
omission of an empty `discovery/receipts` field; it changes no product contract
or protected source.

No hardware, manager, permission probe, recovery, new consent or new registration
occurs. Fresh SCAN, BIND, REGISTER revision 7 and WEAR p21 remain required for
later use. Synchronization to Node `82f9c535` is separate from the retained target
image; no current-source rebuild, primary-branch integration or native
qualification is claimed. P096-005 stays **partial**. See
`node:docs/evidence/sensorium-host-control-20261019/retirement-r6-r7-20261020-runtime.json`
and `node:docs/audits/REVIEW-SENSORIUM-R6-AUTHORITY-RETIREMENT-2026-10-20.md`.

### Revision-7 campaign interruption checkpoint (2026-10-20)

A freshly authorized delegated SSH campaign selects revision 7 and the prepared
`authority-loss` branch. Before effects, the exact nine-file GUI handoff
`6821f1d4`, source `2694f0aa` and signed image `e8ce6d5f` pass verification and an
actual `launchd` preflight. The same image's permission-only observation reports
Bluetooth allowed, confirmed no-scan cleanup and observer exit; the responsible
TCC process remains unverified. Controller and discovery authority are current
until **2026-10-21 00:19:27 CEST** (`1792534767000` Unix ms), with no controller
or resource claim and revision 7 reserved.

Only `CAMPAIGN p21` and `SCAN` are approved. Baseline Case `7aef6c89` returns
`incomplete-released` during scan, with `case-authority-fenced` and
`client-withdrawal`. Discovery reports a cancelled backend terminal, confirmed
`corebluetooth-not-scanning` cleanup, verified worker exit and confirmed
controller release; acquisition is absent. No BIND, REGISTER or WEAR occurs,
and no p21 grant, registration or wearer consent is created.

The operator-side endpoint records no STOP decision and `withdrawn: false`.
Client control code can also emit the withdrawal frame after internal
transport, nonce or timeout failures; the retained observations do not identify
which path fired. This result does not establish deliberate wearer withdrawal,
a missing device, denied Bluetooth access or expired authority. The automatic
report remains partial with `campaign-episode-not-released`: that campaign code
rejects an incomplete baseline and does not contradict confirmed actual release.
All remaining selected operational rows are blocked; the fault branch remains
unselected. No automatic retry, reset, recovery or renewal follows.

Fresh metadata reads confirm journal revision 98/fifteen Cases, a released new
Case, zero controller/resource claims, no pending fence and only discovery
revision 3 in current registered inventory. Revision 7 remains reserved and unregistered.
Diagnose the first closed client-control termination reason before another
freshly approved attempt. P096-005 stays **partial**, with no formal prerequisite
case closed and no branch integration. See
`node:docs/evidence/sensorium-host-control-20261019/campaign-r7-20261020-runtime.json`
and `node:docs/audits/REVIEW-SENSORIUM-CAMPAIGN-R7-2026-10-20.md`.


### Client-control diagnosis and software repair checkpoint (2026-10-20)

Device-free reproduction against the frozen revision-7 client identifies two
control-path defects without identifying the unique cause of historical Case
`7aef6c89`. Ordinary SSH output shares the heartbeat relay thread; a deliberately
blocked real-pipe output writer produces a remote-echo timeout at
approximately 605 ms while endpoint input remains open. Independently, remote
EOF, malformed host challenges and failed relay echoes can emit the same `S`
frame as an explicit STOP. Those internal failures therefore carry false explicit-withdrawal
attribution. The earlier report and its unresolved historical cause remain
unchanged.

The software repair reserves `S` for deliberate STOP/Ctrl-C. Internal failures
close the control socket, allowing the existing host monitor to classify
`ControlLost`; an independent small lock captures the first closed client
reason and monotonic timestamp without waiting for a socket write. SSH output
uses a bounded queue and nonblocking pipe/TTY writes, with heartbeat echoes
independent of ordinary output, bounded drain/final publication and a first
closed relay reason. Review also finds that repeated individually bounded
decision writes can monopolize a relay turn and delay input EOF. Bounded queued
decisions with per-turn EOF/STOP priority prevent that starvation. The existing
600 ms echo, 250 ms socket, one-second host control and 900-second campaign
bounds remain unchanged. Closed confirmation
error handling also accepts the declared LOGOUT/SATURATE/REVOKE/FAULT stages;
that defect is separate from the historical SCAN interruption.

A strict client diagnostic is published separately from host-authored results as
create-only `client-control-<scenario>.json` within the protected campaign
namespace. It contains closed reasons and timing, grants no authority and
attests neither native cleanup nor claim release. It cannot replace the host
observation or promote a campaign prerequisite.

This checkpoint concerns source review and device-free regressions only. No
SSH action, target build/signing, root migration, native attempt or branch
integration occurs. The retained signed client and historical reports are
unchanged. A new exact pinned build and signed client, followed by fresh
operator approval, are required before another physical attempt. P096-005
remains **partial**. See
`node:docs/evidence/sensorium-host-control-20261019/client-control-diagnosis-20261020.json`
and `node:docs/audits/REVIEW-SENSORIUM-CLIENT-CONTROL-2026-10-20.md`.

### Client-release follow-up source checkpoint (2026-10-20)

Follow-up source review separates output ownership, nonce scheduling and package
scope from the unresolved historical SCAN cause. The relay now assigns potentially
blocking display writes to a disposable owned copier instead of changing the
caller's stdout/stderr open-file-description flags. Its lifetime EOF watcher and
cancellable teardown bound the owned output path, including when its destination
stops accepting bytes. This replaces the earlier OFD-mutating output mechanism;
the earlier checkpoint and its measurements remain historical.

Nonce echoes have priority over ordinary decisions. Their shared lock protects
only an immediate write attempt; the original 250-ms write budget includes lock
waiting instead of granting another 250 ms after acquisition. The remote echo
window remains 600 ms. These local scheduling constraints do not guarantee an
SSH round-trip time or turn loss of the endpoint into liveness. EOF/STOP priority,
finite queues, first closed reason and separate client diagnostics remain.
An existing equality regression guards the two closed client-reason sets; source
review does not treat that guard as a new runtime qualification result.

The acquisition owner now distinguishes ordinary and campaign package scope.
The ordinary default refuses the fault-capable package before enrollment effects;
only the closed campaign factory selects that package family for both fresh and
reused targets. Acquisition request fields cannot opt into it. Structural package
verification and inert registration remain separate from execution admission:
a valid signed closure does not authorize acquisition. Fault arming still requires
its separate campaign/session/phase checks and does not follow asset presence
alone. These source changes do not bypass wearer confirmation, current authority,
configuration checks, permits or cleanup fences.

Campaign expectations already map provider loss to `ControlLost` and deliberate
protected stop to `ClientWithdrawal`. The added mapping regression preserves that
meaning; old reports are not rewritten to match the corrected client behavior.
In particular, baseline revision-7 attribution remains unobserved. No native or
full-tuple prerequisite is promoted from these source checks.

At this source checkpoint no target build/signing, permission observation,
hardware trial, root migration or branch integration has been performed. Target
preparation and measured checks require a separate checkpoint. P096-005 remains
**partial**. Before any later physical attempt, ask an interactive readiness
question and wait for explicit operator confirmation. See
`node:docs/audits/REVIEW-SENSORIUM-CLIENT-RELEASE-FOLLOWUPS-2026-10-20.md`
and
`node:docs/evidence/sensorium-host-control-20261019/client-release-followups-20261020.json`.

### Client-release target preparation checkpoint (2026-10-21)

Clean Node `c06d256a` now freezes the client-release repairs as source pin
`d5e12c64`, deployment image `e6f1a78a` and ad-hoc signed GUI
`8e5358d0`/handoff `536181a4`. Exact nine-file GUI closure verification and an
actual rootless `launchd` preflight pass. Neither preflight opens root/controller
authority or creates a Bluetooth manager; new-image permission remains unobserved.
Existing signed packages and acquisition registrations are unchanged.

The corrected target validation kit passes **201 program tests**, with no skips
or errors, against 66 exact inputs. Its first attempt remains retained: omission
of `native_fault.c` and the Rust `acquisition/evidence.rs` fixture caused two errors
and one skip. Restoring those validation inputs changes neither the frozen
candidate nor product code. The inert probe of the existing signed C library
observes no blocking-body entry; software fault tests use a fake board and do not
establish device or native SDK behavior.

The final strict preservation check passes for all 348 old file records: 346
non-key content hashes and two signing-key metadata observations, with every
recorded old metadata field exact. All 112 old directory identities, both parent
directories and the two-file controller namespace also remain exact. Only ten
files and six directories for the new immutable GUI capsule are added. Journal
98/fifteen Cases, zero claims and existing grant bytes remain unchanged; this
preparation issues no new authority or consent.

No Case, permission probe, Bluetooth manager, hardware trial, renewal, recovery,
root migration or branch integration runs at this checkpoint. P096-005 remains
**partial** under the unchanged qualifier, origin matrix and full-tuple rules.
Any later physical attempt requires fresh interactive readiness confirmation and
current authority checks; these device-free results do not reuse older TCC or
physical observations. See
`node:docs/audits/REVIEW-SENSORIUM-CLIENT-RELEASE-PREPARATION-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/client-release-preparation-20261021.json`.

### Client-release authority renewal checkpoint (2026-10-21)

A separately authorized four-hour delegated SSH renewal completes under review
`e2111556`, using Node `c06d256a`, source pin `d5e12c64` and admin image
`e6f1a78a`. The unchanged controller-owner and discovery-revision-3 scopes expire
at **2026-10-21 04:19:06 CEST** (`1792549146000` ms). That deadline is fixed at
prepare plus 14,400 seconds; commit neither restarts the TTL nor expands scope.
Only the selected discovery host/caller expiry fields and controller-owner
expiry/generation change. No p21 grant, consent or registration is created;
revision 7 remains reserved and unregistered.

Independent review matches all twelve protected source slots: eight present
content hashes and four explicit WAL/SHM absences. Of 358 prior root files, 354
other non-key content hashes and two signing-key metadata observations remain
exact; 355 retain every metadata field. Two policy files have the exact reviewed
changes. The remaining exception is read-store SQLite ctime alone, consistent
with normal opening's mode-0600 refresh; its content and other metadata remain
exact. All 118 old directory identities and both parent directories are preserved.
The controller policy has only its reviewed update, its lock remains exact, and
exactly two canonical review/completion files are added without new directories.

Journal 98/fifteen Cases, zero resource/controller claims, absence of a pending
controller transition and the revision-7 reservation are unchanged. Historical
status identifies the completed delegated review with `authority/granted:false`;
that projection grants no new action. No Bluetooth manager, permission/TCC
probe, hardware trial, root migration, recovery or branch integration runs.
P096-005 remains **partial** under the unchanged qualifier and native-origin
matrix. Future acquisition still requires fresh readiness, stage approvals,
current admission and p21 authority. See
`node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-RENEWAL-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/authority-renewal-20261021-runtime.json`.

### Revision-7 finite campaign checkpoint (2026-10-21)

One freshly approved delegated SSH campaign selects the finite eight-scenario
`authority-loss` plan on source `d5e12c64` and signed GUI `8e5358d0`. Fourteen
operator decisions include five fresh WEAR confirmations. Baseline, protected
stop, runner Case deadline and control-provider loss each report
`observed-released`, confirmed cooperative cleanup, executor exit and release.
These are operational source observations; the Case-deadline episode does not
establish the qualifier's separate native activation-deadline prerequisite.

The fifth episode, `wearer-stop-after-operator-logout`, stops during preparation
before LOGOUT is requested or approved. Its monitor reports `validation-timeout`:
a pending current-authority validation reaches an observed 256 ms against the
unchanged 250-ms budget. The underlying authority predicate is not identified.
Required presets never become validated. Cleanup reports native release
unconfirmed despite executor exit; the controller release is not attempted, and
the exact uncertain claim remains quarantined. The runner halts with a partial
report. Saturation, live revocation and the derived expired-grant probe remain
blocked; no logout, saturation, revocation, retry or recovery occurs.

The offline formal collector retains all five episodes as unbound and creates
zero qualification tuple groups. Exact native launch/exit, native preparation
and execution-origin witnesses remain absent; exit booleans do not replace them.
`qualification:false` and `adoption:false` are preserved, with no formal
prerequisite closure. P096-005 remains **partial** under its unchanged qualifier,
origin matrix and full-tuple requirements. Any subsequent claim recovery or
physical continuation remains a separate decision. See
`node:docs/audits/REVIEW-SENSORIUM-CAMPAIGN-R7-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/campaign-r7-20261021-runtime.json`.

### Validation-timeout software checkpoint (2026-10-21)

The device-free follow-up keeps the historical 256-ms observation unattributed.
Source review finds duplicate private current-owner registration/plan walks and
composes their validated plan within one fresh call. Later validation jobs still
read their current owners independently: no cross-job cache, authority predicate
removal or relaxed 250-ms budget follows.

A separate confirmed publication gap could let successful owner reads wait for
session state beyond that original budget, then clear the validation timer
without checking again. Completion now checks the original queue-time budget
under the same session-state lock before clearing that timer. Queued and
between-stage guards avoid further owner reads when their observed work is
already expired or fenced; late results cannot authorize closed effects. This
repairs an independently identified source defect without attributing the earlier
preparing failure to that path.

Optional bounded diagnostics identify the observer (timer lane or validation
job), current queued/authority/configuration/publication stage and independently
observed segment costs. Unobserved costs remain unknown. These observations carry
no configuration contents, extend no deadline, cancel no blocked owner read and
supply no authority, native-origin or cleanup proof.

This source checkpoint performs no SSH action, target build/signing, hardware
trial, recovery, root migration or branch integration. The prepared candidate,
protected root and existing quarantine remain unchanged; historical records are
not rewritten. P096-005 stays **partial** under its unchanged qualifier and
full-tuple rules. Fresh target preparation and separately approved recovery or
physical work remain distinct. See
`node:docs/audits/REVIEW-SENSORIUM-VALIDATION-TIMEOUT-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/validation-timeout-20261021.json`.

### Validation-client target preparation checkpoint (2026-10-21)

The reviewed validation correction now has a separately pinned release and
signed client on the nearby host: clean Node source `a7266693`, source pin
`035c76a7`, deployment `12e0879b` and GUI `b2c83e3e`. Exact signatures, payload
and sidecar pins, rootless GUI launchd preflight and 202 frozen software checks
pass. The 250-ms gate is unchanged; no new native timing observation or
historical attribution follows from preparation.

Strict custody comparison preserves all 412 prior files, 123 directory
identities, three controller files, journal revision 135 and the quarantined
claim. Only the new GUI capsule is added. No permission probe, manager, physical
trial, authority renewal, recovery, root migration or branch integration runs.
P096-005 remains **partial**. New ad-hoc identity and launch-context evidence do
not reuse TCC or physical qualification. Further root/authority/recovery work
requires its own scope; physical work additionally requires a fresh interactive
readiness question. See
`node:docs/audits/REVIEW-SENSORIUM-VALIDATION-CLIENT-PREPARATION-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/validation-client-preparation-20261021.json`.

### Revision-7 recovery baseline checkpoint (2026-10-21)

One explicitly delegated SSH PREPARE on the verified new image `b2c83e3e` /
source pin `035c76a7` creates unconsumed v3 review `c5f0a9e2` for quarantined
revision-7 Case `5e94e1f8`. Its original source/image and uncertain history are
preserved. The review binds current normal owner/custody, actual kernel epoch,
original Case/journal/controller/resource state and eleven protected presence/
digest slots. No acquisition authority or consent is reused.

All old content hashes and custody match. Only the exact review file and a
disclosed storage-owner read-store ctime refresh appear; raw and conditioned
comparisons remain separate. Journal revision 135, twenty Cases, the sole
transport claim and controller marker are unchanged. The next generation is
proposal data only. There is no reset, consumption, renewal, manager, physical
trial, root migration or branch integration. P096-005 stays **partial**.

This is host-restart-only baseline preparation. Method compatibility/selection,
actual reset observation and recovery consumption remain separately authorized
steps; the baseline does not choose the Bluetooth method or authorize a retry.
Any physical continuation also requires fresh interactive readiness. See
`node:docs/audits/REVIEW-SENSORIUM-R7-RECOVERY-BASELINE-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/recovery-r7-baseline-20261021.json`.

### Revision-7 Bluetooth-method compatibility checkpoint (2026-10-21)

The original uncertain Case source `c06d256a` / `d5e12c64` was absent from the
closed historical source set despite a valid newer-actor v3 baseline. Independent
Git-blob inventory reproduces 5075 retained files and the exact pin. Review of
the actual supervisor launch, captured-image execution and read-only subtree/
ancestor rules establishes compatibility before adding that single exact pin.
Unknown source epochs now refuse before even archiving the predecessor.

This software correction preserves the original Case, v3 baseline and all reset,
process-absence, protected-source and separate-consumption requirements. It is
not reset observation, native cleanup or physical qualification. P096-005 stays
**partial**. See
`node:docs/audits/REVIEW-SENSORIUM-R7-BLUETOOTH-REVIEW-2026-10-21.md`.

### Revision-7 Bluetooth method review checkpoint (2026-10-21)

Clean Node `bcdb7094` pins source `a68c227c`, deployment `4eb902ec` and signed GUI
`d56b6c02`. Exact signatures/pins, manager-free preflights and 202 frozen client
checks on each host pass. One separately delegated native PREPARE creates v4
`18f2b21a` for uncertain Case `5e94e1f8`; the exact original v3 `c5f0a9e2` is
archived byte for byte. Only schema, method scope, actor and review time change.

All eleven protected slots, journal 135/twenty Cases, policy, sole claim and
resource inventory remain exact. Raw/conditioned comparisons disclose the
intentional canonical replacement and ordinary read-store ctime refresh.
The current kernel boot and custody are preserved. There is no reset, manager,
observer, consumption, generation installation, release, renewal, hardware,
migration or integration. The two-hour window has not started: it begins only
at separately authorized observed ON. P096-005 remains **partial**, with native
cleanup uncertain; a physical continuation still requires interactive readiness.
Broader release Clippy retains an unchanged pre-existing audit-sink dead-code
warning; that check is not reported as passing.
See `node:docs/audits/REVIEW-SENSORIUM-R7-BLUETOOTH-REVIEW-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/recovery-r7-bluetooth-review-20261021.json`.

### Observer closure and review refresh checkpoint (2026-10-21)

A rootless metadata preflight does not prove the adjacent reset-observer asset.
The existing Case/campaign GUI capsule stays sealed; its bare copy and added-
resource clone fail signature checks. The complete administrator `4eb902ec` /
source `a68c227c` and pinned observer `4b4d0579` pass strict signature/pin checks.

After explicit operator approval, native Discard archives unused v4 `18f2b21a`,
and supported preparation produces same-case v3 `c2465e4e` / v4 `ffe6987a` for
that administrator. Original and new history bytes, eleven protected slots,
journal 135/twenty Cases, policy, sole claim and resources are preserved.
Expired finite runtime grants remain unchanged: cleanup custody requires current
normal identity and exact enrolled-root ownership, and grants no NativeAdmission.
A real iTerm preflight driven by SSH confirms terminal context. No synthetic TTY,
manager, observer, reset, recovery, release, renewal or integration occurs in this
checkpoint. Fresh interactive OFF/ON readiness remains pending; P096-005 stays
**partial**. See
`node:docs/audits/REVIEW-SENSORIUM-OBSERVER-REVIEW-REFRESH-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/observer-review-refresh-20261021.json`.

### Revision-7 Bluetooth OFF/ON observation checkpoint (2026-10-21)

One fresh interactive approval authorizes a single state-only OFF/ON for v4
`ffe6987a`. Delegated SSH opens a real local iTerm for administrator `4eb902ec` /
source `a68c227c` and observer `4b4d0579`. Native ready/OFF/ON completes with exit
zero, no retry and no synthetic TTY. The durable proof records 3321 ms observed
OFF-to-ON and four worker-absence checkpoints. The two-hour window ends at
13:19:13.104 CEST on 2026-10-21; initial consumption still rechecks same-boot
continuous uptime rather than trusting the displayed wall deadline.

All 434 prior non-key hashes, two key metadata records, 135 directory identities,
eleven protected slots, review/archive bytes, journal 135/twenty Cases, sole
held claim and resource rows remain exact. Only the create-only proof and
ordinary read-store ctime refresh differ; the temporary observer image is removed.
Expired runtime grants are preserved. No recovery consumption, generation
installation, release, scan, acquisition, renewal or integration occurs. Native
stop remains unattested and P096-005 stays **partial**. A separate decision must
authorize exact RECOVER-BLUETOOTH after custody, source, absence and window checks.
See `node:docs/audits/REVIEW-SENSORIUM-R7-BLUETOOTH-OBSERVATION-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/recovery-r7-bluetooth-observation-20261021.json`.

### Revision-7 Bluetooth recovery completion checkpoint (2026-10-21)

The operator separately approves initial RECOVER-BLUETOOTH for revision 7 and
exact v4 `ffe6987a`. Through SSH, administrator `4eb902ec` / source `a68c227c`
rechecks strict pins/signatures, proof `68cd3d30`, same boot, protected sources
and normal cleanup custody. The native owner checks current worker absence and
the continuous-clock window again before effects. One attempt exits zero with
receipt v3; durable phase is completed and pending recovery is absent.

Only the selected acquisition row and old controller claim are removed; the
approved generation is installed with original expiry. Other resource tables,
434 other non-key hashes, two key metadata records, 135 directory identities,
eleven protected slots, journal 135/twenty Cases and bound registration/consent
remain exact. The original Case stays uncertain and native stop remains
unattested. Expected marker, resource-store and policy changes are accounted;
only the ordinary read-store ctime refresh differs otherwise. The prior reset
proof and all review history stay immutable.

No new manager, scan, acquisition, renewal, stopped retirement, root migration or
branch integration runs. P096-005 remains **partial**. Any subsequent retirement,
finite authority renewal and physical campaign need their own approved scope;
this recovery creates no grant or reusable acquisition consent. See
`node:docs/audits/REVIEW-SENSORIUM-R7-BLUETOOTH-RECOVERY-2026-10-21.md` and
`node:docs/evidence/sensorium-host-control-20261019/recovery-r7-bluetooth-commit-20261021.json`.


### Reviewer follow-up checkpoint (2026-10-13)

The first follow-up replaces arbitrary digest metadata with closed
`sensorium-biosignal-sample-block.v1` and `-stream-descriptor.v1` contracts.
The nested buffer is a tensor inside the typed sample-block contract; the
follow-up now closes the remaining P096-002 draft shapes and qualifier. Signal rows, source-time,
package numbers and excluded marker rows come from pinned native metadata,
with one block per preset and no alias duplication. Units and source-clock
uncertainty remain explicit unknowns until profile qualification.
All value and mask segments are individually u64BE length-prefixed. Workers
normalize every negative zero; `nonfinite/count` is worker-declared diagnostics.
Generated fixtures contain no real wearer values; no lab-derived fixture exists
until a real lab observation supplies verified layout.

Operator-supplied hardware fact: Muse 2 firmware `1.0.25`, read from the Muse iOS
application on 2026-10-13. Reconfirm before each observation; an update creates a
new qualification tuple. Hardware laboratory work is assigned to the nearby
`host-B.local` host. Terminal, SSH, supervisor-terminal and supervisor-SSH launch
contexts remain separate TCC observations. No inter-node raw delivery is needed
for this early probe. Neither firmware attestation nor prepared probe code is
measured Bluetooth/runtime acceptance.


### P096-002 ownership and executable contract checkpoint

| Layer | Owns | Explicit boundary |
| --- | --- | --- |
| Declaration | Instance revision, profile/mode intent, desired enabled/disabled state | Saving intent grants no acquisition; exact declaration/package refs identify the reviewed input |
| Admission | Current instance/declaration/package authority and allowed sensitive-personal scope | Signature validity and an earlier journal receipt cannot replace current permission |
| Resolution | Exact package platform, private runtime/home/auth bindings, profile metadata and physical binding | No selector, path or secret enters the portable plan; unresolved real metadata blocks readiness |
| Active execution | Supervisor launch/epoch, source generation, output fence and cleanup evidence | Applying a saved plan never implies Start; replay/recovery never restarts a stopped instance |
| Sample admission | Host-replaced identity, clocks, classification and current source/read authority | Worker diagnostic metadata and content digests establish neither consent nor device identity |

The frozen state/stop table in §6 owns transitions. Status separately reports
configuration, supervisor, acquisition, claim, output fence, pending terminal
outcome and required/optional stream health. `streaming` requires a nonempty fresh
required set, resolved configuration and a ready supervisor. Real-device
streaming additionally requires a held physical claim and available wearer
control. Optional stream loss is degraded. `cleanup-uncertain` keeps the fence
closed and claim held until disposal is proven; idle/blocked/failed release the
claim only afterwards. Stop reasons are typed and carry explicit retryability.

The sample-block metadata uses instance revision and exact profile refs to bind
host-resolved device, package/runtime/firmware and admitted source context. The
first slice is raw; transformed recipes are separate 012 work. Per-block tensors
carry only selected signal rows, source time and package counters. Missing contact
quality and unqualified continuity remain unknown; neither is inferred from
nonzero values. `drain/wall-time` carries an observed UTC value, or explicit null
in conformance/unavailable contexts; product admission supplies its clock mapping.
`nonfinite/count` is worker-declared diagnostics, bounded by the missing mask.

`node:tools/acceptance/sensorium-brainflow/budgets.json` fixes the numeric budget
profile. Worker/native owners enforce allocation, drain and ingress bounds;
the source owner enforces retained events/bytes/age; carrier/read owners enforce
batch, queue and current read-grant bounds; the supervisor enforces exit; host
consent/claim owners enforce TTL, fence and cleanup holds. These are declared
requirements, not measured results. The separate live profile freezes presets,
rates, block size, generation, consumer/device/instance counts, polling/batching,
network/load, warmup/duration/repetitions and injected faults. The qualifier binds
that artifact by digest, checks per-stage timing accounting, rates/startup, every
queue owner, healthy-reader/protected-stop coverage and in-flight revocation.
Unknown measurements cannot pass. Lab observations and conformance/playback
reports cannot qualify a synthetic or Muse hardware execution.

### Independent safety evidence scope (2026-10-21)

The Node-local exporter and independent qualifier now have a separate P096-005
scope. It requires all ten unchanged host-boundary cases in one exact full
deployment tuple, including native origin and current firmware/TCC observations.
The full p21 exposure scope continues to require sixteen native plus ten safety
cases. Neither a partial campaign nor the new safety-only decision supplies
native transport qualification, adoption, P096-011a or release readiness.
At this checkpoint the protected receipt/fence/exact-exit limits remained
250/100/5000 ms. The separately adopted prospective revision 2 below changes
only future validation/receipt/fence budgets, without rewriting this evidence.
This is implemented software conformance; device qualification remains partial.
See `node:docs/audits/REVIEW-SENSORIUM-SAFETY-EXPORT-2026-10-21.md`.

### Accountable call and exact child witnesses (2026-10-21)

Node's normal acquisition worker now observes SDK boundary entries and successful
returns with bounded raw clocks; its source class is still separate from
qualification origin. The normal supervisor supplies a retained exact owned
launch/generation, and the acquisition owner records a conservative exit
observation only after reaping that same launch. Unknown or existing process
groups are not replaced with zero descendants. Exit never attests native release.
The device-free tests establish software conformance, not fresh firmware/TCC,
physical native qualification or adoption. Existing target packages/clients are
not upgraded in place. P096-005 remains partial.

### Completed owner-fact exporter (2026-10-21)

The offline Node exporter now projects retained owner measurements into the ten
existing P096-005 case types. It derives result/budget/control summaries, checks
exact source/run/harness/tuple/Case bindings and corroborates actual native,
private-control, fault and host-software witnesses before the unchanged Schema
Gate and semantic gates permit publication. Raw restart observation stays separate
from the original Case. Missing observations yield explicit partial coverage;
no source label, readiness, bool or historical firmware/TCC note fills a gap.
Its own source closure and consumed evidence refs are retained independently of
the standard-library-only qualifier. Full p21 still requires sixteen additional
native transport cases; software exporter completion does not complete P096-005,
native exposure, launchd scope, P096-011a or release acceptance. No hardware,
reset, recovery, target mutation or branch integration occurred.

Final containment review requires the captured actually enforced no-fork adapter
before group absence can supply a zero-descendant observation. A declarative
flag without that adapter, EPERM or an existing group keeps the fact unknown.
This restriction preserves the original qualification requirements.


### Frozen safety-export client preparation (2026-10-21)

Node now freezes the offline exporter, its report and qualifier siblings and a
separately pinned content-only Schema Gate in each new signed-client handoff.
The exporter still records its five-file source closure separately from the
qualifier/interpreter/Gate identities. New capsule readers reject absent,
changed or extra files; historical readers and handoffs remain immutable.
Device-free client conformance does not supply native case measurements, refresh
firmware/TCC evidence or complete P096-005. Installing a client does not replace
an existing registered worker; changed worker bytes need their own reviewed
package transition before a later authorized measurement. The ten-case safety
scope, full sixteen-plus-ten native scope and all numeric gates stay unchanged.
See `node:docs/audits/REVIEW-SENSORIUM-SAFETY-CLIENT-PREPARATION-2026-10-21.md`.


The target preparation now binds corrected Node source `065bd6fb`, source pin
`1713fa35`, release `f734f50a`, signed GUI `bdd1016a` and handoff `68d332ae`.
All 244 frozen software checks pass locally and on target Python 3.13.15, with
exact file/signature/Gate and rootless GUI launchd verification. All 438 prior
root files, journal/history, expired authority and controller custody remain
unchanged; only the new capsule is added. The existing worker remains unchanged
and differs from the new SDK-observation source. A separate reviewed package
transition is required before later native measurement. No Bluetooth, grant
renewal, recovery, root migration, hardware qualification or merge occurred.


### Immutable SDK-observation package transition (2026-10-21)

The separately authorized SSH transition signs distinct ordinary and campaign
SDK-observation packages through the normal initialized PrimaryParticipant.
Both exact source inventories and Ed25519 sidecars pass independent verification,
including changed-preimage refusal. Earlier packages, approvals, runtime capsules
and historical Case/consent/recovery bytes remain unchanged. The recovered,
expired revision 7 retires through its exact reviewed normal-owner corridor,
reserving revision 8 for fresh SCAN/BIND/REGISTER/WEAR. No p21 grant or consent is
created or transferred by package approval or retirement.

A separate exact delegated renewal grants the same controller/discovery scope
for 14400 seconds, fixed at prepare and expiring 2026-10-21 18:06:05 CEST. This
is bounded metadata authority, not a native permit, human-presence attestation
or fresh TCC/firmware observation. Corrected clean Node source `b4bc9862` / pin
`1cda5c5f`, release `c33ac91d`, signed GUI `d21848bb` and handoff `0b768e43` select
the new immutable packages. All 244 frozen software checks pass on target
Python 3.13.15, plus isolated normal-key author/sign conformance for all four
package kinds. Rootless GUI launchd observation supplies no Bluetooth permission.
No hardware, reset/recovery, format migration, merge or adoption occurs.
P096-005 and the full native matrix remain partial; later physical work needs
fresh interactive readiness confirmation and actual permission checks for the
new ad-hoc GUI identity. See
`node:docs/audits/REVIEW-SENSORIUM-WORKER-TRANSITION-2026-10-21.md`.


### Revision-8 finite campaign checkpoint (2026-10-21)

Revision-8 physical SSH campaign on source b4bc9862/pin 1cda5c5f completed baseline and protected stop, then stopped during the deadline episode on timer-lane validation 273 ms against the original 250 ms gate. Protected receipt/fence/exact-exit measured 1/0/4717 ms; all three sessions released with current durable audit and zero claims. SDK entry/return and exact exit witnesses are now present. Three unbound collector episodes supply no formal cases; TCC attribution/full tuple and remaining safety witnesses are still missing. No retry/recovery/merge followed; P096-005 remains partial. See node:docs/audits/REVIEW-SENSORIUM-R8-CAMPAIGN-2026-10-21.md. The unchanged origin matrix, exact tuple and independent qualification remain required.


### Prospective control budget revision 2 (2026-10-21)

After the immutable revision-8 campaign, the operator explicitly approved a 25%
increase for live validation and protected receipt/fence. Validation and receipt
use integer ceilings of 313 ms (312.5 rounded upward); fence is 125 ms. Process
exit remains 5000 ms. All case, consent, grant, cleanup, origin, full-tuple and
per-case proof requirements remain unchanged. The 250-ms retained-state monitor
cadence remains separate from its 313-ms pending-job budget, with scheduling
uncertainty explicitly disclosed. Protected stop remains independently served.

New independent qualifier identities are `sensorium-native-p21-qualifier.v2` and
`sensorium-native-safety-qualifier.v2`. The v1 report shape preserves the historical
identity structurally; current admission still requires the exact newly known
v2 purpose-qualifier artifact. No old report is re-qualified or rewritten. Old
source/GUI/worker pins and nearby roots are unchanged until separate artifact
preparation. P096-005 remains partial; this policy change proves no native
latency improvement and authorizes no retry. See
`node:docs/audits/REVIEW-SENSORIUM-CONTROL-BUDGET-V2-2026-10-21.md`.


### Merged budget-v2 client preparation (2026-10-21)

Merged source 351861c9/pin e55f71a9 now has a verified nearby budget-v2 release b8bf7e8f, signed GUI 3be08e12 and handoff 59362613. Validation/receipt/fence/exit ceilings are 313/313/125/5000 ms. Merged checks pass 148 Rust, 6 Gate, 245 local and 245 nearby frozen-client cases; 22 ledger checks also pass. Exact old root/custody, journal 158 and zero claims remain unchanged; only the new capsule is added. Both temporary worktrees are retained after the approved initial merges; preparation records remain unmerged. No Bluetooth, grant renewal, recovery, migration or native qualification follows. P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-MERGED-BUDGET-CLIENT-2026-10-21.md. Historical campaign results retain their original gates; future hardware evidence must bind this exact candidate and current v2 qualifier.


### Released revision-8 retirement (2026-10-21)

Released revision 8 retired through exact review 728de054 and unchanged journal 158, reserving revision 9. All old Cases, consent, packages, owner/discovery expiry and custody remain; no grant, recovery or hardware effect was created. P096-005 stays partial; fresh SCAN/BIND/REGISTER/WEAR are required. See node:docs/audits/REVIEW-SENSORIUM-R8-RETIREMENT-2026-10-21.md.


### Deadline consumer source correction (2026-10-21)

The deadline campaign branch now continues ordinary authorized draining after readiness, preserving all queue and clock limits and propagating failures without relabelling them as expected deadline evidence. Four bounded-producer regressions cover draining, overflow, pre-existing fence and failure precedence. This is source conformance only; P096-005 remains partial pending a fresh pinned client and native evidence. See node:docs/audits/REVIEW-SENSORIUM-DEADLINE-CONSUMER-2026-10-21.md.


### Deadline consumer client preparation (2026-10-21)

The deadline-consumer correction is prepared nearby from clean source 8cfd21e6/pin 2c4f9669, release 0a85fca5, signed GUI b1f287a3 and handoff 7ba30f4d. All 245 frozen target checks pass against 68 independently matched immutable inputs; all 557 prior root files/custody remain exact, with only the new capsule added. Signature and rootless launchd preflights pass; preparation creates no Bluetooth manager or qualification. Review and originals are pinned by private manifest sha256:0451b14a4e46acd45ab8884815688f1020ef77962f9092559c6588c3b5f2a446. Native permission and the separately approved campaign remain distinct stages. P096-005 stays partial.

### Revision-9 campaign checkpoint (2026-10-21)

Revision-9 campaign on corrected source 8cfd21e6/pin 2c4f9669 completed baseline and protected stop (receipt/fence/exact-exit 1/1/4940 ms), then halted during deadline on sample/discovery-provider-output-refused. All three sessions released with durable audit and zero claims; journal is 181 with 26 Cases. Five later rows are blocked, and P096-005 remains partial. After the initial blocked transfer and the operator's direct plain-text confirmation, all 28 reports (27534 bytes), 19 continuous events and three client-control sidecars are now retained privately and independently verified against the frozen parsers and original local stream; remote originals remain unchanged. Private manifest sha256:68378b0389467d85d926b0b6f36b8ca529ed70a5f2ad73d2378115c5f6ef384a binds the 54-member verified archive. Full tuple and formal qualification remain open. No retry, recovery or merge followed. See node:docs/audits/REVIEW-SENSORIUM-R9-CAMPAIGN-2026-10-21.md.


### Revision-9 sample software correction (2026-10-21)

Device-free reproduction confirms that one queued producer batch per admitted
sample RPC cannot keep up with nominal 100-ms production and a 300-ms consumer:
the real worker loop over a synthetic Board fails at tick 13, after four reads
and 26 simulated SDK drains. The repair returns a FIFO prefix of unchanged
blocks, at most sixteen per RPC within existing byte, queue and age bounds. The
host validates consecutive per-stream sequences before committing progress.
Closed first-worker-failure diagnostics survive cleanup; review also closes a
failure-between-selection-and-response race without blocking pending cleanup.
Distinct SDK-batch package identities require new normal author/sign and a new
pinned daemon/client. Software checks pass 220 daemon cases (11 opt-in ignored),
six Schema Gate cases and 165 Python cases. Historical r9 cause and full
qualification remain open;
P096-005 is partial, with no device work, target/root change or merge. See
node:docs/audits/REVIEW-SENSORIUM-R9-SAMPLE-DRAIN-2026-10-21.md.


### SDK-batch target preparation (2026-10-21)

The device-free correction now has a new pinned nearby release and signed frozen
client from clean Node source `393688e6`/pin `7d5aa913`, image `8d123d82`, GUI
`bd0afa36` and handoff `dfde3be8`. Two distinct ordinary/campaign SDK-batch
packages (`37f55642`/`90238894`) are normally authored, signed and independently
verified; both remain inactive and do not replace the stopped revision-9
registration. All 253 frozen target software tests pass against 69 exact inputs
with zero skips. Initial freeze/test-kit defects remain retained and corrected;
no native result or threshold is reinterpreted.

All earlier root content hashes, key metadata, controller, directory custody,
registration, consent and journal remain preserved, apart from an explicitly
reviewed read-store ctime refresh. No manager, permission probe, scan,
acquisition, renewal, registration transition, root-format migration or merge
runs. The unchanged finite controller authority is expired. P096-005 stays
partial; future hardware work needs current authority, supported registration
handling and fresh interactive wearer readiness. Private preparation manifest:
`sha256:60264ebd6b895d816e42a1d35d5b1e69bb8e4b4027290d47776fddd1e9336b5c`. See
node:docs/audits/REVIEW-SENSORIUM-SDK-BATCH-PREPARATION-2026-10-21.md.


### Revision-9 authority renewal and retirement (2026-10-21)

The existing exact SDK-batch candidate (`393688e6`/source `7d5aa913`, release
`8d123d82`) now completed separately reviewed delegated SSH metadata operations:
renewal `ad0e8c03` extends the same controller/discovery scope for four hours to
**2026-10-22 00:53:26 CEST**; released-case retirement `cab3fb4c` then removes
only expired stopped revision 9 and its binding, reserving unregistered revision
10. The p21 grant is not renewed or replaced. Both reviews and completed live
projections are independently verified before and after their respective commits.

Controller/resources have no claims or pending recovery. Journal 181/twenty-six
Cases, consent, old signed packages/capsules and directory custody remain exact;
the review accounts for seven intended owner/source content changes and a
read-store ctime refresh. No new consent, grant p21, native manager, hardware,
recovery, root-format migration or merge runs. P096-005 remains partial. Future
physical use needs current authority and fresh interactive wearer readiness,
then separate SCAN/BIND/REGISTER/WEAR decisions. The private manifest is
`sha256:5fdca8b91c37f7741c7d7da589b623bff4bcc92c4c4112e8136a76e77f76a48b`; see
node:docs/audits/REVIEW-SENSORIUM-R9-AUTHORITY-RETIREMENT-2026-10-21.md.

### Prospective operation retries — 2026-10-21

The operator approved doubled operation waiting timeouts and two additional serial
attempts of each timed-out operation, rather than replay of a complete sequence.
A step that succeeds on attempt 1, 2 or 3 succeeds; retain the attempt ordinal and
prior timeouts. This changes prospective implementation/qualification policy, not
historical evidence. Current authority, consent scope, parent deadlines and
confirmed disposal before repetition remain mandatory. Unknown cleanup retains
quarantine and requires its separately authorized recovery corridor. No retry can
renew consent or mint an additional registration after an uncertain commit.

Revision-10 baseline released, but protected-stop preparation stopped on 359946 us
against the original 313-ms validation gate; native release was not confirmed and
six later rows were blocked. The private 23-file report set is pinned by manifest
sha256:75691f4e1959626f5035f637a4e33d9cd34504f44cf65e13fda6a3f4f1a4f302.
P096-005 remains partial. The code-coupled contract, current limits and review
status are owned by node:docs/operations/SENSORIUM-OPERATION-RETRIES.md; review of
the old run is node:docs/audits/REVIEW-SENSORIUM-R10-CAMPAIGN-2026-10-21.md.


Pinned operation-retry preparation is verified on source c834ad91/pin be42586a:
release 56b0de73, signed GUI ce1e450e/handoff b2cf05e1 and three new inactive signed
packages. All 265 nearby frozen checks pass after retaining/correcting an omitted
test-input dependency; local checks pass 323 Python and 261 discovery/acquisition
cases. Existing root contents, controller state and journal 197/28 Cases remain
preserved with the explicit normal read-store ctime exception. The one revision-10
claim remains quarantined; no new hardware, reset, recovery, renewal, migration
or merge occurred. Preparation manifest
sha256:93a87ec5420aebcee4648d5ca952755d8a4a7e23fe8e8518382344fd26bc6063.
P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-OPERATION-RETRIES-2026-10-21.md.


Revision-10 v3 baseline 1a0d0370 / v4 1f055b3e now preserve the exact predecessor
and one separately approved Bluetooth OFF/ON proof f90a4aa2. Real-iTerm observation
on pinned release 56b0de73 completed with native exit zero, 2492 ms OFF-to-ON and
four worker-absence checks. All 761 prior file records, 205 directory identities,
parent custody, journal 197/28 Cases, eleven source slots and held claims remain
preserved; only the normal read-store ctime refresh differs. Nine reviewed files
and two directories are added. No consumption, recovery, release, renewal, scan,
acquisition, migration or merge occurred. P096-005 stays partial; separate exact
RECOVER approval remains required. See node:docs/audits/REVIEW-SENSORIUM-R10-BLUETOOTH-OBSERVATION-2026-10-21.md.


Separately approved revision-10 RECOVER-BLUETOOTH for v4 1f055b3e / proof
f90a4aa2 now completes once through SSH on pinned release 56b0de73. Independent
readback confirms the completed marker, exact reviewed generation, free
controller and removal of only the selected acquisition claim. Journal 197 /
28 Cases, the uncertain historical Case, eleven source slots, binding,
registration, consent, expiry and parent custody remain preserved. All 770 old
file records and 207 directories are reconciled; only the reviewed resource
update and ordinary read-store ctime refresh differ. Private manifest fcd00510
binds verified recovery evidence. No new manager, scan, acquisition, renewal,
retirement, transition, migration or merge occurred. P096-005 stays partial.
See node:docs/audits/REVIEW-SENSORIUM-R10-BLUETOOTH-RECOVERY-2026-10-21.md.


### Revision-10 retirement corridor and discovery transition (2026-10-22)

The consumed revision-10 retirement had published its four reviewed sources and
imported the remaining inventory, but the inert stopped apply refused the
revision-3 discovery capsule: release c834ad91 compares capsules with its own
known worker sources, three of which changed. Owner/discovery authority then
expired, renewal refused the incomplete history, and no command could finish
the decision. This is package-generation drift, not a native or authority fact.

Node 6f3fb7be (pin bf66e757, release 7d2df3ea) keeps finish failures as closed
stages with the owner refusal family. Resume of an already consumed review holds
exclusive controller custody without owner currency; only when every remaining
grant expired does it import the exact reviewed bytes, with package material
verified and nothing applied. Prepare, commit and new authority still require
current ownership. The discovery hop becomes data with both historical slots
protected, and the p21/discovery known-worker guards now admit the packaged
operation_retry.py that the operation-retry source omitted.

On turbo, one resume completed retirement 67864dff and reserved unregistered
revision 11. After the user approved SIGTERM to six orphaned, unverifiable
crashpad processes of another application, delegated-SSH renewal a40e3413
extended the same controller/discovery scope to 2026-10-22 16:46:45 CEST, and
transition 2040f9c7 moved discovery to operation-retries revision 4 with a
byte-exact capsule and successful inert apply. 773 old files, 207 directories,
parent custody, journal 197/28 Cases and idle resources are preserved; the full
normal-key matrix passes 12 of 12. No SCAN, BIND, REGISTER, WEAR, measurement,
root migration or merge occurred, and P096-005 remains partial. See
node:docs/audits/REVIEW-SENSORIUM-R10-RETIREMENT-CORRIDOR-2026-10-22.md.

Session renewal 9ee35c69 then extends the same controller and revision-4
discovery scope to 2026-10-22 22:02:32 CEST, again changing only expiry and
generation. Because the current release differs from the earlier operation-retry
release only in its daemon image, the campaign GUI handoff is rebuilt as
cfdc433f around that daemon; strict signature, GUI launchd preflight and all 265
frozen target checks pass. No headband work occurred; a session still needs its
interactive readiness question and fresh scoped approval. P096-005 stays partial.


### Current pinned-client preparation — 2026-10-23

Clean source 48bab564/pin 28efc4c6 now has a newly transferred release 540f1198
and sealed signed client 4364b1a6/handoff 15c50611. Offline locked Cargo validates
exact cached artifacts; no new compiler execution is claimed. Independent
source/postlink/signature checks and 265 frozen target tests pass with no skips.
All 843 prior root file records, 225 directory identities, parent custody,
journal 202/29 Cases and the held revision-11 claims remain exact; only the new
fifteen-file client capsule is added. Expired authority stays expired. No
permission probe, manager, hardware, recovery, renewal, migration or merge runs;
P096-005 remains partial. Private proof manifest
sha256:8f593bef88f6bf21673c8b7f0e04e6e167dadb990eae68ea867eecbfbf4b4b03.
See node:docs/audits/REVIEW-SENSORIUM-CLIENT-PREPARATION-2026-10-23.md.

### Revision-11 recovery baseline — 2026-10-23

Pinned release 540f1198/source 28efc4c6 prepared fresh v2 baseline 36f45aea for
the revision-11 pre-binding Case through delegated SSH. The supported exact
discard archived old review 566f70a2 byte for byte before preparation; both
quarantined claims, journal 202/29 Cases, configuration, consent and expired
authority remain preserved. Independent review passes. No reset method,
observation, recovery, release, hardware work or merge occurs; P096-005 stays
partial. Reset-method selection and eventual RECOVER remain separate decisions.
See node:docs/audits/REVIEW-SENSORIUM-R11-RECOVERY-BASELINE-2026-10-23.md.

### Pre-binding Bluetooth recovery method — 2026-10-23

The Node correction extends exact v4 method selection to an original v2
pre-binding baseline, preserving that scope and its byte-exact predecessor.
The original journal's discovery-plan/package anchors selection of current
normal host-grant and protected-source custody; this is newly observed cleanup
custody, not retrospective grant attestation or runtime authority. Changes to
that custody refuse later observation/consumption. Bound acquisition scope and
existing bound-v4 preimages retain their meaning. Method selection, OFF/ON
observation and RECOVER remain separate decisions; P096-005 remains partial.
See node:docs/audits/REVIEW-SENSORIUM-PRE-BINDING-BLUETOOTH-2026-10-23.md.

On pinned administrator 8ff445ae (source 9a14cd46/pin 4db636c8), one delegated-SSH
selection prepared pre-binding v4 review e79bd11c and archived predecessor
36f45aea byte for byte. Root/custody checks reconcile 859 old files and 231
directories; journal 202/29 Cases, both quarantined claims and expired authority
are unchanged. No observer/reset proof or consumption is created. The two-hour
window awaits a future observed powered-on event, with expiry still null.
This is configuration evidence only; no reset, release, acquisition or merge
occurred and P096-005 remains partial.

The subsequently authorized real-terminal SSH OFF/ON observation for e79bd11c
refused before ready at the process-absence guard. Two own-UID orphaned crashpad
helpers have unavailable executable paths (ENOENT); no admitted executable was
found by read-only diagnosis. No signal, repeat or state-manager construction
occurred. Review/predecessor, both quarantined claims, journal 202/29 Cases,
sources and expired authority remain preserved; no reset proof or consumption
was created. Helper termination and a fresh observation require a separate
operator decision. P096-005 remains partial. See
node:docs/audits/REVIEW-SENSORIUM-R11-BLUETOOTH-OBSERVATION-2026-10-23.md.

After a separate explicit decision, exactly the two freshly reverified helpers
ended with SIGTERM, without escalation. A new process probe found zero admitted
or unverifiable processes. One fresh state-only SSH observation in real iTerm
for v4 e79bd11c then completed: OFF for 3241 ms, four worker checks, native exit
zero and captured-image removal. Proof 3a57b87b binds the exact administrator,
observer, boot and raw v2 predecessor; its separate approval window ends at
2026-10-23 04:30:41 CEST. Independent custody checks preserve 860 old file records,
231 directory identities, eleven sources, journal 202/29 Cases and both
quarantined claims; only the proof and ordinary read-store ctime differ.
The first refusal remains frozen. Authority stays expired, revision 11 remains
pre-binding/unregistered, and recovery has not executed. No scan, acquisition,
release, renewal, migration or merge occurred. P096-005 stays partial; a separate
RECOVER approval and fresh validation are still required. See
node:docs/audits/REVIEW-SENSORIUM-R11-BLUETOOTH-OBSERVATION-RUN02-2026-10-23.md.

### Revision-11 separately approved Bluetooth recovery — 2026-10-23

The operator subsequently approved exact RECOVER-BLUETOOTH for v4 e79bd11c and
proof 3a57b87b. Fresh actor/signature/boot/proof-window/source/custody and process
checks passed before one direct SSH commit on administrator 8ff445ae. Durable
marker 6b87244b is completed, the reviewed policy is exact, the old controller
claim and selected discovery resource are removed, and no pending recovery
remains. Cleanup custody preserves expired runtime authority; policy changes
only generation, leaving expiry unchanged.

Comparison reconciles 861 old file records and 231 directories: journal 202/29
Cases, exact review/v2 predecessor/proof, eleven sources, configuration, consent,
grants and history remain preserved. Only reviewed disposal writes, the completed
marker and ordinary read-store ctime differ. Revision 11 remains pre-binding and
unregistered, with no invented BIND/REGISTER/WEAR. No new state manager, headband
trial, authority renewal, retirement, package transition, migration or merge runs.
This is disposal evidence; P096-005 stays partial. See
node:docs/audits/REVIEW-SENSORIUM-R11-BLUETOOTH-RECOVERY-2026-10-23.md.

### Four-hour controller/discovery renewal — 2026-10-23

The operator separately authorizes same-scope delegated-SSH renewal after
revision-11 recovery. Review e8aada04 completes once on administrator 8ff445ae
(source 9a14cd46/pin 4db636c8), anchored on completed retirement 67864dff for
10→11. TTL 14400 starts at preparation and expires 2026-10-23 06:59:02 CEST.
Only controller expiry/generation and the selected revision-4 host/caller
discovery expiries change. No p21 grant or wearer consent is created.

Independent checks reconcile 862 old file records, 231 directories and custody;
twelve protected sources, journal 202/29 Cases, idle resources, retirement history
and revision-11 recovery/review/proof remain exact. Additions are the exact review
and completed marker; ordinary read-store ctime is the other metadata exception.
Status records the last delegated renewal without granting authority or observing
live ownership. Revision 11 remains unregistered and P096-005 partial. No native
manager, headband trial, package transition, root migration or merge occurs;
future physical work still requires an interactive readiness question and fresh
scoped approval. See
node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-RENEWAL-2026-10-23.md.

### Revision-11 campaign compatibility preflight — 2026-10-23

Before physical work, review finds that the earlier pinned GUI cannot recognize
the newly completed pre-binding recovery review. Full historical parsing, rather
than byte integrity alone, determines compatibility. Retained review fields and
predecessor are preserved; the client is updated instead. Fresh signed GUI
c9200220 / handoff 64e3798e uses the already pinned compatible 9a14cd46 image
8ff445ae / source pin 4db636c8 and unchanged client/helper assets, without a new
compiler execution or package transition. Strict signatures, rootless launchd
preflight and 265 software checks pass.

All 864 previous file records, 231 directories, custody/controller, journal
202/29 Cases, revision-11 recovery/history and finite authority remain exact;
only fifteen new capsule files in six directories appear. Fresh readiness is
still required, using actual SCAN/preparation/session/cleanup/Case/campaign
limits of 20/60/90/20/180/1800 s. Native operation timeout retries do not replay
BIND/REGISTER/WEAR decisions or renew authority. No permission probe, native
manager, scan, acquisition, recovery, renewal, migration or merge occurs;
revision 11 remains unregistered and P096-005 partial. See
node:docs/audits/REVIEW-SENSORIUM-R11-COMPATIBLE-CLIENT-2026-10-23.md.

### Revision-11 final helper runtime guard — 2026-10-23

One approved campaign on compatible GUI c9200220 / source 4db636c8 stops during
baseline SCAN; seven later rows are blocked and no BIND/REGISTER/WEAR/acquisition
occurs. The final supervisor guard still rejects runtimes above 45 s, while the
request is 50 s and the host ceiling 108 s. One shared supervisor constant now
joins the final guard and helper profile without changing actual deadlines,
worker budgets or authority. A real-spawn regression fails with the old guard;
58 supervisor, five daemon profile and 29 console checks pass after correction.
Closed readback links the new uncertain Case to held controller and discovery
claims; journal is 207/30, previous grants/packages/history/custody are preserved.
Permission-only allowed and remembered firmware provide no new qualification.
The fix is local; no new target build, replay, recovery, reset, renewal, further
headband action or merge occurs. P096-005 remains partial. See
node:docs/audits/REVIEW-SENSORIUM-HELPER-RUNTIME-BOUND-2026-10-23.md.

### Corrected final-helper client preparation — 2026-10-23

Clean Node 08cf7c20 now builds source d0d3b335 over 5146 entries into standalone
release d11afcd7 and a new target GUI 3370c13a / handoff 657a0c68. Daemon Cargo
fresh=false records actual new compilation; the validator is verified from cache.
Reviewed postlink/signature equivalence, exact closures, external runtime checks,
rootless launchd preflight and 265 target software tests pass. The final shared
helper ceiling is 108 s; the actual Case SCAN remains 50 s, without broader
runtime authority. All 894 old file records, 238 directories, controller/parent,
journal 207/30, quarantine, packages, grant expiry and history stay exact; only
fifteen capsule files in six directories appear. New TCC is unobserved. Future
recovery from prior source 4db636c8 remains separately reviewed; the older
administrator is retained. No permission probe, headband, recovery, renewal,
transition, migration or merge runs. P096-005 stays partial. See
node:docs/audits/REVIEW-SENSORIUM-HELPER-CLIENT-PREPARATION-2026-10-23.md.

### Current revision-11 quarantine baseline — 2026-10-23

Verified standalone d11afcd7 / source d0d3b335 prepares exact v2 review 0a5cfa9c
through one SSH PREPARE for current uncertain Case 4e6f2774 from source 4db636c8 /
GUI c9200220. The no-radio baseline path is compatible without extending the
prior-source allowlist; future Bluetooth/v4 admission remains separate. Review,
journal/record hashes, controller snapshots and all resource tables match. Only
the proposed generation changes; it is not installed. All 909 old observations
preserve 907 non-key hashes and two key-metadata records; the only metadata
exception is read-store ctime. All 244 directories, controller/parent, journal
207/30, held claims, expired finite authority and history remain unchanged.
One new review appears, with no discarded predecessor, reset/proof/consumption,
recovery, renewal, hardware, migration or merge. P096-005 stays partial. See
node:docs/audits/REVIEW-SENSORIUM-R11-CURRENT-BASELINE-2026-10-23.md.

### Current revision-11 Bluetooth method review — 2026-10-23

One SSH method preparation selects v4 ea635e8c for uncertain pre-binding Case
4e6f2774 and archives baseline v2 0a5cfa9c byte-exact (8497 bytes). Retained
administrator 8ff445ae / source 4db636c8 recognizes the Case source as current;
its 5146 inventory entries, five-file target closure, strict signatures and
rootless preflight are verified. The supported actor change leaves baseline
actor d11afcd7 / d0d3b335 in the archive. No prior-source pin or production code
changes. Only schema, creation time, candidate and radio witness change in v4;
eleven fixed protected-source slots and the matching plan/grant are checked.
Among 910 prior file observations, 908 are identical; canonical review becomes
v4 and read-store ctime is the only other metadata difference. All 907 other
non-key hashes, two key-metadata records, 244 directories, controller/parent,
journal 207/30, held claims, resource tables and finite expiries stay exact.
Private manifest 8f6f51bf and archive 25af43c1 pass 44-member retrieval and
PRIMARY_EVIDENCE_STORE copy readback. Independent review corrects draft guidance:
expired policy/grant bytes remain frozen cleanup custody; no renewal is required
merely for a separately approved OFF/ON observation. V4 awaits that observation,
with no proof or approval-window expiry yet. No observer, reset, recovery,
claim release, grant renewal, hardware, migration or merge runs. P096-005 stays
partial. See
node:docs/audits/REVIEW-SENSORIUM-R11-CURRENT-BLUETOOTH-REVIEW-2026-10-23.md.

### Current revision-11 Bluetooth OFF/ON observation — 2026-10-23

One explicitly approved state-only observation runs through SSH in a real iTerm
on retained source 4db636c8 / administrator 8ff445ae for v4 ea635e8c. Fresh
closure/signature, review/predecessor, boot, protected-source and process checks
pass. The operator toggles Bluetooth; protected proof 24831c70 records OFF for
3002 ms, four worker checks and native exit 0. Captured observer image is
removed; no scan or headband acquisition starts. Approval window ends at
1792749389394 (2026-10-23 11:56:29.394 CEST). All 909 old non-key hashes and
two key-metadata records are exact; 910 of 911 full observations are unchanged,
with read-store ctime the only exception. Exactly one protected proof appears;
244 directories, parent/controller, journal 207/30, held claims, resource tables,
expired finite authority and byte-exact v4/v2 archive remain unchanged.
Independent review passes; private manifest 17428fc9 and archive 9954535a pass
166-member retrieval and PRIMARY_EVIDENCE_STORE copy readback. No retry, recovery,
claim release, consumption, generation installation, renewal, migration or merge
occurs. P096-005 stays partial. RECOVER remains a separate approval with fresh
proof/custody/window checks; no new runtime authority or consent is implied. See
node:docs/audits/REVIEW-SENSORIUM-R11-CURRENT-BLUETOOTH-OBSERVATION-2026-10-23.md.

### Current revision-11 Bluetooth recovery completion — 2026-10-23

After explicit RECOVER approval, fresh exact actor/signature, boot/window,
review/proof, protected-source, claim/resource and process checks pass. One direct
SSH commit on retained 4db636c8 / 8ff445ae consumes v4 ea635e8c and OFF/ON proof
24831c70 for pre-binding Case 4e6f2774. Receipt v3 and completed marker 8baaaf7c
bind the exact disposal: one discovery resource and old controller claim removed,
reviewed next-policy bytes installed. Only generation changes; expiry 1792731542000
stays expired. V4, v2 archive 0a5cfa9c, reset proof, journal 207/30, consent,
grants, sources and historical uncertain Case remain unchanged. Root 912 to 913
adds only completed marker; 910 full prior observations exact, resource DB data
and ordinary read-store ctime are the two differences. All 909 other non-key
hashes, two key-metadata records, 244 directories and parent custody are exact.
Independent review passes; private manifest b45d7b2e and archive 13b5074d pass
47-member and PRIMARY_EVIDENCE_STORE readback. No retry/resume, renewal, OFF/ON state observation,
scan/acquisition, retirement, transition, migration or merge runs. P096-005 stays
partial; future runtime authority and fresh headband approvals remain separate. See
node:docs/audits/REVIEW-SENSORIUM-R11-CURRENT-BLUETOOTH-COMPLETION-2026-10-23.md.

### Four-hour authority renewal after current revision-11 recovery — 2026-10-23

After exact recovery marker 8baaaf7c and idle-state checks, one explicitly
delegated SSH PREPARE/COMMIT on retained 4db636c8 / 8ff445ae completes review
2314cc5b. The latest completed retirement 10→11 remains anchor 67864dff; current
recovered Case 4e6f2774 and reservation 11 are preserved. Controller owner and
existing discovery host/caller grants expire at 1792769759000, 2026-10-23
17:35:59 CEST, four hours from prepare. Only two discovery expiry projections
and controller expiry/generation change; no p21 grant, registration or consent
appears. Root 913 to 915 adds only review and completed marker 97ff1ee6. Of 913
prior observations, 910 are fully exact; all 909 other non-key hashes, two
key-metadata records, 244 directories, parent custody, idle resources, twelve
protected-source slots, journal 207/30 and all recovery/history remain exact.
Ordinary read-store ctime is the sole other metadata difference. Status records
last renewal 2314cc5b, active 0 / stalled 0, without granting authority itself.
Independent review and private manifest 2feb3c1a / archive f6567319 pass
64-member and PRIMARY_EVIDENCE_STORE readback. Manager-free helper process
probes run; no Bluetooth manager, headband, reset/recovery, transition, migration
or merge occurs. P096-005 stays partial; new physical work requires fresh
interactive readiness and SCAN/BIND/REGISTER/WEAR. See
node:docs/audits/REVIEW-SENSORIUM-AUTHORITY-AFTER-R11-RECOVERY-2026-10-23.md.

### Revision-11 campaign run02 and reporting repairs — 2026-10-23

One freshly approved SSH campaign on frozen source d0d3b335 / GUI 3370c13a
passes exact-client Bluetooth permission preflight, then stops at SCAN with
`campaign-episode-interrupted`. Fourteen original files / 5476 bytes are retained.
Only CAMPAIGN and SCAN decisions are sent; no BIND, REGISTER or WEAR. Exact host
Case e7f947bb is released/abandoned, journal 212/31, with no controller/resource
claim or surviving worker. Revision 11 remains unregistered. Native start,
native cleanup and the primary scan cause are unestablished without the missing
terminal. Firmware 1.0.25 remains historical. Controller files, all 244 prior
directories, grants, consent, completed recovery and history are preserved.
Independent review repairs closed typed-discovery terminal coverage, stale
completion timestamps and exporter/collector budgets against unchanged qualifier
v3. Device-free checks pass 152 + 42 tests; the failed combined-interpreter
invocation remains retained and documented. Frozen reports are unchanged;
P096-005 remains partial. Private manifest baefff7f / archive 3eeb65d6 pass
115-member retrieval and PRIMARY_EVIDENCE_STORE readback. No physical retry,
reset/recovery, renewal, migration or merge occurs. The deployed client still
requires a new immutable build before another freshly approved physical trial.
See node:docs/audits/REVIEW-SENSORIUM-R11-CAMPAIGN-RUN02-2026-10-23.md.

### Reporting-client preparation after revision-11 run02 — 2026-10-23

Clean Node e4e13b72 builds source 5f2aeda0 over 5146 entries into signed
standalone 2eda2db5 and a fresh target GUI 47a5cf76 / handoff 1036b698.
Nineteen release files, sidecars and eighteen loaded sections are independently
verified. The 73-input frozen kit includes both Rust owners; isolated runtime
231 and exporter 42 tests pass, zero skips/failures/errors. Worker, native assets,
qualifier and retry limits remain unchanged. Rootless LaunchServices preflight
passes as launchd; new ad-hoc identity Bluetooth permission remains unobserved.
All 929 old files, 245 directories, parent/controller, finite grants and journal
212/31 remain exact. Only fifteen client files in six directories appear;
revision 11 remains unregistered, claims zero. Independent review repairs
retention copies to compare against frozen pins. Private manifest 5af546a0 /
archive 37fb5ba0 pass 170-member retrieval and seven-file primary-copy readback.
Historical run02 and its unknown scan cause remain unchanged. No permission
probe, Bluetooth manager, headband work, renewal, recovery, transition, migration
or merge runs. P096-005 remains partial. See node:docs/audits/REVIEW-SENSORIUM-REPORTING-CLIENT-PREPARATION-2026-10-23.md.

### Ordinary diagnostic loop after revision-11 run03 — 2026-10-23

One freshly approved campaign on source 5f2aeda0 / GUI 47a5cf76 stops at SCAN
with exact host `incomplete-released / case-discovery-authority-refused` and
confirmed controller release. No BIND/REGISTER/WEAR or provider session exists;
revision 11 remains unregistered, journal 217/32, claims/workers zero. The accepted
626 ms v3 live-validation wait now replaces a stale discovery-only 250 ms wait;
250 ms scheduling cadence and fail-closed pending-check semantics remain. A
redundant second signed-plan walk is removed without caching current authority.
The short diagnostic route uses one ordinary Case, exact pins, private reports
and fresh readiness for every pass; it neither starts nor qualifies a campaign.
Run03 originals remain immutable under private manifest 2d7f9d6f / archive
f45d06f4 with verified primary readback. P096-005 remains partial. See
node:docs/audits/REVIEW-SENSORIUM-DIAGNOSTIC-LOOP-2026-10-23.md.

### Signed ordinary diagnostic client — 2026-10-23

Clean source e36eaeb1 / pin 1e593950 now has verified standalone f34d62e6,
GUI 8536aeff and handoff 7907f90b on the nearby host. Twenty release files and
75 kit inputs match; target runtime 246 plus exporter 42 tests pass without
skips. The ordinary package de4f8cae is independently signed and distinct from
campaign/fault scope. All 959 previous root observations, 252 directories,
controller/grants and journal 217/32 stay exact; only fifteen capsule files in
six directories appear. Claims/workers stay zero; revision 11 is unregistered.
Private preparation manifest cee7e742 / archive 7b61b50f retain exact originals.
No Bluetooth manager, permission probe, hardware, migration or merge runs.
Fresh interactive readiness and this new image's permission observation precede
the one-pass diagnosis; a formal campaign remains separate. P096-005 stays
partial. See node:docs/audits/REVIEW-SENSORIUM-DIAGNOSTIC-LOOP-2026-10-23.md.

### Ordinary diagnostic entry correction — 2026-10-23

One approved ordinary diagnostic attempt on source 1e593950 / GUI 8536aeff
ends before SCAN with local relay exit 2 / SSH exit 1 and zero decisions. Exact
root readback preserves all 974 observations, journal 217/32 and zero claims.
Isolated `case_console.py --help` reproduces a missing sibling import before
main on both hosts. The corrected entry admits only its own resolved sibling
directory under unchanged isolation; client diagnostics now name a failed relay
process. Two red regressions and 114 green console/relay/adapter tests establish
software correction, without hardware retry or a campaign. P096-005 stays
partial. See node:docs/audits/REVIEW-SENSORIUM-DIAGNOSTIC-ENTRY-2026-10-23.md.

### Corrected isolated diagnostic client — 2026-10-23

Clean db62e2aa / source 89da8e9e is prepared as standalone 672140a9 and signed
GUI 2ef5a4fc / handoff c6dc78d9. Twenty release files and 75 inputs match;
290 target tests and the exact isolated frozen CLI entry pass. All 974 prior
root observations, 258 directories, grant/controller state and journal 217/32
are preserved; only fifteen new capsule files appear. Original attempt proof
c3891217 / a3eef59f is retained privately. No native retry, permission probe,
reset/recovery, renewal, migration or merge follows preparation. New readiness
and permission precede another ordinary pass; P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-DIAGNOSTIC-ENTRY-2026-10-23.md.

### Successful ordinary diagnostic pass for revision 11 — 2026-10-23

One freshly approved ordinary p21 pass on source 89da8e9e / GUI 2ef5a4fc and
ordinary package de4f8cae completes SCAN, SELECT, BIND, REGISTER and WEAR p21.
The adapter reports observed-released / success true in 71292 ms overall;
scan succeeds on attempt 1, SDK operations have no timeouts or retries, and all
thirty drain calls succeed. Cooperative cleanup, executor exit, durable audit
2/2 with release authorized, and controller release are confirmed. Journal is
226/33, claims/workers zero; revision 11 is now registered with capture/publication
off and manual restart. Controller authority is unchanged. The terminal retains
configuration-refused at running / 48 ms with effects fenced. Its exact cause and
ordering remain unestablished; two existing source-bound deterministic tests pass
without proving that history or establishing a new production defect. No campaign,
retry, recovery or qualification follows. P096-005 remains partial; a later pass
requires the stopped-registration lifecycle and fresh authorization. See node:docs/audits/REVIEW-SENSORIUM-DIAGNOSTIC-R11-RUN02-2026-10-23.md.

### Live validation-only budget (2026-10-23)

A freshly approved campaign for revision 12 on the frozen 626-ms candidate stops
at baseline: preparing validation reports 784 ms with the configuration completion
marker absent. SDK prepare/release each succeed once; config/start/drain are not
called. Cleanup, executor exit, durable audit 2/2 and controller release are
confirmed. The campaign remains partial with later rows blocked; the specific
configuration sub-read cause is unknown. Readback retains the stopped revision-12
registration and journal 235/34, with the controller unchanged and no claims,
admitted workers or unverified processes. No quarantine or recovery is inferred.

The operator-approved next source changes live validation alone to 2048 ms.
Protected receipt/fence/verified-exit remain 626/250/10000 ms; cadence, first-reason,
retries and enclosing authority/Case/session clocks are unchanged. This is not a
hard real-time guarantee, a new qualifier/schema revision or qualification.
The frozen revision-12 candidate and baseline retain 626 ms. A new pinned
target/client and fresh readiness precede any later trial. P096-005 remains partial. See node:docs/audits/REVIEW-SENSORIUM-R12-LIVE-VALIDATION-2026-10-23.md.


### Prepared 2048-ms validation client — 2026-10-23

Clean source 168fb0e0 / pin 5e788509 now has a verified nearby standalone
f3d3c8b and signed GUI e7f7aae6 / handoff 4d0b8078. The 5148-input source inventory,
twenty release files, two sidecars, eighty test inputs and eighteen loaded sections
match; target runtime 249 plus exporter 42 tests pass without skips or errors.
Validation is 2048 ms, with protected receipt/fence/exit unchanged at
626/250/10000 ms. Existing normally signed ordinary/campaign packages remain exact.
Rootless launchd preflight passes without a Bluetooth manager; permission for the
new ad-hoc image is unobserved. All 1036 old files, 273 directory identities,
parent/controller, expired authority and journal 235/34 remain exact. Only fifteen
capsule files in six directories appear; claims/workers stay zero and the stopped
registered revision 12 is preserved. Private proof 13bb61d3 / 09bc04ba and fresh
primary readback dc8c6adc retain exact artifacts. Preparation performs no renewal,
registration, Bluetooth, recovery, root migration or merge. P096-005 remains
partial. Authority renewal and the supported stopped lifecycle precede fresh
readiness and qualification. See node:docs/audits/REVIEW-SENSORIUM-VALIDATION-2048-CLIENT-2026-10-23.md.

### Four-hour authority renewal and released r12 retirement — 2026-10-23

Explicitly delegated SSH maintenance on prepared source 168fb0e0 / pin 5e788509
and administrator f3d3c8b completes renewal 9434f373, preserving the stopped r12
sibling and all twelve protected slots. Controller-owner and discovery authority
are valid to **2026-10-23 22:26:40 Europe/Warsaw** (1792787200000), TTL 14400 s.
Separate released-case v3 retirement 829c416e completes 12→13 through the normal
four-source owners and stopped-inventory application. Revision 13 is reserved,
unregistered, with no declaration, binding, p21 grant or reused WEAR consent.
Journal 235/34, 84 historical controls, consent, resource tables, all 279 directory
identities, 1042 old non-key hashes and two key-metadata observations remain exact;
only seven expected content changes and four new review/consumption files occur.
A private pinned-Python parent correctly refused before review publication;
exec replacement fixes the wrapper without a process exemption. Readback and
retention-tool corrections preserve failed originals and leave gates unchanged.
Private manifest 90062ac7 / archive 9d30b5df, fresh primary readback 80c2b6a7 and
additive count correction ff2a4403 are verified. No Bluetooth, hardware, recovery,
root-format migration or merge runs. P096-005 remains partial. Next physical work
requires current authority, exact-client permission, fresh interactive readiness
and new SCAN/BIND/REGISTER/WEAR. See node:docs/audits/REVIEW-SENSORIUM-R12-AUTHORITY-RETIREMENT-2026-10-23.md.

### Revision-13 2048-ms campaign — 2026-10-23

One freshly approved delegated-SSH campaign on 168fb0e0 / source 5e788509 and
signed GUI e7f7aae6 completes SCAN/BIND/REGISTER r13, baseline and protected stop.
Protected receipt/fence/exact-exit measure **1/1/4721 ms** under unchanged
626/250/10000-ms gates. The deadline episode ends `incomplete-released` /
`case-scope-refused` with first fence `deadline`, 22.820 ms after its original
90-s end; its inner ordinary-call cause remains unidentified. No 2048-ms
validation timeout or SDK retry occurs. All three sessions have confirmed
cleanup, exact exit, durable audit 2/2 and controller release; five later rows
remain blocked. Seven existing clock/drain regressions pass; the conservative
failure-precedence contract is retained without threshold or source changes.
Readback is journal 258/37, zero claims/workers, unchanged controller, 1043 old
non-key hashes, two key-metadata observations and 279 old directory identities.
Revision 13 remains registered and stopped. All 28 reports / 31030 bytes are
retained under private manifest 8dad4a28 / archive 4b106aa8 with fresh primary
readback 5d6b7df6. Owner snapshots retain null formal execution origin; firmware
1.0.25 stays historical and TCC responsibility unverified. P096-005 remains
partial. No retry campaign, recovery, reset, retirement, renewal, migration or
merge follows. See node:docs/audits/REVIEW-SENSORIUM-R13-CAMPAIGN-2026-10-23.md.


### Typed original-deadline source correction — 2026-10-23

Device-free review confirms a boundary race: the Case precheck may pass before
an ordinary owner read reaches the original deadline, where a generic refusal
loses the expected terminal distinction. The exact inner r13 gate remains
unknown; its immutable result and five blocked later scenarios are preserved.

The private acquisition observation now requires the exact operation, actual
shared fence, original admitted cutoff and first Case Deadline. The winning
clock observation is published before the fence. A valid read spanning that
boundary is discarded without disclosure or sequence advancement; earlier
SDK, decoding, normalization, sequence, owner and validation-budget failures
stay refusals. The first local closure precedes diagnostic publication.
A deadline result authorizes neither effects nor release: the normal stop-only
bearer, cleanup, durable audit and claim-release owners remain mandatory.

Public codes and persistent formats are unchanged, as are the 2048-ms
validation, 626/250/10000-ms protected-control gates and enclosing clocks.
Source conformance passes 235 distinct Rust tests (35 opt-in ignored), 148
client/contract/exporter tests and 22 ledger checks. Private source/log manifest
a6fbe97a / archive dd229681 has fresh independent readback 5805957d. There is no
SSH, target mutation, hardware, migration or merge. P096-005 remains partial;
no historical qualification is promoted. See
node:docs/audits/REVIEW-SENSORIUM-DEADLINE-BOUNDARY-2026-10-23.md.


### Prepared typed-deadline client — 2026-10-23

Clean source 6b9e3c94 / pin 93b575e8 (5149 inputs) is prepared as standalone
9acd625a and signed GUI f69d117c / handoff bf037f36. Twenty release files, two
sidecars, eighteen loaded sections and an 84-input frozen kit match. Target
Python 3.13.15 passes runtime 249 plus exporter 42 tests, without skips or errors.
Rootless launchd preflight creates no Bluetooth manager; permission for the new
ad-hoc identity remains unobserved. Validation/protected-control gates and all
enclosing clocks remain unchanged. Existing ordinary/campaign packages and
runtime pin pass independent checks; no worker transition is needed.

All 1082 previous byte hashes, two key-metadata observations, 283 directories,
parent/controller, finite grants, stopped r13 and journal 258/37 are preserved.
Only fifteen GUI-capsule files in six new directories appear; claims/workers stay
zero. Authority expiry remains 2026-10-23 22:26:40 Europe/Warsaw. Private final
manifest 14465d2a / archive 7f949997 and fresh readback c4dd4341 cover 193 controls
and exact retained payloads; the initial stdout-summary retention error and first
bundle remain explicitly preserved. Review finds no blocking artifact defect.
No Bluetooth, headband, renewal, retirement, recovery, root migration or merge
runs; P096-005 remains partial. Current authority, the stopped-registration
lifecycle and fresh interactive readiness/permission precede another physical
attempt. See node:docs/audits/REVIEW-SENSORIUM-DEADLINE-CLIENT-2026-10-23.md.


### Four-hour authority renewal and released r13 retirement — 2026-10-23

Explicitly delegated SSH on clean 6b9e3c94 / source 93b575e8 and administrator
9acd625a completes renewal 29ee6538, preserving the stopped r13 sibling and all
twelve protected slots. Controller-owner and discovery expiry is fixed at
**2026-10-24 01:24:55 Europe/Warsaw** (1792797895000), 14400 seconds from prepare.
Separate confirmed-release retirement a2b04bfb completes **13→14** through normal
source owners and stopped-inventory application (`runtime/applied: true`).
Revision 14 is reserved and unregistered, with no declaration, binding, p21 grant
or reused consent. The exact historical r13 partial campaign remains unchanged.

Journal 258/37, consent 23/19 lifecycle entries, resources, 89 historical controls,
289 directory identities, 1090 old non-key hashes and two key-metadata observations
are preserved; seven expected content changes and four new review/consumption
files occur. Private wrapper/inspector corrections retain original scripts and
the refused inspection without repeating effects or weakening gates. Independent
review and private manifest 482f2265 / archive 14f4fabb / fresh readback d8ef88f0
verify the closure. No Bluetooth, hardware, recovery, root migration or merge
runs. P096-005 stays partial; current authority, exact-client permission and fresh
interactive readiness precede new SCAN/BIND/REGISTER/WEAR. See node:docs/audits/REVIEW-SENSORIUM-R13-AUTHORITY-RETIREMENT-2026-10-23.md.


### Revision-14 authority-loss campaign — 2026-10-23

One freshly approved delegated-SSH campaign on source 93b575e8 / GUI f69d117c
and package c73c8aae completes **8/8 selected rows**: seven native acquisitions
plus the expired-authority refusal. All seven release with confirmed cleanup,
exact executor exit and durable audit 2/2 before claim release. The 314184-ms
run forwards 21 decisions and seven WEAR confirmations; reported SDK operations
have zero timeouts/retries. Protected stop/logout/saturation receipt/fence is
1/1 ms; exact exits are 4675–4807 ms under unchanged 626/250/10000-ms gates.
The corrected deadline succeeds at the original 90-s end, with first fence
8.791375 ms later; r13's partial refusal remains immutable. Target-only p21
expiry reduction and the following refused admission are independently verified.

Readback is journal 309/44, consent 30/26 with old fact prefixes preserved,
zero claims/workers, unchanged controller/discovery and 289 old directories.
R14 remains registered/stopped with expired acquisition authority and its original
finite binding. The baseline's fenced configuration-refused warning (116 ms) is
retained without inferring an initiating failure. All 51 reports / 65996 bytes
are private under manifest b7b90989 / archive 4e7d6ce6 and readback b3461ea9.
The branch succeeds operationally; formal report/qualification remain partial:
origins null, historical firmware, unverified TCC attribution, alternative fault/restart and
full-tuple evidence remain open. No repeat campaign, reset, recovery, authority
renewal, migration or merge follows. See node:docs/audits/REVIEW-SENSORIUM-R14-CAMPAIGN-2026-10-23.md.


### Device-free formal-evidence inventory — 2026-10-24

The initial integration preserves both histories on primary Node `6fc7b24a` and
Orbidocs `1bbae5ff`; temporary branches and trees remain for new unmerged work.
The read-only inventory checks exact r14 support bytes against retained hashes
and maps seven reports to ten P096-005 case types. It reports selected observed,
missing and failed facts, never a formal case verdict or established tuple.

Clarification: raw native origin null is intentional; the existing exporter can
corroborate a separately supplied policy origin against actual native witnesses.
The missing pieces are digest-bound owner measurements/full context, actual
post-return/reconnect/foreign-stop observations, consent demonstration and the
alternative fault/quarantine/restart branch. Historical firmware and unverified
TCC remain explicit. No old report is relabelled, no threshold changes and no
hardware, target-root mutation or further integration occurs. P096-005 remains
partial. See node:docs/audits/REVIEW-SENSORIUM-P005-OFFLINE-EVIDENCE-2026-10-24.md.

The subsequent negative-authority helper derives one existing
`expired-grant-before-effects` measurement from the actual probe clocks and
normal-begin first-refusal branch. Separate complete context is bound to exact
support, Case, target, tuple, run and harness, with unchanged Schema Gate/exporter
checks. Seven helper and twelve exporter regressions pass. This establishes
software conformance only: r14 still lacks full formal context, and positive
counter timing remains unobserved. No historical time, null SDK witness or TCC
identifier is upgraded. P096-005 stays partial.

The device-free proof retains 33 controls under manifest `e281b221`, archive
`b384d31e` and fresh primary readback `a92fb9b1`, with originals preserved and no
archived producer execution. This is evidence-processing conformance/custody,
not renewed native qualification.


### Native reader-pause queue revision — 2026-10-24

The operator authorizes at least fifteen seconds without reader calls. The common
worker's prospective default becomes 20 seconds / 256 FIFO batches / 16 MiB;
per-RPC admission/cardinality/bytes remain eight batches / sixteen original blocks
/ 49152 B payload / 65536 B envelope. Queue age, count and byte budgets are raised
together; bounded catch-up preserves every original value, clock and sequence.
The declared budget table and Node owner contract reflect this separate native
retention workload. Initial data, authority, heartbeat and protected stop clocks
remain independent; deliberate pauses do not become steady-state latency passes.

Software checks cover fifteen-second pauses with full 128-sample matrices,
exact age/count boundaries, FIFO recovery and STOP. The final real-time fake-Board
probe retains all 276 queued blocks after 15058.767 ms without reads; this is not
Muse/SDK or full native qualification. New immutable package identities include
the shared-source Synthetic family. Historical packages/reports remain exact;
a new target build and normal Author/Sign are required before production use of
the new generation. No hardware, target mutation or merge occurs. P096-005 stays
partial. See node:docs/audits/REVIEW-SENSORIUM-QUEUE-RETENTION-2026-10-24.md.


### Twenty-second target preparation and complete package closure — 2026-10-24

Clean Node c4910f8b / source 4081a4b1 now has a separately retained nearby release
f8be4782 and signed GUI c7e87d32. The ordinary, campaign and shared-source Synthetic
queue-retention generations are normally signed; merged shared-channel lifecycle
repairs additionally require a distinct `ble-discovery.channel-lifecycle` package.
Closed kinds and revision 1 remain unchanged. All 294 frozen target software
checks pass without skips, with independent source/package and fresh-retrieval
review. An exact duplicate-descriptor regression also verifies explicit final
Case-writer release while live holders and the Unclosed journal preserve fencing.
No native cleanup qualification follows from that software ownership evidence.

Existing signed/registered predecessors, consent/history and authority are
preserved. One SQLite ctime-only footprint consistent with normal permission enforcement is
recorded with all content/identity/mode checks retained. The new packages and
client are artifacts, not an installed registration transition: the current fixed
3→4 owner cannot yet advance discovery revision 4 to 5. That supported hop remains
separate, as do expired authority and unobserved Bluetooth access for the new
ad-hoc client identity. No hardware, recovery, root migration or branch merge
executes; P096-005 remains partial. The private manifest 99a10dd3, archive fd7d244c
and fresh readback fa4b123c retain preparation evidence through
`PRIMARY_EVIDENCE_STORE`, without a published physical path. See
node:docs/audits/REVIEW-SENSORIUM-QUEUE20-CLIENT-PREPARATION-2026-10-24.md.


### Supported stopped Discovery revision 4 to 5 — 2026-10-24

Node `3046d1ab` implements the software route. The Node acceptance owner now supports the exact stopped operation-retries
revision 4 to channel-lifecycle revision 5 transition through its existing normal
prepare/commit/discard protocol. Fresh channel approval/consumption/discard slots
and a distinct r5 declaration preserve all three earlier hop pairs as immutable
protected history. The current hop cannot reuse an old approval or hide an
interrupted historical publication. Normal signer/runtime/limits/expiry, the
180-second remaining-lifetime floor, sibling admission and source-CAS checks
remain unchanged; the complete stopped runtime snapshot starts no worker.

All 163 ordinary owner tests and two explicit normal-key conformance tests pass,
including five crash phases, retained-history byte binding and sibling/expiry
preservation. The fresh temporary roots are device-free; the constructed history
binds receipts without claiming earlier package execution. This is an
implementation checkpoint, not execution of the transition on the operator's root. It does not create or extend authority, consent or qualification,
and does not release controller or resource claims. A new pinned client and
separate exact current-authority approval remain necessary before actual use.
P096-005 remains partial. No headband, Bluetooth, recovery, target-root transition
or branch integration occurs. See
node:docs/audits/REVIEW-SENSORIUM-DISCOVERY-R4-R5-2026-10-24.md.


### Pinned client for the stopped Discovery 4 to 5 route — 2026-10-24

Node `8499f824` records this preparation and review. Clean Node 3046d1ab / source b9bc971e now has a separately prepared nearby release
219d532f, signed GUI be1d1560 and handoff daa80e7c containing the supported stopped
4-to-5 owner. All 294 frozen target software tests pass without skips. Independent
Git/source review and fresh signed-GUI retrieval verify the frozen artifacts;
all four existing ordinary packages match the compiled closures without re-signing.
All 1236 prior file observations and 308 directory identities remain exact, with
only fifteen new client files/six directories. Private key content is not read.

Discovery remains at operation-retries revision4; no grant renewal, transition,
controller release, recovery, Bluetooth permission or hardware qualification is
inferred. The new ad-hoc client has unobserved TCC access. P096-005 stays partial;
no native operation or branch integration occurs. The initial count-checker
refusal, corrected preservation check and preparation evidence are retained via
`PRIMARY_EVIDENCE_STORE` under the private run locator. See
node:docs/audits/REVIEW-SENSORIUM-DISCOVERY-R5-CLIENT-PREPARATION-2026-10-24.md.


### Renewed authority and completed stopped Discovery 4 to 5 — 2026-10-24

Node `c8d20ba8` records the verified operation and owner-ordering correction. The explicit delegated renewal 2ec54f0d completed with the unchanged four-hour
ceiling, through 2026-10-24 22:27:53 Europe/Warsaw. The operator separately approved
expired p21 revision14 retirement f6a0d8c8, reserving revision15 without new grant
or consent. The new pinned daemon then completed Discovery 4-to-5 c823439b on
signed channel-lifecycle package revision1, applying a stopped snapshot with
unchanged expiry and no native worker. Independent readback verifies the exact
rebind, eleven protected sources, retained journal309 / 44 Cases and zero claims.

The observed process guard, expired-sibling refusal and partial retirement apply
remain evidence. External helper maintenance had its own interactive approval.
The new administrator refuses the remaining old Discovery compiled closure;
source-verified retained administrator 6b9e3c94 resumes only the same approved
retirement, and the new administrator subsequently commits its r5 transition.
No marker edit, source-check bypass or grant relaxation is used. Old reports,
consent and package history are preserved. This is metadata/operational evidence:
P096-005 stays partial, with fresh permission/readiness and SCAN/BIND/REGISTER/WEAR
still required for native revision15. No hardware, reset, recovery or branch
integration occurs. See
node:docs/audits/REVIEW-SENSORIUM-DISCOVERY-R5-AUTHORITY-TRANSITION-2026-10-24.md.


### Revision-15 authority-loss branch on queue-retention-20s — 2026-10-24

Node checkpoint `3313c0f7` records the measured result and reviewed closeout.
A freshly approved SSH campaign on Node source 3046d1ab / pin b9bc971e, signed GUI
be1d1560 and package 7b815bbb completes eight selected operational rows and seven
released native acquisitions in 312702 ms. Protected receipt/fence measures 1/1 ms;
maximum exact owned exit is 4822 ms. Durable audit 2/2 precedes every claim release.
The original 90-second deadline and 2048/626/250/10000-ms control gates remain;
2988 SDK drains report no timeouts or retries. This uses the current signed
twenty-second queue closure without qualifying an injected native-reader pause.

Final journal 360 / 51 Cases and zero claims/processes are independently read back;
Discovery r5, finite owner/discovery authority, custody and previous consent
prefixes are preserved. R15 remains registered/stopped with only its acquisition
expiry reduced. All 51 reports / 65995 bytes and the 149-control private proof
(manifest 208158de, archive 84a18a44) pass fresh primary-store retrieval. Review uses
separate same-assistant algorithms, not a second reviewer. Local mode 0644 input
refusal is corrected to 0600 before the sole child launch; no hardware retry occurs.

The raw-support inventory confirms partial support for seven of ten safety types,
with hung-worker, retained-claim and actual-restart types still missing. Historical
firmware 1.0.25, unverified TCC attribution, missing full formal context and remaining
case-specific owner facts prevent qualification. P096-005/P096-011a and release
readiness stay partial; no reset, recovery, renewal, migration or branch integration
occurs. Earlier evidence is unchanged. See
node:docs/audits/REVIEW-SENSORIUM-R15-CAMPAIGN-2026-10-24.md.


### Device-free preparation of the remaining safety branch — 2026-10-24

Node `2723ef32` records this source/conformance checkpoint.
Prospective v2 retained-claim and restart observations now record their own
wall/monotonic probe interval, exact held-state reads and ordinary inert refusal.
Restart measurement belongs to the new boot and cannot be inferred from Bluetooth
reset. Historical v1 remains strictly readable without new default facts; this
changes private observation output, not root/checkpoint persistence or authority.
A read-only deriver and existing exporter bind the same actual counts, full
context and both wall endpoints under unchanged qualification schemas and budgets.

The remaining-emergency plan selects only baseline and one controlled native
fault, with retained-claim and separately observed actual restart as derived rows.
Plan construction performs no operation and grants no stage decision. Software
checks pass 102 Python tests, four restart-owner and two fault-owner Rust tests,
plus two compiled-C/fake-Board cases. This is preparation/conformance only: no
nearby root, grant, controller or hardware is touched; no reset, recovery, native
qualification or integration occurs. R15 and earlier evidence stay exact. A new
pinned client, supported stopped lifecycle and fresh physical approval remain
necessary. Full P096-005 remains partial, including missing context and remaining
control/consent witnesses. See
node:docs/audits/REVIEW-SENSORIUM-EMERGENCY-EVIDENCE-2026-10-24.md.


### Physical readiness checkpoint — 2026-10-24

The next physical trial is blocked until device-free end-to-end tests prove that
the runner actually collects every required field. Schema acceptance or fixtures
with manually supplied facts do not establish collector completeness. The target
is one ordinary flow and one emergency flow, followed by a separately approved
actual host restart. Fresh interactive headband readiness remains required.

This software slice is not that readiness decision. The timed quarantine/restart
probes close two measurement-production gaps. Full context and remaining positive
authority/control/consent owner witnesses, including post-return emissions,
post-fence reconnects, foreign-launch terminations and shown/demonstrated consent
controls, remain explicitly unresolved. Missing fields block progression; do not
fill them with defaults or repeat hardware runs to discover collector omissions.


### Actual collector owner boundaries — 2026-10-24

The implementation now measures private consumer receipt after normal sample
return, including deadline drains. Its finite receipt history is compared with
the actual fence only after the synchronous sequence and cleanup attempt. Worker
v2 retains every prepare entry and seals the same gate at STOP without waiting
for native completion. Exact exit and complete non-exhausted coverage are
required; a before-return zero or a first entry alone is insufficient.

The supervisor checks the privately retained admitted child against the actual
selected target before disposal. Mismatch refuses before signaling; public
observations retain only opaque launch/generation and check/refusal counts.
This is an owned-process boundary, not a process inventory or radio observation.
A separate write-once authenticated-activation/final-admission interval supports
the bounded positive-authority case; later session counters cannot replace it.
The exporter binds its clocks to SDK preparation without raising any threshold.

Review corrected delayed RPC/seal reconciliation, exhausted entry accounting and
readiness backdating across a slow sample RPC and the gap before publication
of the shared-fence clock. Focused device-free checks pass
172 Python, 107 acquisition-owner, three consumer and 42 supervisor cases, with
eight explicit runtime fixtures ignored. Schema-shaped fixtures establish
reconciliation only. Old reports remain exact and gain no missing defaults.

P096-005 and physical collector readiness remain partial. Actual shown indicator
and protected-stop demonstration, wrong-mode probes, full owner/operator context
and automatic end-to-end collection remain blocking. The next physical target
is still one ordinary flow and one emergency flow, then a separately approved
actual host restart. No SSH, headband, Bluetooth, target mutation or merge occurs.
See node:docs/audits/REVIEW-SENSORIUM-COLLECTOR-BOUNDARIES-2026-10-24.md.

Node checkpoint `d2a43a96` records these implementation and review changes. Its
private manifest is `867538d38b5042cba929e64dda603e3fcf5b3df6128fcd1d8cc7474ae465c1f0`;
all 29 retained members pass extraction/digest verification. This does not
establish complete collector readiness or new physical acceptance.


### Real pre-consent collection checkpoint — 2026-10-24

The private Case now obtains visible preview and preview-stop acknowledgement
clocks from the actual protected wearer view before WEAR, two wrong-mode
refusals through ordinary inert begin, and one logical confirmation observed by
the durable consent writer. The preview explicitly makes no native-stop claim;
protected disposal remains independently qualified. The browser obtains only
view/withdraw authority through a fixed-expiry one-use handoff. No activation
bearer enters a URL; consumed/expired handoffs cannot be renewed by replay.

Read-only status polling does not create visibility. The active view has a
separate visibility-loss fence and neither extends nor renews any authority.
The parser/exporter/inventory bind new facts to the same operation and retain
legacy missing values. Consent-before-native-entry, origin and all qualification
budgets remain unchanged. Device-free tests exercise the real client, served
JavaScript, browser and protected owner; no SDK or nearby device participates.
Verification passes 393 Python, 112 acquisition-owner, 27 private-owner cases
and the explicitly executed real-browser/client/HTTP case, with opt-in exclusions
recorded separately. The actual owner projection passes its closed client parser;
absent SDK/consent observations remain absent.

P096-005 and full collector readiness remain partial: complete owner/operator
context, automatic measurement assembly and whole-run device-free collection
are still blocking. The later physical target stays one ordinary flow and one
emergency flow followed by a separately approved actual host restart. There is
no SSH, Bluetooth, hardware, target migration, recovery or branch integration.
See node:docs/audits/REVIEW-SENSORIUM-PRECONSENT-COLLECTOR-2026-10-24.md.


The private 39-member software checkpoint passes bounded extraction and digest
verification (manifest `a7a056932d91ea65870f2c88b367df6dbd792f795fea3b403d72bdb592f75d51`,
archive `aeaebfd98f0498409f291baabb2131223a81260a5501898d61609dedf7e8eee6`).
Its control explicitly states that full collector completeness is false. Earlier
retained evidence remains exact; no native qualification is inferred.

Node checkpoint `8c2d5de1` carries this implementation and review; full-run
collector readiness and P096-005 remain open.


### Prospective actual-owner qualification context — 2026-10-24

The private enrolled Case captures owner-only tuple fields before SDK effects:
current registered plan/configuration/integrity, exact instance/binding/generation,
profile/mode, the pinned runtime's binding/native manifests and verified host
build/launch identity. The full admitted integrity still covers auxiliary fault
assets. Raw context is bound to its actual operation and Target; the client and
exporter reject grafting available witnesses to a foreign context or tuple.

Firmware and TCC are separate explicit operator observations. Composition keeps
their original status/source/time, rejects historical/unverified/future/stale or
rebound facts, and invents no defaults or approval. The complete independent
qualifier remains required with unchanged issuance/freshness, origin and timing
gates. Baseline comparison over 1450 fixture mutations finds no full-tuple
semantic acceptance drift; this is reconciliation evidence, not native proof.

Actual execution of the wired owner path, automatic all-case assembly and
whole-run device-free field completeness remain blocking before another physical
trial. P096-005 stays partial; no SSH, device, target mutation, recovery or merge
occurs. See node:docs/audits/REVIEW-SENSORIUM-OWNER-CONTEXT-2026-10-24.md.


Focused verification passes 396 Python, 27 private-owner and three runtime tests,
with explicit runtime exclusions. A verified 24-member private software archive
(manifest `bb36eec7c9c97390447fec65b75f10b3d9cca4ccdffe49636dc7f6c42096a833`,
archive `8fd1d98259d502150fea5aadb27f33e7a6034b57014055012a396113e0152fd5`)
explicitly records that the complete owner-context path has not yet executed.
This checkpoint does not establish full collector readiness or qualification.

Node checkpoint `118dc0f5` records this production wiring and focused review.
It does not close the actual-owner/whole-run execution requirement.


### Automatic safety capture checkpoint — 2026-10-24

The actual finite runner now retains boundary-derived captures after immutable
raw episodes, plus separate restart support/capture in the new boot's own clock
interval. Missing observations remain explicit. Owner-derived acquiring-state
reads, provider transition, listener metrics and measured absence of progress
in the controlled drain-thread C fault close producer gaps. Explicit firmware/
TCC observations bind the actual owner context; automatic conversion still runs
the complete episode, existing exporter, Schema Gate and unchanged semantics.
An unarmed injector does not establish zero SDK hangs without confirmed native
cleanup and a sealed complete call ledger with every entry returned.

Device-free verification covers all ten shapes, finite-runner capture retention,
read-only isolated CLI and real inert Init/Author/Sign/Register source collection.
These are component/composition checks, not whole-run collector completeness.
The actual owner/runner/worker/consumer composition across both terminal branches
and the restart observer must still prove every field without manually supplied
facts before another physical trial. P096-005 remains partial. No SSH, headband,
Bluetooth, target migration, recovery, restart or merge occurs. See
node:docs/audits/REVIEW-SENSORIUM-AUTOMATIC-COLLECTOR-2026-10-24.md.

Verification passes 405 Python, 112 acquisition-owner and 28 private-owner tests,
with explicit opt-in exclusions; real inert registration is executed separately.
The private 34-member software archive passes bounded extraction and every member
hash check (manifest `d9fe15d5baa285aa8be5d8a2a34a8caa7fb96dd373eb7fa9eceaa57eb4451cbf`,
archive `3b75edbe6b04b842ce5bbf5c6cb73bb8dd95452b0d1a8a149258b7bd99030a45`).
Its control explicitly leaves whole-run collector completeness false. Node
checkpoint `fe5d50d8` contains this implementation and review; neither full
P096-005 nor the physical-readiness checkpoint is closed.


### Actual-owner software composition — 2026-10-25

Node adds a test-only peripheral boundary around the same operational private
runner and NormalOwners. Real registration, admission, MAC verification, consent,
served browser code and consumer operate with a software SDK Board. Every block
and execution is marked synthetic; the physical exporter still refuses it. The
software child cannot establish canonical native process containment. No new
production effect API or qualification exception is introduced.

The actual baseline composition passes separately in 25.18 s and automatically
captures both baseline case types from its unchanged owner output, without
hand-filled counters or clocks. A size-optimized test image fits the unchanged
hashing bound. Whole-run completeness remains open: the remaining control and
authority cases, both terminal branches and the read-only restart observer must
produce every required field before another headband readiness question. P096-005 remains partial; no nearby device, recovery, migration
or merge is performed. See
node:docs/audits/REVIEW-SENSORIUM-SOFTWARE-COMPOSITION-2026-10-25.md.


### Actual control-owner captures — 2026-10-25

Four device-free actual owner/runner/worker-engine/browser/consumer runs pass in
84.77 s. Their automatic captures provide five more complete case types: logout,
saturation, provider loss, live grant loss and expired enrollment refusal. With
baseline, seven of ten safety measurement types have actual software composition
coverage. No clock, counter or result label is manually populated.

Each case uses its own fresh private root and remains explicitly synthetic. This
union cannot become a physical qualification tuple. Controlled hang, retained
claim, read-only restart composition and exact authority/tuple workflow remain
blocking; P096-005 stays partial and no headband readiness is declared. No device,
nearby mutation, reset, recovery or merge occurs. See
node:docs/audits/REVIEW-SENSORIUM-CONTROL-COMPOSITION-2026-10-25.md.

### Actual emergency-owner and full capture coverage — 2026-10-25

Three actual owner/runner/worker-engine/browser/consumer software compositions
pass in 150.02 s. Six private conformance roots automatically produce all ten
P096-005 measurement types, including the controlled C hang, retained claim and
actual read-only restart-observer logic. Full schema and semantic export accepts
every synthetic record with no missing fields. The next kernel boot identity is
explicitly simulated; this is not a real restart or canonical native containment.
Firmware/TCC inputs are explicit software test metadata.

New Init establishes private 0700 control custody before normal owners create
files, matching the strict read-only restart reader. Existing roots are not
changed. A control-case interval runs from validated required presets to the
exact launch exit. The complete subsequently closed consumer window separately
corroborates post-fence delivery; later cleanup/audit does not inflate control
latency. Late blocks still refuse; receipt/fence/exit and all other budgets are
unchanged. Historical observations and capsules are not rewritten.

413 Python tests run (410 passed, three skipped); 11 controller, four restart,
28 owner and 112 acquisition regressions pass, as does the ordinary library
outside cfg(test). The 81-member private proof was extracted/readback verified;
manifest SHA-256 is
`309a20cea19893ab44eae244ff698a8053d49736624d3e0892af7819e92faf10`.

P096-005 stays partial. Independent root tuples cannot be combined into physical
qualification. The supported same-tuple authority transition between ordinary
grant loss and the emergency flow still needs implementation and device-free
verification. Changed or expired HostGrant/Target must refuse reuse. No grant is
restored here. Only after that full workflow passes may fresh headband readiness
be requested; an actual host restart remains a separately approved operation.
No nearby-host operation, Bluetooth, device open, recovery, root migration or
merge occurred.

### Data-only fresh runtime-authority projection — 2026-10-25

The ordinary terminal branch loses its acquisition authority. Subsequent
emergency testing requires a separately approved fresh grant and fresh WEAR;
old consent or a scenario label cannot supply either. A new private data-only
projection reproduces the exact reduction, preserves scope/siblings and bounds
one proposed expiry by the unchanged live HostGrant and five minutes from
fresh approval. The original runtime expiry bounds only its historical reduction. Seven projection and five reduction tests pass; no writer or route is
present and no grant is created.

The full qualification tuple and operational Target are distinct. Dynamic
HostGrant is not a full-tuple field, but changing it changes Target and must
continue to refuse ordinary old-basis reuse. The first proposed corridor
preserves the original still-current HostGrant. Insufficient/expired authority
refuses; it is not implicitly refreshed or replaced. No requirement is weakened.

Actual exclusive root/controller/history/resource owners, digest-bound separate
approval, publication and partial-write fencing/reconciliation still need
integration. One-root ordinary/emergency software execution must then prove
unchanged full tuples, fresh consent and complete actual captures before any
physical question. Data fixtures are not owner observations or qualification.
No nearby host, Bluetooth, grant publication, recovery, migration or merge was
performed; P096-005 stays partial.

### Current registration owner for runtime-authority review — 2026-10-25

The Node projection now obtains current Target/typed HostGrant, operator and
kernel boot through the normal registered-source owners. Existing signature,
plan/integrity, binding, profile and sandbox checks remain shared; no launch
context, executor or Bluetooth probe is needed for this metadata observation.
The result is neither native admission nor consent or controller-idle evidence.

Publication still needs released history, sole controller custody and separate
digest-bound approval; fresh WEAR and exact old-session fences remain required.
The common-root ordinary/emergency run remains open before physical readiness.
See node:docs/audits/REVIEW-SENSORIUM-RUNTIME-REGISTRATION-OWNER-2026-10-25.md.
No target operation, device, recovery, migration or merge occurs. P096-005 stays
partial. The earlier data-only note's stale original-native-expiry ceiling is
corrected to match the already reviewed implementation; it is not a new grant.

### Affine Case owner for separate fresh runtime authority — 2026-10-25

Node now implements an internal grant stage after checked registration reuse and
before enrollment for the emergency branch following live revocation. It needs
a released same-basis/Target/boot Case, exact original reduction history and
current normal registration/controller observations. Separate GRANT-P21 approval
names a concrete review digest. A durable one-use consumption entry precedes one
atomic policy replacement; frozen parent/five-minute limits are unchanged.

This settles a narrower mechanism than the earlier exploratory general pending
administrative corridor: existing affine Case ownership protects one authority
file, and failures leave a complete approved before or after value. Consumption
is never retried or deleted to restore authority. Existing unresolved-Case and
claim fences remain after a process crash; no cleanup/recovery proof is invented.
New eligibility does not revive the old run or substitute for a fresh WEAR.

Ordinary entry selection is still None; no argv route or client autoapproval is
provided. Actual common-root ordinary/emergency factory/client composition,
complete collector output and old-token/permit denial remain blocking before a
physical question. See Node audit REVIEW-SENSORIUM-RUNTIME-AUTHORITY-CASE-OWNER-2026-10-25.
P096-005 stays partial; no hardware, target operation, reset, recovery, migration
or merge occurs.

### Common-root safety collector completeness — 2026-10-25

The same Node normal owners and finite runner now execute the ordinary and
emergency branches on one private software root: six fresh Cases, a separate
exact-review grant decision after live revocation, new WEAR for every SDK session,
and all ten complete safety records under one exact full qualification tuple.
No HostGrant, Target, binding/generation or old-session fence is replaced.
The corrected whole-run test passes in 84.68 s with unchanged Schema Gate and
semantic thresholds; physical-origin promotion still refuses.

The first trial's helper artifact omitted the full tuple while retaining its
digest, so its aggregate failed. A fresh run retains the exact tuple and explicit
owner-bound external software fixture, independently reassembles them from each
actual context and checks every record digest before using the existing grouper.
The failed trial is immutable and missing values are never backfilled.

The software completeness gate is green; P096-005 remains partial. SDK and
advertisements, kernel restart and grant/firmware/TCC approvals remain explicit
fixtures. Supported signed-client approval/target preparation still precede any
physical question, followed by real SDK/OS/TCC/native containment and separately
approved host restart proof. No target operation, device, reset, recovery,
migration or merge occurs. See Node audit
REVIEW-SENSORIUM-COMMON-ROOT-COMPLETENESS-2026-10-25.

### Separate runtime-grant client approval — 2026-10-25

The real Node console/SSH entry now accepts only an explicitly selected reused
hung-worker episode with an exact earlier reduction Case. Arguments choose
history; a distinct GRANT-P21 prompt binds the complete validated review digest
before enrollment, and fresh WEAR remains independent. The client checks the
frozen parent/five-minute ceiling, flags, clocks and references. Unknown,
broader, expired or foreign reviews refuse even after rehashing. Formal campaigns
do not automatically renew authority or change their budgets.

The actual owner receipt now returns in closed optional observations and is
bound to the approved review/expiry/target. Partial write failure remains
partial. The same normal client validator/prompt/reply participates in the
six-episode common-root software proof: ten complete records under one exact
full tuple in 116.43 s, unchanged Schema Gate and semantic limits, and physical
origin promotion refused. Eight entry, thirteen grant, 56 Case and 424 Python
checks with three opt-in skips pass; the source pin and private proof readback
are verified. Peripheral effects, approval and external facts remain explicit
fixtures, not physical qualification.

Target build and signed control capsule preparation precede a fresh headband
question. SDK/OS/TCC/native containment/current operator observations and
separately approved actual host restart remain required. No target operation,
device, reset, recovery, migration or merge occurs. P096-005 remains partial.
See Node audit REVIEW-SENSORIUM-RUNTIME-GRANT-CLIENT-2026-10-25.


### Pinned runtime-grant target preparation — 2026-10-25

Node `97d4dddf` now has a pinned release and signed nearby-host client. Its
424 frozen Python tests pass with three explicit opt-in skips, as do rootless
signed-client check/launchd observations. Independent Git-object, signature,
fresh retrieval and external runtime-hash checks pass without SDK imports or a
Bluetooth manager. All previous root/controller sources and identities remain
unchanged; only the exact new client capsule is added. The prospective physical
gate is not open: Discovery matches, while the three installed BrainFlow
packages retain their earlier worker and require new immutable package generations
for current boundary observations. Authority remains expired. No renewal, Case,
root migration, transition, hardware, reset, recovery or merge occurs.

The Node ledger's earlier P096 checkpoints are restored to the Sensorium owner
from an incorrectly selected P094 row; historical evidence remains immutable.
See node:docs/audits/REVIEW-SENSORIUM-RUNTIME-GRANT-TARGET-PREPARATION-2026-10-25.md.
P096-005 stays partial. Actual SDK/OS/TCC and native containment plus a separately
approved actual host restart remain required after software/package readiness.


### Immutable safety-boundary package generation — 2026-10-25

Current normal authoring now gives the three updated BrainFlow closures new
`safety-boundaries` package ids (including a separate campaign package). It
preserves earlier queue-retention packages/reviews/signatures, closed kind
spellings, manifest revision 1, exact replay, runtime and every consent/native
and qualification gate. Discovery remains on its matching channel-lifecycle
identity. Author/sign creates no grant, registration, permit or WEAR.

Two pure generation and three explicitly executed real inert normal-owner cases
pass. The actual common-root software runner/client still produces ten safety
records under one exact full tuple over six Cases, with no missing fields, in
106.44 s. Production checking passes; physical-origin promotion refuses and the
SDK/controller/approval/restart fixtures remain explicitly synthetic. The failed
launcher/output-directory attempt is retained and no threshold is changed.
See node:docs/audits/REVIEW-SENSORIUM-SAFETY-BOUNDARY-PACKAGES-2026-10-25.md.
Target release, normal signing/admission and current finite authority remain
required before a fresh interactive hardware decision. P096-005 remains partial;
no existing target root, device, recovery, migration or merge changes here.


### Normally signed safety-boundary packages on the target — 2026-10-25

The pinned `b61a35c1` release, fresh signed client and three new normal-author/sign
packages are prepared and verified on the nearby host. Discovery and all new
BrainFlow closures exactly match the candidate; existing packages and approvals
remain unchanged. Frozen target Python tests pass 424/three explicit opt-in
skips; actual rootless signed launchd preflight and independent source, signature,
image and primary-store retrieval checks pass without a manager or SDK acquisition.

Sixty-one exact new files/twelve directories are the only additions. All 1355 non-key content hashes, two signing-key metadata-only observations
and control/configuration/claim/history state are preserved. Signing-key content
is not independently inspected or byte-qualified.
A measured SQLite ctime-only change follows normal unconditional permission
restriction; its exact frozen path/field/timestamps are separately disclosed,
all other metadata is exact, and no P096 measurement gate is weakened.
See node:docs/audits/REVIEW-SENSORIUM-SAFETY-BOUNDARY-TARGET-PREPARATION-2026-10-25.md.
Authority remains expired and registrations unchanged. Current finite admission
precedes fresh headband readiness; actual SDK/OS/TCC/containment and a separately
approved actual restart remain open. P096-005 stays partial; no hardware, reset,
recovery, authority renewal, root migration or merge is performed.

The final Node gate also found canonical formatting of one shortened static
package literal; its private launcher now checks every gate exit. This correction
changes the source pin while leaving package bytes/values and all measurement
gates identical. A fresh pinned client must precede physical use; the measured
b61a35c1 artifact and both gate refusals remain unchanged.


### Canonical-source replacement client verified — 2026-10-25

The clean formatting-corrected `9458b4b1` source is actually rebuilt and signed
on the target, with independently verified full pin `920c0ec4`. All four existing
package closures remain exact; no Author/Sign action occurs. Frozen target Python
tests pass 424 with three explicit opt-in skips, along with rootless signed launchd
preflight, all 5407 Git blobs, strict signatures and independent image/primary-store
readback. The original generation/common-root proofs remain bound to their actual
b61a35c1 source; only the same static-literal block's canonical form changed.

All 1416 non-key hashes, two key metadata-only observations and every prior file
metadata/directory identity are exact without exception. Only sixteen capsule
files/six directories are added; policies, grants, registration, consent, journal,
claims and historical artifacts remain unchanged. Authority is expired; current
finite admission and the stopped p21 lifecycle precede interactive headband
readiness. Actual SDK/OS/TCC/containment and separate real host-restart approval
remain open. See node:docs/audits/REVIEW-SENSORIUM-CANONICAL-SAFETY-CLIENT-2026-10-25.md.
P096-005 remains partial; no hardware, reset, recovery, renewal, migration or merge.

### Finite authority and stopped p21 lifecycle reconciled — 2026-10-25

The canonical pinned client completed same-scope delegated controller/discovery
renewal for four hours through review `5ed0aac2` and supported retirement of
released/expired p21 r15 through review `c57d1027`. Discovery stays r5; r16 is
reserved without a grant or reused consent. Exact review/marker readback confirms
four targeted source removals, unchanged Case journal and consent, and no claims
or pending recovery. Standing delegation is recorded explicitly; no new human
confirmation is manufactured. Expected owner writes and ctime-only metadata
changes are disclosed in node:docs/audits/REVIEW-SENSORIUM-SAFETY-AUTHORITY-R16-2026-10-25.md.
A private 68-member proof was read back through `PRIMARY_EVIDENCE_STORE`.

This is metadata readiness only. P096-005 remains partial: actual native SDK,
OS/TCC, fresh firmware facts, emergency containment and separately approved real
host restart remain required. Fresh interactive headband approval precedes device
work. No hardware, reset, recovery, migration or merge occurred.

### R16 preview boundary and UI correction — 2026-10-25

The fresh target pass completed discovery, binding and registration but stopped
before WEAR during incomplete protected-view demonstration. The Case is released,
with zero resource/controller claims and no pending recovery; the emergency pass
was not attempted. A stale active preview after failed control requests was
confirmed and corrected. Two browser actions are now explicit, unavailable state
disables preview controls without inventing cleanup, and independent Stop remains
available. The existing 30-second demonstration/parent clocks remain unchanged.

An actual protected-owner/real-browser loss-restoration test and real HTTP refusal
checks pass, along with 424 isolated client tests (three opt-in skips). These are
software UI checks; no SDK entry or durable consent is created. The private proof
passed 77-member primary readback. See
node:docs/audits/REVIEW-SENSORIUM-WEARER-VIEW-R16-2026-10-25.md.
P096-005 stays partial. A new pinned signed artifact and supported stopped-r16
lifecycle precede fresh headband approval; actual host restart still needs its
own later approval. No retry, reset, recovery or merge occurred.

### Repaired wearer-view artifact prepared — 2026-10-25

The corrected client is actually built and signed from clean `aab178ea`, with
independent full-source pin `16cb5ff0`. Source blobs, four existing exact signed
package closures, 263 frozen inputs, 424 target tests (three opt-in skips),
rootless launchd preflight and fresh image/primary readback pass. All 1468 old file
observations/metadata (1466 non-key hashes plus two metadata-only key records) and
349 directory identities remain exact without exception; only the new sixteen-file
capsule/six directories are added. No package or active configuration changes.

Stopped r16 is preserved; supported retirement must wait for its still-live binding
rather than shorten expiry. P096-005 remains partial. Fresh readiness must include
both pre-WEAR browser clicks, new-image Bluetooth observation and separate later
approval of actual emergency host restart. See
node:docs/audits/REVIEW-SENSORIUM-WEARER-VIEW-CLIENT-2026-10-25.md.
No permission manager, hardware, authority/registration transition, reset, recovery,
migration or merge occurred in this preparation.


### Released r16 lifecycle completed — 2026-10-25

The corrected pinned client completed supported expired/released retirement
`12bfa83d` r16→r17. Discovery remains r5; no r17 declaration, grant or wearer
consent exists. Exact source/marker readback and closed write-set review preserve
Case journal 368/52 Cases, consent and controller files. Claims and pending recovery
are absent. Normal database writes and the exact read-store ctime-only change are
scoped in node:docs/audits/REVIEW-SENSORIUM-R16-RETIREMENT-2026-10-25.md.
The 29-member private proof passed fresh primary-store readback. Pure r17 driver
frames/refusals pass without SSH; no new readiness or permission fact is created.

P096-005 remains partial. Fresh interactive headband readiness must explain both
pre-WEAR browser clicks. Native ordinary/emergency measurements, current-image
OS/TCC facts and separately approved actual host restart remain required. The
already fresh firmware observation keeps its original time. No device, permission
probe, reset, recovery, migration or merge occurred in this lifecycle step.


### R17 physical observations and frozen gate refusals — 2026-10-25

One freshly approved ordinary pass completes five native sessions with confirmed
release and no SDK retry. The separately approved emergency preserves the parent
grant ceiling, then closes 68 ms after its expiry before START permit or fault.
It is released, without quarantine or a restart checkpoint; no retry/reset/recovery
or host restart occurs. Actual firmware and TCC observations bind one full tuple.

Five of ten P096-005 records pass the unchanged schema/semantic gates: four control
records (receipt/fence 1/1 ms; exit 4,671–4,771 ms) and the expired-authority refusal.
The raw authority/consent records are complete but exceed their frozen 10-second
budgets at 13,133/10,534 ms; three emergency/restart records remain missing. Full
safety export correctly refuses. No measurement interval or original verdict is
revised. Source review must reconcile the timing domains without weakening the
owning requirements or thresholds and avoid unnecessary emergency dispatch waits.

Journal 412/58 Cases, zero resource/controller claims, no pending recovery and
unchanged controller files are verified. R17 binding retains its actual expiry;
future supported retirement/readiness remain separate. Private report retention
uses an explicit 81-member allowlist with fresh primary readback, excluding SSH
configuration, approval inputs, launchers and full root/configuration snapshots.
See node:docs/audits/REVIEW-SENSORIUM-R17-PHYSICAL-2026-10-25.md.
P096-005 stays partial; no qualification, migration or merge is claimed.


### Finite emergency dispatch preparation — 2026-10-25

A private local operator adapter prepares immediate transition after five
released ordinary sessions and four exact emergency responses: REUSE, GRANT-P21,
WEAR p21 and FAULT. Thirteen device-free tests pass, including real local pipes
and preservation of the actual r17 refusal through its frozen parser. Existing
signed-client review/nonce checks, both browser actions, normal authority and
separate host-restart approval remain. No budget, grant or original result changes.

This is harness preparation; future per-run artifact/fresh-delegation binding
remains before native use. Proposed 15-second budgets for the two refused cases
and seven-minute fresh p21 grants await explicit adoption. P096-005 and the r17
five-of-ten result stay partial. The six-member private proof passes fresh primary
readback; see node:docs/audits/REVIEW-SENSORIUM-EMERGENCY-DISPATCH-2026-10-25.md.
No SSH, device, root change, recovery or merge occurred.


### R17 retirement and adopted prospective limits — 2026-10-25

Supported released/expired retirement `ceb46889` completes r17→r18 without recovery.
Six Cases are released; exact source/marker/predecessor checks preserve journal
412/58 Cases, consent, controller and idle resources. Discovery remains r5; r18 is
reserved without declaration, grant or consent. Closed normal write-set review
and explicit eight-member private report readback pass. See
node:docs/audits/REVIEW-SENSORIUM-R17-RETIREMENT-2026-10-25.md.

The operator explicitly adopted 15 seconds only for current-authority-before-effects
and mode-scoped-wearer-consent, and seven minutes for fresh p21 registration and
matching new runtime-grant ceilings. This is prospective: existing grants and
r17 verdicts stay unchanged, as do protected receipt/fence/exit limits 626/250/10000 ms
and the 90-second session limit. Source changes, coherent Rust/Python boundary tests
and a fresh pinned signed target client remain the next implementation slice.
No device, reset, recovery, migration, merge or new qualification occurs here.
P096-005 remains partial; physical and real-restart approvals remain separate.


### Prospective qualification policy v4 — 2026-10-25

For future collections only, current-authority-before-effects and
mode-scoped-wearer-consent have 15,000-ms maxima. Preserve their original measured
intervals, all required facts and every record's declared budget; a historical
10,000-ms overrun remains refused. Other case caps and protected receipt/fence/
verified-exit limits 626/250/10000 ms remain unchanged. Qualifier identities
advance to v4, with exact current-source admission and readable historical schema
identities. This is an explicitly adopted criteria change, not new native proof.

Fresh post-BIND p21 HostGrants last seven minutes. A separately approved fresh
runtime grant is bounded by the unchanged current parent and 420,000 ms from
preparation; old grants keep their original expiries and wearer consent is never
reused. Discovery's default and same-scope renewal policy are unchanged. Sessions
still last at most 90 seconds (preparation 60 s, cleanup 20 s); validation stays
2048 ms. No worker package source change, native retry, recovery or root migration
follows from this policy. See
node:docs/audits/REVIEW-SENSORIUM-PROSPECTIVE-POLICY-V4-2026-10-25.md.
Rust/Python boundary and actual-owner software completeness tests precede a fresh
pinned signed client. R18 remains reserved; r17's five-of-ten result is frozen.
P096-005 remains partial; fresh hardware and separate actual-restart approvals
remain required. No merge is performed.


### Prepared policy-v4 target client — 2026-10-25

A clean offline release and signed nearby client from Node `8c66f7ad` carry the
prospective two 15-second proof windows and seven-minute new p21 grant ceilings.
Independent review matches 5407 Git blobs, 263 frozen inputs, signatures and loaded
sections; target recheck passes 426 tests with three explicit skips. The original
unchanged fixed-180-ms fixture failure is retained separately, not silently
replaced. Four existing signed worker source closures match, so no new package
is authored or installed. All 1538 prior file observations, 360 directories and
controller files remain exact; only a fresh 16-file client capsule is added.

Explicit selected report/artifact retention passes primary-store fresh readback.
R18 remains reserved without authority or consent; journal 412/58 and idle
resources stay unchanged. Finite controller/discovery authority is expired and
not renewed. Fresh current-image Bluetooth facts and interactive device readiness
remain separate from this no-effects preparation. See
node:docs/audits/REVIEW-SENSORIUM-POLICY-V4-TARGET-2026-10-25.md.
P096-005 remains partial. No device, permission probe, reset, recovery, actual
restart, root migration or merge occurs.


The same policy-v4 pin now completes the actual-owner ordinary→fresh-grant→
emergency software composition: six episodes, ten automatically collected
records, one tuple, zero missing fields, 98.80 seconds. All ten untouched records
also pass the fresh Schema Gate and v4 measurement caps. The real normal client
separately reviews and approves runtime authority, preserving the parent and
requiring new consent. Explicit 33-member/two-image primary readback passes.
This proves software completeness only: SDK/discovery, firmware/TCC and kernel
restart remain explicit fixtures. Native full-tuple/current-image facts and a
separately approved actual host restart still block P096-005 completion.


### Full terminal metadata boundary — 2026-10-25

A subsequent no-device egress check finds that the actual software fault Case
with its normal checkpoint assignment is 17,514 bytes, exceeding the old 16-KiB
terminal capture, SSH reader and copier. The earlier six-owner/ten-record proof
covered record collection, not this full transport boundary; it stays unchanged.
Terminal metadata now has an explicit bounded 64-KiB path through real captures,
closed parser, relay and actual owned copier. Four new regressions and the full
software replay pass, as do 430 pinned Python tests with three explicit skips.
Control/nonce/stderr limits, samples, clocks and all qualification criteria remain
unchanged. See node:docs/audits/REVIEW-SENSORIUM-TERMINAL-METADATA-2026-10-25.md.

A superseding pinned signed target client must precede physical fault use.
The private two-pass draft gates fault on seven validated ordinary records and
restart review on two actual fault records plus checkpoint. It preserves exact
raw support hashes and a shared STOP; fresh human readiness and per-run pins are
mandatory. It contains no restart, reset, recovery or renewal executor. P096-005
remains partial; no native proof, root migration or merge is claimed.


### Complete-terminal target preparation — 2026-10-25

The superseding clean Node `7200df68` candidate is prepared and signed on the
nearby host (source `1ed03697`, GUI `fde8657d`, exact handoff `1fa73814`). All
5407 Git objects, 263 frozen inputs, four unchanged signed worker closures and
430 target tests (three explicit skips) pass. Separate loaded-section/signature
review and preservation of 1554 old file observations/366 directories/controller
pass, with only sixteen new capsule files/six directories. Root journal 412/58,
idle resources, reserved unregistered r18 and expired authority remain unchanged.

The exact pin completes six actual-owner software episodes, ten automatic
record types, one tuple and zero missing fields in 118.90 seconds. All ten
untouched records pass the independent current Schema Gate/policy-v4 checks;
the complete 17514-byte software Case/checkpoint passes the frozen captures,
parser, nonce relay and actual copier byte for byte. Fourteen unarmed two-pass
bridge tests and thirteen isolated dispatcher regressions pass. Explicit selected
preparation/software proofs and their exact images pass full primary-store
readback. See node:docs/audits/REVIEW-SENSORIUM-TERMINAL-METADATA-2026-10-25.md.

Software SDK/discovery/firmware/TCC/kernel restart fixtures do not establish
native evidence. P096-005 remains partial. Fresh finite authority and interactive
headband readiness, actual current-image native/TCC facts and separately approved
actual host restart remain required; no device, permission probe, renewal,
recovery, root migration or merge is performed by this preparation.


### R18 authority renewal — 2026-10-25

Normal exact review `54d5924f` was prepared, independently verified, explicitly
human-approved and committed once via the pinned administrator. Only the same
controller/discovery scope is renewed, to 2026-10-25T23:29:32Z. Complete closed
write-set review preserves 1570 old file observations/372 directories, twelve
protected inputs, journal 412/58, consent/history and zero claims; an ordinary
read-store ctime-only change is disclosed. Discovery stays r5 and reserved r18
has no p21 grant or consent. Seven selected proof members pass primary-store
readback. See node:docs/audits/REVIEW-SENSORIUM-R18-AUTHORITY-2026-10-25.md.
P096-005 stays partial: fresh interactive readiness, current-image TCC/native
facts and a separately approved actual host restart remain. No hardware,
reset, recovery, migration or merge is performed by this metadata renewal.


### R18 physical partial proof — 2026-10-25

The newly approved source `1ed03697`/GUI `fde8657d` sequence reaches fresh
SCAN/BIND/REGISTER r18 and one WEAR. During native prepare an authenticated
protected withdrawal ends baseline incomplete-released with durable audit,
confirmed native/executor/controller cleanup. The operator reports switching
Safari to ChatGPT; the served visibility handler is consistent with that event,
without inventing an independently captured browser event. No later ordinary
or fault session runs. Configuration validation is 149/2048 ms, not a timeout.

The unchanged current collector/Schema Gate/policy-v4 gates accept two actual
full-tuple records: authority 13407 ms and consent 8748 ms against 15000 ms each.
Eight safety types remain missing and full export refuses. Actual Stop-to-exact
exit observation is 10255 ms against the unchanged 10000-ms gate, requiring
investigation before another physical attempt. Journal 421/59 Cases and zero
claims/controller preservation pass; seventeen retrieved reports and an explicit
37-member selected proof pass primary readback. See
node:docs/audits/REVIEW-SENSORIUM-R18-PHYSICAL-2026-10-25.md.
P096-005 stays partial; no retry, reset, recovery, retirement or merge occurs.


### Protected executor-exit window correction — 2026-10-25

Source review confirms that native cooperative release used the twenty-second
completion clock despite the separate ten-second protected-exit gate. The owner
now freezes both original clocks before Stop publication and carries exact
operation-fence/launch identity and absolute cutoffs through channel lookup/RPC,
registry locks and forced process disposal. It preserves 7.3 seconds for normal
native release, the original twenty-second completion/audit cap, actual
post-return exit timestamps and retained ownership on unknown exit or unfinished
finalization. Neither legacy shutdown grace nor a replacement executor can
supply release proof. Review fixes bounded snapshot acquisition, stale session
projection and reuse after failed lifecycle publication.

Tests pass 117 acquisition, ten supervisor-host, 147 private-owner, nineteen
transport and 76 supervisor cases; opt-in exclusions remain explicit. Five real
owned synthetic-process tests include five-second release and nonreturning
release with retained claim. The exact pinned software image completes six
actual-owner episodes in 101.50 s, all ten records in one tuple, zero missing;
all unchanged records independently pass the frozen Schema Gate and policy-v4
checks. An explicit 45-member proof plus three images passes primary readback.
See the review at node:docs/audits/REVIEW-SENSORIUM-PROTECTED-EXIT-2026-10-25.md.

This is prospective software evidence. R18's two native records and 10255-ms
observation remain unchanged; a different image needs its own full native tuple.
P096-005 stays partial pending current-image native/TCC and a separately approved
actual host restart. No hardware, SSH, reset, recovery, retirement, renewal or merge.


Independent post-commit review reads all 5407 source blobs of Node `fa1ec48c`
and reproduces `sha256:5ca01fce9d906f4423ed49d510236d5222b4cd9bb1c0960d058303f9c64a00b2`,
matching the frozen test image. The original selected archive is unchanged;
a separate source-confirmation manifest `dfc19ef0` passes primary-store readback.


### Discovery fixture startup observation — 2026-10-25

Nearby preparation of source `5ca01fce`/GUI `098c7d8f` passes signatures and
rootless context checks, then its 430-test software suite errors because a fixed
180-ms test sleep assumes a first child snapshot is already available. The
original refusal is retained; no native manager or hardware runs. All 1590 old
files/376 directories/controller bytes and journal 421/59 Cases remain exact,
with only sixteen new GUI files/six directories and zero claims.

The test now observes actual revision one before releasing revision two through
a scoped barrier, under the original 1200-ms request deadline. Production code,
protocol and qualification limits are unchanged. Twenty-five repetitions, forced
250-ms delay and 26 provider tests (one explicit skip) pass. Fourteen selected
proof members pass primary readback; see the
review at node:docs/audits/REVIEW-SENSORIUM-DISCOVERY-FIXTURE-2026-10-25.md.
A new clean source pin/client is required; earlier software/native evidence stays
frozen and P096-005 partial. No hardware, renewal, recovery, migration or merge.


### Protected-exit target client prepared; journal capacity pending — 2026-10-25

Clean Node `5ebce37e`, source `0b29a069`, standalone `950db254`/109911504 bytes,
signed GUI `b89d7677` and handoff `4e30d075` pass independent Git, signature,
loaded-section and target-byte review. All 267 frozen inputs and 430 target Python
tests (three explicit skips) pass; four existing signed worker closures stay
exact without Author/Sign. Rootless check/real launchd context pass, with no
manager or permission observation. Earlier local Rust/full-owner software proof
remains at its own original image; no native result is inferred for this client.

All 1606 old files/382 directory identities/controller/parent state and journal
421/59 Cases remain exact, with only sixteen new GUI files/six directories.
Fourteen selected report/manifest members and four artifacts pass primary
readback. See the review at node:docs/audits/REVIEW-SENSORIUM-PROTECTED-EXIT-CLIENT-2026-10-25.md.

Before another physical sequence, resolve journal capacity: 59/64 Cases and
236696/262144 bytes leave fewer than the six required slots. Retirement does not
free them. The operator subsequently adopted prospective 128 Cases / 1 MiB
and a whole-six-session preflight. Implementation and a superseding pinned
client remain pending; this prepared image still has the original limits. Stopped r18, finite authority
and old native evidence remain unchanged. P096-005 stays partial; no hardware,
permission probe, retirement, renewal, recovery, migration or merge occurs.


### Prospective private journal capacity and whole-six preflight — 2026-10-25

The operator-adopted limit is implemented at 128 Cases / 1 MiB without changing
journal v1, historical bytes, qualification gates or finite grants. Conservative
6144-byte records plus envelope account for future disposal growth; all 128 fit
787584 reserved bytes. Read-only closed metadata rejects unknown history.
Scheduler/client/host checks precede adapter, socket and supervisor effects;
five ordinary plus one emergency Case check remaining capacity 6→1. Snapshot
accounting is not a reservation across processes. Affine prepare remains one-use.

Review corrected narrow visibility, an oversized fixture and surplus-argument
truncation; 152 owner/10 entry/443 Python tests and production daemon check pass,
with opt-in exclusions retained. Twenty selected software members pass primary
readback. The private wrapper remains explicitly unarmed. A superseding pinned
client and actual read-only target preflight are next; the old prepared image
still has its original limits. No target/root rewrite, native test, renewal,
retirement, reset, recovery or merge; P096-005 remains partial. See the review at node:docs/audits/REVIEW-SENSORIUM-JOURNAL-CAPACITY-2026-10-25.md.


### Journal-capacity client and actual six-Case preflight — 2026-10-25

Clean `905715d0`/source `6fa1dd72`, standalone `45ccc16c` (110312432 bytes),
signed GUI `19de691d` and handoff `ee6aaed1` pass independent pin/signature/byte
review. All 5409 Git blobs, 270 frozen inputs and 443 target Python tests/three
explicit skips pass; four signed worker closures remain exact without Author/Sign.
Actual frozen-SSH metadata agrees with independent accounting: 59/128 Cases,
69 available, six requested, projected 400449/1048576 bytes including full-record
growth, with no reservation or journal write. The private observer's initial
system-Python API refusal is preserved and corrected without rebuilding product.

All 1622 old file observations/388 directory identities/controller remain exact;
only sixteen new GUI files/six directories are added. Journal 421/59, zero claims
and finite authority stay unchanged. Nineteen selected members/four artifacts
pass full primary readback. Stopped r18 remains registered. No permission probe,
manager, native run, retirement, renewal, recovery, migration or merge follows;
P096-005 stays partial. Fresh native/two-pass consent and separate actual restart
remain required. See the review at node:docs/audits/REVIEW-SENSORIUM-JOURNAL-CAPACITY-CLIENT-2026-10-25.md.


### Released-r18 retirement review prepared, not consumed — 2026-10-26

Verified administrator `905715d0` prepared exact normal released-Case review
`20574413` for r18→r19. Independent canonical digest, four target-only source
projections, expired host/runtime grants and binding, completed predecessor,
journal/consent/controller and idle resources pass. R18 remains registered;
r19 is not reserved and RETIRE-P21 approval is pending. All 1638 old content/key
observations and 394 directory identities remain; only the review is added.
A sole SQLite ctime change preserves all other fields and is consistent with
the normal permission path, without an OS-traced cause. Journal 421/59/zero claims
and finite expiry remain unchanged. Four closed proof members pass primary
readback; raw configs and snapshots are excluded. No retirement, new grant,
hardware, renewal, recovery, migration or merge; P096-005 partial. See the review at node:docs/audits/REVIEW-SENSORIUM-R18-RETIREMENT-PREPARED-2026-10-26.md.


### Unarmed r19 plan and post-restart collector — 2026-10-26

Private preparation binds existing `905715d0` / source `6fa1dd72`, GUI `19de691d`
and handoff `ee6aaed1`; both launch barriers remain unarmed. Review fixes marker-to-
reservation inference, unchecked saved prior results, frozen dependency coverage,
closed plan boundaries and blocking special-file reads. The complete offline
entry preserves stored inputs and refuses output reuse. Forty-seven local tests
pass without errors/failures/skips. All ten records share the retained software
tuple `f844ccf0`, with nine earlier records byte-equivalent and one restart record
added; source `5ca01fce` / software image `af176f24` remain synthetic. This does not
execute the current GUI image or prove an actual new kernel restart.

Forty-nine selected source/test/proof members pass primary readback (`a102d7c3` /
`aa2fb02d`); original refusals and before-review bytes/modes remain. No SSH,
retirement, renewal, native run, reset, recovery, migration or merge occurs.
R19 stays proposed and the recorded authority expiry has passed; actual normal
retirement, renewed authority, fresh readiness/TCC/native scope, separately approved
actual restart and independent final native export remain. P096-005 stays partial.
See the review at node:docs/audits/REVIEW-SENSORIUM-R19-UNARMED-COLLECTOR-2026-10-26.md.


### Independent two-pass safety export — 2026-10-26

An offline extension connects the reviewed unarmed r19 collection to the normal
store/export owner and separately invoked frozen safety qualifier. Eleven local
checks pass. Canonical JSON comparison closes Python bool/numeric aliases in
saved evidence and completed reports. The normal exporter writes six source
Cases and ten exact records in nineteen store files, preserving synthetic origin
and tuple `f844ccf0`; the independent qualifier correctly refuses native acceptance,
including a source-label-only relabel. A handoff is kept outside the closed store.
Thirty-seven source/test/example/refusal members pass primary readback (`950a7275` /
`a1a01cce`). Prior preparation/releases and all thresholds remain unchanged.
No SSH, hardware, authority change, retirement, reset, recovery, migration or
merge occurs; actual native/full-tuple/separately approved restart and passing
independent real-device qualification remain. P096-005 stays partial. See the review at node:docs/audits/REVIEW-SENSORIUM-R19-INDEPENDENT-EXPORT-2026-10-26.md.


### R19 authority review prepared, awaiting approval — 2026-10-26

Fresh SSH metadata confirms expired authority, journal 421/59, zero claims,
stopped registered r18 and unconsumed retirement `20574413`; r19 is unreserved.
Verified administrator `905715d0` prepares exact renewal review `43a37121` for
the same controller/discovery scope, TTL 14400 s and prospective expiry
2026-10-26T12:20:11Z. The approval window elapsed at 08:35:11Z without agent
consumption; a fresh review/approval is required. No renewal is executed. Independent
canonical review checks twelve protected positions, including four explicit
absences, and preserves the expired p21 sibling. All 1639 prior file observations/
394 directory identities/controller remain, with the disclosed SQLite ctime-only
exception; only the review is added. Seven closed proof members pass primary
readback (`c55d3098` / `b578bf89`). No manager, scan, acquisition, retirement, reset,
recovery, migration or merge occurs. Separate exact approval/live checks and
supported retirement refresh remain before any fresh physical delegation.
P096-005 stays partial. See the review at node:docs/audits/REVIEW-SENSORIUM-R19-AUTHORITY-PREPARED-2026-10-26.md.


### Approved r19 authority renewal — 2026-10-26

Expired `43a37121` was preserved without execution. Fresh exact review `984224f0`
was independently checked, explicitly human-approved and committed once by the
pinned administrator. Same-scope controller/discovery authority expires
2026-10-26T13:28:18Z (14:28:18 CET), anchored to the reviewed preparation.
Closed writes, all 1641 prior observations/394 directory identities, twelve
protected positions and expired p21 sibling preservation pass; the SQLite
ctime-only exception is disclosed. Journal 421/59, consent, zero claims and
unconsumed r18 review `20574413` remain. R19 is not reserved. Seven closed proof
members pass primary readback (`aad5055b` / `60c594bb`). No p21 grant, retirement,
Bluetooth, reset, recovery, migration or merge occurs. Supported retirement
review refresh and its separate approval precede fresh physical delegation;
P096-005 remains partial. See the review at node:docs/audits/REVIEW-SENSORIUM-R19-AUTHORITY-RENEWED-2026-10-26.md.


### Approved r18→r19 retirement — 2026-10-26

Supported archival preserves stale `20574413` byte-for-byte and prepares fresh
`eedd2720` against current controller policy. The operator separately approves
that exact review; one normal commit completes and reserves r19. Four live source
projections and durable marker match; normal inventory is applied. Only expired
r18 grant/plan/binding/receipt are removed; discovery r5/authority remain unchanged.
Journal 421/59, consent and zero claims remain. Normal configuration/binding
journals advance intentionally; no raw SQLite byte-identity claim is made.
Other source observations and 394 directory identities are preserved, with the
usual disclosed SQLite ctime exception. Prepared six-member and completed
four-member proofs pass primary readback (`819d029d` / `9d423ed5`). No p21 grant,
consent, hardware, reset, recovery, migration or merge occurs. R19 is reserved,
unregistered; fresh execution-copy/readiness/TCC/native and separately approved
actual restart remain. P096-005 stays partial. See the review at node:docs/audits/REVIEW-SENSORIUM-R18-RETIREMENT-COMPLETED-2026-10-26.md.


### Conditional r19 preparation after completed retirement — 2026-10-26

The new `5d9ee9eb` plan binds actual completed retirement `eedd2720`, current
source/image/package/handoff and four copied harness hashes. Immutable unarmed
`6477ab8c` remains unchanged; normalized operational AST bodies are identical.
Review fixes isolated helper import resolution; nine guard tests pass, including
actual isolated entry and refusal before SSH without fresh delegation. A separate
metadata-only SSH read matches 1644 files/394 directories/controller after
retirement: claims zero, journal 421/59, authority to 2026-10-26T13:28:18Z. No live
approval, permission, operator facts or native output is inferred. The 25-member
private capsule passes primary readback (`ae99ef9c` / `9bc3b85e`). Fresh readiness,
firmware/TCC and actual six-session/restart/native qualification remain open;
P096-005 stays partial. No product rebuild, thresholds, hardware, recovery,
migration or branch merge. See node:docs/audits/REVIEW-SENSORIUM-R19-CONDITIONAL-PREPARATION-2026-10-26.md.


### R19 native two-pass result — 2026-10-26

Fresh scoped readiness, firmware 1.0.25 from Muse iOS, exact-client allowed
permission and bounded TCC attribution precede six actual WEAR decisions. Five
ordinary sessions release and yield seven records; the controlled native fault
exits its worker, keeps its claim and supplies two more valid records under one
full tuple (`cf22826c`). All original gates pass for those nine records. Overall
unmodified collection still exits 2: no restart checkpoint; only
restart-unclosed-marker is missing. Checkpoint failure details were discarded, so the exact historical refusal is
unknown. A retained, hash-verified real-controller test proves a lock-lifetime
hazard in the entry whenever unresolved owners still hold custody. Software used a borrowed cfg(test)
view and did not cover that entry mismatch. Root journal is 465/65 Cases, one
claim retained; 44 target reports are retrieved exactly. The 83-member private
capsule passes primary readback (`572b5726` / `f531c376`). No native retry, restart,
reset, recovery or merge. P096-005 remains partial; prospective production-path
fix and device-free regression remain next. See node:docs/audits/REVIEW-SENSORIUM-R19-PARTIAL-NATIVE-2026-10-26.md.


### Production checkpoint custody regression — 2026-10-26

Node implementation checkpoint: `cb98a5df`.

Prospective restart capture borrows the existing controller and affine Case
writer, verifies exact fenced history and preserves closed refusal diagnostics.
The first actual software regression exposed a second writer re-acquisition;
that defect is fixed without changing any qualification gate. The normal runner
now passes six software episodes/ten records/one synthetic tuple (`7e0f6aaf`) in
144.35 s, using its production-generated checkpoint. One hundred standard Rust
checks, the explicit full composition, 445 Python checks (three skipped) and
non-test compilation pass; eight ordinary owner opt-ins remain explicitly skipped
in that filter. Private 108-member proof passes byte readback (`b1c4cfe9` /
`4c4d4350`), with current retention metadata and unresolved ownership/holds/minimum
retention/restoration/replicas left unknown. Native r19 stays nine records with
its missing checkpoint and unknown historical refusal; no software/new-candidate
record can fill that tuple. No device, target mutation, restart, recovery or merge.
P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-CHECKPOINT-CUSTODY-2026-10-26.md.


### Pinned checkpoint-custody target client — 2026-10-26

Node preparation checkpoint: `18e6f023`; compiled source remains `cb98a5df`.

Clean `cb98a5df` now supplies target source `e44497a1`, standalone `03f0d476`,
actual signed GUI `7d2b8ae6` and handoff `886d530c`. Independent 5409-Git-blob,
loaded-payload/signature checks and 270 frozen target inputs pass; 445 target
tests pass with three explicit skips. Existing four signed worker closures match
and are unchanged. Rootless signed launchd preflight creates no Bluetooth manager
or authority; this image's Bluetooth permission remains unknown. All 1695 old
files/399 directory identities/controller observations are exact; only a new
16-file/six-directory capsule is added. Root journal465/65 Cases, one held claim
and expired authority remain unchanged; no admission/capacity claim follows.
The 399-member private preparation set passes byte readback (`a4e3400a` /
`d02bc430`), with unresolved retention facts left unknown. No device, renewal,
recovery, retirement, migration or merge. Native r19 remains nine records;
P096-005 stays partial. Fresh authority and separately approved reconciliation
precede fresh physical readiness and an actual separately approved restart.
See node:docs/audits/REVIEW-SENSORIUM-CHECKPOINT-TARGET-2026-10-26.md.


### R19 Bluetooth reconciliation and same-scope renewal — 2026-10-26

Node checkpoint: `c43cf4b6`; P096-005 remains partial.

The original compatible pinned administrator preserves baseline `4b8e99cc`,
prepares v4 `1c97486c` and, after one refused observation and a separately approved
new one, records OFF/ON proof `5d5bcdc1` (2998 ms off). Separately approved recovery
completes marker `1f1b72de`: only the exact acquisition resource/old claim are
removed, generation changes and expired policy remains unchanged. Renewal must
follow reconciliation; it cannot bypass the unresolved Case. The new pinned
client prepares/commits separately approved review `2d32bad7` after unexecuted
`9bacacc7` expires. Same-scope owner/discovery expiry is 20:23:56 CET; expired p21
r19, journal465/65, consents and history are preserved. Controller/resources are
free; no p21 retirement/grant, scan, acquisition, host restart or merge occurs.
The private 459-member proof passes byte readback (`71150e83` / `651c264f`), with
unknown retention facts and a disclosed read-store ctime-only exception. Original
native nine-record tuple stays incomplete; P096-005 remains partial.
See node:docs/audits/REVIEW-SENSORIUM-R19-RADIO-RECONCILIATION-2026-10-26.md.


### R20 operational prerequisite and collector readiness — 2026-10-26

Node checkpoint: `377511b8`.

Supported, separately approved retirement of expired r19 has reserved r20 while
preserving consent, recovery and Case history. Reused collection contracts cover
the ten original records in software; no new native or actual-restart evidence
is inferred. P096-005 remains partial, with fresh interactive headband/firmware,
exact-client access, one complete new native tuple and separate actual-restart
approval still required. See node:docs/audits/REVIEW-SENSORIUM-R20-CONDITIONAL-PREPARATION-2026-10-26.md.


The independent r20 emergency Case's later restart observation uses the existing
read-only GUI observer, rather than the formal campaign-directory adapter. Its
inert recipe has software coverage only; separate actual-restart approval and
measured native completion remain open. See the follow-up in
node:docs/audits/REVIEW-SENSORIUM-R20-CONDITIONAL-PREPARATION-2026-10-26.md.


### Native r20 and legacy checkpoint custody — 2026-10-26

Status: P096-005 remains partial. One freshly approved ordinary five-session run
and one separately granted emergency session use source `e44497a1` / GUI
`7d2b8ae6`, fresh Muse iOS firmware 1.0.25 and current OS Bluetooth attribution.
The unchanged collector validates nine record types under one native tuple
`83aaf244`; no actual host restart is observed. Ordinary sessions release; the
injected hang retains exactly its uncertain claim after verified worker exit
and durable audit. Its checkpoint is null with `case-journal-refused`.

Read-only diagnosis reproduces the failure at source collection: the older root
has `control/0755`, while the checkpoint demanded a 0700 marker parent there.
Normal confined source reads are now reused and new create-only 0600 checkpoint
files live under the already private 0700 root. Existing control modes and files
are not migrated. Frozen control-location markers retain their original strict
parent check; ambiguous locations, links and unsafe modes refuse. Candidate,
boot, journal, source, resource, claim and protected-stop requirements stay intact.

The fix is prospective. Old output and quarantine are not changed or qualified
by later software tests. Fresh headband readiness precedes any later native run;
actual host restart and recovery remain distinct approvals. See
node:docs/audits/REVIEW-SENSORIUM-R20-NATIVE-CHECKPOINT-2026-10-26.md.


### Prepared private-root checkpoint client — 2026-10-26

Source `fea95dd1` / pin `6aedb062` and signed GUI `76aee865` are prepared on the
nearby host. Independent source/signature/payload checks, 270 exact inputs and
445 software checks (three skips) pass. Worker packages are unchanged; old root
files, history and the r20 uncertain claim are preserved. Permission readiness,
actual native/restart proof and supported reconciliation remain separate. No
manager, acquisition, renewal, recovery, root migration or merge occurs. The
388-member private artifact set is read back and hashed, with unknown owner,
minimum retention, dependency/hold completeness and replica guarantees protected.
P096-005 remains partial; the new artifact does not complete frozen tuple `83aaf244`.
See node:docs/audits/REVIEW-SENSORIUM-LEGACY-CHECKPOINT-CLIENT-2026-10-26.md.


### r20 Bluetooth recovery observation — 2026-10-26

The separately approved single OFF/ON observation for v4 `05f313fe` completes
with 3739 ms off and confirmed observer exit. Proof `eb4a2c9a` binds the reviewed
historical administrator/source, current boot and four worker-absence checks.
Eleven protected source slots, journal 509 / 71 Cases, controller and resource
bytes are unchanged; the claim/quarantine remain held. A read-store ctime-only
exception has unknown cause and is not claimed as full metadata preservation.

The predecessor baseline is archived byte for byte. New client provenance is
not substituted into this historical recovery epoch. Shared bounded readback
verifies separate preparation and actual-observation archives; unknown custody,
retention, hold/dependency completeness, restoration and replica guarantees stay
protected. No acquisition, host restart, renewal, claim release or merge occurs.
RECOVER requires a separate exact approval. This Bluetooth proof cannot fill the
missing restart checkpoint of native tuple `83aaf244`; P096-005 stays partial.
See node:docs/audits/REVIEW-SENSORIUM-R20-BLUETOOTH-OBSERVED-2026-10-26.md.


### r20 Bluetooth recovery completed — 2026-10-26

One separately approved RECOVER-BLUETOOTH completes review `05f313fe` and proof
`eb4a2c9a`. Independent marker `b874b653` readback confirms the exact reviewed
controller policy, free controller and removal of the selected acquisition
resource only. Journal 509 / 71 Cases, history, consent and eleven protected
source slots remain exact. A read-store ctime-only exception has unknown cause.

Cleanup custody remains separate from expired operation authority; no grant is
renewed. Private retention verifies all 45 selected members with unknown custody
facts protected. No scan, measurement, actual host restart, retry or merge runs.
R20 retirement, fresh operation authority and interactive headband readiness
remain separate. The frozen native tuple `83aaf244` lacks its runtime checkpoint;
this disposal does not complete P096-005. See
node:docs/audits/REVIEW-SENSORIUM-R20-RECOVERY-COMPLETED-2026-10-26.md.


### Legacy-control completeness and r21 readiness — 2026-10-26

Two actual private-runner software compositions each complete six sessions and
all ten required record types: 0700/tuple `1ae924f9` and legacy0755/tuple
`e631599d`. The same scenario table, owners, checkpoint, collector, Schema Gate
and semantic evaluator are used. The control mode is preserved. Independent
recapture checks twelve owner outputs and twenty records. Scan/SDK and kernel
boundary remain explicitly synthetic; no actual host restart is inferred.

Test source `40ab50d4` / image `6e05b3b9` fits the unchanged 128-MiB bound with
assertions/overflow checks retained. Comparison with prepared source `6aedb062`
finds only a test-only helper and acceptance README differ. No native tuple is
promoted. Separate exact approvals complete renewal `f9019882` through
2026-10-27 00:48:18 CET and target-only retirement `ccfc1484`: controller free,
r21 reserved, discovery r5 and journal 509/71, Case history and consent preserved.
No p21 grant, WEAR, Bluetooth, actual restart or merge runs.

Private operational and software archives pass every-member fresh readback;
unknown custody, retention, complete holds/dependencies, restoration and replica
facts stay protected. Native tuple `83aaf244` remains incomplete. Fresh headband
readiness and a separately approved actual restart remain required; P096-005
stays partial. See node:docs/audits/REVIEW-SENSORIUM-LEGACY-COLLECTOR-COMPLETENESS-2026-10-26.md
and node:docs/audits/REVIEW-SENSORIUM-R21-READINESS-2026-10-26.md.


The r21 execution plan remains unarmed. All 47 software guard and post-restart
collector checks pass on the fresh legacy reports; a stale fixture import path
is corrected without relaxing exact-import validation. Read-only capacity has
57 Cases available for six required and projects 474189/1048576 bytes. Exact
release/GUI files and strict signatures pass metadata-only verification without
a permission manager. The 32-member private set passes every-member readback
with unknown custody facts protected. Fresh hardware readiness and current
Bluetooth permission remain required; P096-005 is partial.


### r21 permission-only observation — 2026-10-26

A fresh one-use approval runs the normal prepared `6aedb062` / signed GUI
`76aee865` permission-only SSH command, after exact release/closure and signature
checks. Bluetooth is allowed, manager cleanup and observer exit are confirmed,
and no SCAN, headband acquisition, registration, reset or recovery occurs.
The immutable output's unverified responsible-process projection remains intact;
six separate current OS attribution events identify the exact Orbiplex client
within the actual invocation interval. No system-wide process inventory is
collected; selected private events contain ephemeral PIDs.

Read-only comparison preserves all root/controller observations, journal 509/71,
zero claims, discovery r5 and reserved unregistered r21. Authority remains valid
through 2026-10-27 00:48:18 CET. The 25-member private proof passes fresh archive
readback with explicit unknown custody/retention facts protected. Software
preparation remains 47/47; the plan is unarmed, and fresh interactive headband
readiness/firmware plus a separately approved actual restart remain mandatory.
P096-005 stays partial; no native tuple or release readiness is promoted and no
branch merge occurs. See node:docs/audits/REVIEW-SENSORIUM-R21-PERMISSION-2026-10-26.md.

Node's complete light gate records a pre-existing cumulative Git-history refusal
in the host-control evidence area: 1079179 bytes against 1048576. This permission
checkpoint adds no governed payload and changes no policy, checker or historical
ref. Focused ledger/header/path and Orbidocs JSON/schema-sync checks pass; full
workspace retention qualification is not claimed. The dated Node review retains
this separate repository blocker without weakening any limit.

Node permission checkpoint: `bf2c6563`; P096-005 remains partial.


### r21 native ordinary sequence and budget refusal — 2026-10-26

Fresh approval covers the ordinary pass and a conditional fault pass. Exactly
five WEAR sessions execute on source `6aedb062` / GUI `76aee865`; the sixth WEAR
and fault session never start. Firmware 1.0.25 is freshly reported from Muse on
iOS. Current permission/OS attribution, SCAN/BIND/REGISTER, five sessions and the
negative expired-grant probe complete. Each session confirms exact exit,
cleanup, durable audit and controller release. Driver exit 0 / 304154 ms is an
orchestration result; the outer qualification batch exits 2 before fault admission.

`Current-authority-before-effects` measures 21829 ms against unchanged 15000 ms:
about 10.707 s activation-to-permit, 1.339 s permit-to-SDK entry and 9.782 s native
prepare, with one prepare attempt. Independent unchanged diagnostic checks pass
six other records under full tuple `5cfb9ba6`, preserving the original batch
plan/refusal and input hashes. This is no passing full run. Hung-worker-stop,
uncertain-cleanup-retains-claim and restart-unclosed-marker are unexecuted.
No measurement interval is shortened and no threshold is raised.

Post-run journal 546/76, zero claims and free controller are observed. R21 remains
registered with expired finite grant. No retirement, renewal or recovery runs.
The 55-member private original set passes full archive readback with unknown
retention/custody facts protected. Current policy bytes are retained; builds/cache
stay separate. Further stage-level software measurement is needed before naming
a slow function. P096-005 stays partial; no reset, actual restart, sequence retry
or merge occurs. See node:docs/audits/REVIEW-SENSORIUM-R21-NATIVE-2026-10-26.md.

Node native checkpoint: `21940ebe`; exactly five WEAR sessions executed, fault pass unexecuted, P096-005 partial.


### r21 device-free runtime-integrity measurement — 2026-10-26

A generic ignored supervisor test calls the unchanged production integrity
verifier three times on hash-matched r21 runtime data. Release measurements are
1099/554/548 ms for 820 explicit files and two trees containing 2413 files.
Initial cache state and the actual startup's full-verification count remain
unknown. This measures one primitive, not the complete host admission path or
native preparation, and changes no qualification window or threshold.

Eight software controls and release clippy pass. Review makes profile input
nonblocking/no-follow before bounded regular-file parsing. No interpreter, SDK,
worker, controller or Bluetooth manager is invoked. Expired registration data
is read as data and supplies no authority. The private 56-member proof passes
fresh every-member readback with unknown custody/retention facts protected.
The existing r21 native refusal remains immutable; startup-stage intervals are
the next diagnostic step. P096-005 stays partial. No headband, normal-root write,
grant update, recovery, reset or merge occurs. See node:docs/audits/REVIEW-SENSORIUM-R21-RUNTIME-INTEGRITY-PROFILE-2026-10-26.md.

Node read-only profile checkpoint: `c33f7531`; native P096-005 remains partial.


### Bounded startup-stage observations — 2026-10-26

The existing Node acquisition trace now records ten immutable first-entry slots
and nine fixed adjacent monotonic durations. Missing or reversed clocks stay
unknown. The optional closed diagnostic is engineering data, never authority or
a replacement qualification clock; the 15-second before-effects gate stays
unchanged. Owner documentation distinguishes local intervals from cross-process
clocks and excludes pre-entry scheduling from this projection.

Software tests and one six-session production-owner composition prove collection:
all ten records under one synthetic tuple and all nine startup intervals in each
session. Independent recapture uses the actual Schema Gate and unchanged
semantic evaluator. The original r21 native inputs and 21829/15000 ms refusal
stay immutable. This does not prove a native speedup or permit integrity caching.
A fresh pinned client and separately approved native trial remain prospective;
fault cleanup and actual host-restart evidence stay open. P096-005 remains
partial. See node:docs/audits/REVIEW-SENSORIUM-R21-STARTUP-INTERVALS-2026-10-26.md.

The private 84-member software proof passes every-member byte readback; owner,
minimum retention, complete holds/dependencies, restoration and replica floor
remain unknown and protected. No public-retention or native qualification follows.

Node startup diagnostic checkpoint: `3a13f8cc`; native P096-005 remains partial.


### Prepared startup diagnostic client — 2026-10-26

Clean Node `3a13f8cc`, source pin `45b365d2`, is now prepared nearby with the
bounded startup diagnostic projection and matching strict client. Standalone
`947c558c` / GUI `8a4ec1c4` pass strict signatures and rootless launchd checks.
The actual target verifies 270 frozen inputs and runs 446 software tests (443
pass, three explicit opt-ins skip). Four existing package signatures and exact
worker source closures pass without package mutation. Every prior root file
observation and journal546/76 stay intact; only the fresh client capsule is added.

The 428-member private proof passes every-member byte readback; unknown custody
and retention facts stay protected. No Bluetooth permission, device operation,
registration change, recovery, restart or native speedup is claimed. Stopped r21
must use its supported separately approved transition before fresh readiness and
WEAR. The native 21829/15000 ms refusal and missing fault/restart evidence remain
unchanged; P096-005 stays partial. See
node:docs/audits/REVIEW-SENSORIUM-STARTUP-DIAGNOSTIC-CLIENT-2026-10-26.md.

Node prepared-client evidence checkpoint: `ef5ac216`; the executable source remains `3a13f8cc`.


### Released r21 review after resume — 2026-10-28

Historical review b223f641 passes independent source/release/history checks and
seven refusal controls, preserving one explicit read-store ctime exception.
After separate current approvals, exact 24-helper SIGTERM maintenance, same-scope
renewal d56a0b48 and fresh retirement 2aa65f18 complete. The old review is archived
byte for byte; r21 is retired and r22 reserved without a p21 grant or consent.
Four reviewed source projections match; journal 546/76, consent, predecessor and
idle resources remain exact. Owner/discovery expire at 2026-10-28 14:39:38 CET.

One separately approved permission-only preflight of prepared GUI 8a4ec1c4 reports
allowed, confirmed cleanup and observer exit. All 1863 root file observations,
425 directory identities and controller state remain exact. Its TCC responsible
attribution remains unverified. No SCAN, acquisition, recovery, host restart or
merge occurs. Four additive private sets (52/114/43/44 members) pass fresh byte
readback; unknown custody and retention facts stay protected.

P096-005 remains partial. This lifecycle/permission evidence does not change the
native 21829/15000 ms refusal, identify a startup speedup, qualify missing native
fault cleanup or substitute for the separately approved actual host restart.
Fresh headband readiness precedes any physical diagnostic. The bounded convergence
review keeps release/recovery, historical/current authority, renewal/retirement
and diagnostic/qualification contracts separate while reusing existing owners.
See node:docs/audits/REVIEW-SENSORIUM-R21-RELEASED-RETIREMENT-2026-10-28.md.

Node operational evidence checkpoint: `af2fc218`; executable source remains `3a13f8cc`.


### Ordinary r22 startup diagnostic — 2026-10-28

One freshly approved normal p21 Case through prepared source 3a13f8cc / GUI
8a4ec1c4 completes SCAN/BIND/REGISTER/WEAR, exact exit, confirmed cleanup,
durable audit and controller release. Both required presets are observed; no
operation timeout/retry occurs. All nine bounded startup intervals are present:
admission-to-running is 9355.987750 ms, including ready-to-running 5662.097125 ms.
These host diagnostic clocks are not the 15000 ms qualification interval, an
isolated SDK prepare duration or proof of a particular performance fix.

Journal becomes 555/77, all 76 old Cases remain exact, and resources/controller
are idle. The late configuration-refused observation is recorded with effects
already fenced and does not replace the RunCompleted first cause. The 58-member
private proof (manifest 2d6816db / archive a2968f5f) passes complete byte readback;
unknown custody/retention facts stay protected. Firmware is historical only.
No fault, grant revocation, reset, recovery, actual restart or merge occurs.

P096-005 remains partial. The ordinary package cannot be relabelled as the
campaign package or combined with incompatible historical tuples to fill the
six/two/two origin matrix. The current source-to-owner audit preserves all ten
required records, native corroboration, original thresholds and the actual
host-restart condition. Full compatible native ordinary/fault evidence and the
separately approved actual restart are still required. See
node:docs/audits/REVIEW-SENSORIUM-R22-STARTUP-DIAGNOSTIC-2026-10-28.md.

Node native-diagnostic checkpoint: `3adb00be`; executable source remains `3a13f8cc`.


The following read-only signed-client six-Case capacity gate passes: 77/128 used,
51 available and 511059 projected bytes below 1 MiB. No capacity is reserved.
A prospective unarmed 5+1 plan preserves the ten required origins, reuses the
future baseline for the fault Case and requires separate actual restart approval.
R23 remains unreserved and execution unapproved; supported r22 handling must wait
for the observed binding expiry at 12:10:37 CET. Missing approvals, firmware and
future source/checkpoint references remain absent. The 24-member private proof
(manifest 9034c438 / archive 18b0d910) passes byte readback with unknown custody
protected. P096-005 remains partial; no new device session or source change occurs.

Node unarmed-follow-up checkpoint: `a084c4bb`; executable source remains `3a13f8cc`.


A follow-up source review corrects only the unarmed plan harness binding to the
actual signed GUI inventory. Original plan/capacity evidence stays immutable;
v2 plan 3f01cd46 and its 19-member supplement (manifest 4de934fd / archive a5aa1c69)
pass source/byte review. No authority, execution, source code, threshold or P096-005
qualification status changes.

Node plan-binding review checkpoint: `83d566ec`; executable source remains `3a13f8cc`.


### Current-pin unarmed full-runner integration — 2026-10-28

New prospective r23 working recipes bind the prepared current client while
leaving the exact retirement review/receipt and execution approval absent.
Forty-eight local tests pass, plus three actual isolated entry refusals before
SSH/native work. Current-collector reassembly of previously measured software-SDK
inputs preserves nine original records and adds only the tenth under synthetic
tuple a361e875. This is fresh software composition, not a new owner SDK run,
physical-origin matrix or actual host restart.

Review corrects the exact released-case receipt expectation and a review-digest
test fixture whose broad scope hid the intended transitive dependency check.
Campaign-plan GUI-inventory and source-report qualifier harness preimages retain
distinct owners. No authority or readiness is inferred, no old approvals are
copied, and production source/thresholds remain unchanged. The 56-member private
set (manifest e31950a3 / archive c99159ef) passes byte readback with unknown custody
protected. P096-005 remains partial until full compatible native evidence and a
separately approved actual restart qualify. See
node:docs/audits/REVIEW-SENSORIUM-R23-UNARMED-RUNNER-2026-10-28.md.

Node current unarmed-runner checkpoint: `bbbeb86d`; executable source remains `3a13f8cc`.


### Expired r22 retirement and configured r23 recipe — 2026-10-28

After observed binding expiry, one bounded foreground task prepares exact review
1565525a. Independent four-source/release/history/consent checks pass. The operator
separately approves it and one signed-client commit completes r22 retirement,
reserving r23 without grant or consent. Four final documents match the proposal;
journal 555/77, consent, predecessor and idle claims remain exact, with the explicit
read-store ctime-only exception. Controller/discovery authority remains finite
through 14:39:38 CET and is not renewed by retirement.

The configured current-pin 5+1 recipe binds the real completed receipt. Fresh
operator delegation, firmware, permission and readiness inputs remain absent;
three actual isolated entries refuse before SSH/native effects. The earlier
48-test unarmed/software proof remains separate and no synthetic approval is
copied. Private 44/55-member sets (manifests 75eb7a52/f9c6c6af) pass byte readback
with unknown custody protected. No device session, recovery, actual restart or
merge occurs. P096-005 remains partial; full compatible native ordinary/fault
records and separately approved actual restart still need qualification. See
node:docs/audits/REVIEW-SENSORIUM-R22-RETIREMENT-R23-CONFIGURED-2026-10-28.md.

Node r22-retirement/r23-configuration checkpoint: `d1964824`; executable source remains `3a13f8cc`.


### R23 partial native sequence and separately reproduced UI defect — 2026-10-28

One freshly approved sequence supplies two valid physical-native baseline rows
under full tuple da3061ef (authority 9433/15000 ms, consent 6195/15000 ms). It stops
before the second WEAR after the view wait; the operator reports both clicks,
but the precise original view failure remains unknown. Both Cases are released,
journal 570/79 and idle resources/controller are observed. Eight rows remain;
no further session, fault, reset, recovery or host restart occurs.

A separate device-free reproduction establishes that losing an accepted preview
stop reply strands the old UI. The correction reuses owner-observed stopped state
and a fresh explicit rendering confirmation, without replaying stop or inferring
WEAR. Hidden/fenced checks and all qualification thresholds stay unchanged.
Closed client view refusal codes improve future diagnosis. Python448 discovers
445 pass / three skips; focused view tests cover lost-response recovery and
hidden/fenced refusals. The private 70-member proof 45a9295c/36df9207 passes full
byte readback; unknown custody remains protected. This fix is not deployed or
hardware-qualified. P096-005 remains partial; a new pinned build, fresh scope and
compatible native/fault evidence plus separately approved actual restart remain.
See node:docs/audits/REVIEW-SENSORIUM-R23-PARTIAL-PREVIEW-RECOVERY-2026-10-28.md.

Node r23 partial-run/preview-recovery checkpoint: `12b0c29b`; measured executable source remains `3a13f8cc`.


### Fixed preview client prepared — 2026-10-28

Source 12b0c29b / digest 957562f1 is independently pinned over 5409 Git blobs and
built without incremental state. Standalone 2582451b / signed GUI da7bf9bc /
handoff c5caffc2 pass device-free staging and 448 nearby tests (445 pass / three
skips). Four signed worker closures remain unchanged, 270 frozen inputs match,
and no SDK is imported by the external runtime check. All 1899 old file
observations and 433 directory identities remain exact; only the new GUI capsule
is added. Journal 570/79, stopped r23 and idle controller are preserved.

The private 378-member proof 2ff31839/fbe79e45 passes complete primary readback;
unknown custody remains protected. No Bluetooth permission, device effect, grant,
retirement, recovery or merge occurs. Preparation is not native qualification:
r23's two physical rows retain their old candidate, eight rows remain missing,
and actual fault/restart evidence requires fresh separate decisions. See
node:docs/audits/REVIEW-SENSORIUM-PREVIEW-RECOVERY-CLIENT-2026-10-28.md.

Node fixed-client preparation checkpoint: `dae6853d`; its executable source is `12b0c29b`.


A later separate exact approval permits one permission-only observation of this
new GUI: allowed, confirmed not-scanning cleanup and observer exit, with all
1915 root files / 439 directory identities and controller state preserved.
Four current correlated TCC log records separately establish responsible-image
attribution; their original event time and the raw preflight's unverified field
are preserved. The additional private 32-member proof e10a46e6/f32a2d41 passes
full byte readback with unknown custody protected. No SCAN, WEAR, retirement,
authority renewal or recovery is implied. P096-005 remains partial. See the
separately approved permission addendum in the linked Node review.

Node permission observation checkpoint: `4589b0df`; executable source remains `12b0c29b`.


### Directly authorized r23 removal, r24 reserved — 2026-10-28

The operator requests removal of the current r23 binding, initially asking for
force, then acknowledges expiry. The original waiting task is cancelled before
preparation. The client has no force route: normal review ce440893 is prepared
after actual expiry, independently checked and consumed once. The human authorizes
the direct current-binding action rather than preapproving its later exact digest;
private records preserve that distinction and concrete scope verification.

Four final sources and completed marker match. R24 is reserved without grant or
consent; journal 570/79, consent/history, controller and idle resources are preserved.
The known read-store ctime-only exception remains explicit. Private 81-member
proof 342eb6c2/5d440951 passes full readback with unknown custody protected.
No force bypass, new administrative feature, native effect, recovery, host restart
or merge occurs. Early binding revocation remains P096-009 lifecycle scope;
P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-R23-BINDING-REMOVAL-2026-10-28.md.

Node r23-removal/r24-reservation checkpoint: `a6c37cc1`; no acquisition is authorized by it.


### Fixed-client r24 runner preparation — 2026-10-28

Completed retirement ce440893 binds a configured r24 working recipe to fixed
source 12b0c29b / GUI da7bf9bc, without copying old physical approval. Review fixes
transitive Python integrity before pre-effect imports and reuses that same byte
check in the offline restart collector. Fifty software tests and three actual
isolated no-scope refusals pass. Fresh current collector/Schema Gate assembly
preserves nine software records and adds one synthetic restart row; all ten stay
synthetic-fixture, with no new owner run or actual restart.

Read-only SSH preserves 1917 protected files/439 directory identities, journal 570/79
and the free controller. The private 70-member proof 9b27ee02/7f305fa1 passes fresh
primary readback with incomplete custody metadata protected. This preparation
adds no native qualification, permission manager, grant, consent, reset, recovery
or merge. All ten compatible rows remain required for the new image; a fresh
physical delegation and separately approved actual host restart are still absent.
P096-005 stays partial. Node owns the detailed
[review](node:docs/audits/REVIEW-SENSORIUM-R24-RUNNER-PREPARATION-2026-10-28.md).


### R24 native safety: nine rows, actual restart still pending — 2026-10-28

One freshly approved five-ordinary-plus-one-fault run on source 12b0c29b /
GUI da7bf9bc supplies nine compatible rows under tuple 6bae3b37: six physical-native,
two controlled-native-fault and one host-software. Each of six acquisitions has a
separate WEAR decision; the emergency grant is separately approved. The current
collector, Schema Gate and unchanged qualifier recheck all nine. Authority/consent
13386/4907 ms meet 15000 ms; protected receipt/fence/exit retain 626/250/10000 ms.
The five ordinary Cases release. The fault ends in deliberate uncertain native
disposal, exact process exit and retained claim/controller quarantine.

Journal 614/85, checkpoint 95897ca3 and an on-host exact digest comparison preserve
all 79 earlier Cases without exporting their contents. A narrowed six-Case export
follows automatic refusal of an overly broad read. The 79-member private proof
76498c31/82be2d85 passes full primary readback with unknown custody protected.
The operator separately approves actual host restart, still unobserved here;
`restart-unclosed-marker` remains missing. P096-005 stays partial. No whole-run
retry, reset, recovery, claim release, renewal or merge. See the Node
[review](node:docs/audits/REVIEW-SENSORIUM-R24-NATIVE-NINE-RECORDS-2026-10-28.md).

### P096-005 qualified for the exact r24 tuple — 2026-10-28

The actual five-ordinary-plus-one-fault run is completed by a separately approved
real host restart. The unchanged owner observes a new kernel boot-session,
retained marker/controller/resource claim and the ordinary Case-open refusal,
without any native resume or unknown-disposal release. Its new-boot probe is
217/20000 ms. The tested collector preserves nine original records and adds
exactly one `restart-unclosed-marker`; all ten share tuple 6bae3b37 with the
required six physical-native / two controlled-native-fault / two host-software
origins. Source 12b0c29b and GUI da7bf9bc stay fixed.

Existing source-export APIs and the pinned isolated P096 safety qualifier with
the real Schema Gate validate the complete source d19aae9b and produce decision
e0c72c74. The source deliberately excludes native exposure, P096-011a/015, p51,
publication, recording, contact quality, radio concurrency and P082. This closes
P096-005 for the exact self-wearer Muse 2 BLE p21 / macOS arm64 / signed GUI
LaunchServices scope, leaving broader Sensorium and hard-MVP work partial.

Missing restart, synthetic-origin substitution and automatic-resume copies
refuse. A supplemental readback corrects its transient cross-boot st_dev
assumption; persistent volume/root custody remains checked by the unchanged
owner, and all content/inode/mode/mtime/ctime observations stay exact. Journal
614/85, the held claim and all 79 older Cases remain preserved. The complete
188-member private proof 1ecb0c4d/3490dc06 passes full primary readback with unknown
custody protected. No recovery, claim release, new native session, root adoption,
threshold relaxation or merge follows. Node owns the detailed
[qualification review](node:docs/audits/REVIEW-SENSORIUM-P096-005-QUALIFIED-2026-10-28.md).


### Integration preparation without history integration — 2026-10-28

Prepare prospective resolutions against Node primary e8227589 and Orbidocs primary
1f98becc, preserving the exact-tuple P096-005 decision and all historical reports.
The primary documentation pseudonyms are applied to this documentary projection;
no retained evidence, qualifier, signature, digest or runtime host configuration
is changed. The combined producer remains unqualified. No merge or rebase occurs.
