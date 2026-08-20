# Operator's Manual: INAC (Inter-Node Artifact Channel)

INAC is the adapter for direct transport between nodes. It moves Orbiplex
artifacts without changing their bytes and without publishing them through a
public communication layer.

The [Artifact Delivery FAQ](../faq/artifact-delivery-faq.en.md) introduces the
concepts. Procedures and examples are in the
[Artifact Delivery HOWTO](../howto/artifact-delivery-howto.en.md).

## 1. Purpose and functions

INAC lets nodes exchange artifacts **privately and directly**, without
publishing them through a topic relay. Agora carries public or semi-public topic
traffic. Artifact Delivery receives delivery requests from components and
selects a transport, while INAC performs private transport between nodes.
Memarium remains the local store for entrusted data.

Functions:

- exchange artifact offers, requests, pushes, and refusals over authenticated
  sessions with remote nodes (`peers`),
- keep the artifact envelope byte-identical across transfer and storage,
- use the existing authority mechanisms — capability, invitation, and custody
  passports — instead of creating another source of authority,
- pass received artifacts to the shared Artifact Delivery intake path, which
  has exactly one authoritative domain receiver (`acceptor`) for each kind,
- keep large payloads outside the main JSON control frame by using stream chunks
  bound to one session and content address.

## 2. How it works

Nodes exchange `inac-control.v1` frames through the `msg = "inac.v1"` message
channel inside an authenticated WSS session. A frame contains the operation, an
optional correlation id, artifact and transfer descriptions, authorization
data, and a response.

Initiating operations: `offer`, `request`, `push`.
Response operations: `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial`.

A payload can exist in exactly one place: directly in the frame (`inline`) or in
a stream. The host validates this exclusivity. Small payloads fit in the frame;
larger ones move as chunks. The preferred contract is
`inac.stream.chunk.binary.v1`, with digest, offset, and size checks for every
chunk. JSON/base64url remains a compatibility fallback. A decoded chunk larger
than 8 MiB is rejected **before** it is appended to a file.

Received `push` frames have no separate dispatch table. They enter the shared
Artifact Delivery receiver registry. If no handler exists for an artifact kind,
the host refuses the frame instead of accepting it by default.

Local outbound rules (`outbound/allows`) deny by default. An empty `operations`
or `schemas` set means no authority, not authority over every value.

## 3. Architectural placement and communication channels

INAC runs above authenticated remote-node sessions and in parallel with Agora.
Components still request delivery through Artifact Delivery. They do not manage
WSS sockets, sessions, invitation state, or the meaning of `offer` and `push`;
the node-session layer and the INAC host own those concerns.

Channels and their justifications:

| Channel | Direction | Justification |
| --- | --- | --- |
| `msg = "inac.v1"` in the node-message chain (WSS) | bidirectional, node ↔ node | INAC's only network channel. It uses the existing authenticated session and therefore adds no separate transport authentication. |
| Stream chunks (`inac.stream.chunk.binary.v1`, JSON/base64url fallback) | bidirectional, node ↔ node | Carry large data outside the control frame. They are bound to a session and content address and cannot be reused outside their transfer. |
| `PeerSender` from `ad-host` | outbound, component → INAC | The consumer side of Artifact Delivery asks for delivery through INAC without owning transport knowledge. |
| `InacAdmissionBridge` → Artifact Delivery receiver registry | inbound, INAC → host | Received frames enter the shared intake path instead of a separate INAC dispatch table, so exactly one authoritative receiver exists per artifact kind. |
| `POST /v1/host/capabilities/inac.offer`, `…/inac.request`, `…/inac.push` | inbound, local component → daemon | Host capabilities for supervised components; they require an explicit outbound allow. |
| `GET /v1/inac/status` | read, operator → daemon | Operator projection; grants no authority. |
| SQLite transfer registry | read/write, local disk | Durable transfer decisions, pending offers, and contacts. |
| On-disk stream store | read/write, local disk | Chunk assembly before admission. |
| Seed Directory address evidence (`node-address-attestation.v1`) | read, node discovery → connection supervisor | The address certificate fingerprint becomes part of a connection candidate. Fresh evidence takes precedence over a static pin; expired evidence cannot be used for a connection. |
| Operator notifications (invitation flow) | outbound, daemon → operator | Approving an invitation offer is a human decision, not an automatic one. |

## 4. Data contracts

