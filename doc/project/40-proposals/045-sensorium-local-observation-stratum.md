# Proposal 045: Sensorium as a Local Observation Stratum

Based on:
- `doc/normative/20-vision/en/VISION.en.md`
- `doc/normative/40-constitution/en/CONSTITUTION.en.md`
- `doc/normative/50-constitutional-ops/en/AUTONOMY-LEVELS.en.md`
- `doc/normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md`
- `doc/project/20-memos/orbiplex-monus.md`
- `doc/project/20-memos/emergency-signal-v1-invariants.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/022-monus-as-host-granted-local-observation-middleware.md`
- `doc/project/60-solutions/node.md`
- `doc/project/60-solutions/monus.md`

## Status

Draft

## Date

2026-04-18

## Executive Summary

Sensorium already appears in the Orbiplex corpus as the Node's layer of contact
with reality. The Vision describes it as the layer of adapters to the world:
public-network readers, environmental sensors, microphones, cameras, GPS,
weather, energy, safety signals, and other signal sources. The Constitution
defines it as the organ that provides signals grounding intelligence in reality
and limiting narrative or model drift.

Other documents already assume this role:

- emergency operations describe a `sensorium -> evaluation -> activation`
  pipeline,
- autonomy levels treat sensorium event logging and aggregation as routine
  bounded node activities,
- `emergency-signal.v1` accepts `source/type = sensorium`,
- Monus can consume Sensorium-derived summaries when preparing local concern
  drafts,
- Whisper preserves `monus-sensorium-derived` provenance when local observations
  materially shaped an outgoing social signal,
- story 009 treats Sensorium as connector access to external sources such as
  arXiv, GitHub repositories, mailing lists, and news feeds,
- the Node solution already allows a sensorium provider to attach as a
  Node-scoped role through explicit protocol and API contracts.

This proposal makes that implied layer explicit.

The core maxim is:

> Sensorium is not a grand connector specification. It is a thin stratum for
> local observations, where complexity lives in connectors and Sensorium
> normalizes only the minimal exchange contract.

Sensorium should therefore be implemented first as a supervised local module or
Node-attached component in the spirit of proposal 019. It should expose boring,
bounded host-granted capabilities for observation submission, query, summary,
status, and audit. It should not become a universal ontology of the outside
world, a transport authority, a surveillance platform, or a replacement for
domain modules such as Monus, Whisper, Arca, or emergency evaluation.

## Problem

The system needs contact with external reality, but "connectors to the world" can
become an unbounded design sink. If every connector type forces a new global
protocol, Sensorium becomes too large before the Node can use it. If every
consumer speaks directly to each connector, Monus, Arca, emergency evaluation,
and future modules all acquire duplicated adapter logic and uneven policy
checks.

The design tension is:

- connectors are necessarily messy because the outside world is messy,
- consumers need stable local observations, not raw connector-specific chaos,
- the Node must retain consent, minimization, audit, and capability boundaries,
- the protocol core should not absorb every sensor, API, OS integration, or data
  feed shape.

Without a thin Sensorium stratum, the system is pulled toward one of two bad
forms:

1. a large `SENSORIUM-CONNECTOR-SPEC` that tries to standardize every possible
   connector class too early;
2. ad-hoc side channels where each module reads local files, shells out, calls
   external APIs, or watches devices under its own private policy.

Both forms complect connector mechanics with domain reasoning.

## Decision

Define Sensorium v1 as a **local observation stratum**:

- connectors own adaptation from concrete external systems into local
  observations,
- Sensorium owns admission, minimal normalization, local policy enforcement,
  traceability, and queryable read models,
- consumers such as Monus, Arca, emergency evaluation, and local agents consume
  host-granted Sensorium capabilities,
- network publication remains outside Sensorium and is handled by the appropriate
  protocol layer.

For the first implementation phase, Sensorium SHOULD be deployable as a
supervised Node-attached middleware module using the same operational style as
proposal 019. A later implementation MAY move part of Sensorium in-process if the
runtime needs tighter lifecycle coupling, lower latency, or direct access to
Node storage. That deployment choice must not change the data contract.

## Goals

