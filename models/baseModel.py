# models class
import uuid
import json
import time
import datetime
import re

class BaseModel(object):
    data = None
    db = None
    config = None
    columns = None
    columns_type = None
    table = None
    app = None

    def __init__(self):
        #self.infoLog( "Initialize model %s" % type(self).__name__)
        self.table = type(self).__name__

    def initialize_table(self):
        query_str = self.create_table_string()
        #self.infoLog("CREATE STRING >> %s " % query_str)
        self.exec_query(query_str)
        pass

    def infoLog(self, data):
        print data

    def setConfig(self, config):
        self.config = config

    def setDB(self, dbInstance):
        self.db = dbInstance

    def setApp(self, app):
        self.app = app

    def tableData(self, requestInfo):
        pass

    def getCSVHeader(self):
        return self.columns

    def getWithHash ( self, uuid):
        query_str = "SELECT * FROM %s WHERE id=%d LIMIT 1" % (self.table, int(uuid))
        print query_str
        result = self.db.fetch_one(query_str)
        # convertArray
        return self.convertArray(result, self.columns)

    def deleteId ( self, uuid):
        query_str = "DELETE FROM %s WHERE id=%d" % (self.table, int(uuid))
        self.db.exec_query(query_str)

    def exec_query ( self, query_str):
        self.db.exec_query(query_str)


    def convertStatus ( self, statid):
        if statid == 0:
            return "Disabled"
        else:
            return "Enabled"
    def fetch_one (self, query_str):
        result = self.db.fetch_one(query_str)
        if result == None:
            return None
        return self.convertArray(result, self.columns)


    def convertArray(self, dataArray, columns):
        x = 0
        data = {}
        if columns == None:
            return data


        for d in dataArray:
            if self.columns_type[x] == "float":
                d = "%.2f" % d
            data[columns[x]] = d
            x += 1
        return data

    def getAllWhere(self, where_str):
        query_str = "SELECT * FROM %s WHERE %s" % (self.table, where_str)
        rows = self.db.fetch_query (query_str)
        rows_json = []
        for x in rows:
            temp = self.convertArray(x, self.columns)
            rows_json.append(temp)
        return rows_json

    def getAll(self):
        query_str = "SELECT * FROM %s" % self.table
        rows = self.db.fetch_query (query_str)
        rows_json = []
        for x in rows:
            temp = self.convertArray(x, self.columns)
            rows_json.append(temp)
        return rows_json

    def getAllExtra(self, data):
        query_str = "SELECT * FROM %s %s" % ( self.table , data )
        rows = self.db.fetch_query (query_str)
        rows_json = []
        for x in rows:
            temp = self.convertArray(x, self.columns)
            rows_json.append(temp)
        return rows_json


    def getAllCSV(self):
        query_str = "SELECT * FROM %s" % self.table
        rows = self.db.fetch_query (query_str)
        rows_json = []
        for x in rows:
            #temp = self.convertArray(x, self.columns)
            rows_json.append(x)
        return rows_json

    def get(self, id):
        query_str = "SELECT * FROM %s WHERE id=%d" % (self.table, int(id))
        row = self.db.fetch_one (query_str)
        if row == None:
            return None
        row_json = self.convertArray(row, self.columns)

        return row_json

    def get_db_id(self, db_id):
        query_str = "SELECT * FROM %s WHERE db_id='%s'" % (self.table, db_id)
        row = self.db.fetch_one (query_str)
        if row == None:
            return None
        row_json = self.convertArray(row, self.columns)

        return row_json



    def update(self, json_data):
        query_str = self.create_update_string(json_data)
        query_str += " WHERE id=%d" % (int(json_data['id']))
        print "query_str!!!!! " , query_str
        self.db.exec_query(query_str)


    def populate_data_from_existing_data(self, json_data, temp):
        # get cols
        c_count = len(self.columns)
        for i in range(0, c_count):
            colType = self.getColType(self.columns_type[i])
            if self.columns[i] in json_data:
                if colType == "int":
                    temp[self.columns[i]] = int(json_data[self.columns[i]])
                else:
                    temp[self.columns[i]] = str(json_data[self.columns[i]])
        return temp
  

    def create_or_update(self, json_data):
        if 'id' in json_data:
            temp = self.get(json_data['id'])
            if temp is not None:
                # populate json_data with old data

                # do not update status
                del json_data['status']

                temp = self.populate_data_from_existing_data(json_data, temp)
                self.update(temp)
                return temp
        self.create(json_data)
        return json_data
         
    def create_or_update_db_id(self, json_data):
        if 'db_id' in json_data:
            temp = self.get_db_id(json_data['db_id'])
            if temp is not None:
                # populate json_data with old data
                temp = self.populate_data_from_existing_data(json_data, temp)
                print temp
                self.update(temp)
                return temp
        self.create(json_data)
        return json_data
         






    def getColType(self, data):
        retval = None
        if data == "int":
            retval = "INTEGER"
        elif data == "str":
            retval = "TEXT"
        elif data == "float":
            retval = "REAL"
        elif data == "timestamp":
            retval = "TEXT"
       
        return retval


    def create_table_string (self):
        query_str = "CREATE TABLE if not exists %s (" % self.table
        # get the values on the column except for id and date_created
        c_count = len(self.columns)
        for i in range(0, c_count):
            colType = self.getColType(self.columns_type[i])
            if self.columns[i] == "id":
                #query_str += "%s %s PRIMARY KEY AUTO_INCREMENT, " % (self.columns[i], colType)
                # sqlite remove auto_increment
                query_str += "%s %s PRIMARY KEY , " % (self.columns[i], colType)
            else :
                query_str += "%s %s, " % (self.columns[i], colType)
        # remove the last comma
        query_str = query_str[:-2]
        query_str += ")"
        return query_str


    def create_update_string (self, json_data):
        query_str = "UPDATE %s SET " % self.table
        # get the values on the column except for id and date_created
        c_count = len(self.columns)
        for i in range(0, c_count):
            if self.columns[i] == "id":
                continue
            if self.columns[i] == "date_created":
                continue
            if self.columns[i] not in json_data:
                continue

            if self.columns_type[i] == "int":
                query_str += "%s=%d, " % (self.columns[i], int(json_data[self.columns[i]]))
            elif self.columns_type[i] == "float":
                query_str += "%s=%.2f, " % (self.columns[i], float(json_data[self.columns[i]]))

            elif self.columns_type[i] == "str":
                query_str += "%s='%s', " % (self.columns[i], self.escape(json_data[self.columns[i]]))
            elif self.columns_type[i] == "date":
                query_str += "%s='%s', " % (self.columns[i], self.escape(json_data[self.columns[i]]))
            elif self.columns_type[i] == "datetime":
                query_str += "%s='%s', " % (self.columns[i], self.escape(json_data[self.columns[i]]))
        # remove the last comma
        query_str = query_str[:-2]
        return query_str

    def escape (self, data):
        data_str = data.replace("'", "\\'")
        #data_str = re.sub(r'(\-|\]|\^|\$|\*|\.|\\|\'|\")',lambda m:{'-':'\-',']':'\]','\\':'\\\\','^':'\^','$':'\$','*':'\*','.':'\.',"'",'\'','"','\"'}[m.group()],data)
        return data_str


    def create(self, json_data):
        query_str = self.create_insert_string(json_data)
        self.exec_query(query_str)


    # this will be based on the self.columns
    def create_insert_string (self, json_data):
        query_str = "INSERT INTO %s ( " % self.table
        # get the values on the column except for id and date_created
        c_count = len(self.columns)
        for x in self.columns:
            if x == "id":
                continue
            if x == "date_created":
                continue

            if x not in json_data:
                continue
            query_str += "%s, " % x

        # remove the last comma
        query_str = query_str[:-2]
        query_str += ") VALUES ( "

        for i in range(0, c_count):
            if self.columns[i] == "id":
                continue
            if self.columns[i] == "date_created":
                continue
            if self.columns[i] not in json_data:
                continue

            if self.columns_type[i] == "int":
                query_str += "%d, " % int(json_data[self.columns[i]])
            elif self.columns_type[i] == "float":
                query_str += "%.2f, " % float(json_data[self.columns[i]])

            elif self.columns_type[i] == "str":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
            elif self.columns_type[i] == "date":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
            elif self.columns_type[i] == "datetime":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
        # remove the last comma
        query_str = query_str[:-2]
        query_str += ")"
        return query_str

    # this will be based on the self.columns
    def create_insert_string_col_type (self, table, json_data, data_col, data_type):
        query_str = "INSERT INTO %s ( " % table
        # get the values on the column except for id and date_created
        c_count = len(data_col)
        for x in data_col:
            if x == "date_created":
                continue

            if x not in json_data:
                continue
            query_str += "%s, " % x

        # remove the last comma
        query_str = query_str[:-2]
        query_str += ") VALUES ( "

        for i in range(0, c_count):

            if data_col[i] == "date_created":
                continue
            if data_col[i] not in json_data:
                continue

            if data_type[i] == "int":
                query_str += "%d, " % int(json_data[data_col[i]])
            elif self.columns_type[i] == "float":
                query_str += "%.2f, " % float(json_data[self.columns[i]])

            elif data_type[i] == "str":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
            elif data_type[i] == "date":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
            elif data_type[i] == "datetime":
                query_str += "'%s', " % self.escape(json_data[self.columns[i]])
        # remove the last comma
        query_str = query_str[:-2]
        query_str += ")"
        return query_str























