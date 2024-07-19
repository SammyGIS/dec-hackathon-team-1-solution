FROM Python 3.9:

WORKDIR /app

COPY  requirements.txt ./app/requirements.txt
COPY main.py ./app/main.py

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


CMD ["echo", "python_script"]
