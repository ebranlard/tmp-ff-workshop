from welib.essentials import *
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import FFCaseCreation
import numpy as np
import matplotlib.pyplot as plt
import os
notepath = os.getcwd();


# -----------------------------------------------------------------------------
# USER INPUT: Modify these
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------

# ----------- Case absolute path
path = 'C:/W0/ff_walkthrough/ff_examples_ex2a_regis'

# ----------- Execution parameters
# If you are sure the correct binaries are first on your $PATH and associated
# libraries on $LD_LIBRARY_PATH, you can set the variables below to None or
# remove them from the `FFCaseCreation` call
ffbin = 'C:/W0/ff_walkthrough/FAST.Farm_x64_v4.1.2.exe'
tsbin = 'C:/W0/ff_walkthrough/TurbSim_x64_v4.1.2.exe'


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
# The wts dictionary holds information of each wind turbine. The allowed entries
# are: x, y, z, D, zhub, cmax, fmax, Cmeander, and phi_deg. The phi_deg is the
# only entry that is optional and is related to floating platform heading angle,
# given in degrees. The angle phi_deg is not illustrated on the example below.
wts = {
    0 :{'x': 500.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x':1100.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
    2 :{'x':1800.0, 'y': 480, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T3'},
    3 :{'x': 500.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T4'},
    4 :{'x':1100.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T5'},
    5 :{'x':1800.0, 'y':1200, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T6'},
}
refTurb_rot = 0

# ----------- Turbine parameters
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = None


# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------

# ----------- Additional variables
tmax = 50      # Total simulation time
nSeeds = 6      # Number of seeds
zbot = 1        # Bottom of your domain
mod_wake = 2    # Wake model. 1: Polar, 2: Curled, 3: Cartesian

# ----------- Inflow parameters
inflowType = 'TS'

# ----------- Desired sweeps
vhub       = [8]
shear      = [0.1]
TIvalue    = [10]
inflow_deg = [0]

# ----------- Template files
# templatePath = 'C:/W0/ff_walkthrough/tutorial_files_regis'
# templateFiles = {
#     'FFfilename'              : 'FAST.Farm.fstf',
#     'turbfilename'            : 'IEA-15-240-RWT-Monopile.T',
#     "EDfilename"              : 'IEA-15-240-RWT-Monopile_ElastoDyn.T',
#     'SrvDfilename'            : 'IEA-15-240-RWT-Monopile_ServoDyn.T',
#     'ADfilename'              : 'IEA-15-240-RWT-Monopile_AeroDyn15.dat',
#     'ADbladefilename'         : 'IEA-15-240-RWT_AeroDyn15_blade.dat',
#     'IWfilename'              : 'IW_WT.dat',
#     'EDbladefilename'         : 'IEA-15-240-RWT_ElastoDyn_blade.dat',
#     'EDtowerfilename'         : 'IEA-15-240-RWT-Monopile_ElastoDyn_tower.dat',
#     'controllerInputfilename' : 'IEA-15-240-RWT-Monopile_DISCON_ROSCOv2.9.IN',
#     'libdisconfilepath'       : 'C:/W0/ff_walkthrough/libdiscon.so',
#     'turbsimLowfilepath'      : 'C:/W0/ff_walkthrough/SampleFiles/template_Low_InflowXX_SeedY.inp',
#     'turbsimHighfilepath'     : 'C:/W0/ff_walkthrough/SampleFiles/template_HighT1_InflowXX_SeedY.inp'
# }


templatePath = 'C:/W0/ff_walkthrough/template'
templateFiles = {
    'FFfilename'              : 'Main.fstf',
    'turbfilename'            : 'WT.T',
    "EDfilename"              : 'ED.T',
    'SrvDfilename'            : 'SvD.T',
    'ADfilename'              : 'AD.dat',
    'ADbladefilename'         : 'IEA-15-240-RWT_AeroDyn15_blade.dat',
    'IWfilename'              : 'IW_WT.dat',
    'EDbladefilename'         : 'IEA-15-240-RWT_ElastoDyn_blade.dat',
    'EDtowerfilename'         : 'IEA-15-240-RWT-Monopile_ElastoDyn_tower.dat',
    'controllerInputfilename' : 'DISCON_ROSCOv2.9.IN',
    'libdisconfilepath'       : 'C:/W0/ff_walkthrough/template/libdiscon_rosco_v2.9.0.dll',
    'turbsimLowfilepath'      : 'C:/W0/ff_walkthrough/SampleFiles/template_Low_InflowXX_SeedY.inp',
    'turbsimHighfilepath'     : 'C:/W0/ff_walkthrough/SampleFiles/template_HighT1_InflowXX_SeedY.inp'
}


# SLURM scripts
slurm_TS_high           = 'C:/W0/ff_walkthrough/SampleFiles/runAllHighBox.sh'
slurm_TS_low            = 'C:/W0/ff_walkthrough/SampleFiles/runAllLowBox.sh'
slurm_FF_single         = 'C:/W0/ff_walkthrough/SampleFiles/runFASTFarm_cond0_case0_seed0.sh'


# -----------------------------------------------------------------------------
# ---------------------- Discretization parameters ----------------------------
# -----------------------------------------------------------------------------
# ----------- Low- and high-res boxes parameters
# High-res boxes settings
dt_high     =  0.25               # sampling frequency of high-res files
ds_high     =  5                  # dx, dy, dz of high-res files
extent_high =  1.2                # extent in y and x for each turbine, in D
# Low-res boxes settings
dt_low      = 1.0                 # sampling frequency of low-res files
ds_low      = 25                  # dx, dy, dz of low-res files
extent_low  = [1.5,2.5,1.5,1.5,2] # extent in [xmin,xmax,ymin,ymax,zmax], in D
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        ffbin=ffbin, mod_wake=mod_wake, yaw_init=yaw_init,
                        nSeeds=nSeeds, tsbin=tsbin, inflowType=inflowType,
                        refTurb_rot=refTurb_rot, verbose=1)

# ----------- Perform auxiliary steps in preparing the case
ffcase.setTemplateFilename(templatePath, templateFiles)
ffcase.getDomainParameters()
ffcase.copyTurbineFilesForEachCase()



# # ----------- TurbSim low-res setup
ffcase.TS_low_setup()
# ----------- Prepare script for submission
ffcase.TS_low_batch_prepare(run=False)
ffcase.TS_low_slurm_prepare(slurm_TS_low)
# ----------- Submit the low-res script (can be done from the command line)
#ffcase.TS_low_slurm_submit()
 

# ----------- TurbSim high-res setup
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
ffcase.plot()
ffcase.TS_high_setup()
# ----------- Prepare script for submission
ffcase.TS_high_slurm_prepare(slurm_TS_high)
# ffcase.TS_high_batch_prepare(run=True, run_if_ext_missing='.bts', discard_if_ext_present=None)
# ----------- Submit the high-res script (can be done from the command line)

# -----------------------------------------------------------------------------
# ------------------ Finish FAST.Farm setup and execution ---------------------
# -----------------------------------------------------------------------------
# ----------- FAST.Farm setup
ffcase.FF_setup()
# Update wake model constants (adjust as needed for your turbine model)
# ffcase.set_wake_model_params(k_VortexDecay=0, k_vCurl=2.8)
# 
# # ----------- Prepare script for submission
# ffcase.FF_slurm_prepare(slurm_FF_single)
# 

#ffcase.TS_high_slurm_submit()
plt.show()
