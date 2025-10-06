# FAST.Farm Workshop tutorial

### Installation
git clone the following repository
```bash
git clone https://github.com/ebranlard/tmp-ff-workshop
```

Optional (for postprocessing): 
```bash
pip install dill
```

No need to install anything else, the repository ships with a local copy of `openfast_toolbox` (for now).

### Requirements: 

- All scripts and notebook need to be run from the root of the repository so that the local copy of `openfast_toolbox` gets picked up. 

- Binaries of version v4.x for FAST.Farm and Turbsim (compile from source or donwload the release version on Windows from Github).

- The package ships with `rosco_v9.0.dll` and similar for linux (tested) and mac (not tested)


### Running the examples:    


For jupyter notebooks run `FAST.Farm_Workshop.ipynb` (need to update the binary and dll path at the very beginning). 

For terminal, run Example 1 through 4.  (Example 2 and 3 needs the binary and DLL path to be updated at the beginning)