- Keep Sensorium local-first and capability-bound.
- Put connector complexity at the edge, not in the core Sensorium contract.
- Provide a small common observation shape usable by multiple local consumers.
- Preserve provenance: connector id, source reference, confidence, sensitivity,
  and policy.
- Make observation ingestion and query auditable.
- Support both human-facing summaries and machine-facing structured observations.
- Allow generalized connectors where useful, including an OS/action connector,
  without giving them ambient unrestricted power.

## Non-Goals

- Define a full taxonomy of all connector types.
- Define a network-wide Sensorium federation protocol in v1.
- Make Sensorium a transport or publication authority.
- Let Sensorium directly publish `whisper-signal.v1`, `agora-record.v1`, or
  emergency activation artifacts.
- Replace Monus signal weighting, Whisper publication, Arca orchestration, or
  emergency evaluation.
- Give connectors unrestricted shell, filesystem, camera, microphone, network, or
  memory access.
- Freeze one global ontology for external reality.

## Out of Scope for v1

The following items are intentionally outside the v1 acceptance boundary:

- mandatory OS/action connector support,
- invasive connector classes such as microphone, camera, health/wearable,
  location, private inbox, or browser-history readers,
- federated Sensorium read-through to a neighboring node,
- a Seed Directory-backed connector class registry,
- streaming transport as a requirement,
- runtime addition of OS/action allowlist entries without an operator-signed
  configuration change,
- and making `sensorium-observation.v1` a frozen schema before at least one real
  connector and one real consumer validate the shape.

## Proposed Model

### 1. Layer Split

The v1 stack is:

```text
External world
  -> Connector-specific adapter
  -> Sensorium admission and minimal normalization
  -> Local Sensorium observation store/read model
  -> Host-granted consumer capabilities
  -> Monus / Arca / emergency evaluation / agent / UI
  -> Optional downstream protocol layer
```

The key boundary is between connector and Sensorium:

- the connector knows how to talk to arXiv, GitHub, a local microphone, an OS
  command allowlist, a wearable, a weather endpoint, or a local file watcher;
- Sensorium only knows that an admitted observation has a source, time, kind,
  subject, summary, confidence, sensitivity, provenance, and policy.

### 2. Connector Responsibility

A connector is responsible for:

- concrete integration with one external source or source family,
- authentication to that source if needed,
- polling, streaming, scraping, shelling out, device reading, or API calling,
- transforming raw source output into a small observation candidate,
- attaching connector-local evidence references,
- classifying sensitivity before submission,
- applying source-specific pre-redaction before Sensorium admission when possible,
- surfacing health and last-observed status.

Connector-side redaction is useful but never authoritative. It is a source adapter
optimization: the connector may know that one source field is always unsafe to
emit. Sensorium still owns admission-time redaction, quarantine, rejection, and
the final policy visible to consumers.

Connectors MAY be specialized, for example:

- `sensorium.github.releases`,
- `sensorium.arxiv.search`,
- `sensorium.weather.local`,
- `sensorium.microphone.alarm`,
- `sensorium.wearable.heart-rate`.

Connectors MAY also be generalized when the operator can define a safe bounded
dictionary of actions. The primary example is an OS/action connector.

### 3. Connector I/O Lanes

The Unix `stdin` / `stdout` / `stderr` split is a useful inspiration for
connector design, but the Sensorium contract should model **logical lanes**, not
process streams. A connector may run as a process, local HTTP service, in-process
adapter, queue consumer, or future streaming worker. The common contract is the
shape of exchange, not the transport mechanics.

A reactive connector SHOULD expose up to four logical lanes:

1. **Directive lane** — host or Sensorium instructions to the connector. This is
   the `stdin`-inspired lane: action id, filters, query, observation window,
   timeout, byte budget, redaction profile, and policy constraints.
2. **Observation lane** — normal structured output. This is the `stdout`-inspired
   lane: JSON observations, summaries, timelines, or other data that can be
   represented as text-shaped JSON.
3. **Diagnostic lane** — structured errors, warnings, partial-failure notices,
   retry hints, and degradation reports. This is the `stderr`-inspired lane, but
   it remains JSON and is not mixed with observations.
