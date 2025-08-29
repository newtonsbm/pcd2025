FROM python:3-slim AS builder
RUN pip install "pelican[markdown]"
COPY . /app
WORKDIR /app
EXPOSE 8000
RUN pelican ./content 

FROM nginx:1-alpine
COPY --from=builder /app/output /usr/share/nginx/html
