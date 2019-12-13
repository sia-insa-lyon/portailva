#!/usr/bin/env bash

pipenv run python3 manage.py migrate && pipenv run python3 manage.py collectstatic --noinput && pipenv run uwsgi --module=portailva.wsgi:application --http=0.0.0.0:8000 --threads=4 --processes=1