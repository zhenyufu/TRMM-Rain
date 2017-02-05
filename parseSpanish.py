from rain import *

dataSpanish = readSpanish("raw_senamhi/");
for data in dataSpanish:
    print data.fileName
    print data.startDate
    print data.endDate

# dataTRMM = readTRMM("../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc")
out = open('_data/dataSpanish', 'wb')
pickle.dump(dataSpanish, out, pickle.HIGHEST_PROTOCOL)







# dataTRMM.variables['lon'][:]
# precipitation:   (u'time', u'lon', u'lat')
# access precipitation:
#  dataTRMM.variables['precipitation'][3:88,-76.375,14.125]
#print len(dataSpanish[0])
#print len(dataSpanish[0][0])

