#!/bin/bash

set -e

PROJECT=${1}
VERSION=1.0

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
    echo "=== building image gcr.io/${PROJECT}/weather-${DIR}:${VERSION} ==="
    gcloud builds submit --tag gcr.io/${PROJECT}/weather-${DIR}:${VERSION} --async ${DIR}/ --project ${PROJECT}
done

echo "=== building image gcr.io/${PROJECT}/loadgenerator:${VERSION} ==="
gcloud builds submit --tag gcr.io/${PROJECT}/loadgenerator:${VERSION} --async loadgenerator/ --project ${PROJECT}
