#!/bin/bash

VERSION=0.1
IMG_NAME="us-west1-docker.pkg.dev/buzzer-418603/buzzerapp/buzzerimg:$VERSION"

docker run \
    -v $(readlink -f buzzer-418603-732db8e02147.json):/workspace/buzzer-418603-732db8e02147.json \
    -e GOOGLE_APPLICATION_CREDENTIALS="buzzer-418603-732db8e02147.json" \
    --rm \
    -it \
    -p 8000:8000 \
    $IMG_NAME