| Schema | Purpose of use | Channel |
| --- | --- | --- |
| `inac-control.v1` | Transport-neutral control frame for `offer`, `request`, `push` and every response and refusal. | `msg = "inac.v1"` over the peer session |
| `agora-record.v1` | A transferred signed Agora record, handled by one of the two baseline Artifact Delivery receivers. | transfer payload → AD intake |
| `memarium-blob.v1` | A transferred signed Memarium artifact envelope, handled by the second baseline receiver. | transfer payload → AD intake |
| `artifact-object-pointer.v1` | Indirect object reference when bytes are not carried directly in the frame; the later fetch has its own limit. | artifact descriptor in the control frame |
| `contact-request.v1` | Low-privilege contact request; transport intake does **not** grant messaging authority. | `push` frame → AD preflight and receiver |
| `node-address-attestation.v1` | Address evidence from node discovery; source of the certificate fingerprint for a connection candidate. | Seed Directory → connection supervisor |
| `inac-status.v1` | Current status view for the operator. | `GET /v1/inac/status` |

## 5. Limits and behaviour when exceeded

| Ceiling | Default | Behaviour when exceeded | Configurable |
| --- | --- | --- | --- |
| Payload carried directly in the frame (`inline`) | 64 KiB | refusal `payload-too-large` | yes — `inac.inline_max_bytes` |
| Artifact size | 1 GiB | refusal `payload-too-large` | yes — `inac.max_artifact_size_bytes` |
| Single stream chunk | 8 MiB (decoded) | rejected **before** the file append | no |
| Stream idleness | 15 minutes | the stream is treated as stale | no |
| Fetching an indirect object's data | 256 MiB | refusal | no |
| Pending offers per remote node | 128 | new offers rejected | no |
| Control token | 256 characters | refusal `malformed` | no |
| Metadata properties | 16 entries, 64 B key, 512 B value | refusal `malformed` | no |
| Recent-refusal buffer in status | 16 | oldest fall out (a diagnostic window, not fact loss) | yes — `inac.recent_refusals_limit` |
| Inbound budget per remote node | none by default | refusal `rate-limited` or `quota-exceeded` | yes — `inac_peer_transport.inbound_budgets` |

## 6. Refusal vocabulary

A refusal is a value inside a frame, not an exception. The codes:

| Code | Meaning | Retryable? |
| --- | --- | --- |
| `kind-not-supported` | No handler for this artifact kind. | No, until a matching receiver is registered. |
| `kind-conflict` | The artifact kind conflicts with the transfer declaration. | No — a sender error. |
| `not-authorized` | No authority for this operation. | No, until authority changes. |
| `invitation-unknown` | The receiver does not know this invitation. | No. |
| `invitation-expired` | The invitation is past its TTL. | After the invitation is renewed. |
| `invitation-revoked` | The invitation was revoked. | No. |
| `invitation-scope-mismatch` | The invitation does not cover this operation or kind. | No. |
| `payload-too-large` | The in-frame limit or whole-artifact limit was exceeded. | Not in this shape — use a stream or shrink the artifact. |
| `digest-mismatch` | The bytes do not match the declared digest. | No — integrity is broken. |
| `malformed` | The frame does not satisfy the contract. | No. |
| `handler-unavailable` | The receiver exists but is temporarily unavailable. | **Yes.** |
| `already-present` | The artifact is already present locally. | No — this is an idempotent success, not an error. |
| `operation-not-supported` | The operation is unsupported on this path. | No. |
| `policy-denied` | Local policy refuses. | No, until policy changes. |
| `transport-unavailable` | The transport is unavailable. | **Yes.** |
| `rate-limited` | A rate budget was exceeded. | **Yes, after waiting.** |
| `quota-exceeded` | A size or volume budget was exceeded. | **Yes, once the window renews.** |

`handler-unavailable`, `transport-unavailable`, `rate-limited` and `quota-exceeded` describe a transient state and are worth retrying. The rest are terminal for that frame.

## 7. Authority and its revocation

Host capabilities (for supervised components):

- `inac.offer` — `host/inac.offer`
- `inac.request` — `host/inac.request`
- `inac.push` — `host/inac.push`

Application capability: `inac.invitation` (`app/inac.invitation`), owned by the capability-passport domain. Receiver-issued invitation passports carry a TTL (3600 s by default) and are created inside the operator approval flow.

A component's outbound authority comes from `outbound/allows` and is denied by
default. Each entry binds a `component/id` to specific operations, schemas, and
an optional byte limit. The coarse permission for traffic from a remote node
comes from `inbound_allowed_peers`; an **empty list denies every node
(`deny-all`)**, not allows all.

A revoked or expired invitation yields `invitation-revoked` or
`invitation-expired` on next use. Expired address evidence cannot be used to pin
a connection certificate. Accepting an invitation offer may create a durable
contact entry, but **a contact is not authority**.

