# Project Examples

This directory contains small, copyable examples for Orbiplex project authors.
They are intentionally minimal and contract-focused: each example shows the data
shape and process boundary first, and leaves product logic to the module author.

## Layout

- `middleware/` - middleware examples, including supervised HTTP/JSON modules
  and host-owned JSON-e-flow role providers.

These examples are not normative specifications. Normative contracts live in
`doc/schemas/`, proposals, and the Node middleware schemas. When an example and a
schema disagree, the schema wins.
