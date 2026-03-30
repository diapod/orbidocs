# Story 006: Voluntary Swarm Service Exchange for Cooperative Content Production

## Current Baseline Used by This Story

This story assumes the current Orbiplex corpus where:

- a Node can expose explicit market-facing or exchange-facing service offers through
  attached middleware modules rather than only through generalized answer-room flows,
- attached middleware such as `Orbiplex Dator` may declare priced service contracts
  while still delegating actual model invocation to the Node's model-runtime layer,
- attached workflow middleware such as `Orbiplex Arca` may compose local and remote
  steps into repeatable orchestration pipelines without becoming the semantic source
  of payment, identity, or transport truth,
- in the hard MVP, `Orbiplex Dator` and `Orbiplex Arca` are bundled with the Node
  distribution as Python middleware modules and are attached through the supervised
  `http_local_json` connector/executor,
- a Node may act both as an individual participant and as an organization-bound
  operator when it holds the right key material or delegated signing authority,
- service advertisements can be propagated over a dedicated commercial or exchange
  publication channel, allowing external catalogs to index active offers without
  becoming the only authority over them,
- settlement remains explicit and auditable in ORC credits, while fiat onboarding or
  gateway funding may exist at the ecosystem edge without redefining the protocol
  core,
- the currently executable contract substrate in `Node` remains the procurement
  family plus settlement artifacts:
  `procurement-offer.v1`, `procurement-contract.v1`,
  `procurement-receipt.v1`, `response-envelope.v1`, `ledger-hold.v1`,
  `ledger-transfer.v1`, and `gateway-receipt.v1`,
- local or remote model execution remains transport-agnostic from the perspective of
  the exchange plugin itself: the plugin asks the Node for model-backed work rather
  than integrating provider APIs on its own.

This story is not about speculative high-frequency automation or adversarial market
behavior. It is about a cooperative voluntary exchange where priced services,
workflow composition, provenance, and bounded automation all remain visible.

Related follow-up planning note:

- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/20-memos/service-order-to-procurement-bridge.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/50-requirements/requirements-012.md`

## Identity Model

This story relies on the layered identity model established in the Orbiplex
networking and identity architecture:

- `node:did:key:...` identifies the serving infrastructure and signs transport-level
  artifacts: advertisements, handshakes, keepalives.
- `participant:did:key:...` identifies the human participant and signs
  application-level artifacts: service offers or catalog publications, procurement
  contracts and receipts, response decisions, and reputation signals.
- `org:did:key:...` identifies an organization participant and signs on behalf of the
  organization. An org identity has a `custodian-ref` pointing to the
  `participant:did:key` of its controlling operator.

In MVP, `node-id` and `participant-id` MAY share the same underlying `did:key`. The
protocol does not assume this — it treats them as independent subjects.

For this story:

- Ola, Adam, and Marcin each operate as `participant:did:key:...` — individual
  participants offering services.
- Roman operates as `participant:did:key:...` personally, but acts on behalf of
  `org:did:key:...` (`CasualFeeders`) when placing orders and settling payments.
  Roman's participant identity is listed as `org/custodian-ref` for `CasualFeeders`.

## Middleware Execution Model

`Dator` and `Arca` are hosted middleware extensions, not autonomous agents. In the
hard MVP they are bundled Python modules distributed together with Node and
executed within the Node's runtime under host supervision through
`http_local_json`:

1. The Node daemon builds a `WorkflowEnvelope`.
2. The daemon invokes `run_hook(...)` in the host's runtime.
3. Successive middleware executors receive the envelope and return
   `MiddlewareDecision` proposals.
4. The host validates each decision and checks whether proposed mutations are
   permitted by the active policy and field registry.
5. The host applies permitted changes, revalidates the envelope, and decides whether
   to continue the middleware chain or terminate it.

This means:

- Middleware may influence the payload, but only where the host permits and only in
  ways prescribed by policy and field registry.
- Middleware does **not** sign protocol artifacts. The Node's `participant:did:key`
  (or `org:did:key` when acting on behalf of an organization) signs all
  exchange-level artifacts.
- Middleware does **not** hold private keys, manage transport, or control settlement.
  These remain host responsibilities.

## Service Exchange Lifecycle

This story is intentionally more ambitious than the currently frozen procurement
MVP. To keep it implementable, it should be read in two layers:

1. a service-publication layer specific to exchange plugins such as `Dator`,
2. an execution-and-settlement layer that SHOULD reuse the already frozen
   procurement and settlement contracts until a dedicated service artifact family is
   actually standardized.

Implementation-oriented reading:

| Story layer | Preferred current contract |
|-------------|----------------------------|
| standing offer publication | plugin-level or future `service-offer.v1` |
| buyer selects one standing offer | host-side workflow decision |
| priced execution contract | `procurement-contract.v1` |
| delivered payload | `response-envelope.v1` |
| terminal economic outcome | `procurement-receipt.v1` |
| escrow reservation and release | `ledger-hold.v1` + `ledger-transfer.v1` |

This keeps the story aligned with proposal 011 and with the current `Node`
implementation:

- explicit artifacts at each lifecycle transition,
- settlement through auditable ORC transfer,
- provenance and trace as first-class concerns,
- separation of economic facts from reputation signals,
- participant-side acceptance, rejection, and dispute as explicit operations
  rather than implicit chat convention.

The service-specific concepts introduced by this story remain valuable, but they
should be treated as a future specialization layer over the current procurement
substrate:

- model backing,
- hybrid flags,
- queue posture,
- input and output constraints,
- standing catalog publication,
- buyer-initiated orchestration over many standing offers.

## Service Offer Artifact

`service-offer.v1` is described here as a future exchange-facing artifact, distinct
from `node-advertisement.v1`. `node-advertisement.v1` describes transport endpoints
and capabilities. A service offer would describe a priced, exchange-facing service.

For implementation planning, this artifact SHOULD be treated as future-facing and
non-blocking for the current Node MVP. The current executable path can already ship
the economic core of the story by reusing `procurement-contract.v1`,
`response-envelope.v1`, and `procurement-receipt.v1`, while `Dator` keeps the
service-catalog surface as a plugin-local or later-standardized layer.

A service offer is signed by the provider's `participant:did:key` (not by
`node:did:key`) because it is an application-level commitment, not a transport-level
announcement.

A service offer carries at least:

- `offer/id` — stable identifier for this offer.
- `provider/participant-id` — `participant:did:key:...` of the provider.
- `provider/node-id` — `node:did:key:...` hosting the service.
- `service/type` — schematic service category (e.g. `text/redaction`,
  `research/topical`, `image/generation`).
- `service/description` — human-readable service description.
- `pricing/amount` and `pricing/currency` — price per unit, carried on the wire in
  ORC minor units with fixed scale `2` (e.g. `1000` for `10.00 ORC` per `1800`
  input characters).
- `pricing/unit` — what constitutes one billable unit.
- `constraints/input` — accepted input parameters (format, size, language).
- `constraints/output` — promised output parameters (format, dimensions, size).
- `delivery/max-duration` — maximum time from acceptance to delivery.
- `queue/auto-accept` — whether orders are accepted automatically.
- `queue/max-depth` — maximum concurrent active tasks.
- `queue/current-depth` — current queue occupancy (updated on re-publication).
- `hybrid` — whether the service involves human intervention beyond model output.
- `model-first` — whether model processing precedes human intervention.
- `seq` — monotonic sequence number (higher replaces lower, same as advertisement).
- `ts` — publication timestamp.
- `ttl` — time to live; offer expires after `ts + ttl`.

Service offers are propagated through a dedicated exchange publication channel. They
are signed, sequenced, and TTL-expiring — following the same patterns as
`node-advertisement.v1`.

## Sequence of Steps

### Infrastructure Setup

1. Ola, Adam, and Marcin each run an Orbiplex Node with the `Orbiplex Dator`
   middleware attached as a hosted extension. Each Node has:
   - a stable persisted `node:did:key:...` (infrastructure identity),
   - a stable `participant:did:key:...` (participant identity, same key in MVP),
   - a settlement-capable ORC account bound to `participant:did:key`,
   - the bundled Python `Dator` middleware registered in the host's middleware
     chain through `http_local_json`.

2. Roman runs his own Orbiplex Node and acts on behalf of the organization
   `CasualFeeders`, which holds:
   - `org:did:key:z6MkCF...` as its organization identity,
   - `org/custodian-ref: participant:did:key:z6MkR...` (Roman's participant
     identity),
   - a settlement-capable ORC account bound to `org:did:key:z6MkCF...`.

   Roman's Node also has the bundled Python `Orbiplex Arca` middleware attached
   through `http_local_json` for workflow orchestration.

### Required Infrastructure Roles

The scenario assumes a small but explicit infrastructure shape around those
participants. These are logical roles first; hard MVP may co-locate some of them
in one deployment.

1. `buyer-orchestrator node`

   Roman's Node acts as the buyer-side host and workflow orchestrator. It is
   responsible for:

   - holding workflow state for `CasualFeeders`,
   - selecting or referencing published service offers,
   - projecting remote paid steps into host procurement,
   - preserving local audit joins,
   - performing local packaging and final notification.

2. `provider nodes`

   The Nodes of Ola, Adam, and Marcin publish standing service offers and execute
   accepted work through host-owned runtime adapters.

3. `gateway node`

   A trusted gateway node converts external money into internal `ORC` balances and
   emits signed `gateway-receipt.v1` artifacts.

4. `escrow supervisor node`

   A trusted escrow-capable node creates and releases `ledger-hold.v1` facts,
   enforces settlement timeout semantics, and preserves the settlement-side audit
   trail for paid procurement.

5. `service-catalog listener/indexer`

   A catalog service or Node listens to exchange-offer publications on the
   commercial exchange channel, indexes active `service-offer.v1` artifacts, and
   exposes search/browse surfaces to buyers.

6. `arbiter node` (optional or policy-dependent)

   For `arbiter-confirmed` or disputed paths, a named arbiter role may decide the
   terminal release or refund outcome. In hard MVP this role may be co-located with
   the escrow supervisor, but it remains logically distinct.

The smallest acceptable hard-MVP deployment therefore is:

- one buyer-orchestrator Node (`Roman` / `CasualFeeders`),
- one combined `gateway + escrow + catalog` deployment,
- one or more provider Nodes (`Ola`, `Adam`, `Marcin`).

### Service Configuration and Publication

3. Ola configures `Dator` with the local language model `Bielik`. `Dator` does not
   speak to the model directly; instead it proposes a `MiddlewareDecision` that
   requests model invocation, and the Node's model-runtime layer executes it under
   the Node's own transport, retention, and trace policies.

4. Ola publishes one `service-offer.v1` through `Dator` for Polish text redaction:

   ```
   offer/id:              "offer:ola-redaction-01"
   provider/participant-id: "participant:did:key:z6MkOla..."
   provider/node-id:      "node:did:key:z6MkOla..."
   service/type:          "text/redaction"
   pricing/amount:        1000
   pricing/currency:      "ORC"
   pricing/unit:          "1800 input characters"
   delivery/max-duration: 3600          # 1 hour
   hybrid:                true
   model-first:           true
   queue/auto-accept:     false         # Ola reviews orders manually
   queue/max-depth:       3
   seq:                   1
   ttl:                   86400         # 24 hours
   ```

   The `hybrid: true` flag means the service involves both model output and human
   intervention by Ola. The protocol-visible metadata makes this explicit — the
   buyer knows this is not pure automation.

   The `model-first: true` flag means the processing order is: model draft first,
   then Ola's manual refinement.

   The host validates and signs the offer with Ola's `participant:did:key`, then
   publishes it to the exchange channel.

5. Adam configures his `Dator` instance with `GPT-5` through the Node's
   OpenAI-backed runtime adapter. `Dator` does not call the vendor API directly;
   the Node's runtime layer owns provider credentials, transport policy, and
   request tracing.

6. Adam publishes a `service-offer.v1` for topical-news research:

   ```
   offer/id:              "offer:adam-news-01"
   provider/participant-id: "participant:did:key:z6MkAdam..."
   provider/node-id:      "node:did:key:z6MkAdam..."
   service/type:          "research/topical"
   pricing/amount:        200
   pricing/currency:      "ORC"
   pricing/unit:          "1 summary item"
   constraints/output:    { char_limit: 1000, urls_required: true }
   delivery/max-duration: 1800          # 30 minutes
   hybrid:                false
   queue/auto-accept:     true
   queue/max-depth:       5
   seq:                   1
   ttl:                   86400
   ```

   With `auto-accept: true` and `max-depth: 5`, Adam's Node automatically accepts
   work orders up to queue depth 5. Above that, the service is presented as
   temporarily unavailable (queue-saturated).

7. Marcin configures his `Dator` instance against a diffusion-style image model
   exposed through an OpenAI-like API. As with the others, `Dator` consumes the
   Node's normalized runtime surface.

8. Marcin publishes a `service-offer.v1` for illustration generation:

   ```
   offer/id:              "offer:marcin-illust-01"
   provider/participant-id: "participant:did:key:z6MkMarcin..."
   provider/node-id:      "node:did:key:z6MkMarcin..."
   service/type:          "image/generation"
   pricing/amount:        500
   pricing/currency:      "ORC"
   pricing/unit:          "1 illustration"
   constraints/output:    { max_width: 1920, max_height: 1080, max_size_mb: 10 }
   delivery/max-duration: 900           # 15 minutes
   hybrid:                false
   queue/auto-accept:     true
   queue/max-depth:       3
   seq:                   1
   ttl:                   86400
   ```

### Funding

9. Roman uses an Orbiplex payment gateway node to add `500.00 ORC` to the
   `CasualFeeders` organization account. He pays `500.00 PLN` through an external
   payment rail. The gateway performs an atomic split:

   - `450.00 ORC` credited to `org:did:key:z6MkCF...` account,
   - `50.00 ORC` (10% ingress fee) credited to `community-pool`.

   The gateway emits a signed `gateway-receipt.v1`:

   ```
   receipt/id:                  "gw:01JVGW001"
   gateway/node-id:             "node:did:key:z6MkGW..."
   direction:                   "inbound"
   external/amount:             500.00
   external/currency:           "PLN"
   fee/external-amount:         50.00
   fee/rate:                    0.10
   fee/destination-account-id:  "account:fed-pl-main:community-pool"
   net/external-amount:         450.00
   internal/amount:             45000
   internal/fee-amount:         5000
   internal/currency:           "ORC"
   account/id:                  "account:fed-pl-main:casualfeeders"
   gateway-policy/ref:          "gateway-policy:pl-main-prepaid-v1"
   ts:                          "2026-04-01T06:00:00Z"
   ```

   The fee is visible, auditable, and automatically routed. Roman sees exactly how
   much goes to the organization and how much to the community pool.

### Discovery

10. Roman opens a service-catalog interface that listens to exchange-offer
    publications on the dedicated commercial exchange channel. The catalog is a
    listener and indexer: it discovers active offers by observing signed
    `service-offer.v1` artifacts rather than by privately curating them.

11. Roman searches the catalog for:
    - text redaction,
    - illustration generation,
    - news collection.

    The catalog returns active service offers published by the Nodes of Ola, Marcin,
    and Adam, including pricing, queue posture, declared capabilities, hybrid flags,
    and input/output constraints.

### Workflow Definition

12. Roman uses his Node together with the `Orbiplex Arca` middleware to define a
    recurring workflow. `Arca` acts as a workflow orchestrator within the host's
    middleware chain — it proposes `MiddlewareDecision` sequences, the host validates
    and executes them.

13. The workflow is scheduled to run every morning. It consists of four phases:

    **Phase 1 — News Research (remote, paid)**
    Two parallel service-order submissions to Adam's Node. In the current executable
    substrate these become host-side selection plus `procurement-contract.v1`
    creation rather than a dedicated `service-work-order.v1` wire artifact:
    - three top Polish breakfast-related news summaries,
    - three top Polish lunch-related news summaries.
    Each order carries keywords and negative terms to reduce content repetition.
    Buyer identity: `org:did:key:z6MkCF...` (CasualFeeders).

    **Phase 2 — Text Redaction (remote, paid)**
    Six service-order submissions to Ola's Node — one per research
    output from Phase 1.
    Buyer identity: `org:did:key:z6MkCF...`.

    **Phase 3 — Illustration Generation (remote, paid)**
    Six service-order submissions to Marcin's Node — one per revised
    text from Phase 2.
    Buyer identity: `org:did:key:z6MkCF...`.

    **Phase 4 — Local Packaging (local, unpaid)**
    Roman's own Node uses a local LLM to format the six text-plus-illustration
    pairs into files ready for WordPress import. This step is local to
    `CasualFeeders` and does not involve the exchange lifecycle.

### Execution: Phase 1 — News Research

14. For each work order in Phase 1, the host on Roman's Node:
    - performs a funding precheck against `org:did:key:z6MkCF...` account
      (sufficient balance for `2.00 ORC × 3 items × 2 orders = 12.00 ORC`),
    - requests escrow hold from the escrow supervisor node,
    - creates `procurement-contract.v1` with `settlement/rail: host-ledger`.

    The escrow supervisor creates a `ledger-hold.v1`:

    ```
    hold/id:               "hold:01JV-ph1-news"
    contract/id:           "contract:01JV-ph1"
    payer/account-id:      "account:fed-pl-main:casualfeeders"
    payee/account-id:      "account:fed-pl-main:adam"
    escrow/node-id:        "node:did:key:z6MkESC..."
    escrow-policy/ref:     "escrow-policy:pl-main-standard-v1"
    amount:                1200
    unit:                  "ORC"
    status:                "active"
    created-at:            "2026-04-01T06:05:00Z"
    work-by:               "2026-04-01T08:00:00Z"
    accept-by:             "2026-04-01T09:00:00Z"
    dispute-by:            "2026-04-01T09:00:00Z"
    auto-release-after:    "2026-04-01T10:00:00Z"
    ```

15. Adam's Node receives the two work orders, checks queue capacity (currently 0 of
    5 — accepted), reserves execution slots, and executes the news-research service
    through the Node runtime backing `GPT-5`.

16. Adam's Node returns six structured research outputs with URLs, plus delivery
    metadata. In the current executable substrate the delivered payload is carried
    by `response-envelope.v1`, while the terminal economic outcome is recorded later
    as `procurement-receipt.v1` after acceptance, rejection, expiry, cancel, or
    auto-release.

    The response payload for each completed order carries at least:

    ```
    response/id:           "response:01JV-adam-001"
    question/id:           "question:01JV-ph1-breakfast"
    contract/id:           "contract:01JV-ph1"
    source/participant-id: "participant:did:key:z6MkAdam..."
    provenance/type:       "model-only"
    provenance/model:      "gpt-5"
    delivery/ts:           "2026-04-01T06:18:00Z"
    ```

### Execution: Phase 2 — Text Redaction

17. For each of the six research outputs, Roman's workflow submits one priced
    service-order request to Ola's Node. Funding precheck, escrow hold, and
    `procurement-contract.v1` creation follow the same pattern as Phase 1
    (`6 × 10.00 ORC = 60.00 ORC` held).

18. Ola's Node first runs the `Bielik`-backed model phase (model-first), producing
    an initial draft. Then Ola performs the manual follow-up implied by the `hybrid`
    and `model-first` service flags.

19. Ola's Node returns six revised Polish texts. Each delivered response carries
    hybrid provenance in the response payload or linked delivery metadata:

    ```
    provenance/type:       "hybrid"
    provenance/model:      "bielik"
    provenance/human:      true
    provenance/sequence:   ["model-draft", "human-refinement"]
    ```

    This makes provenance protocol-visible without leaking the specific nature of
    Ola's editorial process.

### Execution: Phase 3 — Illustration Generation

20. For each revised text, Roman's workflow submits an illustration task to Marcin's
    Node, constrained by the declared maximum dimensions and file size from the
    service offer. Funding precheck, escrow hold, and contract creation follow the
    same pattern (`6 × 5.00 ORC = 30.00 ORC` held).

21. Marcin's Node accepts and queues those image-generation tasks up to the published
    queue limit (3 active, so 6 tasks are processed in two batches of 3), executes
    them through the configured diffusion runtime, and returns the resulting
    illustrations plus delivery metadata.

    Each delivered response carries:

    ```
    provenance/type:       "model-only"
    provenance/model:      "diffusion-xl"
    ```

### Settlement

22. After each successful delivery and acceptance or terminal timeout handling, the
    escrow supervisor releases or refunds the held funds. In the current Node
    substrate:

    - delivery is followed by participant-side `response/accept`,
      `response/reject`, or `dispute/file`,
    - `self-confirmed` contracts may auto-release after `deadlines/auto-release`,
    - terminal economic closure is persisted as `procurement-receipt.v1`.

    On the happy path the releases are:

    ```
    For Phase 1 (Adam):    12.00 ORC released to participant:did:key:z6MkAdam...
    For Phase 2 (Ola):     60.00 ORC released to participant:did:key:z6MkOla...
    For Phase 3 (Marcin):  30.00 ORC released to participant:did:key:z6MkMarcin...
    Total spent:          102.00 ORC from CasualFeeders account (of 450.00 ORC available)
    ```

    Each release produces one or more `ledger-transfer.v1` facts from hold to payee,
    and the terminal contract outcome is recorded in `procurement-receipt.v1`.

    If a buyer does not explicitly accept or dispute by `dispute-by`, the escrow
    auto-releases at `auto-release-after`. This prevents indefinite fund lockup
    (griefing protection).

### Local Packaging and Output

23. After all six texts and illustrations are available, Roman's local workflow
    (Phase 4) uses one local LLM through his own Node to format the material into
    separate files ready for WordPress import. This last stage is local to
    `CasualFeeders` — it is not outsourced and does not produce exchange artifacts.

24. `Arca` writes the generated publication files into the configured local directory
    and emits a completion notification so that Roman or another editorial operator
    can review or publish them.

### Audit Trail

25. Throughout the flow, each priced remote task produces explicit records linking:

    - buyer identity (`org:did:key:z6MkCF...`) and acting custodian
      (`participant:did:key:z6MkR...`),
    - provider `participant:did:key` and `node:did:key`,
    - accepted offer snapshot or catalog snapshot captured at order time,
    - `procurement-contract.v1` with agreed terms,
    - escrow hold reference and escrow supervisor node identity,
    - price, quantity, and unit basis,
    - queue acceptance or rejection outcome,
    - `response-envelope.v1` with delivery payload and provenance metadata,
    - `procurement-receipt.v1` with terminal economic outcome,
    - settlement transfer references,
    - gateway fee contribution to community pool (traceable from initial top-up).

26. Roman can later audit the complete morning pipeline not only as an application
    workflow but also as a chain of explicit service exchanges:
    - Adam provided topical news procurement (model-only, GPT-5),
    - Ola provided hybrid human-plus-model redaction (Bielik + manual),
    - Marcin provided illustration generation (model-only, diffusion),
    - Roman's own Node performed local packaging for WordPress (no exchange).

    Each step has a named decision author, auditable provenance, and a settlement
    trail that traces back to the original gateway top-up — including the community
    pool contribution.

## Error Scenarios

### Queue Saturation

If Marcin's queue is full (3 active tasks) when Roman's workflow submits 6
illustration tasks, the first 3 are accepted and the remaining 3 receive an
application-level order rejection or temporary-unavailability outcome
(`queue-saturated`). This MUST NOT be modeled as `E_PROTO_CAP_MISSING`, because that
code belongs to transport or capability-contract mismatch, not to business-level
availability. `Arca` should retry with backoff until slots become available,
respecting the offer's `delivery/max-duration` as an outer timeout.

### Provider Timeout

If Ola does not deliver redacted text within `delivery/max-duration` (1 hour),
Roman's workflow may:
- wait for auto-release of escrow (funds returned to CasualFeeders),
- emit a `reputation-signal.v1` with `signal/type: "contract/delivery-timeout"`,
  `polarity: negative`, `subject/kind: participant`,
  `subject/id: participant:did:key:z6MkOla...`.

### Participant Restrictions

If a provider carries an active participant-level hard block for
`procurement/offer` or `response/deliver`, the workflow should treat that as a
policy-level rejection of the paid path rather than as transport failure.

If the buyer carries an active hard block for `response/accept` or
`response/reject`, the workflow must not pretend the acceptance path is still
available. The protected-floor path `dispute/file` remains admissible and should stay
available as the bounded escalation route.

### Dispute

If Roman is dissatisfied with Adam's research output, he may file a dispute by the
contract or hold dispute deadline (`deadlines/dispute-by` on the contract,
`dispute-by` on the hold). The arbiter reviews the contract terms, the delivered
output, and the offer snapshot, then decides:
- full release to provider (work acceptable),
- full refund to buyer (work unacceptable),
- partial release (work partially acceptable — post-MVP).

The dispute decision has a `decision/author` and `reason/ref` per the named-decisions
principle.

### Partial Pipeline Failure

If Phase 1 succeeds but Phase 2 fails (Ola's Node unreachable), `Arca` should:
- hold Phase 1 outputs locally,
- retry Phase 2 with backoff,
- not proceed to Phase 3 until Phase 2 completes,
- respect an outer workflow timeout after which the entire pipeline is marked as
  failed and remaining holds are released.

`Arca` does not independently decide to substitute a different provider — that would
require buyer authorization (Roman's explicit decision or a pre-configured fallback
policy).

## Trace Events

The implementation should preserve the following domain transitions as auditable
facts. In MVP this does not require a brand-new trace family: the Node may realize
them through existing committed records, `execution/transition`, participant-side
`response/*-requested`, `dispute/file`, settlement artifacts, and `trace/middleware`.

```
offer/publication                — standing offer published or refreshed in catalog layer
offer/expiration                 — standing offer TTL reached or was withdrawn
order/submitted                  — buyer-side orchestration submitted one priced task
order/accepted                   — provider accepted (auto or manual)
order/rejected                   — provider rejected (queue full, policy, etc.)
execution/transition             — execution moved through append-only lifecycle states
response/delivered               — provider returned one response payload
response/accept-requested        — buyer-side participant accepted delivery
response/reject-requested        — buyer-side participant rejected delivery
dispute/opened                   — buyer-side participant opened dispute within window
settlement/hold-created          — escrow hold reserved funds
settlement/hold-released         — hold released to provider
settlement/hold-refunded         — hold refunded to buyer
settlement/receipt-persisted     — terminal procurement receipt committed
workflow/phase-started           — Arca started a workflow phase
workflow/phase-completed         — phase completed successfully
workflow/phase-failed            — phase failed, retry or abort
workflow/completed               — entire workflow completed
workflow/timeout                 — outer workflow timeout reached
```

## Open Continuation

- Exact schema for a future service-publication family such as `service-offer.v1`
  and `service-work-order.v1`, if the project still wants a distinct layer above the
  already frozen procurement family.
- Whether a future service-specific family should wrap, alias, or simply project to
  `procurement-contract.v1`, `response-envelope.v1`, and `procurement-receipt.v1`
  rather than creating a second contract universe.
- Whether catalog listeners should index only currently valid offers or also keep
  bounded historical offer snapshots for audit and reputation purposes.
- How queue depth, `auto-accept`, and saturation state should be represented so that
  remote buyers do not race on stale availability.
- How hybrid human-plus-model services should expose provenance granularity beyond
  `provenance/sequence` without leaking more operator detail than necessary.
- How `Arca` should represent idempotent retries and partial failure recovery,
  including whether fallback provider substitution requires explicit buyer
  authorization or can be pre-configured as policy.
- Whether `service-offer.v1` should carry a `reputation/min-threshold` field
  allowing providers to reject buyers below a certain reputation level.
- How the exchange publication channel relates to the existing peer gossip and
  node-advertisement propagation — shared transport, separate channel semantics.
- Whether `CasualFeeders` as `org:did:key` should be able to delegate signing
  authority to multiple custodians with threshold or rotation policies (post-MVP).
