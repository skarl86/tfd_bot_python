# -*- coding: UTF-8 -*-
'''
Created on 2014. 5. 18.

@author: taeyong
'''

import re
from bs4 import BeautifulSoup
from naversearch import NaverSearch

class NaverBlog(NaverSearch):
    def __init__(self):
        super(NaverBlog, self).__init__()
        self._Target = "blog"
    
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
                
                dic = {"title":title.encode('utf-8'),
                       "link":link.text.encode('utf-8'),
                       "description":desc.encode('utf-8'),
                       "bloggername":blogger.text.encode('utf-8'),
                       "bloggerlink":b_link.text.encode('utf-8')
                       }
                list.append(dic)
#                 title, text = self._blogParsing(link.text) #위에서 얻은 link를 통해 블로그의 내용을 파싱
        return list
    
    def _blogParsing(self, link):
        data = self._connect(link)
        bs = BeautifulSoup(data)
        try:
            frame = bs.findAll("frame")
        except IndexError:
            print "IndexError : "
            return
        src = frame[0].attrs["src"] #블로그 본문파싱 가능한 url을 만들기위해 아이디와 글번호가 있는 주소정보 파싱
        logNo = re.search(r"logNo=\d+", src)    # 본문 글번호만 추가로 파싱
        try:
            logNo = re.sub(r"logNo=", "", logNo.group())
        except AttributeError:
            print "AttributeError : "
            return
        
        blogURL = "http://blog.naver.com" + src #파싱 가능한 URL
        postNo = "post-view" + logNo    #블로그 태그에서 본문에 해당하는 div의 id
        
        data = self._connect(blogURL)
        bs = BeautifulSoup(data)
        title = bs.find("title").text.encode('utf-8')
        text = bs.find("div", {"id":postNo}).text.encode('utf-8')
        
        return title, text
        
        
#================ Test Code ================================================
if __name__ == "__main__":
    list = []
    nm = NaverBlog()
    list = nm.getResult("홍대 식당")
    for i, l in enumerate(list):
        print(l["title"] + "\n")
        print(l["link"] + "\n")
        print(l["description"] + "\n")
        print(l["bloggername"] + "\n")
        print(l["bloggerlink"] + "\n")
        print("----------------------------------------------\n")