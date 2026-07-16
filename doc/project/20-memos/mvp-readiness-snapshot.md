# MVP Readiness Snapshot

Snapshot date: 2026-07-16.

This table is an estimated cross-document readiness snapshot for canonical Story, Proposal, and Solution documents.

Scope rules: localized duplicates (`*.pl.md`), indexes, backlog files, implementation notes, coding guides, and generated registries are excluded. Solution rows use the main `NNN-*/NNN-*.md` document for each component.

Estimation basis: `node/docs/MVP.md` defines the hard-MVP story set (`story-000`, `story-002`, `story-005`, `story-006`, `story-008`, `story-010`, `story-011`); `doc/project/60-solutions/CAPABILITY-MATRIX.en.md` provides coarse implementation status; each document text is used as fallback when no capability row exists. `part of MVP` tracks the hard-MVP story set plus explicitly promoted release-blocking proposals/contracts, and is treated as a release-blocker flag: a row with `part of MVP = true` must be ready before the hard-MVP release can be called closed. `MVP ready` may still be `true` for a post-hard-MVP document when its own MVP slice is implemented. `readiness %` is a document-level engineering estimate over contract clarity, implementation evidence, test coverage, and remaining risk; it is not computed mechanically from the number of capability rows and is not a release-signoff fact.

Hard-MVP release-blocking stories:

- `story-000`
- `story-002`
- `story-005`
- `story-006`
- `story-008`
- `story-010`
- `story-011`

Hard-MVP release-blocking proposals/contracts:

- `proposal-048` / Sensorium OS action-class runtime
- `proposal-076` / `federation-root.v1`
- `proposal-081` / horizontal causal, replication, and scoped-nym-proof primitives

Change basis: this refresh incorporates the current worktree state on 2026-07-16. It retains the previously recorded hard-MVP and federation-root slices and adds the latest P063/P064/P066 closure: live provider-backed image generation/edit, durable evaluation-gated `train.adapt`, bounded repair and output-rail diagnostics, egress-class limits, shared participant-id and monotonicity primitives, explicit local-model provisioning UX, typed communication-control admission including native adapter-envelope mapping, session-memory projection, locale framing, deterministic embedding cache, Inquiry Flow compilation, and their synchronized Node ledger, proposal trackers, and tests. It also includes the explicit Assistant Channel to Agent escalation, recovery, outcome-draft, and render-only acceptance slice tracked by Solution 045, plus the post-MVP Room-attested Corpus-chair binding, inert Corpus answer-draft acceptance, bounded node-local WSS deliberation with metadata-only authority observations and restart recovery, separately authorized signed Agent-chair answer publication, and registered local-policy evaluation of role assignments and policy-rendered instruction overlays through Inquirium host prompt assembly, with append-only delta recovery, tracked by P069/P073 and Solutions 036/038.

The 2026-07-16 refresh additionally closes Proposal 082 and promotes Solution
046. Sensorium Interfaces now has the pure pull-batch core, eight schemas,
classification and Passport bindings, durable host lifecycle, Sensorium and
Workbench source adapters, signed direct-peer reads, loopback SSE, and the WSS
Room latest-state projection with current dual-authority checks. This remains a
post-hard-MVP component whose own MVP slice is ready; it is not added to the
release-blocking proposal list. Subscription reads serialize only per lease,
Passport admission is atomic, direct-peer target binding is explicit, and active
Room projection pumps are capped at 64. The follow-up hardening rejects bare
grantee ids, intersects Room authority only by canonical stable subject key,
separates SSE and Room causal traces, distinguishes revoked Passport replay,
checks tier-vocabulary drift in CI, and adds a negative frame fixture.
The latest post-MVP extension replaces the closed source enum with a generic,
bounded adapter registry, migrates all existing Sensorium and Workbench sources,
adds an admitted Artifact Delivery pointer snapshot source, and exposes process-local
operator read metrics with bounded source/carrier/delivery-kind dimensions, flat
revoke-commit timing, and isolated source-registry, active-subscription,
metric-accumulator, and Room partial-failure reporting. Daemon startup now requires
all four built-in adapters, while the exact-name, fail-fast four-carrier conformance
runner uses separate build/test timeouts and exercises bounded host load, signed
direct-peer reads, SSE revocation, and Room projection revocation.
These additions improve extensibility and evidence
collection without changing the component's `100` readiness estimate or adding it
to the hard-MVP blocker set.

The same closure is now hardened with a uniform 32 MiB pre-read image-source
limit, a 96 MiB decoded adapted-model artifact cap, operation-kind/status-scoped
paged training recovery, recursive provider-usage aggregation, and full
classification no-broadening checks for crisis-candidate projection. These are
contract and recovery hardening changes; P063, P064, and P066 are now at `100`
for their tracked implementation slices.

The P064 prompt-assembly policy slice remains tracked as `done`: support for a
future text-generative operation will receive a separate work item only when the
operation exists. Its previously additive communication-dialect, session-memory,
deterministic-cache, Flow-IR, and locale-policy slices now have bounded contracts
and host implementations, without moving plan execution or summary production
into Inquirium.

The Inquirium refresh in this snapshot additionally includes executable
classify/rerank verticals, provider-native structured output under host
validation, prompt-epoch promotion gating, baseline profile rendering,
host-derived context-grant binding, complete local context resolvers,
operator-question cancel/supersede, and transcript blob/projection/feedback
durability. The latest closure adds a live provider-backed image path, the
durable bounded `train.adapt` execution/evaluation/publication worker, bounded
structured-output repair and rail diagnostics, egress-class ceilings, shared
participant-id and monotonicity primitives, and explicit local-model
diagnosis/provisioning commands.

The current Inquirium closure also adds archive-before-prune context-grant
revocation and bounded scheduler maintenance, non-empty participant projection
rebuild from validated Memarium facts, resolved retention admission, exact
participant/feedback-bound revocable training grants, atomic baseline profile activation,
registered notification widgets with server-side answer validation, host-owned
mode/class escalation policy, complete assembled-prompt token accounting, and
explicit fail-closed SQLite schema migration checks.

The latest P063/P064/P066 closure adds forward-only host-keyed assistant trace
references, automatic sustained-degradation and boundary-risk escalation,
metadata-only crisis candidates, provider-backed OpenAI embeddings, supervised
OpenAI/Anthropic lifecycle coverage, explicit remote model-acceptance and egress
acknowledgement, semantic transcript tags, canonical participant-bound
cross-device export/import, content-addressed training dataset manifests with
grant-rechecked local `train.adapt` admission, and complete bounded
summarize/transform/image contract verticals. Image output remains artifact-only;
the deterministic backend remains the conformance/smoke oracle, while the
supervised provider adapter now supplies a live image generation/edit path under
the same host verification and object-store boundary.

The P081 review closure additionally distinguishes non-canonical causation from
operation-id conflicts, unifies component-domain-separated receipt identifiers
across the four first consumers, strengthens durable nonce concurrency and Room
boundary tests, and bounds Agora proof clock skew. These are hardening changes;
P081 and Solution 043 remain at `100` for the hard-MVP slice, while Inquirium
adoption and signed revocation-snapshot admission remain explicit post-MVP
questions.

The Workbench refresh in this snapshot also includes native non-Workbench
broker providers, explicit artifact handoff, bounded argv-prefix consent and
operator UI, shared sidecar merge, the required Rust actuation bridge, the
managed `fixture-copy.v1` Sensorium Virt executor, and host-verified
Agent/Corpus/Room tool-request lineage.

Recent component deltas:

- Proposal 081 / Solution 043 are hard-MVP ready. Canonical causal context and
  receipt contracts are consumed by Scheduler, Bounded Deferred Operations,
  Artifact Delivery, Sensorium, and redacted P074 trace adapters. Contact Catalog
  and Seed Directory consume the bounded replication core with domain-owned trust
  and merge policy. The durable scoped-claim runtime, Ed25519 nym-certificate
  adapter, and Agora/Room consumers are implemented with replay, expiry, candidate
  binding, and stale-revocation refusal. The repeatable 13-check acceptance runner
  passes and emits a metadata-only trace bundle. Stronger zero-knowledge suites,
  Agora cross-relay mesh, federated Memarium replication, and universal consumer
  migration remain explicitly post-MVP.
- Proposal 082 / Solution 046 are MVP ready outside the hard-MVP release blocker
  set. The implementation has one carrier-neutral bounded read-next contract,
  exact local and Passport authority, revocation/restart coverage, direct-peer,
  SSE, and WSS Room adapters, and temperature plus collaborative Workbench
  acceptance tests. Canonical grantee refs prevent cross-kind Room identity
  collisions, carrier-specific traces preserve diagnostic provenance, and the
  bounded source registry now includes an admitted Artifact Delivery pointer
  adapter and fails startup when any built-in adapter is absent. Host-local
  aggregate read metrics separate delivery kinds, expose revoke transaction commit
  duration without mislabeling it as enforcement lag, isolate every unavailable
  operator section, reset explicitly on restart, and pair with the exact-name
  four-carrier conformance runner and separate build/test timeouts to provide the
  measurement boundary for the remaining evidence-gated decisions.
  Provider push, descriptor search, and split management authority remain
  evidence-gated post-V1 decisions.
