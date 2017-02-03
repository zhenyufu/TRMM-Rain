import glob
import csv
import pickle
import netCDF4
import numpy as np
import datetime
import tables as tb

def strToNum(tempList):
    print tempList.shape
    a = np.zeros(shape=(tempList.shape))
    print a
    position = 0
    for i in np.nditer(tempList):
        try:
            x = i.astype(np.float)
        except:
            x = -1
        if x < 0:
            x = -1
        a[position] = x
        position += 1
    return a
def monthToNum(month):
    x = 0
    if month == "Ene":
        x = 1
    elif month == "Feb":
        x = 2
    elif month == "Mar":
        x = 3
    elif month == "Abr":
        x = 4
    elif month == "May":
        x = 5
    elif month == "Jun":
        x = 6
    elif month == "Jul":
        x = 7
    elif month == "Ago":
        x = 8
    elif month == "Sep":
        x = 9
    elif month == "Oct":
        x = 10
    elif month == "Nov":
        x = 11
    elif month == "Dic":
        x = 12
    else:
        x = -1
    return x


# have a list of date and a np array of the precipitation
class StationData:
    def __init__(self, tempArray, fileName):
        self.fileName = fileName
        self.mapId = "NA"
        self.startDate = "NA"
        self.endDate = "NA"

        self.lat = 0
        self.lon = 0

        self.rowNum = tempArray.shape[0]
        self.colNum = 1 # 1 for the data
        self.isRain = False # be true for the stations with only one rain column
        # self.listPrep = np.array([], dtype=np.float64)


        ##### precipitation
        # tempRow, tempCol = tempArray.shape
        tempCol = tempArray.shape[1]
        print fileName
        print tempCol
        if tempCol == 13:
            self.listPrep = np.add(strToNum(tempArray[:,9]), strToNum(tempArray[:,10]))
        elif tempCol == 9:
            self.isRain = True
            self.listPrep = strToNum(tempArray[:,5])
        elif tempCol ==3:
            self.listPrep = np.add(strToNum(tempArray[:,1]), strToNum(tempArray[:,2]))
        else:
            print "data format wrong"


        ##### precipitation
        # self.dataList = [[l[i] for i in selectCol] for l in tempList]
        self.listDate = [] # np.zeros(shape=(self.rowNum, 3), dtype='int') # 3 for day month year
        for s in np.nditer(tempArray[:,0]):
            s = s.tostring()
            temp = s.split("-")

            # day
            d = int(temp[0])
            # month
            m = monthToNum(temp[1])
            # year
            y = int(temp[2])
            #

            date = datetime.date(y,m,d)
            self.listDate.append(date)






def readSpanish(path):
    dataArray = []
    print "read from " + path
    print "*************************"
    temp =  sorted(glob.glob(path + "*.csv"))
    for p in temp:
        f = open(p, 'rb')
        c = csv.reader(f, delimiter=',')
        c = list(c) # pass in a list
        c = np.asarray(c)
        stationData = StationData(c,p)
        dataArray.append(stationData)
    return dataArray




def readTRMM(path):
    print "read from " + path
    print "*************************"
    return netCDF4.Dataset(path,'r')




def pickleSave(thing,path):
    out = open(path, 'wb')
    pickle.dump(thing, out, pickle.HIGHEST_PROTOCOL)

