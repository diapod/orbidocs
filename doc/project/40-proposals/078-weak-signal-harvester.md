# Proposal 078: Weak Signal Harvester

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
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

The eventual schema should be `weak-signal-finding.v1`. The minimal semantic
shape is:

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

Inquirium may be used for classification, summarization, entity redaction, and
semantic grouping, but model output is evidence only. Inquirium does not choose
publication.

Agent may orchestrate a bounded harvesting pass: schedule scan, ask Inquirium to
cluster candidates, write findings, and stop. The Agent must not bypass source
grants, output directory policy, or review gates.

### 8. Network-capable future

The proposal intentionally omits "local" from the name. Later harvesters may
scan configured remote sources or federated feeds, but the same boundary holds:

- network access must be explicitly configured and auditable,
- findings remain candidate facts,
- raw remote payload retention is policy-bound,
- publication still requires node-owned review and downstream protocol gates.

The filesystem findings seam remains useful even then: network-capable tools can
still deposit findings for node review without gaining node authority.

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
| P078-001 | Define findings directory convention | todo | Include incoming/accepted/rejected/archive semantics, immutable write rule, and import digest behavior. |
| P078-002 | Define `weak-signal-finding.v1` candidate schema | todo | Introduce immediately as a canonical schema; must include source refs, group key, confidence, and privacy flags. |
| P078-003 | Node import and review read-model | todo | MVP import is an explicit operator action into a dedicated Harvester review store; continuous directory watch is a later opt-in profile. |
| P078-004 | Whisper draft handoff | todo | Accepted finding can create a local Whisper draft, not publish directly. |
| P078-005 | First source adapter acceptance fixture | todo | Use filesystem Markdown/text as the first acceptance source adapter. |
| P078-006 | Inquirium/Agent-assisted grouping profile | deferred | Bounded model-assisted clustering and summarization; model output remains advisory. |
| P078-007 | Network-capable Harvester profile | deferred | Future Artifact Delivery handoff profile for explicitly configured remote sources; still findings-only and bounded/quarantined. |
| P078-008 | Public Harvester Gateway profile | deferred | Separate future proposal for public web/API intake, attachment quarantine, receipt tokens, redacted finding promotion, and reviewer queue; P078 only keeps hook compatibility. |
| P078-009 | Collector-submitted corroboration profile | deferred | Umbrella-operated collectors submit supporting/contradicting/context findings anchored to accepted phenomena or reviewer-approved queries. |

## Next Actions

1. Draft `weak-signal-finding.v1`.
2. Implement explicit operator import into the dedicated Harvester review store.
3. Add the filesystem Markdown/text source adapter and acceptance fixture.
4. Wire accepted finding -> local Whisper draft, preserving the separate
   publication approval gate.
