#!/bin/bash

VERSION=0.1
IMG_NAME="us-west1-docker.pkg.dev/buzzer-418603/buzzerapp/buzzerimg"

if [ "$1" == "prod" ]; then
    docker build --platform=linux/amd64 -t "$IMG_NAME:$VERSION-prod" .
    docker push "$IMG_NAME:$VERSION-prod"
else
    docker build -t "$IMG_NAME:$VERSION-dev" -t "$IMG_NAME:latest-dev" .
fi
