# Proposal 034: Node Operator Binding and Derived Node Assurance

Based on:
- `doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`
- `doc/normative/50-constitutional-ops/pl/IDENTITY-ATTESTATION-AND-RECOVERY.pl.md`
- `doc/normative/50-constitutional-ops/pl/ROLE-TO-IAL-MATRIX.pl.md`
- `doc/normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md`
- `doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/20-memos/node-identity-layering-and-upgrade-path.md`
- `doc/schemas/node-identity.v1.schema.json`
- `doc/schemas/capability-passport.v1.schema.json`

## Status

Draft

## Date

2026-04-11

## Executive Summary

Participant attestation belongs to the participant or their underlying identity
chain. A `node-id` is a durable public operational identity, not a person. Still,
many policies need to know whether a node is controlled by an adequately attested
primary operator before allowing high-impact actions, spendable rewards, grants,
or trust-sensitive roles.

This proposal introduces one portable binding:

- `node-operator-binding.v1`

The binding is modeled as a small bundle over an existing passport primitive. It
connects:

- one `node/id`,
- one primary `operator/participant-id`,
- the operator's attestation reference and assurance level,
- and a derived `node-assurance-level` used only as an eligibility gate.

The operator's consent is expressed as a `capability-passport.v1` whose virtual
capability is:

- `node-primary-operator`

The target Node's consent is expressed as a separate Node signature over that
passport reference. A participant-issued passport alone is not a complete
binding; the Node must also accept the participant as its operator.

The binding does not merge participant reputation with node reputation, does not
make the node a person, and does not de-anonymize the operator by default.
It is also a node-held certificate: the node stores the active signed binding and
can present it when a peer, federation policy, grant process, or payout path needs
proof of operator assurance.

## Context and Problem Statement

Existing documents already separate the strata:

- a participant may have identity assurance and Proof-of-Personhood evidence,
- a `node-id` is the public pseudonym of operational responsibility,
- a node may have a custodian or operator,
- hosted participants must not inherit the operator's reputation, nor should the
  operator inherit theirs.

The missing portable contract is the explicit relation:

```text
participant attestation
  -> primary operator binding
  -> derived node assurance gate
```

Without this contract, reward systems and role gates face a bad choice:

- treat `node-id` as if it had its own human attestation,
- inspect local implementation state,
- or skip the assurance check entirely.

All three options complect identity, node operation, and policy enforcement.

## Goals

- Define a small artifact that binds one node to one primary operator participant.
- Let policies derive node assurance from the operator's attestation without
  collapsing node and participant identity.
- Preserve the existing semantic split between node reputation and participant
  reputation.
- Support the one-operator MVP while leaving a path for later multi-operator or
  organization-custodian policies.
- Give creator-credit, reputation-adjacent, and community-pool policies a clean
  eligibility input.

## Non-Goals

- This proposal does not define full root-identity disclosure.
- This proposal does not define hosted-user identity or pod-user reputation.
- This proposal does not define key rotation or mutable DID semantics.
- This proposal does not make `IAL` a reputation multiplier.
- This proposal does not define the final creator-credit or community-grant
  distribution policy.

## Decision

### 1. Add `node-operator-binding.v1`

The binding artifact records one active, mutually accepted claim that a
participant is the primary operator of a node.

Minimum fields:

| Field | Meaning |
|---|---|
| `binding/id` | Stable identifier of the binding record. |
| `passport` | Full `capability-passport.v1` issued by the operator participant. |
| `passport.capability_id` | MUST be `node-primary-operator` in v1. |
| `passport.node_id` | Public node identity being operated. |
| `passport.issuer/participant_id` | Participant identity of the primary operator. |
| `passport.scope.operator/role` | `primary` in v1. |
| `passport.scope.operator/attestation-ref` | Reference to the operator attestation basis. |
| `passport.scope.operator/assurance-level` | Assurance level of the operator participant. |
| `passport.scope.derived/node-assurance-level` | Assurance level carried by the node for gates. |
| `passport.scope.derivation/mode` | How the node assurance was derived. |
| `passport.scope.valid/from`, `passport.scope.valid/until` | Validity window. |
| `passport.scope.basis/refs` | Evidence references supporting the binding. |
| `node_acceptance` | Node-side acceptance of the passport-backed operator claim. |
| `node_acceptance.signature` | Node signature over the canonical acceptance payload. |

The corresponding schema seed is:

- `doc/schemas/node-operator-binding.v1.schema.json`

### 2. Passport Profile

`node-primary-operator` is a virtual capability profile. It does not mean that
the operator receives a generic right to execute arbitrary operations on the
Node. It means:

