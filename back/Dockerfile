FROM python:3.12

WORKDIR /back

COPY ./requirements.txt /back/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /back/requirements.txt

COPY . /back/app

CMD [ "python", "app/main.py"]
