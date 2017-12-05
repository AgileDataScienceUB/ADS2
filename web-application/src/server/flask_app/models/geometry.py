class Geometry:
    def __init__(self):
        self.polygons = []
        self.area = None
        self.perimiter = None
        self.centroid = None

    def compute(self):
        self.area = 0
        self.centroid = Point(0,0)
        for polygon in self.polygons:
            polygon.compute()
            self.perimiter += polygon.perimiter
            self.area += polygon.area
            weighted_point = Point(polygon.centroid.x*polygon.area,polygon.centroid.y*polygon.area)
            self.centroid.add(weighted_point)
        self.centroid.mult(1/self.area)

class Polygon:
    def __init__(self):
        self.area = None
        self.perimiter = None
        self.centroid = None
        self.points = None

    def compute(self):
        """Compute the centroid point of the polygon assuming well orderd points"""
        #https://en.wikipedia.org/wiki/Centroid#Centroid_of_a_polygon
        import numpy as np
        x,y,a,perim = 0,0,0,0
        n = len(self.points)
        for i in range(n-1):
            p = self.points[i]
            q = self.points[(i + 1) % n]
            #print('p.x',p.x)
            c_i = (p.x * q.y - p.y * q.x)
            x += (p.x + q.x) * c_i
            y += (p.y + q.y) * c_i
            a += c_i
            perim += np.sqrt((p.x-q.x)*(p.x-q.x)+(p.y-q.y)*(p.y-q.y))
        a /=2
        self.area = abs(a)
        self.perimiter = perim
        self.centroid = Point(x/(6*a),y/(6*a))

class Point:
    def __init__(self,E,N):
        self.x = E
        self.y = N
    def add(self,point):
        self.x += point.x
        self.y += point.y
    def mult(self,scalar):
        self.x *= scalar
        self.y *= scalar