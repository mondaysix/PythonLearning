import requests
import re
from bs4 import BeautifulSoup
import json
from openpyxl.workbook import Workbook
# base_url = "https://book.douban.com/"
# xinshu_url = "latest?icn=index-latestbook-all"
# subject_url = "https://book.douban.com/subject/";
#
# response = requests.get(base_url+xinshu_url)
# response.encoding = response.apparent_encoding
# soup = BeautifulSoup(response.text,"html.parser")
# def getXinshu():
#     xinshu = {}
#     for k in soup.find_all('a', class_='', href=re.compile(subject_url)):
#         xinshu[k.string] = k['href']
#     return xinshu
# def setXinshuJson(fileName='xinshu.json'):
#     with open(fileName,'w') as json_file:
#         json_file.write(json.dumps(getXinshu()))
# setXinshuJson()

# print(response.text)
# print('a'=='\u0061')
# print('\u2027')
# with open("xinshu.html",'w',encoding='utf-8') as f:
#     f.write(response.text)
#图书标签的特定主题的数据
#比如：https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6
#https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=20&type=T
tag_url = "https://book.douban.com/tag/"
def bookTag(tag):
    book_list = []
    request_tag = requests.get(tag_url+tag+"?start=10&type=T")
    # print(request_tag.text)
    request_tag.encoding = request_tag.apparent_encoding
    soup_tag = BeautifulSoup(request_tag.text,"html.parser")
    lists = soup_tag.find("ul",class_="subject-list")
    for lis in lists.find_all('li',class_="subject-item"):
       div_info = lis.find_all('div')[1]
       a_info = div_info.find("a")
       book_title = a_info.get("title")
       book_href = a_info.get("href")
       pub_info = div_info.find("div",class_="pub").string.strip()
       pub_desc = pub_info.split("/")
       try:
           author_info = "作者/译者: " + '/'.join(pub_desc[0:-3])
       except:
           author_info="作者/译者：暂无"
       try:
            publisher="出版社/出版日期: " + '/'.join(pub_desc[-3:-1])
       except:
            publisher="出版社: 暂无"
       try:
           prices = '' .join(pub_desc[-1])
       except:
            prices = "售价:暂无"
       try:
           rating = div_info.find("span",class_='rating_nums').string
           pub_nums = div_info.find("span",class_='pl').string.strip()[1:][:-4]
       except Exception as e:
           rating = '0.0'
       book_list.append([book_title,author_info,rating,pub_nums,publisher])
    return book_list
    # with open("biaoqian.html",'w',encoding='utf-8') as f:
    #     f.write(res.text)
def print_booklists_excel(book_list,book_tag):
    wb = Workbook(write_only=True)
    ws = []
    ws.append(wb.create_sheet(title=book_tag))
    ws.append(['序号','书名','作者','评分','评论人数','出版社'])
    count = 1
    for b in book_list:
        print(count)
        ws.append([count,b[0],b[1],b[2],b[3],b[4]])
        count += 1
    save_path = "book_list.xlsx"
    wb.save(save_path)


book_tag = "外国文学"
books = bookTag(book_tag)


print_booklists_excel(books,book_tag)