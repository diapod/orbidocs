# Proposal 084: Sensorium Web Observation Connector

Based on:

- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/078-weak-signal-harvester.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`

## Status

Draft

## Date

2026-07-29

## Executive Summary

Orbiplex should add **Sensorium Web Observation Connector** as an opt-in,
supervised Sensorium connector for acquiring bounded, provenance-bearing
observations from web resources.

The connector is not a browser exposed to an Agent, a general-purpose crawler,
or a remote proxy. It accepts host-admitted fetch plans, extracts inert document
representations, and submits those representations through the existing Sensorium
observation lane. An operator may then publish an admitted snapshot through a
Sensorium Interface without giving the consumer access to connector credentials,
network sockets, browser state, or the source site's authority boundary.

The first implementation is deliberately stratified:

```text
caller or scheduled source refresh
  -> sensorium.directive.invoke
  -> Sensorium Core action resolution and grant checks
  -> supervised sensorium-web connector
  -> private Rust host egress broker
       URL and policy validation
       DNS and destination admission
       bounded HTTP(S) fetch
  -> Python extraction mechanics
  -> Sensorium observation admission
  -> optional P082 Sensorium Interface publication
```

Rust owns the trusted fetch boundary, URL and destination policy, resource
budgets, contract validation, audit, and host authority. Python owns replaceable
HTML extraction and later Playwright-based browser mechanics. The Python process
has no ambient network access in the reference profile.

V1 supports static HTTP(S) document snapshots only. JavaScript rendering and
multi-page crawling are separate, deferred profiles because they introduce
materially different process, storage, queue, and security envelopes.

## Context and Problem Statement

Sensorium already mediates local contact with external reality. Its documented
examples include public-network readers, repositories, mailing lists, news feeds,
and other externally observed sources. Sensorium Interfaces already provide the
resource, grant, classification, cursor, carrier, and revocation contracts needed
to share an admitted observation locally or with an authorized remote consumer.

What is missing is one reusable connector that turns a web resource into a
bounded, inspectable observation without allowing every Agent, flow, or domain
component to implement its own HTTP client.

Without this connector, web acquisition tends to leak into higher layers:

- an Agent receives ambient Internet access instead of proposing an observation
  need;
- each domain module implements URL parsing, redirects, DNS checks, timeouts,
  decompression limits, and retention differently;
- model prompts receive raw hostile HTML without a stable provenance boundary;
- remote consumers may be given connector or credential access instead of a
  deliberately published representation;
- crawling queues and browser processes appear as incidental implementation
  details with no explicit lifecycle or operator inspection.

The web is not merely another file source. A fetch has observable effects and a
distinct threat model: it discloses the node's network position and timing to the
remote server, may follow attacker-controlled redirects, may resolve into local
or metadata networks, and returns attacker-controlled bytes that can target HTML
parsers, browsers, operator consoles, and model prompts.

The connector must therefore be useful enough to become the common path, while
remaining narrower than a general web automation platform.

## Goals

- Provide one supervised Sensorium connector for bounded web document
  acquisition and extraction.
- Keep network authority in a host-owned Rust boundary rather than in Python,
  Agent, Inquirium, or consumer code.
- Support operator-configured durable sources and explicitly granted ad hoc
  fetches without conflating the two authority models.
- Produce immutable, digest-bound observations with fetch and extraction
  provenance.
- Reuse Sensorium Core for action resolution and observation admission, P081 for
  causal context and receipts, P082 for publication, and Artifact Delivery for
  large bodies and extracted representations.
- Make redirects, DNS resolution, destination networks, response bytes,
  decompression, duration, concurrency, and retention explicitly bounded.
- Preserve a path to JavaScript rendering and crawling without weakening the V1
  static-fetch contract.

## Non-Goals

- A generic HTTP proxy for Agents, middleware modules, or remote peers.
- Direct consumer access to URLs, sockets, cookies, browser profiles, or
  connector credentials.
- Browser interaction, form submission, login, purchase, posting, uploading, or
  other remote actuation in V1.
- A search engine, global index, or unbounded web crawler.
- Automatic truth attribution to fetched content. A successful fetch proves what
  bytes were observed, not that the page is accurate.
- Automatic execution or semantic trust of scripts, markup, links, embedded
  instructions, or extracted text.
- A replacement for Weak Signal Harvester. P078 owns finding discovery,
  grouping, review, and Whisper handoff; this proposal owns web acquisition.
- Automatic persistence in Memarium or publication to Agora, Room, or Whisper.
- Bypassing source terms, robots policy, authentication, paywalls, or legal and
  organizational collection policy.

## Terminology

| Term | Meaning |
|---|---|
| Web source | One operator-configured resource identity with a URL, fetch policy, extraction profile, classification posture, and current source generation. |
| Fetch plan | A closed, host-validated request describing one bounded HTTP(S) acquisition. It is inert data, not a socket handle. |
| Fetch result | A private connector result containing response metadata and bounded body bytes or an Artifact Delivery reference. |
| Document snapshot | An admitted Sensorium observation derived from one fetch result under one extraction profile. |
| Extraction profile | A pinned declaration of parser/extractor identity, version, output shape, and content-selection options. |
| Browser profile | A future isolated rendering profile that executes a browser under a separate process and egress envelope. |
| Crawl frontier | A future bounded queue of discovered URLs. It is not part of V1 static snapshot acquisition. |

## Proposed Model

### 1. Component boundary

The implementation introduces one separate middleware connector with a stable
module identity such as `sensorium-web`. It advertises connector actions through
the existing middleware report and is invoked only through Sensorium Core's
internal connector dispatch.

Ordinary callers use public Sensorium capabilities and stable action ids. They do
not call connector-local HTTP endpoints or the host egress broker directly.

The connector exposes two logical V1 actions:

- `web.source.refresh`: refresh one operator-configured durable web source by
  opaque `source/ref`;
- `web.document.fetch`: perform one ad hoc fetch under an explicit grant whose
  scope contains the admitted URL/domain and budgets.

Concrete action ids remain operator-authored catalog entries. The names above are
contract roles, not globally mandatory deployment ids.

Observation authority and acquisition authority remain separate:

- permission to read or subscribe to a P082 interface does not permit a new web
  fetch;
- permission to invoke a web fetch does not permit publication to another
  consumer;
- carrier access never grants either authority.

### 2. Trusted and replaceable strata

The reference implementation has three layers.

#### `sensorium-web-core` in Rust

A small pure crate should own:

- closed fetch-plan and fetch-result types;
- URL canonicalization rules;
- scheme, port, method, redirect, byte, time, and media-type constraints;
- destination-network classes and matching;
- source-generation and extraction-profile binding;
- typed failure classification;
- canonical digest inputs;
- invariants shared by the host broker, schema gate, and tests.

It has no HTTP client, daemon, browser, Python, database, or async-runtime
dependency unless an async trait is required by a later implementation layer.

#### Daemon-owned web egress broker in Rust

The host broker owns actual network authority:

- admission of the exact connector caller and action;
- resolution of A and AAAA records;
- rejection of prohibited destination classes;
- connection establishment and TLS policy;
- redirect-by-redirect revalidation;
- response streaming with compressed and decompressed byte caps;
- total and phase-specific deadlines;
- bounded concurrency and per-origin rate accounting;
- metadata-only audit and operator status.

The broker returns bounded bytes over the private middleware channel or writes a
large body into Artifact Delivery and returns an immutable pointer. It never
returns a reusable socket, DNS resolver, cookie jar, or credential handle.

#### Python `sensorium-web` connector

Python owns replaceable mechanics:

- invoking the private host fetch capability;
- decoding admitted text encodings under bounded rules;
- HTML parsing and main-content extraction;
- metadata and link extraction;
- conversion to the canonical observation shape;
- connector-local source scheduling state and conditional-request hints;
- later Playwright orchestration for the separate browser profile.

The reference connector runs without ambient network access. Missing host fetch
authority is a hard refusal, not a fallback to Python HTTP libraries or a
subprocess such as `curl`.

### 3. Static fetch profile

The initial profile is `sensorium-web-static.v1`:

- methods: `GET` and bounded conditional `HEAD` only;
- schemes: HTTPS by default; HTTP requires an explicit source or grant posture;
- no URL user-info;
- no `file:`, `data:`, `blob:`, `javascript:`, custom, or opaque schemes;
- no request body;
- no cookies, client certificates, ambient credentials, browser state, system
  proxy, or inherited authorization headers;
- bounded redirects, with policy re-evaluation before every hop;
- bounded compressed and decompressed response bytes;
- bounded connect, TLS, first-byte, read-idle, and total duration;
- bounded response headers and header count;
- initial accepted media types limited to `text/html`,
  `application/xhtml+xml`, and `text/plain`;
- no script execution or subresource loading;
- optional conditional requests using connector-owned `ETag` and
  `Last-Modified` state.

Content encoding, MIME sniffing, and character decoding are separate steps. A
declared media type does not authorize an unbounded parser, and a parser failure
does not erase the successfully observed response metadata.

### 3.1. Deliberate reuse and non-reuse

The implementation reuses the standard middleware supervisor and channel,
Sensorium directive and observation lanes, host capability admission, Replay
Scheduler, Bounded Deferred Operations, Artifact Delivery, P081 causal context,
and the P082 source-provider registry.

The web connector may also reuse lower-level URL, IP-classification, TLS, byte
stream, digest, and bounded HTTP primitives when those primitives have no
Sensorium Web semantics.

It deliberately does not model web acquisition as:

- a Sensorium OS `egress-network-spawn` action: P048's generic network class
  admits bounded socket/process effects, while this proposal requires
  redirect-by-redirect destination admission, response provenance, extraction
  profiles, source generations, conditional refresh, and document observation
  semantics;
- a Workbench command: Workbench owns environments, terminals, files, patches,
  and explicit tool effects, not the canonical public-web observation boundary;
- an Inquirium adapter: model inquiry may consume the admitted snapshot but does
  not own acquisition, egress, or source truth;
- a P082 carrier: Sensorium Interfaces publish an already admitted
  representation and never contact the source site on a consumer's behalf.

This non-reuse does not justify a second generic HTTP stack. The Rust host broker
should expose the narrowest reusable bounded-fetch primitive whose authority can
be shared safely with future connectors, while all document and extraction
semantics remain in `sensorium-web`.

### 4. URL and destination admission

URL validation is structural and destination admission is network-aware.

For every initial URL and redirect target, the host must:

1. parse and canonicalize the URL with one implementation;
2. reject credentials, remove fragments from fetch identity, and reject
   unsupported schemes and ports, oversized components, and malformed IDNA;
3. match the canonical host and port against the effective grant and host
   policy;
4. resolve all applicable A and AAAA records under a deadline;
5. classify every result as public, loopback, private, link-local, multicast,
   documentation, reserved, carrier-grade NAT, or deployment-defined internal;
6. reject the request if any candidate address is outside the admitted class;
7. bind the connection to one admitted resolved address without performing an
   unvalidated second resolution;
8. repeat the process for every redirect.

Cloud metadata endpoints, local daemon ports, Unix sockets, peer control planes,
and host capability endpoints are denied by construction. A future internal-web
profile requires a separate capability and policy; it must not be obtained by
loosening the public-web classifier.

### 5. Contract family

The first implementation should define closed schemas for:

| Schema | Purpose |
|---|---|
| `sensorium-web-source.v1` | Operator-owned durable source configuration and current generation. |
| `sensorium-web-fetch-request.v1` | Private connector-to-host bounded fetch plan. |
| `sensorium-web-fetch-result.v1` | Private response metadata plus bounded inline bytes or one artifact pointer. |
| `sensorium-web-document-snapshot.v1` | Canonical admitted document observation. |
| `sensorium-web-error-codes.v1` | Closed typed failure vocabulary and retry class. |
| `sensorium-web-operator-snapshot.v1` | Bounded aggregate readiness, occupancy, refusal, and retention evidence. |

The document snapshot should carry at least:

- `source/ref` and `source/generation-ref`;
- redacted requested and final display URLs plus digests of the exact private
  canonical URLs;
- `fetched/at` and response status;
- media type, declared charset, selected charset, byte count, and body digest;
- body artifact ref when raw retention is enabled;
- extraction profile ref, version, and digest;
- extracted representation digest and optional artifact ref;
- bounded title, byline, publication-time claim, language claim, and link refs;
- `sensorium-operational-context.v1` and `classification.v1`;
- P081 causal context joining the directive, host fetch, extraction, observation
  admission, and optional interface publication.

Remote headers are untrusted input. Only an explicit bounded allowlist may enter
the observation. Authorization, cookies, `Set-Cookie`, proxy metadata, local
socket details, and full request headers never enter consumer-visible output.
Exact query strings and redirect locations are host-private by default. A source
may expose only explicitly allowlisted query fields whose values have been
classified as non-secret; every other query value is removed from the display
URL while the exact private URL remains bound by digest.

### 6. Source identity, generations, and refresh

A durable source is identified independently from its current URL bytes. Its
generation changes when any authority- or interpretation-relevant declaration
changes, including:

- canonical URL or admitted origin;
- redirect posture;
- authentication posture;
- extraction profile or parser version policy;
- media-type policy;
- classification or operational context;
- fetch budgets that may change observable coverage.

The exact canonical fetch URL is retained only in restricted connector/host
configuration. Audit, diagnostics, and consumer-visible observations use the
redacted display form and exact URL digest, so a signed URL or query token cannot
become durable evidence by accident.

A new page version under an unchanged source declaration advances the source
position or snapshot digest; it does not create a new source generation.

`ETag` and `Last-Modified` are optimization hints, not truth or authorization.
A `304 Not Modified` may preserve the previous admitted representation only when
the current source generation, policy, retained body digest, and extraction
profile still match.

### 7. Extraction and hostile content

Extraction transforms bytes into a representation; it does not validate claims
made by the page.

The connector must:

- parse within byte, node-count, depth, and time limits;
- sanitize control characters before operator presentation;
- keep scripts, event handlers, styles, hidden nodes, and active content inert;
- represent links as data without following them in V1;
- mark title, author, date, language, and canonical-link values as page claims;
- record extractor identity and configuration in the output digest;
- treat empty or low-confidence extraction as a typed outcome rather than
  silently substituting arbitrary HTML text;
- label every extracted representation as untrusted external content for Agent
  and Inquirium consumers.

Prompt injection is a content-integrity problem, not only an LLM prompt problem.
Higher layers must receive source attribution and the external-content caution
layer before inference. Page text cannot produce grants, tool calls, wiring,
policy, or executable plans by interpolation.

### 8. Artifact and retention model

Raw body retention is opt-in per source or grant. The default durable record is
metadata-first:

- response and extraction digests;
- bounded selected metadata;
- immutable artifact refs when retention is enabled;
- no cookies, credentials, authorization headers, browser storage, or local
  connection details.

Large bodies and extracted representations use Artifact Delivery rather than
inline Sensorium envelopes. Inline values remain under schema-specific byte
caps. Artifact acceptance does not imply interface publication or Memarium
retention.

Cache entries require an owner, key, byte cap, entry cap, TTL or retention rule,
and restart behavior. Cache eviction may force a full refetch but must not turn a
stale retained representation into a fresh observation.

### 9. Sensorium Interface projection

The connector-specific source-provider adapter registers through P082's open,
bounded source-adapter registry. It exposes an already admitted document
snapshot, never a live connector or URL handle.

The first projection uses `latest-state` semantics:

- each changed representation advances the opaque cursor;
- unchanged refresh yields `no-change`;
- source-generation replacement fences old publications;
- interface read and subscribe authority are checked independently from source
  fetch authority;
- local SSE, direct peer, and Room remain thin P082 carriers;
- carrier selection never triggers a refresh unless a separately authorized
  host workflow explicitly does so.

An ordered history of page changes is deferred until retention, capture, and
deletion semantics are evidenced. V1 does not imply an archival crawler.

### 10. Scheduling and deferred work

One ad hoc fetch may complete synchronously only within the middleware request
budget. Refreshes that can outlive one request use Bounded Deferred Operations.
Periodic durable-source refresh uses Replay Scheduler rather than a private sleep
loop.

Schedules are host-owned and bounded by:

- minimum interval and jitter;
- per-source and per-origin concurrency;
- backoff and terminal/retryable error classes;
- maximum launches per period;
- operator pause, resume, run-now, and inspection;
- no automatic retry after policy denial, schema failure, destination mismatch,
  or content oversize.

### 11. Browser rendering profile

`sensorium-web-browser.v1` is deferred and additive. It does not weaken the
static profile.

The browser runs in a dedicated sandbox or Workbench virtual environment with:

- an empty, one-use browser profile;
- no host cookies, keychain, SSH agent, clipboard, browser profile, client
  certificates, or ambient proxy;
- no host filesystem sharing;
- a host-controlled egress proxy or equivalent network enforcement;
- bounded process count, CPU, RAM, storage, console output, subresources, and
  wall time;
- no downloads, uploads, dialogs, permissions, service-worker persistence, or
  extension loading by default;
- one per-boot/session nonce and exact source-generation binding.

Python may use Playwright for mechanics, but browser ownership and egress remain
host-controlled. Browser success produces a rendered snapshot; it does not grant
DOM interaction or remote actuation.

### 12. Crawling profile

`sensorium-web-crawl.v1` is deferred because a crawler owns a queue and discovery
policy, not just repeated fetch calls.

Before implementation it requires explicit contracts for:

- frontier identity, deduplication key, cap, TTL, and persistence;
- maximum depth, pages, origins, bytes, and total duration;
- URL normalization and query-parameter policy;
- per-origin politeness and retry timing;
- robots policy and operator overrides;
- sitemap and feed handling;
- restart reconciliation and partial completion;
- output grouping and retention;
- cancellation and teardown.

A crawl result is a bounded collection of observations or artifact refs, not a
new publication authority.

### 13. Relationship to Weak Signal Harvester

P078 and this proposal compose without merging responsibilities:

```text
sensorium-web snapshot
  -> explicitly configured Harvester source
  -> grouping and candidate finding
  -> human/operator review
  -> optional Whisper draft
