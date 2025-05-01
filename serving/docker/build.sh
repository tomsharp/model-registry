#!/bin/bash

# Fail the script if any command fails
set -e

REGISTRY_NAME=$1
FRAMEWORK=$2

if [[ -z "$REGISTRY_NAME" || -z "$FRAMEWORK" ]]; then
  echo "Error: REGISTRY_NAME and FRAMEWORK variables must be set."
  exit 1
fi

REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
TAG="${FRAMEWORK}-latest"
FULL_IMAGE="${REGISTRY}/${APP_NAME}:${TAG}"

echo "🔨 Building Docker image: ${FULL_IMAGE} from serving/docker/Dockerfile.${FRAMEWORK}"
docker build --platform linux/amd64 -t "${FULL_IMAGE}" -f "serving/docker/Dockerfile.${FRAMEWORK}" .

echo "🔐 Logging in to Amazon ECR..."
aws ecr get-login-password --region "${AWS_DEFAULT_REGION}" | docker login --username AWS --password-stdin "${REGISTRY}"

echo "📤 Pushing Docker image to ECR: ${FULL_IMAGE}"
docker push "${FULL_IMAGE}"

echo "✅ Docker image built and pushed: ${FULL_IMAGE}"