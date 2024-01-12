FROM python:3.12.1-slim AS requirements-image

ENV PYTHONUNBUFFERED=1

RUN ["pip","install","poetry>=1.7,<1.8","--upgrade"]

RUN ["poetry","self","add","poetry-plugin-export"]

WORKDIR /export

COPY pyproject.toml poetry.lock ./

RUN ["poetry","export","--format","requirements.txt","--output","requirements.txt"]

FROM python:3.12.1-slim AS runtime-image

LABEL description="CYSCOM VIT's leaderboard"

ENV PYTHONUNBUFFERED=1

COPY --from=requirements-image /export/requirements.txt requirements.txt

RUN ["useradd","--create-home","cyscom-docker"]

USER cyscom-docker

RUN ["pip","install","--requirement","requirements.txt"]

WORKDIR /home/cyscom-docker/opensrc-website

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app