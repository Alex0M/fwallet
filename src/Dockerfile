FROM python:3.6.2

COPY . /usr/app

WORKDIR /usr/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["run.py"]