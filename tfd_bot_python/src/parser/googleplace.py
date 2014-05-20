#-*- coding: utf-8 -*-

'''
Created on 2014. 5. 3.

@author: NCri
'''

'''
https://maps.googleapis.com/maps/api/place/textsearch/json?query=""&sensor=true&language=ko&key=""
https://maps.googleapis.com/maps/api/place/details/json?reference=""&sensor=true&language=ko&key=""
https://maps.googleapis.com/maps/api/place/photo?maxwidth=""&photoreference=""&sensor=true&language=ko&key=""

'''

import urllib2
import json

class GooglePlace(object):
    def __init__(self):
        self._API_KEY = "AIzaSyCJQXicui49gzhAwbGWGmm3OJEpKPjUeJE"
        self._BASE_URL = "https://maps.googleapis.com/maps/api/place"
        self._returnType = "json"
        self._language = "ko"
        self._sensor = "true"
    def getResult(self, keyword):
        query = keyword.replace(" ", "+")
        print query
        function = "textsearch"
        url = "/".join([self._BASE_URL, function])
        url = "/".join([url, self._returnType])
        
        param = {"query":query,
                 "sensor":self._sensor,
                 "language":self._language,
                 "key":self._API_KEY
                 }
        print param
        completParam = self._generateParam(param)
        url = "?".join([url, completParam])
        print url
        return self._connect(url)
        
    def getDetailResult(self):
        function = "details"
        
    def getPhotoResult(self):
        function = "photo"
        
    def _connect(self, url):
        try:
            #구글 플레이스에서 API 리턴값을 받는다. 
            data = urllib2.urlopen(url).read()            
            #JSON 값을 Dictionary로 Converse.
            data = json.loads(data)            
            # DB에 넣기 전 데이터 가공단계.
            return self._generateData(data)
            
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
        
    def _generateParam(self, param):
        list = []
        for k in param.keys():
            list.append("=".join([k,param[k]]))
        return "&".join(list)
    
    def _generateData(self, data):
        returnList = []
        resultList = data["results"]
        for dict in resultList:
            lat, lng = self._seperateLocation(dict["geometry"])
            newData = {"name":dict["name"],
                       "address":dict["formatted_address"],
                       "category":",".join(dict["types"]),
                       "pointx":lng,
                       "pointy":lat
                       }
            returnList.append(newData)
        return returnList
                    
    def _seperateLocation(self, location):
        try:
            lat = location["location"]["lat"]
            lng = location["location"]["lng"]
        except KeyError:
            print "Dictionary Key error."
            return None, None
        return lat, lng
    
if __name__ == "__main__":
    gp = GooglePlace()
    gp.getResult("홍대 식당")
        