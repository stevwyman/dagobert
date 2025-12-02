#!/bin/sh

python manage.py makemigrations beta
python manage.py migrate

exec "$@"