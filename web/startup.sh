#!/bin/bash
set -e

# Wait for the postgres database
#echo "Waiting for postgres..."
#while ! nc -z Goalkeeper-db 5432; do
#    sleep 0.1
#done
#echo "PostgreSQL started"

# Destroy and recreate the database on starting the server
# in development mode
if [ "$FLASK_ENV" = "development" ]
then
    echo "Creating database..."
    python manage.py create_db
    echo "Seeding database..."
    python manage.py seed_db
    echo "Done!"
fi

# Start the web app
gunicorn -w 4 --bind 0.0.0.0:5000 --reload wsgi:app