- Communication Protocol Baseline is now hard-MVP ready as a historical baseline:
  Proposal 002 explicitly maps its implemented or superseded areas to the current
  runtime owners (P014/Solution 000 transport, P056/Solution 024 TLS trust,
  Seed Directory/Federation Root discovery trust, Capability Registry/Binding
  admission, AD/INAC payload transport, and Messaging/Room group semantics) and
  no longer carries independent hard-MVP implementation blockers.
- Proposal 048 / Sensorium OS Action Classes is now hard-MVP ready for the
  minimal reference connector runtime: `sensorium-os` normalizes class-aware
  action catalog entries, reports per-action availability, executes script-backed
  C1/C2 entries, rejects allowlist-local sensitivity overrides, enforces exact
  and prefix `result_pointer_fields`, blocks C3/C4/C5 under emergency posture
  without an explicit host-policy exception, and fails closed for unavailable
  C3-C7 classes until their enforcement envelopes exist.
- Proposal 071 / Solution 042 now have the host-owned operator-consent
  spine for exact and bounded-prefix Workbench terminal commands: typed request/decision schemas,
  daemon persistence and submit/list/detail/revoke/projection APIs, P066-backed
  operator questions and durable notifications, Workbench
  `sensorium-workbench.consent-descriptor.v1`, matching `allow-once` admission,
  `remember-exact-argv`, and workspace-bound `remember-argv-prefix` sidecar
  projection that refuses to loosen egress,
  credential, timeout, or output-byte caps. The latest hardening also makes
  operator-consent read/projection APIs reject module callers, replays duplicate
  consent requests by semantic request equality, validates Workbench consent
  descriptor and sidecar entry schemas, and refreshes Workbench sidecar profiles
  through a bounded TTL. It now also requires active
  `node-operator-binding.v1` authority for consent answers and revocation,
  gates durable answers through host capability authorization policy, and
  filters expired entries, inactive operator-binding entries, and capabilities
  no longer durable-grantable by host policy from the effective sidecar with
  `consent-expired`, `consent-operator-binding-inactive`, or
  `consent-capability-not-grantable` diagnostics, which the Workbench connector
  now imports into operator-visible config diagnostics. The same host-owned
  consent spine now projects granted Sensorium OS action-catalog deltas into
  `sensorium-os.action-catalog-sidecar.v1`, materializes the sidecar into the
  Sensorium OS middleware config tree, publishes binding/delta/sidecar schemas,
  and the connector loads valid non-overriding deltas into its effective
  catalog with a bounded TTL/mtime cache. A shared append-only sidecar merge
  core now owns conflict/provenance semantics, node-ui exposes consent
  inspection/revocation, and `fixture-copy.v1` provides the first managed
  virtual executor without claiming process isolation.
- Raw Signal Access is now hard-MVP complete as both proposal and solution:
  hook-chain runtime and direct JSON-e-flow dispatch preserve raw context only
  in memory, expose it only to declaring executors, strip it from final
  envelopes, and now enforce declared raw-signal / component-trace byte limits
  by replacing oversized exposures with `sha256:` digest metadata.
- Bounded Local Server Runtime is now hard-MVP complete: the shared Rust and
  Python bounded-server primitives were already migrated across the production
  local server surfaces, and the remaining daemon-context overload gap is closed
  by a real health-endpoint integration test that forces `max_connections = 1`
  and observes fast HTTP 503 rejection.
- Host-Owned Module Store is now hard-MVP complete: the four module-store host
  capabilities have committed local schema-gate contracts, daemon routes
  validate raw request and response JSON before and after typed dispatch, and
  Story-009 verifies supervised module-store writes plus daemon restart/replay
  through real processes.
- Sealer, Capability Advertisement, and Pseudonym Vault / Key Roles are now
  aligned with their component trackers as hard-MVP complete solution slices.
  Sealer's hard-MVP `done` status is backed by the daemon passport-aware
  dispatch gate, real revocation-view diagnostics, sealer master lifecycle,
  audit parity, and HTTP dispatch coverage. Capability Advertisement's `done`
  status reflects the registry-backed fail-closed advertisement path, while
  remaining per-passport ingress verification, lifecycle rebuilds, reusable
  schema retrieval, and Seed Directory reconciliation are post-MVP hardening.
  Pseudonym Vault / Key Roles was already marked `hard-mvp-done` in its
  solution tracker and caps sidecar; the snapshot now reflects that source of
  truth.
- Proposal 003 and Proposal 011 are now hard-MVP ready for the selected-responder
  procurement slice. `question-envelope.v1`, `procurement-offer.v1`, and
  `response-envelope.v1` are schema-gated at daemon ingress; the host-owned
  service-order bridge derives full schema-valid question and offer artifacts;
  selected-responder executions persist transition facts, offers, contracts,
  responses, receipts, disputes, and settlement-aware closure. The full P003
  NATS/JetStream plus Matrix collaborative-room transport remains post-MVP, and
  P011's broader collaborative/dispute lifecycle remains a later extension.
- Proposal 072 is now implemented and promoted to Solution 037 for the hard-MVP scope: `capability-registry.v1` is the machine source of truth, formal capability ids are checked for canonical grammar, status, wire-name uniqueness, derived surfaces, and use-specific eligibility, and capability advertisement, passport validation, host capability dispatch/routing, literal control-plane `POST /v1/host/capabilities/*` routes, and supervised middleware reports fail closed for unregistered or ineligible formal ids. `capability-authorization-policy.v1` adds the checked P071 Workbench/Interaction Broker authorization-policy sidecar for required grants, caller posture, approval mode, autonomy floor, and COI policy; daemon startup preflight validates both registry and policy, while runtime grant enforcement remains host-policy owned. Federation namespace governance remains a separate post-P072 proposal track.
- Proposal 076 / Solution 041 / `federation-root.v1` is hard-MVP ready while remaining a
  release blocker. The contract defines the `data-dir`-scoped federation root
  used to select `federation_id`, bootstrap seed peers, Seed Directory
  endpoints/trust, sovereign subject refs, and official-service endorsement
  authority before the node enters the network. Node runtime now has the
  node-wide federation selector, startup schema-gated loading from explicit
  data-dir packs, Ed25519 signature verification, participant self-signature
  checks, org custody-policy evaluation for `any-authorized` / `threshold`,
  key-counted threshold semantics, same-federation data-dir state guards,
  rollback/digest-swap refusal, a fail-closed default when no explicit root pack
  exists, and a raw-digest-pinned bundled `orbiplex-main` dev/demo fixture behind
  explicit `federation.allow_bundled_fixture_root = true`. The hard-MVP slice now
  also includes `federation-service-endorsement.v1` as the sole official-service
  proof, participant/org verifier core, root-pack endorsement revocations,
  Seed Directory attach/read/revoke surfaces, own-node endorsement fetch/install
  cache, capability-advertisement endorsement projection with per-use
  re-verification, a thin participant-sovereign operator issuance API, offline
  MVP multisig ceremony tooling for root packs and endorsements, strict
  rejection of unauthorized excess endorsement signatures, production
  `orbiplex-main` ceremony profile checks for manifest digest/threshold parity,
  explicit-roster root draft authoring, strict deterministic assembly,
  org-threshold shape, charter-version
  `policy_ref`, at least a 2-of-3 unique signer-key threshold, and rejected
  signature refusal, optional
  `seed_directory_bootstrap[].tls_certificate_sha256` projection into
  Seed Directory sources with HTTPS-only runtime enforcement and peer leaf
  certificate digest verification, and restart-only federation-root activation
  with specific first-activation/removal/change reload events. The hard-MVP
  acceptance harness seeders now write explicit signed
  local root packs and embed signed Seed Directory official-service
  endorsements for federation-endorsed bootstrap entries, so local Story-005,
  Story-009, Story-010, and Story-011 profiles exercise the same root-backed
  authority chain as runtime consumers. Story-011 now also proves the provider
  side of the projection: its managed smoke creates provider participants during
  first boot, inserts B/C participant attestation roots with matching
  self-signatures into the refreshed runtime root, restarts, asserts active
  `/v1/seed-directory` trust for Node B, and only then issues/publishes
  `corpus.provider` capability passports. Concrete production roster/keys,
  final charter adoption and appeal body seating, consumer-specific alliance
  admission enforcement from Proposal 079, optional remote co-signing/FROST-style threshold
  protocols, and broader
  multi-federation matrix polish remain post-MVP governance/testnet follow-ups,
  not release blockers for the runtime contract. Room/Solution 036 now explicitly
  grounds `federation-local`, `cross-federation`, and `global` exposure in the
  active P076 `federation_id` instead of letting any carrier define federation
  authority.
