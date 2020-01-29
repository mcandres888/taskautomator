import mysql.connector
import sqlite3

class BaseSQL():
    def __init__(self):
        pass
    def reconnect(self):
        self.connect()

    def disconnect(self):
        self.close()

    def close(self):
        self.db.close()

    def fetch_query (self, query_str):
        self.reconnect()
        self.cur.execute(query_str)
        rows = self.cur.fetchall()
        self.close()
        return rows

    def fetch_one (self, query_str):
        self.reconnect()
        self.cur.execute(query_str)
        data = self.cur.fetchone()
        self.close()
        return data

    def exec_query(self, query_string):
        self.connect()
        cursor = self.db.cursor()
        print query_string
        cursor.execute(query_string)
        self.db.commit()
        self.close()


    def getLastInsertedId ( self ):
        return self.cur.lastrowid




class SqliteLib(BaseSQL):
    cur = None
    cnx = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.connect()

    def connect(self):
        self.db = sqlite3.connect(self.filepath)
        self.cnx = self.db
        self.cur = self.db.cursor()
        return self.db

    def test(self):
        query_string = "CREATE TABLE if not exists users(id INTEGER PRIMARY KEY, name TEXT,"
        query_string += "phone TEXT, email TEXT unique, password TEXT)"
        self.exec_query(query_string)

    def testinsert(self):
        query_string = "INSERT INTO users(name, phone, email, password) "
        query_string += "VALUES ('andres', '2323', 'test@tes.com', 'password' ) "
        self.exec_query(query_string)



class MySqlLib(BaseSQL):



    cur = None
    cnx = None
    user = None
    password = None
    host = None
    database = None
    port = None

    def __init__(self, user, password, database=None, host='localhost', port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.connect()

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user,
                              password=self.password,
                              host=self.host,
                              port=self.port,
                              database=self.database)
        self.db = self.cnx
        self.cur = self.cnx.cursor()
        return self.db

    def test(self):
        query_string = "CREATE TABLE if not exists users(id int PRIMARY KEY, name varchar(50),"
        query_string += "phone varchar(50), email varchar(50), password varchar(100))"
        self.exec_query(query_string)

    def testinsert(self):
        query_string = "INSERT INTO users(name, phone, email, password) "
        query_string += "VALUES ('andres', '2323', 'test@tes.com', 'password' ) "
        self.exec_query(query_string)




class DBFactory:

    @staticmethod
    def load(app, dbtype):
        prototype = None
        if dbtype == 'sqlite':
            prototype = SqliteLib(app.config['SQL_FILE'])
        elif dbtype == 'mysql':
            user  = app.config['DBUSER']
            password  = app.config['DBPASS']
            database  = app.config['DBNAME']
            host  = app.config['DBHOST']
            port  = app.config['DBPORT']
            prototype = MySqlLib(user, password, database, host, port)
        else:
            print 'DB type Not available'

        return prototype
