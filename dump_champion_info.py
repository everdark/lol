#!/usr/bin/env python

import ConfigParser

import crawlertool


def main():
    config = ConfigParser.ConfigParser()
    if len(config.read(["conf.ini"])):
        api_key = config.get("user", "api_key")
        crawlertool.getAllChampionInfo(api_key, region="na", ver="v1.2", outfile="champion_id.json")
    else:
        print "File conf.ini not found. Program aborted."
        exit(1)

if __name__ == "__main__":
    main()
