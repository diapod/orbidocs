# DIA Orbiplex-Main Root Charter

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | DIA Constitution (root-of-trust and appeal principles); `ENTRENCHMENT-CLAUSE.en.md`; `PANEL-SELECTION-PROTOCOL.en.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`; `doc/project/40-proposals/076-federation-identity-and-network-selector.md` (§4, §6, P076-004/013/014/026) |

---

## 1. Purpose of the Document

Proposal 076 defines the *shape* of the `orbiplex-main` federation root (an
org-kind threshold root carried by `federation-root.v1`) and explicitly
excludes from its scope the governance deliverables that make that root
production-trustworthy: the concrete custodian roster, the concrete signing
keys, the final custody threshold, the rotation procedure, and the appeal
body. This charter is the home for those deliverables. Until it is adopted at
version `1.0.0` or later with a filled roster, `orbiplex-main` remains a
development bootstrap fixture and MUST NOT be treated as production root
authority (P076-004).

## 2. Scope and Authority Boundary

This charter governs: custodian eligibility and roster, custody keys,
threshold, root-pack ceremony conduct, rotation and succession, emergency
custodian removal, official-service endorsement issuance, and the appeal
path. It does not define schema mechanics (Proposal 076), runtime
verification (the Node loader and `capability-binding`), or federation
membership at large (`FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`).

Nothing in this charter can override cryptographic verification: a pack or
endorsement that fails signature or custody checks stays rejected while any
appeal runs. Appeals change *who decides next*, never *what verifies now*.

## 3. Root Shape and Threshold

- The `orbiplex-main` root is an **org-kind threshold root**
  (`org:did:key:...`) whose custody policy carries the purpose
  `federation-root`.
- The custody threshold is **`2-of-3` at minimum**. An amendment may raise
  it; no amendment may lower it below `2-of-3`. Threshold semantics follow
  Proposal 076: M-of-N unique authorized signing keys, not M-of-N people.
- The roster size MUST be at least 3 custodian keys at all times.

## 4. Custodian Roster

| Seat | Custodian identity (`participant:did:key:...`) | Key fingerprint (`z...`) | Since |
| :--- | :--- | :--- | :--- |
| 1 | *TBD — governance appointment pending* | *TBD* | — |
| 2 | *TBD — governance appointment pending* | *TBD* | — |
| 3 | *TBD — governance appointment pending* | *TBD* | — |

Eligibility (per P076-013):

- a custodian identity is a **dedicated operational identity** used only for
  root-pack approval, rotation, and recovery ceremonies,
- it MUST NOT be a nym, an ordinary operator identity, or a day-to-day
  participant key, and it lives in a **separate custodian `data-dir`**,
- no single natural person or organization may control a number of custodian
  keys sufficient to meet the threshold alone,
- a custodian seat is vacated by resignation, by confirmed key compromise, or
  by removal decided under §7.

## 5. Keys

- Custodian keys are dedicated Ed25519 keys generated during a ceremony using
  the P076-014 tooling; they are never reused for any other key role.
- Private key material is stored under the custodian's encrypted `data-dir`
  flow (passphrase via stdin only; never in shell arguments or plaintext
  files).
- Suspected compromise of any custodian key triggers §7 without waiting for
  proof of misuse — rotation is cheap, standing compromise is not.

## 6. Ceremony

Root-pack releases follow the frozen ceremony shape (P076-026): authored
pack → manifest digest → independent verification of the digest by every
signer → detached signatures collected offline → deterministic assembly →
verification → publication. `pack_version` increases monotonically; loaders
reject rollback and same-version digest swaps. Every signer verifies the
exact bytes they sign; no custodian signs a digest they have not derived
themselves.

## 7. Rotation, Succession, and Emergency Removal

- **Planned rotation**: the outgoing and incoming rosters co-sign a
  transitional pack during an overlap window, then the incoming roster signs
  the next pack alone. Overlap length is set per rotation and recorded in the
  pack's `policy_ref` document.
- **Emergency removal** (compromise or incapacity): the remaining custodians,
  meeting the threshold without the affected key, sign a new pack that
  removes it. If the threshold cannot be met without the affected key, the
  appeal body (§9) convenes an extraordinary re-seating.
- Rotation lapses derived authority for free: endorsements and other
  artifacts verified against the active pack stop resolving when their
  signers leave the roster (Proposal 076 §6).

## 8. Official-Service Endorsements

The roster acts as the sovereign org subject of `orbiplex-main` for
`federation-service-endorsement.v1` issuance (Proposal 076 §6): issuance
requires the custody threshold (ceremony per P076-018); **revocation is
deliberately asymmetric** — any single authorized custodian key may revoke,
because unilateral withdrawal narrows trust and is fail-safe.

## 9. Appeal Path

- The appeal body is drawn using `PANEL-SELECTION-PROTOCOL.en.md`, with the
  conflict-of-interest rules applied against the current roster (no sitting
  custodian, nor an identity operationally tied to one, may sit on a panel
  reviewing that roster's decision).
- Appealable matters: contested rotation or removal, refusal to issue or
  revoke an official-service endorsement, and contested custody-policy
  amendments.
- An appeal outcome binds the roster to re-run the contested decision under
  the panel's finding; it never substitutes the panel's signature for the
  custody threshold.

## 10. Amendment

Amendments to this charter require the custody threshold in force and MUST
respect `ENTRENCHMENT-CLAUSE.en.md`. The charter version is bumped on every
amendment; the root pack's `policy_ref` SHOULD reference the charter version
under which it was signed.

## 11. Adoption Status

This document is a **draft skeleton** (0.1.0-draft): the roster and key
table are deliberately unfilled. Adoption at `1.0.0` requires: three named
custodian identities with generated keys, a signed production
`federation-root.v1` pack replacing the bundled fixture, and production
packaging that disables `federation.allow_bundled_fixture_root` (Proposal
076, Next Actions 1–2). Until then, every consumer MUST treat
`orbiplex-main` trust as development-grade.
