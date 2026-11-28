# Federation Root and Network Selector

Based on:

- `doc/normative/40-constitution/en/CONSTITUTION.en.md`
- `doc/normative/50-constitutional-ops/en/FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`
- `doc/project/40-proposals/079-cross-federation-alliance.md`
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`
- `doc/project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md`
- `doc/normative/50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md`
  (`DIA-ROOT-001` — governance charter for the `orbiplex-main` root)

Related schemas:

- `federation-root.v1`
- `federation-service-endorsement.v1`
- `federation-service-endorsement-revocation.v1`
- `seed-directory-query-attestation.v1`
- `capability-passport-present.v1`
- `capability-advertisement.v1`

Adjacent policy contracts:

- `alliance-policy.v1` (canonical cross-federation admission input; one-half
  verifier and active-alliance resolver live in Proposal 079; consumer-specific
  admission enforcement remains deferred)

## Status

Implemented hard-MVP solution foundation.

Federation root activation, official-service endorsement verification, Seed
Directory bootstrap projection, optional Seed Directory bootstrap TLS pinning,
restart-only root changes, production `orbiplex-main` ceremony profile checks,
and explicit-roster root draft authoring are implemented. Remote co-signing and
final production roster/packaging remain activation and post-MVP hardening.

Production trust in `orbiplex-main` is additionally gated by governance, not
only code: the root charter (`DIA-ROOT-001`,
`doc/normative/50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md`)
is adopted at version 0.1.0, but production activation still requires a filled
Guardian roster and keys before the bundled fixture is replaced by a
production pack and `federation.allow_bundled_fixture_root` is disabled
(P076-004).

## Date

2026-07-03

## Executive Summary

Federation Root and Network Selector defines the local trust anchor that binds a
node to one federation's identity, official service policy, Seed Directory
bootstrap set, and routing/discovery defaults.

Key Guardians hold the keys that sign the federation root pack under its custody
policy. Verifying the pack establishes the technical trust domain. A community's
constitution, its membership and the mandate to represent it require separate
evidence. The active selector and root cannot serve as a record of constitutional
adoption (see the [proposed jurisdiction rule](../../../normative/40-constitution/en/CONSTITUTION.en.md#const:norm.13)).

The root does not make remote facts true by itself. It defines which local
policy material may be used to evaluate official-service endorsements,
bootstrap candidates, Seed Directory trust, and federation-scoped discovery.
Runtime consumers still verify artifacts at each use site.

The intended first public federation is named **Emergat**, with primary domain
`emergat.org`, under [P102](../../40-proposals/102-community-brand-and-naming-layers.md).
Its technical selector remains `orbiplex-main`. A public name or domain supplies
neither root authority nor evidence of production activation; the gates in
the Status section still apply. This naming does not extend to other federations.

**Planned presentation extension:** P076-BRAND-001 owns name, optional localized
tagline/description, optional homepage and optional embedded PNG logo in
versioned root configuration, plus a bounded projection from the verified active
root. It is not implemented by the existing
closed v1 schema. Only explicitly public fields may enter a public UI shell;
restricted fields retain existing read guards. P102-006 consumes that projection
for a name heading, tagline below it and `powered by Orbiplex.AI` footer. Reuse
signing, ceremony and restart-only activation; no separate branding authority or
ordinary overlay may impersonate root metadata. See the
[owner contract](../../40-proposals/076-federation-identity-and-network-selector.md#federation-presentation-metadata-planned).

Cross-federation cooperation is deliberately above this component. Proposal
079's `alliance-policy.v1` runtime foundation can verify unilateral policy
halves and resolve an active alliance from matching fresh halves. It may become
an admission input for Room, Whisper, Corpus, Artifact Delivery, INAC, or Agora
bridging, but it does not change the single active `federation_id` selected by
this solution and does not substitute for federation-root or official-service
verification.

## Context and Problem Statement

Several subsystems needed a shared answer to the same question: "which
federation am I acting within, and whose authority counts for this scope?"

Without a federation root, official Seed Directory status, capability
endorsement, transport trust, Corpus taxonomy scope, Room federation policy, and
bootstrap peer selection would each drift into local configuration conventions.

## Proposed Model / Decision

`federation-root.v1` is the governance-authored root pack for a federation. It
defines:

- `federation/id`;
- sovereign subject refs;
- official service endorsement policy;
- Seed Directory bootstrap entries;
- route/network selector defaults;
- revocation and ceremony metadata.

Official service status is carried by `federation-service-endorsement.v1`, not
by capability passports alone. Consumers must verify endorsements against the
active federation root before treating a service as official.

**Planned consumer, P058-024.** For [alias allocation](../025-contact-catalog/025-contact-catalog.md#alias-allocation-authority),
the active federation configuration must authenticate the selected allocation
policy and its revision. The initial policy designates one writer by stable
node identity. Its current endpoint is discovered through Seed Directory.
The existing bootstrap entries suffice for locating that directory. P058-024
still has to specify and test the binding between the configuration and the
policy before clients can rely on it.

Root activation is restart-only. Runtime reload may validate candidate config,
but changing the active root fingerprint requires daemon restart so a federation
identity switch cannot happen as an incidental hot reload.

Acceptance profile seeders must exercise the same authority model as runtime:
local testnet roots are explicit signed `federation-root.v1` files, and any
bootstrap Seed Directory claimed as `federation-endorsed` carries an inline
signed `federation-service-endorsement.v1`. These seeders are intentionally
single-participant/single-secret local fixtures; production org/threshold roots
must use the ceremony tooling instead.

## Must Implement

### Federation Root Contract

Based on:

- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`

