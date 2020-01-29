# Controller Factory
from controllers.adminController import *
 

class ControllerFactory:
    @staticmethod
    def load(app, modelType):
        print "loading controller %s" % modelType
        prototype = None
        if modelType == 'adminController':
            prototype =  AdminController(app)


        




        return prototype
        



