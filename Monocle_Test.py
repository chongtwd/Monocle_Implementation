#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:54:50 2021

@author: David Chong
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Prims import Prims
from LongestPath import LongestPath
from sklearn.decomposition import FastICA
from scipy.spatial.distance import pdist, squareform

data = np.log(pd.read_csv("GSE52529_fpkm_matrix.txt", sep="\t").T + 1)
ica = FastICA(2)
projection = ica.fit_transform(data)
G = squareform(pdist(projection))

mst = Prims(G)

plt.figure(figsize=(10,10))
plt.scatter(projection[:,0], projection[:,1])
plt.xlabel("IC 2")
plt.ylabel("IC 1")
for i in range(len(mst)):
    for e in mst[i]:
        p1 = projection[i,:]
        p2 = projection[e[0], :]
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]], color="r")
        
lp = LongestPath(mst)

for i in range(len(lp)-1):
    p1 = projection[lp[i],:]
    p2 = projection[lp[i+1],:]
    plt.plot([p1[0],p2[0]], [p1[1],p2[1]], color="g")

plt.title("GSE52529 Trajectory")
plt.savefig("GSE52529_MST.png")
plt.close()

print("Length of longest path through MST : %d" % len(lp))

# Try to project a cell onto a particular step in development?
# Using each cell along the longest path as a representative cell 
# we assign each cell to the nearest representitive cell
bins = [[x] for x in lp]

for x in np.delete(range(G.shape[0]), lp):
    bins[np.argmin(G[x, lp])].append(x)

plt.figure()
plt.bar(range(len(bins)), [len(x) for x in bins])
plt.ylabel("Number of cells")
plt.xlabel("Step in pseudotime")
plt.title("Fine pseudotime")
plt.savefig("GSE52529_Fine_Pseudotime.png")

# Lets try having a bit coarser pseudoime
bins = [lp[x:x+5] for x in range(0,len(lp), 5)]
for x in np.delete(range(G.shape[0]), lp):
    bins[np.argmin(G[x, lp]) // 5].append(x)

plt.figure()
plt.bar(range(len(bins)), [len(x) for x in bins])
plt.ylabel("Number of cells")
plt.xlabel("Step in pseudotime")
plt.title("Coarse pseudotime")
plt.savefig("GSE52529_Coarse_Pseudotime.png")
plt.close()

# Use cells in each bin to calculate mean gene expression for each gene
g_expr = np.zeros((data.shape[1], len(bins)))

for i in range(len(bins)):
    cells = data.iloc[bins[i],:]
    g_expr[:,i] = cells.mean(axis=0).values

myog_index = [x.split(".")[0] for x in data.columns].index("ENSG00000122180")

plt.figure()
plt.plot(range(len(bins)), g_expr[myog_index,:])
plt.xlabel("Pseudotime")
plt.ylabel("Gene expression")
plt.title("MYOG gene expression over pseudotime")
plt.savefig("MYOG_Pseudotime_expr.png")
plt.close()
