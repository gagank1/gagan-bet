#!/bin/bash

docker run \
    -v $(readlink -f buzzer-418603-732db8e02147.json):/workspace/buzzer-418603-732db8e02147.json \
    -e GOOGLE_APPLICATION_CREDENTIALS="buzzer-418603-732db8e02147.json" \
    --rm \
    -it \
    -p 8000:8000 \
    docker.io/library/gaganbet
