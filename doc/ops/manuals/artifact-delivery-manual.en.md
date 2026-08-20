# Operator's Manual: Artifact Delivery

Artifact Delivery is the host-owned service for sending and receiving artifacts
described by data schemas. A component states what it wants to deliver and to
whom; the host selects the route and adapter, handles retries, receives inbound
data, and exposes its status to the operator.

The [Artifact Delivery FAQ](../faq/artifact-delivery-faq.en.md) introduces the
concepts. The [Artifact Delivery HOWTO](../howto/artifact-delivery-howto.en.md)
contains integration examples, configuration guidance, and operating sequences.
This manual does not repeat those examples. It collects limits, failure codes,
trust boundaries, durable state, and default values.

## 1. Purpose and functions

Artifact Delivery exists so that **components do not have to manage transport
themselves**. A component declares an artifact and its recipients. The host
selects a route and adapter, handles retries and recovery, receives inbound
data, and shows status to the operator.

Functions:

- accept an `artifact-delivery-envelope.v1` from a component and reduce it to a delivery plan,
- resolve recipients through named selectors, groups and routes,
- enforce outbound authority per component, schema and selector class,
- select a transport adapter and execute the plan with fallbacks,
- persist deliveries and intake decisions and recover deferred deliveries,
- direct inbound data to **exactly one authoritative domain receiver
  (`acceptor`)** for each artifact kind,
- expose a current status and diagnostics view to the operator.

## 2. How it works

On the outbound path, a component calls `artifact.delivery.send` with an
envelope. The host checks the envelope and the sender's authority, resolves the
recipients, expands the plan into concrete targets, and executes it through
adapters. The result is an `artifact-delivery-result.v1`; the overall delivery
state and every target state are persisted.

The inbound path has two stages that must not be conflated:

1. **Preflight check (`preflight`)** — an optional early check owned by the
   schema owner. It may **reject** an artifact or attach hints (`Abstain`,
   `Continue { hints }`, `Reject { failure_class, message, retryable }`). It may
   inspect the artifact descriptor and a small payload carried directly in the
   envelope before the host fetches the content named by `artifact/ref`.
   **A preflight check cannot accept an artifact.**
2. **Domain receiver (`acceptor`)** — a registered `InboundArtifactAcceptor` is
   the **only path that can accept an artifact**. Exactly one authoritative
   receiver exists for each (schema, content type) pair.

Dispatch is closed when configuration is missing (`fail-closed`). If no receiver
exists for an artifact kind, the host returns `kind-not-supported` instead of
accepting the data by default.

Large payloads are not carried directly in the envelope. Above that threshold,
the host uses the object store. The `object_store_indirect` adapter sends an
`artifact-object-pointer.v1`, and the receiver fetches the actual bytes through
`POST /v1/artifact-delivery/object-store/fetch` with a registry token.

## 3. Architectural placement and communication channels

Artifact Delivery sits **between components and transport mechanisms**. Agora is
the public topic relay, [INAC](inac-manual.en.md) is the private node-to-node
transport, Matrix mailbox stores data until it can be forwarded, and the object
store keeps content locally. Artifact Delivery replaces none of them; it selects
the appropriate mechanism for a delivery plan.

| Channel | Direction | Justification |
| --- | --- | --- |
| `POST /v1/host/capabilities/artifact.delivery.send` | inbound, component → host | The only entry point for delivery intent. Requires an outbound allow. |
| `artifact.delivery.status` | read, component → host | A component asks about its own delivery without reaching another's. |
| `artifact.delivery.submit` | inbound, component → host | Submits an artifact for delivery in the deferred variant. |
| `daemon.agora-publish` adapter | outbound, host → Agora | Topic publication. The adapter's error body is truncated to 16 KiB so a remote service cannot flood the log. |
| `daemon.inac-direct` adapter | outbound, host → peer | Private direct delivery. Stream sends split the payload into 24 KiB chunks. |
| `matrix_mailbox` adapter | bidirectional, host ↔ homeserver | Store-and-forward when a peer is not directly reachable. |
| `object-store-indirect` adapter | outbound, host → peer (pointer) | Large payloads travel as a pointer, not as bytes in the envelope. |
| `POST /v1/artifact-delivery/admissions` | inbound, source adapter → host | Intake through the control interface. When the allowed source-adapter list is empty, the host denies every source (`deny-all`). |
| `POST /v1/artifact-delivery/object-store/fetch` | inbound, receiver → host | Fetches the bytes of an indirect delivery with a registry token. |
| Receivers in HTTP-supervised modules (`supervised-HTTP`) | outbound, host → middleware module | The host passes the artifact to a module through a local interface; the response has size and time limits. |
| JSON-e Flow and in-process receivers | internal, host → domain | The target domain decides authority; transport does not grant it. |
| `GET /v1/artifact-delivery/{deliveries,admissions,routes}` | read, operator → host | Operator projections; they grant no authority. |
| `POST /v1/artifact-delivery/recover` | write, operator → host | Manual recovery run alongside the background worker. |
| SQLite registry | read/write, local disk | Durable deliveries, targets, and intake decisions. |

