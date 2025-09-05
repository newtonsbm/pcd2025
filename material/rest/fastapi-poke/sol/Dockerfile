FROM python:3.0

WORKDIR /code

COPY . /code/

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
