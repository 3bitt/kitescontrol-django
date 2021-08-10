#!/bin/bash

set -o errexit
set -o nounset

bash /entrypoint/wait-for-it.sh db-mysql:3306 -- echo "postgres is up"

exec "$@"
