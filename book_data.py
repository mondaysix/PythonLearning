import requests
import re
from bs4 import BeautifulSoup
import json
base_url = "https://book.douban.com/"
xinshu_url = "latest?icn=index-latestbook-all"
subject_url = "https://book.douban.com/subject/";

response = requests.get(base_url+xinshu_url)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text,"html.parser")
def getXinshu():
    xinshu = {}
    for k in soup.find_all('a', class_='', href=re.compile(subject_url)):
        xinshu[k.string] = k['href']
    return xinshu
def setXinshuJson(fileName='xinshu.json'):
    with open(fileName,'w') as json_file:
        json_file.write(json.dumps(getXinshu()))
setXinshuJson()
# print(response.text)
# print('a'=='\u0061')
# print('\u2027')
# with open("xinshu.html",'w',encoding='utf-8') as f:
#     f.write(response.text)
