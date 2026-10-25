# Whisper-source-profile.v1

Source schema: [`doc/schemas/whisper-source-profile.v1.schema.json`](../../schemas/whisper-source-profile.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-source-profile.v1` |  |
| [`profile/kind`](#field-profile-kind) | `yes` | enum: `production`, `acceptance-fixture` |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`epoch/anchor`](#field-epoch-anchor) | `yes` | const: `1970-01-05T00:00:00Z` |  |
| [`source/derivation`](#field-source-derivation) | `yes` | const: `issuer-derived-v1` |  |
| [`renewal/default`](#field-renewal-default) | `yes` | const: `on-demand` |  |
| [`key/active-limit`](#field-key-active-limit) | `yes` | const: `4096` |  |
| [`renewal/consent-limit`](#field-renewal-consent-limit) | `yes` | const: `7` |  |
| [`clock/skew-seconds`](#field-clock-skew-seconds) | `yes` | const: `5` |  |
| [`epoch/seconds`](#field-epoch-seconds) | `yes` | integer |  |
| [`certificate/ttl-seconds`](#field-certificate-ttl-seconds) | `yes` | integer |  |
| [`request/ttl-seconds`](#field-request-ttl-seconds) | `yes` | integer |  |
| [`status/collection-max-age-seconds`](#field-status-collection-max-age-seconds) | `yes` | integer |  |
| [`status/emission-max-age-seconds`](#field-status-emission-max-age-seconds) | `yes` | integer |  |
| [`retention/identifying-seconds`](#field-retention-identifying-seconds) | `yes` | integer |  |
| [`retention/reset-buffer-seconds`](#field-retention-reset-buffer-seconds) | `yes` | integer |  |
| [`retention/tombstone-seconds`](#field-retention-tombstone-seconds) | `yes` | integer |  |
| [`epoch/certificate-limit`](#field-epoch-certificate-limit) | `yes` | const: `2048` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "profile/kind": {
      "const": "production"
    }
  },
  "required": [
    "profile/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "epoch/seconds": {
      "const": 604800
    },
    "certificate/ttl-seconds": {
      "const": 86400
    },
    "request/ttl-seconds": {
      "const": 900
    },
    "status/collection-max-age-seconds": {
      "const": 3600
    },
    "status/emission-max-age-seconds": {
      "const": 300
    },
    "retention/identifying-seconds": {
      "const": 86400
    },
    "retention/reset-buffer-seconds": {
      "const": 300
    },
    "retention/tombstone-seconds": {
      "const": 604800
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "profile/kind": {
      "const": "acceptance-fixture"
    }
  },
  "required": [
    "profile/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "epoch/seconds": {
      "const": 600
    },
    "certificate/ttl-seconds": {
      "const": 120
    },
    "request/ttl-seconds": {
      "const": 60
    },
    "status/collection-max-age-seconds": {
      "const": 60
    },
    "status/emission-max-age-seconds": {
      "const": 30
    },
    "retention/identifying-seconds": {
      "const": 60
    },
    "retention/reset-buffer-seconds": {
      "const": 10
    },
    "retention/tombstone-seconds": {
      "const": 600
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-source-profile.v1`

<a id="field-profile-kind"></a>
## `profile/kind`

- Required: `yes`
- Shape: enum: `production`, `acceptance-fixture`

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-epoch-anchor"></a>
## `epoch/anchor`

- Required: `yes`
- Shape: const: `1970-01-05T00:00:00Z`

<a id="field-source-derivation"></a>
## `source/derivation`

- Required: `yes`
- Shape: const: `issuer-derived-v1`

<a id="field-renewal-default"></a>
## `renewal/default`

- Required: `yes`
- Shape: const: `on-demand`

<a id="field-key-active-limit"></a>
## `key/active-limit`

- Required: `yes`
- Shape: const: `4096`

<a id="field-renewal-consent-limit"></a>
## `renewal/consent-limit`

- Required: `yes`
- Shape: const: `7`

<a id="field-clock-skew-seconds"></a>
## `clock/skew-seconds`

- Required: `yes`
- Shape: const: `5`

<a id="field-epoch-seconds"></a>
## `epoch/seconds`

- Required: `yes`
- Shape: integer

<a id="field-certificate-ttl-seconds"></a>
## `certificate/ttl-seconds`

- Required: `yes`
- Shape: integer

<a id="field-request-ttl-seconds"></a>
## `request/ttl-seconds`

- Required: `yes`
- Shape: integer

<a id="field-status-collection-max-age-seconds"></a>
## `status/collection-max-age-seconds`

- Required: `yes`
- Shape: integer

<a id="field-status-emission-max-age-seconds"></a>
## `status/emission-max-age-seconds`

- Required: `yes`
- Shape: integer

<a id="field-retention-identifying-seconds"></a>
## `retention/identifying-seconds`

- Required: `yes`
- Shape: integer

<a id="field-retention-reset-buffer-seconds"></a>
## `retention/reset-buffer-seconds`

- Required: `yes`
- Shape: integer

<a id="field-retention-tombstone-seconds"></a>
## `retention/tombstone-seconds`

- Required: `yes`
- Shape: integer

<a id="field-epoch-certificate-limit"></a>
## `epoch/certificate-limit`

- Required: `yes`
- Shape: const: `2048`
