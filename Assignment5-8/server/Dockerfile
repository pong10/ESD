FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
RUN python3 -m pip install --upgrade pip


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install pika && \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]