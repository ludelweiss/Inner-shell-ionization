#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:49:33 2022

@author: Ludmilla Allard

Modelling of the average number of electrons emitted during a K-shell ionisation of Fe
(only Fe I)

Table 2 from:
https://ui.adsabs.harvard.edu/abs/1993A%26AS...97..443K/abstract
"""
import numpy as np
import matplotlib.pylab as plt

"""
Z = 26  # atomic number (Fe)
st = 1  # ionisation stage
s = 1 # shell with the initial vacancy
"""

table2 = np.loadtxt("table2")   # importing the data

Z = table2[:, 0]
Z_Fe = np.where(Z == 26)  # extracting the right atomic number
Z_Fe = Z_Fe[0]  # turning Z_Fe into an array with the indexes (instead of a tuple)

st_Fe = np.where(table2[Z_Fe[0]:Z_Fe[len(Z_Fe)-1], 1] == 1) # extracting the right ionisation stage
st_Fe = st_Fe[0]    # turning into an array with the indexes

s_Fe = np.where(table2[Z_Fe[0]: Z_Fe[0]+(len(st_Fe)-1), 2] == 1)    # extracting the shell with the initial vacancy

"""
Creating the graph (probability of getting X emitted electrons)
"""

x = np.arange(1,11)
y_global = table2[Z_Fe[0]:Z_Fe[0]+(len(st_Fe)-1), 6:16]
y = y_global[0,:]/10000

plt.plot(x, y, drawstyle = 'steps', label = "Fe I")
plt.title("K-shell ionisation of Fe")
plt.xlabel("Number of emitted electrons")
plt.ylabel("Probability")