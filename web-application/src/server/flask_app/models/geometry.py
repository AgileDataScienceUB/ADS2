class Geometry:
    def __init__(self):
        self.polygon = []
        self.area = None
        self.perimiter = None
        #self.coord_x = None
        #self.coord_y = None

    def centroid(self):
        """Compute the centroid point of the polygon assuming well orderd points"""
        #https://en.wikipedia.org/wiki/Centroid#Centroid_of_a_polygon
        x,y,a = 0,0,0
        n = len(self.polygon)
        for i in range(n):
            p = self.polygon[i]
            q = self.polygon[i + 1 % n]
            c_i = (p.x * q.y - p.y * q.x)
            x += (p.x + q.x) * c_i
            y += (p.y + q.y) * c_i
            a += c_i
        a /=2
        return Point(x/(6*a),y/(6*a))

class Point:
    def __init__(self,E,N):
        self.x = E
        self.y = N