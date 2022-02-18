FROM python:3.10.2-bullseye

EXPOSE 7500

WORKDIR /tg_bot

COPY requirements.txt /tg_bot/
RUN pip install -r /tg_bot/requirements.txt
COPY . /tg_bot/

CMD python3 /tg_bot/app.py
