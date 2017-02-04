from rain import *


inPath = "../../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc"
inTRMM = netCDF4.Dataset(inPath,'r')

# 4D: lat, lon, date, precipitation
#     f    f    date  f
# python dict: dict[date] = a numpy 3d array of lat*lon*precipitation

date = datetime.date(1998,1,1)

dateList = [] # date (6878)
dataTRMM = np.empty((240, 260,62400))
# 3d array of lon, lat, prep
#             240, 260, 6878


for i in range(0, 6878):
    print i
    print date
    dateList.append(date)

    date += datetime.timedelta(days=1)

    # access the lat lon precipitation for the current year
    prep = inTRMM.variables['precipitation'][i][:][:]







