#!/bin/bash

# Builds a docker image for the given Dockerfile and pushes it to the docker registry
# given by the env variable

image_name=$1
env=$2

# Validate arguments
if [ -z "$image_name" ] || [ -z "$env" ]; then
    echo "Usage: $0 <image_name> <env>"
    exit 1
fi

# Validate environment
if [ "$env" != "dev" ] && [ "$env" != "prod" ]; then
    echo "env must be either dev or prod"
    exit 1
fi

# Build for dev
if [ "$env" = "dev" ]; then
    echo "Building image for dev"
    
    # Replace underscores with dashes in image name
    dev_image_name=$(echo "${image_name}" | sed 's/_/-/g')
    
    docker build -t "${dev_image_name}:dev" -f "docker/${image_name}.Dockerfile" .
    kind load docker-image "${dev_image_name}:dev" --name rwml-34fa

# Build for prod
else
    echo "Building image ${image_name} for prod"
    BUILD_DATE=$(date +%s)

    docker buildx build --push \
        --platform linux/amd64 \
        -t "ghcr.io/tushar-r-09/${image_name}:0.1.5-beta.${BUILD_DATE}" \
        --label org.opencontainers.image.revision="$(git rev-parse HEAD)" \
        --label org.opencontainers.image.created="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --label org.opencontainers.image.url="https://github.com/Tushar-R-09/crypto-price-prediction/blob/main/docker/${image_name}.Dockerfile" \
        --label org.opencontainers.image.title="${image_name}" \
        --label org.opencontainers.image.description="${image_name} Dockerfile" \
        --label org.opencontainers.image.licenses="" \
        --label org.opencontainers.image.source="https://github.com/Tushar-R-09/crypto-price-prediction" \
        -f "docker/${image_name}.Dockerfile" .
fi