```

Sensorium Web proves and records acquisition. Weak Signal Harvester owns
correlation, findings, redaction workflow, and review. A web snapshot does not
automatically become a finding, and a finding cannot request broader crawl or
publication authority.

## Implementation Guidance

### Reuse map: named primitives before new mechanism

The Development Guidelines require consulting the shared host-owned runtime
primitive before building a private mechanism. For this connector the mapping is
already determined. Treat any deviation as a decision recorded in this proposal,
not as an implementation detail discovered during coding.

| Need | Existing primitive | Do not build |
|---|---|---|
| Supervised connector lifecycle, health, report | `middleware-supervisor`, `middleware-channel-core`, `middleware-channel-transport`, Solution 019 | a private service manager or bespoke process wrapper |
| Private connector-to-host call | the module channel and host capability admission already used by `sensorium-workbench` | a connector-local HTTP endpoint reachable by other callers |
| Periodic durable-source refresh | `replay-scheduler`, Solution 020 | a private sleep or timer loop inside the connector |
| Work that outlives one request | `deferred-operation`, Solution 029 | a background thread without an operation id or cancellation |
| Large bodies and extracted representations | `artifact-delivery`, `artifact-delivery-core`, Solution 023 | oversized inline envelopes or a private blob directory |
| Causal context, receipts, cursors | `horizontal-protocol-core`: `CausalContext`, `RootContextInput`/`ChildContextInput`/`JoinContextInput`, `canonicalize_causation_refs`, `validate_causal_context`, `causal_context_digest`, `ExecutionReceipt`, `validate_execution_receipt`, `CursorRef` | ad hoc correlation ids or a private trace shape |
| Interface publication | `sensorium-interface-core`: `InterfaceResource`, `AccessMode`, `DeliverySemantics`, `OverflowPolicy`, `InterfaceLifecycle`, `BatchOutcome`, `CURSOR_PREFIX`, `DEFAULT_MAX_FRAME_BYTES`, `DEFAULT_MAX_BATCH_BYTES`, `DEFAULT_MAX_LEASE_SECONDS` | a connector-specific publication or cursor format |
| Operational context and labels | `sensorium-interface-core::OperationalContext`, `MAX_OPERATIONAL_CONTEXT_SUMMARY_BYTES`, `classification` | a private severity or sensitivity vocabulary |
| Canonical digest inputs | `canonical-json` | per-call JSON serialization for digest computation |
| Connector-local state | `storage-sqlite` conventions | a private file format or unindexed JSON directory |
| Append-only operator sidecars | `config-sidecar-core` | direct mutation of the module config tree |
| Bounded output, timeout, containment | `sensorium-actuation-core`, `relative-path-core` | new path or cap validators |
| Process identity for the deferred browser profile | `process-supervision-core`: `ProcessIdentity { pid, start_marker }`, `capture_process_identity`, `process_is_exact`, `signal_exact_process`, `stop_exact_process` | PID-only supervision |

The connector is also subject to the middleware HTTP listener inventory gate.
Even a connector with no product listener must carry an explicit classification
and listener outcome; "no listener" is a recorded decision, not an omission.

### Crate purity and layer direction

`sensorium-web-core` must be enforced pure, not merely described as pure. The
repository already has this mechanism: the `check-*-core-deps` build guards fail
on banned dependencies **and** on banned source terms. Add an equivalent guard
for this crate in the first commit that creates it, banning at minimum HTTP
clients, TLS stacks, DNS resolvers, async runtimes, database drivers, and
process or filesystem access, plus source terms for socket, resolver, and client
construction. A purity rule introduced after the crate has grown is a rule that
will be negotiated away.

Dependency direction is one-way and must stay so:

```text
sensorium-web-core        pure types, policy, digests, invariants
  <- daemon egress broker network authority, admission, audit
  <- Sensorium Core       action resolution, observation admission
  <- Python connector     extraction mechanics only
