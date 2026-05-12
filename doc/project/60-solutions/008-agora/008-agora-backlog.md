# Agora Backlog

This is the solution-local backlog for the Agora relay implementation. It
records fine-grained P-items that are too implementation-specific for the
solution overview but still need a canonical home next to the Agora solution.

## 1. What is missing for a complete MVP?

Nothing. Once Memarium arrives, we may need a mechanism that first stores
things published to Agora (local or remote) locally, so the node has tracking
and a local copy (so they do not disappear and can be republished if needed).
In that future shape, Agora will communicate with the daemon and hand it
things to preserve in Memarium, including the fact that a given entry intended
for a remote Agora was published successfully or unsuccessfully, separately
from the remembered entry itself but with a reference to it by unique ID.

The substrate for this integration is already present: the `memarium-runtime`
crate exists and exposes `MemariumRuntime::observe_dispatch()`, and the
daemon's `peer_handler.rs` has a complete observer layer (`PostChainObserver`,
`PhaseObserver` + emission in `dispatch`) that should receive a Memarium
adapter in daemon wiring. The adapter itself plus the Agora → Memarium coupling
(republish queue, per-publish fact tracking) do not exist yet; this is a
separate post-MVP task outside the scope of agora-core.

**Everything else is closed at the MVP level:**
- ✅ Signature verification (7-step, fail-closed, VerifiedRecord newtype)
- ✅ Matrix federation (store-and-forward, inbound sync, dedup)
- ✅ Retention sweep (per-topic, configurable)
- ✅ 3-channel auth (lifecycle, host capability, client)
- ✅ Passport issuance (capability.passport.issue) — startup flow +
  status in `/v1/agora/status`
- ✅ Operational limits (body, rate, SSE caps)
- ✅ CLI, OpenAPI, Python client+builder+demo, UI with SSE proxy
- ✅ Cross-language test vectors (seed=42)
- ✅ agora-verifier (Python host capability)
- ✅ Reproducible homeserver harness (Conduit fixture in
  `node/tools/matrix-fixture/`) + server-side Matrix `/sync` filters
  in `HttpMatrixEventSink`

---

## 2. What is missing for complete post-MVP?

