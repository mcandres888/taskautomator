import os, sys
import requests
import json

# get config data
# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)

from config import *

CONFIG = DevelopmentConfig()
print CONFIG.API_URL


# network node must be unique
machines = [
  { "name" : "Washer_1", "network_node" : 1, "machine_type" : "washer", "machine_size": "small", "sc_type" : "SC20", "base_url" : "http://192.168.1.12/8000", "on_endpoint" : "00", "off_endpoint" : "01"},
  { "name" : "Washer_2", "network_node" : 2, "machine_type" : "washer", "machine_size": "small", "sc_type" : "SC20", "base_url" : "http://192.168.1.12", "on_endpoint" : "03", "off_endpoint" : "04"},
  { "name" : "Washer_3", "network_node" : 3, "machine_type" : "washer", "machine_size": "small", "sc_type" : "SC20", "base_url" : "http://192.168.1.12", "on_endpoint" : "05", "off_endpoint" : "06"},
]

print machines
headers = {"Content-Type" : "Application/json"}

_url = "%s/laundromachine/add" % CONFIG.API_URL
for x in machines:
    res = requests.post(_url, data=json.dumps(x), headers=headers)
    print res.text