- Proposal 078 now has its local post-hard-MVP intake spine implemented: the
  canonical `weak-signal-finding.v1` schema and fixtures are schema-gated at
  import/export, daemon exposes explicit operator import/list/detail/review
  endpoints, a dedicated SQLite Harvester review store owns review state, the
  first filesystem Markdown/text adapter is bounded under the node data-dir, and
  accepted findings can create local Whisper draft stubs without publishing.
  Directory-watch automation, network-capable harvesting, public gateway intake,
  and collector corroboration remain deferred profiles.
- Proposal 018 / Solution 040 is no longer a low-coverage placeholder. Code review on
  2026-06-22 confirmed schema-gated `participant-capability-limits.v1`
  import/export, durable daemon replay, operator HTTP import/list/detail/clear,
  hard-block enforcement for the current procurement/response operation set,
  protected-floor behavior for `signal-marker/send` and `dispute/file`,
  procurement ranking penalties through `priority-factor`, and per-participant
  cooldown through `rate-limit-factor`. Follow-up hardening added reasoned clear
  tombstones, dead/already-expired hard-block import rejection, stale
  `recorded-at` overwrite rejection, monotonic `last_cleared_at` replay so old
  records cannot reappear after clear, full participant-id validation on clear,
  schema-gated list/detail export, bounded local control bodies, runtime
  soft-factor and `reason/ref` validation, and metadata-only operator SSE
  refresh events for import/clear.
  P018 is now hard-MVP complete; remaining questions are post-MVP scope expansion
  and registry/policy refinement.
- Artifact Delivery moved from "MVP transport foundation" to hard-MVP complete: Memarium custody target-space policy, profiling counters, metadata-only observers, Matrix mailbox hardening, and `object-store-indirect` fetch/rehydrate through `artifact-object-pointer.v1` are now documented and implemented. Lower-level zero-copy and Matrix media variants remain post-MVP optimization layers.
- Notifications now have a local durable MVP foundation promoted to Solution 039: schema-gated `notification.create`, temporal SQLite event log, derived queue projection, JSONL audit mirror, SSE state ping, operator UI, legacy `notify_emit` adapter, first daemon-owned actions, profile-aware manifests, and destructive temporal compaction for local notification history. They remain partial because pod-user UX, OS notifications, and cross-node aggregation are later layers.
- Node UI security readiness advanced: Solution 001 now documents and implements physically separate public/user/pod-user/operator router strata, participant-session enforcement for user-mode routes, header-first reflective CSRF without the legacy CSRF header alias, local user-action audit JSONL, `security-audit.v1.sqlite` query projection with 90-day retention, `/admin/audit/user-actions`, and optional best-effort Memarium `user-action.v1` mirroring. Proposal 052 now carries the same audit/redaction/retention contract for the Tauri-hosted shell. Node UI remains partial because richer desktop settings writes, external preview isolation, pod-user auth, and native integration hardening are still later product/runtime layers.
- Contact Catalog hard-MVP is tracker-complete: Proposal 058 and Solution 025 now report the implemented route-set `contact-claim.v1` / `contact-lookup-result.v1` runtime, supervised service, local contact recovery, tombstone/revocation replay, PSI/blinded lookup, provider sync, provider trust controls, and contact-control-vs-identity wording as done for the hard-MVP slice.
- Messaging hard-MVP is tracker-complete: Proposal 060 and Solution 027 now report supervised messaging runtime, daemon-mediated contactability provider discovery/challenge/redeem, Contact Catalog lookup/contact-request handoff, classification-bearing private-direct AD/INAC delivery, `messaging.flag.v1` read/unread replay, recorded-message lineage plus best-effort encrypted Agora Vault storage, Node UI controls, user-mode wizard readiness for pseudonymous-only or public-handle-draft messaging setup, and Story 010 strict `ad-smoke` as done for the hard-MVP slice. Latest hardening adds EML body/profile recovery, route-key normalization, mark-read routing fixes, readiness/routing retry gates, SSE mutation guards, and conversation diagnostics. Production privacy/federation expansion, receive-passport restoration matrices beyond the current sealed local recovery path, Maildir body encryption, richer per-recipient vault key wrapping, HTML rendering, group messaging, and live multi-device push remain post-MVP work.
- Inquirium is now promoted to Solution 044 as an MVP-capable bounded-inquiry
  organ rather than only a runtime substrate. The Assistant Channel is promoted
  separately to Solution 045 as the human-facing interaction surface over that
  organ, while Proposal 064 remains their shared implementation recommendations.
  The solution has a first `generate` vertical through `inquirium-core`,
  daemon `inquirium.generate`, JSON-e Flow ingress/preflight, NSE runtime
  selection, deterministic stub runtime, classification-aware request
  validation, metadata-only trace records, direct embedding, report-backed
  conformance, and the direct data-plane lease/batch-embed pilot for
  lease-backed work. `inquirium.classify` and `inquirium.rerank` now continue
  from bounded pair-validated contracts through inference-granted host
  capabilities, runtime/model-binding selection, deterministic and local
  HTTP/simulator execution, shared budgets, host-keyed metadata-only traces,
  and conformance fixtures. The same bounded host boundary now exposes
  summarize/transform through generate lowering and image generate/edit through
  explicit image candidates, operation-bound leases, verified artifact intents,
  a uniform 32 MiB source-media cap, and artifact-only responses. Proposal
  064's core runtime-adapter foundation is
  implemented across model-runtime catalog v0.2, runtime-candidate routing,
  HTTP/stdio adapters, remote provider adapters, embedding contracts, durable
  lease APIs, deferred `batch.embed`, verified artifact descriptors, signed
  adapter manifests, conformance report storage/runner, host-owned prompt
  assembly (`PromptAssemblyPolicy`, daemon `inquirium.prompt_assembly`
  HostRoot/Organ/Operation sourcechain with default fixed non-empty host-root
  boundary plus coarse temporal context layer, real bounded host `content/ref`
  materialization, config-load validation for generate candidate sourcechains
  and base prompt refs, scoped adjustments for profile/model-binding/
  adapter-instance, manifest-declared instruction roles, pure assembler,
  `inquirium-host` adapter request planning, NFC-normalized canonical
  instruction hash, caller boundary count, content-source trace, fail-closed
  tests), and the first output-boundary foundation (`output_contract.schema/ref`,
  host-owned output schema registry with a narrow JSON Schema subset, structured
  JSON shape limits enforced without materializing oversized serialized buffers,
  at most two policy-admitted metadata-only repair attempts, adapter structured-I/O
  declarations, `GenerateOutputEnvelope` with bounded params/control, typed
  unsafe output preserving usage/cost accountability, configurable deterministic
  host I/O rails, safety-critical effective budget diagnostics with typed
  `budget_exceeded`, provider model snapshot/effective sampling trace, redacted
  output-projection traces carrying schema digest plus violation codes/counts,
  deterministic-stub/simulator structured happy paths, and host-capped assistant
  output, plus the `inquirium-host` stratum for generate budget/prompt/adapter
  request planning, reusable Inquirium config types/defaults, output-schema
  normalization, embed admission predicates, bounded duplicate-free batch source
  lease refs, symlink-hardened file leases with capped metadata, assistant
  output/transcript-fact planning, table-driven daemon dispatch for
  `inquirium.*` host capabilities, typed returned-value effect intent DTOs,
  daemon effect-intent interpretation for trace, assistant transcript writes,
  durable generate/embed/assistant budget-charge records with idempotent replay
  protection, scoped per-principal/per-session/per-operation/per-agent budget
  preflight and final-charge enforcement, and shared daemon artifact-output
  intent execution).
  OpenAI and Anthropic adapters now compile the admitted schema subset into
  provider-native structured-output requests; native selection intersects
  adapter and selected runtime/model declarations, and host schema/rail checks
  still run. OpenAI direct embeddings use the same supervised adapter and
  runtime/model-binding policy boundary. Full schema ecosystem features such as dynamic
  refs/recursion/combinators/grammar artifact caching, richer optional evaluator
  critics, and provider packaging remain open. Deterministic embedding caching
  and pure CandidatePlan-to-Inquiry-Flow compilation are implemented; durable
  plan execution remains correctly owned by Agent and other effect strata. The
  current host boundary already has schema-owned
  string redaction, bounded multi-violation diagnostics, explicit egress-class
  limits, complete repair-attempt accounting, live image execution, and a
  durable evaluation-gated training worker. Solution 045 has a local-only
  assistant turn capability, host-capped assistant output, principal-scoped
  transcript fallback with local-control excision markers, Memarium-backed
  transcript fact attempts with local fallback/read-index, idempotent turn
  replay, metadata-only assistant trace/feed, direct local OpenAI-compatible
  baseline assistant target coverage with a validated operator override,
  profile-scoped baseline-assistant conformance/freshness gating with
  deployment-controlled `host-class/...` scope, local-transport allowlisting,
  16 KiB host-visible output-cap assertion, and schema-gated
  candidate-requirement diagnostics, hard-MVP readiness gating through
  `inquirium.baseline_assistant_required`, operator-visible
  `inquirium.baseline-assistant` status with `registry-error` and stable
  failure reason projection, `run-conformance` bootstrap paths,
  render-only Node UI affordance under
  `/admin/inquirium/assistant`, a durable participant/session/source-bound
  context grant registry, host-owned operator-inline/Relationship/Memarium/
  Query/Messaging/Artifact/Dataset resolvers with classification ceilings and
  exact egress-ack binding, operator-question
  widget registry/projection contracts plus a bounded durable daemon registry
  with `expires/at`, conservative `default/on-timeout`, lazy/recovery timeout
  sweeps, fail-closed late-answer handling, and notification/action expiry
  projection, source-component-scoped notification ids, and idempotent
  notification-store projection path, explicit cancel/supersede transitions
  with paired notification closure, digest/size-verified transcript object
  descriptors and replay hydration, participant-scoped text/tag projection with
  semantic tags, canonical participant-bound transcript bundle export/import,
  inquiry-feedback persistence, mode-keyed rigor policy, the shared
  ordered-axis resolver/monotonicity helper, and the canonical shared
  `participant:did:key:` validator. The baseline profile renderer emits loopback
  Ollama or managed digest-pinned `llama-server` operator config without an
  extra proxy and provides explicit doctor/pull/status/deactivate operations.
  Automatic sustained-loss/boundary-risk notification projection,
  metadata-only crisis candidates, remote model acceptance/egress acknowledgement,
  content-addressed training manifests, and grant-rechecked local
  `train.adapt` admission and execution are implemented; training recovery is
  operation-kind/status scoped and paged, cancellation is compare-and-set, and
  decoded model artifacts are capped at 96 MiB. Solution 044's bounded organ,
  P064's tracked implementation recommendations, and Solution 045's assistant
  channel are MVP-ready. Richer schema/evaluator profiles, provider-binary
  packaging, optional scheduler-owned timeout surfacing, and Agent-owned effect
  governance remain additive later work rather than incomplete P064 tracker
  items.
