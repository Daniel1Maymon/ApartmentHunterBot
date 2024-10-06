#!/bin/bash

# Stop and remove all running containers
CONTAINERS=$(docker ps -aq)
if [ -n "$CONTAINERS" ]; then
    docker stop $CONTAINERS
    docker rm -f $CONTAINERS
fi

# Build the new image
docker build -f dockerfile -t apartment-hunter-bot .

# Remove all dangling images (images with <none> tag) after the build process
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$DANGLING_IMAGES" ]; then
    docker rmi -f $DANGLING_IMAGES
fi

# Run the new container
docker run -p 5001:5000 apartment-hunter-bot
