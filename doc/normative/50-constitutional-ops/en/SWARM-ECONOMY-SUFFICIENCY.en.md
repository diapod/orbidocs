# DIA Swarm-Economy Sufficiency and Common-Circulation Specification

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-SUFF-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | `0.1.0-draft` |
| `basis` | Art. VIII.4-8, XII.5-13, XIV of the DIA Constitution; `doc/normative/30-core-values/en/CORE-VALUES.en.md` section "Sufficiency Over Accumulation" |
| `mechanism status` | data model and compliance tests are normative; reward functions may be parameterized by federations within this document's limits |

---

## 1. Purpose of the Document

The Constitution prohibits converting economic advantage into lasting
constitutional dominance and requires surpluses above the sufficiency threshold to
return to common circulation. What is still missing is the minimal specification:
how a federation defines the sufficiency threshold, which concentration brakes are
mandatory, and how redistribution is audited.

This document defines:

- the minimal concepts and data model of economic policy,
- the compliance test for the sufficiency threshold,
- permissible classes of reward curves,
- the mandatory circulation of surpluses,
- the ban on converting economic reward into procedural power,
- minimum federation audit metrics,
- the relation to constitutional exceptions.

---

## 2. General Rule

1. Swarm economics serves the maintenance of the capacity to act of people, nodes,
   and the community, not endless accumulation.
2. Voluntary contractual exchange among participants is an admissible mode of
   reciprocity alongside gift, but its economic traces may not by themselves act as
   a shortcut to reputational, procedural, or constitutional force.
3. A federation MUST design rewards so that, once sufficiency is reached, further
   gain is diminishing or automatically redirected into common circulation.
4. No economic mechanism may make compensation depend primarily on the inflow of
   new participants instead of auditable use, impact, maintenance of value, or real
   protective/helpful action.
5. Economic reward is not a path for bypassing rules of procedural reputation,
   routing, quorum, exceptions, or eligibility for high-stakes roles; this also
   applies to balance, exchange history, and the mere fact of entering into or
   performing a contract.
6. Verified personhood in the network may by itself be a sufficient basis for a
   non-withdrawable minimum of compute resources for communication, orientation, and
   emergency/care modes, regardless of temporary reputation or economic contribution.

---

## 3. Core Terms

| Term | Meaning |
| :--- | :--- |
| `sufficiency_threshold` | the level of resources or reward flow sufficient for safe and stable upkeep of the node and its operator |
| `sufficiency_band` | a tolerance band around the sufficiency threshold within which the system may smooth reward behavior instead of applying a hard step |
| `surplus` | the part of reward exceeding `sufficiency_threshold` after taking `sufficiency_band` into account |
| `common_circulation` | common circulation of surpluses according to explicit federation rules |
| `infrastructural_function` | a function of high communal value that need not generate high reputational or market return |
| `conversion_barrier` | a rule forbidding translation of economic reward into procedural or constitutional advantage |
| `universal_basic_compute` | a non-withdrawable minimum of compute guaranteed to a verified person for communication, orientation, and protective modes |

The sufficiency threshold may be defined as:

- an amount per period,
- a cost budget per node,
- a multi-factor resource band,
- or another functionally equivalent model.

A federation MUST NOT define the threshold in a purely narrative way. There must
be an operational model that can be audited and reviewed.

---

## 4. Minimal Data Model of Economic Policy

Any federation that activates reward or token mechanisms MUST publish at least:

```yaml
swarm_economy_policy:
  policy_id: "DIA-SUFF-001"
  federation_id: "[federation]"
  version: "0.1.0"
  reward_unit: "[token / credit / point / other unit]"
  measurement_period: "P30D"
  sufficiency_threshold:
    model_type: "fixed" # fixed | indexed | cost_profile | mixed
    value: "[value or formula]"
    review_period: "P90D"
    basis_ref: "[public rationale or index]"
  sufficiency_band:
    lower: 0.9
    upper: 1.1
  reward_curve:
    type: "piecewise_sublinear"
    parameters: {}
  universal_basic_compute:
    enabled: true
    eligibility_basis: "proof_of_personhood"
    non_withdrawable: true
    guaranteed_modes:
      - "emergency"
      - "care"
    funding_sources:
      - "business_nodes"
      - "high_margin_instances"
      - "surplus_recirculation"
      - "voluntary_operator_surplus"
  surplus_policy:
    destination_classes:
      - "basic_survival_floor"
      - "bootstrap"
      - "weaker_links"
      - "temporary_harm"
      - "infrastructure"
    allocation_rule: "[public rule or formula]"
    settlement_period: "P30D"
  conversion_barriers:
    governance_weight_from_rewards: false
    privileged_routing_from_rewards: false
    exception_access_from_rewards: false
    oracle_power_from_rewards: false
  audit_metrics:
    - "top_1_share"
    - "top_5_share"
    - "surplus_recirculation_rate"
    - "coverage_ratio"
    - "infrastructure_share"
```

Absence of a public `swarm_economy_policy` means the federation does not meet the
minimum standard for exchangeable or quasi-exchangeable mechanisms.

---

## 5. Sufficiency Threshold

### 5.1. Compliance Test

