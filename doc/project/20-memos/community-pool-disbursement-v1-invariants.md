# community-pool-disbursement.v1 invariants

`community-pool-disbursement.v1` is the smallest policy-facing record for one
community-pool outflow in the host-ledger rail.

## Invariants

1. `pool/account-id` MUST identify a `ledger-account.v1` whose `account/purpose`
   is `community-pool`.
2. `approved-by/id` MUST be canonical `council:did:key:...`.
3. `purpose ∈ { ubc-subsidy, infrastructure-support, emergency-relief }`.
4. `basis/refs` MUST be non-empty.
5. `ledger-transfer/id` MUST point at the append-only transfer that executed the
   outflow.
6. The signed surface is
   `orbiplex-community-pool-disbursement-v1\x00 || deterministic_cbor(payload_without_signature)`.
7. This artifact records the approved outflow and its purpose; it does not
   replace `ledger-transfer.v1` as the financial source of truth.
