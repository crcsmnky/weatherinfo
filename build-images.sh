#!/bin/bash

set -e

PROJECT=YOUR-PROJECTID-HERE

for DIR in frontend backend-single backend-multiple; do
    echo "=== building image for weather-${DIR} ==="
    gcloud builds submit --tag gcr.io/${PROJECT}/weather-${DIR}:1.0 --async ${DIR}/
done

echo "=== building image for loadgenerator ==="
gcloud builds submit --tag gcr.io/${PROJECT}/loadgenerator:1.0 --async loadgenerator/
