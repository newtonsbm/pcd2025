FROM python:3-alpine
RUN pip install rpyc
EXPOSE 18811
RUN mkdir /code
COPY . /code
WORKDIR /code
CMD python rpyc_services_server.py