# Communication Protocol Baseline for Orbiplex Swarm

Based on: `doc/project/10-challenges/002-sybil.md`

## Status

Baseline vision — superseded as an implementation source by the proposals and
solutions mapped below. Hard-MVP ready as a historical baseline: P002 now owns
the problem framing, not the frozen runtime contracts.

## Date

2026-02-22

## Executive Summary

This proposal defines the original node-to-node communication architecture for
the Orbiplex Swarm, designed for mixed environments (consumer networks +
corporate networks with mandatory proxy/TLS inspection). The design was built
around Ed25519 identity, a proxy-friendly WSS transport, optional message-level
E2E encryption with PFS, and untrusted Edge relay nodes. Later hard-MVP work kept
the core direction but moved the frozen contracts into narrower owners:
transport and discovery into P014 / Solution 000, TLS trust into P056 / Solution
024, discovery trust into Seed Directory and Federation Root, large payloads
into Artifact Delivery / INAC, and group/user messaging into Messaging and Room.

## Current Status and Superseded-By Mapping

P002 remains the **baseline vision** for Orbiplex node-to-node communication: the
problem framing (mixed corporate/consumer networks, transport-vs-confidentiality
separation, governance-aware profiles, Sybil/DoS posture) and the directional
model still hold. It is **not** the frozen source of truth for the implemented
runtime. Much of what it described has since been specified in detail and
implemented elsewhere, so this proposal has become directional where those layers
took over. Read P002 for the *why* and the shape; for anything you intend to
build or freeze, follow the mapped source. If a mapped source and P002 disagree,
the mapped source wins and P002 is read as historical intent.

As of 2026-07-06, P002 has no live hard-MVP implementation blockers of its own.
The remaining concrete work belongs either to mapped runtime owners or to
post-MVP hardening tracks. This document is ready when it accurately points to
those owners.

