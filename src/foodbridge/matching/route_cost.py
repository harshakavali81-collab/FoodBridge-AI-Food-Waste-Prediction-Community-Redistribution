from math import sin,cos,asin,sqrt,radians
def haversine_km(a,b,c,d):
    """Straight-line geographic distance only; not an actual driving route."""
    lat1,lon1,lat2,lon2=map(radians,(a,b,c,d))
    x=sin((lat2-lat1)/2)**2+cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    return 6371*2*asin(sqrt(min(1,max(0,x))))