```

The pure crate must not learn about the broker, the broker must not learn about
extraction, and extraction must not learn about grants. A helper needing facts
from two of these layers belongs in neither; it belongs in the caller that
already holds both.

Keep the boundary thin in the P084-specific sense: the broker returns response
metadata plus bytes or an artifact pointer, and nothing else. Every request to
return "just the parsed title" or "just whether it changed" moves interpretation
into the trusted layer and should be refused.

### Recommended technology split

- Rust: `url`, a pinned HTTP client such as `reqwest`, TLS configuration,
  destination classification, streaming byte caps, digesting, schema-backed
  DTOs, host admission, and audit.
- Python: a pinned extractor such as Trafilatura/lxml for main-content and
  metadata extraction, plus Playwright only in the later browser profile.
- JSON schemas: canonical in `orbidocs`, synchronized into Node and registered
  in Schema Gate before cross-process use.
- SQLite: connector-local source metadata, conditional-request hints, and bounded
  cache index; immutable bodies remain Artifact Delivery objects when retained.

The connector must not fall back to Python HTTP, `curl`, a system browser, or an
unmediated subprocess when the Rust host broker is absent.

### Egress denial is a host property, not a connector promise

`inv-swo-no-ambient-egress` must be enforced by something other than the
connector's own restraint, and the node already has the vocabulary. The model
runtime layer defines an egress policy shape of `offline_ok`, `allowed_domains`,
`proxy_profile`, and `on_error`, plus an optional host-resolved sandbox profile
reference; the daemon's runtime conformance fixtures assert `require_no_egress`
and `require_process_no_egress` and refuse a runtime whose declared policy
contradicts them. Reuse that shape rather than inventing a second egress
vocabulary:

- the connector's declared egress policy has empty `allowed_domains` and
  `offline_ok = true`;
- a host conformance fixture asserts process-level no-egress for the connector
  and fails closed when either the declared policy or the observed process
  contradicts it;
- absence of the private host fetch capability is terminal, and the refusal is a
  typed member of `sensorium-web-error-codes.v1`, not a log line;
- the acceptance pack proves the negative directly: with the broker capability
  withheld, an ordinary fetch fails with the typed refusal and produces no
  socket, no subprocess, and no observation.

Platform enforcement already exists for the model-package no-egress path
(seccomp-bpf on Linux, `sandbox-exec` on macOS). Reuse that implementation
instead of adding a third mechanism. Where a platform has no enforcement, the
fallback is refusal, not a weaker profile.

### One fetch is a state machine, not a call chain

A fetch has too many distinct failure surfaces to survive as an implicit chain of
fallible calls. Declare states and legal transitions as data in
`sensorium-web-core`, and drive both the broker and the tests from that table:

```text
planned -> url-admitted -> destination-resolved -> destination-admitted
        -> connected -> tls-established -> headers-received
        -> body-streaming -> body-complete -> decoded -> extracted
        -> observed -> published
