#!/usr/bin/env python

import ConfigParser
import elasticsearch

import dbtools

def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        es_host = "localhost"
        es_port = 9200
        es_index = "statics"
        es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])
        if not es.indices.exists(es_index):
            dbtools.initIndexOfStatics(es, index_name=es_index, doc_champ="champ")
        else:
            print "Index already exists. Do nothing."
            exit(0)
    else:
       print "File conf.ini not found. Program aborted."
       exit(1)

if __name__ == "__main__":
    main()
