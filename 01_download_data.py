# prepare datasests via downloading from Copernicus Marine Services

import os
import copernicus_marine_client as copernicusmarine

from datetime import datetime

# configuration parameters
t_start, t_end = datetime(2023, 11, 11), datetime(2023, 12, 26)
lat_min, lat_max = 45, 50 # latitude
lon_min, lon_max = -8, -3 # longitude

# processes to include
Stokes = True
Ocean = True

# file organization
dat_dir = '../data'

print('downloading ocean data')
if Stokes:
   copernicusmarine.subset(
      dataset_id = "cmems_mod_ibi_wav_anfc_0.05deg_PT1H-i",
      variables = ['VSDX',  # sea_surface_wave_stokes_drift_x_velocity
                   'VSDY',  # sea_surface_wave_stokes_drift_y_velocity
                   'VTPK'], # sea_surface_wave_period_at_variance_spectral_density_maximum
      start_datetime = t_start.strftime('%Y-%m-%dT%H:%M:%S'),
      end_datetime = t_end.strftime('%Y-%m-%dT%H:%M:%S'),
      minimum_longitude = lon_min,
      maximum_longitude = lon_max,
      minimum_latitude = lat_min,
      maximum_latitude = lat_max,
      minimum_depth = 0,
      maximum_depth = 5,
      output_filename = os.path.join(dat_dir, "stokes_drift.nc"),
   )

if Ocean:
   copernicusmarine.subset(
      dataset_id = "cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-i",
      variables = ['uo', 'vo'],
      start_datetime=t_start.strftime('%Y-%m-%dT%H:%M:%S'),
      end_datetime=t_end.strftime('%Y-%m-%dT%H:%M:%S'),
      minimum_longitude=lon_min,
      maximum_longitude=lon_max,
      minimum_latitude=lat_min,
      maximum_latitude=lat_max,
      output_filename = os.path.join(dat_dir, "ocean_circulation_2D.nc"),
   )
