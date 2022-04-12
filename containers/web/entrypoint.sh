#!/bin/bash
set -e

# define settings module
export DJANGO_SETTINGS_MODULE=settings.production

if [ "$STARTUP" == "APP" ]
then

  # execute migrations
  python manage.py migrate --noinput

  # execute collect static
  python manage.py collectstatic --noinput

  # start the gunicorn server
  gunicorn -c /gunicorn.py wsgi:application

else
  exit 1
fi

exec "$@"
