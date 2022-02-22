FROM python:3.10.2-bullseye

WORKDIR /usr/src/tg_bot

COPY  ./tg_bot/requirements.txt .
RUN pip install -r requirements.txt
COPY /tg_bot/ .

CMD python3 app.py
