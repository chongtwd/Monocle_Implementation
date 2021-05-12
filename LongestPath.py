#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:29:25 2021

@author: David Chong
"""
import numpy as np

def LongestPath(T):
    u = np.argmax([len(x) for x in bfs(T,0)])
    paths = bfs(T,u)
    return paths[np.argmax([len(x) for x in paths])]

def bfs(T, i):
    d = [[] for _ in range(len(T))]
    buffer = [[i]]
    while d.count([]) > 0:
        new_buffer = []
        for u in buffer:
            d[u[-1]] = u
        for u in buffer:
            new_buffer += [u + [x[0]] for x in T[u[-1]] if d[x[0]] == []]
        buffer = new_buffer
    return d