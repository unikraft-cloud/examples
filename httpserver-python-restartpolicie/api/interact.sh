#!/bin/bash

# Folosire: ./interact.sh <fqdn> <comanda> [exit_code]
# Exemple:
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app hello
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app exit 1
#   ./interact.sh purple-pine-j7i7rl30.fra.unikraft.app exit 0

FQDN=$1
CMD=$2
CODE=${3:-1}

if [ "$CMD" = "hello" ]; then
  curl -s https://$FQDN/
elif [ "$CMD" = "exit" ]; then
  curl -s https://$FQDN/exit?code=$CODE
fi