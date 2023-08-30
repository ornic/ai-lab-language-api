FROM python:3

COPY requirements.txt /
COPY gunicorn.conf /
RUN pip install gunicorn --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

RUN  mkdir -p models

#COPY /models/lid.176.bin /models/lid.176.bin
ADD https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin /models/lid.176.bin


COPY server.py /

CMD [ "gunicorn", "-c", "gunicorn.conf", "server:app" ]
