# QueueJobs
import requests
from flask import request
from models.baseModel import *
import os, sys

# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)


class ServerModel(BaseModel):

    columns = ["id", "type", "name", "location", "ip_address",
               "username", "info", "status" ]

    columns_type = ["int", "str", "str", "str", "str",
                    "str", "str", "str", "str" ]

    def initialize_table(self):
        super(ServerModel, self).initialize_table()

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

            actions = "<button onclick=\"location.href='%sserver/uname/%d';\" type='button' class='btn btn-block btn-primary'> uname </button>" % ( request.url_root, temp['id'] )

            tableData['data'].append([
                temp['name'],
                temp['location'],
                temp['ip_address'],
                temp['info'],
                actions,
            ])

        return tableData





