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
    
    zipped_e = zip(N_e, E_e)
    sorted_e = sorted(zipped_e)
    tuples_e = zip(*sorted_e)
    N_e, E_e =  [list(tuple) for tuple in tuples_e]
    
    zipped_p = zip(N_e, E_p)
    sorted_p = sorted(zipped_p)
    tuples_p = zip(*sorted_p)
    N_e, E_p =  [list(tuple) for tuple in tuples_p]
    
    plt.plot(N_e, E_e, drawstyle="steps",label="electrons")
    plt.plot(N_e, E_p, drawstyle="steps",label="photons")
    plt.title("Z="+str(Z)+" and s="+str(s))
    plt.xlabel("Number of Auger electrons")
    plt.ylabel("Energy (eV)")
    plt.legend()
    return(N_e, E_e, E_p)
    
A = energy_Z(17, 1)

"""
plt.figure()
plt.plot(tab[:,3], tab[:,4], drawstyle="steps",label="electrons")
plt.plot(tab[:,3], tab[:,6], drawstyle="steps", label="photons")
"""