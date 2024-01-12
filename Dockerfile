FROM python:3.12.1-slim

LABEL description="CYSCOM VIT's leaderboard"

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN ["pip","install","-r","requirements.txt"]

RUN useradd --create-home cyscom-docker

WORKDIR /home/cyscom-docker/opensrc-website

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app