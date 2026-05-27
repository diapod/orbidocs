# Marketplace Anti-Fraud Policy

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-MARKETPLACE-ANTI-FRAUD-001` |
| `type` | Constitutional operational act / marketplace risk policy |
| `version` | `0.1.0-draft` |
| `date` | `2026-05-27` |
| `basis` | Constitution Art. XV, XVI; Role to IAL Matrix; Proposal 021; Proposal 051 |

## Purpose

Marketplace surfaces create financial and operational risk.
Orbiplex should keep ordinary cooperation easy while making scams, self-dealing, and high-value abuse slow, visible, and costly.

## Baseline Rules

The default marketplace policy is:

- no unsolicited financial offers through DM,
- all financial offers should use explicit service or marketplace surfaces,
- new participants begin with very low value caps,
- escrow or procurement contracts are required where risk is non-trivial,
- external payment links are restricted for new or low-evidence participants,
- self-dealing does not create transferable reputation,
- high-value surfaces require stronger IAL, procedural reputation, cooling-off, and dispute paths.

## Risk Tiers

```yaml
marketplace:
  new_participant:
    max_contract_value: low
    escrow_required: true
    external_payment_links: denied
    unsolicited_offers: denied
  elevated:
    min_IAL: IAL1_or_higher
    min_contract_reputation: threshold
    independent_receipts_required: true
  high_value:
    min_IAL: strong
    cooldown: required
    dispute_path: required
    legal_notice_policy: required
```

## Evidence

Marketplace reputation should derive from first-hand settled receipts linked to contracts, orders, settlements, or dispute outcomes.
Gossip-only score updates and closed-loop boosting should not unlock value caps.

## Enforcement

Patterns such as hidden acquisition, unsolicited financial solicitation, suspicious fan-out, repeated refund abuse, fake receipt loops, and target asymmetry may trigger:

- marketplace hold,
- value cap reduction,
- escrow-only mode,
- procedural reputation signals,
- sponsor review,
- routing cut-off from marketplace surfaces,
- or formal dispute escalation.