| P002 area | Current source(s) of truth | Status note |
| --- | --- | --- |
| Transport, discovery, handshake, sessions, keepalive/reconnect (§1, §4, §7) | [P014 Node Transport and Discovery MVP](014-node-transport-and-discovery-mvp.md); [Solution 000 Node](../60-solutions/000-node/000-node.md); [requirements-006 node networking](../50-requirements/requirements-006-node-networking-mvp.md) | Implemented for the hard-MVP transport seed. P014 owns signed node advertisement, peer handshake, static seed peers, WSS listener/dialer, keepalive/reconnect, peer status, and the narrower transport contract. |
| Control-plane **Envelope** and signing canonicalization (§6) | Concrete schema families in `node:protocol/contracts/schemas`: `node-identity.v1`, `node-advertisement.v1`, `peer-handshake.v1`, `capability-advertisement.v1`, `signal-marker-envelope.v1`, `peer-status.v1`, `node-succession.v1`; [P014](014-node-transport-and-discovery-mvp.md); [P037 Generic Signing Service](037-generic-signing-service.md); [P038 Key Roles and Key Use Taxonomy](038-key-roles-and-key-use-taxonomy.md) | The generic `Envelope` is **not** the frozen runtime contract. Per-purpose signed artifacts and their explicit canonicalization/domain-separation rules are implemented where needed. P002's envelope remains illustrative. |
| Identity model: base identity, session keys, multi-station, contextual nyms, stratification (§2) | [P059 Participant/Nym/Routing-Subject Key-Role Derivation](059-participant-and-nym-key-role-derivation.md); [Solution 026 Pseudonym Vault and Key Roles](../60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md); [P014 identity baseline](014-node-transport-and-discovery-mvp.md); [Solution 000 Node](../60-solutions/000-node/000-node.md); [P076 Federation Identity and Network Selector](076-federation-identity-and-network-selector.md); [Solution 041 Federation Root](../60-solutions/041-federation-root/041-federation-root.md) | Node identity, participant/nym/routing-subject key roles, pseudonym vault storage, and federation-root sovereign subject selection are implemented in the downstream owners. P002's identity section is the conceptual layering. |
| Capability advertisement, admission, Sybil posture, and DoS gates (§3) | [P024 Capability Passports](024-capability-passports-and-network-ledger-delegation.md); [P025 Seed Directory as Capability Catalog](025-seed-directory-as-capability-catalog.md); [P072 Capability Registry](072-capability-registry.md); [Solution 006 Capability Binding](../60-solutions/006-capability-binding/006-capability-binding.md); [Solution 037 Capability Registry](../60-solutions/037-capability-registry/037-capability-registry.md); [Solution 031 Seed Directory](../60-solutions/031-seed-directory/031-seed-directory.md) | The posture is preserved, but concrete enforcement is no longer one protocol section. Capability ids, passports, official-service endorsements, registry eligibility, and runtime grant/admission checks carry the implemented hard-MVP gates. Sponsor-token bootstrap remains a later membership/governance track rather than a P002 blocker. |
| Transport vs E2E crypto; TLS / certificates / inspection (§4, §9 TLS) | [P056 Orbiplex TLS Trust Policy](056-orbiplex-tls-trust-policy.md); [Solution 024 TLS Trust Policy](../60-solutions/024-tls-trust-policy/024-tls-trust-policy.md); [P043 Node Address Attestation Fallback](043-node-address-attestation-fallback.md); [P076 Federation Identity and Network Selector](076-federation-identity-and-network-selector.md) | P002's original "system trust store / corporate TLS" wording is now too broad. P056 + Solution 024 own route-id, local CA, endpoint evidence, and TLS pin/policy semantics. Message-level E2E profile switches remain a future policy layer. |
| Security profiles `CORP_COMPLIANT` / `E2E_PREFERRED` / `E2E_REQUIRED` (§5) | Policy concept; nearest runtime expressions are P056/S024 TLS trust policy, P014 locality/trust modes, host policy, and signed artifact admission | The profile names remain useful governance vocabulary, but they are **not** implemented as one closed runtime switch. Runtime owners implement narrower policy facts instead. |
| Edge relaying as public backbone (§8) | P014 peer runtime + WSS listener/dialer; [P054 User-Maintained Federated Seed Directory](054-user-maintained-federated-seed-directory.md); [Solution 031 Seed Directory](../60-solutions/031-seed-directory/031-seed-directory.md); P056/S024 endpoint evidence and TLS trust; [P042 INAC](042-inter-node-artifact-channel.md); [Solution 017 INAC](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md); [Solution 023 Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md) | The single "Edge relay" model is superseded in practice by peer-runtime + Seed Directory + AD/INAC. Edge relay remains a sensible future option, not the current backbone. |
| Large payload transfer | [Solution 023 Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md); [P042 INAC](042-inter-node-artifact-channel.md); [Solution 017 INAC](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md); object-store indirect | Implemented for the hard-MVP data-plane path. P002 no longer owns a separate large-payload extension. |
| User messaging, group scopes, and room semantics | [P060 Messaging Middleware](060-messaging-middleware.md); [Solution 027 Messaging Middleware](../60-solutions/027-messaging-middleware/027-messaging-middleware.md); [P070 Room](070-room-primitive.md); [Solution 036 Room](../60-solutions/036-room/036-room.md) | Story-facing messaging and group/room semantics are implemented in Messaging and Room. P002 does not own group-key or room lifecycle semantics. |
| Federation genesis trust set and network selector | [P076 Federation Identity and Network Selector](076-federation-identity-and-network-selector.md); [Solution 041 Federation Root](../60-solutions/041-federation-root/041-federation-root.md); P054/S031 Seed Directory | The "genesis trust set" decision is implemented through `federation-root.v1`, signed root packs, bootstrap seed peers, Seed Directory bootstrap/trust projections, and restart-only root activation. |
| Sybil resistance and anti-abuse posture | [challenge 002 Sybil](../10-challenges/002-sybil.md); P024/P025/P072; Solution 006/Solution 037; rate limits in transport, Agora, Seed Directory, AD/INAC, and middleware surfaces | P002 preserves the posture. Concrete anti-abuse mechanisms live at each boundary and should be reviewed in the relevant owner document. |

