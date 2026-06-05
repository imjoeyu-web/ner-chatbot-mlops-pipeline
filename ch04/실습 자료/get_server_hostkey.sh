#!/bin/bash

docker compose exec -it -u airflow airflow-worker /bin/bash -c 'cat /etc/ssh/ssh_host_ecdsa_key.pub'