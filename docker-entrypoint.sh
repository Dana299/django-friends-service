#!/bin/bash

sleep 3

# Apply database migrations
echo "Make and apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Creating superuser
echo "Creating superuser"
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8080