4. **Artifact lane** — optional raw or binary outputs, such as audio snippets,
   images, raw telemetry, HTML captures, dumps, or source payloads. These SHOULD
   be returned by reference rather than inline when they are large, sensitive, or
   not naturally JSON-shaped.

This split keeps three facts separate:

- what the connector was asked to do,
- what it observed about the world,
- and what happened inside the connector while trying to observe it.

For example:

```json
{
  "schema": "sensorium-connector-directive.v1",
  "invocation/id": "inv:local:01J...",
  "connector/id": "sensorium.os.action",
  "action/id": "git_recent_commits",
  "params": {
    "limit": 20
  },
  "budget": {
    "timeout_ms": 5000,
    "max_output_bytes": 65536
  },
  "policy": {
    "allow_artifacts": false,
    "redaction_profile": "default"
  }
}
```

A connector response may contain observations, diagnostics, artifacts, or a
combination of those lanes:

```json
{
  "schema": "sensorium-connector-result.v1",
  "invocation/id": "inv:local:01J...",
  "status": "partial",
  "observations": [
    {
      "schema": "sensorium-observation.v1",
      "connector/id": "sensorium.github.releases",
      "signal/kind": "release",
      "subject/kind": "github-repository",
      "subject/id": "speakleash/bielik",
      "summary": {
        "lang": "en",
        "text": "A new Bielik release candidate was observed."
      }
    }
  ],
  "diagnostics": [
    {
      "level": "warning",
      "kind": "rate-limit-near",
      "message": "GitHub API budget is close to exhaustion.",
      "retry_after_sec": 900
    }
  ],
  "artifacts": [
    {
      "artifact/ref": "orbiplex:blob:sha256:...",
      "media_type": "application/json",
      "role": "raw-source-response",
      "sensitivity/class": "public"
    }
  ]
}
```

The lane-level invariants are:

- diagnostics are not observations,
- raw artifacts are evidence or source material, not normalized observations by
  default,
- every directive should carry an invocation id, timeout, and output budget,
- every artifact should carry media type, sensitivity class, and preferably a
  content-addressed reference,
- partial success is valid: observations may coexist with diagnostics,
- the directive lane never bypasses host-granted capability policy.

### 4. Generalized OS/Action Connector

An OS/action connector MAY expose a whitelist such as:

```json
{
  "actions": {
    "git_recent_commits": {
      "argv": ["git", "log", "--oneline", "-n", "{limit}"],
      "cwd_policy": "configured-repository",
      "params": {
        "limit": { "type": "integer", "minimum": 1, "maximum": 50 }
      }
    },
    "disk_free": {
      "argv": ["df", "-h", "{path}"],
      "params": {
        "path": { "type": "string", "enum": ["/", "/var", "/tmp"] }
      }
    }
  }
}
```

The connector MUST treat this as `action -> argv`, not as raw arbitrary shell
strings. A safe OS/action connector should enforce:

- an explicit action allowlist,
- typed parameter validation,
- no shell interpolation by default,
- timeout,
- output byte cap,
- stderr capture policy,
- working-directory allowlist,
- environment allowlist,
- redaction rules,
- per-consumer capability grants,
- and audit events for every invocation.

No action may be added, removed, or changed at runtime without an operator-signed
configuration change. A distribution may ship a reference OS/action connector,
but it remains an optional concrete connector to the local operating system, not
a built-in Sensorium privilege and not a requirement for Sensorium MVP.

This gives operators a practical adapter to local reality without turning
Sensorium into ambient shell access.

### 5. Sensorium Responsibility

Sensorium is responsible for:

- admitting or rejecting connector-submitted observation candidates,
- assigning stable local observation identifiers,
- enforcing local policy gates,
- normalizing into the minimal observation contract,
- storing recent observations or forwarding them to Memarium under policy,
- deriving read models such as timelines, topic summaries, and connector status,
- exposing host-granted query and summary capabilities,
- emitting audit records for admission, rejection, query, and redaction.

Sensorium SHOULD NOT embed connector-specific parsers in its core. If a source
requires special parsing, that logic belongs in the connector.

#### Redaction authority