```

with `refused{reason}`, `expired{phase}`, and `unknown{phase}` as terminal
classes reachable from named states. Two rules the table must make structural
rather than aspirational:

- a redirect is a transition **back** to `url-admitted` carrying an incremented
  hop count, not a loop inside the connection step. `inv-swo-redirect-revalidated`
  then holds by construction instead of by reviewer vigilance;
- `unknown` is a first-class outcome. A read that times out mid-body has an
  honest outcome distinct from both success and refusal, exactly as P083 treats a
  timed-out actuation. Never collapse `unknown` into `refused` for tidiness: the
  remote server may have observed and served the request either way, and a
  partial body must never be extracted as if it were complete.

### Coupled state changes need one journal and one point of routability

A single successful acquisition writes to several stores: artifact objects,
connector source state and conditional hints, observation admission, and possibly
interface publication. Leaving these coupled by hope is the failure the
guidelines name explicitly. Follow the staging-then-commit pattern the node
already uses for model-package activation:

- artifacts are written and digest-verified **before** any snapshot record
  references them;
- the snapshot becomes readable only after one commit binding
  `source/generation-ref`, body digest, extraction digest, and artifact refs
  together;
- a crash between stages leaves staged artifacts unreferenced and collectable,
  never a snapshot pointing at a missing or partial body;
- publication is a separate commit with its own authority check, so a fetch
  commit can never imply an interface commit
  (`inv-swo-fetch-does-not-authorize-publication`).

### Recovery has one source of truth

On restart the host, not the connector, decides what was in flight. Enumerate at
startup and resolve every case to a typed terminal state before serving:

| Interrupted state | Resolution |
|---|---|
| Broker fetch without a completion record | mark failed with a retryable class; never silently re-issue |
| Staged artifact without a snapshot commit | collect under the artifact lifecycle |
| Snapshot commit without publication | leave unpublished; publication needs its own authority |
| Deferred operation in `pending`/`running` | mark failed with retry diagnostics, per the existing recovery contract |
| Scheduler launch mid-flight | reconcile through scheduler accounting; do not double-count |

Blind re-invocation after restart is the specific failure to avoid. A fetch is
externally observable, so replay is never free: it re-discloses the node's
network position and timing to the remote server.

### Every store has an owner, a key, caps, a TTL, and a restart rule

Declare these in the schemas rather than in code comments. The connector
introduces at least four stores, and each needs the full five-tuple:

| Store | Key | Bounds to declare |
|---|---|---|
| conditional-request hints (`ETag`, `Last-Modified`) | `source/ref` plus generation | entry cap, TTL, invalidation on generation change |
| response and extraction cache index | body digest | entry cap, byte cap, age cap, eviction policy |
| retained bodies and representations | artifact ref | opt-in per source, retention rule, deletion path |
| per-origin rate and concurrency accounting | canonical origin | window, cap, reset semantics, restart behaviour |

Eviction may force a full refetch but must never turn a stale retained
representation into a fresh observation. That is the `304` reuse rule expressed
as a cache invariant, and it is the same rule stated twice on purpose.

### Identifiers are explicit; identity is never derived from labels

- The display URL is a redaction; the digest is the identity. Never join,
  deduplicate, cache, or fence on the display form.
- A source generation is a declared ref, not a hash of the current URL string.
  Two sources may legitimately share a URL under different extraction or
  classification postures.
- Never derive trust, origin identity, or classification from `Host`,
  `Content-Type`, a canonical-link tag, or any other remote-controlled label. The
  canonical origin comes from the host's own canonicalization and the admitted
  resolved address, never from what the response says about itself.
- Give `source/ref`, `source/generation-ref`, snapshot ids, and artifact refs
  distinct prefixes with validators, following the existing
  `sensorium-interface:`, `sensorium-subscription:`, and `sifc1:` conventions.

### Schema Gate registration is a checklist, not a step

A partial contract registration compiles cleanly while leaving the gate open, so
treat it as a checklist. For each of the six V1 schemas complete all of:

1. the contract-family variant;
2. the lazily initialized validator static;
3. the contract spec entry with schema id, file name, and boundary;
4. the public validation function;
5. the private validator that compiles the schema;
6. embedded reference aliases for the bare, `embedded://`, and
   `urn:orbiplex:schema:` forms;
