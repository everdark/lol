#!/usr/bin/env python


import ConfigParser
import requests

config = ConfigParser.ConfigParser()
if not len(config.read(['conf.ini'])):
    print "No config file found. Program aborted."
    exit(1)

api_key = config.get("user", "api_key")
region = "kr"
match_id = "2083727714" # one of Faker's solo-rank match
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

def getAllItems(region, api_key, ver="v1.2"):
    api_server = "https://global.api.pvp.net"
    api_call = "%s/api/lol/static-data/%s/%s/item" % (api_server, region, ver)
    qs = {"api_key": api_key, 
          "locale": "en_US", 
          "itemListData": "all"}
    r = requests.get(api_call, params=qs)
    if r.status_code == 200:
        rj = r.json()
        return rj
    else:
        return None

def getItemInfo(all_items, item_id):
    pass



