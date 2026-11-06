# Proposal 078: Weak Signal Harvester

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`

## Status

Draft

## Date

2026-07-03

## Executive Summary

Orbiplex should define **Weak Signal Harvester** as a separate tool class for
discovering candidate weak signals in user-controlled corpora: documents, mail,
local notes, exported archives, and later explicitly configured network sources.

The Harvester is not Whisper and not a network protocol authority. It is an
upstream discovery tool. It scans allowed sources, groups and deduplicates
candidate findings, prepares redacted summaries, and writes them into a
host-visible **findings directory** on disk. The node then imports those findings
through a review surface. Only a user- or operator-approved finding may become a
Whisper draft or another node artifact.

The boundary is deliberately boring:

```text
documents / mail / configured sources
  -> Weak Signal Harvester
  -> findings directory on disk
  -> node import + review
  -> approved Whisper draft / local note / no action
```

The Harvester MAY later gain network protocols, but the MVP contract remains a
filesystem handoff. This keeps authority with the node, lets independent tools
innovate, and avoids granting a crawler or model helper direct publication power.

## Context and Problem Statement

Whisper (Proposal 013) defines the protocol layer for privacy-bounded weak social
signals. Monus describes local pattern noticing for wellbeing and tension signals.
Inquirium and Agent give the node bounded model-backed inquiry and orchestration.

What is missing is a practical intake bridge for weak signals that already exist
inside private or semi-private user material:

- repeated concerns in e-mail threads,
- similar complaints spread across many documents,
- emerging idea convergence in notes and drafts,
- recurring names of institutions, services, products, or events,
- weak evidence that several small anomalies may belong to one pattern.

If the user must notice and type every signal manually, Whisper intake becomes
too narrow. If a crawler or model helper can publish directly, the system becomes
unsafe. The missing middle is a tool that can discover candidates without
becoming an authority.

## Goals

- Define Weak Signal Harvester as an external or node-adjacent tool that produces
  candidate findings, not network artifacts.
- Use a disk findings directory as the first stable integration boundary.
- Require grouping, deduplication, source references, confidence, and redaction
  metadata before node import.
- Preserve raw user documents and mail locally; findings must carry references
  and digests rather than raw source copies by default.
- Require explicit review before a finding becomes a Whisper draft or outgoing
  signal.
- Leave room for later network-capable harvesters without making network access
  part of the MVP.

## Non-Goals

- Not a replacement for Whisper. Whisper starts after a finding has been reviewed
  and shaped into a social-signal draft.
- Not a hidden surveillance subsystem. The user or operator chooses source
  roots, mailboxes, schedules, and retention.
- Not an evidence engine. A finding is a candidate weak signal, not proof.
- Not a general search index for the node.
- Not an Inquirium adapter. The Harvester may call model inference through
  Inquirium, but source crawling, grouping, and finding emission are its own tool
  responsibilities.
- Not a direct publisher. The Harvester MUST NOT write Agora, Whisper, Memarium,
  or network artifacts directly in the MVP.

## Proposed Model

### 1. Tool boundary

The Harvester is a separate executable, package, or supervised module. It may be
installed and updated independently from the node. Its authority is bounded by
configuration:

- source roots and mailbox accounts it may read,
- source classes it may index,
- maximum scan size and cadence,
- redaction policy,
- model/inference profile if model assistance is enabled,
- output findings directory.

The Harvester may be implemented with ordinary filesystem/mail libraries, a
local search index, Inquirium calls, or an Agent-controlled workflow. Those are
implementation choices. The node-facing contract is the findings directory.

### 2. Findings directory handoff

The first stable handoff is a host-visible directory such as:

```text
<data-dir>/weak-signal-harvester/findings/
  incoming/
  accepted/
  rejected/
  archived/
