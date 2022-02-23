FROM python:3.10.2-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/rest_API

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python manage.py migrate