
import time
import logger
from logging.handlers import (RotatingFileHandler, TimedRotatingFileHandler)
import requests
import json

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
    fhandler = TimedRotatingFileHandler(log_path, when='H', interval=1, backupCount=24*7)
    logger.addHandler(fhandler)
    return logger

def getSummonerIdByName(region, api_key, names, ver='v1.4', delay=None):
    api_server = "https://kr.api.pvp.net"
    api_call = "%s/api/lol/%s/%s/summoner/by-name/%s" % (api_server, region, ver, names)
    qs = {"api_key": api_key,
          "locale": "en_US",
          "itemListData": "all"}
    r = requests.get(api_call, params=qs)
    if delay is not None:
        time.sleep(delay)
    if r.status_code == 200:
        rj = r.json()
        for s in rj:
            id = rj.get(s).get("id")
        return id
    else:
        return None

def getLastMatchByPid(region, api_key, pid, ver="v1.3", delay=None):
    api_server = "https://%s.api.pvp.net" % region
    api_call = "%s/api/lol/%s/%s/game/by-summoner/%s/recent?" % (api_server, region, ver, pid)
    qs = {"api_key": api_key}
    r = requests.get(api_call, params=qs)
    if delay is not None:
        time.sleep(delay)
    if r.status_code == 200:
        rj = r.json()
        last_game = rj["games"][0]
        create_date, last_match = last_game["createDate"], last_game["gameId"]
        return create_date, last_match
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

def getAllChampionInfo(api_key, region="na", ver="v1.2", outfile="champion_id.json"):
    api_server = "https://global.api.pvp.net" 
    api_call = "%s/api/lol/static-data/%s/%s/champion" % (api_server, region, ver)
    qs = {"api_key": api_key}
    r = requests.get(api_call, params=qs)
    if r.status_code == 200:
        rj = r.json()
        with open(outfile, 'w') as f:
            for k, v in rj["data"].items():
                f.write(json.dumps(v) + "\n")
    else:
        return None

def increaseId(match_id, inc=1):
    next_match_id = str(int(match_id) + inc)
    return next_match_id




