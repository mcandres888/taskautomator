from daemons.DaemonWorker import *
import time
import requests
import bs4
import hashlib
import json
from bs4 import BeautifulSoup


class SSBServer(DaemonWorderBase):
    def initialize(self):
        pass

    def start(self):
        print("start")


