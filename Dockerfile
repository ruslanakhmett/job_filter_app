FROM python:3.8.3-alpine

WORKDIR /job_filter_app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m pip install --upgrade pip

COPY req.txt .

RUN pip install -r req.txt

RUN addgroup -S app && adduser -S app -G app

RUN chown -R app:app /job_filter_app

USER app

COPY . .