7. the embedded schema source entry;
8. a positive example in the content tests;
9. a negative example in the invalid-example list;
10. membership in the family coverage list.

Canonical schemas live in `orbidocs` and are synchronized into the Node contract
root. Both schema copies, both example sets, and the coverage generators must
move together; drift between those copies has been a recurring CI failure and is
never caught by local tests alone.

### Observability without a second disclosure channel

For this connector the operator surface is itself a leak risk, so state the rule
as a schema property rather than a convention. `sensorium-web-operator-snapshot.v1`
and every audit record are metadata-only, and none of the following may ever
appear in them: request headers, `Authorization`, cookies or `Set-Cookie`, exact
query values outside the source allowlist, redirect `Location` values, resolved
addresses, local socket details, proxy metadata, or response bodies.

What must appear, because a refusal that cannot be diagnosed will be worked
around: the typed refusal reason, the phase in which it occurred, the hop index
for redirect refusals, the destination class for classification refusals, and the
limit that was hit reported alongside its configured value.

Prove the redaction the way retained Story 012 evidence proves it: run a real
fetch against a fixture that serves secret-shaped headers, cookies, and signed
query values, then assert their absence across every persisted record, artifact,
audit row, operator snapshot, and interface frame.

### Refusal and replay first

The corpus below is close to sufficient. Two structural additions make it
self-maintaining:

