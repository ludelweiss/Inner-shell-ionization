#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:54:15 2022

@author: Ludmilla Allard

Modelling of the average number of electrons emitted during an inner-shell ionisation of an element (Z = 4-30).
The function graph(Z, st, s) plots the graph of the probability distribution of the number of electrons emitted for a given element, ionisation stage and initial vacany position.

Table 2 from:
https://ui.adsabs.harvard.edu/abs/1993A%26AS...97..443K/abstract

Z : atomic number
st : ionisation stage
s : shell with the initial vacancy
"""

import numpy as np
import matplotlib.pylab as plt

table = np.loadtxt("table2")   # importing the data
elements = np.loadtxt("elements_names", dtype = str)
stages = np.loadtxt("ionisation_stages", dtype = str)
gaps = np.loadtxt("initial_gap", dtype = str)
"""
element = "Fe"
stage = "I"
gap = "K"
"""
def correspondence(Z, st, s):
    return elements[Z-1], stages[st-1], gaps[s-1]


def graph(Z, st, s):
    # extracting the right Z and ionisation stage indexes from the data
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1], 1] == st)     
    st_idx = st_idx[0]
    
    # turning Z, st and s into their corresponding names (for a more detailled graph)
    element, stage, gap =  correspondence(Z, st, s)
    
    # plotting the graph
    x= np.arange(1,11)  # number of electrons
    
    y_global = table[Z_idx[0]:Z_idx[0]+(len(st_idx)-1), 6:16]/10000 # probability for each vacancy position
    y = y_global[s-1]   # probability for a specific vacancy
    
    plt.plot(x, y , drawstyle = 'steps', label = element + " " + stage)
    plt.title(gap + "-shell ionisation of " + element + " " + stage)
    plt.legend()
    plt.xlabel("Number of emitted electrons")
    plt.ylabel("Probability")
    #plt.savefig('graph.png')
    
graph(26, 1, 1)   # example with Fe I