# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /job_filter_app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN python3 -m pip install --upgrade pip
COPY req.txt .
RUN pip install -r req.txt


COPY . .

#CMD ["python3", "manage.py", "poolbot"]