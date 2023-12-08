CPPFLAGS = -I.
CFLAGS = -Wall -Wextra -fPIC
LDFLAGS = -pie

.PHONY: all clean

all: epoll_echo_server

epoll_echo_server: epoll_echo_server.o utils/sock/sock_util.o utils/log/log.o

epoll_echo_server.o: epoll_echo_server.c utils/sock/sock_util.h utils/log/log.h utils/utils.h

utils/sock/sock_util.o: utils/sock/sock_util.c utils/sock/sock_util.h

utils/log/log.o: utils/log/log.c utils/log/log.h

clean::
	-rm -f utils/sock/sock_util.o utils/log/log.o
	-rm -f epoll_echo_server.o epoll_echo_server
	-rm -f *~
