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
  -> daemon-owned bounded HTTP(S) fetch host capability
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
not call connector-local HTTP endpoints or the bounded-fetch host capability
directly.

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

#### Pure Rust contract cores

Two small crates keep reusable fetch authority separate from web-observation
semantics:

- `bounded-http-fetch-core` owns the fetch request/result vocabulary, URL and
  origin canonicalization, destination classes, intersected budgets, and typed
  failures;
- `sensorium-web-core` owns source identity, source-generation replacement,
  extraction-profile binding, snapshot provenance, and web-observation digests.

Together they own:

- closed fetch-plan and fetch-result types;
- URL canonicalization rules;
- scheme, port, method, redirect, byte, time, and media-type constraints;
- destination-network classes and matching;
- source-generation and extraction-profile binding;
- typed failure classification;
- canonical digest inputs;
- invariants shared by the bounded-fetch host capability, schema gate, and tests.

It has no HTTP client, daemon, browser, Python, database, or async-runtime
dependency unless an async trait is required by a later implementation layer.

#### Reusable daemon-owned bounded HTTP(S) fetch host capability

P084 is the first admitted consumer of this narrow reusable primitive. Reuse
does not make it a public fetch proxy: every consumer and action requires exact
host-capability registration, policy, scope, and budget admission, while
connector-specific interpretation remains outside the host capability.

The host capability owns actual network authority:

- admission of the exact connector caller and action;
- resolution of A and AAAA records;
- rejection of prohibited destination classes;
- connection establishment and TLS policy;
- redirect-by-redirect revalidation;
- response streaming with compressed and decompressed byte caps;
- one total deadline plus bounded connect and per-hop request deadlines;
- bounded concurrency and per-origin rate accounting;
- metadata-only audit and operator status.

The host capability returns bounded bytes over the private middleware channel or
writes a large body into Artifact Delivery and returns an immutable pointer. It
never returns a reusable socket, DNS resolver, cookie jar, or credential handle.

The reference host resolves through the host's configured DNS servers using an
in-process resolver with one bounded attempt, an internal lookup deadline, a
bounded worker pool, and bounded queue backpressure. Caller timeout therefore
does not leave an unbounded libc `getaddrinfo` call occupying a worker. Queue
saturation is `concurrency-limit`; loss of the worker channel is
`transport-failed`.

The reference HTTPS client explicitly selects rustls with the pinned WebPKI root
set and does not consume the platform-native trust store or ambient corporate
root additions. Explicit DER roots are additive deployment or conformance
inputs. Certificate or SPKI pinning is not part of the static V1 source
contract.

Each admitted hop receives a fresh client bound to that hop's newly resolved and
revalidated address. This intentionally prevents connection pooling from
reusing a socket admitted under an earlier DNS answer. Explicit DER roots are
validated and parsed once when the host service is constructed, not once per
hop. `hop-timeout/ms` bounds the complete request hop, including response-body
transfer; it is not an idle-read timeout. The unchanged total deadline remains
the outer bound across DNS, connects, redirects, and body transfer.

#### Python `sensorium-web` connector

Python owns replaceable mechanics:

- invoking the private bounded-fetch host capability;
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

The initial acquisition profile is `sensorium-web-static.v1`. Its first frozen
extraction implementation is
`sensorium-web-extraction:static-stdlib-main-v1`, version `1.2.1`, with profile
digest `sha256:0gMi6eb_EENqcuRAdqjUJq-tNJxgskpqFOuzIzd7gmk`, output schema
`sensorium-web-document-blocks.v1`, and algorithm identity
`python-stdlib-html-parser-main-content-v1`. An alternative extractor is a new,
separately versioned and evidenced profile; package substitution under this
identity is forbidden.

Version `1.2.0` adds the content-bound descriptor field
`link-query/policy: strip-all`: extracted link destinations omit all query
parameters as well as fragments and user-info, before link and representation
digests are computed. The private acquisition URL keeps its exact identity.
This supersedes `1.1.0` explicitly; old source configurations are refused before
host effects, not silently relabeled. An operator must select the new profile in
a new source generation and republish with fresh interface authority. Existing
artifacts and evidence are not rewritten or claimed to have been scrubbed.

Revision `1.2.1` binds `link-truncation/policy: distinct-published-urls`.
Truncation reflects omitted distinct output after link redaction/deduplication;
query variants alone cannot mark a complete representation truncated. Its new
identity is explicit because this correction changes representation digests.
Migration from 1.2.0 likewise requires a new source generation. Historical
acceptance remains labeled with the profile actually executed.

Persisted-generation admission refusal is a first-class `not-started` variant
of `sensorium-web-refresh-status.v1`, with no operation identity or attempt.
The bounded source refusal projection excludes that generation from scheduling
and exposes the reason in the operator snapshot; healthy sources continue.
An already claimed operation instead settles `terminal` with the same typed
failure/code and failure/phase. Both return the declared contract at HTTP 200.
This preserves operation accounting without inventing an operation merely to
report a deterministic refusal. New generation admission clears the projection.

The acquisition profile has these boundaries:

- methods: `GET` and bounded conditional `HEAD` only;
- schemes: HTTPS by default; HTTP requires an explicit source or grant posture;
- no URL user-info;
- no `file:`, `data:`, `blob:`, `javascript:`, custom, or opaque schemes;
- no request body;
- no cookies, client certificates, ambient credentials, browser state, system
  proxy, or inherited authorization headers;
- bounded redirects, with policy re-evaluation before every hop;
- bounded compressed and decompressed response bytes;
- bounded connect, complete per-hop request, and total duration;
- response headers bounded independently by 64 fields and the admitted byte cap;
- initial accepted media types limited to `text/html`,
  `application/xhtml+xml`, and `text/plain`;
- no script execution or subresource loading;
- optional conditional requests using connector-owned `ETag` and
  `Last-Modified` state.

Content encoding, MIME sniffing, and character decoding are separate steps. A
declared media type does not authorize an unbounded parser, and a parser failure
does not erase the successfully observed response metadata.

The reusable host capability records a normalized media type but remains
consumer-neutral. The P084 static connector must pass that value through the
closed `sensorium-web-core` media-type gate before parsing or observation
admission; a missing value or any value outside the three-item set is a typed
refusal. The request contract therefore does not let a consumer widen the host
primitive by supplying its own media allowlist.

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

[Proposal 088: Pull-Based Artifact Acquisition](088-pull-based-artifact-acquisition.md)
is one such future consumer. It may reuse the daemon-owned bounded HTTP fetch
mechanism to retrieve exact portable artifact bytes, but it owns custody staging,
receipts, anti-rollback, and Artifact Delivery admission handoff rather than web
observation semantics. P084 remains the owner of changing web-source snapshots
and Sensorium Interface publication. When a P088 location points to a static web
page that embeds an artifact, the shared host fetch seam returns only the admitted,
bounded response bytes. P088 then applies its own offline, operator-bound extraction
profile; P084 neither selects that parser nor gains custody or admission authority.

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

The V1 admission posture uses operator-configured origin allowlists. An
allowlist entry binds an exact scheme and port to either an exact canonical host
or a bounded host glob. In a host glob, `*` matches zero or more characters and
`?` matches exactly one character within one DNS label; neither symbol matches a
dot. Matching is anchored to the whole canonical ASCII host after IDNA
normalization. Wildcards are forbidden in schemes, ports, IP literals, and URL
paths, queries, or fragments. Consequently, `*.example.org` may match
`www.example.org` but not `example.org`, `www.example.org.evil.invalid`, or a
resolved address outside the admitted destination class.

The operator allowlist is only the outer policy boundary. An ad hoc fetch grant
must name one exact canonical origin admitted by that boundary; it cannot carry
or inherit a host glob. Redirects must match both the operator allowlist and the
effective exact-origin grant. Globbing therefore reduces operator configuration
duplication without turning a caller grant into open-ended destination
authority.

### 5. Contract family

The first implementation defines eight reusable host-capability schemas and
twelve P084 domain schemas:

| Schema | Purpose |
|---|---|
| `bounded-http-fetch-request.v1` | Private middleware-to-host bounded fetch plan. |
| `bounded-http-fetch-result.v1` | Private response metadata plus bounded inline bytes or one Artifact Delivery pointer. |
| `bounded-http-fetch-artifact-read-request.v1` | Content-bound continuation request for a body moved into Artifact Delivery. |
| `bounded-http-fetch-artifact-read-result.v1` | Bounded body bytes bound to the admitted caller, action, artifact ref, digest, and size. |
| `bounded-http-fetch-error-codes.v1` | Closed typed host failure vocabulary and retry class. |
| `bounded-http-fetch-operator-snapshot.v1` | Identifier-free aggregate readiness, occupancy, refusal, failure, and handoff evidence. |
| `artifact-delivery-retain-request.v1` | Exact caller-owned, content-bound request to retain one representation without gaining read or publication authority. |
| `artifact-delivery-retain-result.v1` | Immutable Artifact Delivery ref plus the P081 execution receipt for the completed retention effect. |
| `sensorium-web-source.v1` | Operator-owned durable source configuration and current generation. |
| `sensorium-web-extraction-request.v1` | Exact source/profile/fetch binding accepted by the supervised extractor. |
| `sensorium-web-document-blocks.v1` | Bounded inert title, text block, heading, and link representation. |
| `sensorium-web-extraction-result.v1` | Typed extraction outcome and content-bound representation. |
| `sensorium-web-document-snapshot.v1` | Canonical admitted document observation. |
| `sensorium-web-durable-source.v1` | Bounded durable-source declaration, schedule, retention, classification, and generation. |
| `sensorium-web-refresh-claim.v1` | Closed idle-or-claimed handoff from the supervised connector to the daemon worker, including the exact source operation and timeout. |
| `sensorium-web-refresh-status.v1` | Content-bound refresh lifecycle and typed terminal outcome. |
| `sensorium-web-refresh-sweep.v1` | Bounded worker/scheduler launch summary with exact deferred-operation bindings and a closed stop reason. |
| `sensorium-web-refresh-sweep-outcome.v1` | Persisted Replay Scheduler outcome whose details are one schema-gated refresh sweep. |
| `sensorium-web-operator-snapshot.v1` | Metadata-only bounded source, cache, schedule, and occupancy inspection. |
| `sensorium-web-latest-state.v1` | Exact current generation, admitted snapshot, optional representation, and observation binding consumed by P082. |