## 4. Data contracts

| Schema | Purpose of use | Channel |
| --- | --- | --- |
| `artifact-delivery-envelope.v1` | Delivery intent declared by a component: artifact, recipients, plan. | `artifact.delivery.send` |
| `artifact-delivery-result.v1` | Delivery result returned to the component. | response to `send`/`submit` |
| `artifact-delivery-status.v1` | Current view of the delivery and target states. | `GET /v1/artifact-delivery/deliveries/{id}` |
| `artifact-delivery-recovery.v1` | Recovery contract for deferred deliveries. | background worker and `POST …/recover` |
| `artifact-object-pointer.v1` | Object reference when bytes are not carried directly in the envelope. | `object-store-indirect` adapter |
| `artifact-mailbox-sealed.v1` | Sealed Matrix mailbox payload. | `matrix_mailbox` adapter |
| `artifact-mailbox-chunk.v1` | Mailbox payload chunk above the event limit. | `matrix_mailbox` adapter |
| `routing-subject-binding.v1` | Routing-subject binding during recipient resolution. | route resolution |
| `capability-proof-presentation-batch.v1` | Batched capability proof presentation; a built-in acceptor. | inbound admission |

Artifacts **carried** by this service (`agora-record.v1`, `memarium-blob.v1`,
`contact-request.v1`, `corpus-*`, `capability-passport-present.v1`,
`federation-service-endorsement.v1`) belong to their own domains, not to
Artifact Delivery. The service knows their schemas only to select the correct
receiver.

## 5. Limits and behaviour when exceeded

| Ceiling | Default | Behaviour when exceeded | Configurable |
| --- | --- | --- | --- |
| Resolved artifact | 64 MiB | failure `runtime-limit` | no |
| Payload carried directly in the envelope | 64 KiB | above it the payload goes through the object store | no |
| Indirect delivery threshold | 1 MiB | above it a pointer is sent instead of bytes | yes — `object_store_indirect.threshold_bytes` |
| Object in the store | 256 MiB | write rejected | yes — `object_store.max_object_bytes` |
| Object store retention | 7 days | object removed | yes — `object_store.retention_seconds` |
| INAC stream chunk on send | 24 KiB | a fixed value, not a ceiling | no |
| Remote-node artifact cache | 4096 entries / 256 MiB | oldest entries removed; cleanup every 64 writes | yes — `matrix_mailbox` configuration |
| `supervised-HTTP` receiver response | 64 KiB | failure `adapter-permanent` | yes — `…acceptor_response_limit_bytes` |
| Receiver response time | 5000 ms | `admission-timeout` | yes — `…acceptor_request_timeout_ms` |
| Agora adapter error body | 16 KiB | truncated in diagnostics | no |
| Artifact store reference suffix | 1024 B | rejected | no |
| Recovery batch | 32 deliveries | the rest waits for the next pass | yes — `artifact_delivery_recovery.batch_limit` |
| Budget for one recovery pass | 4000 ms | the pass ends, the rest waits | yes — `…pass_deadline_ms` |
| Profiling "large payload" threshold | 1 MiB | flagged in diagnostics | yes — `artifact_delivery_profiling…` |

## 6. Failure and status vocabularies

A failure is a **class**, not a text. Twelve classes:

