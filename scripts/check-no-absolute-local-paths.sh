#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

files=()

while IFS= read -r path; do
  case "$path" in
    scripts/check-no-absolute-local-paths.sh)
      ;;
    *.md|*.toml|*.yml|*.yaml|*.json|*.py|*.sh|*.txt|*.edn|*.clj|*.cljs|*.cljc)
      files+=("$path")
      ;;
  esac
done < <(git ls-files)

if [ "${#files[@]}" -eq 0 ]; then
  exit 0
fi

if grep -nH -E '/Users/|/home/users/' "${files[@]}"; then
  echo
  echo "Forbidden local absolute path reference detected."
  echo "Use repository-relative paths or github.com/diapod/... locators instead."
  exit 1
fi
