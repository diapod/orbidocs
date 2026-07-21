# Federation Bootstrap and Trust HOWTO

This document leads from ceremony material to a running and diagnosable
federation bootstrap. It composes Federation Root, official-service
endorsements, Seed Directory, TLS evidence, capability passports, and peer
handshake without collapsing them into one notion of "trust".

The key ceremony has its own
[Federation Root Ceremony HOWTO](federation-root-ceremony-howto.en.md).
Conceptual boundaries are explained in the
[Federation Bootstrap and Trust FAQ](../faq/federation-bootstrap-and-trust-faq.en.md).

Unless a command says otherwise, run every `cargo` and `tools/...` command below
from the root of the `node/` workspace.

## Before starting: separate the proofs

| Layer | Question it answers |
| :--- | :--- |
| `federation-root.v1` | whose authority and policy constitute the federation? |
| official-service endorsement | is this service official in this federation? |
| capability passport | which capability scope belongs to this subject? |
| Seed Directory | which accepted discovery facts are currently projected? |
| TLS pin/CA/evidence | does the encrypted channel lead to the expected endpoint? |
| peer handshake | does the peer possess the declared Node identity key? |
| local policy | does this Node permit the effect in the current context? |

Do not replace a missing proof with another one. In particular, a certificate
is not a passport, bootstrap is not an endorsement, and a directory response is
not a peer handshake.

## 1. Select the ceremony profile

Use an explicit local fixture profile for disposable acceptance. Use
org/threshold custody conforming to the federation charter for production. A
production custodian key should be passphrase-encrypted; plaintext PEM is only
for an explicit short-lived fixture.

Before signing, establish:

- `federation/id`;
- custodian roster and threshold;
- sovereign/attestation subjects;
- endorsement policy;
- Seed Directory bootstrap;
- optional TLS pins;
- initial `pack_version` and policy refs.

## 2. Perform the root ceremony

Follow the ceremony document: workspace, keys, roster, frozen digest,
manifest, verify-before-sign, detached signatures, assembly, and final verify.

The result is a verified `federation-root.v1.json`. Archive the published
digest and manifest independently of the file itself. The artifact's transport
does not become its authority.

## 3. Install the root pack in the data dir

Place the verified file at:

```text
<data-dir>/federation-root.v1.json
```

Disable fixture fallback in a production profile:

```json
{
  "federation": {
    "allow_bundled_fixture_root": false
  }
}
```

Validate configuration before startup:

```sh
cargo run -p orbiplex-node-daemon -- check-config \
  --data-dir "$ORBIPLEX_DATA_DIR"
```

The loader must reject an invalid signature, unmet threshold, unknown custody
policy, `pack_version` rollback, the same version with a different digest, and
a conflict with the active `federation/id` recorded in the data dir.

## 4. Start the daemon and inspect activation

First activation and every root-fingerprint change require a full restart.
SIGHUP or hot reload may report that a candidate requires restart, but must not
change the process's active federation.

After startup, inspect:

```http
GET /v1/seed-directory
GET /v1/operator/network/peer-supervisor/status
GET /v1/operator/federation-service-endorsements
```

Expect a consistent `federation/id`, root digest, and `pack_version`. Missing
usable Seed Directory sources should be visible as isolated/bootstrap or
degraded, not hidden behind an empty list.

## 5. Verify Seed Directory bootstrap

Every active bootstrap entry should carry:

- explicit `enabled`;
- `node/id` and endpoint consistent with the root;
- a valid official-service endorsement when it claims
  `federation-endorsed`;
- HTTPS and valid `tls_certificate_sha256` when root pinning is used;
- capability passport or registration required by the consumer.

An entry without an active endorsement may remain advisory. Do not repair it
by locally rewriting its trust level to `official`.

## 6. Configure additional trusted directories

`network.seed_directory_trust[]` describes locally accepted sources and their
trust levels. Select one explicit query policy:

- `preferred-directory` for deterministic primary with controlled fallback;
- `quorum` when a minimum of independent directories must agree;
- `weighted-trust` when sources carry explicit unequal weights.

