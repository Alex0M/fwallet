FROM python:alpine

WORKDIR /backend
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
		gcc \
		musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
	&& pip install -r requirements.txt \
	&& apk del .build-deps

COPY ./src /backend
ENV FLASK_APP=api.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