- Proposal 073 introduces Agent as the bounded stateful orchestration organ above Inquirium. Its node-local FlowNode and Assistant Channel scopes are complete: `agent-core` owns substrate-free lifecycle, fork, step, memory, binding, outcome, Assistant escalation/acceptance, and effect contracts; `agent-host` owns pure step decisions, operator-profile admission, and the closed table-driven Sensorium/Artifact Delivery effect-policy registry; and the daemon exposes lifecycle, proposal, binding, bounded controller-run, Assistant escalation/draft-acceptance, and contextual effect-dispatch capabilities. Local control is administrative authority, while module calls require explicit bounded JSON-e Flow `agent_grants`, Agent ownership, and target-capability allowlists. Memarium Personal facts remain the source of truth; startup performs bounded replay, partial-bundle and interrupted-outcome repair, immutable admission-snapshot recovery, current-policy quarantine cascading through descendants, and terminal/expired-owner lease reconciliation. Assistant approval is durably recorded before Agent/binding authority, uses the durable operator-question record as typed authority, rejects unapproved bindings during replay, and idempotently completes interrupted materialization. The binding's narrowed budget and wall-time deadline are effective across controller, Inquirium, lease, fork, reaper, and status paths. The general real HTTP process smoke covers spawn/status/binding/controller/suspend/resume/controller-mediated fork/stop plus durable recovery after `SIGKILL`. A second process smoke covers Assistant turn, explicit escalation, pending-question restart, exact replay, approval, denial, timeout, bounded controller execution, content-addressed `agent.outcome.v1`, and render-only acceptance. Ambient Assistant binding is denied, generated content stays outside status and notifications before acceptance, and acceptance fixes publication authority to false. The active controller executes admitted Inquirium, inert effect-proposal, and child-spawn actions through their owning host strata; Inquirium remains constrained by classification, pinned profile, runtime allowlist, and grants. Effect dispatch consumes transport-independent host plans, persists bounded deferred/completed/failed execution outcomes, avoids target reinvocation on exact replay, and reconciles Deferred Operation Registry terminal state with lease release through a bounded scheduler job. Child reservations reconcile bottom-up, lease acquisition is charged, and old inactive lease details compact to restart-safe audit tombstones after the configurable 30-day default horizon. Summary-producer authority is the intersection of Capability Registry-eligible modules and the host allowlist. The post-MVP Corpus-chair extension is now implemented: signed and fresh Room evidence from the node-local round authority admits one exact query/room/participant binding, and Corpus durably accepts its `agent.outcome.v1` as an inert answer draft without publication authority. Corpus room policy, signed invitations, typed control-plane failures, AD-owned transport idempotency, Corpus-owned semantic replay by signed `invite/id`, configured remote trust-root verification, bounded live WSS join/readiness/messages, metadata-only authority observations, stable authority bind and subject-sequence recovery, controlled session rejoin, and recipient restart recovery are implemented. A separate local-control Corpus transition validates current quorum, room high-water, chair identity, evidence, output digest, and idempotency before signing and publishing the inert Agent draft; Agent authority remains non-publishing. Federated Room transport and remote Room-authority trust remain later work and do not change the hard-MVP verdict.
- The latest post-MVP Agent/Corpus profile is also implemented without changing
  the hard-MVP verdict: Story-011 selects B while C remains a competing bidder,
  admits B as a Room-attested `corpus-participant` Agent, routes one inert
  `corpus-reasoning-turn-proposal.v1` through HIL-gated `corpus.room.turn`, wakes
  A's chair Agent through an epoch-bound Interaction Broker `room-event` watch,
  and accepts the chair result only as an unpublished Corpus draft. Process
  coverage includes altered-evidence denial, metadata-only durable watch replay,
  dirty restart, stale cursor refusal, exact effect replay, exact Room-scoped
  module-watch authority, skew-tolerant turn expiry, schema fixtures, and absence
  of ambient publication. P069, P073, Solution 038, and Story-011 trackers carry the same
  evidence; readiness percentages remain unchanged because both documents were
  already at their completed node-local slices.
