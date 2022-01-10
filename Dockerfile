FROM python:3.9-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y 
COPY requirements.txt requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN git clone https://github.com/M-DEVAMARIA/mdownbot.git
RUN mkdir /mdownbot
WORKDIR /mdownbot
COPY start.sh /start.sh
CMD python3 bot.py

CMD python3 bot.py
 






