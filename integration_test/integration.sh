#!/bin/bash

export WANDB_KEY=202ada5746d12050a9ba2b9834945a9c1c973d08

if [ -z "${GITHUB_ACTIONS}" ]; then
    cd "$(dirname "$0")"
fi

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    export LOCAL_IMAGE_NAME=mlops-capstone:latest
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
    cd ../src
    if [[ -z "${GITHUB_ACTIONS}" ]]; then
        docker buildx build --platform=linux/amd64 --build-arg WANDB_KEY=${WANDB_KEY} -t ${LOCAL_IMAGE_NAME} .
    else
        docker build --build-arg WANDB_KEY=${WANDB_KEY} -t ${LOCAL_IMAGE_NAME} .
    fi
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

docker run --detach -p 9000:8080 ${LOCAL_IMAGE_NAME}

sleep 5

cd "$(dirname "$0")"
pipenv run python integration.py

ERROR_CODE=$?

# if [ ${ERROR_CODE} != 0 ]; then
#     docker logs mlops:capstone
#     docker stop mlops:capstone
#     exit ${ERROR_CODE}
# fi
