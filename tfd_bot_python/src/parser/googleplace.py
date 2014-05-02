'''
Created on 2014. 5. 3.

@author: NCri
'''

'''
https://maps.googleapis.com/maps/api/place/textsearch/json?query=""&sensor=true&language=ko&key=""
https://maps.googleapis.com/maps/api/place/details/json?reference=""&sensor=true&language=ko&key=""
https://maps.googleapis.com/maps/api/place/photo?maxwidth=""&photoreference=""&sensor=true&language=ko&key=""

'''

class GooglePlace(object):
    def __init__(self):
        self._API_KEY = "AIzaSyCJQXicui49gzhAwbGWGmm3OJEpKPjUeJE"
        self._BASE_URL = "https://maps.googleapis.com/maps/api/place/"
        self._parameters = {}
        self._returnType = "json"
        self._language = "ko"
        
    def getResult(self, keyword):
        query = keyword
        function = "textsearch"
        url = "/".join(self._BASE_URL, function)
        
    def getDetailResult(self):
        function = "details"
        
    def getPhotoResult(self):
        function = "photo"
        
    def _connect(self, url):
        pass
    