# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:27:59 2017

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

def grapho_metro(nodelist,edgelist):
    Ledgelist=pd.read_csv("Ledgelist.csv", header=0)#edge list
    Lnodelist=pd.read_csv("Lnodelist.csv", header=0)#node list
    g=nx.Graph()
    for i, node in Lnodelist.iterrows():
        g.add_node(node['name'], node[1:].to_dict())
    for i, elrow in Ledgelist.iterrows():
        g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
    return(g)