Related schemas:

- `federation-root.v1`

Responsibilities:

- define the federation id, sovereign subject refs, bootstrap entries, and
  policy roots;
- require explicit `seed_directory_bootstrap[].enabled`;
- reject malformed root material before runtime consumers can use it;
- keep activation fingerprint stable for the process lifetime.

Status:

- `done`

### Official-Service Endorsements

Based on:

- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`

Related schemas:

- `federation-service-endorsement.v1`
- `federation-service-endorsement-revocation.v1`

Responsibilities:

- make `federation-service-endorsement.v1` the sole proof of official-service
  status;
- verify endorsement signatures, validity windows, signer authority, node id,
  and capability id against the active root;
- apply endorsement revocations before projecting official status;
- preserve scope-only capability passports as non-official unless an active
  endorsement is present.

Status:

- `done`

### Seed Directory Bootstrap and Discovery Policy

Based on:

- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`

Related schemas:

- `federation-root.v1`
- `seed-directory-query-attestation.v1`

Responsibilities:

- project enabled Seed Directory bootstrap entries from the active root;
- downgrade bootstrap entries without verified official endorsement to
  community/advisory status;
- apply one strict multi-directory policy across host queries, AD/capability
  routing, subject lookup, and Contact Catalog provider discovery;
- expose safe trusted-directory diagnostics and replay status.

Status:

- `done`

### Acceptance Profile Root Seeding

Based on:

- `doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`

Related schemas:

- `federation-root.v1`
- `federation-service-endorsement.v1`

Responsibilities:

- write explicit signed federation-root packs into acceptance profile data
  directories;
- refresh placeholder bootstrap node ids to runtime `node:did:key` values after
  first daemon boot;
- embed signed `seed-directory` endorsements for bootstrap Seed Directory
  entries that claim `federation-endorsed`;
- keep those local acceptance endorsements bounded in time and refresh them by
  rerunning the profile seeder or managed smoke, instead of treating acceptance
  fixtures as long-lived production authority;
- support acceptance roots that include runtime-created participant attestation
  roots with matching self-signatures, so local provider passport issuance and
  requester verification exercise the active federation-root sovereign
  projection rather than an unsigned config override;