| # | Gap | Status | Description | Priority |
|---|---|---|---|---|
| **P2** | **Content schema validation** | [done] | Agora content schemas (`plain-comment.v1`, `comment-thread-policy.v1`, `public-log-entry.v1`, `resource-opinion.v1`, `public-gossip.v1`, `moderation-marker.v1`, `agora-public-rejection.v1`, `reputation-snapshot.v1`, plus accepted domain-fact payloads) are now validated at the relay edge by `schema-gate` through `validate_agora_content_ingress`. agora-service gates both `POST /v1/agora/topics/{key}/records` (after JSON parse, before relay ingest) and `POST /v1/agora/records.sign` (before signer call, so malformed content cannot burn unlock-cache or rate-limit slots). Unknown schemas follow an open-world policy by default (warn log, accept) and flip to 422 when `strict_content_schemas = true`. | Medium — `schema-gate` boundary at the relay edge, as suggested by the agora-core docstring |
| **P3** | **Flagging/moderation** | [partial] | Local operator visibility is implemented as an operator-local control surface: `POST /v1/agora/operator/records/{record_id}/hide-local`, `unhide-local`, `flag-local`, and `unflag-local` record durable local markers in `<data_dir>/agora-local-visibility.v1.json`, `/v1/agora/status` exposes a `local_visibility` summary, and topic/subject historical listings filter locally hidden records without deleting them. Public cross-node marker language is now specified as `moderation-marker.v1`, validated by `schema-gate`, and routed under `ai.orbiplex.moderation.v1/markers/<target-kind>/<target-id-hash>` using Agora's JCS-NFC SHA-256 base64url target hash helper. Accepted public moderation marker records are replayed into `agora-projections.v1.sqlite` as a target/action/reason read model. Remaining P3 work: publish/list UI, policy evaluation for marker weight, `flag/clear` authority/quorum verification, web-capture-to-Memarium evidence, and any automatic hide/quarantine decision layer. | Medium — local safety, public marker contract, and replay projection exist; policy automation remains |
| **P4** | **Rate limiter persistence** | [done] | Token buckets now persist to `<data_dir>/agora-rate-limiter.v1.json` (atomic tmp+rename). `RateLimiter::snapshot_at`/`restore` convert between the in-memory `Instant`-based clock and a portable wall-clock snapshot; restore clamps tokens to the configured burst, drops classes disabled in the new config, and pins future timestamps (clock skew) to `now`. `main()` loads the snapshot at startup, a background thread flushes every `rate_limiter_persist_interval_secs` (default 60 s), and the shutdown path writes a final snapshot. | Low — acceptable with rare restarts |
| **P5** | **Record supersedes/parent enforcement** | [done] | Publisher-edge referential gate: `classify_parent_references` (pure) probes `record/parent` and `record/supersedes` against the local relay via `AgoraHttpApi::fetch_record`; the HTTP wrapper `gate_parent_references` runs on both `POST /v1/agora/topics/{key}/records` and `POST /v1/agora/records.sign`. Open-world by default (warn log + accept) and flips to HTTP 422 with `{status: "dangling_parent"\|"dangling_supersedes", reference_kind, missing_record_id}` when `strict_parent_refs = true`. Federation edge in `agora-relay-matrix` stays warn-only (`log_dangling_references_warn` on fresh inbound ingest) — rejecting on out-of-order Matrix delivery would break eventual consistency. | Low — open-world default keeps federation safe; strict mode is an opt-in operator choice |
| **P6** | **Pagination cursor expiry** | [done] | `AgoraRelay::topic_oldest_sequence()` exposes the lowest retained topic-local sequence; implementations that cannot expose pruning state return `None`. `AgoraHttpApi::list_topic_records` probes it whenever the caller paginates with `since`; when the decoded cursor falls below the retained window, the response carries a non-fatal `cursor_pruned: { requested_from, first_available }` notice next to `records` and `next_cursor` (both fields stay `skip_serializing_if = Option::is_none`, open-world: relays that return `None` stay quiet). | Low |
| **P7** | **Multi-homeserver** | [todo] | One relay = one homeserver (`matrix_homeserver_url` + `matrix_access_token`). There is no multi-homeserver configuration or fallback. | Low |
| **P8** | **UI signing** | [done] | The L2 adapter `sign_agora_record_via_host`, the `POST /v1/agora/records.sign` endpoint in agora-service (HTTP delegation to the daemon `HostSigner`), and the compose page in node-ui with 423 handling (unlock modal) are implemented and tested. Details in the note below. | Medium |
| **P9** | **Record search** | [todo] | No full-text search. The only indexes are topic, subject (about), and record_id. | Low — outside MVP |
| **P10** | **Webhook / push notification** | [todo] | SSE is pull-only (client connects). There is no push-to-webhook on ingest events. | Low |
| **P11** | **Signer policy allow-list for `agora-service`** | [done] | The daemon signer policy is already data-driven (`daemon/src/signer_integration.rs::policy_from_rules` builds a `DomainPolicy` from `BTreeMap<caller, Vec<domain-pattern>>` supplied by the daemon config), and `daemon/src/config.rs::default_signer_policy_rules()` contains the entry `("agora-service", vec!["agora.record.v1"])` (lines 650–652). `daemon/src/config.rs::tests::default_signer_policy_includes_agora_service` locks the default config shape, while `daemon/src/signer_integration.rs::tests` now composes `policy_from_rules(default_signer_policy_rules())` with a real `SignerEngine`: `http_module("agora-service", _)` can sign `DomainTag("agora.record.v1")`, and `http_module("agora-verifier", _)` is denied until the verifier gains a real signing duty. Earlier diagnostic notes in this TODO that claimed the allow-list was missing were based on an older tree (pre-`policy_from_rules` migration) and are superseded by this entry. | Resolved — config surface, rule, shape test, and engine-level policy regression test are in place |
| **P12** | **Proxy-key / delegated signing support in Agora envelope** | [done] | Phase (a), the Rust service/relay path, Rust Matrix federation parity, and cross-language fixture hardening are wired. `AgoraSignature` carries required-on-wire `key/public` plus optional opaque `key/delegation`; direct records bind `key/public` to `author/participant-id`; delegated records require inline proof when the concrete signing key differs from the author key. `verify_envelope` remains fail-closed through `RejectingDelegationVerifier`, while `verify_envelope_with(record, &dyn DelegationProofVerifier)` delegates proof semantics upward. `orbiplex-node-agora-capability-bridge` implements `CapabilityDelegationVerifier`; `agora-core::sign_agora_record_via_host_with_delegation` and `POST /v1/agora/records.sign` accept top-level `key_delegation`; invalid supplied delegation proofs return a policy-level `delegation_rejected` / HTTP 403 rather than an internal self-check failure. `agora-service` uses the bridge for signing self-checks and authority checks. `SqliteRelay`/`InMemoryRelay` are verifier-aware and default to fail-closed. `agora-matrix` exposes `_with` parser variants, `MatrixRelayTransport` has a configurable delegation verifier, and `MatrixBackedRelay` uses the same verifier for outbound and inbound Matrix paths. The daemon exposes `POST /v1/host/capabilities/agora.record.verify` and read-only `POST /v1/host/capabilities/agora.record.admit`; bundled Python middleware has `HostAgoraClient.verify_record()` and `HostAgoraClient.admit_record()`. Contract fixtures under `protocol/contracts/fixtures/agora/delegated/` assert the same accepted/rejected decisions across Rust, Matrix, SQLite replay, Python host-capability verification, and daemon admission transport. | Resolved — one delegated admission core across Rust, Matrix, replay, and Python host-capability clients |
| **P16** | **Org custody policy for authority roots** | [done] | Org authority roots now point at explicit `org-custody-policy.v1` artifacts in merged Agora config via `custody_policy_ref`; unknown refs and unsupported/missing rules fail closed. M2b supports `any-authorized` and real `threshold` mode. Threshold mode requires an inline `org-custody-decision.v1` bundle embedded in the delegated proof, verifies decision signatures against authorized participants/keys, deduplicates signers, checks the target record digest, topic namespace, policy ref, org id, purpose, decision expiry, delegation id, and optional delegation TTL. Public schemas and examples live in `orbidocs/doc/schemas`. | Resolved — org roots are policy-resolved instead of hard-coded allowlists |
| **P13** | **`agora-verifier` signer policy when it gains contrasigning duties** | [todo] | `default_signer_policy_rules()` currently assigns `agora-verifier` → `Vec::new()` (deny-all), which is correct today because the verifier only verifies — it never signs. If `agora-verifier` ever starts contrasigning artifacts (e.g. a moderation marker tied to P3 flagging, or a capability-passport-revocation), the empty allow-list will silently block signing with `domain_not_authorized` before any feature-level test catches it. Action when it happens: extend `default_signer_policy_rules()` with the narrow domain family the verifier needs (likely `agora.moderation.v1` or similar), mirror the pattern P11 uses for `agora-service`, and add a shape test next to `default_signer_policy_includes_agora_service`. Filed here so the reminder travels with Agora's TODO rather than living only in recipe form. | Low — dormant until P3 or another verifier-signed artifact lands |
| **P14** | **Query attestations** | [done] | Historical query responses now include `agora-query-attestation.v1` as `query_attestation`. The proof binds query mode, topic/subject scope, normalized filter, returned record ids, `next_cursor`, cursor-pruning metadata, and a deterministic JCS-NFC SHA-256 digest. The outer `RecordsPage.cursor_pruned` notice keeps Rust/JSON response field names (`requested_from`, `first_available`), while the exported attestation payload follows the schema contract under `result/cursor-pruned` with `requested-from` and `first-available`. `agora-service` re-attests subject-index pages after per-record subscribe-policy filtering so the proof describes the exact response returned. The v1 proof may be unsigned; relay signatures are a later signer/authority integration. | Low |
| **P15** | **Operator visibility** | [done] | `agora-service` now declares its own middleware operator surface in the module report and exposes an `operator_visibility` summary in `/v1/agora/status`: public endpoint, namespace enforcement mode, strict gates, topic ACL, authority roots, client auth, Matrix posture, HTTP/SSE limits, rate-limit persistence, and retention summary. `agora-ui` owns the rendered `/middleware/agora/operator` view and shows query-attestation JSON on historical topic/subject pages. Node UI only mounts Agora's surface and no longer treats Agora as a hard-coded bundled middleware nav item. | Low |

