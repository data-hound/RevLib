import requests
from bs4 import BeautifulSoup
import re
import json

def crawl_specifications(query):
    url = 'https://www.gsmarena.com/res.php3?sSearch=' + re.sub(" ", "+", query)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get(url, headers = headers).content
    container = BeautifulSoup(data, "html.parser")
    print(container)
    return container.find("div", id = "review-body").a['href']

    

def scrape_specifications(urlin):
    url = 'https://www.gsmarena.com/' + urlin
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get(url, headers = headers).content
    container = BeautifulSoup(data, "html.parser")

    name = container.find("h1", class_ = "specs-phone-name-title")
    if name is None:
        brand = urlin; model = ""
    else:
        name = name.text
        brand = re.sub(r"^(.*?) .*$", r"\1", name)
        model = re.sub(r"^(.+?) (.*)$", r"\2", name)
    params = {
        "maxbudget" : -1,
        "brand" : brand,
        "model" : model,
        "dualsim" : -1,
        "4g" : -1,
        "3g" : -1,
        "display": -1,
        "rearcamera" : -1,
        "frontcamera" : -1,
        "cpu" : -1,
        "chipset" : -1,
        "ram" : -1,
        "internal" : -1,
        "fingerprint" : 0,
        "os" : -1
    }

    tables = container.find_all("table")
    for table in tables:
        title = table.tr.th.text
        if title == "Network":
            _3g = table.find("td", class_ = "nfo", attrs = {"data-spec" : "net3g"})
            if _3g is not None : params['3g'] = 1
            _4g = table.find("td", class_ = "nfo", attrs = {"data-spec" : "net4g"})
            if _4g is not None : params['4g'] = 1
        
        elif title == "Body":
            sim = table.find("td", class_ = "nfo", attrs = {"data-spec" : "sim"})        
            if 'dual' in sim.text: params['dualsim'] = 1
        
        elif title == "Display":
            display = table.find("td", class_ = "nfo", attrs = {"data-spec" : "displaysize"})        
            params['display'] = display.text

        elif title == "Platform":
            os = table.find("td", class_ = "nfo", attrs = {"data-spec" : "os"})        
            chip = table.find("td", class_ = "nfo", attrs = {"data-spec" : "chipset"})        
            cpu = table.find("td", class_ = "nfo", attrs = {"data-spec" : "cpu"})        
            params['os'] = os.text
            params['chipset'] = chip.text
            params['cpu'] = cpu.text

        elif title == "Memory":
            internal = table.find("td", class_ = "nfo", attrs = {"data-spec" : "internalmemory"})        
            params['internal'] = re.sub(r"^(?i).*?([0-9/]+ GB).*$", r"\1", internal.text)
            params['ram'] = re.sub(r"(?i).*?(\d\d? GB RAM).*$", r"\1", internal.text)

        elif title == "Camera":
            fcam = table.find("td", class_ = "nfo", attrs = {"data-spec" : "cameraprimary"})        
            scam = table.find("td", class_ = "nfo", attrs = {"data-spec" : "camerasecondary"})        
            params['rearcamera'] = fcam.text        
            params['frontcamera'] = scam.text        

        elif title == "Features":
            sens = table.find("td", class_ = "nfo", attrs = {"data-spec" : "sensors"})        
            if "fingerprint" in sens.text.lower(): params['fingerprint'] = 1

        elif title == "Battery":
            batt = table.find("td", class_ = "nfo", attrs = {"data-spec" : "batdescription1"})        
            params['battery'] = batt.text
    return params


import csv
output = []
def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    counter = 0
    for line in reader:
        counter += 1
        print(counter)
        q = line['PHONE NAME']
        link = crawl_specifications(q)
        param = scrape_specifications(link)
        param['minbudget'] = line['MIN PRICE']
        out = {param['brand'] + ' ' + param['model'] : param}
        output.append(out)
        

with open("d_day.csv") as f_obj:
    csv_dict_reader(f_obj)

with open("out.json", 'w') as f:
    json.dump(output, f, indent=4)