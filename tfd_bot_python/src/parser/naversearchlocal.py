# -*- coding: UTF-8 -*-
'''
Created on 2014. 5. 10.

@author: taeyong
'''

import urllib2
from bs4 import BeautifulSoup

class NaverSearch(object):
    def __init__(self):
        self._API_KEY = "a0504c8ef72934d16be6d2a29e5b69aa"
        self._BASE_URL = "http://openapi.naver.com/search"
        self._Target = "local"
        
    def getResult(self, keyword, sort = "random"):
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
            completeParam = self.__generateParam__(param)
            url = self._BASE_URL + "?"
            url = url + completeParam
            
            #HTML Parsing
            data = self.__connect__(url)
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
        itemList = self.__generateData__(soupList)
        return itemList
        
    def __generateParam__(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k, str(param[k])]))
        return "&".join(list)
    
    def __generateData__(self, soupList):
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
                
                dic = {"title":title.encode('utf-8'),
                       "category":category.text.encode('utf-8'),
                       "telephone":tel.text.encode('utf-8'),
                       "address":addr.text.encode('utf-8'),
                       "link":link.text.encode('utf-8'),
                       "description":desc.encode('utf-8'),
                       "mapx":mapx.text.encode('utf-8'),
                       "mapy":mapy.text.encode('utf-8')
                       }
                list.append(dic)
        return list
    
    def __connect__(self, url):
        try:
            #HTML parsing
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
    def __linkParsing__(self, link):
        if link == "":
            return ""
        data = self.__connect__(link)
        if not data:
            return ""
        bs = BeautifulSoup(data)
        a = bs.find("frame")
        if not a:
            return link
        return a.attrs["src"].encode('utf-8')
        
            
        
#================ Test Code ================================================
if __name__ == "__main__":
    list = []
    nm = NaverSearch()
    list = nm.getResult("홍대 식당")
#     for i, l in enumerate(list):
#         print(l["title"] + "\n")
#         print(l["category"] + "\n")
#         print(l["telephone"] + "\n")
#         print(l["address"] + "\n")
#         print(l["link"] + "\n")
#         print(l["description"] + "\n")
#         print(l["mapx"] + ", " + l["mapy"] + "\n")
#         print("----------------------------------------------\n")