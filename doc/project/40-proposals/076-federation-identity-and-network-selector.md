# Proposal 076: Federation Identity and Network Selector

Based on:

- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`
- `doc/project/40-proposals/075-matrix-homeserver-runtime-profile.md`
- `doc/project/60-solutions/021-agora-authority/021-agora-authority.md`
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`
- `doc/project/60-solutions/036-room/036-room.md`

## Status

Draft

## Date

2026-07-01

## Executive Summary

Orbiplex already uses `federation_id` as a data field (Seed Directory trust
entries, Corpus taxonomy artifacts) and already has a Room exposure ladder that
assumes federations are countable, distinguishable things (`federation-local`
vs `cross-federation/global`). None of that is grounded in one concrete answer
to "what, operationally, is a federation."

This proposal promotes `federation_id` from descriptive metadata on individual
trust-registry entries to a **node-wide network selector**, in the sense that
`mainnet`/`testnet` are network selectors in existing distributed-ledger
systems: a value resolved once, before the node does anything else, that
determines which root trust and which default services apply.

The central rule is:

```text
A federation is a separate operational identity: separate data-dir, separate
root trust, separate default services. Cooperation across federations is a
property of what participants explicitly do together (a room, a query, a
gossip promotion) — never an automatic consequence of running the same
software.
```

Unconfigured nodes default to `orbiplex-main`, the reference public network. An
operator who wants full structural isolation (for example, a company or a
closed group of friends whose top-level attestation keys must never mix with
the public network) configures a distinct `federation_id`, backed by its own
`data-dir` and its own root trust file. This proposal deliberately narrows
"federation" to that operational sense, and leaves broader cross-federation
cooperation to the separate, lighter `alliance` concept.

This root trust file is also the boundary between Orbiplex authority and
ordinary transport compatibility. Public WebPKI can protect an HTTPS/WSS
connection to a public endpoint, but it is not the source of federation
authority. A node accepts Seed Directory authority, top-level attestation roots,
service roots, and bootstrap peers because they are present in or derived from
the signed `federation-root.v1` pack and local policy, not merely because an
endpoint presents a certificate chaining to a public browser CA. A private or
self-signed federation root is valid when it is explicit, scoped to the
federation, signed/accepted, and auditable.

## Context and Problem Statement

`federation_id` already appears in the documentation and in code, in two
places, neither of which defines it as a node identity:

- `seed-directory-trust.v1` (Proposal 054) carries `federation_id` as an
  optional field on *individual trusted-directory entries* — descriptive
  metadata about which federation a given directory claims to serve, not a
  property of the node consulting that registry.
- `daemon/src/config.rs` implements exactly that: `federation_id` lives on
  `DaemonSeedDirectoryTrustConfig`, one field among several on one trust-registry
  row.
- Corpus taxonomy artifacts (Proposal 069) carry a `federation/id` field
  (distinct from that same artifact's own `taxonomy/id`, for example
  `"taxonomy/id": "orbiplex.core"` alongside `"federation/id": "orbiplex"`)
  identifying which federation owns/signs a taxonomy, again as a property of
  one artifact, not of the node.

Meanwhile, Room (Proposal 070 / Solution 036) already has a policy axis that
presumes federations are first-class, countable things: room TTL policy
distinguishes `federation-local` rooms from `cross-federation/global` rooms.
That distinction is meaningless without a concrete answer to "which federation
is *this* room, or *this* node, actually in."

The practical trigger for this proposal was a Matrix homeserver profile
discussion (Proposal 075): without a clear definition, "federation" risked
quietly becoming "whatever Matrix's own homeserver-to-homeserver federation
protocol provides" — importing a transport's trust model into a concept that
must remain transport-independent (see Proposal 075's Authority Boundary rule,
which this proposal extends one level up: a carrier must not become an
authority, and neither should a specific federation's infrastructure become
*the* definition of federation for everyone else).

A second, independent trigger is operational: an organization (a company, a
closed group) wants to run Orbiplex entirely on its own root of trust, with a
structural guarantee — not a configuration convention — that its data can never
mix with the public default network.

## Goals

- Define `federation_id` as a node-wide, pre-runtime network selector,
  analogous to a chain id (`mainnet`/`testnet`/custom) in existing distributed
  systems.
- Default to `orbiplex-main` when unconfigured, so a zero-config node safely
  joins the reference public network.