### Priority recommendation

```
1. M1: envelope error → 422             (30 min, improves DX immediately)     [done]
2. M2: seed.directory.publish           (2-3h, unblocks discovery)            [done]
3. M3: document idempotent ingest       (15 min, OpenAPI update)              [done]
─── MVP boundary ───
4. P1: per-topic ACL                    (one day, required before multi-user use) [done]
5. P8: agora.record.sign as an L2 wrapper over the generic signer (proposal 037) [done]
   ├─ L0/L1 substrate (signer-core / signer-service / signer-http)            [done]
   ├─ L2 agora-core/src/sign_adapter.rs                                       [done]
   ├─ L2 HTTP POST /v1/agora/records.sign in agora-service                    [done]
   └─ L3 node-ui compose page with 423 handling (unlock modal)                 [done]
6. P2: content schema validation        (one day, schema-gate at relay edge)  [done]
```

### Note for P8: layer decomposition

P8 is not implemented as a standalone Agora capability. It is a thin L2 wrapper
over the generic signing mechanism defined in
`orbidocs/doc/project/40-proposals/037-generic-signing-service.md`:

- **L0/L1 (outside Agora) [done]**: `signer-core` (the `HostSigner` trait and
  types), `signer-service` (engine: unlock cache with persistent scope, policy
  with the `agora.record.v1` domain, audit), and `signer-http` (the
  `/v1/host/capabilities/signer.{sign,unlock,lock,status}` endpoints mounted on
  the module-authtok dispatch path) are implemented and tested. None of them
  knows about Agora.
