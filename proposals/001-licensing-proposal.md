# Licensing Baseline for Orbiplex Swarm Components

Based on: `challenges/001-licensing.md`

## Status
Proposed

## Date
2026-02-22

## Context

Orbiplex Swarm includes multiple artifact classes with different legal and ecosystem requirements:
- runtime software (`swarm-node`, `orchestrator`, GUI assistant),
- machine-readable protocol artifacts (schemas, test vectors, reference implementations),
- documentation artifacts (protocol prose, manuals, runbooks),
- UI font assets.

The project needs a license baseline that:
1. preserves interoperability across organizations and infrastructures,
2. minimizes legal ambiguity in mixed repositories,
3. supports adoption without losing governance control.

Input analysis is documented in:
- `challenges/licensing.md`
- `stories/story-001.md`
- `requirements/requirements-001.md`

## Options Considered

### Option A: Strong Copyleft-First Everywhere (`GPL-3.0` for most code and artifacts where possible)

- Pros:
  - strongest anti-enclosure posture for software distribution.
  - clear reciprocity expectation for derivatives.
- Cons:
  - higher integration friction for mixed enterprise/federated participants.
  - added complexity for protocol assets and tooling ecosystems.
  - unsuitable for some artifact classes (fonts/docs need separate handling anyway).

### Option B: Fully Permissive Everywhere (`MIT/BSD` for code + permissive docs license)

- Pros:
  - lowest adoption friction.
  - broad compatibility and simpler downstream integration.
- Cons:
  - weaker reciprocity incentives.
  - weaker patent clarity under MIT/BSD compared to Apache-2.0.
  - higher risk of fragmented closed forks reducing commons contribution.

### Option C: Layered Hybrid Baseline by Artifact Class

- Pros:
  - aligns legal model with artifact semantics.
  - balances adoption, patent clarity, and documentation openness.
  - reduces cross-artifact licensing mistakes.
- Cons:
  - more governance overhead than single-license policy.
  - requires stricter repository hygiene (SPDX, file placement, CI checks).

## Decision

Adopt **Option C (Layered Hybrid Baseline)** with the following defaults:

1. Runtime software (`swarm-node`, `orchestrator`, GUI assistant): `Apache-2.0`.
2. Protocol schemas, reference vectors, executable examples, SDK code: `Apache-2.0`.
3. Documentation prose (manuals, architecture docs, protocol text): `CC BY 4.0`.
4. Font assets: `OFL-1.1`.
5. New modules MUST NOT introduce `GPL-2.0-only`.
6. Any deviation from these defaults requires a new ADR or an ADR amendment with explicit compatibility analysis.

Rationale:
- `Apache-2.0` provides strong interoperability and explicit patent grant posture.
- `CC BY 4.0` keeps documentation reusable and attribution-preserving.
- `OFL-1.1` is purpose-specific for fonts and avoids misuse in code artifacts.

## Consequences

### Short-term

1. Need to add SPDX headers and license metadata across existing files.
2. Need CI checks for dependency license compatibility and disallowed licenses.
3. Need contributor guidance explaining license boundaries by artifact class.

### Long-term

1. Lower legal friction for federated adoption and downstream integrations.
2. Better patent-risk predictability for runtime components.
3. Clearer governance for multi-repo growth and protocol reuse.
4. Ongoing requirement to manage exceptions explicitly through ADR process.

## Implementation Notes

1. Create `LICENSE` and `NOTICE` files in repositories containing runtime code.
2. Keep documentation and executable code in separate paths to avoid mixed-license ambiguity.
3. Add a machine-readable third-party license inventory to release artifacts.
4. Define a review checklist gate: "license compatibility verified" before merge.
