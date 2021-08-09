FROM python:3

WORKDIR /app

RUN mkdir /entrypoint

COPY ./requirements.txt /app

RUN apt-get install libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt-get install libssl-dev

COPY ./compose/app/wait-for-it.sh /entrypoint
RUN chmod +x /entrypoint/wait-for-it.sh

COPY ./compose/app/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint/entrypoint.sh


ENTRYPOINT ["/entrypoint/entrypoint.sh"]