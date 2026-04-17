# Proposal 039: Crisis Space Seed v1

Based on:
- `doc/normative/20-vision/en/VISION.en.md` (escape kit)
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. IX.7)
- `doc/project/40-proposals/036-memarium.md` (crisis space obligations)
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md` (`key_ref` taxonomy)
- `doc/project/60-solutions/memarium.md` (Crisis Space Management)

## Status

Signed off for implementation.

The constitutional-content review is recorded in
`doc/project/40-proposals/039-crisis-space-seed-v1-review.md`.

## Date

2026-04-16

## Executive Summary

Memarium's crisis space is a constitutional escape-kit surface: it should be
available on a fresh Node from the first second after `daemon.start()`, even
when the network, federation, or external coordination channels are degraded,
and even before any operator unlock has occurred.

This proposal defines the review candidate for the first crisis seed bundle:
six small, operator-readable entries that cover infrastructure failure,
identity recovery, abuse disclosure, emergency contacts, the constitutional
basis, and cold-start restoration.

The seed is local, encrypted, append-only, and node-held. It uses the Node AEAD
key (see Proposal 038 amendment), which is available to the Node process
without operator unlock because the seed content carries no operator secrets
the Node must hide from its own process. Operator-entered crisis material
(recovery phrases, private contacts, other operator secrets) is a separate,
deferred surface that uses an operator-held AEAD key and remains sealer-unlock-
gated.

The seed is not fetched from Seed Directory, not shared as public material,
and not editable in place. Future revisions add new entries and marker facts
instead of mutating or deleting old ones.

The crisis space also hosts autonomic crisis facts written by node-side
detectors (federation availability, sealer readiness, revocation view
freshness, storage integrity). Those facts use the same Node AEAD key as the
seed. See the "Autonomous Crisis Facts" section below.

## Context and Problem Statement

Proposal 036 defines four Memarium spaces: personal, community, public, and
crisis. The crisis space has mandatory encryption, constitutional-minimum
retention, and restricted forget semantics. The Node implementation already has
the space and policy boundary, but a fresh Node starts with an empty crisis
space.

That leaves a gap in the intended "escape kit" model from the vision document:
the operator has the mechanism, but no first-start minimum content to use under
pressure.

The missing artifact is not primarily code. It is a reviewed constitutional
content bundle whose presence in the binary is deliberate and auditable.

## Proposed Model / Decision

### Seed Bundle Contract

The crisis seed bundle is a versioned value:

```text
version: 1
entries: [CrisisSeedEntryTemplate]
signature: none
```

For v1, trust is implicit in the reviewed Node binary. A future file-loaded seed
bundle may require detached signature verification, but that authority model is
out of scope for this proposal.

Each entry has:

- `seed_entry_id`: stable identifier used for idempotence and additive upgrades,
- `artifact_kind`: Memarium entry kind,
- `tags`: reviewable classification tags,
- `content_json`: operator-facing JSON content to be sealed into the crisis
  space.

The implementation writes a marker fact:

```text
fact_kind: constitutional-seed-applied
fields:
  version
  bundle_digest
  applied_at
  entries_written
  entries_skipped_existing
