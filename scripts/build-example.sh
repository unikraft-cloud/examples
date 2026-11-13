#!/usr/bin/env bash
# Usage: scripts/build-example.sh <example> <x86_64|arm64>

set -euo pipefail

example=${1:?example directory required}
arch=${2:?architecture required}

case "$arch" in
    x86_64|arm64) ;;
    *) echo "Unsupported architecture: ${arch}" >&2; exit 1 ;;
esac

# `unikraft build` needs a profile even when it only writes a local archive.
export UNIKRAFT_PROFILE_ENV=true UKC_METRO=local UKC_TOKEN=unused

out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT

built=0
while IFS= read -r kraftfile; do
    dir=$(dirname "$kraftfile")
    "$(dirname "$0")/kraftfile-targets.sh" "$kraftfile" "$arch" || continue
    echo "==> Building ${dir} for ${arch}"
    unikraft build "$dir" --arch "$arch" --output "${out}/${dir//\//-}.tar"
    built=$((built + 1))
done < <(find "$example" -maxdepth 2 -name Kraftfile | sort)

if [[ $built -eq 0 ]]; then
    echo "No Kraftfile in ${example} targets kraftcloud/${arch}" >&2
    exit 1
fi
