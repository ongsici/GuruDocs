FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev


COPY requirements.txt requirements.txt

RUN pip install -U pip && \
    pip install -r requirements.txt 

COPY ./nltk_data /root/nltk_data
COPY ./api/api_data_models.py /app/api/api_data_models.py
COPY ./api/llm_fastapi.py /app/api/llm_fastapi.py
COPY ./api/llm_utils.py /app/api/llm_utils.py
COPY ./docs /app/docs
COPY main.py /app/main.py

WORKDIR /app

CMD python main.py