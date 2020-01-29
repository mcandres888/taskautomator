import requests
import time
import json
import sys, os
import pprint
from datetime import datetime, date, timedelta as td

ZDAEMON = "zdaemon"
PYTHON = "python"

# daemon runner codes

def runDaemon( daemon_class, action):
    # create command string
    app_str = "DaemonRun.py %s" % daemon_class
    worker_inst = "%s.%d" % (daemon_class, 0)
    command_str = "%s -d -p '%s %s' " % (ZDAEMON, PYTHON , app_str)
    command_str += " -s 'pids/%s.sock' -t 'logs/%s.log'" % (worker_inst, worker_inst)
    command_str += " %s &" % action

    print "command_str  "  , command_str
    os.system(command_str)


class DaemonWorkerBase():
    config = None
    headers = {'Content-Type': 'application/json'}
    data_id = 0
    _api_headers = {"Content-Type" : "application/json"}
    
    def __init__(self, config ):
        self.config = config
    def initialize(self):
        pass

    def set_data_id(self, _data_id):
        self.data_id = _data_id

    def pretty(self, json):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(json)

    def infoLog(self, data):
        print(data)

    def start(self):
        # must be implemented on parent
        pass

    def get_DataFromAPI(self, route):
        url = "%s/%s" % (self.config.API_URL, route)
        r = requests.get(url)
        return r.json()


