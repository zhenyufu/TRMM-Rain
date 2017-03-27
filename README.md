# rain

Thesis

## require 
* python
* BeautifulSoup for parsing
* netcdf4: https://github.com/Unidata/netcdf4-python
    * git clone 
    * pip install h5py
    * pip install netcdf4
* pip install tables


## _data/dataSpanish change log
* original from running parseSpanish
* 0.1 added lat and lon to all stations 


### GDAL for netcdf - untested did not use:
```
apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip install GDALi==1.10.0
```

## Running 

Run 


python -i main.py

## _data change Log

dataSpanish_0.5 added meanAP
dataSpanish_0.6 added string of time covered  
dataSpanish_0.7 added TRMMUsedMAP and TRMMAllMAP 
dataSpanish_0.8 added actual station names 
dataSpanish_0.8.1 changed to invalidating everythin -999 -1 and empty



dataCorrelation_0.1 added dry and wet correlation data
dataCorrelation_0.2 changed units to mm
dataCorrelation_0.3 added annual

dataRatioMAP_0.1 2d grid of ralationship of station/TRMM
