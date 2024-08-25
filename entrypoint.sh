#!/bin/bash

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable

# Start Celery worker and beat in the background
#celery -A backend worker --loglevel=info --detach
#celery -A backend beat --loglevel=info --detach

# Start the Gunicorn server
exec "$@"