Sensorium is authoritative for the final admitted observation. The connector may
submit a pre-redacted candidate or a redaction hint, but Sensorium decides:

- whether the candidate can be admitted as-is,
- whether it must be transformed into a redacted observation,
- whether it must be quarantined for operator or policy review,
- or whether it must be rejected with diagnostics.

If a connector cannot redact a candidate and Sensorium has no policy for the
candidate's sensitivity class, Sensorium MUST fail closed. The default outcome is
quarantine when the payload can be safely retained locally without consumer
access; otherwise the outcome is rejection with a diagnostic record. Quarantined
observations are not visible to Monus, Arca, Whisper, emergency evaluation, or
other consumers until a policy grants release.

### 6. Minimal Observation Contract

The initial contract should be intentionally boring. A candidate
`sensorium-observation.v1` shape is:

```json
{
  "schema": "sensorium-observation.v1",
  "observation/id": "obs:local:01J...",
  "invocation/id": "inv:local:01J...",
  "directive/ref": "sensorium-directive:local:01J...",
  "connector/id": "sensorium.github.releases",
  "connector/kind": "public-network-reader",
  "observed/at": "2026-04-18T10:00:00Z",
  "ingested/at": "2026-04-18T10:00:02Z",
  "signal/kind": "release",
  "subject/kind": "github-repository",
  "subject/id": "speakleash/bielik",
  "summary": {
    "lang": "en",
    "text": "A new Bielik release candidate was observed."
  },
  "confidence": {
    "class": "high",
    "rationale": "Observed from the upstream repository release feed."
  },
  "freshness": {
    "ttl_sec": 86400
  },
  "sensitivity": {
    "class": "public",
    "redaction": "none"
  },
  "source/ref": {
    "kind": "url",
    "value": "https://github.com/speakleash/bielik/releases"
  },
  "evidence/refs": [],
  "policy/hints": {
    "shareable": false,
    "memarium_admit": true,
    "requested_consumer_scopes": ["monus.read", "arca.read"]
  },
  "admission": {
    "status": "admitted",
    "redaction_status": "not-needed",
    "memarium_admit": true,
    "consumer_scopes": ["monus.read", "arca.read"]
  }
}
```

The shape is not meant to be a universal ontology. It is a common local envelope
for observations. Domain-specific payloads MAY be attached later, but consumers
should be able to make basic policy decisions from the envelope alone.

`confidence.class` in this proposal is Sensorium-local and intentionally not the
same contract as the emergency `C0`-`C4` credibility scale. A promotion rule may
map Sensorium confidence into emergency credibility when creating an
`emergency-signal.v1`, but that mapping belongs at the emergency boundary rather
than in the base observation envelope.

`policy/hints` are connector-supplied requests or suggestions. `admission` is
the Sensorium-authored decision and is the only policy section that consumers may
treat as authoritative.

Reactive observations SHOULD carry `invocation/id` and `directive/ref` so the
trace connects directive, connector execution, diagnostics, artifacts, and final
admission. Autonomous observations MAY instead carry a schedule, subscription, or
source-event reference once those shapes exist.

### 7. Host Capability Surface

The first useful host-granted capability families are:

```text
sensorium.connector.list
sensorium.connector.status
sensorium.connector.invoke
sensorium.observe.submit
sensorium.observe.query
sensorium.observation.get
sensorium.topic.summary
sensorium.health
```

For a supervised HTTP/JSON module, these may be exposed as local host capability
requests rather than public network APIs. The Node grants them per module and per
operator policy.

Suggested behavior:

- `sensorium.connector.list` returns configured connectors and their declared
  classes.
- `sensorium.connector.status` returns health, last success, last error class,
  and freshness.
- `sensorium.connector.invoke` submits an active directive to a reactive
  connector under host policy.
- `sensorium.observe.submit` admits a connector-produced observation candidate.
- `sensorium.observe.query` returns bounded observation records by time, subject,
  signal kind, connector, or sensitivity class.
- `sensorium.observation.get` returns one observation by id if the caller has
  scope.
- `sensorium.topic.summary` returns a compact local summary for a topic or
  subject class.
