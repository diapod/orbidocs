# Story 008: Leaving an Opinion on a Website via the Local Node

## Summary

As an operator who also runs a local Agora relay on the same node, I want
to open the Node UI, type "cool site" under `https://randomseed.io/`, and
have my node sign the opinion and hand it to a relay — without me having
to know, configure, or even remember where the relay lives — so that
leaving an honest opinion on the open web is as cheap as a sentence by
the fence, and no platform operator gets to decide whether my words
appear.

This story is a direct translation of the Polgrzybix thread from the
seqnote ["The Swarm Has
Opinions"](https://orbiplex.ai/seq/i-imagine-that/03-swarm-has-opinions/).
Matthew is blocked because the police station website has comments
disabled. In the world of this story, he would not need the station's
permission: his opinion would be a signed `resource-opinion.v1` record
tied to the station's URL, living in the swarm. Here we walk the
simplest possible version of that same act: one author, one URL, one
node that happens to be both the UI host and the relay.

## Current Baseline Used by This Story

This story is grounded in:

- **Proposal 035** (Agora — topic-addressed record relay), in particular
  §5.7 *Capability passport semantics for `agora.relay`* and the
  `AgoraRecord` envelope with `record/about` for external resource
  references;
- **Proposal 026** (Resource opinions and discussion surfaces) for the
  `resource/kind` + `resource/id` pair and the `resource-opinion.v1`
  content schema;
- **Proposal 024** (Capability passports and network-ledger delegation)
  for the idea that capability *routing* — i.e. "who offers this
  capability and how do I reach them" — stays inside the capability
  model rather than being hardcoded;
- Story 000 for node identity and the host capability channel the
  Node UI uses to ask the daemon questions.

This story assumes the node's own `agora-service` is running locally
(loopback) and has already announced `agora.relay` to the daemon's host
capability API. No Seed Directory, no federation, no delegated keys —
just the simplest possible end-to-end path.

## Cast and Scene

- **Ela**, node operator, participant
  `participant:did:key:z6MkEla...`, runs `orbiplex-node-daemon` on
  `localhost`.
- **Local Agora relay**, an `agora-service` process supervised by the
  same daemon, reachable on a loopback port known only to the daemon's
  module registry.
- **Node UI**, a browser tab Ela has open against the operator-only
  control surface on loopback.

The subject resource is the website `https://randomseed.io/`. Ela wants
to say "cool site" about it.

## Sequence of Steps

### Step 1: Ela opens the compose form

In the Node UI, Ela clicks **New opinion** and types:

- **Subject**: `https://randomseed.io/`
- **Opinion**: `cool site`
- (rating, tags, language — left blank; the field is optional)

The UI does not ask Ela which relay will carry the record. It does not
ask for a topic. Those are infrastructure choices — the node makes
them.

### Step 2: Node UI resolves the local Agora relay via capability routing

Before the UI can POST the opinion anywhere, it needs an endpoint. It
asks the daemon's **host capability API** for a provider of capability
`agora.relay`:

```http
GET /v1/host/capabilities/agora.relay
X-Orbiplex-Authtok: <daemon control token>
```

For this story the caller is Node UI, so the request uses the daemon
control token. Middleware modules use their separate host-capability
token when they call daemon-owned POST capabilities such as
`signer.sign`; this read-only lookup is the UI's control-plane view of
the same host capability registry.

The daemon answers from its module registry — the same registry
populated when `agora-service` started up and announced itself:

```json
{
  "capability": "agora.relay",
  "providers": [
    {
      "module_id": "agora-service",
      "endpoint_url": "http://127.0.0.1:47991",
      "transport": "http-local",
      "scope": "local",
      "description": "Topic-addressed Agora record relay",
      "passport": null
    }
  ]
}
```

Three things matter here:

- The UI learned the relay's address **from the capability model**, not
  from a config file it owns. If tomorrow the relay moves to a
  different loopback port, the UI still finds it.
- `scope: "local"` and `passport: null` tell the UI this is the
  operator's own relay. No `agora.relay` capability passport is needed
  for local ingest (see proposal 035 §5.7: "Agora without an
  `agora.relay` passport remains a valid local relay").
- If the capability is known but no local provider is currently ready,
  the daemon returns `200` with an empty `providers` array. If the
  capability is unknown, it returns `404 capability_unknown`. The UI
  uses that distinction to show an explicit "no local relay available"
  state instead of silently falling back to a remote relay.

### Step 3: Node UI assembles the Agora record

The UI builds an `agora-record.v1` envelope, filling in the opinion
fields and the external resource reference:

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:pending",
  "record/kind": "opinion",
  "topic/key": "opinions/url",
  "author/participant-id": "participant:did:key:z6MkEla...",
  "authored/at": "2026-04-16T14:02:11Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "cool site",
    "opinion/lang": "en"
  },
  "record/about": [
    {
      "resource/kind": "url",
      "resource/id": "https://randomseed.io/"
    }
  ],
  "signature": { "alg": "ed25519", "value": "pending" }
}
```

Shape notes:

- `record/kind = "opinion"` and `content/schema = "resource-opinion.v1"`
  are the first content-schema row in proposal 035 §3 (Table of MVP
  kinds × content schemas).
- `record/about` carries the `{resource/kind, resource/id}` pair from
  proposal 026. The resource is identified as `url:<the URL>`.
- `topic/key` is derived from the subject kind (`opinions/url` for a
  URL opinion). A more elaborate deployment might split further by
  domain or community; the MVP keeps the first partition per resource
  kind.
- `record/id` and `signature.value` are placeholders; the signer
  replaces them.

### Step 4: Node UI signs through the host signer

The UI POSTs the envelope to the local relay's signing endpoint:

```http
POST <endpoint_url>/v1/agora/records.sign
Content-Type: application/json

