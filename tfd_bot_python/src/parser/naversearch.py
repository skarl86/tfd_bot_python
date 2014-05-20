#-*- coding: utf-8 -*-
'''
Created on 2014. 5. 18.

@author: taeyong
'''
import re
import urllib2
from bs4 import BeautifulSoup

class NaverSearch(object):
    def __init__(self):
        self._API_KEY = "a0504c8ef72934d16be6d2a29e5b69aa"
        self._BASE_URL = "http://openapi.naver.com/search"
        self._Target = ""
    
    def getResult(self, keyword):
        soupList = []
        start = 1
        display = 100
        query = keyword.replace(" ", "+")
        
        while True:
            param = {"key":self._API_KEY,
                     "query":query,
                     "target":self._Target,
                     "display":display,
                     "start":start
                     }
            completeParam = self._generateParam(param)
            url = self._BASE_URL + "?"
            url = url + completeParam
            
            #HTML Parsing
            data = self._connect(url)
            #Import to BeautifulSoup
            soup = BeautifulSoup(data)
            
            if soup.find("error_code"):
                break
            soupList.append(soup)

            start += 100
            if start == 901:
                display = 99 #901~999
            elif start == 1001:
                start = 1000
                display = 100 #1000~1099
            elif start > 1000:
                break
            
        #Item Parsing
        itemList = self._generateData(soupList)
        return itemList
    
    def _generateData(self, soupList):
        #This function is needed to implement
        pass
    
    def _generateParam(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k, str(param[k])]))
        return "&".join(list)
    
    def _connect(self, url):
        try:
            #HTML parsing
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
            
            
class NaverLocal(NaverSearch):
    def __init__(self):
        super(NaverLocal, self).__init__()
        self._Target = "local"
    
    def _generateData(self, soupList):
        list = []
        for soup in soupList:
            #All item is added to items list
            items = soup.findAll("item")
            for item in items:
                title = item.find("title")
                title = title.text.replace("<b>", "")   #Remove <b> tag
                title = title.replace("</b>", "")       #Remove </b> tag
                category = item.find("category")
                tel = item.find("telephone")
                addr = item.find("address")
                desc = item.find("description")
                desc = desc.text.replace("<b>", "")
                desc = desc.replace("</b>", "")
                link = item.find("link")
                mapx = item.find("mapx")
                mapy = item.find("mapy")
                
                dic = {"name":title.encode('utf-8'),
                       "category":category.text.encode('utf-8'),
                       "telephone":tel.text.encode('utf-8'),
                       "address":addr.text.encode('utf-8'),
                       "url":link.text.encode('utf-8'),
                       "description":desc.encode('utf-8'),
                       "pointx":mapx.text.encode('utf-8'),
                       "pointy":mapy.text.encode('utf-8')
                       }
                list.append(dic)
        return list
    
    
class NaverBlog(NaverSearch):
    def __init__(self):
        super(NaverBlog, self).__init__()
        self._Target = "blog"
        self._BlogURL = "http://blog.naver.com"
        self._PostID = "post-view"
    
    def _generateData(self, soupList):
        list = []
        for soup in soupList:
            #All item is added to items list
            items = soup.findAll("item")
            for item in items:
                title = item.find("title")
                title = title.text.replace("<b>", "")   #Remove <b> tag
                title = title.replace("</b>", "")       #Remove </b> tag
                desc = item.find("description")
                desc = desc.text.replace("<b>", "")
                desc = desc.replace("</b>", "")
                link = item.find("link")
                blogger = item.find("bloggername")
                b_link = item.find("bloggerlink")
                
                text = self._blogParsing(link.text) #위에서 얻은 link를 통해 블로그의 내용을 파싱
                if len(text) == 0:
                    continue
                dic = {"title":title.encode('utf-8'),
                       "text":text.encode('utf-8'),
                       "link":link.text.encode('utf-8'),
                       "description":desc.encode('utf-8'),
                       "bloggername":blogger.text.encode('utf-8'),
                       "bloggerlink":b_link.text.encode('utf-8')
                       }
                list.append(dic)
#                 print "Processing at " + str(len(list))
        return list
    
    def _blogParsing(self, link):
        data = self._connect(link)
        bs = BeautifulSoup(data)
        frame = bs.findAll("frame")
        try:
            src = frame[0].attrs["src"] #블로그 본문파싱 가능한 url을 만들기위해 아이디와 글번호가 있는 주소정보 파싱
            logNo = re.search(r"logNo=\d+", src)    # 본문 글번호만 추가로 파싱
            logNo = re.sub(r"logNo=", "", logNo.group())
        except IndexError:
            print "IndexError"
            return ""
        except AttributeError:
            print "AttributeError"
            return ""
        
        blogURL = self._BlogURL + src #파싱 가능한 URL
        postNo = self._PostID + logNo    #블로그 태그에서 본문에 해당하는 div의 id
        
        data = self._connect(blogURL)
        bs = BeautifulSoup(data)
        text = bs.find("div", {"id":postNo}).text
        
        return text
    
# if __name__ == "__main__":
#     list = []
#     a = NaverBlog()
#     list = a.getResult("홍대 술집")
#     for dict in list:
#         print dict["title"]
#         print dict["link"]
#         print dict["description"]
#         print dict["bloggername"]
#         print dict["bloggerlink"]
#         print dict["text"]
#         print "="*50