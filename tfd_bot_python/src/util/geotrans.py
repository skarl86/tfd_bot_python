# -*- coding: UTF-8 -*-
'''
Created on 2014. 5. 13.

@author: taeyong
'''

"""
jpype 설치법(OS X 기준)
1. http://jpype.sourceforge.net에서 jpype최신 버전을 받는다.
2. 적당한 곳에 압축을 푼다.
3. 터미널에서 압축푼 곳의 경로에 맞춘다.
4. sudo -E python setup.py install 을 입력한다.
"""

import jpype

def katechToWgs84(x, y):
    if(type(x) != type(0.0) or type(y) != type(0.0)):
        print "Parameters must be type of float"
        return -1
    """
    classpath = os.path.join(os.path.abspath('../'), 'bin')
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)
    """
#     jarpath = os.path.join(os.path.abspath('.'), 'GeoTrans.jar')
#     jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)
    # JVM Start
    if not jpype.isJVMStarted():
        jarpath = ".:GeoTrans.jar"
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jarpath))
    
    # Package Import
    GeoPkg = jpype.JPackage("GeoTrans")
    # Class Import
    GeoPoint = GeoPkg.GeoPoint
    GeoTrans = GeoPkg.GeoTrans
    
    # Point convert
    oKA = GeoPoint(x, y)
    oGeo = GeoTrans.convert(GeoTrans.KATEC, GeoTrans.GEO, oKA)
    
    return {"x":oGeo.getX(), "y":oGeo.getY()}

def Wgs84ToKatech(x, y):
    if(type(x) != type(0.0) or type(y) != type(0.0)):
        print "Parameters must be type of float"
        return -1
    
    if not jpype.isJVMStarted():
        jarpath = ".:GeoTrans.jar"
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jarpath))
    
    GeoPkg = jpype.JPackage("GeoTrans")
    GeoPoint = GeoPkg.GeoPoint
    GeoTrans = GeoPkg.GeoTrans
    
    oGeo = GeoPoint(x, y)
    oKA = GeoTrans.convert(GeoTrans.GEO, GeoTrans.KATEC, oGeo)
    
    return {"x":oKA.getX(), "y":oKA.getY()}


#================= Test Code ===================================
if __name__ == "__main__":
    dict = {}
#     dict = katechToWgs84(304888.0, 551340.0)    
    dict = katechToWgs84(306062.0, 550992.0)
    print str(dict["x"]) + " " + str(dict["y"])
    
    dict = Wgs84ToKatech(dict["x"], dict["y"])
    print str(dict["x"]) + " " + str(dict["y"])