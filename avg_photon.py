#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:05:26 2022

@author: Ludmilla Allard
"""

import numpy as np
import matplotlib.pylab as plt
from emitted_electrons import correspondence, Z_st_s_idx

tab = np.loadtxt("avg_photons_electrons")

def energy_Z(Z, s):
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
    E_p = [i * 10 for i in E_p]

    """
    zipped_lists = zip(N_e, E_e)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    N_e, energy_e =  [list(tuple) for tuple in tuples] 
    """
    
    fig, ax = plt.subplots()
    
    ax.plot(st_tab, E_e, drawstyle='steps', label="electrons energy")
    ax.plot(st_tab, E_p, drawstyle='steps', label="photons energy (x10)")
    #ax2 = ax1.secondary_xaxis('top', functions=(N_e, E_e))
    #ax2.set_xlabel('number of Auger electrons')
    
    plt.title("Z="+str(Z)+" and s="+str(s))
    plt.xlabel("Ionisation stage")
    plt.ylabel("Energy (eV)")
    plt.legend()
    return(N_e, E_e, E_p)
    
A = energy_Z(8, 1)