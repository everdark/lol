#!/usr/bin/env python

import time
import json
import subprocess
import ConfigParser

from crawlertools import *


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
            last_match = getLatestMatchBySummonerNames(region, 
                    seed_players.split(','), api_key, delay=1)
            match_id = increaseId(last_match)
            logger.info("Set matchId starting point to %s." % match_id)
        else:
            # resume the previous crawling job
            last_match = json.loads(last_line)["matchId"]
            match_id = increaseId(last_match)
            logger.info("Previous dumped file found. Set matchId continue at %s." % match_id)

        cnt = 0
        while True:
            status_code, match_details = getMatchDetails(region=region, api_key=api_key, match_id=match_id)
            logger.info("Crawled possible matchId %s | status code resolved: %s" % (match_id, status_code))
            if match_details is not None:
                match_details["insertTime"] = int(time.time() * 1000)
                dumper.info(json.dumps(match_details))
            match_id = increaseId(match_id)

            cnt += 1
            if cnt >= 10000: 
                # jump to a recent game, if any
                seed_players = config.get("seed", "player")
                latest_match = getLatestMatchBySummonerNames(region, 
                        seed_players.split(','), api_key, delay=1)
                if int(latest_match) > int(match_id):
                    match_id = latest_match
                cnt = 0

            time.sleep(1) # to avoid api overshooting (max 500 queries per 10 min)
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

if __name__ == "__main__":
    main()