| Class | Meaning | Retryable? |
| --- | --- | --- |
| `envelope-malformed` | The envelope does not satisfy the schema. | No. |
| `envelope-invalid` | The envelope parses but is semantically inconsistent. | No. |
| `route-unresolved` | No route or recipients could be resolved. | No, until routes change. |
| `admission-conflict` | A conflict while the receiver is admitting the artifact. | No. |
| `kind-not-supported` | No receiver for this artifact kind. | No, until a receiver is registered. |
| `outbound-denied` | No outbound authority for this component, schema or selector. | No, until policy changes. |
| `adapter-transient` | The adapter failed transiently. | **Yes.** |
| `adapter-permanent` | The adapter failed permanently. | No. |
| `stage-timeout` | A plan stage ran out of time. | **Yes.** |
| `admission-timeout` | The receiver did not answer in time. | **Yes.** |
| `ledger-error` | The durable registry could not be read or written. | **Yes.** |
| `runtime-limit` | An execution ceiling was exceeded. | Not in this shape. |

Delivery status (7): `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`, `expired`.
Per-target status (4): `pending`, `succeeded`, `failed-retryable`, `failed-permanent`.
Inbound intake status (4): `accepted`, `already-present`, `rejected`, `retryable`.

`partial` is a first-class state, not a malfunction: some targets may have succeeded. `already-present` is an idempotent success.

## 7. Authority and its revocation

Host capabilities: `artifact.delivery.send`, `artifact.delivery.status`, `artifact.delivery.submit` (`host/*`).

Outbound authority comes from `artifact_delivery.outbound/allows`. Each entry
binds a component to permitted artifact schemas, recipient selector classes,
routes, target nodes, maximum recipient count, fallback-route count, and byte
limit. No matching entry produces `outbound-denied`.

Inbound authority has two separate gates:

- `artifact_delivery_acceptors.http_admission_allowed_source_adapters` — an
  **empty list denies every source (`deny-all`)** at the HTTP entry point.
  In-process transport adapters may still call the runtime directly.
- receiver registration — no entry for an artifact kind means
  `kind-not-supported`.

Revocation takes effect on the next use. Changing `outbound/allows` may block
later sends, and unregistering a receiver blocks later intake attempts.
Deliveries already stored in the registry keep their state: revocation does not
rewrite history.

## 8. Trust boundaries

| What | Who verifies it |
| --- | --- |
| Envelope conformance | Artifact Delivery, before any effect. |
| A component's outbound authority | Artifact Delivery, from `outbound/allows`. |
| Peer identity | The transport's peer session (INAC/WSS), not Artifact Delivery. |
| Payload digest and size | The transport adapter (per chunk for INAC) and the host during resolution. |
| Eligibility of the artifact kind | The receiver registry; no entry means refusal. |
| **The artifact's domain authority** | **Not Artifact Delivery.** The receiver and target domain decide it. Successful transport intake grants no domain authority. |
| Target custody space for `memarium-blob.v1` | **Daemon-local policy**, never the sender. Default `public`, allowed `["public"]`; `crisis` is rejected by config validation. |
| The preflight verdict | A preflight check may reject an artifact or attach hints; it **cannot accept** it. |

Two rules matter most. First, **transport intake never means domain consent**.
For `contact-request.v1`, it only permits the preflight check and contact-request
receiver to run. Second, **the sender does not select the custody space**. This
is a local decision because Memarium spaces apply local policy to stored data.

## 9. Dependencies and degraded modes

Requires the SQLite registry, artifact object store, and at least one configured
transport adapter. `supervised-HTTP` receivers require the middleware
supervisor; JSON-e Flow receivers require the Flow runtime.

Provides one delivery interface for every component and one inbound intake path
for every transport, including [INAC](inac-manual.en.md).

Degraded modes:

- **Adapter unavailable** — `adapter-transient`; the delivery receives
  `failed-retryable` and waits for the background recovery task.
- **Receiver not answering** — `admission-timeout`; the intake attempt is
  `retryable`, not permanently rejected.
- **Registry unavailable** — `ledger-error`; the operation is retryable because
  a registry failure is not a judgment about the artifact.
