#!/bin/bash

echo "Waiting for db..."
while ! nc -z db 3306; do sleep 1; done;
echo "Db up."
yes | python manage.py migrate --settings=api.settings.development
python manage.py populate_db_currencies
retVal=$?
if [ $retVal -ne 0 ]; then
  echo "Could not populate database with currencies, stopping."
  exit $retVal
fi
python manage.py runserver 0.0.0.0:8000 --settings=api.settings.development
