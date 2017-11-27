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
source="Bellvitge"
target="Joanic"

def shortpath(source,target):
    ruta=nx.shortest_path(g, source, target, weight="weight")
    l=nx.shortest_path_length(g, source, target, weight="weight")
    v=26
    t = (l/v)*60+1.2*len(ruta)#Sumo 1.2 minutos de espera por cada parada 
    return(t)

print("Tiempo medio:",round(shortpath(source,target),3),"min")