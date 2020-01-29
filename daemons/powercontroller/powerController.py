from daemons.DaemonWorker import *
import time
import requests
import bs4
import hashlib
import json
from bs4 import BeautifulSoup




class DLIParser():

    def get_status_per_row(self, row):
        td = row.findAll('td')

        temp = {}
        temp['id'] = td[0].text
        temp['name'] = td[1].text
        temp['state'] = td[2].text.strip()

        return temp

    def get_outlet_status(self, contents):
        soup = BeautifulSoup(contents, features="lxml")
        table = soup.findAll('table')[5]
        rows = table.findAll('tr')[2:]
        temp = []
        for x in rows:
            data = self.get_status_per_row(x)
            print(data)
            temp.append(data)
        return temp


class PowerController(DaemonWorkerBase):
    _username = "admin"
    _password = "br3w3d888"
    _session = None
    _url = None
    _log = False
    _headers = { "Accept-Encoding" : "gzip, deflate" ,
                 "Cache-Control" : "max-age=0",
                 "Content-Type" : "application/x-www-form-urlencoded",
                 "DNT" : "1",
                 "Upgrade-Insecure-Requests" : "1",
                 "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
               }

    def initialize(self):
        self.dliparser = DLIParser()
        pass


    def gethashpassword(self,username, password, challenge):
        temp = "%s%s%s%s" % (challenge, username, password, challenge)
        result = hashlib.md5(temp.encode()).hexdigest()
        return result

    def login(self, url=None, username=None , password=None ):
        if url is None:
            url = self._url
        if username is None:
            username = self._username
        if password is None:
            password = self._password

        r = requests.get(url)
        #self.infoLog(r.text)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        challenge = soup.select('input[name="Challenge"]')[0].get('value')
        hashpassword = self.gethashpassword(username, password, challenge)
        session = requests.Session()
        temp = {"Username": username , "Password": hashpassword }
        resp = session.request('POST', "%s/login.tgi" % url, data=temp, headers=self._headers)
        resp = session.request('GET', "%s/index.htm" % url)
        self._session = session
        return session


    def logout(self):
        url = "%s/logout" % self._url
        r = requests.get(url)
        #print(r.text)
         

    def switch(self, action, outlet, session=None):
        if session is None:
            session = self._session
        resp = session.request('GET', "%s/outlet?%d=%s" % (self._url, outlet, action ))
        print(resp.text)

    
    def populate(self, data, session=None):
        # goto index.htm then parse the data / this will only be acceptable in digital logger
        if session is None:
            session = self._session
        resp = session.request('GET', "%s/index.htm" % (self._url))
        outlets = self.dliparser.get_outlet_status(resp.text)
        print outlets
        url = "%s/powercontrolleroutlets/add/%d" % (self.config.API_URL, data['powercontrollerdata']['id'])
        r = requests.post(url, data=json.dumps(outlets), headers=self._api_headers)
        print r.json()
    


    def runbyaction(self, data):
        # set local information
        self._username = data['powercontrollerdata']['username']
        self._password = data['powercontrollerdata']['password']
        self._url = "http://%s" % data['powercontrollerdata']['ip_address']
        self.login()
        if data['action'] == "populate":
            self.populate(data)

        elif data['action'] == "switchon":
            self.switch("ON", int(data['outletid']) )
            self.populate(data)

        elif data['action'] == "switchoff":
            self.switch("OFF", int(data['outletid']) )
            self.populate(data)

        self.logout()


    def start(self):
        # get all the task from this type
        tasks = self.get_DataFromAPI('tasks/getbytype/powercontroller')
        for x in tasks:
            print(x)
            # get the input information
            if 'action' in x['input']:
                self.runbyaction(x['input'])
       
            # update status       
            self.get_DataFromAPI('tasks/update_status/%d/done' % x['id'])





if __name__ == "__main__":
    print("starting main")
    pc = PowerController("http://192.168.2.6")
    pc.login()
    pc.switch("ON", 8)
    pc.logout()


