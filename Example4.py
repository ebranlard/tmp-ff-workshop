""" 
4. Some post-processing
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



print('# --------------------------------------------------------------------------------')
print('# ---  4.1 Basic postprocessing')
print('# --------------------------------------------------------------------------------')
# We use the io package to read single `.outb`, `.out`, or `.vtk` files
from openfast_toolbox.io import FASTOutputFile, VTKFile
df1 = FASTOutputFile('ff_example2_onesim/FF.T1.outb').toDataFrame()
df2 = FASTOutputFile('ff_example2_onesim/FF.T2.outb').toDataFrame()
print('# The columns available are:\n', list(df1.columns))

col = 'RotPwr_[kW]'
fig, ax = plt.subplots(1,1,figsize=(10,3.5))
ax.plot(df1['Time_[s]'], df1[col], label='Turbine 1')
ax.plot(df2['Time_[s]'], df2[col], label='Turbine 2')
ax.set_xlabel('Time [s]')
ax.set_ylabel(col.replace('_', ' '))
ax.legend();


vtk = VTKFile('ff_example2_onesim/vtk_ff/FF.Low.DisXY001.060.vtk')
print(vtk)


u = vtk.point_data_grid['Velocity'][:,:,:,0]
v = vtk.point_data_grid['Velocity'][:,:,:,1]
w = vtk.point_data_grid['Velocity'][:,:,:,2]
fig, ax = plt.subplots(1,1,figsize=(10,3.5))
vtk.xp_grid
vtk.yp_grid
im=ax.contourf(vtk.xp_grid, vtk.yp_grid, u[:,:,0].T)
fig.colorbar(im)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_aspect('equal','box')
ax.set_title('Streamwise velocity in horizontal plane');


print('# --------------------------------------------------------------------------------')
print('# ---  4.2 More advanced postprocessing')
print('# --------------------------------------------------------------------------------')
# # 
# - We reload the ffcase setup (need the package dill)
# - We use dedicated FAST.Farm postprocessing functions that stores the postprocessed data in xarrays and netcdf format

# Let's load the object of the case we executed until the end
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import load
#path = 'ff_example2_onesim'
path = 'ff_example3_seeds'
ff = load(path)


# Dedicated FAST.Farm postprocessing
from openfast_toolbox.fastfarm.postpro.ff_postpro import readTurbineOutput, readTurbineOutputPar, readFFPlanes, readFFPlanesPar

# There are serial and parallel versions of the functions to read turbine data and vtk slices.


# Let's read all the turbine data, but we don't need the results at the full resolution.
dt_openfast = 0.01
dt_processing = 0.1
ds_turbs = readTurbineOutput(ff, dt_openfast, dt_processing, output='nc')

print(ds_turbs)

# Mean power across the seeds and the simulation time can easily be obtained with:
ds_turbs.mean(dim=['seed','time'])['RotPwr_[kW]'].values
# (note that this is a dummy simulation and the data is still in its transient)

print('Conditions:', ds_turbs.cond.values)
print('Turbines  :',ds_turbs.turbine.values)
print('Cases     :',ds_turbs.case.values)
print('Seeds     :',ds_turbs.seed.values)
# How to select one time series
print('Time vector shape:', ds_turbs.time.shape)
print('Time series shape:', ds_turbs['GenPwr_[kW]'].sel(case='Case0_wdirp00', cond='Cond00_v08.0_PL0.1_TI7', seed=0, turbine=1).shape)


fig, ax = plt.subplots(1,1,figsize=(10,3.5))
for cond in ds_turbs.cond.values:
    for case in ds_turbs.case.values:    
        for seed in ds_turbs.seed.values:
            for turb in ds_turbs.turbine.values:
                ax.plot(ds_turbs.time, ds_turbs['GenPwr_[kW]'].sel(case=case, cond=cond, seed=seed, turbine=turb),
                    label=f"case={case}, cond={cond}, seed={seed}, turb={turb}"
            )
ax.set_xlabel("Time [s]")
ax.set_ylabel("GenPwr [kW]")
ax.legend();


# Let's get the planes of data
# NOTE the parallel version does not work from the terminal
# ds_planes = readFFPlanesPar(ff, sliceToRead='z', saveOutput=False, itime=0, ftime=-1, nCores=1)
ds_planes = readFFPlanes(ff, slicesToRead=['z'], saveOutput=False, itime=0, ftime=-1)
# 
xx, yy = np.meshgrid(ds_planes.x, ds_planes.y, indexing='ij')
fig, ax = plt.subplots(1,1,figsize=(10,3.5))
cm = ax.pcolormesh(xx, yy, ds_planes.squeeze()['u'].mean(dim=['time','seed']))
#cm = ax.pcolormesh(xx, yy, ds_planes.squeeze()['u'].mean(dim=['time']))
fig.colorbar(cm)
ax.set_aspect('equal')


fig, ax = plt.subplots(1,1,figsize=(12,3.5))
cm = ax.pcolormesh(xx, yy, ds_planes.squeeze()['u'].isel(time=-1,seed=0))
#cm = ax.pcolormesh(xx, yy, ds_planes.squeeze()['u'].isel(time=-1))
ax.set_aspect('equal')
fig.colorbar(cm);


OK('Example 4 ran successfully')

plt.show()
