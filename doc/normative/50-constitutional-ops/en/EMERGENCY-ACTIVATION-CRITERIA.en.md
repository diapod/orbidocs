# DIA Emergency Activation Criteria

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-EMRG-ACT-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. II.2, II.8, IX.3-5, V.10, V.13 of the DIA Constitution; `AUTONOMY-LEVELS.en.md` (A3); `EXCEPTION-POLICY.en.md` (section 4.2) |
| `mechanism status` | `[mechanism - hypothesis]` for credibility scoring thresholds; trigger taxonomy and pipeline are normative |

---

## 1. Purpose of the Document

The Constitution permits emergency action when there is direct danger to life or
sudden serious harm (Art. II.8). `AUTONOMY-LEVELS.en.md` defines A3 (Emergency
Mode) as the highest autonomy level for agents. `EXCEPTION-POLICY.en.md` defines
the emergency exception type. However, no specification exists for **what
triggers emergency activation**, **how signals are evaluated**, or **what
safeguards prevent abuse**.

This document defines:

- trigger classes and their scope,
- signal credibility levels and evaluation rules,
- the sensorium-to-operator pipeline,
- activation paths (manual and automatic),
- time limits and extension rules,
- mandatory post-crisis review,
- false alarm classification and accountability,
- cascading crisis rules,
- operator timeout and escalation.

---

## 2. Design Principles

1. **A3 accelerates, it does not create new powers**. Emergency mode allows
   faster action within existing permissions; it does not grant permissions that
   the agent contract does not contain (Art. V.10, V.13).

2. **Fail-closed by default**. Expiry of any time limit returns the system to
   A0. Extending emergency mode requires fresh evidence and an explicit decision.

3. **Full trace, no exceptions**. Every action taken under A3 generates an
   unredacted trace (AUTONOMY-LEVELS 5.1). The trace is the price of speed.

4. **Mandatory review**. Every A3 activation undergoes post-crisis review
   (AUTONOMY-LEVELS 5.3). Review results feed back into reputation signals.

5. **TC5 is a meta-class, not a direct activator**. An epistemic crisis (TC5)
   cannot independently activate A3. It activates heightened monitoring and
   operator alerts. A3 requires manifestation through TC1-TC4.

6. **Proportionality**. The response MUST be proportional to the threat.
   Emergency powers are not a shortcut for convenience or political advantage.

---

## 3. Trigger Classes

### 3.1. Taxonomy

| Class | Name | Scope | Examples | Constitutional basis |
| :--- | :--- | :--- | :--- | :--- |
| `TC1` | Immediate threat to life | Direct, personal danger | Violence, suicide risk, acute medical emergency, hostage situation | Art. II.2, II.8 |
| `TC2` | Infrastructure crisis | Systemic failure of critical infrastructure | Blackout, network collapse, critical system failure, key compromise (including council key compromise) | Art. IX.3-5, IV.7 |
| `TC3` | Health crisis | Threat to health at scale | Epidemic, poisoning, environmental hazard, contamination | Art. II.2, IX.7 |
| `TC4` | Persecution or targeted violence | Attack on persons through or against the system | Targeted attack, doxxing, political persecution, whistleblower retaliation, stalking | Art. X.1-3, II.11 |
| `TC5` | Epistemic crisis (meta-class) | Degradation of the system's ability to distinguish signal from noise | Disinformation campaign, oracle poisoning, source contamination, coordinated narrative manipulation | Art. XI.1, XI.7-8 |

### 3.2. TC5 — Special Rules

TC5 is a **meta-crisis class**. It describes a condition where the system's
epistemic infrastructure is compromised: oracles produce unreliable outputs,
signals are poisoned, or coordinated manipulation distorts the information
environment.

**TC5 alone CANNOT activate A3.** The rationale:

- A3 is designed for situations of **direct, sudden harm** (Art. II.8). An
  epistemic crisis is typically gradual and diffuse.
- Granting A3 on the basis of "the system cannot tell truth from noise" creates
  a paradox: the mechanism that evaluates whether A3 is warranted is itself
  compromised.
- History shows that "epistemic emergency" framing is a vector for
  authoritarian overreach.

**TC5 activates:**

1. **Heightened monitoring** — all sensorium signals tagged with increased
   uncertainty; automated credibility scoring enters `degraded_trust` mode.
