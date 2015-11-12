#!/usr/bin/env python

import ConfigParser
import requests

config = ConfigParser.ConfigParser()
if not len(config.read(['conf.ini'])):
    print "No config file found. Program aborted."
    exit(1)

def getSummonerId(region, api_key, summonerNames, ver='v1.4'):
    api_server = "https://kr.api.pvp.net" 
    api_call = "%s/api/lol/%s/%s/summoner/by-name/%s" % (api_server, region, ver, summonerNames)
    qs = {"api_key": api_key,                                                                           
          "locale": "en_US",                                                                              
          "itemListData": "all"} 
    r = requests.get(api_call, params=qs) 
    if r.status_code == 200:
        rj = r.json()
        for s in rj:
            id = rj.get(s).get('id')
        return id
    else:
        return None
        
def getRecentMatchInfo(region, api_key, summonerId, ver='v1.3'):
    api_server = "https://kr.api.pvp.net" 
    api_call = "%s/api/lol/%s/%s/game/by-summoner/%s/recent" % (api_server, region, ver, summonerId)
    qs = {"api_key": api_key,                                                                           
          "locale": "en_US",                                                                              
          "itemListData": "all"} 
    r = requests.get(api_call, params=qs) 
    if r.status_code == 200:
        rj = r.json()
        match_id_dict = dict(gameId = rj.get('games')[0].get('gameId'), createDate = rj.get('games')[0].get('createDate'))
        return match_id_dict
    else:
        return None
        
#need error handle if summonerName is invalid
def getSummonerIdList(region, api_key, summonerNamesList):
    summoner_id_list =[]
    for s,t in enumerate(summonerNamesList):
        summoner_id_list.append (getSummonerId(region, api_key, summonerNamesList[s]))
    return summoner_id_list

#need error handle
def getRecentMatchInfoList(region, api_key, summonerIdList):
    match_info_list =[]
    for s,t in enumerate(summonerIdList):
        match_info_list.append (getRecentMatchInfo(region, api_key, summonerIdList[s]))
    return match_info_list

def getMostRecentMatchId(recentMatchIdList):
    most_recent = 0
    for s,t in enumerate(recentMatchIdList):
        if(s==0):
            break
        else:
            if(recentMatchIdList[s].get('createDate') > recentMatchIdList[s-1].get('createDate')):
                most_recent = s
            else:
                pass   
    return recentMatchIdList[most_recent].get('gameId')

# test
def main(summonerNameList):
    api_key = config.get("user", "api_key")
    region = "kr"
    summonerId_list = getSummonerIdList(region, api_key, summonerNameList) #get summoner id by summoner name
    recent_match_info = getRecentMatchInfoList(region, api_key, summonerId_list) #get recent match info by summoner id
    return getMostRecentMatchId(recent_match_info)

summoner_names_list = ['hide on bush', 'dopa', 'SKT T1 Scout']
print main(summoner_names_list)
