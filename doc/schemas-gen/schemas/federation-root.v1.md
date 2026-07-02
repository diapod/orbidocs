# Federation Root v1

Source schema: [`doc/schemas/federation-root.v1.schema.json`](../../schemas/federation-root.v1.schema.json)

Data-dir-scoped root config file (the 'federation pack') loaded at daemon startup and merged into runtime configuration. It is the local, signed source of truth for exactly four daemon configuration surfaces: `peer_discovery.seeds[]`, `network.seed_directory[]`, `network.seed_directory_trust[]`, and the sovereign identity-root surface (`identity.sovereign_subject_refs[]` plus the participant-only compatibility projection `identity.sovereign_participant_ids[]`). This is a config-registry artifact (same family as `seed-directory-trust.v1`), not a peer-to-peer wire envelope (contrast `node-advertisement.v1`), so it follows that family's snake_case field convention rather than the `noun/attribute` convention used by signed inter-node messages. A federation-root file that carries any field outside this schema MUST be rejected, not silently ignored.

## Governing Basis

- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)
- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`](../../project/40-proposals/054-user-maintained-federated-seed-directory.md)
- [`doc/project/60-solutions/021-agora-authority/021-agora-authority.md`](../../project/60-solutions/021-agora-authority/021-agora-authority.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-008-org-subject-rollout.md`](../../project/50-requirements/requirements-008-org-subject-rollout.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federation-root.v1` | Schema discriminator. |
| [`federation_id`](#field-federation-id) | `yes` | string | Network selector this pack describes (chain-id analogy: mainnet/testnet). Distinct from the wire-envelope `federation/id` used by `node-advertisement.v1` and Corpus taxonomy records — see Proposal 076 Open Question 3. A running node has exactly one active `federation_id`, bound to its `data-dir`; it is never a multi-valued or per-request field here. |
| [`pack_version`](#field-pack-version) | `yes` | integer | Monotonic revision counter for this federation's pack, analogous to `node-advertisement.v1`'s `sequence/no`. A loader MUST reject a pack whose `pack_version` is lower than the last one it accepted for this `federation_id`, to prevent downgrade/replay of a revoked or superseded pack. |
| [`issued_at`](#field-issued-at) | `no` | string | Optional timestamp when this pack revision was produced. Diagnostic only; `pack_version` is the authoritative ordering, not this timestamp. |
| [`attestation_roots`](#field-attestation-roots) | `yes` | array | This federation's OWN canonical top-level anchor(s). NOT a copy of any relay's local Agora Authority `authority_roots[]` (Solution 021) — those are narrower, per-namespace, per-relay policy that MAY adopt an entry here as their namespace default, but are never required to equal this list. |
| [`bootstrap_seed_peers`](#field-bootstrap-seed-peers) | `no` | array | This federation's static WSS seed peers (Proposal 014's 'mandatory first bootstrap layer'), resolving to `peer_discovery.seeds[]`. Deliberately flat — one endpoint per entry, no priority/enabled toggle — to match today's `DaemonSeedPeerConfig` exactly; richer multi-endpoint peer entries would require enriching that struct first, which this schema does not assume. |
| [`seed_directory_bootstrap`](#field-seed-directory-bootstrap) | `no` | array | This federation's own canonical default trusted Seed Directories. Each entry fans out to two existing daemon config surfaces at load time: `network.seed_directory[]` (endpoint/node_id/passport) and `network.seed_directory_trust[]` (trust_level/weight/passport_ref/policy_ref/endorsement_refs/reputation_ref/enabled). The loader MUST fill `network.seed_directory_trust[].federation_id` from this pack's own top-level `federation_id`; it is not repeated per entry here. |
| [`federation_service_endorsement_revocations`](#field-federation-service-endorsement-revocations) | `no` | array | Optional signed `federation-service-endorsement-revocation.v1` artifacts known at root-pack activation time. Loaders use these revocations when deciding whether inline Seed Directory bootstrap endorsements may confer federation-official status. |
| [`custody_policies`](#field-custody-policies) | `no` | array | Self-contained organization custody policies referenced by `attestation_roots[].custody_policy_ref`. MVP loaders resolve policy refs inside this same federation-root pack, so bootstrap does not depend on an external policy registry. |
| [`policy_ref`](#field-policy-ref) | `no` | string | Optional reference to the policy document governing this federation's root and bootstrap decisions. |
| [`endorsement_refs`](#field-endorsement-refs) | `no` | array | Optional references to endorsement facts supporting this pack's trust claims (for example community-elected public-service recognition), carried via the existing `reputation-signal.v1` mechanism rather than a new primitive. |
| [`signatures`](#field-signatures) | `yes` | array | Signatures over the canonical payload (every field above, excluding `signatures` itself). A local, self-authored federation-root file is still signed by its own operator-held root key(s) — 'self-signed' is a valid case, 'unsigned' is not. Which keys and how many are required is governed by whatever custody mode/policy applies to this federation's `attestation_roots[]` entries (see Proposal 076 section 4 and its resolved custody-mode decision), not by this schema. Runtime threshold evaluation is over unique signing keys, not over externally asserted people or organizations. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`AttestationRoot`](#def-attestationroot) | object |  |
| [`BootstrapSeedPeer`](#def-bootstrapseedpeer) | object | Mirrors `DaemonSeedPeerConfig` field-for-field (daemon/src/config.rs:761). |
| [`SeedDirectoryBootstrap`](#def-seeddirectorybootstrap) | object | Fans out to `DaemonSeedDirectoryConfig` (daemon/src/config.rs:528) and `DaemonSeedDirectoryTrustConfig` (daemon/src/config.rs:551) at load time. |
| [`CustodyPolicy`](#def-custodypolicy) | object |  |
| [`CustodyRule`](#def-custodyrule) | object |  |
| [`Signature`](#def-signature) | object |  |
| [`FederationServiceEndorsement`](#def-federationserviceendorsement) | object | Embedded form of `federation-service-endorsement.v1` used only so a bootstrap Seed Directory can be verified before any directory is trusted. Runtime verification still enforces signature, custody, time, federation, node, and capability invariants. |
| [`FederationServiceEndorsementRevocation`](#def-federationserviceendorsementrevocation) | object | Embedded startup-time endorsement revocation. Runtime Seed Directory verification remains authoritative for live feeds; this root-pack form lets startup bootstrap apply known withdrawals before trusting inline official-service proofs. |
| [`FederationServiceEndorsementSignature`](#def-federationserviceendorsementsignature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-root.v1`

Schema discriminator.

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

Network selector this pack describes (chain-id analogy: mainnet/testnet). Distinct from the wire-envelope `federation/id` used by `node-advertisement.v1` and Corpus taxonomy records — see Proposal 076 Open Question 3. A running node has exactly one active `federation_id`, bound to its `data-dir`; it is never a multi-valued or per-request field here.

<a id="field-pack-version"></a>
## `pack_version`

- Required: `yes`
- Shape: integer

Monotonic revision counter for this federation's pack, analogous to `node-advertisement.v1`'s `sequence/no`. A loader MUST reject a pack whose `pack_version` is lower than the last one it accepted for this `federation_id`, to prevent downgrade/replay of a revoked or superseded pack.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `no`
- Shape: string

Optional timestamp when this pack revision was produced. Diagnostic only; `pack_version` is the authoritative ordering, not this timestamp.

<a id="field-attestation-roots"></a>
## `attestation_roots`

- Required: `yes`
- Shape: array

This federation's OWN canonical top-level anchor(s). NOT a copy of any relay's local Agora Authority `authority_roots[]` (Solution 021) — those are narrower, per-namespace, per-relay policy that MAY adopt an entry here as their namespace default, but are never required to equal this list.

<a id="field-bootstrap-seed-peers"></a>
## `bootstrap_seed_peers`

- Required: `no`
- Shape: array

This federation's static WSS seed peers (Proposal 014's 'mandatory first bootstrap layer'), resolving to `peer_discovery.seeds[]`. Deliberately flat — one endpoint per entry, no priority/enabled toggle — to match today's `DaemonSeedPeerConfig` exactly; richer multi-endpoint peer entries would require enriching that struct first, which this schema does not assume.

