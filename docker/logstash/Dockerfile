FROM baseimg

RUN wget -O /opt/logstash.zip \
        https://download.elastic.co/logstash/logstash/logstash-2.0.0.zip \
&&  cd /opt \
&&  unzip /opt/logstash.zip \
&&  rm -rf /opt/logstash.zip \
&&  mkdir /opt/logstash-2.0.0/config \
&&  useradd -M logstash \
&&  echo "logstash:logstash" | chpasswd \
&&  adduser logstash sudo \ 
&&  chown -R logstash:logstash /opt/logstash-2.0.0

COPY config /opt/logstash-2.0.0/config
COPY entrypoint_create_index.sh /opt/logstash-2.0.0/entrypoint.sh

USER logstash

WORKDIR /opt/logstash-2.0.0



