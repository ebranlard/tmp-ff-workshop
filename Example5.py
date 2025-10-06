# # 5. LES

# ## 5.1. LES sampling
# Starting from scratch again.

# In[86]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import FFCaseCreation # Main case creation class
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import modifyProperty # Helper functions 
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import check_files_exist, check_discon_library # Helper functions 
from openfast_toolbox.fastfarm.fastfarm import plotFastFarmSetup # Low level FAST.Farm functions 
from openfast_toolbox.tools.strings import OK, FAIL # helper functions, colorful printing functions
OK('The toolbox was successfully loaded!')

from openfast_toolbox.fastfarm.AMRWindSimulation import AMRWindSimulation


# In[87]:


# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------
# ----------- Case absolute path
path = 'ff_example4_amr'
# -----------------------------------------------------------------------------
# --------------------------- Farm parameters ---------------------------------
# -----------------------------------------------------------------------------
# ----------- General turbine parameters
cmax     = 5      # Maximum blade chord (m)
fmax     = 10/6   # Maximum excitation frequency (Hz)
Cmeander = 1.9    # Meandering constant (-)
D = 240           # Rotor diameter (m)
zhub = 150        # Hub height (m)
# ----------- Wind farm
wts = {
    0 :{'x': 500.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x':1100.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
    2 :{'x':1800.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T3'},
    3 :{'x': 500.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T4'},
    4 :{'x':1100.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T5'},
    5 :{'x':1800.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T6'},
}
refTurb_rot = 0
# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------
# ----------- Additional variables
mod_wake = 2    # Wake model. 1: Polar, 2: Curled, 3: Cartesian
# -----------------------------------------------------------------------------
# ---------------------- Discretization parameters ----------------------------
# -----------------------------------------------------------------------------
# ----------- Low- and high-res boxes parameters
# High-res boxes settings
dt_high     =  0.25               # sampling frequency of high-res files
ds_high     =  5                  # dx, dy, dz of high-res files
# Low-res boxes settings
dt_low      = 1.0                 # sampling frequency of low-res files
ds_low      = 25                  # dx, dy, dz of low-res files


# Now we input some LES settings. First is the buffer we want to have around each box. This is very similar to the `extent` values from before, but note the difference for the high-res boxes.
# Next, we input the limits of your domain, in the same fashion as done in AMR-Wind. The variable names here reflect exactly how they are given in AMR-Wind to avoid issues. We give the domain limits and the maximum level available in your simulation. Then, we need to choose on which level do we want to sample each of the boxes-- this is important as it places the sampling point right in the middle of the cell center (avoids spatial interpolation). It is expected that the low-res will be sampled from a lower level (lower spatial resolution), and the high-res from the highest level available.

# In[88]:


# ----------- Low- and high-res boxes parameters. Note the buffer for high-res is given as hand the extent.
buffer_lr = [1.5,2,1.5,1.5,2] # [xmin,xmax,ymin,ymax,zmax], in D
buffer_hr = 0.6


# -----------------------------------------------------------------------------
# ------------------------- AMR-Wind parameters -------------------------------
# -----------------------------------------------------------------------------
fixed_dt = 0.01
prob_lo =  (0,     0,   0  )
prob_hi =  (5120, 2560, 960) 
n_cell  =  (128, 64, 24)   # 40,40,40 m resolution at level 0
max_level = 3

incflo_velocity_hh = (8,0,0) 
postproc_name = 'box'

# Levels of each box
level_lr=2
level_hr=3


# In[89]:


# The errors thrown tend to be verbose and tell the user what to do. Uncomment this line for an example of an error when the low-res now spans outside the domain:
# buffer_lr = [2.5,6,2.5,2.5,2]


# Upon calling the constructor of AMRWindSimulation, several errors will be thrown if your inputs have issues. Some common errors are:
# - if the limits of the computed boxes are outside your domain
# - if you don't have enough spatial resolution on your LES to accomodate the required spatial resolutions
# - if you request a box at a level that is higher than the max_level
# 
# Note that you can give the AMR-Wind class below your resolutions already computed using example 1 or you can let it compute for you and you can iterate the same way. Internally, the very same function is called.
# 
# Some warnings may also be printed:
# - If the user request a certain box resolution that does not fit the underlying LES resolution such that the points cannot be placed on the cell centers.
# 
# For the sake of illustration, let's start with the resolutions we computed previously. However, our LES grid is 40 m resolution at level 0, and the low-res sits at level 2, which means at level 2 (where the low-res box sits), the local resolution is 10x10x10 m which does not fit the 25 m low-res resolution. See how clear the warning is. It is just a warning because you can still sample your LES like that and perform the interpolated sampling; it is just suggested the user avoids interpolation.

# In[90]:


amr = AMRWindSimulation(wts, fixed_dt, prob_lo, prob_hi,
                        n_cell, max_level, incflo_velocity_hh,
                        postproc_name, buffer_lr = buffer_lr, buffer_hr=buffer_hr,
                        ds_hr=5,
                        ds_lr=10,
                        dt_hr=0.1,
                        dt_lr=0.4,
                        mod_wake=mod_wake,
                        level_lr=level_lr, level_hr=level_hr)


# In[91]:


ds_hr = 5
ds_lr = 25
dt_hr = 0.25
dt_lr = 1.00
amr = AMRWindSimulation(wts, fixed_dt, prob_lo, prob_hi,
                        n_cell, max_level, incflo_velocity_hh,
                        postproc_name, buffer_lr = buffer_lr, buffer_hr=buffer_hr,
                        ds_hr=ds_hr, ds_lr=ds_lr, dt_hr=dt_hr, dt_lr=dt_lr,
                        mod_wake=mod_wake, level_lr=level_lr, level_hr=level_hr)



# In[92]:


# at any moment, you can print the object to see more information:
print(amr)


# Let's now change the resolution. Alternatively, we could change our LES grid.

# In[93]:


ds_hr = 5
ds_lr = 20
dt_hr = 0.25
dt_lr = 1.00

amr = AMRWindSimulation(wts, fixed_dt, prob_lo, prob_hi,
                        n_cell, max_level, incflo_velocity_hh,
                        postproc_name, buffer_lr = buffer_lr, buffer_hr=buffer_hr,
                        ds_hr=ds_hr, ds_lr=ds_lr, dt_hr=dt_hr, dt_lr=dt_lr,
                        mod_wake=mod_wake, level_lr=level_lr, level_hr=level_hr)



# Finally, notice how the initial dt from the LES was very small. That was to allow the computed temporal resolutions to be anything, not putting restrictions on them being multiple of the LES. After you execute this call a few times, you should go back and set the dt to a more realistic value ensuring the boxes are still saved at the desired resolution.

# In[94]:


# Finally, write the input file to disk (or screen):

amr.write_sampling_params(terrain=False)  # write to screen

# amr.write_sampling_params(out='/your/full/path', format='native', terrain=False)



OK('Example 5 ran successfully')
