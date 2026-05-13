# Proposal 056: Orbiplex TLS Trust Policy

Based on:

- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/043-node-address-attestation-fallback.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `node:network/src/lib.rs`
- `node:seed-directory/src/lib.rs`
- `https://randomseed.pl/rna/ssl-jest-do-bani/`

## Status

Draft

## Date

2026-05-13

## Executive Summary

Orbiplex should not treat the public WebPKI as the only trust root for node
communication. Most Orbiplex nodes are expected to be distributed, local,
client-owned, intermittently reachable, and frequently operated outside a
traditional public hosting environment. Requiring every WSS/HTTP endpoint to
obtain a WebPKI certificate would add operational friction and would make the
transport trust model depend on authorities that are not part of the Orbiplex
governance model.

At the same time, Orbiplex should not replace the public WebPKI with one
global, all-powerful Orbiplex CA. That would recreate the same structural
problem at a smaller scale.

This proposal defines a stratified TLS trust model:

1. **Official service trust** for public Orbiplex-operated services.
2. **Node endpoint trust** for node-to-node WSS/HTTP communication.
3. **Local/dev trust** for generated local profiles and acceptance setups.
4. **Diagnostic trust** for explicitly unsafe debugging modes.

The invariant is:

```text
TLS authenticates and protects the transport endpoint.
Orbiplex identity is proven by Orbiplex protocol handshakes and signed artifacts.
Authorization remains in passports, capabilities, and local policy.
```

## Context and Problem Statement

The current implementation already uses X.509 primarily at transport
boundaries:

- WSS peer transport accepts a server certificate chain and a PKCS#8 private key.
- WSS dialers verify the peer endpoint with either WebPKI roots or configured
  root certificates.
- Seed Directory reachability probes verify WSS endpoints before accepting or
  attesting advertised node addresses.
- Local acceptance profiles generate certificate material under the node data
  directory.
- Agora CLI and ordinary HTTPS clients use `rustls`/`webpki` unless configured
  otherwise.

This is a good layering baseline. X.509 is a channel mechanism, not the primary
Orbiplex identity model.

The problem is that a single global certificate policy is not appropriate for
all Orbiplex surfaces:

- public bootstrap services need stable operator-grade trust;
- ordinary nodes need cheap, local, self-generated endpoint protection;
- Seed Directory must be stricter than arbitrary node-to-node dialers;
- local development needs repeatable certificates without hand-editing byte
  arrays in configuration;
- diagnostic tools sometimes need explicit insecure operation, but never as a
  silent default.

## Proposed Model / Decision

### 1. Separate TLS Trust Classes

Orbiplex implementations SHOULD model TLS trust as an explicit endpoint-class
policy, not as one process-wide boolean.

The initial trust classes are:

| Trust class | Typical endpoints | Trust source |
| --- | --- | --- |
| `official-service` | public Seed Directory, official Agora, bootstrap APIs | Orbiplex Public Service CA, optionally WebPKI |
| `node-endpoint` | INAC, Artifact Delivery, peer WSS/HTTP | Seed Directory attested fingerprint plus Orbiplex peer handshake |
| `local-dev` | story profiles, acceptance tests, local multi-node setups | data-dir generated local roots |
| `diagnostic` | operator debugging only | explicit insecure mode, disabled by default |

Every runtime surface that opens outbound TLS SHOULD know which class it is
using.

### 2. Official Service Trust

Official public services MAY use a distribution-shipped Orbiplex Public Service
CA.

The public key or root certificate of that CA may be bundled with the
distribution and referenced by configuration independently of the host operating
system trust store.

This CA is intended for:

- public Seed Directory endpoints operated by a network or organization;
- official Agora endpoints;
- bootstrap endpoints;
- release or update endpoints, if such endpoints become part of the runtime.

This CA MUST NOT become the default issuer for ordinary user-operated nodes.
Using it for every node would create a private WebPKI and would centralize node
admission, revocation, and operational burden in one root.

### 3. Node Endpoint Trust

For node-to-node WSS/HTTP communication, the default SHOULD be:

1. the node generates a self-signed endpoint certificate in its data directory;
2. the node advertises or registers its current endpoint through Seed Directory;
3. Seed Directory probes the endpoint and records the observed certificate
   fingerprint;
4. other nodes use the Seed Directory signed observation as pinning material;
5. after the TLS channel is established, the Orbiplex peer handshake proves the
   node identity with the node identity key.

