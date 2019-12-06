#!/usr/bin/env bash

pipenv run python3 manage.py migrate && pipenv run python3 manage.py collectstatic --noinput && pipenv run gunicorn portailva.wsgi -b 0.0.0.0:8000 --log-file -