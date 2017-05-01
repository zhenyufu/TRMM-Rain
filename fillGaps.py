from rain import *
# fill the gaps for dataSpanish and Atrium datasets

dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
yearLength = 2016 - 1998
myBar = 180 * 0.1  # seasonal ~ 18

f = open('_data/dataSpanish_0.8.2', 'rb')
dataSpanish = pickle.load(f)

# got all the data
for station in dataSpanish:
    print station.fileName
    print station.lat , ",", station.lon
    print station.dateList[0] , "to", station.dateList[-1]
    dayCounter = station.dateList[0]
    dayEnd = station.dateList[-1]
    while dayCounter != dayEnd:
        try:
            iSpanish = station.dateList.index(dayCounter)
        except:
            # fix the missing
            missing1 = dayCounter - datetime.timedelta(days=1)

            while True:
                try:
                    iSpanish = station.dateList.index(dayCounter)
                    break
                except:
                    dayCounter += datetime.timedelta(days=1)
                    if dayCounter == dayEnd:
                        break
                    pass
            # comes out of the continuous missing days
            missing2 = dayCounter
            missed = (missing2 - missing1).days
            if missed > 18:
                break
            print "Missing" , missed ,"between points:", missing1 ,"-" , missing2
            # calculate and loop through to put them back
            i1 = station.dateList.index(missing1)
            i2 = station.dateList.index(missing2)

            prep1 = station.listPrep[i1]
            prep2 = station.listPrep[i2]

            avg = (prep1 + prep2)/2
            print "avg" , avg


            # catch if missing2 is the last day
            if dayCounter == dayEnd:
                break
        dayCounter += datetime.timedelta(days=1)



