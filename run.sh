#!/bin/bash

IMG_NAME="us-west1-docker.pkg.dev/buzzer-418603/buzzerapp/buzzerimg"

docker run \
    -v $(readlink -f buzzer-418603-732db8e02147.json):/workspace/buzzer-418603-732db8e02147.json \
    -e GOOGLE_APPLICATION_CREDENTIALS="buzzer-418603-732db8e02147.json" \
    --rm \
    -it \
    -p 8000:8000 \
    "$IMG_NAME:latest-dev"
