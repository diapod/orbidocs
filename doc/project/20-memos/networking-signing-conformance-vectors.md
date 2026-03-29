# Networking Signing Conformance Vectors

## Status

Memo

## Date

2026-03-28

## Purpose

This memo freezes the first byte-exact conformance vectors for the signed Node
networking seed.

It is intentionally narrow:

- one positive `ack` handshake fixture,
- one signed node-advertisement fixture,
- and the exact domain-separated signing-input bytes plus resulting Ed25519
  signatures as emitted by the current reference implementation in the sibling
  `node` workspace.

## Scope

These vectors are for:

- interoperability checks,
- regression tests in future implementations,
- and avoiding ambiguity around deterministic CBOR signing inputs.

They do not yet cover:

- session-key derivation outputs,
- capability-advertisement,
- or Phase 1 `nym` certificate signing inputs.

## Fixed Test Signer

The vectors below use one fixed test signer:

- secret key bytes: `32 * 0x29`
- secret key base64url (unpadded): `KSkpKSkpKSkpKSkpKSkpKSkpKSkpKSkpKSkpKSkpKSk`
- `node-id`: `node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE`
- `key/public`: `z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE`

This key is a deterministic test fixture only.

## Vector 1: `peer-handshake.v1` `ack`

Fixture:

- `doc/schemas/examples/bootstrap.ack.peer-handshake.json`

Expected domain-separated signing-input hex:

```text
706565722d68616e647368616b652e763100ad62747374323032362d30332d32335431383a31303a30335a656e6f6e6365736e6f6e63653a30314a514e4f44454853303032676b65792f616c67676564323535313968736368656d612f76016a6b65792f7075626c696378307a364d6b774a4670764a564665313579674767594c54597569507766686b6b44526b4d4734654b5146543867363579456b73657373696f6e2f707562782b544f44626137686e4a484153394d3567506e4f6a763572384253555842664c66754933316e59354e4131346c68616e647368616b652f69647068733a30314a514e4f444548533030326e68616e647368616b652f6d6f64656361636b6e73656e6465722f6e6f64652d6964783d6e6f64653a6469643a6b65793a7a364d6b774a4670764a564665313579674767594c54597569507766686b6b44526b4d4734654b5146543867363579456e73657373696f6e2f696e74656e746c706565722d636f6e6e65637471726563697069656e742f6e6f64652d6964783d6e6f64653a6469643a6b65793a7a364d6b724c516b4a72325951364c3865597736516b3866395038476d4a6d37613378365031763151327733453472357361636b2f6f662d68616e647368616b652d69647068733a30314a514e4f44454853303031746361706162696c69746965732f6f666665726564816e636f72652f6d6573736167696e67
```

Expected Ed25519 signature base64url:

```text
kh-QM5zHwOMbIaoL8SXbQMfGJX826D7B5rM-8mZtu6KaCS6drQPSXICfJOED-iRDQOoadOcTszgeZWDyuji8Cw
```

## Vector 2: `node-advertisement.v1`

Fixture:

- `doc/schemas/examples/vector-signed.node-advertisement.json`

Expected domain-separated signing-input hex:

```text
6e6f64652d6164766572746973656d656e742e763100ab676b65792f616c676765643235353139676e6f64652f6964783d6e6f64653a6469643a6b65793a7a364d6b774a4670764a564665313579674767594c54597569507766686b6b44526b4d4734654b51465438673635794568736368656d612f760169656e64706f696e747381a46c656e64706f696e742f75726c78237773733a2f2f6e6f64652d30312e646f63732e6f726269706c65782e61692f706565726d656e64706f696e742f726f6c65686c697374656e657271656e64706f696e742f7072696f726974790072656e64706f696e742f7472616e73706f7274637773736a657870697265732d617474323032362d30332d32335431383a31383a30305a6a6b65792f7075626c696378307a364d6b774a4670764a564665313579674767594c54597569507766686b6b44526b4d4734654b5146543867363579456b73657175656e63652f6e6f116d616476657274697365642d617474323032362d30332d32335431383a30383a30305a6d66656465726174696f6e2f69646f6665643a6f726269706c65782d706c706164766572746973656d656e742f6964726164763a30314a514e4f4445414456303031747472616e73706f7274732f737570706f727465648163777373
```

Expected Ed25519 signature base64url:

```text
GGxfc1fHLYqoUhSygpyHSl_yKuilR2YsCx1peziDLhGLXfO2YQz9IXGU4VMDWnh-Zwltk0D-JXnO1IeF1GZMAQ
```

## Provenance

These vectors were emitted from the current sibling Node implementation through:

- `github.com/diapod/orbiplex/node/protocol/src/lib.rs`
- `github.com/diapod/orbiplex/node/crypto/src/lib.rs`

The intention is not to make the implementation authoritative, but to freeze one
concrete interoperable byte-level baseline for future independent runtimes.

## Promote To

Promote these vectors into a more formal conformance surface when:

- Phase 1 `nym` artifacts gain byte-exact signing helpers in the implementation,
- session-KDF vectors are needed across more than one runtime,
- or a dedicated protocol conformance directory emerges in `orbidocs`.
