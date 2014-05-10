'''
Created on 2014. 5. 10.

@author: taeyong
'''

import math

class GeoPoint(object):
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
        
class GeoTrans(object):
    GEO = 0
    KATEC = 1
    TM = 2
    GRS80 = 3
    EPSLN = 0.0000000001
    
    def __init__(self):
        self.keys = {"GEO":"GEO", "KATEC":"KATEC", "TM":"TM"}
        self.m_arScaleFactor = {"GEO":1.0, "KATEC":0.9999, "TM":1.0}
        self.m_arLonCenter = {"GEO":0.0, "KATEC":2.23402144255274, "TM":2.21656815003280}
        self.m_arLatCenter = {"GEO":0.0, "KATEC":0.663225115757845, "TM":0.663225115757845}
        self.m_arFalseNorthing = {"GEO":0.0, "KATEC":600000.0, "TM":500000.0}
        self.m_arFalseEasting = {"GEO":0.0, "KATEC":400000.0, "TM":200000.0}
        self.m_arMajor = {"GEO":6378137.0, "KATEC":6377397.155, "TM":6377397.155}
        self.m_arMinor = {"GEO":6356752.3142, "KATEC":6356078.9633422494, "TM":6356078.9633422494}
        self.datum_params = [-146.43, 507.89, 681.46]
        self.m_Es = {}
        self.m_Esp = {}
        self.m_Ind = {}
        self.src_m = {}
        self.dst_m = {}
        
        for k in self.keys:
            tmp = self.m_arMinor[k] / self.m_arMajor[k]
            self.m_Es[k] = 1.0 - tmp * tmp
            self.m_Esp[k] = self.m_Es[k] / (1.0 - self.m_Es[k])
            
            if self.m_Es[k] < 0.00001:
                self.m_Ind[k] = 1.0
            else:
                self.m_Ind[k] = 0.0
            
            self.src_m[k] = self.m_arMajor[k] * self.mlfn(self.e0fn(self.m_Es[k]), self.e1fn(self.m_Es[k]), self.e2fn(self.m_Es[k]), self.e3fn(self.m_Es[k]), self.m_arLatCenter[k])
            self.dst_m[k] = self.m_arMajor[k] * self.mlfn(self.e0fn(self.m_Es[k]), self.e1fn(self.m_Es[k]), self.e2fn(self.m_Es[k]), self.e3fn(self.m_Es[k]), self.m_arLatCenter[k])
    
    def D2R(self, degree):
        return degree * math.pi / 180.0
    def R2D(self, radian):
        return radian * 180.0 / math.pi
    def e0fn(self, x):
        return 1.0 - 0.25 * x * (1.0 + x / 16.0 * (3.0 + 1.25 * x))
    def e1fn(self, x):
        return 0.375 * x * (1.0 + 0.25 * x * (1.0 + 0.46875 * x))
    def e2fn(self, x):
        return 0.05859375 * x * x * (1.0 + 0.75 * x)
    def e3fn(self, x):
        return x * x * x * (35.0 / 3072.0)
    def mlfn(self, e0, e1, e2, e3, phi):
        return e0 * phi - e1 * math.sin(2.0 * phi) + e2 * math.sin(4.0 * phi) - e3 * math.sin(6.0 * phi)
    def asinz(self, value):
        if abs(value) > 1.0:
            if value > 0:
                value = 1
            else:
                value = -1
        return math.asin(value);
    
    def convert(self, srctype, dsttype, in_pt):
        tmpPt = GeoPoint()
        out_pt = GeoPoint()
        
        if srctype == "GEO":
            tmpPt.x = self.D2R(in_pt.x)
            tmpPt.y = self.D2R(in_pt.y)
        else:
            self.tm2geo(srctype, in_pt, tmpPt)
            
        if dsttype == "GEO":
            out_pt.x = self.R2D(tmpPt.x)
            out_pt.y = self.R2D(tmpPt.y)
        else:
            self.geo2tm(dsttype, tmpPt, out_pt)
            
        return out_pt;
    
    def geo2tm(self, dsttype, in_pt, out_pt):
        self.transform("GEO", dsttype, in_pt)
        delta_lon = in_pt.x - self.m_arLonCenter[dsttype] #dsttype dictionary
        sin_phi = math.sin(in_pt.y)
        cos_phi = math.cos(in_pt.y)
        
        if self.m_Ind[dsttype] != 0:
            b = cos_phi * math.sin(delta_lon)
            if abs(abs(b) - 1.0) < self.EPSLN:
                pass
        else:
            b = 0
            x = 0.5 * self.m_arMajor[dsttype] * self.m_arScaleFactor[dsttype] * math.log((1.0 + b) / (1.0 - b))
            con = math.acos(cos_phi * math.cos(delta_lon) / math.sqrt(1.0 - b * b))
            if in_pt.y < 0:
                con = con * -1
                y = self.m_arMajor[dsttype] * self.m_arScaleFactor[dsttype] * (con - self.m_arLatCenter[dsttype])
                    
        al = cos_phi * delta_lon
        als = al * al
        c = self.m_Esp[dsttype] * cos_phi * cos_phi
        tq = math.tan(in_pt.y)
        t = tq * tq
        con = 1.0 - self.m_Es[dsttype] * sin_phi * sin_phi
        n = self.m_arMajor[dsttype] / math.sqrt(con)
        ml = self.m_arMajor[dsttype] * self.mlfn(self.e0fn(self.m_Es[dsttype]), self.e1fn(self.m_Es[dsttype]), self.e2fn(self.m_Es[dsttype]), self.e3fn(self.m_Es[dsttype]), in_pt.y)
            
        out_pt.x = self.m_arScaleFactor[dsttype] * n * al * (1.0 + als / 6.0 * (1.0 - t + c + als / 20.0 * (5.0 - 18.0 * t + t * t + 72.0 * c - 58.0 * self.m_Esp[dsttype]))) + self.m_arFalseEasting[dsttype];
        out_pt.y = self.m_arScaleFactor[dsttype] * (ml - self.dst_m[dsttype] + n * tq * (als * (0.5 + als / 24.0 * (5.0 - t + 9.0 * c + 4.0 * c * c + als / 30.0 * (61.0 - 58.0 * t + t * t + 600.0 * c - 330.0 * self.m_Esp[dsttype]))))) + self.m_arFalseNorthing[dsttype];

    def tm2geo(self, srctype, in_pt, out_pt):
        tmpPt = GeoPoint(in_pt.getX(), in_pt.getY())
        max_iter = 6
        if self.m_Ind[srctype] != 0:
            f = math.exp(in_pt.x / (self.m_arMajor[srctype] * self.m_arScaleFactor[srctype]))
            g = 0.5 * (f - 1.0 / f)
            temp = self.m_arLatCenter[srctype] + tmpPt.y / (self.m_arMajor[srctype] * self.m_arScaleFactor[srctype])
            h = math.cos(temp)
            con = math.sqrt((1.0 - h * h) / (1.0 + g * g))
            out_pt.y = self.asinz(con)

            if temp < 0:
                out_pt.y *= -1

            if (g == 0) and (h == 0):
                out_pt.x = self.m_arLonCenter[srctype]
            else:
                out_pt.x = math.atan(g / h) + self.m_arLonCenter[srctype]
            
        tmpPt.x -= self.m_arFalseEasting[srctype]
        tmpPt.y -= self.m_arFalseNorthing[srctype]
    
        con = (self.src_m[srctype] + tmpPt.y / self.m_arScaleFactor[srctype]) / self.m_arMajor[srctype]
        phi = con
        
        i = 0;

        while True:
            delta_Phi = ((con + self.e1fn(self.m_Es[srctype]) * math.sin(2.0 * phi) - self.e2fn(self.m_Es[srctype]) * math.sin(4.0 * phi) + self.e3fn(self.m_Es[srctype]) * math.sin(6.0 * phi)) / self.e0fn(self.m_Es[srctype])) - phi;
            phi = phi + delta_Phi;

            if abs(delta_Phi) <= self.EPSLN:
                break

            if i >= max_iter:
                break    
            i += 1
            
        if abs(phi) < (math.pi / 2):
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)
            tan_phi = math.tan(phi)
            c = self.m_Esp[srctype] * cos_phi * cos_phi
            cs = c * c
            t = tan_phi * tan_phi
            ts = t * t
            cont = 1.0 - self.m_Es[srctype] * sin_phi * sin_phi
            n = self.m_arMajor[srctype] / math.sqrt(cont)
            r = n * (1.0 - self.m_Es[srctype]) / cont
            d = tmpPt.x / (n * self.m_arScaleFactor[srctype])
            ds = d * d
            out_pt.y = phi - (n * tan_phi * ds / r) * (0.5 - ds / 24.0 * (5.0 + 3.0 * t + 10.0 * c - 4.0 * cs - 9.0 * self.m_Esp[srctype] - ds / 30.0 * (61.0 + 90.0 * t + 298.0 * c + 45.0 * ts - 252.0 * self.m_Esp[srctype] - 3.0 * cs)))
            out_pt.x = self.m_arLonCenter[srctype] + (d * (1.0 - ds / 6.0 * (1.0 + 2.0 * t + c - ds / 20.0 * (5.0 - 2.0 * c + 28.0 * t - 3.0 * cs + 8.0 * self.m_Esp[srctype] + 24.0 * ts))) / cos_phi)
        else:
            out_pt.y = math.pi * 0.5 * math.sin(tmpPt.y)
            out_pt.x = self.m_arLonCenter[srctype]
            
        self.transform(srctype, "GEO", out_pt)
            
    def getDistancebyGeo(self, pt1, pt2):
        lat1 = self.D2R(pt1.y)
        lon1 = self.D2R(pt1.x)
        lat2 = self.D2R(pt2.y)
        lon2 = self.D2R(pt2.x)

        longitude = lon2 - lon1
        latitude = lat2 - lat1

        a = math.pow(math.sin(latitude / 2.0), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(longitude / 2.0), 2)
        return 6376.5 * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    def getDistancebyKatec(self, pt1, pt2):
        pt1 = self.convert(self.KATEC, self.GEO, pt1)
        pt2 = self.convert(self.KATEC, self.GEO, pt2)
        return self.getDistancebyGeo(pt1, pt2)
    
    def getDistancebyTm(self, pt1, pt2):
        pt1 = self.convert(self.TM, self.GEO, pt1)
        pt2 = self.convert(self.TM, self.GEO, pt2)
        return self.getDistancebyGeo(pt1, pt2)

    def getTimebySec(self, distance):
        return round(3600 * distance / 4)

    def getTimebyMin(self, distance):
        return (long)(math.ceil(self.getTimebySec(distance) / 60))
    
    
    HALF_PI = 0.5 * math.pi
    COS_67P5  = 0.38268343236508977  #cosine of 67.5 degrees
    AD_C = 1.0026000
    
    def transform(self, srctype, dsttype, point):
        if srctype == dsttype:
            return
        
        if srctype != 0 or dsttype != 0:
            # Convert to geocentric coordinates.
            self.geodetic_to_geocentric(srctype, point)
            
            # Convert between datums
            if srctype != 0:
                self.geocentric_to_wgs84(point)
            
            if dsttype != 0:
                self.geocentric_from_wgs84(point)
            
            # Convert back to geodetic coordinates
            self.geocentric_to_geodetic(dsttype, point)

    def geodetic_to_geocentric (self, type, p):
        Longitude = p.x
        Latitude = p.y
        Height = p.z
        X = 0.0  # output
        Y = 0.0
        Z = 0.0
        
        Rn = 0.0            #Earth radius at location
        Sin_Lat = 0.0       #  Math.sin(Latitude)
        Sin2_Lat = 0.0      #  Square of Math.sin(Latitude)
        Cos_Lat = 0.0       #  Math.cos(Latitude)
        
        if Latitude < -self.HALF_PI and Latitude > -1.001 * self.HALF_PI:
            Latitude = -self.HALF_PI
        elif Latitude > self.HALF_PI and Latitude < 1.001 * self.HALF_PI:
            Latitude = self.HALF_PI
        elif (Latitude < -self.HALF_PI) or (Latitude > self.HALF_PI): # Latitude out of range
            return True
        
        # no errors
        if Longitude > math.pi:
            Longitude -= (2 * math.pi)
        Sin_Lat = math.sin(Latitude)
        Cos_Lat = math.cos(Latitude)
        Sin2_Lat = Sin_Lat * Sin_Lat
        Rn = self.m_arMajor[type] / (math.sqrt(1.0e0 - self.m_Es[type] * Sin2_Lat))
        X = (Rn + Height) * Cos_Lat * math.cos(Longitude)
        Y = (Rn + Height) * Cos_Lat * math.sin(Longitude)
        Z = ((Rn * (1 - self.m_Es[type])) + Height) * Sin_Lat
        
        p.x = X
        p.y = Y
        p.z = Z
        return False


    def geocentric_to_geodetic (self, type_t, p):
        X = p.x;
        Y = p.y;
        Z = p.z;
        Longitude = 0.0
        Latitude = 0.0
        Height = 0.0

        W = 0.0        # distance from Z axis */
        W2 = 0.0       # square of distance from Z axis */
        T0 = 0.0       # initial estimate of vertical component */
        T1 = 0.0       # corrected estimate of vertical component */
        S0 = 0.0       # initial estimate of horizontal component */
        S1 = 0.0       # corrected estimate of horizontal component */
        Sin_B0 = 0.0   # Math.sin(B0), B0 is estimate of Bowring aux doubleiable */
        Sin3_B0 = 0.0  # cube of Math.sin(B0) */
        Cos_B0 = 0.0   # Math.cos(B0) */
        Sin_p1 = 0.0   # Math.sin(phi1), phi1 is estimated latitude */
        Cos_p1 = 0.0   # Math.cos(phi1) */
        Rn = 0.0       # Earth radius at location */
        Sum = 0.0      # numerator of Math.cos(phi1) */
        At_Pole = False  # indicates location is in polar region */

        At_Pole = False
        if X != 0.0:
            Longitude = math.atan2(Y,X)
        else:
            if Y > 0:
                Longitude = self.HALF_PI
            elif Y < 0:
                Longitude = -self.HALF_PI
            else:
                At_Pole = True
                Longitude = 0.0
                if Z > 0.0:  # north pole */
                    Latitude = self.HALF_PI
                elif Z < 0.0:  # south pole */
                    Latitude = -self.HALF_PI
                else:  # center of earth */
                    Latitude = self.HALF_PI
                    Height = -self.m_arMinor[type_t]
                    return
                
        W2 = X*X + Y*Y
        W = math.sqrt(W2)
        T0 = Z * self.AD_C
        S0 = math.sqrt(T0 * T0 + W2)
        Sin_B0 = T0 / S0
        Cos_B0 = W / S0
        Sin3_B0 = Sin_B0 * Sin_B0 * Sin_B0
        T1 = Z + self.m_arMinor[type_t] * self.m_Esp[type_t] * Sin3_B0
        Sum = W - self.m_arMajor[type_t] * self.m_Es[type_t] * Cos_B0 * Cos_B0 * Cos_B0
        S1 = math.sqrt(T1*T1 + Sum * Sum)
        Sin_p1 = T1 / S1
        Cos_p1 = Sum / S1
        Rn = self.m_arMajor[type_t] / math.sqrt(1.0 - self.m_Es[type_t] * Sin_p1 * Sin_p1);
        if Cos_p1 >= self.COS_67P5:
            Height = W / Cos_p1 - Rn
        elif Cos_p1 <= -self.COS_67P5:
            Height = W / -Cos_p1 - Rn
        else:
            Height = Z / Sin_p1 + Rn * (self.m_Es[type_t] - 1.0)

        if At_Pole == False:
            Latitude = math.atan(Sin_p1 / Cos_p1)
        
        p.x = Longitude
        p.y =Latitude
        p.z = Height
        return

    def geocentric_to_wgs84(self, p):
        p.x += self.datum_params[0];
        p.y += self.datum_params[1];
        p.z += self.datum_params[2];

    def geocentric_from_wgs84(self, p): 
        p.x -= self.datum_params[0];
        p.y -= self.datum_params[1];
        p.z -= self.datum_params[2];