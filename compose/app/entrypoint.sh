#!/bin/bash

set -o errexit
set -o nounset

bash /entrypoint/wait-for-it.sh db:5432 -- echo "postgres is up"

exec "$@"
