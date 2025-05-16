FROM python:3.12

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . ./back
ENV PYTHONPATH=/app

CMD [ "uvicorn", "back.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
