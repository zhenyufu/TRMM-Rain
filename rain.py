import glob
import csv

dataArray = []

class StationData:
    def __init__(self, temp, fileName):
        self.fileName = "NA"
        self.startDate = "NA"
        self.endDate = "NA"
        self.rowNum = 0
        self.colNum = 0 # should be 3: time, 07, 19
        self.isRain = False # be true for the stations with only rain
        self.dataList = []

        ###
        self.fileName = fileName
        # tempRow = len(temp)
        tempCol = len(temp[0])
        selectCol = []

        if tempCol == 13:
            selectCol = [0,10,11]
        elif tempCol == 9:
            selectCol = [0,6,6]
            self.isRain = True
        elif tempCol ==3:
            selectCol = [0,1,2]
        else:
            print "data format wrong"

        self.dataList = [[l[i] for i in selectCol] for l in temp]
        self.rowNum = len(self.dataList)
        self.colNum = len(self.dataList[0])
        self.startDate = self.dataList[0][0]
        self.endDate = self.dataList[self.rowNum-1][0]



def readSpanish(path):
    # dataArray = []
    print "read from " + path
    print "*************************"
    temp =  glob.glob(path + "*.csv")
    for p in temp:
        f = open(p, 'rb')
        c = csv.reader(f, delimiter=',')
        c = list(c) # pass in a list
        stationData = StationData(c,p)
        dataArray.append(stationData)
    return dataArray