<a id="field-seed-directory-bootstrap"></a>
## `seed_directory_bootstrap`

- Required: `no`
- Shape: array

This federation's own canonical default trusted Seed Directories. Each entry fans out to two existing daemon config surfaces at load time: `network.seed_directory[]` (endpoint/node_id/passport) and `network.seed_directory_trust[]` (trust_level/weight/passport_ref/policy_ref/endorsement_refs/reputation_ref/enabled). The loader MUST fill `network.seed_directory_trust[].federation_id` from this pack's own top-level `federation_id`; it is not repeated per entry here.

<a id="field-federation-service-endorsement-revocations"></a>
## `federation_service_endorsement_revocations`

- Required: `no`
- Shape: array

Optional signed `federation-service-endorsement-revocation.v1` artifacts known at root-pack activation time. Loaders use these revocations when deciding whether inline Seed Directory bootstrap endorsements may confer federation-official status.

<a id="field-custody-policies"></a>
## `custody_policies`

- Required: `no`
- Shape: array

Self-contained organization custody policies referenced by `attestation_roots[].custody_policy_ref`. MVP loaders resolve policy refs inside this same federation-root pack, so bootstrap does not depend on an external policy registry.

<a id="field-policy-ref"></a>
## `policy_ref`

- Required: `no`
- Shape: string

