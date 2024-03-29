FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm /app/requirements.txt

EXPOSE 8080

COPY ./src /app/src
RUN chmod +x /app/src
CMD [ "python3", "-m", "src.api" ]
