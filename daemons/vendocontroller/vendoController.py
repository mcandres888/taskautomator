from daemons.DaemonWorker import *
import time
import requests



class VendoController(DaemonWorkerBase):

    PER_SIGNAL = 5

    def initialize(self):
        print("intialize")


    def send_signal(self, url_array):
        for x in url_array:
            print x
            #r = requests.get(x)
            #print r.text
            time.sleep(0.2)

    # signal data compose of url of on and off endpoint
    # signal_data = ["http://192.168.1.12/00", "http://192.168.1.12/01"]
    def vend(self, signal_data, price):
        signal_count = price / self.PER_SIGNAL
        print("Signal Count %d" % signal_count)
        for x in range(0, signal_count):
            self.send_signal(signal_data)
        print("Signal End")
        return True
 

    def getForVendMachines(self):
        url_str = "%s/api/getforvend" % self.config.API_URL
        r = requests.get(url_str)
        return r.json()

    def closeMachineRequest(self, id):
        url_str = "%s/api/machinerequestclose/%d" %  (self.config.API_URL, id)
        r = requests.get(url_str)
        return r.json()

    def main(self):
        # get all the data that are for vend
        forvend = self.getForVendMachines()
        for x in forvend:
            print("Vending %s with amount %d" % (x['item'], x['srp']))
            price = x['srp']
            signal_data = []
            signal_data.append("%s/%s" % (x['machine_data']['base_url'], 
                                          x['machine_data']['off_endpoint']))
            signal_data.append("%s/%s" % (x['machine_data']['base_url'], 
                                          x['machine_data']['on_endpoint']))
            self.vend(signal_data, price)
            # close this machine request
            self.closeMachineRequest(x['id'])
      
          
    def start(self):
        print("start")
        self.main()
        time.sleep(2)
        # check if there is another machine to vend
        self.main()
        print("end")




