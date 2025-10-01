### Load the openfast_toolbox and import the main class we will use `FFCaseCreation`
from openfast_toolbox.fastfarm.FASTFarmCaseCreation import FFCaseCreation
from openfast_toolbox.tools.strings import OK

OK('The toolbox was successfully loaded!')

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
    0 :{'x':  0.0, 'y':    0,  'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T1'},
    1 :{'x':  5*D, 'y':   D/2, 'z':0.0, 'D':D, 'zhub':zhub, 'cmax':cmax, 'fmax':fmax, 'Cmeander':Cmeander, 'name':'T2'},
}
# -----------------------------------------------------------------------------
# ------------------- Inflow conditions and input files -----------------------
# -----------------------------------------------------------------------------
# ----------- Additional variables
mod_wake = 2    # Wake model. 1: Polar, 2: Curled, 3: Cartesian. NOTE: Resolution guidelines vary based on this.
# ----------- Inflow parameters
inflowType = 'TS' # TS: TurbSim, or LES: LES (VTK files needs to exist)
# ----------- Desired sweeps
vhub       = [8]  # NOTE: use the maximum velocity here


# -----------------------------------------------------------------------------
# -------------------- FAST.Farm initial setup --------------------------------
# -----------------------------------------------------------------------------
# ----------- Initial setup
# Below we provide the minimal set of arguments needed to compute the resolution automatically.
ffcc = FFCaseCreation(wts=wts, vhub=vhub, 
                      mod_wake=mod_wake,
                      inflowType=inflowType)
