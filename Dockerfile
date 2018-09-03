FROM python:3.6-alpine

RUN apk add --no-cache build-base

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "main.py"]
