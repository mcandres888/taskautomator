# base class for controllers
from flask import render_template, request, redirect, jsonify, make_response
import os, sys

# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)

class BaseController(object):
    _app = None
    _config = None
    user_session = None

    def __init__(self, app):
        self._app = app

    def setConfig(self, config):
        self._config = config

    # base data will be the user data
    def getBaseData (self):
        data = {
            "title" : self._app.config['UI_TITLE'],
            "ui_title_1" : self._app.config['UI_ICONTITLE1'],
            "ui_title_2" : self._app.config['UI_ICONTITLE2'],
            "ui_minititle_1" : self._app.config['UI_MINITITLE1'],
            "ui_minititle_2" : self._app.config['UI_MINITITLE2'],

            "username" : self.getUserName(),
            "domain" : request.url_root,
            "nav" : self.getNav()
        }
        return data

    def getUserName(self):
        # must be implemented in the child object
        pass

    def getNav(self):
        # must be implemented in the child object
        pass

    def main(self):
        data = self.getBaseData()
        return render_template('main.html', data=data)
    def test(self):
        print "test"

    def getUserName(self):
        # get username based on user session
        username = self._app.UserModel.getUserNameViaSession(self.user_session)
        return username

    def dashboard(self, user_session):
        self.user_session = user_session
        # based on the user session get base data
        data = self.getBaseData()
        resp = make_response(render_template('main.html', data=data))
        resp.set_cookie('user_session', user_session)
        return resp


    def login(self, isError=False):
        message =  "Sign in to start your session"
        if isError:
            message = "Incorrect email or password"
        data = self.getBaseData()
        data['message'] = message
        return render_template ('login.html', data=data)
