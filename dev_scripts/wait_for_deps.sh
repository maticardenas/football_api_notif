#!/usr/bin/env bash
echo "Wait for deps"

until curl -qs "http://db:5432" 1>/dev/null; do
  >&2 echo "Waiting for Postgres DB"
  sleep 1
done

