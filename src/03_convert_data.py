import os

import numpy as np
import xarray as xr


run_dir = '../run'

# find latest run in folder
dir_list = [f.path for f in os.scandir(run_dir) if f.is_dir()]
dir_list.sort(key=lambda x: os.path.getmtime(x))
run_name = dir_list[-1] # take the newest run

# read output
pfile = xr.open_zarr(run_name, decode_cf=True)
lon_p = np.ma.filled(pfile.variables['lon'], np.nan)
lat_p = np.ma.filled(pfile.variables['lat'], np.nan)
time_p = np.ma.filled(pfile.variables['time'], np.nan)
instance_p = np.ma.filled(pfile.variables['instance'], np.nan)

# export data to compressed numpy format
np.savez(os.path.splitext(os.path.basename(run_name))[0] + '.npz',
         run_name, lon_p, lat_p, time_p, instance_p)