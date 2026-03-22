# Schema Metadata Convention

This directory keeps JSON Schema as the canonical machine-readable boundary contract.

We also use lightweight schema metadata to carry semantic meaning close to the fields
without changing validation behavior.

## Preferred metadata

### `description`

Use `description` for the primary semantic meaning of:

- the whole schema,
- a field,
- a nested object,
- a reusable `$defs` entry.

`description` should explain what the field means in the Orbiplex domain, not only its
syntax or storage shape.

### `$comment`

Use `$comment` for short author-side notes that help maintainers but are not required
for end-user documentation. Validators may ignore this field.

Typical use cases:

- local modeling caveats,
- migration notes,
- why a constraint exists,
- reminders about non-obvious edge cases.

### `x-dia-basis`

Use `x-dia-basis` as an Orbiplex-specific extension that links a schema or a field to
the normative or operational documents that define its semantics.

Recommended shape:

```json
{
  "x-dia-basis": [
    "CONSTITUTION.pl.md",
    "constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md"
  ]
}
```

Notes:

- paths should be repository-relative, from `/orbidocs`,
- prefer the most direct governing sources,
- keep the list short and specific.

## Authoring rule

Use metadata only where it adds semantic clarity.

Do not turn schema files into prose-heavy documents. The schema should remain readable
as a contract first. Richer narrative belongs in the governing markdown documents.

## Practical rule of thumb

- put the core meaning in `description`,
- put traceability in `x-dia-basis`,
- put maintainer-only notes in `$comment`.
