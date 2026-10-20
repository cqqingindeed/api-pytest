FROM python:latest
MAINTAINER sheng.chen1992@gmail.com

RUN mkdir /automation

COPY . /automation

WORKDIR /automation

RUN pip install -r