#!/usr/bin/env python

import traceback
import ConfigParser
import requests
import daemon
from elasticsearch import Elasticsearch
import time

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
        return rj
    else:
        return None

def increaseId(match_id, inc=1):
    next_match_id = str(int(match_id) + inc)
    return next_match_id

def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(['/home/pi/lol/conf.ini'])):
        region = "kr"
        api_key = config.get("user", "api_key")
        es_host = config.get("elasticsearch", "host")
        es_port = config.get("elasticsearch", "port")
        es = Elasticsearch(hosts=[{"host": es_host, "port": es_port}])

        try:
            last_updated = es.search("match", "updatetime", size=1, sort="date:desc")["hits"]["hits"]
        except NotFoundError as e: # for brand-new deployment
            match_id = getLastMatch(region, seed_pid="4460427", api_key=api_key)
        else:
            last_match = last_updated[0]["_source"]["matchId"]

        if not len(last_match):
            match_id = getLastMatch(region, seed_pid="4460427", api_key=api_key)
        else:
            match_id = increaseId(last_match)

        while True:
            # crawl the match data
            match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)
            if match_details is not None:
                match_details["_id"] = match_details.pop("matchId") # replace the default es _id
                es.create(index="match", doc_type="updatetime", 
                          body= {"matchId": match_details["_id"], "date": int(time.time())} )
                es.create(index="match", doc_type="details", 
                          body=match_details)
            match_id = increaseId(match_id)    
            time.sleep(1) # to avoid api overshooting (max 500 queries per 10 min)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

def runAsDaemon():
    with daemon.DaemonContext():
        try:
            main()
        except:
            f = open("/home/pi/lol/log", 'w')
            f.write(traceback.format_exc())

if __name__ == "__main__":
    runAsDaemon()



