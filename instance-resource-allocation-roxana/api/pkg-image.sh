#!/bin/sh

. ./ukc.config
. ./app.config

kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"${UKC_USER}"/"${IMAGE_NAME}" .