- drive the refusal matrix from `sensorium-web-error-codes.v1` so that every
  declared code has at least one fixture, and a new code without a fixture fails
  the build. A closed error vocabulary whose members are unreachable is a
  documentation artifact, not a gate;
- order the tiers by cost and keep the expensive tier out of the diagnostic loop.
  Pure-core tests need no I/O; broker tests need only local HTTP/TLS fixtures and
  a deterministic resolver; extraction tests need only checked-in HTML. The full
  connector-to-interface path is the last tier and should be entered with the
  earlier tiers green. No tier may reach a public site.

### Suggested implementation order

Each step ends at a gate the next step assumes. Do not carry an unproven
assumption forward, and do not use the most expensive layer as the diagnostic
loop for a question a cheaper layer can answer.

1. Resolve Open Questions 1-4 and record the decisions here. Contract shape
   depends on them, so freezing schemas first would freeze a guess.
2. Freeze the six schemas with positive and negative fixtures and complete Schema
   Gate registration end to end. *Gate:* unknown fields, missing bounds, and
   malformed provenance are rejected by the gate, not by application code.
3. Implement `sensorium-web-core` with the purity guard present from the first
   commit: URL canonicalization, destination classes, budget relations,
   generation replacement, the fetch state table, typed errors, digest inputs.
   *Gate:* the crate has no HTTP, DNS, TLS, async, storage, or process
   dependency, and the guard proves it in CI.
4. Implement the private daemon-owned egress broker against local HTTP/TLS
   fixtures and a deterministic resolver. *Gate:* the SSRF and redirect matrix
   passes, and no reusable socket, resolver, cookie jar, or credential handle
   crosses the boundary.
5. Add the Python static extractor against offline HTML fixtures only, with
   pinned extractor identity bound into the output digest. *Gate:* deterministic
   extraction digests and typed empty or low-confidence outcomes.
6. Wire egress denial and prove the negative: with the broker capability
   withheld, the connector refuses with a typed error and produces no network
   activity at all.
7. Compose fetch, artifact retention, and observation admission under the
   single-commit routability rule and the restart resolution table. *Gate:* a
   crash injected between any two stages leaves no snapshot referencing a partial
   body.
8. Add durable sources, conditional refresh, scheduler, and deferred operations,
   with every cache and rate store fully declared. *Gate:* `304` reuse requires
   exact retained evidence under an unchanged generation.
9. Register the P082 `latest-state` source-provider adapter. *Gate:* read and
   subscribe authority provably cannot cause a refresh.
10. Collect end-to-end evidence including the redaction proof, then synchronize
    Solutions 030 and 046, the Node ledgers, trackers, and readiness before
    considering the deferred browser or crawl profiles.

### Conformance corpus

The checked-in test corpus should include:

- ordinary HTML, malformed HTML, conflicting charset declarations, compressed
  bodies, oversized headers, decompression bombs, empty extraction, and invalid
  UTF encodings;
- redirect loops, cross-origin redirects, redirects to loopback/private/link-local
  addresses, DNS rebinding fixtures, mixed A/AAAA results, and prohibited ports;
- conditional refresh, changed content, unchanged content, source replacement,
  cache eviction, restart, and superseded publication;
- prompt-injection text, hostile ANSI/control characters, misleading canonical
  links, active scripts, tracking pixels, and secret-shaped query values;
- interface publication, revocation, stale generation, remote read, and consumer
  digest verification;
- authority negatives: a fetch attempted without the broker capability, an
  interface read attempting to trigger a refresh, a publication attempted from
  fetch authority alone, and a carrier attempting to reinterpret or widen an
  admitted snapshot;
- restart and recovery: a crash between artifact staging and snapshot commit, a
  crash mid-body, an interrupted deferred operation, and an interrupted scheduler
  launch, each resolving to the typed terminal state named in the recovery table
  without blind refetch;
- redaction proof: a fixture serving secret-shaped headers, cookies, and signed
  query values, with absence asserted across snapshots, artifacts, audit records,
  the operator snapshot, and interface frames;
- one fixture per declared member of `sensorium-web-error-codes.v1`, enforced so
  that an unreachable error code fails the build.