Weights, policy refs, and federation ids are local-policy inputs. The embedded
directory should not vote for itself without explicit opt-in. Every result is
still verified by the consuming boundary.

## 7. Enable trusted Agora replay when needed

`network.seed_directory_agora_replay` is opt-in. When enabled, it must name an
explicit executor/provider and bounded page limit. The runtime replays `adv`,
`cap`, and `revocations` lanes only for configured federation ids.

After the first pass, inspect `/v1/seed-directory` for:

- cursor per `(federation_id, lane)`;
- accepted and rejected counts;
- last run and last error;
- skip reason when a source is ineligible.

One malformed record must be rejected and diagnosed, not stop the entire
daemon or enter the projection as a default value.

## 8. Issue or install a service endorsement

The operator surface exposes:

```http
POST /v1/operator/federation-service-endorsements/issue
POST /v1/operator/federation-service-endorsements/install
GET  /v1/operator/federation-service-endorsements
```

Issuance must conform to the active root custody policy. Under org/threshold,
do not pretend that one local signature replaces the ceremony. Install records
the ingress-enforced source; the body may provide only additional
`source/detail` and cannot rewrite audited provenance.

After installation, verify node id, capability id, validity window, signer
authority, and revocation status. Only then may a consumer project official
status.

## 9. Register the capability and inspect discovery

A Seed Directory capability registration is passport-backed and monotonic by
positive `sequence/no`. Identical republish is idempotent; an older sequence
cannot overwrite a newer one. Expired or revoked registrations must not appear
in active lookup.

Inspect separately:

1. registration and passport;
2. official endorsement when required;
3. endpoint projection;
4. TLS evidence;
5. peer handshake during a real connection.

A green lookup without the last two steps is a discovery candidate, not proof
of a working session.

## 10. Request query attestation only when useful

Critical `/adv`, `/cap`, and `/revocations` reads may request:

```text
attest=seed-directory-query.v1
```

Verify the canonical response digest, normalized query, projection high-water,
validity window, and signer id. A missing signer under an explicit attestation
request should return `503 attestation_unavailable`; without the parameter the
response remains an ordinary directory projection.

## 11. Inspect TLS and peer identity as separate layers

When bootstrap carries a pin, compare `sha256:<base64url>` with raw leaf
certificate DER. The connection must use HTTPS/WSS. Node endpoint evidence may
use active `sha256-leaf-der` or `sha256-spki` according to policy.

After TLS establishment, perform the Orbiplex peer handshake and verify the
declared `node:did:key`. An opaque `route:` certificate subject limits stable
identity leakage to TLS scanners; it does not replace the handshake.

## 12. Rotate without split brain

For a root-pack change:

1. prepare a higher `pack_version`;
2. perform the complete ceremony and final verify;
3. distribute the pack outside the channel whose authority is changing;
4. stop the daemon;
5. atomically replace `federation-root.v1.json`;
6. run `check-config`;
7. start the daemon and inspect every trust layer.

Never reuse a `pack_version` for another digest. During TLS-pin rotation,
coordinate new-certificate availability with consumer restart; the MVP does
not keep two active pins for one endpoint.

## 13. Run acceptance

Root helper and acceptance-seeder contracts are covered by:

```sh
python3 tools/acceptance/test_federation_root_acceptance.py
```

Story 010 and Story 011 build the runtime root after obtaining real Node ids,
attach bounded endorsements, and inspect `/v1/seed-directory` before higher
flows begin. For component coverage, run:

```sh
cargo test -p orbiplex-node-seed-directory
cargo test -p orbiplex-node-daemon seed_directory
cargo test -p orbiplex-node-daemon federation_root
```

An acceptance fixture proves the local path. It does not prove that the
production roster, external pack distribution, or public endpoints are already
operationally ready.

## 14. Diagnose from root to effect

When discovery fails, inspect in this order:

1. root signature, threshold, digest, and `pack_version`;
2. bootstrap endorsement and revocation;
3. Seed Directory source status and replay;
4. capability passport/registration;
5. TLS pin or endpoint evidence;
6. peer handshake;
7. consumer-local policy.

This order disentangles the cause. Repairing from the other end – for example
by adding a peer allowlist – may hide missing authority, but does not create it.
