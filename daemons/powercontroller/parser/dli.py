from parser.baseparser import *

class DLI(BaseParser):



    def get_status_per_row(self, row):
        td = row.findAll('td')

        temp = {}
        temp['id'] = td[0].text
        temp['name'] = td[1].text
        temp['state'] = td[2].text.strip()
        
        return temp
   


    def get_outlets_fromfile(self, filepath):
        contents = self.loadfromhtml(filepath)
        #print contents
        soup = BeautifulSoup(contents, features="lxml")
        table = soup.findAll('table')[5]
        rows = table.findAll('tr')[2:]
        for x in rows:
            data = self.get_status_per_row(x)
            print(data)
     

    



