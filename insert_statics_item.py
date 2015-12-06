#!/usr/bin/env python

import json
import ConfigParser
import elasticsearch

import dbtools
import crawlertools


def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["config/conf.ini"])):
        api_key = config.get("user", "api_key")
        outfile = config.get("static", "item")
        es_host = "localhost"
        es_port = 9200
        es_index = "statics"
        es_doctype = "items"
        res = crawlertools.getAllItemInfo(api_key, region="na", ver="v1.2")
        if res is not None:
            items = [ v for k, v in res["data"].items() ]
            es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])
            if es.indices.exists(es_index):
                for i in items:
                    item_id = i.pop("id")
                    es.create(index=es_index, doc_type=es_doctype, id=item_id, body=i)
            else:
                print "Index %s does not exist. Do nothing." % es_index
                exit(1)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

if __name__ == "__main__":
    main()



