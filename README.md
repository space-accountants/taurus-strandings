# taurus-strandings
Simulation runs for stranded bulls along the coast of Brittany, which occured in November and December 2023.
This is supplementary code for the followthemoney article, that can be found [here](www.ftm.nl). 

#### Main Scripts


- **src/01_download_data.py** : downloads datasets within a given timespan and 

    In order to download ocean data from Coperncius, a registration is mandatory. This can be done [here](https://data.marine.copernicus.eu/register).

- **src/02_run_parcels.py** : compute advection forward in time, via seeding from the ship trajectories.

- **src/03_convert_data.py** : convert data to compressed numpy files.