- **Recovery disabled** (`artifact_delivery_recovery.enabled = false`) — deferred deliveries wait for a manual `POST /v1/artifact-delivery/recover`.
- **Partial multi-recipient delivery** — status `partial`; some targets are
  `succeeded`, others `failed-*`. This is a complete outcome, not a runtime
  malfunction.

## 10. Durable state and restart

| Store | Path | Durability | After restart |
| --- | --- | --- | --- |
| Delivery and intake registry | `<data-dir>/storage/artifact-delivery.sqlite` | durable (schema v2) | rebuilt from the database; deferred deliveries return to the recovery queue |
| Object fetch token registry | `<data-dir>/storage/artifact-delivery/object-fetch-tokens.v1.json` | durable | rebuilt; tokens survive restart |
| Remote-node artifact cache | `<data-dir>/storage/artifact-delivery/peer-artifacts` | durable (files) | preserved; entries are removed according to the configured limits |
| Stream assembly | `<data-dir>/storage/artifact-delivery/streams` | durable (files) | see the [INAC manual](inac-manual.en.md) |
| Object store | directory from `object_store.root` | durable | 7-day retention by default |
| Profiling counters | process memory | ephemeral | reset on start |

After restart, a separate background task performs recovery; status reads do
not. The task starts a pass every `interval_ms`, processes at most `batch_limit`
deliveries, and stops the pass after `pass_deadline_ms`.

## 11. Configuration

The HOWTO uses examples to show how to configure the host, package, and
envelope. This section adds the layer merge order and default values.

### Layer composition

The daemon's effective configuration is built in this order, each layer deep-merged over the previous one:

1. **Built-in defaults** — compiled into the daemon, including four receivers
   that run in its process (below).
2. **Factory module configuration** — bundled middleware module fragments.
3. **`<data-dir>/config/*.json`** — every `.json` file in the directory, read in **alphabetical filename order** and deep-merged.
4. **`<data-dir>/control/middleware-settings.json`** — settings applied at runtime by the operator.

A package may supply a proposed configuration fragment, but **effective
authorization comes from the daemon configuration accepted by the operator**.
Invalid JSON in layer 3 stops startup and identifies the affected file; the host
does not apply that configuration partially.

### Top-level keys

| Key | Scope |
| --- | --- |
| `artifact_delivery` | Delivery policy: `defaults`, `groups`, `routes`, `outbound/allows`. |
| `artifact_delivery_adapters` | Adapter behaviour: `agora_publish`, `matrix_mailbox`, `object_store`, `object_store_indirect`. |
| `artifact_delivery_acceptors` | Inbound intake and receiver registration. |
| `artifact_delivery_recovery` | The deferred-delivery recovery task. |
| `artifact_delivery_profiling` | Visibility of profiling counters in status. |
| `artifact_delivery_observers` | Observation events that do not change state. |
| `inac_peer_transport` | INAC receiver-side transport policy — described in the [INAC manual](inac-manual.en.md). |

### Default values

| Option | Default | Note |
| --- | --- | --- |
| `artifact_delivery_recovery.enabled` | `true` | |
| `artifact_delivery_recovery.interval_ms` | 5000 | idle interval between passes |
| `artifact_delivery_recovery.batch_limit` | 32 | deliveries per pass |
| `artifact_delivery_recovery.pass_deadline_ms` | 4000 | budget for one pass |
| `artifact_delivery_profiling.enabled` | `true` | |
| `artifact_delivery_profiling.large_payload_threshold_bytes` | 1 MiB | |
| `artifact_delivery_observers.tracing_enabled` | `false` | metadata-only events |
| `artifact_delivery_acceptors.http_admission_allowed_source_adapters` | `[]` | denies every source (`deny-all`) |
| `…acceptor_request_timeout_ms` | 5000 | |
| `…acceptor_response_limit_bytes` | 64 KiB | |
| `object_store.max_object_bytes` | 256 MiB | |
| `object_store.retention_seconds` | 604800 (7 days) | |
| `object_store_indirect.enabled` | `false` | |
| `object_store_indirect.threshold_bytes` | 1 MiB | |
| `object_store_indirect.control_adapter` | built-in value | |
| `memarium_blob_custody.default_target_space` | `"public"` | |
| `memarium_blob_custody.allowed_target_spaces` | `["public"]` | `crisis` rejected by validation |

### Receivers built into the process

