# Communication Protocol Baseline for Orbiplex Swarm

Based on: `challenges/002-sybil.md`

## Status

Proposed (Draft)

## Date

2026-02-22

## Executive Summary

This proposal defines the node-to-node communication architecture for the Orbiplex Swarm, designed for mixed environments (consumer networks + corporate networks with mandatory proxy/TLS inspection). The design is built around Ed25519 identity, a proxy-friendly WSS transport, optional message-level E2E encryption with PFS, and untrusted Edge relay nodes. Three security profiles (`CORP_COMPLIANT`, `E2E_PREFERRED`, `E2E_REQUIRED`) allow nodes to operate under different governance constraints without breaking connectivity.

## Context and Problem Statement

Orbiplex Swarm nodes must communicate reliably across heterogeneous network environments:
- Consumer nodes behind NAT.
- Corporate nodes behind mandatory HTTPS proxies with TLS inspection (MITM).
- Public Edge nodes providing relay and rendezvous.

Transport-level TLS alone does not guarantee end-to-end privacy when corporate proxies inspect traffic. The protocol must therefore separate transport security from message-level confidentiality, while remaining compatible with enterprise governance requirements (proxy-only egress, system trust stores, DLP visibility).

Additionally, the hostile nature of open-membership swarms requires built-in Sybil resistance and DoS mitigation at the protocol level.

Input analysis is documented in:
- `challenges/002-sybil.md`
- `stories/story-001.md`
- `requirements/requirements-001.md`

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
- Each node has a long-term **`identity-key`** (Ed25519).
- **`node-id = H(pubkey)`** (or compatible stable derivation).
- All control-plane messages are **signed**.

#### Session keys and continuity
- Nodes may use short-lived **session keys**:
  - `identity-key` signs a "session certificate" binding `session-pubkey` + validity window.
- Reputation attaches to the long-term identity; session keys reduce the blast radius of compromise.

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

### 4. Transport vs. end-to-end crypto

#### Transport
- Primary: **HTTPS/WSS (TCP 443)**, proxy-compatible, long-lived sessions.
- TLS verification uses **system trust store** in corporate mode.

#### End-to-end confidentiality / PFS (optional but crucial)
Because corporate proxy can MITM transport, real privacy requires:
- **E2E encryption at message layer** (AEAD).
- **PFS** via ephemeral ECDH (X25519) + frequent rekeying (time or message count).

### 5. Security profiles (client policy knob)

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
- If `e2e` is present, `body` may be empty and all payload moves into `ciphertext` (with `aad` carrying the signed metadata).

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
  "to": "nodeB",
  "ts": 1700000000000,
  "ttl_s": 30,
  "nonce": "c3b2...uuid",
  "seq": 1,
  "intent": "swarm/hello",
  "body": {
    "identity_pub": "ed25519:...",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600000,
    "capabilities": {
      "transport": ["wss443-proxy"],
      "e2e": ["preferred", "required"],
      "rekey": {"messages": 2048, "minutes": 30}
    }
  },
  "sig": "ed25519sig(identity over envelope)"
}
```

Notes:
- `session_pub` is ephemeral for E2E key agreement.
- `sig` authenticates identity and binds the ephemeral key to the long-term identity.

#### Step 2 — `HELLO_ACK` (peer agrees + returns its ephemeral key)
**B -> Edge -> A**

```json
{
  "v": 1,
  "from": "nodeB",
  "to": "nodeA",
  "ts": 1700000000500,
  "ttl_s": 30,
  "nonce": "a91e...uuid",
  "seq": 1,
  "intent": "swarm/hello-ack",
  "body": {
    "identity_pub": "ed25519:...",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600500,
    "e2e_mode": "preferred"
  },
  "sig": "ed25519sig(identity over envelope)"
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

### 9. `CORP_COMPLIANT` governance checklist

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

## Open Questions

1. **Canonicalization format**: EDN or JSON as the canonical signing format? EDN is natural for Clojure; JSON has wider tooling. Needs a decision before implementation.
2. **Metadata privacy**: Should a metadata-wrapping layer be specified for `E2E_REQUIRED` mode, or is metadata exposure to Edge acceptable?
3. **Group messaging**: Current envelope supports `group-id` in `to`, but group key management (e.g., sender keys, MLS-style) is unspecified.
4. **Large payload transfer**: Data-plane for large payloads is mentioned (content-hash references) but not specified. Needs a separate proposal or extension.
5. **Edge incentives**: What motivates operators to run Edge nodes? Token rewards, reputation, altruism? Ties into the broader economics model.
6. **Admission bootstrap**: How does the first node get admitted when no sponsors exist yet? Genesis ceremony or initial trust set?

## Next Actions

1. **Specify canonical envelope format** (EDN vs JSON, canonicalization rules, signing algorithm details) as a sub-document or appendix.
2. **Implement MVP transport**: WSS/HTTP2 over 443 via system proxy with Edge relay (no E2E initially).
3. **Implement Edge presence + relay** (no-trust pipe, rate limiting, presence table).
4. **Add E2E mode** (`E2E_PREFERRED` first, then `E2E_REQUIRED`) with rekey schedule.
5. **Add admission control** (invite/sponsor tokens) + DoS gates.
6. **Add optional direct/UDP paths** later (optimization only).
7. **Write story and requirements** for group messaging and large payload transfer scenarios.

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