Optional reference to the policy document governing this federation's root and bootstrap decisions.

<a id="field-endorsement-refs"></a>
## `endorsement_refs`

- Required: `no`
- Shape: array

Optional references to endorsement facts supporting this pack's trust claims (for example community-elected public-service recognition), carried via the existing `reputation-signal.v1` mechanism rather than a new primitive.

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

Signatures over the canonical payload (every field above, excluding `signatures` itself). A local, self-authored federation-root file is still signed by its own operator-held root key(s) — 'self-signed' is a valid case, 'unsigned' is not. Which keys and how many are required is governed by whatever custody mode/policy applies to this federation's `attestation_roots[]` entries (see Proposal 076 section 4 and its resolved custody-mode decision), not by this schema. Runtime threshold evaluation is over unique signing keys, not over externally asserted people or organizations.

## Definition Semantics

<a id="def-attestationroot"></a>
## `$defs.AttestationRoot`

- Shape: object

<a id="def-bootstrapseedpeer"></a>
## `$defs.BootstrapSeedPeer`

- Shape: object

Mirrors `DaemonSeedPeerConfig` field-for-field (daemon/src/config.rs:761).

<a id="def-seeddirectorybootstrap"></a>
## `$defs.SeedDirectoryBootstrap`

- Shape: object

Fans out to `DaemonSeedDirectoryConfig` (daemon/src/config.rs:528) and `DaemonSeedDirectoryTrustConfig` (daemon/src/config.rs:551) at load time.

<a id="def-custodypolicy"></a>
## `$defs.CustodyPolicy`

- Shape: object

<a id="def-custodyrule"></a>
## `$defs.CustodyRule`

- Shape: object

<a id="def-signature"></a>
## `$defs.Signature`

- Shape: object

<a id="def-federationserviceendorsement"></a>
## `$defs.FederationServiceEndorsement`

- Shape: object

Embedded form of `federation-service-endorsement.v1` used only so a bootstrap Seed Directory can be verified before any directory is trusted. Runtime verification still enforces signature, custody, time, federation, node, and capability invariants.

<a id="def-federationserviceendorsementrevocation"></a>
## `$defs.FederationServiceEndorsementRevocation`

- Shape: object

Embedded startup-time endorsement revocation. Runtime Seed Directory verification remains authoritative for live feeds; this root-pack form lets startup bootstrap apply known withdrawals before trusting inline official-service proofs.

<a id="def-federationserviceendorsementsignature"></a>
## `$defs.FederationServiceEndorsementSignature`

- Shape: object
