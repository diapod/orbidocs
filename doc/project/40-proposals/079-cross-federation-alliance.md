# Proposal 079: Cross-Federation Alliance

Based on:
- `doc/project/20-memos/whisper-corpus-composition.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/60-solutions/041-federation-root/041-federation-root.md`

Related schemas:
- `alliance-policy.v1`

## Status

Draft

## Date

2026-07-04

## Executive Summary

Proposal 076 deliberately keeps **federation** narrow: one active
`federation_id`, selected from one `federation-root.v1`, per node `data-dir`.
This proposal freezes the separate cross-federation cooperation concept named
**alliance**.

An alliance is not a second federation, not Seed Directory trust, and not a
transport reachability shortcut. It is a policy input used by local admission
logic when Room, Whisper, Corpus, Artifact Delivery, INAC, or future components
need to decide whether work may intentionally cross federation boundaries.

The minimal contract is `alliance-policy.v1`: a **unilateral declaration** by
one federation. A cooperation relationship becomes operationally active only
when every involved federation holds a fresh, matching declaration half. The
effective scope is the intersection of the halves' `allowed_scopes`, with
`denied_scopes` overriding any allow.

Runtime enforcement is deferred. The schema and semantics are frozen now so
future consumers do not invent incompatible meanings for cross-federation
cooperation.

## Context and Problem Statement

Several Orbiplex surfaces already need a vocabulary beyond one federation:

- Room distinguishes `federation-local`, `cross-federation`, and `global`
  exposure.
- Whisper can publish signals with `cross-federation` or public aggregate
  disclosure.
- Corpus may solicit bids outside one federation.
- Memarium must prevent implicit cross-federation leakage when Room or other
  group membership spans more than one federation.

Without one canonical alliance model, each consumer would likely invent its own
interpretation: one might trust a Seed Directory entry, another might pin a
root-pack digest, and a third might treat Matrix reachability as policy. Those
would be different authority systems hiding under one word.

## Goals

- Define `alliance` as a canonical cross-federation cooperation concept above
  the P076 node-local federation selector.
- Define `alliance-policy.v1` as a unilateral policy half signed under the
  issuer federation's own root/custody rules.
- Keep alliance validity stable across routine federation-root pack rotations by
  pinning member subjects, not root-pack digests.
- Define effective scope as intersection of matching halves, with deny
  overriding allow.
- Allow private/local-only alliances. The fact that two federations cooperate
  can itself be sensitive.
- Keep unknown scopes fail-closed through a closed v1 scope registry.
- State that alliance is only an input to local admission and never replaces
  verification of artifacts, endorsements, memberships, or service authority.

## Non-Goals

- Not a cross-federation runtime verifier implementation.
- Not a remote co-signing or joint ceremony protocol.
- Not a Seed Directory authority transfer. Seed Directory authority remains
  federation-local unless independently endorsed and verified.
- Not a way to widen Memarium Federated replication. Memarium promotion across
  federation boundaries still requires explicit target-space transition.
- Not transitive. If A is allied with B and B is allied with C, A is not allied
  with C unless A and C hold matching policy halves.
- Not a replacement for Room membership, Artifact Delivery authorization,
  capability passports, official-service endorsements, or local host policy.

## Proposed Model

### 1. Alliance as Matching Unilateral Halves

`alliance-policy.v1` is a unilateral declaration by exactly one federation.
It says: "for this deterministic alliance id, this federation is willing to
cooperate with these member federations under these scopes and denials."

A cross-federation alliance is operationally active only when all required
member federations hold current declarations that match on:

1. the same deterministic `alliance_id`,
2. the same unordered member federation set,
3. issuer federation membership in that set,
4. successful signature/custody verification against each issuer's active
   federation root,
5. non-expired, non-revoked, highest-known `sequence_no` per issuer.

The issuer subject is not an independent third axis. Runtime MUST verify that
`issuer_subject_ref` matches the `members[]` entry whose `federation_id` equals
`issuer_federation_id`. Runtime also MUST enforce unique signer keys and
`expires_at > issued_at`; portable JSON Schema can reject exact duplicate
signature objects, but it cannot express these cross-field/runtime invariants
fully.

The active scope is calculated locally:

```text
effective_allowed_scopes = intersection(all halves.allowed_scopes)
                           - union(all halves.denied_scopes)
```

If the intersection is empty, the alliance exists as an auditable policy fact
but authorizes no operation.

This shape avoids a cross-federation ceremony for every alliance update. Each
federation can narrow, rotate, expire, or revoke its own half. Revocation is
therefore fail-safe: withdrawing one half disables the cooperation locally once
that withdrawal is observed.

### 2. Stable Member Identity, Digest as Evidence

Alliance membership is pinned to stable federation identity material:

- `members[].federation_id`,
- `members[].sovereign_subject_ref`.

`members[].root_digest_at_issuance` and
`members[].root_pack_version_at_issuance` are evidence only. They record what
root pack the issuer saw when it authored the policy half. They are not
validity pins.

A verifier MUST re-check, at the point of use, that each member subject still
resolves in that member federation's active root under the expected custody
rules. Decisions MUST NOT be cached across root-pack changes. Routine root-pack
rotation therefore does not invalidate the alliance by digest churn; removing
or changing the sovereign subject does.

### 3. Local Admission Input, Never Authority Substitution

An alliance is an input to local admission. It never substitutes for verifying
artifacts or authority.

Consequences:

- Room must still verify membership, room policy, and live credentials.
- Whisper must still verify author identity, disclosure scope, and publication
  policy.
- Corpus must still verify bids, offers, procurement contracts, and settlement
  authority.
- Artifact Delivery and INAC must still verify delivery authorization.
- Seed Directory entries do not become federation-official through alliance;
  official service status still requires `federation-service-endorsement.v1`.
- Memarium Community-to-Public or cross-space promotion remains an explicit
  policy transition with provenance.

The alliance answers only: "may local policy consider this other federation
inside this declared cross-federation cooperation scope?" It does not answer:
"is this artifact valid?" or "does this service have authority?"

### 4. Publication Surface

A policy half may be distributed through several surfaces, none of which confer
authority by themselves:

- `local-only`: kept in local policy storage or exchanged out of band.
- `seed-directory`: advertised through a Seed Directory entry or metadata ref.
- `federation-root-ref`: referenced from a future federation-root extension or
  adjacent signed pack metadata.
- `public`: intentionally published as a public policy artifact.

Private alliances are valid. Consumers MUST verify the artifact and issuer
root/custody regardless of how the half was obtained.

### 5. Scope Registry

`alliance-policy.v1` uses a closed v1 registry. Unknown scope values fail
closed at schema-gate or equivalent boundary validation.

Initial scopes:

| Scope | Meaning |
|---|---|
| `room/cross-federation` | Room admission may consider members rooted in the allied federation set. |
| `whisper/cross-federation` | Whisper policy may consider cross-federation signal exchange under local disclosure rules. |
| `corpus/cross-federation` | Corpus query/bid discovery may include allied federations. |
| `artifact-delivery/cross-federation` | Artifact Delivery admission may consider allied federation subjects. |
| `inac/cross-federation` | Inter-node Artifact Channel admission may consider allied federation subjects. |
| `agora/topic-bridge` | Agora topic bridging may consider allied federation topics or relays. |

Future scopes require schema/proposal update. They are not free strings.

### 6. Identifier and Sequencing Rules

`alliance_id` is deterministic over the sorted member federation ids and a
policy-family label. The v1 recommendation is:

```text
alliance_id = "alliance:sha256:" + base64url_no_pad(
  sha256("orbiplex-alliance-policy-v1\0" || join("\n", sort(federation_id)))
)
```

`sequence_no` is monotonic per `(issuer_federation_id, alliance_id)`. Verifiers
use the highest valid sequence they know for each issuer. Older sequence numbers
are rollback candidates and MUST NOT replace newer accepted halves.

### 7. Field Naming Convention

`alliance-policy.v1` belongs to the config-registry / policy-artifact family,
like `federation-root.v1`, not to the inter-node message-envelope family.
It therefore uses snake_case field names (`alliance_id`,
`issuer_federation_id`, `sequence_no`) rather than namespaced slash keys.

## Contract Shape

Minimal happy-path instance:

```json
{
  "schema": "alliance-policy.v1",
  "alliance_id": "alliance:sha256:...",
  "issuer_federation_id": "orbiplex-main",
  "issuer_subject_ref": "org:did:key:z6Mk...",
  "sequence_no": 1,
  "members": [
    {
      "federation_id": "orbiplex-main",
      "sovereign_subject_ref": "org:did:key:z6Mk...",
      "root_digest_at_issuance": "sha256:...",
      "root_pack_version_at_issuance": 42
    },
    {
      "federation_id": "research-eu",
      "sovereign_subject_ref": "org:did:key:z6Mk...",
      "root_digest_at_issuance": "sha256:...",
      "root_pack_version_at_issuance": 7
    }
  ],
  "allowed_scopes": ["room/cross-federation", "corpus/cross-federation"],
  "denied_scopes": ["agora/topic-bridge"],
  "publication": { "mode": "local-only" },
  "issued_at": "2026-07-04T00:00:00Z",
  "expires_at": "2026-10-04T00:00:00Z",
  "policy_ref": "policy:alliance:orbiplex-main:research-eu:2026q3",
  "signatures": [
    {
      "alg": "ed25519",
      "key_public": "z6Mk...",
      "value": "..."
    }
  ]
}
```