> I, the issuer participant, consent to be treated as the primary operator of
> this target Node for the bounded purpose of operator assurance.

The passport is signed by `issuer/participant_id`. Unlike infrastructure
capabilities such as `network-ledger` or `seed-directory`, this profile does not
require the issuer to be a software-pinned `sovereign-operator` by definition.
Instead, the passport scope carries the operator attestation basis and the
derived node assurance claimed for policy gates.

Consumers MUST verify the passport signature first and then apply the binding
profile policy:

1. `passport.capability_id` MUST equal `node-primary-operator`.
2. `passport.node_id` MUST equal `node_acceptance.node_id`.
3. `passport.issuer/participant_id` MUST equal
   `node_acceptance.operator/participant_id`.
4. `node_acceptance.passport_id` MUST equal `passport.passport_id`.
5. `node_acceptance.passport_hash` MUST match the canonical signed passport.
6. `node_acceptance.signature` MUST verify against the public key embedded in
   `node_acceptance.node_id`.

### 3. Derivation Rules

Consumers SHOULD enforce the following invariants:

1. `passport.scope.derived/node-assurance-level` MUST NOT exceed
   `passport.scope.operator/assurance-level`.
2. A node SHOULD have at most one active `operator/role = primary` binding at a
   time within a federation.
3. The binding MUST carry both a participant-issued passport and a node-signed
   acceptance over that passport reference.
4. If an active binding expires, is revoked, or is superseded, the node's derived
   assurance SHOULD fall back to unbound or `IAL0` until a replacement binding is
   accepted.
5. A reviewed exception MAY derive node assurance without an ordinary operator
   attestation path, but it MUST carry council or federation approval.

The schema captures the portable shape. Cross-field comparison such as "derived
level must not exceed operator level" remains a policy/runtime invariant.

### 4. Node-Held Certificate, Presentation, and Seed Directory Availability

An active `node-operator-binding.v1` is a certificate-like artifact held by the
node.

The node SHOULD store its current active binding alongside local identity
material or in an equivalent durable identity bundle. The node MAY present the
binding when a counterparty or policy gate needs to verify that:

- this `passport.node_id` is operated by the declared
  `passport.issuer/participant_id`,
- the operator explicitly accepted primary-operator responsibility,
- the node explicitly accepted that participant as its primary operator,
- the operator attestation basis was known at binding time,
- and the node may claim the declared
  `passport.scope.derived/node-assurance-level`.

Presentation is not a default gossip primitive. A node SHOULD disclose the
binding only to parties or local policy components that need it for a concrete
eligibility, audit, grant, payout, settlement, moderation, or role-admission
decision.

The ordinary presentation payload SHOULD contain the signed binding and any
public or selectively disclosable `basis/refs`. It MUST NOT include raw civil
identity unless a separate unsealing or abuse-disclosure procedure authorizes
that escalation.

For availability, a node MAY publish this binding to a Seed Directory, but this
MUST be an explicit disclosure-mode decision:

| Disclosure mode | Meaning |
|---|---|
| `local-only` | The node stores the binding locally and does not expose it unless another local policy component requests it. |
| `present-on-demand` | The node presents the binding only during a concrete peer or policy exchange. |
| `seed-directory` | The node publishes the passport-backed binding bundle to a directory for higher availability. |

A Seed Directory MUST NOT treat a participant-issued `node-primary-operator`
passport as sufficient by itself. Directory acceptance requires the full
`node-operator-binding.v1` bundle or an equivalent payload containing the
passport plus node acceptance. This prevents a participant from publicly claiming
operator status for a node that has not accepted them.

### 5. Semantics of Derived Node Assurance

Derived node assurance is an eligibility signal, not a reputation signal.

It may answer questions such as:

- "May this node receive spendable creator-credit rewards?"
- "May this node's operator request a community-pool recognition grant?"
- "May this node serve a role that requires an attested operator?"
- "Does this node satisfy the minimum operator assurance for a settlement or
  moderation duty?"

It must not answer:

- "Is this node reputable?"
- "Does this participant inherit the node's reputation?"
- "Does this node inherit all standing of the participant?"
- "Does this assurance level multiply voting or reputation weight?"

### 6. Relation to Reputation and Creator Credits

Low-attestation nodes and participants may still accumulate evidence:

- contribution history,
- attribution graph edges,
- signed usage traces,
- community signals,
- and non-spendable or review-pending recognition.

However, policies MAY require an active `node-operator-binding.v1` with a minimum
derived node assurance level before:

