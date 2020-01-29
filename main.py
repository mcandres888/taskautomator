#!/usr/bin/python
import random, os
from flask import Flask, jsonify, request, redirect, Response, url_for
import logging
from flask import make_response
import sys 
import flask_login
from logging.handlers import RotatingFileHandler
import json
import uuid
from daemons.DaemonWorker import runDaemon

from controllers import *
from models import *
from library.dbfactory import *
import jinja2
from datetime import datetime


# flask initialization
app = Flask(__name__)
app.config.from_object("config.ProductionConfig")
#app.config.from_object("config.DevelopmentConfig")


# add the jinja template folders
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['templates', 'views',
                                 'library/adminlte/templates']),
    ])
app.jinja_loader = my_loader


# added socketio
async_mode = "threading"
import socketio
sio = socketio.Server(logger=True, async_mode=async_mode)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

# load login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# intialize controllers
app.admin = ControllerFactory.load(app, 'adminController')



# intialize database
app.db = DBFactory.load(app, 'sqlite')


##############################
#
#  M O D E L S
#
##############################
# initialize models
ModelFactory.setDatabase(app.db)
app.UserModel = ModelFactory.load(app, "User")
app.TaskModel = ModelFactory.load(app, "Task")
app.PowerController = ModelFactory.load(app, "PowerController")
app.PowerControllerOutlets = ModelFactory.load(app, "PowerControllerOutlets")
app.Server = ModelFactory.load(app, "Server")



##############################
#
#  R O U T E S
#
##############################
#@login_manager.request_loader
def load_user(request):
    cookie = request.cookies.get('user_session')
    print 'load_user', cookie
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    print request.method
    if request.method == 'GET':
        return app.admin.login()
    email = request.form['email']
    password = request.form['password']
    if app.UserModel.isPasswordOK(email, password):
        user = app.UserModel.create_flaskUser(email)
        print user.id
        flask_login.login_user(user)
        return app.admin.dashboard(user.id)
        #return redirect(url_for('dashboard'))
    return app.admin.login( True)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return app.admin.login()

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ',  flask_login.current_user.id


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/login')

@login_manager.user_loader
def user_loader(userid):
    print 'load_user', userid
    return app.UserModel.user_loader(userid)

# routes
@app.route('/')
@flask_login.login_required
def index ():
    return app.admin.dashboard( flask_login.current_user.id)

@app.route('/dashboard')
@flask_login.login_required
def dashboard ():
    user_session = request.cookies.get('user_session')
    return app.admin.dashboard(user_session)


# routes
@app.route('/test')
def test ():
    test = { "status" : "ok"}
    return jsonify(test)





##################################
#
# P A G E S    R O U T E S
#
##################################
###################################################
# T A S K S
###################################################

@app.route('/tasks', methods=['POST', 'GET'])
@flask_login.login_required
def tasks():
    if request.method == 'GET':
        return app.admin.tasks()
    return redirect("/tasks")

@app.route('/tasks/list')
def tasks_list():
    return app.admin.tasks_list()


@app.route('/tasks/getbytype/<task_type>')
def tasks_getbytype(task_type):
    return jsonify(app.TaskModel.getbytype(task_type))


@app.route('/tasks/update_status/<task_id>/<status>', methods=['GET'])
def tasks_update_status(task_id, status):
    task = {
        "id" : task_id, 
        "status" : status
    }
    app.TaskModel.update(task)
     
    return jsonify({"status" : "ok"})


###################################################
# P O W E R  C O N T R O L L E R
###################################################

@app.route('/powercontroller', methods=['POST', 'GET'])
@flask_login.login_required
def powercontroller():
    if request.method == 'GET':
        return app.admin.powerController()
    app.admin.powerController_create()
    return redirect("/powercontroller")

@app.route('/powercontroller/list')
def powercontroller_list():
    return app.admin.powerController_list()

