FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install python-pip python-dev -yq

RUN pip install -r requirements.txt 

VOLUME ['/srv/app']

ADD app.py /srv/app/app.py
ADD run.sh /srv/app/run.sh

CMD /srv/app/run.sh


