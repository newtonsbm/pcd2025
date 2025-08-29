FROM python:3-slim
COPY . /app 
WORKDIR /app
EXPOSE 8000
RUN pip install "pelican[markdown]"
CMD pelican -r -l -b 0.0.0.0 -p 8000 