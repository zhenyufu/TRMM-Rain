import glob
import csv
import pickle
import netCDF4
import numpy as np
import datetime
import matplotlib.pyplot as plt
# import tables as tb
from bisect import bisect_left
import simplekml
from pylab import *
from scipy.optimize import curve_fit
import math as Math

hostPath = "/media/sf_myshareDebianMain/"

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
        self.elevation = 0

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
        self.dateList = [] # np.zeros(shape=(self.rowNum, 3), dtype='int') # 3 for day month year
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
            self.dateList.append(date)






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





def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0], pos
    if pos == len(myList):
        return myList[-1], pos
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after, pos
    else:
       return before, pos-1


def getOverlap(A_start, A_end, B_start, B_end):
    latest_start = max(A_start, B_start)
    earliest_end = min(A_end, B_end)
    return (earliest_end-latest_start).days, latest_start, earliest_end,





def compareListDistance(dSpanish, dTRMM, isMeaned):
    try:
        pMax = max(max(dSpanish), max(dTRMM))
        plt.plot([0,pMax], [0,pMax], c="red")
    except:
        print "hi"
    listLength = 0
    total = 0
    if isMeaned:
        listLength = 1
        x = dTRMM
        y = dSpanish
        d = pointLineDistance(x, y, 0, 0, x, y)
             # print "d" , d
             # negative - underestimate - if above the line
        if x < y:
            d = -d
            total=d

    else:
        listLength = len(dSpanish)
        for i in range(0,listLength):
            x = dTRMM[i]
            y = dSpanish[i]
            d = pointLineDistance(x, y, 0, 0, pMax, pMax)
            # print "d" , d
            # negative - underestimate - if above the line
            if x < y:
                d = -d
            total+=d
    return total




def compareList(dSpanish, dTRMM):
    listLength = len(dSpanish)
    biggerTRMM = 0
    for i in range(0,listLength):
        if dSpanish[i] <  dTRMM[i]:
            biggerTRMM += 1
        else:
            biggerTRMM -= 1
    return biggerTRMM


def curveExpo(x, a, b, c):
    return a*np.exp(b*x)+c

def curvePower(x,a,b):
    #return a*np.power(x, -b)
    return a*x**(b)

def plotAOverB(totalTRMM, totalSpanish ,drawCurve, col, lab):
    smallNum = 0.1
    delList = set() # fucking set !!
    for f in range(0, len(totalSpanish)):
        if totalSpanish[f] < smallNum or Math.isnan( totalSpanish[f]):
            delList.add(f)
    for f in range(0, len(totalTRMM)):
        if totalTRMM[f] < smallNum or Math.isnan( totalSpanish[f]):
            delList.add(f)

    for i in sorted(delList, reverse=True):
        print "deleting:" , i
        del totalSpanish[i]
        del totalTRMM[i]

    fdiv = [float(ai)/bi for ai,bi in zip(totalTRMM,totalSpanish)]


    totalSpanish = [float(f/1000) for f in totalSpanish]

    plt.scatter(totalSpanish, fdiv ,c= col, label=lab)

    #popt, pcov = curve_fit(curvePower, totalSpanish, fdiv,p0=(1, -0.87))
    popt, pcov = curve_fit(curvePower, totalSpanish, fdiv, p0 = (0.8, -0.8))
    print "plotting stuff:"
    print "x-totalSpanish:", totalSpanish
    print "y-fdiv:" , fdiv
    print popt
    print pcov
    xx = np.linspace(0.1, max(totalSpanish), 100)
    yy = curvePower(xx, *popt)
    plt.plot(xx,yy, c=col)
    #plot(totalSpanish, curvePower(totalSpanish, *popt), 'r-', label='Fit')
    # calculate R squared
    residuals = fdiv- curvePower(totalSpanish, popt[0], popt[1])
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((fdiv-np.mean(fdiv))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return popt, r_squared




def pointLineDistance(x, y, x1, y1, x2, y2):
    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = -1
    if (len_sq != 0):
        param = dot

    xx = 0
    yy = 0

    if (param < 0):
        xx = x1
        yy = y1

    elif (param > 1):
        xx = x2
        yy = y2

    else:
        xx = x1 + param * C
        yy = y1 + param * D


    dx = x - xx
    dy = y - yy
    sq = Math.sqrt(dx * dx + dy * dy)
    return sq

def isDrySeason(month):
    if month >= 5 and  month <= 10:
        return 1#True
    else:
        return 2#False

    #if month >= 5 and  month <= 9:
    #    return 1
    #elif month <= 3 or month == 12 :
    #    return 2

    #return -1

def getRainOnDay(d):
    print "l"
