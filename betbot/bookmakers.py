import os
import json

# import bs4

# frombs4 import BeautifulSoup
from betbot.utils import Printer as p


def build_data():
    with open("data/book.html", "r") as f:
        return f.read()
def load_data(k=None):
    try:
        html = ''
        if not os.path.exists('data/bookmakers.json'):
            html = build_data()
        # soup = bs4.BeautifulSoup(html,'lxml')
        # tables = [table for table in soup.findAll("table")]
        tables = []
        b = {}
        for tab in tables:
            for row in tab.findAll("tr")[1:]:
                cells = [cell.text for cell in row.findAll("td")]
                cells.append(row.findAll("a")[0].attrs.get("href"))
                region,key,name,website = cells
                b[key]={
                    "name"    : name,
                    "region"  : region,
                    "key"     : key,
                    "website" : website}
        with open('data/bookeepers.json','w') as bk:
            bk.write(json.dumps(b))
        return b if not k else b[k.lower()]
    except Exception as ex:
        p.exc(ex)
        return None
def save_data(bookeepers:dict):
    try:
        new_data = json.load(bookeepers)
        if os.path.exists('/data/bookeepers.json'):
            os.rename('/data/bookeepers.json','/data/bookeepers.backup')
        with open('/data/bookeepers.json','w') as file:
            file.write(json.dumps(new_data))
        return True
    except Exception as ex:
        p.exc(ex)
        return False
class Bookeeper:
    def __int__(self, key=None):
        try:
            if key:
                data = load_data(key)
                self.key     = data['key']
                self.name    = data['name']
                self.region  = data['region']
                self.website = data['website']
            return self
        except Exception as ex:
            p.exc(ex)
            return None

if __name__ == '__main__':
    # load_data()
    pass