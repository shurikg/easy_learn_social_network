FROM python:3-alpine

RUN apk add --no-cache jpeg-dev zlib-dev

RUN apk add --no-cache --virtual .build-deps build-base linux-headers \ 
    && pip3 install pip --upgrade \ 
    && pip3 install <packages list> \ 
    && apk del .build-deps
