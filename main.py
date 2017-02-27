from rain import *



print "MAIN: This is the main script"
hostPath = "/media/sf_myshareDebianMain/"
splitLength = 90
# 1 is by day
# 30
# 365
isMeaned = True
bySeason = False # use only with isMeaned set to True
# Wet: 11-4
# dry: 5-10


plotType = 3
# 0 doulbe scatter with time
# 1 double line with time
# 2 correlation
# 3 ratio over weather station

# 4 correlation with range
# 5 differnt x  - not working yet
kml = simplekml.Kml()
kmlName = hostPath + "comparison_Spanish_TRMM_" + str(splitLength) + ".kml"


###########################################################
print "reading spanish data"
f = open('_data/dataSpanish_0.1', 'rb')
dataSpanish = pickle.load(f)
for data in dataSpanish:
    print data.fileName
    print data.lat , ",", data.lon
    print data.dateList[0] , "to", data.dateList[-1]




print "reading TRMM data"
#dataTRMM = readTRMM("../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc")
dataTRMM = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")



#TRMM date fixi
TRMMDateList = []
TRMMDate = datetime.date(1998,1,1)

for i in range(0, 6878):
     TRMMDateList.append(TRMMDate)
     TRMMDate += datetime.timedelta(days=1)

print TRMMDateList[0], "to", TRMMDateList[-1]

totalSpanish = []
totalTRMM = []
totalSpanish2 = []
totalTRMM2 = []

##############################################
for station in dataSpanish:
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

    overLap , lapStart, lapEnd = getOverlap(TRMMDateList[0], TRMMDateList[-1], station.dateList[0], station.dateList[-1])
    if overLap > 0:
        # strange stuff
        if station.fileName == "raw_senamhi/madre5.csv":
            lapEnd = datetime.date(2016,10,6)
            overLap = (lapEnd - lapStart).days
        print "days: ", overLap
        print lapStart, "to", lapEnd

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


        while( dayCounter <= lapEnd):
            # for everyday in slpitLength
            # print dayCounter
            cumuDay = dayCounter
            # 1 is dry, 2 is wet
            cumuSpanish = 0
            cumuTRMM = 0
            cumuSpanish2 = 0
            cumuTRMM2 = 0
            seasonIsDry = isDrySeason(dayCounter.month) # -1 # true for dry, false for wet

            if bySeason:
                while isDrySeason(dayCounter.month) ==  seasonIsDry:


                    try:
                        iSpanish = station.dateList.index(dayCounter)
                        iTRMM = TRMMDateList.index(dayCounter)
                    except:
                        dayCounter += datetime.timedelta(days=1)
                        continue
                    p = station.listPrep[iSpanish]
                    if p >= 0:
                        addSpanish = p
                        addTRMM = dataTRMM.variables['precipitation'][iTRMM,iLon,iLat]

                    if isDrySeason(dayCounter.month):
                        cumuSpanish += addSpanish
                        cumuTRMM += addTRMM
                    else:
                        cumuSpanish2 += addSpanish
                        cumuTRMM2 += addTRMM

                    dayCounter += datetime.timedelta(days=1)
                dSpanish.append(cumuSpanish)
                dTRMM.append(cumuTRMM)
                dSpanish2.append(cumuSpanish2)
                dTRMM2.append(cumuTRMM2)

                seasonIsDry = isDrySeason(dayCounter.month)
                continue

            # else ##################
            for i in range(0, splitLength):
                if (dayCounter > lapEnd):
                    dataDone = True
                    break;
                meanCount +=1
                # print dayCounter
                try:
                    # get index
                    iSpanish = station.dateList.index(dayCounter)
                    iTRMM = TRMMDateList.index(dayCounter)
                    #if station.fileName == "raw_senamhi/madre5.csv":
                    #    print dayCounter, "and", overLap
                except:
                    # this date is not in one of the two lists
                    dayCounter += datetime.timedelta(days=1)
                    continue

                # get the prep only if the station is not -1
                p = station.listPrep[iSpanish]
                if p >= 0:
                    cumuSpanish += p
                    cumuTRMM += dataTRMM.variables['precipitation'][iTRMM,iLon,iLat]
                dayCounter += datetime.timedelta(days=1)
            if (dataDone):
                break;
            # end for i in range(0, splitLength):
            dDate.append(cumuDay)
            dSpanish.append(cumuSpanish)
            #dTRMM.append(dataTRMM.variables['precipitation'][iTRMM,nearLon,nearLat])
            dTRMM.append(cumuTRMM)

        # end of while( dayCounter <= lapEnd):

        print "Mean by", meanCount
        if isMeaned:
            dSpanish = np.mean(dSpanish)
            dTRMM = np.mean(dTRMM)
            totalSpanish.append(dSpanish)
            totalTRMM.append(dTRMM)

            if bySeason:
                dSpanish2 = np.mean(dSpanish2)
                dTRMM2 = np.mean(dTRMM2)
                totalSpanish2.append(dSpanish2)
                totalTRMM2.append(dTRMM2)
                print totalTRMM2
        else:
            totalSpanish.extend(dSpanish)
            totalTRMM.extend(dTRMM)


        #print len(dDate)
        ##print len(dSpanish)
        #print len(dTRMM)
        pnt = kml.newpoint(name=station.fileName)
        #pnt.coords = [(nearLon, nearLat)]
        pnt.coords = [(station.lon, station.lat)]
        #comp = compareList(dSpanish, dTRMM)
        comp = compareListDistance(dSpanish, dTRMM, isMeaned)
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
            if not isMeaned:
                plotAOverB(dTRMM, dSpanish, False)

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

    popt,r_squared = plotAOverB(totalTRMM, totalSpanish, True, "blue", "dry")
    if bySeason:
        popt2,r_squared2 = plotAOverB(totalTRMM2, totalSpanish2, True, "red", "wet")
 ####################################################
    pre = ""
    if isMeaned:
        pre = "isMeaned - "
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


kml.save(kmlName)