- **L2 core (in Agora) [done]**: `agora-core/src/sign_adapter.rs` — the
  `sign_agora_record_via_host(record, key_ref, caller, unlock_token, &dyn HostSigner)`
  function canonicalizes the record (compute_record_id → canonical_signed_bytes),
  delegates signing to `HostSigner` with `DomainTag("agora.record.v1")`, verifies
  returned `alg = "ed25519"`, matches returned `key_public` to
  `author/participant-id`, base64url-encodes the signature, and finally calls
  `verify_envelope` as a self-check. `SignAdapterError` carries variant errors
  (UnexpectedAlg, PublicKeyMismatch, MalformedAuthorId, RecordId,
  Canonicalization, SelfCheck, Signer).
- **L2 HTTP (in Agora) [done]**: `POST /v1/agora/records.sign` in
  `agora-service` accepts `{record, key_ref?, unlock_token?}`, gates topic ACL
  write access (so topic policy cannot be bypassed), builds
  `CallerIdentity::internal("agora-service")`, calls `sign_agora_record_via_host`
  through the `HttpHostSigner` adapter (HTTP to the daemon), and returns a
  verified record or an error envelope compatible with signer-http
  (`{status, reason, key_ref?, retry_after_secs?, expected?, got?}`).
  `HttpHostSigner` maps `SignerError` variants back while preserving `KeyRef`
  echo and `retry_after_secs`.
- **L3 node-ui [done]**: the `/agora/compose` page builds an unsigned envelope
  from the form, calls `AgoraClient::sign_record`, publishes through
  `POST /v1/agora/topics/{key}/records` on success, and redirects to
  `record_detail`. On `key_locked` / `unlock_failed`, it re-renders the form with
  a passphrase field; submitting the passphrase calls
  `DaemonClient::unlock_local_participant_signing_key` before retry. Error
  envelope codes (`domain_not_authorized`, `public_key_mismatch`,
  `malformed_author_id`, `unlock_rate_limited`) are shown to humans as readable
  messages; the full JSON envelope is preserved in template context for
  operators.

Key property: `signer-core` contains no import from `agora-core` and does not
know about the concept of an "Agora record". All Agora-specific knowledge lives
in `sign_adapter.rs`. We use the same pattern for passports (refactor),
Memarium (future), and any future artifact types.
