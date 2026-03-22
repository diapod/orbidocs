# Licensing Challenges for Orbiplex Swarm Components

Based on: `doc/project/30-stories/story-001.md`, `doc/project/50-requirements/requirements-001.md`  
Date: `2026-02-22`  
Status: Draft

## Executive Summary

Orbiplex Swarm needs a licensing strategy that supports federation, interoperability, and long-term governance while reducing legal friction for adopters.

This document analyzes 10 popular FLOSS licenses (using the 2025 OSI pageview ranking as a measurable popularity proxy) and maps them to potential Orbiplex components:
- software components (`node`, `orchestrator`, `GUI assistant`),
- protocol artifacts (schemas, examples, reference behaviors),
- documentation assets (manuals, playbooks, architecture docs).

Recommended baseline:
1. Use `Apache-2.0` for core software components where ecosystem adoption and patent clarity are critical.
2. Use `LGPL-3.0` selectively for libraries where proprietary linking is acceptable but library improvements should remain open.
3. Avoid `GPL-2.0-only` for new components due compatibility constraints.
4. Use `CC BY 4.0` or `CC BY-SA 4.0` for documentation; keep software code and schemas under software licenses.
5. Use `OFL-1.1` only for fonts and related font software.

## Context and Problem Statement

Orbiplex Swarm combines:
- distributed runtime software,
- protocol definitions and implementation contracts,
- operational and user documentation.

If these layers are licensed inconsistently, the project can suffer:
- license incompatibility between components,
- blocked integrations,
- unclear patent posture,
- weak reciprocity incentives,
- compliance overhead for downstream adopters.

The licensing model must therefore encode a deliberate trade-off between:
- adoption speed (permissive licenses),
- reciprocity/commons protection (copyleft),
- legal predictability (widely used licenses with known compatibility behavior).

## Proposed Model / Decision

### A. Popularity Baseline: Top 10 Licenses (2025 OSI ranking)

`Assumption`: "Most popular" is measured by OSI 2025 human pageviews of license pages, not by repository count or package downloads.

| Rank | License | Family | Typical Copyleft Strength | Primary Notes for Orbiplex |
|---|---|---|---|---|
| 1 | MIT | Permissive | None | Minimal obligations; high adoption; no explicit patent grant in license text. |
| 2 | Apache-2.0 | Permissive | None | Explicit patent grant and patent retaliation; strong enterprise interoperability profile. |
| 3 | BSD-3-Clause | Permissive | None | Similar to MIT with non-endorsement clause; no explicit patent grant. |
| 4 | BSD-2-Clause | Permissive | None | Very simple permissive license; no explicit patent grant. |
| 5 | GPL-2.0 | Strong copyleft | Strong | Distribution copyleft; compatibility caveats with newer ecosystems. |
| 6 | GPL-3.0 | Strong copyleft | Strong | Strong copyleft with additional patent and anti-tivoization provisions. |
| 7 | ISC | Permissive | None | Short permissive text, close to MIT/BSD style. |
| 8 | LGPL-3.0 | Weak copyleft | Weak | Copyleft focused on library modifications, not all dependent code. |
| 9 | OFL-1.1 | Font license | Specialized | Intended for fonts and related font software; not a general software license. |
| 10 | LGPL-2.1 | Weak copyleft | Weak | Older LGPL variant; still common in legacy/runtime libraries. |

### B. Analysis of the 10 Licenses for Orbiplex Use Cases

| License | Strengths | Risks / Constraints | Orbiplex Fit |
|---|---|---|---|
| MIT | Very low friction, broad compatibility, easy adoption. | Weaker patent posture than Apache-2.0 in practice. | Good for lightweight tooling and examples. |
| Apache-2.0 | Explicit patent grant and retaliation, clear NOTICE model, broad ecosystem acceptance. | Extra notice/compliance steps vs MIT/BSD. | Strong default for node/orchestrator/GUI. |
| BSD-3-Clause | Permissive with non-endorsement clause. | No explicit patent grant. | Good alternative for simple permissive modules. |
| BSD-2-Clause | Minimal and familiar. | No explicit patent grant; fewer governance signals. | Good for low-risk utility modules. |
| GPL-2.0 | Protects commons via strong copyleft on distribution. | Compatibility complexity, especially with newer license stacks. | Prefer avoiding in new Orbiplex components. |
| GPL-3.0 | Strong reciprocity, modernized protections. | Higher adoption friction for some commercial users. | Candidate for "commons-protection-first" core. |
| ISC | Extremely simple permissive form. | Similar patent caveat as MIT/BSD families. | Suitable for small helpers and bootstrap tools. |
| LGPL-3.0 | Keeps library improvements open while allowing broader linking patterns. | More complex compliance than permissive licenses. | Good for extension SDK/runtime libraries. |
| OFL-1.1 | Purpose-built for fonts; strong ecosystem fit for UI typography assets. | Not suitable as a general code license. | Use only for GUI font assets. |
| LGPL-2.1 | Familiar in older dependency ecosystems. | Legacy semantics, versioning complexity with modern stacks. | Use only when needed for dependency compatibility. |

### C. Component-to-License Recommendations for Orbiplex Swarm

