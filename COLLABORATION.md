# Orbiplex Collaboration Card

Version: 0.2 (2026-02-21)
Parties: Sebastian + Paweł

Goal: build distributed AI + community + a prompt marketplace (without lock-in and without attention/upside asymmetry).

## 0) Top-level principles

1. **Non-lock-in / Exitability**: no technical or social "hostages"; forking is allowed.
2. **Commons-first**: the core is a shared commons; monetization should reinforce it, not drain it.
3. **Parity of paths**: core work and marketplace work are first-class (both have rhythm, ownership, and shipping).
4. **Intent transparency**: monetization and side-ventures are communicated *before* launch, not after.

## 1) Definitions

- **Core/Commons**: repos/protocols, orchestration, evals, tooling, documentation, community channels.
- **Prompt Marketplace**: catalog + listings + discovery + versioning/IDs + validation + settlement.
- **Wrapper / Side-venture**: a product/service that profits thanks to the
  core/marketplace (hosting, enterprise gateway, consulting "on the brand", private
  registries, etc.).

## 2) Licensing and IP

- Core/Commons: **Apache-2.0** (default repo license), possibly dual-licensing with GPL/LGPL.
- Community contributions: clear `AUTHORS.md` + attribution (metadata).
- Prompts: authors keep authorship; the marketplace stores content/metadata under agreed terms (see 6).

## 3) Roles and responsibilities (simple)

### Paweł (siefca)

- Owner: core architecture, contracts, quality, supply-chain security, automation.
- Responsibility: hard system properties and long-term standards/maintenance.

### Sebastian

- Owner: community initiation, partnerships, distribution/adoption, market feedback.
- Responsibility: ecosystem momentum and community health, code reviews.

### Shared

- roadmap,
- architecture strategies (e.g., protocols and rules),
- governance,
- marketplace rules (prompt publishing, pricing/fees, prompt licensing, publicity),
- hotfixing,
- obtaining man/AI power.

## 4) Work cadence (anti-asymmetry)

- **Weekly**: at least 1 "ship" in Core **and** at least 1 "ship" in Marketplace
  (small is fine, but real: PR, release, deploy, fix, test).
- Sebastian keeps a fixed slot for marketplace work: 2-4 hours/week (non-architecture).
- Paweł keeps a fixed slot for marketplace work: 2-4 hours/week (non-architecture).
- Weekly 30-min review: what shipped, where debt grows, what blocks us.

## 5) Governance and decisions

Strategic decisions require approval from both parties:

1) license changes / contribution terms changes,
2) infrastructure partnerships and vendor dependence,
3) telemetry and user data,
4) marketplace monetization rules,
5) using the brand for selling.

Dispute path: 48h written clarification → 60-min call → if still stuck: 7-day cooldown.

## 6) Prompt marketplace: ethical + technical guardrails

1. **Portability**: authors can export their prompts + metadata (in a standard format).
2. **Transparency**: clear fees/commission and settlement; no hidden charges.
3. **Moderation**: publishing rules are public (safety, copyright, etc.).
4. **Prompt licensing**: each prompt has an explicit license choice (e.g., CC-BY/CC0/commercial-allowed, etc.).
5. **Attribution**: visible author + version history.
6. **No exclusivity by default**: authors are not blocked from publishing elsewhere (unless they explicitly opt in).

## 7) Side-ventures / wrappers: the hard guardrail (red line)

### 7.1 No competing wrappers

For the first 17 months after collaboration starts:

- neither party launches a wrapper/side-venture based on the core/marketplace/brand
  without the other party's consent.

### 7.2 ROFR — Right of First Refusal (fixed 50/50)

If one party wants to launch a wrapper:

- they offer it first as a joint initiative,
- the other party has the right to join **50/50** on pre-defined terms,
- decision window: 7 days.

If the other party declines:

- the initiator may proceed solo, but:
  1) without using the "official" brand,
  2) with attribution and no misrepresentation,
  3) without exclusivity over the commons,
  4) without capturing community channels as sales channels.

## 8) Brand and communications

- "Official" announcements require joint approval.
- The project brand is not used for selling without both parties' consent.
- Sponsors/partners: disclosed, including any influence if applicable.

## 9) Exit and hygiene

- Either party may exit with a 31-day handover period (access, docs,
  obligations).
- Forking is allowed (Apache-2.0), with no impersonation of official accounts/brand.

## 10) Success after 120 days (a concrete test)

- A vertical slice works: core + prompt marketplace  
  (publish → discover → version/ID → settlement/commission, even if MVP).
- Shipping rhythm works on both tracks.
- Monetization + ROFR rules are respected in practice (no "silent wrappers").