The host schemas are intentionally consumer-neutral. The Rust `WebSource` type
uses the same nested
`extraction/profile`, `origin/policy-ref`, `operational/context`, and
`classification` fields as `sensorium-web-source.v1`; its canonical fixture must
round-trip through the typed contract without translation. P084 remains
responsible for translating a completed bounded fetch into the web source and
document snapshot contracts; the host capability does not interpret HTML or
publish a Sensorium observation.

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
the current source generation, policy, requested and final URL digests, retained
body digest, retained fetch-result digest, and extraction profile still match.

Only `301`, `302`, `303`, `307`, and `308` invoke redirect handling and require a
valid same-origin `Location`. Other 3xx statuses, including `300` and `304`, are
terminal bounded responses; connector policy decides whether their metadata can
be used, and only the exact `304` rule above permits prior-body reuse.

### 7. Extraction and hostile content

Extraction transforms bytes into a representation; it does not validate claims
made by the page.

The connector must:

- parse HTML/XHTML within a `512 KiB` input cap, `65,536` parser-event cap,
  `128`-element nesting-depth cap, and the existing bounded output counts; these
  deterministic work limits bound parser time without making canonical output
  depend on a host-speed-sensitive wall-clock cutoff; `text/plain` remains
  bounded by the same input and output caps without an HTML event/depth budget;
- preserve `consumer-denied`, `artifact-binding-mismatch`, and
  `artifact-size-limit` across the content-bound artifact handoff; preserve
  `artifact-transfer-expired` only when the host retains an exact tombstone for
  the previously admitted caller/action/ref/digest/size binding, while unknown
  or altered bindings remain `artifact-binding-mismatch`; report
  conflicting HTTP and document charset declarations as the closed
  `charset-conflict` refusal rather than hiding these conditions behind a
  generic artifact or decode failure;
- sanitize control characters before operator presentation;
- keep scripts, event handlers, styles, hidden nodes, and active content inert;
- represent links as data without following them in V1;
- mark title, author, date, language, and canonical-link values as page claims;
- record extractor identity and configuration in the output digest;
- treat empty or low-confidence extraction as a typed outcome rather than
  silently substituting arbitrary HTML text;
- label every extracted representation as untrusted external content for Agent
  and Inquirium consumers.

`sensorium-web-refresh-status.v1` carries those typed causes rather than one
flat code. A refused extraction reports the extraction stage's own
`failure/code` and `failure/phase` — `unsupported-media-type`,
`charset-conflict`, `decode-failed`, `empty-document`, `parser-limit`,
`invalid-request`, or one of the artifact-handoff refusals — and keeps
`extraction-refused` only when the stage named no cause. Collapsing every cause
into `extraction-refused` would contradict the preservation required above and
leaves a failing refresh undiagnosable from its status alone.

A refusal owned by the layer under the connector is reported the same way.
`fetch-not-completed` says the host fetch delivered no body; the host's own
cause travels beside it as `failure/upstream-code` and `failure/upstream-phase`,
so one status answers both what refused and why the layer under it did, without
asking an operator to correlate two logs.

The canonical extracted representation is a closed sequence of structured JSON
blocks plus a deterministic plain-text projection derived from those blocks.
Block order, whitespace normalization, omitted-node policy, and metadata bounds
belong to the pinned extraction profile and participate in the representation
digest. Markdown may be emitted only as an optional derived artifact; it is not
the canonical observation and cannot replace the structured blocks or plain-text
projection during admission or replay.

Consumer-visible links contain only a canonical destination URL without
user-info, fragment, or query parameters and bounded relation and text metadata. They remain inert
data: publication never follows them automatically and never grants acquisition
authority. The active 1.2.1 profile exposes no allowlisted query fields; it
strips the query entirely before computing the published link digest.

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

The daemon-owned `artifact.delivery.retain` host capability accepts only an
authenticated component whose exact id equals `owner/component-id`. It verifies
the declared digest and size before storage, returns a content-addressed
`artifact-store:` ref, and emits a P081 receipt. The connector then derives a
child causal context from that receipt before `sensorium.observe.submit`;
Sensorium Core emits the second receipt with `previous/receipt-ref` bound to the
retention receipt. Durable source status retains at most four receipt refs and a
closed failure phase, never representation bytes, URLs, or host paths.
Those refs reuse the P081 `execution-receipt.v1` identifier contract, including
namespaced issuer identifiers; P084 does not narrow them to an unqualified digest.

Cache entries require an owner, key, byte cap, entry cap, TTL or retention rule,
and restart behavior. Cache eviction may force a full refetch but must not turn a
stale retained representation into a fresh observation.

The reusable fetch host keeps at most `1,024` active artifact-transfer bindings
and `1,024` bounded eviction tombstones. An exact read of an evicted binding is
refused as `artifact-transfer-expired`; an unknown, cross-caller, cross-action,
or content-mismatched read is refused as `artifact-binding-mismatch`. Tombstone
expiry intentionally collapses back to `artifact-binding-mismatch`, so the
diagnostic does not become an unbounded history or an artifact-discovery oracle.

### 8.1. Original web content for reviewed rumors {#web-original-custody}

