# Requesting models

The swarm protocol should allow requests to specify checksums of models that must and/or must not be used.

Nodes that provide only models listed as unwanted should ignore such requests. If a list of required models is provided, only nodes that have those models should respond.

Checksums should use official model hashes whenever available. If a model is unofficial, it should generate the hash itself.
