#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:05:26 2022

@author: Ludmilla Allard
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
    
    st_tab = np.arange(1, 27)
    multiplicator = 10
    E_p = [i*multiplicator for i in E_p]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(st_tab, E_e, '--', drawstyle='steps', color='tab:blue', label="electrons energy")
    ax.plot(st_tab, E_p, drawstyle='steps', color='tab:blue', label="photons energy (x"+str(multiplicator)+")")
    ax2.plot(st_tab, N_e, drawstyle="steps", color='tab:orange')
    ax.set_ylabel('Energy (eV)', color='tab:blue')
    ax2.set_ylabel('number of Auger electrons', color='tab:orange')
    
    plt.title("Z="+str(Z)+" and s="+str(s))
    ax.set_xlabel("Ionisation stage")
    ax.legend()
    return(N_e, E_e, E_p)
    

def energy_Z(s):
    E_e = []
    E_p = []
    N_e = []
    for Z in range(4, 31):
        Z_idx, st_idx, s_idx = Z_st_s_idx(tab, Z, 1, s)
        E_e = np.append(E_e, tab[Z_idx[0]+st_idx[0]+s_idx[0], 4])
        E_p = np.append(E_p, tab[Z_idx[0]+st_idx[0]+s_idx[0], 6])
        N_e = np.append(N_e, tab[Z_idx[0]+st_idx[0]+s_idx[0], 3])
        
        """
        E_e = np.empty(26)
        E_e.fill(np.NaN)
        E_p = np.empty(26)
        E_p.fill(np.NaN)
        N_e = np.empty(26)
        N_e.fill(np.NaN)
        
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
        """
    Z_tab = np.arange(4, 31)
    multiplicator = 100
    E_p = [i*multiplicator for i in E_p]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(Z_tab, E_e, '--', drawstyle='steps', color='tab:blue', label="electrons energy")
    ax.plot(Z_tab, E_p, drawstyle='steps', color='tab:blue', label="photons energy (x"+str(multiplicator)+")")
    ax2.plot(Z_tab, N_e, drawstyle="steps", color='tab:orange')
    ax.set_ylabel('Energy (eV)', color='tab:blue')
    ax2.set_ylabel('number of Auger electrons', color='tab:orange')
    
    plt.title("Neutral atoms with s="+str(s))
    ax.set_xlabel("Atomic number")
    ax.legend()
    return(N_e, E_e, E_p)

A = energy_st(17, 1)
B = energy_Z(1)

