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

Accepted for partial implementation.

Implementation contract: `doc/project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md`.

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

A publicly trusted WebPKI certificate is therefore sufficient only for the
ordinary HTTPS/WSS transport question. It is not, by itself, an Orbiplex
authority decision. Federation membership, Seed Directory authority, service
authority, and node identity MUST be grounded in Orbiplex-controlled trust
material: `federation-root.v1`, locally accepted service CA material, signed
endpoint evidence, pinned endpoint fingerprints, peer handshakes, capability
passports, and local operator policy. A federation MAY use its own private or
self-signed trust anchor; the important property is that the anchor is explicit,
scoped, signed/accepted, and auditable, not that it chains to a public browser
CA.

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

The Orbiplex Public Service CA, if used, is a scoped Orbiplex trust anchor, not a
request to be signed by an external public CA. Public WebPKI MAY still be used
for browser and CLI compatibility, but public WebPKI MUST NOT be the sole source
of truth for accepting a Seed Directory, federation root, service capability, or
node identity.

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

1. the node generates node-local endpoint certificate material in its data
   directory with bounded validity;
2. the node advertises or registers its current endpoint through Seed Directory;
3. Seed Directory probes the endpoint and records the observed certificate
   fingerprint;
4. other nodes use the Seed Directory signed observation as pinning material;
5. after the TLS channel is established, the Orbiplex peer handshake proves the
   node identity with the node identity key.

The endpoint certificate is therefore not the node identity. It is a transport
key for one reachable endpoint.

Generated node-local CA and listener certificates SHOULD have bounded validity
so stale endpoint trust material naturally lapses. The reference node
implementation uses a 365-day validity window and backdates by 5 minutes for
local clock skew. The operator rotation path is explicit: the generation
endpoint may be called with `force: true` to replace the listener leaf, listener
private key, and node-local trust root, followed by daemon restart/reload so WSS
listener and dialer trust roots observe the new files.

The generated listener certificate SHOULD NOT expose the stable Orbiplex
`node_id` in the TLS subject by default. A public TLS listener is visible to
ordinary port scanners before the Orbiplex peer-handshake layer can apply any
friend, capability, or network-membership checks. Publishing `node:did:key:...`
as the TLS Common Name would therefore create a cheap reconnaissance vector:
any non-peer client could correlate one node across addresses, restarts, NATs,
or networks.

The privacy-preserving default is an opaque `route_id`: the generated local CA
uses a route-local Common Name and the listener leaf certificate uses the same
route identifier as its TLS subject. Operators MAY explicitly configure
`node_id` as the TLS certificate identity for local diagnostics or deliberately
public services, but this is not the default.

The TLS layer and the peer-identity layer SHOULD propagate different facts:

- `tls_chain_verified`: whether the transport certificate chain, hostname/SNI,
  configured CA material, WebPKI roots, or explicit pin passed the TLS endpoint
  policy;
- `subject_common_name`: the observed leaf certificate Common Name, when present;
- `advisory_subject_verified`: whether a higher Orbiplex layer has interpreted
  the CN as an Orbiplex subject and checked it against the expected peer context.

If the observed CN is an ordinary DNS-style name and the endpoint policy uses
Orbiplex Public Service CA or WebPKI, the TLS layer verifies the certificate
through the configured root store and propagates the CN with
`tls_chain_verified = true`. The peer layer does not need to reinterpret such a
CN as Orbiplex identity.

If the observed CN contains Orbiplex-style structured identity material, such as
`node:did:key:...`, an opaque `route:...`, or a delegated
`routing:did:key:...` routing subject, the transport layer MUST propagate the CN
but MUST NOT treat it as a complete identity proof by itself. The peer layer
then applies contextual checks:

- `node:did:key:...` MUST match the signed `peer-handshake.v1` sender node id;
- `route:...` and `routing:did:key:...` MAY be checked against the expected
  route id carried by endpoint evidence, local seed configuration, or another
  explicit routing contract;
- `route:...` MUST have a non-empty suffix, and `routing:did:key:...` endpoint
  evidence MUST validate as Ed25519 did:key material rather than only matching a
  string prefix;
- when Artifact Delivery resolves a `routing-subject` selector for direct
  delivery, endpoint evidence MUST carry matching
  `endpoint/certificate.advisory/route-id = routing:did:key:...` before the
  daemon emits a concrete node target;
- mismatch MUST reject the connection before protocol payload exchange;
- absence of a node-id or route-id CN MUST NOT reject otherwise valid WebPKI,
  public-service-CA, private-CA, or pinned endpoint certificates.

This keeps CN as an advisory cross-layer consistency check rather than a source
of Orbiplex authority.

