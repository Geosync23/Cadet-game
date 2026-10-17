#!/bin/bash
# go.sh COMMIT OLD — runs a private copy of runcommit.sh so editing the runner never breaks a run in progress
H="$(cd "$(dirname "$0")" && pwd)"; mkdir -p /tmp/cw; T=$(mktemp /tmp/cw/rc_XXXX.sh); cp "$H/runcommit.sh" $T; BM="$H" exec bash $T "$@"
