# taurus-strandings
![map of spatial temporal trajectories](docs/img/taurus_header.png?raw=true)

Simulation runs for stranded bulls along the coast of Brittany, which occured in November and December 2023.
This is supplementary code for the [follow the money](https://www.ftm.nl) article, that can be found [here](https://www.ftm.nl/artikelen/aangespoelde-kalfjes-in-bretagne). 

## Main Scripts
Scripts for running a basic forward in time simulation, can be done by running the following scripts:

- **src/01_download_data.py** : downloads datasets within a given timespan and 

    In order to download ocean data from Coperncius, a registration is mandatory. This can be done [here](https://data.marine.copernicus.eu/register).

- **src/02_run_parcels.py** : compute advection forward in time, via seeding from the ship trajectories.

- **src/03_convert_data.py** : convert data to compressed numpy files.

## Data-sources and software

The simulation is based on [Copernicus marine data](https://marine.copernicus.eu), simulations are based on [Parcels](https://oceanparcels.org) software.
