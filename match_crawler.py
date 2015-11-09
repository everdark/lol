#!/usr/bin/env python


import ConfigParser
import requests
import daemon

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

def main():
    while True:
        pass

def runAsDaemon():
    with daemon.DaemonContext():
        main()

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    if len(config.read(['conf.ini'])):
        runAsDaemon()
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)
