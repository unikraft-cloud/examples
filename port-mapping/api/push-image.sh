#!/bin/sh

. ./ukc.config
. ./app.config

kraft pkg push index.unikraft.io/"${UKC_USER}"/"${IMAGE_NAME}" .