- Bind federation identity, root trust keys, and Seed Directory bootstrap state
  to one `data-dir`-scoped root-config file, merged into runtime config at
  startup.
- Guarantee structural (filesystem-level) non-leakage between differently
  configured federations — no shared mutable state across two `data-dir`s.
- Preserve cross-federation cooperation as an explicit, higher-layer concept
  realized by Room/Whisper/Corpus, not eliminate it or fold it back into node
  identity.
- Reuse existing primitives — Agora Authority's organization root and custody
  modes, `key-delegation.v1`, Seed Directory's trust-tier model — rather than
  inventing a parallel trust mechanism.

## Non-Goals

- Not a redefinition of Room's existing `federation-local` /
  `cross-federation/global` exposure vocabulary. Those terms are correct; this
  proposal gives them a concrete node-level referent.
- Not a full specification of the lighter, cross-cutting cooperation concept
  named `alliance` in this proposal. `Alliance` is the vocabulary for explicit
  cross-federation cooperation; its richer policy model belongs in a follow-up
  artifact if and when Room/Whisper/Corpus need it.
- Not a reputation or ranking system for federations.
- Not a requirement that every deployment explicitly configure a federation —
  the unconfigured `orbiplex-main` default path must stay safe and zero-config.
- Not a global registry or arbitration authority for `federation_id` strings;
  identifiers remain self-declared, consistent with Seed Directory's own
  anti-monopoly stance ("must not become one global source of truth").
- Not a live migration or merge tool for moving a running node between
  federations.
- Not the governance charter for the `orbiplex-main` root itself. This proposal
  selects an org-kind threshold root as the required shape, but concrete
  custodian selection, rotation ceremony, appeal path, and production signer
  roster remain governance artifacts rather than schema mechanics.

## Proposed Model

### 1. Federation as a Network Selector

`federation_id` becomes one node-wide configuration value, resolved before any
other subsystem starts:

- Default: `orbiplex-main` — the reference public network, inferred when no
  federation is explicitly configured.
- Alternative: any operator-chosen string (for example `acme-org`), resolved
  only from an explicit root-config file (section 3) — never inferred, never
  guessed from environment.
- A `federation_id` is self-declared data, not a globally arbitrated registry
  entry. Two unrelated operators may pick the same string; implementations
  distinguish them by explicit local pinning of root-pack digest and root keys,
  not by first-seen string ownership.

### 2. `data-dir` as the Isolation Boundary

A running node instance is bound to exactly one federation for the full
lifetime of that `data-dir`.

- Changing federation means pointing at a different `--data-dir`, not a runtime
  toggle or a config hot-reload.
- No code path may share mutable state — identity keys, Room projections, Agora
  authority cache, Seed Directory trust registry, capability passports — across
  two `data-dir`s.
- This is not a new isolation primitive. One-daemon-one-`data-dir` already
  implies this; this proposal makes federation scope explicitly co-located with
  it, so isolation is a structural property of "which directory did you point
  at," not an accident of careful configuration.

**Operating in more than one federation is switching, never concurrent use.**
An operator who genuinely needs both — for example, participating in the
public `orbiplex-main` network and running a closed corporate federation —
runs two entirely separate `data-dir`s, each with its own root config, its own
`peer_discovery.seeds[]` / `network.seed_directory[]` /
`network.seed_directory_trust[]` / `identity.sovereign_participant_ids[]`, and
its own local storage. The
operator switches which one is active by choosing which `data-dir` to start the
daemon against. There is no mode where one running node instance is
simultaneously a member of two federations; that would reopen exactly the
leakage risk this proposal exists to close.

### 3. Root Config File (Federation Pack, Local Form)

A `data-dir`-scoped file, merged into runtime configuration at startup the same
way other config overlays already are (for example the model-runtime catalog
override pattern), carries the fields below. This is now a real, checkable
artifact rather than a pseudo-block:
[`doc/schemas/federation-root.v1.schema.json`](../../schemas/federation-root.v1.schema.json),
with a positive example at
[`doc/schemas/examples/orbiplex-main.federation-root.json`](../../schemas/examples/orbiplex-main.federation-root.json)
and negative fixtures under
[`doc/schemas/examples/invalid/`](../../schemas/examples/invalid/)
(`org-without-custody.federation-root.json`, `unsigned.federation-root.json`,
`unknown-field.federation-root.json`). Field names are snake_case throughout,
deliberately matching `seed-directory-trust.v1` rather than the `noun/attribute`
convention of signed inter-node wire messages (`node-advertisement.v1`,
Corpus taxonomy records) — see the schema's own top-level `description` and
the resolved field-naming decision below. Shape, in outline:

```text
federation-root.v1 {
  schema                  # const "federation-root.v1"
  federation_id
  pack_version            # monotonic; a loader rejects a lower pack_version
                          #   than the last one accepted for this federation_id
  issued_at?
  attestation_roots[]     # this federation's OWN canonical top-level anchor(s).
                          # kind: participant — { id (participant:did:key),
                          #   purposes[]? (informational only, see below),
                          #   valid_from?, valid_until? }, feeding
                          #   identity.sovereign_participant_ids[].
                          # kind: org — adds required custody_mode
                          #   (any-authorized | threshold) and custody_policy_ref.
                          #   Loaded through identity.sovereign_subject_refs[]
                          #   (P076-011), not silently projected into the
                          #   participant-only compatibility list. NOT a copy of
                          #   any relay's Agora authority_roots[].
  custody_policies[]      # optional, self-contained org custody rules referenced
                          #   by attestation_roots[].custody_policy_ref. MVP
                          #   runtime evaluates only purpose=federation-root,
                          #   exactly one rule per policy,
                          #   mode=any-authorized|threshold, and authorized
                          #   participant/key signer sets.
  bootstrap_seed_peers[]  # this federation's static WSS seed peers (Proposal 014's
                          #   "mandatory first bootstrap layer"), matching
                          #   DaemonSeedPeerConfig field-for-field (one endpoint_url
                          #   per entry, no priority/enabled — richer multi-endpoint
                          #   peers would need that struct enriched first)
  seed_directory_bootstrap[]
                          # this federation's own canonical default trusted
                          #   directories; each entry fans out to BOTH
                          #   network.seed_directory[] and
                          #   network.seed_directory_trust[] at load time — the
                          #   latter's federation_id is filled from this pack's
                          #   own federation_id, not repeated per entry
  policy_ref?
  endorsement_refs[]?
  signatures[]            # required; "self-signed by the pack's own root" is
                          #   valid, "unsigned" is not
}
```

`purposes[]` on an `attestation_roots[]` entry mirrors
`AgoraAuthorityRootConfig.purposes`. The generalized
`identity.sovereign_subject_refs[]` surface preserves this metadata; the older
`identity.sovereign_participant_ids[]` remains only a participant-id compatibility
projection and intentionally cannot carry per-root purpose metadata. Per-root
`valid_from`/`valid_until` live on each `attestation_roots[]` entry, not the whole
pack, mirroring `AgoraAuthorityRootConfig` exactly — different roots in one pack
may rotate on independent schedules. `assurance` and `namespaces[]` are
deliberately NOT part of `attestation_roots[]`: those are Agora Authority's own
local, per-relay, per-namespace policy vocabulary (Solution 021); a federation
root becomes Agora's *default* root for its reserved namespace (see below), and
Agora assigns its own assurance/namespace values when adopting it, rather than
this federation-wide pack carrying Agora-specific fields.

This is the concrete, local shape of the "federation pack" already named
(but not specified) in Proposal 054. This proposal defines its file shape and
load-time binding; it does not introduce a new kind of trust artifact.

Loading this file resolves, and where present overrides, exactly four existing
daemon configuration surfaces: `peer_discovery.seeds[]` (static WSS bootstrap
peers, Proposal 014), `network.seed_directory[]` and `network.seed_directory_trust[]`
(Seed Directory query targets and trust tiers, Proposal 054), and
`identity.sovereign_participant_ids[]` (the root/sovereign issuer list consumed
by capability-passport-chain verification, Seed Directory admission, and
Artifact Delivery bindings). Nothing else in daemon configuration is federation
material; a federation-root file that tries to carry any other field is
rejected, not silently ignored.

**Runtime surface.** `identity.sovereign_subject_refs[]` is the canonical runtime
projection for federation attestation roots. It accepts both `participant` and
`org` roots with optional custody metadata, while
`identity.sovereign_participant_ids[]` remains the narrower participant-only
compatibility projection. The loader validates this shape at startup; an
org-kind root without `custody_mode`/`custody_policy_ref`, or a participant root
with custody metadata, is rejected rather than silently coerced.

