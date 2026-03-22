# Story 001: Swarm Node Onboarding and Knowledge Query Flow

## Sequence of Steps

1. The user downloads the Swarm Node tool.
2. The user launches Swarm Node.
3. The user is prompted to provide a node name and a specialization set.
4. The application, on behalf of the user, creates a pseudonymous unique wallet on the Avax network, or allows entering recovery words to restore an existing one. This wallet is dedicated to node operations and should not be the user's personal wallet.
5. The user can optionally provide a payout address for surplus transfers.
6. The user is shown a list of compatible LLM models that can be installed, including descriptions of best-fit use cases.
7. The user is prompted to add directories for scanning. These directories may contain files with knowledge correlated to the selected specializations. If multiple specializations are selected, directory-to-specialization mapping is allowed.
8. The user selects models and confirms. The application starts downloading them.
9. After some time, the user receives a notification that models are ready for operation.
10. The application connects to one or more IRC-like networks maintained by nodes and provider servers, then joins specialization-indicating channels to listen for requests.
11. In parallel, content discovered in the configured directories is indexed into a local vector store and used to enrich local orchestrator memory.
12. The user asks the local assistant (paired with the Swarm Node) a domain-specific question, for example: "How to handle STM failures in Clojure?"
13. The node application analyzes the question and checks whether local knowledge is sufficient and complete to answer it. If yes, it answers immediately.
14. If local knowledge is insufficient, the application determines the knowledge domain, joins the relevant IRC channel, and broadcasts a discovery request that contains only a query hash and execution constraints (for example: max price, max wait time, target specialization tags). Full query content is not disclosed at this stage.
15. Other topic-specialized nodes respond with structured offers that include at least: price, deadline, minimum and maximum answer length, specialization tags, node public key, and references/proofs for reputation verification.
16. The application selects the most suitable node by scoring offers using: reputation, leniency fit, answer price, maximum waiting time, proposed minimum and maximum answer length, specialization fit, and other advertised traits. It then creates a uniquely named private channel, invites the selected node, and optionally invites one or more arbiters. The application sends the full question to that channel, optionally encrypted for each recipient with their public key (standalone PGP key or key associated with an Avax address). The question may be refined, but only within agreed leniency bounds (`max_delta_tokens`).
17. Before settlement setup, the application performs a wallet balance and gas-fee precheck. It then creates an Avax contract with explicit acceptance criteria (deadline, length bounds, and expected response format) and settlement mode: arbiter-confirmed; self-confirmed by the application when no arbiter is present; or no confirmation required (for explicit zero-price "free sample" offers).
18. When an answer arrives, the application validates it against contract criteria. If accepted and (when required) confirmed by an arbiter oracle who also receives the answer, the contract settles and the remote node receives payment if payment was agreed.
19. Based on answer quality and contract outcome, the application records a signed transaction receipt and updates node reputation in a distributed-capable reputation store (MVP may keep local records and periodically publish integrity hashes).
20. The application post-processes the remote answer and injects it into the user session response, or forwards it further when the local node acts only as an intermediary. The response includes provenance metadata (source node, contract id, and confidence signal).

## Open Continuation

- Continuation pending (`... cdn`) for retries, disputes, and long-term reputation lifecycle.
