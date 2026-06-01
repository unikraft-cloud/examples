#!/bin/sh
#
# compare-boot.sh — Cold vs warm boot time comparison.
# Spawns N instances from the image (cold boot) and N from the template
# (warm restore), then prints summary statistics (count/min/max/mean/
# median) of timing.boot-time for each group. Cleans up at exit so
# nothing is left running.
#
# Requires a published image and a template (see README.md for the
# `unikraft build` and template-creation commands).
#
# Usage:
#   ./compare-boot.sh        # 3 of each (default)
#   ./compare-boot.sh 5      # 5 of each

set -e

[ -f ./config ] && . ./config

N="${1:-3}"
TEMPLATE_NAME="${INSTANCE_NAME}-tpl"
TS=$(date +%s)
COLD=""
WARM=""

# Read boot-time values from stdin (one per line, e.g. "352.1ms") and
# print count/min/max/mean/median, normalized to milliseconds.
stats() {
    awk '
    function tonum(v,   n) {
        n = v + 0                      # leading numeric part
        if (v ~ /ns$/)    return n / 1000000
        if (v ~ /[uµ]s$/) return n / 1000
        if (v ~ /ms$/)    return n
        if (v ~ /s$/)     return n * 1000
        return n                       # assume already ms
    }
    $1 ~ /^[0-9.]/ {
        x = tonum($1)
        v[n++] = x
        sum += x
        if (n == 1 || x < min) min = x
        if (n == 1 || x > max) max = x
    }
    END {
        if (n == 0) { print "  (no data)"; exit }
        for (i = 0; i < n; i++)
            for (j = i + 1; j < n; j++)
                if (v[j] < v[i]) { t = v[i]; v[i] = v[j]; v[j] = t }
        mean = sum / n
        if (n % 2) median = v[int(n / 2)]
        else       median = (v[n / 2 - 1] + v[n / 2]) / 2
        printf "  count : %d\n", n
        printf "  min   : %.3f ms\n", min
        printf "  max   : %.3f ms\n", max
        printf "  mean  : %.3f ms\n", mean
        printf "  median: %.3f ms\n", median
    }'
}

cleanup() {
    [ -n "${COLD}${WARM}" ] && \
        unikraft instances delete ${COLD} ${WARM} >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

echo "==> Booting ${N} cold + ${N} warm instances..."
i=1
while [ "$i" -le "$N" ]; do
    cn="${INSTANCE_NAME}-cold-${TS}-${i}"
    wn="${INSTANCE_NAME}-warm-${TS}-${i}"
    COLD="${COLD} ${cn}"
    WARM="${WARM} ${wn}"

    unikraft run \
        --name "${cn}" \
        --image "index.unikraft.io/${BASE_IMAGE}:latest" \
        --memory "${MEMORY_MB}MiB" \
        --autostart \
        --restart never \
        -p 443:3000/tls+http \
        -o quiet >/dev/null

    unikraft run \
        --name "${wn}" \
        --template "${TEMPLATE_NAME}" \
        --autostart \
        --scale-to-zero policy=on,stateful=true,cooldown-time=1000 \
        -p 443:3000/tls+http \
        -o quiet >/dev/null

    i=$((i + 1))
done

echo "==> Waiting for instances to finish booting..."
unikraft --log-level warn instances wait --until "state!=starting" ${COLD} ${WARM} >/dev/null

echo ""
echo "==> Cold-boot (from image) — ${N} instances"
unikraft instances list ${COLD} -f timing.boot-time -o table | stats

echo ""
echo "==> Warm-boot (from template) — ${N} instances"
unikraft instances list ${WARM} -f timing.boot-time -o table | stats
