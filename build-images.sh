#!/bin/bash

set -e

PROJECT=${1}

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

function usage
{
    echo "Usage:"
    echo "$ build-images.sh [YOUR-PROJECT-ID]"
}

if [[ -z $@ ]]; then
    usage
    exit 0
fi

for DIR in frontend backend-single backend-multiple; do
    echo "=== building image for weather-${DIR} ==="
    gcloud builds submit --tag gcr.io/${PROJECT}/weather-${DIR}:1.0 --async ${DIR}/
done

echo "=== building image for loadgenerator ==="
gcloud builds submit --tag gcr.io/${PROJECT}/loadgenerator:1.0 --async loadgenerator/
