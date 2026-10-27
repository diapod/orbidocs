# Story 014: A Dormant Contest Entry Meets a Rumor

Status: Proposed acceptance story for
[P013 dormant-fact resonance](../40-proposals/013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27),
grouping task `P013-DFR-000`. Nothing in this story is implemented yet. It
fixes the observable behaviour that the grouped tasks must prove together.

Date: 2026-10-27

Related:

- [Proposal 013: Whisper, dormant-fact resonance](../40-proposals/013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27)
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

## Open Continuation

- The wire conjunction rule (P013-DFR-005).
- Vocabulary governance, cardinality floors and epoch length (P013 open
  questions).
- Whether a confirmed link may later register `whisper-interest.v1` as a
  separate, explicit disclosure.
