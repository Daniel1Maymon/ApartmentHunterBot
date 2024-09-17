#!/bin/bash

docker stop $(docker ps -aq)

docker rm -f $(docker ps -aq)

# Find and remove all dangling images (images with <none> tag)
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$DANGLING_IMAGES" ]; then
    docker rmi -f $DANGLING_IMAGES
fi

# Build the new image
docker build -f dockerfile -t apartment-hunter-bot .

# Find and remove all dangling images (images with <none> tag)
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$DANGLING_IMAGES" ]; then
    docker rmi -f $DANGLING_IMAGES
fi

docker run -p 5000:5000 apartment-hunter-bot