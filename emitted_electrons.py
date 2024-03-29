#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:54:15 2022

@author: Ludmilla Allard

Tables 2 and 3 from Kaastra and Mewe (1993):
https://ui.adsabs.harvard.edu/abs/1993A%26AS...97..443K/abstract

Z: atomic number
st: ionisation stage
s: initial inner-shell vacancy
il: type of fluorescence transition
w: fluorescence yield

Recap of all functions:

correspondence(Z, st, s, il): used to give the details of each ionisation in the graph legend/ title
Z_st_s_idx(table, Z, st, s): returns indexes of Z, st and s for chosen table

electrons(Z, st, s): number distribution of emitted electrons for a given element, ionisation stage and initial inner-shell vacancy.
all_electrons(S): mean number distribution of emitted electrons for all neutral atoms and a given inner shell.
fluo_yield(Z, il): fluorescence yield for all ions of an element.
energy(Z, s): energy distribution (ionisation and Auger electron) for all ions of a given element and inner shell.
energy_st(Z, s): energy per number of electrons for a given ionisation stage of an element and a given inner shell.
all_fluo_yield(st, il): fluorescence yield for all enutral atoms for a given fluorescence transition.

avg_photon(Z, st, s): was used to obtain the table with the mean number of electrons and the mean number and photons energy
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

def Z_st_s_idx(table, Z, st, s):
    Z_idx = np.where(table[:, 0] == Z)
    Z_idx = Z_idx[0]
    
    if len(Z_idx) > 1 :
        st_idx = np.where(table[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 1] == st)
    elif (len(Z_idx) == 1):
        st_idx = np.where(table[Z_idx[0], 1] == st)
    st_idx = st_idx[0]
    
    if len(st_idx) > 1:
        s_idx = np.where(table[Z_idx[0]+st_idx[0]:Z_idx[0]+st_idx[0]+(len(st_idx)-1)+1, 2] == s)
    elif (len(st_idx) == 1):
        s_idx = np.where(table[Z_idx[0]+st_idx[0], 2] == s)
    else:
        return(Z_idx, st_idx, [])
    s_idx = s_idx[0]
    return(Z_idx, st_idx, s_idx)


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

    electron_nb = []
    for z in range(5,30) :
        Z_idx = np.where(fluo_tab[:, 0] == z)
        Z_idx = Z_idx[0]
        if S==1:
            e_nb = 0
            s_idx = np.where(fluo_tab[Z_idx[0]: Z_idx[len(Z_idx)-1]+1, 2]==S)
            s_idx = s_idx[0]
            if fluo_tab[Z_idx[0] + s_idx[S-1], 1] == 1 and fluo_tab[Z_idx[0] + s_idx[S-1], 0] == z and fluo_tab[Z_idx[0] + s_idx[S-1], 2] == S:
                for i in range(len(s_idx)):
                    e_nb += fluo_tab[Z_idx[0]+s_idx[i], 3] # number of electrons
                electron_nb = np.append(electron_nb, e_nb)
            
            
    
    # Plotting the graph
    #plt.figure()
    gap = correspondence(0, 0, S, 0)[2]    # the only useful value is the gap type
    x = np.arange(6,31)
    plt.plot(x, electron_nb , drawstyle = 'steps', label = gap + "-shell vacancy")
    plt.title("Electrons emitted during the decay of an inner-shell vacancy")
    plt.legend()
    plt.xlabel("Atomic number")
    plt.ylabel("Number of Auger electrons")
    #plt.savefig("nb_of_electrons_" + gap + "-shell.png")
    return(electron_nb)


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
    ionisation = np.zeros(len(s_idx))
    
    plt.figure()
    element= correspondence(Z, 0, s, 0)[0]
    gap = correspondence(Z, 0, s, 0)[2]
    
    plt.plot(e_nb, energy, drawstyle = 'steps', label = gap+" shell vacancy")
    plt.title("Energy for " + element)
    plt.legend()
    plt.xlabel("number of electrons")
    plt.ylabel("energy (eV)")
    #plt.savefig("energy_per_electron_"+element+"_"+gap+"-shell.png")
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


