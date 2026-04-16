# Host Capability Authorization Strata

Status: Draft  
Scope: Shared architecture diagram for host-capability authorization.

This diagram shows the main authorization strata used when a local host
capability, such as Sealer, Signer, or a future Memarium surface, receives a
request through the daemon.

``` mermaid
flowchart TB
  Request["HTTP request<br/>module authtok / control auth"]
  CallerIdentity["CallerIdentity<br/>who is invoking?"]
  CallerBinding["CallerBinding<br/>local subject-key binding"]
  Passport["CapabilityPassport<br/>what capability is presented?"]
  Profiles["Profile evaluators<br/>OR across recognized profiles"]
  Revocation["RevocationView<br/>freshness + revoked ids"]
  Decision["AuthorizationDecision"]
  Operation["Host capability operation<br/>Sealer / Signer / Memarium"]
  Audit["Authorization audit event"]

  Request --> CallerIdentity
  CallerIdentity --> CallerBinding
  CallerBinding --> Passport
  Passport --> Profiles
  Profiles --> Revocation
  Revocation --> Decision
  Decision -->|Authorized| Operation
  Decision -->|Denied| Audit
  Operation --> Audit
```

## Reading Notes

1. `CallerIdentity` is the request-level identity observed by the daemon
   dispatch layer.
2. `CallerBinding` is local verifier state. It binds a caller label/source to
   public subject keys without embedding secrets.
3. `CapabilityPassport` carries delegated authority, but it does not by itself
   prove that the current caller is allowed to use it.
4. Profile evaluators are domain-specific. A verifier authorizes when at least
   one recognized profile independently matches the requested operation.
5. `RevocationView` is local verifier state. Freshness and explicit revocation
   checks happen after a profile match narrows the applicable revocation window.
6. Operation-level audit and authorization-level audit are separate strata.

Related documents:

- [Capability Binding](../../project/60-solutions/capability-binding.md)
- [Sealer](../../project/60-solutions/sealer.md)
- [Key Roles and Key Use Taxonomy](../../project/40-proposals/038-key-roles-and-key-use-taxonomy.md)