- Story 005 remains hard-MVP complete, and its post-M4 productization tracker now lives in the Whisper implementation note instead of a workspace-root draft file. The closed slice has a CI-runnable Inquirium acceptance bridge: an opt-in supervised simulator adapter is routed only through model-runtime/Inquirium by `runtime/ref` and host-owned `model.binding/ref`. `whisper-core` carries the production-shaped policy primitives for routing failure mode, source class, outbound privacy resolution, correlation policy explanation, association-room proposal lifecycle, public-gossip promotion, and bounded trace integrity/privacy. The current Node worktree consumes those primitives in the publish path: `whisper-intake` performs outbound privacy preflight before public/private signal publication and now implements `whisper.trace.publish` with exact one-time operator consent for inline disclosure, transient byte validation, and metadata-only read models. Trace authoring atomically reserves idempotency keys, independently bounds inline bytes, extensions, and total JSON, and applies a 30-day default retention sweep to its local read model. Agora enforces public trace topic/disclosure admission and projects traces outside signal thresholding, while AD/INAC admits private traces through the existing signed-envelope carrier. Story-005 asserts the exact `agora-publish` and `inac-direct` carriers, proves that private traces stay absent from Agora projection, and retains its private-signal regression guard. `agora-projections` and `agora-service` also provide a minimal local association-room lifecycle seed plus public-gossip promotion drafts from accepted rooms, with authenticated actor binding, bounded lifecycle facts, FK-backed proposal refs, and bounded opaque lineage refs. These move Proposal 013 closer to post-M4 productization while preserving the readiness interpretation for unfinished product/runtime surfaces such as real Anon relay transport, production semantic correlation, full association-room case management on the accepted signed room-event log over Artifact Delivery with multi-Agora fanout/merge, bounded replica retention status, and per-thread predecessor digest links, final public-gossip publication runtime, live Monus/Sensorium source verification, richer room/curation UI, and remote model deployment.
- Shared Offer Catalog is now hard-MVP complete. Proposal 067 and Solution 033 document the extracted shared Python offer-catalog runtime, Agora replay, fail-closed Agora/Seed Directory admission, Arca embedded-cache reuse, query parity, withdrawal active filtering, public/shared catalog deployment profile (`node/middleware-modules/offer-catalog/config/profiles/public-shared-catalog.json`), automatic `shared-offer-catalog` passport publication readiness with classified pending reasons, redacted Host Agora and Seed Directory admission diagnostics, and a local public-profile smoke runner (`node/tools/acceptance/shared-offer-catalog-public-smoke.py`) covering authorized replay, bad-signature refusal, unknown-provider refusal, withdrawn-offer inspection semantics, and the HTTP query surface. The remaining public-profile operating policy is now resolved and enforced where applicable: passport renewal is supervisor-driven by default, and non-loopback Agora URLs must use HTTPS/TLS with Node fail-closed replay validation. Remaining work is post-MVP production hardening such as broader monitoring matrices and eventual legacy peer-message retirement.
- Proposal 080 is complete through P080-020. Bundled factory data now selects `channel_json` or `http_local_json` explicitly and records whether a product listener remains. Eligible host-only modules project to the shared channel without allocating per-module ports; intentional network and mixed product listeners remain explicit. Agora Verifier and Snooper use the shared Python channel adapter. Operator-installed `http_local_json` remains a visible explicit legacy compatibility path, while stale listener keys under channel-only module config fail closed. Story-005 proves host-owned `runtime/ref` and model-binding invocation over the channel plus stop/non-routable/restart; Story-009 and strict Story-010 also pass.
- Corpus and Story 011 are tracked as hard-MVP blockers through Proposal 069 and Solution 038. Its MVP slice is
  intentionally narrow: topic taxonomy/resolution, topic-scoped offer discovery,
  `question-envelope.v1`-decorated query broadcast, bid-state aggregation, and a
  single-provider P011/P016 settlement path. The contract gate is implemented:
  canonical schemas and examples for topic taxonomy/resolution, query, bid and
  bid-state; the `service-offer.v1` Corpus extension; node schema sync; schema-gate
  validation including query price-bracket and service-offer topic-subset
  constrainers; deterministic taxonomy digesting; topic resolution; topic-scoped offer
  indexing helpers; schema-valid AD `capability-many` query envelope construction;
  bid-state projection; bid/query price validation; and single-provider settlement
  selection over the embedded `procurement-offer.v1`. The latest Node slice adds Dator
  Corpus offer projection, daemon-owned Corpus round persistence, query/bid
  registration APIs, provider-side bid acceptor runtime, unique provider-scoped bid
  ids, real node-identity Ed25519 signatures on generated local bids, exact-plus-parent
  topic matching, price-bracket rejection without silent offer-price mutation, the
  selected-offer bridge into the P011 procurement path, AD `capability-many` runtime
  fan-out over INAC with taxonomy-digest candidate filtering, opt-in provider-side
  Corpus AD query admission, admitted-bid signature verification bound to
  `bidder/node-id`, P057 notifications for bid readiness/requester-satisfied/settlement failure, operator-visible
  `settlement-failed` recovery state for bridge failures after selection, operator
  visibility under `/admin/corpus/rounds`, and passing Story-011 acceptance coverage
  under full Seed Directory `sovereign-policy` capability lookup backed by a
  refreshed signed federation root. The current slice also
  adds `corpus-reasoning-answer.v1` as a validated, digest-bound final answer artifact
  that can be attached to the requester-owned round read model after provider-local
  `inquirium.generate` drafting; answer admission now uses ordinary Artifact Delivery
  with an in-process `corpus.answer` acceptor, tier-correct answer classification
  propagation, provider signature verification, selected-bid binding, policy-digest
  binding, and append-only federation metadata through `supersedes` plus optional
  `revision/no` while local snapshots remain latest read-models.
  The remaining hard-MVP closure is now covered as well: P069 specifies the
  `orbiplex-canonical-json-jcs-v1` profile for Corpus signatures/idempotency, and the
  Shared Offer Catalog exposes a path-first Corpus topic-index query surface with
  bounded pagination, HATEOAS-style navigation links, invalid-digest refusal, and
  partial-withdrawal supersession tests. P069 is now hard-MVP ready for the procurement
  slice. The post-MVP node-local live layer now connects admitted participants to
  a bounded WSS Room carrier, propagates metadata-only join/readiness/message
  observations to the authority, suppresses exact replay redelivery, and recovers
  stable authority binding plus subject/session sequence across authority and
  recipient restarts through fixed-high-water paged recovery and checkpoint
  validation at append and restore boundaries. The requester-appointed Agent-chair path also has a separate
  local-control transition that signs and publishes only after current quorum,
  room-high-water, chair, evidence, output-digest, and idempotency validation;
  the first profile is text-only and uses the dedicated
  `corpus-reasoning-answer-signature.v1` domain.
  Remaining post-MVP work is federated WSS/TLS or a real Matrix homeserver,
  remote Room-authority trust, arbiter election, multi-provider final answer
  composition, optional Sensorium Interface views, and N-way settlement.
- Room primitive is now tracked explicitly through Proposal 070 and Solution 036. The current code
  implements the durable Room skeleton, deterministic projection over Agora facts,
  signer-backed short-lived membership attestations, explicit POST attestation request
  contracts, no-disclosure request modes, per-exposure TTL caps, rate-limit/dedup,
  metadata-only attestation audit, bounded Room contract validation, golden projection
  vectors, authenticated Agora query surfaces, schema-gate import/export helpers,
  room-scoped live authorization, host-owned Room lifecycle service, bounded WebSocket
  pub/sub live carrier, Matrix live carrier with cleanup redaction, and compatibility
  consolidation for answer-room/association-room projections. The latest hardening
  makes the attestation endpoint skew-tolerant for authorization expiry, rejects
  over-cap TTL instead of silently clamping it, scopes rate-limit buckets by room, and
  records audit facts with `exposure`, `ttl/requested`, and `ttl/granted` while schema
  tests reject raw payload and passport bodies. P070 is now complete for
  its functional standalone Room foundation, including the live plane required by
  Corpus at the primitive layer. CR-88/CR-89 security hardening remains tracked as a
  separate follow-up stream, and remaining product work belongs to consumers such as
  Corpus and richer collaborative answer-room products.
- Sensorium Workbench is now tracked through Proposal 071 and promoted to
  Solution 042 as a post-MVP actuator foundation. The opt-in supervised Python
  connector now has a complete local foundation: allowlisted workspaces,
  bounded file and artifact operations, PTY lifecycle, artifact-backed patching,
  waits/probes/watches, replay/recovery, metadata-only audit, and explicit
  operator controls. Path and command-profile admission crosses the required
  bounded `sensorium-actuation.bridge.{request,response}.v1` companion-process
  boundary into the Rust `sensorium-actuation-core`; unavailable or malformed
  bridge behavior fails closed without a Python validation fallback. The
  daemon-owned Interaction Broker enforces grant-context admission,
  persistence, recovery, retention, provider health,
  Workbench file/terminal adapters, dynamic providers, and native Artifact
  Delivery, approval/consent, and Memarium-query adapters. Verified Workbench
  artifacts can be handed off explicitly to Artifact Delivery resolution and/or
  metadata-only Memarium provenance, with replay bound to the original
  `correlation/id`. Consent supports allow-once, exact argv,
  and bounded workspace-bound argv prefixes through shared append-only sidecar
  merge; node-ui provides consent revoke and broker remediation screens. The
  managed `fixture-copy.v1` Sensorium Virt executor copies a bounded symlink-free
  tree, permits approved writes only in the copy, exports a bounded artifact,
  persists lifecycle, and tears down only its managed root while refusing PTY
  without process isolation. Agent, Corpus, and the current execution-derived
  answer-room tool requests now use a
  schema-backed host lineage wrapper around `sensorium.directive.invoke`, so no
  product receives direct Workbench connector authority. Proposal 071 remains
  outside hard MVP; production container/microVM executors and richer command-
  BDO signal policy are post-MVP hardening rather than current blockers.
  Interaction Broker is implementation-complete for its current provider
  foundation; provider-pushed events and richer deferred-wait retry policy stay
  deferred, so the component is not yet marked post-MVP ready.
