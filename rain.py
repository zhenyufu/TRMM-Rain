import glob
import csv
import pickle
import netCDF4
import numpy as np

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

class StationData:
    def __init__(self, tempArray, fileName):
        self.fileName = "NA"
        self.mapId = "NA"
        self.startDate = "NA"
        self.endDate = "NA"

        self.lat = 0
        self.lon = 0

        self.rowNum = 0
        self.colNum = 4 # should be 4: day, month, year, perp
        self.isRain = False # be true for the stations with only one rain column
        # self.dataList = []



        ###
        self.fileName = fileName
        # tempRow, tempCol = tempArray.shape
        tempCol = tempArray.shape[1]
        print fileName
        print tempCol
        if tempCol == 13:
            tempArray[:,1] = np.add(strToNum(tempArray[:,9]), strToNum(tempArray[:,10]))
            #print type(strToNum(tempArray[5,9]))
        elif tempCol == 9:
            self.isRain = True
            tempArray[:,1] = strToNum(tempArray[:,5])
        elif tempCol ==3:
            tempArray[:,1] = np.add(strToNum(tempArray[:,1]), strToNum(tempArray[:,2]))


        else:
            print "data format wrong"

        # self.dataList = [[l[i] for i in selectCol] for l in tempList]
        self.dataArray = tempArray[:,[0,1]]

        self.rowNum, self.colNum = (self.dataArray).shape
        #self.startDate = self.dataList[0][0]
        #self.endDate = self.dataList[self.rowNum-1][0]






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





