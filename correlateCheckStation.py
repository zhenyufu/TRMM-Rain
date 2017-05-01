from rain import *
# fill the gaps for dataSpanish and Atrium datasets

dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
yearLength = 2016 - 1998


f = open('_data/dataSpanish_0.8.2', 'rb')
dataSpanish = pickle.load(f)
for data in dataSpanish:
    print data.fileName
    print data.lat , ",", data.lon
    print data.dateList[0] , "to", data.dateList[-1]
    print data.elevation



aFile = "_data/dataAnnualRatio_0.2"
fa = open(aFile, 'rb')
ratioList  = pickle.load(fa)
ratioDry =  ratioList[0]
ratioWet =  ratioList[1]

#fa = open('_data/dataAtrium_0.2', 'rb')
#dataAtrium = pickle.load(fa)
#dataSpanish.extend(dataAtrium)

# got all the data
for station in dataSpanish:
    if (math.isnan(station.meanAP) or station.meanAP == 0 ):
        continue
    else:
        print "good ", station.fileName , "with MAP:", station.meanAP

    # for TRMM
    dayCounter = TRMMDateList[0]
    endDay = datetime.date(2016,10,30) #TRMMDateList[-1]
    tempArray = []
    tempSum = 0
    while (dayCounter <= endDay):
        for i in range(0, splitLength):
            if isDrySeason(dayCounter.month) == 1:
                 tempSum += prepArray[i,:,:]*ratioDry
             else:
                 tempSum += prepArray[i,:,:]*ratioWet
            dayCounter += datetime.timedelta(days=1)

        tempArray.append(tempSum)
        tempSum = 0


