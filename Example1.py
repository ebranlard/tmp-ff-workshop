"""
1. Example 1: `Ex1_FASTFarm_discretization.py`
 This example calculates the desired temporal and spatial resolution given a wind farm layout. 

 The FAST.Farm guidelines requires several parameters to be set to find the resolutsion:
  - Spatial parameters: max chord (`cmax`), rotor diameter (`D`), meandering constant (`Cmeander`)
  - Temporal parameters: maximum excitation frequency (`fmax`), mean wind speed (`vhub`)
  - Model parameters: wake models (`mod_wake`), and background inflow type (`inflowType`)
 
 Based on these parameters, the FFCaseCreation class can compute some default resolution, but it is often required to adjust some of them manually and not fully rely on the defaults.
 
 In this example, we do the following:
 - First, we obtain the default parameters and plot the layout
 - Then, we manually adjust some of the resolution parameters

"""
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

# --------------------------------------------------------------------------------}
# --- 1.1 Parameters affecting the resolution
# --------------------------------------------------------------------------------{

# --------------------------- Farm parameters ---------------------------------
# -----------------------------------------------------------------------------
# ----------- General turbine parameters
cmax     = 5.5    # Maximum blade chord (m), affects dr
fmax     = 10/6   # Maximum excitation frequency (Hz), affects dt_high
Cmeander = 1.9    # Meandering constant (-)
D = 240           # Rotor diameter (m)
zhub = 150        # Hub height (m)
# ----------- Wind farm
# The wts dictionary holds information of each wind turbine. The allowed entries
# are: x, y, z, D, zhub, cmax, fmax, Cmeander, and phi_deg. The phi_deg is the
# only entry that is optional and is related to floating platform heading angle,
# given in degrees. The angle phi_deg is not illustrated on the example below.
wts = {
    0 :{'x':  0.0, 'y':    0,  'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x':  2*D, 'y':   D/2, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
}
fig = plotFastFarmSetup(wts, figsize=(6,3))
# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------
# ----------- Additional variables
mod_wake = 1    # Wake model. 1: Polar, 2: Curled, 3: Cartesian. NOTE: Resolution guidelines vary based on this.
# ----------- Inflow parameters
inflowType = 'TS' # TS: TurbSim, or LES: LES (VTK files needs to exist)
# ----------- Desired sweeps of inflow conditions (here, only one value, no sweep)
vhub       = [8]  # NOTE: use the maximum velocity here [m/s]




# --------------------------------------------------------------------------------}
# --- 1.2 Getting the default resolution and plotting the layout
# --------------------------------------------------------------------------------{

# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
# Below we provide the minimal set of arguments needed to compute the resolution automatically.
ffcc = FFCaseCreation(wts=wts, vhub=vhub, 
                      mod_wake=mod_wake,
                      inflowType=inflowType)

# Plot the FARM Layout
ffcc.plot() # Note: the grids are not plotted by this function

# The call to `FFCaseCreation` with no resolution expicitely provided (i.e., all the arguments `ds_low`, `dt_high` are set to  `None`) triggers the lengthy message above. From there, we can just check if those numbers make sense given the available computational resources. Highlight the warning printed with further instructions. Also, note that `dt_high=0.3` is a just a consequence of the value we selected for `fmax`, which isn't the actual maximum exitation frequency of the IEA 15MW. It is slightly more conservative than the (already conservative) 12P excitation frequency of about 1.5Hz. The reason we chose 10/6 is to get a round number for dt_high.

# --------------------------------------------------------------------------------}
# --- 1.3 Adjusting the resolution
# --------------------------------------------------------------------------------{
# The output message above is saying that the low-res should be 24.32, but since it needs to be a multiple of the high res, then it automatically selects 20 m. However, since 24.32 is close to 25, we might want to just run at 25. Then, an option is to re-run the same command, but now passing a value for `ds_low`:
ds_low = 25 # user define low resolution [m]
# ----------- Initial setup (Now, with ds_low)
ffcc = FFCaseCreation(wts=wts, vhub=vhub, 
                      ds_low=ds_low,
                      mod_wake=mod_wake,
                      inflowType=inflowType, verbose=0)
# Note how now the low-res grid resolution is set to 25 m. We can do the same with the dt if we want. Let's say we want the time steps of the low to be a more round number, we can set both dts:

dt_high = 0.50 # [s]
dt_low  = 2.00 # [s]
ds_low  = 25   # [m]
# ----------- Initial setup
ffcc = FFCaseCreation(wts=wts, vhub=vhub,
                     dt_high=dt_high,
                     dt_low=dt_low,   ds_low=ds_low,
                     mod_wake=mod_wake,
                     inflowType=inflowType)

"""
 This ends the illustration of the first example. Now we can move forward with the FAST.Farm setup using two options:
 
 1. Use directly the `ffcc` object:
 ```
 # ----------- Low- and high-res boxes parameters
 # High-res boxes settings
 dt_high     = ffcc.dt_high
 ds_high     = ffcc.ds_high
 extent_high = ffcc.extent_high
 # Low-res boxes settings
 dt_low      = ffcc.dt_low
 ds_low      = ffcc.ds_low
 extent_low  = ffcc.extent_low
 ```
 
 2. Manually add those values to their corresponding variables:
 ```
 # ----------- Low- and high-res boxes parameters
 # High-res boxes settings
 dt_high     =  0.5               
 ds_high     =  5                 
 extent_high =  1.2               
 # Low-res boxes settings
 dt_low      = 1.0                  
 ds_low      = 25                 
 extent_low  = [1.5,2.5,1.5,1.5,2]
 
"""

# Note you can always print the object and get some information about the farm and the set of cases that will be setup:
print(ffcc)



OK('Example 1 ran successfully')

plt.show()


