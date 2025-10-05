import os
import matplotlib.pyplot as plt
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import check_files_exist, plotFastFarmSetup
from openfast_toolbox.fastfarm.fastfarm import printWT

FFfilepath = './template/FF_ForInitialDebug.fstf'
FFfilepath = './template/FF.fstf'

# plotFastFarmSetup(FFfilepath)
# plotFastFarmSetup(FFfilepath, plane='XZ')
# plotFastFarmSetup(FFfilepath, plane='YZ')






from openfast_toolbox.io.fast_input_file import FASTInputFile
fstf = FASTInputFile(FFfilepath)
# print('Keys available in the input file: ', fstf.keys())


printWT(fstf)


# fstf['dY_Low'] = 40
# 
# plotFastFarmSetup(fstf)
# 
# 
# D=240
# wts = {
#     0 :{'x': 0.0, 'y': 0, 'z':0.0, 'D':D},
#     1 :{'x': 5*D, 'y': D/2, 'z':0.0, 'D':D},
# }
# plotFastFarmSetup(wts)

plt.show()
