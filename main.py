from rain import *



print "MAIN: This is the main script"




print "reading spanish data"
f = open('_data/dataSpanish_0.1', 'rb')
dataSpanish = pickle.load(f)
for data in dataSpanish:
    print data.fileName
    print data.lat , ",", data.lon
    print data.dateList[0] , "to", data.dateList[-1]




print "reading TRMM data"
dataTRMM = readTRMM("../TRMM_3B42_Daily_precipitation.7.SouthAmerica.nc")


#TRMM date fixi
TRMMDateList = []
TRMMDate = datetime.date(1998,1,1)

for i in range(0, 6878):
     TRMMDateList.append(TRMMDate)
     TRMMDate += datetime.timedelta(days=1)

print TRMMDateList[0], "to", TRMMDateList[-1]

###############################################
for station in dataSpanish:
    nearLat = 0
    nearLon = 0
    allLat = dataTRMM.variables['lat'][:]
    allLon = dataTRMM.variables['lon'][:]


    nearLat = takeClosest(allLat, station.lat)
    nearLon = takeClosest(allLon, station.lon)

    # get time range

    overLap , lapStart, lapEnd = getOverlap(TRMMDateList[0], TRMMDateList[-1], station.dateList[0], station.dateList[-1])
    if overLap > 0:
        # strange stuff
        if station.fileName == "raw_senamhi/madre5.csv":
            lapEnd = datetime.date(2016,10,6)

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
        dDate = []
        dSpanish = []
        dTRMM = []
        dayCounter = lapStart
        plt.ion()# turns on interactive mode to enable plotting more
        for i in range(0, overLap+1):
            # print dayCounter
            try:
                # get index
                iSpanish = station.dateList.index(dayCounter)
                iTRMM = TRMMDateList.index(dayCounter)
            except:
                # this date is not in one of the two lists
                continue

            # get the prep only if the station is not -1
            p = station.listPrep[iSpanish]
            if p >= 0:
                dDate.append(dayCounter)
                dSpanish.append(p)
                dTRMM.append(dataTRMM.variables['precipitation'][iTRMM,nearLat,nearLon])

            # at the end
            dayCounter += datetime.timedelta(days=1)



        # divide conresponding to each day !!
        print len(dDate)
        print len(dSpanish)
        print len(dTRMM)
        #dPlot = [float(ai)/bi for ai,bi in zip(dSpanish,dTRMM)]
        #print dPlot

        # graph
        fig = plt.figure()
        plotType = 1
        # 0 doulbe scatter
        # 1 double line
        # 2 correlation
        # 3 time shift correlation
        # 4 differnt x y

        ###
        if plotType == 0:
            plt.scatter(dDate, dSpanish, c= "blue")
            plt.scatter(dDate, dTRMM, c="red")
            plt.ylim(ymin=0)
        elif plotType == 1:
             plt.plot(dDate, dSpanish, c= "blue")
             plt.plot(dDate, dTRMM, c="red")
             plt.ylim(ymin=0)

        elif plotType == 2:
            plt.scatter(dTRMM, dSpanish, c= "blue")
        elif plotType == 3:

        elif plotType == 4:

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



        ###
        plt.show()
        #plt.show(block=False)


    else:
        print "No OverLap in" , station.fileName


