For production-trust packs, runtime verification now goes beyond schema shape:
the daemon canonicalizes the payload excluding `signatures[]`, verifies Ed25519
signatures, requires participant roots to be self-signed by the corresponding
participant key, and evaluates org roots against self-contained
`custody_policies[]` rules for `purpose = federation-root`. The schema catches
local shape errors such as `kind`/`id` prefix mismatch and multiple custody rules
per policy; parity between `attestation_roots[].custody_mode` and the referenced
policy rule mode remains a runtime invariant because portable JSON Schema cannot
express that cross-array reference cleanly. Runtime threshold evaluation counts
unique authorized signing keys, not real-world people, orgs, or custody seats;
governance process must ensure that the signer roster maps to actually separate
custodians.

The bundled `orbiplex-main` pack is a dev-bootstrap hard-MVP fixture gated by
`federation.allow_bundled_fixture_root`. The daemon default is fail-closed
(`false`): a node without an explicit data-dir `federation-root.v1.json` refuses
to start. Enabling the bundled fixture is an explicit local operator choice for
development/demo bootstrap only, and the fixture bypass is pinned to the raw pack
digest so a same-shape but byte-different bundled payload cannot inherit the
bypass. Explicit data-dir packs always require real signatures.

`attestation_roots[]` is **not** the same list as Agora Authority's own
`authority_roots[]` (Solution 021, `AgoraAuthorityRootConfig`). Agora Authority's
roots are deliberately narrower and more local: each entry is scoped to specific
Agora topic-namespace prefixes (`namespaces[]` is required and non-empty), and
Solution 021 is explicit that this configuration is local relay policy, not a
public federation contract that other relays must honor. This proposal's
`attestation_roots[]` answers a different, more foundational question — "what is
this federation's own top-level anchor" — and is meant to be canonical for every
node that joins the federation (via distribution defaults or a corporate root
file), not a per-relay variant.

The relationship is layering, not replacement: a federation's root naturally
becomes the *default* entry Agora Authority (and Seed Directory's own sovereign-
issuer policy, per Proposal 054 section 4) recognizes for the federation's own
reserved namespace, using the same `{id, kind, custody mode}` shape. Agora
Authority remains free to configure additional, narrower, purpose-scoped
`authority_roots[]` entries locally — for specific sub-namespaces, moderation
records, or delegated purposes — layered on top of, never in place of, the
federation root.

Absent file: the node runs as `orbiplex-main` under distribution defaults
(section 4) — the distributed software package itself populates these four
surfaces for `orbiplex-main`, so a zero-config node is not merely "safe", it is
actually able to discover peers and directories out of the box. Present file:
it is authoritative for that `data-dir` and **replaces**, not merges with, the
distribution defaults for these four surfaces — this is precisely how a closed
deployment (for example a corporate installation) locally overrides the public
`orbiplex-main` values with its own. A parse, signature, or custody-threshold
failure fails the node closed rather than falling back to `orbiplex-main`
defaults — falling back silently would quietly weaken exactly the isolation
guarantee an operator configured this file to get.

### 4. Distribution Defaults (`orbiplex-main`)

**Current state, verified in code.** Today all four surfaces default to empty
or inert: `peer_discovery.seeds` (`DaemonPeerDiscoveryConfig::default()`),
`network.seed_directory`, and `network.seed_directory_trust` (both
`DaemonNetworkConfig::default()`) all default to `Vec::new()`
(`daemon/src/config.rs`), and
`identity.sovereign_participant_ids` ships exactly one hardcoded placeholder
(`daemon/src/config.rs:341`) whose matching private key does not appear
anywhere else in the codebase — it functions as schema filler, not a working
root of trust. A fresh, unconfigured node cannot discover any peer or directory
today. This proposal changes that default from "safe but inert" to "safe and
actually able to join `orbiplex-main`."

The reference public federation ships as a signed default pack bundled with
the distributed software:

- Only the *verification key(s)* for this default pack are embedded/pinned in
  distributed code.
- Pack *content* (bootstrap directory list, thresholds, endorsements) can be
  updated by shipping a newer signed pack without re-baking a new binary for
  routine changes, using `key-delegation.v1` so the cold root key is rarely
  touched.
- Root custody for `orbiplex-main` SHOULD be `threshold`, not
  `any-authorized`, per the high-stakes-mechanism guardrails in
  `DEV-GUIDELINES.md` (multisig/threshold review, appeal path, audit trace).
  The selected shape is an org-kind threshold root, with `3-of-5` as the
  conservative initial target unless the governance charter chooses a stricter
  threshold. Concrete custodian names, ceremony, rotation, and appeal mechanics
  remain out of this proposal's schema scope and block treating `orbiplex-main`
  as production-trustworthy until documented.
