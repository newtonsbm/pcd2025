FROM python:3-alpine
RUN pip install rpyc
RUN mkdir /code
COPY . /code
WORKDIR /code
CMD python rpyc_services_client.py