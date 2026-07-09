# Federation Root Ceremony HOWTO

This HOWTO describes the key-generation path for a federation-root ceremony:
each custodian generates a fresh ceremony key with
`tools/federation-root-ceremony/federation_root_ceremony.py keygen`. It does
not cover importing a node participant key, using a node `data-dir`, or deriving
an operator identity from a custodian key.

Related documents:

- Proposal 076: `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- Solution 041: `doc/project/60-solutions/041-federation-root/041-federation-root.md`
- Root charter: `doc/normative/50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md`
- Tool reference: `node/tools/federation-root-ceremony/README.md`

## Roles

- **Coordinator** prepares the governance roster, unsigned root draft, manifest,
  ceremony transcript, and final assembly.
- **Custodian** generates one dedicated key on their own machine, verifies the
  frozen digest, signs the exact root draft, and returns only public material and
  a detached signature.
- **Verifier** independently runs manifest, assembly, and final pack checks
  before publication. This may be the coordinator plus at least one custodian.

The coordinator never receives private key material. Custodian keys may later
attest or authorize a separate operator identity through an explicit binding,
but they are not operator identities and must not be converted into one.

## Pre-Ceremony Checklist

Agree on these values before any digest is frozen:

- `federation_id`, for example `orbiplex-main`;
- `pack_version`;
- root subject, usually an `org:did:key:...` for production;
- custody policy reference, for example `org-custody:orbiplex-main-root:v1`;
- threshold, for example `2-of-3`;
- charter or governance `policy_ref`;
- exact custodian roster and display names;
- ceremony id;
- publication target for the final `federation-root.v1` pack;
- redaction rules for the public transcript.

All commands below use repository-relative paths. Run them from the repository
root that contains `node/`.

## 1. Coordinator Creates the Workspace

```sh
mkdir -p ceremony/keys ceremony/public ceremony/signatures ceremony/out
```

`ceremony/keys/` is shown only for local examples. In a real ceremony, each
custodian keeps their own private-key directory on their own machine; the
coordinator should not create or collect private keys.

## 2. Each Custodian Generates Their Key

Each custodian runs this locally, using their own label in file names:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py keygen \
  --out ceremony/keys/alice.ed25519.pem \
  --public-json ceremony/public/alice.public.json \
  --prompt-passphrase
```

The tool asks for and confirms a passphrase, writes an encrypted PEM private
key, and never accepts the passphrase as a CLI argument. For non-interactive
offline automation, use `--passphrase-stdin` or a short-lived,
permission-restricted `--passphrase-file`.

Expected local outputs:

- `ceremony/keys/alice.ed25519.pem` — passphrase-encrypted private Ed25519
  key, mode `0600`, keep secret and offline;
- `ceremony/public/alice.public.json` — public `key_public` record, safe to send
  to the coordinator.

The custodian sends only `alice.public.json` to the coordinator. Do not send the
PEM file, paste it into chat, attach it to tickets, or include it in the
transcript.

## 3. Coordinator Builds the Roster

The coordinator extracts each `key_public` from the public records and prepares
the unsigned root draft from the explicit governance roster:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py \
  root-draft-from-roster \
  --confirm-roster \
  --production-orbiplex-main \
  --out ceremony/unsigned.federation-root.json \
  --federation-id orbiplex-main \
  --pack-version 1 \
  --issued-at-now \
  --policy-ref policy:dia-root-001@0.1.0#appeals \
  --org-id org:did:key:z6Mk... \
  --custody-policy-ref org-custody:orbiplex-main-root:v1 \
  --threshold-min-signers 2 \
  --authorized-key-public z6MkAlice... \
  --authorized-key-public z6MkBob... \
  --authorized-key-public z6MkCarol...
```

`--confirm-roster` is required because authority comes from the governance
roster, not from whichever signatures later appear in a directory.

## 4. Coordinator Freezes the Digest

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py digest \
  ceremony/unsigned.federation-root.json
```

Record the returned `sha256:...` digest in the ceremony transcript. This digest
is the value every custodian must independently compare before signing.

## 5. Coordinator Creates and Verifies the Manifest

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py manifest-init \
  --production-orbiplex-main \
  --out ceremony/manifest.json \
  --ceremony-id orbiplex-main-root-001 \
  --federation-id orbiplex-main \
  --min-signers 2 \
  --total-signers 3 \
  --root ceremony/unsigned.federation-root.json
```

Then verify that the manifest still points to the frozen root draft:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py manifest-verify \
  --production-orbiplex-main \
  --manifest ceremony/manifest.json
```

Send the following to each custodian:

- `ceremony/unsigned.federation-root.json`;
- `ceremony/manifest.json`;
- the expected `sha256:...` digest through a second channel, if possible;
- the exact ceremony id and roster summary.

Do not send private keys because the coordinator must not have them.

## 6. Each Custodian Verifies Before Signing

Each custodian verifies the digest locally:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py digest \
  ceremony/unsigned.federation-root.json
```

They compare the output with the digest recorded by the coordinator. If it does
not match, stop the ceremony. Do not sign a "nearly identical" root draft.

Each custodian should also inspect at least:

- `federation_id`;
- `pack_version`;
- `attestation_roots[]`;
- `custody_policies[]`;
- `threshold/min_signers`;
- their own `key_public` in the authorized signer list;
- `policy_ref`;
- bootstrap and Seed Directory entries.

## 7. Each Custodian Signs the Frozen Root

Each custodian signs with their local private key:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py sign \
  --root ceremony/unsigned.federation-root.json \
  --key ceremony/keys/alice.ed25519.pem \
  --prompt-passphrase \
  --out ceremony/signatures/alice.sig.json
```

The passphrase unlocks only the local encrypted PEM. It is not written to the
signature record, manifest, transcript, or root pack.

The custodian sends only `alice.sig.json` back to the coordinator. The detached
signature is public ceremony material; the private key remains local.

## 8. Coordinator Assembles the Root Pack

After collecting enough detached signatures, the coordinator assembles strictly:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py assemble \
  --production-orbiplex-main \
  --strict \
  --root ceremony/unsigned.federation-root.json \
  --out ceremony/out/federation-root.v1.json \
  ceremony/signatures
```

Strict assembly rejects invalid and unauthorized signatures. For production
`orbiplex-main`, the command also enforces the production profile and requires
`--strict`.

## 9. Everyone Verifies the Final Pack

The coordinator and at least one custodian verify the final artifact:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py verify \
  --production-orbiplex-main \
  ceremony/out/federation-root.v1.json
```

The reported digest should match the frozen digest. If verification fails, do
not publish the pack.

## 10. Publish and Archive

Publish:

- `ceremony/out/federation-root.v1.json`;
- the redacted ceremony transcript;
- public custodian records;
- manifest and final digest.

Archive privately:

- each custodian's encrypted private key, controlled only by that custodian;
- local machine notes needed for future rotation/recovery;
- any non-public incident notes.

Never archive private keys in the repository, public transcript, issue tracker,
chat, or shared backup. A backup of the encrypted PEM is acceptable only when
the backup and passphrase are managed as separate secrets for that custodian.

## Failure Rules

Stop and restart from a new draft or new digest when:

- any custodian receives a different digest;
- the manifest no longer verifies;
- the roster is wrong or incomplete;
- the threshold is wrong;
- a private key may have been copied to the coordinator or a public channel;
- strict assembly rejects a signature;
- final verification reports a different digest or rejected signature.

Facts beat convenience: if the frozen bytes change, signatures over the old
bytes are not reusable.