def avg_photon(Z, st, s):
    if Z>4:
        Z_idx, st_idx, s_idx = Z_st_s_idx(fluo_tab, Z, st, s)
    Z_idx2, st_idx2, s_idx2 = Z_st_s_idx(table, Z, st, s)
    avg_N = 0
    avg_E = 0
    
    # Calculating the average number of Auger electron emitted N_e
    if len(s_idx2) > 1:
        proba = table[Z_idx2[0]+st_idx2[0]+s_idx2[0]:Z_idx2[len(s_idx2)-1]+1, 6:]/10000
        E_e = table[Z_idx2[0]+st_idx2[0]+s_idx2[0]:Z_idx2[len(s_idx2)-1]+1, 4]
    elif len(s_idx2) == 1:
        proba = table[Z_idx2[0]+st_idx2[0]+s_idx2[0], 6:]/10000
        E_e = table[Z_idx2[0]+st_idx2[0]+s_idx2[0], 4]
    else:
        return([])
    
    N_e = 0
    for n in range(len(proba)):
        N_e += proba[n]*n    # n instead of n+1 to remove the photo-electron (1-10 electrons -> 0-9 Auger electrons)
    if Z<5:
        return(Z, st, s, N_e, E_e, 0, 0)
    
    # Calculating the average photon number avg_N and the average photon energy avg_E
    MAX = int(max(fluo_tab[:, 3]))
    for delta in range(MAX+1):
        if len(s_idx) > 1:
            D_idx = np.where(fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0]:Z_idx[0]+st_idx[0]+s_idx[len(s_idx)-1]+1, 3] == delta)
        elif len(s_idx) == 1:
            D_idx = np.where(fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0], 3] == delta)
        elif len(s_idx2)!=0:
            return(Z, st, s, N_e, E_e, 0, 0)    # we can stop now because there is no fluorescent yield in that situation
        else:
            return([])
        
        D_idx = D_idx[0]
        if len(D_idx)>1:
            w = fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0]:Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0]+len(D_idx),6]
            E_p_all = fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0]:Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0]+len(D_idx),5]
        elif len(D_idx)==1:
            w = fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0], 6]
            E_p_all = fluo_tab[Z_idx[0]+st_idx[0]+s_idx[0]+D_idx[0], 5]
        else:
            w = []
            E_p_all = []
        
        N_p = np.zeros(MAX+1)     # number of emitted photons
        E_p = np.zeros(MAX+1)
        if type(w)==np.float64:
            N_p[delta] += w
            E_p[delta] += E_p_all*w
        else:
            for il in range(len(w)):
                N_p[delta] += w[il]
                E_p[delta] += E_p_all[il]*w[il]
        avg_N+=proba[delta]*N_p[delta]
        avg_E+=proba[delta]*E_p[delta]
    return(Z, st, s, N_e, E_e, avg_N, avg_E)



"""
Applications of the functions
"""

#electrons(26, 1, 1)   # Fe I with K-shell vacancy

# graphs for the K, L_1 and M_1 shell vacancies:
#all_electrons(1), all_electrons(2), all_electrons(5)

# K alpha and K beta fluorescence for all ions of iron:
#fluo_yield(26, (1, 2)), fluo_yield(26, (3, 4))


# All fluorescence yields of neutral elements:
"""
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
all_fluo_yield(st, (16,17)), all_fluo_yield(st, 18), all_fluo_yield(st, 19), all_fluo_yield(st, (20,21)), all_fluo_yield(st, 22)
"""

# Oxygen ions energy:
#energy(8, 1)

# Ions energy for each ionisation stage (shown as the most probable number of electrons)
#energy_st(8, 1)

# Average number of photons, average photon energy and average number of Auger electrons for oxygens atoms with a K_shell vacancy
#avg_photon(8, 1, 1)


"""
oxygen_tab = []
for st in range(1, 5):
    oxygen_tab = np.append(oxygen_tab, avg_photon(8, st, 1))
Q = np.reshape(oxygen_tab, (4, 7))
"""


"""
energy_tab = []
for Z in range(4, 31):
    for st in range(1, 28):
        for s in range(1, 8):
            #print(Z, st, s)
            energy_tab = np.append(energy_tab, avg_photon(Z, st, s))
energy_tab = np.reshape(energy_tab, (1090, 7))
"""