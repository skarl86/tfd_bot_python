# -*- coding: UTF-8 -*-
'''
Created on 2014. 5. 10.

@author: taeyong
'''

from naversearch import NaverSearch

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
        
#================ Test Code ================================================
if __name__ == "__main__":
    list = []
    nm = NaverLocal()
    list = nm.getResult("홍대 식당")
    for i, l in enumerate(list):
        print(l["title"] + "\n")
        print(l["category"] + "\n")
        print(l["telephone"] + "\n")
        print(l["address"] + "\n")
        print(l["link"] + "\n")
        print(l["description"] + "\n")
        print(l["mapx"] + ", " + l["mapy"] + "\n")
        print("----------------------------------------------\n")