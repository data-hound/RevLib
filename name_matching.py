'''
import glob
#C:\Users\MY\Desktop\flipkart\flipkart\*.json
a= (glob.glob("C:\\Users\\MY\\Desktop\\flipkart\\flipkart\\.*.json"))


'''
'''
import os
os.listdir("C:\Users\MY\Desktop\flipkart\flipkart\")
'''

'''
for name in os.listdir("."):
    if name.endswith(".txt"):
        print(name)
'''
from difflib import SequenceMatcher
import glob
import os
import json

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
a=[]
a = (os.listdir("/home/deepak/Desktop/flipkart/"))
json_data=open(file_directory).read()

datas = json.loads("out.json)

b= []t
for data in datas:
    for reviews in data:
        b.append(reviews)

for elea in a:
    for eleb in b:
        if similar(a,b)> 0.45
                   print(elea,' ',eleb)
