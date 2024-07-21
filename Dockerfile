FROM python:3.9

WORKDIR /app

COPY  ./requirements.txt ./app/requirements.txt
COPY main.py ./app/main.py
COPY .env/ .env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["echo", "main.py"]
