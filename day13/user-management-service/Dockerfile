FROM python:3.10-slim-buster

LABEL maintainer="saurav.samantray@gmail.com"
WORKDIR /user-management-service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "server.py"]