FROM baseimg

RUN wget -O /opt/elasticsearch.zip \
        https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.0.0/elasticsearch-2.0.0.zip \
&&  cd /opt \
&&  unzip /opt/elasticsearch.zip \
&&  rm -rf /opt/elasticsearch.zip \
&&  useradd -M elastic \
&&  echo "elastic:elastic" | chpasswd \
&&  adduser elastic sudo \ 
&&  chown -R elastic:elastic /opt/elasticsearch-2.0.0 \
&&  mkdir /elastic_data \
&&  chown -R elastic:elastic /elastic_data

COPY config /opt/elasticsearch-2.0.0/config

USER elastic

EXPOSE 9200 9300

CMD ["/opt/elasticsearch-2.0.0/bin/elasticsearch"]



