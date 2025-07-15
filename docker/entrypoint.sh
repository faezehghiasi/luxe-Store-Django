#!/bin/sh

echo "Waiting for database to be ready..."

# Wait until PostgreSQL is ready
while ! nc -z db 5432; do
  sleep 1
done

echo "Database is up! Running migrations..."

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

echo "Starting Django server..."

# Start Django server
exec python manage.py runserver 0.0.0.0:8000
