#!/usr/bin/env python

import ConfigParser
import elasticsearch

import dbtools

def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["config/conf.ini"])):
        es_host = config.get("database", "elasticsearch_host")
        es_port = config.get("database", "elasticsearch_port")
        es_index = config.get("database", "elasticsearch_index")
        es_doctype = config.get("database", "elasticsearch_doctype")

        es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])
        if not es.indices.exists(es_index):
            dbtools.initIndexOfMatches(es, index_name=es_index, doc_type=es_doctype)
        else:
            print "Index already exists. Do nothing."
            exit(0)
    else:
       print "File conf.ini not found. Program aborted."
       exit(1)

if __name__ == "__main__":
    main()
