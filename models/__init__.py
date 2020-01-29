from models.userModel import *
from models.taskModel import *
from models.powerControllerModel import *
from models.powerControllerOutletsModel import *
from models.serverModel import *

dbInstance = None
class ModelFactory:
    @staticmethod
    def setDatabase(db):
        global dbInstance
        if dbInstance == None:
            print "dbInstance not yet initialized"
            dbInstance = db
        else:
            print "dbInstance already created"

    @staticmethod
    def load(app, modelType, config=None):
        if config is None:
            config = app.config

        global dbInstance
        print "loadin model %s " % modelType
        if dbInstance == None:
            raise Exception("initialize ModelFactory first")

        prototype = None
        if modelType == "User":
            prototype = User()

        elif modelType == "Task":
            prototype = TaskModel()

        elif modelType == "PowerController":
            prototype = PowerControllerModel()

        elif modelType == "PowerControllerOutlets":
            prototype = PowerControllerOutletsModel()

        elif modelType == "Server":
            prototype = ServerModel()

        if prototype == None:
            raise Exception("Prototype Not Available")

        prototype.setDB(dbInstance)
        prototype.setConfig(config)
        prototype.setApp(app)
	prototype.initialize_table()
        return prototype






