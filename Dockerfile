FROM python:latest
WORKDIR /usr/src/bot
COPY . /usr/src/bot
# RUN apt upgrade & apt update
RUN pip install --pre -r /usr/src/bot/requirements.txt
