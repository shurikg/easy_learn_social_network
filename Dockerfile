FROM python:3-alpine

RUN apk add --no-cache jpeg-dev zlib-dev

RUN apk add --no-cache --virtual .build-deps build-base linux-headers && pip3 install pip --upgrade && pip3 install -r requirements.txt && apk del .build-deps

