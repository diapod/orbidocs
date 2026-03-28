# Reputation Signal v1

Source schema: [`doc/schemas/reputation-signal.v1.schema.json`](../../schemas/reputation-signal.v1.schema.json)

Machine-readable schema for a small append-only reputation fact record. This contract carries one reputation-affecting signal about a `node`, `participant`, or `nym` subject. It is intentionally unsigned in the core shape so local write-path storage and later transport envelopes stay decoupled.

## Governing Basis

- [`doc/normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md`](../../normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md)
- [`doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`](../../normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md)
- [`doc/normative/50-constitutional-ops/pl/EMERGENCY-ACTIVATION-CRITERIA.pl.md`](../../normative/50-constitutional-ops/pl/EMERGENCY-ACTIVATION-CRITERIA.pl.md)
- [`doc/normative/50-constitutional-ops/pl/ABUSE-DISCLOSURE-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/ABUSE-DISCLOSURE-PROTOCOL.pl.md)
- [`doc/project/20-memos/reputation-signal-v1-invariants.md`](../../project/20-memos/reputation-signal-v1-invariants.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`signal/id`](#field-signal-id) | `yes` | string | Stable identifier of the emitted reputation signal record. |
| [`observed/at`](#field-observed-at) | `yes` | string | Time when the underlying behavior, incident, or review outcome was observed. |
| [`recorded/at`](#field-recorded-at) | `yes` | string | Time when the reputation signal was written as a fact record. Consumers SHOULD enforce `recorded/at >= observed/at`. |
| [`signal/type`](#field-signal-type) | `yes` | string | Open signal namespace. The first path segment is the reputation domain and MUST stay consistent with subject constraints. |
| [`polarity`](#field-polarity) | `yes` | enum: `positive`, `negative` | Reputation direction of the signal. Neutral observations do not belong in this contract. |
| [`weight`](#field-weight) | `yes` | number | Relative strength of the signal, normalized to `(0.0, 1.0]`. |
| [`subject/kind`](#field-subject-kind) | `yes` | enum: `node`, `participant`, `nym` | Identity layer on which the signal lands. |
| [`subject/id`](#field-subject-id) | `yes` | string | Canonical identifier of the reputation subject. The allowed format depends on `subject/kind`. |
| [`observed-via/node-id`](#field-observed-via-node-id) | `no` | string | Optional node through which the behavior was observed when the subject is a participant or nym. |
| [`emitted-by/kind`](#field-emitted-by-kind) | `yes` | enum: `local-runtime`, `operator`, `peer`, `panel`, `federation-review`, `council` | Emitter class of the signal. |
| [`emitted-by/id`](#field-emitted-by-id) | `yes` | string | Identifier of the emitter. The format may depend on `emitted-by/kind`; `council` uses canonical `council:did:key:...`. |
| [`case/ref`](#field-case-ref) | `no` | string | Optional case or review reference when the signal originates in a formal case pipeline. |
| [`basis/refs`](#field-basis-refs) | `no` | array | Optional references to supporting artifacts, reviews, exceptions, or evidence. Negative signals without basis may be downranked by consumers. |
| [`retention/hint`](#field-retention-hint) | `yes` | enum: `ephemeral`, `persistent`, `epoch-scoped` | Emitter-side hint about how long this signal should naturally matter. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable explanation. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "subject/kind": {
      "const": "node"
    }
  },
  "required": [
    "subject/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "subject/id": {
      "pattern": "^node:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "subject/kind": {
      "const": "participant"
    }
  },
  "required": [
    "subject/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "subject/id": {
      "pattern": "^participant:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "subject/kind": {
      "const": "nym"
    }
  },
  "required": [
    "subject/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "subject/id": {
      "pattern": "^nym:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "signal/type": {
      "pattern": "^procedural/"
    }
  },
  "required": [
    "signal/type"
  ]
}
```

Then:

```json
{
  "properties": {
    "subject/kind": {
      "not": {
        "const": "nym"
      }
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "signal/type": {
      "pattern": "^contract/"
    }
  },
  "required": [
    "signal/type"
  ]
}
```

Then:

```json
{
  "properties": {
    "subject/kind": {
      "not": {
        "const": "nym"
      }
    }
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "emitted-by/kind": {
      "const": "council"
    }
  },
  "required": [
    "emitted-by/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "emitted-by/id": {
      "pattern": "^council:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-signal-id"></a>
## `signal/id`

- Required: `yes`
- Shape: string

Stable identifier of the emitted reputation signal record.

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

Time when the underlying behavior, incident, or review outcome was observed.

<a id="field-recorded-at"></a>
## `recorded/at`

- Required: `yes`
- Shape: string

Time when the reputation signal was written as a fact record. Consumers SHOULD enforce `recorded/at >= observed/at`.

<a id="field-signal-type"></a>
## `signal/type`

- Required: `yes`
- Shape: string

Open signal namespace. The first path segment is the reputation domain and MUST stay consistent with subject constraints.

<a id="field-polarity"></a>
## `polarity`

- Required: `yes`
- Shape: enum: `positive`, `negative`

Reputation direction of the signal. Neutral observations do not belong in this contract.

<a id="field-weight"></a>
## `weight`

- Required: `yes`
- Shape: number

Relative strength of the signal, normalized to `(0.0, 1.0]`.

<a id="field-subject-kind"></a>
## `subject/kind`

- Required: `yes`
- Shape: enum: `node`, `participant`, `nym`

Identity layer on which the signal lands.

<a id="field-subject-id"></a>
## `subject/id`

- Required: `yes`
- Shape: string

Canonical identifier of the reputation subject. The allowed format depends on `subject/kind`.

<a id="field-observed-via-node-id"></a>
## `observed-via/node-id`

- Required: `no`
- Shape: string

Optional node through which the behavior was observed when the subject is a participant or nym.

<a id="field-emitted-by-kind"></a>
## `emitted-by/kind`

- Required: `yes`
- Shape: enum: `local-runtime`, `operator`, `peer`, `panel`, `federation-review`, `council`

Emitter class of the signal.

<a id="field-emitted-by-id"></a>
## `emitted-by/id`

- Required: `yes`
- Shape: string

Identifier of the emitter. The format may depend on `emitted-by/kind`; `council` uses canonical `council:did:key:...`.

<a id="field-case-ref"></a>
## `case/ref`

- Required: `no`
- Shape: string

Optional case or review reference when the signal originates in a formal case pipeline.

<a id="field-basis-refs"></a>
## `basis/refs`

- Required: `no`
- Shape: array

Optional references to supporting artifacts, reviews, exceptions, or evidence. Negative signals without basis may be downranked by consumers.

<a id="field-retention-hint"></a>
## `retention/hint`

- Required: `yes`
- Shape: enum: `ephemeral`, `persistent`, `epoch-scoped`

Emitter-side hint about how long this signal should naturally matter.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable explanation.
