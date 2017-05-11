from rain import *
# fill the gaps for dataSpanish and Atrium datasets

dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
yearLength = 2016 - 1998
splitLength = 365

f = open('_data/dataSpanish_0.8.4', 'rb')
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
mapArray = []
stationMap = []
# got all the data
for station in dataSpanish:
    if (math.isnan(station.meanAP) or station.meanAP == 0 ):
        continue
    else:
        print "good"
    print "good ", station.fileName , "with MAP:", station.meanAP
    stationMap.append(station.meanAP)
    # for TRMM
    allLat = dataTRMM.variables['lat'][:]
    allLon = dataTRMM.variables['lon'][:]

    nearLat, iLat = takeClosest(allLat, station.lat)
    nearLon, iLon = takeClosest(allLon, station.lon)

    print "ratios" , str(ratioDry[iLon][iLat]), "," , str(ratioWet[iLon][iLat])

    #iDay = 0
    # prepArray = dataTRMM.variables['precipitation'][:,iLon, iLat]
    dayCounter = TRMMDateList[0]
    endDay = datetime.date(2016,10,30) #TRMMDateList[-1]
    tempArray = []

    while (dayCounter <= endDay):
        tempSum = 0
        for i in range(0, splitLength):
            iDay = TRMMDateList.index(dayCounter)
            if isDrySeason(dayCounter.month) == 1:
                #print "dry" , ratioDry[iLon, iLat], "or" ,ratioDry[iLat, iLon]
                tempSum += dataTRMM.variables['precipitation'][iDay,iLon, iLat] * ratioDry[iLon, iLat]
            else:
                tempSum += dataTRMM.variables['precipitation'][iDay,iLon, iLat] * ratioWet[iLon, iLat]
            dayCounter += datetime.timedelta(days=1)
            if dayCounter > endDay:
                break
            #iDay++
        if dayCounter > endDay:
            break
        tempArray.append(tempSum)
        tempSum = 0
    print tempArray
    m = np.mean(tempArray)
    print station.fileName , "has annual of years" , len(tempArray), "this gives MAP" , m
    mapArray.append(m)
    print "************"


print "station actual" , stationMap
# finished with all stations
fig = plt.figure()
plt.scatter(mapArray, stationMap, c= "blue")
plt.xlabel('Calculated ')
plt.ylabel("Actual ")


plt.xlim([0,20000])
plt.ylim([0,20000])


aFile = "plot/check1"
out = open(aFile, 'wb')
dataAll = []
dataAll.append(mapArray)
dataAll.append(stationMap)
pickle.dump(dataAll, out, pickle.HIGHEST_PROTOCOL)
out.close()


plt.show()
