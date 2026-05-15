#!/bin/sh

image_name=asia-northeast3-docker.pkg.dev/project-47ee8279-d093-40d1-8f6/morise-kubeflow-cr/ner-preprocess
image_tag=latest

full_image_name=${image_name}:${image_tag}
base_image_tag=3.11.6-slim

cd "$(dirname "$0")" 

docker build --build-arg BASE_IMAGE_TAG=${base_image_tag} -t "${full_image_name}" .
docker push "$full_image_name"
