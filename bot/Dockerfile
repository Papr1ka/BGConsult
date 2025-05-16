FROM python:3.12

WORKDIR /

COPY ./requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY . /bot

CMD [ "python", "-m", "bot.main"]
