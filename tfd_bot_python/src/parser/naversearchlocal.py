# -*- coding: UTF-8 -*-
'''
Created on 2014. 5. 10.

@author: taeyong
'''

import urllib2
from bs4 import BeautifulSoup
import re
import htmlentitydefs

class NaverSearch(object):
    def __init__(self):
        self._API_KEY = "a0504c8ef72934d16be6d2a29e5b69aa"
        self._BASE_URL = "http://openapi.naver.com/search"
        self._Target = "local"
        
    def getResult(self, keyword, display = "100", start = "1", sort = "random"):
        query = keyword.replace(" ", "+")
        url = self._BASE_URL + "?"
        
        param = {"key":self._API_KEY,
                 "query":query,
                 "target":self._Target,
                 "display":display,
                 "start":start
                 }
        completeParam = self._generateParam(param)
        url = url + completeParam
        
        #HTML Parsing
        data = self._connect(url)
        #Import to BeautifulSoup
        soup = BeautifulSoup(data)
        #Item Parsing
        itemList = self._generateData(soup)
        return itemList
        
    def _generateParam(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k, str(param[k])]))
        return "&".join(list)
    
    def _generateData(self, data):
        list = []
        #All item is added to items list
        items = data.findAll("item")
        for item in items:
            title = item.find("title")
            tel = item.find("telephone")
            addr = item.find("address")
            desc = item.find("description")
            mapx = item.find("mpax")
            mapy = item.find("mapy")
            list.append({"title":title, "telephone":tel, "address":addr, "description":desc, "mapx":mapx, "mapy":mapy})
        return list
    
    def _connect(self, url):
        try:
            #HTML parsing
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
        
#================ Test Code ================================================
def unescape(matched):
    return htmlentitydefs.entitydefs[matched.group(1)]

if __name__ == "__main__":
    list = []
    nm = NaverSearch()
    list = nm.getResult("홍대 식당")
    for l in list:
        print l["title"]
#         print re.sub('&([a-z]+);', unescape, l["title"])