@app.route('/powercontroller/populate/<id>', methods=['GET'])
@flask_login.login_required
def powercontroller_populate(id):
     
    # create a task for with action populate for powercontroller
    # type class
    # get power controller information
    temp = app.PowerController.get(id)
    input_data = {
        "powercontrollerdata": temp,
        "action" : "populate"
    }
    data = {
      "type" : "powercontroller",
      "date_queued" : str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")),
      "date_finished" : "",
      "input" : json.dumps(input_data),
      "output" : "", 
      "callback" : "",
      "status" : "on queue"
    }
    print(data)
    app.TaskModel.create(data)
    runDaemon("powercontroller", "start")
    return redirect("/powercontroller")


###################################################
# P O W E R  C O N T R O L L E R  O U T L E T S
###################################################

@app.route('/powercontrolleroutlets', methods=['POST', 'GET'])
@flask_login.login_required
def powercontrolleroutlets():
    if request.method == 'GET':
        return app.admin.powercontrolleroutlets()
    return redirect("/powercontrolleroutlets")

@app.route('/powercontrolleroutlets/list')
def powercontrolleroutlets_list():
    return app.admin.powercontrolleroutlets_list()

@app.route('/powercontrolleroutlets/add/<pc_id>', methods=['POST'])
def powercontrolleroutlets_add(pc_id):
    json_data = request.json
    if json_data is None:
        return jsonify({"status": "error", "error" : "No json data"})
    # pc id is the power controller id
    # this will recieved all the outlets data
    app.PowerControllerOutlets.updatePowerControllerStates(pc_id, json_data)
    retval = { "status": "ok"}
    return jsonify(retval)

@app.route('/powercontrolleroutlets/on/<id>', methods=['GET'])
@flask_login.login_required
def powercontrolleroutlets_on(id):
    app.admin.powercontrolleroutlets_swtich_action(id, "switchon")
    runDaemon("powercontroller", "start")
    return redirect("/powercontrolleroutlets")


@app.route('/powercontrolleroutlets/off/<id>', methods=['GET'])
@flask_login.login_required
def powercontrolleroutlets_off(id):
    app.admin.powercontrolleroutlets_swtich_action(id, "switchoff")
    runDaemon("powercontroller", "start")
    return redirect("/powercontrolleroutlets")


###################################################
# S E R V E R 
###################################################

@app.route('/server', methods=['POST', 'GET'])
@flask_login.login_required
def server():
    if request.method == 'GET':
        return app.admin.server()
    app.admin.server_create()
    return redirect("/server")

@app.route('/server/list')
def server_list():
    return app.admin.server_list()


@app.route('/server/uname/<id>', methods=['GET'])
@flask_login.login_required
def server_uname(id):
     
    # create a task for with action populate for powercontroller
    # type class
    # get power controller information
    temp = app.Server.get(id)
    input_data = {
        "serverdata": temp,
        "action" : "uname"
    }
    data = {
      "type" : "fabric",
      "date_queued" : str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")),
      "date_finished" : "",
      "input" : json.dumps(input_data),
      "output" : "", 
      "callback" : "server/uname/update/%d" % int(id),
      "status" : "on queue"
    }
    print(data)
    app.TaskModel.create(data)
    runDaemon("fabric", "start")
    return redirect("/server")



@app.route('/server/uname/update/<id>', methods=['POST'])
def server_uname_update(id):
    json_data = request.json
    print json_data
    temp = {
        "id" : id, 
        "info" : json.dumps(json_data)
    }
    print temp
    app.Server.update(temp)
    return jsonify({"status" : "ok"})





# PRODUCTION
port = app.config['APP_PORT']
if __name__ == "__main__":
    if len(sys.argv) == 2:
        port = sys.argv[1]
    print "Running app at port ", port
    handler = RotatingFileHandler('logs/Chloroxv3.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    #app.run(host='0.0.0.0', port=int(port), threaded=True, debug=True, ssl_context='adhoc')
    #app.run(host='0.0.0.0', port=int(port), threaded=True, debug=True)
    app.run(host='0.0.0.0', port=int(port), threaded=True, debug=False)