2. **Operator alert** — all federation operators receive an explicit alert with
   the TC5 classification and supporting evidence.
3. **Signal pre-qualification** — signals that would normally auto-activate at
   C3+ (section 4) require manual operator confirmation while TC5 is active.
4. **Oracle quarantine** — oracles flagged as potentially compromised are
   quarantined: their outputs are still collected but excluded from automated
   decision paths.

**TC5 escalation to A3** occurs only when an epistemic crisis **manifests
through** TC1-TC4. Example: oracle poisoning (TC5) leads to a routing failure
that isolates a node under active threat (TC4) — the TC4 manifestation
activates A3, not the TC5 classification itself.

### 3.3. Council Key Compromise (TC2 Subclass)

The compromise of a `council:did:key` (as defined in the nym protocol) is a
TC2 infrastructure crisis with specific consequences:

1. **Trapdoor freeze** — the council's nym-to-participant binding trapdoor is
   immediately frozen. No deanonymization requests are processed until the
   compromise is resolved.
2. **Emergency key rotation** — a new `council:did:key` is generated and
   distributed. Existing nym certificates remain valid until their TTL expires
   but cannot be renewed with the compromised key.
3. **Ad-hoc audit panel** — a panel is composed under
   `PANEL-SELECTION-PROTOCOL` to audit the scope of the compromise: which
   bindings were exposed, which trapdoor operations were performed, and whether
   any deanonymization occurred without authorization.
4. **Nym chain continuity** — participants may request accelerated nym renewal
   using the new council key. The leniency window of existing certificates
   ensures continuity during transition.

This subclass connects the identity infrastructure (GENYM design) with the
constitutional crisis framework.

---

## 4. Signal Credibility Levels `[hypothesis]`

Every signal entering the emergency pipeline is evaluated for credibility
before triggering any activation path.

### 4.1. Credibility Scale

| Level | Name | Definition | Minimum evidence |
| :--- | :--- | :--- | :--- |
| `C0` | Noise | Unverifiable or internally inconsistent | — |
| `C1` | Single source | One source, no corroboration | One signal from one sensor/reporter |
| `C2` | Corroborated | Two independent sources, or one source with supporting context | Two signals from different operators/sources, or one signal + contextual match |
| `C3` | High confidence | Three independent sources, or two + material evidence | Three signals, or two + auditable artifact |
| `C4` | Overwhelming | Multiple convergent sources with material evidence | Multi-source auditable material, coherent in time and authorship |

### 4.2. Activation Rules by Credibility

| Credibility | Activation path | Constraints |
| :--- | :--- | :--- |
| `C0` | No activation | Signal is logged but generates no action |
| `C1` | Manual only (operator decision) | Operator receives alert; no automated response |
| `C2` | Manual with system recommendation | System presents classification and recommended response; operator decides |
| `C3` | Automatic permitted for TC1, TC2, TC4 | Auto-activation with immediate operator notification; operator may override within `operator_override_window` (default: 5 min) |
| `C4` | Automatic for TC1-TC4 | Auto-activation with enhanced trace; post-hoc review mandatory within 24h |

**TC5 exception:** Regardless of credibility level, TC5 never triggers
automatic A3 activation. At C3+, TC5 activates automatic alerting and
heightened monitoring, but A3 requires manifestation through TC1-TC4.

### 4.3. Source Independence Requirements

For a signal to count as "independent" for credibility scoring:

1. The sources MUST be operated by **different operators** (distinct
   `node:did:key` with distinct operator identity).
2. The sources MUST derive from **different data feeds** (not mirrors of the
   same upstream).
3. Temporal proximity (signals within `correlation_window`, default: 15 min) is
   treated as corroborating, not independent, unless the sources can demonstrate
   independent causal paths.

---

## 5. Emergency Pipeline

### 5.1. Architecture

