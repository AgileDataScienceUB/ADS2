# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:51:04 2017

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


def shortpath(source,target):
    ruta=nx.shortest_path(g, source, target, weight="weight")
    l=nx.shortest_path_length(g, source, target, weight="weight")
    v=26
    t = (l/v)*60+1.2*len(ruta)#Sumo 1.2 minutos de espera por cada parada 
    return(t,ruta)


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
    return(t,ruta)