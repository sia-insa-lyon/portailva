#!/usr/bin/env bash

pipenv run python3 manage.py migrate && pipenv run python3 manage.py collectstatic --noinput && pipenv run python3 manage.py runserver 0.0.0.0:8000