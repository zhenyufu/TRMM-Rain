import glob
import csv

def readSpanish(path):
    dataArray = []
    print "read from " + path
    temp =  glob.glob(path + "*.csv")
    for p in temp:
        print p
        f = open(p, 'rb')
        c = csv.reader(f, delimiter=',')
        dataArray.append(c)
    return dataArray

