# Documentation host and address pseudonyms

## Purpose and scope

Public documentation uses stable pseudonyms for private deployment hosts and
addresses. This changes presentation, not host identity, execution authority or
acceptance status. The private reverse mapping lives at
`orbidocs:local/host-pseudonyms.json`; it is shared conceptually with Node rather
than copied into a second registry. It is not distributed or required by CI.

## Private mapping

The local JSON file has this shape (the empty arrays are an editing template):

```json
{
  "schema": "documentation-pseudonyms.local.v1",
  "hosts": {
    "host-A.local": { "aliases": [] }
  },
  "addresses": {}
}
```

Each populated host entry contains the original DNS aliases in `aliases`.
Each address entry uses an `IPADDR-A`-style key and an `address` string containing
one IPv4 or IPv6 address. Append new labels; never renumber existing ones. Use
uppercase letters A through Z, then AA, AB and so on. Keep aliases unique after
DNS case/trailing-dot normalization and addresses unique after IP normalization.
The suffix letters of a host and an address do not by themselves establish an
association. A physical host is distinct from logical roles such as `node-a`.

Keep the map with owner-only permissions (`0600`). The existing `/local/` ignore
rule prevents ordinary additions; it does not protect against `git add -f`.
The source gate refuses tracked local material. Never copy the map into the
publication tree, upload it to CI, paste it into reports, or treat it as Node
runtime configuration. Local validation does not print its contents:

```sh
python3 scripts/check_document_privacy.py --check-map
```

## Editing documents

Use `host-A.local` and `IPADDR-A` in prose. These are documentation labels, not
reachable endpoints. In each affected proposal, add a **Host pseudonyms** section
linking here and giving the private map's repository locator as inline code.
Do not make a broken public link to the ignored file.

Replace complete tokens, including occurrences inside URLs and code blocks,
without changing longer identifiers or logical node roles. Review the diff.
An `IPADDR-A` label is not a valid IP literal: an IP-typed runnable JSON example
must either keep a reviewed illustrative address or become an explicitly marked
local template that is materialized before contract validation. Do not silently
break JSON Schema examples. The current example topology uses illustrative
addresses; none has been asserted to identify a private machine.

Do not modify signed artifacts, retained evidence bytes, historical digests or
qualifiers. Pseudonymize their documentary projection and keep its evidence
reference. This does not erase names from Git history or already published copies.
Node evidence and runtime files are outside this Orbidocs migration.

## Privacy gate and exceptions

`make check-no-absolute-local-paths` retains the existing CI entry point and now
checks source-like text for private absolute paths, IPv4, IPv6 and `.local` hosts.
It includes tracked and non-ignored untracked files; ignored local files, build
outputs and binary assets are outside that source pass. Symlinks and undecodable
source-like text fail instead of silently passing. There is no whole-file waiver
for the checker or its tests.

The explicit exclusions are:

- `localhost`, IPv4 loopback in the entire `127.0.0.0/8` range, `0.0.0.0`, and
  IPv6 loopback in equivalent spellings (including IPv4-mapped loopback);
- complete host pseudonyms of the form `host-[A-Z]+.local` and address labels of
  the form `IPADDR-[A-Z]+`; suffixes must not extend them into another name;
- a bare `/Volumes` or `/Volumes/` prefix without a concrete path component.

Two additional project-wide exceptions are the exact example hostname
`orbiplex.local` (case-insensitive) and the exact IPv4-shaped token `1.3.2.1`,
which also occurs as an upstream zlib version. These exceptions apply to sources,
rendered pages, search indexes and text downloads. They do not admit subdomains,
neighboring addresses or IPv4-mapped IPv6 forms. They are explicit documentation
policy, not a claim that either token could never identify a real endpoint.

All other syntactically valid IP addresses require review, including addresses
used in examples. An IPv4 address embedded in IPv6 is counted once. Schema URNs
are identifiers, not DNS hostnames. A double colon inside a regex non-capturing
group is syntax; a standalone unspecified IPv6 address is not globally exempt.
Apart from the explicit token above, version/section numbers, SVG coordinates and other code syntax resembling IPs
require contextual qualification, not a global allowlist of those numbers.

Reviewed exceptions are kept in `scripts/document-privacy-exceptions.json` as
an exact **path + token + context + reason**. They include illustrative topology
addresses, fixture domains, DNS-SD service types and capability/scope identifiers.
A private deployment name must be pseudonymized rather than added as an exception.
The registry literals are reviewed inputs; its other fields are scanned normally.
New contexts and new files do not inherit an exception automatically.

## Verification and publication

```sh
make test-document-privacy
make check-no-absolute-local-paths
make validate-schemas
make html-i18n
make check-published-privacy
```

Publication checking scans generated HTML text and attributes (rejoining syntax
highlighting spans), each search-index entry, and text downloads. Exceptions in
rendered prose are limited to the same source document and exact reviewed token;
the source pass must also pass with the original context. Static third-party
JavaScript/CSS bundles and binary assets are outside the publication text pass;
repository-owned script/style sources remain covered by the source gate.

The Pages workflow runs this check before artifact upload. It also rejects a
published private-map filename. These checks are safeguards for the stated address
and path classes, not a general detector of secrets, obfuscated identifiers or
private DNS names outside `.local`. Regenerate outputs from sanitized sources;
do not hand-edit generated pages or search indexes.
