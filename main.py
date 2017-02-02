from rain import *



print "MAIN: This is the main script"




print "reading spanish data"
f = open('_data/spanish', 'rb')
dataSpanish = pickle.load(f)
for data in dataSpanish:
    print data.fileName
    print data.lat
    print data.lon
    print data.startDate
    print data.endDate




print "reading TRMM data"
dataTRMM = readTRMM("../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc")