- converting creator-credit entitlement into a spendable balance,
- paying ORC from a community-pool grant,
- using reputation-adjacent evidence as a basis for economic disbursement,
- or admitting a node into high-trust operational roles.

This keeps evidence open while keeping spendable value and institutional power
behind explicit accountability gates.

### 7. Privacy Boundary

The binding SHOULD use `passport.issuer/participant_id`, scoped attestation
references, and selectively disclosable basis references, not raw civil identity.

If a dispute requires escalation from `node/id` to `custodian_ref` or
`root-identity`, it must use the existing unsealing and abuse-disclosure tracks.
The ordinary binding is not a deanonymization artifact.

## Example Scenario

1. A participant creates or imports a local node identity.
2. The participant obtains or refreshes an identity attestation.
3. The node prepares a `capability-passport.v1` profile with
   `capability_id = "node-primary-operator"` and `node_id` equal to its own
   `node:did:key`.
4. The operator signs that passport with the participant key.
5. The node verifies the passport and signs a `node_acceptance` record that
   names the passport, passport hash, node id, and operator participant id.
6. The node stores the resulting `node-operator-binding.v1` bundle as its current
   operator-assurance certificate.
7. If the operator chooses wider availability, the node publishes the bundle to a
   Seed Directory under an explicit `seed-directory` disclosure mode.
8. When needed, the node presents the binding to a federation policy, grant
   process, payout path, or peer that requires operator-assurance proof.
9. A federation policy reads
   `passport.scope.derived/node-assurance-level` when deciding whether
   creator-credit payout or community-pool grant disbursement may become
   spendable.

## Trade-Offs

Benefits:

- makes the participant-to-node assurance bridge explicit,
- reuses the existing passport signing, storage, presentation, revocation, and
  Seed Directory availability model,
- avoids treating node identity as human identity,
- gives reward and grant policies a small gate input,
- preserves reputation separation across node, participant, nym, and hosted-user
  subjects.

Risks:

- badly designed consumers may treat derived node assurance as reputation,
- consumers may accidentally accept the participant passport without checking the
  node acceptance,
- stale bindings may keep privileged access alive after operator loss,
- Seed Directory publication may over-disclose the node/operator relation,
- emergency help flows may become too strict if all support requires high
  assurance,
- multi-operator organizations will need a richer successor model.

Constraints:

- v1 is intentionally primary-operator-only,
- root identity remains hidden unless another procedure opens it,
- `node-primary-operator` is a virtual binding capability, not a generic runtime
  execution permission,
- cross-field assurance comparison is a policy invariant rather than a pure JSON
  Schema constraint.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Node key is stolen | Revoke or expire the binding; preserve operator attestation but drop node assurance until re-bound. |
| Operator attestation is revoked | Derived node assurance falls back to unbound or `IAL0`. |
| One person binds many nodes to farm rewards | Apply anti-Sybil accounting at the anchor or attestation source level. |
| Node overshares the certificate | Require need-bound presentation and redact or withhold non-public basis material. |
| Participant publishes a passport without Node consent | Require `node_acceptance` before treating any passport as a binding or accepting it into a Seed Directory binding surface. |
| Hosted user reputation collapses into operator reputation | Keep hosted-user and participant identity artifacts separate; do not use this binding for pod users. |
| Binding reveals too much identity | Store only participant and attestation references; use unsealing tracks for higher-stakes disclosure. |
| Emergency support is blocked by low assurance | Allow separate emergency or mutual-aid exception paths with stronger review rather than silent automatic conversion. |

## Open Questions

- Should v2 support multiple active operators with threshold control?
- Should organization-owned nodes use `org/custodian-ref` plus one or more
  participant operator bindings?
- Should creator-credit payout require `IAL1`, Proof-of-Personhood, or a
  stronger federation-defined threshold?
- Should community-pool mutual-aid disbursement use a lower gate than
  recognition-grant disbursement?
- Should `node-identity.v1` embed a current binding reference, or should bindings
  remain separate append-only records?
- Should Seed Directory support a dedicated `operator-binding` surface, or should
  this use the existing passport-backed capability catalog with profile-specific
  verification?
- Should peers receive the whole binding bundle, or should a later version add a
  smaller `node-operator-binding-presentation.v1` proof wrapper?

## Next Actions

1. Validate `node-operator-binding.v1.schema.json` with one positive example.
2. Add runtime support for issuing the `node-primary-operator` passport, signing
   node acceptance, storing the bundle, and optionally publishing it.
3. Add requirements when the reward/grant policy is promoted from concept to
   implementation.
3. Decide whether current Node identity creation should emit this binding during
   onboarding or only after participant attestation exists.
