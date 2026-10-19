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

Planning update (2026-10-11): do not implement the transport part as a new
Agora-specific republish queue. [P035-001–003](../../40-proposals/035-agora-topic-addressed-record-relay.md#delivery-integration-tracker)
own consolidation onto existing AD delivery/retry/status, with Memarium holding
bounded domain observation facts and retained artifacts under its own policy.
Preserve publication intent and reconcile its AD delivery id across crashes.
This supersedes the private-queue direction above, not the completed relay MVP
or P8 signing baseline. Existing P8 describes the pre-migration HTTP producer.

**The original relay/signing MVP baseline is closed:**
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

This baseline does not claim complete domain-consumer coverage. Generic resource
authoring and pair-only opinion reads were qualified through
[P026-001–003](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#implementation-tracker)
on 2026-10-12 (`node:docs/evidence/open-references/README.md`);
public-gossip related-link navigation is the independent P17 continuation below.

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
| **P17** | **Public-gossip resource links** | [todo] | Project `gossip/see-also` through the existing related-link machinery and expose bounded, policy-filtered lookup/navigation without conflating related resources with envelope subjects. Reuse P026 resource conversions; no country-specific core cases. See the completion gate below. | Medium — independent consumer continuation, not a blocker for P026-003 |
| **P18** | **Opaque Agora carrier over Matrix** | [done] | [P035-004](../../40-proposals/035-agora-topic-addressed-record-relay.md#matrix-carrier-tracker) qualified on 2026-10-12: four SQLite and 21 Matrix cases at Node 20c4c16c / Orbidocs 862586f, confidence 0.5 and permitted Whisper signal/trace/threshold, exact bytes, restart/replay and recovery review. Every Node-created complete PDU fits 65,536 (maximum 50,043); direct Client-Server enforcement is an independent pinned-fixture result. Original v0.7.0 oversize finding/refusal stays retained. The frozen run selected v2 explicitly; P035-006 separately qualifies the default-v2/explicit-legacy-v1 policy on 2026-10-14. P026 confidence=1 and applicable P096 qualification retain their scope. Evidence: `node:docs/evidence/matrix-opaque-envelope/README.md`. | Resolved for the carrier profile; one disclosed fixture does not qualify federation or production readiness |
| **P19** | **Pruned-source opinion carry-forward** | [P026-004](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#pruned-source-continuation) | Explicit inherited projection provenance can enable migration after retention; strict rebuild remains the default and inherited rows do not establish full-source replay equivalence. The canonical task and acceptance gate are P026-004. | Medium — current strict rebuild refuses after source pruning |
| **P20** | **Unmodified reference homeserver interoperability** | [done] | [P035-005](../../40-proposals/035-agora-topic-addressed-record-relay.md#matrix-carrier-tracker) qualified 2026-10-13 at Node dcc8133c / Orbidocs c84df99: four SQLite and 22 Matrix cases on official unmodified Synapse v1.162.0/PostgreSQL 16.13, room v10. Independent Node budget gate: 42 full PDUs, maximum 49,927 within 65,536. Homeserver gate: direct protocol maximum 65,535, actual 413 M_TOO_LARGE including requests below the PDU ceiling. Confidence 0.5, exact bytes, permitted Whisper families, restart/backfill/replay and stock-serializer hash/signature verification pass. Initial failed Synapse and previous Conduit evidence remain frozen. `node:docs/evidence/matrix-opaque-envelope/2026-10-13-synapse/qualification.json`. | Resolved for one explicit-v2 room-v10 reference profile; default path, federation and production remain separate |
| **P21** | **Default v2 writer and explicit legacy v1** | [done] | [P035-006](../../40-proposals/035-agora-topic-addressed-record-relay.md#matrix-carrier-tracker) qualified 2026-10-14 at Node 42fde666 / Orbidocs 4ecec76: five SQLite and 27 Matrix cases, absent A/B config, confidence 0.5, exact bytes, first-intent and unknown-third-claim controls, restart/replay. All 692 Node full PDUs fit 65536 (maximum 49927); unmodified Synapse has its independent positive enforcement gate. Long filtered history restores 643 records over 12 pages across crash; empty bootstrap and non-limited late binding pass. Bounded archives preserve equivalent qualifications and all initial refusals. P035-007 owns account-delivery isolation; frozen P18/P20 and broader exclusions are unchanged. | Resolved for the omitted-config room-v10 profile; global Agora partial, federation and production readiness stay separate |

### P17: Public-Gossip Resource Links

Based on [P026 resource references](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#12-references-in-opinions-and-gossip)
and its [implementation recommendations](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#implementation-recommendations).
Scope is explicit `public-gossip.v1` publication, not private Whisper intake or
automatic publication of private associations.

Reuse `node:agora-projections/src/lib.rs` pair-link decoding and replacement,
projection cursor/diagnostics, and existing API/UI read paths. The minimal local
edge is `(source record/id, relation = see-also, target ResourceRef)`; the signed
payload remains authoritative. Related edges must not be inserted into the
`record/about` subject index or interpreted as endorsements, verified identity,
or evidence. Unknown namespace values remain opaque. No additional wire schema
or persistent source of truth is required.

Completion gate: retained fixtures show exact kind/id preservation for
`pl-nil-pwz` and an unknown kind, namespace separation, idempotent ingest and
replay, bounded/paginated query and escaped UI navigation. Query results must
obey source-record access/visibility and gossip expiry policy; retention/rebuild
must not leave stale visible edges. Missing targets remain inspectable references
without automatic external fetches. Keep the existing public-signals topic and
epistemic/disclosure gates. Link queries and UI must not disclose a hidden source
through counts or navigation. Reconcile Node evidence and ledger at delivery.

P17 has no dependency on P026-001 or P026-002 completion: it consumes the same
pair contract and may reuse their helpers when available. Its evidence is
separate from P026-003 basic publication/subject-lookup acceptance.

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

The earlier 2026-10-16 P035-007 checkpoint implemented independent recovery with a focused four-case
Synapse isolation proof at Node 5d5392b2 / Orbidocs b3813122. The restart correction
is separately qualified by five focused cases at Node b0a44ade / Orbidocs aee179e,
including a publication-bound noncanonical room. It remains partial:
the full campaign waits for P035-009 external retention. The filtered,
page-durable long-history, empty-bootstrap and late-binding paths are qualified by
P035-006 on unmodified Synapse; token-cycle/legacy-anchor controls keep their conformance scope. Archive identity is tar/member
content, with gzip/zlib provenance and bounded streaming extraction.

The full 2026-10-19 continuation closes P035-007/009/010 for per-room-recovery-v2:
34 Matrix/five SQLite cases, continuing live delivery during two 640-record history
workloads, complete admission matrix, restart/replay and both independent PDU gates.
All 2041 Node PDUs fit 65536 bytes (maximum 49927); confidence-0.5 gossip and permitted
Whisper retain exact bytes. The complete 16511847-byte set has identical original,
extracted and fresh-retrieved qualification, with payload outside Git and 2282442
bytes of controls. The original 128 MiB retention refusal remains an attested
measurement receipt; explicit 192 MiB compression changes no tar/member bytes or
decoder/budget ceiling. Earlier P18/P20/P21 and focused results keep their scopes.
Evidence: `node:docs/evidence/matrix-opaque-envelope/2026-10-19-room-recovery-full/README.md`.
Global Agora partial, one-volume retention limitations, federation, all Whisper,
P095 inline-unlock and release/production gates remain separate.


The separate 2026-10-19 review closes P035-010's implausible-delay correction:
four focused Synapse cases at Node ac386090 / Orbidocs fbba8e73 qualify the checked
24 h boundary, reasoned local operator CAS escape, restart, live confidence-0.5
and exact-source replay. The 142758-byte complete proof is externally retrieved;
full gates remain the original campaign. Original failed attempts are retained as
cause-only capsules with preserved qualifier refusals. Source deduplication before
larger campaigns (P035-011), qualified independent copy and manual release verify
(P035-012), and S039/batch CAS (P035-013) remain open, with unchanged budgets.
