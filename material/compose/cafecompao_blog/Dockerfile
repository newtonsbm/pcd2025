FROM python:3-slim
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN apt-get update 
RUN apt-get install -y git
RUN pip install pelican[markdown] git+https://github.com/arulrajnet/attila.git@master
