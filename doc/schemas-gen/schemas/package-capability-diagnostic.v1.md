# Package Capability Diagnostic V1

Source schema: [`doc/schemas/package-capability-diagnostic.v1.schema.json`](../../schemas/package-capability-diagnostic.v1.schema.json)

Host-derived, bounded local operator metadata. Never caller authority; no prompts, inputs or outputs.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-diagnostic.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`cause`](#field-cause) | `yes` | enum: `package-revoked`, `safe-mode`, `signer-untrusted`, `member-pin-mismatch`, `declaration-invalid`, `peer-scope-unsupported`, `flow-not-loaded`, `flow-digest-mismatch`, `provider-mismatch`, `provider-collision`, `schema-invalid`, `activation-required`, `activation-expired`, `operator-binding-lost`, `use-missing`, `loop-cancelled`, `loop-stopped`, `use-withdrawn`, `use-expired`, `use-stale`, `use-scope-mismatch`, `provider-unavailable`, `capacity-exhausted`, `request-invalid`, `deadline-elapsed`, `request-stale`, `invocation-conflict` |  |
| [`subject/refs`](#field-subject-refs) | `yes` | array |  |
| [`next/action`](#field-next-action) | `yes` | enum: `activate-package`, `exit-safe-mode`, `trust-signer`, `reimport-package`, `await-peer-support`, `load-provider`, `disable-conflicting-package`, `rebind-operator`, `open-loop`, `none`, `renew-loop`, `reapprove-after-reactivation`, `review-request`, `retry-later` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "use-withdrawn"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "none"
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "package-revoked"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "activate-package"
    }
  }
}
```

### Rule 3

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "safe-mode"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "exit-safe-mode"
    }
  }
}
```

### Rule 4

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "signer-untrusted"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "trust-signer"
    }
  }
}
```

### Rule 5

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "member-pin-mismatch"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "reimport-package"
    }
  }
}
```

### Rule 6

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "declaration-invalid"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "reimport-package"
    }
  }
}
```

### Rule 7

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "peer-scope-unsupported"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "await-peer-support"
    }
  }
}
```

### Rule 8

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "flow-not-loaded"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "load-provider"
    }
  }
}
```

### Rule 9

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "flow-digest-mismatch"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "load-provider"
    }
  }
}
```

### Rule 10

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "provider-mismatch"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "load-provider"
    }
  }
}
```

### Rule 11

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "provider-collision"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "disable-conflicting-package"
    }
  }
}
```

### Rule 12

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "schema-invalid"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "reimport-package"
    }
  }
}
```

### Rule 13

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "activation-required"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "activate-package"
    }
  }
}
```

### Rule 14

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "activation-expired"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "activate-package"
    }
  }
}
```

### Rule 15

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "operator-binding-lost"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "rebind-operator"
    }
  }
}
```

### Rule 16

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "use-missing"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "open-loop"
    }
  }
}
```

### Rule 17

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "loop-cancelled"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "open-loop"
    }
  }
}
```

### Rule 18

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "loop-stopped"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "none"
    }
  }
}
```

### Rule 19

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "use-expired"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "renew-loop"
    }
  }
}
```

### Rule 20

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "use-stale"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "reapprove-after-reactivation"
    }
  }
}
```

### Rule 21

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "use-scope-mismatch"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "review-request"
    }
  }
}
```

### Rule 22

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "provider-unavailable"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "load-provider"
    }
  }
}
```

### Rule 23

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "capacity-exhausted"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "retry-later"
    }
  }
}
```

### Rule 24

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "request-invalid"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "review-request"
    }
  }
}
```

### Rule 25

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "deadline-elapsed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "review-request"
    }
  }
}
```

### Rule 26

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "request-stale"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "review-request"
    }
  }
}
```

### Rule 27

When:

```json
{
  "required": [
    "cause"
  ],
  "properties": {
    "cause": {
      "const": "invocation-conflict"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "next/action": {
      "const": "review-request"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-diagnostic.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-cause"></a>
## `cause`

- Required: `yes`
- Shape: enum: `package-revoked`, `safe-mode`, `signer-untrusted`, `member-pin-mismatch`, `declaration-invalid`, `peer-scope-unsupported`, `flow-not-loaded`, `flow-digest-mismatch`, `provider-mismatch`, `provider-collision`, `schema-invalid`, `activation-required`, `activation-expired`, `operator-binding-lost`, `use-missing`, `loop-cancelled`, `loop-stopped`, `use-withdrawn`, `use-expired`, `use-stale`, `use-scope-mismatch`, `provider-unavailable`, `capacity-exhausted`, `request-invalid`, `deadline-elapsed`, `request-stale`, `invocation-conflict`

<a id="field-subject-refs"></a>
## `subject/refs`

- Required: `yes`
- Shape: array

<a id="field-next-action"></a>
## `next/action`

- Required: `yes`
- Shape: enum: `activate-package`, `exit-safe-mode`, `trust-signer`, `reimport-package`, `await-peer-support`, `load-provider`, `disable-conflicting-package`, `rebind-operator`, `open-loop`, `none`, `renew-loop`, `reapprove-after-reactivation`, `review-request`, `retry-later`
