import netCDF4
import datetime


inPath = "../../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc"
inFile = netCDF4.Dataset(inPath,'r')


outPath = "../../TRMM_3B42_Daily_precipitation.7.SouthAmerica.edit.nc"
outFile = netCDF4.Dataset(outPath,'w', format='NETCDF4')



date = datetime.date(1998,1,1)


outFile = inFile

for i in range(0, 6878):
    print i


    d = date.isoformat() #YYYY-MM-DD
    print d
    outFile.variables["time"][i] = d# cannot write due to its type being float
    print outFile.variables['time'][i]


    date += datetime.timedelta(days=1)






inFile.close()
outFile.close()