### Implemented / Transferred Reference Inventory

- **Transport and peer runtime**: P014 and Solution 000 own the hard-MVP node
  networking baseline: node identity, signed advertisements, peer handshake,
  static seed peers, WSS listener/dialer, keepalive/reconnect, and peer status.
- **TLS and endpoint trust**: P056 and Solution 024 replace the original broad
  corporate TLS checklist with route-id, local CA, endpoint evidence, and
  source-aware TLS trust semantics.
- **Discovery trust and federation bootstrap**: P054/Solution 031 and
  P076/Solution 041 own Seed Directory discovery, official-service endorsement
  proofs, signed federation-root packs, bootstrap seed peers, and genesis trust
  set replacement.
- **Capability admission and anti-Sybil boundary**: P024, P025, P072,
  Solution 006, and Solution 037 own capability passports, capability registry
  eligibility, official-service endorsement verification, and runtime
  capability binding.
- **Data-plane payloads**: P042/Solution 017 and Solution 023 own large or
  indirect payload delivery, including hard-MVP object-store-indirect delivery.
- **Messaging and group/room semantics**: P060/Solution 027 and
  P070/Solution 036 own user messaging, private delivery, group/room scope, and
  room lifecycle semantics.

## Context and Problem Statement

Orbiplex Swarm nodes must communicate reliably across heterogeneous network environments:
- Consumer nodes behind NAT.
- Corporate nodes behind mandatory HTTPS proxies with TLS inspection (MITM).
- Public Edge nodes providing relay and rendezvous.

Transport-level TLS alone does not guarantee end-to-end privacy when corporate proxies inspect traffic. The protocol must therefore separate transport security from message-level confidentiality, while remaining compatible with enterprise governance requirements (proxy-only egress, system trust stores, DLP visibility).

Additionally, the hostile nature of open-membership swarms requires built-in Sybil resistance and DoS mitigation at the protocol level.

Input analysis is documented in:
- `doc/project/10-challenges/002-sybil.md`
- `doc/project/30-stories/story-001-swarm-node-onboarding.md`
- `doc/project/50-requirements/requirements-001-node-onboarding.md`

## Options Considered

### Option A: IRC/Matrix as Primary Bus

Use an existing chat protocol (IRC, Matrix) as the primary control-plane transport.

- Pros:
  - Existing infrastructure and tooling.
  - Quick bootstrap for early prototyping.
- Cons:
  - Weak identity and authorization model.
  - Limited delivery guarantees and backpressure.
  - Not proxy-governance friendly as a primary corporate channel.
  - Operational/security optics (IRC often associated with legacy C2).

### Option B: Custom Protocol over Direct TCP/UDP

Purpose-built binary protocol with direct peer connections and NAT traversal.

- Pros:
  - Full control over framing, crypto, and efficiency.
  - Potentially lower latency for direct connections.
- Cons:
  - Blocked by most corporate proxies (non-443 ports, non-HTTP protocols).
  - Requires complex NAT traversal infrastructure from day one.
  - Higher implementation effort before any node can communicate.

### Option C: Layered Protocol over WSS/443 with Edge Relay and Optional E2E

WSS over TCP 443 via system proxy as primary transport. Untrusted Edge nodes as relay/rendezvous backbone. Optional message-level E2E crypto (X25519 + AEAD) for confidentiality/PFS independent of transport.

- Pros:
  - Works in corporate proxy environments out of the box.
  - Clean separation: transport (proxy-compatible) vs. confidentiality (E2E).
  - Security profiles allow governance-appropriate operation.
  - Edge relay is always-available fallback; direct/UDP paths are optimizations.
- Cons:
  - More governance overhead than single-mode protocols.
  - Edge infrastructure required for bootstrap and relay.
  - Three security profiles increase testing surface.

## Decision

Adopt **Option C (Layered Protocol over WSS/443 with Edge Relay and Optional E2E)**.

IRC/Matrix may serve as bootstrap hints or "apocalypse fallback" for presence/endpoint discovery, but not as the primary control-plane.

---

## Proposed Model

### 1. High-level architecture