```

MVP shape:

- the Harvester writes immutable finding files under `incoming/`,
- the node imports files by digest and moves or records them into a review read
  model,
- review actions mark findings accepted, rejected, archived, or converted to a
  Whisper draft,
- the Harvester never edits a finding after writing it; corrections are new
  finding revisions with `supersedes`.

The directory is a transport seam, not the source of truth. After import, the
node owns the review state and audit facts.

### 3. Candidate finding shape

The canonical schema is
[`weak-signal-finding.v1.schema.json`](../../schemas/weak-signal-finding.v1.schema.json).
The minimal semantic shape is:

```json
{
  "schema": "weak-signal-finding.v1",
  "finding/id": "finding:...",
  "created/at": "2026-07-03T00:00:00Z",
  "source/classes": ["mail", "document"],
  "signal/polarity": "problem",
  "topic/class": "workplace-retaliation",
  "finding/summary": "Several messages mention similar retaliation patterns after escalation.",
  "finding/confidence": "low",
  "finding/group-key": "sha256:...",
  "finding/supersedes": [],
  "source/refs": [
    {
      "source/ref": "mailbox:local:inbox#msg:...",
      "source/digest": "sha256:...",
      "source/snippet/redacted": "..."
    }
  ],
  "privacy/review-required": true,
  "suggested/actions": ["whisper-draft", "local-note", "ignore"]
}
```

Rules:

- raw source text is not copied by default;
- redacted snippets are bounded and optional;
- source refs are local references or opaque handles, not public identifiers;
- `finding/group-key` supports deduplication across repeated scans;
- `signal/polarity` uses Whisper's `problem` / `idea` vocabulary when the
  finding is intended for Whisper, but other downstream uses may define their
  own classifications later.

### 4. Grouping and deduplication

The Harvester should group duplicates before presenting findings. Grouping is a
local read-model, not a truth claim. A group may be based on:

- source digests,
- normalized topic/class,
- named entity clusters after redaction,
- temporal proximity,
- semantic similarity from a local or approved model profile,
- explicit operator merge/split corrections.

The user should see "one possible signal with N local references" rather than N
near-identical notifications.

### 5. Review and approval gate

Every imported finding remains local until the user or operator approves an
action. Possible review outcomes:

- **ignore**: no downstream artifact;
- **archive**: keep as local weak-signal note;
- **merge / split**: adjust grouping;
- **redact further**: prepare a safer summary;
- **create Whisper draft**: produce a local draft for Proposal 013 publication
  flow;
- **create assistance request**: future path into Proposal 077 when the user is
  asking for help rather than correlating a weak signal.

Approval of a finding is not approval to publish. It only authorizes the next
local draft or workflow step. Whisper still owns redaction, disclosure posture,
and publication approval.

#### MVP implementation decisions

The Node MVP implementation freezes these operational choices:

- `POST /v1/weak-signal-harvester/import` accepts either a direct
  `weak-signal-finding.v1` artifact or an operator wrapper carrying
  `finding` plus optional `import/source`; both paths enter the same
  schema-gated import function.
- `POST /v1/weak-signal-harvester/filesystem-text/import` reads only
  Markdown/text sources under `<data-dir>/weak-signal-harvester/sources`.
  The runtime canonicalizes the source root and candidate path before reading
  and rejects symlinks or other resolutions that escape the sources root.
- The filesystem adapter is intentionally redaction-light: it normalizes and
  bounds `source/snippet/redacted`, but it also sets `redaction-required`.
  Human/model redaction remains a later review or Whisper publication gate.
- For non-web findings, `accepted` review creates a local Whisper draft stub by
  default unless the operator request sets `create/whisper-draft = false`. The draft carries
  `publication/state = "not-published"` and has no publication authority.
- Repeating the same terminal review outcome is idempotent and returns a
  `review/no-op = true` receipt rather than mutating `reviewed/by` or
  `review/note`.
- Listing findings with an unknown `status` query value is rejected with
  `400 Bad Request`; empty result sets are reserved for valid statuses that
  currently have no rows.
- The status directories under `findings/{incoming,accepted,rejected,archived}`
  are convention markers and future export/materialization roots. The dedicated
  review store remains the source of truth in the MVP.

### P084-012b: explicit web review and local draft

The dedicated operator web review route extends the P084-012a local intake with
an immutable redaction decision and explicit local draft intent. It preserves
the original finding, classification and provenance; the new
`weak-signal-web-review.v1` fact binds the approved summary/topic/polarity and
reviewer/time to the exact finding digest. A false draft choice, rejection or
archival creates no draft. A true accepted choice creates only a local,
unpublished Whisper draft subject to the existing publication gate.

The canonical request, state machine, v3 migration, bounded fact/projection
recovery and compatibility rules are in
[P084, explicit web review](084-sensorium-web-observation-connector.md#132-p084-012b-explicit-web-review-and-local-draft).
In particular, web findings require the dedicated review endpoint, while non-web
findings retain the MVP review behavior. Review consumes already admitted local
evidence and neither reacquires P082 access nor initiates network acquisition.
Acceptance is recorded in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEWED-DRAFT-EVIDENCE.md`.
Broader P084-012 remains partial and P078-007 remains deferred.

### 6. Relationship to Whisper

Whisper remains the protocol for publishing, exchanging, correlating, and
thresholding weak social signals. The Harvester is only an upstream discovery
tool:

```text
Harvester finding -> local review -> Whisper draft -> Whisper publication gate
```

This separation prevents private source corpora from becoming network-facing
rumor buses. It also lets a deployment use the Harvester only for local notes
without enabling Whisper at all.

### 7. Relationship to Monus, Sensorium, Inquirium, and Agent

Monus is narrower: local wellbeing/tension pattern noticing and candidate
concern preparation. Weak Signal Harvester is broader: arbitrary configured
corpora and later configured network sources. Monus may be one producer of
findings, or it may consume Harvester findings when local policy allows it.

Sensorium may provide observations or connector outputs that become source
material, but Sensorium does not own the Harvester. Sensorium observes and acts
through bounded connectors; the Harvester indexes and groups configured corpora.
For changing web observations, [Proposal 084: Sensorium Web Observation Connector](084-sensorium-web-observation-connector.md)
owns bounded acquisition, provenance, and optional Sensorium Interface
publication. For carrier-neutral custody of exact portable artifact bytes,
[Proposal 088: Pull-Based Artifact Acquisition](088-pull-based-artifact-acquisition.md)
owns source orchestration, staging receipts, verification, and handoff to the
existing Artifact Delivery admission boundary. The Harvester may consume an
explicitly admitted P084 snapshot or P088-derived intake artifact, but it does
not inherit fetch, crawl, source-registration, or publication authority.