```
┌─ Stage 1: Ingestion ──────────────────────────────────────┐
│  Sensorium connectors → raw signals with metadata         │
│  (source, timestamp, type, confidence, evidence_ref)      │
├─ Stage 2: Evaluation ─────────────────────────────────────┤
│  Classification (TC1-TC5)                                 │
│  Corroboration (cross-source, temporal, contextual)       │
│  Credibility scoring (C0-C4)                              │
│  TC5 degraded-trust check                                 │
├─ Stage 3: Decision ───────────────────────────────────────┤
│  IF C0: log only                                          │
│  IF C1: alert operator                                    │
│  IF C2: alert + recommend                                 │
│  IF C3+ AND auto-eligible: activate + notify operator     │
│  IF C3+ AND NOT auto-eligible: alert + require operator   │
│  Create exception record (EXCEPTION-POLICY data model)    │
│  Start TTL countdown                                      │
├─ Stage 4: Active Response ────────────────────────────────┤
│  Agent operates at A3 within contract limits              │
│  Full trace on every action                               │
│  TTL monitored; extension requires fresh evidence         │
├─ Stage 5: Deactivation ──────────────────────────────────┤
│  TTL expires OR operator deactivates OR threat resolved   │
│  System returns to A0 (fail-closed)                       │
│  Post-crisis review clock starts (72h)                    │
└───────────────────────────────────────────────────────────┘
```

### 5.2. Signal Data Model

```yaml
emergency_signal:
  signal_id: "[unique identifier]"
  source_node_id: "[node:did:key of the reporting node]"
  source_type: "sensorium"    # sensorium | operator | peer_report | oracle
  timestamp: "[ISO 8601]"
  trigger_class: "TC1"        # TC1 | TC2 | TC3 | TC4 | TC5
  description: "[human-readable summary]"
  evidence_ref: "[reference to auditable evidence]"
  confidence: "C2"            # C0 | C1 | C2 | C3 | C4
  corroborating_signals: []   # list of signal_ids
  tc5_active: false           # whether TC5 degraded-trust mode is active
  metadata:
    geo_hint: "[optional, coarse location]"
    affected_scope: "[node | federation | inter-federation]"
    urgency: "immediate"      # immediate | hours | days
```

### 5.3. Activation Record

Every emergency activation creates an exception record per
`EXCEPTION-POLICY.en.md` section 3, with the following additional fields:

```yaml
emergency_activation:
  exception_id: "EXC-[federation]-[timestamp]-[nonce]"
  type: "emergency"
  trigger_class: "TC1"
  trigger_signals: ["sig_001", "sig_002"]
  credibility: "C3"
  activation_path: "automatic"    # automatic | manual
  activated_by: "[operator node:did:key or 'system']"
  activated_at: "[ISO 8601]"
  ttl_expires_at: "[ISO 8601]"
  max_extension_until: "[ISO 8601]"
  extensions: []
  agents_elevated: ["[agent_id:A3]"]
  scope: "[description of what is covered]"
  fail_closed_target: "A0"
  deactivated_at: null
  deactivation_reason: null
  review_due_at: null           # set at deactivation: deactivated_at + 72h
  review_status: "pending"      # pending | in_progress | completed
```

---

## 6. Time Limits

### 6.1. Default TTL per Trigger Class

| Class | Initial TTL | Max extension | Extension requirement |
| :--- | :--- | :--- | :--- |
| `TC1` | 4 hours | 24 hours | Operator + fresh evidence |
| `TC2` | 12 hours | 48 hours | Operator + status report |
| `TC3` | 24 hours | 72 hours | Operator + fresh evidence |
| `TC4` | 8 hours | 48 hours | Operator + fresh evidence |
| `TC5` (alert only, not A3) | 24 hours | 72 hours | Operator + independent corroboration |

### 6.2. Extension Rules

1. Each extension MUST create a new entry in the `extensions` array of the
   activation record, containing:
   - `extended_by`: operator identity,
   - `extended_at`: timestamp,
   - `new_expires_at`: new expiry,
   - `justification`: rationale with reference to fresh evidence,
   - `evidence_refs`: references to new evidence.

2. Extensions beyond `max_extension` are **prohibited**. If the threat persists,
   a new activation cycle begins with a new exception record and a fresh
   evidence evaluation. This prevents indefinite emergency mode.

3. The `max_extension` values are **absolute ceilings**, not cumulative. A TC1
   activation with initial TTL of 4h may be extended to at most 24h total, not
   4h + 24h = 28h.

### 6.3. Fail-Closed Return

When TTL expires without extension:

