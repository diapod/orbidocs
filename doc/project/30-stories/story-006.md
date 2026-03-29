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
- a Node may act both as an individual participant and as an organization-bound
  operator when it holds the right key material or delegated signing authority,
- service advertisements can be propagated over a dedicated commercial or exchange
  publication channel, allowing external catalogs to index active offers without
  becoming the only authority over them,
- settlement remains explicit and auditable in ORC credits, while fiat onboarding or
  gateway funding may exist at the ecosystem edge without redefining the protocol
  core,
- local or remote model execution remains transport-agnostic from the perspective of
  the exchange plugin itself: the plugin asks the Node for model-backed work rather
  than integrating provider APIs on its own.

This story is not about speculative high-frequency automation or adversarial market
behavior. It is about a cooperative voluntary exchange where priced services,
workflow composition, provenance, and bounded automation all remain visible.

## Sequence of Steps

1. Ola, Adam, and Marcin each run an Orbiplex Node with the standard `Orbiplex Dator`
   middleware attached. `Dator` is the exchange-facing module responsible for
   advertising service offers, receiving work orders, and reporting bounded delivery
   and settlement outcomes.
2. Each Node already has a stable persisted `node-id`, local operator identity, and a
   settlement-capable ORC account or equivalent credit-bearing profile suitable for
   accepting paid work.
3. Ola configures `Dator` with the local language model `Bielik`. `Dator` does not
   speak to the model directly; instead it asks the Node's model-runtime surface to
   invoke the configured LLM under the Node's own transport, retention, and trace
   policies.
4. Ola publishes one service offer through `Dator` for Polish text redaction. The
   offer declares at least:
   - Polish-language editing intent,
   - price `10 ORC` per `1800` input characters,
   - expected completion within one hour,
   - `hybrid = true`,
   - `model-first = true`.
5. The `hybrid = true` flag means the service is not represented as a pure machine
   completion. The protocol-visible service metadata makes clear that the work is
   expected to involve both model output and later human intervention by Ola.
6. The `model-first = true` flag means the initial processing order is explicit:
   - the Node should first obtain a draft or pre-redaction from the configured model,
   - then Ola performs the later manual refinement phase.
7. Adam configures his `Dator` instance with `GPT-5` through the Node's OpenAI-backed
   runtime adapter. Again, `Dator` does not call the vendor API directly; the Node's
   runtime layer owns provider credentials, transport policy, and request tracing.
8. Adam publishes a topical-news research offer. The offer declares at least:
   - topical-event research for the last hours,
   - output as a list of approximately `1000`-character bullet summaries,
   - source URLs required in every output item,
   - caller-provided output count,
   - caller-provided output language,
   - price `2 ORC` per summary item.
9. Adam enables automatic acceptance and queueing up to a queue depth of `5`. Above
   that threshold, `Dator` should stop auto-accepting new work and should instead
   present the service as temporarily unavailable or queue-saturated.
10. Marcin configures his `Dator` instance against a diffusion-style image model
    exposed through an OpenAI-like API. As with the others, `Dator` consumes the
    Node's normalized runtime surface rather than directly integrating the model API.
11. Marcin publishes an illustration-generation offer. The offer declares at least:
    - one illustration per accepted task,
    - text-prompted generation,
    - price `5 ORC` per illustration,
    - maximum dimensions `1920x1080`,
    - maximum file size `10 MB`,
    - automatic acceptance with queueing up to `3` active tasks.
12. Roman runs his own Orbiplex Node and acts on behalf of the organization
    `CasualFeeders`, which already has an Orbiplex organization identity and for
    which Roman controls or is delegated the necessary signing authority.
13. On the `CasualFeeders` side, Roman also runs a WordPress-based editorial site
    where short food-related news items with images are published on a schedule.
14. Roman uses an Orbiplex payment gateway or funding rail to add `500 ORC` to the
    organization's balance by paying `500 PLN`. The exact fiat rail is out of scope
    for the protocol core, but the Node records the resulting ORC balance as usable
    operational funds.
15. Roman opens a service-catalog page that listens to exchange-offer publications on
    the dedicated commercial exchange channel. The catalog is a listener and indexer:
    it discovers active offers by observing signed service advertisements rather than
    by privately curating them out of band.
16. Roman searches the catalog for:
    - text redaction,
    - illustration generation,
    - news collection.
    The catalog returns active service offers published by the Nodes of Ola, Marcin,
    and Adam.
17. From the catalog Roman obtains the stable service identifiers and relevant offer
    metadata for those three providers, including pricing, queue posture, declared
    capabilities, and accepted input/output constraints.
18. Roman then uses his own Node together with the `Orbiplex Arca` middleware to
    define a recurring workflow. `Arca` acts as a workflow orchestrator, not as the
    authority over service exchange semantics.
19. The workflow is scheduled to run every morning. Its first two remote steps submit
    separate paid orders to Adam's Node:
    - three top Polish breakfast-related news summaries,
    - three top Polish lunch-related news summaries.
    Each request carries keywords and negative terms to reduce content repetition.
20. Adam's Node receives the two work orders, checks queue capacity, reserves the
    corresponding execution slots, and executes the news-research service through the
    Node runtime backing `GPT-5`.
21. After Adam's Node returns six structured research outputs with URLs, Roman's
    workflow submits those six texts as redaction tasks to Ola's Node.
22. Ola's Node first runs the configured `Bielik`-backed model phase, then Ola
    performs the manual follow-up implied by the `hybrid` and `model-first` service
    flags, and finally the Node returns six revised Polish texts together with the
    service-result provenance required by the exchange flow.
23. For each revised text, Roman's workflow submits an illustration task to Marcin's
    Node, constrained by the declared maximum size and dimensions of the offer.
24. Marcin's Node accepts and queues those image-generation tasks up to the published
    queue limit, executes them through the configured diffusion runtime, and returns
    the resulting illustrations plus delivery metadata.
25. After all six texts and illustrations are available, Roman's local workflow uses
    one local LLM through his own Node to format the material into separate files
    ready for WordPress import. This last formatting stage is local to
    `CasualFeeders`; it is not outsourced to the previously selected remote service
    providers.
26. `Arca` writes the generated publication files into the configured local directory
    and emits a completion notification so that Roman or another editorial operator
    can review or publish them.
27. Throughout the flow, each priced remote task produces explicit exchange records at
    least linking:
    - buyer identity or acting organization identity,
    - provider node and service id,
    - accepted offer snapshot,
    - price and quantity basis,
    - queue or acceptance outcome,
    - delivery result,
    - settlement result or payable obligation.
28. Roman can later audit the complete morning pipeline not only as an application
    workflow but also as a chain of explicit service exchanges:
    - Adam provided topical news procurement,
    - Ola provided hybrid human-plus-model redaction,
    - Marcin provided illustration generation,
    - Roman's own Node performed local packaging for WordPress.

## Open Continuation

- Exact schema family for exchange offers, service ids, work orders, receipts, and
  settlement records.
- Whether catalog listeners should index only currently valid advertisements or also
  keep bounded historical offer snapshots for audit and reputation purposes.
- How queue depth, `auto-accept`, and saturation state should be represented so that
  remote buyers do not race on stale availability.
- How hybrid human-plus-model services should expose provenance without leaking more
  operator detail than necessary.
- Whether organization-acting identities such as `CasualFeeders` should sign orders
  directly, through delegated operator signatures, or through a two-layer actor model.
- How Arca should represent idempotent retries and partial failure recovery when one
  provider succeeds and a later provider rejects or delays execution.
