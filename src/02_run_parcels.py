from datetime import timedelta, datetime

from parcels import FieldSet, JITParticle, AdvectionRK4
from parcels.tools.converters import GeographicPolar, Geographic

from functions.seeds import create_ais_release_pset
from functions.execution import DeleteErrorParticle
from functions.advection import StokesDrift

# configuration parameters
t_min, t_max = datetime(2023, 11, 11), datetime(2023, 11, 18)
lat_min, lat_max = 45, 50 # latitude
lon_min, lon_max = -8, -3 # longitude

# processes to include
Stokes = True

# specifics on time steps and extent
instance_depth = .4            # mean depth of seed
pdt = timedelta(minutes=15)    # timestep within parcels
t_span = timedelta(days=55)    # total run time of the parcels configuration
dt_output = timedelta(hours=1) # timestep of output from parcels
# sample configuration
dt_samples = timedelta(hours=1)# timestep to release a particle from a track

# admin on locations where models and data are situated and
# results should be placed
ocea_dir = '../data'
ais_dir = '../data'
ais_file = 'ship_locations.csv'

run_name = f'../run/fwd_{datetime.now().strftime("%Y-%m-%d_%H")}.zarr'

# get ocean model into Fieldset
filenames = {
    "U": f"{ocea_dir}/ocean_circulation_2D.nc",
    "V": f"{ocea_dir}/ocean_circulation_2D.nc"
}
variables = {"U": "uo", "V": "vo"}
dimensions = {"lat": "latitude", "lon": "longitude", "time": "time"}

if Stokes:
    filenames.update({
        "Stokes_U": f"{ocea_dir}/stokes_drift.nc",
        "Stokes_V": f"{ocea_dir}/stokes_drift.nc",
        "wave_period": f"{ocea_dir}/stokes_drift.nc"
    })
    variables.update({
        "Stokes_U": "VSDX",
        "Stokes_V": "VSDY",
        "wave_period": "VTPK"
    })

fieldset = FieldSet.from_netcdf(filenames, variables, dimensions,
                                allow_time_extrapolation=True)
fieldset.U.units = GeographicPolar()
fieldset.V.units = Geographic()
if Stokes:
    fieldset.Stokes_U.units = GeographicPolar()
    fieldset.Stokes_V.units = Geographic()

pset = create_ais_release_pset(
        ais_file, ais_dir=ais_dir,
        depth=instance_depth,
        samples_release_interval=dt_samples, t_min=t_min, t_max=t_max,
        t_fmt='%Y-%m-%d %H:%M:%S',
        fieldset=fieldset, pclass=JITParticle, to_write='once'
)

pfile = pset.ParticleFile(name=run_name, outputdt=dt_output)

kernels = []
kernels.append(AdvectionRK4)
if Stokes:
    kernels.append(StokesDrift)
kernels.append(DeleteErrorParticle)

pset.execute(kernels,
             runtime=t_span,
             dt=pdt,
             output_file=pfile)

print(f'analyis done, output can be found at: \n {run_name}')
