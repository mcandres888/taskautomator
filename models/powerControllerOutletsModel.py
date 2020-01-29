# QueueJobs
import requests
from flask import request
from models.baseModel import *
import os, sys

# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)


class PowerControllerOutletsModel(BaseModel):

    columns = ["id", "pc_id", "outlet_id", "name", "status"]

    columns_type = ["int", "int", "int", "str", "str" ]

    def initialize_table(self):
        super(PowerControllerOutletsModel, self).initialize_table()


    def isOutletAvailable(self, pc_id, outlet_id):
        query_str = "SELECT * FROM %s WHERE pc_id=%d and outlet_id=%d LIMIT 1" % (self.table, int(pc_id), int(outlet_id))
        result = self.db.fetch_query(query_str)
        retval = None
        for x in result:
            retval = self.convertArray(x, self.columns)
        return retval



    def updatePowerControllerStates(self, pc_id, json_data):

        for x in json_data:
            temp = {
                "pc_id" : pc_id,
                "outlet_id" : int(x['id']),
                "name" : x['name'],
                "status" : x['state'],
            }
            res = self.isOutletAvailable(pc_id, int(x['id']))
            if res is None:
                self.create(temp)
            else:
                temp['id'] = res['id']
                self.update(temp)
                

    def tableData(self, requestInfo):
        # request info data
        draw = int(requestInfo.get("draw"))
        start = int(requestInfo.get("start"))
        length = int(requestInfo.get("length"))
        search = requestInfo.get("search[value]")

        tableData = {}

        # get count
        query_str = "SELECT ID FROM %s" % (self.table)


        result = self.db.fetch_query(query_str)
        tableData['recordsFiltered'] = len(result) # must be filtered based on key
        search = '%' + search + '%' 

        query_str = "SELECT * FROM %s WHERE name LIKE '%s' LIMIT %d,%d" % (self.table,search,  start, length) 
        result = self.db.fetch_query(query_str)
        # create the table data
        tableData['recordsTotal'] = len(result)
        # draw must be different from last draw
        tableData['draw'] = draw + 1 # this must be the index / page
        # recreate data
        tableData['data'] = []
        for x in result:

            temp = self.convertArray(x, self.columns)

            if temp['status'] == "OFF":
                actions = "<button onclick=\"location.href='%spowercontrolleroutlets/on/%d';\" type='button' class='btn btn-block btn-success'> Switch ON </button>" % ( request.url_root, temp['id'] )
            else:
                actions = "<button onclick=\"location.href='%spowercontrolleroutlets/off/%d';\" type='button' class='btn btn-block btn-danger'> Switch OFF </button>" % ( request.url_root, temp['id'] )

            tableData['data'].append([
                temp['name'],
                temp['status'],
                actions,
            ])

        return tableData