#### Node types
- **Edge nodes** (public backbone):
  - Publicly reachable (VPS), deployed across multiple regions/ASNs.
  - Provide **bootstrap / rendezvous / relay** services.
  - Apply strong **DoS controls** and admission policies.
- **Field nodes** (behind NAT/proxy):
  - Typically behind NAT or corporate proxy.
  - Maintain outbound connections to Edge nodes (most reliable path).

#### Connectivity ladder (mixed networks)
1. **Outbound HTTPS/WSS over TCP 443 via system proxy** (most reliable in corp).
2. Opportunistic **direct TCP** when reachable.
3. Opportunistic **UDP hole punching (STUN)** when allowed.
4. **Relay via Edge** as the always-works fallback.

> In mixed environments, direct/NAT traversal is an optimization, not a dependency.

### 2. Identity model

#### Base identity
- Each accountable subject has a long-term **root / anchor identity**, which is
  not public by default.
- Each node has a long-term **`node-key`** (Ed25519 or compatible), controlled by
  that anchor identity.
- For Ed25519 in v1, **`node-id = node:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`**.
- Parsers for that v1 `node-id` shape SHOULD be strict; alternative textual forms
  should be treated as different versions, not as equivalent aliases.
- All control-plane messages are **signed**.

#### Session keys and continuity
- Nodes may use short-lived **session keys**:
  - `node-key` signs a "session certificate" binding `session-pubkey` + validity window.
- Reputation attaches primarily to `node-id`; session keys reduce the blast
  radius of compromise.

#### Multi-station continuity under one node identity
- **`node-id` is the public identity and the reputation anchor**, not a single host.
- One human or one operating entity MAY run **multiple stations / devices** under the same `node-id`.
- Each concrete device SHOULD have its own **`station-key`** and derived **`station-id = H(station-pubkey)`**.
- `node-key` signs a **station certificate** binding `station-pubkey` + allowed scopes + validity window.
- One station MAY host many local agents, but agents do not become separate node identities only by running on separate processes or hosts.
- Reputation, governance weight, and anti-Sybil accounting attach to `node-id`; operational traces and incident handling MAY be refined per `station-id`.
- Compromise of one station SHOULD, by default, trigger revocation of that station certificate, not forced rotation of the whole `node-id`, unless the long-term `node-key` or its anchor is also suspected compromised.

#### Contextual nyms under one node identity
- A `node-id` MAY issue **contextual nyms** for transactions, disputes,
  payments, actions, or bounded communication relationships.
- A contextual nym is **ephemeral and deniable** relative to the public `node-id`,
  but remains attributable to that `node-id` on the audit track.
- Anti-Sybil accounting and durable governance weight attach to `node-id` and its
  common anchor source, not to the raw number of contextual nyms.
- Networking and transport SHOULD NOT require `nym` resolution. Contextual nym
  verification belongs above the session layer, while the transport boundary
  continues to see only node and station or participant infrastructure artifacts.

#### Identity stratification
- `root-identity` (private) = civil or registry identity of the accountable subject.
- `anchor-identity` (private / selectively disclosable) = stable derived identity or attestation binding the subject to one or more node identities.
- `node-id` (public) = stable swarm identity used for reputation, routing, and governance.
- `custodian-ref` (audit-only or selectively disclosed) = the procedural reference to the human or organization responsible for the node.
- `station-id` (public or selectively disclosed) = concrete device or host acting under delegated authority from the node identity.
- `nym` (public, contextual) = temporary pseudonym created by `node-id` for bounded interactions.

This means that "one person, many devices" is modeled as **one node identity with multiple delegated stations**, not as many unrelated node identities, while "one node, many contextual masks" is modeled as **one durable `node-id` issuing many bounded nyms**.

### 3. Trust, Sybil, and DoS protections

#### Sybil resistance (pragmatic)
Use at least one "cost of identity" mechanism:
- **Admission control (recommended for Orbiplex Swarm)**:
  - `invite/sponsor` tokens signed by existing trusted nodes.
  - Rate-limit sponsorship (per sponsor per epoch).
