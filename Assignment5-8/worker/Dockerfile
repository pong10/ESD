FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN python3 -m pip install --upgrade pip


RUN pip3 install pika
RUN pip3 install flask
RUN pip3 install pysqlite3
RUN pip3 install pydblite

WORKDIR /app
COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
