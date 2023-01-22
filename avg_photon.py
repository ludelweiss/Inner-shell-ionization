#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:05:26 2022

@author: Ludmilla Allard

All functions are using the new table created in emitted_electrons.py

Recap of all functions:

energy_st(Z, s): number and energy distributions of emitted electrons and photons for each ionisation stage for a given atomic number and inner shell.
energy_Z(s): number and energy distributions of emitted electrons and photons for all neutral atoms and a given inner shell.
"""

import numpy as np
import matplotlib.pylab as plt
from emitted_electrons import correspondence, Z_st_s_idx

tab = np.loadtxt("avg_photons_electrons2")


def energy_st(Z, s):
    Z_idx = Z_st_s_idx(tab, Z, 0, s)[0]
    if len(Z_idx) > 1 :
        s_idx = np.where(tab[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 2] == s)
    elif (len(Z_idx) == 1):
        s_idx = np.where(tab[Z_idx[0], 2] == s)
    s_idx = s_idx[0]
    
    E_e = np.empty(26)
    E_e.fill(np.NaN)
    E_p = np.empty(26)
    E_p.fill(np.NaN)
    N_e = np.empty(26)
    N_e.fill(np.NaN)
    N_p = np.empty(26)
    N_p.fill(np.NaN)
        
    for st in range(26):
        if len(Z_idx) > 1 :
            st_idx = np.where(tab[Z_idx[0]:Z_idx[len(Z_idx)-1]+1, 1] == st+1)
        elif (len(Z_idx) == 1):
            st_idx = np.where(tab[Z_idx[0], 1] == st+1)
        st_idx = st_idx[0]
        
        for ST in range(len(st_idx)):
            if tab[Z_idx[0]+st_idx[ST], 2] == s and tab[Z_idx[0]+st_idx[ST], 0] == Z:
                if np.isnan(E_e[st]):
                    E_e[st] = tab[Z_idx[0]+st_idx[ST], 4]
                else:
                    E_e[st] += tab[Z_idx[0]+st_idx[ST], 4]
                if np.isnan(E_p[st]):
                    E_p[st] = tab[Z_idx[0]+st_idx[ST], 6]
                else:
                    E_p[st] += tab[Z_idx[0]+st_idx[ST], 6]
                if np.isnan(N_e[st]):
                    N_e[st] = tab[Z_idx[0]+st_idx[ST], 3]
                else:
                    N_e[st] += tab[Z_idx[0]+st_idx[ST], 3]
                if np.isnan(N_p[st]):
                    N_p[st] = tab[Z_idx[0]+st_idx[ST], 5]
                else:
                    N_p[st] += tab[Z_idx[0]+st_idx[ST], 5]
    
    st_tab = np.arange(1, 27)
    
    # multiplicator for the photon energy if needed (because it is much lower than the electron energy)
    multiplicator = 1
    E_p = [i*multiplicator for i in E_p]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(st_tab, E_e, drawstyle='steps', color='tab:blue', label="electrons energy")
    ax.plot(st_tab, E_p, '--', drawstyle='steps', color='tab:blue', label="photons energy (x"+str(multiplicator)+")")
    ax2.plot(st_tab, N_e, drawstyle="steps", color='tab:orange', label="number of Auger electrons")
    ax2.plot(st_tab, N_p, '--', drawstyle="steps", color='tab:orange', label="number of photons")
    ax.set_ylabel('Energy (eV)', color='tab:blue')
    ax2.set_ylabel("number of photons/ electrons", color='tab:orange')
    
    plt.title("Z="+str(Z)+" and s="+str(s))
    ax.set_xlabel("Ionisation stage")
    ax.legend(loc="lower right")
    ax2.legend()
    return(N_e, E_e, E_p)
    

def energy_Z(s):
    E_e = []
    E_p = []
    N_e = []
    N_p = []
    gap = correspondence(0, 0, s, 0)[2]
    
    for Z in range(4, 31):
        Z_idx, st_idx, s_idx = Z_st_s_idx(tab, Z, 1, s)
        if len(s_idx)<1:
            E_e = np.append(E_e, np.NaN)
            E_p = np.append(E_p, np.NaN)
            N_e = np.append(N_e, np.NaN)
            N_p = np.append(N_p, np.NaN)
        else: 
            E_e = np.append(E_e, tab[Z_idx[0]+st_idx[0]+s_idx[0], 4])
            E_p = np.append(E_p, tab[Z_idx[0]+st_idx[0]+s_idx[0], 6])
            N_e = np.append(N_e, tab[Z_idx[0]+st_idx[0]+s_idx[0], 3])
            N_p = np.append(N_p, tab[Z_idx[0]+st_idx[0]+s_idx[0], 5])
    
    Z_tab = np.arange(4, 31)
    multiplicator = 1
    E_p = [i*multiplicator for i in E_p]
    
    
    # Energy distribution
    plt.figure()
    plt.plot(Z_tab, E_e , drawstyle = 'steps', color = "tab:orange", label = "electrons")
    plt.plot(Z_tab, E_p, '--', drawstyle='steps', color='tab:orange', label="photons")
    plt.title("Neutral atoms with a "+gap+"-shell gap")
    plt.legend()
    plt.ylabel("Mean energy (eV)")
    plt.xlabel("Atomic number")
    plt.savefig("mean_energy_"+gap+"-shell.png")
    
    # Number distribution
    plt.figure()
    plt.plot(Z_tab, N_e , drawstyle = 'steps', color = "tab:blue", label = "electrons")
    plt.plot(Z_tab, N_p, '--', drawstyle='steps', color='tab:blue', label="photons")
    plt.title("Neutral atoms with a "+gap+"-shell gap")
    plt.legend()
    plt.ylabel("Number of electrons/ photons")
    plt.xlabel("Atomic number")
    plt.savefig("mean_number_"+gap+"-shell.png")
    
    #Both distributions on the same graph (two axis)
    """
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax2.plot(Z_tab, N_e, drawstyle="steps", color='tab:orange', label="number of electrons")
    ax2.plot(Z_tab, N_p, '--', drawstyle="steps", color='tab:orange', label="number of photons")
    ax.plot(Z_tab, E_e, drawstyle='steps', color='tab:blue', label="electrons energy")
    ax.plot(Z_tab, E_p, '--', drawstyle='steps', color='tab:blue', label="photons energy (x"+str(multiplicator)+")")
    ax2.set_ylabel('number of photons/ electrons', color='tab:orange')
    ax.set_ylabel('Energy (eV)', color='tab:blue')
    plt.title("Neutral atoms with a "+gap+"-shell gap")
    ax.set_xlabel("Atomic number")
    ax.legend(loc="lower right")
    ax2.legend()
    """
    return(N_e, E_e, E_p)

"""
# graphs for all inner shells
for I in range(1, 8):
    A= energy_Z(I)
"""