1. All agents elevated to A3 return to **A0** (Propose & Wait).
2. The activation record is marked `deactivated_at` with reason `ttl_expired`.
3. The post-crisis review clock starts (72h).
4. If the threat is still present, the operator MUST initiate a new activation
   cycle with fresh evidence.

---

## 7. Operator Timeout and Escalation

When a signal requires manual operator action (C1-C2, or C3+ for non-auto-
eligible classes):

### 7.1. Timeout Thresholds

| Trigger class | Operator response window | Escalation target |
| :--- | :--- | :--- |
| `TC1` | 15 minutes | Federation emergency operator |
| `TC2` | 30 minutes | Federation emergency operator |
| `TC3` | 30 minutes | Federation emergency operator |
| `TC4` | 15 minutes | Federation emergency operator |
| `TC5` | 60 minutes | Federation governance contact |

### 7.2. Escalation Chain

1. **Primary operator** receives the alert with full signal data.
2. If no response within the timeout:
   - alert escalates to **federation-level emergency operator** (a designated
     backup role).
3. If the federation-level operator also does not respond within one additional
   timeout period:
   - for TC1 and TC4 (immediate human safety): **auto-activation** with
     `activation_path: "escalation_auto"` and enhanced trace. Review is
     mandatory within 24h instead of the usual 72h.
   - for TC2, TC3, TC5: the signal is broadcast to **all federation operators**
     with `urgency: critical`. No auto-activation without operator.

### 7.3. Operator Accountability

- Repeated operator timeouts (> `max_operator_timeouts_per_period`, default: 3
  in 30 days) generate a negative `procedural` signal (`governance_inaction`)
  in `PROCEDURAL-REPUTATION-SPEC`.
- Persistent unavailability triggers review of the operator's public-trust role
  fitness.

---

## 8. Mandatory Post-Crisis Review

### 8.1. Timeline

The review MUST begin no later than **72 hours** after deactivation of
emergency mode. For escalation-auto activations (section 7.2), the review MUST
begin within **24 hours**.

### 8.2. Scope

The review covers:

1. **Adequacy** — Was the trigger class correctly identified? Was the
   credibility assessment accurate?
2. **Proportionality** — Were the actions taken proportional to the threat?
   Were less invasive alternatives available?
3. **Side effects** — What unintended consequences occurred? Were any rights
   violated?
4. **Trace completeness** — Is the action trace complete and unredacted?
5. **Calibration recommendations** — Should activation thresholds,
   credibility scoring, or timeout values be adjusted?

### 8.3. Review Body

- For **manual activations**: review by the operator's federation governance
  body.
- For **automatic activations**: review by an independent reviewer (not the
  operator who received the alert).
- For **escalation-auto activations**: review by an ad-hoc panel composed under
  `PANEL-SELECTION-PROTOCOL`.

### 8.4. Reputation Feedback

Review outcomes generate signals in `PROCEDURAL-REPUTATION-SPEC`:

| Outcome | Signal domain | Signal type | Polarity |
| :--- | :--- | :--- | :--- |
| Adequate and proportional response | `procedural` | `crisis_response_adequate` | positive |
| Excessive response | `procedural` | `crisis_response_disproportionate` | negative |
| Inadequate response (under-reaction) | `incident` | `crisis_response_inadequate` | negative |
| False alarm — premature (honest error) | `incident` | `false_alarm_premature` | neutral (logged, no score impact) |
| False alarm — mistaken (systemic error) | `incident` | `false_alarm_mistaken` | negative (mild) |
| False alarm — manipulated (deliberate) | `procedural` | `false_alarm_manipulated` | negative (severe) |

---

## 9. False Alarm Classification

### 9.1. Categories

| Category | Definition | Accountability |
| :--- | :--- | :--- |
| `premature` | Trigger conditions appeared genuine but resolved before activation took effect | No negative signal. System functioned as designed. |
| `mistaken` | Evaluation error: credibility was overestimated or trigger class was misidentified | Mild negative signal in `incident` domain. Calibration review required. |
| `manipulated` | Deliberate fabrication of signals to trigger emergency activation | Severe negative signal in `procedural` domain. Investigation under `ABUSE-DISCLOSURE-PROTOCOL` if evidence warrants `S2+`. |

### 9.2. Health Metric

The federation MUST track:

