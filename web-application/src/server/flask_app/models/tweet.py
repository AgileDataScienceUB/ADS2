from .base import Base
from .geometry import Geometry,Point

class Tweet(Base):
    def __init__(self,id,text,N,E,created):
        super(Tweet, self).__init__()
        self.created_at = created
        self.id = id
        self.point = Point(N=N,E=E)
        self.text = text
        self.score = None