- Optional add-ons:
  - Lightweight **puzzle/PoW** for join/handshake bursts.
  - Deposit/stake mechanisms if you later anchor membership rules on-chain.

#### DoS mitigation ("expensive before you believe")
- **Pre-auth gate**: minimal parsing, tiny first-message limits, connection rate limits.
- **Before costly work**: require puzzle/PoW or invite token before allocating heavy resources.
- **Peer scoring and eviction**: hot/warm/cold pools; degrade/evict misbehaving peers.
- If application traffic later carries `nym` signatures, transport-layer
  throttling and peer scoring should still operate primarily per `node-id`, not
  per resolved pseudonym.

### 4. Transport vs. end-to-end crypto

#### Transport
- Primary: **HTTPS/WSS (TCP 443)**, proxy-compatible, long-lived sessions.
- TLS verification uses **system trust store** in corporate mode.

#### End-to-end confidentiality / PFS (optional but crucial)
Because corporate proxy can MITM transport, real privacy requires:
- **E2E encryption at message layer** (AEAD).
- **PFS** via ephemeral ECDH (X25519) + frequent rekeying (time or message count).

### 5. Security profiles (client policy knob)

> Status: a policy concept, **not** a frozen runtime switch in the current
> implementation. See *Current Status and Superseded-By Mapping*.

#### `CORP_COMPLIANT` (default for corporate environments)
- Must use **system proxy only** (PAC/NTLM/Kerberos).
- Must use **system trust store** (proxy MITM is treated as "legitimate").
- E2E is **off or opportunistic** (depending on governance).
- Messages may be plaintext **for inspection/DLP**, but **critical commands should still be signed**.

#### `E2E_PREFERRED`
- Still uses proxy and system trust store.
- Attempts E2E; falls back if peer cannot.

#### `E2E_REQUIRED`
- Requires E2E; if peer cannot do E2E, no session is established.
- Uses ephemeral key exchange + rekey schedule to guarantee PFS at message level.

### 6. Message envelope (control-plane)

A minimal signed envelope (serialization: EDN/JSON; canonicalization required for signing):

```text
Envelope {
  v:            int
  from:         node-id
  station:      station-id | null
  to:           node-id | group-id | null
  ts:           unix-ms
  ttl_s:        int
  nonce:        bytes/uuid
  seq:          u64 (per-session monotonic)
  intent:       keyword/string (mini-protocol selector)
  body:         object (small)
  e2e:          { mode, kid, ciphertext, aad, tag } | null
  sig:          signature over canonical(envelope_without_sig)
}
```

- `nonce + ttl + seq` provide replay protection.
- `from` identifies the stable node identity; `station` identifies the concrete delegated device when the node operates in multi-station mode.
- If `e2e` is present, `body` may be empty and all payload moves into `ciphertext` (with `aad` carrying the signed metadata).

Note: the networking MVP may freeze narrower artifact-specific signing rules
earlier than this general envelope section. In particular, `node-advertisement.v1`
and `peer-handshake.v1` may use deterministic CBOR with explicit domain
separation before a generic control-plane envelope canonicalization is fully
settled.

### 7. Example handshake (proxy-friendly transport + optional E2E)

This handshake assumes the transport channel is already established:
- **WSS over 443 via system proxy** to an Edge node.
- Edge only forwards; it does not interpret the E2E layer.

#### Step 1 — `HELLO` (identity + capabilities)
**A -> Edge -> B** (or to rendezvous first, then to B)

```json
{
  "v": 1,
  "from": "nodeA",
  "station": "stationA",
  "to": "nodeB",
  "ts": 1700000000000,
  "ttl_s": 30,
  "nonce": "c3b2...uuid",
  "seq": 1,
  "intent": "swarm/hello",
  "body": {
    "node_pub": "ed25519:...",
    "station_pub": "ed25519:...",
    "station_cert": "ed25519sig(node over station binding)",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600000,
    "capabilities": {
      "transport": ["wss443-proxy"],
      "e2e": ["preferred", "required"],
      "rekey": {"messages": 2048, "minutes": 30}
    }
  },
  "sig": "ed25519sig(node over envelope)"
}
```