- keep pre-first-boot roots allowed to omit Seed Directory bootstrap entries
  until runtime DID node ids are known;
- keep local acceptance roots separate from production org/threshold custody
  roots;
- avoid loose trust-list shortcuts as a substitute for root-backed authority.

Status:

- `done`

### Root-Ceremony and Endorsement Tooling

Based on:

- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`

Related schemas:

- `federation-root.v1`
- `federation-service-endorsement.v1`

Responsibilities:

- support offline digest, detached signing, deterministic assembly, and verify
  commands for root and endorsement artifacts;
- enforce the production `orbiplex-main` ceremony profile for manifest,
  assembly, and verification;
- generate passphrase-encrypted PEM Guardian keys by default, with plaintext
  PEM output limited to explicit disposable fixtures;
- allow participant mnemonic, data-dir, and key-record signing variants;
- reject unknown or unauthorized signers in strict mode;
- keep org-governed issuance ceremony-bound rather than pretending one
  Guardian can issue.
- keep Guardian identity and operator identity stratified: a Guardian key may
  attest or authorize a separate operator identity through an explicit binding,
  but tooling MUST NOT convert, promote, or derive that key into a full operator
  identity.

Status:

- `done` for the implemented ceremony tooling and production `orbiplex-main`
  profile checks; the root charter is adopted, while concrete production
  roster/keys remain activation-authored.

## May Implement

### Alliance Policy Distribution Binding

Planned distribution continuation:
[P079-005a–005c](../../40-proposals/079-cross-federation-alliance.md#distribution-implementation-recommendations)
compose policy-half/revocation exchange with AD/INAC after local import/export.
This does not change this solution's root authority: fetched packs are evidence
against independently admitted roots, never permission to replace the active root.
An independent narrow delivery grant must allow bootstrap exchange without first
accepting the alliance being delivered. Candidate receipt and alliance activation
remain distinct; private policies cannot fall back to public publication.

### Remote Co-Signing Protocol

Based on:

- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`

Related schemas:

- `federation-service-endorsement.v1`

Responsibilities:

- let sovereign signers add detached signatures over a shared digest through a
  bounded protocol;
- preserve verify-before-sign behavior;
- keep transport separate from authority.

Status:

- `deferred`

### Seed Directory TLS Pinning

Based on:

- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md`

Related schemas:

- `federation-root.v1`

Responsibilities:

- optionally carry a Seed Directory transport certificate pin in bootstrap
  entries;
- treat the pin as transport privacy/integrity material, never as service
  authority;
- require HTTPS when the pin is present and verify the peer leaf certificate
  digest on source-aware Seed Directory client paths;
- reject duplicate manual Seed Directory endpoint entries whose pins differ
  within bootstrap entries, within trust entries, or across the bootstrap and
  trust surfaces;
- use a single active pin per endpoint in MVP; certificate rotation requires a
  higher `pack_version`, a new signed root pack, and daemon restart;
- coordinate schema, loader, fixtures, and compatibility notes in one change.

Status:

- `done`

## Out of Scope

- treating WebPKI or a Seed Directory response as federation authority by
  itself;
- switching active federation roots during hot reload;
- making capability passports official without endorsements;
- deriving full operator identities from federation-root signing keys;
- enforcing consumer-specific cross-federation admission; Proposal 079 defines
  the minimal alliance policy contract plus runtime verifier/resolver
  foundation, while Room/Whisper/Corpus/AD/INAC/Agora hooks remain future
  layers;
- replacing TLS trust policy or Seed Directory replay semantics.

## Consumes

- federation root packs;
- official-service endorsements and revocations;
- Seed Directory bootstrap configuration;
- TLS trust and endpoint evidence policy.

## Produces

- active federation authority snapshots;
- official-service verification decisions;
- trusted directory and bootstrap projections;
- root activation diagnostics.

## Related Capability Data

- `041-federation-root-caps.edn`