- Local Relationship Layer is now hard-MVP complete for the Node-owned slice: Proposal 065 and Solution 032 have contracts, pure core, vault-first daemon storage, sealed rebuildable SQLite projection, local control/host capabilities, operator class/membership/predicate/decision audit UI, package trust queue with approval history, canonical Messaging consumption, dynamic Artifact Delivery group resolution, repeatable Story-010 relationship acceptance runner with a local CI wrapper, projection replay/privacy regression gates, verified `remote-disclosed` node-operator-binding import through the identity control surface, durable revocation invalidation for imported binding evidence, registry-driven pairwise nym context-kind admission, and relationship-class retention profile inheritance. Public federated Local Relationship capability, richer multi-operator UX, hosted CI-provider wiring for the runner, and performance profiling under real relationship cardinalities remain post-MVP work.
- Replay Scheduler M1 is now fully closed for the hard-MVP slice: the generic bounded scheduler, durable launch ledger, host-owned job-source merge, authority gate, cooperative shutdown, Agora projection replay action, and operator status/control surface are all documented as implemented. Richer Agora-domain panels and non-Agora maintenance jobs are post-M1 extensions.
- Agora gained a generic encrypted-artifact Vault surface: `agora-vault-entry.v1` exposes only opaque artifact ids, kind, ciphertext, and cryptographic envelope metadata; supervised local routes are client-auth / daemon-dispatch gated, while remote provider deployments bind the same operations to the frozen `agora-vault@v1` passport profile.
- Temporal Storage Convention is now hard-MVP complete: notification-store is the full-compaction-required adopter, while messaging outbox and Seed Directory accepted facts are converged bounded/no-op adopters with manifests, temporal status/feed/replay-check, and explicit `compaction.policy = "bounded-noop"` diagnostics.
- Bounded Deferred Operations were promoted from Proposal 055 to Solution 029 as a horizontal host control-plane component. The MVP slice is complete: shared wire contracts, host registry, poll/cancel surfaces, JSON-e Flow persisted continuation, Sensorium OS deferred state, operator visibility, and AD consumer integration.
- Sensorium has been promoted to Solution 030 as a constitutional organ. Its MVP slice is implemented for `sensorium-core` observation admission/query, directive invocation, audit-only outcomes, internal connector dispatch, the supervised Sensorium OS reference connector, action-catalog sidecar authorization, and deferred Sensorium actions. Local Agora observation publication remains partial because runtime support currently exposes topic metadata and read surfaces rather than a complete local subscription bus.
- Node Address Attestation Fallback is now counted as hard-MVP ready through the Seed Directory / TLS Trust path: `node-address-attestation.v1` exists, Seed Directory can issue signed endpoint evidence, daemon consumers import usable evidence, peer supervisor enforces endpoint pins, and TLS leaf/SPKI plus advisory route-id checks are wired. Peer-relayed endpoint evidence over INAC remains a post-MVP fallback extension.
- Classification is now counted as hard-MVP ready at proposal and solution level. `classification.v1` and `orbiplex-node-classification` provide the common lattice, egress helper, quarantine/declassification vocabulary, and projection-aware bound-subject handling consumed by Memarium, Agora, Whisper, INAC/private Artifact Delivery, archival export, and adjacent host boundaries. Whole-program IFC, per-field labels, complete historical backfill, and richer quarantine UI remain post-MVP work.
- Proposal 025/Seed Directory capability catalog is now post-MVP complete for its current scope: official-service status rests on `federation-service-endorsement.v1`, root-pack endorsement revocations are applied at startup, the unified `/revocations` feed carries `{artifact_family, artifact}` entries for passport and endorsement revocations, operator/AD endorsement install is scoped and conflict-aware with ingress-enforced `source` plus optional `source/detail`, participant-sovereign operators can issue non-own official-service endorsements through the daemon API, `federation-service-endorsement-revocation.v1` has shared schemas/fixtures, and `capability-proof-presentation-batch.v1` plus `capability-passport-present.v1` can refresh local proof caches through AD with metadata-only presentation facts; outbound batch proof allows must carry explicit `max/bytes` capped at 256 KiB.
- Proposal 054 is hard-MVP complete: `seed-directory-query-attestation.v1` is schema-gated, Seed Directory can attach opt-in signed response attestations, daemon can opt into trusted Agora replay for `adv`, `cap`, and `revocations` lanes, replay follows paginated Agora result pages, replay cursors/status are persisted in the embedded store, projection equivalence tests include revocation effects, and daemon-owned Seed Directory discovery now applies one strict multi-directory policy (`preferred-directory`, `quorum`, or `weighted-trust`) across host queries, AD/capability routing, subject lookup, and Contact Catalog provider discovery, with cross-directory revocation suppression for revoked capability passports. `/v1/seed-directory` and Node UI expose safe trusted-directory diagnostics, local endorsement/reputation policy inputs, replay state, and skip reasons.
- Memarium Proposal 036 and Solution 002 are now implementation-complete for v1: neutral `MemariumObservation` bridges post-chain and phase observers without daemon-private runtime dependencies, observe-rule paths are validated with explicit-null extraction semantics, governed community forget accepts explicit governance references, the read sidecar performs startup catch-up while retaining scan fallback, local backup packages can be submitted through operator remote-archivist handoff/retrieval control surfaces over Artifact Delivery, and Story-005 smoke confirms the classification-bearing private AD/INAC path used by Memarium-adjacent archival/export boundaries. Richer Node UI batch UX remains a product layer, not a Proposal 036 blocker.
- Story 000 is now hard-MVP complete: the minimal two-node operator acceptance pack under `node/tools/acceptance/story-000-operator/` was hardened to keep all non-story middleware disabled by real module id and its `ad-smoke` path passes with two local WSS peer sessions, connected peer read models, running peer supervisors, and metadata-only daemon status.
- Proposal 014 / Node Transport and Discovery is now counted as hard-MVP ready:
  P014, Requirements 006, Solution 000, `node/docs/MVP.md`, and the Node
  implementation ledger were reconciled against the current `protocol`,
  `network`, `peer-runtime`, daemon, and Story 000 acceptance implementation.
  Federated node-id succession publication/replay, richer federation-wide
  peer-governor policy, and additional transports remain post-MVP expansion
  rather than blockers for the transport seed. The local peer-governor slice is
  now seeded through `peer-status.v1`, daemon-configurable quality thresholds,
  and operator-visible peer scorecards. The local NT-018 node-succession
  lifecycle is implemented through `node-succession.v1`, host-derived operator
  import/accept/reject provenance, successor identity activation, and Story 000
  `rotation-smoke`; future successor routing eligibility remains a live local
  policy-registry resolution rather than a mutation of the accepted fact. The
  local client-instance recovery read model is now bounded and replay-idempotent,
  so evicted or unknown detachment references fail closed.
- Key Delegation Passports are now hard-MVP complete at solution level: Seed Directory `/key` publication/query surfaces have focused signed-artifact coverage, daemon operator routes already expose proxy-key and delegation lifecycle management, and remaining multi-hop delegation plus richer Node UI screens are explicitly post-MVP/product-layer work.
- Middleware is now counted as hard-MVP complete: Solution 019 already covers the implemented host-owned lifecycle, readiness, dispatch, claimed-route, host capability, observer/audit, raw-signal, and schema-presentation surfaces, while additional executor classes or product-specific module UX are future extension points owned by their specific proposals.
- Capability Binding is now counted as hard-MVP complete: the reference runtime uses the shared `capability-binding` organ through daemon dispatch and Sealer integration, while solution-level service adapters and caches remain optional seams for alternate embeddings or profiled hot paths rather than MVP blockers.
- Agora/P035 is now counted as hard-MVP complete: the reference runtime covers the public record relay, content addressing, signing/ingest, query/readback, SSE subscription, Matrix-backed federation, retention, subject indexing, Agora Vault, and Story-008 resource-opinion path. Remaining ingest-policy tightening and hot-path/status-product work stay post-MVP and are listed in Proposal 035's hardening queue.

## Stories

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Story 000: Two Nodes See Each Other](../30-stories/story-000-two-nodes-see-each-other.md) | `true` | `true` | `false` | `100` |
| [Story 001: Swarm Node Onboarding and Federated Answer Procurement](../30-stories/story-001-swarm-node-onboarding.md) | `false` | `false` | `false` | `65` |
| [Story 002: Federated Peer Learning and Consensus Correction](../30-stories/story-002-federated-peer-learning.md) | `true` | `true` | `false` | `90` |
| [Story 003: Remote Memory Preservation, Archivists, and Vault Publication](../30-stories/story-003-remote-memory-preservation.md) | `false` | `false` | `false` | `38` |
| [Story 004: Pod-Client Onboarding and Delegated Federated Answer Procurement](../30-stories/story-004-pod-client-onboarding.md) | `false` | `false` | `false` | `65` |
| [Story 005: Whisper Rumor Intake, Redaction, and Thresholded Association Bootstrap](../30-stories/story-005-whisper-rumor-intake.md) | `true` | `true` | `false` | `100` |
| [Story 006 Buyer Node Components for Arca](../30-stories/story-006-buyer-node-components.md) | `true` | `true` | `false` | `90` |
| [Story 006: Voluntary Swarm Service Exchange for Cooperative Content Production](../30-stories/story-006-voluntary-swarm-exchange.md) | `true` | `true` | `false` | `90` |
| [Story 007: Settlement-Capable Node as the Authoritative ORC Ledger](../30-stories/story-007-settlement-capable-node.md) | `false` | `false` | `false` | `82` |
| [Story 008: Leaving an Opinion on a Website via the Local Node](../30-stories/story-008-cool-site-comment.md) | `true` | `true` | `false` | `100` |
| [Story 009: The magazine publishes itself — a three-node blogging pipeline about Bielik, conducted by Arca](../30-stories/story-009-bielik-blog-arca.md) | `false` | `false` | `false` | `90` |
| [Story 010: Message to a Friend](../30-stories/story-010-message-to-a-friend.md) | `true` | `true` | `false` | `100` |
| [Story 011: Corpus answers the fish-water question](../30-stories/story-011-corpus-fish.md) | `true` | `true` | `false` | `100` |

