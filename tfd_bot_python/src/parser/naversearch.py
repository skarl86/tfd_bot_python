'''
Created on 2014. 5. 18.

@author: taeyong
'''
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
            break
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
            