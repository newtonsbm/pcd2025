FROM python:3-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pelican content -o output -s publishconf.py

FROM nginx:1-alpine
COPY --from=builder /app/output/ /usr/share/nginx/html

