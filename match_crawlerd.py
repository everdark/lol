#!/usr/bin/env python

import ConfigParser
import requests
import daemon
import redis
import time

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

def setRedisConn(host="localhost", port="6379"):
    r = redis.Redis(host=host, port=port, db=0)
    return r

def main():
    while True:
        match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)
        if match_details is not None:
            mid = match_details.pop("matchId")
            redis.hmset(mid, match_details)
        time.sleep(1)

def runAsDaemon():
    with daemon.DaemonContext():
        main()

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    if len(config.read(['conf.ini'])):
        api_key = config.get("user", "api_key")
        region = "kr"
        redis_host = config.get("redis", "host")
        redis_port = config.get("redis", "port")
        redis = setRedisConn(host=redis_host, port=redis_port)
        runAsDaemon()
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)



