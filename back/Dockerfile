FROM python:3.12

WORKDIR /

COPY ./requirements.txt /back/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /back/requirements.txt

COPY . /back

CMD [ "python", "-m", "back.main"]