## Proposals

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Licensing Baseline for Orbiplex Swarm Components](../40-proposals/001-licensing-proposal.md) | `false` | `false` | `false` | `25` |
| [Communication Protocol Baseline for Orbiplex Swarm](../40-proposals/002-comm-protocol.md) | `true` | `true` | `false` | `90` |
| [Question Envelope and Answer-Channel Transport for Orbiplex Swarm](../40-proposals/003-question-envelope-and-answer-channel.md) | `true` | `true` | `false` | `82` |
| [Human-Origin Flags and Operator Participation in Answer Channels](../40-proposals/004-human-origin-flags-and-operator-participation.md) | `false` | `false` | `false` | `65` |
| [Operator Participation Room Policy Profiles](../40-proposals/005-operator-participation-room-policy-profiles.md) | `false` | `false` | `false` | `25` |
| [Pod-Backed Access Layer for Thin Clients](../40-proposals/006-pod-access-layer-for-thin-clients.md) | `false` | `false` | `false` | `55` |
| [Pod Identity and Tenancy Model](../40-proposals/007-pod-identity-and-tenancy-model.md) | `false` | `false` | `false` | `25` |
| [Transcription Monitors, Archivists, and Public Vaults](../40-proposals/008-transcription-monitors-and-public-vaults.md) | `false` | `false` | `false` | `20` |
| [Communication Exposure Modes for Swarm Requests](../40-proposals/009-communication-exposure-modes.md) | `false` | `false` | `false` | `25` |
| [Operator Proxy and Co-Regulation Channels](../40-proposals/010-operator-proxy-co-regulation.md) | `false` | `false` | `false` | `25` |
| [Federated Answer Procurement Lifecycle Artifacts](../40-proposals/011-federated-answer-procurement-lifecycle.md) | `true` | `true` | `false` | `90` |
| [Learning Outcomes, Knowledge Artifacts, and Archival Contracts](../40-proposals/012-learning-outcomes-and-archival-contracts.md) | `false` | `false` | `false` | `38` |
| [Whisper Social-Signal Exchange and Threshold Bootstrap](../40-proposals/013-whisper-social-signal-exchange.md) | `true` | `true` | `false` | `95` |
| [Node Transport and Discovery MVP](../40-proposals/014-node-transport-and-discovery-mvp.md) | `true` | `true` | `false` | `96` |
| [Nym Certificates and Renewal Baseline](../40-proposals/015-nym-certificates-and-renewal-baseline.md) | `false` | `false` | `false` | `25` |
| [Supervised Prepaid Gateway and Escrow MVP](../40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md) | `true` | `false` | `false` | `65` |
| [Proposal 017: Organization Subjects and org:did:key](../40-proposals/017-organization-subjects-and-org-did-key.md) | `true` | `true` | `false` | `88` |
| [Proposal 018: Layered capability_limited Participant Restrictions](../40-proposals/018-layered-capability-limited-participant-restrictions.md) | `true` | `true` | `false` | `100` |
| [Proposal 019: Supervised http_local_json Middleware Executor](../40-proposals/019-supervised-local-http-json-middleware-executor.md) | `true` | `true` | `false` | `100` |
| [Proposal 020: Bundled Python Middleware Modules for Hard MVP](../40-proposals/020-bundled-python-middleware-modules.md) | `true` | `true` | `false` | `100` |
| [Proposal 021: Service Offers, Service Orders, and the Host-Owned Procurement Bridge](../40-proposals/021-service-offers-orders-and-procurement-bridge.md) | `true` | `true` | `false` | `88` |
| [Proposal 022: Monus as Host-Granted Local Observation Middleware](../40-proposals/022-monus-as-host-granted-local-observation-middleware.md) | `false` | `false` | `false` | `15` |
| [Proposal 023: Federated Offer Distribution and Catalog Listener](../40-proposals/023-federated-offer-distribution-and-catalog-listener.md) | `true` | `true` | `false` | `100` |
| [Proposal 024: Capability Passports and Network Ledger Delegation](../40-proposals/024-capability-passports-and-network-ledger-delegation.md) | `true` | `true` | `false` | `85` |
| [Proposal 025: Seed Directory as Capability Catalog](../40-proposals/025-seed-directory-as-capability-catalog.md) | `true` | `true` | `true` | `100` |
| [Proposal 026: Resource Opinions and Discussion Surfaces](../40-proposals/026-resource-opinions-and-discussion-surfaces.md) | `false` | `false` | `false` | `100` |
| [Proposal 027: Middleware Peer-Message Dispatch](../40-proposals/027-middleware-peer-message-dispatch.md) | `true` | `true` | `true` | `100` |
| [Proposal 028: Service Schema Catalog](../40-proposals/028-service-schema-catalog.md) | `false` | `false` | `false` | `25` |
| [Proposal 029: Workflow Template Catalog](../40-proposals/029-workflow-template-catalog.md) | `false` | `false` | `false` | `40` |
| [Proposal 030: Identity Recovery Service](../40-proposals/030-identity-recovery-service.md) | `false` | `false` | `false` | `55` |
| [Proposal 031: Participant Key Passphrase Lock](../40-proposals/031-participant-key-passphrase-lock.md) | `true` | `true` | `false` | `100` |
| [Proposal 032: Key Delegation Passports](../40-proposals/032-key-delegation-passports.md) | `true` | `true` | `false` | `100` |
| [Proposal 033: Workflow Fan-Out and Temporal Orchestration](../40-proposals/033-workflow-fan-out-and-temporal-orchestration.md) | `true` | `true` | `false` | `77` |
| [Proposal 034: Node Operator Binding and Derived Node Assurance](../40-proposals/034-node-operator-binding-and-derived-node-assurance.md) | `true` | `true` | `false` | `90` |
| [Proposal 035: Agora — Topic-Addressed Record Relay and Shared Record Substrate](../40-proposals/035-agora-topic-addressed-record-relay.md) | `true` | `true` | `false` | `100` |
| [Proposal 036: Memarium — Local Memory Organ for the Orbiplex Node](../40-proposals/036-memarium.md) | `true` | `true` | `true` | `100` |
| [Proposal 037: Generic Signing Service](../40-proposals/037-generic-signing-service.md) | `true` | `true` | `false` | `100` |
| [Proposal 038: Key Roles and Key Use Taxonomy](../40-proposals/038-key-roles-and-key-use-taxonomy.md) | `true` | `true` | `false` | `100` |
| [Proposal 039 Crisis Seed v1 Review Record](../40-proposals/039-crisis-space-seed-v1-review.md) | `false` | `false` | `false` | `25` |
| [Proposal 039: Crisis Space Seed v1](../40-proposals/039-crisis-space-seed-v1.md) | `false` | `false` | `false` | `100` |
| [Proposal 040: Custodial Redelivery and Tombstones for Agora Records](../40-proposals/040-custodial-redelivery-and-tombstones.md) | `false` | `false` | `false` | `38` |
| [Proposal 041: Agora Ingest Attestation and Tiered Access](../40-proposals/041-agora-ingest-attestation.md) | `false` | `false` | `false` | `65` |
| [Proposal 042: Inter-Node Artifact Channel (F2F Memarium Exchange)](../40-proposals/042-inter-node-artifact-channel.md) | `true` | `true` | `false` | `88` |
| [Proposal 043: Node Address Attestation Fallback](../40-proposals/043-node-address-attestation-fallback.md) | `true` | `true` | `false` | `86` |
| [Proposal 044: Host-Owned Generic Module Store](../40-proposals/044-host-owned-generic-module-store.md) | `true` | `true` | `false` | `100` |
| [Proposal 045: Sensorium as a Local Enaction Stratum](../40-proposals/045-sensorium-local-enaction-stratum.md) | `true` | `true` | `false` | `92` |
| [Proposal 046: Agora Topic-Key Namespace Conventions](../40-proposals/046-agora-topic-key-namespace-conventions.md) | `false` | `false` | `false` | `100` |
| [Proposal 047: Classification Label Propagation for Memarium-Touching Data](../40-proposals/047-classification-label-propagation.md) | `true` | `true` | `false` | `88` |
| [Proposal 048: Sensorium OS Connector Action Classes](../40-proposals/048-sensorium-os-connector-action-classes.md) | `true` | `true` | `false` | `100` |
| [Proposal 049: JSON-e Middleware Transformer Executor](../40-proposals/049-json-e-middleware-transformer-executor.md) | `true` | `true` | `false` | `82` |
| [Proposal 050: Local Readiness Gate](../40-proposals/050-local-readiness-gate.md) | `true` | `true` | `false` | `85` |
| [Proposal 051: Swarm Membership, Reputation Bootstrap, and Public Adjudication](../40-proposals/051-swarm-membership-and-reputation-bootstrap.md) | `false` | `false` | `false` | `25` |
| [Proposal 052: Tauri-Hosted Node UI](../40-proposals/052-tauri-hosted-node-ui.md) | `false` | `false` | `false` | `82` |
| [Proposal 053: Raw Signal Access for Middleware Flows](../40-proposals/053-raw-signal-access.md) | `true` | `true` | `false` | `100` |
| [Proposal 054: User-Maintained Federated Seed Directory](../40-proposals/054-user-maintained-federated-seed-directory.md) | `true` | `true` | `false` | `100` |
| [Proposal 055: Bounded Deferred Operation Contract](../40-proposals/055-bounded-deferred-operation-contract.md) | `true` | `true` | `false` | `100` |
| [Proposal 056: Orbiplex TLS Trust Policy](../40-proposals/056-orbiplex-tls-trust-policy.md) | `true` | `true` | `false` | `86` |
| [Proposal 057: User and Operator Notifications](../40-proposals/057-user-and-operator-notifications.md) | `true` | `true` | `false` | `90` |
| [Proposal 058: Contact Catalog and Private Contact Discovery](../40-proposals/058-contact-catalog.md) | `true` | `true` | `false` | `100` |
| [Proposal 059: Participant, Nym, and Routing-Subject Key-Role Derivation](../40-proposals/059-participant-and-nym-key-role-derivation.md) | `false` | `true` | `false` | `90` |
| [Proposal 060: Messaging Middleware and Personal Message Delivery](../40-proposals/060-messaging-middleware.md) | `true` | `true` | `false` | `100` |
| [Proposal 061: Contact Attestation Service](../40-proposals/061-contact-attestation-service.md) | `true` | `true` | `false` | `78` |
| [Proposal 062: Temporal Storage Convention](../40-proposals/062-temporal-storage-convention.md) | `false` | `true` | `false` | `100` |
| [Proposal 063: Inquirium as a Model Inquiry Organ](../40-proposals/063-inquirium-model-inquiry-organ.md) | `false` | `true` | `false` | `100` |
| [Proposal 064: Inquirium Implementation Recommendations](../40-proposals/064-inquirium-implementation-recommendations.md) | `false` | `true` | `false` | `100` |
| [Proposal 065: Local Relationship Layer](../40-proposals/065-local-relationship-layer.md) | `true` | `true` | `false` | `100` |
| [Proposal 066: Inquirium Assistant Channel](../40-proposals/066-inquirium-assistant-channel.md) | `false` | `true` | `false` | `100` |
| [Proposal 067: Shared Offer Catalog over Agora](../40-proposals/067-shared-offer-catalog-over-agora.md) | `true` | `true` | `false` | `100` |
| [Proposal 069: Corpus — Topic-Routed Collaborative Reasoning](../40-proposals/069-corpus.md) | `true` | `true` | `false` | `100` |
| [Proposal 070: Room — Generic Subject-Addressed Room Primitive](../40-proposals/070-room-primitive.md) | `true` | `true` | `true` | `100` |
| [Proposal 071: Sensorium Workbench](../40-proposals/071-sensorium-workbench.md) | `false` | `false` | `false` | `98` |
| [Proposal 072: Capability Registry — Enforced Core and Policy Sidecar](../40-proposals/072-capability-registry.md) | `true` | `true` | `false` | `100` |
| [Proposal 073: Agent — Bounded Stateful Orchestration Organ](../40-proposals/073-agent-orchestration-organ.md) | `false` | `false` | `false` | `100` |
| [Proposal 076: Federation Identity and Network Selector](../40-proposals/076-federation-identity-and-network-selector.md) | `true` | `true` | `false` | `92` |
| [Proposal 077: Swarm Broadcast Assistance](../40-proposals/077-swarm-broadcast-assistance.md) | `false` | `false` | `false` | `15` |
| [Proposal 078: Weak Signal Harvester](../40-proposals/078-weak-signal-harvester.md) | `false` | `true` | `false` | `68` |
| [Proposal 079: Cross-Federation Alliance](../40-proposals/079-cross-federation-alliance.md) | `false` | `false` | `false` | `45` |
| [Proposal 080: Multiplexed Middleware Channel Executor](../40-proposals/080-multiplexed-middleware-channel-executor.md) | `false` | `true` | `true` | `100` |
| [Proposal 081: Horizontal Protocol Primitives for Causality, Federated Synchronization, and Scoped Nym Claims](../40-proposals/081-horizontal-protocol-primitives.md) | `true` | `true` | `false` | `100` |
| [Proposal 082: Sensorium Interfaces](../40-proposals/082-sensorium-interfaces.md) | `false` | `true` | `false` | `100` |

