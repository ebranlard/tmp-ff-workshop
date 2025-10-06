"""
0. Example 0: `Ex0_Existing_FASTFarm_setup.py`
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
from openfast_toolbox.tools.strings import OK, FAIL, INFO # helper functions, colorful printing functions
from openfast_toolbox.fastfarm.fastfarm import printWT
from openfast_toolbox.fastfarm.fastfarm import plotFastFarmSetup
from openfast_toolbox.io.fast_input_file import FASTInputFile
OK('The toolbox was successfully loaded!')



# --- Plot an existing setup
FFfilepath = './template/FF.fstf'
check_files_exist(FFfilepath)
plotFastFarmSetup(FFfilepath, figsize=(10,3)); # Plot the setup of an existing FAST.Farm file, optional argument plane='XY'
INFO('These errors are expected as part of this tutorial. The goal of this example is to fix them.\n\n')



# --- 0.2 Read and Modify an existing FAST.Farm file
# In this section, we look at the keys available in a FAST.Farm file, we modify some keys (to fix the issue with the low-res domain), and write to a new file.

fstf = FASTInputFile(FFfilepath)

print('Keys available in the input file: ', fstf.keys())
# Let's look at the low resolution inputs:
print('X0_Low:', fstf['X0_Low'])
print('Y0_Low:', fstf['Y0_Low'])
print('Z0_Low:', fstf['Z0_Low'])
print('dX_Low:', fstf['dX_Low'])
print('dY_Low:', fstf['dY_Low'])
print('dZ_Low:', fstf['dZ_Low'])
print('NX_Low:', fstf['NX_Low'])
print('NY_Low:', fstf['NY_Low'])
print('NZ_Low:', fstf['NZ_Low'])


# We can estimate the y-extent:
print('Y_low start : ', fstf['Y0_Low'])
print('Y_low end   : ', fstf['Y0_Low']+fstf['dY_Low']*fstf['NY_Low'])
print('Y_low extent: ', fstf['dY_Low']*fstf['NY_Low'])


# --- Modify the low resolution inputs below so that it's centered about the y=0 line
# fstf['NY_Low'] = ?  # Can you find the value such that the low-res box is centered about the y=0 line?
# fig = plotFastFarmSetup(fstf, plane='YZ', figsize=(10,3))


# --- 
# Let's fix the bounding box of the high-res domain, which is defined using the `N*_High` keys and for each turbine within the key `WindTurbines`.
print('WindTurbine Array from input file:\n',fstf['WindTurbines'],'\n')
# Pretty print
printWT(fstf)
print('')
print('NX_High:', fstf['NX_High'])
print('NY_High:', fstf['NY_High'])
print('NZ_High:', fstf['NZ_High'])

# --- Which parameter should we change to make sure the turbine fits in the domain?
#fstf['NZ_High'] = ?
#fstf['WindTurbines'][0, ?] = ?
#fig = plotFastFarmSetup(fstf, plane='YZ', figsize=(10,3))

# Once we have fixed it, we can write to a new input file:
fstf.write('./_FF_new.fstf')



OK('Example 0 ran successfully')

plt.show()