## 8. Trust boundaries

| What | Who verifies it |
| --- | --- |
| Remote-node identity | The authenticated WSS session, not INAC. |
| Artifact digest and size | INAC, before admission — including per stream chunk. |
| Envelope byte identity | INAC, across transfer and storage. |
| Frame conformance | Schema Gate plus `inac-core` validation. |
| Eligibility of the artifact kind | The receiver registry; no entry means refusal. |
| The artifact's domain authority | **Not INAC.** The Artifact Delivery receiver and target domain decide it. Successful transport intake grants no domain authority. |
| Address certificate fingerprint | The connection supervisor, from node-discovery evidence; freshness is checked before use. |

The main rule is: **transport intake never means domain consent.** For
`contact-request.v1`, it only permits the preflight check and contact-request
receiver to run; it grants no messaging authority by itself.

## 9. Dependencies and degraded modes

Requires an authenticated session with the remote node, the Artifact Delivery
receiver registry, the artifact object store, the transfer registry, and — for
the invitation flow — operator notifications.

Provides: the `inac-direct` transport for remote Artifact Delivery targets.

Degraded modes:

- **Transport unavailable** — no active session with the remote node; outbound
  operations end in `transport-unavailable`, and transfer state remains in the
  registry.
- **Receiver unavailable** — `handler-unavailable`; the artifact is not
  accepted, and the refusal counter grows.
- **Registry unavailable** — the status read still works but returns empty lists
  and writes `inac_status_ledger_read_failed` to the log.
- **Damaged shared state** — if a panic poisons the internal state lock, status
  returns one synthetic `handler-unavailable` refusal with the cause.

## 10. Durable state and restart

| Store | Path | Durability | After restart |
| --- | --- | --- | --- |
| Transfer ledger | `<data-dir>/storage/inac.sqlite` | durable | rebuilt from the database; decisions, pending offers and contacts survive restart |
| Stream store | `<data-dir>/storage/artifact-delivery/streams` | durable (files) | unfinished streams older than 15 minutes are stale |
| Counters and recent refusals | process memory | ephemeral | reset on start — a diagnostic window, not a ledger |

The distinction matters: **status counters are not history**. Durable transfer
decision history lives in the SQLite registry.

## 11. Configuration

### Layer composition

The daemon's effective configuration is built in this order, each layer deep-merged over the previous one:

1. **Built-in defaults** — `InacRuntimeConfig::default()` and `DaemonInacPeerTransportAdapterConfig::default()`, compiled into the daemon.
2. **Factory module configuration** — bundled middleware module fragments. INAC keys do not come from this layer, but the layer is part of the shared composition.
3. **`<data-dir>/config/*.json`** — every `.json` file in the directory, read in **alphabetical filename order** and deep-merged. This is where INAC configuration belongs.
4. **`<data-dir>/control/middleware-settings.json`** — settings applied at runtime by the operator; merged over layer 3.

Invalid JSON in any layer-3 file stops startup and identifies the affected file;
the configuration is never partially applied.

### Options: `inac`

| Option | Type | Default | Effect |
| --- | --- | --- | --- |
| `inline_max_bytes` | number | 65536 | Largest payload carried directly in the control frame. Above it a stream is required. |
| `max_artifact_size_bytes` | number | 1073741824 | Absolute artifact size ceiling, regardless of payload location. |
| `recent_refusals_limit` | number | 16 | How many recent refusals the status projection keeps. A diagnostic window. |
| `outbound/allows` | list | `[]` | Outbound allows for local components. **An empty list means no outbound authority.** |

An `outbound/allows` entry:

| Field | Type | Effect |
| --- | --- | --- |
| `component/id` | text | The component the allow applies to. |
| `operations` | set | Permitted operations. **An empty set is no authority, not a wildcard.** |
| `schemas` | set | Permitted artifact schemas. Same rule. |
| `max/bytes` | number or absent | Optional byte ceiling narrower than the global one. |

### Options: `inac_peer_transport`

| Option | Type | Default | Effect |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | Enables INAC transport between nodes. |
| `inbound_allowed_peers` | list of text | `[]` | Nodes allowed to send inbound `offer` and `push` frames. **An empty list denies every node (`deny-all`).** |
| `inbound_budgets` | list | `[]` | Receiver-side budgets for inbound frames. |
| `invitation_passport_ttl_seconds` | number | 3600 | TTL of the receiver-issued invitation passport created in the operator approval flow. |
| `contact_creation_after_accept` | bool | `true` | Whether accepting an invitation offer creates a durable contact projection. A contact is not authority. |
| `response_timeout_ms` | number | 5000 | How long to wait for a remote-node response. |
| `contact_requests.enabled` | bool | `false` | Whether to admit low-privilege `contact-request.v1` artifacts. |
| `contact_requests.unknown_peer_mode` | `auto-admit` / `operator-approval` / `deny` | `deny` | How to treat a request from an unknown peer. |
| `contact_requests.deny_blocked` | bool | `true` | Whether to refuse requests from blocked nodes. |

