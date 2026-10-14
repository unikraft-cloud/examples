#!/bin/sh -e
export HOME=/root

mkdir -p "${HOME}"
chmod 700 "${HOME}"
cd "${HOME}"

# Install public key if given by user
if test -n "${PUBKEY}"; then
	mkdir -p  "${HOME}/.ssh"
	chmod 700 "${HOME}/.ssh"
	echo "${PUBKEY}" >> "${HOME}/.ssh/authorized_keys"
	chmod 600 "${HOME}/.ssh/authorized_keys"
	unset PUBKEY
fi

# Launch dropbear SSH server
exec /usr/sbin/dropbear -ERF
