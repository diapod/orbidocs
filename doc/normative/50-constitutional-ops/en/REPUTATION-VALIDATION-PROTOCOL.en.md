# DIA Reputation Mechanism Validation Protocol

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-REP-VALID-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. VII.4-5, Art. XIV of the Constitution; `doc/normative/30-core-values/en/CORE-VALUES.en.md` section "Reputation as Leverage, Not Power" |
| `mechanism status` | `[mechanism - hypothesis]` in accordance with `NORMATIVE-HIERARCHY.en.md` |

---

## 1. Purpose of the Document

The reputation mechanisms described in `doc/normative/30-core-values/en/CORE-VALUES.en.md` -
weighted voting, flowing recognition points, sublinear growth curves, cartel
detection, COI-by-default - are **architectural hypotheses**. None of them has
been empirically verified in an environment close to DIA.

This protocol defines:

- an experimental clause for reputation mechanisms,
- health metrics that must be measured,
- alarm thresholds and circuit breakers,
- the minimum validation path.

The goal is not to block deployment, but to **design a path from hypothesis to
norm while preserving safety**.

---

## 2. Experimental Clause

Proposed text to be placed in Constitution Art. VII or in the preamble of the
reputation section of `doc/normative/30-core-values/en/CORE-VALUES.en.md`:

> The reputation mechanisms described in this document, in particular: weighted
> voting in resolutions, flowing recognition points, sublinear gain curves,
> cartel detection, and asymmetry of reputational risk, have the status of
> **architectural hypotheses**. Before being granted normative force, they require
> empirical validation in at least two independent federations for a period of no
> less than 6 months, with measurement of the health metrics defined in this
> protocol. Until successful validation, a federation may deploy such mechanisms
> in experimental mode with a mandatory circuit breaker.

---

## 3. Reputation Health Metrics

### 3.1. Core Metrics (Mandatory)

Every federation deploying reputation mechanisms MUST measure and report the
following metrics in cycles no longer than 30 days.

#### M1: Reputation Concentration Coefficient (Gini)

| Parameter | Value |
| :--- | :--- |
| **What it measures** | Whether the reputation distribution creates an oligarchy |
| **Definition** | Gini coefficient of the distribution of aggregated reputation of all active nodes in the federation |
| **Alarm threshold** | Gini > 0.65 |
| **Circuit breaker threshold** | Gini > 0.80 |
| **Measurement frequency** | Every 7 days (rolling 30-day window) |

#### M2: Time to Influence Threshold

| Parameter | Value |
| :--- | :--- |
| **What it measures** | Whether the barrier to entry grows over time (ossification) |
| **Definition** | Median time (in days) from a new node's first contribution to reaching the threshold at which the node gains weighted vote (reputation A1) |
| **Alarm threshold** | Increase > 50% relative to the median from the first quarter of validation |
| **Circuit breaker threshold** | Increase > 100% (doubling) |
| **Measurement frequency** | Every 30 days |

#### M3: Cartel Detection Ratio

| Parameter | Value |
| :--- | :--- |
| **What it measures** | Effectiveness of the anti-cartel system |
| **Definition** | Ratio of detected cartel patterns (mutual boosting, flowing within closed groups) to the total number of reputation transactions |
| **Alarm threshold** | > 5% of transactions flagged as cartel-like |
| **Circuit breaker threshold** | > 15% of transactions flagged OR growth > 3x in one measurement cycle |
| **Measurement frequency** | Every 7 days |

#### M4: Reputation-Quality Correlation

| Parameter | Value |
| :--- | :--- |
| **What it measures** | Whether reputation leverage is justified by quality |
| **Definition** | Spearman correlation between a node's reputation rank and the quality of its decisions as measured by oracles (prediction accuracy, contract keeping, quality of updates) |
| **Alarm threshold** | ρ < 0.3 (weak correlation: reputation does not reflect quality) |
| **Circuit breaker threshold** | ρ < 0.1 or ρ < 0 (reputation is an anti-signal of quality) |
| **Measurement frequency** | Every 30 days (requires oracle data) |

#### M5: Rotation Ratio in the Top Reputation Layer

| Parameter | Value |
| :--- | :--- |
| **What it measures** | Whether the top layer is frozen (oligarchy) or dynamic |
| **Definition** | Percentage of nodes in the top reputation decile that entered or left that decile within the last 90 days |
| **Alarm threshold** | Rotation < 10% (freeze) |
| **Circuit breaker threshold** | Rotation < 5% for two consecutive cycles |
| **Measurement frequency** | Every 30 days |

### 3.2. Additional Metrics (Recommended)

- **M6: Percentage of decisions with a COI declaration** - measures whether
  COI-by-default is actually applied. Alarm threshold: < 20% of weighted
  decisions with any COI declaration (suggesting the mechanism is dead).

- **M7: Entropy of the distribution of flowing-reputation sources** - measures
  whether recognition points come from many sources or from a few dominant ones.
  Low entropy means clique risk.

- **M8: Time to recover after reputation loss** - measures whether the system
  allows repair and reintegration (Art. XVI.4), or whether penalties are de
  facto permanent.

---

## 4. Circuit Breaker

### 4.1. Definition

