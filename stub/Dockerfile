FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80

COPY ./app /app
WORKDIR /app

CMD ["uvicorn", "webservice:app", "--host", "0.0.0.0", "--port", "80"]