Notes:
- `session_pub` is ephemeral for E2E key agreement.
- `sig` authenticates the public node identity and binds the ephemeral key to the long-term node identity.
- `station_pub` and `station_cert` allow the peer to verify that the concrete device is acting under delegated authority from the long-term node identity.

#### Step 2 — `HELLO_ACK` (peer agrees + returns its ephemeral key)
**B -> Edge -> A**

```json
{
  "v": 1,
  "from": "nodeB",
  "station": "stationB",
  "to": "nodeA",
  "ts": 1700000000500,
  "ttl_s": 30,
  "nonce": "a91e...uuid",
  "seq": 1,
  "intent": "swarm/hello-ack",
  "body": {
    "node_pub": "ed25519:...",
    "station_pub": "ed25519:...",
    "station_cert": "ed25519sig(node over station binding)",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600500,
    "e2e_mode": "preferred"
  },
  "sig": "ed25519sig(node over envelope)"
}
```

#### Step 3 — derive session keys (E2E)
Both sides compute:

```text
shared_secret = X25519(A_session_priv, B_session_pub)
prk          = HKDF-Extract(salt = H(nodeA||nodeB||nonces), IKM = shared_secret)
keys         = HKDF-Expand(prk, info="orbiplex-e2e-v1", L=key_material)
tx_key, rx_key, ... (AEAD keys)
```

Then subsequent messages carry:

- `e2e.ciphertext = AEAD_Encrypt(tx_key, nonce=seq, aad=canonical(meta), plaintext=payload)`
- `sig` still covers the envelope meta + `e2e` fields (defense-in-depth, optional).

#### Rekeying (PFS strengthening)
- Rekey periodically: **every N messages or T minutes**.
- Use a new ephemeral X25519 pair; repeat `HELLO`-style key update (or a smaller `KEY_UPDATE` intent).

### 8. Edge relaying (routing by node-id, no trust in Edge)

> Status: the single Edge-relay backbone is superseded in practice by peer-runtime
> + Seed Directory (P054) + AD/INAC (P042, Solution 023). Retained as a future
> option, not the current backbone. See *Current Status and Superseded-By Mapping*.

#### Model
- Edge is a **rendezvous + relay**, not a trusted party.
- Edge can:
  - route frames by `to` / `node-id`,
  - apply DoS controls,
  - maintain presence tables,
  - optionally provide "mailbox" buffering (bounded).
- Edge must NOT be required to:
  - decrypt E2E payloads,
  - decide semantics of intents,
  - validate business logic.

#### Connection model
- Each Field node maintains 1-2 outbound sessions to Edge:
  - `edge_conn_id` assigned by Edge on connect.
  - Node registers presence: `(node-id -> edge_conn_id)`.

#### Relay routing algorithm (simplified)
On Edge:

```text
on frame(envelope):
  enforce_rate_limits(envelope.from, conn, ip/asn)
  if envelope.to is null:
     broadcast within allowed scope (rare; heavily limited)
  else:
     lookup dst = presence_table[envelope.to]
     if dst exists:
        forward(frame, dst)
     else:
        optionally queue in bounded mailbox OR return "peer/offline"
```

**Security properties:**
- Edge sees metadata (unless you also wrap metadata), but cannot read payload under E2E.
- Integrity and authentication come from signatures and/or E2E AEAD.
- Replay protection is enforced by endpoints (nonce/seq/ttl), not by Edge.

#### Rendezvous / discovery
- Nodes can ask Edge for "who is currently present in namespace X?" (subject to policy).
- Edge responses are treated as **hints**; endpoints still authenticate peers via signatures.

For a later post-MVP gossip layer, Orbiplex may also carry limited propagation-path
metadata alongside the advertised or relayed artifact itself. The point would not be
to centralize discovery, but to let receivers observe a small causal or propagation
trace of how the artifact reached them.

That future layer could help with:

- detecting suspiciously coordinated propagation patterns relevant to anti-Sybil review,
- building local transport reputation from observed delivery speed and consistency,
- and reasoning about dissemination quality without turning discovery into a fully
  trusted registry.