The endpoint certificate is therefore not the node identity. It is a transport
key for one reachable endpoint.

The minimum attested material is:

```text
node_id
endpoint_url
tls_cert_fingerprint_sha256
observed_at
expires_at
probe_method
seed_directory_signature
```

This material can be carried by `node-address-attestation.v1` or a future
version of that artifact if the current schema needs an explicit TLS fingerprint
field.

### 4. Seed Directory Trust Must Be Stricter Than Node Trust

Seed Directory cannot use the same relaxed policy as arbitrary node endpoints.

A public Seed Directory endpoint SHOULD use one of:

- `official-service` trust through the Orbiplex Public Service CA;
- WebPKI, when normal browser and CLI compatibility is more important;
- an explicit pinned trust root configured by the operator.

It MUST NOT accept its own self-signed endpoint certificate merely because that
certificate was advertised through the same discovery path it is supposed to
protect.

This prevents a circular trust loop:

```text
trust Seed Directory because it says its own certificate is trusted
```

### 5. Local/Dev Trust

Local story profiles and acceptance setups SHOULD continue to generate
certificate material under the data directory.

The preferred shape is:

```text
<data-dir>/certificates/listener/certificates/*.der
<data-dir>/certificates/listener/key.pkcs8.der
<data-dir>/certificates/trust-roots/*.der
```

Configuration should reference directories or files, not raw byte arrays.

Hidden files, backup files, cache files, and temporary directories are ignored
when loading certificate sources, following the same operational hygiene rules
used for middleware package integrity.

This supports:

- one-laptop multi-node story runs;
- local self-signed roots;
- moving generated profile skeletons between machines after replacing or
  regenerating endpoint facts.

### 6. Diagnostic Trust

An insecure TLS mode MAY exist for diagnostics, but it MUST be explicit,
operator-visible, and disabled by default.

Examples:

- CLI `--tls-insecure-skip-verify`;
- local debugging profile flags;
- temporary probe tools.

Diagnostic trust MUST NOT be the fallback when certificate verification fails.
Verification failure should remain visible as a transport error such as
`UnknownIssuer`, fingerprint mismatch, expiry, or hostname mismatch.

## Identity and Authorization Boundary

TLS certificate verification answers a narrow question:

```text
Did we establish an encrypted channel to an endpoint matching this endpoint
trust policy?
```

It does not answer:

- which Orbiplex node this is;
- whether the node may provide a capability;
- whether the caller may use a capability;
- whether the endpoint is currently authorized by community policy.

Those questions remain in separate layers:

| Question | Layer |
| --- | --- |
| Is the transport endpoint cryptographically bound to this TLS key? | TLS/X.509 |
| Is this endpoint the one Seed Directory recently observed for `node_id`? | node-address attestation |
| Does the peer possess the node identity key? | Orbiplex peer handshake |
| May this node or caller use a capability? | passports and capability binding |
| Is the action locally allowed? | local operator policy |

This avoids turning X.509 into an accidental ontology for Orbiplex identity.

## Example Sequence: Node-to-Node WSS

1. Node A generates a self-signed WSS certificate in its data directory.
2. Node A registers `node_id`, endpoint URL, and service metadata with Seed
   Directory.
3. Seed Directory probes the endpoint.
4. During the probe, Seed Directory verifies reachability and records the TLS
   certificate fingerprint it observed.
5. Seed Directory signs an address attestation for Node A.
6. Node B asks Seed Directory for Node A's address.
7. Node B receives the signed attestation.
8. Node B opens TLS to the advertised endpoint and checks that the observed
   certificate fingerprint matches the attestation.
9. Node B runs the Orbiplex peer handshake over the channel.
10. Node B accepts the connection only if the peer proves possession of Node A's
    identity key.

## Configuration Sketch

The exact schema is out of scope for this proposal, but a runtime configuration
should be able to express the policy shape:

```toml
[tls.official_service]
trust = "orbiplex-public-service-ca"
root_certificates_source = "certificates/orbiplex-public-service-ca"

[tls.node_endpoint]
trust = "seed-directory-attested-fingerprint"
require_peer_handshake = true

[tls.local_dev]
trust = "local-profile-roots"
root_certificates_source = "certificates/trust-roots"

[tls.diagnostic]
insecure_skip_verify = false
```

