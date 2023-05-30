import os
import json
from bs4 import BeautifulSoup

def build_data():
    with open("data/book.html", "r") as f:
        return f.read()

def main():
    html = ''
    if not os.path.exists('data/bookmakers.json'):
        html = build_data()

    soup = BeautifulSoup(html,'lxml')
    tables = [table for table in soup.findAll("table")]

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

if __name__ == '__main__':
    main()