# QueueJobs
import requests
from flask import request
from models.baseModel import *
import os, sys

# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)


class TaskModel(BaseModel):

    columns = ["id", "type", "date_queued", "date_finished", "input",
               "output", "callback", "status" ]

    columns_type = ["int", "str", "str", "str", "str",
                    "str", "str", "str", "str" ]

    def initialize_table(self):
        super(TaskModel, self).initialize_table()

    def getbytype(self, task_type):
        query_str = "SELECT * FROM %s WHERE type='%s' AND status NOT LIKE 'done'" % (self.table, task_type)
        result = self.db.fetch_query(query_str)
        retval = []
        for x in result:
            temp = self.convertArray(x, self.columns)
            temp['input'] = json.loads(temp['input'])
            retval.append(temp)
        return retval



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

        query_str = "SELECT * FROM %s WHERE type LIKE '%s' ORDER BY id DESC LIMIT %d,%d " % (self.table,search,  start, length) 
        result = self.db.fetch_query(query_str)
        # create the table data
        tableData['recordsTotal'] = len(result)
        # draw must be different from last draw
        tableData['draw'] = draw + 1 # this must be the index / page
        # recreate data
        tableData['data'] = []
        for x in result:

            temp = self.convertArray(x, self.columns)

            actions = "<button onclick=\"location.href='%stasks/delete/%d';\" type='button' class='btn btn-block btn-danger'> Delete </button>" % ( request.url_root, temp['id'] )

            tableData['data'].append([
                temp['id'],
                temp['type'],
                temp['input'],
                temp['date_queued'],
                temp['status'],
            ])

        return tableData





