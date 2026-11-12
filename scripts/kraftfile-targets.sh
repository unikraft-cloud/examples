#!/usr/bin/env bash
# Usage: scripts/kraftfile-targets.sh <Kraftfile> <x86_64|arm64>

set -euo pipefail

kraftfile=${1:?Kraftfile required}
arch=${2:?architecture required}

grep -qE "^[[:space:]]*-[[:space:]]*[\"']?kraftcloud/${arch}[\"']?[[:space:]]*(#.*)?$" "$kraftfile"