{ "record": { ... as above ... } }
```

The relay canonicalizes the record, asks the daemon's host signer for
an Ed25519 signature in the `agora.record.v1` domain with Ela's
`PrimaryParticipant` key, verifies the returned key matches the author,
and hands the envelope back with `record/id` and `signature.value`
filled in.

### Step 5: Ingest into the same local relay

The signed envelope is POSTed to the same service's ingest endpoint:

```http
POST <endpoint_url>/v1/agora/topics/opinions%2Furl/records
Content-Type: application/json

{ ... signed envelope ... }
```

Because signing and ingest are separate publisher-edge operations, the
ingest path re-verifies the signed envelope, checks content-addressing
and topic ACL, then persists the record into the local relay backend.
The first successful POST returns `201 Created` with the canonical
`record/id`; a duplicate POST of the same content-addressed record
returns `200 OK`.

### Step 6: The UI confirms the opinion is live

The UI reads back the record by id:

```http
GET <endpoint_url>/v1/agora/records/sha256:…
```

Ela sees her opinion in the node's own timeline for
`https://randomseed.io/`, tied to her participant id and her signature.
From this moment the opinion exists independently of `randomseed.io`:
the site does not have to host a comment form, enable comments, or
approve Ela's text. The opinion belongs to Ela.

## Acceptance Criteria

| # | Criterion | Verification |
| :--- | :--- | :--- |
| 1 | Node UI has no hardcoded Agora endpoint; it learns it from the daemon's host capability API under capability id `agora.relay` | inspect UI config + trace the HTTP call to the daemon |
| 2 | With no `agora-service` registered, the UI surfaces "no local relay available" and does NOT silently fall back to a public one | test: stop the module, reload UI |
| 3 | `resource-opinion.v1` content passes schema validation against the copy in `orbidocs/doc/schemas/` | schema test |
| 4 | `record/about` contains exactly one entry with `resource/kind = "url"` and `resource/id = "https://randomseed.io/"` (byte-identical, no normalization drift) | integration test |
| 5 | Signing uses `KeyRef::PrimaryParticipant` and domain tag `agora.record.v1`; the envelope self-verifies before ingest | log inspection + `verify_envelope` assertion |
| 6 | Ingest returns `201 Created` with the same `record/id` computed by the signer; duplicate POST returns `200 OK` and is idempotent | integration test |
| 7 | Full action trace exists under `trace/agora` and includes: capability lookup, sign request, ingest, readback | log inspection after test run |
| 8 | The whole flow works with zero `agora.relay` capability passport configured (local-only mode) | deploy without a passport, re-run steps 1–6 |

## What This Story Does NOT Cover

- **Federation and Seed Directory publication** — the opinion stays on
  Ela's node. Replication to peer relays, Seed Directory discovery of
  other `agora.relay` providers, and passport-backed federation are
  separate stories. Capability routing in this story resolves only
  local providers.
- **Delegated / proxy-key signing** — Ela signs with her primary
  participant key. Proxy keys and `key-delegation.v1` are tracked as
  P12 in `docs/agora/TODO.md`.
- **Content moderation, reputation, or filtering** — the seqnote makes
  clear filtering is the listener's concern. This story produces an
  opinion; it does not say anything about whose attention it reaches.
- **Multi-subject opinions** — `record/about` is an array in the
  schema, but this story writes exactly one entry.
- **Ratings and richer opinion metadata** (`rating`, `tags`) — the
  `resource-opinion.v1` schema allows them; Ela just does not use them.

## Architectural Significance

This is the smallest coherent slice that demonstrates three
Orbiplex-specific commitments simultaneously:

1. **An opinion belongs to its author.** The record is signed by Ela's
   participant key and content-addressed; no operator (not even the
   subject site) holds the delete button.
