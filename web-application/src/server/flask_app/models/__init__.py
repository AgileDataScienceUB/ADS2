"""Module level init for database Models"""

from .district import District
from .neighborhood import Neighborhood
from .transport_graph import TransportGraph
from .root import Root

Root()#this runs an instantiation, for testing purposes only, remove when done testing