- Federation-root custodian identities SHOULD be dedicated operational
  identities used only for root-pack approval, rotation, and recovery
  ceremonies. They SHOULD live in separate custodian `data-dir`s rather than in
  the same `data-dir` as the same person's ordinary participant/node activity.
  The reason is structural privacy and audit separation: `signatures[].key_public`
  and custody-policy authorized signer sets are public, stable correlation
  handles. Reusing a day-to-day participant identity would link root governance
  participation with unrelated Orbiplex activity by construction. Dedicated
  custodian identities remain accountable without making ordinary activity
  correlateable through the federation root.

### 5. Federation vs. Group

"Federation" in this proposal is deliberately narrow: an operational,
`data-dir`-scoped identity, one per running node instance.

Cross-federation cooperation — a Room whose membership spans participants
configured under different `federation_id`s, a Whisper public-gossip
promotion, a Corpus deliberation that solicits bids beyond one federation — is
a property of what participants deliberately do *together*, realized at the
Room/Whisper/Corpus layer. It is never a silent consequence of a node
belonging to two federations at once, because under this model it cannot: a
node has exactly one `federation_id`.

This grounds, without changing, Solution 036's existing Room exposure tiers:

- `federation-local` — bounded to participants who share the acting node's
  configured `federation_id`.
- `cross-federation/global` — a room whose membership is not bounded that way.