A fresh configuration has four registered receivers. Overriding
`artifact_delivery_acceptors.in_process` **replaces the entire list**. When you
add a receiver, repeat every existing entry that must remain enabled.

| `acceptor_id` | Schema | `invoke` |
| --- | --- | --- |
| `contact-request.local` | `contact-request.v1` | `contact.request` |
| `federation-service-endorsement.install` | `federation-service-endorsement.v1` | `federation-service-endorsement.install` |
| `capability-passport-present.accept` | `capability-passport-present.v1` | `capability-passport-present.accept` |
| `capability-proof-presentation-batch.accept` | `capability-proof-presentation-batch.v1` | `capability-proof-presentation-batch.accept` |

Other `invoke` values available to receivers: `inac.push`,
`agora.record.ingest`, `memarium.inac.accept`, `corpus.query`, `corpus.answer`,
`corpus.room-invite`.

## 12. Observability

| Route | Content |
| --- | --- |
| `GET /v1/artifact-delivery/deliveries?limit={n}` | delivery list |
| `GET /v1/artifact-delivery/deliveries/{delivery_id}` | delivery state and all target states |
| `GET /v1/artifact-delivery/deliveries/{delivery_id}/operation-status` | operation status for the caller |
| `GET /v1/artifact-delivery/admissions?limit={n}` | inbound intake decisions |
| `GET /v1/artifact-delivery/admissions/{admission_id}` | details of one intake decision |
| `GET /v1/artifact-delivery/routes` | resolved routes and selectors |

When `artifact_delivery_profiling.enabled` is enabled, status views contain
payload-preparation and transport counters. Payloads above the configured
threshold are highlighted in diagnostics. The observer
(`observers.tracing_enabled`) emits delivery and intake completion events that
contain **metadata only**, never artifact bytes.

## 13. Cost and resources

Artifact Delivery charges no inference budget. Its material costs:

- **disk** — the SQLite registry, object store (up to 256 MiB per object, kept
  for 7 days), remote-node artifact cache (up to 256 MiB), and stream files,
- **network** — traffic determined by artifact size and recipient count; for
  multi-recipient delivery, recipient count is the dominant multiplier,
- **memory** — payloads up to 64 KiB carried directly in the envelope, plus
  receiver responses up to 64 KiB.

Indirect delivery limits duplication of a large payload across recipients. The
plan carries a small pointer, and only a receiver that needs the content fetches
the actual bytes.

## 14. Contract versions and compatibility

Envelope: `artifact-delivery-envelope.v1`. Result: `artifact-delivery-result.v1`. The SQLite ledger carries its own schema version (currently 2), independent of the contract versions — a ledger migration is not a contract change and requires nothing from components.

## 15. Known limitations

The `Artifact Delivery MVP` implementation-ledger row is `done`. The broader
Solution 023 remains `partial` because two directions are deliberately open:

- the decision about a lower-level zero-copy WebSocket frame split is to be made **from profiling counters**, not up front — which is why profiling is enabled by default,
- Matrix media remains a post-MVP transport variant until deployment evidence requires it.

Additionally, overriding `in_process` replaces the whole built-in receiver
list. This is the component's most common configuration trap.

## 16. Implementation references

| Field | Value |
| --- | --- |
| Component | Artifact Delivery |
| Implementation-ledger row | `Artifact Delivery MVP` (status `done`) |
| Rust crates | `artifact-delivery-core`, `artifact-delivery`, `ad-host`, `memarium-host`, `daemon`, `node-ui` |
| Schemas | `artifact-delivery-envelope.v1`, `artifact-delivery-result.v1`, `artifact-delivery-status.v1`, `artifact-delivery-recovery.v1`, `artifact-object-pointer.v1`, `artifact-mailbox-sealed.v1`, `artifact-mailbox-chunk.v1`, `routing-subject-binding.v1`, `capability-proof-presentation-batch.v1` |
| Capabilities | `artifact.delivery.send`, `artifact.delivery.status`, `artifact.delivery.submit` |
| Routes | `/v1/artifact-delivery/{deliveries,admissions,routes,recover,object-store/fetch}` |
| Sources | [Solution 023](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md), [Artifact Delivery HOWTO](../howto/artifact-delivery-howto.en.md) |