- false alarm rate per period (rolling 6 months),
- breakdown by category (`premature` / `mistaken` / `manipulated`),
- breakdown by trigger class.

**Threshold**: if `mistaken` + `manipulated` false alarms exceed **30%** of all
activations in a 6-month window, a mandatory calibration review is triggered.
This review examines sensor quality, credibility scoring parameters, and
operator training.

---

## 10. Cascading Crises

When multiple trigger classes are active simultaneously:

### 10.1. Rules

1. Each trigger class creates a **separate exception record**. Crises are not
   merged into a single activation.

2. The combined TTL equals the **longest individual TTL**, not the sum. A
   simultaneous TC1 (4h) + TC3 (24h) has a combined ceiling of 24h, not 28h.

3. Powers do not stack. A3 is the maximum; two concurrent A3 activations do not
   create "A4". The scope of each activation is the union of the individual
   scopes.

4. Deactivation is **per trigger**. When TC1 resolves but TC3 persists, the TC1
   record is closed and reviewed independently.

5. If a cascading crisis involves TC5, the TC5 `degraded_trust` mode applies to
   the credibility evaluation of all concurrent triggers (section 3.2, point 3:
   auto-activation requires manual confirmation).

### 10.2. Cascade Detection

The system MUST flag concurrent activations as a `cascade_event` in the
activation records. Cascades are subject to enhanced monitoring and priority
review.

---

## 11. Interaction with Art. X (Whistleblowers and Abuse Disclosure)

Emergency activation may interact with the abuse disclosure framework:

1. **Whistleblower protection under crisis** (Art. X.1-3): If a TC4 activation
   involves a whistleblower under active threat, the emergency response includes
   securing the whistleblower's communication channel
   (`ABUSE-DISCLOSURE-PROTOCOL` section 4).

2. **Abuse as trigger** (Art. X.4-X.8): Discovery of ongoing severe abuse
   (meeting `S3+` and `E3+` thresholds from `ABUSE-DISCLOSURE-PROTOCOL`) may
   constitute a TC4 trigger if there is active persecution or targeted violence
   against the reporter or affected persons.

3. **Emergency does not bypass disclosure procedure**. A3 activation does not
   grant authority to perform disclosure (D1-D4) without following the
   multi-role co-signing and evidence requirements of
   `ABUSE-DISCLOSURE-PROTOCOL`. Emergency mode accelerates the timeline but does
   not relax the evidentiary standard.

4. **Art. III.9 boundary**: Privacy does not shield abuse from emergency
   response. However, the emergency pipeline MUST respect the principle of
   minimal disclosure: only data directly relevant to the threat is accessed.

---

## 12. Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| False trigger (fabricated signal) | C3+ required for auto-activation; `manipulated` classification carries severe reputation penalty; investigation under ABUSE-DISCLOSURE-PROTOCOL |
| Sensor compromise | Source independence requirement (section 4.3); TC5 degrades trust in automated evaluation |
| Operator unavailable | Escalation chain with timeout (section 7); auto-activation for life-threatening cases only |
| A3 used as backdoor for unauthorized actions | A3 does not create new permissions; full trace; mandatory review; actions outside agent contract are violations |
| Indefinite emergency mode | Absolute max_extension ceiling; new cycle requires new exception record with fresh evidence |
| Cascading crises as path to permanent A3 | Separate records per trigger; combined TTL = longest, not sum; per-trigger deactivation and review |
| TC5 abuse (declaring epistemic crisis to suppress action) | TC5 cannot activate A3; only heightened monitoring and alerts |
| Council key compromise exploited during crisis | TC2 subclass with specific trapdoor freeze, key rotation, and audit panel (section 3.3) |
| Review fatigue (too many reviews) | Health metric for false alarm rate; calibration review when threshold exceeded |

---

## 13. Federation Parameters

