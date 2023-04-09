FROM python:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm /app/requirements.txt

COPY ./src /app/src
RUN chmod +x /app/src