For operator-managed bootstrap seeds, a daemon MAY additionally configure a
static leaf-certificate pin on the seed entry. This is not a replacement for
Seed Directory endpoint evidence; it is a local bootstrap contract that lets the
peer supervisor reject a seed endpoint when the observed TLS leaf fingerprint no
longer matches the operator's configured expectation. Pins use
`sha256:<base64url-no-pad>` over the leaf certificate DER and MUST fail
configuration validation if the digest body is malformed.

For local node-generated certificates, the preferred public-listener shape is a
route-local CA with a generated CA key and an opaque route-id Common Name. The
WSS listener receives a separate random leaf key signed by that issuer. This
avoids copying node identity private key material into the TLS listener key
file and avoids leaking the stable node id through the TLS certificate chain.
The peer handshake remains the proof of node identity.

Route ids SHOULD be stable operational route subjects, not per-connection random
values. A node should generate the route id when listener certificate material is
first created, persist it in local configuration, and reuse it across daemon
restarts and ordinary leaf-certificate rotations. Regenerating the route id is a
route-identity rotation: it requires regenerating the listener certificate and
refreshing any endpoint evidence, local seed records, or peer expectations that
referenced the previous route id. This cadence makes advisory route-id
validation useful without exposing the stable node id.

The generated listener private key is a secret configuration artifact and SHOULD
be written with owner-only permissions (`0600` on Unix-like systems). Public
certificates and trust roots may remain world-readable.

If an operator explicitly configures certificate or private-key source paths,
missing paths or empty certificate directories are configuration errors. The
readiness helper may offer generation only when the source is absent/defaulted,
not when an explicit path is mistyped.

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

This material is carried by `node-address-attestation.v1` as signed
`endpoint/certificate` evidence on transcript-bound observations. The v1
implementation supports `sha256-leaf-der` and `sha256-spki`; leaf DER remains
the default required pin, while SPKI supports continuity checks across leaf
certificate renewal.

Endpoint certificate observation is an initiator-side fact: it records what the
dialing/probing side verified for the remote endpoint during TLS setup. A
listener/responder transcript MUST NOT populate this observation with its own
server certificate as if it were peer evidence.

`endpoint/certificate.verified/at` means the time at which the observer
completed local endpoint-certificate verification. It is not the later evidence
signing time and not a re-emission timestamp. In v1, when endpoint certificate
evidence is present, implementations MUST enforce:

```text
signed/at <= endpoint/certificate.verified/at <= expires/at
```

with at most 16 seconds of clock-skew tolerance on either side of the evidence
freshness window.

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

1. Node A generates a bounded-validity node-local CA certificate and a
   CA-signed WSS listener certificate in its data directory.
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
| Route id is regenerated too often | Treat route id rotation as an explicit route-identity rotation that refreshes listener certificates and endpoint evidence. |

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
3. Keep `node-address-attestation.v1` evidence signed over
   `endpoint/certificate` whenever a session transcript hash is present.
4. Add diagnostics for `UnknownIssuer`, fingerprint mismatch, expired
   attestation, and peer-handshake identity mismatch.
5. Expose effective TLS trust policy in readiness/status reports.
6. Document local certificate rotation and trust-root installation.

## Resolved Questions

1. `sha256-leaf-der` is sufficient for the current implementation. `sha256-spki`
   remains deferred until certificate renewal or deployment constraints make
   public-key pinning technically necessary.
2. Seed Directory SHOULD support multiple valid fingerprints for one node
   endpoint during rotation windows. Rotation needs overlap rather than an
   instantaneous cut-over.
3. Freshness is class-specific:
   - `node_id` is a stable cryptographic identity fact and has no ordinary TTL,
     though it can be revoked, replaced, or marked compromised.
   - Node identity confirmation, certificate, or binding records SHOULD carry
     `issued_at`, `expires_at`, and revocation references; validity is typically
     months to years.
   - Node operator or routing bindings SHOULD be medium-lived; days, weeks, or
     months depending on local governance policy.
   - Node endpoint advertisements are reachability candidates, not durable
     identity facts; dynamic laptop-style nodes should use about `5-15 min`,
     stable servers may use about `1 h`, and re-announcement SHOULD happen at
     `TTL / 2` or `TTL / 3`.
   - Endpoint attestations SHOULD be short to medium lived, about `15 min` to
     `24 h` depending on endpoint class and risk.
   - Fresh liveness probes are very short lived, usually a few minutes.
   - Resolvers MAY cache active endpoint results for about `30-120 s`.
   - Old endpoint records MAY be retained historically for about `24-72 h`, but
     MUST NOT be treated as active routing truth.
4. Official non-browser node services SHOULD prefer Orbiplex Public Service CA
   over WebPKI. Browser-facing surfaces MAY need WebPKI in parallel, but node
   runtime trust should not silently trust the global WebPKI root set.
