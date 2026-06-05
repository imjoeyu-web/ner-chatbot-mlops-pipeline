#!/bin/bash

docker compose exec -it -u root airflow-worker /bin/bash -c 'curl https://dl.min.io/client/mc/release/linux-amd64/mc > mc && \
                                                             chmod +x mc && \
                                                             mv mc /usr/bin/mc'