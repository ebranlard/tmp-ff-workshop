import matplotlib.pyplot as plt
import os
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import FFCaseCreation, check_files_exist
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import check_files_exist, plotFastFarmSetup, check_discon_library
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import modifyProperty
from openfast_toolbox.case_generation.runner import runBatch

runTurbSim=True
flat=True


# -----------------------------------------------------------------------------
# ------------------------ General parameters ---------------------------------
# -----------------------------------------------------------------------------
if flat:
    simPath = 'ff_example2a_flat'            # folder (preferably new) where all the simulation files will be written
else:
    simPath = 'ff_example2a_directory'            # folder (preferably new) where all the simulation files will be written
ffbin = './FAST.Farm_x64_v4.1.2.exe' # relative or absolute path of FAST.Farm executable
tsbin = './TurbSim_x64_v4.1.2.exe'   # relative or absolute path of TurbSim executable
# ffbin = './FAST.Farm' # relative or absolute path of FAST.Farm executable
# tsbin = './turbsim'   # relative or absolute path of TurbSim executable

templateFSTF= './template/FF.fstf'
templateFiles = {'libdisconfilepath': './template/libdiscon_rosco_v2.9.0.dll'}
check_files_exist(ffbin, tsbin, templateFiles)
check_discon_library(templateFiles['libdisconfilepath'])
if not check_files_exist(ffbin, tsbin, templateFiles):
    raise Exception('Some files are missing')
if not check_discon_library(templateFiles['libdisconfilepath']):
    raise Exception('DISCO not ready')

# -----------------------------------------------------------------------------
# --------------------------- Farm parameters ---------------------------------
# -----------------------------------------------------------------------------

# ----------- General turbine parameters
cmax     = 5.5    # Maximum blade chord (m), affects dr when mod_wake=1
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
    0 :{'x': 0.0, 'y': 0, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x': 2*D, 'y': D/2, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
}

# plotFastFarmSetup(fastFarmFile, grid=True, fig=None, D=None, plane='XY', hubHeight=None, showLegend=True):
# plotFastFarmSetup(os.path.join(templatePath, templateFiles['FFfilename']))
# plt.show()

# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------

# ----------- Additional variables
zbot = 1        # Bottom of your domain

# ----------- Inflow parameters
inflowType = 'TS'

# ----------- Desired sweeps
vhub       = [8]
shear      = [0.1]
TIvalue    = [7]
inflow_deg = [0]


# -----------------------------------------------------------------------------
# ---------------------- Discretization parameters ----------------------------
# -----------------------------------------------------------------------------
# ----------- Low- and high-res boxes parameters
# High-res boxes settings
tmax = 120      # Total simulation time
mod_wake    = 1    # Wake model. 1: Polar, 2: Curled, 3: Cartesian
dt_high     =  0.5                # sampling frequency of high-res files
ds_high     = 10.0                 # dx, dy, dz of high-res files
extent_high =  1.2                # extent in y and x for each turbine, in D
# Low-res boxes settings
dt_low      =  2.0                 # sampling frequency of low-res files
ds_low      =  25                  # dx, dy, dz of low-res files
extent_low  = [1.5,2.5,1.5,1.5,2] # extent in [xmin,xmax,ymin,ymax,zmax], in D


# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
ffcase = FFCaseCreation(simPath, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, 
                        dt_high=dt_high, ds_high=ds_high, extent_high=extent_high,
                        dt_low=dt_low,   ds_low=ds_low,   extent_low=extent_low,
                        mod_wake=mod_wake, inflowType=inflowType,
                        ffbin=ffbin, tsbin=tsbin, flat=flat)

# ----------- Perform auxiliary steps in preparing the case
ffcase.setTemplateFilename(templateFiles=templateFiles, templateFSTF=templateFSTF)
ffcase.getDomainParameters()
ffcase.copyTurbineFilesForEachCase()
 
# -----------------------------------------------------------------------------
# ---------------------- TurbSim setup and execution --------------------------
# -----------------------------------------------------------------------------
# ----------- TurbSim low-res setup
ffcase.TS_low_setup()
# ----------- Prepare script for submission
ffcase.TS_low_batch_prepare()
if runTurbSim:
    ffcase.TS_low_batch_run(showOutputs=True, showCommand=True, shell_cmd='bash')

# ----------- TurbSim high-res setup
ffcase.TS_high_setup()
ffcase.TS_high_batch_prepare()
if runTurbSim:
    ffcase.TS_high_batch_run(showOutputs=True, showCommand=True, shell_cmd='bash')
# 
# ----------- FAST.Farm setup
ffcase.FF_setup()
print('FFFiles:\n', ffcase.FFFiles)
# modifyProperty(ffcase.FFFiles[0], 'TMax', 80)
modifyProperty(ffcase.FFFiles[0], 'NX_Low', 100)
# 
# 
ffcase.FF_batch_prepare()
ffcase.FF_batch_run()

plt.show()



# ----------- Submit the low-res script (can be done from the command line)
#ffcase.TS_low_slurm_submit()
# slurm_FF_single         = 'C:/W0/ff_walkthrough/SampleFiles/runFASTFarm_cond0_case0_seed0.sh'
# ----------- Submit the high-res script (can be done from the command line)
# slurm_TS_low  = './SampleFiles/runAllLowBox.sh'
# ffcase.TS_low_slurm_prepare(slurm_TS_low)
#  # ----------- Prepare script for submission
# slurm_TS_high           = './SampleFiles/runAllHighBox.sh'
# # ffcase.TS_high_slurm_prepare(slurm_TS_high)
# #ffcase.TS_high_slurm_submit()