This is intentionally deferred. The MVP should not require propagation-path metadata
before the basic seed, advertisement, handshake, keepalive, and reconnect slice is
already proven end to end.

### 9. `CORP_COMPLIANT` governance checklist

> Status: TLS, certificate, and inspection specifics are now governed by P056
> Orbiplex TLS Trust Policy and Solution 024 (route-id / local CA / endpoint
> evidence). This checklist remains a governance reference. See *Current Status
> and Superseded-By Mapping*.

Use this as a policy checklist for corporate governance / security review.

#### Network egress / proxy
- [ ] Client uses **system proxy only** (PAC / OS proxy settings).
- [ ] No direct outbound connections unless explicitly permitted.
- [ ] Only standard ports: **TCP 443** (and optionally 80 for proxy discovery if required).
- [ ] DNS usage follows corporate policy (no custom resolvers unless allowed).

#### TLS / certificates / inspection
- [ ] TLS verification uses **system trust store**.
- [ ] No certificate pinning that would bypass legitimate corporate TLS inspection (unless a separate approved profile exists).
- [ ] TLS versions follow corporate baseline (typically TLS 1.2+; prefer TLS 1.3).

#### Content visibility / DLP
- [ ] Payload visibility is configurable:
  - `observable` (plaintext application payload) allowed for inspection/DLP.
  - `opaque` (E2E encrypted payload) only if governance explicitly allows it.
- [ ] Even in `observable`, **critical control-plane commands are signed** to prevent spoofing/replay.

#### Authentication and identity
- [ ] Node identity uses cryptographic keys; keys are stored securely (OS keychain/keystore where possible).
- [ ] Key rotation supported (session keys, rekey).
- [ ] Admission control mode documented:
  - invites/sponsors, allowlists, or managed enrollment.

#### Logging and audit
- [ ] Client logs are configurable and follow corporate retention rules.
- [ ] No sensitive plaintext is logged by default.
- [ ] Edge nodes provide operational metrics and audit trails for routing events (metadata only).

#### Safety controls
- [ ] Rate limiting and abuse controls are in place on Edge and client.
- [ ] Graceful degradation: if E2E is disallowed by governance, system runs in `CORP_COMPLIANT` without breaking connectivity.
- [ ] Clear UI/CLI indication of the active security profile.

---

## Trade-offs

| Benefit | Cost |
|---|---|
| Works in corporate proxy environments out of the box | Requires Edge infrastructure for relay/rendezvous |
| Three security profiles cover diverse governance needs | Increased testing surface and configuration complexity |
| E2E crypto is independent of transport | Dual crypto layers (transport TLS + E2E) add implementation weight |
| Edge is untrusted by design | Metadata is visible to Edge unless additional wrapping is applied |
| Admission control (invite/sponsor) limits Sybil | Legitimate new nodes face an onboarding barrier |
| WSS/443 is firewall-friendly | Binary/UDP optimizations are deferred (higher latency initially) |

## Failure Modes and Mitigations

| Failure mode | Impact | Mitigation |
|---|---|---|
| Edge node compromise | Metadata leakage, relay disruption; E2E payloads remain safe | Multi-Edge topology; endpoints treat Edge as untrusted; rotate Edge nodes |
| Session key compromise | Attacker decrypts traffic until rekey | Short rekey intervals (N messages or T minutes); PFS limits blast radius |
| Sponsor collusion (Sybil) | Malicious nodes admitted via colluding sponsors | Rate-limit sponsorship per epoch; reputation scoring of sponsors; revocation |
| Corporate proxy blocks WSS upgrade | Node cannot connect | Fallback to HTTP long-polling or chunked transfer; document proxy requirements |
| Canonicalization mismatch | Signature verification fails across implementations | Specify canonical form precisely (sorted keys, UTF-8 NFC, no trailing whitespace) |
| Clock skew beyond TTL window | Legitimate messages rejected | Bounded tolerance (e.g., 30s); NTP requirement for nodes; `ttl_s` as tunable |

