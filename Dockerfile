FROM python:3.7

EXPOSE 8000

RUN apt update && apt install -y git curl build-essential libreadline-dev zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev libffi-dev libmagic-dev

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /app

RUN pip install -U pip && pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install

# Then copy the rest of the app
COPY . /app

ENV DATABASE_URL ''
ENV DJANGO_SETTINGS_MODULE portailva.settings
ENV WSGI_APP portailva.wsgi
ENV APP_DEBUG False
ENV MAILGUN_API_KEY ''
ENV DEFAULT_FROM_EMAIL 'no-reply@example.com'
ENV SITE_URL 'http://portail.example.com'
ENV API_URL 'http://portail.example.com/api'
ENV SECRET_KEY '%8r$1anftcza)6)uth+ij(2o)si0)l^8o4=t!7^c_0_sz%1gkz'

VOLUME /app/staticfiles
VOLUME /app/mediafiles

RUN chmod +x /app/bash/run-prod.sh
CMD /app/bash/run-prod.sh