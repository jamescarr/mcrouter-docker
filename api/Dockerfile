FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install python-pip -yq

RUN pip install flask 

RUN pip install pymemcache

VOLUME ['/srv/app']

ADD app.py /srv/app/app.py

CMD python /srv/app/app.py

