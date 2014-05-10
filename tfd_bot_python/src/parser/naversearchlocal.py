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
        print url
        return self._connect(url)
        
    def _generateParam(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k, param[k]]))
        return "&".join(list)
    
    def _generateData(self, data):
        list = []
        items = data.findAll("item")
        for item in items:
            title = item.find("title")
            tel = item.find("telephone")
            addr = item.find("address")
            desc = item.find("description")
            mapx = item.find("mpax")
            mapy = item.find("mapy")
            list.append(NaverLocalDTO(title, tel, addr, desc, mapx, mapy))
        return list
    
    def _connect(self, url):
        try:
            data = urllib2.urlopen(url).read()
            soup = BeautifulSoup(data)
            return self._generateData(soup)
        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
            
class NaverLocalDTO(object):
    def __init__(self, title, telephone, address, description, mapx, mapy):
        self._Title = title
        self._Telephone = telephone
        self._Address = address
        self._Description = description
        self._Mapx = mapx
        self._Mapy = mapy
        
#================ Test Code ================================================
def unescape(matched):
    return htmlentitydefs.entitydefs[matched.group(1)]

if __name__ == "__main__":
    list = []
    nm = NaverSearch()
    list = nm.getResult("홍대 식당")
    for l in list:
        print re.sub('&([a-z]+);', unescape, l._Title.string)