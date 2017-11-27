from .base import Base
from .geometry import Geometry

class Neighborhood(Base):
    def __init__(self):
        super(Neighborhood, self).__init__()
        self.name = None
        self.geometry = Geometry()
        #statistics
        #economics
        self.avg_flat_rental_from_council = None
        self.avg_flat_rental_from_web = None
        self.avg_flat_size = None
        self.avg_flat_meter_rental = None
        self.avg_income = None
        #demographics
        self.secondary_studies_fraction = None
        self.age_distr = {}
        self.flats_count = None
        self.flat_nationals_only = None
        self.flats_foreigners_only = None
        self.flats_mixed = None