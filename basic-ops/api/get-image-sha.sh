#!/bin/sh

. ./ukc.config
. ./app.config

unikraft images get "${UKC_USER}/${IMAGE_NAME}:latest" -o json > out 2> err

if test $? -ne 0; then
    cat err 1>&2
else
    cat out | jq -r ".[0].digest"
fi

rm -f out err
