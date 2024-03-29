from rain import *
#from scipy.optimize import curve_fit
#import scipy.optimize.curve_fit as curve_fit

print "MAIN: This is the main script"
#hostPath = "/media/sf_myshareDebianMain/"
splitLength = 365
yearThreshold = 0.1 # 10%
# 1 is by day
# 30
# 365
plotElevation = True #True # use only with isMeaned = True
calEveryMonth = True
isMeaned = True
bySeason = False # e
seasonThreshold = 0.1
# Wet: 11-4
# dry: 5-10
doCalTRMMAll = False # True

plotType = 3
# 0 doulbe scatter with time
# 1 double line with time
# 2 correlation
# 3 ratio over weather station
# 5 differnt x  - not working yet
kml = simplekml.Kml()
kmlName = hostPath + "comparison_Spanish_TRMM_" + str(splitLength) + ".kml"
isClark = False
clarkRain = [1908, 2148, 1752, 2940, 4140, 4116, 5436]
clarkTRMM = [1800, 2516, 1600, 3154, 4152, 3998, 4831]
isAtrium =  True #False

isAllThree = True #False
###########################################################
print "reading spanish data"
f = open('_data/dataSpanish_0.8.4', 'rb')
dataSpanish = pickle.load(f)

#dataSpanish = dataSpanish[:-4] ######################################### remove the altrium

for data in dataSpanish:
    print data.fileName
    print data.lat , ",", data.lon
    print data.dateList[0] , "to", data.dateList[-1]
    print data.elevation

if isAtrium:
    fa = open('_data/dataAtrium_0.2', 'rb')
    dataAtrium = pickle.load(fa)
    dataSpanish.extend(dataAtrium)


print "reading TRMM data"
#dataTRMM = readTRMM("../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc")
dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")



#TRMM date fixi
#TRMMDateList = []
#TRMMDate = datetime.date(1998,1,1)

#for i in range(0, 6878):
#     TRMMDateList.append(TRMMDate)
#     TRMMDate += datetime.timedelta(days=1)

#print TRMMDateList[0], "to", TRMMDateList[-1]




totalSpanish = []
totalTRMM = []
totalSpanish2 = []
totalTRMM2 = []

