FROM python:3.6

#ENV FLASK_APP goalkeeper
ENV FLASK_ENV development
ENV PYTHONPATH = "$PYTHONPATH:/app"
ENV PYTHONDONTWRITEBYTECODE = 1

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

#RUN apt-get update && apt-get install -y netcat

#CMD ./startup.sh
CMD ./wait-for-postgres.sh \
    --host=Goalkeeper-db \
    --port=5432 \
    -s -t 0 -- \
    ./startup.sh
