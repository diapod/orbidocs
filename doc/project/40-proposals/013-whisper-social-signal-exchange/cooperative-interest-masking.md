# Cooperative Interest Masking {#cooperative-interest-masking}

Created: 2026-10-27. Revised: 2026-10-28.

Based on: [P013 domain map](../013-whisper-social-signal-exchange.md).

Status: proposed post-MVP feature; no runtime claim. It extends the
[dormant-fact pull plan](../013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27) and adds no
transport.

## Summary {#summary}

A relay that serves bucket pulls learns which node reads which coarse topic,
and when. Local decoys blur that, but a node with a real interest can remain
the only stable reader of a term over many epochs. Cooperative interest masking
lets a node ask selected peers to "also pull X" for a bounded period. It never
asks them to "pull X for me": every participant performs its own ordinary pull,
keeps its own response and reports nothing back. This is neither brokering nor
onion routing.

The promise is bounded. Reads become a weaker indicator of interest. The
mechanism does not hide the reader's address or identity, and it does not make
it impossible to learn who is really interested.

## Context and Problem {#context-and-problem}

- **Fact.** The epoch pull plan (P013-DFR-002) mixes real terms with decoys
  sampled from rated vocabulary terms, and pulls complete slices.
- **Inference.** Independent decoys are uncorrelated across nodes and rotate.
  A real interest persists, so across epochs the persistent reader of a term
  stands out. Cooperative cover adds other persistent readers of the same term.
- **Constraint.** A helper learns what it is asked to read. Requests therefore
  mix real and decoy terms and carry no motive, so that knowledge stays
  ambiguous.
- **Constraint.** Artifact Delivery leaves durable state (S023). Using it is not
  traceless; it needs a dedicated retention profile before exposure.

## One Plan, Three Origins {#one-plan-three-origins}

Following the reusable-data-abstraction rule of `node:DEV-GUIDELINES.md`, the
DFR plan becomes the general `whisper-pull-plan.local.v1` rather than gaining a
parallel structure. It has one entry abstraction:

| Field | Meaning |
|---|---|
| `term` | A rated vocabulary term id |
| `window` | The epoch and its pull window |
| `origin` | `need` (interest profile), `decoy` (local draw) or `cover` (accepted request) |
| `origin/ref` | The local source: profile revision, draw id or request id |
| `expires-at` | The end of the entry's validity |

`origin` is local data. The executor ignores it, the relay never sees it, and
diagnostics show only aggregate counts per origin. One executor serves every
entry: the same relays and mirrors, endpoints, headers, pagination, complete
download, retry budget and storage path. A cover pull never aborts early and
never carries a marker. Its results enter the ordinary local rumor store under
ordinary retention, and whether they were useful is reported to no one.

## Cover Requests {#cover-requests}

`whisper-cover-request.v1` is deliberately small:

| Field | Meaning |
|---|---|
| `schema` | Constant schema id |
| `request/id` | A random 128-bit id; the idempotency key per sender |
| `cover/terms` | 1–8 rated factory vocabulary term ids |
| `cover/from-epoch` | The first covered epoch |
| `cover/epochs` | 1–8 whole epochs |
| `schedule/rule` | The shared timing rule, `cover-schedule/v1` |

The schema has `additionalProperties: false` and a 2 KiB bound. It deliberately
omits a motive, a real-or-decoy marker, the initiator's profile, a result
route, forwarding fields, URLs or addresses, and any vocabulary version or
digest.

- **Composition.** The initiator builds requests from its plan by a rule that
  includes real terms only probabilistically and also sends requests with no
  real term. Every term is drawn from the same rated distribution as local
  decoys.
- **No own signature.** Authenticity comes from the authenticated peer session
  and AD admission, so a helper holds no transferable signed proof of what the
  initiator asked. Whether INAC session authentication actually has that
  property must be verified (`P013-CIM-002`); if not, the claim narrows.
- **No cancellation.** Requests expire. A cancellation sent when a real need
  ends would itself reveal the need.
- **No recursion.** A helper never forwards a request, and the schema has no
  field that could ask it to.

## Delivery Through Artifact Delivery {#delivery-through-artifact-delivery}

```text
Node A cover component
  -> whisper-cover-request.v1
  -> Artifact Delivery A (private route, inac-direct)
  -> INAC over an authenticated peer session
  -> Artifact Delivery B (admission)
  -> cover component B (single authoritative acceptor):
     local consent, budget, validity, deduplication, prior execution
  -> B's pull plan and S020 job, at a locally drawn time
  -> ordinary Agora topic read; results stay at B
```

AD is the component interface and `inac-direct` the carrier, per S023 and
`node:DEV-GUIDELINES.md`. Delivery authority is not control authority. The
acceptor checks consent, budget, validity and prior execution before any state
change, and it refuses generically, without telling the sender why.

