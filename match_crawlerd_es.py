#!/usr/bin/env python

import os
import time
import logging
from logging.handlers import RotatingFileHandler
import traceback
import daemon
import ConfigParser
import requests
import elasticsearch

import dbtools

def getLogger(log_path, level=logging.INFO):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(level)
    fhandler = RotatingFileHandler(log_path, maxBytes=1024*1024*10, backupCount=5)
    fhandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
    logger.addHandler(fhandler)
    return logger

def getLastMatch(region, seed_pid, api_key, ver="v1.3"):
    api_server = "https://%s.api.pvp.net" % region
    api_call = "%s/api/lol/%s/%s/game/by-summoner/%s/recent?" % (api_server, region, ver, seed_pid)
    qs = {"api_key": api_key}
    r = requests.get(api_call, params=qs)
    if r.status_code == 200:
        rj = r.json()
        last_match = rj["games"][0]["gameId"]
        return last_match
    else:
        return None

def getMatchDetails(region, match_id, api_key, ver="v2.2"):
    api_server = "https://%s.api.pvp.net" % region
    api_call = "%s/api/lol/%s/%s/match/%s" % (api_server, region, ver, match_id)
    qs = {"api_key": api_key,
          "includeTimeline": "true"}
    r = requests.get(api_call, params=qs)
    if r.status_code == 200:
        rj = r.json()
        return r.status_code, rj
    else:
        return r.status_code, None

def increaseId(match_id, inc=1):
    next_match_id = str(int(match_id) + inc)
    return next_match_id

def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        api_key = config.get("user", "api_key")
        region = config.get("user", "region")
        log_path = config.get("logging", "log_path")
        logger = getLogger(log_path, level=logging.INFO)
        es_host = config.get("database", "elasticsearch_host")
        es_port = config.get("database", "elasticsearch_port")
        es_index = config.get("database", "elasticsearch_index")
        es_doctype = config.get("database", "elasticsearch_doctype")

        es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])
        if not es.indices.exists(es_index):
            logger.info("Elastic index name %s not found. Create it." % es_index)
            dbtools.initElasticIndices(es, index_name=es_index, doc_type=es_doctype)
            match_id = getLastMatch(region, seed_pid="22071749", api_key=api_key)
            logger.info("Set matchId starting point to %s." % match_id)
        else:
            last_updated = es.search(es_index, es_doctype, _source=False, size=1, sort="insertTime:desc")["hits"]["hits"]
            if not len(last_updated):
                match_id = getLastMatch(region, seed_pid="22071749", api_key=api_key)
                logger.info("Document not found. Set matchId starting point to %s." % match_id)
            else:
                last_match = last_updated[0]["_id"]
                match_id = increaseId(last_match)
                logger.info("Latest matchId found to be %s. Start at %s" % (last_match, match_id))

        while True:
            status_code, match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)
            logger.info("Crawled possible matchId %s | status code resolved: %s" % (match_id, status_code))
            if match_details is not None:
                mid = match_details.pop("matchId") # replace the default auto-index field _id
                match_details["insertTime"] = int(time.time() * 1000)
                es.create(es_index, es_doctype, id=mid, body=match_details)
            match_id = increaseId(match_id)    
            time.sleep(1) # to avoid api overshooting (max 500 queries per 10 min)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

def runAsDaemon():
    with daemon.DaemonContext(working_directory='.'):
        try:
            main()
        except:
            f = open("debug.log", 'w')
            f.write(traceback.format_exc())
            f.close()

if __name__ == "__main__":
    runAsDaemon()



