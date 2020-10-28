FROM python:3.8

WORKDIR /gifify-src

COPY requirements.txt /gifify-src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY gifify /gifify-src

CMD [ "./gifify/runserver.sh" ]