- `sensorium.health` reports module readiness and degraded dependencies.

Subject timelines are a query profile, not a separate v1 capability, unless a
real consumer later needs a distinct optimized surface.

### 8. Relationship to Monus

Monus consumes Sensorium, but Sensorium does not replace Monus.

- Sensorium observes and normalizes local reality-facing signals.
- Monus weighs admitted local signals over time.
- Monus prepares candidate concern drafts, recommendations, or
  do-not-publish decisions.
- Whisper publication remains a separate Node-owned and policy-gated path.

If Sensorium materially shaped a Whisper-bound concern through Monus, downstream
provenance should preserve `monus-sensorium-derived`.

### 9. Relationship to Emergency Evaluation

Emergency evaluation may consume Sensorium observations, but Sensorium does not
decide emergency activation.

`emergency-signal.v1` already sits above raw connector telemetry and below
activation decisions. Sensorium may supply source observations that an emergency
pipeline transforms into `emergency-signal.v1`, but trigger classification,
corroboration thresholds, TC5 degraded-trust behavior, activation, TTL, and
post-crisis review remain emergency-domain responsibilities.

### 10. Relationship to Arca

Arca may consume Sensorium summaries as workflow inputs. For example, story 009
uses a research node with connectors to arXiv, GitHub repositories, mailing
lists, and news feeds.

The healthy boundary is:

- Sensorium provides observations and summaries,
- Arca orchestrates workflow intent and task progression,
- external artifact movement remains in the chosen data plane, such as git, INAC,
  or another explicitly selected substrate.

Arca should not learn how to poll every external source itself when a local
Sensorium capability can provide a bounded observation surface.

Story 009 can be the first full non-emergency Sensorium consumer because its
research step can use non-invasive public-network connector classes:

- `sensorium.github.releases`,
- `sensorium.arxiv.search`,
- `sensorium.mailing-list`,
- `sensorium.feed.reader`.

None of those requires OS/action support or high-sensitivity sensors. Therefore
story 009 can be satisfied in Phase 1 using public-network readers. A deployment
may emulate some of those readers through an OS/action connector later, but that
is a connector implementation choice rather than a Sensorium contract
requirement.

### 11. Relationship to Memarium

Sensorium observations may be ephemeral or durable.

Memarium is the organ of durable memory and knowledge. Sensorium may forward
selected observations into Memarium when policy allows durability. Sensorium
should not assume that every observation deserves permanent storage.

A useful default split is:

- Sensorium keeps short-lived operational observations and connector state,
- Memarium preserves admitted observations that should not disappear,
- audit traces record why an observation was admitted, redacted, rejected,
  expired, or promoted.

### 12. Relationship to Whisper

Sensorium should not publish whispers.

Sensorium-originated signals can become part of a local reasoning chain:

```text
Sensorium observation -> Monus weighting -> candidate concern draft
  -> Node/Whisper review -> optional whisper-signal.v1 publication
```

This preserves the difference between:

- raw local observation,
- local interpretation,
- social-signal publication,
- and distributed correlation.

Acute personal emergencies should still prefer local help or emergency-assistance
paths before Whisper. Whisper is for correlation-worthy distributed patterns, not
the first response to likely cardiac arrest, fire, collapse, or comparable direct
danger.

## Policy and Safety

Sensorium is powerful because it touches reality. Its default safety posture must
therefore be conservative:

- consent before invasive sources,
- data minimization by default,
- local-first processing,
- context separation between connectors and consumers,
- explicit capability grants,
- no ambient connector access to Node memory,
- no ambient consumer access to all observations,
- redaction before broader consumption,
- auditability for connector actions and observation reads,
- fail-closed behavior for high-sensitivity or high-risk connector classes.

Sensitive connector classes such as microphone, camera, health sensor, location,
browser history, filesystem watcher, shell/action, and private inbox reader
should require explicit operator policy and visible UI state.

Baseline connector class policy:

