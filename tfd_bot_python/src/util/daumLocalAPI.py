'''
Created on 2014. 5. 11.

@author: taeyong
'''

import urllib2
from bs4 import BeautifulSoup

class GeoTrans(object):
    def __init__(self, x, y, fromCoord = "KTM", toCoord = "WGS84"):
        self._BASE_URL = "http://apis.daum.net/local/geo/transcoord"
        self._API_KEY = "5efcc32648c68db3fee479e259bdc8ea2440f289"
        self._FROM_COORD = fromCoord
        self._TO_COORD = toCoord
        self._OUTPUT = "json"
        self._X = str(x)
        self._Y = str(y)
        self._trans()
        
    def _trans(self):
        param = {"apikey":self._API_KEY,
                "fromCoord":self._FROM_COORD,
                "toCoord":self._TO_COORD,
                "output":self._OUTPUT,
                "x":self._X,
                "y":self._Y
                }
        url = self._generateURL(param)
        data = self._connect(url)
        geoPoints = self._generateData(data)
        self._X = str(geoPoints["x"])
        self._Y = str(geoPoints["y"])
        
    def _generateURL(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k, str(param[k])]))
        url = "&".join(list)
        url = "?".join([self._BASE_URL, url])
        return url
    
    def _connect(self, url):
        try:
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
    def _generateData(self, data):
        replaceText = "{}:\""
        for t in replaceText:
            data = data.replace(t, "")
        geoPointList = data.split(",")
        geoPointDic = {geoPointList[0][:1]:geoPointList[0][1:],
                       geoPointList[1][:1]:geoPointList[1][1:]}
        return geoPointDic
        

#============= Test Code ==================================
naverToGoogle = GeoTrans(308213, 544106)
googleToNaver = GeoTrans(naverToGoogle._X, naverToGoogle._Y, "WGS84", "KTM")

print naverToGoogle._X + " " + naverToGoogle._Y
print googleToNaver._X + " " + googleToNaver._Y