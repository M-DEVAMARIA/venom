FROM python:3.8-slim-buster
WORKDIR /mdownbot
COPY requirements.txt requirements.txt
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

COPY . .

CMD python3 bot.py
