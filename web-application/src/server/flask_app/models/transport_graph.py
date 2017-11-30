from .base import Base
import geopy as gp
import geopy.distance
import networkx as nx
import pandas as pd
class TransportGraph(Base):
    def __init__(self):
        pass

    def constructGraph(self):
        Ledgelist=pd.read_csv('./data/' +'Ledgelist.csv', header=0)#edge list
        Lnodelist=pd.read_csv('./data/' +'Lnodelist.csv', header=0)#node list
        #This should build the networkx instances
        g=nx.Graph()
        for i, node in Lnodelist.iterrows():
            g.add_node(node['name'], node[1:].to_dict())
        for i, elrow in Ledgelist.iterrows():
            g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
        return g

    def shortpath(self, source,target):
        ruta=nx.shortest_path(g, source, target, weight="weight")
        l=nx.shortest_path_length(g, source, target, weight="weight")
        v=26.0#km/h
        t = (l/v)*60.0+1.2*len(ruta)#Sumo 1.2 minutos de espera por cada parada 
        return [t, ruta]

    def calculateRouteBetween(self, A, B):
        init = gp.Point(i)
        #finiq = gp.Point(f)
        distsini = [gp.distance.distance(init,gp.Point(np.hstack([Lnodelist.loc[i,'Lat'],Lnodelist.loc[i,'Lon']]))).km for i in range(len(Lnodelist['Lat']))]
        idxini = np.argmin(distsini)

        finiq = gp.Point(f)
        distsfin = [gp.distance.distance(finiq,gp.Point(np.hstack([Lnodelist.loc[i,'Lat'],Lnodelist.loc[i,'Lon']]))).km for i in range(len(Lnodelist['Lat']))]
        idxfin = np.argmin(distsfin)

        source=Lnodelist.loc[idxini,'name']
        target=Lnodelist.loc[idxfin,'name']
        t,ruta=shortpath(source,target)
        v=4#km/h
        tfin=((idxini/v)+(idxfin/v))+t  

        return [tfin, ruta]