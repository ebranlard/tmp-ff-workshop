"""
3 Parametric sweep

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
try:
    import dill
except ImportError as e:
    FAIL('The python package fill is not installed. FFCaseCreation cannot be saved to disk.\nPlease install it using:\n`pip install dill`\n\nNOTE: this is not critical for running Example 3, but will prevent some of the postprocessing in Example 4. So feel free to uncomment.')
    raise e



# **Adapt the path below if necessary for your machine. The paths can be relative or absolute.**
# --- Windows
ffbin = './FAST.Farm_x64_v4.1.2.exe' # relative or absolute path of FAST.Farm executable
tsbin = './TurbSim_x64_v4.1.2.exe'   # relative or absolute path of TurbSim executable
libdisconfilepath = './template/libdiscon_rosco_v2.9.0.dll' # relative or absolute path of ROSCO library
# --- Linux
# ffbin = './FAST.Farm' # relative or absolute path of FAST.Farm executable
# tsbin = './turbsim'   # relative or absolute path of TurbSim executable
# libdisconfilepath = './template/libdiscon_rosco_v2.9.0.so' # relative or absolute path of ROSCO library
# --- Mac
# ffbin = './FAST.Farm' # relative or absolute path of FAST.Farm executable
# tsbin = './turbsim'   # relative or absolute path of TurbSim executable
# libdisconfilepath = './template/libdiscon_rosco_v2.9.0.dylib' # relative or absolute path of ROSCO library

check_files_exist(ffbin, tsbin);
check_discon_library(libdisconfilepath);



print('# --------------------------------------------------------------------------------')
print('# ---  3.1 Getting Ready for Parametric Sweep')
print('# --------------------------------------------------------------------------------')
"""
Example 2 above consisted of one inflow condition, one turbulent seed, and one simulation case. 
Because we passed `flat=True` and there is only one simulation to run, the class `FFCaseCreation` put all input files into a single directory. 
The `FFCaseCreation` can support parametric sweep with mutiple conditions, cases, seeds. To get you familiar with the directory structure for more advanced simulations, we re-run the Example 2, but this time, we set `flat=False`. 
Also, to get you more familiar with the examples presented in the toolbox, we put all the inputs into one cell. 
"""


# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------
path = 'ff_example3_seeds'    # folder (preferably new) where all the simulation files will be written
# -----------------------------------------------------------------------------
# --------------------------- Farm parameters ---------------------------------
# -----------------------------------------------------------------------------
# ----------- General turbine parameters
cmax     = 5.5    # Maximum blade chord (m)
fmax     = 10/6   # Maximum excitation frequency (Hz)
Cmeander = 1.9    # Meandering constant (-)
D = 240           # Rotor diameter (m)
zhub = 150        # Hub height (m)
# ----------- Wind farm
wts = {
    0 :{'x':  0.0, 'y':    0,  'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x':  2*D, 'y':   D/2, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
}
refTurb_rot = 0
# ----------- Turbine parameters
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = None
# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------
# ----------- Additional variables
tmax = 120       # Total simulation time
zbot = 1        # Bottom of your domain
mod_wake = 1    # Wake model. 1: Polar, 2: Curled, 3: Cartesian
# ----------- Inflow parameters
inflowType = 'TS'
# ----------- Desired sweeps, fill array with multiple values if necessary
nSeeds     = 2      # Number of seeds
vhub       = [8]    # Hub velocity [m/s]
shear      = [0.1]  # Power law exponent [-]
TIvalue    = [7]    # Turbulence intensity [%]
inflow_deg = [0]    # Wind direction [deg]
# ----------- Template files
templateFSTF = './template/FF.fstf'
templateFiles = {'libdisconfilepath': libdisconfilepath}
# -----------------------------------------------------------------------------
# ---------------------- Discretization parameters ----------------------------
# -----------------------------------------------------------------------------
# ----------- Low- and high-res boxes parameters
# High-res boxes settings
dt_high     =  0.5                # sampling time of high-res files [s]
ds_high     =  10.0               # dx, dy, dz of high-res files [m]
extent_high =  1.2                # extent in y and x for each turbine, in D
# Low-res boxes settings
dt_low      = 2.0                 # sampling time of low-res files [s]
ds_low      = 25                  # dx, dy, dz of low-res files [m]
extent_low  = [1.5,2.5,1.5,1.5,2] # extent in [xmin,xmax,ymin,ymax,zmax], in D

# --- Simple Debugging before running
#fig = plotFastFarmSetup(wts)
#check_files_exist(ffbin, tsbin, templateFSTF, templateFiles);
#check_discon_library(libdisconfilepath);
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, nSeeds=nSeeds, yaw_init=yaw_init,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        mod_wake=mod_wake, inflowType=inflowType, 
                        ffbin=ffbin, tsbin=tsbin, refTurb_rot=refTurb_rot)
# ----------- Perform auxiliary steps in preparing the case
ffcase.setTemplateFilename(templateFSTF=templateFSTF, templateFiles=templateFiles)
ffcase.getDomainParameters()
ffcase.copyTurbineFilesForEachCase()

# There are a few things the user can look at to check the setup. 
# One of them, as mentioned is to print the object. Others are to print the datasets that hold the information for all the cases:
# ----------- TurbSim low-res setup
ffcase.TS_low_setup()
ffcase.TS_low_batch_prepare()
ffcase.TS_low_batch_run(showOutputs=True, showCommand=True, nBuffer=5, shell_cmd='bash')
# ----------- TurbSim high-res setup
ffcase.TS_high_setup()
ffcase.TS_high_batch_prepare()
ffcase.TS_high_batch_run(showOutputs=True, showCommand=True, nBuffer=5, shell_cmd='bash')
# ----------- FAST.Farm setup
ffcase.FF_setup()
ffcase.FF_batch_prepare()
for fff in ffcase.FFFiles:
    print('FFFile:', fff)
    modifyProperty(fff, 'TMax', 120)
ffcase.save()
print('#The content of the batch file is:\n'+''.join(open(ffcase.batchfile_ff).readlines()[:10]))
ffcase.FF_batch_run(showOutputs=True, showCommand=True, nBuffer=8, shell_cmd='bash')



print('# --------------------------------------------------------------------------------')
print('# --- 3.2 Wind speed and wind dir sweep')
print('# --------------------------------------------------------------------------------')
# Let's now try to sweep in some wind speeds and directions.
# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------
path = 'ff_example3_ws_wd'    # folder (preferably new) where all the simulation files will be written
yaw_init = None
# ----------- Desired sweeps
nSeeds     = 6
vhub       = [8, 10]
shear      = [0.1]
TIvalue    = [10]
inflow_deg = [-5, 0, 5]
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase2 = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, nSeeds=nSeeds, yaw_init=yaw_init,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        mod_wake=mod_wake, inflowType=inflowType, 
                        ffbin=ffbin, tsbin=tsbin, refTurb_rot=refTurb_rot)
# ----------- Perform auxiliary steps in preparing the case
ffcase2.setTemplateFilename(templateFSTF=templateFSTF, templateFiles=templateFiles)
ffcase2.getDomainParameters()
ffcase2.copyTurbineFilesForEachCase()
# Note that we asked for 2 wind speeds (two _conditions_) and 3 inflow directions. A change in direction only doesn't mean we will re-run the inflow, but rather we will rotate the farm. So a sweep in wind direction means another _case_. For each _condition_, we then have 3 _cases_. We can see all the conditions and cases as follows:
print(ffcase2.allCond)
print(ffcase2.allCases)
# Now the plotting function is more helpful. See how the farm was rotated to accomodate the new wind direction
# Also note how the turbine has been yawed so that it remains aligned given the change in the wind direction.
ffcase2.plot()


print('# --------------------------------------------------------------------------------')
print('# --- 3.3 Yaw misalignmen')
print('# --------------------------------------------------------------------------------')
# Let's add some yaw misalignment. Let's reduce to a single _condition_ and reduce the sweeps in wdir to only two.
# ----------- Case absolute path
path = 'ff_example3_yaw'
# ----------- Turbine parameters
refTurb_rot = 0 # reference turbine used for rotating layout
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = [[0, 0],     # [Yaw WT1, Yaw WT2] for inflow_deg[0]
            [10, 10]]   # [Yaw WT1, Yaw WT2] for inflow_deg[1]
# ----------- Desired sweeps
nSeeds     = 6
vhub       = [10]
inflow_deg = [0, 35]
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase3 = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, nSeeds=nSeeds, yaw_init=yaw_init,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        mod_wake=mod_wake, inflowType=inflowType, 
                        ffbin=ffbin, tsbin=tsbin, refTurb_rot=refTurb_rot)
# ----------- Perform auxiliary steps in preparing the case
ffcase3.setTemplateFilename(templateFSTF=templateFSTF, templateFiles=templateFiles, verbose=0)
ffcase3.getDomainParameters()
ffcase3.copyTurbineFilesForEachCase()
# Note, however, that the setup above does zero yaw with the 0 wind direction and 10 deg yaw with the 35 deg wind direction. These fields are not combinatory. If we want that, we need to set it up slightly different:
# Note how each turbine has two yaw angles now 
ffcase3.plot()
# ----------- Case absolute path
path = 'ff_example3_yaw2'
# ----------- Turbine parameters
refTurb_rot = 0 # reference turbine used for rotating layout
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = [[0, 0],  # [Yaw WT1, Yaw WT2] for inflow_deg[0]
            [10, 10],  # [Yaw WT1, Yaw WT2] for inflow_deg[1]
            [0, 0],  # [Yaw WT1, Yaw WT2] for inflow_deg[2]
            [10, 10]]  # [Yaw WT1, Yaw WT2] for inflow_deg[3]
# ----------- Desired sweeps
vhub       = [10]
inflow_deg = [0, 0, 35, 35]
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase3 = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        ffbin=ffbin, mod_wake=mod_wake, yaw_init=yaw_init,
                        nSeeds=nSeeds, tsbin=tsbin, inflowType=inflowType,
                        refTurb_rot=refTurb_rot, verbose=0)
# ----------- Perform auxiliary steps in preparing the case
ffcase3.setTemplateFilename(templateFSTF=templateFSTF, templateFiles=templateFiles, verbose=0)
ffcase3.getDomainParameters()
ffcase3.copyTurbineFilesForEachCase()


OK('Example 3 ran successfully')