The sufficiency threshold MUST pass all three tests at once:

1. **Upkeep test**: the threshold is enough for safe and stable upkeep of the node
   and its operator in ordinary operation.
2. **Non-domination test**: the threshold may not be set so high that it
   effectively disables concentration brakes for a small privileged group.
3. **Transparency test**: the method of setting the threshold can be described,
   recalculated, and challenged procedurally.

### 5.2. Minimum Rules

1. The sufficiency threshold MUST be reviewed periodically.
2. A change in the threshold MUST leave a decision trace, rationale, and effective
   date.
3. A federation may use different cost profiles for different node classes, but it
   may not use them to covertly privilege its own operators or public-trust roles.

---

## 6. Reward Curves and Concentration Brakes

### 6.1. Permissible Classes of Mechanisms

After crossing `sufficiency_threshold`, a federation MUST apply at least one of the
following classes of limits:

1. diminishing gains (`sublinear`),
2. a tapering plateau,
3. a hard cap with surplus redirection,
4. a hybrid of the above.

### 6.2. Impermissible Classes of Mechanisms

Impermissible are mechanisms that:

1. retain linear or superlinear growth indefinitely,
2. reward mainly for position in time,
3. increase reward power faster than auditable contribution grows,
4. hide concentration through side channels or opaque benefit classes.

### 6.3. Anti-Pyramid Test

An economic mechanism does NOT pass the constitutional test if any of the following
holds:

1. the dominant part of payouts for earlier participants comes from the inflow of
   new participants rather than auditable use or value,
2. seniority by itself creates a lasting bonus without decay,
3. loss of new-participant inflow causes structural collapse of baseline payouts.

---

## 7. Common Circulation of Surpluses

### 7.1. Destination Classes

At least the following classes MUST be served by `surplus_policy`:

1. `basic_survival_floor` - the minimum allocation for verified persons without
   sufficient current reputational or economic contribution,
2. `bootstrap` - new nodes and entry into the ecosystem,
3. `weaker_links` - nodes with lower operational capacity,
4. `temporary_harm` - nodes or operators temporarily harmed,
5. `infrastructure` - functions of high communal value.

A federation may add other classes, but it may not remove all protective and
infrastructural classes at once.

### 7.2. Minimum Redistribution Rules

1. Surplus MUST be settled periodically, not ad hoc by sympathy.
2. The allocation rule MUST be public or expressed as a public algorithm.
3. Funds routed into common circulation may not return in the same round to the
   source beneficiary through a hidden channel.
4. Redistribution MUST leave an auditable trace per period.

### 7.3. Minimal Settlement Record

```yaml
surplus_settlement:
  settlement_id: "[unique identifier]"
  federation_id: "[federation]"
  period_start: "[timestamp]"
  period_end: "[timestamp]"
  source_node_id: "[source node]"
  gross_reward: 0
  retained_reward: 0
  surplus_amount: 0
  destination_class: "bootstrap"
  destination_ref: "[fund / pool / recipient]"
  policy_ref: "DIA-SUFF-001"
  created_at: "[timestamp]"
```

---

## 8. Barrier Against Conversion into Constitutional Power

1. Token, credit, or other economic-reward balances may not be a direct input into
   calculation of voting weight, panel eligibility, oracle force, or access to
   exceptions.
2. A federation may not sell or grant shortcuts into public-trust roles in
   exchange for economic reward.
3. If the system uses both economic rewards and reputation, their accrual paths
   MUST be separated and auditable.
4. Any attempt to circumvent the conversion barrier through an indirect benefit is
   treated as a constitutional violation, not as ordinary economic optimization.

---

## 9. Federation Health Metrics

A federation operating reward economics MUST measure at least:

- `top_1_share` - the largest beneficiary's share of all payouts,
- `top_5_share` - the top five beneficiaries' share,
- `surplus_recirculation_rate` - the share of surplus that actually returned to
  common circulation,
- `coverage_ratio` - the share of active nodes reaching the minimum upkeep level,
- `infrastructure_share` - the share of redistribution allocated to
  infrastructural functions,
- `new_node_support_rate` - the share of new nodes covered by bootstrap support.

Persistent growth of concentration together with low `surplus_recirculation_rate`
is a signal of institutional pathology and should trigger review of economic policy.

---

## 10. Exceptions and Relation to Other Documents

1. Bypassing concentration brakes may occur only through an exception compliant
   with `EXCEPTION-POLICY.en.md`.
2. An exception may not suspend the barrier against converting economic reward into
   procedural power.
3. Every exception concerning the sufficiency threshold or redistribution MUST
   specify: `reason`, `expiry`, `owner`, `risk-level`, and side-effect metrics.

Document relations:

- **Constitution Art. VIII.4**: prohibition of pyramid-type economics and of
  converting economic advantage into power.
- **Constitution Art. XII.6-13**: contractual exchange as an admissible mode of
  reciprocity, the purpose of economics, concentration brakes, common circulation
  of surpluses, and the conversion barrier.
- **`EXCEPTION-POLICY.en.md`**: exception procedure for temporary departures.
- **`PROCEDURAL-REPUTATION-SPEC.en.md`**: separation of procedural reputation from
  economic reward.
