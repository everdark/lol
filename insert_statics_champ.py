#!/usr/bin/env python

import json
import ConfigParser
import elasticsearch

import dbtools
import crawlertools


def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        api_key = config.get("user", "api_key")
        outfile = config.get("static", "champion_id")
        es_host = "localhost"
        es_port = 9200
        es_index = "statics"
        es_doctype = "champs"
        res = crawlertools.getAllChampionInfo(api_key, region="na", ver="v1.2")
        if res is not None:
            champs = [ v for k, v in res["data"].items() ]
            es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])
            if es.indices.exists(es_index):
                for ch in champs:
                    champ_id = ch.pop("id")
                    es.create(index=es_index, doc_type=es_doctype, id=champ_id, body=ch)
            else:
                print "Index %s does not exist. Do nothing." % es_index
                exit(1)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

if __name__ == "__main__":
    main()



