#!/bin/bash

# Folosire: ./interact.sh <fqdn> <comanda> [exit_code]
# Exemple:
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app hello
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app exit 1
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app exit 0

FQDN=$1
CMD=$2
CODE=${3:-1}

if [ -z "$FQDN" ] || [ -z "$CMD" ]; then
   echo "Usage: $0 <fqdn> <hello|exit> [exit_code]" >&2
   exit 2
 fi
 if [ "$CMD" = "hello" ]; then
   curl -s "https://$FQDN/"
 elif [ "$CMD" = "exit" ]; then
   curl -s "https://$FQDN/exit?code=$CODE"
 else
   echo "Unknown command: $CMD (expected: hello|exit)" >&2
   exit 2
 fi