A circuit breaker is an **automatic safety mechanism** that disables reputation
leverage and restores equal vote when health metrics exceed defined thresholds.

### 4.2. Operating Principle

```text
Normal state: reputation leverage active
       ->
Metric exceeds alarm threshold
       ->
[ALARM] -> report to federation operators + log entry
       -> (if no correction within 14 days OR circuit breaker threshold)
       ->
[CIRCUIT BREAK] -> automatic disabling of reputation leverage
       ->
Federation returns to EQUAL VOTE for all nodes
       ->
Cause analysis, parameter correction, renewed validation
       ->
Reactivation of leverage (requires explicit governance decision with multisig)
```

### 4.3. Circuit Breaker Conditions

The circuit breaker activates automatically when **any** of the following
situations occurs:

1. Any core metric (M1-M5) exceeds the circuit breaker threshold.
2. Two or more core metrics simultaneously exceed the alarm threshold.
3. Metric M4 (reputation-quality correlation) drops below 0 (reputation is an
   anti-signal).

### 4.4. Effects of the Circuit Breaker

- Weighted vote in resolutions -> equal vote (1 node = 1 vote).
- Flowing recognition points -> disabled (rewards without system-level top-up).
- Reputation is still measured and displayed, but **has no operational power**.
- The circuit-break state is logged and publicly visible.

### 4.5. Reactivation

Reactivation of reputation leverage after a circuit break requires:

1. Identification of the cause of threshold crossing.
2. Correction of mechanism parameters.
3. Renewed validation for at least 30 days with metrics below alarm thresholds.
4. Explicit governance decision with multisig (Art. VII.9).

---

## 5. Validation Flow

### 5.1. Phase 0: Simulation (Before Deployment)

- Simulation of reputation mechanisms on synthetic and/or historical data.
- Testing of scenarios: Sybil, cartels, ossification, mass inflow of new nodes.
- Initial calibration of thresholds and parameters.
- Duration: dependent on data availability, minimum 30 days.

### 5.2. Phase 1: Shadow Mode (Deployment Without Operational Force)

- Reputation mechanisms operate in parallel to the equal-vote system.
- Reputation is measured, but **does not affect decisions**.
- Health metrics are gathered and reported.
- Duration: minimum 3 months in at least one federation.
- Transition criterion: all core metrics below alarm thresholds for the entire
  period.

### 5.3. Phase 2: Pilot with Circuit Breaker (Limited Deployment)

- Reputation leverage is activated in at least two independent federations.
- The circuit breaker is active.
- Health metrics are monitored in 7-day cycles.
- Duration: minimum 6 months.
- Transition criterion: no circuit-break activation, all metrics below alarm
  thresholds for >=80% of the period.

### 5.4. Phase 3: Validation and Formalization

After successful completion of Phase 2:

1. Publication of a validation report (data, metrics, anomalies, conclusions).
2. Adversarial review of the report (independent red team).
3. Proposal of formalization: change of mechanism status from
   `[mechanism - hypothesis]` to `[mechanism - validated]` in
   `doc/normative/30-core-values/en/CORE-VALUES.en.md`.
4. Federation decision on formal adoption (Art. XVI procedure for medium-stakes
   changes).

---

## 6. Configurable Parameters at Federation Level

The parameters below are **defaults** and may be changed by a federation within
federation policies (Level 4 of the normative hierarchy). A federation **may not**
disable the circuit breaker or raise thresholds above the default values.

| Parameter | Default value | Allowed range |
| :--- | :--- | :--- |
| `gini_alarm_threshold` | 0.65 | <= 0.65 |
| `gini_breaker_threshold` | 0.80 | <= 0.80 |
| `time_to_influence_alarm_pct` | 50% growth | <= 50% |
| `cartel_alarm_pct` | 5% | <= 5% |
| `correlation_alarm_rho` | 0.3 | >= 0.3 |
| `top_decile_rotation_alarm` | 10% | >= 10% |
| `shadow_mode_min_months` | 3 | >= 3 |
| `pilot_min_months` | 6 | >= 6 |
| `pilot_min_federations` | 2 | >= 2 |
| `measurement_cycle_days` | 7 | <= 7 |

Interpretation: a federation may be **more cautious** (lower thresholds, longer
validation), but not **more permissive** than the default values.

---

## 7. Relation to Other Documents

- **Constitution Art. VII.4-5**: This protocol operationalizes the rule that
  reputation is a safeguard, not a status.
- **`doc/normative/30-core-values/en/CORE-VALUES.en.md` - "Reputation as Leverage, Not Power"**:
  source of the mechanisms subjected to validation. After successful validation,
  the section changes status from `[mechanism - hypothesis]` to
  `[mechanism - validated]`.
- **`NORMATIVE-HIERARCHY.en.md`**: explains why mechanisms from core values do not
  automatically gain normative force.
- **`ENTRENCHMENT-CLAUSE.en.md`**: if a validated reputation mechanism begins to
  violate the non-negotiable core (e.g. dignity, right to exit), it becomes
  subject to a constitutional challenge.
- **`AUTONOMY-LEVELS.en.md`**: reputation voting requires autonomy level A0
  (proposal and human approval).
