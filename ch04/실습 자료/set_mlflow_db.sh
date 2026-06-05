#!/bin/bash

docker compose exec -it postgres /bin/bash -c 'psql postgresql://mlops:mlops@postgres/mlops -c "create database mlflow;"'