| Component Class | Recommended License(s) | Rationale | Key Caveat |
|---|---|---|---|
| `swarm-node` runtime | Apache-2.0 | Interoperability and patent clarity across organizations. | Keep NOTICE discipline and dependency audits. |
| `orchestrator` runtime | Apache-2.0 (default) or GPL-3.0 (if reciprocity-first strategy chosen) | Apache favors adoption; GPL-3.0 favors anti-enclosure reciprocity. | Must choose one strategy explicitly in governance ADR. |
| `GUI assistant` code | Apache-2.0 | Integrator-friendly for desktop/mobile packaging. | Separate code license from artwork/font licenses. |
| Shared protocol libraries / SDKs | LGPL-3.0 or Apache-2.0 | LGPL-3.0 protects library-level changes; Apache-2.0 maximizes uptake. | Avoid mixing incompatible copyleft assumptions across SDK variants. |
| CLI/tools/examples | MIT or Apache-2.0 | Fast reuse and low legal overhead for adoption. | Prefer Apache-2.0 if patent posture matters. |
| Protocol specifications (text) | CC BY 4.0 or CC BY-SA 4.0 | Standard open-doc model for specs and public technical text. | Keep executable code samples separately software-licensed. |
| Manuals/runbooks/architecture docs | CC BY 4.0 (adoption-first) or CC BY-SA 4.0 (reciprocity-first) | Reusable documentation with clear attribution/share-alike policy. | Avoid CC licenses for software code itself. |
| Machine-readable schemas and reference test vectors | Apache-2.0 (or MIT) | Best compatibility with tooling and code generation workflows. | Do not place these under CC unless there is a deliberate reason. |
| Fonts and typographic assets | OFL-1.1 | License fit for font redistribution and modification. | OFL applies to fonts, not to runtime code. |

### D. Compatibility and Governance Rules (Minimal)

1. New Orbiplex code SHOULD NOT use `GPL-2.0-only` in new modules.
2. If `GPL-3.0` is selected for any core component, compatibility implications must be documented before integration.
3. Protocol text and software artifacts MUST remain license-separated (docs vs executable artifacts).
4. Every repo/module MUST include SPDX identifiers and a machine-readable license inventory.
5. Third-party dependency intake MUST include explicit compatibility checks against chosen project baseline.

## Trade-offs

1. Permissive adoption vs reciprocity:
   - permissive licenses increase federation uptake,
   - stronger copyleft better protects the commons from enclosure.
2. Patent certainty vs simplicity:
   - Apache-2.0 improves patent clarity,
   - MIT/BSD/ISC reduce textual complexity.
3. Single-license simplicity vs component-specific fitness:
   - one license is easy to explain,
   - layered licensing is more correct for mixed assets (code/docs/fonts).
4. Documentation openness vs code-license confusion:
   - CC licenses work well for manuals/spec prose,
   - but can create friction if mixed with software code artifacts.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Mixing CC-licensed text with executable code in one artifact | Downstream compliance confusion | Keep separate paths/packages for docs and code; explicit headers per file type. |
| Introducing GPL-2.0-only dependency into Apache-centric core | Integration deadlock | Add CI license-policy gate and compatibility review before merge. |
| Using OFL for non-font software components | Invalid legal assumptions | Restrict OFL usage to font directories/assets only. |
| Missing SPDX and NOTICE metadata | Unclear redistribution obligations | Enforce SPDX + NOTICE checks in CI and release pipeline. |
| Patent ambiguity in permissive-only stack | Enterprise adoption friction | Prefer Apache-2.0 for core runtime modules. |
| Inconsistent license policy across repositories | Fragmented ecosystem governance | Create one licensing ADR and apply as org-wide baseline. |

## Open Questions

1. Should Orbiplex prioritize maximum adoption (`Apache-2.0`) or stronger reciprocity (`GPL-3.0`) for orchestrator core?
2. Should SDKs be strictly permissive, or weak-copyleft (`LGPL-3.0`) to protect shared library improvements?
3. For documentation, is `CC BY 4.0` sufficient, or is `CC BY-SA 4.0` needed to preserve reciprocity?
4. Should protocol schemas and conformance vectors be dual-licensed (e.g., Apache-2.0 + MIT) for toolchain flexibility?
5. Do we require contributor legal statements (DCO/CLA) for patent-risk management?

## Next Actions

1. Create an ADR defining Orbiplex licensing baseline by component type.
2. Decide one of two orchestrator strategies: `Apache-2.0` (adoption-first) or `GPL-3.0` (reciprocity-first).
3. Define a strict file-level policy: code vs docs vs fonts, each with allowed license set.
4. Add SPDX headers and license-scanning CI checks across all repositories.
5. Publish a contributor licensing guide (including dependency intake rules).
6. Add `NOTICE` and third-party attribution generation to release automation.

## Fact / Inference / Speculation Notes

- `Fact`: The top-10 ranking in this document follows OSI's 2025 pageview list.
- `Fact`: Apache-2.0 has explicit GPLv3 compatibility directionality documented by ASF and GNU references.
- `Fact`: MPL is file-level copyleft (Mozilla FAQ), and CC recommends software-specific licenses for software while allowing CC for documentation.
- `Inference`: The recommended Orbiplex split (Apache for runtime, CC for docs, OFL for fonts) minimizes legal ambiguity in mixed artifact repositories.
- `Speculation`: If Orbiplex gains high enterprise adoption, patent-explicit licensing is likely to reduce procurement friction.

## Sources

1. Open Source Initiative, "Top Open Source licenses in 2025" (published 2025-12-17): https://opensource.org/blog/top-open-source-licenses-in-2025
2. Open Source Initiative, "Licenses" index and categories: https://opensource.org/licenses
3. Apache Software Foundation, Apache v2 and GPL compatibility note: https://www.apache.org/licenses/GPL-compatibility
4. GNU, "Various Licenses and Comments about Them": https://www.gnu.org/licenses/license-list
5. Mozilla, "MPL 2.0 FAQ" (updated 2024-01-30): https://www.mozilla.org/en-US/MPL/2.0/FAQ/
6. Creative Commons FAQ (software licensing guidance): https://creativecommons.org/faq/
7. Creative Commons software page: https://creativecommons.org/about/software/
8. SIL Open Font License resources: https://software.sil.org/oflt/