AD records deliveries and admissions durably, and AD does not store arbitrary
artifacts in Memarium. The absence of a Memarium entry therefore does not mean
the absence of data on disk. Before runtime exposure this consumer requires the
[minimal-trace delivery profile](../../60-solutions/023-artifact-delivery/023-artifact-delivery.md#minimal-trace-delivery-profile)
(`S023-001`, `S023-002`). Validity and retention are different things: an
expired request is not an erased request.

## Shared Timing {#shared-timing}

Under `cover-schedule/v1`, every participant, the initiator included, draws for
each executable bucket job and epoch an independent uniform offset within the
epoch's pull window and fetches at that time. Duplicate planning entries are
coalesced first, as specified in the [implementation recommendations](#implementation-recommendations). Entries of every origin follow the same rule,
so a real interest produces no "interested first" or "interested last"
pattern. The window bounds and any additional jitter are profile values, tuned
by `P013-CIM-007`.

## Multi-Epoch Cover {#multi-epoch-cover}

A request covers whole epochs, and a helper keeps an accepted term for the
whole period. The initiator keeps its helper set for a term stable during the
term's cover period. It starts cover together with the need and keeps it after
the need ends (tail padding). Helpers and terms rotate only by rules evaluated
on multi-epoch histories (`P013-CIM-007`), because drawing new helpers for every
read can leave the interested node as the only constant reader.

## Participation and Budgets {#participation-and-budgets}

Participation is voluntary and bounded by P091 settings:

- initiation and acceptance are separate settings, both off by default;
- acceptance admits senders from `contacts`, an `allowlist` or `advertised`
  peers;
- limits cover active cover terms, bytes per epoch, request duration in epochs
  and requests per sender per epoch;
- helper selection reuses AD recipient selectors: explicit node lists, or
  `capability-many` with `max/nodes` against peers advertising
  `whisper.cover.v1`. Advertising participation is itself a disclosure and is
  opt-in.

A helper accepts only rated vocabulary terms: no arbitrary addresses, no
recursion, and no obligation beyond the request's expiry.

## Not Memory, Not Support {#not-memory-not-support}

Cover and decoy entries never enter the interest profile, Memarium personal
records or link-candidate claims. A cover pull creates no rumor, no
confirmation and no source counted toward a coordination threshold or an author
disclosure condition. The mechanism masks observable behaviour; it does not
falsify personal memory or reports.

## Effect Recovery Classes {#effect-recovery-classes}

| Effect | Class | Owner | Point of no return |
|---|---|---|---|
| Sending a cover request | `irreversible-external` | Initiator cover component through AD | AD hands the bytes to INAC |
| Accepting a request into the plan | `transactional-withheld` | Helper cover component | The plan commit |
| A cover pull | `irreversible-external` | Whisper pull job | The relay observes the read |

## Effectiveness Must Be Measured {#effectiveness-must-be-measured}

`P013-CIM-007` compares cooperative cover with independent decoys at the same
byte budget, on multi-epoch histories, against three adversaries:

1. relays that see node, term and time;
2. relays together with helpers that reveal the requests they received;
3. a federation-wide passive observer.

Metrics include how accurately real interests per node can be inferred, the
rank of true terms and the number of epochs until identification, across helper
counts, request mixes, durations and timing parameters. The documentation may
claim only what these measurements show.

## Invariants {#invariants}

1. Each participant pulls for itself; nothing is relayed to the initiator.
2. `origin` never leaves the node and never changes how a pull is executed.
3. Requests carry no motive, no marker and no forwarding instruction.
4. All participants follow the same timing rule.
5. Acceptance follows local consent and budgets; delivery grants no control.
6. Requests expire, are never cancelled and never recurse.
7. Cover never becomes interest, memory, a rumor or a counted source.
8. Runtime exposure requires the minimal-trace delivery profile.

## Trade-offs {#trade-offs}

- Cover costs bandwidth that independent decoys could also spend. Its value
  must be demonstrated on equal budgets.
- Helpers learn request contents. Mixing makes that knowledge ambiguous, not
  absent.
- Stable helper sets help against persistence analysis but concentrate
  knowledge in fewer helpers.
- Tail padding prolongs cost after a need ends.

## Failure Modes and Mitigations {#failure-modes-and-mitigations}

| Failure | Effect | Mitigation |
|---|---|---|
| A helper reveals requests to an observer | The initiator's candidate terms are exposed | Mixed requests without motive, no portable signature, evaluation with colluding helpers |
| A cover pull behaves differently | Cover is recognizable | One executor, complete download, no markers, the shared timing rule |
| Rotating helpers every read | The interested node remains the only constant reader | Stable sets per cover period, tail padding, history-based rotation rules |
| Requests used for amplification | Load on relays or helpers | Rated terms only, per-sender and per-epoch budgets, no recursion |
| Durable AD traces | Requests reconstructable from disk | Minimal-trace profile with scheduled purge |
| Cancellation timing | Reveals the end of a need | No cancellation; expiry only |

## Open Questions {#open-questions}

1. Default request mix, helper count and cover duration, pending
   `P013-CIM-007`.
2. Whether a deniable request carrier is available on every private-safe
   adapter, or only on INAC sessions.
3. Whether helpers should also pad their own acceptance so that refusal under
   load does not reveal their capacity.

## Implementation Recommendations {#implementation-recommendations}

The [shared-mechanism dispositions](../013-whisper-social-signal-exchange.md#implementation-reuse)
choose DFR's plan and executor as the single owner. Keep local planning causes
separate from executable jobs:

```text
PlanEntry = (term, window, origin, origin_ref, expires_at)
PullJob = (topic_key, window, relay_profile_ref, scheduled_at, budget_ref)
```

`compile_pull_jobs` consumes the immutable epoch vocabulary resolution and all
admitted entries. It maps terms to topic keys, coalesces identical bucket/window/
relay-profile requests, checks bounded work and byte budgets, and persists the
jobs before dispatch. Several origins may explain one job; retain those causes
locally within the plan's retention, never as request fields or executor branches.
This prevents a need and a cover entry for the same bucket from causing a second
revealing fetch. Different windows remain different jobs. Pull-all uses the same
listing/pagination executor, not a second acquisition implementation.

Draw one offset per executable job and epoch using `cover-schedule/v1`, after
coalescing, for every origin alike. Save the sampled time: restart and S020 retry
must not draw it again. S020 executes the persisted deadline, without an additional
jitter layer. An accepted cover cause survives until its original expiry even
when a matching local need disappears. Late inputs do not cause an immediate,
origin-specific fetch; epoch planning owns their admission to the schedule.

The executor receives only jobs. It uses the same completion, pagination, mirror
deduplication and budget handling for all of them. Budget exhaustion, pruning or
missing pages yield an explicit incomplete result, not an empty complete slice;
there is no early exit because a local match was found. Results enter the ordinary
rumor store. The planner never promotes a cover cause into personal interest.

CIM-001/003/004 fixtures cover mixed-origin duplicate buckets, deterministic
replay of saved offsets, changed request bytes under one sender/request id,
bounded plan growth and expiry without cancellation. Compare emitted requests
and completion behavior after erasing local provenance from otherwise equal
plans. This proves path equivalence, not anonymity: CIM-007 still owns the
multi-epoch effectiveness experiment.

## Cooperative Interest Masking Tracker {#cooperative-interest-masking-tracker}

All rows are post-MVP `todo`. The grouping row closes on the composed run and
the measured claim.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P013-CIM-000 | Cooperative masking acceptance and bounded claim | todo | P013-CIM-001–008; [S023-001–002](../../60-solutions/023-artifact-delivery/023-artifact-delivery.md#minimal-trace-delivery-profile) | A retained three-node run (initiator, two helpers, relay with a mirror) shows identical pull behaviour across origins, expiry without cancellation and purged traces; the claim in this section is restated from `P013-CIM-007` results. |
| P013-CIM-001 | Generalize the pull plan | todo | P013-DFR-002 | `whisper-pull-plan.local.v1` with one origin-tagged entry abstraction and one executor; origin never leaves the node; fixtures prove identical requests, pagination and completion for every origin. Coalesce mixed-origin duplicate buckets into one job; retain bounded local causes without leaking them or changing completion behavior. |
| P013-CIM-002 | Freeze the cover request contract | todo | P013-DFR-001 | `whisper-cover-request.v1` with closed fields and bounds; the composition rule, including requests without real terms; no own signature, no cancellation and no forwarding fields. Verify whether the INAC session gives helpers no transferable proof; negative fixtures for extra fields and unrated terms. |
| P013-CIM-003 | Shared timing rule | todo | P013-CIM-001; S020 | `cover-schedule/v1` with independent uniform offsets per compiled job and epoch from a CSPRNG for all origins and the initiator; profile parameters; order-statistic tests showing no stable first or last reader. Persist offsets after coalescing and replay them unchanged; no extra S020 draw or immediate late-origin fetch. |
| P013-CIM-004 | Helper acceptor | todo | P013-CIM-002; S023-001; P091 | One authoritative AD acceptor that checks consent, sender class, budgets, validity, deduplication and prior execution before any state change. It refuses generically, follows a transition table and keeps bounded state purged at expiry, and its tests cover refusal, replay and bounded growth. |
| P013-CIM-005 | Initiator helper selection and multi-epoch maintenance | todo | P013-CIM-002; S023 selectors | Stable helper sets per cover period, tail padding and rotation rules; reuse of AD recipient selectors and the `whisper.cover.v1` advertisement; P091 initiation settings. |
| P013-CIM-006 | Separation from memory and social signals | todo | P013-CIM-001 | Fixtures prove that cover and decoy entries never reach the interest profile, Memarium personal records, link candidates, thresholds or disclosure-condition counts. |
| P013-CIM-007 | Effectiveness evaluation | todo | P013-CIM-001–005 | A multi-epoch simulation comparing cooperative cover with independent decoys at equal byte budgets against the three adversaries; parameter sweeps; a recorded bounded claim and recommended defaults. |
| P013-CIM-008 | Operator settings and readiness | todo | P013-CIM-004–005; P091 | Initiation and acceptance settings, budgets and aggregate load per origin in readiness; diagnostics without request contents or sender lists. |
