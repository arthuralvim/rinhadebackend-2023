#!/usr/bin/env bash

set -o errexit
set -o nounset

postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="db",
        port="5432",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

if [ "$RUN_INITIAL_DATA" = "True" ]
then
    echo 'Running initial data in DB.'
    python initdb.py
    echo 'Running initial data in DB. : FINISHED'
else
    echo "Skipping initial data."
fi
