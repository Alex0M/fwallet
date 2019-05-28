FROM python:3.7.3

COPY . /usr/app
WORKDIR /usr/app

ENV FLASK_APP=run.py

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
