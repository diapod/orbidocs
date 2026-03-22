# Node Capability Advertisement

Nodes should expose their capabilities to other nodes using hierarchical keyword prefixes, e.g., `:solve/math`, `:write/poetry`, `:control/camera`, `:store/memory`.

A node should be able to recognize that a synonymous capability matches one of its own, e.g., `:calculate/math` should match if the node provides `:solve/math`.

Each node may have a short, discoverable description of its role in the swarm, e.g., "I store memories and dispatch math puzzles."

Promote to: story or requirements document when the discovery/matching protocol is designed.
