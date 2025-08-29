FROM python:3-alpine

COPY . /app

WORKDIR /app

RUN pip install fastapi[standard]

EXPOSE 8000

CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]