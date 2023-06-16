#!/bin/sh

echo "Waiting for database..."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "Database started"

alembic upgrade head
uvicorn main:app --host 0.0.0.0 --reload

exec "$@"