Tests use local fixture servers and deterministic DNS adapters. Ordinary CI does
not scrape public sites.

## Named Invariants

| Invariant | Requirement |
|---|---|
| `inv-swo-no-ambient-egress` | The connector cannot fetch when the private host broker or exact fetch authority is absent. |
| `inv-swo-observation-does-not-authorize-fetch` | P082 read/subscribe authority never grants acquisition authority. |
| `inv-swo-fetch-does-not-authorize-publication` | A successful fetch never creates interface, Room, Agora, Whisper, or Memarium authority. |
| `inv-swo-redirect-revalidated` | Every redirect target repeats URL, grant, DNS, destination, port, and budget admission before connection. |
| `inv-swo-destination-public-by-proof` | Unknown, mixed, missing, or prohibited destination classification fails closed. |
| `inv-swo-body-bounded-before-parse` | Compressed, decompressed, header, and body limits are enforced before unbounded parsing or storage. |
| `inv-swo-source-generation-fenced` | URL, policy, extraction, classification, or operational-context replacement fences the prior generation. |
| `inv-swo-extraction-content-bound` | Extracted representation digest binds body digest, extractor identity, version, and options. |
| `inv-swo-hostile-content-inert` | Remote bytes and extracted text cannot establish policy, authority, wiring, or executable intent. |
| `inv-swo-retention-explicit` | Raw bodies, rendered DOM, screenshots, and extracted text are retained only under explicit bounded policy. |
| `inv-swo-carrier-neutral` | P082 carriers preserve the admitted snapshot and never refresh, reinterpret, or widen it. |
| `inv-swo-crawl-frontier-bounded` | Any future crawler has an explicit owner, cap, lifecycle, restart rule, and cancellation path. |

## Trade-offs

| Decision | Benefit | Cost |
|---|---|---|
| Rust performs the actual fetch | Network authority and SSRF controls remain in the trusted host boundary. | The host broker carries response bytes or artifact creation rather than exposing a lightweight socket grant. |
| Python performs extraction | Reuses mature extraction and browser ecosystems and keeps heuristics replaceable. | Requires cross-language golden vectors and pinned extraction profiles. |
| Static HTML first | Produces a small, testable, useful V1 without browser process authority. | Some modern sites yield incomplete content until the browser profile exists. |
| Latest-state interface first | Reuses P082 and avoids accidental archival semantics. | Consumers cannot request historical page versions unless a separate retention profile exists. |
| Raw retention is opt-in | Minimizes storage, privacy, copyright, and secret-retention exposure. | Extraction defects may be harder to reproduce when the body was deliberately not retained. |
| Durable and ad hoc sources are distinct | Makes scheduling, generations, and grants understandable. | Two action roles and policy paths require separate acceptance coverage. |

## Failure Modes and Mitigations

| Failure | Risk | Mitigation |
|---|---|---|
| URL resolves to local or metadata service | Connector becomes an SSRF proxy into host authority. | Host resolves and classifies all A/AAAA results, pins the admitted address, rejects mixed/unknown sets, and repeats admission for redirects. |
| Python connector receives ambient network access | Missing host admission silently becomes a weaker path. | Reference sandbox denies egress; absence of the private host fetch capability is terminal. |
| Redirect crosses the grant boundary | Initially safe URL escapes into another origin or network class. | Redirects are disabled in the client and followed only by the host admission loop. |
| Compressed response expands without bound | Memory, disk, or parser exhaustion. | Separate compressed and decompressed streaming caps plus total deadline. |
| Hostile HTML attacks parser or operator terminal | Code execution, denial of service, or terminal injection. | Pinned parser, process isolation where practical, tree/depth/time caps, inert output, and presentation sanitization. |
| Page text instructs an Agent to act | Prompt injection becomes confused-deputy authority. | External-content caution layer, inert artifact binding, and ordinary host admission for every later effect. |
| Conditional request revives stale data | Old body is represented as current after policy or extractor change. | Reuse only under the same source generation and extraction profile with retained digest evidence. |
| Cache grows without bound | Storage exhaustion and unreviewable retention. | Entry/byte/age caps, explicit owner and cleanup, metadata-first records. |
| Browser profile inherits host state | Cookies, credentials, identity, or private history leak to the site. | Empty one-use profile, no host shares, no ambient credentials, isolated environment. |
| Crawler ignores service-owner policy | Excessive load, legal or ethical violations, blocking. | Separate crawler contract, robots and politeness policy, per-origin budgets, operator inspection. |
| Consumer mistakes a snapshot for truth | Fetched claim becomes asserted fact. | Preserve source and extraction provenance; page metadata remains a claim; corroboration belongs to higher layers. |
| URL query contains a token or signed capability | Credentials leak through observations, audit, logs, or remote interfaces. | Keep exact URLs host-private, expose redacted display URLs plus exact digests, and require an allowlist for visible query fields. |
| Remote consumer causes source refresh | Read authority widens into network acquisition authority. | Interface reads consume admitted snapshots only; refresh requires a separate local action and grant. |

## Open Questions

1. **Which URL admission posture should V1 expose?**
   - **A (sensible default):** operator-configured domain/origin allowlists only;
     ad hoc fetch grants must still name an allowed origin.
   - **B:** any public HTTPS destination passing SSRF controls.
   - **C:** both profiles, with A as default and B requiring an explicit
     non-delegable operator policy.

2. **What should happen when `robots.txt` cannot be fetched or parsed?**
   - **A (sensible default):** durable crawling fails closed, while one explicit
     operator-requested snapshot may proceed only when source policy says robots
     is not applicable or the operator controls the origin.
   - **B:** follow RFC error semantics for all profiles and record the result.
   - **C:** treat robots only as advisory and never block acquisition.

3. **What is the canonical extracted representation?**
   - **A (sensible default):** structured JSON blocks plus a deterministic plain
     text projection; Markdown is an optional derived artifact.
   - **B:** canonical Markdown with metadata sidecar.
   - **C:** plain text only in V1.

