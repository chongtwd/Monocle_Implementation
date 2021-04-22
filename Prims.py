#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:37:47 2021

@author: David Chong Tian Wei
"""

class BinaryHeap:
    """
    Implementation of a binary heap using list as underlying storage
    """
    def __init__(self, values=[], comparator = lambda x, y : x < y, identifier = lambda x : x):
        """
        The binary heap may be instantiated with a comparator to enable
        specification as max or min heap as well as to allow comparison
        of objects
        """
        self.store = []
        self.comparator = comparator
        self.identifier = identifier
        self.map = {}
        for x in values:
            self.add(x)
        
    def __len__(self):
        return len(self.store)
    
    def add(self, x):
        """
        When we add an element to the heap the rest of the list is already
        in the form of a heap, so we need only bubble the added element
        until the heap property is satisfied across the whole list
        """
        self.store.append(x)
        self.map[self.identifier(x)] = len(self.store) - 1
        i = len(self.store) - 1
        p = (i-1) // 2
        while p >= 0:
            if self.comparator(self.store[i], self.store[p]):
                self.__swap_nodes(self.store[i], self.store[p])
                i = p
                p = (i-1) // 2
            else:
                return
    
    def get(self):
        """
        When we remove the most extreme element, it will always be the root
        of the tree. We can then move the last element to the root without
        breaking the tree structure and then heapify to re-establish the heap
        property
        """
        output = self.store[0]
        self.remove(self.identifier(self.store[0]))
        i = 0
        j = self.__compare_children(i)
        while i != j:
            self.__swap_nodes(self.store[i], self.store[j])
            i = j
            j = self.__compare_children(i)
            
        return output
    
    def peek(self):
        return self.store[0]
    
    def remove(self, x):
        i = self.map[x]
        self.__swap_nodes(self.store[i], self.store[-1])
        self.store = self.store[:-1]
        del self.map[x]
        j = self.__compare_children(i)
        while i != j:
            self.__swap_nodes(self.store[i], self.store[j])
            i = j
            j = self.__compare_children(i)
    
    def update(self, k, v):
        i = self.map[k]
        if self.comparator(v, self.store[i]):
            self.remove(k)
            self.add(v)
    
    def __compare_children(self, i):
        if 2*i + 2 < len(self.store):
            if self.comparator(self.store[2*i+1], self.store[2*i+2]):
                if self.comparator(self.store[i], self.store[2*i+1]):
                    return i
                else:
                    return 2*i + 1
            else:
                if self.comparator(self.store[i], self.store[2*i+2]):
                    return i
                else:
                    return 2*i+2
        elif 2*i + 1 < len(self.store):
            if self.comparator(self.store[i], self.store[2*i+1]):
                return i
            else:
                return 2*i + 1
        else:
            return i
    
    def __swap_nodes(self, x, y):
        i = self.map[self.identifier(x)]
        j = self.map[self.identifier(y)]
        temp = self.store[i]
        self.store[i] = self.store[j]
        self.store[j] = temp
        self.map[self.identifier(x)] = j
        self.map[self.identifier(y)] = i
        
def Prims(G, inf=999999999):
    """
    Expect G to be an n x n ajacency matrix of an undirected graph
    """
    g = [] # Here we are just converting our adjacency matrix into an adjacency list representation of a graph
    for i in range(G.shape[0]):
        edges = []
        for j in range(0, G.shape[0]):
            if j == i:
                edges.append([j, inf])
            else:
                edges.append([j, G[i,j]])
        g.append(edges)
    # We use a binary heap to help us find the vertex with the smallest edge weight to connect to our growing MST
    Q = BinaryHeap([[i, None, inf] for i in range(len(g))], lambda x,y : x[2] < y[2], lambda x : x[0])
    # Storage for our growing MST
    mst = []
    # We keep track of all vertices in the graph and initially leave them as unmarked
    reached = {}
    for i in range(len(Q)):
        reached[i] = False
    # Start from any vertex
    i = 0
    while len(Q) > 1:
        reached[i] = True
        # Update the list of vertices with the smallest weight connected to our growing MST
        for x in g[i]:
            if not reached[x[0]]:
                Q.update(x[0], [x[0], i, x[1]])
        v, u, w = Q.get() # Get the edge and vertex of smallest weight
        mst.append((u, v, w)) # Add the edge and vertex to our growing MST
        i = v
    return mst