Adopted design extension, 2026-11-04; implementation is P084-014/015 (`in-progress`).
The metadata-first default above remains valid for ordinary web observation.
A source explicitly selected for the original-backed Harvester publication
profile must retain its original response body as well as its extracted
representation before it can produce a publication-ready draft. Enabling this
profile requires explicit source/retention admission; selecting an existing
snapshot must not silently enable retention, refetch it, or widen acquisition.
[P078](078-weak-signal-harvester.md#web-source-retention-and-origin) owns review
and [P013](013-whisper-social-signal-exchange.md#web-origin-publication) owns
publication. Existing 012a/b/c evidence does not qualify this extension.

**Byte boundary.** The original is the exact bounded response body after HTTP
content decoding/decompression and before charset decoding, HTML parsing,
normalization or redaction, bound to the existing `body/digest`. It is not a
packet capture, rendered browser state or complete website archive. Preserve the
existing digest law; do not relabel parsed text or recompressed bytes as the
original. Bind the byte count, media type, charset/encoding metadata, fetched
instant, source generation, extraction profile and representation digest through
the existing snapshot. Private URL identity stays restricted; display URLs
remain redacted. Cookies and request credentials are not part of the archive.

**Custody and retention.** Reuse `artifact.delivery.retain`, its digest/size
checks, authenticated owner, content-addressed storage and P081 receipt chain.
Both inline and artifact-transfer responses must reach the same durable custody
boundary. A transient fetch binding or `body/artifact-ref` alone is not a
retention receipt. No second Harvester blob store or independent cleanup worker
is introduced. Before accepting this extension, freeze an owner-bound retention
claim using the existing artifact lifecycle and S028 facts, with at least:

| Proposed claim field | Meaning |
|---|---|
| `owner/ref`, `purpose/ref`, `snapshot/digest` | Owning source/workflow, concrete review/publication purpose and exact captured snapshot |
| `body/ref`, `body/digest`, `body/bytes`, `retention/receipt-ref` | Durable original and verified custody receipt |
| `retention/requested-until`, `retention/effective-until`, `retention/policy-ref` | Requested and admitted finite horizon, separately from metadata/cache TTL |
| `retention/state` | Closed lifecycle: `retained`, `expired`, `released`, `missing` or `corrupt`; a timestamp alone does not prove availability |

These are proposed contract fields, not currently implemented schemas. P091
composes defaults and operator ceilings; the source/workflow owner admits them.
A shortened horizon is shown before approval and cannot be silently accepted as
the requested duration. No indefinite retention or lifetime-of-rumor promise is
implied. An explicit extension needs current authority and capacity. S020 may
schedule expiry through the existing owner; reads and admission check expiry
independently of scheduler execution. Metadata and original/representation
retention have separate finite policies.

A refresh never overwrites previously claimed bytes. Shared content is reclaimed
only after all applicable owner claims permit it; releasing one finding cannot
remove another consumer's retained original. Early deletion, expiry, corruption
or loss must become an explicit availability fact. Original and representation
claims are acquired idempotently before a publication-ready handoff; a crash
between them leaves an incomplete state, never a false complete receipt. Recovery
reuses exact pinned inputs and the existing owner journals. Missing originals
block this profile's promotion; an authorized later fetch creates a new capture
and cannot repair the identity of an older one. A `304` records a new validation
time against the same retained capture; it neither creates new original bytes
nor silently renews their retention horizon. Do not claim the representation
was originally fetched at the later validation time.

**Limits and acceptance.** Preservation supports checking what the collector
received; it does not prove that the remote publisher authored the claim or that
it is true. Classification and read admission apply to original bytes separately
from redacted summaries. Storage cost and shorter approved retention are explicit
trade-offs. Offline fixtures must cover small inline and large artifact bodies,
compressed/non-UTF-8 HTML, exact digest equality, extraction that omits content,
retention refusal/quota/ceiling, `304` without horizon renewal, shared-reference
release, expiry with Scheduler
stopped, lost replies/restart between custody steps and unavailable originals.
No live website, crawler, model or new transport is needed for that gate.

### 8.2. Custody and origin implementation contract (2026-11-04)

Status: accepted implementation contract; P084-014/015 are in progress, not
qualified. P013-WEB-001/002 and P078-015/016 share this milestone. Production
adoption is explicitly outside its acceptance gate.

- The owner is Artifact Delivery: pure transitions in `artifact-delivery-core`,
  durable claim/transfer/hold facts in its existing ledger and S028 journal;
  the daemon authenticates and wires ports. No Harvester blob store is added.
- A durable reservation (claim key, digest, size) precedes staging. File and
  parent-directory synchronization precede claim commit and its receipt.
  Recovery completes or releases an interrupted reservation; its files never
  become `legacy-unclaimed`. Legacy interest is monotonic until explicit
  operator release. GC considers only managed history and all active interests.
- Retain v2 consumes either bounded inline bytes or an exact, single-use host
  transfer binding. The AD transaction consumes that binding with the claim.
  A transfer is a byte source, not custody evidence. Extraction reads are separate.
- Claim idempotency binds owner, purpose, snapshot and body digest; changed
  normative parameters refuse as `idempotency-conflict`. A replay never renews
  the original horizon. Default 24-hour custody starts at acquisition retain.
  Exact results remain available through the finite claim tombstone. Afterwards
  `idempotency-result-expired` refuses that consumed key. Its minimal hashed
  use fact remains in the existing AD journal; full private claim metadata is
  omitted from current projections after its horizon. This is not a new retain.
- P091 admits a complete, digest-pinned inactive factory policy without field
  inheritance. Only normative factory fields enter its digest. Factory drift
  and a policy above current host ceilings are distinct refusals. Claims retain
  their original terms and `resolution/id` policy reference.
- The owner persists its time high-water mark before deadline decisions. A
  regressed clock cannot revive claims; new timed effects refuse. Expiry is
  enforced without Scheduler. Extending a claim requires explicit pre-expiry
  admission; an expired web input requires a new observation and review.
- Preview refuses when any required claim ends before document validity. It
  never shortens public validity to a private custody deadline. Sign atomically
  holds all required claims until preview expiry (at most 900 seconds), keyed
  by preview digest and claim id. A retry reuses those holds. The prepared
  check token stays within the daemon process and cannot be deserialized.
- P084's existing source journal and BDO own the two-custody handoff. Neither
  `304`, restart nor review performs an implicit fetch or retention renewal.

| Effect | Recovery class | Commit / recovery boundary |
|---|---|---|
| Claim reservation/retain | transactional-withheld | Durable reservation; synchronized payload before claim receipt; reconcile exact intent |
| Release/expiry | compensatable metadata; irreversible payload erasure | Durable deletion intent and tombstone, then idempotent owner cleanup |
| Publication | irreversible-external | First admitted publication within document validity; signature alone is an artifact |

The reviewed Harvester path produces v3 for web, mixed and non-web findings.
The receiver law supports every existing source class. The bounded dual-v2/v3
profile spans exactly one epoch aligned to its anchor (at most seven days in
production). End-of-window refusal applies to every producer. Fixture acceptance
covers the whole window. Production adoption separately requires ready receiver
inventory and accepted exclusion of other receivers, plus a feasible remaining
producer migration or explicit publication-outage acceptance. A profile change
changes context/source identity; cross-profile case succession is unsupported.

Evidence uses this milestone's operator-only development profile. Keep private
originals/canaries out of Git, record path-free inventory and actual results,
and review retention by concrete technical purpose, without a fixed minimum.
Historical P084 and P015 qualifications remain pinned and unchanged.

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

One scheduler tick may claim at most 16 due sources. The effective batch is the
intersection of that hard ceiling, the scheduler `max_records` budget, the
remaining launch deadline, and the worker queue capacity. Reaching idle state,
the launch deadline, queue capacity, worker shutdown, or connector unavailability
stops the current batch with a closed `stop/reason`; a source-local rate-limit
refusal is deferred and does not prevent later due sources from being considered.
Every successful claim carries its own `timeout/ms` into the private BDO
continuation. That timeout bounds the actual connector invocation and the BDO TTL
adds only a 30-second reconciliation margin; it never replaces the invocation
bound. Any failure after a claim is returned invokes exact operation-bound
compensation, and compensation failure is emitted as structured diagnostics.

Schedules are host-owned and bounded by:

- minimum interval and jitter;
- per-source and per-origin concurrency;
- backoff and terminal/retryable error classes;
- maximum launches per period;
- operator pause, resume, run-now, and inspection;
- no automatic retry after policy denial, schema failure, destination mismatch,
  or content oversize.

### 11. Browser rendering profile

`sensorium-web-browser.v1` remains in the `sensorium-web` connector family but
is a distinct, deferred backend with its own actions and policy profile. It is
additive and does not weaken the static profile or reuse static-fetch authority
as browser-process authority.

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

### 11.1. Authenticated-source profile

Authenticated acquisition is deferred until the static public-web profile has
end-to-end acceptance evidence. It enters as a separate credential-bound profile,
not as optional fields that silently widen `sensorium-web-static.v1`.

The host owns secret resolution and use. The connector receives only the bounded
response authorized for the current source generation; credentials, cookies,
authorization headers, browser storage, and reusable authenticated handles never
enter snapshots, artifacts, audit payloads, operator output, or Sensorium
Interface frames. Missing credential authority or unavailable host secret use is
a typed terminal refusal, never an anonymous fallback.

### 12. Crawling profile

`sensorium-web-crawl.v1` is Phase 2 of P084. Its implementation remains deferred
until the static snapshot profile has end-to-end acceptance evidence because a
crawler owns a queue and discovery policy, not just repeated fetch calls. It does
not require a separate proposal, but it must complete the contracts and gates
tracked by P084-011 before implementation is accepted.

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

Durable crawling fails closed when `robots.txt` cannot be fetched or parsed. A
single explicit operator-requested snapshot may proceed without usable robots
evidence only when the source policy declares robots inapplicable or the operator
controls the origin. Such a snapshot does not establish crawl authority or seed a
frontier.

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

### 13.1. P084-012a: admitted snapshot to local review

The first Harvester slice is explicit local intake. The operator registers an
immutable, bounded binding between a Harvester source id and a P082 interface,
P084 source/generation and extraction profile digest, then selects an exact
snapshot digest. Configuration is not a read grant. Each import requires the
operator session and an independent current resource-scoped P082 read grant for
`operator:local-control`; body-supplied actors cannot replace that identity.

The host admits a one-shot P082 read, verifies the web adapter and exact binding,
then verifies and schema-gates the locally retained representation under a 1 MiB
ceiling. It rechecks current admission and snapshot after artifact I/O. Missing
retention, stale generations, revoked grants, digest/profile mismatches and
corrupt representations refuse, including on repeated imports. An admitted read
is the authorization point; subsequent revocation does not delete prior review.

The review registry stores one stable finding per configured source and selected
snapshot, with durable deduplication across reopen. The finding is
`pending-review`, preserves the full source classification and digest/reference
provenance, and requires redaction review. Source text, titles, bylines and URLs
are not copied into findings. This reference-only candidate records an operator
selection, not automated signal detection. Grouping, correlation, remote artifact
handoff, automatic harvesting and publication remain outside 012a. Review and
optional local Whisper draft preparation remain separate operator actions.

The daemon-local configure/import request shapes remain typed operator API data;
P082 reads, snapshots, document blocks and findings retain their canonical
Schema Gate contracts. `weak-signal-finding.v1` adds optional
`source/refs[]/source/classification`, preserving source policy without changing
existing findings. Implementation and measured evidence are tracked separately
in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-EVIDENCE.md` and its review follow-up
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-REVIEW-EVIDENCE.md`.

### 13.2. P084-012b: explicit web review and local draft

The operator-only `POST /v1/weak-signal-harvester/web-snapshot/review` accepts an
exact `finding/id` and `source/finding-digest`, a terminal `outcome` (`accepted`,
`rejected`, `archived`) and mandatory Boolean `create/whisper-draft`. Accepted
review requires `redaction` with nonblank `summary/redacted` (at most 4,096 Unicode
characters), `topic/class` (at most 160 ASCII token characters), and optional
`signal/polarity` (`problem`, `idea`, `question`, `context`, `mixed`). Rejected and
archived decisions forbid redaction and require `create/whisper-draft = false`.
Unknown fields and explicit nulls outside the contract refuse. The request body
is bounded to 24 KiB. Redaction means operator-authored content, not a claim that
an automatic secret detector has proved arbitrary text safe.

The host assigns `reviewed/by = operator:local-control`, the review time and a
canonical content-addressed `review/id`: `web-review:` followed by the lowercase
SHA-256 hex digest of JCS v1 JSON containing exactly `schema`, `reviewed/by`, and
`review/request`. The timestamp belongs to the first committed fact, not its
idempotency identity. A `weak-signal-web-review.v1` fact binds
the entire request to the immutable original finding digest. The original finding,
classification and acquisition provenance remain unchanged. Review operates on
already admitted local evidence: it neither rereads P082 nor fetches retained
source content. Revoking a source grant does not erase that prior admission.

The local request parser validates the canonical `review/request` fragment without
fabricating a fact or reading the clock. Invalid input/binding returns HTTP 400;
conflicting terminal intent returns 409; retained-decision capacity returns 503;
host storage/corrupt-state failures return 500. Safe closed response statuses
expose no source content or private underlying cause. Capacity requires operator
intervention, not automatic retry or evidence eviction.

One decision per finding is append-only. The fact, terminal review projection,
optional local draft and event digest commit in one SQLite transaction. Exact
replay returns the original decision and `review/no-op = true`; a changed digest,
redaction, outcome or draft intent refuses. No-op replay does not change the
reviewer, timestamp or draft id. A terminal decision cannot be edited in this
slice; revision/supersession needs a separately specified contract.

Store schema v3 adds `weak_signal_web_reviews`. Registry open validates retained
facts through Schema Gate at `Import` and repairs only divergent review projections;
emission crosses `Export`. At most 4,096 decisions are retained, each no more
than 32 KiB. The byte bound is checked before append and at replay, with a
SQLite CHECK as defense in depth. Capacity refuses new decisions while exact
replay remains available. Every registry connection explicitly enables foreign keys.
There is no automatic eviction of review evidence; retention follows the local
Harvester store, and operator export/pruning remains outside this slice. A corrupt
fact fails registry open rather than silently discarding review history; because
the registry is a required daemon startup dependency, this also blocks daemon
startup until the retained store is repaired or restored. Enabling foreign keys
does not repair previously damaged data. This is
a bounded fact/projection application of Solution 028, not a rewrite of older
Harvester event storage.

A local `weak-signal-whisper-draft.local.v1` is created only when the accepted
request explicitly sets `create/whisper-draft = true`. It carries the approved
summary/topic/polarity, finding digest, review reference, original source refs
with classification, and snapshot/source/generation/profile provenance. It stays
`publication/state = not-published` with `next/gate = whisper-publication-review`.
Preparing the draft supplies no publication authority and executes no publication
call. A draft remains subject to the separate Whisper disclosure gate. Both
legacy and web review paths use one typed local draft serializer. Required source
refs and web provenance must be present; missing evidence refuses instead of
becoming null. This local draft shape is not a publication wire contract.

Compatibility: pre-v3 findings and local drafts are retained. Pending web findings
now require the dedicated review route; the generic findings review route refuses
them instead of applying its historical default draft creation. Non-web findings
keep the P078 MVP behavior. The generic import wrapper cannot assign the reserved
host import source `sensorium-web-snapshot`. Existing already-terminal web reviews
are not silently replaced or backfilled with new approval facts.

Acceptance covers the real daemon import/redaction/draft path, module-token and
forged-actor refusals, digest binding, immutable replay, explicit rejection,
daemon restart, classification/provenance preservation and canary-free retained
state. Unit controls cover transaction failure, projection reconstruction, bounds,
corrupt facts and accepted review without a draft. Browser, crawl, authenticated
sources, automatic discovery/grouping, remote artifact handoff and publication
remain separate work; the operator UI is tracked separately as P084-012c. P084-012 remains `partial`.



### 13.3. P084-012c: operator review UI

The Node operator UI exposes the existing local review contract for already
imported web findings. It projects a bounded status queue, finding digest,
source classification and reference provenance. The operator supplies the
approved summary, topic and optional polarity; local draft creation requires
an explicit initially unchecked choice. Reject/archive carry neither redaction
nor draft intent. Terminal views show the immutable decision and any unpublished
draft; legacy terminal records remain read only.

This is a thin operator surface over P084-012b. The daemon remains the sole
owner of review authority and persistence. Operator authentication, same-origin
checks and CSRF protect mutations; a participant session alone gives no access.
The UI does not acquire source content, grant P082 access, or publish Whisper.
An exact repeated decision remains a no-op; changed intent conflicts. A transport
failure cannot trigger automatic mutation retry because the host may already
have committed. Input, conflict, capacity and host failures retain separate safe
presentations. Successful submission redirects to the committed read model.

Measured acceptance on 2026-09-15 passes real node-ui/daemon form requests for acceptance with and
without a draft, rejection and archive; independent auth/CSRF controls, escaping,
replay/conflict, restart, unchanged acquisition/delivery counts and canary checks.
Procedure: `node:tools/acceptance/sensorium-web-review-ui/README.md`.
Evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEW-UI-EVIDENCE.md`.
The UI slice does not complete broader P084-012, browser extraction, crawl,
credential-bound observation, remote handoff or publication.

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
  <- bounded-fetch host capability network authority, admission, audit
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
- Python: the frozen standard-library `HTMLParser` extraction profile for V1;
  alternate Trafilatura/lxml profiles require a new profile identity and
  evidence. Playwright belongs only to the later browser profile.
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
- absence of the private bounded-fetch host capability is terminal, and the
  refusal is a typed member of the `failure.code` enum of `sensorium-web-extraction-result.v1`, not a log line;
- the acceptance pack proves the negative directly: with the bounded-fetch host
  capability withheld, an ordinary fetch fails with the typed refusal and produces no
  socket, no subprocess, and no observation.

The factory binding requires the named `sensorium-web-no-egress` sandbox profile
and refuses startup when the enabled module lacks that profile. On macOS the
middleware runtime now compiles that profile to a Seatbelt policy which denies
ambient network and process creation while admitting only the exact host-created
loopback middleware endpoint. Deployment acceptance proves that the exact
channel works while another loopback port, DNS, proxy use, and subprocess
fallback fail. Unsupported operating-system adapters refuse the profile rather
than silently degrading to metadata-only enforcement.

The ambient network denial is inherited across `exec`; this inherited policy,
not the process-fork denial, prevents an executed child from regaining egress.
The independent process-fork rule refuses the connector's current subprocess
creation paths. Portable tests cover the probe catalog, profile shape, typed
skip, and report shaping, while CI runs the actual Seatbelt probe on macOS.

No-egress does not mean no supervision channel. The current macOS adapter admits
one exact host-created loopback WebSocket endpoint; every other `AF_INET` or
`AF_INET6` destination, inherited proxy path, and subprocess-mediated network
path remains denied. A future Unix-domain transport may replace this adapter
detail without changing the domain contract or widening connector authority.

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

On restart the host, not the connector, decides what was in flight. Recovery runs
synchronously after the supervised connector is ready but before Replay Scheduler
starts or the daemon enters its running phase. It enumerates owned BDOs with a
stable keyset cursor and resolves every case to a typed terminal state before the
worker is marked recovered. An incomplete pass remains retryable rather than being
marked recovered:

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
treat it as a checklist. For each of the twenty V1 schemas complete all of:

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
V1 source rows expose only `url/digest`; a display URL is deliberately absent
until a separately schema-gated redaction contract has a real consumer.

What must appear, because a refusal that cannot be diagnosed will be worked
around: the typed refusal reason, the phase in which it occurred, the hop index
for redirect refusals, the destination class for classification refusals, and the
limit that was hit reported alongside its configured value.

`requests/total` counts every typed request reaching the fetch-service
`execute` boundary, including requests refused by contract validation or policy
admission. Malformed JSON and values rejected by the daemon Schema Gate before
that boundary are not counted. `refused/total` includes terminal pre-dispatch
outcomes produced by the fetch service. These counters describe pressure at the
service boundary and its refusal rate; they are not an admission-only
denominator.

Prove the redaction the way retained Story 012 evidence proves it: run a real
fetch against a fixture that serves secret-shaped headers, cookies, and signed
query values, then assert their absence across every persisted record, artifact,
audit row, operator snapshot, and interface frame.

### Refusal and replay first

The corpus below is close to sufficient. Two structural additions make it
self-maintaining:

- drive the refusal matrix from the `failure.code` enum of `sensorium-web-extraction-result.v1` so that every
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

1. Apply resolved Decisions 1-8 to the appropriate profile contracts. This gate
   is complete; browser rendering, authenticated acquisition, and crawling remain
   separately capability-bound work and do not block the twenty static V1 schemas.
2. Freeze the twenty schemas with positive and negative fixtures and complete Schema
   Gate registration end to end. *Gate:* unknown fields, missing bounds, and
   malformed provenance are rejected by the gate, not by application code.
3. Implement `sensorium-web-core` with the purity guard present from the first
   commit: URL canonicalization, destination classes, budget relations,
   generation replacement, the fetch state table, typed errors, digest inputs.
   *Gate:* the crate has no HTTP, DNS, TLS, async, storage, or process
   dependency, and the guard proves it in CI.
4. Implement the daemon-owned reusable bounded HTTP(S) fetch host capability,
   with P084 as its first admitted consumer, against local HTTP/TLS
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
- one fixture per declared member of the `failure.code` enum of `sensorium-web-extraction-result.v1`, enforced so
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
| Python connector receives ambient network access | Missing host admission silently becomes a weaker path. | Reference sandbox denies egress; absence of the private bounded-fetch host capability is terminal. |
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

## Resolved Decisions

The decision numbers preserve the original Open Questions numbering so later
reviews and implementation evidence can refer to stable identifiers.

1. **URL admission posture: A, with bounded operator-side host globbing.** V1
   uses operator-configured origin allowlists. Host patterns may contain `*` and
   `?` under the label-bounded, whole-host semantics defined in Section 4.
   Scheme and port remain exact, destination classification still applies to
   every resolved address, and ad hoc fetch grants name one exact admitted
   origin rather than a glob.
2. **Unavailable or malformed `robots.txt`: A.** Durable crawling fails closed.
   One explicit operator-requested snapshot may proceed only when source policy
   declares robots inapplicable or the operator controls the origin; it never
   creates crawl authority.
3. **Canonical extracted representation: A.** The canonical value is structured
   JSON blocks plus a deterministic plain-text projection. Markdown is an
   optional derived artifact.
4. **Raw HTML retention: A.** Raw bodies are not retained by default. Durable
   state keeps digests and bounded metadata; Artifact Delivery retention must be
   enabled explicitly per source or grant.
5. **Browser rendering boundary: A.** JavaScript rendering remains in the
   `sensorium-web` connector family but uses a distinct
   `sensorium-web-browser.v1` backend, action set, and policy profile.
6. **Authenticated-source timing: A.** Authentication follows static public-web
   acceptance as a separate credential-bound profile with host-owned secret use
   and no credential or cookie exposure to consumers.
7. **Crawling ownership: B.** Crawling is defined and implemented as Phase 2 of
   P084. P084-011 owns its frontier and politeness contracts; no separate
   proposal is required.
8. **Consumer-visible link data: A.** A snapshot may carry a canonical
   destination URL without user-info, fragment, or query parameters plus bounded relation and text
   metadata. Links are inert and are never followed automatically.

## Open Questions

None. Decisions 1-8 freeze the current static V1 boundaries and ownership of the
deferred browser, authenticated-source, and crawl profiles. New questions found
while specifying Phase 2 must be recorded here before their contract is frozen.

## Static acceptance closeout (2026-09-09)

The initial carrier-only closure was too broad: it had not exercised secret
canaries or full store capacity. The combined closeout now passes recognizable
header/cookie/signed-query and in-main link canaries through real direct-peer
and Room carriers, including retained artifacts and every persisted record.
It also passes full-capacity load, eight controlled SIGKILL barriers, real HTTP
body failures/overload, BDO recovery, OS isolation and the additional randomseed
article run. The stronger fixture exposed link-query leakage and led to the
explicit 1.2.0 profile and migration boundary above. All 14 extraction-error
enum members are executed by a schema-derived gate.

The reviewed aggregate is `node:docs/evidence/sensorium-web/SENSORIUM-WEB-STATIC-ACCEPTANCE-EVIDENCE.md`.
Solutions 030/046, the Node ledger and readiness projection are synchronized.
P084-001 through P084-009 are done for this static macOS acceptance scope;
P084-010/011/013 remain deferred; P084-012 is partial with completed local intake (012a), explicit local review/draft (012b) and operator review UI (012c). This is not full browser, crawl,
credential-bound, multi-host or non-macOS deployment acceptance.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Work item | Status | Acceptance boundary |
|---|---|---|---|
| P084-001 | Freeze architecture, static V1 scope, source identity, authority split, named invariants, and profile ownership decisions | done | Decisions 1-8 freeze static admission and representation plus the boundaries of deferred robots, browser, credential-bound, and crawl work. |
| P084-002 | Define the twenty-schema V1 contract family, typed errors, positive/negative fixtures, and Schema Gate registration | done | Eight reusable host schemas and twelve P084 domain schemas are closed, mirrored, Schema Gate-tested, and semantically checked for source/profile/fetch bindings, artifact ref/digest binding, representation counts, relation uniqueness, durable schedule bounds, generation fencing, operator redaction, latest-state digests, claim/timeout bindings, bounded sweep outcomes, and caller-bound Artifact Delivery retention receipts. |
| P084-003 | Implement pure URL, destination, budget, generation, digest, and failure semantics in `bounded-http-fetch-core` and `sensorium-web-core` | done | Pure Rust tests cover URL/origin canonicalization, bounded label globs, literal-IP policy including wildcard IPv6 refusal, bracket-normalized IPv6 hosts, IPv4-compatible and mapped IPv6, standard and local-use NAT64 classification, limit intersection, the closed static media-type gate, cross-runtime frozen extraction-profile `1.2.1` identity including deterministic parser-event and nesting-depth limits, bounded inert document blocks with unique relation tokens, generation replacement, snapshot fencing, retry classification, and exact canonical source-envelope round-trip. Durable source-state semantics are completed under P084-006 rather than duplicated in the pure cores. |
| P084-004 | Implement the daemon-owned reusable bounded HTTP(S) fetch host capability, with P084 as its first admitted consumer | done | Exact caller/action/origin admission including explicit missing-caller refusal, internally timed DNS resolution, bounded workers and queue backpressure, a 64-address answer cap, all-address classification, fresh per-hop connection pinning with explicit rustls/WebPKI TLS and once-parsed roots, exact redirect-status handling, independent 64-header and byte caps, compressed/decompressed caps, per-hop plus total deadlines, global/per-origin concurrency, inline or content-bound Artifact Delivery handoff with recency-aware bounded transfer retention, exact caller/action isolation, and exact bounded eviction tombstones that distinguish `artifact-transfer-expired` from binding mismatch, metadata-only terminal trace, aggregate snapshot, daemon ingress/egress integration, no-socket-return conformance, and the P084-006 durable operator projection are implemented. |
| P084-005 | Implement the supervised Python static extraction connector without ambient egress | done | The channel-only `sensorium-web` module consumes only daemon-fetched schema-gated values, revalidates inline and content-bound artifact bytes, applies the frozen stdlib profile, and produces bounded inert blocks. macOS Seatbelt permits only the exact host-created loopback middleware endpoint; portable harness tests and automated macOS deployment evidence prove exact-channel success plus refusal of another loopback port, DNS, proxy, and subprocess paths. Unsupported host adapters fail closed. |
| P084-006 | Add durable source configuration, metadata-first cache, conditional refresh, scheduler, BDO, restart, and operator inspection | done | SQLite WAL state content-binds idempotent source updates, fences replacements, caps sources, generations, operations, and snapshots, retains metadata before bodies, and resolves interrupted work to `unknown`. Exact `304` reuse requires retained generation, requested/final URL, profile, fetch-result, and body evidence. Replay Scheduler launches a bounded batch of at most 16 due sources per tick, narrowed by `max_records`, the remaining deadline, and worker capacity. Each claim's 1-120000 ms timeout is schema-gated, retained in the private P055 continuation, and applied to the actual connector invocation; every post-claim refusal is compensated with structured failure diagnostics. Cancellation remains fenced before every external effect and commit. Restart recovery runs synchronously after connector readiness and before scheduler startup, traverses owned BDOs once by stable keyset pages, and is marked recovered only after the full pass succeeds. Shutdown never blocks on a full queue or an unbounded join. Connector absence and source launch-rate exhaustion remain distinct typed scheduler diagnostics. Direct refresh remains capped at 20 seconds. Pause/resume/run-now, launch budgets, bounded backoff, and schema-gated operator inspection remain source-owned. |
| P084-007 | Integrate Sensorium observation admission, P081 causal context, classification, operational context, and Artifact Delivery | done | Changed documents are submitted through `sensorium.observe.submit` with classification, required operational context, source and generation refs, fetch and extraction digests, and P081 causal context. Explicit representation retention invokes authenticated `artifact.delivery.retain`, stores only the immutable artifact ref in the source snapshot, omits representation bytes from the observation envelope and SQLite cache evidence, and chains the Artifact Delivery receipt into the Sensorium observation receipt. Refresh status retains a bounded redacted receipt-ref chain plus closed failure code, phase, and retry class; raw-body artifact refs remain opt-in. |
| P084-008 | Register the P082 `latest-state` source-provider adapter and local/remote interface acceptance | done | The optional `sensorium-web-latest-state` adapter registers only when the connector is configured, schema-gates the daemon/module boundary, rechecks source, generation, and canonical snapshot digest, emits latest-state cursors, coalesces unchanged reads, and rejects stale generations. It exposes no refresh operation, so P082 read/subscribe cannot acquire fetch authority. Real macOS local read/SSE acceptance now covers admitted snapshot and digest binding, no-change coalescing, changed content, grant revocation, typed generation fencing, and explicit supersession with fresh authority; exact host/fixture counters prove no consumer fetch. Dedicated macOS acceptance also verifies real authenticated TLS peer read/subscription and Room projection, exact and dual authority, revocation, generation fencing, explicit supersession, and remote-refresh refusal; 4/4/8 operator/host/HTTP-hop counters prove zero consumer acquisition. Secret canaries include signed redirects and an extracted in-main link; zero leakage is asserted in carrier/operator values, 100 files, 31 databases, 274 rows and two real retained artifacts on profile 1.2.0. Evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REMOTE-INTERFACE-EVIDENCE.md` and `node:docs/evidence/sensorium-web/SENSORIUM-WEB-STATIC-ACCEPTANCE-EVIDENCE.md`. |
| P084-009 | Add static-profile conformance, load, refusal, and end-to-end evidence; synchronize Solution 030/046, Node ledgers, trackers, and readiness | done | The reviewed aggregate `node:docs/evidence/sensorium-web/SENSORIUM-WEB-STATIC-ACCEPTANCE-EVIDENCE.md` combines real local SSE/direct-peer/Room and retained-artifact canaries, 31 service tests, 13 conformance checks including all 14 extraction errors, the Schema Gate family/boundary matrix, 83 daemon regressions, real OS no-egress and 24 host tests. Deterministic capacity reaches 1,024 sources, 4,096 generations/operations and 1,024 snapshots across 5,120 refreshes; 128 interrupted claims and eight SIGKILL barriers recover without automatic effects. Real truncated/stalled bodies reject excess calls and release capacity. Randomseed is a separate successful live probe. Solutions 030/046, Node ledger and readiness are synchronized; deferred extensions and platform/evidence limits remain explicit. |
| P084-010 | Add `sensorium-web-browser.v1` isolated JavaScript rendering profile | deferred | Requires a separately accepted browser process, host-controlled egress, empty profile, resource caps, no credentials/shares, rendered snapshot contracts, and deployment evidence. |
| P084-011 | Define and implement P084 Phase 2 `sensorium-web-crawl.v1` frontier and politeness profile | deferred | After static-profile acceptance, P084 must freeze frontier lifecycle, fail-closed robots behavior, depth/page/origin budgets, restart, cancellation, retention, and operator evidence before implementation is accepted. |
| P084-012 | Integrate explicitly configured P084 snapshots as an optional P078 Harvester source | partial | Harvester receives only admitted snapshot/artifact refs and cannot widen fetch, crawl, finding-publication, or Whisper authority. |
| P084-012a | Admitted web snapshot to local Harvester review | done | Immutable source binding; independent P082 read authority; bounded retained-artifact verification; reference-only classified pending review; durable dedup; no acquisition or publication. |
| P084-012b | Explicit web finding redaction to optional local Whisper draft | done | Immutable digest-bound operator decision, explicit draft intent, atomic fact/projection persistence; deterministic daemon HTTP/restart, refusal and canary acceptance recorded in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEWED-DRAFT-EVIDENCE.md`. Broader integration remains partial. |
| P084-012c | Operator UI over admitted web finding review | done | Bounded operator queue, explicit redaction/draft forms, auth/CSRF, safe failures, real UI/daemon replay/restart, zero extra acquisition/delivery and no escaped canaries; evidence in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEW-UI-EVIDENCE.md`. |
| P084-013 | Define and implement the separate credential-bound authenticated-source profile | deferred | Starts only after static public-web acceptance; host-owned secret use is fail-closed and no credential, cookie, authenticated handle, or secret-bearing diagnostic reaches consumer-visible or durable evidence. |
| P084-014 | Retain exact original web bodies under an explicit finite custody contract | in-progress | Freeze and implement [original custody](#web-original-custody) using existing fetch bytes, AD retain/owner lifecycle, P081 receipts, S028 facts and P091 policy. Cover inline and artifact paths, source-generation binding, original/representation claim ordering, finite horizons and shared-reference-safe release. No new blob store; no promotion from a transient transfer ref. |
| P084-015 | Qualify original custody and Harvester handoff offline | in-progress | Depends on P084-014 and P078-015. Run the byte, quota, expiry, sharing, lost-reply/restart and missing-original cases in the existing Sensorium Web/Harvester harness; prove zero implicit refetch and zero raw-body/secret leakage to drafts or public views. Record separate current evidence and update owning Solutions/Node ledger at implementation closeout; historical 012a/b/c qualifications remain unchanged. |

### Single-URL operator acceptance (2026-09-08)

`node:tools/acceptance/sensorium-web-url/` closes a bounded operator experiment
within P084-009. The macOS live run fetched the explicitly selected
`https://randomseed.io/txt/ai-and-consciousness/` through the real daemon and
supervised connector: HTTP 200, 82,172 body bytes, 39,148 extracted characters,
164 blocks, 29 inert links, no truncation, one host fetch, an admitted observation
receipt reference, and graceful process cleanup. A separate mismatched-origin
run proved `OriginDenied`, no output document, and graceful cleanup. Evidence is
retained in `node:docs/evidence/sensorium-web/SENSORIUM-WEB-URL-EVIDENCE.md`.
A subsequent review-closure run also verified both `all` and `internal-loopback`
OpenAPI projections, the documentation shell, and module health/readiness before
fetching, after correcting response bindings and shared launch-environment order.

The runner reads the admitted inline representation through
`sensorium.observation.get`; separate representation Artifact Delivery retention
is disabled for this experiment. Its offline mode uses the real connector and
SQLite source store with explicit host fetch/admission doubles. On its own, this historical experiment does not establish carrier redaction
or capacity; the combined 2026-09-09 closeout above supplies those gates.

### Local P082 read/SSE acceptance (2026-09-08)

`node:tools/acceptance/sensorium-web-local-interface/` closes the local part of
P084-008 using the real daemon, bounded fetch host, supervised no-egress static
connector, SQLite source store, observation admission, and authenticated P082
HTTP/SSE routes. A deterministic local HTTP fixture uses a test-only resolver
and loopback destination admission. The daemon release integration exposes no
fixture injection switch; the reusable fetch library still has a public custom-policy
constructor, and no lint fences other callers.
The test checks initial payload/digest binding, no-change, changed content,
revocation, typed stale-generation refusal, stream closure, and explicit
supersession with a fresh grant. Four explicit operator refreshes account for
all four host fetch attempts and fixture requests; consumer read/subscribe adds
none. The daemon and isolated data are cleaned up.

This evidence exposed and corrected runtime Schema Gate boundary selections,
P084 receipt references narrower than the P081 identifier contract, inconsistent
authenticated module actor refs across HTTP/SSE, and loss of terminal generation
errors after broker failure. The measured run, 60 P082 regression tests, and two
focused Schema Gate tests are retained in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-LOCAL-INTERFACE-EVIDENCE.md`. The final combined
2026-09-09 run re-executed local and remote acceptance on profile 1.2.0; the
aggregate closeout supplies redaction, load and crash evidence for P084-008/009.

### Remote P082 acceptance and review closure (2026-09-09)

`node:tools/acceptance/sensorium-web-remote-interface/` closes P084-008 using the
same real static connector, bounded fetch host, durable source store and admitted
Sensorium snapshot. Signed interface Passports authorize read/subscription over
an actual daemon TLS/WebSocket peer session. A real loopback Room WebSocket
projection requires both admitted Room observe authority and a current interface
grant. The Room fixture supplies membership facts directly; it is not remote
membership issuance, TLS Room deployment or federated relay evidence.

The scenario verifies unchanged/changed snapshots and digest binding, exact
Passport target/resource scopes, both sides of Room authority, grant revocation,
stale-generation refusal, explicit supersession with fresh authority, and remote
refresh refusal on both carriers. The strengthened canary scenario uses real
representation retention and signed redirects: four explicit refreshes account
for four host calls and eight HTTP hops. Zero markers escaped into 100 files,
31 databases, 274 rows or two retained artifacts. The final combined daemon run
passed 83 tests in 45.19 seconds, including local and remote acceptance. The
measured boundary and regressions are retained in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-REMOTE-INTERFACE-EVIDENCE.md`.

Review corrected the Schema Gate registry rather than relabeling transport reads
as file imports: every module response is admitted at receiver-relative `Ingress`.
The P084 family/boundary matrix and six declared response routes now execute their
validators against positive and malformed fixtures. Test cleanup cannot turn a
worker panic into a second panic during unwind; terminal SSE batches may close
without an extra terminal event. Raw legacy P082 actors are not aliased into
canonical identities: operators inspect and reissue authority where needed,
without assuming all deployed state was empty. P068 separately tracks transitive
OpenAPI schema bundling; top-level URN resolution alone does not close that debt.

### Finite capture integration checkpoint (2026-11-04)

The new opt-in source contract is `sensorium-web-durable-source.v2`, selecting
`finite-originals.v1` with both original and representation retention. The host
separately resolves the complete P091 adoption. Fetch v2 always keeps decompressed,
pre-decoding originals in AD, even below the former inline threshold. An exact
owner/session/action/content binding admits repeatable bounded extraction pages;
a different single-use binding supplies explicit retain v2. Neither binding is a
receipt or publication grant.

Retain v2 commits the claim, transfer consumption, original owner-observed
execution receipt and idempotency result together. The source's existing refresh
journal records each committed owner result before exposing
`sensorium-web-document-snapshot.v2`. Its stable snapshot id precedes receipts;
the final snapshot digest covers both claim bindings and the receipt chain.
Partial custody never creates a ready handoff. A bound 304 reuses the original
snapshot and horizons without payload read or retain; a new explicit 200
observation creates a new snapshot even if bytes repeat. Restart does not fetch.

The common current-owner/session resolver is retained. Bundled Sensorium obtains
a distribution-owned pin of its exact launch declaration and bounded first-party
sources, with current eligibility checks; it does not impersonate an independent
signed package. HTTP credentials cannot manufacture this admission. The new registry mode `host-configured-live-session` selects a separate current
caller proof for the three custody ports. The old signed-package target remains
unchanged; the new proof cannot authorize launch, scheduling or signing, and a
failed package guard has no configuration fallback. The latest
API has an explicit offline-bundled version union, and P082 descriptors select the
exact snapshot contract. This checkpoint is integration in progress, not shared
Harvester review, v3 publication, A/B qualification or production adoption.


### Common review and protected publication checkpoint (2026-11-05)

Current implementation resolves snapshot v2 into the common Harvester review,
with immutable material digests, explicit revision CAS and a local draft v2.
The queue exposes current claim generations and nearest custody deadlines. An
explicit extension commits the full claim set and receipt together; changed
terms require another review. A separate classified read admits original bytes
as inert bounded file pages, never rendered source HTML. No action implicitly
fetches or renews custody.

Protected preview/sign v2 resolve the approved draft at the host. Preview refuses
insufficient custody instead of disclosing its deadline through document expiry.
Sign rechecks after key unlock and atomically obtains the mixed-material holds.
First publication checks existing exact review/holds through a current live
channel; no AD prepared token crosses a module boundary. Public-gossip v2
preserves minimized admitted origin lineage, including legacy absence, through
the existing promotion projection. It remains an explicit unpublished candidate.

Component and process regression results remain distinct from the freshly pinned
full fixture qualification, which is still open on SQLite and unmodified Synapse.
This checkpoint does not renew the historical 012a/b/c reports or close P084.

A later scoped component preflight on 2026-11-05 verified all 64 selected named Rust
assertions and 96 mirrored contract pairs: 333 Rust tests and eleven named
schema-sync tests passed; two unselected manual fixtures were not executed.
Ordinary local preparation also verified five distinct nodes/four protected
participants and restart/unlock controls. Actual local fetch, independently
authorized mixed review/replay and a supplementary ordinary-network randomseed
capture remain bounded observations, with their earlier harness/availability
refusals preserved. The Node record is
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-COMPONENT-PREFLIGHT-20261105.md`.
Neither component conformance nor fixture preparation supplies fresh complete
A/B, native APFS/ENOSPC, window-end publication or rollout qualification.
P084-014/015 remain in progress. At that checkpoint the complete new campaign
matrix/qualifier was still open. These measured results do not change the
accepted contract or the production-adoption conditions.


### Composed review and independent campaign inventory (2026-11-05)

A separate APFS-image-independent continuation now qualifies one deterministic
fetch, two finite claims, independent read grant/revocation/regrant, mixed
web/document review and actual restart with exact replay and no refetch. This
ends at an unpublished local draft. The separately adopted P084 v3 campaign
reader freezes 131 mandatory obligations, freshly verifies seven composed and
six component obligations, and explicitly leaves 118 missing. Ordinary and
optimized inspection agree. Missing signed/native/carrier cases still block the
full milestone; additional runtime predicates remain owned work rather than
claims inferred from component tests. No production adoption or historical
qualification is renewed. P084-014/015 remain in progress. Source pins, original
refusals, retention review and measured limits live in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-COMPOSED-REVIEW-20261105.md`.

## Next Actions

1. Reproduce the static acceptance gates when changing the profile, host boundary,
   retention or carriers. Migrate old configurations through an explicit new
   source generation; never relabel retained profile evidence.
2. Evaluate any alternate extraction profile against the same checked-in corpus
   under its own version and digest.
3. Keep browser rendering, credentials and Phase 2 crawling in their separately
   accepted deferred workstreams; broader P078 integration remains partial. Static acceptance does not
   grant their authority or provide their deployment evidence.

## External Standards and Implementation References

- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html)
- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Playwright supported languages](https://playwright.dev/docs/languages)
- [Trafilatura documentation](https://trafilatura.readthedocs.io/en/stable/index.html)
- [Reqwest `ClientBuilder`](https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html)

### Inactive owner restart guard (2026-11-05)

Turning off adoption stops new retain, extension and holds. It does not detach
previously recorded custody, remove managed read fences, alter granted terms,
clear legacy interests or suspend expiry enforcement. AD selects reattachment
from durable owner history independently of the current opt-in flag. A fresh
inactive store creates no owner. An owner identity marker without source history
is an explicit corruption/reconciliation refusal, never a reason to classify
its payload as legacy. This guard changes no historical evidence or production
adoption; composed original/review/publication qualification remains open.

### Native AD I/O prerequisite (2026-11-06)

A fresh independently qualified APFS run now covers actual owner payload ENOSPC
(errno 28), a killed process after payload publication but before claim commit,
and a distinct controlled SQLite commit abort (1811). Recovery preserves the
original intent, terms and payload, including lost-response replay. Original and
exact durable-copy reads agree in ordinary and optimized processes. Earlier
location/pressure refusals and rehearsal remain unqualified and unchanged.

This is the focused AD prerequisite, not the full P084 campaign. At that
standalone checkpoint its native-case adapter and fresh composition were still
required; the then-current complete-matrix result was 13/131 verified with 118
missing at its recorded revision.
P084-014/015 and the signed, remaining native, remote privacy and two-backend
qualification remain in progress. No production adoption follows. Exact pins,
private retention review and measured limits are in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-NATIVE-CUSTODY-20261106.md`.

### Native composition and expiry-before-review checkpoint (2026-11-06)

A fresh independently qualified campaign now credits 18/131 mandatory
requirements and leaves 113 missing, with identical ordinary/optimized incomplete
results. The original three native AD cases are explicitly adopted across a
reviewed tooling/documentation-only source bridge; their original revisions and
scope remain visible. Fresh same-source review/component captures are joined by
actual-clock expiry before review and explicit new observation/review acceptance.

The expired pending finding has no decision/draft and remains unpublishable
across restart without another fetch. Only a new source generation, explicit P082
source-slot supersession, fresh grant/claims and new review permit continuation.
This uses a five-second fixture policy without changing factory 24-hour identity
or terms. P084-014/015 remain in progress; signed Gate A/B, remaining fault/load
and new-profile carrier privacy cases are still missing. No production adoption
or historical evidence renewal follows. Exact source/reader pins, paired controls
and scoped retention review are in
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-EXPIRY-CAMPAIGN-20261106.md`.

### Issuer authority continuation (2026-11-06)

Strict encrypted-media and native provider checks are prerequisites, not Gate
A/B. Three separately approved one-shot attempts respectively missed the fixed
start cutoff, refused an unadmitted AD outbound scope, and reached full request
v2 before D refused consent. No terminal certificate, decision export or signed
Whisper was observed. The corrected shared path requires a separately
root-approved `nym-bootstrap-consent-v2`; original signed v1 grants retain their
four-family scope. Component/schema tests cover the separation, while a new
ordinary exchange and the signed two-backend campaign remain open.

The earlier 18/131 result retains its historical source pins. New runtime/schema
bytes require fresh native/source campaign admission, not an implicit bridge or
repin. Existing P084-014/015 and P078-015/016 status stays in progress; no
production adoption follows. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ISSUER-AUTHORITY-20261106.md`.

### First ordinary v3 certificate checkpoint (2026-11-06)

A fresh ordinary encrypted-owner fixture has issued a v3 certificate over all
four exact TLS/AD phases using separately signed bootstrap-v2 authority.
Independent native inspection verifies `A/issue` and `A/reference-readback`.
Together with fresh same-source R/C/W7/native inputs, the campaign is now
20/131 verified with 111 missing; ordinary/optimized results agree. Original
reports/refusals remain preserved, with process inventory added only in a
separately bound derived view. No Whisper was signed or published.

A separate 128 MiB capacity observation stopped after 2479 retains with an
untyped host cause; a complete DB/WAL copy passes integrity checks. It grants
no load/recovery credit. Full signed SQLite/Synapse, all-producer window-end,
recipient/privacy and remaining load/fault qualification remains open. Existing
P084/P078 and dependent owner trackers stay in progress. This does not adopt
production or renew historical evidence. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-FIRST-ISSUANCE-20261106.md`.

### Local reviewed-v3 producer preparation (2026-11-06)

The current UI fixture selects the applicant's local review/custody owner for
first v3 publication; receiving C remains a separate carrier/admission claim.
The inspector rejects a remote-owner process topology. Inline v2 keeps its
historical topology. Three actual applicants retain mixed reviews after exactly
three explicit controlled fetches and paused schedules. A separate 4096-claim
saturation/reopen observation is not campaign load qualification. None of this
adds to the source-bound 20/131 checkpoint or completes signed Gate A/B. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-LOCAL-PRODUCER-PREPARATION-20261106.md`.

### Ordinary UI continuation refusal (2026-11-06)

A later approved SQLite series issued A's v3 certificate and retained its two
exact recovery exports, then stopped on a capture-tool `UnboundLocalError` after
the first UI form. B/A2 did not start and no Whisper was signed or published.
Node corrected the local name shadowing and added complete doubled v2/v3 UI
orchestration regressions on both backends; 516 Python and 21 optimized UI tests
pass. The original runtime refusal remains preserved and adds no campaign credit.
Fresh corrected-source UI, common receiver and full A/B qualification remain open.
See `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ORDINARY-UI-REFUSAL-20261106.md`.


### Scoped ordinary SQLite publication and stopped series (2026-11-06)

The next clean-source fixture completed A through AD certification, reviewed UI,
restart/locked-sign refusal, protected v3 signing and a signed SQLite publication
receipt/public readback. Independent inspection credits four exact requirements.
The source-bound aggregate is 16/131 with 115 missing; its fresh C domain command
failed and earns no six-row credit. B arrived before request expiry but was
refused during later owner validation; A2 did not start. The once-selected series
stopped without retry or deadline extension. Historical 18/131 and 20/131 reports
retain their distinct source bindings. Full A/B, shared receiver, Matrix, remote
privacy and remaining window/load/fault qualification stay open.

A deterministic provider-lock regression separately demonstrates an incidental
descriptor prolonging a dropped owner. Explicit RAII unlock preserves replacement
exclusion; fresh clean-source qualification is required after this Rust change.
This does not establish the unique cause of the original parallel C failure.
See `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-SQLITE-PUBLICATION-20261106.md`
for exact inputs, original refusals, canary scope and retained-evidence boundaries.


### Two verified local publishers; replica recipe correction (2026-11-06)

The next source-bound fixture independently verifies A and B through actual
reviewed v3 signing, local SQLite publication and signed receipts. Fresh component,
review, expiry and native AD inputs plus four distinct runtime predicates yield
22/131 verified, 109 missing. Both publishers satisfy the same four predicates;
credit is not doubled. A2's second `issue` for participant A receives typed
`policy-denied` and stops the series before decision export. A positive replica
must use `renew` bound to A's verified predecessor in the same profile/context.
An ended profile window cannot be extended or replaced while retaining context.

A separately versioned one-based epoch selector corrects the read adapter from
pinned profile/window law. The original refusal and all runtime bytes remain
unchanged; same-certificate negative/positive isolation confirms the selector.
No threshold, common receiver, replica-renewal, Matrix, full A/B or production
claim follows. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-TWO-PUBLISHERS-20261106.md`.


### Independent reviewed-v3 Matrix receiver preparation (2026-11-06)

Owned Synapse preparation observes healthy admitted A/B producer instances and a
separate C receiver, with existing local instances and signer defaults preserved.
It performs no certification, recovery export or Whisper publication. The shared
first-pair reader now binds each reviewed-v3 producer's custody/publication
process independently of the original C/D projection continuation. Both producers
must use the same issuer D; C must differ from each producer and from D. Inline
v2 bindings and all native complete-basis, first-pair, public-readback and expiry
requirements remain unchanged. Mixed-version and substitution tests do not award
runtime credit. Matrix, common-receiver/threshold and full A/B qualification stay
open; the preceding source-bound two-publisher report is unchanged.


### First reviewed Matrix publication and status-cache withdrawal (2026-11-06)

The source-bound Sensorium fixture independently verifies A's private AD
certificate, reviewed protected v3 UI signing and Matrix HTTP 202/public readback.
Its separately pinned campaign reaches 21/131, with 110 missing and identical
ordinary/optimized results. B fails startup before export: status-cache compaction
requires a formerly adopted profile absent from current configuration. C is
reaped; no common-receiver, threshold, complete-PDU or full A/B credit follows.
The earlier SQLite 22/131 retains its separate source and result.

The owner correction validates retained canonical bytes, digest and source links
before withholding unadopted status. It preserves facts and existing budgets,
refuses current use without adoption and restores signature/cursor verification
only on exact readoption. Other adopted profiles can operate and missing
projections can rebuild; corruption remains a refusal. Component regressions
pass and the next v3 conformance selection requires both withdrawal/corruption
assertions. Fresh current-source native/runtime and Matrix qualification remain
open; no historical gate or production adoption is renewed. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-FIRST-MATRIX-PUBLICATION-20261106.md`
and `node:daemon/docs/CONTEXTUAL-NYM-CERTIFICATION.md`.


### Scoped reviewed-v3 Matrix first pair (2026-11-07)

A/B ordinary reviewed v3 publication, independent C/D S020 first pair and
post-expiry evaluation now have original-source qualification, including separate
read-only `/sync` and all four complete room-v10 PDUs. Two copies of one 507-byte
fixture article count two participant sources without a corroboration assertion.
Five canaries are absent from the selected public/native corpus; complete gossip
and P082 direct-peer/Room privacy are not inferred. P084-014/015 remain in progress.

The independently composed campaign verifies **25/131**, with **106 missing**,
and identical ordinary/optimized incomplete results. Runtime/capture Node
`985964ee83` / Orbidocs `2b5ea4fd` and corrected reader Node `d83a9a0f` remain
separately pinned. Both original reader refusals and every source observation are
preserved; no certification/publication retry, production adoption or historical
gate renewal follows. Current implementation evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-MATRIX-FIRST-PAIR-20261107.md`.

### Later 2026-11-07 fixture replica/window checkpoint

The source-bound campaign now verifies **29/131**, with **102 missing**, identically
in ordinary and optimized readers. Exact-predecessor A2 renewal on a distinct
registered node of A's participant retains one source and no first emission at
independent C. A newly started C reads the same signed records after the single
aligned window ends. Runtime `985964ee83` / `2b5ea4fd`, capture `845bf6f7` /
`ca9b73c9` and window reader `fb4301fb` remain separate pins. Earlier source-bound
reports and the original four-PDU scope remain unchanged.

This adds two replica/source-count and two window/history obligations. It does
not qualify certificate-at-boundary, all-producer end refusal, old-node v2 cutoff,
complete public/P082 direct-peer/Room/gossip privacy or full Gate A/B. Production
is not adopted. The remaining fixture matrix and existing parent trackers stay
open; another profile digest does not automatically preserve source continuity.
Current implementation evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-REPLICA-WINDOW-20261107.md`.

### Later 2026-11-07 SQLite/late-receipt checkpoint

The SQLite/late-receipt fixture checkpoint verifies **32/131**, with **99 missing**,
identically in ordinary and optimized readers. One reviewed Harvester v3 owner
completed protected UI preview/sign across restart, SQLite publication (201) and
a signed receipt. A new SDK receiving store first admitted the exact original
author bytes/receipt after certificate expiry plus skew, using the real clock,
and retained its facts across close/reopen. This is not an HTTP import, common
SQLite threshold/room proof, second publication or full Gate A/B.

Runtime `985964ee83` / `2b5ea4fd`, capture `fe7c595e` / `65a4b8a3`, receiver
build `2995a9f7` and final reader `ba4a235b` stay separate. All previous29
original predicates reverify. The earlier wrong-backend runtime refusal,
unattempted late SDK, incomplete reader and empty-stderr campaign refusal remain
preserved; corrections use new cases or read-only views, without retrying an
uncertain publication. Backend readiness now precedes certification. The bounded
thirteen-root retention review leaves all217 exact-copy candidates blocked;
no retirement action or production adoption occurred. Parent trackers and the
remaining99 obligations stay open, including all-producer end refusal, boundary/
old-node-v2 cutoff and full P082/gossip privacy.

Current implementation evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-SQLITE-LATE-RECEIPT-20261107.md`.

### Native owner-policy checkpoint (2026-11-07)

The native policy checkpoint verifies **37/131**, with **94 missing**,
identically in ordinary and optimized readers, exit 2. All previous32 original
predicates reverify. Five native AD/P091 obligations add inactive/complete
adoption, editorial versus normative factory identity, separate ceiling refusal
and unchanged old claim terms. Eleven actual system-clock stages include restored
controls and owner reopen; three coherently rehashed scratch substitutions each
refuse and restore the original positive.

Native build `190552c41`, capture `a8933630` and final reader `714e0bc10` remain
separate from existing runtime `985964ee83` / normative `2b5ea4fd`. Original
rehearsals, cold-WAL collector refusal and hold-field reader refusal remain
preserved; the successful runtime was not repeated for reader correction.
Full gates and production adoption remain open, and parent statuses are unchanged.

The 24-hour default is exercised on a synthetic native retain; this does not
close the separately required fetch-to-retain horizon or P082 privacy rows.
Policy checkpoint evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-POLICY-20261107.md`.

### Native claim and transfer checkpoint (2026-11-07)

The native claim checkpoint verifies **41/131**, with **90 missing**, identically
in ordinary and optimized readers (incomplete, exit 2). All previous37 original
predicates reverify. Four native AD obligations add same-key parameter conflict,
overlapping concurrent retain and lost-response reopen/retry, atomic transfer/
claim/first-result commit, and explicit live extension with real expiry controls.
Four coherently rehashed scratch substitutions each refuse with a restored
original positive. The native build/capture `069e95bbd` and corrected reader
`b7d0d6fc8` stay separate from unchanged runtime `985964ee83` / normative
`2b5ea4fd`; the original reader expiry-model refusal remains preserved.

The transfer is owned and committed by AD. This does not close HTTP
fetch-to-retain, source scheduling or the 24-hour fetch horizon.
Full gates and production adoption remain open; parent statuses are unchanged.
Claim checkpoint evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-CLAIMS-20261107.md`.

### Native legacy checkpoint (2026-11-07)

The native legacy checkpoint verified **43/131**, with **88 missing**,
identically in ordinary and optimized readers (incomplete, exit 2). All previous41
predicates reverify. Two native AD rows add digest collision/monotonic interest
through ordinary release, actual expiry/sweep and unadopted reopen, plus explicit
native operator-method release with a withdrawn admission witness. Same-object,
managed-only GC and healthy controls establish the causes; four rehashed scratch
substitutions each refuse and restore the original. Native build/capture/reader
`6fcf49a3d` / `35c23a9c` remains separate from runtime `985964ee83` / normative
`2b5ea4fd`. Both pre-effect preparation refusals remain preserved.

No HTTP observation, fetch horizon or source-journal/304 qualification is
inferred from the synthetic legacy object.
Full gates and production remain open; parent statuses are unchanged.
Legacy checkpoint evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-LEGACY-20261107.md`.

### Original bytes and explicit revalidation checkpoint (2026-11-07)

At this original-byte checkpoint the campaign verified **48/131**, with **83 missing**,
identically in ordinary and optimized readers (incomplete, exit 2). All previous 43
cases reverify. Five composed predicates cover exact original transfer/inline
representation custody, actual gzip and typed ISO-8859-2 refusal without handoff,
original-preserved extractor omissions, acquisition horizons and three explicit 304
through delayed review, restart and replay. Two owners are reaped; no unsolicited
fetch or renewed claim occurs. Six coherently rehashed controls per mode each
refuse then restore original positives. 73 Python tests per mode pass.

Capture `dade45982` and corrected reader `945a2bf9c` / Orbidocs `e37021ad` remain
separate from the pinned runtime `985964ee83` / normative `2b5ea4fd`. The original
capture runs once; three reader precondition refusals remain preserved. No
production Rust, schema or capability contract changed. Ten-root catalog/dry-run
review records 158 selected files/6264441 bytes, seven exact duplicate-output
candidates 1767461 bytes and zero eligible. Active 48 evidence/authority remains
protected; no retained deletion/move/retirement authorization/execution occurred.

The current 512 KiB static cap is unchanged; a 384 KiB omission payload cannot satisfy the separate >2 MiB original obligation. Raw charset refusal is not an admitted handoff.
Full gates and production remain open; parent statuses are unchanged.
Original-byte checkpoint evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ORIGINAL-BYTES-20261107.md`.

### Finding origin and adopted monitoring checkpoint (2026-11-07)

The original-input campaign verifies **51/131**, with **80 missing**, identically
in ordinary and optimized readers (incomplete, exit 2). All previous 48 cases
reverify. Three new rows cover all nine canonical finding-class mappings,
non-web Sensorium/mixed material, and collection bound to an adopted configuration
after its real 60-second interval. Thirteen immutable reviews replay across an
actual owner restart, with two web snapshots and four exact custody refs.
Scalar metadata cannot create web, monitoring or model lineage. These synthetic
operator-inline finding classes imply no mail/filesystem/device acquisition or
signed author-class reception. Scheduler is disabled; due execution is explicit.

Collector/reader `bfb0d90b0` / Orbidocs `f2abbe21` remain separate from runtime
`985964ee83` / normative `2b5ea4fd`. Six coherently rehashed controls per mode
refuse, each followed by a restored-original positive; 82 Python tests per mode
pass. The original capture is unchanged and runs once. Six-root catalog/dry-run
review records 138 selected files/4863454 bytes, three duplicate-output candidates
1294585 bytes and zero eligible. Active qualification and authority dependencies
remain protected; no retained deletion/move/retirement authorization/execution.
These numbers are run observations, not contract thresholds.

Full processing/inference provenance, signed v2 absence versus v3 unknown,
author-class reception, mixed authorship holds, clock/load/fault, all-producer
window/cutoff, P082/gossip privacy and full two-backend gates remain open. Parent
statuses and production adoption are unchanged.
Current measured evidence: `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ORIGIN-MONITORING-20261107.md`.

### Participant observation integration tracker — 2026-11-06

These tasks expose existing admitted representations through P082; they do not
convert operator source management or the operator P084-012c review route into a
participant surface. Refresh/fetch, observation, finite custody, reviewed draft
handoff and publication remain separate decisions. The participant reviewed
handoff belongs to P078-017/018 and P013-PA-001/002; original custody remains
P084-014. A supported snapshot version must be selected explicitly on both sides.
P084-016 may freeze against accepted P082 delivery semantics in parallel with
P082-023; P084-017 checks the actual source/carrier contract pair at runtime.

| ID | Status | Dependencies | Deliverable and gate | Consumers (not prerequisites) |
|---|---|---|---|---|---|
| P084-016 | todo | P024-009; P084-006; P084-008; accepted P082 delivery and original-custody contracts | Freeze participant-safe Web source/snapshot/status DTOs: exact schema/profile, source generation, snapshot/representation identity, classification, retained availability/deadline and typed supersession/refusal. Separate not-started admission refusal from an existing terminal operation and HTTP transport status. No signed URL/query credential or host-private source metadata enters the UI contract. Pin current legacy and planned finite-original version mappings with unsupported-version refusal; a planned mapping grants no runtime support. | P084-017; optional P098-025 |
| P084-017 | todo | P084-016; P082-024; P084-008 | Deliver participant-authorized read-only snapshot/status mapping for explicitly supported existing representation profiles. Recheck exact source generation before cache/availability fallback; no GET, lease reconnect or expired material causes fetch/retain/publication. Prove current source/profile/custody refusals, no acquisition counters changed and private-source canaries absent. Finite-original-backed promotion additionally needs P084-014 and P078-018; ordinary admitted observation does not wait for those paths. | P098-025 |