## Resolved Questions

1. **Group messaging**: Current envelope supports `group-id` in `to`, but group
   key management (for example sender keys or MLS-style designs) is not owned by
   P002 anymore. It is resolved by P070 Room and P060 Messaging; group-key
   management belongs to those layers.
2. **Large payload transfer**: Data-plane for large payloads is resolved by
   Artifact Delivery (Solution 023), INAC (P042), and object-store indirect.
   P002 no longer owns a separate large-payload extension.

## Remaining Questions

None for this baseline vision document. Open implementation questions should be
tracked in the mapped runtime proposals and solutions.

## Resolved Decisions

1. **Canonicalization family alignment**: per-purpose canonicalization remains
   allowed. Deterministic CBOR stays frozen where P014 already uses it, while
   other signed artifact families may retain their own explicit canonical forms.
   A universal canonicalization mandate would be cleaner in the abstract, but it
   is not worth the migration risk at this stage.
2. **Metadata privacy**: `E2E_REQUIRED` means payload confidentiality for now.
   Metadata wrapping is a future privacy-hardening layer, not a requirement of
   the current baseline.
3. **Edge / relay / rendezvous incentives**: if a public relay, seed, or
   rendezvous role returns, the default incentive model is reputation and
   public-service posture first. Cost reimbursement or marketplace offers may
   be added later, but the baseline does not require token rewards.
4. **Admission bootstrap / genesis trust set**: first-network admission should
   use an explicit, versioned genesis trust set. Static seeds provide
   reachability, but the initial authority set must be auditable and later
   replaceable by normal governance.

## Next Actions

> These are the original 2026-02 draft actions, retained as historical intent.
> Most are now realized or superseded by the mapped sources above; status tags are
> inline.

1. **Specify canonical envelope format** (EDN vs JSON, canonicalization rules, signing algorithm details) as a sub-document or appendix. → Realized differently: per-purpose schema families + deterministic CBOR (P014).
2. **Implement MVP transport**: WSS/HTTP2 over 443 via system proxy with Edge relay (no E2E initially). → Realized: WSS transport + peer-runtime (P014, Solution 000).
3. **Implement Edge presence + relay** (no-trust pipe, rate limiting, presence table). → Superseded: peer-runtime + Seed Directory (P054) + AD/INAC instead of an Edge-relay backbone.
4. **Add E2E mode** (`E2E_PREFERRED` first, then `E2E_REQUIRED`) with rekey schedule. → Partial: encrypted session frames are implemented; E2E security profiles are not a frozen runtime switch.
5. **Add admission control** (invite/sponsor tokens) + DoS gates. → Partial: capability-based admission and rate-limit gates exist; sponsor-token bootstrap remains open.
6. **Add optional direct/UDP paths** later (optimization only). → Open (post-MVP optimization).
7. **Write story and requirements** for group messaging and large payload transfer scenarios. → Realized: Messaging (P060), Room (P070), AD/INAC; Story 010 messaging acceptance.

## Fact / Inference / Speculation Notes

- **Fact**: Corporate proxies commonly perform TLS inspection via MITM; transport TLS does not guarantee E2E privacy in such environments.
- **Fact**: Ed25519 and X25519 are widely supported, audited, and suitable for identity and key agreement respectively.
- **Inference**: WSS over TCP 443 via system proxy is the most reliable transport for mixed corporate/consumer environments.
- **Inference**: Separating transport from E2E crypto cleanly addresses the proxy-inspection problem without requiring protocol forks.
- **Speculation**: IRC/Matrix bootstrap hints may prove unnecessary if Edge rendezvous is reliable enough; retained as fallback option.

## Appendix: Why IRC Is Not the Core Bus

IRC is useful as a **bootstrap/fallback bulletin board** (presence, endpoints, pubkeys), but not as the primary control-plane:
- weak identity and authorization model,
- limited delivery guarantees and backpressure,
- operational/security optics (often associated with legacy C2),
- not proxy-governance friendly as a primary corporate channel.

Use IRC/Matrix only as *bootstrap hints* if you want an "apocalypse fallback".
