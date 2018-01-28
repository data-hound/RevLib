import requests
import json as m_json
query = input ( 'Query: ' )
data = { 'q' : query }
headers = ({"x-user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36 FKUA/website/41/website/Desktop"})
json = requests.get ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ,params=data).json()
# json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
for result in results:
    title = result['title']
    url = result['url']   # was URL in the original and that threw a name error exception
    print ( title + '; ' + url )