#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -p 5432; do
  echo "Waiting for Postgres at $host:5432..."
  sleep 2
done

echo "Postgres is ready! Starting backend..."
exec $cmd
