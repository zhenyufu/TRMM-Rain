from rain import *


dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
# 1998/1/1 datetime.date(2016, 10, 30)
yearLength = 2016 - 1998

cFile = "_data/dataCorrelation_0.3"
aFile = "_data/dataAnnualRatio_0.1"



f = open(cFile, 'rb')
dataCorrelation = pickle.load(f)
annualC =  dataCorrelation[-1]
popt = annualC.popt
a = popt[0]
b = popt[1]

prepArray = dataTRMM.variables['precipitation'][:,:,:]


dataTRMMMAP = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));
allMAP = np.zeros((yearLength , prepArray.shape[1] , prepArray.shape[2] ));
temp = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));

dayCounter = TRMMDateList[0]


i = 0
year = 0
while (dayCounter.year != 2016):
    #print i, "is day", dayCounter , "shapes",  temp.shape , "and " ,  prepArray[i,:,:].shape

    temp += prepArray[i,:,:]
    #temp = np.add(temp, prepArray[i,:,:])
    # detect end of year
    if dayCounter.month == 12 and dayCounter.day == 31:
        allMAP[year,:,:] = temp
        year += 1
        temp = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));
        #allMAP.append(temp)
    dayCounter += datetime.timedelta(days=1)
    i += 1


print "allMAP length", len(allMAP)
dataTRMMMAP = np.mean(allMAP, axis = 0)
print "shape" , dataTRMMMAP.shape


## correction
corrected = ((dataTRMMMAP)/ a )**(1/(b+1))
dataRatioMAP = corrected / dataTRMMMAP


## output
out = open(aFile, 'wb')
pickle.dump(dataRatioMAP, out, pickle.HIGHEST_PROTOCOL)
out.close()



