#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:54:15 2022

@author: Ludmilla Allard

Modelling of the average number of electrons emitted during an inner-shell ionisation of an element (Z = 4-30).

The function electrons(Z, st, s) plots the graph of the probability distribution of the number of electrons emitted for a given element, ionisation stage and initial vacany position.
The function all_electrons() plots the average number of emitted electrons in function of the atomic number for different shell vacancy.

Table 2 from:
https://ui.adsabs.harvard.edu/abs/1993A%26AS...97..443K/abstract

Z : atomic number
st : ionisation stage
s : shell with the initial vacancy
"""

import numpy as np
import matplotlib.pylab as plt

table = np.loadtxt("table2")   # importing the data
elements = np.loadtxt("elements_names", dtype = str)    # importing the names of Z, st and s (used in the legend of the graphs)
stages = np.loadtxt("ionisation_stages", dtype = str)
gaps = np.loadtxt("initial_gap", dtype = str)


def correspondence(Z, st, s):   # used to give the details of each ionisation in the graph legend/ title
    return elements[Z-1], stages[st-1], gaps[s-1]


def electrons(Z, st, s):
    # extracting the right Z and ionisation stage indexes from the data
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    if len(Z_idx) > 1 :
        st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1], 1] == st)
    elif (len(Z_idx) == 1):
        st_idx = np.where(table[Z_idx[0], 1] == st)    
    st_idx = st_idx[0]  # before that, st_idx is a tuple of a single array
    
    # turning Z, st and s into their corresponding names (for a more detailled graph)
    element, stage, gap =  correspondence(Z, st, s)
    
    # plotting the graph
    plt.figure()
    x= np.arange(1,11)  # number of electrons

    if ((len(st_idx) != 0) and (len(st_idx) != 1)) :
        y_global = table[Z_idx[0]+st_idx[0]:Z_idx[0]+st_idx[0]+(len(st_idx)-1), 6:16]/10000 # probability for each vacancy position
        y = y_global[s-1]   # probability for a specific vacancy
    
    elif (len(st_idx) == 1):
        y_global = table[Z_idx[0]+st_idx[0], 6:16]/10000 # probability for each vacancy position
        y = y_global   # there is only one vacancy possible
    
    plt.plot(x, y , drawstyle = 'steps', label = element + " " + stage)
    plt.title(gap + "-shell ionisation of " + element + " " + stage + " (Z = " + str(Z) + ")")
    plt.legend()
    plt.xlabel("Number of emitted electrons")
    plt.ylabel("Probability")
    plt.savefig('graph_' + element + '_' + stage + '_' + gap + '.png')

"""
# examples : Fe I and Cr XII
electrons(26, 1, 1)   # Fe I
electrons(24, 12, 3)    # Cr XII
"""

def all_electrons(S) :  # the only variable is the intial shell vacancy. Three choices : K (1), L_1 (2) or M_1 (3)
    
    electrons_nb = []
    Z_elec = []
    for z in range(4,30) :  # iterating for each neutral atom (Z: 4-30)
        Z_idx = np.where(table[:, 0] == z)
        Z_idx = Z_idx[0]
        
        average = 0 # average number of electrons for a specific Z and inner shell vacancy
        proba = table[Z_idx[0] + S-1, 6:] # probability to get X electrons
        if table[Z_idx[0] + S-1, 1] == 1 and table[Z_idx[0] + S-1, 0] == z: # to make sure the right ionisation stage exists for this atom
            for i in range(len(proba)) :
                average += proba[i]*(i+1)
        
        Z_elec = np.append(Z_elec, average)
    electrons_nb = np.append(electrons_nb, Z_elec)/10000    # divided by 10000
    

    # Plotting the graph
    gap = correspondence(0, 0, S)[2]    # the only relevant data is the gap type
    x = np.arange(5,31)
    plt.plot(x, electrons_nb , drawstyle = 'steps', label = gap + "-shell vacancy")
    plt.title("Average number of electrons emitted during the decay of an inner-shell vacancy")
    plt.legend()
    plt.xlabel("Atomic number")
    plt.ylabel("Number of electrons")
    plt.savefig("nb_of_electrons_" + gap + "-shell.png")
    return(electrons_nb)


all_electrons(1), all_electrons(2), all_electrons(5)    # graphs for the K, L_1 and M_1 shell vacancies



