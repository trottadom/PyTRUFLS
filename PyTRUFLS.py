#%% Imports etc
# First few imports
import datetime as dt
import numpy as np
import os
import sys
import pandas as pd
import warnings
import importlib
from matplotlib import pyplot as plt
sys.path.append('/Users/domenico.trotta/Desktop/PestoLab/PestoPantry')
#%matplotlib ipympl
from seppy.loader.solo import mag_load
from solo_swa_loader import swa_load_grnd_mom
#%% Load needed dataset into Pandas dataframes
#%
# Path where to dump Solar Orbiter data
datapath = '/Users/domenico.trotta/Desktop/PestoLab/DataSolO'
# whether missing data files should automatically downloaded from SOAR:
autodownload = True

# Start and end searching time  (for example here we do October 2021)
startdate = dt.date(2022,2,28)
enddate   = dt.date(2022,4,1)    

df_mag = mag_load(startdate, enddate, level='l2', data_type='normal', frame='rtn', path=datapath) # MAG data
df_swa = swa_load_grnd_mom(startdate, enddate, path=datapath) # SWA Ground Moments data

df_mag["B"] = np.linalg.norm(df_mag[["B_RTN_0","B_RTN_1","B_RTN_2"]],axis=1) # Compute magnetic field magnitude
df_swa["V"] = np.linalg.norm(df_swa[["V_RTN_0","V_RTN_1","V_RTN_2"]],axis=1) # Compute bulk flow speed


# %
l_avg = dt.timedelta(minutes=3)   # How big of an averaging window you want 
l_exc = dt.timedelta(seconds=30)  # Length of half exclusion zone you want
l_inc = dt.timedelta(minutes=2)   # Time Stepping
# %
start_time = dt.datetime(2021,10,1,1,0,0)
end_time   = dt.datetime(2021,10,31,23,0,0)

# %% Smell shocks
candidates_FF = []     # This is where the times for your Fast Forward shock candidates will be stored
candidates_FR = []     # This is where the times for your Fast Reverse shock candidates will be stored


t_now = start_time  # Central time now

while t_now < end_time:

    # Smell Fast Forward shocks
    t_us = t_now - (l_avg + l_exc)   # Start of candidate upstream window time
    t_ue = t_now - l_exc             # End of candidate upstream window time
    t_ds = t_now + l_exc   # Start of candidate downstream window time
    t_de = t_now + (l_avg + l_exc)             # End of candidate downstream window time

    Bu = df_mag.loc[t_us:t_ue]['B'].mean(skipna=True) # Mean upstream magnetic field
    Vu = df_swa.loc[t_us:t_ue]['V'].mean(skipna=True) # Mean upstream ion speed
    Nu = df_swa.loc[t_us:t_ue]['N'].mean(skipna=True) # Mean upstream density

    Bd = df_mag.loc[t_ds:t_de]['B'].mean(skipna=True) # Mean downstream magnetic field
    Vd = df_swa.loc[t_ds:t_de]['V'].mean(skipna=True) # Mean downstream ion speed
    Nd = df_swa.loc[t_ds:t_de]['N'].mean(skipna=True) # Mean downstream density

    if Bd/Bu > 1.2 and Nd/Nu > 1.2 and (Vd-Vu >= 20) : # Condition for Fast Forward shock
        print(["PyTRUFLS :: I smell a candidate Fast Forward shock at ", t_now] )
        candidates_FF.append(t_now)


    # Smell Fast Reverse shocks
    t_ds = t_now - (l_avg + l_exc)   # Start of candidate upstream window time
    t_de = t_now - l_exc             # End of candidate upstream window time
    t_us = t_now + l_exc   # Start of candidate downstream window time
    t_ue = t_now + (l_avg + l_exc)             # End of candidate downstream window time


    Bu = df_mag.loc[t_us:t_ue]['B'].mean(skipna=True) # Mean upstream magnetic field
    Vu = df_swa.loc[t_us:t_ue]['V'].mean(skipna=True) # Mean upstream ion speed
    Nu = df_swa.loc[t_us:t_ue]['N'].mean(skipna=True) # Mean upstream density

    Bd = df_mag.loc[t_ds:t_de]['B'].mean(skipna=True) # Mean downstream magnetic field
    Vd = df_swa.loc[t_ds:t_de]['V'].mean(skipna=True) # Mean downstream ion speed
    Nd = df_swa.loc[t_ds:t_de]['N'].mean(skipna=True) # Mean downstream density

    if Bd/Bu > 1.2 and Nd/Nu > 1.2 and (Vd-Vu >= 20) : # Condition for Fast Forward shock
        print(["PyTRUFLS :: I smell a candidate Fast Reverse shock at ", t_now] )
        candidates_FR.append(t_now)



    t_now = t_now + l_inc







# %%
