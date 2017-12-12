from .base import Base
import geopy as gp
import geopy.distance
import networkx as nx
import pandas as pd
import numpy as np

class TransportGraph(Base):
    def __init__(self):
        self.Ledgelist = pd.read_csv('./data/' +'Ledgelist.csv', header=0)#edge list
        self.Lnodelist = pd.read_csv('./data/' +'Lnodelist.csv', header=0)#node list
        self.g = self.constructGraph()

    def constructGraph(self):
        
        #This should build the networkx instances
        g=nx.Graph()
        for i, node in self.Lnodelist.iterrows():
            g.add_node(node['name'], node[1:].to_dict())
        for i, elrow in self.Ledgelist.iterrows():
            g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
        return g

    def shortpath(self, source,target):
        ruta=nx.shortest_path(self.g, source, target, weight="weight")
        l=nx.shortest_path_length(self.g, source, target, weight="weight")
        print(l)
        v=80.0#km/h
        t = (l/v)*60.0+1.2*len(ruta)#Sumo 1.2 minutos de espera por cada parada 
        return [t, ruta]

    def calculateRouteBetween(self, i,f):
        init = gp.Point(i)
        #finiq = gp.Point(f)
        distsini = [gp.distance.distance(init,gp.Point(np.hstack([self.Lnodelist.loc[i,'Lat'],self.Lnodelist.loc[i,'Lon']]))).km for i in range(len(self.Lnodelist['Lat']))]
        idxini = np.argmin(distsini)

        finiq = gp.Point(f)
        distsfin = [gp.distance.distance(finiq,gp.Point(np.hstack([self.Lnodelist.loc[i,'Lat'],self.Lnodelist.loc[i,'Lon']]))).km for i in range(len(self.Lnodelist['Lat']))]
        idxfin = np.argmin(distsfin)

        source=self.Lnodelist.loc[idxini,'name']
        target=self.Lnodelist.loc[idxfin,'name']
        t,ruta=self.shortpath(source,target)
        v=4#km/h
        tfin=((idxini/v)+(idxfin/v))+t  

        return [tfin, ruta]