5. User-maintained Seed Directory instances MAY publish service CA material as
   signed governance artifacts. Nodes MUST treat that material as scoped trust
   material candidates and MUST require local policy or an accepted governance
   authority before using it for endpoint validation.
6. Scoped service CA governance material SHOULD use `service-ca-material.v1` for
   M4/M5. The schema is sufficient if it cleanly separates:
   - CA material,
   - usage scope,
   - governance authority or proof,
   - validity and rotation,
   - and local acceptance policy.

   Important contract:

   ```text
   service-ca-material.v1 != trust decision
   ```

   `service-ca-material.v1` means "this CA material is announced for this
   scope." Local trust policy means "this issuer may establish CA material for
   this scope." A node MUST NOT use published CA material until local policy
   accepts the issuer, scope, and policy reference. Future complexity should use
   adjacent artifacts such as `service-ca-revocation.v1`,
   `service-ca-policy.v1`, or `service-ca-transparency-checkpoint.v1` rather
   than overloading the initial material artifact.

   `authority/class` is only a declared class and MAY narrow a local rule. It
   MUST NOT authorize a service CA candidate by itself; the local rule still
   needs an explicit `authority/id` match.
7. The first public federation profile SHOULD use conservative TTLs:

   | Deployment class | Endpoint advertisement | Endpoint attestation | Liveness freshness | Service CA material | Operator/routing binding |
   |---|---:|---:|---:|---:|---:|
   | `laptop-dynamic` | `10 min` | `30 min` | `2 min` | `30 days` | `30 days` |
   | `home-node` | `30 min` | `2 h` | `5 min` | `60 days` | `90 days` |
   | `vps-stable` | `1 h` | `12 h` | `10 min` | `90 days` | `180 days` |
   | `seed-directory` | `1 h` | `24 h` | `15 min` | `90 days` | `180 days` |
   | `bootstrap-anchor` | `6 h` | `72 h` | probe-before-use | `180 days` | `365 days` |

   Re-announcement cadence SHOULD be:

   ```text
   reannounce_at = TTL / 3
   jitter = +/- 10%
   ```

   Hard rules:

   ```text
   endpoint advertisement TTL <= endpoint attestation TTL
   liveness freshness <= endpoint advertisement TTL
   service CA material TTL >> endpoint attestation TTL
   binding TTL >> endpoint advertisement TTL
   ```

   Routing SHOULD distinguish freshness classes:

   ```text
   fresh   = verified_at <= class fresh window
   usable  = now <= expires_at, but verified_at is older than the fresh window
   stale   = now > expires_at, only history or probe fallback
   dead    = stale retention exceeded or explicit revocation
   ```

   Even when endpoint attestation remains valid for hours, direct or private
   delivery SHOULD NOT rely on an old attestation alone; it should perform a
   fresh probe or peer handshake when the freshness window has elapsed.

## Remaining Open Questions

None for this proposal revision.

## Next Actions

1. Done: `service-ca-material.v1` defines the signed governance-published CA
   material candidate. It deliberately does not encode the local trust decision.
2. Done: node endpoint evidence has an implementation bridge. Seed Directory
   node candidate resolution can fetch `node-address-attestation.v1`, copy the
   selected `endpoint/certificate` fingerprint into the daemon's endpoint
   evidence companion, and the peer supervisor prefers that attested fingerprint
   over static bootstrap seed pins when building `DialCandidate`.
3. Done: discovery/routing freshness policy is configurable through
   `peer_discovery.freshness_policy`, with deployment-class defaults and
   `fresh` / `usable` / `stale` / `dead` classification helpers.
4. Done: local `service_ca_trust_policy` is represented at daemon-config level
   and evaluated by the pure `orbiplex-node-service-ca-trust` crate. The
   operator API exposes the configured rules and can evaluate a
   `service-ca-material.v1` candidate without installing it as a trust root.
   The daemon-side evaluation surface verifies the canonical candidate
   signature before policy evaluation; the pure crate remains a policy
   evaluator and does not resolve keys by itself.
5. Done: peer supervisor operator status exposes endpoint evidence and
   freshness classification so operators can inspect fresh vs. stale endpoint
   pins. Direct subject-node resolution promotes only usable endpoint
   certificate evidence into Artifact Delivery direct targets; stale and dead
   evidence remain diagnostic or historical only.
6. Done: `service-ca-revocation.v1`, persisted Service CA candidates,
   persisted evaluations, scoped installations, and multi-pin endpoint evidence
   close the Phase 4 production-minimum lifecycle.
7. Next: update operator runbooks for local certificates, official service
   roots, service CA material acceptance, and fingerprint mismatch
   troubleshooting.
