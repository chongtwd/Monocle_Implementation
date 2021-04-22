#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:40:24 2021

@author: David Chong Tian Wei
"""
import pygraphviz as pgv
import numpy as np
from Prims import Prims

def generate_graph(n=5):
    G = np.zeros(shape=(n,n))
    for i in range(n):
        for j in range(i+1,n):
            G[i,j] = np.random.randint(1,10)
            G[j,i] = G[i,j]
    return G

g = generate_graph()

G = pgv.AGraph(strict=True, directed=False)
G.add_nodes_from(range(g.shape[0]))
for i in range(g.shape[0]):
    for j in range(i+1, g.shape[0]):
        G.add_edge(str(i), str(j), label=str(g[i,j]))
G.layout(prog="dot")
G.draw("test.png")


mst = Prims(g)

for i in range(len(mst)):
    x = mst[i]
    e = G.get_edge(str(x[0]), str(x[1]))
    e.attr["color"] = "red"
    e.attr["fontcolor"] = "red"
    G.draw("test_mst_{}.png".format(i))
