from rain import *


inPath = "../../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc"
inFile = netCDF4.Dataset(inPath,'r')

# 4D: lat, lon, date, precipitation
#     f    f    date  f
# python dict: dict[date] = a numpy 3d array of lat*lon*precipitation

date = datetime.date(1998,1,1)

dateList = []

for i in range(0, 6878):
    print i

    d

    date += datetime.timedelta(days=1)









