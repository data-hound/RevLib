import requests
from bs4 import BeautifulSoup 
url = 'https://pricebaba.com/mobile/pricelist/top-mobile-phones?page=7'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
data = requests.get(url, headers = headers).content
soup = BeautifulSoup(data, "html.parser")
container = soup.find("div", id = "productsCnt")
#tables = container.find_all("table")
print(container)