Endpoint-specific configuration may still override this when an operator has a
clear reason, but the override should be visible in readiness and diagnostics.

## Trade-offs

### Benefits

- Reduces dependence on public WebPKI for node-to-node communication.
- Preserves TLS confidentiality and integrity.
- Keeps node identity in Orbiplex-native protocol layers.
- Allows official public services to have stable operator-grade trust.
- Keeps local development and story profiles simple.
- Makes Seed Directory observations useful even when Seed Directory is
  temporarily unreachable and another trusted peer relays the attestation.

### Costs

- Requires explicit endpoint trust classes in configuration and code.
- Requires careful operator diagnostics for fingerprint mismatch and stale
  attestations.
- Requires revocation/rotation semantics for official service CA material.
- Requires clear UX for replacing local endpoint certificates.

### Rejected Alternative: One Global Orbiplex CA for Everything

A single Orbiplex CA could sign official services and ordinary nodes, but this
would make that CA an admission authority for the whole network. That is not
aligned with the federated model.

It also creates difficult lifecycle questions:

- Who signs ordinary node certificates?
- How are compromised node certs revoked?
- How do user-maintained federations maintain autonomy?
- How does a node join without online access to the CA?

The proposal therefore limits CA use to official service trust.

### Rejected Alternative: WebPKI Everywhere

WebPKI everywhere would make public deployment familiar, but it is a poor fit
for client-owned local nodes, NATed environments, dynamic endpoints, test
profiles, and private federation. It also imports a large external trust base
into a system that already has its own identity and authorization layers.

### Rejected Alternative: Disable TLS Verification for Nodes

Disabling verification would preserve encryption against passive observers but
would weaken active attacker resistance and make downgrade or interception
harder to diagnose. Node endpoints should instead use attested fingerprints and
Orbiplex peer handshakes.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Seed Directory publishes stale fingerprint | Include `observed_at`, `expires_at`, and freshness policy. |
| Node rotates local certificate without updating Seed Directory | Dialers fail closed with fingerprint mismatch. Operator UI explains rotation/update path. |
| Public Seed Directory certificate is self-signed but not trusted | Operator installs official CA or explicit pinned root for the Seed Directory endpoint. |
| Orbiplex Public Service CA is compromised | Rotate bundled root, publish revocation notice, pin service keys where possible. |
| Diagnostic insecure mode leaks into production | Keep it explicit, logged, readiness-visible, and disabled by default. |
| TLS cert is mistaken for node identity | Documentation and code names use `endpoint_certificate`, `fingerprint`, and `peer_handshake` terminology. |

## Implementation Notes

Current code already has most low-level primitives:

- WSS server TLS identity accepts certificate chain DER and PKCS#8 key.
- WSS client TLS config accepts either configured roots or WebPKI roots.
- Seed Directory WSS probes can receive root certificates for endpoint
  verification.
- Local profiles can load certificate directories from the data directory.

Expected implementation work:

1. Define endpoint trust classes in daemon/transport configuration.
2. Ensure Seed Directory public endpoint trust is configured separately from
   node endpoint trust.
3. Extend `node-address-attestation.v1` if it does not already carry an
   explicit TLS certificate fingerprint.
4. Add diagnostics for `UnknownIssuer`, fingerprint mismatch, expired
   attestation, and peer-handshake identity mismatch.
5. Expose effective TLS trust policy in readiness/status reports.
6. Document local certificate rotation and trust-root installation.

## Open Questions

1. Should `node-address-attestation.v1` carry the full leaf certificate
   fingerprint only, or also a public-key/SPKI fingerprint?
2. Should Seed Directory accept multiple fingerprints for one node endpoint
   during rotation windows?
3. How long should node endpoint attestations remain fresh by default?
4. Should official services prefer Orbiplex Public Service CA over WebPKI, or
   support both in parallel for browser-facing surfaces?
5. Should user-maintained Seed Directory instances publish their own service CA
   material as signed governance artifacts?

## Next Actions

1. Audit current TLS call sites and classify them by trust class.
2. Add or update configuration schema for explicit TLS trust policy.
3. Check whether `node-address-attestation.v1` needs a TLS fingerprint field.
4. Add a solution-level update once the implementation shape is stable.
5. Update operator runbooks for local certificates, official service roots, and
   fingerprint mismatch troubleshooting.
