# Federation Bootstrap and Trust FAQ

An Orbiplex federation is neither an address list nor a shared CA. It is a
locally accepted technical order whose roots, roles, and evidence are explicit,
signed, and consumed by independent policy gates.

The operational sequence is documented in the
[Federation Bootstrap and Trust HOWTO](../howto/federation-bootstrap-and-trust-howto.en.md).

## What does `federation-root.v1` establish?

The root pack binds `federation/id`, sovereign subjects, official-service
endorsement policy, Seed Directory bootstrap, default network selectors, and
ceremony and revocation metadata in one signed contract.

It does not make every later record true. It identifies which signatures and
policy material may participate in local evaluation. Every consumer still
verifies the artifact it uses at its own decision point.

## Does a bootstrap entry prove that a service is official?

No. The entry says where to attempt a connection. Official status follows only
from an active `federation-service-endorsement.v1` verified against the current
root pack and revocation view.

A bootstrap without a valid endorsement may remain advisory or community
source material, but must not be silently promoted to official service.

## How does an endorsement differ from a capability passport?

A passport answers: "may this subject provide or invoke this capability within
this scope?". An endorsement answers: "does this service have official status
inside this federation?".

A service may hold a valid passport and remain non-official. It may also be
officially endorsed while failing a capability, recipient, or local invocation
policy check. These proofs form a conjunction; they do not substitute for each
other.

## Does a TLS certificate prove Node identity?

No. TLS proves that the channel satisfied endpoint transport policy. The peer
handshake proves possession of the Node identity key. Passports and
endorsements concern service authority, while local policy makes the final
decision.

Public WebPKI may make HTTPS/WSS on port 443 operationally convenient, but does
not by itself establish federation membership or the right to provide a
capability.

## Why is Seed Directory needed when the root pack contains bootstrap entries?

The root pack should remain small and change rarely. Seed Directory maintains
the temporal projection of reachability, capability registrations,
revocations, subject routing, and endpoint evidence. Bootstrap identifies the
first path to that projection; it does not replace it.

This split bounds the blast radius: an ordinary endpoint or capability change
does not require a new root ceremony, while changing sovereign authority roots
does.

## Is an attested Seed Directory response truth about the network?

No. `seed-directory-query-attestation.v1` proves that one directory served a
specific canonical view at a given projection high-water mark. It does not
prove that the directory knows every fact or that the world matches its
projection.

The consumer must still apply multi-directory policy, revocations, TTLs, peer
handshake, and domain verification.

## What does trusted Agora replay provide?

Replay lets the local Seed Directory reconstruct accepted facts from trusted
Agora lanes without making Agora the domain authority. Agora carries the
envelope and enforces its publish ACL; Seed Directory revalidates record kind,
schema, signature, and semantics.

The cursor is technical replay state. It does not replace the projection
high-water mark or monotonic domain sequence numbers.

## Why does changing the root pack require a restart?

The active root defines the process's federation identity. Hot reload could
leave some subsystems acting under the old order while others use the new one.
The daemon may therefore validate a candidate, but changing the active
fingerprint is restart-only.

The data-dir guard rejects `pack_version` rollback, the same version with a
different digest, and a mismatched `federation/id`. Restart is a controlled
transition point, not a way around these rules.

## How is a Seed Directory TLS pin rotated?

The MVP carries one active leaf-DER pin per endpoint. Rotation requires a root
pack with a higher `pack_version`, a new signature, and restart. The pin
requires HTTPS and protects the channel to the directory; it does not grant
official status.

Do not add a second conflicting pin for the same endpoint in manual trust
configuration. Configuration must refuse rather than pick one arbitrarily.

## What happens when every Seed Directory is unavailable?

The Node enters an isolated/bootstrap or degraded posture according to active
configuration. It must not replace the missing directory with the first
endpoint it encounters or disable passport verification.

Existing fresh and locally verified material may remain usable within its
retention bounds, but new critical decisions that depend on revocation
freshness should fail closed.

## Does federation prevent cross-federation cooperation?

No. Federation Root selects one active `federation/id` and its internal order.
Cooperation across that boundary belongs to higher contracts such as alliance
policy, Room, Corpus, Whisper, or explicit Artifact Delivery.

A cross-federation carrier does not rewrite the local root or automatically
widen Community Memarium, capability passports, or official status.

## Which evidence should the operator be able to inspect?

The operator should be able to distinguish:

- active root digest, `pack_version`, and `federation/id`;
- accepted and rejected official-service endorsements;
- Seed Directory source, trust tier, replay cursor, and last error;
- TLS pin/evidence and peer-handshake result;
- capability passport and its revocation status;
- the consumer's final decision and policy ref.

One green "trusted" field would hide too many distinct causes.