errorArray = []
elevationArray = []
##############################################
iStation = 0
for station in dataSpanish:
    dataSpanish[iStation].lapStart = "na"
    dataSpanish[iStation].lapEnd = "na"
    dataSpanish[iStation].numOverlap = 0
    dataSpanish[iStation].numObservation = 0# overLap - missCount
    dataSpanish[iStation].numOfMissing =  0 #missCount


    if splitLength == 365 and isMeaned:
        dataSpanish[iStation].meanAP = 0
        dataSpanish[iStation].yearUsed = ""
        dataSpanish[iStation].TRMMUsedMAP = 0
        dataSpanish[iStation].TRMMAllMAP = 0


    print "######### processing:",station.fileName
    nearLat = 0
    nearLon = 0
    allLat = dataTRMM.variables['lat'][:]
    allLon = dataTRMM.variables['lon'][:]


    nearLat, iLat = takeClosest(allLat, station.lat)
    nearLon, iLon = takeClosest(allLon, station.lon)
    print "using location(lat,lon)", nearLat, "," , nearLon
    print "with index" , iLat, iLon
    # get time range


    # calculate dataSpanish[iStation].TRMMAllMAP
    if splitLength == 365 and isMeaned and  doCalTRMMAll:
        allByYear = []
        allOneYear = 0
        currentYear = 1998
        tempDay = datetime.date(1998,1,1)
        while tempDay != datetime.date(2016,1,1): # ignore the rest of 2016 to 10/30
            i = TRMMDateList.index(tempDay)
            allOneYear += dataTRMM.variables['precipitation'][i,iLon,iLat];
            tempDay += datetime.timedelta(days=1)
            if tempDay.year != currentYear:
                #print "year: ", currentYear, "had",allOneYear, "which was up to the day before ", tempDay
                currentYear +=1
                allByYear.append(allOneYear)
                allOneYear = 0
        dataSpanish[iStation].TRMMAllMAP = np.mean(allByYear)




    overLap , lapStart, lapEnd = getOverlap(TRMMDateList[0], TRMMDateList[-1], station.dateList[0], station.dateList[-1])
    if overLap > 0:
        # strange stuff
        if station.fileName == "raw_senamhi/madre5.csv":
            lapEnd = datetime.date(2016,10,6)
            overLap = (lapEnd - lapStart).days
        print "days: ", overLap
        print lapStart, "to", lapEnd
        dataSpanish[iStation].lapStart = lapStart
        dataSpanish[iStation].lapEnd = lapEnd
        dataSpanish[iStation].numOverlap = overLap
        # station.numObservation = len(station.dateList)
        # station.numOfMissing = overLap - len(station.dateList)

        # acess index
        #indexStationStart = station.dateList.index(lapStart)
        #indexTRMMStart = TRMMDateList.index(lapStart)

        #indexStationEnd = station.dateList.index(lapEnd)
        #indexTRMMEnd = TRMMDateList.index(lapEnd)

        #print indexStationStart
        #print indexStationEnd
        #print indexTRMMStart
        #print indexTRMMEnd


        # access prep
        #dSpanish = station.listPrep[indexStationStart: indexStationEnd]
        #dTRMM = dataTRMM.variables['precipitation'][indexTRMMStart:indexTRMMEnd,nearLat,nearLon]

        #print dSpanish.shape
        #print dTRMM.shape


        # interate through the overlap time and get the useable dates
        dDate = [] # the start date if cumalating
        dSpanish = []
        dTRMM = []
        #if bySeason:
        dDate2 = [] # the start date if cumalating
        dSpanish2 = []
        dTRMM2 = []

        dayCounter = lapStart
        plt.ion()# turns on interactive mode to enable plotting more
        dataDone = False
        meanCount = 0

        if bySeason:
            # must start by 5 or 11
            while not(dayCounter.month == 5 or dayCounter.month == 11):
                dayCounter += datetime.timedelta(days=1)

        missCount = 0
        monthCumu = 0
        monthCurrent =  dayCounter.month

        while( dayCounter <= lapEnd):
            # for everyday in slpitLength
            print dayCounter
            cumuDay = dayCounter
            # 1 is dry, 2 is wet
            cumuSpanish = 0
            cumuTRMM = 0
            cumuSpanish2 = 0
            cumuTRMM2 = 0
            seasonId = isDrySeason(dayCounter.month) # -1 # true for dry, false for wet
            if bySeason:
                if seasonId == -1:
                    dayCounter += datetime.timedelta(days=1)
                    continue

                seasonMiss = 0
                print "season start:", dayCounter, "with id" , isDrySeason(dayCounter.month), "in season", seasonId
                while isDrySeason(dayCounter.month) ==  seasonId and dayCounter <= lapEnd:

                    p = -1
                    try:
                        iSpanish = station.dateList.index(dayCounter)
                        iTRMM = TRMMDateList.index(dayCounter)
                        p = station.listPrep[iSpanish]
                    except:
                        missing1 = dayCounter - datetime.timedelta(days=1)
                        while True:
                             try:
                                 iSsss = station.dateList.index(missing1)
                                 break
                             except:
                                 missing1 -= datetime.timedelta(days=1)
                                 pass


                        tempCounter = dayCounter
                        while True:
                           # print "checking" , tempCounter
                            try:
                                iSpanish = station.dateList.index(tempCounter)
                                break
                            except:
                                tempCounter += datetime.timedelta(days=1)
                                if tempCounter == station.dateList[-1]:
                                    break
                                pass
                        # comes out of the continuous missing days
                        missing2 = tempCounter
                        missed = (missing2 - missing1).days - 1
                        if missed > 18:
                            dayCounter += datetime.timedelta(days=1)
                            seasonMiss +=1
                            continue
                        # calculate and loop through to put them back
                        i1 = station.dateList.index(missing1)
                        i2 = station.dateList.index(missing2)

                        prep1 = station.listPrep[i1]
                        prep2 = station.listPrep[i2]


                        #######################
                        x1 = 0
                        x2 = missed + 1
                        x3 = (dayCounter - missing1).days
                        dList = [x1, x2]
                        pList = [prep1, prep2]
                        popt, pcov = curve_fit(curveLinear,dList,pList )
                        p = popt[0] * x3 + popt[1]

                        # p = (prep1 + prep2)/2




                        print "Missing" , missed ,"between points:", missing1 ,"-" , missing2, ":", prep1 ,",", prep2
                        print "day " , dayCounter, "prep", p


                       # dayCounter += datetime.timedelta(days=1)
                       # seasonMiss +=1
                        #continue
                    # print "p is " , p
                    if p >= 0:
                        addSpanish = p
                        addTRMM = dataTRMM.variables['precipitation'][iTRMM,iLon,iLat]
                        #if station.fileName == "raw_senamhi/cusco4.csv" and  dayCounter.year == 2007 and dayCounter.month == 3:
                         #   print "on" ,dayCounter , "and p is", str(p)
                    else:
                        seasonMiss +=1
                        print "got" , str(p) , "on" , dayCounter, "----", str(cumuSpanish2)
                        dayCounter += datetime.timedelta(days=1)
                        continue

                    if isDrySeason(dayCounter.month) == 1:
                        cumuSpanish += addSpanish
                        cumuTRMM += addTRMM
                    elif isDrySeason(dayCounter.month) == 2:
                        cumuSpanish2 += addSpanish
                        cumuTRMM2 += addTRMM
                    else:
                        dayCounter += datetime.timedelta(days=1)
                        continue
                    #print "addinggggggggg"
                    dayCounter += datetime.timedelta(days=1)
                if dayCounter > lapEnd:
                    break
                print "season end:", dayCounter
                print "missed days in season", seasonMiss


                if isDrySeason(dayCounter.month) == 1:
                    print str(cumuSpanish2)
                elif isDrySeason(dayCounter.month) == 2:
                    print str(cumuSpanish)
                print "**********"
                if (seasonMiss) / 180.0 < seasonThreshold:
                    # seasonMiss = 0
                    if seasonId == 1:
                        dSpanish.append(cumuSpanish)
                        dTRMM.append(cumuTRMM)
                    elif seasonId == 2:
                        dSpanish2.append(cumuSpanish2)
                        dTRMM2.append(cumuTRMM2)

                seasonId = isDrySeason(dayCounter.month)
                continue
            tempMiss  = 0
            # else ##################
            for i in range(0, splitLength):
                if (dayCounter > lapEnd):
                    dataDone = True
                    break;
                # print dayCounter
                p = -1
                try:
                    # get index
                    iSpanish = station.dateList.index(dayCounter)
                    iTRMM = TRMMDateList.index(dayCounter)
                    #if station.fileName == "raw_senamhi/madre5.csv":
                    p = station.listPrep[iSpanish]
                    #    print dayCounter, "and", overLap
                except:
                    # this date is not in one of the two lists
                    missCount +=1
                    tempMiss +=1
                    #if (station.fileName != "raw_senamhi/cusco4.csv" and station.fileName != "raw_senamhi/cusco5.csv" and station.fileName != "raw_senamhi/cusco6.csv"):
                    #    i-=1
                    dayCounter += datetime.timedelta(days=1)

                    continue

                # get the prep only if the station is not -1
                if p >= 0:
                    cumuSpanish += p
                    cumuTRMM += dataTRMM.variables['precipitation'][iTRMM,iLon,iLat]
                else:
                    missCount +=1
                    dayCounter += datetime.timedelta(days=1)
                    continue

                dayCounter += datetime.timedelta(days=1)

                if calEveryMonth:
                    if monthCurrent == dayCounter.month:
                        monthCumu += p
                        #if station.fileName == "raw_senamhi/cusco4.csv" and monthCurrent == 2 :
                        #    print "adding" , str (dataTRMM.variables['precipitation'][iTRMM,iLon,iLat])

                    else:
                        monthCumu += p # last day
                        print "for" , str(dayCounter.year), ":"  ,str(monthCurrent) , "-" , str(dayCounter.month), "has", str(monthCumu)
                        monthCurrent =  dayCounter.month
                        monthCumu = 0

            if (dataDone):
                break;
            if splitLength == 365 and isMeaned:
                print dayCounter.year - 1, "-", dayCounter.year , "had miss points: " , tempMiss ,"/365 = " , str((tempMiss) / 365.0)
                        # end for i in range(0, splitLength):
            if splitLength == 365 and isMeaned:
                if (tempMiss) / 365.0 < yearThreshold:
                    dDate.append(cumuDay)
                    dSpanish.append(cumuSpanish)
                    dTRMM.append(cumuTRMM)
                    meanCount +=1
                    dataSpanish[iStation].yearUsed += ( str(dayCounter.year - 1) + "-to-" + str(dayCounter.year) + " | " )
            else:
                dDate.append(cumuDay)
                dSpanish.append(cumuSpanish)
                dTRMM.append(cumuTRMM)
                meanCount +=1
        # end of while( dayCounter <= lapEnd):

        dataSpanish[iStation].numObservation = overLap - missCount
        dataSpanish[iStation].numOfMissing = missCount
        print "total missed:", missCount

        print "Mean by", meanCount
        if isMeaned:
            print "dSpanish", dSpanish
            print "dSpanish2", dSpanish2
            if not overLap < splitLength and len(dSpanish) !=0:
                elevationArray.append(station.elevation)
            dSpanish = np.mean(dSpanish)
            dTRMM = np.mean(dTRMM)
            totalSpanish.append(dSpanish)
            print "station:" + station.fileName
            print "meaned is:" ,dSpanish
            if splitLength == 365 and isMeaned:
                dataSpanish[iStation].meanAP = dSpanish
                dataSpanish[iStation].TRMMUsedMAP = dTRMM
            totalTRMM.append(dTRMM)

            if bySeason:
                dSpanish2 = np.mean(dSpanish2)
                dTRMM2 = np.mean(dTRMM2)
                totalSpanish2.append(dSpanish2)
                totalTRMM2.append(dTRMM2)
                print totalTRMM2

        elif bySeason and not isMeaned:
            totalSpanish.extend(dSpanish)
            totalTRMM.extend(dTRMM)
            totalSpanish2.extend(dSpanish2)
            totalTRMM2.extend(dTRMM2)

        else:
            totalSpanish.extend(dSpanish)
            totalTRMM.extend(dTRMM)

        print "totalSpanish:", totalSpanish
        print "totalTMM:", totalTRMM

        #print len(dDate)
        ##print len(dSpanish)
        #print len(dTRMM)
        pnt = kml.newpoint(name=station.fileName)
        #pnt.coords = [(nearLon, nearLat)]
        pnt.coords = [(station.lon, station.lat)]
        #comp = compareList(dSpanish, dTRMM)
        comp = compareListDistance(dSpanish, dTRMM, isMeaned)

        if not overLap < splitLength:
            print "Error: " , comp
            errorArray.append(comp);
        # TRMM overestimates
        if comp > 0:
            pnt.style.labelstyle.color = simplekml.Color.red
        # TRMM underestimates
        elif comp < 0 :
            pnt.style.labelstyle.color = simplekml.Color.blue
        # right in a way
        else:
            pnt.style.labelstyle.color = simplekml.Color.yellow

        #pnt.style.balloonstyle.text = "difference is:" + str(comp) + "/" + str(len(dSpanish))
        pnt.style.balloonstyle.text = "(negative,blue is underestimate) difference is:" + str(comp)

        # graph
        fig = plt.figure()        ###
        if plotType == 0:
            plt.scatter(dDate, dSpanish, c= "blue")
            plt.scatter(dDate, dTRMM, c="red")
            plt.ylim(ymin=0)
        elif plotType == 1:
            plt.plot(dDate, dSpanish, c= "blue")
            plt.plot(dDate, dTRMM, c="red")
            plt.ylim(ymin=0)

        elif plotType == 2:
            try:
                pMax = max(max(dSpanish), max(dTRMM))
                plt.plot([0,pMax], [0,pMax], c="red")
            except:
                print "hi"

            plt.xlabel('dTRMM')
            plt.ylabel('dSpanish')
            plt.scatter(dTRMM, dSpanish, c= "blue")
        elif plotType == 3:
            print "ha"
            #if not isMeaned:
             #   plotAOverB(dTRMM, dSpanish, False,"blue", "na")

        elif plotType == 4:
            plt.scatter(dTRMM, dSpanish, c= "blue")
            lims = [0,20]
            plt.xlim(lims)
            plt.ylim(lims)

        elif plotType == 5:

            plt.xlabel('1st X')
            plt.ylabel('1st Y')
            plt.scatter(dDate, dSpanish, c= "blue")
            plt.ylim(ymin=0)

            plt.twinx()
            plt.ylabel('2nd Y')
            plt.twiny()
            plt.xlabel('2nd X')
            plt.scatter(dTRMM, dDate, c="red")
            plt.xlim(xmin=0)

        #ax1 = fig.add_subplot(111)

        #ax1.set_ylabel('y1')
        #ax2.set_ylabel('y2', color='r')
        #for tl in ax2.get_yticklabels():
         #   tl.set_color('r')



        ##
        fig.suptitle(station.fileName, fontsize=20)#
        plt.show()
        #plt.show(block=False)


    else:
        print "No OverLap in" , station.fileName
        # calculate annual ?

    iStation+=1
