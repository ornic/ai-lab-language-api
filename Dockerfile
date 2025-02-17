FROM python:3-slim

RUN apt-get update \
    && apt-get -y install git build-essential libprotobuf-dev protobuf-compiler

COPY requirements.txt /
COPY gunicorn.conf /
RUN pip install -r requirements.txt --no-cache-dir

RUN  mkdir -p models

#COPY /models/lid.176.bin /models/lid.176.bin
ADD https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin /models/lid.176.bin


COPY *.py /

CMD [ "gunicorn", "-c", "gunicorn.conf", "server:app" ]
