import glob
import csv

def readSpanish(path):
    print "read from " + path
    temp =  glob.glob(path + "*.csv")
    for p in temp:
        print p
        with open(p, 'rb') as f:
            c = csv.reader(f, delimiter=',')

    return 1

