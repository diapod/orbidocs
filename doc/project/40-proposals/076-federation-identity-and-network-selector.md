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

### 6. Sovereign Operator Identity and Official-Service Endorsement

Infrastructure capability profiles (`network-ledger`, `seed-directory`,
`offer-catalog`) carried a *sovereign operator* notion that was previously
deployment-local and vague (Proposal 025 §2/§4/§6). This proposal grounds that
notion in the federation root, and moves the federation vouch off the
`capability-passport.v1` (which stays a capability *scope* artifact) onto a
dedicated endorsement artifact:

> **Sovereign operator.** A sovereign operator of federation `F` is an identity
> present in the *active* `federation-root.v1` `identity.sovereign_subject_refs[]`
> for `F` (equivalently: one of `F`'s `attestation_roots[]`). It is defined by
> the sovereign *subject*, not by a raw signing key.

The subject-not-key distinction is what keeps threshold custody intact:

- a **participant** sovereign subject can vouch with its single key;
- an **org** sovereign subject inherits its `custody_mode`/`custody_policy_ref`,
  so vouching "as the org" MUST satisfy the same `federation-root` custody
  threshold. A single custodian key is a fraction of org authority, never a
  sovereign operator on its own (consistent with Open Questions §Resolved 2:
  threshold is M-of-N unique keys, not M-of-N people).

An **official service** is one a federation vouches for cryptographically, not
only by address. Reachability and endorsement stay stratified (Proposal 014:
address evidence is not capability authorization):

- the **address** stays a rotatable pointer (`seed_directory_bootstrap[]` here,
  or `node-address-attestation.v1`);
- the **endorsement** is a single `federation-service-endorsement.v1` artifact
  (below), signed by the federation's sovereign(s). It is deliberately *not* the
  service's operational `capability-passport.v1`: the passport carries capability
  *scope*, the endorsement carries the *federation vouch*. A single-issuer
  `capability-passport.v1` never confers official status on its own.

The endorsement carries a `signatures[]` array; the sovereign subject kind only
sets how many co-signers are required — participant = 1, org = its custody
threshold (see below).

Because signers are checked against the *active* pack, key rotation is free
revocation: when a new `pack_version` drops a subject, an endorsement whose
signer set no longer meets the requirement silently lapses. Verifiers therefore
MUST re-check signer membership on every use and MUST NOT cache an endorsement
decision across pack updates.

An official-service pointer in `federation-root.v1` (a `seed_directory_bootstrap[]`
entry, or an offer-catalog recommended by a seed directory) that carries no
resolvable sovereign endorsement MUST be treated as an unendorsed community
pointer, not as an official service. The endorsement contract and verifier rule
are defined below.

#### Sovereign subjects are governance-authored, not signature-derived

Membership of `identity.sovereign_subject_refs[]` is authored in the pack's
`attestation_roots[]` and only then signed; it is not derived from who signed.
The loader enforces the reverse constraint (every signature must tie back to an
attestation root or its custody policy — no stranger signatures), but signing a
pack never by itself confers standing sovereign-operator authority. A custodian
of an org root is a fraction of that org's authority, not an independent
sovereign subject, unless the pack also lists that identity as its own
`participant`-kind root. This keeps the sovereign-operator roster a deliberate
governance decision, immune to "signer creep".

One endorsement shape serves both subject kinds: the **same**
`federation-service-endorsement.v1` artifact, with a `signatures[]` array of
length 1..M. Subject kind only sets the required signer count:

- **participant subject →** one signature (`M = 1`) — not a different artifact,
  just the single-signer case;
- **org subject →** threshold co-signatures (`signatures[]` meeting the org's
  `federation-root` custody policy); no single custodian can vouch officially.

#### `federation-service-endorsement.v1` (the single endorsement artifact)

A thin artifact — the `signatures[]` shape of `federation-root.v1`, a distinct
domain — by which a federation's sovereign(s) vouch for an official service. One
artifact serves both subject kinds: `signatures[]` of length 1 for a participant
subject, `M`-of-N for an org subject. It stays separate from the service's
operational `capability-passport.v1`: the passport carries *scope*, the
endorsement carries *the federation's vouch*.

Minimal contract sketch:

- binds `federation_id`, service `node_id`, `capability_id`
  (`seed-directory` | `offer-catalog` | ...), `issued_at`, `expires_at`,
  optional `policy_ref`, optional `revocation_ref` (where endorsement
  revocations are expected to appear), and an `endorsement_id`;
- names the **endorsing sovereign subject** in `endorser_subject_ref`
  (`(participant|org):did:key:...`), which MUST be present in the verifier's
  active `identity.sovereign_subject_refs[]`. The artifact names the subject
  explicitly rather than inferring it from the signers, so the verifier knows
  *which* custody policy applies even with several org roots or overlapping keys;
- `signatures[]` — one `{key_public, value}` per co-signer, each over
  `federation-service-endorsement.v1\x00 || canonical JSON/JCS payload_without_signatures`
  (domain separator distinct from `federation-root.v1`, so a root-pack signature
  can never be replayed as an endorsement, or vice versa);
- `additionalProperties: false`; unknown top-level fields rejected.

Verifier acceptance:

1. each signature verifies over the canonical payload;
2. resolve `endorser_subject_ref` in the active `identity.sovereign_subject_refs[]`
   (else reject). If the subject is `kind = participant`, its own key MUST be the
   sole signer. If the subject is `kind = org`, the signatures MUST satisfy *that
   org's* `federation-root` custody policy — the custodian keys sign *on behalf
   of* the org and are **not** themselves sovereign subjects (this is exactly why
   the artifact names the subject rather than inferring authority from the
   signers, preserving "governance-authored, not signature-derived"). The local
   `endorsement-multiplicity` policy (below) may raise the bar. Rotation that
   removes the subject, or drops its satisfying signer set below the requirement,
   lapses the endorsement (re-check on every use, no cross-pack caching);
3. `capability_id`/`node_id` match the service being consumed, `expires_at` is
   in the future, and `endorsement_id` is not revoked.

#### Endorsement acquisition is source-agnostic

The endorsement is a self-verifying artifact, so **where a consumer got it
carries no authority**. A consumer verifying an official service MAY rely on
whichever copy is available:

1. a **locally cached** endorsement (obtained earlier, still unexpired),
2. the **Seed Directory** read surface (`GET /cap*` `endorsement` field,
   Proposal 025 §3),
3. the **serving node itself** — the existing
   `capability-advertisement.v1` `capabilities_presented[].endorsements[]`
   slot already carries "federation or issuer endorsement artifacts" over the
   post-handshake capability exchange (Proposal 014 §4), so the service can
   present its own proof without any directory round-trip.

Verification is **identical regardless of source**: resolve
`endorser_subject_ref` in the consumer's *active* root, check signer set,
expiry, and revocation. Provenance never substitutes for verification, and a
copy from a "more trusted" source grants nothing extra — freshness, revocation,
and the active root are the only discriminators.

**Single-exchange verification (no connect-time round-trips).** The normal
path is: the client connects, and the P014 session baseline already delivers
everything in one capability exchange — `capabilities_presented[]` carries the
`passport` *and* `endorsements[]` in the same message. From there,
official-status verification is **pure local computation**: the active
federation root (loaded from the `data-dir`), the local revocation view
(background-polled per Proposal 025 §5, bounded staleness by design), and the
clock. A consumer MUST NOT need a live Seed Directory query to decide official
status at connect time — the directory is discovery and revocation *feed*, not
per-connection authority. Service nodes SHOULD therefore include their current
endorsement in every capability advertisement for their official capabilities
(the P076-023 cache keeps it at hand).

#### Endorsement multiplicity policy (verifier-local)

A consuming node (and a Seed Directory at registration) MAY require *more* than
the subject-kind default through a local `endorsement-multiplicity` policy:

- `subject-default` — participant subject = 1, org subject = its custody
  threshold (the §6 default);
- `mirror-root-threshold` — require the federation root's own custody threshold
  regardless of subject kind;
- `explicit-N` — require at least `N` distinct sovereign co-signers.

Policy raises, never lowers, the bar. An "official" service whose available
endorsement does not meet the effective requirement downgrades to an unendorsed
community pointer; it never fails open to "official".

Multiplicity counts **signers within the named `endorser_subject_ref`**, not
distinct sovereign subjects: a participant subject always yields exactly one
accepted signer, so `explicit-N` with `N > 1` deliberately makes
participant-endorsed services unacceptable under that local policy. A future
policy that requires vouches from several *distinct* sovereigns would count
distinct valid endorsement artifacts (one per subject), not signatures inside
one artifact; that is out of scope for v1.

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
- `federation-service-endorsement.v1` (new, §6) — the sole official-service
  *endorsement* artifact: a thin multi-signature (1..M) vouch naming the
  endorsing sovereign subject (`endorser_subject_ref`) and the endorsed
  `node_id`/`capability_id`.
- `capability-passport.v1` (existing, Proposals 024/025) — unchanged, used only
  for capability *scope*/advertisement; it never confers official status (§6).

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
| An "official" `seed-directory`/`offer-catalog` is trusted from its address alone, with no resolvable sovereign endorsement | Address authority is mistaken for federation authority; a swapped pointer inherits "official" trust | Treat an official-service pointer without a valid `federation-service-endorsement.v1` (endorsing subject ∈ active `sovereign_subject_refs[]`; participant = its key, org = custody met) as an unendorsed community pointer; never fail open to "official" (§6). |
| A sovereign subject is rotated out but its previously issued service passports keep being honored | Stale endorsement outlives the federation's trust in that key | Verifiers resolve issuer against the *active* pack on every use and MUST NOT cache an endorsement decision across `pack_version` updates; rotation lapses endorsement for free (§6). |

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
4. For an official-service pointer in `federation-root.v1`, should a resolvable
   `federation-service-endorsement.v1` be *required* (fail-closed:
   an unendorsed "official" entry refuses to load) or *advisory* (loads but is
   marked an unendorsed community pointer)? §6 recommends advisory for
   community/address-only directories and required for anything the pack labels
   "official"; the exact default per capability profile is open.

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
| P076-015 | Ground "sovereign operator" in the federation root | done | The §6 definition now treats a sovereign operator of federation `F` as a subject in `F`'s active `identity.sovereign_subject_refs[]`; participant subjects vouch with their own key and org subjects are held to their `federation-root` custody policy. Proposal 025 §2/§4/§6 now uses this split: `capability-passport.v1` is scope-only, while official-service status is carried by `federation-service-endorsement.v1`. |
| P076-016 | Enforce federation-endorsement resolution in the loader and `capability-binding` | partial | `capability-binding` now contains the pure verifier core for `federation-service-endorsement.v1`: it resolves `endorser_subject_ref` against a supplied active sovereign-subject snapshot, verifies domain-separated Ed25519 signatures over canonical JSON/JCS payloads, enforces participant sole-signer and org custody-threshold semantics, rejects duplicate signer inflation, checks revocation/time/node/capability context, and applies verifier-local `endorsement-multiplicity`. Remaining work: wire this core into loader/Seed Directory consumers and official/community projections, with rotation-triggered re-checks on every use. |
| P076-017 | Define `federation-service-endorsement.v1` (single endorsement artifact, 1..M signatures) | done | `doc/schemas/federation-service-endorsement.v1.schema.json` defines the single endorsement artifact with `additionalProperties: false`, explicit `endorser_subject_ref`, `federation_id`, `node_id`, `capability_id`, validity window, optional policy/revocation refs, and `signatures[]`. Positive and negative fixtures are synced into `node/protocol/contracts`; `schema-gate` exposes dedicated ingress/export validators and rejects import-boundary use. The node verifier core uses the same domain separator and canonical JSON/JCS signing payload. §6. |
| P076-018 | New offline ceremony process for joint-issuance endorsements | todo | **High priority.** A ceremony command/sibling producing a threshold-cosigned `federation-service-endorsement.v1`, reusing the digest → collect-detached-signatures → assemble → verify *pattern* of the federation-root ceremony but with the endorsement's own domain separator and payload. Extends P076-014 tooling; the MVP path for the Option-1 decision. Note: the current ceremony signs only `federation-root` payloads, so this is new tooling surface, not reuse of an existing command. |
| P076-019 | Post-MVP remote co-signing protocol for endorsements | deferred | Transport-agnostic protocol letting sovereign signers add detached signatures over a shared endorsement digest without an in-person ceremony. Guardrails: every signer verifies the exact digest/payload before signing (no "trust and sign"); deterministic assembly; the channel carries detached signatures, not authority. Transport is undecided — messaging plus an attachment primitive is one candidate, not a commitment; any attachment primitive would need its own bounded spec first. |
| P076-020 | Ceremony option to author `attestation_roots[]`/`sovereign_subject_refs[]` from supplied keys | todo | Operator-owned follow-up (tracked for visibility). Let the ceremony optionally author `participant`-kind roots from a supplied key set instead of requiring the roots to be hand-authored in the pack beforehand. Must preserve the governance-authored guarantee: the resulting roster stays an explicit, signed decision, never silently signature-derived. |
| P076-021 | Make `federation-service-endorsement.v1` the sole proof of "official" status | todo | **High priority.** Consumers, Seed Directory registration, and the loader accept ONLY a valid `federation-service-endorsement.v1` (participant `M=1`, org `M`-of-N under custody plus local `endorsement-multiplicity`) as conferring official / federation-endorsed status; a single-issuer `capability-passport.v1` is scope/advertisement only and never confers "official" on its own. Update Proposal 025 §2/§4/§6 and any `capability-binding` path accordingly. Negative test: a lone single-issuer seed-directory passport is not treated as official. |
| P076-022 | Operator UI for issuing official-service endorsements for non-own services | todo | **High priority.** The node has local passport issuance and capability-advertisement publication surfaces, but no operator flow for a *sovereign* to endorse someone else's service. Add an operator UI/API surface where a sovereign operator enters (or picks) a target `node_id`, selects the official capability from a menu (`seed-directory`, `offer-catalog`, …), and the node builds the `federation-service-endorsement.v1` (participant subject signs locally; org subject hands off to the P076-018 ceremony), then announces it via the Seed Directory attach endpoint (`PUT /cap/{node-id}/{capability-id}/endorsement`, P025 §3) with the retryable `scope-entry-missing` backoff (`5s → 30s → 120s → 360s`). Preconditions surfaced in the UI: the local identity resolves to an active sovereign subject; the target node has (or will have) a node-signed scope entry. |
| P076-023 | Endorsed-node periodic endorsement fetch and local cache | todo | **High priority.** A node that is the *subject* of an endorsement should not depend on Seed Directory availability to prove "I am an official service". Add a bounded periodic task (default ~30 min, jittered) that queries the configured Seed Directories for endorsements targeting the node's own `node_id` (+ advertised official capabilities), verifies each via `capability-binding::verify_federation_service_endorsement` against the active federation root, and caches verified artifacts locally (persisted, TTL-bounded by `expires_at`). The cached endorsement is then presentable to peers directly (independent proof), while acceptance on the consumer side still re-checks against *their* active root on every use. Facts for fetched/verified/lapsed endorsements; refusal to cache anything that fails verification. Presentation to peers uses the existing `capability-advertisement.v1` `capabilities_presented[].endorsements[]` slot (source-agnostic acquisition, §6) rather than widening `capability-passport-present.v1`. |

## Implementation Recommendations

Task-level guidance for the tracker entries above, aligned with
`node/DEV-GUIDELINES.md`. The goal is a smooth, layered implementation with no
entanglement surprises. Registration-surface details live in Proposal 025
(P025-002/003/004); this section covers the node-side chain.

### Layering map for the endorsement chain

```
protocol/contracts        schema + fixtures (federation-service-endorsement.v1)
  → schema-gate           ingress/export boundary validation (shape only)
  → capability-binding    pure verifier: no IO, no clock ownership, no config
  → daemon                host adapters: authority snapshot from the loaded
                          federation root, decision surface, facts, cache
  → seed-directory        registration / attach / read projection (P025 §2–§3)
  → node-ui / operator    thin surface over host APIs; never touches keys
```

Keep the verifier **pure**: `capability-binding::federation_endorsement` takes
an explicit `now_rfc3339`, an explicit authority snapshot, and an explicit
revocation set. It must never read config, storage, or the system clock —
callers own time and state. This is what makes threshold semantics testable
without a daemon.

### P076-015 — grounding the definition (done; invariant to preserve)

- The definition landed in the schema descriptions and `x-dia-basis`. If ever
  revisiting those descriptions, keep the pointers: the §6 note in
  `capability-passport.v1.schema.json` and the §6 pointer next to
  `seed_directory_bootstrap`/`endorsement_refs` in
  `federation-root.v1.schema.json`.
- **Do not** add new envelope fields to `capability-passport.v1`. It stays a
  scope artifact; the federation binding is a verifier rule, not schema shape.

### P076-016 — runtime verification in the daemon

- Build the authority snapshot **once per loaded pack**, in the same place the
  loader already projects `attestation_roots[]`:

  ```rust
  // daemon: derived alongside identity.sovereign_subject_refs projection
  FederationSovereignSubjectSnapshot::try_new(
      federation_id,
      subjects, // Participant { id } | Org { id, policy: mode + authorized_* }
  )
  ```

  Map `custody_policies[]` rules (purpose `federation-root`) into
  `FederationSovereignOrgPolicy` exactly as `validate_org_federation_root`
  reads them — one source of custody truth, two consumers.
- Surface the outcome as a **typed decision**, not a bool or string:

  ```rust
  enum OfficialStatusDecision {
      FederationEndorsed { endorsement_id: String, endorser_subject_ref: String },
      ScopeOnly { reason: OfficialStatusRefusal },  // community pointer
  }
  ```

  Downgrade is data, not an error branch — consumers route on it.
- Re-verify **on every use**. If profiling ever justifies a cache, key it by
  `(endorsement_id, pack_digest)` so a pack update invalidates implicitly.
- **Do not**: cache across `pack_version`; treat custodian keys as subjects;
  expose the verifier to module callers directly (host-owned surface, same
  posture as the Agent lifecycle capabilities); let a failed endorsement check
  abort an otherwise valid scope connection unless local policy demands it.

### P076-017 — the artifact contract (verifier core landed)

- Fixture wiring is covered: the positive and `invalid/missing-endorser`
  fixtures are exercised by `schema-gate/tests/networking_contracts.rs`.
  Remaining: add an `invalid/` fixture per rejection class the runtime
  distinguishes (tampered payload, duplicate signer, sub-threshold).
- Signing input stays `federation-service-endorsement.v1\x00 ||
  canonical_json(JcsV1, payload_without_signatures)` — config-registry family,
  like `federation-root.v1`. **Do not** switch to the CBOR wire-envelope
  family or reuse the root domain separator.
- **Do not** put endpoints, addresses, or TLS material into the endorsement —
  reachability stays in advertisements (§6 stratification).
- The verifier uses a 30s clock-skew tolerance for `issued_at`
  (`ISSUED_AT_CLOCK_SKEW_TOLERANCE`, mirroring the P014 handshake window);
  `expires_at` stays exact. Keep that asymmetry — skew absorbs issuance races,
  never extends validity.

### P076-018 — offline ceremony for endorsements

- Sibling command set in `tools/federation-root-ceremony`, reusing the
  digest → collect detached signatures → assemble → verify *pattern* with:
  - its **own** manifest schema string and the endorsement domain separator,
  - passphrases via stdin only (as the unlock helper enforces), never argv,
  - a signer-side sanity resolve of `endorser_subject_ref` against a provided
    root pack **before** signing (fail early), while authoritative truth stays
    verifier-side.
- **Do not**: reuse the `federation-root-ceremony-manifest.v1` schema string;
  sign before `endorser_subject_ref` and all payload fields are final (any
  later mutation invalidates signatures — TOCTOU discipline as in the whisper
  preflight); auto-derive the endorser subject from whichever key signs.

### P076-020 — authoring roots from supplied keys (operator-owned)

- Explicit flag (e.g. `--author-participant-roots key1,key2`), echo the
  resulting roster, require confirmation, and write `attestation_roots[]`
  **before** computing the manifest digest (the payload changes it).
- **Do not** derive the roster from signature files discovered on disk — that
  reintroduces signature-derived authority.

### P076-021 — cutover to endorsement-only official status

- Land read/verify paths (P076-016/017, P025 read surface) before flipping any
  consumer to *require* endorsements; existing scope-only registrations remain
  valid community entries — the cutover changes what "official" means, not
  what is stored.
- Gate the flip behind a config default so a deployment can stage it; the
  negative test "lone single-issuer passport ≠ official" is the cutover's
  definition of done.

### P076-022 — operator UI for endorsing non-own services

- Thin UI over a host API; the request DTO is closed:

  ```
  { "node_id": "node:did:key:z...",         // target service node
    "capability_id": "seed-directory",      // from a closed menu of official
                                            // profiles, never free text
    "expires_at": "...",                    // bounded default, e.g. 90 days
    "policy_ref": "..." (optional) }
  ```

- Participant subject: sign through the signer service (UI never holds keys).
  Org subject: emit an *unsigned* endorsement + ceremony manifest for
  P076-018 instead of signing inline — the UI must not pretend one custodian
  can issue.
- Submit via the P025 attach endpoint honoring the retryable
  `scope-entry-missing` backoff (`5s → 30s → 120s → 360s`); terminal `403` is
  surfaced to the operator, never retried.
- Leave facts: `endorsement/drafted`, `signed`, `submitted`, `attach-retried`,
  `attach-gave-up` — the operator must be able to reconstruct why an
  endorsement did or did not land.

### P076-023 — endorsed-node fetch and cache

- Bounded periodic worker (default ~30 min, jittered like the peer-runtime
  backoff helpers), querying configured Seed Directories for endorsements
  targeting the node's own `node_id`.
- Verify **before** storing, against the node's active root. Suggested cache
  row (storage layer, byte-preserving):

  ```
  endorsement_id (PK) | node_id | capability_id | endorser_subject_ref
  | expires_at | verified_at | pack_digest_at_verification | raw_artifact_bytes
  ```

  `raw_artifact_bytes` byte-identical for re-presentation; `pack_digest` so a
  root update triggers re-verification of every cached row.
- Presenting from cache is fine — consumers re-verify against *their* root
  anyway (P025 §4 step 6), so the cache is availability, not authority. The
  wire slot already exists: present the cached artifact through
  `capability-advertisement.v1` `capabilities_presented[].endorsements[]`
  (§6, "source-agnostic"). **Do not** smuggle it through
  `capability-passport-present.v1`'s `additionalProperties: true` — that slot
  is a single-passport contract; widening it silently is exactly the
  silent-laxity anti-pattern.
- **Do not**: extend usable lifetime beyond `expires_at`; tighten the poll
  interval on failure (back off instead); cache anything that failed
  verification; treat a directory outage as loss of official status (the
  cached, unexpired endorsement keeps serving).

### P076-019 (deferred) — remote co-signing

Keep transport-agnostic. Whatever carries detached signatures, each signer
verifies the exact digest before signing, assembly stays deterministic, and
the channel carries signatures — never authority.

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
4. Implement the official-service endorsement chain in dependency order (high
   priority): **P076-015** (ground the definition in docs/schema notes) →
   **P076-017** (the `federation-service-endorsement.v1` contract; now done)
   → then in parallel **P076-018** (ceremony tooling that produces
   endorsements) and the remaining **P076-016** wiring (loader/Seed Directory
   consumers; verifier core in `capability-binding` is done) → **P025-003**
   (node-signed advertisement at
   `PUT /cap`; independent, can start any time — precondition of the attach
   rule) → **P025-002** (Seed Directory registration/consumption incl. two-phase
   endorsement-attach and the official/endorsement read-surface projection;
   needs P076-016/017 and P025-003) with **P025-004** (endorsement revocation in
   the shared revocation log) riding alongside → **P076-021** (cutover:
   endorsement becomes the sole proof of "official"). **P076-020** is an
   independent operator-owned ceremony ergonomics task; **P076-019** stays
   deferred post-MVP.
