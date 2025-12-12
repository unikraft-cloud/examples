#!/usr/bin/env bash

set -e

mkdir -p /root && \
    echo "Hello from UKP!" > /root/hello.txt
chown -R root:root /root

/usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf &

tail -f /var/log/vsftpd.log
