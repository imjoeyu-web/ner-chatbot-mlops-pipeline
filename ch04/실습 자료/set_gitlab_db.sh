#!/bin/bash

docker compose exec -it gitlab /bin/bash -c "gitlab-rake gitlab:setup"