Schema and fixtures:

- `doc/schemas/alliance-policy.v1.schema.json`
- `doc/schemas/examples/orbiplex-main-research-eu.alliance-policy.json`
- `doc/schemas/examples/invalid/duplicate-signature.alliance-policy.json`
- `doc/schemas/examples/invalid/unknown-scope.alliance-policy.json`
- `doc/schemas/examples/invalid/non-goals-field.alliance-policy.json`
- `doc/schemas/examples/invalid/root-digest-as-required-pin.alliance-policy.json`

## Trade-offs

- Unilateral halves avoid cross-federation signing ceremonies, but consumers
  must assemble and compare multiple local facts before declaring an alliance
  active.
- Stable subject pins survive routine root-pack rotation, but validity checking
  requires access to each member's active root view at use time.
- A closed scope registry prevents policy confusion, but every new surface needs
  an explicit schema/proposal update.
- Allowing `local-only` publication protects sensitive cooperation, but makes
  discovery an operator concern until a runtime distribution profile exists.

## Failure Modes and Mitigations

| Failure | Risk | Mitigation |
|---|---|---|
| Digest-pinned alliance breaks on routine pack rotation | Unnecessary re-ceremony and brittle operations | Pin stable sovereign subjects; keep digest only as evidence. |
| One federation widens scope unilaterally | Other members are dragged into broader cooperation | Effective scope is intersection; `denied_scopes` override allow. |
| Seed Directory trust is mistaken for alliance authority | Directory reachability becomes governance authority | Alliance never transfers Seed Directory authority; official services still need endorsements. |
| Artifact verification skipped because alliance exists | Invalid data crosses policy boundary | Alliance is only admission input; artifact and capability verification remain mandatory. |
| Unknown future scope accepted silently | Scope confusion across consumers | Closed v1 registry and fail-closed schema validation. |
| Private alliance accidentally disclosed | Sensitive cooperation graph leaks | `publication.mode = local-only` is a valid first-class mode. |
| A->B and B->C treated as A->C | Transitive authority appears without consent | Non-transitivity is an invariant; each member set requires matching halves. |

## Open Questions

The concept and minimal policy contract frozen here have no open questions.
Runtime questions remain tracked as deferred implementation rows below.

1. **Remote root acquisition for member verification.** How does a verifier
   obtain and refresh another member federation's active `federation-root.v1`
   when resolving `members[].sovereign_subject_ref` at use time? Sensible
   default for the first runtime slice: local-only import/export of trusted root
   snapshots, with Seed Directory or public distribution deferred until P079-005.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Task | Status | Notes |
|---|---|---|---|
| P079-001 | Define canonical alliance concept and invariants | done | Alliance is cross-federation cooperation above P076's single-federation selector; non-transitive; no Seed Directory authority transfer; no Memarium widening; admission input only. |
| P079-002 | Define `alliance-policy.v1` schema and fixtures | done | Minimal unilateral policy-half contract with snake_case fields, stable member subject pins, evidence-only root digest/version, closed scope registry, `sequence_no`, publication mode, and deny-overrides-allow semantics. |
| P079-003 | Runtime verifier for one policy half | deferred | Should reuse the P076 endorsement verifier shape: domain-separated canonical payload, issuer root/custody resolution, issuer subject matching the issuer member entry, `expires_at > issued_at`, unique signer keys, expiry, revocation, sequence rollback refusal, and no cross-pack decision cache. |
| P079-004 | Active alliance resolver | deferred | Collect matching halves, select highest valid sequence per issuer, verify same member set, compute scope intersection minus denied scopes, and expose local admission decision. Empty effective scope is an explicit auditable state, not silent failure. |
| P079-005 | Distribution and revocation profile | deferred | Decide whether first runtime transport is local-only import/export, Seed Directory metadata, federation-root-adjacent refs, or public publication. |
| P079-006 | Room consumer integration | deferred | Room may consume active alliance decisions for `cross-federation` admission, while still verifying room membership/policy independently. |
| P079-007 | Whisper, Corpus, Artifact Delivery, INAC, and Agora consumers | deferred | Each consumer must map its own operation to the closed scope registry and still verify its own artifacts/capabilities. |
| P079-008 | MVP readiness follow-through | done | P076-008 is closed as concept plus minimal policy contract; runtime enforcement remains deferred here and is not a hard-MVP release blocker. |

## Next Actions

1. When a runtime consumer needs alliance enforcement, implement P079-003 and
   P079-004 before touching consumer-specific policy.
2. Choose the first distribution profile (likely local-only import/export for a
   small pilot) and only then wire Seed Directory or public publication.
3. Add consumer-specific tests that prove alliance is an admission input, not a
   substitute for artifact, capability, or membership verification.
