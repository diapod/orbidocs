# Solution 035: Agora — Topic-Addressed Record Relay — Implementation Guidelines

Proposal: `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Solution: `doc/project/60-solutions/agora.md`

Capability catalog: `doc/project/60-solutions/agora-caps.edn`

## Purpose of this document

This note is the implementation entry point for the Agora relay. It does
**not** duplicate the per-capability status (that lives in
`agora-caps.edn` and is surfaced by `CAPABILITY-MATRIX.en.md`) and it does
**not** try to replace the fine-grained backlog (that lives in
`node/docs/agora/TODO.md` in the sibling `node` repository).

It exists to:

- name the layers and the crates they map to,
- fix the invariants that hold *across* layers (signing domain, canonical
  bytes, `record/id` formula, topic ACL evaluation point),
- give readers a stable commit order when reshaping the stack,
- point at the P-item backlog for per-task status.

## Crate stratification

The runtime side of Agora is split into a thin stack of crates, each owning
one concern:

| Layer | Crate | Role |
|---|---|---|
| L0 | `agora-core` | envelope types, canonicalization, `agora.record.v1` domain, sign adapter, delegation verifier trait |
| L1 | `agora-relay-trait` | `AgoraRelay`, `SubjectIndex`, `IngestReceipt`, topic ACL contract, subscribe opts |
| L2a | `agora-relay-sqlite` | SQLite-backed local relay (records, topics, subject index) |
| L2b | `agora-relay-mem` | in-memory relay for tests and loopback experiments |
| L3 | `agora-matrix-client` | Matrix HTTP sink (send event, sync) |
| L3.5 | `agora-relay-matrix` | federated `MatrixBackedRelay` combining a local relay with the Matrix sink/transport |
| L4 | `agora-http` | `AgoraHttpApi` — request handlers over the relay trait, error mapping, SSE stream |
| L4.b | `agora-capability-bridge` | (planned, P12) `DelegationProofVerifier` impl that reads `capability` crate types |
| L5 | `agora-service` | supervised middleware binary: HTTP server + relay stack + retention sweep |
| L6 | `daemon` | bundled middleware wiring (executable override, config materialization), capability lookup surface |

Each layer compiles and makes sense independently. Swapping a backend means
swapping L2a/L2b; swapping transport means swapping L3/L3.5; swapping the
delegation verifier means swapping L4.b.

## Invariants that cross layers

These must be identical wherever they appear. If they drift between layers,
archival and federated verification will silently diverge.

1. **Signing domain.** The constant `AGORA_RECORD_DOMAIN_V1 =
   "agora.record.v1"` is the only domain tag used for Agora record
   signatures. It is prefixed before the canonical bytes at sign time and
   at verify time.
2. **Canonical signed bytes.** `canonical_signed_bytes` is the JCS
   canonicalization of the envelope with these fields pruned:
   `signature`, `relay/received-at`, `relay/id`. The `record/id` is
   included (post-compute) so that it participates in the signature.
3. **`record/id` formula.**
   `sha256:<base64url-no-pad(sha256(canonical_content_address_bytes))>`.
   The prefix is literal; the hash is SHA-256; the encoding is the same
   URL-safe no-padding convention used by the node's other signed
   artifacts.
4. **Participant id shape.** `participant:did:key:<base58btc ed25519>`. The
   `PARTICIPANT_ID_PREFIX` constant lives in signer-core and is reused by
   `agora-core` when binding the returned public key to the author.
5. **Topic ACL evaluation point.** ACL is evaluated inside the relay trait
   impl on ingest, before persistence, and again on federated inbound after
   envelope re-validation. Never at the HTTP layer only.

## Layer 0 — JSON Schemas

Canonical schemas:

- `agora-record.v1` — envelope.
- `resource-opinion.v1` — content schema for `record/kind = "opinion"` with
  a URL subject (proposal 026).
- `plain-comment.v1` — content schema for `record/kind = "comment"`.
- `key-delegation.v1` — already published; referenced inline by P12
  delegated signing (optional).

Schema publication happens through the daemon's schema surface (same style
as `/v1/schemas/key-delegation`). Keep schema names stable; do not encode
relay role or topic into the schema id.

## Layer 1 — `agora-core`

### Envelope and canonical bytes

- `AgoraRecord` struct with slash-style keys preserved verbatim on the
  wire (`record/id`, `record/kind`, `topic/key`, `author/participant-id`,
  `authored/at`, `content/schema`, `content`, `record/about`, `signature`).
- `canonical_signed_bytes(&AgoraRecord) -> Vec<u8>` — JCS with the pruning
  rules above.
- `compute_record_id(&canonical_content_address_bytes) -> String` —
  `sha256:<base64url-no-pad(sha256(...))>`.

### Sign adapter (L2 into host signer)

- `sign_agora_record_via_host(record, key_ref, host_signer) -> Result<...,
  SignAdapterError>`:
  1. compute canonical bytes of the unsigned envelope,
  2. request a signature in the `agora.record.v1` domain,
  3. verify the signer's returned `key_public` against the author's
     participant id (hard block, `SignAdapterError::PublicKeyMismatch`),
  4. populate `record/id` and `signature.value`, return the record.
- Never skip step 3 even when the key_ref is `PrimaryParticipant`. The
  check is what prevents a misconfigured signer from producing a record
  whose author id disagrees with its signature.

### Delegation verifier trait (P12 seam)

- `trait DelegationProofVerifier { fn verify(&self, record: &AgoraRecord,
  proof: &serde_json::Value) -> Result<(), DelegationVerifyError>; }`
- `RejectingDelegationVerifier` is the fail-closed default. A production
  deployment installs `CapabilityDelegationVerifier` from
  `agora-capability-bridge`.
- The docstring in `agora-core/src/signature.rs` explicitly commits to this
  seam so that `agora-core` stays free of any `capability` crate dependency.
  Do not regress this by importing capability types into agora-core.

## Layer 2 — relay trait and storage backends

### `AgoraRelay` trait

Minimum methods:

- `ingest_signed(record: AgoraRecord) -> Result<IngestReceipt, IngestError>`
- `get_record(id: &str) -> Result<Option<AgoraRecord>, RelayError>`
- `list_topic(key: &str, opts: PageOpts) -> Result<RecordsPage, RelayError>`
- `list_subject(kind: &str, id: &str, opts: PageOpts) -> Result<RecordsPage,
  RelayError>`
- `subscribe_topic(key: &str, opts: SubscribeOpts) -> Result<TopicStream,
  RelayError>`

### SQLite backend (`agora-relay-sqlite`)

- one file, multiple tables: `records`, `topics`, `subject_index`,
  `sweep_cursor`.
- idempotent ingest by `record/id` unique constraint (duplicate → 200 OK in
  the HTTP layer).
- subject index is maintained synchronously on ingest; `rebuild_subject_index`
  on startup covers crash recovery.

### Memory backend (`agora-relay-mem`)

Same trait surface, in-memory `BTreeMap`s, used for tests and for loopback
experiments that do not need durability.

## Layer 3 — Matrix transport

### `agora-matrix-client`

- `HttpMatrixEventSink` — `/_matrix/client/v3/rooms/{room}/send/{type}/{txn}`,
  plus sync.
- fails closed on non-2xx; retries are the caller's concern.

### `agora-relay-matrix`

- `MatrixBackedRelay` composes a local relay + `MatrixRelayTransport` +
  `SubjectIndex`.
- three roles (`canonical`, `cache`, `origin`) gate outbound/inbound and
  ACL authority per topic.
- bridges are started once at service startup
  (`start_configured_bridges()`), never inside request handlers.

## Layer 4 — HTTP surface

### `agora-http`

- `AgoraHttpApi` holds `Arc<dyn AgoraRelay>` and `Arc<dyn SubjectIndex>`.
- Endpoints (same shape at v1 and v2 if that ever comes):

  | Method | Path | Handler |
  |---|---|---|
  | GET | `/v1/agora/status` | status snapshot |
  | GET | `/v1/agora/records/{id}` | record-by-id |
  | GET | `/v1/agora/topics/{key…}/records` | topic page |
  | POST | `/v1/agora/topics/{key…}/records` | post signed record |
  | GET | `/v1/agora/topics/{key…}/subscribe` | SSE stream |
  | GET | `/v1/agora/about/{kind}/{id}/records` | subject-index page |
  | POST | `/v1/agora/records.sign` | sign unsigned envelope through host signer |

- Error mapping:
  - `PublicKeyMismatch` → HTTP 422 `author_signature_binding_failed`,
  - `TopicAclDenied` → HTTP 403 `topic_acl_denied`,
  - `DelegationVerifyError::*` → HTTP 422 with per-variant error code
    (one code per verify-error variant — schema mismatch, proxy/principal
    key mismatch, principal signature invalid, expired, grants
    insufficient),
  - duplicate `record/id` → HTTP 200 with `duplicate: true`.

- SSE frame: `event: agora.record\ndata: <json>\n\n`. One event per accepted
  record; the stream never reorders events across the authored-at axis on
  a single topic.

## Layer 4.b — `agora-capability-bridge` (P12)

Separate crate so that production nodes install the capability-backed
verifier while tests can run with `RejectingDelegationVerifier`. Contract
summary:

- `CapabilityDelegationVerifier` parses the `serde_json::Value` proof into
  the typed `capability::DelegationProof`,
- validates schema, proxy/principal key match to record author, grants
  include `signing/capability` for `agora.record.v1`, and expiry against
  `record.authored/at` (deterministic, not wall clock).

Full phase plan for this layer lives in the sibling `node` repository
alongside the other Agora implementation notes; this solution document
only fixes the contract.

## Layer 5 — `agora-service` (supervised middleware binary)

### Shape

- binary crate under `node/agora-service/`, entry `src/main.rs`,
- loads JSON config from `$ORBIPLEX_NODE_CONFIG_DIR` section
  `"agora_service"`,
- supports both the **middleware supervisor protocol** (`/readyz`,
  `/healthz`, `/v1/middleware/init`, `/shutdownz`) and the **Agora HTTP
  API** under `/v1/agora/...` on the same listen port,
- spawns a retention sweep thread using the configured interval.

### Middleware `init` report

Returns `MiddlewareModuleReport` advertising exactly one capability:
`agora.relay` (class `Other`). No `input_chains`, no `local_routes` — this
middleware does not participate in the dispatch chain; clients connect to
the port directly once the daemon's capability lookup returns it.

### Auth

- `/v1/middleware/init` and `/shutdownz` validate `Authorization` against
  the token loaded from `$ORBIPLEX_MIDDLEWARE_AUTHTOK_FILE` using the header
  name in `$ORBIPLEX_MIDDLEWARE_AUTH_HEADER` (default `Authorization`).
- `/readyz`, `/healthz` are open (same as other supervised middleware).
- Agora endpoints are auth-free at this layer; authorization is the topic
  ACL's job, not a per-request token.

### Path handling

- percent-decoding on every path segment that may include slashes (topic
  key, record id, subject id). Do not decode `+ → space` — that is HTTP
  query semantics only.
- query-string decoding supports `+ → space`.

### Error diagnostics

Replace `.expect()` in `build_relay` with `unwrap_or_else(|e|
panic!(...))` that includes the SQLite path, the homeserver URL, the
`relay_id`, and the role. These messages are read at 3am by operators who
did not write the code.

## Layer 6 — daemon wiring

### Config-driven activation

Agora is **not** enabled by default. The operator enables it by adding an
`"agora_service"` section to the Node config (typical path:
`<data_dir>/config/30-agora.json`). The bundled fabric config
`middleware-modules/agora-service/config/00-agora-service.json` has
`seed_config: false` so the daemon does not auto-materialize it.

The daemon's `build_generated_http_local_executor_config()` is extended
with a generic `executable` override:

- if the bundled config carries `"executable": "run.sh"`, resolve it
  relative to the middleware module directory and use it instead of the
  default Python runner;
- otherwise fall back to `bundled_middleware_runner_script()` (Python
  middleware shape).

This change is generic — it applies to any bundled middleware that ships a
native binary, not just Agora.

### Launcher

`middleware-modules/agora-service/run.sh` locates the compiled
`orbiplex-node-agora-service` binary in
`$WORKSPACE/target/release|debug`, falls back to `$PATH`, and `exec`s it
with the listen port as the first argument.

### Capability lookup

The daemon's host capability API exposes

```
GET /v1/host/capabilities/agora.relay
X-Orbiplex-Authtok: <daemon control token>
```

which returns the local provider (module id, endpoint URL, transport, scope,
description, passport). For Node UI this is a daemon control-plane read using
the control token; middleware modules use their separate
`X-Orbiplex-Module-Authtok` token for daemon-owned POST capabilities such as
`signer.sign`.

If the capability is known but no provider is ready, the daemon returns `200`
with an empty `providers` array. If the capability is unknown, it returns
`404 capability_unknown`. The UI maps both cases to an explicit no-local-relay
or capability-unavailable state rather than silently falling back to a public
relay (story-008 acceptance criterion 2).

## Layer 7 — Node UI discovery

The Node UI does not ship a hardcoded Agora endpoint. For compose flows
(e.g. the "opinion about URL" form from story-008) it calls the host
capability API above and uses the first `scope: "local"` provider. If none
is returned, the UI shows a clear "no local relay available" notice and
does not offer a remote fallback.

## Recommended commit order when reshaping the stack

1. **Schemas first.** Any envelope or content shape change lands as a
   schema update, with the old schema either deprecated or versioned
   (`agora-record.v2`) before any code reads the new shape.
2. **L0 (`agora-core`).** Canonicalization, domain constant, sign adapter,
   delegation trait.
3. **L1 (`agora-relay-trait`).** Trait changes must preserve existing
   impls; add methods with default impls where possible.
4. **L2 (backends).** SQLite first, memory second — the test backend
   should never outrun the production one.
5. **L3 (Matrix).** Only once backends compile; federation is an amplifier
   of existing bugs.
6. **L4 (`agora-http`).** HTTP surface changes after the core is stable.
7. **L4.b (`agora-capability-bridge`).** P12 — gated on the record-level
   fields and verifier trait landing in L0 first.
8. **L5 (`agora-service`).** Binary integrates the above.
9. **L6 (daemon wiring).** The `executable` override + bundled config.
10. **L7 (Node UI).** Discovery UX.

Each step should leave the tree in a compiling state.

## MVP boundaries

Keep these restrictions explicit in both code and docs:

- one author per record; no co-signatures, no multisig,
- no sub-topic ACL inheritance — topic keys are flat strings treated as
  a namespace, not a tree with permission descent,
- no wildcard revocation of past records (records are immutable once
  ingested; retention sweep is the only removal path),
- no automatic cross-relay federation before an explicit
  `agora.relay` passport is issued,
- no content-semantic interpretation inside the relay — Agora does not
  read `content` beyond `content/schema` for ACL and retention purposes,
- `KeyRef::Proxy` is runtime-rejected (HTTP 422
  `delegated_signing_unsupported`) until L4.b lands.

## Testing posture

- **Golden vectors** for `canonical_signed_bytes` and `record/id` in
  `agora-core/tests/`. One vector per content schema. These vectors are
  the federation-level contract — they do not change without a schema
  version bump.
- **Roundtrip tests** for each backend: ingest → list → get-by-id →
  subject-list.
- **Federation tests** in `agora-relay-matrix/tests/` using the Matrix
  mock sink from `agora-matrix-client`.
- **SSE harness** in `agora-http/tests/` — subscribe, ingest, assert
  delivery order.
- **Service integration test** in `agora-service/tests/` — spawn the
  binary with a temp SQLite, POST a signed record, GET it back, close.

## Related documents

- `doc/project/60-solutions/agora.md` — solution-level description.
- `doc/project/60-solutions/agora-caps.edn` — capability catalog.
- `doc/project/30-stories/story-008-cool-site-comment.md` — first
  end-to-end user story.
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md` —
  source proposal.
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
  — content schema for URL opinions.
- `node/docs/agora/TODO.md` — granular P1–P13 backlog (source of truth for
  status of implementation tasks).
- `node/docs/implementation-ledger.toml` — per-crate implementation status.
- `doc/project/40-proposals/032-key-delegation-passports.md` — source
  proposal for the P12 delegated-signing layer.