4. **Should raw HTML retention be enabled for durable sources by default?**
   - **A (sensible default):** no; retain digest and bounded metadata, with raw
     Artifact Delivery storage enabled explicitly per source.
   - **B:** retain every body for reproducibility under a short TTL.
   - **C:** retain only bodies whose extraction failed or changed unexpectedly.

5. **Should JavaScript rendering remain a profile of `sensorium-web` or become a
   separate connector?**
   - **A (sensible default):** one connector family with a distinct
     `sensorium-web-browser.v1` backend and separate action/policy profile.
   - **B:** a separate `sensorium-browser` connector because browser process and
     egress authority are materially different.
   - **C:** keep browser rendering entirely inside Workbench jobs.

6. **When should authenticated sources enter scope?**
   - **A (sensible default):** after static public-web acceptance; introduce a
     separate credential-bound profile with host-owned secret use and no cookie
     exposure to consumers.
   - **B:** include bearer/basic authentication in V1 durable sources.
   - **C:** never support authentication in this connector; require source-side
     export or a domain-specific connector.

7. **Does crawling belong to this proposal after V1?**
   - **A (sensible default):** keep the extension points and deferred tracker
     item here, but require a dedicated follow-up proposal before implementing
     the crawl frontier.
   - **B:** define and implement crawling as Phase 2 of P084.
   - **C:** leave crawling exclusively to Weak Signal Harvester.

8. **Which link data may enter the consumer-visible snapshot?**
   - **A (sensible default):** canonical destination URL without user-info or
     fragment, bounded relation/text metadata, and no automatic follow.
   - **B:** only link digests and same-origin counts.
   - **C:** all extracted href values after syntax validation.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Work item | Status | Acceptance boundary |
|---|---|---|---|
| P084-001 | Freeze architecture, V1 scope, source identity, authority split, named invariants, and Open Questions | in-progress | Draft proposal defines the stratified baseline; acceptance requires resolving V1 questions and recording decisions here. |
| P084-002 | Define the six-schema V1 contract family, typed errors, positive/negative fixtures, and Schema Gate registration | todo | Closed schemas reject unknown fields, missing bounds, unsupported methods/schemes, mixed inline/artifact bodies, invalid generation bindings, and malformed provenance. |
| P084-003 | Implement `sensorium-web-core` URL, destination, budget, generation, digest, and failure semantics | todo | Pure Rust tests cover canonicalization, every destination class, redirect revalidation plans, limit relations, generation replacement, and retry classification without daemon or HTTP dependencies. |
| P084-004 | Implement the private daemon-owned Rust HTTP(S) egress broker | todo | Exact connector/action admission, DNS A/AAAA classification, pinned connections, TLS, redirect loop, compressed/decompressed caps, deadlines, concurrency, aggregate metrics, and no-socket-return invariants pass. |
| P084-005 | Implement the supervised Python static extraction connector without ambient egress | todo | Offline fixtures prove bounded parsing, deterministic extraction digests, hostile-content inertness, typed empty/failure outcomes, and hard refusal when the host broker is absent. |
| P084-006 | Add durable source configuration, metadata-first cache, conditional refresh, scheduler, BDO, restart, and operator inspection | todo | Source replacement fences prior generations; `304` reuse requires exact retained evidence; caches and schedules remain bounded and inspectable across restart. |
| P084-007 | Integrate Sensorium observation admission, P081 causal context, classification, operational context, and Artifact Delivery | todo | One fetch-to-observation trace binds directive, host response digest, extractor profile, admitted snapshot, artifacts, and typed failures without retaining secrets. |
| P084-008 | Register the P082 `latest-state` source-provider adapter and local/remote interface acceptance | todo | Local read/SSE and authorized direct-peer or Room projection return the same admitted snapshot; revocation, stale generation, supersession, and remote-refresh attempts fail closed. |
| P084-009 | Add static-profile conformance, load, refusal, and end-to-end evidence; synchronize Solution 030/046, Node ledgers, trackers, and readiness | todo | Deterministic local HTTP/TLS and DNS fixtures cover the named invariants; no public-site dependency enters CI. |
| P084-010 | Add `sensorium-web-browser.v1` isolated JavaScript rendering profile | deferred | Requires a separately accepted browser process, host-controlled egress, empty profile, resource caps, no credentials/shares, rendered snapshot contracts, and deployment evidence. |
| P084-011 | Define and implement `sensorium-web-crawl.v1` frontier and politeness profile | deferred | Requires a dedicated follow-up proposal resolving frontier lifecycle, robots behavior, depth/page/origin budgets, restart, cancellation, retention, and operator evidence. |
| P084-012 | Integrate explicitly configured P084 snapshots as an optional P078 Harvester source | deferred | Harvester receives only admitted snapshot/artifact refs and cannot widen fetch, crawl, finding-publication, or Whisper authority. |

## Next Actions

1. Resolve Open Questions 1-4 to freeze the static V1 contract.
2. Draft the six canonical schemas and refusal fixtures before selecting concrete
   HTTP or extraction library APIs.
3. Prototype the pure Rust URL/destination/budget core and verify that the host
   can fetch local deterministic HTTPS fixtures without exposing a reusable
   socket to Python.
4. Evaluate two pinned Python extraction profiles against one checked-in corpus
   and select the profile by reproducibility and extraction quality rather than
   package popularity alone.
5. Keep browser rendering, credentials, crawling, and P078 integration deferred
   until the static snapshot path has end-to-end authority and retention
   evidence.

## External Standards and Implementation References

- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html)
- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Playwright supported languages](https://playwright.dev/docs/languages)
- [Trafilatura documentation](https://trafilatura.readthedocs.io/en/stable/index.html)
- [Reqwest `ClientBuilder`](https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html)
