#!/usr/bin/env bash
# Checks the examples whose Kraftfiles target kraftcloud/arm64.

set -euo pipefail

cd "$(dirname "$0")/.."

arch_pattern='(^|[^[:alnum:]_])(x86_64|x86-64|amd64|aarch64|arm64|x64)([^[:alnum:]_]|$)|/lib64/'
skip_pattern='^[[:space:]]*(#|"?[[:alnum:]_-]+"?([[:space:]]*\|[[:space:]]*"?[[:alnum:]_-]+"?)*\))'

status=0

for example in */; do
    example=${example%/}
    kraftfiles=$(find "$example" -maxdepth 2 -name Kraftfile | sort)
    [[ -n $kraftfiles ]] || continue

    multiarch=0
    while IFS= read -r kraftfile; do
        if scripts/kraftfile-targets.sh "$kraftfile" arm64; then
            multiarch=1
        fi
    done <<< "$kraftfiles"
    [[ $multiarch -eq 1 ]] || continue

    while IFS= read -r kraftfile; do
        for target in x86_64 arm64; do
            if ! scripts/kraftfile-targets.sh "$kraftfile" "$target"; then
                echo "::error file=${kraftfile}::Missing target kraftcloud/${target}"
                status=1
            fi
        done
    done <<< "$kraftfiles"

    while IFS=: read -r file line match; do
        [[ $match =~ $skip_pattern ]] && continue
        echo "::error file=${file},line=${line}::Architecture-specific value: ${match}"
        status=1
    done < <(find "$example" -maxdepth 2 -name 'Dockerfile*' -exec grep -nHE "$arch_pattern" {} + || true)
done

exit $status
