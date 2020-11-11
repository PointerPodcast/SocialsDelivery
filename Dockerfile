FROM alpine:latest

WORKDIR /home

RUN apk update 

#Install Python and pip3
RUN apk add --no-cache python3-dev \
    && apk add --no-cache py3-pip


RUN apk add --no-cache \
        libffi-dev \
        libressl-dev \
        musl-dev \
        build-base 

RUN pip3 install urllib3==1.25.11 
RUN apk add --no-cache jpeg-dev zlib-dev
RUN pip3 install APScheduler \
        cryptography \
        facebook-sdk \
        Flask \
        Flask-Cors \
        instabot \
        numpy \
        Pillow \
        oauthlib \
        python-telegram-bot \
        requests \
        tweepy

#Setting timezone to Europe/Rome
RUN apk add tzdata
RUN cp /usr/share/zoneinfo/Europe/Rome /etc/localtime
RUN echo "Europe/Rome" >  /etc/timezone
RUN apk del tzdata

COPY . /home/

RUN chmod +x /home/run.sh
RUN /home/run.sh
ENTRYPOINT sh

