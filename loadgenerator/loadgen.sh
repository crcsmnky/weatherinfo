#!/bin/bash

set -e
trap "exit" TERM

if [[ -z "${FRONTEND_HOST}" ]]; then
    echo >&2 "FRONTEND_HOST not specified"
    exit 1
fi

set -x
locust --host="http://${FRONTEND_HOST}" --no-web -c 5