2. **Infrastructure is discovered, not configured.** The UI asks the
   daemon "who speaks `agora.relay`?" and gets the local provider. On a
   node without a ready local relay, the same call returns an explicit
   no-provider state rather than making the UI guess or silently use a
   public relay.
3. **The simplest useful Agora shape is already interoperable.** The
   envelope used here (`record/kind = opinion`, `content/schema =
   resource-opinion.v1`, `record/about` carrying `url:<url>`) is the
   same envelope a federated, passport-gated, multi-relay deployment
   would use. No local shortcuts, no dialects.

The value of this story is negative in the best sense: nothing about
being local requires a special path. The envelope, the signer contract,
and the capability lookup are all the same machinery that a post-MVP,
federated, passport-backed deployment will run — just with one
provider and zero hops.

## Realisation

This section is a **map**, not a mirror. Capability status (`:todo`,
`:in-progress`, `:done`, `:planned`, `:optional`) lives in the
`*-caps.edn` sidecars under `doc/project/60-solutions/` and is surfaced
in the generated `CAPABILITY-MATRIX.en.md`. The table below tells the
reader **where to look** for each slice of the story; it does not carry
the status itself, to avoid drift.

| Story scope | Component | Capability (catalog entry — status lives here) | Solution doc |
|---|---|---|---|
| Step 1 (compose form) · Step 3 (envelope assembly) | Orbiplex Node UI | `node-ui-caps.edn` → `:opinion-compose-form` | [`node-ui.md`](../60-solutions/node-ui.md) |
| Step 2 (resolve `agora.relay` provider via host capability API) | Orbiplex Node (daemon) | `node-caps.edn` → `:host-capability-lookup` | [`node.md`](../60-solutions/node.md) |
| Step 4 (sign through host signer, domain `agora.record.v1`) | Orbiplex Agora (node-attached module) | [`agora-caps.edn`](../60-solutions/agora-caps.edn) → `:agora-record-sign` | [`agora.md`](../60-solutions/agora.md) |
| Step 5 (ingest signed envelope) | Orbiplex Agora | [`agora-caps.edn`](../60-solutions/agora-caps.edn) → `:agora-record-ingest` | [`agora.md`](../60-solutions/agora.md) |
| Step 6 (readback by `record/id`) | Orbiplex Agora | [`agora-caps.edn`](../60-solutions/agora-caps.edn) → `:agora-record-query` | [`agora.md`](../60-solutions/agora.md) |

The implementation-oriented companion for the Agora rows is
[`035-agora-topic-addressed-relay-impl.md`](../60-solutions/035-agora-topic-addressed-relay-impl.md).
The requirements contract this story enforces lives in
[`requirements-014.md`](../50-requirements/requirements-014.md).

**Declared capability anchors**:

1. `:opinion-compose-form` lives in `node-ui-caps.edn`. It names the
   dedicated UI surface for composing a resource opinion instead of
   hiding the story behind the generic node control surface.
2. `:host-capability-lookup` lives in `node-caps.edn`. It names the
   daemon read model used by Step 2, independently of the supervised
   middleware runtime that currently supplies the provider reports.

**Implementation anchors** (runtime, Rust side — status kept in the
implementation ledger and module-level backlogs in the sibling `node`
repository, not in this document):

- `node/docs/implementation-ledger.toml` — per-crate status for
  `agora-core`, `agora-service`, and adjacent crates.
- `node/docs/agora/TODO.md` — granular P1–P13 backlog for the Agora
  module. Step 4 of this story depends on P12 only if Ela uses a proxy
  key; with `PrimaryParticipant` (the scenario as written), no P-item
  is blocking.
- A future delegated-signing variant of this story would exercise
  `key-delegation.v1` (proposal 032) and is out of scope for the
  direct-signature MVP path.

## References

- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
  (§3 MVP kinds × schemas table, §5.7 `agora.relay` passport semantics)
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
  (`resource/kind` + `resource/id`, `resource-opinion.v1`)
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
  (capability routing within the capability model)
- `doc/project/30-stories/story-000.md` (identity + host capability
  channel baseline)
- `doc/project/50-requirements/requirements-014.md` (contract for the
  URL-opinion local-relay MVP path)
- `doc/project/60-solutions/agora.md` (Agora solution document)
- `doc/project/60-solutions/agora-caps.edn` (Agora capability catalog)
- `doc/project/60-solutions/035-agora-topic-addressed-relay-impl.md`
  (layered implementation guidelines for proposal 035)
- `doc/project/60-solutions/CAPABILITY-MATRIX.en.md` (generated
  architecture-level status view)
- `doc/project/60-solutions/_templates/` (authoring templates for
  new solution documents and capability catalogs)
- ["The Swarm Has Opinions"](https://orbiplex.ai/seq/i-imagine-that/03-swarm-has-opinions/)
  (the Polgrzybix thread — the human motivation this story translates
  into a minimal technical flow)
