FROM python:3.7-alpine

WORKDIR /fwallet
COPY requirements.txt .

RUN apk add --update --no-cache mariadb-connector-c-dev \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install -r requirements.txt \
	&& apk del .build-deps

COPY ./src /fwallet
ENV FLASK_APP=run.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
