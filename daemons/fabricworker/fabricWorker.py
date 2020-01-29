from daemons.DaemonWorker import *
import time
import requests
import hashlib
import json
from fabric import Connection


class FabricWorker(DaemonWorkerBase):

    def intialize(self):
        pass


    def send_uname_cmd(self, data):
        # send uname command to serverer
        ip_address = data['serverdata']['ip_address']
        retval = {}
        result = Connection(ip_address).run('uname -s', hide=True)
        msg = "{0.stdout}"
        retval['uname'] = msg.format(result).strip()
        return retval

    def update_info(self, ret, data):
        print (data)
        print (ret)
        # must get it from callback
        url = "%s/%s" % (self.config.API_URL, data['callback'])
        r = requests.post(url, data=json.dumps(ret), headers=self._api_headers)
        print r.json()

    def runbyaction(self, data ):
        retval = None
        if data['action'] == "uname":
            retval = self.send_uname_cmd(data)

        return retval




    def start(self):
        # get all the task from this type
        tasks = self.get_DataFromAPI('tasks/getbytype/fabric')
        retval = None
        for x in tasks:
            print(x)
            # get the input information
            if 'action' in x['input']:
                retval = self.runbyaction(x['input'])


            if retval is not None:
                self.update_info(retval, x)
                retval = None
            # update status
            self.get_DataFromAPI('tasks/update_status/%d/done' % x['id'])


if __name__ == "__main__":
    print("starting main")