# plots for total check in excel
if plotType == 333:

    cPath = hostPath + "divid_correlation_Spanish_TRMM_" + str(splitLength) + ".csv"
    for f in range(0, len(totalSpanish)):
          if totalSpanish[f] == 0:
              totalSpanish[f] = 0.00001

    fdiv = [float(ai)/bi for ai,bi in zip(totalTRMM,totalSpanish)]
    stuff = zip(totalSpanish,fdiv)

    with open(cPath, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(stuff)


# power curve not working
if plotType == 3:
    fig = plt.figure()


    if bySeason:
        popt, pcov, r_squared = plotAOverB(totalTRMM, totalSpanish, True, "blue", "dry")
        popt2, pcov2, r_squared2 = plotAOverB(totalTRMM2, totalSpanish2, True, "red", "wet")
    else:

        #if isClark:
         #   totalSpanish.extend(clarkRain)
          #  totalTRMM.extend(clarkTRMM)

        if isAllThree:
            totalSpanish.extend(clarkRain)
            totalTRMM.extend(clarkTRMM)
            popt, pcov, r_squared = plotAOverB(totalTRMM, totalSpanish, True, "blue", "data")

        else:
            #popt, pcov, r_squared = plotAOverB(totalTRMM[:12], totalSpanish[:12], True, "blue", "data") # this is fit without atrium
            popt, pcov, r_squared = plotAOverB(totalTRMM, totalSpanish, True, "blue", "data") # this is fit with atrium

            if isClark:
                # add clark data
                cDiv = [float(ai)/bi for ai,bi in zip(clarkTRMM, clarkRain)]
                #clarkRain = [float(f/1000) for f in clarkRain]
                plt.scatter(clarkRain, cDiv ,c= "red", label="Clark")
                plt.ylim([0,7])

            if isAtrium:
                # USE -4 or -3:
                # -3: when it is used as fit

                aDiv = [float(ai)/bi for ai,bi in zip(totalTRMM[-3:], totalSpanish[-3:])]
                plt.scatter(totalSpanish[-3:], aDiv ,c= "green", label="Atrium")
                #popt, pcov, r_squared = plotAOverB(totalTRMM, totalSpanish, True, "green", "atrium")


 ####################################################
    pre = ""
    if isMeaned:
        pre = "isMeaned " + str(splitLength) + "-"
    if bySeason:
        pre+= "bySeason - Dry: "
    title = pre + "y=" + str(popt[0]) + " x^(" + str(popt[1]) + ")" + "\n      Rsqrt: " + str(r_squared)
    if bySeason:
        title +=  "\n Wet: y=" + str(popt2[0]) + " x^(" + str(popt2[1]) + ")" +          "\n      Rsqrt: " + str(r_squared2)

    fig.suptitle( title, fontsize=20)
    plt.xlabel('totalSpanish(m)')
    plt.ylabel("totalTRMM/totalSpanish")
    plt.legend(loc='upper right')
    plt.show()

if plotElevation and isMeaned:

    fig = plt.figure()
    plt.scatter(totalSpanish,elevationArray, c= "blue")
    plt.xlabel('totalSpanish')
    plt.ylabel("elevation (m)")
    title = "mean " + str(splitLength) + "- vs elevation "
    fig.suptitle( title, fontsize=20)
    plt.show()

    #fig = plt.figure()
    #fdiv = [float(ai)/bi for ai,bi in zip(totalTRMM,totalSpanish)]
    #plt.scatter(fdiv,elevationArray, c= "blue")
    #plt.xlabel('fdiv')
    #plt.ylabel("elevation (mm)")
    #title = "mean " + str(splitLength) + "- vs elevation vs fdiv"
    #fig.suptitle( title, fontsize=20)
    #plt.show()


    #fig = plt.figure()
    #fdiv = [float(ai)/bi for ai,bi in zip(totalTRMM,totalSpanish)]
    #plt.scatter(errorArray,elevationArray, c= "blue")
    ##plt.xlabel('errorArray')
    #plt.ylabel("elevation (m)")
    #title = "mean " + str(splitLength) + "- vs elevation vs error"
    #fig.suptitle( title, fontsize=20)
    #plt.show()


kml.save(kmlName)






