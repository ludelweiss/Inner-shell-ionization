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
    
    if len(Z_idx)>1:
        N_e = tab[Z_idx[0]+s_idx[0]:Z_idx[0]+s_idx[0]+(len(s_idx)-1), 3]
        E_e = tab[Z_idx[0]+s_idx[0]:Z_idx[0]+s_idx[0]+(len(s_idx)-1), 4]
        E_p = tab[Z_idx[0]+s_idx[0]:Z_idx[0]+s_idx[0]+(len(s_idx)-1), 6]
    else:
        N_e = tab[Z_idx[0]+s_idx[0], 3]
        E_e = tab[Z_idx[0]+s_idx[0], 4]
        E_p = tab[Z_idx[0]+s_idx[0], 6]
    
    plt.plot(N_e, E_e, label="electrons")
    plt.plot(N_e, E_p, label="photons")
    plt.title("Element")
    plt.xlabel("Number of Auger electrons")
    plt.ylabel("Energy (eV)")
    plt.legend()
    return(N_e, E_e, E_p)
    
A = energy_Z(8, 1)