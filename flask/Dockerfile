FROM python:3

RUN pip install --upgrade pip

WORKDIR /docker-flask-test

ADD . /docker-flask-test

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]