FROM python:3.6

WORKDIR /app
ADD . .

RUN pip install pipenv uwsgi && pipenv install --system --deploy
