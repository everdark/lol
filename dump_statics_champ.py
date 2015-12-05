#!/usr/bin/env python

import json
import ConfigParser

import crawlertools


def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        api_key = config.get("user", "api_key")
        outfile = config.get("static", "champion_id")
        res = crawlertools.getAllChampionInfo(api_key, region="na", ver="v1.2")
        if res is not None:
            with open(outfile, 'w') as f:
                for k, v in res["data"].items():
                    f.write(json.dumps(v) + "\n")
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

if __name__ == "__main__":
    main()
