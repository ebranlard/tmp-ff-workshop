"""
2. Example 2: `Ex2a_FASTFarm_TurbSim_driven.py`

The example 2 for TurbSim has the same inputs as example 1 (the ones for the discretization), 
but additional inputs are now added to define the simulation setup. The new inputs are listed below:



- **General parameters**
    - `path` : folder (preferably new) where all the simulation files will be written
    -  `ffbin` and `tsbin`: location of the FAST.Farm and TurbSim executables
    - `templatePath`: existing folder, where the template FAST.Farm and OpenFAST files can be found.
    - `templateFiles`: location of files within templatePath to be used, or absolute location of required files.
        Note: some template files provided (like ED, SD, turbine fst) need to end with `.T` while  the actual filename inside `templatePath` is `*.T.<ext>` where `<ext>` is either `dat` or `fst`.

- **Farm parameters** (same as above)

- Inflow conditions and input files (same as above, but with more details):
   - `shear`, `TIvalue`, `inflow_deg`, together with `vhub` define the inflow values.
   - `tmax`: defines the maximum simulation time

- **Discretization parameters** (`dt_high`, `dt_low`, etc): these are the parameters we determined in Example 1.


### Pre-requisites to run the cells below:
 - A FAST.Farm Executable with version v4.*  (to be compatible with the input files provided)
 - A TurbSim Executable (any version>2 should do)
 - ROSCO libdiscon DLL or shared object with version 4.9

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
print('# --- 2.3 Setup of FFCaseCreation Object and creation of OpenFAST input file')
print('# --------------------------------------------------------------------------------')

# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------
path = 'ff_example2_onesim'          # folder (preferably new) where all the simulation files will be written
templateFSTF = './template/FF.fstf'
templateFiles = {'libdisconfilepath' : libdisconfilepath,}
check_files_exist(ffbin, tsbin, templateFSTF, templateFiles)
check_discon_library(libdisconfilepath);
# -----------------------------------------------------------------------------
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
vhub       = [8]    # Hub velocity [m/s]
shear      = [0.1]  # Power law exponent [-]
TIvalue    = [7]    # Turbulence intensity [%]
inflow_deg = [0]    # Wind direction [deg]
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
fig = plotFastFarmSetup(wts)

# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, 
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        mod_wake=mod_wake, inflowType=inflowType,
                        ffbin=ffbin, tsbin=tsbin, verbose=1, flat=True)

# ----------- Perform auxiliary steps in preparing the case
ffcase.setTemplateFilename(templateFiles=templateFiles, templateFSTF=templateFSTF)
ffcase.getDomainParameters()
ffcase.copyTurbineFilesForEachCase()
ffcase.plot()  # add showTurbNumber=True to help with potential debugging
# The plot command above saves the images to the case root `ffcase.path`



print('# --------------------------------------------------------------------------------')
print('# --- 2.4 Creation of Low Res turbulence box')
print('# --------------------------------------------------------------------------------')
# Now comes the main part, which is the turbsim setup. 
# First we create the low-res boxes, then the high-res boxes based on time series of the low-res box at the location of the turbines

# -----------------------------------------------------------------------------
# ---------------------- TurbSim setup and execution --------------------------
# -----------------------------------------------------------------------------
# ----------- TurbSim low-res setup
ffcase.TS_low_setup() # Create TurbSim input files
ffcase.TS_low_batch_prepare() # write a batch file to disk
#ffcase.TS_low_slurm_prepare(slurm_TS_High) # Alternative, write a slurm batch file, see below

print('#The content of the batch file is:\n'+''.join(open(ffcase.batchfile_low).readlines()[:10]))

# You might want to run these commands locally or on a cluster (see below for more on that). 
# Alternatively, the function below attempts to run the batch file locally.
ffcase.TS_low_batch_run(showOutputs=True, showCommand=True, nBuffer=8, shell_cmd='bash')
#ffcase.TS_low_slurm_submit() # Alternative, submit a slurm batch file, see below


print('# --------------------------------------------------------------------------------')
print('# --- 2.5 Creation of HighRes turbulence box')
print('# --------------------------------------------------------------------------------')
# Now with the low-res completed, we can move forward with the high-res. Note that if you try to call `ffcase.TS_high_setup()` before the low-res is done, it will stop when trying to open the low-res box.

# ----------- TurbSim high-res setup
ffcase.TS_high_setup() # Create TurbSim input files
ffcase.TS_high_batch_prepare() # write a batch file to disk
#ffcase.TS_low_slurm_prepare(slurm_TS_low) # Alternative, write a slurm batch file, see below
# The calls above create the time series to drive the high-res box, taking into account where the turbines are, inclusing the `offset` parameter to TurbSim and also the rolling of the time series, considering how downstream each turbine is.
# In addition, a batch file is written to disk. 
print('#The content of the batch file is:\n'+''.join(open(ffcase.batchfile_high).readlines()[:10]))
# We advise to run batch files locally, but otherwise, you can try the command below.
ffcase.TS_high_batch_run(showOutputs=True, showCommand=True, nBuffer=8, shell_cmd='bash')
#ffcase.TS_high_slurm_submit() # Alternative, submit a slurm batch file, see below

# After this runs, we can move forward with the FAST.Farm setup. Note how the wake model parameters can be easily set.


print('# --------------------------------------------------------------------------------')
print('# --- 2.6 Create FAST.Farm input files')
print('# --------------------------------------------------------------------------------')

# -----------------------------------------------------------------------------
# ------------------ Finish FAST.Farm setup and execution ---------------------
# -----------------------------------------------------------------------------
# ----------- FAST.Farm setup
ffcase.FF_setup() # Write FAST.Farm input files
ffcase.FF_batch_prepare() # Write batch files with all commands to be run
#ffcase.FF_slurm_prepare(slurm_FF_single) # Alternative, write slurm file, see section below
## We can dump the object to disk so we can re-open another time or for post-processing. It will be saved on the ffcase.path path
# The dump relies on the package dill. 
# You need to `pip install dill`
ffcase.save()
print('#The FASTFarm files created are:\n'+'\n'.join(ffcase.FFFiles))
# We can do simple modifications:
modifyProperty(ffcase.FFFiles[0], 'NX_Low', 100) # Making the domain longer for visualization purposes
# We can visualize the setup:
plotFastFarmSetup(ffcase.FFFiles[0], grid=True, figsize=(10,3));
print('#The content of the batch file is:\n'+''.join(open(ffcase.batchfile_ff).readlines()[:10]))
# At this stage, we advise to run the commands locally, or if you have many cases, you can look at section 2.6 for running on a cluster. 
# Below we provide a command to run the batch script directly. 
ffcase.FF_batch_run(showOutputs=True, showCommand=True, nBuffer=10, shell_cmd='bash')
# This terminates the main part of Example 2
#
#


OK('Example 2 ran successfully')

plt.show()
