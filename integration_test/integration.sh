#!/bin/bash

export WANDB_KEY=202ada5746d12050a9ba2b9834945a9c1c973d08
export S3_ENDPOINT="http://localhost:4566"

if [ -z "${GITHUB_ACTIONS}" ]; then
    cd "$(dirname "$0")"
fi

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    export LOCAL_IMAGE_NAME=mlops-capstone:latest
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
    cd ../src
    if [[ -z "${GITHUB_ACTIONS}" ]]; then
        docker buildx build --platform=linux/amd64 -t ${LOCAL_IMAGE_NAME} .
    else
        docker build -t ${LOCAL_IMAGE_NAME} .
    fi
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

docker-compose up -d
sleep 5

aws --endpoint-url=${S3_ENDPOINT} s3 mb s3://testing

pipenv run python integration.py

ERROR_CODE=$?

echo ${ERROR_CODE}

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down
