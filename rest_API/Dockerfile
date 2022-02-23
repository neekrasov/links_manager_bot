FROM python:3.10.2-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/rest_API

COPY requirements.txt /usr/src/rest_API
RUN pip install -r requirements.txt
COPY . /usr/src/rest_API

CMD python manage.py runserver 0.0.0.0:8000