```

### Encryption Key Alias

Crisis seed entries use the Node AEAD key:

```text
key:node:self:epoch:1:aead
```

Rationale: the constitutional seed is produced by the Node itself, contains no
secrets the Node must hide from its own process, and must be available
immediately after `daemon.start()` to satisfy the constitutional obligation
that a fresh Node expose its crisis material without operator intervention.
Gating seed application on operator unlock would leave a crashed or abandoned
Node with an empty crisis space.

Autonomic crisis facts written by node-side detectors (see "Autonomous Crisis
Facts" below) use the same Node AEAD key for the same reason.

Operator-entered crisis notes — a separate, deferred surface — use a distinct
operator-held AEAD key:

```text
key:operator:crisis:memarium:epoch:1:aead
```

That key is sealer-unlock-gated. It keeps operator secrets (personal recovery
phrases, private contact details, sensitive recovery material) out of reach of
any process that runs without operator consent.

The crisis space therefore hosts two writer classes with two key roles under
one policy envelope (encryption required, retention constitutional, forget
restricted). Sealer core treats both references as opaque; only the operator
vocabulary and the Proposal 038 taxonomy distinguish them.

### Candidate Seed Entries

The v1 bundle contains six entries.

#### 1. Federation-Failure Recovery

```json
{
  "title": "Federation-failure recovery",
  "summary": "Restore useful local operation when federation, Seed Directory, or peer discovery is unavailable.",
  "procedure": [
    "Switch the Node to local-first operation and stop waiting for remote capability discovery.",
    "Inspect local daemon status, storage health, sealer unlock status, and Memarium crisis-space availability.",
    "Prefer locally cached procedures, contacts, maps, and signed records over unverified network responses.",
    "Record the incident timeline locally before attempting federation repair.",
    "When connectivity returns, reconcile only signed and source-attributed records."
  ],
  "limits": [
    "Do not treat network silence as evidence of participant consent, revocation, or safety.",
    "Do not publish crisis material to federation by default."
  ],
  "operator_prompt": "What minimum local services are still working, and what must remain offline until trust is restored?"
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:federation-failure-recovery
artifact_kind: crisis-procedure
tags: constitutional, escape-kit, federation, recovery, procedure
```

#### 2. Identity-Loss Recovery

```json
{
  "title": "Identity-loss recovery",
  "summary": "Recover operational continuity after suspected loss, lockout, or compromise of local identity material.",
  "procedure": [
    "Stop automated publication and remote capability issuance until the identity state is understood.",
    "Check whether the participant recovery seed, node identity backup, or operator binding bundle is available.",
    "Prefer recovery paths that preserve audit history over ad-hoc identity replacement.",
    "If compromise is plausible, prepare revocation or supersession artifacts before reconnecting broadly.",
    "Document which keys, devices, backups, and operator actions were involved."
  ],
  "limits": [
    "Do not silently create a new primary identity and continue as if continuity were proven.",
    "Do not disclose recovery material to helpers without a separate minimal-disclosure decision."
  ],
  "operator_prompt": "Is this a lockout, suspected compromise, device loss, or uncertain state?"
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:identity-loss-recovery
artifact_kind: crisis-procedure
tags: constitutional, escape-kit, identity, recovery, procedure
```

#### 3. Abuse-Disclosure Protocol Pointer

```json
{
  "title": "Abuse-disclosure protocol pointer",
  "summary": "Keep crisis disclosure decisions procedural, minimal, and evidence-bound.",
  "procedure": [
    "Separate immediate safety needs from disclosure or attribution decisions.",
    "Preserve evidence without widening access to private or root-identity material.",
    "Use the Abuse Disclosure Protocol thresholds before escalating identity disclosure.",
    "Prefer the smallest disclosure scope that can protect people and preserve due process.",
    "Record the basis, stake level, evidence level, and reviewers involved."
  ],
  "references": [
    "doc/normative/50-constitutional-ops/en/ABUSE-DISCLOSURE-PROTOCOL.en.md",
    "doc/normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md"
  ],
  "limits": [
    "Do not use emergency language to bypass evidence thresholds.",
    "Do not expose root identity as a convenience shortcut."
  ]
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:abuse-disclosure-protocol-pointer
artifact_kind: constitutional-reference
tags: constitutional, escape-kit, abuse-disclosure, minimal-disclosure, reference
```

#### 4. Emergency Contact Placeholder

```json
{
  "title": "Emergency contact placeholder",
  "summary": "A local placeholder reminding the operator to add concrete crisis contacts after first start.",
  "contacts": [
    {
      "role": "constitutional-review",
      "name": "TODO: add trusted constitutional reviewer",
      "channel": "TODO: add offline-reachable channel",
      "notes": "Use for governance or high-stakes procedural review, not for immediate medical or legal emergencies."
    },
    {
      "role": "local-support",
      "name": "TODO: add local trusted contact",
      "channel": "TODO: add phone or offline channel",
      "notes": "Use for practical support when network/federation channels fail."
    }
  ],
  "operator_prompt": "Replace this placeholder with real local contacts before relying on the crisis space."
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:emergency-contact-placeholder
artifact_kind: emergency-contact
tags: constitutional, escape-kit, contact, placeholder
```

#### 5. Constitutional Basis Reference

```json
{
  "title": "Constitutional basis for crisis space",
  "summary": "Crisis memory exists to protect people while respecting privacy and procedural limits.",
  "basis": [
    "A Node should preserve operation under partial isolation, blackout, network constraints, or center failure.",
    "Memarium may maintain crisis spaces and emergency caches if they serve to protect people and remain consistent with privacy rules.",
    "Lawful rescue scenarios may include shelter, food, legal, medical, and operational triage, without pretending to possess competences the system does not have."
  ],
  "references": [
    "doc/normative/40-constitution/en/CONSTITUTION.en.md",
    "doc/normative/20-vision/en/VISION.en.md"
  ]
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:constitutional-basis-reference
artifact_kind: constitutional-reference
tags: constitutional, escape-kit, crisis-space, reference
```

#### 6. Cold-Start Checklist

```json
{
  "title": "Cold-start checklist",
  "summary": "Bring a Node back to a minimally useful local state from backup or fresh install.",
  "procedure": [
    "Verify the binary or package source before importing local identity or recovery material.",
    "Restore storage from the most recent trusted local backup, if one exists.",
    "Unlock the sealer master only after confirming that the local data directory and operator environment are expected.",
    "Confirm that Memarium crisis space contains seed entries and a constitutional-seed-applied marker fact.",
    "Keep federation disabled until identity, revocation view freshness, and local audit surfaces are inspected.",
    "Record what was restored, what was missing, and what remains untrusted."
  ],
  "limits": [
    "Do not import unknown sealed envelopes as trusted crisis material.",
    "Do not treat a successful boot as proof that restored data is current."
  ]
}
```

Metadata:

```text
seed_entry_id: crisis-seed:v1:cold-start-checklist
artifact_kind: recovery-instruction
tags: constitutional, escape-kit, cold-start, backup, recovery
```

### Autonomous Crisis Facts

The crisis space is not only a seed store. A Node that detects its own
constitutional degradation writes crisis facts to the same space, using the
same Node AEAD key.

Four node-side detectors are in scope for v1:

| Detector | Condition | Fact shape |
| --- | --- | --- |
| federation-unavailable | zero active SD peers for > 30 min AND SD poll failure > 15 min | `fact_kind = "crisis-detected"`, `fields.detector = "federation-unavailable"` |
| sealer-operator-unavailable | uptime since start without first unlock > 6 h, or time since last re-lock > 6 h | `fact_kind = "crisis-detected"`, `fields.detector = "sealer-operator-unavailable"` |
| revocation-freshness-stale | freshness budget exceeded per capability-binding revocation view | `fact_kind = "crisis-detected"`, `fields.detector = "revocation-freshness-stale"` |
| storage-integrity-warning | commit-log anomaly count > 0 in the most recent scan | `fact_kind = "crisis-detected"`, `fields.detector = "storage-integrity-warning"` |

Detectors are edge-triggered: they write a detected fact on the false-to-true
transition of their condition and a resolved fact on the true-to-false
transition. Resolution uses `fact_kind = "crisis-resolved"`,
`fields.detector = <detector>`, and tags such as `autodetected` or
`operator-forced`. Detector state is reconstructed on daemon start by querying
the latest detected/resolved facts per detector id.

Operator-forced close is available through a separate Memarium capability
(`memarium.crisis_resolve`, A0), which writes an append-only
`crisis-resolved` fact with `fields.detector = <detector>` and an
`operator-forced` tag even if the underlying condition has not opened. The
resolution cause is distinguished by fields/tags while keeping the fact-kind
vocabulary small and queryable.

Thresholds listed above are defaults configurable per-Node and may be adjusted
by operator without breaking the fact vocabulary.

## Trade-offs

Benefits:

- A fresh Node gains a minimal crisis-space baseline without network access.
- The seed content is reviewable before implementation embeds it.
- Entries are small enough for operator reading under pressure.
- The model stays append-only and compatible with crisis restricted-forget
  semantics.

Risks and constraints:

- English-only v1 is not sufficient for every operator context.
- Placeholder contacts are not useful until the operator replaces or supplements
  them with real local contacts.
- Compile-time seed content requires a Node release to fix wording.
- The seed can guide procedure, but it cannot provide professional medical,
  legal, or psychological advice.

## Failure Modes and Mitigations

| Failure mode | Impact | Mitigation |
| --- | --- | --- |
| Seed content changes without version bump | Digest mismatch and operator confusion | Implementation refuses same-version digest mismatch and requires a new bundle version |
| Node AEAD key backend not yet initialized at first start | Seed cannot be sealed | Node AEAD backend initializes on first touch before `apply_crisis_seed`; daemon start fails loudly if initialization fails, rather than silently skipping |
| Partial write during first apply | Some entries exist without marker | Retry skips existing `seed_entry_id` values and writes the marker only after full success |
| Placeholder contacts stay unedited | Operator lacks actionable human contacts | Entry explicitly tells the operator to replace placeholders after first start |
| Seed content is treated as professional advice | Misuse under pressure | Entries use procedural prompts and limits, not professional diagnosis or legal instruction |
| Detector emits duplicate `crisis-detected` after crash-restart while condition still holds | Two identical facts in audit | Acceptable under append-only semantics; `memarium.crisis_status` read path deduplicates by `fields.detector` when composing the active-findings snapshot |
| Operator-forced resolve closes finding while underlying condition persists | Autodetector would re-detect | Detector re-evaluation after operator-forced resolve does not re-fire until a full true→false→true cycle of its condition; operator reason is preserved in audit |

## Open Questions

1. Who gives final constitutional-content sign-off for this v1 bundle?
2. Should v2 add Polish-language entries with separate `seed_entry_id` suffixes
   such as `:pl`, or should localization wait for a UI-level display layer?
3. Should the emergency-contact placeholder be accompanied by a first-run UI or
   CLI reminder to add real contacts?
4. Should future seed bundles be signed detached JSON files, and if so which
   authority signs them?
5. Does the operator require per-Node threshold overrides for autonomous
   detectors stored as configuration, or is a compiled-in default sufficient
   for v1?
6. Should `crisis-resolved` operator-forced facts expose richer operator
   rationale structure beyond the mandatory reason string and audit subject?

## Next Actions

1. Review the six candidate entries for content, tone, safety, and constitutional
   fit.
2. Record explicit sign-off or requested edits in this proposal.
3. After sign-off, embed the reviewed v1 bundle into
   `node:memarium-runtime/src/bootstrap/seed_v1.rs` and
   `node:memarium-runtime/src/bootstrap/seed_v1/*.json`.
4. Implement the daemon bootstrap task that applies the seed synchronously in
   `Daemon::start()` before `DaemonPhase::Running` is set, using the Node AEAD
   key (no operator unlock required).
5. Coordinate with the Proposal 038 amendment that introduces the Node AEAD Key
   role (`key:node:self:epoch:<n>:aead`).
6. Scope the four v1 detectors, their thresholds, and the autonomous fact
   vocabulary (`crisis-detected` / `crisis-resolved` with
   `fields.detector`) alongside seed sign-off.
7. Scope the two Memarium host capabilities implied by this proposal:
   `memarium.crisis_status` (A1, snapshot read) and `memarium.crisis_resolve`
   (A0, operator-forced close).
