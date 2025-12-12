FROM debian:bookworm AS base

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

COPY ./vsftpd.conf /etc/vsftpd/vsftpd.conf

COPY --chmod=755 ./wrapper.sh /wrapper.sh
