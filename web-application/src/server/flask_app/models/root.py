import pandas as pd
from .neighborhood import Neighborhood
from .district import District
from .geometry import Geometry, Point
import networkx as nx

class Root:
    """Class containing a dictionaries of District and Neighborhood type objects and methods to fill them.
    Note that Neighborhood are referenced both at root.neighborhoods (all of them) and at district.neighborhoods (those of such district),
    but both point to the same instances."""
    def __init__(self):
        self.districts = {}
        self.neighborhoods = {}
        self.read()

    def read(self):
        """Initializes and fills instances of District objects."""
        self.initialise_districts()
        self.fill_district_neighborhoods()

        self.fill_neighborhood_rental_stats()
        self.fill_neighborhood_secondary_studies_fraction()
        #...
        self.fill_store_grocery()
        self.fill_store_bar()
        self.fill_store_disco()
        self.fill_store_sport()
        self.fill_store_drugstore()
        self.fill_store_restaurant()
        self.fill_store_clothes()

        self.fill_flats()
        self.fill_neighborhood_rental_web()

        self.fill_neighborhood_age_distr()

        self.fill_neighborhood_geometry()

        #falta fer
        self.fill_district_safety_statistics()
        self.fill_district_geometry()

        #Grapho transport
        #self.fill_grapho_metro()


    def initialise_districts(self):
        df = pd.read_csv('./data/'+'district_neighborhood.csv')
        self.districts = {}
        for district_id in pd.unique(df['district_id']):
            district = District()
            district.id = district_id
            self.districts[district_id] = district

    def fill_district_neighborhoods(self):
        """Fill the Neighborhood list attribute of District with initialized instances containing id and name"""
        df = pd.read_csv('./data/' + 'district_neighborhood.csv')
        self.neighborhoods = {}
        for index, row in df.iterrows():
            #initialize
            neighborhood = Neighborhood()
            neighborhood.id = row['neighborhood_id']
            neighborhood.name = row['neighborhood_name']
            #add to district's neighborhoods dictionary
            district = self.districts[row['district_id']]
            district.neighborhoods[neighborhood.id] = neighborhood
            #also add it to our dictionary of all neighborhoods
            self.neighborhoods[neighborhood.id] = neighborhood

        ## check filled correctly
        #for district in self.districts.values():
        #    print('district id', district.id)
        #    for neighborhood in district.neighborhoods.values():
        #        print('neighborhood id', neighborhood.id, 'name', neighborhood.name)

    def fill_district_safety_statistics(self):
        """fill the following fields:
            neighbors_comunal_incidents_100
            criminal_offences_1000
            crimes_against_property_100
            domestic_crimes_1000"""
        pass

    def fill_neighborhood_rental_stats(self):
        df = pd.read_csv('./data/' + 'flats_rental_council.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['neighborhood_id']]
            neighborhood.avg_flat_rental_from_council = row['value']

    def fill_neighborhood_income(self):
        df = pd.read_csv('./data/' + 'avincome2015.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['neighborhood_id']]
            neighborhood.avg_income = row['value']

    def fill_neighborhood_secondary_studies_fraction(self):
        df = pd.read_csv('./data/' + 'estudis.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.secondary_studies_fraction = row['value']
#comerços
    def fill_store_grocery(self):
        df = pd.read_csv('./data/' + 'alimentacio.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_grocery = row['#alimentacio']

    def fill_store_bar(self):
        df = pd.read_csv('./data/' + 'bars.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_bar = row['#bars']

    def fill_store_disco(self):
        df = pd.read_csv('./data/' + 'discos.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_disco = row['#discos']

    def fill_store_sport(self):
        df = pd.read_csv('./data/' + 'esport.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_sport = row['#esport']

    def fill_store_drugstore(self):
        df = pd.read_csv('./data/' + 'farmacies.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_drugstore = row['#farmacies']

    def fill_store_restaurant(self):
        df = pd.read_csv('./data/' + 'restaurants.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_restaurant = row['#restaurants']

    def fill_store_clothes(self):
        df = pd.read_csv('./data/' + 'roba.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.store_clothes = row['#roba']
#fi comerços
#domicilis
    def fill_flats(self):
        df = pd.read_csv('./data/' + 'domicilis_nacionalitat.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.flats_count = row['TOTAL']
            neighborhood.flats_nationals_only = row['TOTS ESPANYOLS']
            neighborhood.flats_foreigners_only = row['TOTS EXTRANGERS']
            neighborhood.flats_mixed = row['DOMICILIS_MIXTOS']

#web flat price
    def fill_neighborhood_rental_web(self):
        df = pd.read_csv('./data/' + 'plloguer_Idealista.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.avg_flat_rental_from_web = row['value']
            neighborhood.avg_flat_size = row['mean-size(m^2)']
            neighborhood.avg_flat_meter_rental = row['mean-price-size(€/m^2)']

    def fill_neighborhood_age_distr(self):
        df = pd.read_csv('./data/' + 'poblacio_anys_homo.csv')
        for index, row in df.iterrows():
            neighborhood = self.neighborhoods[row['id']]
            neighborhood.age_child = row['nens']
            neighborhood.age_young = row['joves']
            neighborhood.age_adult = row['adults']
            neighborhood.age_old   = row['avis']
    #...do the same for all neighborhood statistics

    def fill_neighborhood_geometry(self):
        import json
        json_data = open('./data/polygons_neighborhoods_geo.json').read()
        data = json.loads(json_data)
        for item in data['features']:
            #print(item['properties'])
            properties = item['properties']
            district_id = int(properties['C_Distri'])
            assert district_id in self.districts.keys()
            self.districts[district_id].name = properties['N_Barri']

            neighborhood_id = int(properties['C_Barri'])
            assert neighborhood_id in self.neighborhoods.keys()
            neighborhood = self.neighborhoods[neighborhood_id]
            neighborhood.men = int(properties['Homes'])
            neighborhood.women = int(properties['Dones'])
            neighborhood.geometry = Geometry()
            neighborhood.geometry.area = properties['Area']
            neighborhood.geometry.perimiter = properties['Perim']

            coords = item['geometry']['coordinates'][0]
            neighborhood.geometry.polygon = []
            for coord in coords:
                point = Point(coord[0],coord[1])
                #print(point.x,point.y)
                neighborhood.geometry.polygon.append(point)

    def fill_district_geometry(self):
        #imitate code of neighborhoods polygon
        import json
        json_data = open('./data/polygons_districts_geo.json').read()
        data = json.loads(json_data)
        for item in data['features']:
            #print(item['properties'])
            properties = item['properties']
            district_id = int(properties['C_Distri'])
            assert district_id in self.districts.keys()
            district = self.districts[district_id]
            district.men = int(properties['Homes'])
            district.women = int(properties['Dones'])
            district.geometry = Geometry()
            district.geometry.area = properties['Area']
            district.geometry.perimiter = properties['Perim']
            coords = item['geometry']['coordinates'][0]
            district.geometry.polygon = []
            for coord in coords:
                point = Point(coord[0],coord[1])
                #print(point.x,point.y)
                district.geometry.polygon.append(point)


    """def fill_grapho_metro(self):
                            Ledgelist=pd.read_csv('./data/' +'Ledgelist.csv', header=0)#edge list
                            Lnodelist=pd.read_csv('./data/' +'Lnodelist.csv', header=0)#node list
                            #This should build the networkx instances
                            g=nx.Graph()
                            for i, node in Lnodelist.iterrows():
                                g.add_node(node['name'], node[1:].to_dict())
                            for i, elrow in Ledgelist.iterrows():
                                g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())"""		