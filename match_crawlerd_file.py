#!/usr/bin/env python

import os
import time
import json
import logging
from logging.handlers import (RotatingFileHandler, TimedRotatingFileHandler)
import traceback
import daemon
import ConfigParser
import requests
import elasticsearch

import dbtools

def getLogger(log_path, level=logging.INFO):
    logger = logging.getLogger("Rotating Logger")
    logger.setLevel(level)
    fhandler = RotatingFileHandler(log_path, maxBytes=1024*1024*10, backupCount=5)
    fhandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
    logger.addHandler(fhandler)
    return logger

def getDumper(log_path, level=logging.INFO):
    logger = logging.getLogger("Rotating Dumpper")
    logger.setLevel(level)
    fhandler = TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=7)
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
        dumper = getDumper("testdumps", level=logging.INFO)

        match_id = getLastMatch(region, seed_pid="22071749", api_key=api_key)
        logger.info("Set matchId starting point to %s." % match_id)

        while True:
            status_code, match_details = getMatchDetails(region=region, match_id=match_id, api_key=api_key)
            logger.info("Crawled possible matchId %s | status code resolved: %s" % (match_id, status_code))
            if match_details is not None:
                match_details["insertTime"] = int(time.time() * 1000)
                dumper.info(json.dumps(match_details))
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



