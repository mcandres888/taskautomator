# rabbit library
import pika
import time
import json


def pretty(json):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(json)


def infoLog( data):
    print data

# sample config
# config = {}
# config['amqp'] = "amqp://localhost"
# config['queue'] = "PACK_DEVELOPMENT"

def connectToRabbit(queue, host="amqp://localhost", retry=0):

    if retry > 3:
        infoLog( "Maximum tries already exceeds. returning None.")
        return None
    try:
        # note static to this server only
        params = pika.URLParameters(host)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        # note static to this server only
        channel.queue_declare(queue=queue)
        rabbit = {}
        rabbit['conn'] = connection
        rabbit['chan'] = channel
        return rabbit

    except:
        infoLog("Cant connect to rabbit mq. retrying")
        retry += 1
        return connectToRabbit(queue, host, retry)


def sendToRabbit(rabbit, queue_name,  data):
    rabbit['chan'].basic_publish('',
        routing_key=queue_name,
        body=json.dumps(data))


def sendto_worker(queue, action, params=None, host="amqp://localhost"):
    data = {}
    data['action'] = action
    data['epoch_time'] = int(time.time())
    if params != None: data['params'] = params

    rabbit = connectToRabbit(queue, host)
    if rabbit == None:
        infoLog("Error. Cannot connect to rabbitmq.")
        return

    print "[action sent] > %s" % action
    sendToRabbit(rabbit, queue, data)
    rabbit['conn'].close()



