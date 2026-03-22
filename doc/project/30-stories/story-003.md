# Story 003: Memory Nodes

## Sequence of Steps

1. Node A needs to preserve an important knowledge artifact so it remains available beyond Node A's current runtime instance.
2. Node A connects to an IRC-like network and joins a public thematic channel relevant to the knowledge classification.
3. Node A publishes a storage request specifying required capacity, subject (short description), and visibility mode (`public` or `private`).
4. Other nodes respond with storage offers. For private memory, offers may include paid storage terms where payload access is limited to authorized parties.
5. Offers may also include optional retention constraints: maximum storage duration and maximum idle TTL (time without retrieval requests).
6. Node A selects the most suitable offer.
7. Node A and the selected storage provider (Node B) move to a private channel.
8. If payment is involved, arbiters are invited according to the settlement flow from `story-001.md`.
9. Node A sends the memory object in JSON form (metadata plus Base64-encoded payload) to the private channel.
10. Node B confirms successful storage and enables free validation retrieval for Node A (and arbiters, when present).
11. Node A stores the returned knowledge identifier(s) and Node B identifier required for future retrieval.
12. When Node A needs the stored knowledge, it may request it directly from Node B or, for distributed/public memory, request it through a public channel.