| Connector class | Sensitivity baseline | Default policy |
| :--- | :--- | :--- |
| `public-network-reader` | `public` | admit locally with bounded TTL; no network publication |
| `feed-reader` / `mailing-list-reader` | `public` or `community` | admit locally when source is public or explicitly configured |
| `os-action` | `operational-sensitive` | disabled by default; requires operator-signed action allowlist |
| `filesystem-watcher` / `private-inbox-reader` | `private` | fail closed; explicit operator policy and redaction required |
| `microphone` / `camera` / `health-wearable` / `location` | `sensitive-personal` | fail closed; visible UI state and explicit consent required |

## Deployment Shape

The initial implementation SHOULD use one of two shapes:

1. **Supervised sidecar module** through `http_local_json`:
   - best for language independence and connector experimentation,
   - aligns with proposal 019,
   - keeps connector faults outside the daemon process.
2. **In-process Sensorium core with sidecar connectors**:
   - useful later if observation admission and read models need tighter coupling
     to Node storage,
   - keeps connector complexity still outside the trusted core.

The v1 proposal prefers the first shape unless a concrete implementation path
proves that in-process admission is required.

## No-Sensorium Mode

Absence of Sensorium is a valid Node configuration. A Node without configured
connectors remains a valid Node.

Consumers such as Monus or Arca MUST treat missing Sensorium capabilities as a
degraded input condition, not as a runtime error. They may show reduced
functionality, skip Sensorium-derived enrichment, or request operator
configuration, but they must not fail the whole workflow merely because no
Sensorium provider is attached.

## Invariants

- Sensorium is local-first.
- Connectors adapt; Sensorium normalizes.
- Sensorium observations are not network publications.
- Consumers receive only host-granted views.
- Connector-specific logic does not leak into every consumer.
- Raw sensitive data is not retained or shared unless policy explicitly allows it.
- Downstream artifacts preserve provenance when Sensorium materially contributed.
- Sensorium MUST NOT publish Whisper artifacts.
- Sensorium MUST NOT decide emergency activation.
- Sensorium MUST NOT own Arca workflow authority.
- OS/action is an optional connector class, not a built-in Sensorium privilege.
- No OS/action allowlist entry may be changed without an operator-signed
  configuration update.
- Absence of Sensorium is a valid Node configuration; consumers MUST degrade,
  not crash.

## Open Questions

1. Should `sensorium-observation.v1` become a formal JSON Schema immediately, or
   stay as a proposal-level candidate until the first connector is implemented?
2. Should Sensorium keep its own short-lived observation store, or should it write
   every admitted observation into a Node-owned generic module store with TTL?
3. Which connector classes are safe enough for the first reference
   implementation: public-network reader, local file watcher, OS/action allowlist,
   weather, or health/wearable?
4. Should connector definitions themselves be represented as host-owned module
   store records?
5. What minimal UI indicator is required when invasive connectors such as camera,
   microphone, location, or shell/action are active?
6. How should story-009 `task_type` values map onto Sensorium query shapes and
   connector classes? Should connector classes eventually have their own catalog,
   or borrow discovery semantics from Seed Directory?
7. Can Sensorium v2 support read-through to a trusted neighboring node at an
   explicit trust level, or should cross-node observation remain a separate
   protocol family?

## Implementation Sketch

Phase 0:

- create a supervised Sensorium module skeleton,
- implement connector list/status and health,
- implement `sensorium.observe.submit` with in-memory admission,
- implement no-sensorium degradation behavior for consumers,
- define directive/result fixtures for connector I/O lanes,
- define the first candidate `sensorium-observation.v1` JSON shape in code or
  fixtures only.

Phase 1:

- persist admitted observations with TTL,
- expose bounded query, get, and topic summary capabilities,
- implement `sensorium.connector.invoke` for at least one public-network reader,
- add audit events for submit/query/get,
- implement one non-invasive public-network connector,
- satisfy story-009 research input through public-network connectors where
  possible.

Phase 2:

- add host-owned connector configuration,
- optionally add OS/action connector with strict operator-signed action allowlist,
- allow Monus and Arca to consume Sensorium summaries through explicit host
  grants.

Phase 3:

- formalize `sensorium-observation.v1` as a schema if two or more consumers need
  the same contract,
- define promotion rules from Sensorium observation to `emergency-signal.v1`,
  Monus concern draft, or Memarium durable fact.
