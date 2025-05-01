#!/bin/bash

# Fail the script if any command fails
set -e

REGISTRY=$1
FRAMEWORK=$2

if [[ -z "$REGISTRY" || -z "$FRAMEWORK" ]]; then
  echo "Error: REGISTRY and FRAMEWORK variables must be set."
  exit 1
fi

IMAGE_NAME="mlops-model-serving"
TAG="${FRAMEWORK}-latest"

echo "Building Docker image: ${REGISTRY}/${IMAGE_NAME}:${TAG} from serving/docker/Dockerfile.${FRAMEWORK}"
docker build --platform linux/amd64 -t ${REGISTRY}/${IMAGE_NAME}:${TAG} -f serving/docker/Dockerfile.${FRAMEWORK} .
echo "Docker image built and tagged as ${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo "Pushing..."
docker push