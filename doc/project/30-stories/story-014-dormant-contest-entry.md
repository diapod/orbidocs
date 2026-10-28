# Story 014: A Dormant Contest Entry Meets a Rumor

Status: Proposed acceptance story for
[P013 dormant-fact resonance](../40-proposals/013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27),
grouping task `P013-DFR-000`. Its
[variant](#variant-author-disclosure-condition) is the acceptance story for
[P013 author disclosure conditions](../40-proposals/013-whisper-social-signal-exchange.md#author-disclosure-conditions-2026-10-27),
grouping task `P013-ADC-000`. Nothing in this story is implemented yet. It
fixes the observable behaviour that the grouped tasks must prove together.

Date: 2026-10-27

Related:

- [Proposal 013: Whisper, dormant-fact resonance](../40-proposals/013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27)
- [Proposal 013: Whisper, author disclosure conditions](../40-proposals/013-whisper-social-signal-exchange.md#author-disclosure-conditions-2026-10-27)
  (the [variant](#variant-author-disclosure-condition) below)
- [Proposal 036: Memarium, fact retention horizons and personal records](../40-proposals/036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27)
- [Proposal 078: Weak Signal Harvester, Memarium dormant-fact profile](../40-proposals/078-weak-signal-harvester.md#memarium-dormant-fact-profile-2026-10-27)
- [Proposal 035: Agora, decorrelated bucket pull](../40-proposals/035-agora-topic-addressed-record-relay.md#decorrelated-bucket-pull-2026-10-27)
- [Proposal 057: User and operator notifications, P057-015 and P057-016](../40-proposals/057-user-and-operator-notifications.md#tracking)
- [Proposal 066: Inquirium Assistant Channel, dormant-fact capture](../40-proposals/066-inquirium-assistant-channel.md#dormant-fact-capture-and-rumor-suggestions-2026-10-27)
- [Proposal 015: Contextual Whisper authorship](../40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)
- [Proposal 070: Room primitive](../40-proposals/070-room-primitive.md)
- [Solution 002: Memarium](../60-solutions/002-memarium/002-memarium.md#fact-retention-horizons-and-personal-records)
- [Solution 011: Whisper](../60-solutions/011-whisper/011-whisper.md#dormant-fact-resonance)
- [Solution 020: Scheduler](../60-solutions/020-scheduler/020-scheduler.md#dormant-fact-resonance-jobs)
- [Solution 045: Inquirium Assistant Channel](../60-solutions/045-inquirium-assistant-channel/045-inquirium-assistant-channel.md#channel-not-counterparty)
- [Story 005: Whisper rumor intake](story-005-whisper-rumor-intake.md)

## Current Baseline Used by This Story

This story assumes the current Orbiplex corpus where:

- Memarium personal space is encrypted and operator-controlled. It keeps facts
  until an explicit forget and has no per-fact time horizon yet; P036-004 adds
  one.
- The Inquirium Assistant Channel is an inquiry affordance, not a contact, nym,
  Messaging peer or route. It advises and proposes; host-owned paths perform
  effects (S045).
- The Weak Signal Harvester is findings-only. It reads explicitly granted
  sources and emits `weak-signal-finding.v1` candidates for human review
  (P078).
- Whisper redaction, rumor nyms, thresholds and `association-room-proposal.v1`
  follow Story 005. The P015 contextual profile counts council-admitted
  participant sources per rumor context and epoch; the context binds
  `topic/class` and `signal/similarity-key`.
- Agora serves topic-addressed records with cursor-based listing (P035
  section 5.1). Room hosts association rooms after explicit opt-in (P070).
- A "rumor server" in this story is an Agora relay carrying Whisper topics, or
  a set of mirrored relays.
- The decorrelation vocabulary is a versioned JSON setting. The factory
  version ships with the Node distribution, and operators or power users may
  override it through ordinary P091 layers (P013-DFR-001). Both nodes in the
  main path use the factory version.

## Actors and Nodes

| Actor | Role |
|---|---|
| Agnes | Participant on node A; a poet who entered the contest. |
| Rant | Participant on node B; another entrant. |
| Relay R | Agora relay, with one mirror, carrying `ai.orbiplex.whispers/...` topics. |
| Council D | Contextual-authorship issuer and council (P015). |
| Projection C | Whisper projection authority that emits threshold and proposal records. |
| Organizer | A cultural institution outside Orbiplex. |

## Sequence of Steps

### Part 1: A fact without tension

1. Agnes decides to enter a poetry contest organized by a cultural institution.
2. She sends her entry to the organizer outside Orbiplex. Then she opens the
   recipient picker in Node UI. It lists her contacts and, visibly marked as a
   channel rather than a contact, the local assistant. She selects the
   assistant and writes an internal message: she has submitted her poem
   "Szaleństwo bobrów" ("The Madness of Beavers"), and the message includes the
   local path of the submitted file. Selecting the assistant opens an Assistant
   Channel turn. No contact record, Messaging envelope or route is created
   (P066-DFR-001).
3. The assistant asks the host to resolve the path. Agnes approves a one-shot
   read grant for that file. The host computes the SHA-256 digest of the
   original bytes, the media type, the size and a bounded text representation
   (P066-DFR-002). The assistant drafts a personal record (P036-007) and returns
   it as an inert capture proposal. The draft has:
   - kind `artifact-dispatched` with provenance `first-person-report`;
   - the organizer as counterparty, the contest name and the submission date;
   - the poem title;
   - two attachments: the original (its path as given, digest, media type and
     size) and the text representation;
   - the default retention horizon for this record kind.

   Agnes reviews the draft and accepts it. Had she requested a horizon above
   the operator ceiling, the draft would show the clamped value and an inline
   warning (P036-004). The host, not the assistant, writes the record into her
   personal space (P066-DFR-003).

   The contract admits three forms for the text: inline in the record, an
   embedded attachment, or a reference to the Memarium blob store. Inline and
   embedded forms are bounded by size limits. Agnes's node stores the text
   representation in the blob store and leaves the original file at its path;
   the recorded digest identifies the bytes she meant.

   Nothing leaves node A. The record is not a rumor, an opinion or a trace.

### Part 2: The context forms elsewhere

4. Weeks later, the organizer's website reports 1500 entries, so the jury will
   have very little time to read them all. A day later, social media
   announce a winner chosen surprisingly early. Several entrants are worried:
   the jury would have had to work without a break for several days, with
   about one minute per text at best. The organizer does not answer questions.
   Some entrants start to doubt the process, and some regret that the poems are
   not public for reading and comparison, although the organizer has the right
   to publish them.
5. Rant shares his doubts with his own local assistant. The assistant proposes
   drafting a rumor and, after Rant accepts, opens the Story 005 redaction flow
   (P066-DFR-004).
6. The rumor states doubt that so many entries could be evaluated in so short
   a time and links the entrants' public discussion. Rant's assistant labels
   its `topic/class` with one coarse term from the decorrelation vocabulary,
   `culture.competitions` (P013-DFR-001). The organizer, contest and dates go
   into the body and `context/facets`, and the draft derives a
   `signal/similarity-key` for this contest. Rant publishes the rumor under a
   contextual nym (P015) to relay R, topic key
   `ai.orbiplex.whispers/culture.competitions`.

### Part 3: Pull, not push

7. On node A, a scheduled Harvester job with the dormant-fact profile scans
   every current personal record in rotating, budgeted batches (P078-010).
   Inclusion is deliberately broad: no record is skipped for looking
   unimportant.
8. The job maps the contest record to vocabulary terms such as
   `culture.competitions` and `culture.literature` (P078-011). The mapping
   selects term ids only, and a term below the cardinality floor is replaced by
   its parent. The result updates a local interest profile that never leaves
   the node.

   Open point: may terms be combined with AND on the wire? AND could shrink the
   response pool but may lower recall and identify the reader more precisely.
   v1 sends a union of single terms and applies any conjunction locally;
   P013-DFR-005 measures the alternative.
9. At the next epoch boundary, Whisper's pull job builds the epoch pull plan
   from the profile: a bounded set of real terms plus decoy terms drawn from
   the vocabulary's popularity hints (P013-DFR-002). It pulls complete time
   slices for each planned term from relay R and its mirror (P035-016). The
   relays see only coarse topic keys, window ids and cursors.
10. Locally, the Harvester scores the pulled rumors against the unnarrowed
    record projection: organizer, contest name, submission date against the
    rumor window, record kind and title (P078-012). Rant's rumor exceeds the
    positive threshold, and the job emits a link-candidate finding that
    references both the record and the rumor.

### Part 4: Decision and follow-through

11. Agnes receives a batched local notification: a rumor may concern her
    contest entry (P057-015). The actions are Related, Not related (this rumor
    or this rumor context) and Later. Had she answered Not related, the host
    would record the decision and its time in Memarium; the record view and the
    rumor view would both show it, and the matcher would suppress the pair (or
    the context) in later epochs, avoiding repeated matches and false alerts
    (P036-008). She confirms the link instead.
12. Her "My rumors" view now lists the rumor beside the rumors she authored and
    shows its fate: threshold state, association proposals, room state and her
    own curation (P013-DFR-003).
13. Prompted by the confirmed link, the assistant proposes drafting Agnes's own
    rumor related to Rant's (P066-DFR-004).
14. Agnes drafts it through redaction: she submitted an entry within the
    stated window and shares the doubts. Poem text, title and path are
    excluded by default. She marks the rumor explicitly as related to Rant's.
    The draft inherits Rant's `topic/class` and `signal/similarity-key`, so it
    joins the same rumor context (P013-DFR-004). She publishes it under her own
    contextual nym (P015).
15. Projection C sees two council-admitted sources in the same context and
    epoch and emits threshold and `association-room-proposal.v1` records
    (Story 005, P015 Gate B). Rant and Agnes opt in, and a Room opens (P070).
    There they exchange opinions and agree to share their entries with each
    other, so everyone can read them. They can paste text into room messages,
    open a linked message thread, or post a link to an external file-sharing
    server. Sharing Agnes's poem from Memarium requires an explicit per-share
    declassification of the attachment, and an external link carries a warning
    that the server is outside Orbiplex guarantees (P013-DFR-006).

## Acceptance Assertions

| ID | Assertion | Proves |
|---|---|---|
| S014-A1 | Before step 14, no outbound byte from node A (Agora, AD, INAC, Matrix, model egress) contains the poem text, title, path, digest, organizer or contest name; a canary scan checks every surface. | P013-DFR-002, P078-011, P035-016 |
| S014-A2 | Node A's discovery requests contain only vocabulary term ids, window ids and cursors. Real and decoy terms are indistinguishable in shape and fetch behaviour, and the request set changes only at epoch boundaries. | P013-DFR-002 |
| S014-A3 | Relay logs show complete-slice pulls and no single-record fetch selected by a local match. | P035-016 |
| S014-A4 | In the not-related variant, no further alert appears for the same pair (or context) in later epochs, and the decision is visible from both the record and the rumor views. | P036-008, P057-015, P078-012 |
| S014-A5 | Forgetting or expiry of the record removes its interest terms, scores and link candidates; the matcher no longer sees it. | P036-005, P036-006, P078-013 |
| S014-A6 | A requested horizon above the ceiling becomes the ceiling, with an inline warning for manual capture or a notice for automatic capture. | P036-004, P057-016 |
| S014-A7 | The assistant never writes Memarium; the write follows Agnes's acceptance under host authority. | P066-DFR-003 |
| S014-A8 | Agnes's related rumor counts as a second source in Rant's context, and no public record reveals either node id. | P013-DFR-004, P015 Gate B |
| S014-A9 | Pull bytes per epoch stay within budget. In the small-federation variant, node A pulls every Whisper topic and expresses no interest. | P013-DFR-002, P035-017 |
| S014-A10 | Sharing a Memarium attachment in the Room requires explicit declassification, and external links show a warning. | P013-DFR-006 |
| S014-A11 | In the local-term variant, the unrated local term stays out of the pull plan until the operator admits it after a warning, and no vocabulary version or digest appears in any outbound request or record. | P013-DFR-001, P013-DFR-002 |

## Fixture Profile

- A 10-minute epoch and 2-minute certificates, as in the P015 fixture, and a
  threshold of two sources.
- A vocabulary fixture of at least 20 terms, including `culture.competitions`
  and `culture.literature`, with population hints and one term below the floor.
- Relay R and one mirror. A fixed number of decoy terms per epoch.
- Controlled clocks for retention expiry and epoch boundaries.

## Variants

- **Not related.** Agnes rejects the link (S014-A4).
- **Expired record.** The record expires before the rumor appears. There is no
  match and Agnes learns nothing; that is the cost of the horizon she chose.
- **Below-floor term.** The parent term is pulled instead.
- **Mislabeled rumor.** Rant labels the rumor `culture.literature`. Agnes still
  finds it if her profile includes that term; otherwise she misses it, which is
  a documented limitation.
- **Small federation.** The whole Whisper prefix fits the budget, so node A
  pulls everything (S014-A9).
- **Local term.** Agnes's operator adds `local.poetry-contests` in a local
  P091 layer, and the generalization job maps her record to it as well. The
  term is unrated, so the pull plan leaves it out until the operator admits it
  after a warning (S014-A11). Authoring with that term would warn Rant that
  factory-vocabulary readers do not pull its bucket.

## Variant: Author Disclosure Condition

This variant exercises
[P013 author disclosure conditions](../40-proposals/013-whisper-social-signal-exchange.md#author-disclosure-conditions-2026-10-27)
and closes with `P013-ADC-000`. It changes steps 6 to 15 of the main path as
described; everything else still holds. The room proposal at two sources is a
coordination threshold; Rant's embargo on his content is a separate condition.

1. In step 6, Rant decides to embargo his rumor. With his assistant he
   approves a correlation descriptor under the grouping rule
   `contest-assessment/v1`: doubts about how entries were assessed in the 2026
   edition of contest K organized by O. He rejects the broader `contest/v1`,
   which would also count unrelated reports about payouts or the entry form.
2. He sets the condition: at least three other qualified sources, a window of
   four epochs, the audience `federation-scoped`, mode `confirm`, custody
   `withheld`, join policy `keyed-and-confirmed-joins`, coordination
   participation `allowed` and descriptor visibility `public-notice`. The
   Story 005 flow produces two redactions: a minimal correlation text and a
   release payload for federation-scoped readers.
3. Rant's node sends the protected signal privately to projection C, which is
   both the counting authority and the only correlator. It also publishes a
   content-free correlation notice in `culture.competitions`, under the exact
   P015-005 publication tuple. The author first signs an embargo manifest; the
   protected signal references its digest. C's admission receipt binds both.
   A companion fixture uses a separate correlator D: the named protected-holder
   set is {C, D}, with role-specific grants, not a larger forwarding budget.
4. Agnes's pull (step 9) finds the notice and her record matches it. She
   confirms and authors a related signal in the same context (steps 11–14).
   Its typed `signal/related-to` points to the public notice's `record/id`
   (`target/kind = whisper-correlation-notice`), never to the unseen protected
   signal. She needs no private signal lookup or id. The context key is inherited,
   and C counts one other source. Because Rant allowed coordination
   participation, the two sources reach the coordination threshold and C emits
   the room proposal (step 15). Rant's content stays embargoed for wider
   audiences.
5. Agnes reposts her signal and a holder forwards it; the count stays at one.
   Two more entrants find the notice and publish their own reports in the same
   context during Rant's epoch, so the count reaches three.
6. C attests three other sources under a fresh status. Rant's node retrieves
   the attestation by condition id, and Rant gets a confirmation prompt
   (P057-017) with the criterion, count, audience and deadline. He confirms
   with the condition's control key, and C accepts the confirmation as a case
   event.
7. Rant's node freezes an embargo release intent, then submits a commit to C.
   It binds the exact intent digest (payload and prepared public proofs, without
   the future commit receipt), canonical federation/topic/access descriptor,
   executor, route and hand-over deadline. C atomically checks active consent,
   the slot keyed by original condition and audience digests and a count under
   a source status at most 300 seconds old. The signed receipt binds this intent.
   Rant's node journals the final release envelope, now containing the receipt,
   before AD receives its frozen bytes and delivery id. Agora's content-addressed
   `record/id` is separate from the logical per-slot `release/id`.
   Readers verify the manifest, certificate, admission claim, author confirmation,
   commit and payload offline, including when retrieval of the protected signal
   is explicitly denied. They trust C's admission/count claims about hidden data;
   the record states that distinct sources are not evidence of truth.
8. Negative paths:
   - Had Rant declined, or let the prompt expire, nothing would be released.
     Decline suppresses that proposal across restart; the active condition does
     not cause another prompt without explicit retry or a consented bounded rule.
   - In pre-authorized mode, withdrawal or expiry after a satisfying attestation
     but before commit still refuses. `satisfied` is a derived predicate, never
     an irrevocable reservation or a persisted case state.
   - Had a source been revoked before the commit, C's count would have fallen
     below three and C would have refused the commit, provided the revocation
     had reached C's source status. A revocation newer than that status, which
     may be up to 300 seconds old, may not be reflected.
   - Had C accepted Rant's withdrawal before the commit, the commit would have
     been refused. A withdrawal accepted after the commit stops only other and
     later releases.
   - Had C's response to the commit been lost, Rant's node would read the
     outcome by request id and recover the same accepted commit, even if a
     withdrawal had been accepted after it. Had the node crashed after the
     commit but before the hand-over, it would hand over the same bytes with
     the same delivery id before the deadline, without preparing a new release.
   - A second attestation after the release produces no second release for the
     same audience.
   - A third source that appears only in a later epoch does not suffice; there
     the requirement is four distinct sources within that epoch, even when
     Rant publishes nothing in it. The UI shows that conservative effective threshold.

| ID | Assertion | Proves |
|---|---|---|
| S014-A12 | Before release, the correlation text reaches only named holders (C alone in the baseline, C and D in the split-role fixture) and the release payload does not leave Rant's node. C's query endpoints, Agora records, notices, notifications, logs and exports contain neither, and the public notice is content-free. | P013-ADC-003, P013-ADC-007 |
| S014-A13 | The room proposal at two sources releases nothing. The release happens only after Rant's confirmation and a commit accepted by C, counting at least three other sources at the commit point. A revocation already reflected in C's status or a withdrawal accepted earlier refuses the commit, while a withdrawal accepted later does not cancel it. A lost commit response recovers the same commit, a crash after the commit hands over the same bytes and delivery id, and a later attestation yields no second release. | P013-ADC-004, P013-ADC-005, P013-LLR-008 |
| S014-A14 | Reposts and forwards by one source leave the count unchanged; later epochs require N + 1 both with and without Rant, and succession changes no count. | P013-ADC-004 |
| S014-A15 | The offline release exposes only the approved payload, criterion/count metadata and minimal verification package. It reveals no participant identity, correlation text, private facets, source lists or contact route; nym/case linkage carried by approved proof is explicitly previewed. | P013-ADC-001, P013-ADC-005 |
| S014-A16 | Two routes to one room reserve one slot. Two different rooms reserve two only with consent for both; a third or widened history audience refuses. Logical release/id and Agora record/id are different identities. | P013-ADC-005, P070 |
| S014-A17 | Receiver verification succeeds with no protected body and with its retrieval denied. Changing the manifest, certificate scope, admission binding, intent or payload refuses. No digest commits an envelope containing that same digest's receipt. | P013-ADC-001/005, P035-019, P015-005 |
| S014-A18 | With C and D separate, both explicitly admitted holders receive only their role-authorized material. An unnamed node refuses even when hop budget remains. | P013-PEX-001, P013-ADC-003 |
| S014-A19 | Both pre-commit withdrawal/expiry paths work in pre-authorized mode; declined prompts remain suppressed after restart. No durable case status claims satisfied. | P013-ADC-005/008, P013-LLR-008 |
| S014-A20 | Narrowing keeps the original condition id/slots. Widening creates a new anchor/case/consent; it neither withdraws the old case nor leaks an automatic link. | P013-ADC-001, P013-LLR-006 |
| S014-A21 | Agnes sees only the notice and authors a relation to its public id and typed kind. Wrong notice publication tuples refuse; no hidden signal id appears in the finding, relation or wire trace. | P013-DFR-004, P013-ADC-007, P015-005, P078-012 |

### Variant Evidence Ownership

These are required future proofs, not results. ADC-000 owns the composed report;
no producer can mark that row done from isolated schema tests. Its report maps
every assertion to the exact source revisions, fixture, observed outcome and
retained artifact/qualifier. Missing evidence remains pending.

| Assertion(s) | Prerequisite task(s) | Required evidence |
|---|---|---|
| S014-A1–A3, A11 (pull and local match) | P013-DFR-001/002; P078-010/011/012; P035-016/017 | Bounded pull trace and canary scan; no fact-specific wire query |
| S014-A4–A7 (decision and My rumors) | P036-008; P013-DFR-003; P066-DFR-003; P057-015/016 | Retained local decisions/read views; no autonomous publication |
| S014-A8, A21 (notice-related signal) | P013-DFR-004; P013-ADC-007; P015-005; P015 Gate B | Notice-only authoring, exact certificate tuple and distinct-source result |
| S014-A9/A10, A16 (coordination and rooms) | P013-DFR-006; P070; P013-ADC-005 | No release at proposal time; room consent/history and slot tests |
| S014-A12, A18 (custody) | P013-PEX-001; P013-ADC-003 | Two-node private exchange, separate holder roles and all-surface canary scan |
| S014-A13/A14/A19 (ordering and execution) | P013-ADC-004/005/008; P013-LLR-008; P057-017 | Both race orders, author absent/present, lost reply, crash-before-AD and declined-prompt replay |
| S014-A15/A17/A20 (proof and case identity) | P013-ADC-001/005; P035-019; P013-LLR-006; P015-005 | Offline package with private retrieval refused, tamper vectors and new-case/narrowing tests |


## Open Continuation

The variant proves the current single-epoch, single-authority contract only.
It does not close ADC's cross-epoch accumulation or confirm-mode author
reachability questions. Withheld custody also requires the author at release;
authority-independent verification of hidden counts and committee authorization
remain open. A missing author/status/proof defers or expires the operation,
never authorizes a public fallback.


- The wire conjunction rule (P013-DFR-005).
- Vocabulary governance, cardinality floors and epoch length (P013 open
  questions).
- Whether a confirmed link may later register `whisper-interest.v1` as a
  separate, explicit disclosure.
