#!/bin/sh

. ./ukc.config
. ./app.config

unikraft build . --output "${UKC_USER}/${IMAGE_NAME}:latest"
