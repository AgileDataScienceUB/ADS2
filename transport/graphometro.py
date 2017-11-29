# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 20:04:43 2017

@author: USER
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import copy
import geopy as gp
import geopy.distance 

Ledgelist=pd.read_csv("Ledgelist.csv", header=0)#edge list
Lnodelist=pd.read_csv("Lnodelist.csv", header=0)#node list

g=nx.Graph()
for i, node in Lnodelist.iterrows():
    g.add_node(node['name'], node[1:].to_dict())
for i, elrow in Ledgelist.iterrows():
    g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
    
plt.figure(figsize=(10, 10))
nx.draw_networkx(g, node_size=20, node_color='black')
plt.title('Graph Representation of metro', size=15)
plt.show()

##Funció que retorna el tems del camí més curt
source="Universitat"
target="Clot"

def shortpath(source,target):
    ruta=nx.shortest_path(g, source, target, weight="weight")
    l=nx.shortest_path_length(g, source, target, weight="weight")
    v=26
    t = (l/v)*60+1.2*len(ruta)#Sumo 1.2 minutos de espera por cada parada 
    return(t,ruta)

#t, ruta = shortpath(source,target)

print("Tiempo medio:",t,"min")
print("Ruta:",ruta)

i = [41.374638, 2.115991]
init = gp.Point(i)
f = [41.407219, 2.163054]
init1 = gp.Point(i)
gp.distance.distance(init,init1)
def near(f,i):
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
    return(tfin,ruta)
    
near(f,i)