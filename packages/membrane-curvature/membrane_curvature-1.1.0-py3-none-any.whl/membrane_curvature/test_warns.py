from membrane_curvature.base import MembraneCurvature
import MDAnalysis as mda
import time
t0 = time.time()
dir_ = '/Users/estefania/python_playground/abca1/test'
grofile = f"{dir_}/ABCA1_sym.gro"
trjfile = f"{dir_}/25-30us_ABCA1_S1_rt.xtc"

u = mda.Universe(grofile, trjfile)

curv = MembraneCurvature(u,          # universe
                        select= f'name PO4 and index 14591-26462', # selection of reference
                        n_x_bins=10,       # number of bins in the x dimension
                        n_y_bins=10,       # number of bins in the y_dimension
                        wrap=False).run()
t1 = time.time()
print(t0-t1)