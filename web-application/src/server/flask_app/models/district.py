from .base import Base
from .geometry import Geometry

class District(Base):
    def __init__(self):
        super(District, self).__init__()
        self.name = None
        self.neighborhoods = {}
        self.geometry = Geometry()
        #statistics
        #safety
        self.neighbors_comunal_incidents_100 = None
        self.criminal_offences_1000 = None
        self.crimes_against_property_100 = None
        self.domestic_crimes_1000 = None