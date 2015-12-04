FROM python:2.7

RUN apt-get -y update && apt-get install -y python-pip \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/* \
&&  pip install python-daemon requests elasticsearch



