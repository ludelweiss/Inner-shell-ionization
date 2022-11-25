#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:54:15 2022

@author: Ludmilla Allard

Modelling of the average number of electrons emitted during an inner-shell ionisation of an element (Z = 4-30).

The function electrons(Z, st, s) plots the graph of the probability distribution of the number of electrons emitted for a given element, ionisation stage and initial vacany position.
The function all_electrons(S) plots the average number of emitted electrons in function of the atomic number for different shell vacancy.
The function fluo_yield(Z, il) plots a given fluorescence yield for all ions of an element.

Tables 2 and 3 from:
https://ui.adsabs.harvard.edu/abs/1993A%26AS...97..443K/abstract

Z: atomic number
st: ionisation stage
s: shell with the initial vacancy
il: type of inner-shell ionisation
w: fluorescence yield
"""

import numpy as np
import matplotlib.pylab as plt

table = np.loadtxt("table2")   # importing the data
elements = np.loadtxt("elements_names", dtype = str)    # importing the names of Z, st and s (used in the legend of the graphs)
stages = np.loadtxt("ionisation_stages", dtype = str)
gaps = np.loadtxt("initial_gap", dtype = str)
ils = np.loadtxt("il", dtype = str)
fluo_tab = np.loadtxt("table3")


def correspondence(Z, st, s, il):   # used to give the details of each ionisation in the graph legend/ title
    il = ils[il-1]
    return elements[Z-1], stages[st-1], gaps[s-1], il


def electrons(Z, st, s):
    # extracting the right Z and ionisation stage indexes from the data
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    if len(Z_idx) > 1 :
        st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 1] == st)
    elif (len(Z_idx) == 1):
        st_idx = np.where(table[Z_idx[0], 1] == st)
        
    st_idx = st_idx[0]  # before that, st_idx is a tuple of a single array
    
    element, stage, gap, il =  correspondence(Z, st, s, 0)  # turning Z, st and s into their corresponding names (for a more detailled graph)
    
    if ((len(st_idx) != 0) and (len(st_idx) != 1)) :
        proba_global = table[Z_idx[0]+st_idx[0]:Z_idx[0]+st_idx[0]+(len(st_idx)-1), 6:16]/10000 # probability for each vacancy position
        proba = proba_global[s-1]   # probability for a specific vacancy
    elif (len(st_idx) == 1):
        proba_global = table[Z_idx[0]+st_idx[0], 6:16]/10000 # probability for each vacancy position
        proba = proba_global   # there is only one vacancy possible
    

    # Plotting the graph
    plt.figure()
    x= np.arange(1,11)  # number of electrons
    plt.plot(x, proba , drawstyle = 'steps', label = element + " " + stage)
    plt.title(gap + "-shell ionisation of " + element + " " + stage + " (Z = " + str(Z) + ")")
    plt.legend()
    plt.xlabel("Number of emitted electrons")
    plt.ylabel("Probability")
    plt.savefig('graph_' + element + '_' + stage + '_' + gap + '.png')
    
    return(proba)


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
    #plt.figure()
    gap = correspondence(0, 0, S, 0)[2]    # the only relevant data is the gap type
    x = np.arange(5,31)
    plt.plot(x, electrons_nb , drawstyle = 'steps', label = gap + "-shell vacancy")
    plt.title("Electrons emitted during the decay of an inner-shell vacancy")
    plt.legend()
    plt.xlabel("Atomic number")
    plt.ylabel("Number of electrons")
    plt.savefig("nb_of_electrons_" + gap + "-shell.png")
    return(electrons_nb)


def fluo_yield(Z, il):  # if il is an array, the fluorescence yields will be added into a single fluorescence yield (example : K alpha_1 + K alpha_2 to get K alpha)
    Z_idx = np.where(fluo_tab[:, 0] == Z)
    Z_idx = Z_idx[0]
    w = np.empty(26)    # base array for the fluorescence yield for each ionisation stage
    w.fill(np.NaN)
    if type(il) == int:
        il = [il]
    il_name = ""  # for the graph legend
    
    for I in range(len(il)) :
        il_name = " ".join([il_name, correspondence(0, 0, 0, il[I])[3]])    # for the graph legend
        
        if len(Z_idx) > 1 :
            il_idx = np.where(fluo_tab[Z_idx[0]:Z_idx[len(Z_idx)-1], 4] == il[I])
        elif (len(Z_idx) == 1):
            il_idx = np.where(fluo_tab[Z_idx[0], 4] == il[I])    
        il_idx = il_idx[0]
        
        for st in range(Z):    # iteration for each ionisation stage
            for i in range(len(il_idx)):
                if fluo_tab[Z_idx[0] + il_idx[i], 1] == st+1 and fluo_tab[Z_idx[0] + il_idx[i], 0] == Z:
                    if np.isnan(w[st]) :
                        w[st] = fluo_tab[Z_idx[0]+il_idx[i], 6]
                    else :
                        w[st] += fluo_tab[Z_idx[0]+il_idx[i], 6]      
    # graph
    #plt.figure()
    element= correspondence(Z, 0, 0, 0)[0]
    x = np.arange(1, 27)
    plt.plot(x, w, drawstyle = 'steps', label = il_name)
    plt.title("Fluorescence yield for all ions of " + element)
    plt.legend()
    plt.xlabel("ionisation stage")
    plt.ylabel("fluorescence yield")
    #plt.savefig("fluorescence_yield" + il_name + ".png")
    return(w)

def energy(Z, s):
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    if len(Z_idx) > 1 :
        s_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 2] == s)

    elif (len(Z_idx) == 1):
        s_idx = np.where(table[Z_idx[0], 2] == s)
    s_idx = s_idx[0]
    
    energy_I = np.empty(26) # base tables for the energies
    energy_I.fill(np.NaN)
    energy_E = np.empty(26)
    energy_E.fill(np.NaN)
    
    for st in range(26):
        if len(Z_idx) > 1 :
            st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 1] == st+1)
        elif (len(Z_idx) == 1):
            st_idx = np.where(table[Z_idx[0], 1] == st+1)
        st_idx = st_idx[0]
        
        for ST in range(len(st_idx)):
            if table[Z_idx[0]+st_idx[ST], 2] == s and table[Z_idx[0]+st_idx[ST], 0] == Z:
                if np.isnan(energy_I[st]):
                    energy_I[st] = table[Z_idx[0]+st_idx[ST], 3]
                else:
                    energy_I[st] += table[Z_idx[0]+st_idx[ST], 3]
                if np.isnan(energy_E[st]):
                    energy_E[st] = table[Z_idx[0]+st_idx[ST], 4]
                else:
                    energy_E[st] += table[Z_idx[0]+st_idx[ST], 4]
    # graph
    plt.figure()
    element= correspondence(Z, 0, s, 0)[0]
    gap = correspondence(Z, 0, s, 0)[2]
    x = np.arange(1, 27)
    plt.plot(x, energy_I, drawstyle = 'steps', label = "Ionisation energy")
    plt.plot(x, energy_E, drawstyle = 'steps', label = "Average Auger electron energy")
    #plt.plot(x, energy_E + energy_I, drawstyle = 'steps', label = "Total")
    plt.title("Energy for " + element+" ("+gap+"-shell vacancy)")
    plt.legend()
    plt.xlabel("ionisation stage")
    plt.ylabel("energy (eV)")
    #plt.savefig("energy_"+element+"_"+gap+"-shell.png")
    return(energy_I, energy_E, energy_I + energy_E)



def energy_st(Z, s):
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    if len(Z_idx) > 1 :
        s_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 2] == s)
    elif (len(Z_idx) == 1):
        s_idx = np.where(table[Z_idx[0], 2] == s)
    s_idx = s_idx[0]
        
    energy = np.zeros(len(s_idx))
    
    #proba = table[Z_idx[0]+s_idx[0] : Z_idx[0]+s_idx[len(s_idx)-1]+1, 6:]/10000 # probability to get X electrons
    e_nb = np.zeros(len(s_idx)) # average number of electrons for a given Z and initial vacancy
    
    
    
    for c in range(len(s_idx)):
        if table[Z_idx[0] + s_idx[c], 2] == s and table[Z_idx[0] + s_idx[c], 0] == Z:
            proba = table[Z_idx[0]+s_idx[c], 6:]/10000
            energy[c] += table[Z_idx[0]+s_idx[c], 4]
            for i in range(len(proba)) :
                e_nb[c] += proba[i]*(i+1)
        
    # we need to sort the energy in ascending order
    zipped_lists = zip(e_nb, energy)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    e_nb, energy =  [list(tuple) for tuple in tuples]
    
    # graph
    plt.figure()
    element= correspondence(Z, 0, s, 0)[0]
    gap = correspondence(Z, 0, s, 0)[2]
    plt.plot(e_nb, energy, drawstyle = 'steps', label = gap+" shell vacancy")
    plt.title("Energy for " + element)
    plt.legend()
    plt.xlabel("number of electrons")
    plt.ylabel("energy (eV)")
    plt.savefig("energy_per_electron_"+element+"_"+gap+"-shell.png")
    return(e_nb, energy)


def all_fluo_yield(st, il):  # if il is an array, the fluorescence yields will be added into a single fluorescence yield (example : K alpha_1 + K alpha_2 to get K alpha)
    w = np.empty(30)    # base array for the fluorescence yield of a given element
    w.fill(np.NaN)
    for Z in range(5, 31):
        Z_idx = np.where(fluo_tab[:, 0] == Z)
        Z_idx = Z_idx[0]
        
        if type(il) == int:
            il = [il]
        il_name = ""  # for the graph legend
        
        for I in range(len(il)) :
            il_name = " ".join([il_name, correspondence(0, 0, 0, il[I])[3]])    # for the graph legend
            
            if len(Z_idx) > 1 :
                il_idx = np.where(fluo_tab[Z_idx[0]:Z_idx[len(Z_idx)-1], 4] == il[I])
            elif (len(Z_idx) == 1):
                il_idx = np.where(fluo_tab[Z_idx[0], 4] == il[I])    
            il_idx = il_idx[0]
            for i in range(len(il_idx)):
                if fluo_tab[Z_idx[0] + il_idx[i], 1] == st and fluo_tab[Z_idx[0] + il_idx[i], 0] == Z:
                    if np.isnan(w[Z-1]) :
                        w[Z-1] = fluo_tab[Z_idx[0]+il_idx[i], 6]
                    else :
                        w[Z-1] += fluo_tab[Z_idx[0]+il_idx[i], 6]  
    #graph
    #plt.figure()
    x = np.arange(1, 31)
    plt.plot(x, w, drawstyle = 'steps', label = il_name)
    plt.title("Fluorescence yield for all neutral atoms (Z=5-30)")
    plt.legend()
    plt.xlabel("atomic number")
    plt.ylabel("fluorescence yield")
    #plt.savefig("fluorescence_yield" + il_name + ".png")
    return(w)

"""
Applications of the functions
"""

#electrons(26, 1, 1)   # Fe I with K-shell vacancy

# graphs for the K, L_1 and M_1 shell vacancies:
#all_electrons(1), all_electrons(2), all_electrons(5)

# K alpha and K beta fluorescence for all ions of iron:
#fluo_yield(26, (1, 2)), fluo_yield(26, (3, 4))

# All fluorescence yields of neutral elements:

st = 1
# K-shell
plt.figure()
for il in range(1, 8, 2):
    all_fluo_yield(st, (il, il+1))

# L-shell
plt.figure()
for il in range(9, 13,):
    all_fluo_yield(st, il)
all_fluo_yield(st, (13,14)), all_fluo_yield(st, 15)

# M-shell
plt.figure()
A = all_fluo_yield(st, (16,17)), all_fluo_yield(st, 18), all_fluo_yield(st, 19), all_fluo_yield(st, (20,21)), all_fluo_yield(st, 22)


# Oxygen ions energy:
#energy(8, 1)

# Ions energy for each ionisation stage (shown as the most probable number of electrons)
#Z = energy_st(8, 1)






