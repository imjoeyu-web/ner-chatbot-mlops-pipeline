ARG BASE_IMAGE_TAG=3.11.6-slim
FROM python:$BASE_IMAGE_TAG
RUN python3 -m pip install tensorflow pandas scikit-learn
COPY ./src /pipelines/component/src