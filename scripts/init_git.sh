#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ ! -d .git ]; then git init -b main; fi
git status --short
printf '\nRepository initialized. Review files, then create the first commit when ready.\n'
