#!/usr/bin/env python3
"""Refresh only the generated PL/EN host-capability blocks from Node's registry."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from capability_registry_docs import update_document

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-src", type=Path, default=ROOT.parent / "node")
    parser.add_argument(
        "--check", action="store_true", help="report drift without writing"
    )
    args = parser.parse_args()

    # Reuse the existing registry validator; rendering must not grow a second contract.
    spec = importlib.util.spec_from_file_location(
        "check_capability_registry",
        Path(__file__).with_name("check-capability-registry.py"),
    )
    assert spec is not None and spec.loader is not None
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    try:
        registry = checker.load_machine_registry(
            args.node_src / "capability" / "capability-registry.v1.json"
        )
        changes = []
        # Validate both destinations before changing either one.
        for language in ("pl", "en"):
            path = (
                ROOT / "doc/project/60-solutions" / f"CAPABILITY-REGISTRY.{language}.md"
            )
            original = path.read_bytes().decode("utf-8")
            updated = update_document(original, registry, language)
            if updated != original:
                changes.append((path, updated))
    except (OSError, ValueError, checker.RegistryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        for path, _ in changes:
            print(
                f"ERROR: stale generated host catalogue: {path.name}", file=sys.stderr
            )
        if changes:
            print(
                "Run make capability-registry-docs with the same Node checkout.",
                file=sys.stderr,
            )
            return 1
    else:
        for path, updated in changes:
            path.write_bytes(updated.encode("utf-8"))
            print(f"updated {path.relative_to(ROOT)}")
    count = sum("host-local" in entry["surfaces"] for entry in registry.values())
    print(
        f"ok PL/EN host catalogues: {count} host-local / {len(registry)} registry entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
