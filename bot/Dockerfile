FROM python:3.12

WORKDIR /bot

COPY ./requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY . /bot/app

CMD [ "python", "app/main.py"]
