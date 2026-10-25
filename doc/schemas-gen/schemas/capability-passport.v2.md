# Capability-passport.v2

Source schema: [`doc/schemas/capability-passport.v2.schema.json`](../../schemas/capability-passport.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport.v2` |  |
| [`passport_id`](#field-passport-id) | `yes` | string |  |
| [`beneficiary_participant_id`](#field-beneficiary-participant-id) | `yes` | string |  |
| [`beneficiary_node_id`](#field-beneficiary-node-id) | `yes` | string |  |
| [`authority_subject_ref`](#field-authority-subject-ref) | `yes` | string |  |
| [`signer_key`](#field-signer-key) | `yes` | string |  |
| [`capability_id`](#field-capability-id) | `yes` | enum: `messaging-send`, `messaging-receive`, `inac.invitation` |  |
| [`scope`](#field-scope) | `yes` | object |  |
| [`issued_at`](#field-issued-at) | `yes` | string |  |
| [`expires_at`](#field-expires-at) | `yes` | string |  |
| [`issuance_authority`](#field-issuance-authority) | `yes` | object |  |
| [`signature`](#field-signature) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`allowedCaller`](#def-allowedcaller) | object | Exact host-resolved caller for one of the closed Messaging issuance templates. No client-selected caller or wildcard. |
| [`messagingLocalSendProfileV1`](#def-messaginglocalsendprofilev1) | object | P097 local preparation evidence, distinct from INAC push and recipient consent. Stage A does not enforce this profile at outbound execution. |
| [`messagingReceiveProfileV1`](#def-messagingreceiveprofilev1) | object |  |
| [`inacInvitationProfileV1`](#def-inacinvitationprofilev1) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "issuance_authority": {
      "properties": {
        "delegation": {
          "properties": {
            "templates": {
              "contains": {
                "properties": {
                  "template": {
                    "const": "nym-bootstrap-consent"
                  }
                },
                "required": [
                  "template"
                ]
              }
            }
          },
          "required": [
            "templates"
          ]
        }
      },
      "required": [
        "delegation"
      ]
    }
  },
  "required": [
    "issuance_authority"
  ]
}
```

Then:

```json
{
  "allOf": [
    {
      "properties": {
        "capability_id": {
          "const": "inac.invitation"
        }
      }
    },
    {
      "properties": {
        "scope": {
          "properties": {
            "profiles": {
              "items": {
                "properties": {
                  "profile": {
                    "const": "inac-invitation@v1"
                  },
                  "artifact_schemas": {
                    "items": {
                      "enum": [
                        "nym-key-request-sealed.v1",
                        "nym-key-offer-sealed.v1",
                        "nym-issuance-request-sealed.v1",
                        "nym-issuance-decision-sealed.v1"
                      ]
                    }
                  }
                },
                "required": [
                  "profile",
                  "artifact_schemas"
                ]
              }
            }
          }
        }
      }
    },
    {
      "properties": {
        "issuance_authority": {
          "properties": {
            "issuance_caller": {
              "const": "host:nym-bootstrap.accept"
            }
          }
        }
      }
    }
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "scope": {
      "properties": {
        "profiles": {
          "contains": {
            "properties": {
              "artifact_schemas": {
                "items": {
                  "enum": [
                    "nym-key-request-sealed.v1",
                    "nym-key-offer-sealed.v1",
                    "nym-issuance-request-sealed.v1",
                    "nym-issuance-decision-sealed.v1"
                  ]
                }
              }
            },
            "required": [
              "artifact_schemas"
            ]
          }
        }
      },
      "required": [
        "profiles"
      ]
    }
  },
  "required": [
    "scope"
  ]
}
```

Then:

```json
{
  "allOf": [
    {
      "properties": {
        "issuance_authority": {
          "properties": {
            "issuance_caller": {
              "const": "host:nym-bootstrap.accept"
            }
          }
        }
      }
    },
    {
      "properties": {
        "issuance_authority": {
          "properties": {
            "delegation": {
              "properties": {
                "templates": {
                  "maxItems": 1,
                  "items": {
                    "properties": {
                      "template": {
                        "const": "nym-bootstrap-consent"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "issuance_authority": {
      "properties": {
        "issuance_caller": {
          "const": "host:nym-bootstrap.accept"
        }
      }
    }
  }
}
```

Then:

```json
{
  "allOf": [
    {
      "properties": {
        "issuance_authority": {
          "properties": {
            "issuance_caller": {
              "const": "host:nym-bootstrap.accept"
            }
          }
        }
      }
    },
    {
      "properties": {
        "issuance_authority": {
          "properties": {
            "delegation": {
              "properties": {
                "templates": {
                  "maxItems": 1,
                  "items": {
                    "properties": {
                      "template": {
                        "const": "nym-bootstrap-consent"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport.v2`

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string

<a id="field-beneficiary-participant-id"></a>
## `beneficiary_participant_id`

- Required: `yes`
- Shape: string

<a id="field-beneficiary-node-id"></a>
## `beneficiary_node_id`

- Required: `yes`
- Shape: string

<a id="field-authority-subject-ref"></a>
## `authority_subject_ref`

- Required: `yes`
- Shape: string

<a id="field-signer-key"></a>
## `signer_key`

- Required: `yes`
- Shape: string

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: enum: `messaging-send`, `messaging-receive`, `inac.invitation`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

<a id="field-issuance-authority"></a>
## `issuance_authority`

- Required: `yes`
- Shape: object

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-allowedcaller"></a>
## `$defs.allowedCaller`

- Shape: object

Exact host-resolved caller for one of the closed Messaging issuance templates. No client-selected caller or wildcard.

<a id="def-messaginglocalsendprofilev1"></a>
## `$defs.messagingLocalSendProfileV1`

- Shape: object

P097 local preparation evidence, distinct from INAC push and recipient consent. Stage A does not enforce this profile at outbound execution.

<a id="def-messagingreceiveprofilev1"></a>
## `$defs.messagingReceiveProfileV1`

- Shape: object

<a id="def-inacinvitationprofilev1"></a>
## `$defs.inacInvitationProfileV1`

- Shape: object
