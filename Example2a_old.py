import matplotlib.pyplot as plt
from welib.essentials import *
from openfast_toolbox.fastfarm.FASTFarmCaseCreation_v03 import FFCaseCreation
import numpy as np
import os
notepath = os.getcwd();

try:
    scriptDir = os.path.dirname(__file__)
except:
    import inspect
    scriptDir = os.path.dirname(inspect.getsourcefile(lambda:0))
print(scriptDir)
print(notepath)


# -----------------------------------------------------------------------------
# USER INPUT: Modify these
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------

# ----------- Case absolute path
simPath = 'ff_example2a_manu'

# ----------- Execution parameters
# If you are sure the correct binaries are first on your $PATH and associated
# libraries on $LD_LIBRARY_PATH, you can set the variables below to None or
# remove them from the `FFCaseCreation` call
ffbin = './FAST.Farm_x64_v4.1.2.exe'
tsbin = './TurbSim_x64_v4.1.2.exe'

# --- OPTION 1
# templateFSTF= './template/Main.fstf'
# templateFiles = {
#     'turbsimLowfilepath'      : './SampleFiles/template_Low_InflowXX_SeedY.inp',
#     'turbsimHighfilepath'     : './SampleFiles/template_HighT1_InflowXX_SeedY.inp'
# }


templatePath = './template'
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
    'libdisconfilepath'       : './template/libdiscon_rosco_v2.9.0.dll',
    'turbsimLowfilepath'      : './SampleFiles/template_Low_InflowXX_SeedY.inp',
    'turbsimHighfilepath'     : './SampleFiles/template_HighT1_InflowXX_SeedY.inp'
}
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
# nSeeds = 2      # Number of seeds
zbot = 1        # Bottom of your domain
mod_wake = 2    # Wake model. 1: Polar, 2: Curled, 3: Cartesian

# ----------- Inflow parameters
inflowType = 'TS'

# ----------- Desired sweeps
vhub       = [8]
shear      = [0.1]
TIvalue    = [10]
inflow_deg = [0]


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
# END OF USER INPUT
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
os.chdir(notepath)
ffcase = FFCaseCreation(simPath, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, nSeeds=nSeeds,
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        ffbin=ffbin, mod_wake=mod_wake, yaw_init=yaw_init,
                        tsbin=tsbin, inflowType=inflowType,
                        refTurb_rot=refTurb_rot, verbose=1)

# ----------- Perform auxiliary steps in preparing the case
# ffcase.setTemplateFilename(templatePath, templateFiles)
ffcase.setTemplateFilename(templateFiles=templateFiles, templatePath=templatePath)
# ffcase.setTemplateFilename(templateFiles=templateFiles, templateFSTF=templateFSTF)
ffcase.getDomainParameters()
ffcase.copyTurbineFilesForEachCase()
# 
# # -----------------------------------------------------------------------------
# # ---------------------- TurbSim setup and execution --------------------------
# # -----------------------------------------------------------------------------
# # ----------- TurbSim low-res setup
ffcase.TS_low_setup()
# ----------- Prepare script for submission
slurm_TS_low            = './SampleFiles/runAllLowBox.sh'
ffcase.TS_low_slurm_prepare(slurm_TS_low)
ffcase.TS_low_batch_prepare(run=False)
# ----------- Submit the low-res script (can be done from the command line)
#ffcase.TS_low_slurm_submit()



#  
# slurm_FF_single         = 'C:/W0/ff_walkthrough/SampleFiles/runFASTFarm_cond0_case0_seed0.sh'


# ----------- TurbSim high-res setup
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
ffcase.plot()
ffcase.TS_high_setup()
# # ----------- Prepare script for submission
slurm_TS_high           = './SampleFiles/runAllHighBox.sh'
ffcase.TS_high_slurm_prepare(slurm_TS_high)
ffcase.TS_high_batch_prepare(run=False, run_if_ext_missing='.bts', discard_if_ext_present=None)
# ----------- Submit the high-res script (can be done from the command line)


#ffcase.TS_high_slurm_submit()


# ----------- FAST.Farm setup
ffcase.FF_setup()

plt.show()
