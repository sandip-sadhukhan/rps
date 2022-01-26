FROM python:3.8

ENV MICRO_SERVICE=/home/app/microservice

RUN mkdir -p $MICRO_SERVICE

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# # install psycopg2 dependencies
# RUN apk update \
#     && apk add --virtual build-deps gcc python3-dev musl-dev \
#     && apk add postgresql-dev gcc python3-dev musl-dev \
#     && apk del build-deps \
#     && apk --no-cache add musl-dev linux-headers g++


RUN apt-get update

# RUN apt-get install python3-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . $MICRO_SERVICE
