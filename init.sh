#!/bin/bash

fdir=$(dirname "${BASH_SOURCE[0]}")

function f() {
    if test "$#" -eq 1 && test -d "$1"; then
        cd "$1"
    else
        python3 "$fdir/f.py" "$@"
    fi
}
