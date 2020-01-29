from flask import render_template, request, redirect, jsonify, make_response
from controllers.baseController import *
import os, sys
import random
from datetime import datetime
import json


# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)

from library.adminlte.forms import *


class AdminController(BaseController):

#########################################
#
# N A V I G A T I O N
#
#########################################

    # eventually nav will be different per user type
    def getNav(self):
        domain = request.url_root

        nav = [
            { "href" : "%sdashboard" % domain, "class" : "fa fa-dashboard", "text" : "Dashboard" },
            { "href" : "%stasks" % domain, "class" : "fa fa-exclamation-triangle", "text" : "Tasks" },
            { "href" : "%spowercontroller" % domain, "class" : "fa fa-industry", "text" : "Power Controller Devices" },
            { "href" : "%spowercontrolleroutlets" % domain, "class" : "fa fa-flash", "text" : "Power Controller Outlets" },
            { "href" : "%sserver" % domain, "class" : "fa fa-building-o", "text" : "Server" }
        ]
        return nav

################################
#
#   P A G E S
#
################################


#################
# T A S K S   L I S T
#################


    def tasks(self):
        data = self.getBaseData()
        subData = {
            "titleFirst" : "Task",
            "titleSecond" : "Lists",
            "boxTitle" : "Tasks Table",
            "headers" : ["id", "Type", "Input", "Created","Status"],
            "data_url" : "/tasks/list"
        }

        data['subData'] = subData
        data['tableHtml'] = "table.html"
        return render_template('tableTemplate.html', data=data)

    def tasks_list(self):
        data = self._app.TaskModel.tableData(request.args)
        return jsonify(data)


#################
# POWER CONTROLLER OUTLETS
#################


    def powercontrolleroutlets(self):
        data = self.getBaseData()
        subData = {
            "titleFirst" : "Power Controller",
            "titleSecond" : "Outlets",
            "boxTitle" : "Outlets Table",
            "headers" : ["Name", "Status", "Action"],
            "data_url" : "/powercontrolleroutlets/list"
        }

        data['subData'] = subData
        data['tableHtml'] = "table.html"
        return render_template('tableTemplate.html', data=data)

    def powercontrolleroutlets_list(self):
        data = self._app.PowerControllerOutlets.tableData(request.args)
        return jsonify(data)



    def powercontrolleroutlets_swtich_action(self, id, action):
        outlet = self._app.PowerControllerOutlets.get(id)
        pc = self._app.PowerController.get(outlet['pc_id'])

        # create a task for with action populate for powercontroller
        # type class
        # get power controller information
        temp = self._app.PowerController.get(id)
        input_data = {
            "powercontrollerdata": pc,
            "action" : action,
            "outletid" : outlet['outlet_id'],
            "outletdata" : outlet,
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
        self._app.TaskModel.create(data)






#################
# P O W E R  C O N T R O L L E R
#################

    def powerController(self):
        data = self.getBaseData()
        subData = {
            "titleFirst" : "Power",
            "titleSecond" : "Controller",
            "boxTitle" : "Device Table",
            "headers" : ["Name", "Location", "IP Address", "Status", "Action"],
            "data_url" : "/powercontroller/list"
        }

        header = { 'action' : '', 'method' : 'post', 'enctype' :'multipart/form-data'}
        form_data = [
             {'type' : 'hidden', 'name' : 'actionType', 'value' : 'add'},
             {'type' : 'text', 'name' : 'name', 'label' : 'Name'},
             {'type' : 'text', 'name' : 'location', 'label' : 'Location'},
             {'type' : 'text', 'name' : 'ip_address', 'label' : 'IP Address'},
             {'type' : 'select', 'name' : 'type', 'label' : 'Controller Type', 'options' : [
                {'value' : 'digitalloggers', 'label' : 'Digital Loggers', 'selected' : True} ,
                {'value' : 'webrelay', 'label' : 'Web Relay'}
             ]},
             {'type' : 'text', 'name' : 'username', 'label' : 'Username '},
             {'type' : 'text', 'name' : 'password', 'label' : 'Password'}
        ]

        data['form'] = Forms.createForm(header, form_data, "Create")
        data['form_title'] = "Create Power Controllers"

        data['subData'] = subData
        data['tableHtml'] = "table_withform.html"
        return render_template('tableTemplate.html', data=data)

    def powerController_list(self):
        data = self._app.PowerController.tableData(request.args)
        return jsonify(data)

    def powerController_create(self):
        json_data = request.form
        self._app.PowerController.create(json_data)
        return self.powerController()





#################
# S E R V E R
#################

    def server(self):
        data = self.getBaseData()
        subData = {
            "titleFirst" : "Server",
            "titleSecond" : "Machines",
            "boxTitle" : "Server Table",
            "headers" : ["Name", "Location", "IP Address", "Info", "Action"],
            "data_url" : "/server/list"
        }

        header = { 'action' : '', 'method' : 'post', 'enctype' :'multipart/form-data'}
        form_data = [
             {'type' : 'hidden', 'name' : 'actionType', 'value' : 'add'},
             {'type' : 'text', 'name' : 'name', 'label' : 'Name'},
             {'type' : 'text', 'name' : 'location', 'label' : 'Location'},
             {'type' : 'text', 'name' : 'ip_address', 'label' : 'IP Address'},
             {'type' : 'text', 'name' : 'username', 'label' : 'Username'},
             {'type' : 'select', 'name' : 'type', 'label' : 'Server Type', 'options' : [
                {'value' : 'samba', 'label' : 'Samba', 'selected' : True} ,
                {'value' : 'web', 'label' : 'Web App'}
             ]}
        ]

        data['form'] = Forms.createForm(header, form_data, "Create")
        data['form_title'] = "Create Server"

        data['subData'] = subData
        data['tableHtml'] = "table_withform.html"
        return render_template('tableTemplate.html', data=data)

    def server_list(self):
        data = self._app.Server.tableData(request.args)
        return jsonify(data)

    def server_create(self):
        json_data = request.form
        self._app.Server.create(json_data)
        return self.server()



