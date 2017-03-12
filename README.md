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

## change Log

dataSpanish_0.5 added meanAP
dataSpanish_0.6 added string of time covered  
dataSpanish_0.7 added TRMMUsedMAP and TRMMAllMAP  





