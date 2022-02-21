FROM python:3.10.2-bullseye


WORKDIR /usr/src/tg_bot

COPY  requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python3 app.py
