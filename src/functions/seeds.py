import os

import numpy as np
import pandas as pd
import geopandas as gpd
import movingpandas as mpd

from datetime import datetime, timedelta, date
from parcels import JITParticle, ParticleSet, Variable

def create_ais_release_pset(
        ais_file, ais_dir=None,
        samples_release_interval=timedelta(hours=3), samples_per_point=200,
        t_fmt='%Y-%m-%d %H:%M:%S',
        t_min=None, t_max=None, depth=None,
        fieldset=None, pclass=JITParticle, to_write=False
):
    pclass.instance = Variable('instance',
                               dtype=np.int16,
                               initial=0,
                               to_write=to_write)

    # get ship into trajectory collection
    if ais_dir == None:
        ais_dir = os.getcwd()
    ais_data = pd.read_csv(os.path.join(ais_dir, ais_file))
    gdf = gpd.GeoDataFrame(ais_data, crs="EPSG:4326",
                           geometry=gpd.points_from_xy(ais_data.lon,
                                                       ais_data.lat))
    gdf = gdf.to_crs(epsg=4326)
    gdf['t'] = pd.to_datetime(gdf['timestamp'], format=t_fmt)
    traj_col = mpd.TrajectoryCollection(gdf, 'name', t='t')
    del ais_data, gdf

    t_seed_min = datetime.strptime(traj_col.get_min('timestamp'), t_fmt)
    t_seed_max = datetime.strptime(traj_col.get_max('timestamp'), t_fmt)
    if t_min != None:
        t_seed_min = max([t_min, t_seed_min])
    if t_max != None:
        t_seed_max = min([t_max, t_seed_max])

    t_seed_list = time_range(t_seed_min, t_seed_max, samples_release_interval)

    Lon,Lat,Time,Inst = [], [], [], []
    # create spatial temporal particle set
    for t_samp in t_seed_list:
        for idx, traj in enumerate(traj_col):
            xy = traj.interpolate_position_at(t_samp)
            Lon.append(xy.x)
            Lat.append(xy.y)
            Time.append(t_samp)
            Inst.append(idx)

    if isinstance(depth, float):
        Depth = [depth] * len(Lat)
    else:
        Depth = None

    return ParticleSet.from_list(
        fieldset=fieldset,
        pclass=pclass,
        lon=Lon,
        lat=Lat,
        time=Time,
        depth=Depth,
        instance=Inst
    )

def time_range(start_date, end_date, dt):
    """ create list with two time instances, at a given interval

    Examples
    --------
    >>> start_date = datetime(2022, 11, 28, 19, 54, 0)
    >>> end_date = datetime(2022, 11, 28, 19, 56, 0)
    >>> dt = timedelta(seconds=12)

    >>> time_range(start_date, end_date, dt)
    [datetime.datetime(2022, 11, 28, 19, 54),
     ...
     datetime.datetime(2022, 11, 28, 19, 55, 48),
     datetime.datetime(2022, 11, 28, 19, 56)]
    """
    assert isinstance(start_date, date), "please provide a datetime entry"
    assert isinstance(end_date, date), "please provide a datetime entry"
    assert isinstance(dt, timedelta), "please provide a timedelta entry"
    tr = np.arange(start_date, end_date, dt).astype(datetime).tolist()
    tr.append(end_date)
    return tr