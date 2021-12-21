FROM python:3.9.5-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL 'postgresql://admin:admin@172.17.0.1:5432/flask_app'
ENV FLASK_APP 'interview.py'

COPY requirements.txt /app/requirements.txt

RUN apt-get update && pip install --upgrade pip && \
    apt-get -y install libpq-dev gcc && \
    pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python", "interview.py"]
