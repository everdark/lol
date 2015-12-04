#!/usr/bin/env python

import traceback
import ConfigParser
import requests
import daemon
import redis
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

def setRedisConn(host="localhost", port="6379"):
    r = redis.Redis(host=host, port=port, db=0)
    return r

def increaseId(match_id, inc=1):
    next_match_id = str(int(match_id) + inc)
    return next_match_id

def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(['/home/pi/lol/conf.ini'])):
        api_key = config.get("user", "api_key")
        redis_host = config.get("database", "redis_host")
        redis_port = config.get("database", "redis_port")
        redis = setRedisConn(host=redis_host, port=redis_port)
        last_match = redis.lindex("last100", 0)
        if last_match is None: # for brand-new database
            match_id = getLastMatch(region, seed_pid="4460427", api_key=api_key)
        else:
            match_id = increaseId(last_match)
        region = "kr"

        while True:
            # crawl the match data
            match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)

            if match_details is not None:

                # insert match data into redis
                mid = match_details.pop("matchId")
                redis.hmset(mid, match_details)
                
                # update list of last-inserted
                redis.lpush("last100", mid)
                redis.ltrim("last100", 0, 99)

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