## Solutions

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Orbiplex Node](../60-solutions/000-node/000-node.md) | `true` | `true` | `false` | `85` |
| [Orbiplex Node UI](../60-solutions/001-node-ui/001-node-ui.md) | `true` | `false` | `false` | `88` |
| [Orbiplex Memarium](../60-solutions/002-memarium/002-memarium.md) | `true` | `true` | `true` | `100` |
| [Orbiplex Arca](../60-solutions/003-arca/003-arca.md) | `true` | `true` | `false` | `88` |
| [Orbiplex Dator](../60-solutions/004-dator/004-dator.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Sealer](../60-solutions/005-sealer/005-sealer.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Capability Binding](../60-solutions/006-capability-binding/006-capability-binding.md) | `true` | `true` | `true` | `100` |
| [Capability Advertisement](../60-solutions/007-capability-advertisement/007-capability-advertisement.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Agora](../60-solutions/008-agora/008-agora.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Monus](../60-solutions/009-monus/009-monus.md) | `false` | `false` | `false` | `15` |
| [Orbiplex Anon](../60-solutions/010-anon/010-anon.md) | `false` | `false` | `false` | `10` |
| [Orbiplex Whisper](../60-solutions/011-whisper/011-whisper.md) | `true` | `true` | `false` | `100` |
| [Ferment](../60-solutions/012-ferment/012-ferment.md) | `false` | `false` | `false` | `15` |
| [Raw Signal Access](../60-solutions/013-raw-signal-access/013-raw-signal-access.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Key Delegation Passports](../60-solutions/014-key-delegation-passports/014-key-delegation-passports.md) | `true` | `true` | `false` | `100` |
| [Host-Owned Module Store](../60-solutions/015-host-owned-module-store/015-host-owned-module-store.md) | `true` | `true` | `false` | `100` |
| [Bounded Local Server Runtime](../60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md) | `true` | `true` | `false` | `100` |
| [Inter-Node Artifact Channel (INAC)](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md) | `true` | `true` | `false` | `88` |
| [Classification](../60-solutions/018-classification/018-classification.md) | `true` | `true` | `false` | `88` |
| [Middleware](../60-solutions/019-middleware/019-middleware.md) | `true` | `true` | `false` | `100` |
| [Replay Scheduler](../60-solutions/020-scheduler/020-scheduler.md) | `true` | `true` | `false` | `100` |
| [Agora Authority](../60-solutions/021-agora-authority/021-agora-authority.md) | `false` | `false` | `false` | `77` |
| [Orbiplex Semantic Index](../60-solutions/022-semantic-index/022-semantic-index.md) | `false` | `false` | `false` | `15` |
| [Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md) | `true` | `true` | `false` | `100` |
| [TLS Trust Policy](../60-solutions/024-tls-trust-policy/024-tls-trust-policy.md) | `true` | `true` | `false` | `86` |
| [Contact Catalog](../60-solutions/025-contact-catalog/025-contact-catalog.md) | `true` | `true` | `false` | `100` |
| [Pseudonym Vault and Key Roles](../60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md) | `true` | `true` | `false` | `100` |
| [Messaging Middleware](../60-solutions/027-messaging-middleware/027-messaging-middleware.md) | `true` | `true` | `false` | `100` |
| [Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md) | `false` | `true` | `false` | `100` |
| [Bounded Deferred Operations](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md) | `true` | `true` | `false` | `100` |
| [Sensorium](../60-solutions/030-sensorium/030-sensorium.md) | `true` | `true` | `false` | `92` |
| [Seed Directory](../60-solutions/031-seed-directory/031-seed-directory.md) | `true` | `true` | `false` | `100` |
| [Local Relationship Layer](../60-solutions/032-local-relationship-layer/032-local-relationship-layer.md) | `true` | `true` | `false` | `100` |
| [Shared Offer Catalog](../60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md) | `true` | `true` | `false` | `100` |
| [API Surface Projection](../60-solutions/034-api-surface-projection/034-api-surface-projection.md) | `false` | `true` | `true` | `100` |
| [Interaction Broker](../60-solutions/035-interaction-broker/035-interaction-broker.md) | `false` | `true` | `false` | `100` |
| [Room](../60-solutions/036-room/036-room.md) | `true` | `true` | `true` | `100` |
| [Capability Registry](../60-solutions/037-capability-registry/037-capability-registry.md) | `true` | `true` | `false` | `100` |
| [Corpus](../60-solutions/038-corpus/038-corpus.md) | `true` | `true` | `false` | `100` |
| [Notifications](../60-solutions/039-notifications/039-notifications.md) | `true` | `true` | `false` | `90` |
| [Capability-Limited Restrictions](../60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md) | `true` | `true` | `false` | `100` |
| [Federation Root and Network Selector](../60-solutions/041-federation-root/041-federation-root.md) | `true` | `true` | `false` | `92` |
| [Sensorium Workbench](../60-solutions/042-sensorium-workbench/042-sensorium-workbench.md) | `false` | `false` | `false` | `98` |
| [Horizontal Protocol Primitives](../60-solutions/043-horizontal-protocol-primitives/043-horizontal-protocol-primitives.md) | `true` | `true` | `false` | `100` |
| [Inquirium](../60-solutions/044-inquirium/044-inquirium.md) | `false` | `true` | `false` | `100` |
| [Inquirium Assistant Channel](../60-solutions/045-inquirium-assistant-channel/045-inquirium-assistant-channel.md) | `false` | `true` | `false` | `100` |
| [Sensorium Interfaces](../60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md) | `false` | `true` | `false` | `100` |
