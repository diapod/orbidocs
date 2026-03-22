# DIA Raw Signal and Style-Transformation Policy

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-RAW-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | `0.1.0-draft` |
| `basis` | Art. II.8-9, III.1-4, XI.7 of the DIA Constitution; `doc/normative/30-core-values/en/CORE-VALUES.en.md` section "Right to the Raw Signal" |
| `mechanism status` | signal modes, transformation bases, and the meta-marker model are normative; presentation layers may be parameterized by federations |

---

## 1. Purpose of the Document

The Constitution grants the user a right to the raw signal and requires that every
AI transformation of style, tone, structure, or level of formalization leave a
meta-marker. What is still missing is an implementing document that defines:

- the modes of work on an utterance,
- when transformation is allowed,
- which meta-markers are mandatory,
- how to leave an auditable trace of such intervention.

This document operationalizes those duties.

---

## 2. General Rule

1. The user's raw signal is a protected good.
2. The default operating mode of the system is preservation of the character of the
   utterance, not its smoothing, professionalization, or aestheticization.
3. Transformation of an utterance may occur only on the basis of:
   - an explicit user request,
   - an explicit user policy,
   - minimally necessary protective redaction,
   - an exception compliant with `EXCEPTION-POLICY.en.md`.
4. Absence of a procedural basis means transformation is forbidden.

---

## 3. Signal Modes

The system MUST distinguish at least the following modes:

| Mode | Meaning |
| :--- | :--- |
| `raw` | signal preserved without intentional transformation of style, tone, or structure beyond technical transport |
| `structured` | content has been organized or mapped into structure without intentional smoothing of the character of the utterance |
| `transformed` | style, tone, form, or level of formalization has been deliberately changed |
| `redacted` | signal has been limited or masked for protective, privacy, or legal reasons |

`structured` may not be used as a loophole for hidden smoothing of the signal. If
ordering materially changes the character of the utterance for reception purposes,
`transformed` must be used.

---

## 4. Permissible Bases for Transformation

### 4.1. Explicit User Request

Transformation is permissible when the user explicitly asks for:

- a summary,
- a task list,
- translation,
- a tone change,
- a formality change,
- smoothing or stylistic editing,
- another semantically equivalent transformation.

### 4.2. User Policy

The user may set a persistent transformation policy, provided that:

1. the policy is explicit,
2. it can be disabled,
3. it does not hide from the user the fact that the signal was processed.

### 4.3. Protective Redaction

Without a user request, only transformations minimally necessary for the following
are permissible:

1. protection of sensitive data,
2. reduction of risk of direct harm,
3. compliance with a legal or constitutional obligation,
4. protection of a whistleblower or a person exposed to retaliation.

Such an operation should be as narrow as possible and use mode `redacted`, not
`transformed`, unless an additional style transformation actually occurs.

### 4.4. Procedural Exception

A departure from the above rules requires an exception compliant with
`EXCEPTION-POLICY.en.md` and may not become the default mode.

---

## 5. Meta-Markers

### 5.1. Mandatory Rule

If the output is not in mode `raw`, the system MUST attach a meta-marker visible to
the end recipient or unambiguously available in the same interface.

### 5.2. Minimal Meta-Marker Fields

```yaml
signal_marker:
  mode: "transformed" # raw | structured | transformed | redacted
  actor: "ai"         # ai | human | hybrid
  requested_by: "user" # user | user_policy | safety_policy | exception
  basis_ref: "[prompt / policy-id / exception-id / rule-id]"
  operations:
    - "tone_shift"
    - "structure_extraction"
  visible_to_user: true
```

### 5.3. Minimal Operation Semantics

`operations` SHOULD use a controlled vocabulary covering at least:

- `structure_extraction`,
- `summarization`,
- `translation`,
- `tone_shift`,
- `formality_shift`,
- `style_polish`,
- `safety_redaction`,
- `privacy_redaction`.

---

## 6. Audit Trace of Transformation

Every transformation other than `raw` MUST leave an audit trace:

```yaml
signal_transform_event:
  transform_id: "[unique identifier]"
  source_ref: "[message / segment / artifact]"
  input_mode: "raw"
  output_mode: "structured"
  actor_type: "ai"
  requested_by: "user"
  basis_ref: "[reference]"
  operations:
    - "structure_extraction"
  created_at: "[timestamp]"
```

The trace need not disclose the full content of the transformed signal to all
participants, but it MUST be available under minimum-disclosure rules for audit,
appeal, and abuse analysis.

---

## 7. Compliance Tests

The system is non-compliant with this policy if any of the following occurs:

1. it smooths or professionalizes utterances by default without a basis,
2. it hides from the user the fact of transformation,
3. it uses mode `structured` to conceal a real change of tone or style,
4. it leaves no `basis_ref` for a transformation that is not `raw`,
5. it treats the raw form of expression as a default reason to lower the user's
   rights or credibility.

---

## 8. Federation Health Metrics

A federation should measure at least:

- `raw_preservation_rate` - the share of signals left in mode `raw`,
- `non_requested_transform_rate` - the share of transformations not triggered by a
  direct user request,
- `hidden_transform_incidents` - the number of detected transformations without a
  meta-marker,
- `redaction_overreach_rate` - the share of protective redactions found in review to
  be too broad,
- `appeals_on_signal_transform` - the number of appeals concerning signal
  transformation.

High `non_requested_transform_rate` or `hidden_transform_incidents` is a sign of
drift toward paternalism or masking of reality.

---

## 9. Relation to Other Documents

- **Constitution Art. II.8-9**: right to the raw signal and mandatory meta-marker.
- **Constitution Art. III.1-4**: the user retains control over data and policies.
- **Constitution Art. XI.7**: the filter may not operate as hidden censorship.
- **`EXCEPTION-POLICY.en.md`**: procedural departures and protective redactions.

