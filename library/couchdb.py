import requests
import pprint
import time
import json

class CouchDBAccess(object):

    _couchurl = None
    _username = None
    _password = None
    headers = {'Content-Type': 'application/json'}


#########################
#
#  C O U C H   A P I
#
#########################



    def pretty(self, json):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(json)


    def couch_get(self, database, route, params=None):
        auth = None
        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s/%s/%s" % (self._couchurl, database, route)
        print url
        r = requests.get(url, auth=auth, params=params, headers=self.headers)
        return r.json()

    def couch_get2(self, database, route, params=None):
        auth = None
        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s%s/%s" % (self._couchurl, database, route)

        r = requests.get(url, auth=auth, params=params, headers=self.headers)
        return r.json()


    def couch_put(self,route, data=None):
        auth = None
        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s%s" % (self._couchurl, route)

        r = requests.put(url, auth=auth, data=data, headers=self.headers)
        return r.json()

    def couch_put2(self, dbname, route, data=None):
        auth = None
        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s%s/%s" % (self._couchurl, dbname,  route)

        r = requests.put(url, auth=auth, data=json.dumps(data), headers=self.headers)
        return r.json()


    def couch_post(self, config, route, data=None):
        auth = None

        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s%s/%s/%s" % (self._couchurl, database, route)
        if data == None:
            r = requests.post(url, auth=auth, headers=self.headers)
        else:
            r = requests.post(url, auth=auth, data=data, headers=self.headers)
        return r.json()

    def couch_post2(self, database, route, data=None):
        auth = None

        if self._username is not None:
            auth = HTTPBasicAuth(self._username, self._password)
        url = "%s%s/%s" % (self._couchurl, database, route)
        print url
        if data == None:
            r = requests.post(url, auth=auth, headers=self.headers)
        else:
            r = requests.post(url, auth=auth, data=data, headers=self.headers)
        
        return r.json()



    def http_get(self, api_url):
        r = requests.get(api_url)
        json_data = r.json()

        return json_data


    def createCouchDatabase(self, dbname):
        r = requests.get("%s%s" % (self._couchurl, dbname))
        json_data = r.json()
        if 'error' in json_data:
            print "database does not exists, creating one"
            r = requests.put("%s%s" % (self._couchurl, dbname))
            return True
        else:
            print "db %s already created" % dbname
        return False



    def change_rev_limit(self, dbname, rev_limit):
        print "change rev limit to %d" % rev_limit
        r = requests.put("%s%s/_revs_limit" % (self._couchurl, dbname), data=str(rev_limit))
        print r.json()



    def checkAndAddViews(self, dbname, view_data, needsupdate=False):

        r = requests.get("%s%s/%s" % (self._couchurl, dbname, view_data['_id']))
        json_data = r.json()
        if 'error' in json_data:
            print "view %s does not exists, creating one on %s" % (view_data['_id'], dbname)
            r = self.couch_put("%s/%s" % (dbname, view_data['_id']), json.dumps(view_data))
            return True
        else:


            print "view %s already created on %s" % (view_data['_id'], dbname)
        return False


    def getCurrentEpoch(self):
        return int(time.time())


    def getDbCurrentSeq(self, dbname):
        r = requests.get("%s%s/_changes?descending=true&limit=1" % (self._couchurl, dbname))
        json_data = r.json()
        if 'error' in json_data:
            print "error occured"
            return None
        else:
            return json_data['last_seq']


    def getDBchanges(self, dbname, last_seq, limit=100):
        r = requests.get("%s%s/_changes?limit=%d&include_docs=true&since=%s" % (self._couchurl, dbname, limit,  last_seq ))
        json_data = r.json()
        if len(json_data['results']) < 1:
            return [0, []]
        return [ json_data['last_seq'], json_data['results'] ]



    def post_method(self, url, data=None):
        auth = None
        print json.dumps(data)
        r = requests.post(url, auth=auth, data=json.dumps(data), headers=self.headers)
        return r.text



    def update_doc(self, dbname, data):
        temp_doc = self.couch_get2(dbname, data['_id'])
        if '_rev' in temp_doc:
            data['_rev'] = temp_doc['_rev']
        if 'error' in temp_doc:
            print "doc id does not exist yet"
        self.couch_put2(dbname, data['_id'], data)





 






