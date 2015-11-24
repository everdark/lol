FROM ubuntu:14.04

RUN apt-get -y update && apt-get install -y \ 
        wget \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

RUN cd /opt \
&&  wget https://download.elastic.co/kibana/kibana/kibana-4.2.1-linux-x64.tar.gz \
&&  tar -zxvf kibana-4.2.1-linux-x64.tar.gz \
&&  rm -f /opt/kibana-4.2.1-linux-x64.tar.gz \
&&  useradd -M kibana \
&&  echo "kibana:kibana" | chpasswd \
&&  adduser kibana sudo \ 
&&  chown -R kibana:kibana /opt/kibana-4.2.1-linux-x64

COPY config /opt/kibana-4.2.1-linux-x64/config

USER kibana

CMD ["/opt/kibana-4.2.1-linux-x64/bin/kibana"]


