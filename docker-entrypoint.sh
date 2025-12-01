#!/bin/sh

python manage.py makemigrations data
python manage.py migrate

exec "$@"