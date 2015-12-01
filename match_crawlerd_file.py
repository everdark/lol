#!/usr/bin/env python

import time
import json
import daemon
import traceback
import subprocess
import ConfigParser
import elasticsearch

import dbtools
import crawlertools


def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        api_key = config.get("user", "api_key")
        region = config.get("user", "region")
        log_path = config.get("logging", "log_path")
        dump_path = config.get("dumping", "dump_path")
        logger = getLogger(log_path, level=logging.INFO)
        dumper = getDumper(dump_path, level=logging.INFO)

        last_line = subprocess.check_output(["tail", "-n1", dump_path])
        if last_line == '':
            # cold-start
            logger.info("No previous dumped file found. Do cold-start.")
            seed_players = config.get("seed", "player")
            if not len(seed_players):
                logger.error("No seed player names in config file. Cold-start failed.")
                exit(1)
            seed_pids = [ getSummonerIdByName(region, api_key, p, delay=1) 
                          for p in config.get("seed", "player").split(',')]
            valid_pids = [ p for p in seed_pids if p is not None ]
            if not len(valid_pids):
                logger.error("No available data for given seed player names. Cold-start failed.")
                exit(1)
            match_info_from_seeds = [ getLastMatchByPid(region, api_key, pid, delay=1) 
                                      for pid in valid_pids ]
            latest_match = max([m for m in match_info_from_seeds if m is not None], 
                               key=lambda x:x[0])[1]
            logger.info("Set matchId starting point to %s." % latest_match)
        else:
            # resume the previous crawling job
            last_match = json.loads(last_line)["matchId"]
            match_id = str(last_match + 1)
            logger.info("Previous dumped file found. Set matchId continue at %s." % match_id)

        while True:
            status_code, match_details = getMatchDetails(region=region, api_key=api_key, match_id=match_id)
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



