# this will run the daemon worker class based on the passed action
import sys
from config import *

config = ProductionConfig()

#from daemons.rabbitmqlistener import *
#r = RabbitMQListener(config)


prototype = None

worker_class = None
worker_id = 0
if len(sys.argv) > 1:
    worker_class = sys.argv[1]
if len(sys.argv) > 2:
    worker_id = sys.argv[2]

print( "worker class ", worker_class)
if worker_class == "vendocontroller":
    from daemons.vendoController import *
    prototype = VendoController(config)    


elif worker_class == "rabbitmqlistener":
    from daemons.rabbitmqlistener import *
    prototype = RabbitMQListener(config)    

elif worker_class == "powercontroller":
    from daemons.powercontroller import *
    prototype = PowerController(config)    

elif worker_class == "fabric":
    from daemons.fabricworker import *
    prototype = FabricWorker(config)    


else:
    print( "worker class not available")
    quit()

prototype.set_data_id(worker_id)
prototype.initialize()
prototype.start()