| Parameter | Default | Allowed range | Rule |
| :--- | :--- | :--- | :--- |
| `ttl_tc1` | 4h | 2-8h | More cautious yes, more permissive no |
| `ttl_tc2` | 12h | 6-24h | " |
| `ttl_tc3` | 24h | 12-48h | " |
| `ttl_tc4` | 8h | 4-16h | " |
| `ttl_tc5_alert` | 24h | 12-48h | " |
| `max_ext_tc1` | 24h | 12-48h | " |
| `max_ext_tc2` | 48h | 24-96h | " |
| `max_ext_tc3` | 72h | 36-144h | " |
| `max_ext_tc4` | 48h | 24-96h | " |
| `max_ext_tc5_alert` | 72h | 36-144h | " |
| `operator_timeout_tc1` | 15 min | 5-30 min | " |
| `operator_timeout_tc2` | 30 min | 15-60 min | " |
| `operator_timeout_tc3` | 30 min | 15-60 min | " |
| `operator_timeout_tc4` | 15 min | 5-30 min | " |
| `operator_timeout_tc5` | 60 min | 30-120 min | " |
| `operator_override_window` | 5 min | 2-15 min | " |
| `correlation_window` | 15 min | 5-30 min | " |
| `review_deadline_normal` | 72h | 48-168h | " |
| `review_deadline_escalation` | 24h | 12-48h | " |
| `false_alarm_review_threshold` | 30% | 20-40% | " |
| `max_operator_timeouts_per_period` | 3 in 30 days | 2-5 in 30 days | " |

---

## 14. Open Questions

1. **Credibility scoring automation**: How exactly should C-level be computed
   from raw signals? The current spec describes thresholds qualitatively. A
   quantitative model needs simulation (similar to the reputation scoring
   `[hypothesis]` in `PROCEDURAL-REPUTATION-SPEC`).

2. **Sensorium connector taxonomy**: What types of sensorium connectors exist
   and what signal types do they produce? This document assumes the existence of
   sensorium signals but does not define the connector interface. A separate
   `SENSORIUM-CONNECTOR-SPEC` may be needed.

3. **Cross-federation emergency coordination**: When a crisis spans multiple
   federations (e.g., a network-wide TC2), how are activations coordinated?
   The current spec handles federation-local activation only.

4. **TC5 quantification**: What measurable indicators define an epistemic
   crisis? Oracle output variance? Signal-to-noise ratio? Consensus divergence?
   Currently TC5 activation is operator-assessed.

5. **Legal obligations**: Some jurisdictions may require mandatory reporting for
   certain TC1/TC4 scenarios. The interaction between emergency activation and
   `ABUSE-DISCLOSURE-PROTOCOL` section 10 (jurisdictional notifications) needs
   further specification.

---

## 15. Relation to Other Documents

- **Constitution Art. II.2, II.8**: This document operationalizes the emergency
  action principle: direct danger permits faster action, with trace and review.
- **Constitution Art. IX.3-5**: Crisis mode distinction (normal / crisis /
  support) is realized through the trigger class taxonomy.
- **Constitution Art. V.10, V.13**: A3 operates within agent contract limits;
  agents cannot self-authorize escalation.
- **Constitution Art. X.1-3, X.4-X.8**: Whistleblower protection and abuse
  disclosure interact with TC4 activation (section 11).
- **Constitution Art. III.9**: Privacy does not shield abuse from emergency
  response, but minimal disclosure applies.
- **Constitution Art. XI.1, XI.7-8**: TC5 (epistemic crisis) is grounded in
  the epistemic regime requirements.
- **`AUTONOMY-LEVELS.en.md`**: A3 is the emergency autonomy level; this
  document defines when and how it activates.
- **`EXCEPTION-POLICY.en.md`**: Every A3 activation is an emergency exception
  (section 4.2). The activation record extends the exception data model.
- **`PROCEDURAL-REPUTATION-SPEC.en.md`**: Review outcomes generate `procedural`
  and `incident` domain signals. Operator timeout generates
  `governance_inaction`.
- **`PANEL-SELECTION-PROTOCOL.en.md`**: Escalation-auto review uses ad-hoc
  panels. Council key compromise audit uses ad-hoc panels.
- **`ABUSE-DISCLOSURE-PROTOCOL.en.md`**: TC4 activation may involve abuse
  disclosure; manipulated false alarms may trigger investigation at `S2+`.
- **`REPUTATION-VALIDATION-PROTOCOL.en.md`**: False alarm rate is a health
  metric complementing M1-M5.
- **`NORMATIVE-HIERARCHY.en.md`**: This document is a Level 3 implementing act.
- **Nym protocol (GENYM design)**: Council key compromise (TC2 subclass)
  connects the identity infrastructure with the crisis framework.
