FROM python:3.6-alpine

RUN apk add --no-cache build-base

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python" "main.py"]
