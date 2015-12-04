#!/usr/bin/env python

import daemon
import traceback

from crawler import *

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



