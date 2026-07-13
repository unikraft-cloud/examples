FROM --platform=linux/x86_64 debian:bookworm AS build

# Install packages.
RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install vsftpd \
    ;

# Create FTP user
RUN echo "root:rootpass" | chpasswd

# Configure vsftpd.
RUN mkdir -p /var/run/vsftpd/empty && \
    touch /var/log/vsftpd.log
RUN echo "root" > /etc/vsftpd.userlist
RUN sed -i '/^root/d' /etc/ftpusers || true

FROM scratch

# vsftpd binary
COPY --from=build /usr/sbin/vsftpd /usr/sbin/vsftpd

# System files
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/group /etc/group
COPY --from=build /etc/shadow /etc/shadow
COPY --from=build /etc/ftpusers /etc/ftpusers
COPY --from=build /etc/vsftpd.userlist /etc/vsftpd.userlist
COPY --from=build /etc/ld.so.cache /etc/ld.so.cache

# PAM configuration
COPY --from=build /etc/pam.d /etc/pam.d
COPY --from=build /lib/x86_64-linux-gnu/security /lib/x86_64-linux-gnu/security

# NSS libraries (required for PAM user/password lookups)
COPY --from=build /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=build /lib/x86_64-linux-gnu/libnss_files.so.2 /lib/x86_64-linux-gnu/libnss_files.so.2
COPY --from=build /lib/x86_64-linux-gnu/libnss_compat.so.2 /lib/x86_64-linux-gnu/libnss_compat.so.2

# Required by PAM modules (pam_shells.so needs /etc/shells, pam_unix.so needs login.defs)
COPY --from=build /etc/shells /etc/shells
COPY --from=build /etc/login.defs /etc/login.defs

# Runtime directories
COPY --from=build /var/run/vsftpd/empty /var/run/vsftpd/empty
COPY --from=build /var/log/vsftpd.log /var/log/vsftpd.log

# Shell (needed by wrapper.sh)
COPY --from=build /bin/sh /bin/sh
COPY --from=build /bin/mkdir /bin/mkdir
COPY --from=build /bin/chown /bin/chown
COPY --from=build /bin/echo /bin/echo
COPY --from=build /usr/bin/tail /usr/bin/tail

# Required shared libraries (from ldd /usr/sbin/vsftpd)
COPY --from=build /lib/x86_64-linux-gnu/libwrap.so.0 /lib/x86_64-linux-gnu/libwrap.so.0
COPY --from=build /lib/x86_64-linux-gnu/libpam.so.0 /lib/x86_64-linux-gnu/libpam.so.0
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libcap.so.2 /lib/x86_64-linux-gnu/libcap.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libnsl.so.2 /lib/x86_64-linux-gnu/libnsl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libaudit.so.1 /lib/x86_64-linux-gnu/libaudit.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libtirpc.so.3 /lib/x86_64-linux-gnu/libtirpc.so.3
COPY --from=build /lib/x86_64-linux-gnu/libcap-ng.so.0 /lib/x86_64-linux-gnu/libcap-ng.so.0
COPY --from=build /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.3 /lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /lib/x86_64-linux-gnu/libk5crypto.so.3 /lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libcom_err.so.2 /lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /lib/x86_64-linux-gnu/libkrb5support.so.0 /lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /lib/x86_64-linux-gnu/libkeyutils.so.1 /lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2

# Required by coreutils (mkdir, chown, tail)
COPY --from=build /lib/x86_64-linux-gnu/libselinux.so.1 /lib/x86_64-linux-gnu/libselinux.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpcre2-8.so.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0

# Required by PAM (pam_unix.so password verification)
COPY --from=build /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1

# Configuration and entrypoint
COPY ./vsftpd.conf /etc/vsftpd/vsftpd.conf

COPY --chmod=755 ./wrapper.sh /wrapper.sh
