import requests

api_key = "5c03763b-2119-446c-a699-787d2e248283"                                                         
region = "kr"
summoner_names_list = ['hide on bush', 'dopa', 'SKT T1 Scout']
#get summoner id by summoner name
summonerId_list = getSummonerIdList(region, api_key, summoner_names_list)
#get summoner's recent match info by summoner id
recent_match_info = getRecentMatchInfoList(region, api_key, summonerId_list)
#get most recent match
print "recentMatch=",getMostRecentMatchId(recent_match_info)

def getSummonerId(region, api_key, summonerNames):
    api_server = "https://kr.api.pvp.net" 
    api_call = "%s/api/lol/%s/v1.4/summoner/by-name/%s" % (api_server, region, summonerNames)
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
        
def getRecentMatchInfo(region, api_key, summonerId):
    api_server = "https://kr.api.pvp.net" 
    api_call = "%s/api/lol/%s/v1.3/game/by-summoner/%s/recent" % (api_server, region, summonerId)
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
    for s,t in enumerate(recentMatch):
        if(s==0):
            break
        else:
            if(recentMatch[s].get('createDate') > recentMatch[s-1].get('createDate')):
                most_recent = s
            else:
                pass   
    return recentMatch[most_recent].get('gameId')
