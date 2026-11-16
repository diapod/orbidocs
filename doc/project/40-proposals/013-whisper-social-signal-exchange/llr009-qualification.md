# LLR-009 qualification contract

Status: accepted implementation contract, 2026-11-16. Runtime qualification is
pending. The LLR-009 tracker remains todo until all required gates pass.

## Claims and authority

The independently admitted controller selects trust, evaluation time and the
run mode. A capsule supplies exact proof bytes and provenance, never trust.
`portable/independent` requires `IndependentlyVerified` registration reliance.
`authority-attested` is a separate verdict for explicit operator-enabled
`AuthorityAttested`; it cannot satisfy or contribute to the independent verdict.
ReceiptProfile, WitnessSourceUse and RegistrationReliance retain their existing
meanings. Matrix server keys require separate local admission.

The single matrix is `node:tools/acceptance/case-continuity/llr009-profile.json`.
Development execution, formal execution and qualification consume its exact
rows. Required negative rows cannot disappear from a selected campaign.

## Work and byte boundaries

Presentation work includes every carried or exact-store-resolved presentation
role and is at most 32 signature checks. Recipient-local observations have a
separate finite role table, derived from CaseKnowledge's existing input bounds,
and a distinct LocalWork type. Total work is at most 32 + LOCAL_WORK_MAX.
Verified persisted knowledge needs no repeated signature check only when the
owner establishes its checked provenance and store integrity. Imported bytes or
an external verified flag cannot manufacture that provenance. Time, scope,
current trust, fencing and terminal-state checks still apply.

Negative and terminal knowledge precedes positive freshness. Local exhaustion
blocks continue-case with local-knowledge-limit, preserving already verified
negative facts and separately reportable history. Report presentation/work and
local/work independently; the same presentation has the same presentation/work
at recipients with different knowledge.

V1 remains 2740 KiB unique decoded bytes. V2 counts occurrences and may use a
role-derived 2996 KiB bound (2740 + the 256 KiB aggregate source allowance).
Before activation, D23 must establish which source bytes are necessary, including
unavoidable author bytes inside signed Matrix PDUs; signed objects are never
trimmed. D24 must measure actual carried JSON, plaintext and sealed PEX output.
4 MiB carried, 64 KiB referenced, 5 MiB sealed and depth 16 remain fixed.
If encoding exceeds these limits, retain the old decoded bound and explicitly
qualify non-composable role maxima with presentation-decoded-limit refusal.
Const assertions bind versioned sums and per-element base64/JSON overhead.
Structural maximum vectors do not claim semantic acceptance of contradictory
closures. Real legal maximum proofs and structural capacity are separate tests.

## Registration reliance

| Saved basis | Allowed next basis |
| --- | --- |
| none | Attested only for Unproven with explicit policy; Verified for complete proof; Refuted for Before |
| AuthorityAttested | same, Verified, Refuted |
| IndependentlyVerified | same or Refuted, never Attested |
| IndependentlyRefuted | Refuted only |

Operator policy authority_attested_basis defaults to false. Turning it off
requires independent readmission of a saved attested basis before another
current effect. Freshness expiry does not undo historical Verified admission.
Before is sticky even against a fresh active authority status and across restart.
Every result, saved decision and qualifier observation reports reliance.

## Rehearsal, formal capture and retention

Use the existing cold receiver driver and qualification/archive mechanisms with
profile data, not another driver family. A controller-admitted development run
executes the complete matrix, including negative, restart, retention, maximum,
mutation and temporary extraction checks, but can never qualify. It defers formal
hash inventories, retained logging and replicas; protocol integrity still applies.
Only after the full rehearsal and review pass on the final clean candidate may a
new formal campaign start with empty recipient stores. Relabeling development
output is rejected. A failed formal run retains its own diagnostic outcome.

Copy a self-contained exact subset of LLR-012 source inputs, retaining original
digests and provenance; trust is independently supplied. Controlled times refer
to preserved observations, not present-day validity. A copied subset must include
every authority asset necessary to interpret its dependencies.

Replay/import never renew payload, case or proof horizons. source_payload_refs
remain distinct from non-payload decision dependencies. Proof holds cannot extend
private payload retention. Missing exact local references remain unresolved.
Read current RETENTION/RETIREMENT/EXTERNAL-RETENTION before designation; record
owner, classification, inventory/hashes, dependencies/holds, minimum retention,
reconstruction and replica facts, retaining unknowns. Work/cache/evidence roots
are separate. Historical capsules are immutable.

## Gates and completion

A: contracts, matrix and resolver. B: full receipt/SQLite/Matrix offline.
C: detached offline without the private signal. D: time, negative knowledge,
reliance transitions, restart and retention. E: byte/work maxima and privacy.
F: independent qualifier mutations, extracted equivalence and scoped regressions.
B/C require actual macOS sandbox-exec denial (deprecated), a negative probe and
adapter counters. No Linux claim follows without a separate executed profile.

Review and repair after each stage; source and evidence/status commits remain
separate on codex/self-contained-signatures, without primary integration or push.
Convergence review includes the harness and existing P032 contract-law fixtures.
P015-005, P015-011, PEX-002, ADC, context transitions and release readiness remain
outside this qualification.
