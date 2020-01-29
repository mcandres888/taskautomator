# models class
import requests
import flask_login
from flask import render_template, request, redirect, jsonify
import uuid
import json
import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.baseModel import *


class FlaskUser(flask_login.UserMixin):
    # flask_login functions
    id = None
    name = None
    def __init__(self, id, active=True):
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True



class User(BaseModel):
    # columns product info
    columns = ["id", "username", "password", "date_created", "session", "expiration"]
    columns_type = ["int", "str", "str", "str", "str", "int"]
    id = None

    def getUserNameViaSession(self, user_session):
        query_str = "SELECT * FROM %s WHERE session='%s'" % (self.table, user_session)
        result = self.db.fetch_one(query_str)
        if result == None:
            return "NA"
        return result[1]
 
    def user_loader(self, id):
        print "LOADING USER"
        # get user information based on session id
        print "session id >> ", id 
        query_str = "SELECT * FROM %s WHERE session='%s'" % (self.table, id)
        result = self.db.fetch_one(query_str)
        if result == None:
            return None
        return FlaskUser(id)

    def create_flaskUser(self, username):
        # create uuid for the session
        session_id =  str(uuid.uuid4())
        query_str = "UPDATE %s SET session='%s' WHERE username='%s'" % (self.table, session_id, username) 
        result = self.db.exec_query(query_str)
        user = FlaskUser(session_id)
        return user
 

    def initialize_table(self):
        super(User, self).initialize_table()
        # check if admin user is create if not create one
        print "check if admin is available"
        if self.isUserAvailable('admin') == True:
            print "admin is not available. create one"
            self.registerUser({"username" : "admin" , "password" : "admin"})




    def isUserAvailable(self, username):
        query_str = "SELECT * FROM %s WHERE username='%s'" % (self.table, username)
        result = self.db.fetch_one(query_str)
        if result == None:
            self.infoLog( "username still available")
            return True
        else:
            self.infoLog( "username  unavailable")
            return False

    def tableData(self, requestInfo):
        # request info data
        draw = int(requestInfo.get("draw"))
        start = int(requestInfo.get("start"))
        length = int(requestInfo.get("length"))

        url = '%s/_design/data/_view/userList' % (self._db)
        result = self.couchdb.get(url)
        # create the table data
        tableData = {}
        # draw must be different from last draw
        tableData['draw'] = draw + 1 # this must be the index / page
        tableData['recordsTotal'] = len(result['rows'])
        tableData['recordsFiltered'] = len(result['rows']) # must be filtered based on key
        # recreate data
        tableData['data'] = []
        for x in result['rows']:

            temp = self.convertArray(x, self.columns)

            date_created =  datetime.datetime.fromtimestamp(
                    temp['date_created']).strftime('%Y-%m-%d %H:%M:%S')
            actions = "<a href='%s/profile/%s'><button type='button' class='btn btn-block btn-success'> View </button></a>" % ( request.url_root, x['id'] )
            tableData['data'].append([
                temp['id'],
                temp['username'],
                date_created,
                actions
            ])

        return tableData


    def loadUser( self, username):
        print "load user %s" % username

        query_str = "SELECT * FROM %s WHERE username='%s'" % (self.table, username)
        result = self.db.fetch_one(query_str)
        print "waaa"
        if result == None:
            self.infoLog( "username  unavailable")
            return False
        else:

            temp = self.convertArray(result, self.columns)

            self.id = temp['username']
            self.data = temp
            self.is_authenticated = True
            return True
        return False



    def isPasswordOK( self, username, password):

        query_str = "SELECT * FROM %s WHERE username='%s'" % (self.table, username)
        result = self.db.fetch_one(query_str)

        print result
        if result == None:
            self.infoLog( "username  unavailable")
            return False
        else:
            # check user data
            temp = self.convertArray(result, self.columns)

            self.id = temp['username']
            self.data = temp
            self.is_active = True

            if check_password_hash(temp['password'], password):
                self.infoLog("password ok")
                return True
            else:
                self.infoLog("incorrect password")
        return False


    def registerUser(self, json_data):
        print json_data
        query_str = "INSERT INTO %s (username, password ) VALUES ('%s', '%s' )" % (self.table, json_data['username'], generate_password_hash(json_data['password']))

        self.db.exec_query(query_str)
        return self.data

    def create(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