Inquirium may be used for classification, summarization, entity redaction,
semantic grouping and advisory epistemic analysis under
[P078-006](#inquirium-epistemic-analysis). Model output is a proposed interpretation,
not independent corroboration or a publication decision.

Agent may orchestrate a bounded harvesting pass: schedule scan, ask Inquirium to
cluster candidates, write findings, and stop. The Agent must not bypass source
grants, output directory policy, or review gates.

P084-012a narrows the first integration to an operator-selected, already admitted
snapshot on the same Node. Its immutable source configuration does not grant
read access; independent P082 admission and bounded retained-artifact verification
precede a classified, reference-only local review candidate. It creates neither
network acquisition nor a Whisper draft. The full P078-007 network-capable
profile remains deferred, including remote handoff and automated correlation.

### Inquirium-assisted epistemic analysis {#inquirium-epistemic-analysis}

Design refinement, 2026-11-04; implementation remains deferred under P078-006.
This opt-in profile consumes explicitly admitted source representations and
produces local analysis for review. It is not a prerequisite for P078-015/016,
P084-014/015 or P013-WEB-001/002: retention, origin propagation and manual review
must work with the profile disabled, absent or unavailable. Its web path consumes
those custody/origin contracts when applicable; it does not introduce another
acquisition or retention mechanism.

**Keep three records of meaning distinct.** The following are recommended logical
shapes to freeze in versioned contracts during implementation, not fields already
implemented in `weak-signal-finding.v1`:

| Layer | Minimum binding and content | What it does not establish |
|---|---|---|
| Source claim | `claim/ref`, admitted `source/ref`, exact representation digest and bounded fragment selector; quotation or explicitly labelled paraphrase | That the claim is true, first-hand or independent of another source. Model-extracted claims remain proposed extractions until checked against the fragment. |
| Model analysis | `analysis/ref`, input claim refs, question/profile revision, existing execution provenance ref, proposed classifications/inferences, supporting/contradicting refs, alternatives and gaps | Source authorship, verification of the event, independent corroboration, or permission to publish. |
| Human decision | Existing immutable review identity, reviewer, exact finding/analysis/input revision and accepted, amended or rejected interpretation | That accepting a summary proves the event or approves every model inference. Publication still requires its own gate. |

Source statements and model conclusions must remain separately inspectable. A
proposed relation such as supports, contradicts or provides context names its
target claim and basis; unverified relations remain advisory. The assistant may
present these layers and collect corrections, but cannot manufacture a review
fact on the user's behalf. Corrections create a new bound revision rather than
rewriting the source or the earlier analysis. A change to the accepted content
or analysis invalidates approval for that changed version.

For example, a retained article says that a person sent a document to an
institution. The source claim is "the article reports a sending", with its
fragment reference. A model may propose "possible administrative delay", while
recording that neither delivery nor the institution's response is evidenced.
The reviewer can accept the source summary and reject that inference. Three
reprints of the article do not become three independent accounts; where lineage
is unknown, independence remains unknown.

**Implementation recommendations and reuse.**

1. Start with `node:docs/development/reuse-index.v1.json` and verify the actual
   contracts of Harvester review/draft storage, P084 admitted representations,
   [P063 Inquirium](063-inquirium-model-inquiry-organ.md) requests and
   [P064](064-inquirium-implementation-recommendations.md) adapters, quality gates
   and execution provenance. Use an existing Inquirium request or bounded Flow
   for a single analysis. Use [P073 Agent](073-agent-orchestration-organ.md) only
   when bounded multi-step orchestration is needed; no Harvester model adapter,
   inference loop, review log or blob store is added in parallel.
2. Reuse [P066 Decision 8](066-inquirium-assistant-channel.md#decision-8-epistemic-posture-and-dignity)
   for `epistemic.stance`, `confidence`, `grounded_in` and `caveats`, preserving
   alternatives. This describes the model response's epistemic posture, not a
   probability that a source claim is true. Neither this confidence nor
   `finding/confidence` automatically changes rumor credibility, source counts,
   reputation or publication authority. Execution provenance records how the
   answer was produced, not whether its claim is correct.
3. Keep domain analysis as a bounded structured result validated through Schema
   Gate, referring to existing source and review identities. Verify every claimed
   fragment/ref against admitted inputs; fabricated or mismatched grounding is
   rejected, not repaired by fetching another source. Treat source text as
   untrusted data, including instructions embedded in web pages. Apply existing
   context, egress, privacy and token/time limits before dispatch; local source
   access does not authorize sending private text to a remote model.
4. Reuse owner-controlled source custody and derived-artifact lifecycle rules.
   Analysis does not extend source retention or make private refs public. Inspect
   availability at use time; expired or missing evidence is explicit and cannot
   be silently reacquired. Reuse the P013 reviewed origin projection to preserve
   `model-assisted` processing where applicable, without publishing private
   reasoning, prompts or input references by default.
5. Keep unavailable, refused, malformed and insufficient-evidence results
   distinct from "no concern found". Bound analysis size and retries through the
   existing quality contract. Failure leaves manual review available and cannot
   mark an unperformed analysis successful. Do not retry or raise limits silently.

**Acceptance for P078-006.** Extend existing Harvester and Inquirium harnesses;
do not build a separate acceptance runner or require a real model for structural
offline checks:

- With deterministic source fixtures and stubbed Inquirium responses, verify the
  three layers, exact input/fragment bindings, human amendment, stale-review
  refusal and replay without duplicate decisions or drafts.
- Cover contradiction, insufficient evidence, copied articles with shared
  lineage, unknown independence and conflicting interpretations. Confidence must
  not become truth probability or an additional corroborating source.
- Reject fabricated citations, out-of-range selectors, source-digest mismatch,
  authoritative/effect-bearing output and prompt-injection attempts. Check
  private-text canaries across model dispatch, review and public projection;
  no fetch or publication is triggered by an analysis response.
- Exercise timeout/refusal, malformed output, exhausted budgets and expired
  source access. With analysis disabled or failing, run the retention/origin
  handoff fixtures unchanged and prove manual review remains available.
- Qualify a concrete model/profile separately using P064's quality gate and a
  preregistered, human-labelled set of extraction, attribution, contradiction and
  abstention cases. Record per-case results and failure thresholds before the
  run; offline stubs prove integration, not semantic quality. Real model runs
  require separate explicit authorization. A failed calibration keeps that
  profile unavailable without blocking the retention slice.
- Close P078-006 only with contract/integration evidence and the explicitly
  scoped model/profile qualification; update the Node ledger and owning solution
  status without upgrading earlier reports. Record reuse decisions and any
  intentionally separate domain types in the closeout.

### Web source retention and origin {#web-source-retention-and-origin}

Adopted design extension, 2026-11-04; P078-015/016 remain `in-progress`. Web findings
intended for publication consume the original-backed profile in
[P084](084-sensorium-web-observation-connector.md#web-original-custody), including
its exact original byte boundary and finite custody claim. Harvester retains
references and review facts, not a second copy of HTML. Existing reference-only
intake remains useful for local review, but cannot claim this stronger profile.

At review, bind the original custody claim, snapshot/representation digests,
source classification, requested/effective retention horizon and origin summary
to the existing immutable finding/review identity. Recheck availability under
current read authority before issuing a publication-ready handoff. A missing,
expired or corrupt original leaves the candidate inspectable with that state,
but blocks promotion under this profile. Never refetch silently or infer
retention from an artifact reference. Changing source or extending retention
requires explicit owner action; exact review replay remains idempotent, while
current availability is a separate read projection.

Reuse `weak-signal-finding.v1`, the dedicated SQLite review owner,
`weak-signal-web-review.v1`, and the typed local draft serializer. Extend their
versioned contracts as necessary; do not add a second review log or overload
`source/classes` (currently `sensorium`/`document` for web intake) with publication semantics.
Local draft provenance can bind precise sources, but its publishable projection
carries only the independently reviewed origin summary specified by
[P013](013-whisper-social-signal-exchange.md#web-origin-publication). Selecting
"media monitoring" describes the approved collection purpose, not an inference
from the presence of an HTTP URL. Model assistance is another axis. Mixed-source
findings preserve their material origins rather than selecting one convenient
label; legacy/missing provenance remains explicitly unknown.

The operator sees the retained-original status, effective deadline, extracted
representation and proposed public origin label before approving a draft. Raw
HTML, full URLs, artifact refs and body digests stay private unless separately
approved for disclosure. A public origin label is not a read grant. Existing
urgent-protection paths remain available under their own contracts; unavailable
web custody must not prevent a person from reporting their own situation, but
that report cannot masquerade as an original-backed web finding.

Implementation starts with a reuse inventory of P084 acquisition/custody,
existing review/draft serialization, P091 configuration and the Whisper
publication gate. Share the pure origin validator/projection between these
consumers once its contract is frozen in P013; leave custody checks with P084
and review decisions with Harvester. Test body loss between import/review/publish,
clamped horizons, review replay after expiry, mixed and unknown origins, explicit
media-monitoring selection, model-assisted transformation and secret canaries.
Do not equate matching body digests with independent corroboration: local
source lineage may identify copied material, while different hashes alone prove
neither independent sources nor different claims.

### 8. Network-capable future

The proposal intentionally omits "local" from the name. Later harvesters may
scan configured remote sources or federated feeds, but the same boundary holds:

- network access must be explicitly configured and auditable,
- findings remain candidate facts,
- raw remote payload retention is policy-bound,
- publication still requires node-owned review and downstream protocol gates.

The filesystem findings seam remains useful even then: network-capable tools can
still deposit findings for node review without gaining node authority.

Generic web fetching and crawling are not Harvester mechanics. P084 owns the
web-observation connector and keeps crawling behind a separate deferred profile;
P078 owns only the later transformation from an admitted source representation
into a reviewable candidate finding.

### 9. Public Harvester Gateway

A public Harvester is a different profile from a source-indexing Harvester. The
canonical example is a web form for whistleblowers or external contributors where
a person can submit text and attach documents. This profile should be called a
**Public Harvester Gateway** or **Public Weak Signal Intake Gateway**.

The gateway is still upstream of Whisper. It accepts submissions and produces
candidate findings; it does not publish `whisper-signal.v1`, write public
Memarium facts, or route artifacts into the network by itself.

Flow:

```text
public web form / intake API
  -> submission quarantine
  -> malware / size / MIME / archive / metadata checks
  -> optional redaction and deduplication
  -> weak-signal finding candidate
  -> operator / reviewer queue
  -> accepted local finding
  -> optional Whisper draft
  -> optional Whisper publication
```

Public intake has a stronger threat model than local document/mail harvesting:

- the endpoint is reachable by strangers and therefore needs rate limits,
  captcha or proof-of-work where appropriate, abuse filtering, and upload quotas;
- every attachment enters quarantine before any parser, previewer, or model sees
  it;
- the gateway must defend against malware, zip bombs, misleading MIME types,
  oversized payloads, embedded tracking beacons, EXIF/location metadata, and
  accidental secret disclosure;
- the submission form must state that the channel is not an emergency service
  and does not guarantee immediate action;
- anonymous, pseudonymous, and contactable submission modes should be separate
  choices, not one confused identity mode;
- the submitter should receive a `submission/id` and optionally a separate
  status secret or receipt token for later follow-up without forcing civil
  identity disclosure;
- raw submissions and attachments stay in quarantine or a dedicated private
  custody space until a reviewer explicitly promotes a redacted finding.

The public gateway therefore has two outputs:

1. an immutable raw submission package in quarantine, governed by strict
   retention and access policy;
2. a redacted `weak-signal-finding.v1` candidate or refusal record for the node
   review queue.

The split is essential. A whistleblower submission may contain evidence,
personal data, trade secrets, privileged material, or dangerous files. The
Harvester finding should carry only the minimum summary, source refs, digests,
and review metadata needed to decide whether the material is correlation-worthy.

#### Collector-submitted corroboration

The API intake profile may also accept findings from organization-operated
collectors. In the recommended model, those collectors are run by an umbrella
organization to corroborate or contextualize phenomena that people have already
submitted or reviewers have already accepted as worth checking. They are not the
default mechanism for discovering "what society thinks".

Recommended flow:

```text
human-submitted weak signal
  -> reviewer accepts candidate phenomenon
  -> umbrella collector runs a bounded corroboration query
  -> collector submits corroboration finding
  -> reviewer/projection links it as supporting / contradicting / inconclusive
```

The collector-submitted finding should carry:

- `collector/id` and `operator/org-id`,
- `phenomenon/ref`, `finding/group-key`, or another reviewer-approved anchor,
- declared source scope and sampling method,
- query time window and budget,
- raw-source retention policy,
- result class: `supporting`, `contradicting`, `inconclusive`, or
  `context-only`,
- source refs, digests, bounded snippets, or aggregate indicators rather than
  unrestricted raw scraped content.

This mode should preserve the human-first epistemic boundary. A collector may
help answer "is there external public corroboration for this reported pattern?"
It should not automatically create a new phenomenon, raise a Whisper threshold,
or generate reputation effects. If a federation wants early public anomaly
scanning without a human/reviewer anchor, that is a separate, explicitly enabled
policy profile with a higher surveillance and abuse risk.

## Trade-offs

- A directory handoff is less elegant than a direct host capability, but it is
  simple, inspectable, language-neutral, and easy to sandbox.
- Requiring review slows automation, but prevents private mail and documents from
  becoming accidental gossip.
- Keeping the Harvester outside Whisper creates one more component, but preserves
  stratification: discovery, review, publication, and correlation stay separate.
- Grouping/deduplication may hide distinct cases if tuned too aggressively, so
  the UI must allow split/merge correction and preserve source refs.

## Failure Modes and Mitigations

| Failure | Risk | Mitigation |
|---|---|---|
| Harvester leaks raw mail/document content | Private source material becomes network-facing | Findings carry refs/digests and bounded redacted snippets; Whisper publication requires separate review. |
| Harvester publishes directly | Tool becomes hidden authority | MVP forbids direct writes to Agora/Whisper/Memarium/network surfaces. |
| Over-grouping hides distinct signals | User misses important differences | Grouping is a mutable local projection; review UI supports split and merge. |
| Under-grouping floods the user | Attention overload | `finding/group-key`, source digest grouping, and rate-limited review queues. |
| Model hallucination creates false findings | User sees invented patterns | Findings cite local source refs and confidence; model output is advisory only. |
| Network-capable harvester becomes crawler malware | Excessive egress and data collection | Network sources are explicit grants; output remains findings-only; audit scan scope and timing. |
| Public gateway accepts hostile attachments | Malware, parser exploits, zip bombs, or tracking payloads enter trusted tools | Quarantine first; scan size, MIME, archives, metadata, and malware before preview, model processing, or promotion. |
| Public submitter assumes emergency response | Harm escalates while waiting for review | Submission UI must state non-emergency scope and direct acute cases to local emergency channels. |
| Whistleblower identity leaks through metadata | Retaliation or deanonymization risk | Strip or warn on EXIF, document authors, mail headers, filenames, and other reconstructive metadata before finding promotion. |
| Umbrella collector becomes mass social surveillance | Organization turns corroboration tooling into a general population sonar | Collector runs should be anchored to accepted phenomena or reviewer-approved queries; unanchored public anomaly scanning requires a separate explicit policy profile. |

## Open Questions

No unresolved questions remain for this proposal's MVP contract.

1. ~~Should `weak-signal-finding.v1` be introduced immediately as a canonical
   schema, or should the first implementation use a documented JSONL shape and
   freeze the schema after one prototype?~~ **Resolved:** introduce
   `weak-signal-finding.v1` immediately as a canonical schema.
2. ~~Should node import watch a directory continuously, or should import be an
   explicit operator action in the MVP?~~ **Resolved:** MVP import is an
   explicit operator action. A continuous directory watch may be added later as
   an opt-in profile after the bounded import contract is stable.
3. ~~Should findings be imported into Memarium as local private facts, or should
   the node keep a dedicated Harvester review store until the user accepts an
   action?~~ **Resolved:** keep a dedicated Harvester review store first.
   Accepted/promoted findings may later write Memarium/private facts through an
   explicit user action.
4. ~~What is the first source adapter for acceptance testing: Maildir,
   filesystem Markdown/text, or exported mbox?~~ **Resolved:** filesystem
   Markdown/text is the first acceptance source adapter.
5. ~~Should a future network-capable Harvester use Artifact Delivery for remote
   source handoff, or remain outside node transport and only write local
   findings?~~ **Resolved:** a future network-capable Harvester may use
   Artifact Delivery for explicitly configured remote source handoff, preserving
   bounded/quarantined findings-only semantics.
6. ~~Should Public Harvester Gateway be a profile of this proposal, or should it
   become a separate proposal once quarantine, receipts, and reviewer workflow
   are ready for implementation?~~ **Resolved:** P078 defines only the hook
   shape. Public Harvester Gateway should become a separate proposal once
   quarantine, receipts, reviewer workflow, and redaction semantics are ready.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Task | Status | Notes |
|---|---|---|---|
| P078-001 | Define findings directory convention | done | Node creates `<data-dir>/weak-signal-harvester/findings/{incoming,accepted,rejected,archived}` plus a controlled `sources/` root; imported findings are digest-addressed and review state is node-owned. |
| P078-002 | Define `weak-signal-finding.v1` candidate schema | done | Canonical schema and positive/negative fixtures exist; schema-gate validates import/export and enforces source refs, group key, confidence, privacy flags, and mandatory review. |
| P078-003 | Node import and review read-model | done | Daemon exposes explicit operator import/list/detail/review endpoints backed by a dedicated SQLite Harvester review store; continuous directory watch remains a later opt-in profile. |
| P078-004 | Whisper draft handoff | done | Accepted findings can create a local `weak-signal-whisper-draft.local.v1` stub with `publication/state = not-published`; Whisper publication remains a separate approval gate. |
| P078-005 | First source adapter acceptance fixture | done | Filesystem Markdown/text import is the first adapter: it reads only under the configured Harvester `sources/` root, bounds source size/snippets, and emits schema-valid findings. |
| P078-006 | Inquirium-assisted grouping and epistemic analysis profile | deferred | Optional profile under [the analysis contract and acceptance](#inquirium-epistemic-analysis). Reuse P063/P064 inference, P066 epistemic posture, existing source bindings and immutable Harvester review; P073 orchestrates only when needed. Separate source claims, model inferences and human decisions; validate grounding and preserve uncertainty. Require offline boundary fixtures and separately authorized, calibrated model/profile evidence. Not a prerequisite for P078-015/016, P084-014/015 or P013-WEB-001/002; manual review and origin/retention handoff remain usable without it. |
| P078-007 | Network-capable Harvester profile | deferred | Future Artifact Delivery handoff for explicitly configured remote sources; P084 owns changing web observation, P088 owns carrier-neutral artifact custody, and P078 consumes only explicitly admitted snapshots or derived intake artifacts under findings-only, bounded/quarantined semantics. |
| P078-008 | Public Harvester Gateway profile | deferred | Separate future proposal for public web/API intake, attachment quarantine, receipt tokens, redacted finding promotion, and reviewer queue; P078 only keeps hook compatibility. |
| P078-009 | Collector-submitted corroboration profile | deferred | Umbrella-operated collectors submit supporting/contradicting/context findings anchored to accepted phenomena or reviewer-approved queries. |
| P078-010 | Memarium dormant-fact source profile | todo | Depends on P036-007 and a scoped `memarium.read` grant. A scheduled scan reads current personal records in rotating, budgeted batches with recall-oriented inclusion; it refuses expired or forgotten records and writes neither Memarium nor network artifacts. See [the profile](#memarium-dormant-fact-profile-2026-10-27). |
| P078-011 | Vocabulary generalization to a local interest profile | todo | Depends on P078-010 and P013-DFR-001. Rules first; an optional model may choose vocabulary ids only. Below-floor terms fall back to their parent. Output is `dormant-fact-interest-profile.local.v1`; a canary fixture proves that no record token, path or digest appears in it. |
| P078-012 | Local resonance scoring and link candidates | todo | Depends on P078-011, P013-DFR-002 and P036-008. Deterministic, explainable scores against the unnarrowed record projection; a configured threshold; `weak-signal-finding.v1` candidates that reference record and rumor; pair and context suppression; a per-epoch candidate cap. |
| P078-013 | Dormant-fact derived artifact lifecycle | todo | Depends on P036-006. Profiles, scores and candidates carry `derived-from` references, expire with their source and are purged on forget; review-store retention is bounded. |
| P078-014 | Authored rumors as dormant records | todo | Depends on P078-010 and P013-LLR-003. The dormant-fact profile also reads the participant's own authored rumors from Memarium, so a later twin can be matched for re-contact ([P013 long-lived rumors](013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship)). Authored-rumor matches produce findings for the author only; they never count as sources or re-publish the old record. |
| P078-015 | Bind retained originals and finite horizons to web review and draft handoff | in-progress | Depends on P084-014 and P013-WEB-001. Extend existing finding/review/local-draft contracts with exact custody bindings and reviewed public origin summary; preserve source/representation identity and classification. Current authority, availability, deadline and quota refusals block only this original-backed promotion; no raw-copy store or implicit refetch. Legacy drafts remain explicitly unqualified. |
| P078-016 | Qualify operator review and provenance handoff | in-progress | Depends on P078-015; feeds P084-015 and P013-WEB-002. Extend existing Harvester API/UI harnesses with retention deadline/status, mixed/unknown/media-monitoring labels, exact review replay, loss/expiry before publication and zero private-source leakage. Use deterministic offline sources and separately record UI evidence; synchronize Node ledger and owning solutions on implementation, without upgrading earlier reports. |

### Operator UI checkpoint (P084-012c)

P084-012c is done for the measured local operator UI scope. The web-finding
operator queue in node-ui composes the local review API without
adding intake or publication authority. The UI presents classification, provenance
and the bound digest before accepting operator redaction and explicit local draft
intent. The daemon owns immutable decisions; refresh reads committed state and
exact replay does not create another draft. Other source classes keep their
existing API review flow. See
[P084 operator UI](084-sensorium-web-observation-connector.md#133-p084-012c-operator-review-ui)
and `node:tools/acceptance/sensorium-web-review-ui/README.md` for acceptance.

## Memarium Dormant-Fact Profile (2026-10-27)

Planned continuation for
[P013 dormant-fact resonance](013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27),
exercised by [Story 014](../30-stories/story-014-dormant-contest-entry.md).
The profile keeps the Harvester boundary: it reads explicitly granted sources
and emits findings for review. It writes neither Memarium nor network
artifacts. The host records the participant's decisions
([P036-008](036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27)),
and Whisper performs the pulls (P013-DFR-002). This follows Resolved
Question 3: accepted findings reach Memarium only through an explicit user
action.

1. **Scan** (`P078-010`). A scheduled module job reads current personal
   records through `memarium.read` under an explicit grant, scoped to the
   record kinds the participant enabled. Batches rotate and are budgeted.
   Inclusion is recall-oriented: every current record is considered, and cheap
   rules only order the work.
2. **Generalize** (`P078-011`). Each record maps to term ids from the current
   decorrelation vocabulary. Rules come first. An optional local model may
   choose among ids, but its output is validated against the vocabulary and
   any free text is discarded. A term below the cardinality floor falls back
   to its parent. The output, `dormant-fact-interest-profile.local.v1`, is a
   derived local artifact that Whisper's pull plan consumes; it never leaves
   the node.
3. **Score** (`P078-012`). After a pull completes, the job scores pulled
   rumors from the local Whisper store against the unnarrowed record
   projection. Features include counterparty and named-entity overlap, event
   time against the rumor window, kind compatibility, title and facet tokens,
   and link domains. v1 is deterministic and explainable; model-assisted
   scoring stays with `P078-006` and embeddings with S022. A score above the
   configured threshold yields a `weak-signal-finding.v1` link candidate. Its
   source refs name the record and the rumor, and its group key is the rumor
   context. Rejected pairs and contexts are suppressed.
4. **Lifecycle** (`P078-013`). Profiles, scores and candidates carry
   `derived-from` references, expire with their source and are purged on
   forget.

## Next Actions

1. Consider other source classes separately before extending the operator review
   surface beyond the completed P084-012c admitted-web queue.
2. Decide whether a bounded directory-watch import profile is worth adding
   before public gateway work.
3. Keep network-capable and public gateway profiles deferred until their
   quarantine, receipt, and reviewer contracts are first-class.

### Notice-Only Dormant-Fact Match

The optional [P013-ADC-007 notice](013-whisper-social-signal-exchange/author-disclosure-conditions.md#optional-public-notice)
is a separate public record. A finding preserves its public record/id and closed
target kind (`whisper-correlation-notice` rather than `whisper-signal`), plus the
permitted grouping key. P078-012 and P013-DFR-004 qualify a reader who has only the
notice: acceptance authors a related signal targeting that notice without
fetching, guessing or publishing any protected signal id. A finding remains a
local proposal; the author still confirms both the link and new publication.

## Common reviewed v3 publication contract (2026-11-05)

All new Harvester decisions use `weak-signal-review.v1`; accepted decisions carry
explicit redacted summary, topic and polarity. Rejected/archived decisions carry
neither redaction nor a draft. Actor identity comes from authenticated local
operator admission. Historical web reviews/drafts retain their bytes and decoder;
they cannot become v3 publication evidence without a new common review.

A review binds one primary finding and up to fifteen additional admitted findings
as a canonical semantic set, with every immutable finding digest. This admits a
mixed inventory without mutating old findings. The owner, never request metadata,
derives origin and collects at most thirty-two exact original/representation
claim bindings. Web classification requires the independently admitted P084
binding. Missing collection/processing grounds remain unknown/empty. Material
coverage concerns that private reviewed inventory, not independent corroboration.

`expected/review-revision` provides the projection CAS. Idempotency binds the
normalized request, exact material inventory and current claim generations;
review time is the first committed owner observation. New extension generations
need a new review. A committed replay does not renew custody. Request size is at
most 24 KiB, decision size at most 64 KiB, with at most 4096 decisions. Capacity
and host storage/corruption remain distinct from malformed input. These limits
are checked before SQLite effects. Facts and projections use the existing review
store, not a source-acquisition journal.

Only `weak-signal-whisper-draft.local.v2` feeds the new protected authoring
profile. It carries the exact review reference/digest, origin and private claim
requirements, with derived-local author posture. Publication parameters remain
an explicit later review; neither raw findings nor HTML become publishable text.
A queue shows and sorts by the nearest required claim deadline (no-deadline
findings last). Expiry before review marks the web ingredient unpublishable;
only a new observation and review can proceed. Explicit extension is available
before expiry, never automatic revival. Implementation and composed acceptance
remain in progress.

### Actual expiry and new-review qualification checkpoint (2026-11-06)

The real-clock local fixture now verifies W7 with a live successful control review
and a second unreviewed finding on the same initial material. After expiry, the
latter remains without decision/draft across actual restart and receives a typed
custody conflict. Only an explicitly acquired new generation/snapshot with new
claims, source-slot supersession, grant and common review succeeds. No implicit
fetch or retention renewal occurs; the queue retains the old unpublishable item.

This supplies two scoped retention requirements within the current 18/131
campaign checkpoint (113 missing), alongside fresh review/component and original
native prerequisites. P078-015/016 and composed signed publication remain in
progress. The five-second fixture adoption does not change factory 24-hour terms.
Measured pins, original HTTP/owner-image bindings and refusal controls are owned by
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-EXPIRY-CAMPAIGN-20261106.md`.

### Issuer authority continuation (2026-11-06)

Strict encrypted-media and native provider checks are prerequisites, not Gate
A/B. Three separately approved one-shot attempts respectively missed the fixed
start cutoff, refused an unadmitted AD outbound scope, and reached full request
v2 before D refused consent. No terminal certificate, decision export or signed
Whisper was observed. The corrected shared path requires a separately
root-approved `nym-bootstrap-consent-v2`; original signed v1 grants retain their
four-family scope. Component/schema tests cover the separation, while a new
ordinary exchange and the signed two-backend campaign remain open.

The earlier 18/131 result retains its historical source pins. New runtime/schema
bytes require fresh native/source campaign admission, not an implicit bridge or
repin. Existing P084-014/015 and P078-015/016 status stays in progress; no
production adoption follows. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ISSUER-AUTHORITY-20261106.md`.

### First ordinary v3 certificate checkpoint (2026-11-06)

A fresh ordinary encrypted-owner fixture has issued a v3 certificate over all
four exact TLS/AD phases using separately signed bootstrap-v2 authority.
Independent native inspection verifies `A/issue` and `A/reference-readback`.
Together with fresh same-source R/C/W7/native inputs, the campaign is now
20/131 verified with 111 missing; ordinary/optimized results agree. Original
reports/refusals remain preserved, with process inventory added only in a
separately bound derived view. No Whisper was signed or published.

A separate 128 MiB capacity observation stopped after 2479 retains with an
untyped host cause; a complete DB/WAL copy passes integrity checks. It grants
no load/recovery credit. Full signed SQLite/Synapse, all-producer window-end,
recipient/privacy and remaining load/fault qualification remains open. Existing
P084/P078 and dependent owner trackers stay in progress. This does not adopt
production or renew historical evidence. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-FIRST-ISSUANCE-20261106.md`.

### Local reviewed-v3 producer preparation (2026-11-06)

The current UI fixture selects the applicant's local review/custody owner for
first v3 publication; receiving C remains a separate carrier/admission claim.
The inspector rejects a remote-owner process topology. Inline v2 keeps its
historical topology. Three actual applicants retain mixed reviews after exactly
three explicit controlled fetches and paused schedules. A separate 4096-claim
saturation/reopen observation is not campaign load qualification. None of this
adds to the source-bound 20/131 checkpoint or completes signed Gate A/B. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-LOCAL-PRODUCER-PREPARATION-20261106.md`.

### Ordinary UI continuation refusal (2026-11-06)

A later approved SQLite series issued A's v3 certificate and retained its two
exact recovery exports, then stopped on a capture-tool `UnboundLocalError` after
the first UI form. B/A2 did not start and no Whisper was signed or published.
Node corrected the local name shadowing and added complete doubled v2/v3 UI
orchestration regressions on both backends; 516 Python and 21 optimized UI tests
pass. The original runtime refusal remains preserved and adds no campaign credit.
Fresh corrected-source UI, common receiver and full A/B qualification remain open.
See `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ORDINARY-UI-REFUSAL-20261106.md`.


### Scoped reviewed v3 SQLite publication (2026-11-06)

The next independently inspected A fixture completes reviewed v3 signing and a
signed local SQLite publication receipt. The distinct source-bound aggregate is
16/131, with failed fresh C and stopped B expiry retaining their missing rows;
A2, Matrix, shared receiver and full remote privacy qualification remain open.
The provider-lock correction requires fresh clean-source qualification. See the
P084 scoped-publication checkpoint and
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-SQLITE-PUBLICATION-20261106.md`.


### Two verified local reviewed publishers (2026-11-06)

The next independently inspected A/B SQLite publications and fresh prerequisites
reach a source-bound 22/131, with 109 missing and identical normal/optimized
incomplete results. A2's second issue is refused; the positive replica path needs
same-context predecessor-bound renew. The explicit derived epoch-selector
correction preserves original refusals. Common receiver/threshold, Matrix, remote
privacy and full A/B remain open. See P084 and
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-TWO-PUBLISHERS-20261106.md`.


### Independent reviewed-v3 Matrix receiver preparation (2026-11-06)

Owned Synapse preparation observes healthy admitted A/B producer instances and a
separate C receiver, with existing local instances and signer defaults preserved.
It performs no certification, recovery export or Whisper publication. The shared
first-pair reader now binds each reviewed-v3 producer's custody/publication
process independently of the original C/D projection continuation. Both producers
must use the same issuer D; C must differ from each producer and from D. Inline
v2 bindings and all native complete-basis, first-pair, public-readback and expiry
requirements remain unchanged. Mixed-version and substitution tests do not award
runtime credit. Matrix, common-receiver/threshold and full A/B qualification stay
open; the preceding source-bound two-publisher report is unchanged.


### First reviewed Matrix publication and status-cache withdrawal (2026-11-06)

The source-bound Sensorium fixture independently verifies A's private AD
certificate, reviewed protected v3 UI signing and Matrix HTTP 202/public readback.
Its separately pinned campaign reaches 21/131, with 110 missing and identical
ordinary/optimized results. B fails startup before export: status-cache compaction
requires a formerly adopted profile absent from current configuration. C is
reaped; no common-receiver, threshold, complete-PDU or full A/B credit follows.
The earlier SQLite 22/131 retains its separate source and result.

The owner correction validates retained canonical bytes, digest and source links
before withholding unadopted status. It preserves facts and existing budgets,
refuses current use without adoption and restores signature/cursor verification
only on exact readoption. Other adopted profiles can operate and missing
projections can rebuild; corruption remains a refusal. Component regressions
pass and the next v3 conformance selection requires both withdrawal/corruption
assertions. Fresh current-source native/runtime and Matrix qualification remain
open; no historical gate or production adoption is renewed. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-FIRST-MATRIX-PUBLICATION-20261106.md`
and `node:daemon/docs/CONTEXTUAL-NYM-CERTIFICATION.md`.


### Scoped reviewed-v3 Matrix first pair (2026-11-07)

Both ordinary Harvester producers completed common mixed-material review,
protected v3 signing and publication at their own custody owners. C independently
received and aggregated them, and a fourth account observed all four exact PDUs.
Expiry is checked against the owner's independently reverified current evaluation;
unchanged membership history retains its original time. P078-015/016 and remaining
origin, recipient/privacy and two-backend qualification stay in progress.

The independently composed campaign verifies **25/131**, with **106 missing**,
and identical ordinary/optimized incomplete results. Runtime/capture Node
`985964ee83` / Orbidocs `2b5ea4fd` and corrected reader Node `d83a9a0f` remain
separately pinned. Both original reader refusals and every source observation are
preserved; no certification/publication retry, production adoption or historical
gate renewal follows. Current implementation evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-MATRIX-FIRST-PAIR-20261107.md`.
