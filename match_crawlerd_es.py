#!/usr/bin/env python

import os
import time
import logging
import traceback
import daemon
import ConfigParser
import requests
import elasticsearch

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
    if len(config.read(['conf.ini'])):
        logging.basicConfig(filename='crawld.log',level=logging.INFO, format='[%(asctime)s] %(message)s')
        region = "kr"
        api_key = config.get("user", "api_key")
        es_host = config.get("elasticsearch", "host")
        es_port = config.get("elasticsearch", "port")
        es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": es_port}])

        if not es.indices.exists("match"):
            settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                    },
                "mappings": {
                    "timeinfo": {
                        "properties": {
                            "matchId" : {
                                "type":  "string",
                                "index": "not_analyzed"
                                },
                            "insertTime": {
                                "type":   "date",
                                "format": "epoch_second"
                                },
                            "createTime": {
                                "type":   "date",
                                "format": "epoch_second"
                                }
                            }
                        }
                    }
                }
            es.indices.create(index="match", body=settings)

        last_updated = es.search("match", "timeinfo", size=1, sort="insertTime:desc")["hits"]["hits"]
        if not len(last_updated):
            match_id = getLastMatch(region, seed_pid="4460427", api_key=api_key)
        else:
            last_match = last_updated[0]["_source"]["matchId"]
            match_id = increaseId(last_match)

        while True:
            # crawl the match data
            status_code, match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)
            logging.info("crawled possible matchId %s | status code resolved: %s" % (match_id, status_code))
            if match_details is not None:
                mid = match_details.pop("matchId") # replace the default es _id
                es.create("match", "timeinfo", body={
                    "matchId": mid, 
                    "insertTime": int(time.time()), 
                    "createTime": match_details["matchCreation"] / 1000} )
                es.create("match", "details", id=mid, body=match_details)
            match_id = increaseId(match_id)    
            time.sleep(1) # to avoid api overshooting (max 500 queries per 10 min)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

def runAsDaemon():
    with daemon.DaemonContext(working_directory="."):
        try:
            main()
        except:
            f = open("debug.log", 'w')
            f.write(traceback.format_exc())

if __name__ == "__main__":
    runAsDaemon()



