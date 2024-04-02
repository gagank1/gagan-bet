#!/bin/bash

if [ "$1" == "prod" ]; then
    docker build -t gaganbet .
else
    docker build -t gaganbet .
fi
