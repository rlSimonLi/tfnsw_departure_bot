FROM python

RUN mkdir /var/bot

WORKDIR /var/bot

ADD requirements.txt ./

RUN pip install -r requirements.txt

ADD ./bot.py ./
ADD ./env.py ./
ADD ./cogs/* ./cogs/
ADD ./lib/* ./lib/

CMD [ "python", "-u", "./bot.py" ]
