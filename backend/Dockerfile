FROM python:3.7-alpine

WORKDIR /backend
COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY ./src /backend
ENV FLASK_APP=api.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