The lighter, cross-cutting concept is named `alliance`. An `alliance` is an
explicit cooperation relationship across federation boundaries, distinct from
both "federation" (this proposal's `data-dir`-scoped network selector) and Seed
Directory's already-used "community" trust tier.

## Relationship to Existing Proposals

- **Proposal 054 / Solution 031 (Seed Directory).** This proposal elevates
  `federation_id` from a per-trust-entry tag to a node-wide selector, and gives
  concrete shape to the "federation pack" / "distribution defaults" language
  already present there. Seed Directory's own trust-tier model
  (personal/community/federation-endorsed) is unchanged; a federation's
  bootstrap directory list is what a fresh node under that federation starts
  from.
- **Solution 021 (Agora Authority).** Reused for its custody-mode pattern
  (`any-authorized`/`threshold`, `AgoraAuthorityRootConfig`) and
  `key-delegation.v1`; this proposal adds no new key-authority mechanism. Agora
  Authority's own `authority_roots[]` remain a distinct, narrower, per-relay,
  namespace-scoped configuration — explicitly local policy, not a federation-wide
  contract (Solution 021: "MUST NOT be used as a policy input by other relays").
  This proposal's `attestation_roots[]` is the federation's own canonical anchor,
  which naturally becomes the default root Agora Authority recognizes for the
  federation's reserved namespace; it does not replace Agora Authority's ability
  to configure additional, narrower roots locally.
- **Proposal 070 / Solution 036 (Room).** Grounds the existing
  `federation-local` / `cross-federation/global` exposure tiers in a concrete
  node-level definition without changing them.
- **Proposal 074 (Multi-Node Federation Harness).** Can pin distinct,
  structurally isolated `federation-root.v1` files per test node — a
  "testnet"-style harness federation, distinct from `orbiplex-main`, instead of
  ad hoc per-test configuration.
- **Proposal 014 (Node Transport and Discovery MVP).** `peer_discovery.seeds[]`
  is exactly P014's static seed peer list, "the mandatory first bootstrap layer."
  This proposal's distribution defaults are what let that layer be non-empty
  for `orbiplex-main` out of the box, instead of requiring every fresh node to
  be told about a first peer manually.
- **Proposal 075 (Matrix Homeserver Runtime Profile).** P075's "Matrix as an
  Inter-Federation Carrier" profile is Matrix used as an optional carrier for
  moving federation-relevant data between two Orbiplex federations. Matrix's
  own homeserver-to-homeserver federation protocol is not what this proposal
  means by federation and must not become a stand-in definition for it — the
  same carrier-is-not-authority rule P075 already applies to Room/Agora/AD,
  applied one level up to the concept of federation itself.
- **Proposal 069 (Corpus).** Taxonomy artifacts already carry `federation/id`
  identifying the owning/signing federation for a namespace. This proposal's
  node-level `federation_id` is what a node uses to decide whether it treats an
  artifact's asserted `federation/id` as its own or as an explicitly recognized
  foreign one. Field-naming convention differs today (`federation/id` in
  taxonomy fixtures vs. `federation_id` in Seed Directory config) is deliberate:
  config/runtime registry artifacts use `federation_id`, while wire/domain
  artifacts may keep `federation/id`.
- **`federation_unavailable` crisis detector** (daemon configuration). Already
  monitors peer/Seed Directory reachability. Should be read as monitoring
  reachability of the node's *configured* federation's infrastructure
  specifically, which this proposal makes an explicit, named thing rather than
  an implicit global assumption.
- **Proposal 036 (Memarium).** The Community memory space's
  `ReplicationScope::Federated` (documented, not yet implemented) resolves
  against this proposal's `federation_id`: replication is bounded to peers
  sharing the local node's federation, a hard ceiling that a cross-federation
  alliance must not widen. Sharing Community-space knowledge
  across a federation boundary remains the existing explicit
  Community-to-Public promotion (Memarium section 3.3), riding Agora's
  federation-agnostic substrate — never an implicit consequence of shared
  Room/group membership.

## Data Contracts

- `federation-root.v1` (new) — the `data-dir`-scoped root config file:
  `federation_id`, `attestation_roots[]` (participant or org + custody mode),
  optional self-contained `custody_policies[]`,
  `bootstrap_seed_peers[]`, `seed_directory_bootstrap[]`, `signatures[]`,
  optional `policy_ref`/`endorsement_refs[]`. Schema:
  [`doc/schemas/federation-root.v1.schema.json`](../../schemas/federation-root.v1.schema.json);
  example: [`doc/schemas/examples/orbiplex-main.federation-root.json`](../../schemas/examples/orbiplex-main.federation-root.json);
  negative fixtures under [`doc/schemas/examples/invalid/`](../../schemas/examples/invalid/).
- `seed-directory-trust.v1` (existing, Proposal 054) — unchanged; a
  federation's bootstrap list populates this registry on first run.
- Reused unchanged: `capability-authorization-policy.v1`, `key-delegation.v1`,
  and the Agora Authority organization-root configuration shape.

## Failure Modes and Guardrails

| Failure | Risk | Mitigation |
|---|---|---|
| Root-config file missing/unreadable | Node silently runs under wrong trust | Fail closed by default: refuse to start unless the operator explicitly enables the bundled dev fixture. |
| Root-config file present but signature/custody threshold not met | Unauthorized root trust accepted | Fail closed at startup, not a degraded-mode warning. |
| Two `data-dir`s point at overlapping storage (for example a shared object-store path) | Cross-federation data leakage | Detect and refuse at startup; never silently merge. |
| Bundled `orbiplex-main` fixture enabled in production | Node relies on a bootstrap fixture rather than production root custody | Treat `federation.allow_bundled_fixture_root = true` as development/demo-only; production deployments provide an explicit signed data-dir pack. |
| Bundled fixture bytes differ from the pinned digest | A modified fixture inherits the invalid-signature bypass | Refuse the bypass and validate signatures normally, which currently rejects the fixture signature. |
| Legacy data-dir state has the same `pack_version` but no `pack_digest` | First post-upgrade load could pin the currently present pack bytes | Accept as a one-time migration caveat for pre-digest state only; after migration, same-version digest swaps are rejected. |
| Local attacker can write `federation-root.state.v1.json` | Anti-rollback state can be edited down | State guard is an operational guard against honest mistakes, not tamper-proof storage. Signature/custody verification remains the trust boundary; protect `data-dir` with host filesystem controls. |
| Operator assumes changing `federation_id` in a running config reloads trust | Stale keys/directories remain active | `federation_id` changes require a new `data-dir`; document and enforce that a live config reload MUST NOT silently accept a `federation_id` change. |
| Root custodian reuses an ordinary participant identity or ordinary node `data-dir` | Public root signatures become a correlation handle for unrelated Orbiplex activity | Use dedicated root-custodian participant identities and separate custodian `data-dir`s for federation-root ceremonies; do not use nyms, ordinary operator identities, or day-to-day participant keys as root custodians. |

## Open Questions

Open as of 2026-07-01:

1. Should `federation-root.v1` remain strictly restart-only, or should a bounded
   operator-triggered hot reload exist for the same `federation_id` with
   monotonic `pack_version`?
2. Should `seed_directory_bootstrap[].enabled` default to `true` for
   federation-endorsed directories, or should every federation-root pack require
   an explicit value to avoid hidden admission?
3. When `orbiplex-main` moves from hard-MVP bootstrap fixture to production root,
   which exact signer roster, custody threshold, rotation ceremony, and appeal
   path become part of the signed pack release process?

Resolved 2026-07-01:

1. The lighter, cross-cutting cooperation concept is named `alliance`.
2. `orbiplex-main` uses an org-kind threshold root; `3-of-5` is the conservative
   initial target unless the governance charter chooses a stricter threshold.
   Concrete custodian names, rotation ceremony, appeal path, and production
   signer roster remain governance deliverables, not schema questions. Runtime
   custody modes are exactly `any-authorized` and `threshold`; `threshold` means
   M-of-N unique authorized signing keys, not M-of-N people/orgs.
3. `federation-root.v1` uses `federation_id` (snake_case), deliberately matching
   its closest sibling artifact `seed-directory-trust.v1`. Config/runtime
   registry artifacts use `federation_id`; wire/domain artifacts such as Corpus
   taxonomy records may keep `federation/id`.
4. ~~Should a node ever hold root-config files for more than one federation and
   switch which is "active" without a full `data-dir` change, or should "one
   federation per `data-dir`, no exceptions" remain absolute?~~ **Resolved:**
   "one federation per `data-dir`, no exceptions" is absolute. An operator
   needing more than one federation (for example public + corporate) runs one
   `data-dir` per federation and switches which is active by choosing which to
   start the daemon against; a running instance is never concurrently a member
   of two federations. See section 2.
5. `federation_id` collisions are handled by explicit local pinning of the root
   pack digest and root keys. The string is not a global ownership claim, and
   first-seen-wins is not a trust rule.
6. Runtime should add `identity.sovereign_subject_refs[]` now, preserving
   `identity.sovereign_participant_ids[]` as the narrower participant-only
   compatibility projection. This lets an org-kind `orbiplex-main` threshold
   root be represented from the start instead of shipping a participant-only
   root that must be semantically migrated later.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Item | Status | Notes |
|---|---|---|---|
| P076-001 | Define `federation-root.v1` schema | done | `doc/schemas/federation-root.v1.schema.json` is accepted; covers exactly `peer_discovery.seeds[]`, `network.seed_directory[]`, `network.seed_directory_trust[]`, `identity.sovereign_subject_refs[]`, the participant-only compatibility projection `identity.sovereign_participant_ids[]`, plus `federation_id`, `pack_version`, attestation-root/custody refs, and self-contained `custody_policies[]`; `additionalProperties: false` at every level; `kind` constrains attestation-root id prefixes; custody policy v1 allows exactly one `federation-root` rule; `tls_certificate_sha256` and `key_public` patterns matched to the real runtime formats (base64url digest, bare multibase fingerprint); wired into `scripts/validate-json-schemas.sh` (`*.federation-root.json` mapping, next to `*.seed-directory-trust.json`); `make validate-schemas` passes. Positive example plus three negative schema-shape fixtures under `doc/schemas/examples/`; signature-validity, referenced-policy mode parity, and custody-threshold failures, including threshold-not-met, are covered by node runtime tests because JSON Schema cannot express cryptographic truth or clean cross-array references. |
| P076-002 | Promote `federation_id` from per-entry tag to node-wide config | done | Node runtime now has a node-wide `federation.federation_id` config surface and includes it in the daemon config snapshot. Config-selected non-default federation ids must match the loaded `federation-root.v1`, so `federation_id` is no longer only an attribute of individual Seed Directory trust entries. |
| P076-003 | Load `federation-root.v1` from `data-dir` at daemon startup | done | Node startup now schema-gates and loads `<data-dir>/federation-root.v1.json` when present. If no explicit file exists, startup fails closed unless the local operator explicitly enables the bundled `orbiplex-main` dev fixture. Accepted packs project seed peers, Seed Directory bootstrap/trust, and sovereign identity roots into daemon config. Explicit data-dir packs require real Ed25519 signatures over canonical payloads, participant roots must be self-signed, org roots are evaluated against self-contained `custody_policies[]`, and the loader fails closed on schema/semantic/signature/custody errors plus state downgrade/mismatch. |
| P076-004 | Ship a signed `orbiplex-main` default federation pack | partial | Node ships a bundled `orbiplex-main` federation-root fixture that exercises the runtime path and populates the four surfaces, but it is not trusted by default. Treat it as a development/demo bootstrap fixture, not production root authority, until the governance charter names concrete custodians, signer roster, rotation, and threshold ceremony. |
| P076-005 | Add a startup guard against overlapping `data-dir`/storage paths | done | Node writes a local `federation-root.state.v1.json` under the selected `data-dir` and rejects startup if the stored federation differs, if the root digest changes unexpectedly, or if the accepted `pack_version` would roll back. This preserves the "one federation per `data-dir`" invariant. The state file is an operational guard, not tamper-proof storage against a local actor who can write the data-dir. |
| P076-006 | Cross-reference Room's `federation-local`/`cross-federation` exposure docs with this proposal's node-level definition | todo | No semantic change expected; add explicit cross-reference in Solution 036. |
| P076-007 | Update Proposal 075's "Federated Homeserver Deployment" framing | done | Renamed to "Matrix as an Inter-Federation Carrier"; Executive Summary and Non-Goals now state explicitly that Matrix's homeserver-to-homeserver federation protocol is a separate mechanism from Orbiplex's own federation identity, and that adopting it is not a goal. |
| P076-010 | Ground Memarium's `ReplicationScope::Federated` in `federation_id` | done | Proposal 036 section 3.1/3.2 now defines `Federated` as bounded to peers sharing the node's `federation_id`, and section 3.3 states that cross-federation Community sharing is the existing explicit Community-to-Public promotion, never implicit group/Room membership. |
| P076-011 | Add an org-kind sovereign root surface (`identity.sovereign_subject_refs[]`) | done | Node config now has `identity.sovereign_subject_refs[]` with participant/org kind, optional custody metadata, purpose refs, and a participant-only compatibility projection into `identity.sovereign_participant_ids[]`. Org entries are representable and validated for custody metadata; org federation-root signature evaluation is implemented through self-contained `custody_policies[]` rather than being a config-shape blocker. |
| P076-012 | Verify federation-root signatures and custody policies at startup | done | The daemon canonicalizes the federation-root payload without `signatures[]`, verifies Ed25519 signatures, requires participant roots to have a matching self-signature, evaluates org roots with `any-authorized` or `threshold` custody rules for `purpose = federation-root`, counts threshold over unique authorized keys, rejects empty/missing explicit packs by default, pins/migrates the data-dir state digest, and keeps the bundled `orbiplex-main` fixture behind explicit `federation.allow_bundled_fixture_root = true` plus a raw-digest-pinned bypass so production deployments require an explicit signed data-dir pack. |
| P076-013 | Document root custodian operational separation | done | Production federation-root custodians should use dedicated participant identities and separate custodian `data-dir`s for root-pack approval, rotation, and recovery ceremony work. Public `signatures[].key_public` values and custody-policy signer sets are stable correlation handles, so ordinary participant identities, ordinary node data-dirs, and nyms must not be reused as federation-root custodians when privacy separation matters. Node-side ceremony tooling documents this operational guardrail. |
| P076-014 | Provide hard-MVP federation-root ceremony tooling | done | Node-side tooling can derive public ceremony identities from node participant mnemonics, sign root packs with PEM keys, mnemonics, plaintext participant key records, plaintext data-dirs, or encrypted participant signing keys opened through the narrow Rust unlock helper. The tool supports manifest digest verification, strict pre-assembly signature checks, per-root custody threshold verification, and an end-to-end smoke test that covers encrypted data-dir signing. This remains MVP multisig custody, not FROST/DKG threshold signing. |
| P076-008 | Define the `alliance` cross-federation cooperation concept | todo | Name resolved in this proposal; a follow-up artifact should define policy semantics only when Room/Whisper/Corpus need more than the name and boundary rule. |
| P076-009 | Update Proposal 074's harness to pin distinct federation-root files per test node | todo | Enables a testnet-style, multi-federation harness profile. |

## Next Actions

1. Convene the `orbiplex-main` governance charter to name custodians, signer
   roster, rotation, and appeal mechanics before treating the default federation
   as production-trustworthy.
2. Replace the bundled hard-MVP fixture with a real `orbiplex-main` signed pack
   once the governance charter is approved, then set production packaging to
   disable `federation.allow_bundled_fixture_root`.
3. Decide whether P076-001 should gain additional conformance fixtures for
   org-threshold positive examples, even though cryptographic/custody truth is
   already covered by node runtime tests rather than JSON Schema.
