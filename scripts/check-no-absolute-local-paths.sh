#!/usr/bin/env bash
set -euo pipefail

# Retained CI/Make entry point; the gate now checks hosts and IPs as well.
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
exec "${PYTHON:-python3}" "$repo_root/scripts/check_document_privacy.py" "$@"
