url = "http://www.en8848.com.cn"
lessonUrls = "/tingli/brand/USA"

from bs4 import BeautifulSoup
import requests


import re
def parseLesson():
    response = requests.get(url + lessonUrls)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text,"html.parser")
    pattrn = re.compile('\s*'+u'走遍美国第')
    res = soup.find_all('a',title=pattrn)
    lessonDict = {}
    for lesson in res:
        if('title' in lesson.attrs) and ('href' in lesson.attrs):
            title_str = lesson['title']
            lessonDict[title_str]=lesson['href']
    return lessonDict


def getLessonDownloadUrls():
    le = parseLesson()
    lessonUrlList = []
    for(title,urlStr) in le.items():
        if url not in urlStr:
            downPageUrl = parseSingleLesson(url + urlStr)#第一个url地址不全
            # print(downPageUrl)
        else:
            downPageUrl = parseSingleLesson(urlStr)
        voiceUrls = getOneLessonDownUrl(downPageUrl)
        lessonUrl = {}
        lessonUrl['title'] = title
        lessonUrl['urls'] = voiceUrls
        lessonUrlList.append(lessonUrl)
    return lessonUrlList
#http://mp3.en8848.com/zhuo-bian-mei-guo/u01-1.mp3
# $(".jp-download").click(function(){
#  window.open('/e/action/down.php?classid=9340&id=44210&mp3=http://Mp3.en8848.com/zhuo-bian-mei-guo/u01-1.mp3') ;
#  });
#正则表达式符号解释：
# + 	匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。
# ？  匹配前面的子表达式零次或一次。例如，"do(es)?" 可以匹配 "do" 或 "does" 中的"do" 。? 等价于 {0,1}。
# \s  匹配任何空白字符

def parseSingleLesson(singleLessUrl):
    response = requests.get(singleLessUrl)
    response.encoding = response.apparent_encoding
    str = response.text
    soup = BeautifulSoup(str,"html.parser")
    for script_str in soup.find_all("script"):
        script_str = script_str.text
        if script_str.find("jp-download") > -1:
            pattern = re.compile('(?<=jp-download)(.+?)open\s?''\(\s?\'(.+?)\s?\'\)(.+?)(?<=;)', re.S)
            res = re.search(pattern,script_str)
            if(res.lastindex >=2):
               #返回匹配到一个或者多个分组的字符串
                return res.group(2)

def getOneLessonDownUrl(oneDownUrl):
    try:
        response = requests.get(url+oneDownUrl)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text,"html.parser")
        res = soup.find('a',id="dload")
        downloadUrls={}
        if 'href' in res.attrs:
            downloadUrls['mp3'] = res.attrs['href']
        res = soup.find('a',id='dloadword')
        if 'href' in res.attrs:
            downloadUrls['lrc'] = res.attrs['href']
            return downloadUrls
    except Exception as e:
        return None
import codecs
def saveFileUtf8(filename,str):
    with codecs.open(filename,'w',encoding='utf-8') as fp:
        fp.write(str)
import json
import pathlib
#保存所有mp3文件为json格式显示
def saveAllLessonnDownUrls(filename="lessonMp3Urls.json"):
    getAllUrls = getLessonDownloadUrls()
    k = pathlib.Path(filename).exists()
    if k:
        return getAllUrls
    else:
        jsonLesson = json.dumps(getAllUrls,sort_keys=True,indent=4)
        saveFileUtf8(filename, jsonLesson)
    return getAllUrls
allUrls = saveAllLessonnDownUrls()
from urllib import request
def downloadFile(srcFilename,desFilename):
    request.urlretrieve(srcFilename,desFilename)
def downloadFromJsonFile(allUrls):
    for lesson in allUrls:
        urls = None
        urls = lesson['urls']
        if urls and 'mp3'in urls and 'lrc' in urls:
            downloadFile(urls['mp3'],"download/"+lesson['title']+".mp3")
            downloadFile(urls['lrc'],"download/"+lesson['title']+".lrc")

downloadFromJsonFile(allUrls)