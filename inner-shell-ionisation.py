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
#correspondence = np.loadtxt("correspondence")

def graph(Z, st, s):
    # first step : extracting the right Z and ionisation stage indexes from the data
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1], 1] == st)     
    st_idx = st_idx[0]
    
    # second step : plotting the graph
    x= np.arange(1,11)  # number of electrons
    
    y_global = table[Z_idx[0]:Z_idx[0]+(len(st_idx)-1), 6:16]/10000 # probability for each vacancy position
    y = y_global[s-1]   # probability for a specific vacancy
    
    plt.plot(x, y , drawstyle = 'steps', label="Element I")
    plt.title("-shell ionisation of Z")
    plt.xlabel("Number of emitted electrons")
    plt.ylabel("Probability")
    
graph(26, 1, 1)   # example with Fe I