An `inbound_budgets` entry:

| Field | Type | Effect |
| --- | --- | --- |
| `remote_node_ids` | list | Remote nodes covered by the rule. **An empty list acts as a wildcard.** |
| `operations` | list | Operations the rule covers. Empty — wildcard. |
| `artifact_schemas` | list | Schemas the rule covers. Empty — wildcard. |
| `content_types` | list | Content types the rule covers. Empty — wildcard. |
| `max_size_bytes` | number or absent | Size ceiling for matched frames. |
| `max_per_minute` | number or absent | Rate ceiling for matched frames. |

These two places deliberately use different semantics. In `outbound/allows`, an
empty set means **no authority**. In `inbound_budgets`, an empty match list means
**match every value**. The first grants authority; the second selects traffic
covered by a rule.

## 12. Observability

`GET /v1/inac/status` returns an `inac-status.v1` document:

- `runtime.handlers` — registered receivers and the data they handle,
- `runtime.counters` — `accepted`, `ingested`, `refused`, `malformed` (ephemeral, since process start),
- `runtime.recent_refusals` — recent refusals with code and message (a window sized by `recent_refusals_limit`),
- `transfers.diagnostics` — durable transfer-registry diagnostics,
- `transfers.recent_decisions` — up to 25 recent transfer decisions,
- `contacts.recent_contacts` — up to 25 recent contacts.

The current view contains no payloads: it exposes neither artifact bytes nor
secrets. Reading status grants no authority.

The daemon also exposes diagnostics for address evidence used by the connection
supervisor. Fresh evidence may identify a direct INAC target. Stale or dead
evidence remains only a node-discovery and troubleshooting hint; **it cannot
become a delivery target without fresh verification**.

## 13. Cost and resources

INAC charges no inference budget. Its costs are material:

- **disk** — the SQLite transfer ledger and stream files; unfinished streams hold space until they are treated as stale (15 minutes),
- **network** — inbound and outbound traffic equal to artifact size; the 1 GiB artifact ceiling is the only hard limit on a single transfer,
- **memory** — payloads up to 64 KiB carried directly in a frame, plus the
  recent-refusal window.

## 14. Contract versions and compatibility

The control frame is `inac-control.v1`. Stream chunks prefer
`inac.stream.chunk.binary.v1`; JSON/base64url remains a deliberately supported
compatibility path. The two baseline Artifact Delivery receivers handle
`agora-record.v1` and `memarium-blob.v1`.

## 15. Known limitations

The `INAC Local Operator MVP` implementation-ledger row is still **`partial`**.
WSS and Matrix transport, streaming, passport-based receiver gates, the decision
registry, operator UI, and two baseline receivers are implemented. The
following limits remain:

- The baseline registry contains two concrete artifact kinds
  (`agora-record.v1`, `memarium-blob.v1`). Middleware-owned kinds are added
  through explicit composition points, not a closed list in INAC.
- `inbound_allowed_peers` remains a flat, coarse list of allowed nodes. More
  precise authority for each push is already checked separately through
  invitation, capability, messaging, and custody passports; the list does not
  replace those checks.
- Static certificate pins from seed nodes remain a bootstrap shortcut. Fresh
  attested address evidence takes precedence over them.
- Status counters are ephemeral — correlate events over time through the transfer ledger, not through status.

## 16. Implementation references

| Field | Value |
| --- | --- |
| Component | INAC (Inter-Node Artifact Channel) |
| Implementation-ledger row | `INAC Local Operator MVP` |
| Rust crates | `inac-core`, `inac-runtime`, `inac-handlers`, `inac-host`, `daemon`, `node-ui` |
| Schemas | `inac-control.v1`, `memarium-blob.v1`, `agora-record.v1` |
| Capabilities | `inac.offer`, `inac.request`, `inac.push`, `inac.invitation` |
| Routes | `POST /v1/host/capabilities/inac.{offer,request,push}`, `GET /v1/inac/status` |
| Sources | [Proposal 042](../../project/40-proposals/042-inter-node-artifact-channel.md), [Solution 017](../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md) |
| Component status | `partial` |
